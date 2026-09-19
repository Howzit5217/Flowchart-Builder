"""A block of chart, and a straight run of steps."""
import math

from .. import settings
from ..measure import FONT_SIZE, LINE_H, text_w
from ..parse.nodes import Node
from ..shapes import SHAPES, geom_of


# ------------------------------------------------------------------- layout --
#  Drawing elements are tuples:
#      ("shape", kind, cx, cy, w, h, [text lines])
#      ("line", x1, y1, x2, y2, arrowhead?)
#      ("text", x, y, string, anchor)          branch labels
#      ("htext", x, y, string, anchor)         chart headings
# The same words, wrapped to the same width, come out the same way, and a
# chart laid out several times over asks for exactly that again and again.
# The answer is kept rather than worked out afresh; what goes back is a copy,
# because callers treat the list as theirs.
_WRAPS = {}
_WRAP_MAX = 100000


def wrap(text, width_px, size=None, bold=False):
    """Wrap text to a pixel width, honoring explicit newlines."""
    if size is None:
        size = FONT_SIZE
    key = (text, round(width_px, 3), size, bold)
    got = _WRAPS.get(key)
    if got is not None:
        return list(got)
    out = []
    for paragraph in text.split("\n"):
        words, line = [], ""
        for w in paragraph.split():            # chop a word wider than the box
            while len(w) > 1 and text_w(w, size, bold) > width_px:
                cut = len(w) - 1
                while cut > 1 and text_w(w[:cut], size, bold) > width_px:
                    cut -= 1
                words.append(w[:cut])
                w = w[cut:]
            words.append(w)
        for w in words:
            trial = (line + " " + w).strip()
            if text_w(trial, size, bold) > width_px and line:
                out.append(line)
                line = w
            else:
                line = trial
        out.append(line)
    out = out or [""]
    if len(_WRAPS) >= _WRAP_MAX:
        _WRAPS.clear()
    _WRAPS[key] = out
    return list(out)


def shift(elems, dx, dy):
    """The same drawing, moved.  This is the busiest thing in the layout --
    every block that goes anywhere is rewritten by it -- so it is written
    for speed rather than for looks: the appending is bound to a name once
    instead of looked up a quarter of a million times, and a move of nothing
    hands back the pieces as they are.  They are tuples and nobody writes to
    them, so only the list has to be a new one."""
    if not dx and not dy:
        return list(elems)
    moved = []
    add = moved.append
    for e in elems:
        kind = e[0]
        if kind == "shape":
            add(("shape", e[1], e[2] + dx, e[3] + dy, e[4], e[5],
                 e[6], e[7] if len(e) > 7 else 0))
        elif kind == "line":
            add(("line", e[1] + dx, e[2] + dy, e[3] + dx, e[4] + dy, e[5]))
        else:
            add((e[0], e[1] + dx, e[2] + dy, e[3], e[4]))
    return moved


class Block:
    """A laid-out piece of chart.  Entry is (axis, 0); exit is (axis, h)."""

    def __init__(self, w, h, axis, elems, terminal=False, loop=False):
        self.w, self.h, self.axis, self.elems = w, h, axis, elems
        self.terminal = terminal        # nothing flows out of the bottom
        self.loop = loop                # the way out runs down the far side


def edge_shape(block, top=False):
    """The single shape a block ends on, or starts on if top is asked for.

    A plain run of statements has one: its last box sits flush with the foot
    of the block, on the flow line, and its first with the head.  An If or a
    loop does not -- what sits at the foot of those is the point where two
    routes meet, and a line has to leave that from below.

    Knowing the shape is what lets a route meet it at the side.  A line that
    is travelling sideways anyway can leave a box's side instead of dropping
    clear of its bottom and turning, and a line arriving sideways can go
    into the side it arrives at instead of bending to come in over the top:
    a turn fewer each time, and a shorter line.  Returns (left, right,
    middle height) in the block's own coordinates, taken at the height where
    the shape is widest, or None.
    """
    found = None
    for e in block.elems:
        if e[0] != "shape":
            continue
        flush = (e[3] - e[5] / 2.0 < 1.0 if top
                 else abs((e[3] + e[5] / 2.0) - block.h) < 1.0)
        if flush:
            if found is not None:
                return None             # two of them level: use the foot
            found = e
    if found is None:
        return None
    _, kind, cx, cy, w, _h, _lines = found[:7]
    if abs(cx - block.axis) > 1.0:      # not sitting on the flow line
        return None
    if kind in ("diamond", "hex"):
        return None                     # a test's sides are its own answers'
    # Where the outline actually is at half height, which for anything that
    # leans or bows is not where the box is.  A line meeting the box instead
    # would stop short of the shape, in mid-air beside it.
    if kind in ("io", "io_back", "trap"):
        lean = min(settings.SLANT, w / 4.0) / 2.0          # a parallelogram's waist
    elif kind == "screen":
        lean = min(16.0, w * 0.16) / 4.0          # the bowed-in left side
    else:
        lean = 0.0
    return cx - w / 2.0 + lean, cx + w / 2.0 - lean, cy


def clear_foot(block, side):
    """Is the foot of this block clear of lines running out to that side?

    A block ending on an If leaves the last line of each branch lying along
    its foot, so a route setting off sideways from there would run down the
    top of one of them.  A block ending on a loop leaves only the loop's way
    out, which comes in from the other hand and is already going the way we
    are."""
    for e in block.elems:
        if e[0] != "line" or abs(e[2] - e[4]) > 0.5:      # horizontals only
            continue
        if abs(e[2] - block.h) > 1.5:                     # at the foot only
            continue
        reach = (min(e[1], e[3]) if side < 0 else max(e[1], e[3])) - block.axis
        if (reach < -1.0) if side < 0 else (reach > 1.0):
            return False
    return True


def tail_shape(block):
    return edge_shape(block)


def head_shape(block):
    return edge_shape(block, top=True)


def part_of(item, shape, text):
    """A shape drawn for a statement -- the diamond of an If, the boxes a For
    turns into -- carrying that statement's number, so the drawing and the
    data agree about which is which."""
    node = Node(shape, text)
    node.node_id = getattr(item, "node_id", 0)
    node.line = getattr(item, "line", 0)
    return node


def node_block(node):
    longest = max(text_w(l) for l in node.text.split("\n"))
    drawn = SHAPES.get(geom_of(node.shape), SHAPES["rect"])
    if drawn.get("wide"):                       # a diamond: the words sit in
        w = max(settings.DIA_W, min(settings.NODE_MAX_W + 60, longest / 0.55 + 10))
        inner = w * 0.55                        #   the middle band of it
    else:
        pad = drawn["side"]
        base = settings.OVAL_W if drawn.get("floor") == "oval" else settings.NODE_W
        w = max(base, min(settings.NODE_MAX_W, longest + pad))
        inner = w - pad
    lines = wrap(node.text, inner)
    if drawn.get("wide"):
        h = max(settings.DIA_MIN_H, 2.4 * len(lines) * LINE_H + 8)
    elif drawn.get("floor") == "oval":
        h = max(settings.OVAL_H, len(lines) * LINE_H + 2 * settings.PAD_Y)
    else:
        h = max(settings.NODE_MIN_H, len(lines) * LINE_H + 2 * settings.PAD_Y + drawn["top"])
    if drawn.get("round"):                      # a joining point is round
        h = max(h, min(w, 96), 40)
    # Up to a whole number of grid steps.  Every gap between shapes is a whole
    # number too, so a chart built out of these lands on the ruling behind it
    # instead of floating a few pixels off it all the way down.
    if settings.GRID_STEP > 0:
        step = settings.GRID_STEP * 2            # so h / 2 is a whole step as well
        h = math.ceil(h / step - 0.001) * step
    return Block(w, h, w / 2.0,
                 [("shape", node.shape, w / 2.0, h / 2.0, w, h, lines,
                   getattr(node, "node_id", 0))],
                 node.terminal)


def layout_seq(items):
    blocks = [layout_item(it) for it in items]
    if not blocks:
        return Block(0, 0, 0, [])
    axis = max(b.axis for b in blocks)
    right = max(b.w - b.axis for b in blocks)
    elems, y = [], 0.0
    for i, b in enumerate(blocks):
        if i:
            if not blocks[i - 1].terminal:
                elems.append(("line", axis, y, axis, y + settings.VGAP, True))
            y += settings.VGAP
        elems += shift(b.elems, axis - b.axis, y)
        y += b.h
    return Block(axis + right, y, axis, elems, blocks[-1].terminal)


# Which part lays out which kind of statement.  An If, a loop and a Select
# each have a file of their own, and each writes its own name in here as it
# is read.  That is the whole reason this file can be the one they all lean
# on: it knows that something lays out an "if" without knowing what, so it
# needs to know nothing about them at all.  Adding a kind of statement is
# adding a file and one line at the foot of it.
LAYOUTS = {"node": node_block}


def layout_item(item):
    """One statement, laid out by whichever part knows its kind."""
    lay = LAYOUTS.get(getattr(item, "kind", ""))
    return lay(item) if lay else node_block(item)


