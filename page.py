"""The page around the chart."""
import html
import json
import re

from . import parts, settings
from .shapes import SHAPE_ORDER
from .studio.web import PYODIDE, needed
from .words import lookup
from .words.lookup import NAMES, WORDS, in_full, word


# --------------------------------------------------------------- the page --
# A small viewer written beside the .svg: the chart on a sheet of paper, with
# a link that saves it.  Two kinds of save, because they are not the same
# thing.  The SVG is the drawing itself -- lines and letters, not pixels --
# so it stays readable however far you zoom in, prints at any size, and drops
# straight into Word.  The PNG is a photograph of it, taken here at whatever
# size you pick, because pixels have to be decided once and for all.
#
# The page carries the chart inside it rather than pointing at the .svg file,
# so it still works if you move it, mail it, or open it from a flash drive,
# and the download links keep working too.
PAGE_HTML = parts.page_html()

# The pseudocode panel, which only the studio gets: the page written beside
# an .svg has no script behind it to redraw anything.
SOURCE_PANEL = parts.read_ui("source-panel.html")

PNG_SIZES = (1, 2, 3, 4, 6, 8)      # the sizes the page's PNG button offers
PNG_FRAMES = ((1920, 1080), (1080, 1080))   # and the fixed picture sizes it
                                    #   fits the chart inside, centered
SHAPE_NAMES = ("auto", "square", "wide", "page", "tall")



def to_page(svg, title=None, name="flowchart", source=None, seed=None,
            web=False):
    """The .svg wrapped in a page that shows it, colors it and saves it.

    Given `source` -- the pseudocode and what it was drawn with -- the page
    comes out as the studio, with the text to edit and a button to draw it
    again.  Without it the page is a standalone thing to keep beside the
    .svg: the chart, the colors, and the two download links, all in the one
    file, so it still works if you move it or mail it.
    """
    body = svg.split("\n", 1)[1] if svg.startswith("<?xml") else svg
    box = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', body)
    size = "%s x %s" % (box.group(1), box.group(2)) if box else ""
    # Which sizes are on offer is settled here.  What each one comes to in
    # pixels is not: the studio redraws the chart without reloading the page,
    # so a number written in now would be the old chart's within a press of
    # the button.  The page writes the words itself, off the chart in front
    # of it, every time that chart changes -- and the menu is shut until it
    # has, so what is put here is never the thing anybody reads.
    options = []
    for mult in PNG_SIZES:
        pick = " selected" if mult == settings.PNG_SCALE else ""
        options.append('      <option value="%d"%s>%d×</option>'
                       % (mult, pick, mult))
    for fw, fh in PNG_FRAMES:
        options.append('      <option value="%dx%d">%d × %d</option>'
                       % (fw, fh, fw, fh))
    heading = title or name
    # The seed is how the same chart is drawn again from the command line;
    # it is of no use to somebody reading the chart, so it is not paraded
    # across the top of it.
    sub = word("flowchart") + (" · %s px" % size if size else "")

    panel = ""
    if source is not None:
        picks = "".join(
            '<option value="%s"%s>%s</option>'
            % (key, " selected" if key == (source.get("shape") or "auto") else "",
               html.escape(word("shape_" + key))) for key in SHAPE_NAMES)
        tongues = "".join(
            '<option value="%s"%s>%s</option>'
            % (code, " selected" if code == lookup.LANGUAGE else "",
               html.escape(NAMES.get(code, code)))
            for code in sorted(WORDS))
        panel = (SOURCE_PANEL
                 .replace("__LANGS__", tongues)
                 .replace("__SHAPES__", picks)
                 .replace("__T__", html.escape(source.get("title") or "", True))
                 .replace("__A__", html.escape(source.get("author") or "", True))
                 .replace("__CODE__", html.escape(source.get("code") or "")))

    # Which languages travel with the page.  The studio carries them all,
    # because it has a picker and can change its own words without asking
    # anybody for a new page.  A viewer written beside an .svg has no
    # picker -- the panel that holds one is the studio's -- so it carried
    # three languages it could never show, forty-odd kilobytes of them, in
    # every file anybody saved.  Now it carries the one it is written in.
    codes = sorted(WORDS) if source is not None else [lookup.LANGUAGE]
    every = dict((code, in_full(code)) for code in codes)
    said = every.get(lookup.LANGUAGE) or in_full("en")
    page = re.sub(r"__W\((\w+)\)__",
                  lambda m: html.escape(word(m.group(1))),
                  PAGE_HTML.replace("__SOURCE__", panel))
    return (page
            .replace("__ALLWORDS__", json.dumps(every, ensure_ascii=False))
            .replace("__WORDS__", json.dumps(said, ensure_ascii=False))
            .replace("__LANG__", lookup.LANGUAGE)
            .replace("__PYODIDE__", PYODIDE)
            .replace("__PYFILES__", json.dumps(needed() if web else []))
            .replace("__SHAPELIST__", json.dumps(list(SHAPE_ORDER)))
            .replace("__TITLE__", html.escape(heading))
            .replace("__HEADING__", html.escape(heading))
            .replace("__SUB__", html.escape(sub))
            .replace("__FILE__", html.escape(name, quote=True))
            .replace("__OPTIONS__", "\n".join(options))
            .replace("__MODE__", "web" if web else
                     ("studio" if source is not None else "page"))
            .replace("__JSNAME__", json.dumps(name))
            .replace("__SVG__", body))


def empty_chart():
    """What the studio shows before there is anything to show."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="430" height="150" '
            'viewBox="0 0 430 150"><rect class="sheet" width="100%" '
            'height="100%" fill="#ffffff"/><text x="215" y="78" '
            'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
            'font-size="13" fill="#5d6b7a">'
            + html.escape(word("empty_chart")) + "</text></svg>")
