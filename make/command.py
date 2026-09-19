"""The command line."""
import os
import pathlib
import sys
import webbrowser

from .. import settings
from ..make.chart import make_flowchart, make_flowcharts, write_png
from ..make.options import options
from ..make.shake import style_variety
from ..page import to_page
from ..parse.trouble import PROBLEMS
from ..shapes import SHAPES
from ..studio.serve import serve
from ..studio.site import write_site
from ..words.lookup import apply_language, word


def main():
    ap = options()
    args = ap.parse_args()
    apply_language(args.lang)
    for pair in (args.shape_for or []):
        kind, _, drawn = pair.partition("=")
        if kind.strip() in settings.GEOM and drawn.strip() in SHAPES:
            settings.GEOM[kind.strip()] = drawn.strip()
        else:
            print(word("odd_shape", pair=pair))
    settings.FOR_STYLE = args.for_style
    settings.LEGEND = args.legend or settings.LEGEND
    settings.GROUP_OUTPUT = settings.GROUP_OUTPUT and not args.no_group_output
    off = ("tall", "off", "none", "")
    settings.SHAPE = "" if str(args.shape).lower() in off else args.shape
    settings.GRID = settings.GRID and not args.no_grid
    settings.PAGE = settings.PAGE and not args.no_page

    # The varied look goes on first and anything named on the command line
    # over the top of it, so asking for one thing by hand does not hand the
    # rest of the drawing back to the defaults.
    settings.VARIETY = settings.VARIETY and not args.no_variety
    seed = args.seed if args.seed is not None else settings.SEED
    if seed is not None:
        try:
            seed = int(seed)
        except ValueError:                      # a word for a seed is fine
            seed = sum(ord(c) * (i + 7) for i, c in enumerate(str(seed)))
    if settings.VARIETY or seed is not None:
        seed = style_variety(seed)
    if args.roomy:                      # put the old spacing back
        # Into the settings, not into this file: they are the settings'
        # names, and everything that reads them is reading them there.
        vars(settings).update(settings.ROOMY)
    if args.chain_limit is not None:
        settings.CHAIN_LIMIT = args.chain_limit
    if args.grid_step is not None:
        settings.GRID_STEP = args.grid_step
    if not args.color and (args.mono or settings.MONO):
        for shape in settings.FILL:
            settings.FILL[shape] = "#ffffff"

    title, author = args.title, args.author
    here = os.path.dirname(os.path.abspath(__file__))
    split = args.split or settings.SPLIT_MODULES

    if args.site is not None:           # a website to put somewhere
        write_site(args.site or os.path.join(here, "docs"))
        return

    start = ""
    if args.infile:
        with open(args.infile, encoding="utf-8-sig") as f:
            start = f.read()
    elif args.serve is None and not sys.stdin.isatty():
        # Something piped in is something to draw, so it is read.  Asking
        # for --serve is not: the pseudocode is going to be typed in the
        # browser.  And anything started without a terminal behind it -- a
        # shortcut, a scheduled task, an editor's run button -- hands this a
        # pipe that nobody ever writes to and nobody ever closes, so reading
        # it waited here for good and the studio never opened at all.  A
        # file still starts it off: --serve alongside one is read above.
        start = sys.stdin.read()

    # A file, or something piped in, is drawn where it stands.  With neither
    # there is nothing here to draw -- the pseudocode lives in the browser
    # now -- so the studio opens instead.
    if args.serve is not None or (not start.strip() and settings.STUDIO):
        serve(args.serve if args.serve is not None else 8765,
              start, title, author or settings.AUTHOR)
        return
    if not start.strip():
        print(word("nothing"))
        return

    text = start
    if args.infile:
        default_out = os.path.splitext(args.infile)[0] + ".svg"
    else:
        default_out = os.path.join(here, (title or "flowchart") + ".svg")

    if not text.strip():
        print(word("nothing"))
        return

    out = args.out or default_out
    charts = []                            # [(path, svg, heading), ...]
    if split:
        base = os.path.splitext(out)[0]
        for name, svg in make_flowcharts(text, title, author,
                                         args.columns_height):
            charts.append(("%s_%s.svg" % (base, name), svg,
                           "%s — %s" % (title, name) if title else name))
    else:
        charts.append((out, make_flowchart(text, title, author,
                                           args.columns_height), title))

    if seed is not None:
        print(word("style_seed", seed=seed))
    # What the reading had to paper over.  A chart came out either way, but
    # a chart drawn around an If that nobody closed is not the chart that
    # was meant, and this is the only place that says so.
    if PROBLEMS:
        print(word("w_found", n=len(PROBLEMS)))
        for bit in PROBLEMS:
            print("  %s" % bit["says"])
    written, pages = [], []
    for path, svg, heading in charts:
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        written.append(path)
        print(word("wrote", path=path))
        if settings.PAGE:                      # the viewer, with the download links
            page = os.path.splitext(path)[0] + ".html"
            name = os.path.splitext(os.path.basename(path))[0]
            with open(page, "w", encoding="utf-8") as f:
                f.write(to_page(svg, heading, name, seed=seed))
            pages.append(page)
            print(word("wrote", path=page) + "  " + word("open_this"))
        write_png(path, args.png)

    if not args.infile and sys.stdin.isatty():        # opened from Run button
        show = (pages or written)[0]                  # the page, if there is
        webbrowser.open(pathlib.Path(show).absolute().as_uri())


