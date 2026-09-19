"""The faint grid behind the chart."""
from .. import settings


def grid_lines(width, height):
    """The faint graph-paper grid that sits behind the chart.

    It is drawn as two ordinary <path>s -- one for the fine lines, one for
    the darker every-fifth line -- rather than as an SVG <pattern>, for the
    same reason the arrowheads are polygons rather than markers: Word and
    PowerPoint quietly drop the clever bit on import, and a path is just a
    line like any other, so every viewer draws it.  Both paths go in before
    anything else, and every shape is filled, so no grid line ever crosses a
    box, a label or a letter."""
    if not settings.GRID or settings.GRID_STEP <= 0:
        return []
    fine, major = [], []
    n, x = 0, 0.0
    while x <= width + 0.01:
        (major if settings.GRID_MAJOR and n % settings.GRID_MAJOR == 0 else fine).append(
            "M%.1f,0V%.1f" % (x, height))
        x += settings.GRID_STEP
        n += 1
    n, y = 0, 0.0
    while y <= height + 0.01:
        (major if settings.GRID_MAJOR and n % settings.GRID_MAJOR == 0 else fine).append(
            "M0,%.1fH%.1f" % (y, width))
        y += settings.GRID_STEP
        n += 1
    out = []
    for name, d, ink, wide in (("fine", fine, settings.GRID_INK, 0.7),
                               ("major", major, settings.GRID_INK_MAJOR, 1.0)):
        if d:
            out.append('<path class="grid %s" d="%s" fill="none" stroke="%s" '
                       'stroke-width="%s"/>' % (name, "".join(d), ink, wide))
    return out


