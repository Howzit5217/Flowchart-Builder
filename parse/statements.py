"""One line of pseudocode, turned into a shape."""
import re

from ..parse.clean import tidy
from ..parse.nodes import For, If, Loop, Module, Node, Select
from ..parse.keywords import (
    R_CALL, R_END, R_FOR_C, R_FOR_TO, R_IN, R_OUT, R_RETURN, R_START)
from ..words.lookup import word


def simple_node(s):
    """A plain statement (no If / loop / module keywords) -> Node."""
    s = tidy(s)
    if R_START.match(s):
        return Node("oval", word("start"))
    if R_END.match(s):
        return Node("oval", word("end"), terminal=True)
    if R_RETURN.match(s):
        return Node("oval", s, terminal=True)
    if R_CALL.match(s):
        return Node("sub", s)
    if R_OUT.match(s) or R_IN.match(s):
        return Node("io", s)
    return Node("rect", s)


def parse_for(rest, raw):
    """Turn the text after 'For' into a For (expandable) or a hexagon Loop."""
    m = R_FOR_TO.match(rest)
    if m:
        var, start, direction, end, step = m.groups()
        down = direction.lower() == "downto" or (step or "").strip().startswith("-")
        test = "%s %s %s" % (var, ">=" if down else "<=", end)
        if step:
            bump = "Set %s = %s + %s" % (var, var, step) if not down or not step.strip().startswith("-") \
                else "Set %s = %s - %s" % (var, var, step.strip()[1:].strip())
        else:
            bump = "Set %s = %s %s 1" % (var, var, "-" if down else "+")
        return For(raw, "Set %s = %s" % (var, start), test, bump)
    m = R_FOR_C.match(rest)
    if m:
        init, test, bump = (g.strip() for g in m.groups())
        return For(raw, init or None, test or "True", bump or None)
    loop = Loop("pre", raw)                          # For Each x In y, etc.
    loop.hex = True
    return loop


class Frame:
    """One open structure: what it is, the list statements go into, its indent."""

    def __init__(self, owner, items, indent):
        self.owner, self.items, self.indent = owner, items, indent


class Chart:
    """One flowchart: the heading drawn above it, and its top-level items."""

    def __init__(self, heading, items, is_main, module=None):
        self.heading, self.items, self.is_main, self.module = heading, items, is_main, module


# What a function hands back, said after the brackets instead of before the
# name: "As Real", "returns Real", "-> Real", ": Real".  Every textbook
# picks one, and this one only understood the type-in-front form.
R_GIVES_BACK = re.compile(
    r"\)\s*(?:as|returns?|->|:)\s+([\w\[\]]+)\s*$", re.I)


def make_module(kind, rest, header):
    """'Function Real calcTax(Real income)' -> Module(kind, name, params, header).

    The type can come before the name or after the brackets; both are read
    here.  Said after the brackets it used to be read as part of the name --
    there is no closing bracket at the end of the line for the pattern below
    to find, so it fell through to taking the last word.  "Function
    average(a, b) As Real" therefore came out as a module called Real that
    took nothing at all, and the code written from it defined Real() and
    then called average(): a program that will not run, from a chart that
    looked right.
    """
    rest = rest.strip().rstrip(":")
    after = R_GIVES_BACK.search(rest)
    given = ""
    if after:
        given = after.group(1)
        rest = rest[:after.start() + 1]      # back to the closing bracket
    m = re.match(r"^(?:([\w\[\]]+)\s+)?(\w+)\s*\((.*)\)$", rest)
    if m:
        rtype, name, params = m.group(1) or "", m.group(2), m.group(3).strip()
    else:
        words = rest.replace("(", " ").replace(")", " ").split()
        rtype, name, params = "", (words[-1] if words else rest), ""
    return Module(kind.lower(), name, params, header, given or rtype)


def split_outside_quotes(s, sep):
    """Split s at the first sep that is not inside quotes (at most 2 parts)."""
    quote = None
    for i, c in enumerate(s):
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == sep:
            return [s[:i], s[i + 1:]]
    return [s]


def strip_then(cond):
    return re.sub(r"\s+then$", "", cond.strip(), flags=re.I)


def ends_flow(items):
    """Does this statement list end in End / Return on every path?"""
    if not items:
        return False
    last = items[-1]
    if isinstance(last, Node):
        return last.terminal
    if isinstance(last, If):
        return ends_flow(last.then) and ends_flow(last.orelse)
    if isinstance(last, Select):
        return bool(last.branches) and all(ends_flow(b[1]) for b in last.branches)
    return False


