"""Tidying a line up, and gluing the continued ones together."""
import re


# ------------------------------------------------------------- line clean-up --
def strip_comment(s):
    """Drop // ... , # ... and /* ... */ comments (but not inside quotes)."""
    out, quote, i, n = [], None, 0, len(s)
    while i < n:
        c = s[i]
        if quote:
            out.append(c)
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            out.append(c)
        elif c == "#" or s.startswith("//", i):
            break
        elif s.startswith("/*", i):
            j = s.find("*/", i + 2)
            if j < 0:
                break
            i = j + 2
            continue
        else:
            out.append(c)
        i += 1
    return "".join(out)


def split_indent(raw):
    """Return (indent, text): leading '#' markers removed, comments stripped."""
    for smart, plain in (("\u201c", '"'), ("\u201d", '"'), ("\u201e", '"'),
                         ("\u2018", "'"), ("\u2019", "'"), ("\u00a0", " ")):
        raw = raw.replace(smart, plain)             # Word's curly quotes, etc.
    s = raw.expandtabs(4).rstrip()
    body = s.lstrip()
    indent = len(s) - len(body)
    while body.startswith("#"):
        body = body[1:]
        stripped = body.lstrip()
        indent += 1 + len(body) - len(stripped)
        body = stripped
    body = re.sub(r"^\d{1,3}[.):]\s+", "", body)   # "12. Display ..." line numbers
    return indent, strip_comment(body).strip()


def clean(line):
    """Comment markers and whitespace removed (used by the interactive prompt)."""
    return split_indent(line)[1]


CONT_END = re.compile(r"(,|\+|-|\*|/|=|&|\(|\bor|\band|\|\||&&)$", re.I)
STRUCT_START = re.compile(
    r"^(if|else|elseif|elif|end|endif|endwhile|endfor|endselect|while|do|for|"
    r"select|switch|case|default|module|function|sub|procedure|def|loop|next|"
    r"until|repeat|return|call|display|print|input|declare|constant|set)\b", re.I)


def needs_more(s):
    """True when a statement obviously continues on the next line."""
    depth, quote = 0, None
    for c in s:
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
    if s.count('"') % 2 == 1:
        return True
    return depth > 0 or bool(CONT_END.search(s.rstrip()))


def join_lines(raw_lines):
    """Clean every line and glue continuation lines together.

    -> [(indent, text, the line number it started on)].  The number is
    carried so a statement can be pointed back at what was typed."""
    out, buf, buf_indent, joined, buf_line = [], "", 0, 0, 1
    for no, raw in enumerate(raw_lines, 1):
        indent, text = split_indent(raw)
        if not text:                                   # blank: never continue past it
            if buf:
                out.append((buf_indent, buf, buf_line))
                buf = ""
            out.append((indent, "", no))               # kept: a blank line is
            continue                                   #   where a run of
                                                       #   Displays ends
        if buf and (STRUCT_START.match(text) or joined >= 8):
            out.append((buf_indent, buf, buf_line))    # safety: a new statement
            buf = ""
        if buf:
            buf = buf + " " + text
            joined += 1
        else:
            buf, buf_indent, joined, buf_line = text, indent, 0, no
        if needs_more(buf):
            continue
        out.append((buf_indent, buf, buf_line))
        buf = ""
    if buf:
        out.append((buf_indent, buf, buf_line))
    return out


def tidy(s):
    """Single spaces (outside quotes), no trailing punctuation.  Keeps capitals."""
    out, quote, space = [], None, False
    for c in s.strip():
        if quote:
            out.append(c)
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            out.append(c)
            space = False
        elif c.isspace():
            if not space:
                out.append(" ")
            space = True
        else:
            out.append(c)
            space = False
    return "".join(out).rstrip(":;.").strip()


def unwrap(cond):
    """Drop one pair of parentheses that wraps the whole condition."""
    c = cond.strip()
    if c.startswith("(") and c.endswith(")"):
        depth = 0
        for i, ch in enumerate(c):
            depth += (ch == "(") - (ch == ")")
            if depth == 0 and i < len(c) - 1:
                return c
        return c[1:-1].strip()
    return c


