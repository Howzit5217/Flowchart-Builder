"""Making one chart, start to finish."""
import os

from .. import settings
from ..draw.svg import to_svg
from ..make.legend import with_legend
from ..make.fit import fit_shape
from ..layout.columns import arrange, layout_chart
from ..parse.read import parse_program


def make_flowchart(text, title=None, author=None, max_h=settings.COLUMN_H):
    """Whole program -> one SVG string (every module side by side)."""
    charts = parse_program(text)
    if settings.SHAPE and not max_h:                 # let the shape pick the layout
        return to_svg(fit_shape(charts, settings.SHAPE), title, author)
    layouts = [layout_chart(c, max_h, heading=len(charts) > 1) for c in charts]
    return to_svg(with_legend(arrange(layouts)), title, author)


def make_flowcharts(text, title=None, author=None, max_h=settings.COLUMN_H):
    """Whole program -> [(module name, SVG string), ...], one per module."""
    charts = parse_program(text)
    result = []
    for c in charts:
        if settings.SHAPE and not max_h:             # each module shaped on its own
            elems = fit_shape([c], settings.SHAPE)
        else:
            elems, _, _ = layout_chart(c, max_h, heading=len(charts) > 1)
        name = c.module.name if c.module else "main"
        result.append((name, to_svg(with_legend(elems), title, author)))
    return result


def write_png(svg_path, want):
    """PNG copy if cairosvg is installed (pip install cairosvg); optional."""
    try:
        import cairosvg
    except ImportError:
        if want:
            print("PNG skipped -- run: pip install cairosvg")
        return
    png = os.path.splitext(svg_path)[0] + ".png"
    for scale in (4, 3, 2, 1, 0.5):     # big first: a 4x PNG still reads when
                                        #   you zoom in.  Huge charts step
                                        #   down until cairo accepts one
        try:
            cairosvg.svg2png(url=svg_path, write_to=png, scale=scale)
            print("Wrote " + png)
            return
        except Exception as exc:          # cairo present but its DLLs missing, etc.
            if "SIZE" not in str(exc).upper():
                print("PNG skipped (" + str(exc) + ")")
                return
    print("PNG skipped (chart too large)")


