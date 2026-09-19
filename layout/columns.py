"""Wrapping a chart into columns, and setting several
charts side by side."""
from .. import settings
from ..layout.blocks import (
    edge_shape, head_shape, layout_item, shift, tail_shape, wrap)
from ..measure import FONT_SIZE, text_w


# ----------------------------------------------------------- column packing --
def pack_columns(blocks, max_h):
    """Fill one column at a time, top to bottom, breaking past max_h.

    A block taller than max_h all by itself -- a long If, say -- cannot be
    split, so it overshoots its column.  When that happens the shapes after
    it stay in the same column until they would fill a column of their own,
    instead of each starting a fresh one: an End stranded by itself at the
    top of an empty column, a whole page above the branch that reaches it,
    helps nobody.
    """
    columns, current, height, room = [], [], 0.0, max_h
    heights = []
    for b in blocks:
        add = b.h + (settings.VGAP if current else 0)
        if current and height + add > room:
            columns.append(current)
            heights.append(height)
            current, height = [b], b.h
            room = b.h + max_h if b.h > max_h else max_h
        else:
            current.append(b)
            height += add
            if len(current) == 1:
                room = b.h + max_h if b.h > max_h else max_h
    if current:
        columns.append(current)
        heights.append(height)

    # Never end a column on something with no side to leave from.
    #
    # A plain box has a bottom edge and two sides, so the arrow on to the next
    # column can set off from whichever suits.  The foot of a loop, an If or a
    # Case is not a shape at all -- it is the point where two or three routes
    # meet -- so the arrow has to start at the middle and work outwards.  That
    # is where the ugliness came from: the routes arriving at that point come
    # in from the sides, so the line would come in from the right, drop an
    # inch, and set straight back out to the right again past where it had
    # just been.
    #
    # Where there is something else in the column, the offending block goes to
    # the next one and the break happens a shape earlier, at a plain box.
    # Where it is the whole column -- a column shorter than the block itself,
    # so it was overshooting anyway -- there is nothing to break before, and
    # the next shape comes back to join it.
    def lift(i, j, at):                 # move one block from column j to i
        moved = columns[j].pop(at)
        columns[i].insert(len(columns[i]) if at == 0 else 0, moved)
        heights[j] -= moved.h + settings.VGAP
        heights[i] += moved.h + settings.VGAP

    def no_side(col):
        return bool(col) and not col[-1].terminal and tail_shape(col[-1]) is None

    # A column with next to nothing in it is worse than no break at all: the
    # arrow to reach it still climbs a whole column and runs back over the top
    # of the chart, and all it buys is an End sitting alone at the head of an
    # empty lane.  Give a runt back to the column before it.  This is settled
    # first, because merging two columns changes what the earlier one ends on.
    runt = max(120.0, max_h * 0.3)
    while len(columns) > 1 and heights[-1] < runt:
        tail, tall = columns.pop(), heights.pop()
        columns[-1].extend(tail)
        heights[-1] += settings.VGAP + tall

    # Moving a block changes what the column it came from ends on, and what
    # the column it went to begins with, so one pass is not enough: it is
    # worked over until nothing more needs moving.  The count is a guard
    # against a pair of columns handing the same block back and forth, which
    # cannot happen with these rules but costs nothing to rule out.
    for _ in range(8):
        shifted = False
        for i in range(len(columns) - 1):
            while len(columns[i]) > 1 and no_side(columns[i]):
                lift(i + 1, i, -1)      # hand it on to the next column
                shifted = True
            while no_side(columns[i]) and columns[i + 1]:
                lift(i, i + 1, 0)       # or bring the next shape back to it
                shifted = True
        live = [n for n, col in enumerate(columns) if col]
        columns = [columns[n] for n in live]
        heights = [heights[n] for n in live]
        if not shifted:
            break
    return columns


def choose_columns(blocks, max_h):
    """Decide where the chart should break into columns.

    Given a height to obey, obey it.  Given none, don't break it at all.
    A flowchart is allowed to be tall -- that is the shape of the thing --
    and every break costs an arrow that has to climb the whole column it
    leaves and run back over the top of the chart to reach the next one,
    which is a great deal harder to follow than simply scrolling down.
    """
    return pack_columns(blocks, max_h) if max_h else [list(blocks)]


# Laid out once, not once per height tried.  Choosing the outline lays the
# same program out again at a dozen different ceilings, and a ceiling decides
# only where the columns break -- never what goes in them, or how big any of
# it is.  So the pieces are worked out once for a given set of items and kept
# while the choosing goes on.  settings.CHAIN_LIMIT is in the key because it
# does change them: it is what decides whether the two sides of an If queue
# up or fork.  Nothing here is ever written to after it is made, which is why
# the same pieces can be handed out again.
#
# It is switched on for the length of one fitting and off again afterwards,
# and the only reason is that the key is an identity.  An identity is only
# an identity while the thing is alive: let the charts go, and the next list
# to be made can be handed the same number and would be given somebody
# else's blocks.  Whoever turns this on is holding the charts for as long as
# it is on, so within that stretch no key can mean two things.
_LAID = None


def keep_layouts():
    """Start remembering.  The caller must hold the charts until it stops."""
    global _LAID
    _LAID = {}


def forget_layouts():
    """Stop, and let them go."""
    global _LAID
    _LAID = None


def laid_out(items):
    """The blocks for these items, made once while the remembering is on."""
    if _LAID is None:
        return [layout_item(it) for it in items]
    key = (id(items), settings.CHAIN_LIMIT)
    got = _LAID.get(key)
    if got is None:
        got = _LAID[key] = [layout_item(it) for it in items]
    return got


def build_columns(items, max_h):
    """Lay the chart out top-to-bottom, wrapping into columns."""
    blocks = laid_out(items)
    if not blocks:
        return []
    laid, x = [], 0.0
    for col in choose_columns(blocks, max_h):
        axis = max(b.axis for b in col)
        right = max(b.w - b.axis for b in col)
        elems, y, last_top = [], 0.0, 0.0
        for i, b in enumerate(col):
            if i:
                if not col[i - 1].terminal:
                    elems.append(("line", axis, y, axis, y + settings.VGAP, True))
                y += settings.VGAP
            last_top = y
            elems += shift(b.elems, axis - b.axis, y)
            y += b.h
        head, tail = col[0], col[-1]
        # Where an arrow can meet the shape at each end of the column instead
        # of dropping out of a bottom or coming in over a top: the side of the
        # first shape to arrive at, and the side of the last one to leave
        # from.  Either is None where the column ends on something that is not
        # a plain shape -- the foot of an If or a loop is a meeting of routes,
        # and a line has to leave that from below.
        came = head_shape(head)
        went = edge_shape(tail)
        here = {"x": x, "axis": x + axis, "h": y,
                "right": x + axis + right,
                "elems": shift(elems, x, 0),
                "open": not tail.terminal}
        if came:
            here["in_x"] = x + axis - head.axis + came[0]
            here["in_y"] = came[2]
        if went and not tail.terminal:
            here["out_x"] = x + axis - tail.axis + went[1]
            here["out_y"] = last_top + went[2]
        laid.append(here)
        x += axis + right + settings.COL_GAP
    return laid


def connect_columns(cols):
    """One arrow from the foot of a column, up the empty gutter beside it
    and into the head of the next.  The gutter is clear by construction, so
    the route never has to cross anything on the way.  This only happens at
    all when a column height was asked for: left alone, a chart is one
    column and needs no such arrow.

    It goes in at the side of the first shape rather than over the top of
    it, which is the shorter way round and the plainer one to follow: four
    turns instead of five, no run back across the whole width of the chart,
    and it arrives pointing at the shape it is arriving at."""
    elems = []
    for a, b in zip(cols, cols[1:]):
        if not a["open"]:
            continue
        gutter = (a["right"] + b["x"]) / 2.0
        # Out of the side of the last shape where it has one, which is a
        # straight run into the gutter.  Dropping out of its bottom first only
        # to turn and climb back up past it buys nothing and reads as a
        # mistake, which is what it looked like.
        leaves = a.get("out_x")
        if leaves is not None and gutter > leaves + 1.0:
            at = a["out_y"]
            off = [("line", leaves, at, gutter, at, False)]
        else:
            at = a["h"] + settings.VGAP * 0.55
            off = [("line", a["axis"], a["h"], a["axis"], at, False),
                   ("line", a["axis"], at, gutter, at, False)]

        into = b.get("in_y")
        side = b.get("in_x")
        if into is not None and side is not None and side > gutter + 1.0:
            elems += off + [("line", gutter, at, gutter, into, False),
                            ("line", gutter, into, side, into, True)]
            continue
        lane = -settings.VGAP * 0.75               # clear of the top of both columns
        elems += off + [("line", gutter, at, gutter, lane, False),
                        ("line", gutter, lane, b["axis"], lane, False),
                        ("line", b["axis"], lane, b["axis"], 0, True)]
    return elems


def bbox(elems):
    xs, ys = [], []
    for e in elems:
        if e[0] == "shape":
            _, _, cx, cy, w, h = e[:6]
            xs += [cx - w / 2.0, cx + w / 2.0]
            ys += [cy - h / 2.0, cy + h / 2.0]
        elif e[0] == "line":
            xs += [e[1], e[3]]
            ys += [e[2], e[4]]
        else:
            _, x, y, s, anchor = e
            tw = (text_w(s, 13, True) if e[0] == "htext"
                  else text_w(s, FONT_SIZE, True) + 8)
            if anchor == "end":
                xs += [x - tw, x]
            elif anchor == "middle":
                xs += [x - tw / 2.0, x + tw / 2.0]
            else:
                xs += [x, x + tw]
            ys += [y - 12, y + 3]
    if not xs:
        return 0.0, 0.0, 0.0, 0.0
    return min(xs), min(ys), max(xs), max(ys)


def layout_chart(chart, max_h, heading=True):
    """One chart -> (elems, w, h) with its top-left corner at (0, 0)."""
    cols = build_columns(chart.items, max_h)
    elems = connect_columns(cols)
    for c in cols:
        elems += c["elems"]
    minx, miny, maxx, maxy = bbox(elems)
    elems = shift(elems, -minx, -miny)
    w, h = maxx - minx, maxy - miny
    if heading:
        hw = max(w, 360.0)
        lines = wrap(chart.heading, hw, 13, True)
        head_h = settings.HEADING_H + (len(lines) - 1) * 17
        elems = shift(elems, 0, head_h)
        for i, line in enumerate(lines):
            elems.append(("htext", 0, 14 + i * 17, line, "start"))
        w, h = max(w, hw), h + head_h
    return elems, w, h


def onto_grid(elems, down):
    """How far a chart has to be set down for its shapes to land on the ruling.

    One chart is easy: draw/svg.py nudges the whole drawing so the highest
    shape in it sits on a line.  A program with modules is several charts,
    and the ones after the first are set down by a heading's height and by
    whatever the row above came to -- neither of them a whole number of
    steps.  So the first chart sat on the ruling and every other one floated
    a few pixels off it, all the way down.  Each is nudged the last few
    pixels here instead; the nudge is measured from a shape, because the top
    of everything includes a heading and an arrowhead sitting wherever they
    happen to sit.
    """
    step = settings.GRID_STEP
    if step <= 0:
        return down
    tops = [e[3] - e[5] / 2.0 for e in elems if e[0] == "shape"]
    if not tops:
        return down
    return down + (-(min(tops) + down)) % step


def arrange(layouts):
    """Place charts left-to-right, starting a new row past settings.MAX_ROW_W."""
    limit = max(settings.MAX_ROW_W, max(l[1] for l in layouts))
    rows, widths = [], []                         # first fit: fill earlier rows
    for lay in layouts:
        w = lay[1]
        for i, row in enumerate(rows):
            if widths[i] + settings.CHART_GAP + w <= limit:
                row.append(lay)
                widths[i] += settings.CHART_GAP + w
                break
        else:
            rows.append([lay])
            widths.append(w)
    elems, y = [], 0.0
    for row in rows:
        x, tallest = 0.0, max(l[2] for l in row)
        for el, w, h in row:
            elems += shift(el, x, onto_grid(el, y))
            x += w + settings.CHART_GAP
        y += tallest + settings.CHART_GAP
    return elems



