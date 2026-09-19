"""Putting the SVG together."""
import html

from .. import settings
from ..draw.grid import grid_lines
from ..draw.outlines import shape_art
from ..draw.arrows import arrow_head, chain_lines, path_d
from ..layout.blocks import shift
from ..layout.columns import bbox
from ..measure import FONT, FONT_SIZE, LINE_H, text_w
from ..shapes import geom_of


def to_svg(elems, title=None, author=None):
    minx, miny, maxx, maxy = bbox(elems)
    head_h = settings.TITLE_H if title else 0
    # Set the chart down so that the shapes fall on the ruling.  The nudge is
    # measured from a shape rather than from the edge of everything, because
    # the edge of everything includes labels and arrowheads sitting at
    # whatever height they happen to sit at.  Only the whole chart moves, so
    # nothing inside it is disturbed; the margin grows by up to one step.
    over, down = settings.MARGIN - minx, settings.MARGIN - miny + head_h
    if settings.GRID and settings.GRID_STEP > 0:
        tops = [e[3] - e[5] / 2.0 for e in elems if e[0] == "shape"]
        lefts = [e[2] - e[4] / 2.0 for e in elems if e[0] == "shape"]
        if tops:
            over += (-(min(lefts) + over)) % settings.GRID_STEP
            down += (-(min(tops) + down)) % settings.GRID_STEP
    elems = shift(elems, over, down)
    width = maxx - minx + settings.MARGIN * 2
    height = maxy - miny + settings.MARGIN * 2 + head_h

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
        f'<rect class="sheet" width="100%" height="100%" fill="{settings.SHEET}"/>',
    ]
    out += grid_lines(width, height)
    out += [
        f'<g font-family="{FONT}" font-size="{FONT_SIZE}" fill="none" '
        f'stroke="{settings.INK}" stroke-width="1.3" stroke-linecap="round" '
        'stroke-linejoin="round">',
    ]
    # Named, like everything else that carries words, so that a page showing
    # the chart can recolor them with the rest.  Without the name they were
    # the only writing on the chart that stayed black whatever color the
    # paper was put on -- which on dark paper meant they were not there.
    if title:
        out.append(f'<text class="title" x="{settings.MARGIN}" y="25" font-size="16" '
                   f'font-weight="bold" stroke="none" fill="{settings.INK}">'
                   f'{html.escape(title)}</text>')
        if author:
            out.append(f'<text class="author" x="{settings.MARGIN}" y="42" stroke="none" '
                       f'fill="{settings.INK}">{html.escape(author)}</text>')

    # A route gets an arrowhead where it arrives at a shape, and also where
    # it arrives side-on at a line that carries on past the point -- a
    # branch rejoining the flow it left.  It points at that line, which is
    # what it is really arriving at.
    #
    # What never gets a head is a route that merely meets another one: the
    # two sides of an If coming back together arrive nose to nose at the
    # same point, and two heads there read as a collision rather than a
    # join.  There the single arrow leaving the meeting says where it goes.
    nodes = 0                            # shapes get a number as they go
    boxes = [(e[2] - e[4] / 2.0, e[3] - e[5] / 2.0,
              e[2] + e[4] / 2.0, e[3] + e[5] / 2.0)
             for e in elems if e[0] == "shape"]
    segs = [e for e in elems if e[0] == "line"]

    def reaches_a_shape(pt):
        for a, b, c, d in boxes:
            if a - 1.5 <= pt[0] <= c + 1.5 and b - 1.5 <= pt[1] <= d + 1.5:
                return True
        return False

    upright = lambda dx, dy: abs(dy) > abs(dx)
    at = lambda x, y: (round(x, 1), round(y, 1))
    leaving, arriving = {}, {}           # which way lines go at each point
    down_x, across_y = {}, {}            # verticals by x, horizontals by y
    for _, x1, y1, x2, y2, _a in segs:
        way = upright(x2 - x1, y2 - y1)
        leaving.setdefault(at(x1, y1), set()).add(way)
        arriving.setdefault(at(x2, y2), set()).add(way)
        if abs(x1 - x2) < 0.5:
            down_x.setdefault(round(x1, 1), []).append((min(y1, y2), max(y1, y2)))
        elif abs(y1 - y2) < 0.5:
            across_y.setdefault(round(y1, 1), []).append((min(x1, x2), max(x1, x2)))

    def runs_through(pt):
        """Is there a line at pt that carries on past it, rather than one
        that stops there?  Either a single segment pt sits inside, or one
        arriving and one leaving the same way, which is one line with a
        join drawn in the middle of it."""
        if leaving.get(pt, set()) & arriving.get(pt, set()):
            return True
        for lo, hi in down_x.get(pt[0], ()):
            if lo + 1.5 < pt[1] < hi - 1.5:
                return True
        for lo, hi in across_y.get(pt[1], ()):
            if lo + 1.5 < pt[0] < hi - 1.5:
                return True
        return False

    def joins_a_line(pts):
        """Does this route arrive side-on at a line that carries on past?"""
        pt = at(*pts[-1])
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        came = upright(bx - ax, by - ay)
        return came not in leaving.get(pt, set()) and runs_through(pt)

    # Routes first, because the shapes and the labels are meant to paint over
    # them.  The tips are held back to the very end: a label carries a patch
    # of blank paper behind it so the line does not run through the word, and
    # where a label sat near the end of a route that patch took the point off
    # the arrow with it.  Nothing should ever be painted over a tip.
    tips = []
    for pts, arrow in chain_lines(segs):
        head = None
        if reaches_a_shape(pts[-1]) or joins_a_line(pts):
            head, pts = arrow_head(pts)
        d = path_d(pts)
        if d:
            out.append(f'<path class="flow" d="{d}" fill="none"/>')
        if head:
            tips.append(f'<polygon class="head" points="{head}" fill="{settings.INK}" '
                        f'stroke="{settings.INK}" stroke-width="0.6" '
                        'stroke-linejoin="miter"/>')

    for e in elems:
        if e[0] == "line":
            continue
        elif e[0] == "text":                    # Yes / No / Case labels
            _, x, y, s_, anchor = e
            if not s_:
                continue
            tw = text_w(s_, FONT_SIZE, True) + 8  # patch keeps the label off
            bx = {"end": x - tw + 4,            #   whatever line runs behind it
                  "middle": x - tw / 2.0}.get(anchor, x - 4)
            out.append(f'<rect class="patch" x="{bx:.1f}" y="{y - 10:.1f}" '
                       f'width="{tw:.1f}" height="13" fill="{settings.SHEET}" '
                       'stroke="none"/>')
            out.append(f'<text class="label" x="{x:.1f}" y="{y:.1f}" '
                       f'text-anchor="{anchor}" font-weight="bold" '
                       f'stroke="none" fill="{settings.INK}">{html.escape(s_)}</text>')
        elif e[0] == "htext":
            _, x, y, s_, anchor = e
            out.append(f'<text class="heading" x="{x:.1f}" y="{y:.1f}" '
                       f'text-anchor="{anchor}" font-size="13" '
                       f'font-weight="bold" stroke="none" fill="{settings.INK}">'
                       f'{html.escape(s_)}</text>')
        else:
            _, shape, cx, cy, w, h, lines = e[:7]
            said = e[7] if len(e) > 7 else 0
            l, r = cx - w / 2.0, cx + w / 2.0
            t, b = cy - h / 2.0, cy + h / 2.0
            paint = settings.FILL.get(shape, "#ffffff")
            tx, ty = cx, cy                     # where the words go
            # Every shape and the words in it go in a group of their own,
            # named for what kind of thing it is and numbered.  Nothing in
            # the drawing depends on that; it is there so a page showing the
            # chart can pick out one shape, or every shape of one kind, and
            # color it.
            nodes += 1
            out.append(f'<g class="node" data-kind="{shape}" '
                       f'data-i="{said or nodes}">')
            drawn = geom_of(shape)
            out += shape_art(drawn, cx, cy, w, h, paint)
            if drawn == "store":                 # the words clear of the lip
                ty = cy + min(5.0, h * 0.09)
            elif drawn == "offpage":             # clear of the point at the foot
                ty = cy - h * 0.12
            elif drawn == "parallel":            # between the two bars
                ty = cy
            elif drawn == "stored":              # inside the ruled corner
                ty = cy + min(4.0, h * 0.07)
            y0 = ty - (len(lines) - 1) * LINE_H / 2.0 + 4
            for i, line in enumerate(lines):
                out.append(f'<text x="{tx:.1f}" y="{y0 + i*LINE_H:.1f}" '
                           f'text-anchor="middle" stroke="none" fill="{settings.INK}">'
                           f'{html.escape(line)}</text>')
            out.append("</g>")
    out += tips                             # the points of the arrows, on top
    out += ["</g>", "</svg>"]
    return "\n".join(out)



