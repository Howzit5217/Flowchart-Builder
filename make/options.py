"""Everything the command line answers to."""
import argparse

from .. import settings
from ..shapes import DEFAULT_GEOM, SHAPE_ORDER
from ..words import lookup
from ..words.lookup import WORDS


def options():
    """The command line, as something that can read one."""
    ap = argparse.ArgumentParser(description="Pseudocode -> flowchart (SVG).")
    ap.add_argument("infile", nargs="?", help="pseudocode text file "
                                             "(reads standard input if omitted)")
    ap.add_argument("-o", "--out", help="output .svg file")
    ap.add_argument("-t", "--title", help="title drawn at the top")
    ap.add_argument("-a", "--author", help="your name, under the title")
    ap.add_argument("--split", action="store_true",
                    help="write one .svg per module / function")
    ap.add_argument("--for-style", choices=["expand", "hexagon"], default=settings.FOR_STYLE,
                    help="how to draw For loops (default: %(default)s)")
    ap.add_argument("--columns-height", type=float, default=settings.COLUMN_H,
                    help="wrap to a new column past this height "
                         "(default: one column, however tall it comes out)")
    ap.add_argument("--png", action="store_true",
                    help="also write a .png (needs: pip install cairosvg)")
    ap.add_argument("--legend", action="store_true",
                    help="draw a key of the shapes above the chart")
    ap.add_argument("--no-grid", action="store_true",
                    help="leave out the faint grid behind the chart")
    ap.add_argument("--grid-step", type=float,
                    help="spacing of the grid lines (around 20)")
    ap.add_argument("--shape-for", metavar="KIND=settings.SHAPE", action="append",
                    help="draw one kind of step as a different shape, e.g. "
                         "--shape-for io=trap.  Kinds: " +
                         ", ".join(sorted(DEFAULT_GEOM)) + ".  Shapes: " +
                         ", ".join(SHAPE_ORDER))
    ap.add_argument("--lang", default=lookup.LANGUAGE, choices=sorted(WORDS),
                    help="the language the chart and the page are written in "
                         "(default: %(default)s).  The pseudocode keywords "
                         "you type stay as they are")
    ap.add_argument("--site", nargs="?", const="", metavar="DIR",
                    help="write the whole thing out as a website you can "
                         "publish -- on GitHub Pages or anywhere else that "
                         "serves files (default folder: docs)")
    ap.add_argument("--serve", nargs="?", type=int, const=8765,
                    metavar="PORT",
                    help="run the whole thing as a website on this computer "
                         "instead: paste pseudocode, draw it, color it in "
                         "and save it, all in the browser (default port: "
                         "%(const)s)")
    ap.add_argument("--seed", help="draw one exact look again; the script "
                                   "prints the seed it used each time")
    ap.add_argument("--no-variety", action="store_true",
                    help="the same plain drawing every time, instead of one "
                         "that varies a little from run to run")
    ap.add_argument("--shape", default=settings.SHAPE,
                    help="the outline to aim the chart at: auto (default), "
                         "square, wide, page, tall (never reshape), or a "
                         "shape of your own -- 16:9, 1920x1080, 1.4")
    ap.add_argument("--chain-limit", type=float,
                    help="how wide an If / Else If chain may fork before "
                         "the tests queue up down the page instead "
                         "(around 900; 0 always queues them)")
    ap.add_argument("--roomy", action="store_true",
                    help="the older, airier spacing: every gap wider and "
                         "every shape taller, so a bigger chart")
    ap.add_argument("--no-group-output", action="store_true",
                    help="one symbol per Display, instead of one shared by "
                         "a run of them")
    ap.add_argument("--no-page", action="store_true",
                    help="write only the .svg, without the .html page that "
                         "shows it and carries the download links")
    ap.add_argument("--mono", action="store_true",
                    help="plain black and white (this is the default)")
    ap.add_argument("--color", "--colour", action="store_true",
                    help="tint each kind of shape, instead of black and white")
    return ap
