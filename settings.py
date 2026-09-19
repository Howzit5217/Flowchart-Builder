"""Every knob, in one place.

Read them as `settings.NAME`, never by importing the name itself.  That is
not a style rule, it is what makes them work: --seed shakes a dozen of these
before a chart is drawn, --roomy replaces seven, the studio sets four per
request, and a name imported by value would be a copy of whatever it was
when the module was first read.  One module holds them, one module rewrites
them, and everything else is looking at the same copy.
"""
AUTHOR = ""                         # only what the studio's name box starts
                                    #   with; it remembers what you type
STUDIO = True                       # the studio opens when there is nothing
                                    #   on the command line to draw.  False:
                                    #   ask for pseudocode in the terminal

# ---------------------------------------------------------------- settings --
YES = "True"                        # decision labels; use "Yes" / "No"
NO = "False"                        #   if that is what your class uses
FOR_STYLE = "expand"                # "expand": init box + test diamond + step box
                                    # "hexagon": one hexagon for the whole For
SPLIT_MODULES = False               # True: write one .svg per module / function
MAX_ROW_W = 1600                    # charts go left-to-right; wrap past this width
CHART_GAP = 60                      # space between two charts

SHEET = "#ffffff"                   # the paper the chart is drawn on
INK = "#000000"                     # every outline, arrowhead and letter
FILL = {                            # only read when --color is given: charts
    "oval": "#dbeafe",              #   are black and white by default now
    "rect": "#ffffff",
    "io": "#eaf5ff",
    "diamond": "#fff4d6",
    "hex": "#fff4d6",
    "sub": "#f1e7ff",
}
TINTS = dict(FILL)                  # kept, because --mono paints over
                                    #   FILL and the studio can ask for the
                                    #   tints back without a restart
LEGEND_NAME = {                     # what the key calls each shape
    "oval": "Start / End",
    "rect": "Process",
    "io": "Input / Output",
    "diamond": "Decision",
    "hex": "Loop",
    "sub": "Call a module",
}
LEGEND_ORDER = ("oval", "rect", "io", "diamond", "hex", "sub")

# Which shape draws which kind of step.  The keys are what a step *is* --
# a decision, an input, a call -- and the values are what gets drawn for it.
# Left alone each kind is drawn the way a textbook draws it; change one and
# every step of that kind changes with it, in the chart and in the key.  The
# meaning does not move: a decision is still a decision, whatever it looks
# like, and the page still colors by kind.
GEOM = {"oval": "oval", "rect": "rect", "io": "io",
        "diamond": "diamond", "hex": "hex", "sub": "sub"}


NODE_W = 132                        # standard box width
NODE_MAX_W = 186                    # boxes may grow this wide before the words
                                    #   wrap onto another line, so a long
                                    #   Display never runs out in one long line
NODE_MIN_H = 32
OVAL_W = 96
OVAL_H = 36
DIA_W = 132                         # decision diamond
DIA_MIN_H = 48
PAD_Y = 9                           # vertical padding inside a shape
SLANT = 12                          # parallelogram / hexagon slant
BAR = 6                             # inset of the double bars on a Call box

VGAP = 20                           # a whole grid step, so shapes line up                           # vertical arrow length between shapes
HGAP = 24                           # horizontal breathing room for branches
LABEL_PAD = 12                      # room a True / False label needs beside
                                    #   the diamond it belongs to
LOOP_UP = 20                        # room above a loop for the loop-back arrow

HEAD_LEN = 10                       # arrowhead: how far back from the point
HEAD_WIDE = 8                       #   and how wide across its base
TRUE_LEFT = True                    # True leaves a diamond on the left
                                    #   hand and False on the right; variety
                                    #   swaps them over now and then
VARIETY = True                      # shake the drawing up a little from one
                                    #   run to the next: the same pseudocode,
                                    #   drawn a little differently.  Nothing
                                    #   it varies changes what the chart says
SEED = None                         # a number here pins one of those looks
                                    #   down, so you can have it back
SHAKE = None                        # the run's own source of randomness, set
                                    #   by style_variety(); None = no shaking

SHAPE = "auto"                      # the outline the whole chart aims at:
                                    #   auto, square, wide (16:9), page,
                                    #   tall (never reshape), a ratio like
                                    #   16:9, a size like 1920x1080, or a
                                    #   plain number
AUTO_SHAPE = 1.25                   # what auto aims at: between a square
                                    #   and a 16:9 frame
AUTO_KEEP = (0.5, 2.2)              # auto leaves a chart alone while its
                                    #   shape is already inside this
ROUTE_COST = 0.8                    # and how much a layout is marked down
                                    #   for arrows that go the long way
                                    #   about, so that two layouts of much
                                    #   the same shape are settled by which
                                    #   one is easier to follow
COLUMN_COST = 0.22                  # how much better a shape has to be to
                                    #   be worth another column, in log
                                    #   ratio: every one costs an arrow
                                    #   that climbs the column it leaves

CHAIN_LIMIT = 900                   # an If / Else If / Else chain forks
                                    #   into a lane per branch while that
                                    #   stays under this wide; past it the
                                    #   tests queue up down the page instead
FORK_LIMIT = 320                    # an If with no Else forks both ways like
                                    #   any other decision, unless sending
                                    #   its true branch out to a lane of its
                                    #   own would cost a line longer than
                                    #   this; then the branch keeps the axis
                                    #   and only the False side steps aside
CORNER_R = 7                        # how much an elbow corner is rounded

LEGEND = False                      # True: draw a key of the shapes used
MONO = True                         # plain black and white; pass --color to
                                    #   put the old tints back

GROUP_OUTPUT = True                 # a run of Display lines shares one
GROUP_MAX = 5                       #   symbol, up to this many lines, the
                                    #   way a run of Declares already does
ROOMY = dict(VGAP=30, HGAP=30, PAD_Y=11, NODE_MIN_H=38, DIA_MIN_H=60,
             DIA_W=150, LOOP_UP=24)  # the airier old spacing: --roomy

GRID = True                         # faint graph-paper grid behind the chart
GRID_STEP = 20                      # spacing of the fine grid lines, in px
GRID_MAJOR = 5                      # every fifth line is a shade darker
GRID_INK = "#e7ebf0"                # the fine lines
GRID_INK_MAJOR = "#d8dfe8"          # the every-fifth line
PAGE = True                         # also write a small .html viewer beside
                                    #   the .svg, with download links on it
PNG_SCALE = 4                       # the page's PNG button starts at 4x size

MARGIN = 24
COL_GAP = 72                        # gutter between two columns of one chart
COLUMN_H = 0                        # 0: one column, however tall that comes
                                    #   out.  Set a height (or pass
                                    #   --columns-height) to wrap the chart
                                    #   into columns instead -- but every
                                    #   wrap costs an arrow that climbs the
                                    #   whole column it leaves
TITLE_H = 44
HEADING_H = 28                      # room for a module's heading above its chart
