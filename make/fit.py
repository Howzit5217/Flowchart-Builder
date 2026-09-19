"""Picking the layout whose outline fits best."""
import math
import re

from .. import settings
from ..draw.arrows import chain_lines
from ..make.legend import with_legend
from ..layout.columns import (arrange, bbox, forget_layouts,
                              keep_layouts, layout_chart)


def shape_target(spec):
    """What --shape asked for, as a width / height ratio.

    Takes a name (square, wide, page, screen), a ratio (16:9, 4x3), a size
    (1920x1080) or a plain number.  Anything it cannot read falls back to
    the middling shape, which is what "auto" aims at."""
    key = str(spec or "").strip().lower()
    named = {"square": 1.0, "wide": 16 / 9.0, "screen": 16 / 9.0,
             "16:9": 16 / 9.0, "page": 8.5 / 11.0, "auto": settings.AUTO_SHAPE}
    if key in named:
        return named[key]
    m = re.match(r"^(\d+(?:\.\d+)?)\s*[x:/ ]\s*(\d+(?:\.\d+)?)$", key)
    if m and float(m.group(2)):
        return float(m.group(1)) / float(m.group(2))
    try:
        return max(0.05, float(key))
    except ValueError:
        return settings.AUTO_SHAPE


def wander(elems, span):
    """How far the longest single arrow runs, against the size of the whole
    chart.  A chart whose arrows go from one shape to the next scores near
    nothing; one with a route that goes right round the outside scores
    most of 1.  Only the part past a fair allowance counts: a loop has to
    reach back over its own body, and that is not the layout's fault."""
    lines = [e for e in elems if e[0] == "line"]
    if not lines or span <= 0:
        return 0.0
    longest = 0.0
    for pts, _ in chain_lines(lines):
        run = sum(math.hypot(q[0] - p[0], q[1] - p[1])
                  for p, q in zip(pts, pts[1:]))
        longest = max(longest, run)
    return max(0.0, longest / span - 0.45)


def fit_shape(charts, spec):
    """Lay the program out several ways and keep the best-shaped one.

    A flowchart has no one size: the same program is a narrow ribbon if
    every test queues up down the page, a broad sheet if they fork into
    lanes, and anything between if the chart is wrapped into columns.  None
    of that changes a single shape or word -- only the outline the whole
    thing makes.  That outline is worth choosing, because a chart is looked
    at inside something: a screen, a page, an image box.  Whatever room is
    left over when the chart is scaled to fit is room the lettering could
    have had, so the closer the chart sits to the shape of the frame, the
    bigger the words come out in it.

    So: try the layouts, score each on how far its shape falls from the one
    asked for, and take the best.  Wrapping into columns is charged for as
    it goes, because every column after the first costs an arrow that
    climbs the one it leaves; a shape has to be a good deal better before
    it is worth another column.
    """
    keep = (settings.CHAIN_LIMIT, settings.MAX_ROW_W)
    target = shape_target(spec)
    head = len(charts) > 1

    def build(max_h, chain, row_w):
        settings.CHAIN_LIMIT, settings.MAX_ROW_W = chain, row_w
        elems = with_legend(arrange([layout_chart(c, max_h, heading=head)
                                     for c in charts]))
        x0, y0, x1, y1 = bbox(elems)
        return elems, x1 - x0, y1 - y0

    try:
        keep_layouts()          # `charts` is held right through, so it is safe
        chains = sorted({keep[0], 0.0, 1e9})       # queue up / as set / fork
        rows = sorted({keep[1], 900.0, 2400.0, 4000.0}) if head else [keep[1]]
        # Laying the program out is nearly all of the cost of drawing it, so
        # these three are kept whole rather than measured and thrown away.
        # They were being built twice over: once here, and once again by the
        # scoring loop below, which asks for exactly the same three among
        # its candidates -- and a third time by the early return, which
        # rebuilt the very layout it had just measured.
        plain = {}                                 # one column, per chain style
        for chain in chains:
            plain[chain] = build(0, chain, keep[1])
        natural = plain[keep[0]]
        if str(spec).strip().lower() == "auto" \
                and settings.AUTO_KEEP[0] <= natural[1] / natural[2] <= settings.AUTO_KEEP[1]:
            return natural[0]                      # already a sensible shape

        tallest = max(h for _, _, h in plain.values())
        # Columns are the one layout that cannot be routed tidily: the arrow
        # into a column climbs the whole one it leaves and runs back over the
        # top of the chart.  So auto never reaches for them -- it picks the
        # best-shaped of the layouts that read cleanly -- and a shape asked
        # for by name only gets them when they earn COLUMN_COST.
        steps = [0.0]
        if str(spec).strip().lower() != "auto":
            steps += [tallest * (0.92 ** i) for i in range(1, 26)]
        best, best_score = None, None
        for chain in chains:
            for row_w in rows:
                last = None            # the layout the last limit produced
                for max_h in steps:
                    if max_h and max_h < 240:
                        continue
                    # A ceiling no lower than the height the chart already
                    # came out at cannot make it wrap any differently, so
                    # the layout it would produce is the one in hand.  The
                    # ladder steps down in twelfths and most of its rungs
                    # land inside a column count that has not changed; each
                    # of those used to be a whole layout, built from the top
                    # to prove it was the same as the last.  Only the
                    # building is skipped -- the candidate is still scored
                    # and can still win, so the chart that comes out, and
                    # the one a --seed draws, are exactly what they were.
                    if not (max_h and last and max_h >= last[2]):
                        last = (plain[chain]
                                if not max_h and row_w == keep[1]
                                else build(max_h, chain, row_w))
                    elems, w, h = last
                    cols = max(1.0, round(plain[chain][2] / h)) if h else 1.0
                    score = (abs(math.log((w / h) / target))
                             + settings.COLUMN_COST * (cols - 1))
                    if settings.SHAKE is not None:       # a nudge, so two runs of the
                        score += settings.SHAKE.uniform(0, 0.05)   # same file differ
                    # How far the arrows run is the dear part of the score:
                    # it means gluing every segment of the chart back into
                    # routes, over and over, for layouts most of which are
                    # not in the running.  It can only ever mark a layout
                    # down, so a layout already no better than the best one
                    # without it cannot win, and is not measured.  The nudge
                    # is drawn first either way, so a --seed still lands on
                    # the chart it always did.
                    if (settings.ROUTE_COST >= 0 and best_score is not None
                            and score >= best_score - 1e-9):
                        continue
                    score += settings.ROUTE_COST * wander(elems, w + h)
                    if best_score is None or score < best_score - 1e-9:
                        best, best_score = elems, score
        return best
    finally:
        settings.CHAIN_LIMIT, settings.MAX_ROW_W = keep
        forget_layouts()

