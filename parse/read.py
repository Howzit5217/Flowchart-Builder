"""The whole program, read into blocks: branches, loops and all."""
import re

from .. import settings
from ..parse.clean import join_lines, tidy, unwrap
from ..parse.nodes import For, If, Loop, Module, Node, Select
from ..parse.keywords import (
    R_CASE, R_CLOSER, R_DECL, R_DO, R_ELSE, R_ELSEIF, R_ELSE_INLINE, R_END,
    R_ENDANY, R_ENDIF, R_ENDLOOP, R_ENDMOD, R_ENDSEL, R_FOR, R_IF, R_LOOPCOND,
    R_MODULE, R_OUT, R_REPEAT, R_SELECT, R_THEN, R_UNTIL, R_WHILE)
from ..parse.statements import (
    Chart, Frame, ends_flow, make_module, parse_for, simple_node,
    split_outside_quotes, strip_then)
from ..parse.trouble import OPEN_TROUBLE, PROBLEMS, trouble
from ..words.lookup import word


def parse_program(text):
    """Pseudocode text -> [Chart, ...] with the main chart first."""
    del PROBLEMS[:]
    lines = join_lines(text.splitlines())
    top, modules, declares, outs = [], [], [], []
    at_declares, at_outs = [], []       # and the line each of them came from
    counted, here = [0], [0]            # statement numbers, and where we are
    run_at = [0]                        # where the run being gathered began
    stack = [Frame(None, top, -1)]
    # No "End If" / "End While" anywhere but the lines are indented?  Then
    # indentation closes the blocks, Python style.
    indent_mode = (any(ind > 0 for ind, _, _ in lines)
                   and not any(R_CLOSER.match(tidy(t)) for _, t, _ in lines))

    def cur():
        return stack[-1]

    def flush():
        """Empty whichever run of same-kind statements is still open.

        Declares pile into one box, and so does a run of Displays: the four
        lines of a menu are one thing the program says, and four separate
        parallelograms for them make the chart taller without telling the
        reader anything the one symbol does not.  A run only ever holds one
        kind, because whichever kind comes next flushes the other first, and
        it is capped at settings.GROUP_MAX lines so a long stretch of output does not
        grow into one enormous symbol."""
        if declares:
            box = Node("rect", "\n".join(declares))
            box.line = run_at[0]
            box.lines = list(at_declares)
            cur().items.append(stamp(box))
            del declares[:]
            del at_declares[:]
        if outs:
            box = Node("io", "\n".join(outs))
            box.line = run_at[0]
            box.lines = list(at_outs)
            cur().items.append(stamp(box))
            del outs[:]
            del at_outs[:]

    def add(item):
        cur().items.append(stamp(item))

    def stamp(item, at=None):
        """Give a statement its number, and the line it was typed on.

        A number every statement has and no two share is what lets the
        drawing and the data agree about which shape is which -- and so what
        lets the runner light up the shape it is on and point at the line it
        came from.  `at` is for the shapes nobody typed: the Start and End
        the reading adds itself, which belong to no line at all and say so
        with a nought, rather than borrowing whichever line was read last."""
        counted[0] += 1
        item.node_id = counted[0]
        if at is not None:
            item.line = at
        elif not getattr(item, "line", 0):
            item.line = here[0]
        return item

    def find(test):
        """Index of the innermost open frame whose owner passes test, or -1."""
        for i in range(len(stack) - 1, 0, -1):
            if test(stack[i].owner):
                return i
        return -1

    def close(test, cond=None, until=None):
        """Close the innermost matching structure, plus anything left open inside it."""
        i = find(test)
        if i < 0:
            return False
        owner = stack[i].owner
        if cond is not None:
            owner.cond = cond
        if until is not None:
            owner.until = until
        del stack[i:]
        while isinstance(owner, If) and owner.chained and isinstance(cur().owner, If):
            owner = cur().owner                    # End If closes the whole Else-If chain
            stack.pop()
        return True

    def closer_for(owner):
        """The line that would close this block, where it is obvious.

        A Do and a Repeat get none: what closes them is Until <test> or
        Loop While <test>, and the test is the author's to write.  Offering
        to put in an Until with nothing after it would turn a loop that
        never stops into a program that does not read.
        """
        kind = getattr(owner, "kind", "")
        if kind == "if":
            return "End If"
        if kind == "for":
            return "End For"
        if kind == "select":
            return "End Select"
        if kind == "loop" and owner.style == "pre":
            return "End While"
        return ""

    def shuts_before(frame):
        """The line the missing closer was probably meant to go in front of.

        The indentation is what knows.  Somebody who indents the body of an
        If and then steps back out has said where the If ends as plainly as
        End If would have; the reading simply was not looking.  So the
        closer goes in front of the first line that steps back to the If's
        own level, and 0 -- no fix offered -- where nothing was indented
        under it at all, because then there is nothing to go on and a guess
        would put End If directly under the If, which is not what anybody
        meant by leaving it out.
        """
        own = frame.indent
        started, last, last_s = False, 0, ""
        for indent, raw, line_no in lines:
            if line_no <= getattr(frame.owner, "line", 0):
                continue
            s = tidy(raw)
            if not s:
                continue
            if indent > own:
                started = True
            elif not (R_ELSE.match(s) or R_ELSEIF.match(s) or R_CASE.match(s)):
                return line_no if started else 0
            last, last_s = line_no, s
        if not started:
            return 0
        # Nothing below it steps back out, so it runs to the foot of the
        # program -- in front of the End that finishes it, where there is
        # one, rather than underneath it.
        if R_END.match(last_s) or R_ENDMOD.match(last_s):
            return last
        return last + 1

    def still_open():
        """Blocks left standing open, which is hardly ever what was meant.

        Only where End If and its like are being used at all: under
        indentation the blocks close as the lines step back out, so by here
        there is nothing open that was not closed exactly as it should be."""
        if indent_mode:
            return
        for frame in stack[1:]:
            key = OPEN_TROUBLE.get(getattr(frame.owner, "kind", ""), "")
            if key:
                at = getattr(frame.owner, "line", 0)
                shut = closer_for(frame.owner)
                goes = shuts_before(frame) if shut else 0
                trouble(key, at, fix={"how": "insert", "text": shut,
                                      "at": goes, "like": at} if goes else None)

    def is_if(o):
        return isinstance(o, If)

    def is_loop(o):
        return isinstance(o, (Loop, For))

    def is_post(o):
        return isinstance(o, Loop) and o.style == "post" and not o.cond

    def is_sel(o):
        return isinstance(o, Select)

    def is_any(o):
        return not isinstance(o, Module)

    def while_closes_do(idx):
        """Inside a Do: is this 'While cond' the end of the Do, or a nested
        loop?  Scan ahead: a nested While owns the next unmatched End While."""
        depth = bare = 0
        for _, t, _no in lines[idx + 1:]:
            k = tidy(t).lower()
            if R_MODULE.match(k) or R_ENDMOD.match(k):
                break
            if re.match(r"^(do|repeat)$", k):
                bare += 1
            elif re.match(r"^(until\s|loop\s+(while|until)\s)", k):
                bare = max(0, bare - 1)
            elif re.match(r"^while\b", k):
                if bare:
                    bare -= 1                      # closes a later Do
                else:
                    depth += 1
            elif re.match(r"^do\s+(while|until)\b", k):
                depth += 1
            elif re.match(r"^(end[ -]?(while|loop|do)|endwhile|wend|loop)$", k):
                if depth == 0:
                    return False                   # that End While is ours
                depth -= 1
        return True

    for idx, (indent, raw, at_line) in enumerate(lines):
        here[0] = at_line
        s = tidy(raw)
        if not s:
            if outs:
                flush()       # a blank line between two Displays keeps them
            continue          #   apart: the spacing is the author's to set

        if indent_mode and len(stack) > 1 and indent <= cur().indent \
                and not (R_ELSE.match(s) or R_ELSEIF.match(s) or R_CASE.match(s)):
            flush()                                # dedent: close open blocks
            while len(stack) > 1 and indent <= cur().indent:
                stack.pop()

        if R_DECL.match(s):                        # declarations: one shared box
            if outs:
                flush()
            if not declares:
                run_at[0] = at_line
            declares.append(s)
            at_declares.append(at_line)
            continue
        if settings.GROUP_OUTPUT and R_OUT.match(s) and not R_CLOSER.match(s):
            if declares or len(outs) >= settings.GROUP_MAX:  # a run of Displays shares
                flush()                             #   one symbol as well
            if not outs:
                run_at[0] = at_line
            outs.append(s)
            at_outs.append(at_line)
            continue
        flush()

        m = R_MODULE.match(s)
        if m:                                      # a new module closes everything
            still_open()
            del stack[1:]
            mod = make_module(m.group(1), m.group(2), s)
            mod.line = at_line
            modules.append(mod)
            stack.append(Frame(mod, mod.items, indent))
            continue
        if R_END.match(s):
            add(Node("oval", word("end"), terminal=True))
            continue
        if R_ENDMOD.match(s):
            del stack[1:]
            continue
        if R_ENDIF.match(s):
            if not close(is_if):
                trouble("w_no_if", at_line, s, {"how": "drop", "at": at_line})
            continue
        if R_ENDSEL.match(s):
            if not close(is_sel):
                trouble("w_no_select", at_line, s, {"how": "drop", "at": at_line})
            continue
        m = R_LOOPCOND.match(s)                    # Loop While c / Loop Until c
        if m:
            if not close(is_post, cond=unwrap(m.group(2)), until=m.group(1).lower() == "until"):
                close(is_loop)
            continue
        if R_ENDLOOP.match(s):
            shut = find(is_post)                   # a Do nobody ever tested
            if shut >= 0 and not stack[shut].owner.cond:
                trouble("w_do_no_test", stack[shut].owner.line)
            if not close(is_loop):
                trouble("w_no_loop", at_line, s, {"how": "drop", "at": at_line})
            continue
        m = R_UNTIL.match(s)
        if m:
            if not close(is_post, cond=unwrap(m.group(1)), until=True):
                trouble("w_until_alone", at_line, s)
                add(simple_node(s))
            continue
        if R_ENDANY.match(s):                      # some "End Xyz" we don't know
            close(is_any)
            continue

        m = R_ELSEIF.match(s)
        if m and find(is_if) >= 0:
            del stack[find(is_if) + 1:]
            node = If(unwrap(strip_then(m.group(2))))
            node.text = s
            node.chained = True
            # Numbered and dated like any other statement.  It used to be
            # neither, being the one statement that joins the tree without
            # passing through add() -- so every Else If in a program shared
            # the number nought, the runner could not light one up, Follow
            # along would not scroll to it, and an error in its test had no
            # line to point at.
            cur().owner.orelse.append(stamp(node))
            stack.append(Frame(node, node.then, cur().indent))
            continue
        if m:
            s = "If " + m.group(2)                 # stray Else If: treat as an If
        if R_ELSE.match(s):
            i = find(lambda o: isinstance(o, (If, Select)))
            if i >= 0:
                del stack[i + 1:]
                fr = cur()
                if isinstance(fr.owner, If):
                    fr.items = fr.owner.orelse
                else:
                    fr.owner.branches.append(["Else", []])
                    fr.items = fr.owner.branches[-1][1]
            continue
        m = R_SELECT.match(s)
        if m:
            node = Select(unwrap(m.group(2)))
            node.text = s
            add(node)
            stack.append(Frame(node, node.pre, indent))
            continue
        m = R_CASE.match(s)
        if m and find(is_sel) >= 0:
            del stack[find(is_sel) + 1:]
            fr = cur()
            fr.owner.branches.append([m.group(2) or "Default", []])
            fr.items = fr.owner.branches[-1][1]
            continue

        m = R_IF.match(s)
        if m:
            parts = R_THEN.split(m.group(1), 1)
            if len(parts) == 1:
                parts = split_outside_quotes(parts[0], ":")
            node = If(unwrap(parts[0]))
            node.text = s
            inline = parts[1].strip() if len(parts) > 1 else ""
            add(node)
            if inline:                             # If c Then stmt [Else stmt]
                halves = R_ELSE_INLINE.split(inline, 1)
                node.then.append(simple_node(halves[0]))
                if len(halves) > 1 and halves[1].strip():
                    node.orelse.append(simple_node(halves[1]))
            else:
                stack.append(Frame(node, node.then, indent))
            continue
        m = R_WHILE.match(s)
        if m:
            cond = unwrap(re.sub(r"\s+do$", "", m.group(1), flags=re.I))
            if find(is_post) >= 0 and while_closes_do(idx):
                close(is_post, cond=cond, until=False)
                continue
            node = Loop("pre", cond)
            node.text = s
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue
        m = R_DO.match(s)
        if m:
            if m.group(2):                         # Do While c / Do Until c ... Loop
                node = Loop("pre", unwrap(m.group(3)))
                node.until = m.group(2).lower() == "until"
            else:
                node = Loop("post")
            node.text = s
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue
        if R_REPEAT.match(s):
            node = Loop("post")
            node.text = s
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue
        m = R_FOR.match(s)
        if m:
            node = parse_for(m.group(1).strip(), s)
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue

        add(simple_node(s))

    flush()
    still_open()
    del stack[1:]

    # ----- one chart per module; globals and main() share the first chart
    main = next((mod for mod in modules if mod.name.lower() == "main"), None)
    names = set(mod.name.lower() for mod in modules)
    top = [it for it in top if not (isinstance(it, Node) and             # "main()"
           re.match(r"^\w+\(.*\)$", it.text) and it.text.split("(")[0].lower() in names)]
    # What is written outside every module is the program's own.  A Constant
    # at the top of the page is put there to be read from inside the modules
    # under it -- that is the whole reason for putting it there -- so the
    # statements that set it up are marked, and the runner keeps those names
    # apart from the ones each chart makes for itself.
    if modules:
        for item in top:
            if isinstance(item, Node):
                item.scope = "global"
    charts = []
    if main is not None:
        charts.append(Chart("Module main()", top + main.items, True, main))
    elif top or not modules:
        charts.append(Chart("main", top, True, None))
    for mod in modules:
        if mod is not main:
            heading = " ".join(w for w in (mod.kind.capitalize(), mod.rtype, mod.signature()) if w)
            charts.append(Chart(heading, mod.items, False, mod))

    for chart in charts:
        items = chart.items
        first = items[0] if items else None
        opens = (isinstance(first, Node) and first.shape == "oval"
                 and first.text == word("start"))
        if not opens:
            # A module's own name over its own door, main() as much as any
            # other.  The chart for a Module main() used to open on the word
            # Start while every chart beside it opened on its signature,
            # which says the two are different kinds of thing when they are
            # the same kind of thing -- and the oval pointed at the "Module
            # main()" line while saying something that line does not say, so
            # Follow along sent you to a line that did not match.  A program
            # written without modules still opens on Start: there is no
            # signature to put there.
            label = chart.module.signature() if chart.module else word("start")
            items.insert(0, stamp(Node("oval", label),
                                  chart.module.line if chart.module else 0))
        if not ends_flow(items):
            items.append(stamp(Node("oval", word("end") if chart.is_main
                                    else word("ret"), terminal=True), 0))
    return charts



