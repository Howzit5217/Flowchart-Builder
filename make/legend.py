"""The key beside the chart."""
from .. import settings
from ..layout.blocks import shift
from ..layout.columns import bbox
from ..measure import FONT_SIZE, text_w
from ..shapes import SWATCH_H, SWATCH_W


# ------------------------------------------------------------------- driver --
def legend_row(elems):
    """A key of the shapes this chart actually uses, laid out in a row.

    Only the shapes that turn up are listed, so a chart with no loops does
    not advertise a loop symbol."""
    present = {e[1] for e in elems if e[0] == "shape"}
    items = [k for k in settings.LEGEND_ORDER if k in present]
    if not items:
        return [], 0.0
    band = SWATCH_H
    out, x = [], 0.0
    for kind in items:
        out.append(("shape", kind, x + SWATCH_W / 2.0, band / 2.0,
                    SWATCH_W, SWATCH_H, [], 0))
        x += SWATCH_W + 9
        name = settings.LEGEND_NAME[kind]
        out.append(("text", x, band / 2.0 + 4, name, "start"))
        x += text_w(name, FONT_SIZE, True) + 28
    return out, band


def with_legend(elems):
    """Put the key above the chart, lined up with its left edge."""
    if not settings.LEGEND:
        return elems
    key, band = legend_row(elems)
    if not key:
        return elems
    minx, miny, _, _ = bbox(elems)
    return shift(key, minx, miny - band - settings.VGAP) + elems



