"""Lines with square corners, rounded off, and the heads
on them."""
import collections
import math

from .. import settings


# ---------------------------------------------------------------- svg output --
def chain_lines(lines):
    """Glue segments that meet end-to-start into one route.

    The layout code puts an elbow down as two or three separate segments;
    drawn that way each is its own stroke and only the last one carries a
    head.  Chained, an elbow reads as a single arrow from where the flow
    leaves to where it arrives.  A point where more than one route meets is
    left alone, so two branches merging still read as two arrows.
    """
    # Both ends of every segment, rounded once and kept.  They were being
    # rounded again on every look -- tens of thousands of times over a long
    # chart, and this runs once per layout the fitting tries.
    ends = {}
    leaving, arriving = collections.Counter(), collections.Counter()
    onward, into = {}, {}
    for e in lines:
        head = (round(e[1], 1), round(e[2], 1))
        tail = (round(e[3], 1), round(e[4], 1))
        ends[id(e)] = (head, tail)
        leaving[head] += 1
        arriving[tail] += 1
        onward.setdefault(head, []).append(e)
        into.setdefault(tail, []).append(e)

    def corner(pt):                 # one line in and one line out: a bend
        return arriving[pt] == 1 and leaving[pt] == 1

    used, routes = set(), []

    def walk(seed):
        pts, cur, arrow = [(seed[1], seed[2])], seed, seed[5]
        while True:
            used.add(id(cur))
            pts.append((cur[3], cur[4]))
            arrow = cur[5]
            here = ends[id(cur)][1]
            nxt = [x for x in onward.get(here, []) if id(x) not in used]
            if arrow or not corner(here) or not nxt:
                break
            cur = nxt[0]
        routes.append((pts, arrow))

    def fed_by_spare(pt):           # is some untaken segment aimed at pt?
        # Only the segments that end at pt can be, and they are indexed;
        # this used to read the whole list for every point it asked about,
        # inside a loop that asks about every point until none is left.
        return any(id(x) not in used for x in into.get(pt, ()))

    for e in lines:                 # routes that start at a clear head
        if id(e) not in used and not corner(ends[id(e)][0]):
            walk(e)
    again = True                    # then routes that pick up where some
    while again:                    #   other route's arrowhead landed
        again = False
        for e in lines:
            if id(e) not in used and not fed_by_spare(ends[id(e)][0]):
                walk(e)
                again = True
    for e in lines:                 # a closed ring, if one ever turns up
        if id(e) not in used:
            walk(e)
    return routes


def arrow_head(pts):
    """The filled triangle that finishes a route, and where the line
    should stop so the stroke does not poke out through the point.

    This is drawn as an ordinary polygon rather than with an SVG <marker>.
    Word, PowerPoint and Google Docs all quietly throw markers away when
    they import an SVG, which leaves a chart full of lines with no heads on
    them.  A polygon is just another shape, so every viewer draws it.
    """
    (ax, ay), (bx, by) = pts[-2], pts[-1]
    run = math.hypot(bx - ax, by - ay)
    if run < 0.01:
        return None, pts
    ux, uy = (bx - ax) / run, (by - ay) / run      # along the last segment
    nx, ny = -uy, ux                               # across it
    cx, cy = bx - ux * settings.HEAD_LEN, by - uy * settings.HEAD_LEN
    tri = "%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        bx, by,
        cx + nx * settings.HEAD_WIDE / 2.0, cy + ny * settings.HEAD_WIDE / 2.0,
        cx - nx * settings.HEAD_WIDE / 2.0, cy - ny * settings.HEAD_WIDE / 2.0)
    stop = list(pts)
    if run > settings.HEAD_LEN + 1:              # let the stroke stop at the base
        stop[-1] = (cx, cy)
    return tri, stop


def path_d(pts):
    """An SVG path through pts, with the corners eased off a little."""
    clean = [pts[0]]
    for q in pts[1:]:
        if math.hypot(q[0] - clean[-1][0], q[1] - clean[-1][1]) > 0.05:
            clean.append(q)
    if len(clean) < 2:
        return ""
    d = ["M%.1f,%.1f" % clean[0]]
    for i in range(1, len(clean) - 1):
        (ax, ay), (bx, by), (cx, cy) = clean[i - 1], clean[i], clean[i + 1]
        d1 = math.hypot(bx - ax, by - ay)
        d2 = math.hypot(cx - bx, cy - by)
        r = min(settings.CORNER_R, d1 / 2.0, d2 / 2.0)
        if r < 0.5:
            d.append("L%.1f,%.1f" % (bx, by))
            continue
        d.append("L%.1f,%.1f" % (bx - (bx - ax) / d1 * r,
                                 by - (by - ay) / d1 * r))
        d.append("Q%.1f,%.1f %.1f,%.1f" % (bx, by,
                 bx + (cx - bx) / d2 * r, by + (cy - by) / d2 * r))
    d.append("L%.1f,%.1f" % clean[-1])
    return " ".join(d)


