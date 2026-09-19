"""If and Else, and the lanes they need."""
from .. import settings
from ..layout import blocks
from ..layout.blocks import (
    Block, head_shape, layout_seq, node_block, part_of, shift, tail_shape)
from ..measure import text_w


def chain_parts(item):
    """An If with its Else Ifs flattened: [(cond, then), ...] and the Else.

    Only an "Else If" counts.  An If written inside an Else is a nested
    question, not another answer to the same one, and it keeps the nested
    drawing that says so."""
    tests, node = [], item
    while True:
        tests.append((node.cond, node.then, node))
        tail = node.orelse
        if len(tail) == 1 and tail[0].kind == "if" and tail[0].chained:
            node = tail[0]
            continue
        return tests, tail


def layout_chain(tests, tail, thens, other):
    """A chain of tests, one under another down the page.

    Side by side, a chain costs a lane for every branch it has, and the
    four branches of a menu come out wider than the paper they are going
    on: scaled to fit the page, the lettering ends up too small to read.
    So the tests queue up instead.  Each one sits under the last, False
    carries straight on down to the next question, every True branch hangs
    in the one lane beside them, and the branches all come home on a single
    line down the outside.  The chart gets taller for it, which costs
    nothing much -- a reader scrolls, and paper takes another sheet --
    while width is what there is no more of.
    """
    dias = [node_block(part_of(owner, "diamond", cond))
            for cond, _, owner in tests]
    t_gap = max(settings.HGAP, text_w(settings.YES, bold=True) + settings.LABEL_PAD)
    half = max(d.w for d in dias) / 2.0
    side = -1 if settings.TRUE_LEFT else 1           # the hand the branches hang on
    near = max(b.w - b.axis if side < 0 else b.axis for b in thens)
    far = max(b.axis if side < 0 else b.w - b.axis for b in thens)
    lane = side * (half + t_gap + near)     # the branches' own flow line
    # and the way home, outside the branches -- and outside the Else too,
    # which sits on the flow line below them and can be wider than they are
    reach = (other.axis if side < 0 else other.w - other.axis) if other.h else 0.0
    rail = side * max(abs(lane) + far + settings.HGAP, reach + settings.HGAP)

    elems, backs, y = [], [], 0.0
    straight = None                         # a branch that needs no rail
    for i, (dia, then) in enumerate(zip(dias, thens)):
        d_half, mid = dia.w / 2.0, dia.h / 2.0
        last = i == len(tests) - 1
        # Where the branch opens on a box, the box is set level with the
        # middle of the diamond and True runs straight into its side.  The
        # answer and what it leads to then sit on one line, and there is no
        # corner in between to follow.  A branch that opens on something
        # else -- another question, a loop -- is met over the top as before.
        head = head_shape(then) if then.h else None
        sink = max(0.0, (head[2] - mid) if head else 0.0)
        if sink:                            # a tall box: let the test down
            elems.append(("line", 0, y, 0, y + sink, False))
        d_top = y + sink
        cy = d_top + mid
        elems += shift(dia.elems, -dia.axis, d_top)
        elems.append(("text", side * (d_half + 6), cy - 6, settings.YES,
                      "end" if side < 0 else "start"))
        d_bot = d_top + dia.h
        if head:                            # straight in at the side
            elems.append(("line", side * d_half, cy,
                          lane + (head[1] if side < 0 else head[0]) - then.axis,
                          cy, True))
            b_top = cy - head[2]
        else:
            elems.append(("line", side * d_half, cy, lane, cy, not then.h))
            b_top = d_bot
            if then.h:
                elems.append(("line", lane, cy, lane, b_top, True))
        if then.h:
            elems += shift(then.elems, lane - then.axis, b_top)
            bot = b_top + then.h
            if not then.terminal:
                # The last branch has nothing under it in the lane, so it
                # goes home the short way: straight down where it stands
                # and one turn in.  Every branch above it has the branches
                # below in the way, and has to step out to the rail first --
                # and it does that out of the side of the box it ends on,
                # where it ends on one, rather than dropping clear and
                # turning.
                if last and abs(lane) > reach + settings.HGAP / 2.0:
                    straight = bot
                else:
                    foot = tail_shape(then)
                    edge = None
                    if foot:
                        edge = (foot[0] if side < 0 else foot[1]) \
                               - then.axis + lane
                    if edge is not None and abs(edge - rail) > 2:
                        back = foot[2] + b_top
                        elems.append(("line", edge, back, rail, back, False))
                    else:
                        back = bot + settings.VGAP / 2.0
                        elems += [("line", lane, bot, lane, back, False),
                                  ("line", lane, back, rail, back, False)]
                    backs.append(back)
        else:                               # an empty Then: straight home
            bot = d_bot
            backs.append(cy)
        nxt = max(bot, d_bot) + settings.VGAP
        elems += [("line", 0, d_bot, 0, nxt, not (last and not other.h)),
                  ("text", -side * 5, d_bot + 14, settings.NO,
                   "start" if side < 0 else "end")]
        y = nxt

    if other.h:                             # the Else, on the line it is on
        elems += shift(other.elems, -other.axis, y)
        foot, done = y + other.h, other.terminal
    else:
        foot, done = y, False

    # the rail's side reaches out to it; the other side only has to hold the
    # diamonds and the Else, which sit on the flow line
    tail_out = other.axis if side > 0 else other.w - other.axis
    inner = max(half, tail_out if other.h else 0)
    left, right = (-rail, inner) if side < 0 else (inner, rail)

    if not backs and straight is None and done:   # every answer ended the flow
        return Block(left + right, foot, left, shift(elems, left, 0), True)

    coming = backs + ([straight] if straight is not None else [])
    merge = max([foot] + coming) + settings.VGAP
    if not done:
        elems.append(("line", 0, foot, 0, merge, False))
    if backs:                               # the rail, down to the meeting
        elems += [("line", rail, min(backs), rail, merge, False),
                  ("line", rail, merge, lane if straight is not None else 0,
                   merge, straight is None)]
    if straight is not None:                # and the short way home, which
        elems += [("line", lane, straight, lane, merge, False),   # the rail
                  ("line", lane, merge, 0, merge, True)]          # joins
    return Block(left + right, merge, left, shift(elems, left, 0))


def layout_if(item):
    """A chain of tests goes down the page when laying it out side by
    side would come out wider than settings.CHAIN_LIMIT; anything else forks."""
    tests, tail = chain_parts(item)
    if len(tests) > 1:
        thens = [layout_seq(t) for _, t, _owner in tests]
        other = layout_seq(tail)
        # what forking would cost: every test nests inside the last one's
        # False lane, so each one adds its diamond, its branch and the room
        # the two labels need beside it
        gaps = (max(settings.HGAP, text_w(settings.YES, bold=True) + settings.LABEL_PAD)
                + max(settings.HGAP, text_w(settings.NO, bold=True) + settings.LABEL_PAD))
        span = other.w + sum(node_block(part_of(owner, "diamond", cond)).w
                             + b.w + gaps
                             for (cond, _, owner), b in zip(tests, thens))
        if span > settings.CHAIN_LIMIT:
            return layout_chain(tests, tail, thens, other)
    return layout_fork(item)


def layout_fork(item):
    """Local coordinates: the incoming flow line sits at x = 0.

    Both answers fork off the sides of the diamond -- True to the left,
    False to the right -- and meet again on the axis below, so the two
    outcomes read as two paths of equal standing and a reader never has to
    work out which answer the unlabelled line belonged to.

    An If with no Else is the one exception, and only when its true branch
    is a wide one.  There is no second branch to be even-handed about, and
    forking would buy that even-handedness with a line as long as the whole
    branch is wide -- on a big If, the longest line in the chart.  So the
    branch keeps the axis, the False side steps aside into the nearest free
    lane, and its arrow comes back and points at the line where the two
    join.

    A branch that opens on a box is set level with the middle of the
    diamond, so its answer runs straight into the side of that box with no
    corner in between.  Where a branch opens on something else -- another
    question, a loop -- there is no side to aim at and it is met over the
    top, the old way.
    """
    dia = node_block(part_of(item, "diamond", item.cond))
    then = layout_seq(item.then)
    other = layout_seq(item.orelse)
    half, mid = dia.w / 2.0, dia.h / 2.0
    elems = shift(dia.elems, -dia.axis, 0)

    # each lane sits far enough out for the word written above it to fit
    t_gap = max(settings.HGAP, text_w(settings.YES, bold=True) + settings.LABEL_PAD)
    e_gap = max(settings.HGAP, text_w(settings.NO, bold=True) + settings.LABEL_PAD)
    top = dia.h + settings.VGAP

    t_side = -1 if settings.TRUE_LEFT else 1     # which hand True goes out on
    e_side = -t_side

    def lane_at(blk, gap, side):
        """Where a branch's own flow line sits, out far enough on that side
        that the widest thing in it still clears the diamond."""
        out = blk.axis if side > 0 else blk.w - blk.axis
        return side * (half + gap + out)

    if not item.orelse and half + t_gap + (then.w - then.axis) > settings.FORK_LIMIT:
        y = top + then.h
        elems += [("line", 0, dia.h, 0, top, True),
                  ("text", -e_side * 5, dia.h + settings.VGAP / 2.0 + 4, settings.YES,
                   "end" if e_side > 0 else "start")]
        elems += shift(then.elems, -then.axis, top)
        merge = y + settings.VGAP
        if not then.terminal:
            elems.append(("line", 0, y, 0, merge, False))
        out = then.w - then.axis if e_side > 0 else then.axis
        lane = e_side * (max(half, out) + e_gap)       # clear of the branch
        elems += [("line", e_side * half, mid, lane, mid, False),
                  ("text", e_side * (half + 6), mid - 6, settings.NO,
                   "start" if e_side > 0 else "end"),
                  ("line", lane, mid, lane, merge, False),
                  ("line", lane, merge, 0, merge, True)]
        near = max(half, then.axis if e_side > 0 else then.w - then.axis)
        left = near if e_side > 0 else -lane
        right = lane if e_side > 0 else near
        return Block(left + right, merge, left, shift(elems, left, 0))

    t_axis = lane_at(then, t_gap, t_side)
    e_axis = lane_at(other, e_gap, e_side)
    both_end = then.terminal and other.terminal

    # A branch opening on a box is set level with the middle of the diamond,
    # so its answer goes straight in at the side.  If a box is taller than
    # the diamond, the diamond comes down to meet it rather than the branch
    # going up off the top of the block; the line into the diamond simply
    # runs on a little further, which is no line at all to follow.
    lanes = []
    sink = 0.0
    for blk, label, ax, sign in ((then, settings.YES, t_axis, t_side),
                                 (other, settings.NO, e_axis, e_side)):
        head = head_shape(blk) if blk.h else None
        if head:
            sink = max(sink, head[2] - mid)
        lanes.append([blk, label, ax, sign, head, 0.0])
    sink = max(0.0, sink)
    if sink:
        elems = [("line", 0, 0, 0, sink, False)] + shift(elems, 0, sink)
    cy, d_bot = sink + mid, sink + dia.h
    over = d_bot + settings.VGAP                 # a branch met over the top starts here
    for lane in lanes:
        lane[5] = cy - lane[4][2] if lane[4] else over
    merge = max(lane[5] + lane[0].h for lane in lanes)
    merge += 0 if both_end else settings.VGAP

    for side, label, ax, sign, head, b_top in lanes:
        elems.append(("text", sign * (half + 6), cy - 6, label,
                      "end" if sign < 0 else "start"))
        if head:                     # straight in at the side of the box
            elems.append(("line", sign * half, cy,
                          ax + (head[1] if sign < 0 else head[0]) - side.axis,
                          cy, True))
        else:
            elems.append(("line", sign * half, cy, ax, cy, False))
            if side.h:
                elems.append(("line", ax, cy, ax, b_top, True))
        if side.h:
            elems += shift(side.elems, ax - side.axis, b_top)
            if not side.terminal:
                # Both sides drop onto one rail and join there.  Neither
                # carries a head: two heads meeting nose to nose at the same
                # point reads as a collision.  The single arrow leaving the
                # join says which way it goes.
                elems += [("line", ax, b_top + side.h, ax, merge, False),
                          ("line", ax, merge, 0, merge, False)]
        else:                        # nothing on this side: an empty lane
            elems += [("line", ax, cy, ax, merge, False),
                      ("line", ax, merge, 0, merge, False)]

    lefty, righty = ((then, t_axis), (other, e_axis))[::-t_side]
    left = -lefty[1] + lefty[0].axis
    right = righty[1] + (righty[0].w - righty[0].axis)
    return Block(left + right, merge, left, shift(elems, left, 0), both_end)


blocks.LAYOUTS["if"] = layout_if
