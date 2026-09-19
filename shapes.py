"""The catalog of shapes, and which kind of step is drawn as which."""
from . import settings


SWATCH_W = 62                       # size of a sample shape in the key
SWATCH_H = 30

# Every shape that can be drawn, and how much room its outline steals from
# the words inside it.  side: what it takes off the width; top: off the
# height; tall: a height of its own, as a multiple of the lines of words.
SHAPES = {
    "rect":    {"side": 20, "top": 0},
    "oval":    {"side": 24, "top": 0, "floor": "oval"},
    "io":      {"side": 2 * 12 + 10, "top": 0},        # parallelogram
    "diamond": {"side": 0, "top": 0, "wide": True},
    "hex":     {"side": 2 * 12 + 10, "top": 0},
    "sub":     {"side": 2 * 6 + 20, "top": 0},         # call, with side bars
    "trap":    {"side": 2 * 12 + 14, "top": 0},        # manual step
    "doc":     {"side": 20, "top": 9},                 # document, wavy foot
    "store":   {"side": 24, "top": 16},                # drum, for a file
    "delay":   {"side": 34, "top": 0},                 # a wait
    "circle":  {"side": 22, "top": 4, "round": True},  # a joining point
    "roundrect": {"side": 24, "top": 0},               # a softer box
    "card":    {"side": 26, "top": 4},                 # a punched card
    "note":    {"side": 28, "top": 4},                 # something noted down
    "docs":    {"side": 24, "top": 14},                # more than one page
    "manual":  {"side": 22, "top": 10},                # typed in by hand
    "screen":  {"side": 36, "top": 0},                 # shown on a screen
    "offpage": {"side": 24, "top": 18},                # carries on elsewhere
    "loop":    {"side": 24, "top": 8},                 # a loop's limit
    "parallel": {"side": 24, "top": 14},               # side by side
    "stored":  {"side": 30, "top": 8},                 # held inside
    "cloud":   {"side": 44, "top": 12},                # a service, elsewhere
    "text":    {"side": 4, "top": 0},                  # words, and no shape
    "actor":   {"side": 18, "top": 30},                # somebody
    "callout":  {"side": 26, "top": 16},               # something said
    "cube":    {"side": 28, "top": 14},                # a thing with sides
    "step":    {"side": 2 * 22 + 8, "top": 0},         # one step of several
    "table":   {"side": 24, "top": 18},                # rows and columns
    "arrow":   {"side": 40, "top": 0},                 # which way it goes
    "io_back": {"side": 2 * 12 + 10, "top": 0},        # the other lean
}
SHAPE_ORDER = ("rect", "roundrect", "oval", "io", "io_back", "diamond",
               "hex", "loop", "sub", "trap", "manual", "doc", "docs", "note",
               "card", "store", "stored", "delay", "screen", "circle",
               "offpage", "parallel", "cloud", "step", "cube", "table",
               "callout", "actor", "text", "arrow")
DEFAULT_GEOM = dict(settings.GEOM)           # the textbook set, to go back to


def geom_of(kind):
    """What a step of this kind is actually drawn as."""
    return settings.GEOM.get(kind, kind if kind in SHAPES else "rect")
