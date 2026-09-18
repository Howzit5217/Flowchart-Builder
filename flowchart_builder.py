#!/usr/bin/env python3
"""
flowchart.py -- turn textbook-style pseudocode into a flowchart.

This file is built, not written: it is the parts in src/ joined together by
build.py, so that what gets run or published is one file with nothing to
lose, while the work happens in pieces an editor can help with -- the page
in .html, its styling in .css, its script in .js, the Python in parts named
for what they do.  Change src/, run "python build.py", and this file is
written out again.  Changing this file directly works too; just know that
the next build will write over it.  src/README.md says what is where.

Usage:
    python flowchart.py                     the studio, in your browser
    python flowchart.py pseudocode.txt      one file, straight to .svg
    python flowchart.py pseudocode.txt -o mychart.svg -t "Tip Calculator"
    python flowchart.py --site docs         a website you can publish
    python flowchart.py pseudocode.txt --split          (one .svg per module)

There is no pseudocode in this file.  Run it with nothing after it and the
studio opens in your browser: paste the pseudocode there, press the button,
color the chart in and save it.  What you type is kept by the browser, not
by this script.  Give it a file instead and it goes straight to .svg, the
way it always did.

Run it with --site and it writes the whole thing out as a website -- a page,
a copy of this script, and a readme -- that works on any host that serves
files and runs nothing, GitHub Pages included.  The page loads Python into
the browser (Pyodide) and imports the copy, so the drawing is done by this
same code: there is one flowchart builder, not two.

The input is plain text, one pseudocode statement per line.  Lines may start
with '#' (so you can keep the pseudocode as comments inside a .py file), and
anything after // or # on a line is treated as a comment and ignored.  A
statement that ends with a comma, an operator, or an unclosed parenthesis is
joined with the next line.

Recognized statements (keywords are not case sensitive)
--------------------------------------------------------
    Start / End / Stop                      ovals (added automatically if missing)
    Declare <type> <name>  /  Constant ...  rectangle (consecutive ones are grouped)
    Display "..." , var  /  Print  /  Output parallelogram (consecutive
                                            ones are grouped, up to five)
    Input <var>  /  Read  /  Get            parallelogram
    Set <var> = <expr>  /  <var> = <expr>   rectangle
    Call <module>(args)                     rectangle with double side bars
    Return  /  Return <value>               oval (ends the flow)
    If <cond> Then ... Else If ... Else ... End If        diamond(s)
    If <cond> Then <statement>              one-line If
    While <cond> ... End While              diamond, test before the body
    Do ... While <cond>                     diamond, test after the body
    Do ... Until <cond>   /  Repeat ... Until <cond>
    Do While <cond> ... Loop                (also Do Until ... Loop, Wend, End Loop)
    For <var> = a To b [Step s] ... End For init box, test diamond, increment box
    For (init; test; step) ... End For      (also Next, End For, End Loop)
    Select <expr> / Case v: / Default: / End Select   multi-way diamond
    Module name(params) ... End Module      each module gets its own flowchart
    Function <type> name(params) ... End Function

Python-style text (def / if / elif / else / while / for with a colon and no
End lines) also works: there, indentation closes the blocks.

Anything else becomes a plain rectangle, and a missing End If / End While /
End Module is closed automatically, so the script never gives up on a file.

Lines meet shapes at the side when that is the plain way round.  A route
setting off sideways -- a loop-back, or a branch stepping out to the line
that takes it home -- leaves the side of the box it starts from instead of
dropping clear of the bottom and then turning.  A route arriving sideways
goes into the side it arrives at: an answer to a question runs straight out
of the diamond and into the box that answer leads to, with the box set
level with the middle of the diamond so that there is no corner in between
at all.  Each of those is a turn saved and a shorter line, and a straight
line from a question to what it leads to is about as easy to follow as a
chart gets.

Two things are still met over the top, for good reason.  A test -- a
diamond or a hexagon -- keeps its sides for its own answers, so a line
arriving at one comes in above it.  And where a branch or a body does not
begin or end on a box at all, because what sits at the head or foot of an
If or a loop is the point where two routes meet, a line has no side to aim
at and leaves or arrives from above or below, as it did before.

Every shape is joined to the next by a drawn arrow.  Nothing is ever left
hanging: there are no lettered "skip to" tiles standing in for a line that was
too long to draw, and no route stops in mid-air.  An arrowhead lands either on
a shape or on the line a branch is rejoining, pointing at it.  The one place a
head is left off is where two paths meet each other nose to nose -- the two
sides of an If coming back together -- because two heads at one point read as a
collision; there the single arrow leaving the meeting says where it goes.

The same program can be drawn in several outlines without moving a single
shape or changing a word.  A chain of tests -- If / Else If / Else If /
Else -- either forks into a lane per branch, which is broad and short, or
queues up down the page, each test under the last, which is narrow and
tall; and any chart can be wrapped into columns, which trades height for
width again.  None of that is about the program.  It is about the outline
the whole thing makes.

That outline is worth choosing, because a chart is always looked at inside
something: a screen, a page, an image box.  Whatever room is left over when
the chart is scaled to fit the frame is room the lettering could have had,
so the closer the chart sits to the shape of the frame, the bigger the
words come out.  A ribbon of a chart in a 16:9 picture is mostly white
paper with unreadable print down the middle of it.

So --shape says what to aim at and the layouts are tried against it:

    auto (default)  a good middling shape, between a square and a screen.
                    A chart already sitting comfortably is left alone
    square          as near 1:1 as the chart can manage
    wide            16:9 -- for a slide, or a 1920x1080 picture
    page            upright, the shape of a sheet of paper
    tall            no reshaping: one column, chains down the page
    16:9  1920x1080  1.4        a shape of your own

Columns are the one layout here that cannot be routed tidily.  The arrow
into a new column has to climb the whole column it leaves and run back over
the top of the chart, past everything in between, and two or three of those
are what make a chart look like it has been scribbled over.  So auto never
reaches for them: it takes the best-shaped of the layouts that read cleanly,
and if that is a tall chart, a tall chart is what you get.  A shape asked
for by name may still use them -- that is the only way a tall program ever
fills a wide frame -- and then they are charged for as they go, and a
column is never left holding a stub, because an End sitting alone at the
head of an empty lane helps nobody.

An If forks: True leaves the left point of the diamond, False leaves the right,
and the two meet again on the line below, so the two outcomes read as two paths
of equal standing.  An If with no Else forks the same way when its true branch
is small.  When that branch is a big one the branch keeps the line it was
already on and only False steps aside, because forking there would cost an
arrow as long as the whole branch is wide and buy nothing: with only one branch
to look at there is nothing to be even-handed about.

Two runs of the same file do not draw quite the same chart.  Every gap,
the air inside a box, how round a corner is, how fine the grid is, which
hand True goes out on, where a chain of tests stops forking and starts
queueing -- all of that is shaken a little each time, so the same
pseudocode comes out as the same program drawn a different way.  Nothing a
reader leans on moves: the lettering stays the size it was, every shape
still means what it means, and no arrow goes anywhere different.  The
script prints the seed it used; pass it back with --seed to get that exact
chart again, or --no-variety for the same plain drawing every time.

Charts are kept as small as they can be while still reading cleanly: the
gaps are only as long as an arrow needs to be seen, and a run of statements
that says one thing -- a block of Declares, the four Displays of a menu --
shares one symbol instead of taking one each.  Together that is about a third
off the size of the page, with nothing dropped and no lettering shrunk: the
words are the same size they always were, which is what has to stay readable
when the chart is scaled down to fit a page.  Pass --roomy for the old
spacing, --no-group-output to give every Display a symbol of its own.

Behind the chart is a faint grid, like the graph paper the shapes would have
been drawn on by hand.  It is there to rest the eye on and to show how far
apart things are; it never crosses a box or a word, because every shape is
filled.  Pass --no-grid for a plain white background.

Charts are black and white, and they run in one column, however tall that comes
out.  A flowchart is a tall thing by nature; wrapping it into columns only buys
a shorter page by adding an arrow that has to climb the whole column it leaves
and cross back over the top of the chart.  Pass --columns-height if you want
that trade anyway.

Options worth knowing:
    --legend        draw a key of the shapes above the chart
    --color         tint each kind of shape (black and white is the default)
    --split         one .svg per module / function
    --for-style     expand (default) or hexagon, for For loops
    --columns-height   wrap into columns past this height (off by default)
    --serve         run the whole thing as a website on this computer
    --lang          en, es, fr or de: the language the chart and the page
                    are written in.  The pseudocode keywords you type stay
                    as they are
    --shape         the outline to aim at: auto, square, wide, page, tall,
                    or your own -- 16:9, 1920x1080, 1.4
    --seed          draw one exact look again (the seed is printed each run)
    --no-variety    the same plain drawing every time
    --chain-limit   how wide an If / Else If chain may fork before its
                    tests queue up down the page instead (900 by default;
                    --shape overrules this while it is looking for a fit)
    --roomy         the older, airier spacing (a chart about a third bigger)
    --no-group-output  one symbol per Display, not one for a run of them
    --no-grid       plain white behind the chart, no grid
    --grid-step     how far apart the grid lines sit (20 by default)
    --no-page       just the .svg, without the .html viewer beside it

Two files come out: the chart itself as <name>.svg, and <name>.html, a page
that shows it, lets you color it in, and saves it.  The page is the one
that opens.

The studio has two ways of working.  *From pseudocode* is the one this
script has always done: you type it, the layout works out where everything
goes.  *By hand* is for when you want to put the shapes where you want
them: add a shape, drag it about, join it to the next one, and write in it.

Shapes in that mode are yours to do what you like with: two dozen to pick
from -- the six a textbook uses, and the rest of the ones that turn up in
the back of the chapter: a document and a stack of them, a drum, a card, a
tape, a note, a wait, a screen, triangles, junctions, an arrow -- each one
resizable, turnable and colorable on the spot, and removable with the
Delete key.

Shapes are joined by dragging from the handle on a selected one onto
another, or with the Connect button.  An arrow is a thing in its own right
once it is there: click it to give it a word, a colour, a thickness, a
dashed line or no head at all, or to turn it round.  The right mouse button
opens a short menu on whatever is under it -- a shape, an arrow, or the
paper.

A design can be kept: the file button writes everything down -- the shapes,
the arrows, the colors, the pseudocode, which shape draws which kind of
step -- as one small .flowchart.json, and opening it here puts you back
where you were.

The pseudocode side gets a say in shapes too: under *Shape for each kind*
you choose which shape is drawn for each kind of step, so Input / Output
can be a document instead of a parallelogram, or a decision a hexagon.
What the step *means* does not move -- a decision is still a decision, the
key still says so, and the colours still group by kind -- only what it is
drawn as.  On the command line that is --shape-for io=doc.

Double-click a shape to type in it.  In a chart you drew by hand the words
are edited in the shape itself; in one built from pseudocode the line it
came from is picked out in the pseudocode box, because that is where those
words actually live.

What "by hand" adds is a check.  Press it and it goes over the design the
way a marker would: is there one place it starts, and something that ends
it; does everything have a way in and a way out; does each decision have
two ways out, labelled differently; can every shape be reached; and -- the
one that matters -- can an End be reached from everywhere, or is there a
loop the flow gets into and can never leave.  It also says when a line runs
straight through a shape.  Each thing it finds points at the shape it means.

*Run it* does what no drawing can: it runs the program.  It walks the
chart, lighting up the shape it is on, asking for whatever the program asks
a person for, printing what it prints, and stopping to say so if the flow
gets into a loop it never comes out of.  That is the test of whether the
logic works -- not whether it looks like a flowchart, but whether it does
what it is supposed to do.

Set the language beside it -- Python, Java, C# or JavaScript -- and *As
code* writes the same program out in that language, ready to copy or save:
the declarations, the loops, the ifs, the input and output, and each module
as a function.  It is the same program the runner just ran, which is the
point: what you watched happen is what the code does.

On that page: click any shape to give that one a fill, an outline and a
color of words of its own, or set a whole kind at once -- every decision
diamond, every input -- from the Shapes list.  Six palettes set the lot in
one click, and the lines, the words, the paper and the grid have their own
colors too.  Whatever you change is what gets saved: both downloads take
the chart as it looks on the page, drawn from pseudocode or by hand alike.
The page itself is light or dark, following the computer unless the button
in the corner is told otherwise.

Run it with --serve (or set STUDIO = True and press Run) and the whole
thing is a small website on this computer instead: paste pseudocode into
the panel, press the button, and the same code that writes the .svg draws
it in the browser, where you can color it and save it.  Nothing leaves the
machine -- the server listens to this computer only.

Save from the page either way:

    SVG   the drawing itself -- lines and letters, not pixels -- so it stays
          sharp however far you zoom in, prints at any size, and goes into
          Word (Insert > Pictures > This Device; Word 2016 and newer read
          SVG).  This is the copy worth keeping.
    PNG   an ordinary picture, made in your browser at up to eight times
          size, for anywhere that will not take an SVG.  Pick the size
          before you save it: a picture cannot be sharpened afterwards.
          The list also holds 1920 x 1080 and 1080 x 1080, which fit the
          chart inside that exact picture size and center it.

The page carries the chart inside it, so it still works if you move it, mail
it, or open it from a flash drive.  Arrowheads are drawn as ordinary filled
shapes rather than SVG markers, which Word and PowerPoint quietly throw away
on import.
"""

import argparse
import collections
import html
import io
import json
import math
import os
import pathlib
import random
import re
import sys
import webbrowser

# =============================================================================
#  There is no pseudocode in this file.  It is typed into the website: run
#  the script with no arguments and the studio opens in your browser, where
#  you paste it, press the button, color it in and save what comes out.
#  What you type stays in your browser, not in here.
#
#      python "Flowchart Builder.py"               the studio
#      python "Flowchart Builder.py" code.txt      one file, straight to .svg
#      python "Flowchart Builder.py" --site docs   a website to publish
# =============================================================================

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

FONT = "Arial, Helvetica, sans-serif"
FONT_SIZE = 11
LINE_H = 13
CHAR_W = FONT_SIZE * 0.55          # only a fallback: see text_w() below

# Arial advance widths in thousandths of an em, for characters 32 to 126.
# Measuring with the real numbers rather than one average width means a box
# comes out exactly as wide as the words in it -- a line of capitals is
# nearly a quarter wider than the average, and used to run over the outline.
_ADV_N = (
    278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333,
    278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278,
    584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278,
    500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944,
    667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
    278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500,
    278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584)
_ADV_B = (
    278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333,
    278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333,
    584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278,
    556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944,
    667, 667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 611, 556,
    333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556,
    333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584)


def text_w(s, size=None, bold=False):
    """How wide s really comes out, in pixels."""
    table = _ADV_B if bold else _ADV_N
    total = 0
    for ch in s:
        i = ord(ch) - 32
        total += table[i] if 0 <= i < len(table) else 556
    return total * (FONT_SIZE if size is None else size) / 1000.0

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

SWATCH_W = 62                       # size of a sample shape in the key
SWATCH_H = 30

# Which shape draws which kind of step.  The keys are what a step *is* --
# a decision, an input, a call -- and the values are what gets drawn for it.
# Left alone each kind is drawn the way a textbook draws it; change one and
# every step of that kind changes with it, in the chart and in the key.  The
# meaning does not move: a decision is still a decision, whatever it looks
# like, and the page still colours by kind.
GEOM = {"oval": "oval", "rect": "rect", "io": "io",
        "diamond": "diamond", "hex": "hex", "sub": "sub"}

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
DEFAULT_GEOM = dict(GEOM)           # the textbook set, to go back to


def geom_of(kind):
    """What a step of this kind is actually drawn as."""
    return GEOM.get(kind, kind if kind in SHAPES else "rect")


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



EN = {
    # ---- the words the chart draws
    "start": "Start", "end": "End", "ret": "Return",
    "yes": "True", "no": "False", "again": "again?",
    "key_oval": "Start / End", "key_rect": "Process",
    "key_io": "Input / Output", "key_diamond": "Decision",
    "key_hex": "Loop", "key_sub": "Call a module",
    # ---- the page around it
    "palette": "Palette", "shapes": "Shapes",
    "selected": "Selected shape", "rest": "Lines and paper",
    "fill": "Fill", "outline": "Outline", "text": "Words",
    "paper": "Paper", "grid": "Grid", "show_grid": "Show the grid",
    "lines": "Lines and arrows", "reset": "Put every color back",
    "download": "Download", "dl_size": "Size",
    "dl_svg": "Download SVG", "dl_png": "Download PNG", "panel": "Panel",
    "panel_tip": "Show or hide the panel", "png_tip": "How big the PNG comes out",
    "fit": "Fit", "actual": "Actual", "zoom_in": "Zoom in", "zoom_out": "Zoom out",
    "slide_left": "Left", "slide_right": "Right", "slide_up": "Up", "slide_down": "Down",
    "hold_locked": "Locked", "hold_loose": "Unlocked",
    "lock_tip": "Hold the chart in place, scrolling inside the stage",
    "loose_tip": "Drag the chart anywhere; a corner of it always stays in sight",
    "pixels": "pixels",
    "dl_scale": "Times the size it is drawn",
    "dl_frame": "Fitted inside a picture",
    "png_over": "more than this browser can draw",
    "click_shape": "Click a shape in the chart to color that one on its own.",
    "palette_hint": "A palette sets every shape at once. Anything you "
                    "change by hand afterwards stays changed.",
    "shapes_hint": "Fill and outline, for every shape of that kind.",
    "apply_all": "Apply to all {n} {what}", "clear": "Clear",
    "rendering": "Rendering…",
    "png_big": "The browser could not make a PNG that big. Try a smaller "
               "size, or save the SVG.",
    "png_fail": "The browser could not draw the PNG. The SVG download "
                "still works.",
    "png_capped": "{want}× is past what a browser canvas holds, so "
                  "the PNG saves at {got}× ({w} × {h} pixels).",
    "flowchart": "Flowchart",
    "r_head": "Run it",
    "r_run": "Run",
    "r_stop": "Stop",
    "r_code": "As code",
    "r_pseudo": "Pseudocode",
    "r_slowly": "Step slowly",
    "r_follow": "Follow along",
    "r_follow_tip": "While it steps, the chart moves and zooms to the shape being done, and the pseudocode scrolls to the line it came from",
    "r_enter": "Enter",
    "r_hint": "Runs the program the chart was built from: it asks for what it asks a person for, prints what it prints, and lights up the shape it is on. Pick a language to see the same program written out in it.",
    "r_started": "Running...",
    "r_done": "Finished.",
    "r_nothing": "There is nothing to run yet.",
    "r_steps": "{n} steps, {ms} ms.",
    "r_forever": "This has run far too long without stopping -- somewhere there is a loop it never gets out of.",
    "r_zero": "That divides by zero.",
    "r_unknown": "Nothing has been put in {name} yet.",
    "r_odd_op": "I do not know what to do with {op}.",
    "r_half": "This does not read as a whole thing: {bit}",
    "r_back": "Back to the run", "back": "Back",
    "r_copy": "Copy",
    "r_copied": "Copied",
    "r_save_code": "Save it",
    "r_pseudo_only": "Pick Python, Java, C# or JavaScript to see the code.",
    "n_rect": "Box",
    "an_arrow": "Arrow",
    "word_on_it": "Word on it",
    "thickness": "Thickness",
    "color_of_it": "Color",
    "dashed": "Dashed",
    "with_head": "Arrowhead",
    "turn_it_round": "Turn it round",
    "m_type": "Type in it",
    "m_copy": "Make another",
    "c_fill": "Fill colour", "c_line": "Border colour", "c_words": "Word colour",
    "c_clear": "No colour of its own",
    "m_turn": "Turn 90°",
    "m_solid": "Solid",
    "m_no_word": "No word",
    "m_fit": "Fit on screen",
    "the_design": "The design",
    "f_save": "Save this to a file",
    "f_open": "Open a file",
    "f_not_ours": "That file is not one of these.",
    "n_roundrect": "Rounded box",
    "n_offpage": "Off-page", "n_loop": "Loop limit", "n_parallel": "Side by side",
    "n_text": "Text", "n_actor": "Person", "n_callout": "Speech",
    "n_cube": "Cube", "n_step": "Step", "n_table": "Table",
    "n_stored": "Stored inside", "n_cloud": "Cloud",
    "n_card": "Card",
    "n_note": "Note",
    "n_docs": "Pages",
    "n_manual": "Typed in",
    "n_screen": "Screen",
    "n_arrow": "Arrow",
    "n_io_back": "Parallelogram, other way",
    "n_oval": "Oval",
    "n_io": "Parallelogram",
    "n_diamond": "Diamond",
    "n_hex": "Hexagon",
    "n_sub": "Box with bars",
    "n_trap": "Trapezoid",
    "n_doc": "Document",
    "n_store": "Drum",
    "n_delay": "Wait",
    "n_circle": "Circle",
    "shapes_for": "Shape for each kind",
    "shapes_for_hint": "Which shape gets drawn for each kind of step. What a step means does not change.",
    "size": "Size",
    "width": "Width",
    "height": "Height",
    "turn": "Turn",
    "fit_words": "Fit the words",
    "colors_here": "Colors",
    "odd_shape": "Cannot draw {pair} -- see --help.",
    "mode_code": "From pseudocode",
    "mode_hand": "By hand",
    "add_shape": "Add a shape",
    "hand_hint": "Drag shapes about. Click one, then Connect, then click where the flow goes next.",
    "words_in": "Words in the shape",
    "connect": "Connect",
    "connect_now": "Now click the shape it goes to.",
    "goes_to": "Goes to",
    "nothing_yet": "nothing yet",
    "delete": "Delete",
    "start_again": "Start again",
    "check": "Check the design",
    "checked_good": "This design works: one Start, every shape reached, and every path ends at an End.",
    "problems": "{n} to look at",
    "pick_shape": "Click a shape to give it words, move it, or join it to another.",
    "as_chart": "Chart",
    "untitled": "Untitled",
    "p_no_start": "Nothing starts the flow: every shape has something leading into it.",
    "p_many_starts": "{n} shapes have nothing leading into them. A flowchart starts in one place.",
    "p_start_kind": "The shape everything starts from should be an oval.",
    "p_no_end": "There is no End: no oval that the flow stops at.",
    "p_unreached": "Nothing leads to this shape.",
    "p_dead_end": "Nothing leaves this shape, and it is not an End.",
    "p_decision_out": "A decision needs two ways out, one for each answer. This one has {n}.",
    "p_one_out": "This shape has {n} ways out. Only a decision may have more than one.",
    "p_same_labels": "Both ways out of this decision say the same thing.",
    "p_no_label": "A way out of a decision needs a word on it.",
    "p_trapped": "Once the flow gets here it can never reach an End.",
    "p_empty": "This shape has nothing written in it.",
    "p_overlap": "This shape is on top of another one.",
    "p_alone": "This shape is not joined to anything.",
    "p_line_through": "A line runs straight through this shape. Move one of them over a little.",
    "side_chart": "Chart", "side_colors": "Colors", "hide_panel": "Hide the panel", "show_panel": "Show the panel",
    "theme": "Light or dark", "theme_auto": "Auto", "theme_light": "Light", "theme_dark": "Dark",
    "settings": "Settings", "appearance": "Appearance", "panel_side": "Panel side",
    "side_left": "Left", "side_right": "Right", "full_screen": "Full screen",
    "full_on": "Fill the screen", "full_off": "Leave full screen",
    "no_full": "This browser will not go full screen.",
    "p_ink": "Ink", "p_classic": "Classic", "p_slate": "Slate",
    "p_meadow": "Meadow", "p_sunset": "Sunset", "p_night": "Night",
    # ---- the studio
    "pseudocode": "Pseudocode", "title": "Title", "your_name": "Your name",
    "code_big": "Fill the screen", "code_small": "Back to the panel", "done": "Done",
    "code_esc": "Esc to close", "code_lines": "{n} lines",
    "shape": "Shape",
    "language": "Language", "key_switch": "Key", "tint_switch": "Tints",
    "build": "Build the chart", "drawing": "Drawing…",
    "no_code": "There is no pseudocode to draw yet.",
    "failed": "That did not draw.",
    "not_answering": "The studio is not answering ({err}).",
    "empty_chart": "Paste your pseudocode on the left, then press Build.",
    "shape_auto": "Auto", "shape_square": "Square", "shape_wide": "Wide 16:9",
    "shape_page": "Page", "shape_tall": "Tall",
    # ---- what the script says in the terminal
    "wrote": "Wrote {path}",
    "open_this": "<- open this one: it shows the chart and has the "
                 "download links",
    "style_seed": "Style seed {seed} (pass --seed {seed} to draw this "
                  "one again)",
    "nothing": "No pseudocode given -- nothing to draw.",
    "studio_at": "The flowchart studio is running at {url}",
    "leave_open": "Leave this window open while you use it; press Ctrl+C "
                  "to stop.",
    "stopped": "Studio stopped.",
    "site_done": "That folder is a website. Put it on GitHub Pages (or "
                 "any host that serves files) and it works as it does "
                 "here -- {dir}/README.md has the steps.",
    "starting": "Starting Python in your browser…",
    "ready": "Ready.",
    "boot_failed": "Python could not start in this browser ({err}).",
}
ES = {
    "start": "Inicio", "end": "Fin", "ret": "Retornar",
    "yes": "Verdadero", "no": "Falso", "again": "¿otra vez?",
    "key_oval": "Inicio / Fin", "key_rect": "Proceso",
    "key_io": "Entrada / Salida", "key_diamond": "Decisión",
    "key_hex": "Bucle", "key_sub": "Llamar a un módulo",
    "palette": "Paleta", "shapes": "Formas",
    "selected": "Forma seleccionada", "rest": "Líneas y papel",
    "fill": "Relleno", "outline": "Contorno", "text": "Texto",
    "paper": "Papel", "grid": "Cuadrícula",
    "show_grid": "Mostrar la cuadrícula",
    "lines": "Líneas y flechas", "reset": "Restaurar todos los colores",
    "download": "Descargar", "dl_size": "Tamaño",
    "dl_svg": "Descargar SVG", "dl_png": "Descargar PNG", "panel": "Panel",
    "panel_tip": "Mostrar u ocultar el panel",
    "png_tip": "Tamaño del PNG",
    "fit": "Ajustar", "actual": "Real", "zoom_in": "Acercar",
    "slide_left": "Izquierda", "slide_right": "Derecha", "slide_up": "Arriba", "slide_down": "Abajo",
    "hold_locked": "Fijo", "hold_loose": "Libre",
    "lock_tip": "Mantener el diagrama en su sitio, desplazándose dentro del área",
    "loose_tip": "Arrastra el diagrama a donde quieras; siempre queda una esquina a la vista",
    "zoom_out": "Alejar", "pixels": "píxeles",
    "dl_scale": "Veces el tamaño dibujado",
    "dl_frame": "Ajustado dentro de una imagen",
    "png_over": "más de lo que este navegador puede dibujar",
    "click_shape": "Haz clic en una forma del diagrama para colorear solo esa.",
    "palette_hint": "Una paleta cambia todas las formas a la vez. Lo que "
                    "cambies a mano después se conserva.",
    "shapes_hint": "Relleno y contorno, para todas las formas de ese tipo.",
    "apply_all": "Aplicar a las {n} formas: {what}", "clear": "Borrar",
    "rendering": "Generando…",
    "png_big": "El navegador no pudo crear un PNG tan grande. Prueba con "
               "un tamaño menor o guarda el SVG.",
    "png_fail": "El navegador no pudo dibujar el PNG. La descarga del SVG "
                "sigue funcionando.",
    "png_capped": "{want}× supera lo que admite el lienzo del "
                  "navegador, así que el PNG se guarda a {got}× "
                  "({w} × {h} píxeles).",
    "flowchart": "Diagrama de flujo",
    "r_head": "Ejecutar",
    "r_run": "Ejecutar",
    "r_stop": "Detener",
    "r_code": "Como código",
    "r_pseudo": "Pseudocódigo",
    "r_slowly": "Paso a paso",
    "r_follow": "Seguir el paso",
    "r_follow_tip": "Mientras avanza, el diagrama se mueve y se acerca a la forma en curso, y el pseudocódigo se desplaza a su línea",
    "r_enter": "Entrar",
    "r_hint": "Ejecuta el programa del que salió el diagrama: pide lo que le pide a una persona, muestra lo que muestra y resalta la forma en la que está. Elige un lenguaje para ver el mismo programa escrito en él.",
    "r_started": "Ejecutando...",
    "r_done": "Terminado.",
    "r_nothing": "Todavía no hay nada que ejecutar.",
    "r_steps": "{n} pasos, {ms} ms.",
    "r_forever": "Lleva demasiado tiempo sin parar: en algún sitio hay un bucle del que nunca sale.",
    "r_zero": "Eso divide entre cero.",
    "r_unknown": "Todavía no se ha puesto nada en {name}.",
    "r_odd_op": "No sé qué hacer con {op}.",
    "r_half": "Esto no se lee como algo completo: {bit}",
    "r_back": "Volver a la ejecución", "back": "Atrás",
    "r_copy": "Copiar",
    "r_copied": "Copiado",
    "r_save_code": "Guardar",
    "r_pseudo_only": "Elige Python, Java, C# o JavaScript para ver el código.",
    "n_rect": "Rectángulo",
    "an_arrow": "Flecha",
    "word_on_it": "Palabra en ella",
    "thickness": "Grosor",
    "color_of_it": "Color",
    "dashed": "Discontinua",
    "with_head": "Punta",
    "turn_it_round": "Invertir",
    "m_type": "Escribir dentro",
    "m_copy": "Duplicar",
    "c_fill": "Color de relleno", "c_line": "Color del borde", "c_words": "Color del texto",
    "c_clear": "Sin color propio",
    "m_turn": "Girar 90°",
    "m_solid": "Continua",
    "m_no_word": "Sin palabra",
    "m_fit": "Ajustar a la pantalla",
    "the_design": "El diseño",
    "f_save": "Guardar en un archivo",
    "f_open": "Abrir un archivo",
    "f_not_ours": "Ese archivo no es de los nuestros.",
    "n_roundrect": "Caja redondeada",
    "n_offpage": "Fuera de página", "n_loop": "Límite de bucle", "n_parallel": "En paralelo",
    "n_text": "Texto", "n_actor": "Persona", "n_callout": "Bocadillo",
    "n_cube": "Cubo", "n_step": "Paso", "n_table": "Tabla",
    "n_stored": "Almacenado dentro", "n_cloud": "Nube",
    "n_card": "Tarjeta",
    "n_note": "Nota",
    "n_docs": "Páginas",
    "n_manual": "Entrada manual",
    "n_screen": "Pantalla",
    "n_arrow": "Flecha",
    "n_io_back": "Paralelogramo al revés",
    "n_oval": "Óvalo",
    "n_io": "Paralelogramo",
    "n_diamond": "Rombo",
    "n_hex": "Hexágono",
    "n_sub": "Caja con barras",
    "n_trap": "Trapecio",
    "n_doc": "Documento",
    "n_store": "Cilindro",
    "n_delay": "Espera",
    "n_circle": "Círculo",
    "shapes_for": "Forma de cada tipo",
    "shapes_for_hint": "Qué forma se dibuja para cada tipo de paso. Lo que significa el paso no cambia.",
    "size": "Tamaño",
    "width": "Ancho",
    "height": "Alto",
    "turn": "Girar",
    "fit_words": "Ajustar al texto",
    "colors_here": "Colores",
    "odd_shape": "No se puede dibujar {pair}; mira --help.",
    "mode_code": "Desde pseudocódigo",
    "mode_hand": "A mano",
    "add_shape": "Añadir una forma",
    "hand_hint": "Arrastra las formas. Haz clic en una, luego en Conectar, y después en la forma a la que sigue el flujo.",
    "words_in": "Texto de la forma",
    "connect": "Conectar",
    "connect_now": "Ahora haz clic en la forma a la que va.",
    "goes_to": "Va a",
    "nothing_yet": "nada todavía",
    "delete": "Eliminar",
    "start_again": "Empezar de nuevo",
    "check": "Comprobar el diseño",
    "checked_good": "El diseño funciona: un solo Inicio, todas las formas alcanzables y todos los caminos terminan en un Fin.",
    "problems": "{n} cosas que revisar",
    "pick_shape": "Haz clic en una forma para escribir en ella, moverla o unirla a otra.",
    "as_chart": "Diagrama",
    "untitled": "Sin título",
    "p_no_start": "Nada inicia el flujo: todas las formas tienen algo que llega a ellas.",
    "p_many_starts": "{n} formas no tienen nada que llegue a ellas. Un diagrama empieza en un solo sitio.",
    "p_start_kind": "La forma por la que todo empieza debería ser un óvalo.",
    "p_no_end": "No hay Fin: ningún óvalo donde el flujo se detenga.",
    "p_unreached": "Nada lleva a esta forma.",
    "p_dead_end": "No sale nada de esta forma y no es un Fin.",
    "p_decision_out": "Una decisión necesita dos salidas, una por respuesta. Esta tiene {n}.",
    "p_one_out": "Esta forma tiene {n} salidas. Solo una decisión puede tener más de una.",
    "p_same_labels": "Las dos salidas de esta decisión dicen lo mismo.",
    "p_no_label": "Una salida de una decisión necesita una palabra.",
    "p_trapped": "Si el flujo llega aquí, nunca podrá llegar a un Fin.",
    "p_empty": "Esta forma no tiene nada escrito.",
    "p_overlap": "Esta forma está encima de otra.",
    "p_alone": "Esta forma no está unida a nada.",
    "p_line_through": "Una línea atraviesa esta forma. Mueve un poco alguna de las dos.",
    "side_chart": "Diagrama", "side_colors": "Colores", "hide_panel": "Ocultar el panel", "show_panel": "Mostrar el panel",
    "theme": "Claro u oscuro", "theme_auto": "Auto", "theme_light": "Claro", "theme_dark": "Oscuro",
    "settings": "Ajustes", "appearance": "Apariencia", "panel_side": "Lado del panel",
    "side_left": "Izquierda", "side_right": "Derecha", "full_screen": "Pantalla completa",
    "full_on": "Llenar la pantalla", "full_off": "Salir de pantalla completa",
    "no_full": "Este navegador no admite pantalla completa.",
    "p_ink": "Tinta", "p_classic": "Clásica", "p_slate": "Pizarra",
    "p_meadow": "Pradera", "p_sunset": "Ocaso", "p_night": "Noche",
    "pseudocode": "Pseudocódigo", "title": "Título",
    "code_big": "Llenar la pantalla", "code_small": "Volver al panel", "done": "Listo",
    "code_esc": "Esc para cerrar", "code_lines": "{n} líneas",
    "your_name": "Tu nombre", "shape": "Forma",
    "language": "Idioma", "key_switch": "Leyenda",
    "tint_switch": "Tintes", "build": "Dibujar el diagrama",
    "drawing": "Dibujando…",
    "no_code": "Todavía no hay pseudocódigo que dibujar.",
    "failed": "No se pudo dibujar.",
    "not_answering": "El estudio no responde ({err}).",
    "empty_chart": "Pega tu pseudocódigo a la izquierda y pulsa Dibujar.",
    "shape_auto": "Automática", "shape_square": "Cuadrada",
    "shape_wide": "Ancha 16:9", "shape_page": "Página", "shape_tall": "Alta",
    "wrote": "Escrito {path}",
    "open_this": "<- abre este: muestra el diagrama y tiene los enlaces "
                 "de descarga",
    "style_seed": "Semilla de estilo {seed} (usa --seed {seed} para "
                  "volver a dibujarlo igual)",
    "nothing": "No se dio pseudocódigo: no hay nada que dibujar.",
    "studio_at": "El estudio de diagramas está en {url}",
    "leave_open": "Deja esta ventana abierta mientras lo usas; pulsa "
                  "Ctrl+C para detenerlo.",
    "stopped": "Estudio detenido.",
    "site_done": "Esa carpeta es un sitio web. Súbela a GitHub Pages (o "
                 "a cualquier host de archivos) y funcionará igual que "
                 "aquí; los pasos están en {dir}/README.md.",
    "starting": "Iniciando Python en el navegador…",
    "ready": "Listo.",
    "boot_failed": "Python no pudo iniciarse en este navegador ({err}).",
}
FR = {
    "start": "Début", "end": "Fin", "ret": "Retour",
    "yes": "Vrai", "no": "Faux", "again": "encore ?",
    "key_oval": "Début / Fin", "key_rect": "Traitement",
    "key_io": "Entrée / Sortie", "key_diamond": "Décision",
    "key_hex": "Boucle", "key_sub": "Appeler un module",
    "palette": "Palette", "shapes": "Formes",
    "selected": "Forme sélectionnée", "rest": "Lignes et papier",
    "fill": "Remplissage", "outline": "Contour", "text": "Texte",
    "paper": "Papier", "grid": "Grille", "show_grid": "Afficher la grille",
    "lines": "Lignes et flèches", "reset": "Rétablir toutes les couleurs",
    "download": "Télécharger", "dl_size": "Taille",
    "dl_svg": "Télécharger le SVG", "dl_png": "Télécharger le PNG",
    "panel": "Panneau", "panel_tip": "Afficher ou masquer le panneau",
    "png_tip": "Taille du PNG",
    "fit": "Ajuster", "actual": "Réel", "zoom_in": "Agrandir",
    "slide_left": "Gauche", "slide_right": "Droite", "slide_up": "Haut", "slide_down": "Bas",
    "hold_locked": "Fixé", "hold_loose": "Libre",
    "lock_tip": "Garder le schéma en place, en défilant dans la zone",
    "loose_tip": "Déplacez le schéma où vous voulez ; un coin reste toujours visible",
    "zoom_out": "Réduire", "pixels": "pixels",
    "dl_scale": "Fois la taille dessinée",
    "dl_frame": "Ajusté dans une image",
    "png_over": "plus que ce navigateur ne peut dessiner",
    "click_shape": "Cliquez sur une forme de l'organigramme pour ne "
                   "colorer que celle-là.",
    "palette_hint": "Une palette change toutes les formes d'un coup. Ce "
                    "que vous changez ensuite à la main est conservé.",
    "shapes_hint": "Remplissage et contour, pour toutes les formes de ce type.",
    "apply_all": "Appliquer aux {n} formes : {what}", "clear": "Effacer",
    "rendering": "Rendu…",
    "png_big": "Le navigateur n'a pas pu créer un PNG aussi grand. "
               "Essayez une taille plus petite, ou enregistrez le SVG.",
    "png_fail": "Le navigateur n'a pas pu dessiner le PNG. Le "
                "téléchargement du SVG fonctionne toujours.",
    "png_capped": "{want}× dépasse ce qu'un canvas de navigateur "
                  "accepte ; le PNG est donc enregistré à {got}× "
                  "({w} × {h} pixels).",
    "flowchart": "Organigramme",
    "r_head": "Exécuter",
    "r_run": "Lancer",
    "r_stop": "Arrêter",
    "r_code": "En code",
    "r_pseudo": "Pseudocode",
    "r_slowly": "Pas à pas",
    "r_follow": "Suivre le pas",
    "r_follow_tip": "Pendant les pas, le schéma se déplace et zoome sur la forme en cours, et le pseudocode défile jusqu'à sa ligne",
    "r_enter": "Entrer",
    "r_hint": "Exécute le programme dont vient l'organigramme : il demande ce qu'il demande à une personne, affiche ce qu'il affiche, et éclaire la forme où il en est. Choisissez un langage pour voir le même programme écrit dedans.",
    "r_started": "Exécution...",
    "r_done": "Terminé.",
    "r_nothing": "Il n'y a encore rien à exécuter.",
    "r_steps": "{n} étapes, {ms} ms.",
    "r_forever": "Cela tourne depuis bien trop longtemps : quelque part il y a une boucle dont il ne sort jamais.",
    "r_zero": "Cela divise par zéro.",
    "r_unknown": "Rien n'a encore été mis dans {name}.",
    "r_odd_op": "Je ne sais pas quoi faire de {op}.",
    "r_half": "Cela ne se lit pas comme un tout : {bit}",
    "r_back": "Retour à l’exécution", "back": "Retour",
    "r_copy": "Copier",
    "r_copied": "Copié",
    "r_save_code": "Enregistrer",
    "r_pseudo_only": "Choisissez Python, Java, C# ou JavaScript pour voir le code.",
    "n_rect": "Rectangle",
    "an_arrow": "Flèche",
    "word_on_it": "Mot dessus",
    "thickness": "Épaisseur",
    "color_of_it": "Couleur",
    "dashed": "Pointillés",
    "with_head": "Pointe",
    "turn_it_round": "Inverser",
    "m_type": "Écrire dedans",
    "m_copy": "Dupliquer",
    "c_fill": "Couleur de fond", "c_line": "Couleur du bord", "c_words": "Couleur du texte",
    "c_clear": "Aucune couleur propre",
    "m_turn": "Tourner de 90°",
    "m_solid": "Trait plein",
    "m_no_word": "Aucun mot",
    "m_fit": "Ajuster à l'écran",
    "the_design": "Le schéma",
    "f_save": "Enregistrer dans un fichier",
    "f_open": "Ouvrir un fichier",
    "f_not_ours": "Ce fichier n'en est pas un.",
    "n_roundrect": "Boîte arrondie",
    "n_offpage": "Hors page", "n_loop": "Limite de boucle", "n_parallel": "En parallèle",
    "n_text": "Texte", "n_actor": "Personne", "n_callout": "Bulle",
    "n_cube": "Cube", "n_step": "Étape", "n_table": "Tableau",
    "n_stored": "Stocké à l’intérieur", "n_cloud": "Nuage",
    "n_card": "Carte",
    "n_note": "Note",
    "n_docs": "Pages",
    "n_manual": "Saisie manuelle",
    "n_screen": "Écran",
    "n_arrow": "Flèche",
    "n_io_back": "Parallélogramme inversé",
    "n_oval": "Ovale",
    "n_io": "Parallélogramme",
    "n_diamond": "Losange",
    "n_hex": "Hexagone",
    "n_sub": "Boîte à barres",
    "n_trap": "Trapèze",
    "n_doc": "Document",
    "n_store": "Tambour",
    "n_delay": "Attente",
    "n_circle": "Cercle",
    "shapes_for": "Forme de chaque type",
    "shapes_for_hint": "Quelle forme est dessinée pour chaque type d'étape. Ce que l'étape veut dire ne change pas.",
    "size": "Taille",
    "width": "Largeur",
    "height": "Hauteur",
    "turn": "Tourner",
    "fit_words": "Ajuster au texte",
    "colors_here": "Couleurs",
    "odd_shape": "Impossible de dessiner {pair} ; voir --help.",
    "mode_code": "À partir du pseudocode",
    "mode_hand": "À la main",
    "add_shape": "Ajouter une forme",
    "hand_hint": "Déplacez les formes. Cliquez sur l'une, puis sur Relier, puis sur la forme où va la suite.",
    "words_in": "Texte de la forme",
    "connect": "Relier",
    "connect_now": "Cliquez maintenant sur la forme où cela va.",
    "goes_to": "Va vers",
    "nothing_yet": "rien encore",
    "delete": "Supprimer",
    "start_again": "Tout recommencer",
    "check": "Vérifier le schéma",
    "checked_good": "Le schéma tient : un seul Début, toutes les formes atteintes, et tous les chemins finissent sur une Fin.",
    "problems": "{n} choses à revoir",
    "pick_shape": "Cliquez sur une forme pour y écrire, la déplacer ou la relier à une autre.",
    "as_chart": "Organigramme",
    "untitled": "Sans titre",
    "p_no_start": "Rien ne commence le flux : chaque forme a quelque chose qui y mène.",
    "p_many_starts": "{n} formes n'ont rien qui y mène. Un organigramme commence à un seul endroit.",
    "p_start_kind": "La forme par laquelle tout commence devrait être un ovale.",
    "p_no_end": "Il n'y a pas de Fin : aucun ovale où le flux s'arrête.",
    "p_unreached": "Rien ne mène à cette forme.",
    "p_dead_end": "Rien ne sort de cette forme, et ce n'est pas une Fin.",
    "p_decision_out": "Une décision a deux sorties, une par réponse. Celle-ci en a {n}.",
    "p_one_out": "Cette forme a {n} sorties. Seule une décision peut en avoir plus d'une.",
    "p_same_labels": "Les deux sorties de cette décision disent la même chose.",
    "p_no_label": "Une sortie de décision a besoin d'un mot.",
    "p_trapped": "Une fois arrivé ici, le flux ne peut plus atteindre de Fin.",
    "p_empty": "Rien n'est écrit dans cette forme.",
    "p_overlap": "Cette forme est posée sur une autre.",
    "p_alone": "Cette forme n'est reliée à rien.",
    "p_line_through": "Une ligne traverse cette forme. Déplacez un peu l'une ou l'autre.",
    "side_chart": "Schéma", "side_colors": "Couleurs", "hide_panel": "Masquer le panneau", "show_panel": "Afficher le panneau",
    "theme": "Clair ou sombre", "theme_auto": "Auto", "theme_light": "Clair", "theme_dark": "Sombre",
    "settings": "Réglages", "appearance": "Apparence", "panel_side": "Côté du panneau",
    "side_left": "Gauche", "side_right": "Droite", "full_screen": "Plein écran",
    "full_on": "Remplir l’écran", "full_off": "Quitter le plein écran",
    "no_full": "Ce navigateur ne passe pas en plein écran.",
    "p_ink": "Encre", "p_classic": "Classique", "p_slate": "Ardoise",
    "p_meadow": "Prairie", "p_sunset": "Couchant", "p_night": "Nuit",
    "pseudocode": "Pseudocode", "title": "Titre", "your_name": "Votre nom",
    "code_big": "Remplir l’écran", "code_small": "Revenir au panneau", "done": "Terminé",
    "code_esc": "Échap pour fermer", "code_lines": "{n} lignes",
    "shape": "Forme",
    "language": "Langue", "key_switch": "Légende", "tint_switch": "Teintes",
    "build": "Dessiner l'organigramme", "drawing": "Dessin…",
    "no_code": "Il n'y a pas encore de pseudocode à dessiner.",
    "failed": "Le dessin a échoué.",
    "not_answering": "Le studio ne répond pas ({err}).",
    "empty_chart": "Collez votre pseudocode à gauche, puis cliquez sur "
                   "Dessiner.",
    "shape_auto": "Auto", "shape_square": "Carré", "shape_wide": "Large 16:9",
    "shape_page": "Page", "shape_tall": "Haut",
    "wrote": "Écrit {path}",
    "open_this": "<- ouvrez celui-ci : il montre l'organigramme et porte "
                 "les liens de téléchargement",
    "style_seed": "Graine de style {seed} (passez --seed {seed} pour le "
                  "redessiner à l'identique)",
    "nothing": "Aucun pseudocode donné -- rien à dessiner.",
    "studio_at": "Le studio d'organigrammes tourne sur {url}",
    "leave_open": "Laissez cette fenêtre ouverte pendant que vous vous en "
                  "servez ; Ctrl+C pour l'arrêter.",
    "stopped": "Studio arrêté.",
    "site_done": "Ce dossier est un site web. Mettez-le sur GitHub Pages "
                 "(ou tout hébergeur de fichiers) et il marchera comme "
                 "ici ; les étapes sont dans {dir}/README.md.",
    "starting": "Démarrage de Python dans le navigateur…",
    "ready": "Prêt.",
    "boot_failed": "Python n'a pas pu démarrer dans ce navigateur ({err}).",
}
DE = {
    "start": "Start", "end": "Ende", "ret": "Rückgabe",
    "yes": "Wahr", "no": "Falsch", "again": "nochmal?",
    "key_oval": "Start / Ende", "key_rect": "Verarbeitung",
    "key_io": "Eingabe / Ausgabe", "key_diamond": "Entscheidung",
    "key_hex": "Schleife", "key_sub": "Modul aufrufen",
    "palette": "Palette", "shapes": "Formen",
    "selected": "Ausgewählte Form", "rest": "Linien und Papier",
    "fill": "Füllung", "outline": "Umriss", "text": "Text",
    "paper": "Papier", "grid": "Raster", "show_grid": "Raster anzeigen",
    "lines": "Linien und Pfeile", "reset": "Alle Farben zurücksetzen",
    "download": "Herunterladen", "dl_size": "Größe",
    "dl_svg": "SVG herunterladen", "dl_png": "PNG herunterladen",
    "panel": "Bereich", "panel_tip": "Bereich ein- oder ausblenden",
    "png_tip": "Wie groß das PNG wird",
    "fit": "Einpassen", "actual": "Original", "zoom_in": "Vergrößern",
    "slide_left": "Links", "slide_right": "Rechts", "slide_up": "Hoch", "slide_down": "Runter",
    "hold_locked": "Fixiert", "hold_loose": "Frei",
    "lock_tip": "Das Diagramm bleibt an seinem Platz und wird in der Fläche gescrollt",
    "loose_tip": "Das Diagramm frei verschieben; eine Ecke bleibt immer sichtbar",
    "zoom_out": "Verkleinern", "pixels": "Pixel",
    "dl_scale": "Mal so groß wie gezeichnet",
    "dl_frame": "In ein Bild eingepasst",
    "png_over": "mehr, als dieser Browser zeichnen kann",
    "click_shape": "Klicke auf eine Form im Diagramm, um nur diese zu färben.",
    "palette_hint": "Eine Palette setzt alle Formen auf einmal. Was du "
                    "danach von Hand änderst, bleibt erhalten.",
    "shapes_hint": "Füllung und Umriss, für alle Formen dieser Art.",
    "apply_all": "Auf alle {n} anwenden: {what}", "clear": "Löschen",
    "rendering": "Wird erzeugt…",
    "png_big": "Der Browser konnte kein so großes PNG erzeugen. Nimm eine "
               "kleinere Größe oder speichere das SVG.",
    "png_fail": "Der Browser konnte das PNG nicht zeichnen. Der "
                "SVG-Download funktioniert weiterhin.",
    "png_capped": "{want}× ist mehr, als ein Browser-Canvas fasst; "
                  "das PNG wird mit {got}× gespeichert "
                  "({w} × {h} Pixel).",
    "flowchart": "Flussdiagramm",
    "r_head": "Ausführen",
    "r_run": "Starten",
    "r_stop": "Anhalten",
    "r_code": "Als Code",
    "r_pseudo": "Pseudocode",
    "r_slowly": "Schritt für Schritt",
    "r_follow": "Mitlaufen",
    "r_follow_tip": "Während der Schritte fährt das Diagramm zur laufenden Form und zoomt heran; der Pseudocode springt zu ihrer Zeile",
    "r_enter": "Eingeben",
    "r_hint": "Führt das Programm aus, aus dem das Diagramm entstanden ist: es fragt, wonach es fragt, gibt aus, was es ausgibt, und hebt die Form hervor, bei der es gerade ist. Wähle eine Sprache, um dasselbe Programm darin zu sehen.",
    "r_started": "Läuft...",
    "r_done": "Fertig.",
    "r_nothing": "Es gibt noch nichts auszuführen.",
    "r_steps": "{n} Schritte, {ms} ms.",
    "r_forever": "Das läuft viel zu lange ohne anzuhalten -- irgendwo ist eine Schleife, aus der es nie herauskommt.",
    "r_zero": "Das teilt durch null.",
    "r_unknown": "In {name} steht noch nichts.",
    "r_odd_op": "Mit {op} weiß ich nichts anzufangen.",
    "r_half": "Das liest sich nicht als Ganzes: {bit}",
    "r_back": "Zurück zum Lauf", "back": "Zurück",
    "r_copy": "Kopieren",
    "r_copied": "Kopiert",
    "r_save_code": "Speichern",
    "r_pseudo_only": "Wähle Python, Java, C# oder JavaScript, um den Code zu sehen.",
    "n_rect": "Rechteck",
    "an_arrow": "Pfeil",
    "word_on_it": "Wort daran",
    "thickness": "Dicke",
    "color_of_it": "Farbe",
    "dashed": "Gestrichelt",
    "with_head": "Spitze",
    "turn_it_round": "Umdrehen",
    "m_type": "Hineinschreiben",
    "m_copy": "Noch eins",
    "c_fill": "Füllfarbe", "c_line": "Randfarbe", "c_words": "Textfarbe",
    "c_clear": "Keine eigene Farbe",
    "m_turn": "90° drehen",
    "m_solid": "Durchgezogen",
    "m_no_word": "Kein Wort",
    "m_fit": "Auf den Bildschirm passen",
    "the_design": "Der Entwurf",
    "f_save": "In eine Datei speichern",
    "f_open": "Datei öffnen",
    "f_not_ours": "Diese Datei gehört nicht dazu.",
    "n_roundrect": "Abgerundeter Kasten",
    "n_offpage": "Andere Seite", "n_loop": "Schleifengrenze", "n_parallel": "Nebeneinander",
    "n_text": "Text", "n_actor": "Person", "n_callout": "Sprechblase",
    "n_cube": "Würfel", "n_step": "Schritt", "n_table": "Tabelle",
    "n_stored": "Intern gespeichert", "n_cloud": "Cloud",
    "n_card": "Karte",
    "n_note": "Notiz",
    "n_docs": "Seiten",
    "n_manual": "Handeingabe",
    "n_screen": "Bildschirm",
    "n_arrow": "Pfeil",
    "n_io_back": "Parallelogramm andersherum",
    "n_oval": "Oval",
    "n_io": "Parallelogramm",
    "n_diamond": "Raute",
    "n_hex": "Sechseck",
    "n_sub": "Kasten mit Balken",
    "n_trap": "Trapez",
    "n_doc": "Dokument",
    "n_store": "Trommel",
    "n_delay": "Warten",
    "n_circle": "Kreis",
    "shapes_for": "Form je Art",
    "shapes_for_hint": "Welche Form für welche Art von Schritt gezeichnet wird. Was der Schritt bedeutet, ändert sich nicht.",
    "size": "Größe",
    "width": "Breite",
    "height": "Höhe",
    "turn": "Drehen",
    "fit_words": "An den Text anpassen",
    "colors_here": "Farben",
    "odd_shape": "{pair} lässt sich nicht zeichnen -- siehe --help.",
    "mode_code": "Aus Pseudocode",
    "mode_hand": "Von Hand",
    "add_shape": "Form hinzufügen",
    "hand_hint": "Formen verschieben. Eine anklicken, dann Verbinden, dann die Form anklicken, zu der es weitergeht.",
    "words_in": "Text in der Form",
    "connect": "Verbinden",
    "connect_now": "Jetzt die Form anklicken, zu der es geht.",
    "goes_to": "Geht zu",
    "nothing_yet": "noch nichts",
    "delete": "Löschen",
    "start_again": "Neu anfangen",
    "check": "Entwurf prüfen",
    "checked_good": "Der Entwurf trägt: ein Start, alle Formen erreichbar, und jeder Weg endet an einem Ende.",
    "problems": "{n} zum Ansehen",
    "pick_shape": "Klicke eine Form an, um sie zu beschriften, zu verschieben oder zu verbinden.",
    "as_chart": "Diagramm",
    "untitled": "Ohne Titel",
    "p_no_start": "Nichts beginnt den Ablauf: in jede Form führt etwas hinein.",
    "p_many_starts": "In {n} Formen führt nichts hinein. Ein Diagramm beginnt an einer Stelle.",
    "p_start_kind": "Die Form, mit der alles anfängt, sollte ein Oval sein.",
    "p_no_end": "Es gibt kein Ende: kein Oval, an dem der Ablauf aufhört.",
    "p_unreached": "Zu dieser Form führt nichts.",
    "p_dead_end": "Aus dieser Form führt nichts heraus, und sie ist kein Ende.",
    "p_decision_out": "Eine Entscheidung braucht zwei Ausgänge, einen je Antwort. Diese hat {n}.",
    "p_one_out": "Diese Form hat {n} Ausgänge. Nur eine Entscheidung darf mehr als einen haben.",
    "p_same_labels": "Beide Ausgänge dieser Entscheidung sagen dasselbe.",
    "p_no_label": "Ein Ausgang einer Entscheidung braucht ein Wort.",
    "p_trapped": "Kommt der Ablauf hierher, erreicht er nie ein Ende.",
    "p_empty": "In dieser Form steht nichts.",
    "p_overlap": "Diese Form liegt auf einer anderen.",
    "p_alone": "Diese Form ist mit nichts verbunden.",
    "p_line_through": "Eine Linie läuft mitten durch diese Form. Verschiebe eine von beiden etwas.",
    "side_chart": "Diagramm", "side_colors": "Farben", "hide_panel": "Bereich ausblenden", "show_panel": "Bereich einblenden",
    "theme": "Hell oder dunkel", "theme_auto": "Auto", "theme_light": "Hell", "theme_dark": "Dunkel",
    "settings": "Einstellungen", "appearance": "Darstellung", "panel_side": "Seite des Panels",
    "side_left": "Links", "side_right": "Rechts", "full_screen": "Vollbild",
    "full_on": "Bildschirm füllen", "full_off": "Vollbild verlassen",
    "no_full": "Dieser Browser kennt kein Vollbild.",
    "p_ink": "Tinte", "p_classic": "Klassisch", "p_slate": "Schiefer",
    "p_meadow": "Wiese", "p_sunset": "Abendrot", "p_night": "Nacht",
    "pseudocode": "Pseudocode", "title": "Titel", "your_name": "Dein Name",
    "code_big": "Bildschirm füllen", "code_small": "Zurück zum Panel", "done": "Fertig",
    "code_esc": "Esc zum Schließen", "code_lines": "{n} Zeilen",
    "shape": "Form",
    "language": "Sprache", "key_switch": "Legende", "tint_switch": "Farbtöne",
    "build": "Diagramm zeichnen", "drawing": "Wird gezeichnet…",
    "no_code": "Es gibt noch keinen Pseudocode zum Zeichnen.",
    "failed": "Das ließ sich nicht zeichnen.",
    "not_answering": "Das Studio antwortet nicht ({err}).",
    "empty_chart": "Füge links deinen Pseudocode ein und klicke auf "
                   "Zeichnen.",
    "shape_auto": "Automatisch", "shape_square": "Quadratisch",
    "shape_wide": "Breit 16:9", "shape_page": "Seite", "shape_tall": "Hoch",
    "wrote": "Geschrieben {path}",
    "open_this": "<- diese hier öffnen: sie zeigt das Diagramm und hat "
                 "die Download-Links",
    "style_seed": "Stil-Startwert {seed} (mit --seed {seed} kommt genau "
                  "dieses Bild wieder)",
    "nothing": "Kein Pseudocode angegeben -- nichts zu zeichnen.",
    "studio_at": "Das Flussdiagramm-Studio läuft auf {url}",
    "leave_open": "Lass dieses Fenster offen, solange du es benutzt; "
                  "Strg+C beendet es.",
    "stopped": "Studio beendet.",
    "site_done": "Dieser Ordner ist eine Website. Lade ihn zu GitHub "
                 "Pages hoch (oder zu einem anderen Datei-Host); die "
                 "Schritte stehen in {dir}/README.md.",
    "starting": "Python startet im Browser…",
    "ready": "Fertig.",
    "boot_failed": "Python konnte in diesem Browser nicht starten ({err}).",
}
# =============================================================================
#  WORDS -- everything the chart and the page say, in one place.
#
#  Two sorts of text live here: the few words the chart itself draws (True,
#  False, Start, End, and the names in the key) and everything the page shows
#  around it.  Nothing else in the script has words in it that a reader sees,
#  so a language is this table and nothing more.  The pseudocode keywords are
#  not here and are not translated: Display, If, While and the rest are what
#  you type, and they stay as they are whichever language the chart is drawn
#  in.
#
#  To add a language, copy the "en" block, change the right-hand side, and
#  give it a code.  Anything left out falls back to US English, so a partial
#  translation is a perfectly good one.
# =============================================================================

LANGUAGE = "en"                     # en, es, fr, de -- or --lang on the line

WORDS = {"en": EN, "es": ES, "fr": FR, "de": DE}


def word(key, **fill):
    """One piece of text, in whichever language is set.

    Anything a language leaves out falls back to US English, so a half
    finished translation still draws a whole chart."""
    said = WORDS.get(LANGUAGE, {}).get(key) or WORDS["en"].get(key, key)
    for name, value in fill.items():
        said = said.replace("{%s}" % name, str(value))
    return said


def apply_language(code):
    """Point the chart's own words at a language."""
    global LANGUAGE, YES, NO
    LANGUAGE = code if code in WORDS else "en"
    YES, NO = word("yes"), word("no")
    for kind in list(LEGEND_NAME):
        LEGEND_NAME[kind] = word("key_" + kind)
    return LANGUAGE


# ------------------------------------------------------------- the pieces --
class Node:
    """A single flowchart shape: oval | rect | io | diamond | hex | sub."""
    kind = "node"

    def __init__(self, shape, text, terminal=False):
        self.shape = shape
        self.text = text
        self.terminal = terminal        # End / Return: the flow stops here
        self.node_id = 0                # its own number, the same one the
        self.line = 0                   #   drawing gives it, and where in
                                        #   the pseudocode it came from


class If:
    kind = "if"

    def __init__(self, cond):
        self.cond = cond
        self.then = []
        self.orelse = []
        self.chained = False            # created by an "Else If"
        self.node_id = 0
        self.line = 0


class Loop:
    """style 'pre' tests before the body (While); 'post' tests after (Do-While)."""
    kind = "loop"

    def __init__(self, style, cond=""):
        self.style = style
        self.cond = cond
        self.body = []
        self.until = False              # keep looping while cond is FALSE
        self.hex = False                # draw the test as a hexagon (For Each ...)
        self.node_id = 0
        self.line = 0


class For:
    kind = "for"

    def __init__(self, raw, init=None, cond=None, step=None):
        self.raw = raw                  # the For line as written
        self.init, self.cond, self.step = init, cond, step
        self.body = []
        self.node_id = 0
        self.line = 0


class Select:
    kind = "select"

    def __init__(self, expr):
        self.expr = expr
        self.branches = []              # list of [label, items]
        self.pre = []                   # statements before the first Case (ignored)
        self.node_id = 0
        self.line = 0


class Module:
    def __init__(self, kind, name, params, header, rtype=""):
        self.kind, self.name, self.params, self.header = kind, name, params, header
        self.rtype = rtype              # "Real" in "Function Real calcTax(...)"
        self.items = []

    def signature(self):
        return "%s(%s)" % (self.name, self.params)


# ------------------------------------------------------------- line clean-up --
def strip_comment(s):
    """Drop // ... , # ... and /* ... */ comments (but not inside quotes)."""
    out, quote, i, n = [], None, 0, len(s)
    while i < n:
        c = s[i]
        if quote:
            out.append(c)
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            out.append(c)
        elif c == "#" or s.startswith("//", i):
            break
        elif s.startswith("/*", i):
            j = s.find("*/", i + 2)
            if j < 0:
                break
            i = j + 2
            continue
        else:
            out.append(c)
        i += 1
    return "".join(out)


def split_indent(raw):
    """Return (indent, text): leading '#' markers removed, comments stripped."""
    for smart, plain in (("\u201c", '"'), ("\u201d", '"'), ("\u201e", '"'),
                         ("\u2018", "'"), ("\u2019", "'"), ("\u00a0", " ")):
        raw = raw.replace(smart, plain)             # Word's curly quotes, etc.
    s = raw.expandtabs(4).rstrip()
    body = s.lstrip()
    indent = len(s) - len(body)
    while body.startswith("#"):
        body = body[1:]
        stripped = body.lstrip()
        indent += 1 + len(body) - len(stripped)
        body = stripped
    body = re.sub(r"^\d{1,3}[.):]\s+", "", body)   # "12. Display ..." line numbers
    return indent, strip_comment(body).strip()


def clean(line):
    """Comment markers and whitespace removed (used by the interactive prompt)."""
    return split_indent(line)[1]


CONT_END = re.compile(r"(,|\+|-|\*|/|=|&|\(|\bor|\band|\|\||&&)$", re.I)
STRUCT_START = re.compile(
    r"^(if|else|elseif|elif|end|endif|endwhile|endfor|endselect|while|do|for|"
    r"select|switch|case|default|module|function|sub|procedure|def|loop|next|"
    r"until|repeat|return|call|display|print|input|declare|constant|set)\b", re.I)


def needs_more(s):
    """True when a statement obviously continues on the next line."""
    depth, quote = 0, None
    for c in s:
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
    if s.count('"') % 2 == 1:
        return True
    return depth > 0 or bool(CONT_END.search(s.rstrip()))


def join_lines(raw_lines):
    """Clean every line and glue continuation lines together.

    -> [(indent, text, the line number it started on)].  The number is
    carried so a statement can be pointed back at what was typed."""
    out, buf, buf_indent, joined, buf_line = [], "", 0, 0, 1
    for no, raw in enumerate(raw_lines, 1):
        indent, text = split_indent(raw)
        if not text:                                   # blank: never continue past it
            if buf:
                out.append((buf_indent, buf, buf_line))
                buf = ""
            out.append((indent, "", no))               # kept: a blank line is
            continue                                   #   where a run of
                                                       #   Displays ends
        if buf and (STRUCT_START.match(text) or joined >= 8):
            out.append((buf_indent, buf, buf_line))    # safety: a new statement
            buf = ""
        if buf:
            buf = buf + " " + text
            joined += 1
        else:
            buf, buf_indent, joined, buf_line = text, indent, 0, no
        if needs_more(buf):
            continue
        out.append((buf_indent, buf, buf_line))
        buf = ""
    if buf:
        out.append((buf_indent, buf, buf_line))
    return out


def tidy(s):
    """Single spaces (outside quotes), no trailing punctuation.  Keeps capitals."""
    out, quote, space = [], None, False
    for c in s.strip():
        if quote:
            out.append(c)
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
            out.append(c)
            space = False
        elif c.isspace():
            if not space:
                out.append(" ")
            space = True
        else:
            out.append(c)
            space = False
    return "".join(out).rstrip(":;.").strip()


def unwrap(cond):
    """Drop one pair of parentheses that wraps the whole condition."""
    c = cond.strip()
    if c.startswith("(") and c.endswith(")"):
        depth = 0
        for i, ch in enumerate(c):
            depth += (ch == "(") - (ch == ")")
            if depth == 0 and i < len(c) - 1:
                return c
        return c[1:-1].strip()
    return c


# ---------------------------------------------------------- statement forms --
R_MODULE = re.compile(r"^(module|function|sub|procedure|def|method|subroutine)\s+(.+)$", re.I)
R_ENDMOD = re.compile(r"^end[ -]?(module|function|sub|procedure|def|method|main|subroutine)\b", re.I)
R_ENDIF = re.compile(r"^(end[ -]?if|fi)$", re.I)
R_ENDSEL = re.compile(r"^end[ -]?(select|case|switch)$", re.I)
R_ENDLOOP = re.compile(r"^(end[ -]?(while|for|loop|do|repeat|until)|wend|loop|next(\s+\S+)?|done|od)$", re.I)
R_LOOPCOND = re.compile(r"^loop\s+(while|until)\s+(.+)$", re.I)
R_ENDANY = re.compile(r"^end[ -]\w+$", re.I)
R_ELSEIF = re.compile(r"^(else\s*if|elseif|elif|otherwise\s+if)\s+(.+)$", re.I)
R_ELSE = re.compile(r"^(else|otherwise)$", re.I)
R_CASE = re.compile(r"^(case\s+(.+)|default|case\s+else)$", re.I)
R_SELECT = re.compile(r"^(select\s+case|select|switch)\s+(.+)$", re.I)
R_IF = re.compile(r"^if\b\s*(.*)$", re.I)
R_WHILE = re.compile(r"^while\b\s*(.*)$", re.I)
R_DO = re.compile(r"^do(\s+(while|until)\s+(.+))?$", re.I)
R_REPEAT = re.compile(r"^repeat$", re.I)
R_UNTIL = re.compile(r"^until\s+(.+)$", re.I)
R_FOR = re.compile(r"^for\b\s*(.*)$", re.I)
R_FOR_TO = re.compile(r"^([\w\[\]\.]+)\s*(?:=|:=|<-)\s*(.+?)\s+(to|downto)\s+(.+?)(?:\s+step\s+(.+))?$", re.I)
R_FOR_C = re.compile(r"^\(\s*(.*?)\s*;\s*(.*?)\s*;\s*(.*?)\s*\)$")
R_RETURN = re.compile(r"^return\b", re.I)
R_CALL = re.compile(r"^call\b", re.I)
R_OUT = re.compile(r"^(display|print|output|write|echo|println|printf|puts|writeline)\b", re.I)
R_IN = re.compile(r"^(input|read|get|enter|scan|prompt|accept|readline)\b", re.I)
R_DECL = re.compile(r"^(declare|constant|const)\b", re.I)
R_START = re.compile(r"^((start|begin)(\s+program)?|main)$", re.I)
R_END = re.compile(r"^(end|stop|halt|end\s+program|exit\s+program)$", re.I)
R_CLOSER = re.compile(r"^(end[ -]?\w*|endif|endwhile|endfor|endselect|fi|wend|loop\b.*|"
                      r"next\b.*|until\s.*|done|od)$", re.I)
R_THEN = re.compile(r"\bthen\b", re.I)
R_ELSE_INLINE = re.compile(r"\belse\b", re.I)


def simple_node(s):
    """A plain statement (no If / loop / module keywords) -> Node."""
    s = tidy(s)
    if R_START.match(s):
        return Node("oval", word("start"))
    if R_END.match(s):
        return Node("oval", word("end"), terminal=True)
    if R_RETURN.match(s):
        return Node("oval", s, terminal=True)
    if R_CALL.match(s):
        return Node("sub", s)
    if R_OUT.match(s) or R_IN.match(s):
        return Node("io", s)
    return Node("rect", s)


def parse_for(rest, raw):
    """Turn the text after 'For' into a For (expandable) or a hexagon Loop."""
    m = R_FOR_TO.match(rest)
    if m:
        var, start, direction, end, step = m.groups()
        down = direction.lower() == "downto" or (step or "").strip().startswith("-")
        test = "%s %s %s" % (var, ">=" if down else "<=", end)
        if step:
            bump = "Set %s = %s + %s" % (var, var, step) if not down or not step.strip().startswith("-") \
                else "Set %s = %s - %s" % (var, var, step.strip()[1:].strip())
        else:
            bump = "Set %s = %s %s 1" % (var, var, "-" if down else "+")
        return For(raw, "Set %s = %s" % (var, start), test, bump)
    m = R_FOR_C.match(rest)
    if m:
        init, test, bump = (g.strip() for g in m.groups())
        return For(raw, init or None, test or "True", bump or None)
    loop = Loop("pre", raw)                          # For Each x In y, etc.
    loop.hex = True
    return loop


class Frame:
    """One open structure: what it is, the list statements go into, its indent."""

    def __init__(self, owner, items, indent):
        self.owner, self.items, self.indent = owner, items, indent


class Chart:
    """One flowchart: the heading drawn above it, and its top-level items."""

    def __init__(self, heading, items, is_main, module=None):
        self.heading, self.items, self.is_main, self.module = heading, items, is_main, module


def make_module(kind, rest, header):
    """'Function Real calcTax(Real income)' -> Module(kind, name, params, header)."""
    rest = rest.strip().rstrip(":")
    m = re.match(r"^(?:([\w\[\]]+)\s+)?(\w+)\s*\((.*)\)$", rest)
    if m:
        rtype, name, params = m.group(1) or "", m.group(2), m.group(3).strip()
    else:
        words = rest.replace("(", " ").replace(")", " ").split()
        rtype, name, params = "", (words[-1] if words else rest), ""
    return Module(kind.lower(), name, params, header, rtype)


def split_outside_quotes(s, sep):
    """Split s at the first sep that is not inside quotes (at most 2 parts)."""
    quote = None
    for i, c in enumerate(s):
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == sep:
            return [s[:i], s[i + 1:]]
    return [s]


def strip_then(cond):
    return re.sub(r"\s+then$", "", cond.strip(), flags=re.I)


def ends_flow(items):
    """Does this statement list end in End / Return on every path?"""
    if not items:
        return False
    last = items[-1]
    if isinstance(last, Node):
        return last.terminal
    if isinstance(last, If):
        return ends_flow(last.then) and ends_flow(last.orelse)
    if isinstance(last, Select):
        return bool(last.branches) and all(ends_flow(b[1]) for b in last.branches)
    return False


def parse_program(text):
    """Pseudocode text -> [Chart, ...] with the main chart first."""
    lines = join_lines(text.splitlines())
    top, modules, declares, outs = [], [], [], []
    counted, here = [0], [0]            # statement numbers, and where we are
    run_at = [0]                        # where the run being gathered began
    stack = [Frame(None, top, -1)]
    # No "End If" / "End While" anywhere but the lines are indented?  Then
    # indentation closes the blocks, Python style.
    indent_mode = (any(ind > 0 for ind, _, _ in lines)
                   and not any(R_CLOSER.match(tidy(t)) for _, t, _ in lines))

    def cur():
        return stack[-1]

    def flush():
        """Empty whichever run of same-kind statements is still open.

        Declares pile into one box, and so does a run of Displays: the four
        lines of a menu are one thing the program says, and four separate
        parallelograms for them make the chart taller without telling the
        reader anything the one symbol does not.  A run only ever holds one
        kind, because whichever kind comes next flushes the other first, and
        it is capped at GROUP_MAX lines so a long stretch of output does not
        grow into one enormous symbol."""
        if declares:
            box = Node("rect", "\n".join(declares))
            box.line = run_at[0]
            cur().items.append(stamp(box))
            del declares[:]
        if outs:
            box = Node("io", "\n".join(outs))
            box.line = run_at[0]
            cur().items.append(stamp(box))
            del outs[:]

    def add(item):
        cur().items.append(stamp(item))

    def stamp(item):
        """Give a statement its number, and the line it was typed on."""
        counted[0] += 1
        item.node_id = counted[0]
        if not getattr(item, "line", 0):
            item.line = here[0]
        return item

    def find(test):
        """Index of the innermost open frame whose owner passes test, or -1."""
        for i in range(len(stack) - 1, 0, -1):
            if test(stack[i].owner):
                return i
        return -1

    def close(test, cond=None, until=None):
        """Close the innermost matching structure, plus anything left open inside it."""
        i = find(test)
        if i < 0:
            return False
        owner = stack[i].owner
        if cond is not None:
            owner.cond = cond
        if until is not None:
            owner.until = until
        del stack[i:]
        while isinstance(owner, If) and owner.chained and isinstance(cur().owner, If):
            owner = cur().owner                    # End If closes the whole Else-If chain
            stack.pop()
        return True

    def is_if(o):
        return isinstance(o, If)

    def is_loop(o):
        return isinstance(o, (Loop, For))

    def is_post(o):
        return isinstance(o, Loop) and o.style == "post" and not o.cond

    def is_sel(o):
        return isinstance(o, Select)

    def is_any(o):
        return not isinstance(o, Module)

    def while_closes_do(idx):
        """Inside a Do: is this 'While cond' the end of the Do, or a nested
        loop?  Scan ahead: a nested While owns the next unmatched End While."""
        depth = bare = 0
        for _, t, _no in lines[idx + 1:]:
            k = tidy(t).lower()
            if R_MODULE.match(k) or R_ENDMOD.match(k):
                break
            if re.match(r"^(do|repeat)$", k):
                bare += 1
            elif re.match(r"^(until\s|loop\s+(while|until)\s)", k):
                bare = max(0, bare - 1)
            elif re.match(r"^while\b", k):
                if bare:
                    bare -= 1                      # closes a later Do
                else:
                    depth += 1
            elif re.match(r"^do\s+(while|until)\b", k):
                depth += 1
            elif re.match(r"^(end[ -]?(while|loop|do)|endwhile|wend|loop)$", k):
                if depth == 0:
                    return False                   # that End While is ours
                depth -= 1
        return True

    for idx, (indent, raw, at_line) in enumerate(lines):
        here[0] = at_line
        s = tidy(raw)
        if not s:
            if outs:
                flush()       # a blank line between two Displays keeps them
            continue          #   apart: the spacing is the author's to set

        if indent_mode and len(stack) > 1 and indent <= cur().indent \
                and not (R_ELSE.match(s) or R_ELSEIF.match(s) or R_CASE.match(s)):
            flush()                                # dedent: close open blocks
            while len(stack) > 1 and indent <= cur().indent:
                stack.pop()

        if R_DECL.match(s):                        # declarations: one shared box
            if outs:
                flush()
            if not declares:
                run_at[0] = at_line
            declares.append(s)
            continue
        if GROUP_OUTPUT and R_OUT.match(s) and not R_CLOSER.match(s):
            if declares or len(outs) >= GROUP_MAX:  # a run of Displays shares
                flush()                             #   one symbol as well
            if not outs:
                run_at[0] = at_line
            outs.append(s)
            continue
        flush()

        m = R_MODULE.match(s)
        if m:                                      # a new module closes everything
            del stack[1:]
            mod = make_module(m.group(1), m.group(2), s)
            modules.append(mod)
            stack.append(Frame(mod, mod.items, indent))
            continue
        if R_END.match(s):
            add(Node("oval", word("end"), terminal=True))
            continue
        if R_ENDMOD.match(s):
            del stack[1:]
            continue
        if R_ENDIF.match(s):
            close(is_if)
            continue
        if R_ENDSEL.match(s):
            close(is_sel)
            continue
        m = R_LOOPCOND.match(s)                    # Loop While c / Loop Until c
        if m:
            if not close(is_post, cond=unwrap(m.group(2)), until=m.group(1).lower() == "until"):
                close(is_loop)
            continue
        if R_ENDLOOP.match(s):
            close(is_loop)
            continue
        m = R_UNTIL.match(s)
        if m:
            if not close(is_post, cond=unwrap(m.group(1)), until=True):
                add(simple_node(s))
            continue
        if R_ENDANY.match(s):                      # some "End Xyz" we don't know
            close(is_any)
            continue

        m = R_ELSEIF.match(s)
        if m and find(is_if) >= 0:
            del stack[find(is_if) + 1:]
            node = If(unwrap(strip_then(m.group(2))))
            node.chained = True
            cur().owner.orelse.append(node)
            stack.append(Frame(node, node.then, cur().indent))
            continue
        if m:
            s = "If " + m.group(2)                 # stray Else If: treat as an If
        if R_ELSE.match(s):
            i = find(lambda o: isinstance(o, (If, Select)))
            if i >= 0:
                del stack[i + 1:]
                fr = cur()
                if isinstance(fr.owner, If):
                    fr.items = fr.owner.orelse
                else:
                    fr.owner.branches.append(["Else", []])
                    fr.items = fr.owner.branches[-1][1]
            continue
        m = R_SELECT.match(s)
        if m:
            node = Select(unwrap(m.group(2)))
            add(node)
            stack.append(Frame(node, node.pre, indent))
            continue
        m = R_CASE.match(s)
        if m and find(is_sel) >= 0:
            del stack[find(is_sel) + 1:]
            fr = cur()
            fr.owner.branches.append([m.group(2) or "Default", []])
            fr.items = fr.owner.branches[-1][1]
            continue

        m = R_IF.match(s)
        if m:
            parts = R_THEN.split(m.group(1), 1)
            if len(parts) == 1:
                parts = split_outside_quotes(parts[0], ":")
            node = If(unwrap(parts[0]))
            inline = parts[1].strip() if len(parts) > 1 else ""
            add(node)
            if inline:                             # If c Then stmt [Else stmt]
                halves = R_ELSE_INLINE.split(inline, 1)
                node.then.append(simple_node(halves[0]))
                if len(halves) > 1 and halves[1].strip():
                    node.orelse.append(simple_node(halves[1]))
            else:
                stack.append(Frame(node, node.then, indent))
            continue
        m = R_WHILE.match(s)
        if m:
            cond = unwrap(re.sub(r"\s+do$", "", m.group(1), flags=re.I))
            if find(is_post) >= 0 and while_closes_do(idx):
                close(is_post, cond=cond, until=False)
                continue
            node = Loop("pre", cond)
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue
        m = R_DO.match(s)
        if m:
            if m.group(2):                         # Do While c / Do Until c ... Loop
                node = Loop("pre", unwrap(m.group(3)))
                node.until = m.group(2).lower() == "until"
            else:
                node = Loop("post")
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue
        if R_REPEAT.match(s):
            node = Loop("post")
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue
        m = R_FOR.match(s)
        if m:
            node = parse_for(m.group(1).strip(), s)
            add(node)
            stack.append(Frame(node, node.body, indent))
            continue

        add(simple_node(s))

    flush()
    del stack[1:]

    # ----- one chart per module; globals and main() share the first chart
    main = next((mod for mod in modules if mod.name.lower() == "main"), None)
    names = set(mod.name.lower() for mod in modules)
    top = [it for it in top if not (isinstance(it, Node) and             # "main()"
           re.match(r"^\w+\(.*\)$", it.text) and it.text.split("(")[0].lower() in names)]
    charts = []
    if main is not None:
        charts.append(Chart("Module main()", top + main.items, True, main))
    elif top or not modules:
        charts.append(Chart("main", top, True, None))
    for mod in modules:
        if mod is not main:
            heading = " ".join(w for w in (mod.kind.capitalize(), mod.rtype, mod.signature()) if w)
            charts.append(Chart(heading, mod.items, False, mod))

    for chart in charts:
        items = chart.items
        first = items[0] if items else None
        opens = (isinstance(first, Node) and first.shape == "oval"
                 and first.text == word("start"))
        if not opens:
            label = word("start") if chart.is_main else chart.module.signature()
            items.insert(0, stamp(Node("oval", label)))
        if not ends_flow(items):
            items.append(stamp(Node("oval", word("end") if chart.is_main
                                    else word("ret"), terminal=True)))
    return charts



# ------------------------------------------------------------ what it means --
# The chart says what the program looks like.  This says what it *does*: the
# same parse, written out as plain data, one entry per statement, so a page
# can walk it -- run it, ask for the inputs it asks for, print what it
# prints, and turn it into Python or Java.  Nothing here draws anything.
R_SET = re.compile(r"^(?:set\s+|let\s+)?([A-Za-z_]\w*(?:\s*\[[^\]]*\])?)\s*"
                   r"(?:=|:=|<-)\s*(.+)$", re.I)
R_DECL_ONE = re.compile(
    r"^(constant|const|declare)\s+(integer|real|string|char|boolean|bool|"
    r"float|double|int|number|var|let)?\s*([A-Za-z_]\w*)\s*"
    r"(?:(?:=|:=|<-)\s*(.+))?$", re.I)
R_CALL_NAME = re.compile(r"^call\s+([A-Za-z_]\w*)\s*\((.*)\)\s*$", re.I)
R_RETURN_VAL = re.compile(r"^return\b\s*(.*)$", re.I)


def statement_json(text, node_id, line):
    """One statement, as data: what it does and what it does it to."""
    out = {"id": node_id, "line": line, "text": text}
    m = R_DECL_ONE.match(text)
    if m and R_DECL.match(text):
        out.update(op="declare", const=m.group(1).lower() != "declare",
                   type=(m.group(2) or "").title(), var=m.group(3),
                   expr=(m.group(4) or "").strip())
        return out
    if R_OUT.match(text):
        out.update(op="display", parts=text.split(None, 1)[1] if " " in text else "")
        return out
    if R_IN.match(text):
        rest = text.split(None, 1)[1] if " " in text else ""
        out.update(op="input", var=rest.strip().strip(",").strip())
        return out
    m = R_CALL_NAME.match(text)
    if m:
        out.update(op="call", name=m.group(1), args=m.group(2))
        return out
    if R_RETURN.match(text):
        out.update(op="return", expr=R_RETURN_VAL.match(text).group(1).strip())
        return out
    if R_END.match(text) or text.strip() in (word("end"), word("ret")):
        out.update(op="end")
        return out
    if R_START.match(text) or text.strip() == word("start"):
        out.update(op="start")
        return out
    m = R_SET.match(text)
    if m:
        out.update(op="set", var=m.group(1).strip(), expr=m.group(2).strip())
        return out
    out.update(op="other")
    return out


def items_json(items):
    """A run of statements, and whatever they contain."""
    out = []
    for item in items:
        kind = getattr(item, "kind", "")
        if kind == "node":
            for line in (item.text or "").split("\n"):    # a grouped box holds
                if line.strip():                          #   several statements
                    out.append(statement_json(line.strip(), item.node_id,
                                              item.line))
        elif kind == "if":
            out.append({"op": "if", "id": item.node_id, "line": item.line,
                        "cond": item.cond, "then": items_json(item.then),
                        "else": items_json(item.orelse)})
        elif kind == "loop":
            out.append({"op": "dowhile" if item.style == "post" else "while",
                        "id": item.node_id, "line": item.line,
                        "cond": item.cond, "until": bool(item.until),
                        "body": items_json(item.body)})
        elif kind == "for":
            out.append({"op": "for", "id": item.node_id, "line": item.line,
                        "init": item.init or "", "cond": item.cond or "",
                        "step": item.step or "", "raw": item.raw,
                        "body": items_json(item.body)})
        elif kind == "select":
            cases = []
            for label, inside in item.branches:
                cases.append({"match": label, "body": items_json(inside)})
            out.append({"op": "select", "id": item.node_id, "line": item.line,
                        "expr": item.expr, "cases": cases})
    return out


def program_json(charts):
    """The whole program as data: the main flow, and every module in it."""
    out = {"main": [], "modules": []}
    for chart in charts:
        body = items_json(chart.items)
        if chart.is_main:
            out["main"] = body
        else:
            mod = chart.module
            out["modules"].append({
                "name": mod.name if mod else chart.heading,
                "params": mod.params if mod else "",
                "returns": (mod.rtype if mod else ""),
                "body": body})
    return out



# ------------------------------------------------------------------- layout --
#  Drawing elements are tuples:
#      ("shape", kind, cx, cy, w, h, [text lines])
#      ("line", x1, y1, x2, y2, arrowhead?)
#      ("text", x, y, string, anchor)          branch labels
#      ("htext", x, y, string, anchor)         chart headings
def wrap(text, width_px, size=None, bold=False):
    """Wrap text to a pixel width, honoring explicit newlines."""
    out = []
    for paragraph in text.split("\n"):
        words, line = [], ""
        for w in paragraph.split():            # chop a word wider than the box
            while len(w) > 1 and text_w(w, size, bold) > width_px:
                cut = len(w) - 1
                while cut > 1 and text_w(w[:cut], size, bold) > width_px:
                    cut -= 1
                words.append(w[:cut])
                w = w[cut:]
            words.append(w)
        for w in words:
            trial = (line + " " + w).strip()
            if text_w(trial, size, bold) > width_px and line:
                out.append(line)
                line = w
            else:
                line = trial
        out.append(line)
    return out or [""]


def shift(elems, dx, dy):
    moved = []
    for e in elems:
        if e[0] == "shape":
            moved.append(("shape", e[1], e[2] + dx, e[3] + dy, e[4], e[5],
                          e[6], e[7] if len(e) > 7 else 0))
        elif e[0] == "line":
            moved.append(("line", e[1] + dx, e[2] + dy, e[3] + dx, e[4] + dy, e[5]))
        else:
            moved.append((e[0], e[1] + dx, e[2] + dy, e[3], e[4]))
    return moved


class Block:
    """A laid-out piece of chart.  Entry is (axis, 0); exit is (axis, h)."""

    def __init__(self, w, h, axis, elems, terminal=False, loop=False):
        self.w, self.h, self.axis, self.elems = w, h, axis, elems
        self.terminal = terminal        # nothing flows out of the bottom
        self.loop = loop                # the way out runs down the far side


def edge_shape(block, top=False):
    """The single shape a block ends on, or starts on if top is asked for.

    A plain run of statements has one: its last box sits flush with the foot
    of the block, on the flow line, and its first with the head.  An If or a
    loop does not -- what sits at the foot of those is the point where two
    routes meet, and a line has to leave that from below.

    Knowing the shape is what lets a route meet it at the side.  A line that
    is travelling sideways anyway can leave a box's side instead of dropping
    clear of its bottom and turning, and a line arriving sideways can go
    into the side it arrives at instead of bending to come in over the top:
    a turn fewer each time, and a shorter line.  Returns (left, right,
    middle height) in the block's own coordinates, taken at the height where
    the shape is widest, or None.
    """
    found = None
    for e in block.elems:
        if e[0] != "shape":
            continue
        flush = (e[3] - e[5] / 2.0 < 1.0 if top
                 else abs((e[3] + e[5] / 2.0) - block.h) < 1.0)
        if flush:
            if found is not None:
                return None             # two of them level: use the foot
            found = e
    if found is None:
        return None
    _, kind, cx, cy, w, _h, _lines = found[:7]
    if abs(cx - block.axis) > 1.0:      # not sitting on the flow line
        return None
    if kind in ("diamond", "hex"):
        return None                     # a test's sides are its own answers'
    # Where the outline actually is at half height, which for anything that
    # leans or bows is not where the box is.  A line meeting the box instead
    # would stop short of the shape, in mid-air beside it.
    if kind in ("io", "io_back", "trap"):
        lean = min(SLANT, w / 4.0) / 2.0          # a parallelogram's waist
    elif kind == "screen":
        lean = min(16.0, w * 0.16) / 4.0          # the bowed-in left side
    else:
        lean = 0.0
    return cx - w / 2.0 + lean, cx + w / 2.0 - lean, cy


def clear_foot(block, side):
    """Is the foot of this block clear of lines running out to that side?

    A block ending on an If leaves the last line of each branch lying along
    its foot, so a route setting off sideways from there would run down the
    top of one of them.  A block ending on a loop leaves only the loop's way
    out, which comes in from the other hand and is already going the way we
    are."""
    for e in block.elems:
        if e[0] != "line" or abs(e[2] - e[4]) > 0.5:      # horizontals only
            continue
        if abs(e[2] - block.h) > 1.5:                     # at the foot only
            continue
        reach = (min(e[1], e[3]) if side < 0 else max(e[1], e[3])) - block.axis
        if (reach < -1.0) if side < 0 else (reach > 1.0):
            return False
    return True


def tail_shape(block):
    return edge_shape(block)


def head_shape(block):
    return edge_shape(block, top=True)


def part_of(item, shape, text):
    """A shape drawn for a statement -- the diamond of an If, the boxes a For
    turns into -- carrying that statement's number, so the drawing and the
    data agree about which is which."""
    node = Node(shape, text)
    node.node_id = getattr(item, "node_id", 0)
    node.line = getattr(item, "line", 0)
    return node


def node_block(node):
    longest = max(text_w(l) for l in node.text.split("\n"))
    drawn = SHAPES.get(geom_of(node.shape), SHAPES["rect"])
    if drawn.get("wide"):                       # a diamond: the words sit in
        w = max(DIA_W, min(NODE_MAX_W + 60, longest / 0.55 + 10))
        inner = w * 0.55                        #   the middle band of it
    else:
        pad = drawn["side"]
        base = OVAL_W if drawn.get("floor") == "oval" else NODE_W
        w = max(base, min(NODE_MAX_W, longest + pad))
        inner = w - pad
    lines = wrap(node.text, inner)
    if drawn.get("wide"):
        h = max(DIA_MIN_H, 2.4 * len(lines) * LINE_H + 8)
    elif drawn.get("floor") == "oval":
        h = max(OVAL_H, len(lines) * LINE_H + 2 * PAD_Y)
    else:
        h = max(NODE_MIN_H, len(lines) * LINE_H + 2 * PAD_Y + drawn["top"])
    if drawn.get("round"):                      # a joining point is round
        h = max(h, min(w, 96), 40)
    # Up to a whole number of grid steps.  Every gap between shapes is a whole
    # number too, so a chart built out of these lands on the ruling behind it
    # instead of floating a few pixels off it all the way down.
    if GRID_STEP > 0:
        step = GRID_STEP * 2            # so h / 2 is a whole step as well
        h = math.ceil(h / step - 0.001) * step
    return Block(w, h, w / 2.0,
                 [("shape", node.shape, w / 2.0, h / 2.0, w, h, lines,
                   getattr(node, "node_id", 0))],
                 node.terminal)


def layout_seq(items):
    blocks = [layout_item(it) for it in items]
    if not blocks:
        return Block(0, 0, 0, [])
    axis = max(b.axis for b in blocks)
    right = max(b.w - b.axis for b in blocks)
    elems, y = [], 0.0
    for i, b in enumerate(blocks):
        if i:
            if not blocks[i - 1].terminal:
                elems.append(("line", axis, y, axis, y + VGAP, True))
            y += VGAP
        elems += shift(b.elems, axis - b.axis, y)
        y += b.h
    return Block(axis + right, y, axis, elems, blocks[-1].terminal)


def layout_item(item):
    if item.kind == "node":
        return node_block(item)
    if item.kind == "if":
        return layout_if(item)
    if item.kind == "select":
        return layout_select(item)
    if item.kind == "for":
        return layout_for(item)
    if item.style == "post":
        return layout_post(item)
    return layout_pre(item)


def chain_parts(item):
    """An If with its Else Ifs flattened: [(cond, then), ...] and the Else.

    Only an "Else If" counts.  An If written inside an Else is a nested
    question, not another answer to the same one, and it keeps the nested
    drawing that says so."""
    tests, node = [], item
    while True:
        tests.append((node.cond, node.then, node))
        tail = node.orelse
        if len(tail) == 1 and tail[0].kind == "if" and tail[0].chained:
            node = tail[0]
            continue
        return tests, tail


def layout_chain(tests, tail, thens, other):
    """A chain of tests, one under another down the page.

    Side by side, a chain costs a lane for every branch it has, and the
    four branches of a menu come out wider than the paper they are going
    on: scaled to fit the page, the lettering ends up too small to read.
    So the tests queue up instead.  Each one sits under the last, False
    carries straight on down to the next question, every True branch hangs
    in the one lane beside them, and the branches all come home on a single
    line down the outside.  The chart gets taller for it, which costs
    nothing much -- a reader scrolls, and paper takes another sheet --
    while width is what there is no more of.
    """
    dias = [node_block(part_of(owner, "diamond", cond))
            for cond, _, owner in tests]
    t_gap = max(HGAP, text_w(YES, bold=True) + LABEL_PAD)
    half = max(d.w for d in dias) / 2.0
    side = -1 if TRUE_LEFT else 1           # the hand the branches hang on
    near = max(b.w - b.axis if side < 0 else b.axis for b in thens)
    far = max(b.axis if side < 0 else b.w - b.axis for b in thens)
    lane = side * (half + t_gap + near)     # the branches' own flow line
    # and the way home, outside the branches -- and outside the Else too,
    # which sits on the flow line below them and can be wider than they are
    reach = (other.axis if side < 0 else other.w - other.axis) if other.h else 0.0
    rail = side * max(abs(lane) + far + HGAP, reach + HGAP)

    elems, backs, y = [], [], 0.0
    straight = None                         # a branch that needs no rail
    for i, (dia, then) in enumerate(zip(dias, thens)):
        d_half, mid = dia.w / 2.0, dia.h / 2.0
        last = i == len(tests) - 1
        # Where the branch opens on a box, the box is set level with the
        # middle of the diamond and True runs straight into its side.  The
        # answer and what it leads to then sit on one line, and there is no
        # corner in between to follow.  A branch that opens on something
        # else -- another question, a loop -- is met over the top as before.
        head = head_shape(then) if then.h else None
        sink = max(0.0, (head[2] - mid) if head else 0.0)
        if sink:                            # a tall box: let the test down
            elems.append(("line", 0, y, 0, y + sink, False))
        d_top = y + sink
        cy = d_top + mid
        elems += shift(dia.elems, -dia.axis, d_top)
        elems.append(("text", side * (d_half + 6), cy - 6, YES,
                      "end" if side < 0 else "start"))
        d_bot = d_top + dia.h
        if head:                            # straight in at the side
            elems.append(("line", side * d_half, cy,
                          lane + (head[1] if side < 0 else head[0]) - then.axis,
                          cy, True))
            b_top = cy - head[2]
        else:
            elems.append(("line", side * d_half, cy, lane, cy, not then.h))
            b_top = d_bot
            if then.h:
                elems.append(("line", lane, cy, lane, b_top, True))
        if then.h:
            elems += shift(then.elems, lane - then.axis, b_top)
            bot = b_top + then.h
            if not then.terminal:
                # The last branch has nothing under it in the lane, so it
                # goes home the short way: straight down where it stands
                # and one turn in.  Every branch above it has the branches
                # below in the way, and has to step out to the rail first --
                # and it does that out of the side of the box it ends on,
                # where it ends on one, rather than dropping clear and
                # turning.
                if last and abs(lane) > reach + HGAP / 2.0:
                    straight = bot
                else:
                    foot = tail_shape(then)
                    edge = None
                    if foot:
                        edge = (foot[0] if side < 0 else foot[1]) \
                               - then.axis + lane
                    if edge is not None and abs(edge - rail) > 2:
                        back = foot[2] + b_top
                        elems.append(("line", edge, back, rail, back, False))
                    else:
                        back = bot + VGAP / 2.0
                        elems += [("line", lane, bot, lane, back, False),
                                  ("line", lane, back, rail, back, False)]
                    backs.append(back)
        else:                               # an empty Then: straight home
            bot = d_bot
            backs.append(cy)
        nxt = max(bot, d_bot) + VGAP
        elems += [("line", 0, d_bot, 0, nxt, not (last and not other.h)),
                  ("text", -side * 5, d_bot + 14, NO,
                   "start" if side < 0 else "end")]
        y = nxt

    if other.h:                             # the Else, on the line it is on
        elems += shift(other.elems, -other.axis, y)
        foot, done = y + other.h, other.terminal
    else:
        foot, done = y, False

    # the rail's side reaches out to it; the other side only has to hold the
    # diamonds and the Else, which sit on the flow line
    tail_out = other.axis if side > 0 else other.w - other.axis
    inner = max(half, tail_out if other.h else 0)
    left, right = (-rail, inner) if side < 0 else (inner, rail)

    if not backs and straight is None and done:   # every answer ended the flow
        return Block(left + right, foot, left, shift(elems, left, 0), True)

    coming = backs + ([straight] if straight is not None else [])
    merge = max([foot] + coming) + VGAP
    if not done:
        elems.append(("line", 0, foot, 0, merge, False))
    if backs:                               # the rail, down to the meeting
        elems += [("line", rail, min(backs), rail, merge, False),
                  ("line", rail, merge, lane if straight is not None else 0,
                   merge, straight is None)]
    if straight is not None:                # and the short way home, which
        elems += [("line", lane, straight, lane, merge, False),   # the rail
                  ("line", lane, merge, 0, merge, True)]          # joins
    return Block(left + right, merge, left, shift(elems, left, 0))


def layout_if(item):
    """A chain of tests goes down the page when laying it out side by
    side would come out wider than CHAIN_LIMIT; anything else forks."""
    tests, tail = chain_parts(item)
    if len(tests) > 1:
        thens = [layout_seq(t) for _, t, _owner in tests]
        other = layout_seq(tail)
        # what forking would cost: every test nests inside the last one's
        # False lane, so each one adds its diamond, its branch and the room
        # the two labels need beside it
        gaps = (max(HGAP, text_w(YES, bold=True) + LABEL_PAD)
                + max(HGAP, text_w(NO, bold=True) + LABEL_PAD))
        span = other.w + sum(node_block(part_of(owner, "diamond", cond)).w
                             + b.w + gaps
                             for (cond, _, owner), b in zip(tests, thens))
        if span > CHAIN_LIMIT:
            return layout_chain(tests, tail, thens, other)
    return layout_fork(item)


def layout_fork(item):
    """Local coordinates: the incoming flow line sits at x = 0.

    Both answers fork off the sides of the diamond -- True to the left,
    False to the right -- and meet again on the axis below, so the two
    outcomes read as two paths of equal standing and a reader never has to
    work out which answer the unlabelled line belonged to.

    An If with no Else is the one exception, and only when its true branch
    is a wide one.  There is no second branch to be even-handed about, and
    forking would buy that even-handedness with a line as long as the whole
    branch is wide -- on a big If, the longest line in the chart.  So the
    branch keeps the axis, the False side steps aside into the nearest free
    lane, and its arrow comes back and points at the line where the two
    join.

    A branch that opens on a box is set level with the middle of the
    diamond, so its answer runs straight into the side of that box with no
    corner in between.  Where a branch opens on something else -- another
    question, a loop -- there is no side to aim at and it is met over the
    top, the old way.
    """
    dia = node_block(part_of(item, "diamond", item.cond))
    then = layout_seq(item.then)
    other = layout_seq(item.orelse)
    half, mid = dia.w / 2.0, dia.h / 2.0
    elems = shift(dia.elems, -dia.axis, 0)

    # each lane sits far enough out for the word written above it to fit
    t_gap = max(HGAP, text_w(YES, bold=True) + LABEL_PAD)
    e_gap = max(HGAP, text_w(NO, bold=True) + LABEL_PAD)
    top = dia.h + VGAP

    t_side = -1 if TRUE_LEFT else 1     # which hand True goes out on
    e_side = -t_side

    def lane_at(blk, gap, side):
        """Where a branch's own flow line sits, out far enough on that side
        that the widest thing in it still clears the diamond."""
        out = blk.axis if side > 0 else blk.w - blk.axis
        return side * (half + gap + out)

    if not item.orelse and half + t_gap + (then.w - then.axis) > FORK_LIMIT:
        y = top + then.h
        elems += [("line", 0, dia.h, 0, top, True),
                  ("text", -e_side * 5, dia.h + VGAP / 2.0 + 4, YES,
                   "end" if e_side > 0 else "start")]
        elems += shift(then.elems, -then.axis, top)
        merge = y + VGAP
        if not then.terminal:
            elems.append(("line", 0, y, 0, merge, False))
        out = then.w - then.axis if e_side > 0 else then.axis
        lane = e_side * (max(half, out) + e_gap)       # clear of the branch
        elems += [("line", e_side * half, mid, lane, mid, False),
                  ("text", e_side * (half + 6), mid - 6, NO,
                   "start" if e_side > 0 else "end"),
                  ("line", lane, mid, lane, merge, False),
                  ("line", lane, merge, 0, merge, True)]
        near = max(half, then.axis if e_side > 0 else then.w - then.axis)
        left = near if e_side > 0 else -lane
        right = lane if e_side > 0 else near
        return Block(left + right, merge, left, shift(elems, left, 0))

    t_axis = lane_at(then, t_gap, t_side)
    e_axis = lane_at(other, e_gap, e_side)
    both_end = then.terminal and other.terminal

    # A branch opening on a box is set level with the middle of the diamond,
    # so its answer goes straight in at the side.  If a box is taller than
    # the diamond, the diamond comes down to meet it rather than the branch
    # going up off the top of the block; the line into the diamond simply
    # runs on a little further, which is no line at all to follow.
    lanes = []
    sink = 0.0
    for blk, label, ax, sign in ((then, YES, t_axis, t_side),
                                 (other, NO, e_axis, e_side)):
        head = head_shape(blk) if blk.h else None
        if head:
            sink = max(sink, head[2] - mid)
        lanes.append([blk, label, ax, sign, head, 0.0])
    sink = max(0.0, sink)
    if sink:
        elems = [("line", 0, 0, 0, sink, False)] + shift(elems, 0, sink)
    cy, d_bot = sink + mid, sink + dia.h
    over = d_bot + VGAP                 # a branch met over the top starts here
    for lane in lanes:
        lane[5] = cy - lane[4][2] if lane[4] else over
    merge = max(lane[5] + lane[0].h for lane in lanes)
    merge += 0 if both_end else VGAP

    for side, label, ax, sign, head, b_top in lanes:
        elems.append(("text", sign * (half + 6), cy - 6, label,
                      "end" if sign < 0 else "start"))
        if head:                     # straight in at the side of the box
            elems.append(("line", sign * half, cy,
                          ax + (head[1] if sign < 0 else head[0]) - side.axis,
                          cy, True))
        else:
            elems.append(("line", sign * half, cy, ax, cy, False))
            if side.h:
                elems.append(("line", ax, cy, ax, b_top, True))
        if side.h:
            elems += shift(side.elems, ax - side.axis, b_top)
            if not side.terminal:
                # Both sides drop onto one rail and join there.  Neither
                # carries a head: two heads meeting nose to nose at the same
                # point reads as a collision.  The single arrow leaving the
                # join says which way it goes.
                elems += [("line", ax, b_top + side.h, ax, merge, False),
                          ("line", ax, merge, 0, merge, False)]
        else:                        # nothing on this side: an empty lane
            elems += [("line", ax, cy, ax, merge, False),
                      ("line", ax, merge, 0, merge, False)]

    lefty, righty = ((then, t_axis), (other, e_axis))[::-t_side]
    left = -lefty[1] + lefty[0].axis
    right = righty[1] + (righty[0].w - righty[0].axis)
    return Block(left + right, merge, left, shift(elems, left, 0), both_end)


def layout_pre(item):
    """While: test first.  (Do Until ... Loop swaps the Yes / No labels.)"""
    shape = "hex" if item.hex else "diamond"
    dia = node_block(part_of(item, shape, item.cond))
    body = layout_seq(item.body)
    half = dia.w / 2.0
    into, out = (NO, YES) if item.until else (YES, NO)
    if item.hex:
        into = out = ""

    elems = shift(dia.elems, -dia.axis, 0)
    y = dia.h
    elems += [("line", 0, y, 0, y + VGAP, True),
              ("text", 5, y + VGAP / 2.0 + 4, into, "start")]
    y += VGAP
    elems += shift(body.elems, -body.axis, y)
    body_top = y
    y += body.h

    back_x = -(max(half, body.axis) + HGAP)
    if not body.terminal:
        # The way back starts by going sideways, so where the body ends on a
        # box it leaves that box's side.  Dropping out of the bottom first
        # only to turn left buys nothing and costs a corner.
        foot = tail_shape(body)
        edge = foot[0] - body.axis if foot else None
        if edge is not None and edge - 2 > back_x:
            turn = foot[2] + body_top
            elems.append(("line", edge, turn, back_x, turn, False))
        elif clear_foot(body, -1):
            # Nothing of the body's lies along its foot on this side, so the
            # way back sets off from the foot itself.  Stepping down first
            # and then turning puts a jog in the line for no reason -- and
            # where what ends the body is a loop, whose own way out arrives
            # at that foot going this way already, the two are one straight
            # line and read as one.
            turn = y
            elems.append(("line", 0, turn, back_x, turn, False))
        else:
            turn = y + VGAP / 2.0
            elems += [("line", 0, y, 0, turn, False),
                      ("line", 0, turn, back_x, turn, False)]
        elems += [("line", back_x, turn, back_x, -LOOP_UP, False),
                  ("line", back_x, -LOOP_UP, 0, -LOOP_UP, False),
                  ("line", 0, -LOOP_UP, 0, 0, True)]

    exit_y = y + VGAP
    right_x = max(half, body.w - body.axis) + max(
        HGAP, text_w(out, bold=True) + LABEL_PAD)
    # The way out is not finished when it reaches the line below: it *is*
    # that line, and carries on down it.  Left as the end of a route it
    # would stop dead there with a head on it, and the turn would come out
    # square, drawn as two strokes meeting rather than one line bending.
    elems += [("line", half, dia.h / 2.0, right_x, dia.h / 2.0, False),
              ("text", half + 6, dia.h / 2.0 - 6, out, "start"),
              ("line", right_x, dia.h / 2.0, right_x, exit_y, False),
              ("line", right_x, exit_y, 0, exit_y, False)]

    left = -back_x
    return Block(left + right_x, exit_y + LOOP_UP, left,
                 shift(elems, left, LOOP_UP), loop=True)


def layout_post(item):
    """Do ... While / Do ... Until / Repeat ... Until: body first, test last."""
    body = layout_seq(item.body)
    dia = node_block(part_of(item, "diamond", item.cond or word("again")))
    half = dia.w / 2.0
    again, done = (NO, YES) if item.until else (YES, NO)

    elems = shift(body.elems, -body.axis, 0)
    y = body.h
    if not body.terminal:
        elems.append(("line", 0, y, 0, y + VGAP, True))
    y += VGAP
    dia_cy = y + dia.h / 2.0
    elems += shift(dia.elems, -dia.axis, y)
    y += dia.h

    back_x = -(max(half, body.axis) + HGAP)
    elems += [("line", -half, dia_cy, back_x, dia_cy, False),
              ("text", -half - 6, dia_cy - 6, again, "end"),
              ("line", back_x, dia_cy, back_x, -LOOP_UP, False),
              ("line", back_x, -LOOP_UP, 0, -LOOP_UP, False),
              ("line", 0, -LOOP_UP, 0, 0, True),
              ("text", 5, y + 13, done, "start")]

    left = -back_x
    right = max(half, body.w - body.axis)
    return Block(left + right, y + LOOP_UP, left, shift(elems, left, LOOP_UP))


def layout_for(item):
    if FOR_STYLE == "expand" and item.cond:
        loop = Loop("pre", item.cond)
        loop.node_id, loop.line = item.node_id, item.line
        step = [part_of(item, "rect", item.step)] if item.step else []
        start = [part_of(item, "rect", item.init)] if item.init else []
        loop.body = list(item.body) + step
        return layout_seq(start + [loop])
    loop = Loop("pre", item.raw)             # one hexagon holding the whole For
    loop.hex = True
    loop.node_id, loop.line = item.node_id, item.line
    loop.body = item.body
    return layout_pre(loop)


def layout_select(item):
    """Case structure: one diamond, one branch per Case, all merging below."""
    dia = node_block(Node("diamond", item.expr))
    if not item.branches:
        return dia
    branches = []
    for label, items in item.branches:
        b = layout_seq(items)
        need = text_w(label, bold=True) + 14     # room for the label beside the line
        if b.w - b.axis < need:
            b = Block(b.axis + need, b.h, b.axis, b.elems, b.terminal)
        branches.append((label, b))

    # branches side by side, their axes spread under the diamond
    axes, x = [], 0.0
    for i, (label, b) in enumerate(branches):
        if i:
            x += HGAP
        axes.append(x + b.axis)
        x += b.w
    span = x
    center = span / 2.0
    bus_y = dia.h + VGAP / 2.0
    top = dia.h + VGAP + GRID_STEP
    tallest = max(b.h for _, b in branches)
    all_end = all(b.terminal for _, b in branches)
    merge = top + tallest + (0 if all_end else VGAP)

    elems = shift(dia.elems, center - dia.axis, 0)
    elems += [("line", center, dia.h, center, bus_y, len(axes) > 1),
              ("line", min(axes), bus_y, max(axes), bus_y, False)]
    x = 0.0
    for i, (label, b) in enumerate(branches):
        if i:
            x += HGAP
        ax = axes[i]
        elems.append(("text", ax + 5, bus_y + 15, label, "start"))
        if b.h == 0:                              # empty Case: one plain line
            if not all_end:
                elems.append(("line", ax, bus_y, ax, merge, ax != center))
        else:
            elems.append(("line", ax, bus_y, ax, top, True))
            elems += shift(b.elems, x, top)
            if not b.terminal:
                elems.append(("line", ax, top + b.h, ax, merge, ax != center))
        x += b.w
    if not all_end:
        live = [axes[i] for i, (_, b) in enumerate(branches) if not b.terminal]
        lo, hi = min(live + [center]), max(live + [center])
        elems.append(("line", lo, merge, hi, merge, False))

    left = max(center, dia.w / 2.0)
    width = max(span, dia.w)
    return Block(width, merge, left, shift(elems, left - center, 0), all_end)


# ----------------------------------------------------------- column packing --
def pack_columns(blocks, max_h):
    """Fill one column at a time, top to bottom, breaking past max_h.

    A block taller than max_h all by itself -- a long If, say -- cannot be
    split, so it overshoots its column.  When that happens the shapes after
    it stay in the same column until they would fill a column of their own,
    instead of each starting a fresh one: an End stranded by itself at the
    top of an empty column, a whole page above the branch that reaches it,
    helps nobody.
    """
    columns, current, height, room = [], [], 0.0, max_h
    heights = []
    for b in blocks:
        add = b.h + (VGAP if current else 0)
        if current and height + add > room:
            columns.append(current)
            heights.append(height)
            current, height = [b], b.h
            room = b.h + max_h if b.h > max_h else max_h
        else:
            current.append(b)
            height += add
            if len(current) == 1:
                room = b.h + max_h if b.h > max_h else max_h
    if current:
        columns.append(current)
        heights.append(height)

    # Never end a column on something with no side to leave from.
    #
    # A plain box has a bottom edge and two sides, so the arrow on to the next
    # column can set off from whichever suits.  The foot of a loop, an If or a
    # Case is not a shape at all -- it is the point where two or three routes
    # meet -- so the arrow has to start at the middle and work outwards.  That
    # is where the ugliness came from: the routes arriving at that point come
    # in from the sides, so the line would come in from the right, drop an
    # inch, and set straight back out to the right again past where it had
    # just been.
    #
    # Where there is something else in the column, the offending block goes to
    # the next one and the break happens a shape earlier, at a plain box.
    # Where it is the whole column -- a column shorter than the block itself,
    # so it was overshooting anyway -- there is nothing to break before, and
    # the next shape comes back to join it.
    def lift(i, j, at):                 # move one block from column j to i
        moved = columns[j].pop(at)
        columns[i].insert(len(columns[i]) if at == 0 else 0, moved)
        heights[j] -= moved.h + VGAP
        heights[i] += moved.h + VGAP

    def no_side(col):
        return bool(col) and not col[-1].terminal and tail_shape(col[-1]) is None

    # A column with next to nothing in it is worse than no break at all: the
    # arrow to reach it still climbs a whole column and runs back over the top
    # of the chart, and all it buys is an End sitting alone at the head of an
    # empty lane.  Give a runt back to the column before it.  This is settled
    # first, because merging two columns changes what the earlier one ends on.
    runt = max(120.0, max_h * 0.3)
    while len(columns) > 1 and heights[-1] < runt:
        tail, tall = columns.pop(), heights.pop()
        columns[-1].extend(tail)
        heights[-1] += VGAP + tall

    # Moving a block changes what the column it came from ends on, and what
    # the column it went to begins with, so one pass is not enough: it is
    # worked over until nothing more needs moving.  The count is a guard
    # against a pair of columns handing the same block back and forth, which
    # cannot happen with these rules but costs nothing to rule out.
    for _ in range(8):
        shifted = False
        for i in range(len(columns) - 1):
            while len(columns[i]) > 1 and no_side(columns[i]):
                lift(i + 1, i, -1)      # hand it on to the next column
                shifted = True
            while no_side(columns[i]) and columns[i + 1]:
                lift(i, i + 1, 0)       # or bring the next shape back to it
                shifted = True
        live = [n for n, col in enumerate(columns) if col]
        columns = [columns[n] for n in live]
        heights = [heights[n] for n in live]
        if not shifted:
            break
    return columns


def choose_columns(blocks, max_h):
    """Decide where the chart should break into columns.

    Given a height to obey, obey it.  Given none, don't break it at all.
    A flowchart is allowed to be tall -- that is the shape of the thing --
    and every break costs an arrow that has to climb the whole column it
    leaves and run back over the top of the chart to reach the next one,
    which is a great deal harder to follow than simply scrolling down.
    """
    return pack_columns(blocks, max_h) if max_h else [list(blocks)]


def build_columns(items, max_h):
    """Lay the chart out top-to-bottom, wrapping into columns."""
    blocks = [layout_item(it) for it in items]
    if not blocks:
        return []
    laid, x = [], 0.0
    for col in choose_columns(blocks, max_h):
        axis = max(b.axis for b in col)
        right = max(b.w - b.axis for b in col)
        elems, y, last_top = [], 0.0, 0.0
        for i, b in enumerate(col):
            if i:
                if not col[i - 1].terminal:
                    elems.append(("line", axis, y, axis, y + VGAP, True))
                y += VGAP
            last_top = y
            elems += shift(b.elems, axis - b.axis, y)
            y += b.h
        head, tail = col[0], col[-1]
        # Where an arrow can meet the shape at each end of the column instead
        # of dropping out of a bottom or coming in over a top: the side of the
        # first shape to arrive at, and the side of the last one to leave
        # from.  Either is None where the column ends on something that is not
        # a plain shape -- the foot of an If or a loop is a meeting of routes,
        # and a line has to leave that from below.
        came = head_shape(head)
        went = edge_shape(tail)
        here = {"x": x, "axis": x + axis, "h": y,
                "right": x + axis + right,
                "elems": shift(elems, x, 0),
                "open": not tail.terminal}
        if came:
            here["in_x"] = x + axis - head.axis + came[0]
            here["in_y"] = came[2]
        if went and not tail.terminal:
            here["out_x"] = x + axis - tail.axis + went[1]
            here["out_y"] = last_top + went[2]
        laid.append(here)
        x += axis + right + COL_GAP
    return laid


def connect_columns(cols):
    """One arrow from the foot of a column, up the empty gutter beside it
    and into the head of the next.  The gutter is clear by construction, so
    the route never has to cross anything on the way.  This only happens at
    all when a column height was asked for: left alone, a chart is one
    column and needs no such arrow.

    It goes in at the side of the first shape rather than over the top of
    it, which is the shorter way round and the plainer one to follow: four
    turns instead of five, no run back across the whole width of the chart,
    and it arrives pointing at the shape it is arriving at."""
    elems = []
    for a, b in zip(cols, cols[1:]):
        if not a["open"]:
            continue
        gutter = (a["right"] + b["x"]) / 2.0
        # Out of the side of the last shape where it has one, which is a
        # straight run into the gutter.  Dropping out of its bottom first only
        # to turn and climb back up past it buys nothing and reads as a
        # mistake, which is what it looked like.
        leaves = a.get("out_x")
        if leaves is not None and gutter > leaves + 1.0:
            at = a["out_y"]
            off = [("line", leaves, at, gutter, at, False)]
        else:
            at = a["h"] + VGAP * 0.55
            off = [("line", a["axis"], a["h"], a["axis"], at, False),
                   ("line", a["axis"], at, gutter, at, False)]

        into = b.get("in_y")
        side = b.get("in_x")
        if into is not None and side is not None and side > gutter + 1.0:
            elems += off + [("line", gutter, at, gutter, into, False),
                            ("line", gutter, into, side, into, True)]
            continue
        lane = -VGAP * 0.75               # clear of the top of both columns
        elems += off + [("line", gutter, at, gutter, lane, False),
                        ("line", gutter, lane, b["axis"], lane, False),
                        ("line", b["axis"], lane, b["axis"], 0, True)]
    return elems


def bbox(elems):
    xs, ys = [], []
    for e in elems:
        if e[0] == "shape":
            _, _, cx, cy, w, h = e[:6]
            xs += [cx - w / 2.0, cx + w / 2.0]
            ys += [cy - h / 2.0, cy + h / 2.0]
        elif e[0] == "line":
            xs += [e[1], e[3]]
            ys += [e[2], e[4]]
        else:
            _, x, y, s, anchor = e
            tw = (text_w(s, 13, True) if e[0] == "htext"
                  else text_w(s, FONT_SIZE, True) + 8)
            if anchor == "end":
                xs += [x - tw, x]
            elif anchor == "middle":
                xs += [x - tw / 2.0, x + tw / 2.0]
            else:
                xs += [x, x + tw]
            ys += [y - 12, y + 3]
    if not xs:
        return 0.0, 0.0, 0.0, 0.0
    return min(xs), min(ys), max(xs), max(ys)


def layout_chart(chart, max_h, heading=True):
    """One chart -> (elems, w, h) with its top-left corner at (0, 0)."""
    cols = build_columns(chart.items, max_h)
    elems = connect_columns(cols)
    for c in cols:
        elems += c["elems"]
    minx, miny, maxx, maxy = bbox(elems)
    elems = shift(elems, -minx, -miny)
    w, h = maxx - minx, maxy - miny
    if heading:
        hw = max(w, 360.0)
        lines = wrap(chart.heading, hw, 13, True)
        head_h = HEADING_H + (len(lines) - 1) * 17
        elems = shift(elems, 0, head_h)
        for i, line in enumerate(lines):
            elems.append(("htext", 0, 14 + i * 17, line, "start"))
        w, h = max(w, hw), h + head_h
    return elems, w, h


def arrange(layouts):
    """Place charts left-to-right, starting a new row past MAX_ROW_W."""
    limit = max(MAX_ROW_W, max(l[1] for l in layouts))
    rows, widths = [], []                         # first fit: fill earlier rows
    for lay in layouts:
        w = lay[1]
        for i, row in enumerate(rows):
            if widths[i] + CHART_GAP + w <= limit:
                row.append(lay)
                widths[i] += CHART_GAP + w
                break
        else:
            rows.append([lay])
            widths.append(w)
    elems, y = [], 0.0
    for row in rows:
        x, tallest = 0.0, max(l[2] for l in row)
        for el, w, h in row:
            elems += shift(el, x, y)
            x += w + CHART_GAP
        y += tallest + CHART_GAP
    return elems



# ---------------------------------------------------------------- svg output --
def chain_lines(lines):
    """Glue segments that meet end-to-start into one route.

    The layout code puts an elbow down as two or three separate segments;
    drawn that way each is its own stroke and only the last one carries a
    head.  Chained, an elbow reads as a single arrow from where the flow
    leaves to where it arrives.  A point where more than one route meets is
    left alone, so two branches merging still read as two arrows.
    """
    at = lambda x, y: (round(x, 1), round(y, 1))
    leaving, arriving = collections.Counter(), collections.Counter()
    for _, x1, y1, x2, y2, _a in lines:
        leaving[at(x1, y1)] += 1
        arriving[at(x2, y2)] += 1
    onward = {}
    for e in lines:
        onward.setdefault(at(e[1], e[2]), []).append(e)

    def corner(pt):                 # one line in and one line out: a bend
        return arriving[pt] == 1 and leaving[pt] == 1

    used, routes = set(), []

    def walk(seed):
        pts, cur, arrow = [(seed[1], seed[2])], seed, seed[5]
        while True:
            used.add(id(cur))
            pts.append((cur[3], cur[4]))
            arrow = cur[5]
            here = at(cur[3], cur[4])
            nxt = [x for x in onward.get(here, []) if id(x) not in used]
            if arrow or not corner(here) or not nxt:
                break
            cur = nxt[0]
        routes.append((pts, arrow))

    def fed_by_spare(pt):           # is some untaken segment aimed at pt?
        return any(id(x) not in used and at(x[3], x[4]) == pt for x in lines)

    for e in lines:                 # routes that start at a clear head
        if id(e) not in used and not corner(at(e[1], e[2])):
            walk(e)
    again = True                    # then routes that pick up where some
    while again:                    #   other route's arrowhead landed
        again = False
        for e in lines:
            if id(e) not in used and not fed_by_spare(at(e[1], e[2])):
                walk(e)
                again = True
    for e in lines:                 # a closed ring, if one ever turns up
        if id(e) not in used:
            walk(e)
    return routes


def arrow_head(pts):
    """The filled triangle that finishes a route, and where the line
    should stop so the stroke does not poke out through the point.

    This is drawn as an ordinary polygon rather than with an SVG <marker>.
    Word, PowerPoint and Google Docs all quietly throw markers away when
    they import an SVG, which leaves a chart full of lines with no heads on
    them.  A polygon is just another shape, so every viewer draws it.
    """
    (ax, ay), (bx, by) = pts[-2], pts[-1]
    run = math.hypot(bx - ax, by - ay)
    if run < 0.01:
        return None, pts
    ux, uy = (bx - ax) / run, (by - ay) / run      # along the last segment
    nx, ny = -uy, ux                               # across it
    cx, cy = bx - ux * HEAD_LEN, by - uy * HEAD_LEN
    tri = "%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        bx, by,
        cx + nx * HEAD_WIDE / 2.0, cy + ny * HEAD_WIDE / 2.0,
        cx - nx * HEAD_WIDE / 2.0, cy - ny * HEAD_WIDE / 2.0)
    stop = list(pts)
    if run > HEAD_LEN + 1:              # let the stroke stop at the base
        stop[-1] = (cx, cy)
    return tri, stop


def path_d(pts):
    """An SVG path through pts, with the corners eased off a little."""
    clean = [pts[0]]
    for q in pts[1:]:
        if math.hypot(q[0] - clean[-1][0], q[1] - clean[-1][1]) > 0.05:
            clean.append(q)
    if len(clean) < 2:
        return ""
    d = ["M%.1f,%.1f" % clean[0]]
    for i in range(1, len(clean) - 1):
        (ax, ay), (bx, by), (cx, cy) = clean[i - 1], clean[i], clean[i + 1]
        d1 = math.hypot(bx - ax, by - ay)
        d2 = math.hypot(cx - bx, cy - by)
        r = min(CORNER_R, d1 / 2.0, d2 / 2.0)
        if r < 0.5:
            d.append("L%.1f,%.1f" % (bx, by))
            continue
        d.append("L%.1f,%.1f" % (bx - (bx - ax) / d1 * r,
                                 by - (by - ay) / d1 * r))
        d.append("Q%.1f,%.1f %.1f,%.1f" % (bx, by,
                 bx + (cx - bx) / d2 * r, by + (cy - by) / d2 * r))
    d.append("L%.1f,%.1f" % clean[-1])
    return " ".join(d)


def grid_lines(width, height):
    """The faint graph-paper grid that sits behind the chart.

    It is drawn as two ordinary <path>s -- one for the fine lines, one for
    the darker every-fifth line -- rather than as an SVG <pattern>, for the
    same reason the arrowheads are polygons rather than markers: Word and
    PowerPoint quietly drop the clever bit on import, and a path is just a
    line like any other, so every viewer draws it.  Both paths go in before
    anything else, and every shape is filled, so no grid line ever crosses a
    box, a label or a letter."""
    if not GRID or GRID_STEP <= 0:
        return []
    fine, major = [], []
    n, x = 0, 0.0
    while x <= width + 0.01:
        (major if GRID_MAJOR and n % GRID_MAJOR == 0 else fine).append(
            "M%.1f,0V%.1f" % (x, height))
        x += GRID_STEP
        n += 1
    n, y = 0, 0.0
    while y <= height + 0.01:
        (major if GRID_MAJOR and n % GRID_MAJOR == 0 else fine).append(
            "M0,%.1fH%.1f" % (y, width))
        y += GRID_STEP
        n += 1
    out = []
    for name, d, ink, wide in (("fine", fine, GRID_INK, 0.7),
                               ("major", major, GRID_INK_MAJOR, 1.0)):
        if d:
            out.append('<path class="grid %s" d="%s" fill="none" stroke="%s" '
                       'stroke-width="%s"/>' % (name, "".join(d), ink, wide))
    return out


def shape_art(kind, cx, cy, w, h, paint):
    """One shape, drawn: the outline and whatever goes with it.

    Every kind in SHAPES is here.  The first six are the ones a textbook
    uses; the rest are the ones that turn up in the back of the chapter --
    a document, a drum for a file, a wait, a joining point, a step done by
    hand -- and any of them can stand in for any kind of step.
    """
    l, r = cx - w / 2.0, cx + w / 2.0
    t, b = cy - h / 2.0, cy + h / 2.0
    lean = min(SLANT, w / 4.0)
    out = []
    if kind in ("oval", "circle"):
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" '
                   'fill="%s"/>' % (cx, cy, w / 2.0, h / 2.0, paint))
    elif kind in ("rect", "sub"):
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        if kind == "sub":
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                       % (l + BAR, t, l + BAR, b))
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                       % (r - BAR, t, r - BAR, b))
    elif kind == "io":
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l + lean, t, r, t, r - lean, b, l, b, paint))
    elif kind == "trap":
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l + lean, t, r - lean, t, r, b, l, b, paint))
    elif kind == "hex":
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l + lean, t, r - lean, t, r, cy, r - lean, b,
                      l + lean, b, l, cy, paint))
    elif kind == "doc":                       # a page, with a wave at its foot
        wave = min(10.0, h * 0.18)
        out.append('<path d="M%.1f,%.1f H%.1f V%.1f C%.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l, t, r, b - wave,
                      r - w * 0.25, b - wave * 2.2, r - w * 0.4, b + wave * 0.9,
                      cx, b - wave * 0.2,
                      l + w * 0.32, b - wave * 1.6, l + w * 0.18, b + wave * 0.7,
                      l, b - wave, paint))
    elif kind == "store":                     # a drum, for something kept
        lip = min(11.0, h * 0.24)
        out.append('<path d="M%.1f,%.1f V%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f '
                   'V%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z" fill="%s"/>'
                   % (l, t + lip, b - lip, w / 2.0, lip, r, b - lip,
                      t + lip, w / 2.0, lip, l, t + lip, paint))
        out.append('<path class="trim" d="M%.1f,%.1f A%.1f,%.1f 0 0 0 '
                   '%.1f,%.1f" fill="none"/>'
                   % (l, t + lip, w / 2.0, lip, r, t + lip))
    elif kind == "delay":                     # a wait: flat, then a half round
        bulge = min(h / 2.0, w / 2.0)
        out.append('<path d="M%.1f,%.1f H%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f '
                   'H%.1f Z" fill="%s"/>'
                   % (l, t, r - bulge, bulge, h / 2.0, r - bulge, b, l, paint))
    elif kind == "roundrect":
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                   'rx="%.1f" fill="%s"/>'
                   % (l, t, w, h, min(14.0, h / 2.4), paint))
    elif kind == "io_back":                   # leaning the other way
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l, t, r - lean, t, r, b, l + lean, b, paint))
    elif kind == "manual":                    # typed in: a sloping top
        slope = min(11.0, h * 0.28)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l, t + slope, r, t, r, b, l, b, paint))
    elif kind == "card":                      # a punched card
        nick = min(14.0, h * 0.34)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f" fill="%s"/>'
                   % (l + nick, t, r, t, r, b, l, b, l, t + nick, paint))
    elif kind == "note":                      # a page with a folded corner
        fold = min(14.0, h * 0.34)
        out.append('<path d="M%.1f,%.1f H%.1f L%.1f,%.1f V%.1f H%.1f Z" '
                   'fill="%s"/>' % (l, t, r - fold, r, t + fold, b, l, paint))
        out.append('<path class="trim" d="M%.1f,%.1f V%.1f H%.1f" fill="none"/>'
                   % (r - fold, t, t + fold, r))
    elif kind == "docs":                      # a few pages of it
        step = min(5.0, h * 0.12)
        for back in (2, 1):
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                       'rx="2" fill="%s"/>'
                       % (l + back * step, t + (2 - back) * 0, w - back * step,
                          h - back * step * 2, paint))
        out += shape_art("doc", cx - step, cy + step, w - 2 * step,
                         h - 2 * step, paint)
    elif kind == "screen":                    # shown to somebody
        bow = min(16.0, w * 0.16)
        out.append('<path d="M%.1f,%.1f H%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f '
                   'H%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l + bow, t, r - bow, h / 2.0, h / 2.0, r - bow, b,
                      l + bow, l, cy + h * 0.28, l, cy - h * 0.28, l + bow, t,
                      paint))
    elif kind == "offpage":                   # it carries on somewhere else
        point = min(18.0, h * 0.42)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f" fill="%s"/>'
                   % (l, t, r, t, r, b - point, cx, b, l, b - point, paint))
    elif kind == "loop":                      # a loop's limit: For, mostly
        cut = min(14.0, h * 0.34, w / 5.0)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l + cut, t, r - cut, t, r, t + cut, r, b, l, b,
                      l, t + cut, paint))
    elif kind == "parallel":                  # things happening side by side
        bar = max(2.5, min(5.0, h * 0.11))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        out.append('<path class="trim" d="M%.1f,%.1f H%.1f M%.1f,%.1f H%.1f" '
                   'fill="none"/>' % (l, t + bar * 2, r, l, b - bar * 2, r))
    elif kind == "stored":                    # held somewhere inside
        rule = min(11.0, w * 0.14)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        out.append('<path class="trim" d="M%.1f,%.1f V%.1f M%.1f,%.1f H%.1f" '
                   'fill="none"/>' % (l + rule, t, b, l, t + rule, r))
    elif kind == "cloud":                     # a service, or somewhere else
        # Drawn to touch its box at the middle of all four sides, which is
        # where a line joining it expects to meet it.
        qw, qh = w / 2.0, h / 2.0
        out.append('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l, cy,
                      l, cy - qh * 0.75, cx - qw * 0.72, t - qh * 0.18,
                      cx - qw * 0.34, t + qh * 0.16,
                      cx - qw * 0.1, t - qh * 0.2, cx + qw * 0.34, t - qh * 0.2,
                      cx + qw * 0.42, t + qh * 0.2,
                      cx + qw * 0.85, t + qh * 0.02, r, cy - qh * 0.7, r, cy,
                      r, cy + qh * 0.72, cx + qw * 0.5, b, cx, b,
                      cx - qw * 0.55, b, l, cy + qh * 0.75, l, cy, paint))
    elif kind == "text":                      # words on their own
        # Nothing is drawn but something has to be there to take hold of,
        # so the words sit on a pane of clear glass.
        out.append('<rect class="ghost" x="%.1f" y="%.1f" width="%.1f" '
                   'height="%.1f" fill="none" pointer-events="all"/>'
                   % (l, t, w, h))
    elif kind == "actor":                     # somebody, rather than something
        head = min(h * 0.17, w * 0.17)
        neck = t + head * 2
        hip = t + h * 0.62
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
                   % (cx, t + head, head, paint))
        out.append('<path class="trim" d="M%.1f,%.1f V%.1f M%.1f,%.1f H%.1f '
                   'M%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f" fill="none"/>'
                   % (cx, neck, hip, cx - w * 0.22, neck + h * 0.12, cx + w * 0.22,
                      cx, hip, cx - w * 0.2, b, cx, hip, cx + w * 0.2, b))
    elif kind == "callout":                   # something said about it
        tail = min(16.0, h * 0.28)
        sill = b - tail
        rnd = min(10.0, h / 4.0)
        out.append('<path d="M%.1f,%.1f H%.1f Q%.1f,%.1f %.1f,%.1f V%.1f '
                   'Q%.1f,%.1f %.1f,%.1f H%.1f L%.1f,%.1f L%.1f,%.1f H%.1f '
                   'Q%.1f,%.1f %.1f,%.1f V%.1f Q%.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l + rnd, t, r - rnd, r, t, r, t + rnd, sill - rnd,
                      r, sill, r - rnd, sill, l + w * 0.34, l + w * 0.2, b,
                      l + w * 0.24, sill, l + rnd, l, sill, l, sill - rnd,
                      t + rnd, l, t, l + rnd, t, paint))
    elif kind == "cube":
        lip = min(14.0, h * 0.26, w * 0.14)
        out.append('<path d="M%.1f,%.1f L%.1f,%.1f H%.1f V%.1f L%.1f,%.1f '
                   'H%.1f Z" fill="%s"/>'
                   % (l, t + lip, l + lip, t, r, b - lip, r - lip, b, l, paint))
        out.append('<path class="trim" d="M%.1f,%.1f H%.1f V%.1f M%.1f,%.1f '
                   'L%.1f,%.1f" fill="none"/>'
                   % (l, t + lip, r - lip, b, r - lip, t + lip, r, t))
    elif kind == "step":                      # one step of several, in a row
        notch = min(22.0, w * 0.16)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l, t, r - notch, t, r, cy, r - notch, b, l, b,
                      l + notch, cy, paint))
    elif kind == "table":
        head = min(16.0, h * 0.3)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        out.append('<path class="trim" d="M%.1f,%.1f H%.1f M%.1f,%.1f V%.1f '
                   'M%.1f,%.1f V%.1f" fill="none"/>'
                   % (l, t + head, r, l + w / 3.0, t + head, b,
                      l + w * 2.0 / 3.0, t + head, b))
    elif kind == "arrow":                     # which way it goes
        head = min(26.0, w * 0.3)
        wing = h * 0.26
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l, t + wing, r - head, t + wing, r - head, t,
                      r, cy, r - head, b, r - head, b - wing, l, b - wing, paint))
    else:                                     # a decision
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (cx, t, r, cy, cx, b, l, cy, paint))
    return out


def to_svg(elems, title=None, author=None):
    minx, miny, maxx, maxy = bbox(elems)
    head_h = TITLE_H if title else 0
    # Set the chart down so that the shapes fall on the ruling.  The nudge is
    # measured from a shape rather than from the edge of everything, because
    # the edge of everything includes labels and arrowheads sitting at
    # whatever height they happen to sit at.  Only the whole chart moves, so
    # nothing inside it is disturbed; the margin grows by up to one step.
    over, down = MARGIN - minx, MARGIN - miny + head_h
    if GRID and GRID_STEP > 0:
        tops = [e[3] - e[5] / 2.0 for e in elems if e[0] == "shape"]
        lefts = [e[2] - e[4] / 2.0 for e in elems if e[0] == "shape"]
        if tops:
            over += (-(min(lefts) + over)) % GRID_STEP
            down += (-(min(tops) + down)) % GRID_STEP
    elems = shift(elems, over, down)
    width = maxx - minx + MARGIN * 2
    height = maxy - miny + MARGIN * 2 + head_h

    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">',
        f'<rect class="sheet" width="100%" height="100%" fill="{SHEET}"/>',
    ]
    out += grid_lines(width, height)
    out += [
        f'<g font-family="{FONT}" font-size="{FONT_SIZE}" fill="none" '
        f'stroke="{INK}" stroke-width="1.3" stroke-linecap="round" '
        'stroke-linejoin="round">',
    ]
    # Named, like everything else that carries words, so that a page showing
    # the chart can recolour them with the rest.  Without the name they were
    # the only writing on the chart that stayed black whatever colour the
    # paper was put on -- which on dark paper meant they were not there.
    if title:
        out.append(f'<text class="title" x="{MARGIN}" y="25" font-size="16" '
                   f'font-weight="bold" stroke="none" fill="{INK}">'
                   f'{html.escape(title)}</text>')
        if author:
            out.append(f'<text class="author" x="{MARGIN}" y="42" stroke="none" '
                       f'fill="{INK}">{html.escape(author)}</text>')

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
            tips.append(f'<polygon class="head" points="{head}" fill="{INK}" '
                        f'stroke="{INK}" stroke-width="0.6" '
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
                       f'width="{tw:.1f}" height="13" fill="{SHEET}" '
                       'stroke="none"/>')
            out.append(f'<text class="label" x="{x:.1f}" y="{y:.1f}" '
                       f'text-anchor="{anchor}" font-weight="bold" '
                       f'stroke="none" fill="{INK}">{html.escape(s_)}</text>')
        elif e[0] == "htext":
            _, x, y, s_, anchor = e
            out.append(f'<text class="heading" x="{x:.1f}" y="{y:.1f}" '
                       f'text-anchor="{anchor}" font-size="13" '
                       f'font-weight="bold" stroke="none" fill="{INK}">'
                       f'{html.escape(s_)}</text>')
        else:
            _, shape, cx, cy, w, h, lines = e[:7]
            said = e[7] if len(e) > 7 else 0
            l, r = cx - w / 2.0, cx + w / 2.0
            t, b = cy - h / 2.0, cy + h / 2.0
            paint = FILL.get(shape, "#ffffff")
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
                           f'text-anchor="middle" stroke="none" fill="{INK}">'
                           f'{html.escape(line)}</text>')
            out.append("</g>")
    out += tips                             # the points of the arrows, on top
    out += ["</g>", "</svg>"]
    return "\n".join(out)



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
PAGE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<style>
  :root {
    --bg: #eceff3;
    --panel: #ffffff;
    --field: #fcfdfe;
    --ink: #10151b;
    --muted: #5d6b7a;
    --line: #d7dde5;
    --line-soft: #e8edf3;
    --accent: #14427c;
    --accent-soft: #e8effa;
    --good: #116149;
    --busy: #c62828;   /* the colour of something being done right now */
    --bad: #a4262c;
    --dots: #d3d9e2;
    --shadow: 0 1px 2px rgba(16, 24, 40, .06), 0 8px 24px rgba(16, 24, 40, .06);
    --radius: 10px;
    --code-bg: #f7f9fb;                 /* where the pseudocode is written */
    --code-line: #eef2f6;               /*   ruled, the way paper is */
    --code-at: #fdf0d5;                 /*   and the line being run, now */
    --code-well: rgba(16, 24, 40, .05);
    --dim: rgba(16, 24, 40, .34);   /* behind a sheet that fills the screen */
    color-scheme: light;
  }
  /* Dark, when the computer is set dark and the page has not been told
     otherwise -- and whenever it has been told to be. */
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #12161c;
      --panel: #1a2029;
      --field: #141a22;
      --ink: #e7ecf2;
      --muted: #9aa8b8;
      --line: #2c3540;
      --line-soft: #232b35;
      --accent: #5b9bf0;
      --accent-soft: #1d2a3d;
      --code-bg: #10151b;
      --code-line: #171e26;
      --code-at: #2e2418;
      --code-well: rgba(0, 0, 0, .35);
      --dim: rgba(0, 0, 0, .58);   /* behind a sheet that fills the screen */
      --good: #57c7a2;
      --busy: #ff6b6b;   /* the colour of something being done right now */
      --bad: #ff8b8b;
      --dots: #2a323d;
      --shadow: 0 1px 2px rgba(0, 0, 0, .4), 0 10px 26px rgba(0, 0, 0, .34);
      color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --code-bg: #10151b;
    --code-line: #171e26;
    --code-at: #2e2418;
    --code-well: rgba(0, 0, 0, .35);
    --dim: rgba(0, 0, 0, .58);   /* behind a sheet that fills the screen */
    --bg: #12161c;
    --panel: #1a2029;
    --field: #141a22;
    --ink: #e7ecf2;
    --muted: #9aa8b8;
    --line: #2c3540;
    --line-soft: #232b35;
    --accent: #5b9bf0;
    --accent-soft: #1d2a3d;
    --good: #57c7a2;
    --busy: #ff6b6b;   /* the colour of something being done right now */
    --bad: #ff8b8b;
    --dots: #2a323d;
    --shadow: 0 1px 2px rgba(0, 0, 0, .4), 0 10px 26px rgba(0, 0, 0, .34);
    color-scheme: dark;
  }
  * { box-sizing: border-box; }
  [hidden] { display: none !important; }   /* flex and grid outrank it otherwise */
  * { scrollbar-width: thin; scrollbar-color: var(--line) transparent; }
  ::-webkit-scrollbar { width: 11px; height: 11px; }
  ::-webkit-scrollbar-track, ::-webkit-scrollbar-corner { background: transparent; }
  ::-webkit-scrollbar-thumb {
    background: var(--line); border-radius: 8px;
    border: 3px solid transparent; background-clip: content-box;
  }
  ::-webkit-scrollbar-thumb:hover { background: var(--muted); background-clip: content-box; }
  html, body { height: 100%; }
  body {
    margin: 0; display: flex; flex-direction: column; overflow: hidden;
    background: var(--bg); color: var(--ink);
    font: 14px/1.45 "Segoe UI", system-ui, Arial, Helvetica, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  button, input, select, textarea { font: inherit; color: inherit; }

  /* ---------------------------------------------------------- top bar -- */
  .bar {
    flex: none; background: var(--panel); border-bottom: 1px solid var(--line);
    display: flex; align-items: center; gap: 10px 16px;
    padding: 10px 16px; flex-wrap: wrap; z-index: 5;
  }
  /* the mark, at the head of the bar */
  .mark {
    flex: none; display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 9px;
    background: var(--accent-soft); color: var(--accent);
  }
  .mark svg {
    width: 20px; height: 20px; fill: none; stroke: currentColor;
    stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round;
  }
  .brand { font-weight: 650; font-size: 15px; margin-right: auto; line-height: 1.25;
           min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .saves { display: flex; gap: 8px; align-items: center; }
  .pair { display: flex; }
  .pair .btn { border-radius: 8px 0 0 8px; }
  .pair select.btn { border-radius: 0 8px 8px 0; border-left: 0; padding: 7px 6px;
                     max-width: 128px; }
  .brand small { display: block; font-weight: 400; font-size: 12px; color: var(--muted); }
  .grow { margin-right: auto; }
  .btn {
    border: 1px solid var(--line); background: #fff; border-radius: 8px;
    padding: 7px 12px; cursor: pointer; white-space: nowrap;
    text-decoration: none; color: inherit; display: inline-flex;
    align-items: center; gap: 7px; transition: background .12s, border-color .12s;
  }
  .btn { background: var(--panel); }
  .btn:hover { background: var(--accent-soft); border-color: var(--accent); }
  .btn:active { filter: brightness(.96); }
  .btn.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
  .btn.primary:hover { filter: brightness(1.12); }
  .btn.ghost { background: transparent; }
  .btn[disabled] { opacity: .55; cursor: progress; }
  .btn.small { padding: 4px 9px; font-size: 12.5px; border-radius: 7px; }
  select.btn { padding: 7px 8px; }

  /* ----------------------------------------------------------- layout -- */
  main { flex: 1; display: flex; min-height: 0; }
  #panel {
    flex: none; width: 312px; background: var(--panel);
    border-right: 1px solid var(--line); overflow-y: auto; overflow-x: hidden;
    display: flex; flex-direction: column;
  }
  #panel.hide { display: none; }
  .panel-top {
    position: sticky; top: 0; z-index: 3; background: var(--panel);
    border-bottom: 1px solid var(--line); padding: 10px 12px;
    display: flex; gap: 8px; align-items: center;
  }
  .seg {
    flex: 1; display: flex; gap: 2px; padding: 2px; border-radius: 9px;
    background: var(--line-soft);
  }
  .seg-btn {
    flex: 1; border: 0; background: none; color: var(--muted); cursor: pointer;
    border-radius: 7px; padding: 6px 8px; font-size: 13px; font-weight: 550;
  }
  .seg-btn.on { background: var(--panel); color: var(--ink);
                box-shadow: 0 1px 2px rgba(16, 24, 40, .12); }
  .icon {
    flex: none; width: 34px; height: 34px; padding: 0; cursor: pointer;
    border: 1px solid transparent; border-radius: 9px; background: none;
    color: var(--muted); display: inline-flex; align-items: center;
    justify-content: center;
  }
  .icon:hover { background: var(--line-soft); color: var(--ink); }
  .icon svg { width: 19px; height: 19px; fill: none; stroke: currentColor;
              stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
  #rail {
    flex: none; width: 48px; background: var(--panel);
    border-right: 1px solid var(--line); padding: 10px 0;
    display: flex; flex-direction: column; align-items: center; gap: 6px;
  }
  #rail .icon { width: 36px; height: 36px; }
  #side-chart-panel, #side-colors-panel { padding-bottom: 20px; }
  section.card { border-bottom: 1px solid var(--line-soft); padding: 14px 16px; }
  section.card h2 {
    margin: 0 0 10px; font-size: 11.5px; letter-spacing: .07em;
    text-transform: uppercase; color: var(--muted); font-weight: 650;
    display: flex; align-items: center; justify-content: space-between; gap: 8px;
  }
  section.fold h2 { cursor: pointer; margin-bottom: 10px; }
  section.fold h2::after {
    content: ""; width: 6px; height: 6px; flex: none; margin-right: 2px;
    border: solid currentColor; border-width: 0 1.5px 1.5px 0;
    transform: rotate(45deg) translate(-1px, -2px); transition: transform .15s;
  }
  section.fold.shut h2 { margin-bottom: 0; }
  section.fold.shut h2::after { transform: rotate(-45deg) translate(-2px, -1px); }
  section.fold.shut > *:not(h2) { display: none; }
  section.card:last-child { border-bottom: 0; }
  .hint { color: var(--muted); font-size: 12.5px; margin: 8px 0 0; }

  /* ------------------------------------------------- the settings sheet -- */
  /* Anchored under the bar on the right, where its button is.  It is a
     plain box rather than a menu of actions: what is in it are choices you
     set and leave, so each one shows its state rather than doing something
     the moment you touch it. */
  .sheet-menu {
    position: fixed; z-index: 30; top: 56px; right: 14px; width: 244px;
    padding: 12px 14px 14px; background: var(--panel);
    border: 1px solid var(--line); border-radius: 12px; box-shadow: var(--shadow);
  }
  .sheet-menu h3 {
    margin: 4px 0 7px; font-size: 11.5px; letter-spacing: .07em;
    text-transform: uppercase; color: var(--muted); font-weight: 650;
  }
  .sheet-menu h3:first-child { margin-top: 0; }
  .sheet-menu .seg { margin-bottom: 4px; }
  .switch.wide {
    display: flex; align-items: center; justify-content: space-between;
    gap: 10px; width: 100%; margin-top: 12px; padding-top: 12px;
    border-top: 1px solid var(--line-soft); font-size: 13px;
  }
  .switch.wide[hidden] { display: none !important; }

  /* --------------------------------------------- the panel on the right -- */
  /* Flex order does the moving, so nothing in the panel has to know where
     it sits.  Only the borders and the arrow on the collapse button care
     which way round it is. */
  body[data-side="right"] #stage,
  body[data-side="right"] .stage-frame { order: 1; }
  body[data-side="right"] #panel { order: 2; }
  body[data-side="right"] #rail  { order: 3; }
  body[data-side="right"] #panel,
  body[data-side="right"] #rail {
    border-right: 0; border-left: 1px solid var(--line);
  }
  body[data-side="right"] #collapse svg { transform: scaleX(-1); }
  /* ------------------------------------------------- the download sheet -- */
  .sheet-menu .btn.wide {
    display: flex; width: 100%; justify-content: center; margin-top: 8px;
  }
  /* The word sits above the box, not beside it.  Beside it, the row was one
     wide label with a narrow control at the end: a click anywhere along it
     -- the word, and the empty middle, which was the larger part of it --
     opened the list, so the thing that answered a press was half again the
     size of the thing you could see.  Above it, what answers a press is
     exactly the box; and the box gets the whole width, which the longest of
     the sizes needs and at 148px never had. */
  .sheet-menu .pick { margin-top: 12px; font-size: 13px; }
  .sheet-menu .pick > label {
    display: block; margin-bottom: 4px; font-size: 11.5px; color: var(--muted);
  }
  .sheet-menu .pick select { display: block; width: 100%; }
  .sheet-menu .hint:empty { display: none; }
  .sheet-menu .hint { margin-top: 10px; }
  #save-menu { width: 262px; }
  /* ---------------------------------------------------------- palette -- */
  .presets { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .preset {
    border: 1px solid var(--line); border-radius: 8px; background: var(--panel);
    padding: 7px 6px 6px; cursor: pointer; text-align: center;
  }
  .preset:hover { border-color: var(--accent); }
  .preset.on { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
  .preset .chips { display: flex; gap: 3px; justify-content: center; margin-bottom: 5px; }
  .preset .chip { width: 12px; height: 12px; border-radius: 3px; border: 1px solid rgba(0,0,0,.18); }
  .preset span { font-size: 11.5px; color: var(--muted); }

  /* ------------------------------------------------------- color rows -- */
  .row {
    display: flex; align-items: center; gap: 8px; padding: 5px 0;
  }
  .row + .row { border-top: 1px solid var(--line-soft); }
  .row .name { flex: 1; font-size: 13px; }
  .row .count { color: var(--muted); font-size: 11.5px; }
  .row.pick { cursor: pointer; border-radius: 6px; }
  .row.pick:hover { background: var(--line-soft); }
  .swatch {
    width: 26px; height: 26px; padding: 0; border-radius: 7px; cursor: pointer;
    border: 1px solid var(--line); background: var(--panel); overflow: hidden;
  }
  .swatch::-webkit-color-swatch-wrapper { padding: 2px; }
  .swatch::-webkit-color-swatch { border: none; border-radius: 5px; }
  .swatch::-moz-color-swatch { border: none; border-radius: 5px; }
  .legendkey { width: 22px; height: 16px; flex: none; }
  .legendkey svg { display: block; overflow: visible; }

  #sel-card .none { color: var(--muted); font-size: 12.5px; }
  #sel-card .what { font-weight: 600; margin-bottom: 2px; }
  #sel-card .said {
    color: var(--muted); font-size: 12.5px; margin-bottom: 10px;
    overflow-wrap: anywhere;
  }
  .switch { display: flex; align-items: center; gap: 8px; font-size: 13px; }
  .switch input { width: 15px; height: 15px; accent-color: var(--accent); }

  /* ----------------------------------------------------------- source -- */
  /* Where the pseudocode is written.  It was a plain grey box, which is a
     dull thing to look at for as long as this one gets looked at.  It keeps
     to greys -- the code in it is the only thing with any colour to it -- but
     it is given the things that make somewhere feel like somewhere to write:
     a little depth, room to breathe, a ruled edge down the left the way an
     editor has, and a clear ring when it is the thing being typed into. */
  /* The ruling has to be the same height as a line of the type sitting on
     it, and has to start where the type starts.  It was neither: the lines
     were 20.8 apart against type set on 20, and they began at the very top
     of the box while the words began ten pixels down -- so the first line
     looked nearly right and every line after it drifted further off.
     Everything here is in whole pixels for that reason. */
  /* It can be pulled taller or shorter, but only between a floor and a
     ceiling: a box of two lines is no use to anybody, and one that can grow
     without end leaves the rest of the panel somewhere below the bottom of
     the screen.  Both ends are whole numbers of lines -- 10 of padding, then
     twenty to a line -- so it never stops halfway through one.  Past the
     ceiling there is the button beside the heading, which gives the whole
     screen over to it.

     There are no numbers down the side of this one.  A gutter is worth its
     room in the expanded box, where a long program is actually read; in a
     panel this narrow it takes width the words need, and it only works if
     lines are stopped from wrapping, which costs more again. */
  #code-home {
    position: relative; display: flex; resize: vertical; overflow: hidden;
    border-radius: 8px;
    height: 200px;                      /* nine lines to begin with */
    min-height: 120px;                  /* five: enough to see where you are */
    max-height: 520px;                  /* twenty-five, and then no further */
  }
  #source textarea {
    display: block; flex: 1; width: 100%; height: 100%; resize: none;
    min-width: 0;
    border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px;
    font-family: "Cascadia Mono", Consolas, "SF Mono", Menlo, monospace;
    font-size: 12.5px; line-height: 20px; color: var(--ink);
    white-space: pre-wrap; overflow-wrap: anywhere;
    background:
      linear-gradient(var(--code-line) 1px, transparent 1px) 0 10px / 100% 20px,
      var(--code-bg);
    background-attachment: local, local;
    box-shadow: inset 0 1px 2px var(--code-well);
    transition: border-color .14s, box-shadow .14s;
    tab-size: 4;
  }
  /* The line the program is on while it is being followed.  A band laid over
     the ruling rather than a selection, because selecting means focusing,
     and focus during a run belongs to whatever the program is asking to be
     typed.  Where it goes and how tall it is are measured by the script and
     handed down: a line too long for the column wraps, and the mark has to
     sit where the wrapped words actually are and cover as many rows as they
     take.  It is laid on the same local attachment as the ruling, so it
     scrolls with the words rather than sitting still while they move. */
  #source textarea.at {
    background:
      linear-gradient(var(--code-at), var(--code-at))
        0 var(--at-top, 10px) / 100% var(--at-tall, 20px) no-repeat,
      linear-gradient(var(--code-line) 1px, transparent 1px) 0 10px / 100% 20px,
      var(--code-bg);
    background-attachment: local, local, local;
  }
  #source textarea::placeholder { color: var(--muted); }
  #source textarea:focus {
    outline: 0; border-color: var(--accent);
    box-shadow: inset 0 1px 2px var(--code-well), 0 0 0 3px var(--accent-soft);
  }
  #code-slot #code { border-radius: 10px; }
  #source .fields {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px;
  }
  #source .fields > div { min-width: 0; }   /* a long word cannot widen a column */
  #source input[type="text"], #source select, .field {
    width: 100%; border: 1px solid var(--line); border-radius: 8px; padding: 7px 9px;
    background: var(--field); color: var(--ink);
  }
  /* The label over a field and the label beside a switch are different
     things.  This one is for the field labels; saying so keeps it from
     taking the switches with it, which is what made Grid and Key come out
     small and grey while Step slowly, sitting outside #source, did not. */
  #source label:not(.switch) {
    display: block; font-size: 11.5px; color: var(--muted); margin-bottom: 3px;
  }
  /* Two of a kind, side by side, on the same two columns as the fields
     above them -- so everything down the panel lines up on one pair of
     edges instead of each row finding its own. */
  .switches {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px;
    align-items: center;
  }
  #source .go {
    margin-top: 12px; display: flex; gap: 10px; align-items: center;
    justify-content: space-between;
  }
  #source .go .btn { flex: none; }
  /* two buttons of equal weight, filling the width between them */
  .pair-wide {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px;
  }
  .pair-wide .btn { justify-content: center; }
  .switches .field { width: 100%; }
  /* Two switches in the cell one would take, for a pair where the
     second only means anything while the first is on. */
  .switches .stack { display: grid; gap: 7px; }
  .switch.off { opacity: .5; }
  .switch.off input { cursor: default; }
  #source .build-row { margin-top: 12px; }
  #hand-switches:empty { display: none; }
  #hand-switches .switches { margin-top: 0; margin-bottom: 4px; }
  .btn.wide { width: 100%; justify-content: center; }
  /* what the button is doing, said in colour */
  .btn.primary.working {
    background: var(--busy); border-color: var(--busy); color: #fff;
  }
  .btn.primary.done {
    background: var(--good); border-color: var(--good); color: #fff;
  }
  .btn.primary.working, .btn.primary.done { transition: background .2s, border-color .2s; }
  .btn.primary[disabled] { opacity: 1; cursor: progress; }
  #build-note { font-size: 12.5px; color: var(--muted); text-align: center;
                margin-top: 8px; min-height: 1em; overflow: hidden;
                text-overflow: ellipsis; white-space: nowrap; }
  #build-note.bad { color: var(--bad); }

  /* ---------------------------------------------------------- by hand -- */
  .tabs { display: flex; gap: 6px; }
  .tab {
    flex: 1; border: 1px solid var(--line); background: var(--panel);
    border-radius: 8px; padding: 7px 8px; cursor: pointer; font-size: 13px;
  }
  .tab.on { background: var(--accent); border-color: var(--accent); color: #fff; }
  .adders { display: grid; grid-template-columns: repeat(6, 1fr); gap: 5px; }
  .adders .btn {
    padding: 5px 2px; justify-content: center; border-radius: 7px;
  }
  .adders .legendkey { width: 24px; height: 17px; }
  textarea.field { resize: vertical; }
  .trio { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px;
          margin-top: 10px; }
  .trio label { display: flex; flex-direction: column; gap: 3px;
                font-size: 11.5px; color: var(--muted); }
  .trio input[type="number"] { width: 100%; padding: 5px 7px; }
  .trio .swatch { width: 100%; height: 28px; }
  .small-head { font-size: 11.5px; color: var(--muted); margin-top: 12px; }
  .tape {
    margin-top: 10px; max-height: 260px; overflow: auto; border-radius: 8px;
    border: 1px solid var(--line); background: var(--field); padding: 8px 10px;
    font-family: Consolas, "Courier New", monospace; font-size: 12.5px;
    line-height: 1.5; display: none;
  }
  .tape:not(:empty) { display: block; }
  .tape .said { white-space: pre-wrap; overflow-wrap: anywhere; }
  .tape .said.note { color: var(--muted); }
  .tape .said.good { color: var(--good); }
  .tape .said.bad { color: var(--bad); }
  .tape .said.typed { color: var(--accent); }
  .tape .asking { display: flex; gap: 6px; margin: 4px 0; }
  .tape .asking .field { flex: 1; padding: 4px 7px; font-family: inherit; }
  .tape .code { margin: 0; white-space: pre; overflow-x: auto; }
  svg .node.now > :is(rect, ellipse, polygon, path) { stroke-width: 3; }
  svg .node.now { filter: drop-shadow(0 0 8px rgba(17, 97, 73, .65)); }
  /* Above the sheets that fill the screen, not under them: the language
     list is opened from the bar of one of those, and a menu that opened
     behind the thing it was asked from would be a menu nobody could see. */
  .menu {
    position: fixed; z-index: 70; min-width: 176px; padding: 5px;
    background: var(--panel); border: 1px solid var(--line);
    border-radius: 10px; box-shadow: var(--shadow);
  }
  .menu button {
    display: flex; align-items: center; gap: 9px; width: 100%;
    border: 0; background: none; color: inherit; text-align: left;
    padding: 7px 9px; border-radius: 7px; cursor: pointer; font-size: 13px;
  }
  .menu button:hover { background: var(--accent-soft); }
  .menu hr { border: 0; border-top: 1px solid var(--line-soft); margin: 4px 2px; }
  svg .link { cursor: pointer; }
  svg .link.on .flow { stroke-width: 3; }
  svg .link.on { filter: drop-shadow(0 0 6px rgba(20, 66, 124, .6)); }
  svg .knob { cursor: crosshair; }
  svg .knob:hover { r: 7; }
  /* the dot a line is coming from, while it is being aimed */
  svg .knob.lit { fill: var(--accent); }
  /* and the dots on every other shape, waiting to be picked */
  svg .spot {
    cursor: pointer; fill: var(--accent); fill-opacity: .18;
    stroke: var(--accent); stroke-width: 1.6;
    animation: breathe 1.5s ease-in-out infinite;
  }
  svg .spot:hover { fill-opacity: .9; r: 8; animation: none; }
  @keyframes breathe {
    0%, 100% { fill-opacity: .18; }
    50% { fill-opacity: .55; }
  }
  @media (prefers-reduced-motion: reduce) {
    svg .spot { animation: none; fill-opacity: .4; }
  }
  svg .grip { cursor: nwse-resize; }
  /* the line that says what you have lined a shape up with */
  svg .guide {
    stroke: #e01020; stroke-width: 1.4; stroke-dasharray: 7 4;
    pointer-events: none; shape-rendering: crispEdges;
  }
  svg .ghost { fill: none !important; stroke: none !important; }
  /* writing straight into a shape */
  .writing {
    width: 100%; height: 100%; display: flex; align-items: center;
    justify-content: center; text-align: center; outline: 0;
    font: 12.5px/1.2 Arial, Helvetica, sans-serif; overflow: hidden;
    caret-color: var(--accent); word-break: break-word;
  }
  svg .typing-here { overflow: visible; }
  svg .node[data-kind="text"]:hover .ghost {
    stroke: var(--line) !important; stroke-dasharray: 4 3;
  }
  svg .node[data-kind="text"].on .ghost {
    stroke: var(--accent) !important; stroke-dasharray: 4 3;
  }
  svg .node { cursor: move; }
  svg .band { pointer-events: none; }
  svg .band-line { stroke: var(--accent); stroke-width: 2; stroke-linecap: round; }
  svg .band-tip { fill: var(--accent); stroke: var(--accent); stroke-width: .6;
                  stroke-linejoin: miter; }
  #stage.joining { cursor: crosshair; }
  .edit-box {
    position: absolute; z-index: 20; border: 2px solid var(--accent);
    border-radius: 6px; padding: 4px 6px; font: inherit; font-size: 12px;
    text-align: center; resize: none; background: #fff; color: #10151b;
    box-shadow: var(--shadow);
  }
  .good { color: var(--good); font-size: 12.5px; margin: 10px 0 0; }
  .hint.bad { color: var(--bad); }
  .fault {
    display: block; width: 100%; text-align: left; margin-top: 6px;
    border: 1px solid var(--line); border-left: 3px solid var(--bad);
    background: var(--panel); color: inherit; border-radius: 7px;
    padding: 6px 9px; font-size: 12.5px; cursor: pointer; line-height: 1.35;
  }
  .fault:hover { background: var(--line-soft); }

  /* ------------------------------------------------------------ stage -- */
  #stage {
    flex: 1; overflow: auto; padding: 26px; min-width: 0;
    background-image: radial-gradient(circle at 1px 1px, var(--dots) 1px, transparent 0);
    background-size: 22px 22px;
  }
  #stage.grabbing { cursor: grabbing; user-select: none; }
  .wrap { display: flex; justify-content: center; min-width: min-content; }
  .sheet {
    background: #fff; border-radius: 12px; box-shadow: var(--shadow);
    /* the paper stays paper-coloured: the chart is its own thing */
    line-height: 0; display: inline-block; overflow: hidden;
  }
  svg { display: block; height: auto; }
  svg .node { cursor: pointer; }
  svg .node.on > :is(rect, ellipse, polygon) { stroke-width: 2.6; }
  svg .node.on { filter: drop-shadow(0 0 7px rgba(20, 66, 124, .55)); }

  /* --------------------------------------------------------- foot bar -- */
  footer.bar { border-bottom: 0; border-top: 1px solid var(--line); }
  /* One gap the whole way along the row, and one height for everything
     standing in it: the two padlocks, the two zoom steps, the reading
     between them, and the two named buttons.  It used to be spaced into
     little groups -- a wider gap before Fit, a switch two pixels taller
     than the buttons beside it -- and what that read as was not grouping
     but a row nobody had lined up. */
  footer.bar { --foot-h: 28px; gap: 10px; }
  footer.bar .btn.small, footer.bar #hold-seg { height: var(--foot-h); }
  footer.bar .btn.small { padding: 0 11px; }
  /* The two steps are one glyph apiece, so they are square, and the same
     width as each other whatever the font makes of a plus and a minus. */
  footer.bar #out, footer.bar #in {
    width: var(--foot-h); padding: 0; justify-content: center; font-size: 15px;
  }
  /* The reading holds its width as it counts up and down, so nothing on
     either side of it shuffles along when 100% becomes 77%. */
  .zoom { min-width: 52px; text-align: center; color: var(--muted);
          font-variant-numeric: tabular-nums; }
  #note { color: var(--muted); font-size: 12.5px; }
  #note.bad { color: var(--bad); }

  /* ------------------------------------ held in place, or loose upon it -- */
  /* Locked is what the chart has always been: it sits in the middle of the
     stage and scrolls about inside it, and there is nowhere it can go that
     the stage is not.  That is right for reading one.  It is wrong for
     working on one -- shoved aside to read what is under it, or carried off
     past the edge to leave room in front of it -- so it comes off its
     leash here. */
  #hold-seg { flex: none; gap: 2px; }
  #hold-seg .seg-btn {
    flex: none; display: inline-flex; align-items: center; gap: 6px;
    padding: 0 9px; font-size: 12.5px;
  }
  #hold-seg .seg-btn svg {
    width: 13px; height: 13px; fill: none; stroke: currentColor;
    stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round;
  }
  /* Loose, the chart is carried by a translation rather than by scrolling,
     so the stage does none: its own bars would have nothing left to say,
     and the browser's would fight the dragging for the same pixels. */
  body.chart-loose #stage { overflow: hidden; touch-action: none; cursor: grab; }
  body.chart-loose #stage.grabbing { cursor: grabbing; }
  body.chart-loose .slider,
  body.chart-loose .stage-frame::after { display: none; }
  body.chart-loose .wrap {
    transform: translate(var(--hold-x, 0px), var(--hold-y, 0px));
    will-change: transform;
  }

  /* How this fits a screen of any size lives in 06-screens.css.  What was
     here spoke of buttons that no longer exist -- a row of saves, a paired
     select -- and pushed the stage aside with a padding the stage no longer
     answers to, having since been wrapped in a frame of its own. */
  @media print {
    .bar, #panel { display: none !important; }
    body, main, #stage { display: block; overflow: visible; background: #fff; }
    #stage { padding: 0; background-image: none; }
    .sheet { box-shadow: none; border-radius: 0; }
  }
  /* ------------------------------------------------- slider bars of ours -- */
  /* The stage keeps its own scrolling but hides the browser's bars, and the
     two below are drawn over the edges of it instead. */
  #stage.own-sliders { scrollbar-width: none; }
  #stage.own-sliders::-webkit-scrollbar { width: 0; height: 0; }
  .stage-frame { position: relative; flex: 1; display: flex; min-width: 0; }
  .stage-frame > #stage { flex: 1; }
  .slider {
    position: absolute; z-index: 6; display: flex; background: var(--line-soft);
  }
  .slider.x { left: 0; right: 15px; bottom: 0; height: 15px;
              border-top: 1px solid var(--line); }
  .slider.y { top: 0; bottom: 15px; right: 0; width: 15px;
              flex-direction: column; border-left: 1px solid var(--line); }
  .slider.none { display: none; }
  .slider-track { position: relative; flex: 1; min-width: 0; min-height: 0; }
  .slider-grip {
    position: absolute; border-radius: 99px; background: var(--line);
    transition: background .12s;
  }
  .slider.x .slider-grip { top: 3px; bottom: 3px; left: 0; }
  .slider.y .slider-grip { left: 3px; right: 3px; top: 0; }
  .slider-track:hover .slider-grip { background: var(--muted); }
  body.sliding .slider-grip { background: var(--accent); }
  body.sliding { user-select: none; }

  /* the little buttons at each end */
  .slider-step {
    flex: none; display: flex; align-items: center; justify-content: center;
    width: 15px; height: 15px; padding: 0; border: 0; cursor: pointer;
    background: none; color: var(--muted);
  }
  .slider-step:hover { background: var(--line); color: var(--ink); }
  .slider-step:active { background: var(--accent-soft); color: var(--accent); }
  .slider-step svg {
    width: 9px; height: 9px; fill: none; stroke: currentColor;
    stroke-width: 1.7; stroke-linecap: round; stroke-linejoin: round;
  }
  .slider.x .slider-step.less svg { transform: rotate(180deg); }
  .slider.y .slider-step.less svg { transform: rotate(-90deg); }
  .slider.y .slider-step.more svg { transform: rotate(90deg); }
  /* the small square where the two bars meet */
  .stage-frame::after {
    content: ""; position: absolute; right: 0; bottom: 0; width: 15px;
    height: 15px; background: var(--line-soft);
    border-left: 1px solid var(--line); border-top: 1px solid var(--line);
  }

  /* ------------------------------------- the pseudocode, filling the screen -- */
  /* Filling the screen does not mean filling the width: a line of pseudocode
     dragged across a wide monitor is worse to read than one in the panel, so
     the sheet stops at a comfortable measure and sits in the middle, with the
     page dimmed behind it.  Everything inside is set to one line height, so
     the numbers down the side line up with the words beside them. */
  #code-over {
    position: fixed; inset: 0; z-index: 60; display: flex;
    align-items: center; justify-content: center; padding: 26px;
    background: var(--dim);
    backdrop-filter: blur(3px);
  }
  #code-over[hidden] { display: none !important; }
  .code-sheet {
    display: flex; flex-direction: column; min-height: 0;
    width: min(1040px, 100%); height: 100%;
    background: var(--panel); border: 1px solid var(--line);
    border-radius: 16px; box-shadow: 0 24px 64px rgba(16, 24, 40, .28);
    overflow: hidden;
  }
  .code-bar {
    flex: none; display: flex; align-items: center; gap: 12px;
    padding: 12px 16px; border-bottom: 1px solid var(--line);
    background: var(--panel); flex-wrap: wrap;
  }
  .code-bar .btn { flex: none; }
  .code-bar strong { font-size: 14px; }
  .mark.small { width: 26px; height: 26px; border-radius: 8px; }
  .mark.small svg { width: 16px; height: 16px; }
  .code-count {
    margin-left: auto; font-size: 12.5px; color: var(--muted);
    font-variant-numeric: tabular-nums;
  }
  .code-esc {
    font-size: 12px; color: var(--muted); padding: 3px 8px;
    border: 1px solid var(--line); border-radius: 7px; white-space: nowrap;
  }

  #code-slot {
    flex: 1; display: flex; min-height: 0; gap: 0;
    padding: 14px 16px 16px; background: var(--code-bg);
    border-top: 1px solid var(--line-soft);
  }
  /* the numbers down the side */
  .code-rule {
    flex: none; margin: 0; padding: 10px 10px 10px 0; overflow: hidden;
    height: 100%; box-sizing: border-box;
    font: 14px/24px "Cascadia Mono", Consolas, "SF Mono", Menlo, monospace;
    color: var(--muted); opacity: .6; text-align: right; min-width: 34px;
    border-right: 1px solid var(--line-soft); user-select: none;
    font-variant-numeric: tabular-nums;
  }
  #code-slot #code {
    flex: 1; height: auto; min-height: 0; resize: none;
    border: 0; border-radius: 0; box-shadow: none;
    padding: 10px 4px 10px 14px;
    font-size: 14px; line-height: 24px;
    white-space: pre; overflow-wrap: normal; overflow-x: auto;
    background:
      linear-gradient(var(--code-line) 1px, transparent 1px) 0 10px / 100% 24px,
      transparent;
    background-attachment: local;
  }
  #code-slot #code:focus { box-shadow: none; border: 0; outline: 0; }

  /* ----------------------------------- the run and the code, filling the screen -- */
  /* The same trick again, and for the same reason.  What a program prints,
     what it stops to be told, and the same program written out in Java are
     all put in the tape at the foot of the panel -- a box three hundred
     pixels wide and a few lines tall, which is no place to read a program
     in or hold a conversation with one.  So the tape can be thrown up over
     the whole page: the very same box is moved into the sheet and moved
     back again, so there is only ever one of it and whatever is writing
     into it carries on writing into the one there is. */
  #tape-over {
    position: fixed; inset: 0; z-index: 60; display: flex;
    align-items: center; justify-content: center; padding: 26px;
    background: var(--dim);
    backdrop-filter: blur(3px);
  }
  #tape-over[hidden] { display: none !important; }
  #tape-slot {
    flex: 1; display: flex; min-height: 0;
    padding: 14px 16px 16px; background: var(--code-bg);
    border-top: 1px solid var(--line-soft);
  }
  /* In the panel the tape is a small box with a border of its own that
     grows to a point and then scrolls, and which is not there at all until
     something is put in it.  Up here it is the sheet: no border, all the
     room there is, and shown even while it is empty -- a screen with a bar
     and nothing under it looks broken. */
  #tape-slot .tape {
    display: block; flex: 1; margin: 0; padding: 0 4px; max-height: none;
    border: 0; border-radius: 0; background: none; overflow: auto;
    font-size: 13.5px; line-height: 1.65;
  }
  #tape-slot .tape .asking { max-width: 560px; margin: 8px 0; }
  /* the line that says what the screen is for, when nothing has been
     put on it yet: a sentence, so it is set to a width a sentence is
     read at rather than dragged across the whole sheet */
  #tape-slot .tape .hint-line { max-width: 68ch; margin-bottom: 6px; }
  /* --------------------------------------------- the run, and the code --
     Two things live in this sheet and only one of them is on at a time: the
     tape, which is the run, and the code the program was written out as.
     They are kept apart rather than one being written over the other,
     because the run is the thing you went to the code to understand -- what
     it printed, what you typed into it, where it stopped.  Writing the code
     over the top of that threw it away, and the only way back to it was to
     run the whole thing again and type the same answers in.  So the code is
     given a box of its own, the tape is left alone, and the bar carries a
     way back between them. */
  #code-out {
    flex: 1; display: flex; flex-direction: column; min-height: 0;
    padding: 14px 16px 16px; overflow: auto;
    background: var(--code-bg); border-top: 1px solid var(--line-soft);
  }
  #tape-slot[hidden], #code-out[hidden] { display: none !important; }
  #code-out .code {
    margin: 0; white-space: pre; font-size: 13.5px; line-height: 1.65;
  }
  /* the way back sits beside the name of what you are looking at, which is
     where you look when you want to stop looking at it */
  .code-bar .btn.back { margin-left: 2px; }
  .btn.back .short { display: none; }
  .icon.small {
    width: 24px; height: 24px; border-radius: 7px; margin-left: auto;
  }
  .icon.small svg { width: 14px; height: 14px; }
  /* a colour on a menu row, shown as it is now */
  .menu .dot {
    flex: none; width: 15px; height: 15px; border-radius: 4px;
    border: 1px solid var(--line); box-shadow: inset 0 0 0 1px rgba(255,255,255,.35);
  }
  /* the paper, while a shape is being carried onto it */
  #stage.taking { outline: 2px dashed var(--accent); outline-offset: -6px; }
  #adders .btn { cursor: grab; }
  #adders .btn:active { cursor: grabbing; }
  /* A finger dragging a shape should move the shape, not scroll the page;
     the stage still scrolls normally where there is no shape under it. */
  #chart, #chart * { touch-action: none; }
  #chart { -webkit-user-select: none; user-select: none; }

  /* The veil only ever exists on a narrow screen.  Said plainly here so that
     on a wide one it is not a stray box sitting in the row with the panel
     and the stage, quietly taking part in the layout. */
  .veil { display: none; }

  /* ----------------------------------------------- not as wide as it likes -- */
  /* Under this, the panel stops taking a share of the width and lies over the
     chart instead, with the chart full width underneath it.  Taking a third
     of a narrow screen for the panel leaves the chart a column too thin to
     read, and the panel is not wanted all the time -- the chart is. */
  @media (max-width: 899px) {
    main { position: relative; }
    #panel {
      position: absolute; top: 0; bottom: 0; left: 0; z-index: 12;
      width: min(320px, 86vw); box-shadow: var(--shadow);
      border-right: 1px solid var(--line);
    }
    body[data-side="right"] #panel {
      left: auto; right: 0; border-right: 0; border-left: 1px solid var(--line);
    }
    #rail { position: absolute; top: 0; bottom: 0; left: 0; z-index: 11; }
    body[data-side="right"] #rail { left: auto; right: 0; }
    /* the rail lies over the stage, so the chart is kept clear of it */
    body.railed #stage { padding-left: 64px; }
    body.railed[data-side="right"] #stage { padding-left: 10px; padding-right: 64px; }

    /* something to tap to put it away again */
    .veil {
      display: block; position: absolute; inset: 0; z-index: 11;
      background: var(--dim); opacity: 0; pointer-events: none;
      transition: opacity .16s;
    }
    body.drawer .veil { opacity: 1; pointer-events: auto; }
    /* The bars have to stay above the drawer.  The drawer lies over the
       chart, which is the whole point of it at this width -- but it was
       never meant to lie over the bar that opens it, and it did: the bar
       itself cleared the top of the drawer by a pixel or two and looked
       fine, while the sheets that hang off it came down inside it and were
       covered, so Download opened onto nothing you could see. */
    .bar { z-index: 14; }
    .brand small { display: none; }
  }

  /* ------------------------------------------------------- narrow enough -- */
  /* A phone held upright.  The panel takes the screen while it is open,
     because there is no room to show it beside anything, and the bar loses
     what it can spare. */
  @media (max-width: 599px) {
    #panel { width: min(400px, 100vw); }
    .bar { padding: 8px 10px; gap: 8px 10px; }
    .brand { font-size: 14px; }
    .mark { width: 28px; height: 28px; border-radius: 8px; }
    .mark svg { width: 17px; height: 17px; }
    #stage { padding: 10px; }
    .sheet-menu { right: 8px; left: 8px; width: auto; }
    #save-menu { width: auto; }
    footer.bar { justify-content: center; }
    footer.bar .grow { display: none; }
    /* the two padlocks say which it is on their own; there is no room in
       the foot bar for the words as well */
    #hold-seg .seg-btn span { display: none; }
    #hold-seg .seg-btn { padding: 0 10px; }
    /* There is no Esc to press on a phone, and the bar wants the width for
       what the screen is and what can be done to it.  The little mark is
       decoration; the runner's bar carries four things besides it and was
       breaking onto a second row to fit them. */
    .code-esc, .code-bar .mark { display: none; }
    #tape-done { margin-left: auto; }
    /* the bar has five things in it on this screen and room for four, so
       the count goes and the way back says it in one word */
    .code-bar .code-count { display: none; }
    .btn.back .full { display: none; }
    .btn.back .short { display: inline; }
    #tape-over { padding: 0; }
    #tape-over .code-sheet { border: 0; border-radius: 0; }
  }

  /* --------------------------------------------------------- not as tall -- */
  /* A phone on its side, or a short window.  Height is what is scarce, so
     everything that is not the chart gives some back. */
  @media (max-height: 560px) {
    .bar { padding: 6px 12px; }
    .brand { line-height: 1.15; }
    .brand small { display: none; }
    #stage { padding: 8px; }
    footer.bar { padding: 5px 12px; --foot-h: 24px; }
    .btn.small { padding: 3px 8px; }
    section.card { padding: 10px 14px; }
    #code-home { height: 120px; min-height: 90px; }
    #code-over, #tape-over { padding: 10px; }
    .code-bar { padding: 8px 12px; }
  }

  /* -------------------------------------------------- prodded, not pointed -- */
  /* A finger is a blunter instrument than a mouse: everything it has to hit
     is given the room to be hit, and the things that only exist to answer a
     hover are put away. */
  @media (pointer: coarse) {
    .btn { padding: 9px 14px; }
    .btn.small { padding: 7px 11px; }
    .icon { width: 40px; height: 40px; }
    #rail { width: 56px; }
    #rail .icon { width: 44px; height: 44px; }
    body.railed #stage { padding-left: 72px; }
    body.railed[data-side="right"] #stage { padding-right: 72px; }
    .seg-btn { padding: 9px 10px; }
    .menu button { padding: 10px 11px; }
    .slider { display: none; }              /* a finger scrolls by dragging */
    #stage.own-sliders { scrollbar-width: auto; }
    .stage-frame::after { display: none; }
    svg .knob { r: 8; }
    svg .spot { r: 9; }
    svg .grip { rx: 3; }
    .adders .btn { padding: 8px; }
  }

  /* ------------------------------------------------------- room to breathe -- */
  /* On a big screen the chart is given the middle and the panel keeps its
     own width rather than stretching across half a desk. */
  @media (min-width: 1500px) {
    #panel { width: 360px; }
    #stage { padding: 32px; }
  }

  /* --------------------------------------------- phones with a notch in them -- */
  /* The bars keep clear of whatever the screen has taken out of itself. */
  @supports (padding: max(0px)) {
    .bar { padding-left: max(16px, env(safe-area-inset-left));
           padding-right: max(16px, env(safe-area-inset-right)); }
    footer.bar { padding-bottom: max(10px, env(safe-area-inset-bottom)); }
    #rail { padding-left: env(safe-area-inset-left); }
  }
  /* Nothing here changes what anything is, or where it ends up.  It is only
     about the getting there: a thing that moves on its way in is easier to
     follow than one that simply appears, and a thing that answers the moment
     it is touched feels made rather than assembled.

     Two rules run through all of it.  Everything is short -- nothing has to
     wait on an animation before it can be used -- and everything stops when
     the computer has been asked to keep still, which is at the foot of this
     file. */

  /* ------------------------------------------------- how fast, and how -- */
  /* One set of speeds and curves for the whole page, so that two things
     moving at once look like one thing moving.  The curve starts quickly and
     settles, the way something with weight does; the "back" one overshoots by
     a hair, which is what makes a thing look eager rather than dragged. */
  :root {
    --ease: cubic-bezier(.22, 1, .36, 1);
    --ease-soft: cubic-bezier(.4, 0, .2, 1);
    --ease-back: cubic-bezier(.34, 1.36, .64, 1);
    --tap: .11s;                        /* answering a press */
    --quick: .17s;                      /* a colour, a shadow */
    --move: .26s;                       /* something going somewhere */
    --sheet-t: .32s;                    /* a whole panel arriving */
    --lift: 0 2px 10px rgba(16, 24, 40, .10);
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) { --lift: 0 2px 10px rgba(0, 0, 0, .44); }
  }
  :root[data-theme="dark"] { --lift: 0 2px 10px rgba(0, 0, 0, .44); }

  /* ---------------------------------------------------------- arriving -- */
  /* The page puts itself together in about half a second: the bars in from
     their own edges, the panel from its side, the paper up from below.  Each
     one holds its starting look until its turn comes and holds nothing
     afterwards, so ordinary styling takes over the moment a thing has landed
     -- which is what lets the panel still fold away later. */
  header.bar { animation: bar-down .45s var(--ease) backwards; }
  footer.bar { animation: bar-up .45s var(--ease) .05s backwards; }
  #panel { animation: panel-in .5s var(--ease) .06s backwards; }
  #stage { animation: fade-in .5s var(--ease-soft) .04s backwards; }
  .sheet { animation: paper-in .55s var(--ease) .12s backwards; }
  body[data-side="right"] #panel { animation-name: panel-in-right; }
  @keyframes bar-down { from { opacity: 0; transform: translateY(-10px); } }
  @keyframes bar-up { from { opacity: 0; transform: translateY(10px); } }
  @keyframes panel-in { from { opacity: 0; transform: translateX(-14px); } }
  @keyframes panel-in-right { from { opacity: 0; transform: translateX(14px); } }
  @keyframes fade-in { from { opacity: 0; } }
  @keyframes paper-in { from { opacity: 0; transform: translateY(12px) scale(.985); } }

  /* The mark draws itself, once, the way it would be drawn by hand.  The
     dashes exist only while it is being drawn -- afterwards the strokes are
     plain strokes again, which is why the run is told to hold nothing. */
  header .mark svg > * { animation: mark-draw .9s var(--ease-soft) .1s backwards; }
  header .mark svg > *:nth-child(2) { animation-delay: .22s; }
  header .mark svg > *:nth-child(3) { animation-delay: .3s; }
  header .mark svg > *:nth-child(4) { animation-delay: .42s; }
  @keyframes mark-draw {
    from { stroke-dasharray: 48; stroke-dashoffset: 48; opacity: .25; }
    to { stroke-dasharray: 48; stroke-dashoffset: 0; opacity: 1; }
  }
  .mark { transition: transform var(--move) var(--ease-back),
                      background-color var(--quick) var(--ease-soft); }
  .mark:hover { transform: rotate(-3deg) scale(1.05); }

  /* ------------------------------------------------------------- press -- */
  /* A button rises a hair under the mouse and sinks under the press.  The
     sinking is faster than the rising, on purpose: going down should feel
     like the button answering, coming back up like it settling. */
  .btn {
    transition: background-color var(--quick) var(--ease-soft),
                border-color var(--quick) var(--ease-soft),
                color var(--quick) var(--ease-soft),
                box-shadow var(--quick) var(--ease-soft),
                filter var(--quick) var(--ease-soft),
                transform var(--tap) var(--ease-soft);
  }
  .btn:hover { transform: translateY(-1px); box-shadow: var(--lift); }
  .btn:active { transform: translateY(0) scale(.975); transition-duration: .05s; }
  .btn[disabled], .btn[disabled]:hover { transform: none; box-shadow: none; }
  /* the blue ones catch a little light as the mouse crosses them */
  .btn.primary { position: relative; overflow: hidden; }
  .btn.primary::after {
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(112deg, transparent 32%,
                rgba(255, 255, 255, .26) 50%, transparent 68%);
    transform: translateX(-130%);
    transition: transform .65s var(--ease);
  }
  .btn.primary:hover::after { transform: translateX(130%); }
  .btn.primary:hover { box-shadow: 0 3px 14px rgba(20, 66, 124, .3); }

  .icon {
    transition: background-color var(--quick) var(--ease-soft),
                color var(--quick) var(--ease-soft),
                transform var(--tap) var(--ease-soft);
  }
  .icon:hover { transform: translateY(-1px); }
  .icon:active { transform: scale(.9); transition-duration: .05s; }
  .icon svg { transition: transform var(--move) var(--ease); }
  #collapse:hover svg { transform: translateX(-3px); }
  body[data-side="right"] #collapse:hover svg { transform: scaleX(-1) translateX(-3px); }
  .switch input { transition: transform var(--tap) var(--ease-back); }
  .switch input:active { transform: scale(.88); }

  /* Where the keyboard is, said the same way everywhere.  A ring rather than
     a line, so it reads as the page pointing at something rather than as a
     border that was there all along. */
  .btn:focus-visible, .icon:focus-visible, .seg-btn:focus-visible,
  .tab:focus-visible, .preset:focus-visible, .fault:focus-visible,
  .menu button:focus-visible, .slider-step:focus-visible {
    outline: 0;
    box-shadow: 0 0 0 3px var(--accent-soft), 0 0 0 1px var(--accent);
  }
  input[type="text"], select, textarea, .field {
    transition: border-color var(--quick) var(--ease-soft),
                box-shadow var(--quick) var(--ease-soft),
                background-color var(--quick) var(--ease-soft);
  }
  #source input[type="text"]:focus, #source select:focus,
  .field:focus, textarea.field:focus {
    outline: 0; border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-soft);
  }

  /* --------------------------------------------- the two-and-three-way -- */
  /* The pale block behind the chosen side used to be painted onto whichever
     button was on, so it jumped from one to the other.  It is one block now,
     sitting behind them all, and it slides.  The script only says which of
     how many is on; the arithmetic is here. */
  .seg { position: relative; }
  .seg::before {
    content: ""; position: absolute; z-index: 0;
    top: 2px; bottom: 2px; left: 2px;
    width: calc((100% - 4px - (var(--seg-n, 2) - 1) * 2px) / var(--seg-n, 2));
    border-radius: 7px; background: var(--panel);
    box-shadow: 0 1px 2px rgba(16, 24, 40, .12);
    transform: translateX(calc(var(--seg-i, 0) * (100% + 2px)));
    transition: transform var(--move) var(--ease-back),
                opacity var(--quick) var(--ease-soft);
  }
  .seg[data-seg-off]::before { opacity: 0; }
  .seg-btn { position: relative; z-index: 1;
             transition: color var(--quick) var(--ease-soft); }
  .seg-btn.on { background: none; box-shadow: none; }
  .seg-btn:hover { color: var(--ink); }

  /* ------------------------------------------------------- the sheets -- */
  /* Both of the sheets that hang off the bar come down out of the button
     that opened them, and go back up into it.  Which point they come out of
     is measured rather than written here: it is the middle of that button,
     and "Download" and "Herunterladen" are not the same width.

     Two states, not two runs of keyframes.  Keyframes could only ever play
     from the beginning, so a sheet caught on its way out -- the button
     pressed twice over, or pressed again straight after a click somewhere
     else shut it -- had to blink back to nothing and arrive all over again,
     and for the sixth of a second it was leaving the button that opened it
     did nothing at all.  Between two states there is no beginning to go
     back to: whatever is half done turns round and finishes the other way
     from where it got to.

     Visibility is in the list, with a wait on it as long as the move, so
     that a sheet on its way out stops being something the mouse or the Tab
     key can find at the moment it is gone rather than before it has left. */
  .sheet-menu {
    transform-origin: top right;
    opacity: 0; visibility: hidden;
    transform: translateY(-10px) scale(.96);
    transition: opacity var(--quick) var(--ease-soft),
                transform var(--move) var(--ease),
                visibility 0s linear var(--move);
  }
  .sheet-menu.here {
    opacity: 1; visibility: visible; transform: none;
    transition: opacity var(--quick) var(--ease-soft),
                transform var(--move) var(--ease),
                visibility 0s;
  }

  /* The menu on the right button, out of the corner it was asked for.  It is
     a plain visible menu that is told to grow, rather than an invisible one
     that is told to appear: if the script never gets as far as saying so --
     because the system was asked to keep still, or because anything at all
     went wrong -- what is left is a menu, not a hole where one should be. */
  .menu { transform-origin: top left; }
  .menu.in { animation: menu-pop .19s var(--ease) backwards; }
  @keyframes menu-pop { from { opacity: 0; transform: scale(.96); } }
  .menu.out {
    opacity: 0; transform: scale(.98); pointer-events: none;
    transition: opacity .12s var(--ease-soft), transform .12s var(--ease-soft);
  }
  .menu button {
    transition: background-color var(--quick) var(--ease-soft),
                transform var(--tap) var(--ease-soft);
  }
  .menu.in button {
    animation: row-in .24s var(--ease) backwards;
    animation-delay: calc(min(var(--i, 0), 8) * 16ms);
  }
  .menu button:hover { transform: translateX(2px); }
  .menu .dot { transition: background-color var(--quick) var(--ease-soft); }
  @keyframes row-in { from { opacity: 0; transform: translateY(-4px); } }

  /* --------------------------------------------- the panel, going away -- */
  /* It closes to nothing rather than vanishing, and the stage takes the room
     as it is given up.  What is inside keeps its full width while it narrows;
     otherwise every word in it would re-wrap on the way out, which looks like
     the panel falling apart rather than closing. */
  #panel {
    transition: width var(--move) var(--ease),
                opacity .16s var(--ease-soft),
                border-color var(--quick) var(--ease-soft),
                visibility 0s;
  }
  /* How wide the panel is depends on the screen, and is decided in two other
     stylesheets between them; nothing here needs to know which.  The script
     measures it as it starts to close and says so here, and the width goes
     back to being whatever it was once it is open again. */
  #panel > * { width: var(--panel-w, 100%); }
  #panel.hide {
    display: flex; width: 0; opacity: 0; visibility: hidden;
    border-color: transparent; pointer-events: none;
    transition: width var(--move) var(--ease),
                opacity .16s var(--ease-soft),
                border-color var(--quick) var(--ease-soft),
                visibility 0s linear var(--move);
  }
  /* the rail that takes its place, and its buttons after it */
  #rail:not([hidden]) { animation: rail-in var(--move) var(--ease) backwards; }
  #rail .icon { animation: row-up .34s var(--ease) backwards; }
  #rail .icon:nth-child(2) { animation-delay: .07s; }
  @keyframes rail-in { from { opacity: 0; transform: translateX(-12px); } }
  @keyframes row-up { from { opacity: 0; transform: translateY(8px); } }

  /* ---------------------------------------------------- folding a card -- */
  /* A card folds shut by losing its height, not by disappearing.  The part
     that holds the height is a grid of a single row, and a grid row can be
     animated from all of it to none of it -- which is the only way to do this
     without measuring anything in the script. */
  section.fold > .fold-body {
    display: grid; grid-template-rows: 1fr; opacity: 1;
    transition: grid-template-rows var(--move) var(--ease),
                opacity var(--quick) var(--ease-soft);
  }
  section.fold.shut > .fold-body { display: grid; grid-template-rows: 0fr; opacity: 0; }
  section.fold > .fold-body > .fold-inner { overflow: hidden; min-height: 0; }
  section.card h2 { transition: color var(--quick) var(--ease-soft); }
  section.fold h2 { transition: margin-bottom var(--move) var(--ease),
                                color var(--quick) var(--ease-soft); }
  section.fold h2:hover { color: var(--ink); }
  section.fold h2::after { transition: transform var(--move) var(--ease-back); }

  /* ------------------------------------------- the things in the panel -- */
  .tab {
    transition: background-color var(--quick) var(--ease-soft),
                border-color var(--quick) var(--ease-soft),
                color var(--quick) var(--ease-soft),
                transform var(--tap) var(--ease-soft);
  }
  .tab:hover:not(.on) { border-color: var(--accent); transform: translateY(-1px); }
  .tab:active { transform: scale(.98); }
  .preset {
    transition: transform var(--quick) var(--ease-back),
                border-color var(--quick) var(--ease-soft),
                box-shadow var(--quick) var(--ease-soft);
  }
  .preset:hover { transform: translateY(-2px); box-shadow: var(--lift); }
  .preset:active { transform: translateY(0) scale(.98); }
  .preset .chip { transition: transform var(--quick) var(--ease-back); }
  .preset:hover .chip { transform: translateY(-1px) scale(1.08); }
  .preset:hover .chip:nth-child(2) { transition-delay: .03s; }
  .preset:hover .chip:nth-child(3) { transition-delay: .06s; }
  .swatch {
    transition: transform var(--quick) var(--ease-back),
                border-color var(--quick) var(--ease-soft),
                box-shadow var(--quick) var(--ease-soft);
  }
  .swatch:hover { transform: scale(1.1); border-color: var(--accent); }
  .swatch:active { transform: scale(.96); }
  .row { transition: background-color var(--quick) var(--ease-soft); }
  .legendkey svg { transition: transform var(--quick) var(--ease-back); }
  .row:hover .legendkey svg { transform: scale(1.1); }
  /* what is selected, when it becomes something else */
  #sel-card.swap #sel-body { animation: swap-in .3s var(--ease) backwards; }
  /* and the two ways of working, as one gives way to the other */
  #source:not([hidden]), #hand:not([hidden]) { animation: swap-in .3s var(--ease) backwards; }
  @keyframes swap-in { from { opacity: 0; transform: translateY(6px); } }
  /* what the check found, and what the runner said */
  .fault {
    animation: row-in .26s var(--ease) backwards;
    transition: background-color var(--quick) var(--ease-soft),
                transform var(--tap) var(--ease-soft);
  }
  .fault:hover { transform: translateX(2px); }
  .tape .said { animation: line-in .22s var(--ease) backwards; }
  #build-note { transition: color var(--quick) var(--ease-soft); }
  #build-note.said-in { animation: line-in .3s var(--ease); }
  @keyframes line-in { from { opacity: 0; transform: translateY(5px); } }
  /* Pressing a button whose whole answer is already sitting there.  The
     line is not written out again -- see talkOnce -- so the one that is
     there is shaken instead, which says "this, still" without saying it
     twice. */
  .tape .said.again { animation: said-again .42s var(--ease); }
  @keyframes said-again {
    0%, 100% { transform: translateX(0); }
    22% { transform: translateX(4px); }
    58% { transform: translateX(-3px); }
    82% { transform: translateX(1px); }
  }

  /* what the build button is doing, said in light as well as in colour */
  .btn.primary.working {
    background-image: linear-gradient(100deg, transparent 20%,
                      rgba(255, 255, 255, .3) 50%, transparent 80%);
    background-size: 220% 100%;
    animation: sweep 1.1s linear infinite;
  }
  .btn.primary.working::after { display: none; }
  .btn.primary.done { animation: done-pop .42s var(--ease-back); }
  @keyframes sweep {
    from { background-position: 180% 0; }
    to { background-position: -120% 0; }
  }
  @keyframes done-pop {
    0% { transform: scale(1); }
    38% { transform: scale(1.035); }
    100% { transform: scale(1); }
  }

  /* --------------------------------------- the pseudocode, full screen -- */
  #code-over:not([hidden]) { animation: dim-in var(--move) var(--ease-soft) backwards; }
  #code-over:not([hidden]) .code-sheet {
    animation: sheet-rise var(--sheet-t) var(--ease) backwards;
  }
  #code-over.going { animation: dim-out .19s var(--ease-soft) forwards; }
  #code-over.going .code-sheet { animation: sheet-fall .19s var(--ease-soft) forwards; }
  @keyframes dim-in { from { opacity: 0; backdrop-filter: blur(0); } }
  @keyframes dim-out { to { opacity: 0; } }
  @keyframes sheet-rise { from { opacity: 0; transform: translateY(16px) scale(.985); } }
  @keyframes sheet-fall { to { opacity: 0; transform: translateY(10px) scale(.99); } }
  #code-home { transition: box-shadow var(--quick) var(--ease-soft); }

  /* ------------------------------------ the run and the code, full screen -- */
  #tape-over:not([hidden]) { animation: dim-in var(--move) var(--ease-soft) backwards; }
  #tape-over:not([hidden]) .code-sheet {
    animation: sheet-rise var(--sheet-t) var(--ease) backwards;
  }
  #tape-over.going { animation: dim-out .19s var(--ease-soft) forwards; }
  #tape-over.going .code-sheet { animation: sheet-fall .19s var(--ease-soft) forwards; }

  /* -------------------------------------------------- the chart itself -- */
  /* A freshly drawn chart arrives with its paper.  The script puts this on
     only when the drawing is a new one, so nothing flickers while a shape is
     being dragged about: that redraws the same chart many times a second, and
     a chart that faded in each time would be unreadable.

     It moves the paper, not the chart on it.  Moving the chart alone slid it
     inside the sheet it sits on and left a strip of bare sheet showing along
     the top and down each side -- a white line round the edge of the drawing,
     for as long as the arriving took.  The two are one thing and move as one. */
  /* The paper is two things wearing one colour: the rectangle the drawing
     fills, and the rounded block it is clipped to.  This selector catches
     both -- the block takes a background, the rectangle a fill -- so a new
     palette moves them together.  One of them changing while the other was
     still on its way is the whole of how a pale curve appears at each
     corner of the chart, and it only has to last a quarter of a second to
     be seen every single time. */
  .sheet, #chart .patch {
    transition: box-shadow var(--move) var(--ease),
                background-color var(--move) var(--ease-soft),
                fill var(--move) var(--ease-soft);
  }
  .sheet.fresh { animation: chart-in .45s var(--ease) backwards; }
  @keyframes chart-in { from { opacity: 0; transform: translateY(8px) scale(.99); } }
  /* zoom, when a button asked for it rather than a drag */
  .sheet.gliding > svg { transition: width .3s var(--ease); }

  /* the shapes, as they are pointed at, chosen, and stepped through */
  #chart .node { transition: filter var(--quick) var(--ease-soft); }
  #chart .node > * {
    transition: fill var(--quick) linear, stroke var(--quick) linear,
                stroke-width var(--quick) var(--ease-soft);
  }
  #chart .node:not(.on):not(.now):hover {
    filter: drop-shadow(0 1px 4px rgba(16, 24, 40, .25));
  }
  svg .link { transition: filter var(--quick) var(--ease-soft); }
  svg .link .flow { transition: stroke-width var(--quick) var(--ease-soft); }
  /* the shape the runner is standing on, breathing while it stands there */
  svg .node.now { animation: now-glow 1.5s var(--ease-soft) infinite; }
  @keyframes now-glow {
    0%, 100% { filter: drop-shadow(0 0 5px rgba(17, 97, 73, .5)); }
    50% { filter: drop-shadow(0 0 13px rgba(17, 97, 73, .85)); }
  }
  svg .spot { transition: r var(--quick) var(--ease-back); }
  svg .knob { transition: r var(--quick) var(--ease-back),
                          fill var(--quick) var(--ease-soft); }
  #stage {
    transition: outline-color var(--quick) var(--ease-soft),
                padding-left var(--move) var(--ease);
  }
  #stage.taking { outline-color: var(--accent); }
  .slider-grip { transition: background-color var(--quick) var(--ease-soft); }
  .slider-step {
    transition: background-color var(--quick) var(--ease-soft),
                color var(--quick) var(--ease-soft),
                transform var(--tap) var(--ease-soft);
  }
  .slider-step:active { transform: scale(.88); }

  /* ----------------------------------------------- light going to dark -- */
  /* Only while the change is happening.  The script puts this on for as long
     as the fade lasts and takes it off again, because a page that transitions
     every colour all of the time is a page that lags behind the mouse. */
  :root.theming *, :root.theming *::before, :root.theming *::after {
    transition: background-color .36s var(--ease-soft),
                border-color .36s var(--ease-soft),
                color .36s var(--ease-soft),
                fill .36s var(--ease-soft),
                stroke .36s var(--ease-soft) !important;
  }
  /* except the block behind a switch, which is very often the thing that was
     just pressed to make the change happen -- it goes on sliding */
  :root.theming .seg::before {
    transition: transform var(--move) var(--ease-back) !important;
  }
  /* The chart is left out of it.  Its colours are chosen in the panel and do
     not change with the light, so fading them would be a few hundred fades of
     one colour into the same colour, on the largest thing on the page. */
  :root.theming #chart, :root.theming #chart * { transition: none !important; }

  /* ----------------------------------------------------- keeping still -- */
  /* Some people are made ill by this sort of thing and some simply do not
     want it; every system has a switch for saying so.  Where it is set,
     everything above still happens -- it just happens at once. */
  @media (prefers-reduced-motion: reduce) {
    :root { --tap: 0s; --quick: 0s; --move: 0s; --sheet-t: 0s; }
    *, *::before, *::after {
      animation-duration: .001ms !important;
      animation-delay: 0s !important;
      animation-iteration-count: 1 !important;
      transition-duration: .001ms !important;
    }
    .btn:hover, .icon:hover, .preset:hover, .tab:hover, .swatch:hover,
    .menu button:hover, .fault:hover, .mark:hover { transform: none; }
  }
</style>
</head>
<body>

<header class="bar">
  <span class="mark" aria-hidden="true">
    <svg viewBox="0 0 24 24">
      <rect x="7.5" y="1.8" width="9" height="5.4" rx="1.4"/>
      <path d="M12 7.2v3.1"/>
      <path d="M12 10.3l4 3.3-4 3.3-4-3.3z"/>
      <path d="M12 16.9v2.1H4.6v3.2M12 19h7.4v3.2"/>
    </svg>
  </span>
  <div class="brand">__HEADING__<small id="sub">__SUB__</small></div>
  <button class="btn primary" id="save-open" data-w="download"
          aria-expanded="false">__W(download)__</button>
  <button class="icon" id="settings" data-w-title="settings" title="__W(settings)__"
          aria-label="__W(settings)__" aria-expanded="false">
    <svg viewBox="0 0 20 20">
      <path d="M2.6 5.5h5.2M11.8 5.5h5.6M2.6 10h9.2M15.8 10h1.6M2.6 14.5h2.8M9.4 14.5h8"/>
      <circle cx="9.8" cy="5.5" r="1.9"/><circle cx="14" cy="10" r="1.9"/>
      <circle cx="7.4" cy="14.5" r="1.9"/></svg>
  </button>
  <div id="save-menu" class="sheet-menu" hidden role="dialog"
       aria-labelledby="save-title">
    <h3 id="save-title" data-w="download">__W(download)__</h3>
    <a class="btn wide" id="svg-link" data-w="dl_svg"
       download="__FILE__.svg" href="#">__W(dl_svg)__</a>
    <div class="pick">
      <label for="scale" data-w="dl_size">__W(dl_size)__</label>
      <select class="btn" id="scale" data-w-title="png_tip" title="__W(png_tip)__">
__OPTIONS__
      </select>
    </div>
    <button class="btn wide" id="png" data-w="dl_png">__W(dl_png)__</button>
    <p class="hint" id="note"></p>
    <h3 data-w="the_design">__W(the_design)__</h3>
    <button class="btn wide" id="save-file" data-w="f_save">__W(f_save)__</button>
    <button class="btn wide" id="open-file" data-w="f_open">__W(f_open)__</button>
    <input type="file" id="file-in" accept=".json,application/json" hidden>
  </div>
  <div id="settings-menu" class="sheet-menu" hidden role="dialog"
       aria-labelledby="settings-title">
    <h3 id="settings-title" data-w="appearance">__W(appearance)__</h3>
    <button class="icon" id="theme" hidden aria-hidden="true" tabindex="-1">
      <svg viewBox="0 0 20 20" id="theme-mark"></svg>
    </button>
    <div class="seg" id="theme-seg">
      <button class="seg-btn" data-theme="auto" data-w="theme_auto">__W(theme_auto)__</button>
      <button class="seg-btn" data-theme="light" data-w="theme_light">__W(theme_light)__</button>
      <button class="seg-btn" data-theme="dark" data-w="theme_dark">__W(theme_dark)__</button>
    </div>
    <h3 data-w="panel_side">__W(panel_side)__</h3>
    <div class="seg" id="side-seg">
      <button class="seg-btn" data-side="left" data-w="side_left">__W(side_left)__</button>
      <button class="seg-btn" data-side="right" data-w="side_right">__W(side_right)__</button>
    </div>
    <label class="switch wide" id="full-row">
      <span data-w="full_screen">__W(full_screen)__</span>
      <input type="checkbox" id="full-on">
    </label>
    <button class="icon" id="full" hidden aria-hidden="true" tabindex="-1">
      <svg viewBox="0 0 20 20" id="full-mark"></svg>
    </button>
  </div>
</header>

<main>
  <nav id="rail" hidden>
    <button class="icon" id="rail-chart" data-w-title="side_chart" title="__W(side_chart)__">
      <svg viewBox="0 0 20 20"><rect x="6" y="2.5" width="8" height="4.5" rx="1"/>
        <path d="M10 7v3M10 10H5.5v3M10 10h4.5v3"/><rect x="2.5" y="13" width="6" height="4.5" rx="1"/>
        <rect x="11.5" y="13" width="6" height="4.5" rx="1"/></svg>
    </button>
    <button class="icon" id="rail-colors" data-w-title="side_colors" title="__W(side_colors)__">
      <svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="7.5"/>
        <path d="M10 2.5v15M2.5 10h15"/></svg>
    </button>
  </nav>

  <aside id="panel">
    <div class="panel-top">
      <div class="seg" id="side-tabs">
        <button class="seg-btn on" id="side-chart" data-w="side_chart">__W(side_chart)__</button>
        <button class="seg-btn" id="side-colors" data-w="side_colors">__W(side_colors)__</button>
      </div>
      <button class="icon" id="collapse" data-w-title="hide_panel" title="__W(hide_panel)__"
              aria-label="__W(hide_panel)__">
        <svg viewBox="0 0 20 20"><path d="M12 4l-6 6 6 6"/></svg>
      </button>
    </div>

    <div id="side-chart-panel">
__SOURCE__
    </div>

    <div id="side-colors-panel" hidden>
    <section class="card">
      <h2 data-w="palette">__W(palette)__</h2>
      <div class="presets" id="presets"></div>
    </section>

    <section class="card">
      <h2 data-w="shapes">__W(shapes)__</h2>
      <div id="kinds"></div>
    </section>

    <section class="card" id="sel-card">
      <h2 data-w="selected">__W(selected)__</h2>
      <div id="sel-body"><p class="none">__W(click_shape)__</p></div>
    </section>

    <section class="card">
      <h2 data-w="rest">__W(rest)__</h2>
      <div id="globals"></div>
      <div class="row" style="border-top:1px solid var(--line-soft)">
        <span class="name" data-w="show_grid">__W(show_grid)__</span>
        <label class="switch"><input type="checkbox" id="grid-on" checked></label>
      </div>
    </section>

      <section class="card">
        <button class="btn" id="reset" data-w="reset"
                style="width:100%; justify-content:center">__W(reset)__</button>
      </section>
    </div>
  </aside>

  <div id="stage">
    <div class="wrap"><div class="sheet" id="sheet">
__SVG__
    </div></div>
  </div>
</main>

<footer class="bar">
  <span class="grow"></span>
  <div class="seg" id="hold-seg">
    <button class="seg-btn on" id="hold-lock" data-w-title="lock_tip"
            title="__W(lock_tip)__">
      <svg viewBox="0 0 20 20" aria-hidden="true">
        <rect x="4.2" y="8.6" width="11.6" height="8.6" rx="2"/>
        <path d="M6.9 8.6V6.3a3.1 3.1 0 0 1 6.2 0v2.3"/></svg>
      <span data-w="hold_locked">__W(hold_locked)__</span>
    </button>
    <button class="seg-btn" id="hold-loose" data-w-title="loose_tip"
            title="__W(loose_tip)__">
      <svg viewBox="0 0 20 20" aria-hidden="true">
        <rect x="4.2" y="8.6" width="11.6" height="8.6" rx="2"/>
        <path d="M6.9 8.6V6.3a3.1 3.1 0 0 1 6.1-.7"/></svg>
      <span data-w="hold_loose">__W(hold_loose)__</span>
    </button>
  </div>
  <button class="btn small" id="out" data-w-title="zoom_out" title="__W(zoom_out)__">&minus;</button>
  <span class="zoom" id="pct">100%</span>
  <button class="btn small" id="in" data-w-title="zoom_in" title="__W(zoom_in)__">+</button>
  <button class="btn small" id="fit" data-w="fit">__W(fit)__</button>
  <button class="btn small" id="actual">__W(actual)__</button>
</footer>

<div id="code-over" hidden>
  <div class="code-sheet">
    <div class="code-bar">
      <span class="mark small" aria-hidden="true">
        <svg viewBox="0 0 24 24">
          <rect x="7.5" y="1.8" width="9" height="5.4" rx="1.4"/>
          <path d="M12 7.2v3.1"/>
          <path d="M12 10.3l4 3.3-4 3.3-4-3.3z"/>
          <path d="M12 16.9v2.1H4.6v3.2M12 19h7.4v3.2"/>
        </svg>
      </span>
      <strong data-w="pseudocode">__W(pseudocode)__</strong>
      <span class="code-count" id="code-count"></span>
      <span class="code-esc" data-w="code_esc">__W(code_esc)__</span>
      <button class="btn small primary" id="code-done" data-w="done">__W(done)__</button>
    </div>
    <div id="code-slot"><pre class="code-rule" id="code-rule" aria-hidden="true"></pre></div>
  </div>
</div>

<div id="tape-over" hidden>
  <div class="code-sheet">
    <div class="code-bar">
      <span class="mark small" aria-hidden="true">
        <svg viewBox="0 0 24 24">
          <rect x="7.5" y="1.8" width="9" height="5.4" rx="1.4"/>
          <path d="M12 7.2v3.1"/>
          <path d="M12 10.3l4 3.3-4 3.3-4-3.3z"/>
          <path d="M12 16.9v2.1H4.6v3.2M12 19h7.4v3.2"/>
        </svg>
      </span>
      <strong id="tape-title" data-w="r_head">__W(r_head)__</strong>
      <button class="btn small back" id="tape-back" hidden><span class="full" data-w="r_back">__W(r_back)__</span><span class="short" data-w="back">__W(back)__</span></button>
      <span class="code-count" id="tape-count"></span>
      <button class="btn small primary" id="tape-run" data-w="r_run">__W(r_run)__</button>
      <button class="btn small" id="tape-code" data-w="r_code">__W(r_code)__</button>
      <span class="code-esc" data-w="code_esc">__W(code_esc)__</span>
      <button class="btn small" id="tape-done" data-w="done">__W(done)__</button>
    </div>
    <div id="tape-slot"></div>
    <div id="code-out" hidden></div>
  </div>
</div>

<script>
(function () {
  "use strict";
  // Everything below is about looking at the chart and coloring it in.  The
  // drawing itself came out of the script; nothing here can change what it
  // says, only what it looks like.
  var MODE = "__MODE__";                 // "page" beside a file, "studio" served
  var FILE = __JSNAME__;
  var ALL = __ALLWORDS__;                // every word, in every language
  var LANG = "__LANG__";
  var SHAPE_LIST = __SHAPELIST__;        // every shape that can be drawn
  var ROLES = ["oval", "rect", "io", "diamond", "hex", "sub"];
  var geom = {};                         // which shape draws which kind
  var PYODIDE = "__PYODIDE__";           // where the browser gets Python
  var MODULE = "__MODULE__";             // and the builder it imports
  var TXT = ALL[LANG] || ALL.en;         // the ones this page is using
  function say(key, fill) {              // ... with {things} filled in
    var out = TXT[key] || key;
    for (var name in (fill || {})) {
      out = out.split("{" + name + "}").join(fill[name]);
    }
    return out;
  }
  function kinds() {                     // named in the language of the day
    return [["oval", TXT.key_oval], ["rect", TXT.key_rect],
            ["io", TXT.key_io], ["diamond", TXT.key_diamond],
            ["hex", TXT.key_hex], ["sub", TXT.key_sub]];
  }
  var PRESETS = [
    ["p_ink", { sheet: "#ffffff", ink: "#000000", words: "#000000",
              grid: "#e7ebf0",
              fills: { oval: "#ffffff", rect: "#ffffff", io: "#ffffff",
                       diamond: "#ffffff", hex: "#ffffff", sub: "#ffffff" } }],
    ["p_classic", { sheet: "#ffffff", ink: "#111827", words: "#111827",
                  grid: "#e7ebf0",
                  fills: { oval: "#dbeafe", rect: "#ffffff", io: "#eaf5ff",
                           diamond: "#fff4d6", hex: "#fff4d6", sub: "#f1e7ff" } }],
    ["p_slate", { sheet: "#f8fafc", ink: "#334155", words: "#0f172a",
                grid: "#e2e8f0",
                fills: { oval: "#e2e8f0", rect: "#ffffff", io: "#e0f2fe",
                         diamond: "#ede9fe", hex: "#ede9fe", sub: "#f1f5f9" } }],
    ["p_meadow", { sheet: "#ffffff", ink: "#14532d", words: "#14532d",
                 grid: "#e3efe6",
                 fills: { oval: "#dcfce7", rect: "#ffffff", io: "#ecfccb",
                          diamond: "#fef9c3", hex: "#fef9c3", sub: "#e0f2fe" } }],
    ["p_sunset", { sheet: "#fffdf9", ink: "#7c2d12", words: "#7c2d12",
                 grid: "#f2e9df",
                 fills: { oval: "#ffedd5", rect: "#ffffff", io: "#fee2e2",
                          diamond: "#fef3c7", hex: "#fef3c7", sub: "#fae8ff" } }],
    ["p_night", { sheet: "#0f172a", ink: "#cbd5e1", words: "#e2e8f0",
                grid: "#1e293b",
                fills: { oval: "#1e293b", rect: "#111c30", io: "#152744",
                         diamond: "#3a2e17", hex: "#3a2e17", sub: "#2b1b46" } }]
  ];

  function el(q, root) { return (root || document).querySelector(q); }
  function has(q) { return !!document.querySelector(q); }
  function all(q, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(q));
  }
  // Light or dark: whatever the computer is set to, unless the page has
  // been told otherwise, which it remembers.
  var THEMES = ["auto", "light", "dark"];
  var theme = "auto";

  function nightOutside() {             // what the computer itself is set to
    try { return matchMedia("(prefers-color-scheme: dark)").matches; }
    catch (e) { return false; }
  }
  function wearing() {                  // what the page is actually showing
    return theme === "auto" ? (nightOutside() ? "dark" : "light") : theme;
  }

  function wearTheme() {
    if (theme === "auto") { document.documentElement.removeAttribute("data-theme"); }
    else { document.documentElement.setAttribute("data-theme", theme); }
    var now = wearing();
    var mark = el("#theme-mark");
    if (mark) {
      // The button shows the way it would go, not the way it is: a moon to
      // turn the lights off, a sun to turn them back on.
      mark.innerHTML = now === "light"
        ? '<path d="M16.5 12.4A7 7 0 0 1 7.6 3.5a7 7 0 1 0 8.9 8.9z"/>'
        : '<circle cx="10" cy="10" r="4"/><path d="M10 1v2M10 17v2M1 10h2M17 ' +
          '10h2M3.6 3.6l1.4 1.4M15 15l1.4 1.4M16.4 3.6L15 5M5 15l-1.4 1.4"/>';
      mark.style.opacity = "1";
    }
    var button = el("#theme");
    if (button) {
      button.title = (TXT.theme || "") + " · " +
                     (TXT["theme_" + theme] || theme);
    }
    all("#theme-seg .seg-btn").forEach(function (b) {
      b.classList.toggle("on", b.dataset.theme === theme);
    });
    try { localStorage.setItem("flowchart-theme", theme); } catch (e) { /* fine */ }
  }

  function setTheme(want) {
    theme = THEMES.indexOf(want) >= 0 ? want : "auto";
    wearTheme();
  }

  try {
    var kept = localStorage.getItem("flowchart-theme");
    if (THEMES.indexOf(kept) >= 0) { theme = kept; }
  } catch (e) { /* no storage: auto it is */ }

  // Every press has to change the picture.  Cycling auto -> light -> dark
  // did not: on a computer already set to light, the first press moved from
  // auto to light and nothing on the screen moved at all, so the button
  // looked broken every third press.  So the button is a straight switch --
  // whatever is on screen now, show the other one -- and "auto" stays as the
  // setting it starts on and can be put back to in Settings.
  el("#theme").onclick = function () {
    setTheme(wearing() === "dark" ? "light" : "dark");
  };

  try {                                 // follow the computer while on auto
    matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", function () {
        if (theme === "auto") { wearTheme(); }
      });
  } catch (e) { /* older browser: it will catch up on the next press */ }

  function dress() {                     // put the words on the page
    all("[data-w]").forEach(function (e) {
      if (TXT[e.dataset.w]) { e.textContent = TXT[e.dataset.w]; }
    });
    all("[data-w-title]").forEach(function (e) {
      if (TXT[e.dataset.wTitle]) { e.title = TXT[e.dataset.wTitle]; }
    });
    all("[data-w-ph]").forEach(function (e) {
      if (TXT[e.dataset.wPh]) { e.placeholder = TXT[e.dataset.wPh]; }
    });
    document.documentElement.lang = LANG;
    wearTheme();
  }

  function darken(hex, by) {
    var m = /^#?([\da-f]{2})([\da-f]{2})([\da-f]{2})$/i.exec(hex || "");
    if (!m) { return hex; }
    return "#" + [1, 2, 3].map(function (i) {
      var v = Math.round(parseInt(m[i], 16) * by);
      return ("0" + Math.max(0, Math.min(255, v)).toString(16)).slice(-2);
    }).join("");
  }

  var style = { sheet: "", ink: "", words: "", grid: "", gridOff: false,
                kinds: {}, nodes: {} };
  var chart = null, sel = null, W = 0, H = 0, zoom = 1;

  // ------------------------------------------------------------ painting --
  function paint() {
    if (!chart) { return; }
    all(".sheet, .patch", chart).forEach(function (e) {
      e.style.fill = style.sheet || "";
    });
    // The paper is two things: the rectangle the drawing fills, and the
    // rounded block it is clipped to.  Only the rectangle was being
    // coloured, so on any palette whose paper is not white -- Night most of
    // all -- the block's own white showed through where the corners round
    // off, as a pale curve at each corner of the chart.  They are one sheet
    // of paper, so they take one colour; with no palette on, both fall back
    // to the white the stylesheet gives it.
    var block = el("#sheet");
    if (block) { block.style.background = style.sheet || ""; }
    all(".flow", chart).forEach(function (e) { e.style.stroke = style.ink || ""; });
    all(".head", chart).forEach(function (e) {
      e.style.fill = style.ink || "";
      e.style.stroke = style.ink || "";
    });
    all(".label, .heading, .title, .author", chart).forEach(function (e) {
      e.style.fill = style.words || style.ink || "";
    });
    all(".grid.fine", chart).forEach(function (e) { e.style.stroke = style.grid || ""; });
    all(".grid.major", chart).forEach(function (e) {
      e.style.stroke = style.grid ? darken(style.grid, 0.9) : "";
    });
    all(".grid", chart).forEach(function (e) {
      e.style.display = style.gridOff ? "none" : "";
    });
    all(".node", chart).forEach(function (g) {
      var k = style.kinds[g.dataset.kind] || {}, n = style.nodes[g.dataset.i] || {};
      var fill = n.fill || k.fill || "";
      var line = n.line || k.line || style.ink || "";
      var word = n.text || k.text || style.words || style.ink || "";
      all("ellipse, rect, polygon, path", g).forEach(function (e) {
        // .ghost is the clear pane behind a words-only box: it is there to
        // be clicked, never to be seen, so no colour is put on it at all
        if (e.classList.contains("ghost")) { return; }
        if (!e.classList.contains("trim")) { e.style.fill = fill; }
        e.style.stroke = line;
      });
      all("line", g).forEach(function (e) { e.style.stroke = line; });
      all("text", g).forEach(function (e) { e.style.fill = word; });
    });
    all(".keymark", document).forEach(function (mark) {
      var kind = mark.dataset.kind, k = style.kinds[kind] || {};
      all("ellipse, rect, polygon, path, circle", mark).forEach(function (e) {
        e.setAttribute("fill", k.fill || style.sheet || "#ffffff");
        e.setAttribute("stroke", k.line || style.ink || "#10151b");
      });
      all("line", mark).forEach(function (e) {
        e.setAttribute("stroke", k.line || style.ink || "#10151b");
      });
    });
    keep();
  }

  // ----------------------------------------------------- the panel of it --
  // Every shape, drawn the same way the script draws it -- used for the
  // shapes you place by hand and, small, for the picture on each button, so
  // what you pick is exactly what you get.
  function shapeArt(kind, cx, cy, w, h, fill) {
    var l = cx - w / 2, r = cx + w / 2, t = cy - h / 2, b = cy + h / 2;
    var lean = Math.min(12, w / 4), paint = fill || "#ffffff";
    var box = 'fill="' + paint + '"';
    function poly(pts) { return '<polygon points="' + pts.join(" ") + '" ' + box + '/>'; }
    function P(x, y) { return round(x) + "," + round(y); }
    function round(v) { return Math.round(v * 10) / 10; }
    switch (kind) {
      case "oval": case "circle":
        return '<ellipse cx="' + round(cx) + '" cy="' + round(cy) + '" rx="' +
               round(w / 2) + '" ry="' + round(h / 2) + '" ' + box + '/>';
      case "rect": case "sub": {
        var art = '<rect x="' + round(l) + '" y="' + round(t) + '" width="' +
                  round(w) + '" height="' + round(h) + '" rx="3" ' + box + '/>';
        if (kind === "sub") {
          art += '<line x1="' + round(l + 6) + '" y1="' + round(t) + '" x2="' +
                 round(l + 6) + '" y2="' + round(b) + '"/><line x1="' +
                 round(r - 6) + '" y1="' + round(t) + '" x2="' + round(r - 6) +
                 '" y2="' + round(b) + '"/>';
        }
        return art;
      }
      case "roundrect":
        return '<rect x="' + round(l) + '" y="' + round(t) + '" width="' + round(w) +
               '" height="' + round(h) + '" rx="' + round(Math.min(14, h / 2.4)) +
               '" ' + box + '/>';
      case "io": return poly([P(l + lean, t), P(r, t), P(r - lean, b), P(l, b)]);
      case "io_back": return poly([P(l, t), P(r - lean, t), P(r, b), P(l + lean, b)]);
      case "trap": return poly([P(l + lean, t), P(r - lean, t), P(r, b), P(l, b)]);
      case "hex": return poly([P(l + lean, t), P(r - lean, t), P(r, cy),
                               P(r - lean, b), P(l + lean, b), P(l, cy)]);
      case "manual": {
        var slope = Math.min(11, h * 0.28);
        return poly([P(l, t + slope), P(r, t), P(r, b), P(l, b)]);
      }
      case "card": {
        var nick = Math.min(14, h * 0.34);
        return poly([P(l + nick, t), P(r, t), P(r, b), P(l, b), P(l, t + nick)]);
      }
      case "note": {
        var fold = Math.min(14, h * 0.34);
        return '<path d="M' + P(l, t) + "H" + round(r - fold) + "L" + P(r, t + fold) +
               "V" + round(b) + "H" + round(l) + 'Z" ' + box + '/>' +
               '<path class="trim" d="M' + P(r - fold, t) + "V" + round(t + fold) +
               "H" + round(r) + '" fill="none"/>';
      }
      case "doc": {
        var wave = Math.min(10, h * 0.18);
        return '<path d="M' + P(l, t) + "H" + round(r) + "V" + round(b - wave) +
               "C" + P(r - w * 0.25, b - wave * 2.2) + " " + P(r - w * 0.4, b + wave * 0.9) +
               " " + P(cx, b - wave * 0.2) +
               "C" + P(l + w * 0.32, b - wave * 1.6) + " " + P(l + w * 0.18, b + wave * 0.7) +
               " " + P(l, b - wave) + 'Z" ' + box + '/>';
      }
      case "docs": {
        var step = Math.min(5, h * 0.12), art = "";
        [2, 1].forEach(function (back) {
          art += '<rect x="' + round(l + back * step) + '" y="' + round(t) +
                 '" width="' + round(w - back * step) + '" height="' +
                 round(h - back * step * 2) + '" rx="2" ' + box + '/>';
        });
        return art + shapeArt("doc", cx - step, cy + step, w - 2 * step, h - 2 * step, paint);
      }
      case "store": {
        var lip = Math.min(11, h * 0.24);
        return '<path d="M' + P(l, t + lip) + "V" + round(b - lip) +
               "A" + round(w / 2) + "," + round(lip) + " 0 0 0 " + P(r, b - lip) +
               "V" + round(t + lip) + "A" + round(w / 2) + "," + round(lip) +
               " 0 0 0 " + P(l, t + lip) + 'Z" ' + box + '/>' +
               '<path class="trim" d="M' + P(l, t + lip) + "A" + round(w / 2) + "," +
               round(lip) + " 0 0 0 " + P(r, t + lip) + '" fill="none"/>';
      }
      case "delay": {
        var bulge = Math.min(h / 2, w / 2);
        return '<path d="M' + P(l, t) + "H" + round(r - bulge) + "A" + round(bulge) +
               "," + round(h / 2) + " 0 0 1 " + P(r - bulge, b) + "H" + round(l) +
               'Z" ' + box + '/>';
      }
      case "screen": {
        var bow = Math.min(16, w * 0.16);
        return '<path d="M' + P(l + bow, t) + "H" + round(r - bow) +
               "A" + round(h / 2) + "," + round(h / 2) + " 0 0 1 " + P(r - bow, b) +
               "H" + round(l + bow) + "C" + P(l, cy + h * 0.28) + " " +
               P(l, cy - h * 0.28) + " " + P(l + bow, t) + 'Z" ' + box + '/>';
      }
      case "offpage":                     // carries on somewhere else
        return poly([P(l, t), P(r, t), P(r, b - Math.min(18, h * 0.42)),
                     P(cx, b), P(l, b - Math.min(18, h * 0.42))]);
      case "loop": {                      // a loop's limit: For, mostly
        var cut = Math.min(14, h * 0.34, w / 5);
        return poly([P(l + cut, t), P(r - cut, t), P(r, t + cut), P(r, b),
                     P(l, b), P(l, t + cut)]);
      }
      case "parallel": {                  // things happening side by side
        var bar = Math.max(2.5, Math.min(5, h * 0.11));
        return '<rect x="' + round(l) + '" y="' + round(t) + '" width="' + round(w) +
               '" height="' + round(h) + '" rx="2" ' + box + '/>' +
               '<path class="trim" d="M' + P(l, t + bar * 2) + "H" + round(r) +
               "M" + P(l, b - bar * 2) + "H" + round(r) + '" fill="none"/>';
      }
      case "stored": {                    // held somewhere inside
        var rule = Math.min(11, w * 0.14);
        return '<rect x="' + round(l) + '" y="' + round(t) + '" width="' + round(w) +
               '" height="' + round(h) + '" rx="2" ' + box + '/>' +
               '<path class="trim" d="M' + P(l + rule, t) + "V" + round(b) +
               "M" + P(l, t + rule) + "H" + round(r) + '" fill="none"/>';
      }
      case "cloud": {
        // Drawn so that it touches its box at the middle of all four sides,
        // which is where a line joining it expects to meet it.
        var qw = w / 2, qh = h / 2;
        return '<path d="M' + P(l, cy) +
               "C" + P(l, cy - qh * 0.75) + " " + P(cx - qw * 0.72, t - qh * 0.18) +
               " " + P(cx - qw * 0.34, t + qh * 0.16) +
               "C" + P(cx - qw * 0.1, t - qh * 0.2) + " " + P(cx + qw * 0.34, t - qh * 0.2) +
               " " + P(cx + qw * 0.42, t + qh * 0.2) +
               "C" + P(cx + qw * 0.85, t + qh * 0.02) + " " + P(r, cy - qh * 0.7) +
               " " + P(r, cy) +
               "C" + P(r, cy + qh * 0.72) + " " + P(cx + qw * 0.5, b) + " " + P(cx, b) +
               "C" + P(cx - qw * 0.55, b) + " " + P(l, cy + qh * 0.75) + " " + P(l, cy) +
               'Z" ' + box + '/>';
      }
      case "text":                       // words on their own, no outline
        // Nothing is drawn but something has to be there to take hold of,
        // so the words sit on a pane of clear glass.
        return '<rect class="ghost" x="' + round(l) + '" y="' + round(t) +
               '" width="' + round(w) + '" height="' + round(h) +
               '" fill="none" pointer-events="all"/>';
      case "actor": {                    // somebody, rather than something
        var head = Math.min(h * 0.17, w * 0.17);
        var neck = t + head * 2;
        var hip = t + h * 0.62;
        return '<circle cx="' + round(cx) + '" cy="' + round(t + head) + '" r="' +
               round(head) + '" ' + box + '/>' +
               '<path class="trim" d="M' + P(cx, neck) + "V" + round(hip) +
               "M" + P(cx - w * 0.22, neck + h * 0.12) + "H" + round(cx + w * 0.22) +
               "M" + P(cx, hip) + "L" + P(cx - w * 0.2, b) +
               "M" + P(cx, hip) + "L" + P(cx + w * 0.2, b) + '" fill="none"/>';
      }
      case "callout": {                  // something said about it
        var tail = Math.min(16, h * 0.28);
        var sill = b - tail;
        var rnd = Math.min(10, h / 4);
        return '<path d="M' + P(l + rnd, t) + "H" + round(r - rnd) +
               "Q" + P(r, t) + " " + P(r, t + rnd) + "V" + round(sill - rnd) +
               "Q" + P(r, sill) + " " + P(r - rnd, sill) +
               "H" + round(l + w * 0.34) + "L" + P(l + w * 0.2, b) +
               "L" + P(l + w * 0.24, sill) + "H" + round(l + rnd) +
               "Q" + P(l, sill) + " " + P(l, sill - rnd) + "V" + round(t + rnd) +
               "Q" + P(l, t) + " " + P(l + rnd, t) + 'Z" ' + box + '/>';
      }
      case "cube": {
        var lip = Math.min(14, h * 0.26, w * 0.14);
        return '<path d="M' + P(l, t + lip) + "L" + P(l + lip, t) + "H" + round(r) +
               "V" + round(b - lip) + "L" + P(r - lip, b) + "H" + round(l) +
               'Z" ' + box + '/>' +
               '<path class="trim" d="M' + P(l, t + lip) + "H" + round(r - lip) +
               "V" + round(b) + "M" + P(r - lip, t + lip) + "L" + P(r, t) +
               '" fill="none"/>';
      }
      case "step": {                     // one step of several, in a row
        var notch = Math.min(22, w * 0.16);
        return poly([P(l, t), P(r - notch, t), P(r, cy), P(r - notch, b),
                     P(l, b), P(l + notch, cy)]);
      }
      case "table": {
        var head = Math.min(16, h * 0.3);
        return '<rect x="' + round(l) + '" y="' + round(t) + '" width="' + round(w) +
               '" height="' + round(h) + '" rx="2" ' + box + '/>' +
               '<path class="trim" d="M' + P(l, t + head) + "H" + round(r) +
               "M" + P(l + w / 3, t + head) + "V" + round(b) +
               "M" + P(l + w * 2 / 3, t + head) + "V" + round(b) + '" fill="none"/>';
      }
      case "arrow": {
        var head = Math.min(26, w * 0.3), wing = h * 0.26;
        return poly([P(l, t + wing), P(r - head, t + wing), P(r - head, t), P(r, cy),
                     P(r - head, b), P(r - head, b - wing), P(l, b - wing)]);
      }
      default: return poly([P(cx, t), P(r, cy), P(cx, b), P(l, cy)]);
    }
  }

  function keyMark(kind) {               // the same shape, in miniature
    return '<span class="legendkey"><svg class="keymark" data-kind="' + kind +
           '" width="24" height="17" viewBox="0 0 24 17" stroke="#10151b" ' +
           'stroke-width="1.2" fill="none">' +
           shapeArt(kind, 12, 8.5, 21, 14) + "</svg></span>";
  }

  function swatch(value, fallback, onPick) {
    var input = document.createElement("input");
    input.type = "color";
    input.className = "swatch";
    input.value = value || fallback;
    input.oninput = function () { onPick(input.value); };
    return input;
  }

  function buildKinds() {
    var box = el("#kinds");
    box.innerHTML = "";
    kinds().forEach(function (pair) {
      var kind = pair[0], name = pair[1];
      var found = all('.node[data-kind="' + kind + '"]', chart);
      if (!found.length) { return; }
      var row = document.createElement("div");
      row.className = "row";
      row.innerHTML = keyMark(kind) + '<span class="name">' + name +
                      '</span><span class="count">' + found.length + '</span>';
      var k = style.kinds[kind] = style.kinds[kind] || {};
      row.appendChild(swatch(k.fill, "#ffffff", function (v) {
        k.fill = v; paint();
      }));
      row.appendChild(swatch(k.line, style.ink || "#000000", function (v) {
        k.line = v; paint();
      }));
      box.appendChild(row);
    });
  }

  function buildGlobals() {
    var box = el("#globals");
    box.innerHTML = "";
    [[TXT.lines, "ink", "#000000"],
     [TXT.text, "words", "#000000"],
     [TXT.paper, "sheet", "#ffffff"],
     [TXT.grid, "grid", "#e7ebf0"]].forEach(function (item) {
      var row = document.createElement("div");
      row.className = "row";
      row.innerHTML = '<span class="name">' + item[0] + "</span>";
      row.appendChild(swatch(style[item[1]], item[2], function (v) {
        style[item[1]] = v; paint(); buildKinds();
      }));
      box.appendChild(row);
    });
  }

  function said(g) {
    return all("text", g).map(function (t) { return t.textContent; }).join(" ");
  }

  function drawSelection() {
    var body = el("#sel-body");
    body.innerHTML = "";
    if (!sel) {
      body.innerHTML = '<p class="none">' + TXT.click_shape + "</p>";
      return;
    }
    var kind = sel.dataset.kind, i = sel.dataset.i;
    var name = (kinds().filter(function (p) { return p[0] === kind; })[0] || [0, kind])[1];
    var head = document.createElement("div");
    head.innerHTML = '<div class="what">' + name + '</div><div class="said">' +
                     said(sel).replace(/[<>&]/g, "") + "</div>";
    body.appendChild(head);
    var mine = style.nodes[i] = style.nodes[i] || {};
    var k = style.kinds[kind] || {};
    [[TXT.fill, "fill", k.fill || "#ffffff"],
     [TXT.outline, "line", k.line || style.ink || "#000000"],
     [TXT.text, "text", k.text || style.words || style.ink || "#000000"]]
      .forEach(function (item) {
        var row = document.createElement("div");
        row.className = "row";
        row.innerHTML = '<span class="name">' + item[0] + "</span>";
        row.appendChild(swatch(mine[item[1]], item[2], function (v) {
          mine[item[1]] = v; paint();
        }));
        body.appendChild(row);
      });
    var go = document.createElement("div");
    go.className = "go";
    go.style.cssText = "display:flex; gap:8px; margin-top:10px";
    var spread = document.createElement("button");
    spread.className = "btn small";
    spread.textContent = say("apply_all", { n: found(kind), what: name });
    spread.onclick = function () {
      var k2 = style.kinds[kind] = style.kinds[kind] || {};
      if (mine.fill) { k2.fill = mine.fill; }
      if (mine.line) { k2.line = mine.line; }
      if (mine.text) { k2.text = mine.text; }
      style.nodes[i] = {};
      paint(); buildKinds(); drawSelection();
    };
    var clear = document.createElement("button");
    clear.className = "btn small";
    clear.textContent = TXT.clear;
    clear.onclick = function () {
      style.nodes[i] = {};
      paint(); drawSelection();
    };
    go.appendChild(spread);
    go.appendChild(clear);
    body.appendChild(go);
  }

  function found(kind) {
    return all('.node[data-kind="' + kind + '"]', chart).length;
  }

  function select(g) {
    if (sel) { sel.classList.remove("on"); }
    sel = g || null;
    if (sel) { sel.classList.add("on"); }
    drawSelection();
  }

  function buildPresets() {
    var box = el("#presets");
    box.innerHTML = "";
    PRESETS.forEach(function (pair) {
      var name = TXT[pair[0]] || pair[0], p = pair[1];
      var b = document.createElement("button");
      b.className = "preset";
      b.innerHTML = '<span class="chips">' +
        ["oval", "io", "diamond"].map(function (k) {
          return '<span class="chip" style="background:' + p.fills[k] + '"></span>';
        }).join("") + "</span><span>" + name + "</span>";
      b.onclick = function () {
        style.sheet = p.sheet; style.ink = p.ink;
        style.words = p.words; style.grid = p.grid;
        style.kinds = {};
        Object.keys(p.fills).forEach(function (k) {
          style.kinds[k] = { fill: p.fills[k], line: p.ink, text: p.words };
        });
        all(".preset", box).forEach(function (x) { x.classList.remove("on"); });
        b.classList.add("on");
        paint(); buildKinds(); buildGlobals(); drawSelection();
      };
      box.appendChild(b);
    });
  }

  // ------------------------------------------------------ keeping it all --
  // The studio opens on an empty page.  What was written last time is not
  // put back into the box: opening it is nearly always the start of
  // something, and having to clear somebody else's program -- or your own
  // from a fortnight ago -- before you can begin is a worse first minute
  // than an empty box is.  A program worth keeping is kept in a file, which
  // is what Save this to a file is for, and Open a file brings it back
  // whole: the words, the title, the colours and all.
  //
  // So the pseudocode is not written to storage either.  Keeping a copy
  // that nothing ever reads would be no kindness: it would sit there being
  // overwritten by the next empty page, out of sight and out of reach, and
  // look like a safety net while being none.
  //
  // How the studio is set up is still remembered -- your name, the shape to
  // aim at, whether the key and the grid are on, which shape stands for
  // which kind of step.  Those are how you like it rather than what you
  // were doing, and nobody wants to say again every morning that their name
  // is still their name.
  //
  // The title is not among them.  A title belongs to the program it is the
  // title of, and an empty page headed with the name of last week's work is
  // a stranger thing to be handed than an empty page.
  function remember() {
    try {
      localStorage.setItem("flowchart-source", JSON.stringify({
        author: el("#f-author").value, shape: el("#f-shape").value,
        legend: el("#f-legend").checked,
        grid: el("#f-grid").checked, geom: geom
      }));
    } catch (e) { /* storage turned off: it just will not be there next time */ }
  }
  // It used to be called recallSource and hand back whether it had found a
  // program to draw.  It finds no program now, so it is named for what it
  // does do and says nothing back; what is worth drawing on opening is
  // whatever is in the box, which is a thing the page can see for itself.
  function recallSetup() {
    if (!el("#code")) { return; }
    try {
      var was = JSON.parse(localStorage.getItem("flowchart-source"));
      if (!was) { return; }
      el("#f-author").value = was.author || "";
      if (was.shape) { el("#f-shape").value = was.shape; }
      el("#f-legend").checked = !!was.legend;
      el("#f-grid").checked = was.grid !== false;
      if (was.geom) { geom = was.geom; drawRoles(); }
    } catch (e) { /* nothing kept, or unreadable: the defaults stand */ }
  }

  function keep() {
    try {
      localStorage.setItem("flowchart-colors:" + FILE, JSON.stringify(style));
    } catch (e) { /* a private window, or storage turned off: never mind */ }
  }
  function recall() {
    try {
      var was = JSON.parse(localStorage.getItem("flowchart-colors:" + FILE));
      if (was && was.kinds) { style = was; }
    } catch (e) { /* nothing kept, or unreadable */ }
  }

  // ------------------------------------------------------- the chart pane --
  // Where a mouse event lands on the paper, in the chart's own numbers --
  // which is what the shapes and arrows are kept in, whatever the zoom.
  function onPaper(ev) {
    if (!chart || !chart.getScreenCTM) { return null; }
    var frame = chart.getScreenCTM();
    if (!frame) { return null; }
    var spot = chart.createSVGPoint();
    spot.x = ev.clientX;
    spot.y = ev.clientY;
    spot = spot.matrixTransform(frame.inverse());
    return { x: spot.x, y: spot.y };   // the paper's corner is the origin
  }

  function bind() {
    chart = el("#sheet svg");
    if (!chart) { return; }
    chart.id = "chart";
    var box = (chart.getAttribute("viewBox") || "").split(/[\s,]+/).map(Number);
    W = box[2] || 800; H = box[3] || 600;
    sizeList();          // what a PNG of it comes to, now the chart is known
    chart.onclick = function (ev) {
      var g = ev.target.closest ? ev.target.closest(".node") : null;
      if (byHand) {
        var arrow = ev.target.closest ? ev.target.closest(".link") : null;
        var spot = ev.target.closest ? ev.target.closest(".spot") : null;
        if (spot) { handClick(+spot.dataset.i); return; }
        if (g) { handClick(+g.dataset.i.slice(1)); }
        else if (arrow) { pickLink(+arrow.dataset.link); }
        else {
          var spot = onPaper(ev);        // near enough to an arrow to count?
          var meant = spot && linkNear(spot.x, spot.y, 16);
          if (meant) { pickLink(meant.id); return; }
          picked = chosen = null; joining = false;
          drawHand(); drawHandPanel();
        }
        return;
      }
      select(g);
    };
    if (byHand) { joinDrag(chart); dragging(chart); }
    chart.oncontextmenu = function (ev) {
      if (!byHand) { return; }
      var g = ev.target.closest ? ev.target.closest(".node") : null;
      var arrow = ev.target.closest ? ev.target.closest(".link") : null;
      ev.preventDefault();
      if (g) { shapeMenu(nodeById(+g.dataset.i.slice(1)), ev.clientX, ev.clientY); }
      else if (arrow) { arrowMenu(linkById(+arrow.dataset.link), ev.clientX, ev.clientY); }
      else {
        var spot = onPaper(ev);
        var meant = spot && linkNear(spot.x, spot.y, 16);
        if (meant) { arrowMenu(meant, ev.clientX, ev.clientY); }
        else { paperMenu(ev.clientX, ev.clientY); }
      }
    };
    chart.ondblclick = function (ev) {
      var g = ev.target.closest ? ev.target.closest(".node") : null;
      if (g) {
        if (byHand) { typeInto(g); }
        else { pickLine(+g.dataset.i); }
        return;
      }
      if (!byHand) { return; }
      var arrow = ev.target.closest ? ev.target.closest(".link") : null;
      var link = arrow ? linkById(+arrow.dataset.link) : null;
      if (!link) {                       // near enough to it counts as on it
        var spot = onPaper(ev);
        link = spot && linkNear(spot.x, spot.y, 16);
      }
      if (link) { chosen = link.id; typeOnLink(link); }
    };
    sel = null;
    show();
    buildKinds();
    drawSelection();
    linkSvg();
    sizeNote();
  }

  // Carrying something towards the edge takes the view with it.  Without
  // this, dragging a shape to where there is no room yet means letting go,
  // scrolling, picking it up again, and again -- when what you meant was
  // simply to put it further over.  The nearer the edge the mouse gets, the
  // faster the view follows, and it stops the moment you let go.
  var chaseOn = null;

  function chase(at, each) {
    var stage = el("#stage");
    if (!stage) { return; }
    var edge = stage.getBoundingClientRect();
    var REACH = 56, MOST = 22;           // how near, and how fast at most
    var dx = 0, dy = 0;
    if (at.x < edge.left + REACH) { dx = -(REACH - (at.x - edge.left)); }
    else if (at.x > edge.right - REACH) { dx = REACH - (edge.right - at.x); }
    if (at.y < edge.top + REACH) { dy = -(REACH - (at.y - edge.top)); }
    else if (at.y > edge.bottom - REACH) { dy = REACH - (edge.bottom - at.y); }
    dx = Math.max(-MOST, Math.min(MOST, dx / REACH * MOST));
    dy = Math.max(-MOST, Math.min(MOST, dy / REACH * MOST));
    if (!dx && !dy) { chaseStop(); return; }
    if (chaseOn) { chaseOn.dx = dx; chaseOn.dy = dy; chaseOn.each = each; return; }
    chaseOn = { dx: dx, dy: dy, going: true, each: each };
    (function keepUp() {
      if (!chaseOn || !chaseOn.going) { return; }
      // Locked, the view is moved by scrolling it.  Loose, there is no
      // scrolling to do, so the chart is moved the other way instead, which
      // comes to the same thing on screen.
      if (loose) { holdBy(-chaseOn.dx, -chaseOn.dy); }
      else {
        stage.scrollLeft += chaseOn.dx;
        stage.scrollTop += chaseOn.dy;
      }
      // the mouse is standing still while the view moves under it, so what
      // is being carried has to be worked out again each frame
      if (chaseOn.each) { chaseOn.each(); }
      requestAnimationFrame(keepUp);
    })();
  }

  function chaseStop() {
    if (chaseOn) { chaseOn.going = false; }
    chaseOn = null;
  }

  function joinDrag(svg) {               // drag from the handle to a shape
    svg.addEventListener("pointerdown", function (ev) {
      var knob = ev.target.closest && ev.target.closest(".knob");
      if (!knob) { return; }
      ev.preventDefault();
      ev.stopPropagation();
      var from = nodeById(+knob.dataset.i);
      if (!from) { return; }
      try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* mouse: fine */ }
      keepUndo();                        // joining two up can be stepped back
      // What is being drawn is an arrow, so it is drawn as one: a solid line
      // with a point on the end that follows the mouse.  A dotted thread gave
      // no sense of which way round the join was going to be.
      var band = document.createElementNS("http://www.w3.org/2000/svg", "g");
      band.setAttribute("class", "band");
      var wire = document.createElementNS("http://www.w3.org/2000/svg", "path");
      wire.setAttribute("class", "band-line");
      wire.setAttribute("fill", "none");
      var tip = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      tip.setAttribute("class", "band-tip");
      band.appendChild(wire);
      band.appendChild(tip);
      svg.appendChild(band);
      var box = svg.getBoundingClientRect();
      var scale = (box.width || W) / W;
      var at = { x: ev.clientX, y: ev.clientY };
      function reach() {
        box = svg.getBoundingClientRect();   // the view may have moved under us
        var toX = (at.x - box.left) / scale, toY = (at.y - box.top) / scale;
        wire.setAttribute("d", "M" + from.x + "," + from.y + "L" + toX + "," + toY);
        var dx = toX - from.x, dy = toY - from.y;
        var run = Math.hypot(dx, dy) || 1;
        var ux = dx / run, uy = dy / run;
        var back = 11, wide = 4.5;
        var cx = toX - ux * back, cy = toY - uy * back;
        tip.setAttribute("points",
          toX + "," + toY + " " +
          (cx - uy * wide) + "," + (cy + ux * wide) + " " +
          (cx + uy * wide) + "," + (cy - ux * wide));
        tip.style.display = run > back + 2 ? "" : "none";
      }
      function move(e) {
        at = { x: e.clientX, y: e.clientY };
        chase(at, reach);
        reach();
      }
      function drop(e) {
        chaseStop();
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", drop);
        band.remove();
        var went = Math.abs(e.clientX - ev.clientX) + Math.abs(e.clientY - ev.clientY);
        if (went < 5) {
          // Pressed and let go on the spot: take it as a click, and wait for
          // the shape it should go to rather than asking for a drag.
          picked = from.id;
          joining = true;
          drawHand();
          drawHandPanel();
          return;
        }
        var under = document.elementFromPoint(e.clientX, e.clientY);
        var g = under && under.closest ? under.closest(".node") : null;
        var dot = under && under.closest ? under.closest(".spot") : null;
        if (dot) { joinUp(from.id, +dot.dataset.i); return; }
        if (g) { joinUp(from.id, +g.dataset.i.slice(1)); return; }
        // Let go over nothing.  The shape you were drawing from stays the one
        // in hand, so you can simply try again rather than hunt for it.
        picked = from.id;
        drawHand();
        drawHandPanel();
      }
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", drop);
    });
  }

  // Moving a shape, and making one bigger or smaller.
  //
  // Picking one up and putting it down again has to be the same thing as
  // clicking it.  It was not: the first pixel of movement redrew the chart,
  // which threw away the very element the press had landed on, so the browser
  // had nothing left to raise a click against and the shape was never taken
  // up.  You could shove a shape about all day and never once select it.
  // So the press is remembered, the chart is left alone until the mouse has
  // really gone somewhere, and letting go without having moved counts as a
  // click -- which is what makes clicking a shape a second time work.
  var NUDGE = 4;                         // movement below this is a click

  function dragging(svg) {
    svg.addEventListener("pointerdown", function (ev) {
      if (ev.button) { return; }
      if (ev.target.closest &&
          (ev.target.closest(".knob") || ev.target.closest(".spot"))) { return; }
      var grip = ev.target.closest && ev.target.closest(".grip");
      var g = ev.target.closest && ev.target.closest(".node");
      if (!g && !grip) { return; }
      var node = nodeById(+(grip || g).dataset.i.toString().replace(/^h/, ""));
      if (!node) { return; }
      ev.preventDefault();
      var scale = (svg.getBoundingClientRect().width || W) / W;
      var fromX = ev.clientX, fromY = ev.clientY;
      var wasX = node.x, wasY = node.y, wasW = node.w, wasH = node.h;
      var least = ROOM[node.kind] || ROOM.rect;
      var stirred = false, waiting = false;
      // Taking hold of a shape takes it up, whether it then gets moved or
      // not.  It is only noted here; the chart is not redrawn until the
      // mouse has actually gone somewhere, because redrawing under a press
      // is what used to lose the press.
      // Follow this finger or pen wherever it goes, even off the shape and
      // off the chart, and keep the browser from scrolling the page with it.
      try { svg.setPointerCapture(ev.pointerId); } catch (e) { /* mouse: fine */ }
      var pickedBefore = picked;
      var noted = false;                 // a copy is kept the moment it moves
      if (g) { picked = node.id; chosen = null; }

      function paint() {
        if (waiting) { return; }
        waiting = true;
        requestAnimationFrame(function () { waiting = false; drawHand(); });
      }
      var stage = el("#stage");
      var wasLeft = stage ? stage.scrollLeft : 0;
      var wasDown = stage ? stage.scrollTop : 0;
      var wasHoldX = holdX, wasHoldY = holdY;
      var at = { x: ev.clientX, y: ev.clientY };

      function move(e) {
        at = { x: e.clientX, y: e.clientY };
        carry();
      }
      function carry() {
        // How far the view itself has travelled since the press, which the
        // shape has to make up if it is to stay under the mouse: scrolled
        // one way, or, on a loose chart, carried the other.
        var gone = ((stage ? stage.scrollLeft - wasLeft : 0)
                    - (holdX - wasHoldX)) / scale;
        var fell = ((stage ? stage.scrollTop - wasDown : 0)
                    - (holdY - wasHoldY)) / scale;
        var dx = (at.x - fromX) / scale + gone;
        var dy = (at.y - fromY) / scale + fell;
        if (!stirred && Math.abs(dx) < NUDGE && Math.abs(dy) < NUDGE) { return; }
        if (!noted) { noted = true; keepUndo(); }
        stirred = true;
        chase(at, carry);
        if (grip) {
          // The corner opposite the one being held stays where it is, so the
          // shape grows and shrinks from the corner in hand rather than from
          // its middle.  Working from that fixed corner keeps it exact even
          // when the size runs into its smallest.
          var toward = grip.dataset.corner || "se";
          var ax = toward.indexOf("e") >= 0 ? 1 : -1;
          var ay = toward.indexOf("s") >= 0 ? 1 : -1;
          var heldX = wasX - ax * wasW / 2;      // the corner that stays put
          var heldY = wasY - ay * wasH / 2;
          // Sizes go in steps of two quarters, so that half of them is a
          // whole quarter: that is what puts a shape's sides on the ruling
          // rather than only its middle.
          var STEP = HAND_GRID * 2;
          node.w = Math.max(least[0] * 0.5,
                            Math.round((wasW + ax * dx) / STEP) * STEP);
          node.h = Math.max(least[1] * 0.5,
                            Math.round((wasH + ay * dy) / STEP) * STEP);
          if (node.kind === "circle") { node.w = node.h = Math.max(node.w, node.h); }
          node.x = heldX + ax * node.w / 2;
          node.y = heldY + ay * node.h / 2;
          node.own = true;               // a size set by hand, so keep it
        } else {
          node.x = Math.round((wasX + dx) / HAND_GRID) * HAND_GRID;
          node.y = Math.round((wasY + dy) / HAND_GRID) * HAND_GRID;
          lineUp(node);                  // and settle onto anything it is near
        }
        paint();
      }
      function drop() {
        chaseStop();
        guides = [];                     // the red lines go with the holding
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", drop);
        if (!stirred && g) {
          // Clicking a shape that is already the one in hand starts typing
          // in it, the way it does everywhere else -- one press to take it
          // up, another to write in it.  A double-click still works too.
          var was = pickedBefore;
          var id = +g.dataset.i.slice(1);
          handClick(id);
          if (was === id) {
            var now = el('.node[data-i="h' + id + '"]', el("#chart"));
            if (now) { typeInto(now); }
          }
        }
        else { drawHand(); drawHandPanel(); }
      }
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", drop);
    });
  }

  // A chart wider than the room it has is shown at a size that fits.  On a
  // phone that is nearly always, and a chart with its sides cut off is no
  // use to anybody; on a wide screen it only happens to charts that really
  // are too big, which is exactly when it is wanted.
  function fitIfItMustBe() {
    var box = el("#stage");
    if (!chart || !box || !W || !H) { return; }
    var face = getComputedStyle(box);
    var across = box.clientWidth - parseFloat(face.paddingLeft)
                                 - parseFloat(face.paddingRight) - 14;
    var down = box.clientHeight - parseFloat(face.paddingTop)
                                - parseFloat(face.paddingBottom) - 14;
    if (across <= 0) { return; }
    if (W * zoom <= across && H * zoom <= down) { return; }   // it already fits
    // Fit whichever way is the tight one, so the whole chart is there to see.
    // On a screen short enough that fitting the height would shrink it past
    // reading, fit the width instead and let it be scrolled -- a chart too
    // small to read is no better than one with its foot cut off.
    var byWidth = across / W;
    var whole = Math.min(byWidth, down > 0 ? down / H : byWidth);
    zoom = Math.max(0.1, Math.min(4, whole < 0.3 ? byWidth : whole));
    show();
  }

  function show() {
    if (!chart) { return; }
    chart.style.width = (W * zoom).toFixed(0) + "px";
    chart.removeAttribute("height");
    el("#pct").textContent = Math.round(zoom * 100) + "%";
    holdClamp();                         // a bigger chart has less room to roam
  }
  // A step that would carry the zoom past actual size stops there instead.
  // Every zoom set by something other than these two buttons -- Fit, or a
  // chart shrunk on opening to the room it had -- leaves it on a number the
  // steps then never meet: from 77% they go 96%, 120%, 150%, and 100%, the
  // one place anybody is trying to get back to, is stepped straight over
  // every time.  So the step that crosses it lands on it, and the next one
  // carries on from there.
  function zoomLands(want) {
    var to = Math.min(8, Math.max(0.1, want));
    var already = Math.abs(zoom - 1) < 0.001;        // standing on it already
    if (!already && (zoom < 1) !== (to < 1)) { to = 1; }
    return to;
  }

  function step(by) {
    glideStop();
    zoom = zoomLands(zoom * by);
    show();
  }
  // Zooming about a point rather than about the middle: whatever is under
  // that spot on the screen is still under it afterwards.  That is what the
  // wheel wants -- you point at the bit you mean and lean in on it -- and
  // the middle would send it sliding off instead.
  //
  // Measured off the page, not worked out from the numbers, for the same
  // reason the camera below is: the chart may be held or loose, scrolled or
  // carried, and the two keep their position in different places.  Where it
  // is now is one question with one answer; putting it back takes a scroll
  // or a carry, and that is the only line that has to know which.
  function zoomAt(x, y, want) {
    var stage = el("#stage");
    if (!chart || !stage || !zoom) { return; }
    var r = chart.getBoundingClientRect();
    if (!r.width) { return; }
    var onX = (x - r.left) / zoom;       // the spot, in the chart's own numbers
    var onY = (y - r.top) / zoom;
    // A button pressed a moment ago leaves the width gliding to where it
    // was told to go.  Measuring against a width that is still on its way
    // would put the spot back wrong, and a wheel wants the size it asked
    // for at once in any case, so the glide comes off first.
    var paper = el("#sheet");
    if (paper) { paper.classList.remove("gliding"); }
    zoom = want;
    show();
    r = chart.getBoundingClientRect();   // it has only just changed size
    var dx = (r.left + onX * zoom) - x;
    var dy = (r.top + onY * zoom) - y;
    if (loose) { holdBy(-dx, -dy); }
    else { stage.scrollLeft += dx; stage.scrollTop += dy; }
  }

  el("#in").onclick = function () { step(1.25); };
  el("#out").onclick = function () { step(1 / 1.25); };
  el("#actual").onclick = function () { glideStop(); zoom = 1; show(); };
  el("#fit").onclick = function () {
    var box = el("#stage"), face = getComputedStyle(box);
    glideStop();
    var room = box.clientWidth - parseFloat(face.paddingLeft)
                               - parseFloat(face.paddingRight) - 14;
    zoom = Math.max(0.1, Math.min(4, room / W));
    show();
  };

  // ---------------------------------------------------------- the camera --
  // Following the program as it runs.  The view is carried to whatever shape
  // is being done and stood at a distance that suits it, so that watching a
  // program step is watching one thing at a time rather than hunting for the
  // glowing shape somewhere in a chart eight feet long.
  //
  // Everything here is done by measuring the page rather than by arithmetic
  // on the numbers that put it there.  The chart can be scrolled, dragged,
  // zoomed, redrawn or switched between held and loose by half a dozen other
  // things in this file, and each of those keeps its position somewhere
  // different; a camera that remembered its own would be wrong after any of
  // them.  Measured, there is only one thing to be right about.
  var glide = null;                      // the move in progress, if any

  // Where the middle of the stage is, in the chart's own numbers.
  function viewNow() {
    var stage = el("#stage");
    if (!chart || !stage || !zoom) { return null; }
    var r = chart.getBoundingClientRect(), s = stage.getBoundingClientRect();
    if (!r.width) { return null; }
    return { zoom: zoom,
             x: (s.left + stage.clientWidth / 2 - r.left) / zoom,
             y: (s.top + stage.clientHeight / 2 - r.top) / zoom };
  }

  // Put a point of the chart in the middle of the stage, at once.  Held,
  // that is the stage scrolling; loose, it is the chart being carried.  The
  // measurement is the same either way, which is the whole reason for doing
  // it this way round.
  function centreOn(x, y) {
    var stage = el("#stage");
    if (!chart || !stage) { return; }
    var r = chart.getBoundingClientRect(), s = stage.getBoundingClientRect();
    var dx = (r.left + x * zoom) - (s.left + stage.clientWidth / 2);
    var dy = (r.top + y * zoom) - (s.top + stage.clientHeight / 2);
    if (loose) { holdBy(-dx, -dy); }
    else { stage.scrollLeft += dx; stage.scrollTop += dy; }
  }

  function glideStop() {
    if (!glide) { return; }
    cancelAnimationFrame(glide.frame);
    clearTimeout(glide.last);
    glide = null;
  }

  // The move itself.  How close it stands and where it stands travel over
  // the same short moment, which is what makes it read as a camera rather
  // than as two things happening near each other.  Each frame sets the zoom
  // first and centres afterwards, because centring is measured off a chart
  // whose size has only just changed.
  function glideTo(x, y, want, ms) {
    var from = viewNow();
    if (!from) { return; }
    glideStop();
    want = Math.max(0.1, Math.min(8, want || from.zoom));
    if (STILL || !ms) {                  // told to keep still: simply be there
      zoom = want; show(); centreOn(x, y);
      return;
    }
    var mine = { frame: 0, last: 0 }, began = 0;
    glide = mine;
    function move(now) {
      if (glide !== mine) { return; }    // something else took the wheel
      if (!began) { began = now; }
      var t = Math.min(1, (now - began) / ms);
      var e = 1 - Math.pow(1 - t, 3);    // off quickly, settling at the end
      zoom = from.zoom + (want - from.zoom) * e;
      show();
      centreOn(from.x + (x - from.x) * e, from.y + (y - from.y) * e);
      if (t < 1) { mine.frame = requestAnimationFrame(move); }
      else { glideStop(); }
    }
    mine.frame = requestAnimationFrame(move);
    // Frames are only drawn for a window somebody can see.  Left behind
    // another one -- or on a tab in the background, which a slow run is a
    // fine reason to leave a page on -- the clock above never ticks at all,
    // and the camera would stop wherever it had got to and stay there for
    // the rest of the program.  So the end of the move is waited for on an
    // ordinary timer as well, and whichever arrives first finishes it.
    mine.last = setTimeout(function () {
      if (glide !== mine) { return; }
      glideStop();
      zoom = want;
      show();
      centreOn(x, y);
    }, ms + 60);
  }

  // How close to stand to one shape.  A fixed zoom would be wrong both ways:
  // a Start oval is a few dozen units across and wants going right in on,
  // while a Process carrying six lines of declarations is wider than some
  // whole charts and would end up with its sides off the screen.  So the
  // shape is given a share of the stage and the distance follows from that
  // -- which is what does the zooming in and out as the program moves
  // between its big steps and its small ones.
  //
  // The share is well under half on purpose.  Filling the stage with the one
  // shape would say what is being done and nothing about where it sits, and
  // where it sits -- what led into it, what waits under it -- is most of
  // what there is to learn from watching a chart run.
  var SHARE_X = 0.40, SHARE_Y = 0.32;    // of the stage, across and down
  var CLOSEST = 2.4, FURTHEST = 0.35;

  function followNode(node) {
    var stage = el("#stage"), box = null;
    if (!stage || !node || !node.getBBox) { return; }
    try { box = node.getBBox(); } catch (e) { return; }
    if (!box || !box.width || !box.height) { return; }
    var across = stage.clientWidth - 52, down = stage.clientHeight - 52;
    if (across < 40 || down < 40) { return; }
    var want = Math.min(across * SHARE_X / box.width,
                        down * SHARE_Y / box.height);
    glideTo(box.x + box.width / 2, box.y + box.height / 2,
            Math.max(FURTHEST, Math.min(CLOSEST, want)), 240);
  }

  // Where it was before the program took the wheel, so it can be given back
  // afterwards.  A run that ends leaving the chart somewhere in the middle
  // of itself at some zoom nobody chose is a run that has to be tidied up
  // after by hand, every time.
  var wasView = null;
  function keepView() { wasView = viewNow(); }
  function backToView() {
    var was = wasView;
    wasView = null;
    if (was) { glideTo(was.x, was.y, was.zoom, 300); }
  }

  // ------------------------------------- held in place, or loose upon it --
  // Two ways to have the chart, and a padlock to say which.
  //
  // Locked -- the way it has always been -- the chart sits in the stage and
  // scrolls inside it.  It cannot be put anywhere the stage is not, which is
  // exactly right for reading one: there is no way to lose it, and the bars
  // always say where in it you are.
  //
  // Loose, it is picked up and set down wherever it is dragged: shoved off
  // to one side to read what was under it, or carried out past the edge to
  // leave room in front of it.  Nothing scrolls then -- the chart is simply
  // moved, by a translation on the block that holds it -- so the stage's
  // bars are put away for as long as it lasts.
  //
  // The one rule is that it cannot be lost.  A chart dragged clean off the
  // stage would be gone for good: nothing left on screen to take hold of,
  // and no bar to bring it back with.  So every move is clamped to leave a
  // strip of it showing, and that strip is always enough to grab and drag
  // back with.
  var loose = false, holdX = 0, holdY = 0;
  var KEEP = 72;                         // how much has to stay in sight

  function holdApply() {
    var wrap = el("#stage .wrap");
    if (!wrap) { return; }
    wrap.style.setProperty("--hold-x", holdX.toFixed(1) + "px");
    wrap.style.setProperty("--hold-y", holdY.toFixed(1) + "px");
  }

  // Where the offset is allowed to be, given how big the chart is right now
  // and how much room the stage has.  Zooming in, drawing it again, turning
  // the phone on its side -- any of those can leave a position that was
  // legal no longer so, which is why this is asked again afterwards and not
  // only while something is being dragged.
  function holdRoom() {
    var stage = el("#stage"), paper = el("#sheet");
    if (!stage || !paper) { return null; }
    var edge = stage.getBoundingClientRect();
    var box = paper.getBoundingClientRect();
    var left = box.left - holdX;         // where it would sit at no offset
    var top = box.top - holdY;
    // A chart smaller than the strip cannot spare the whole strip, so what
    // it has to keep in sight is however much of it there is.
    var keepX = Math.min(KEEP, box.width), keepY = Math.min(KEEP, box.height);
    return {
      x: [edge.left + keepX - left - box.width, edge.right - keepX - left],
      y: [edge.top + keepY - top - box.height, edge.bottom - keepY - top]
    };
  }

  // The numbers go on the page before anything is measured off it.  Left
  // the other way round, what came back was the chart's old position paired
  // with its new offset, and the difference between the two -- a whole
  // drag's worth -- came off the room it was allowed: one good shove and
  // the chart went clean over the edge the strip was there to stop.
  function holdClamp() {
    if (!loose) { return; }
    holdApply();
    var room = holdRoom();
    if (!room) { return; }
    var x = Math.max(room.x[0], Math.min(room.x[1], holdX));
    var y = Math.max(room.y[0], Math.min(room.y[1], holdY));
    if (x === holdX && y === holdY) { return; }
    holdX = x;
    holdY = y;
    holdApply();
  }

  function holdBy(dx, dy) {
    holdX += dx;
    holdY += dy;
    holdClamp();
  }

  // Switching either way leaves the chart looking exactly where it was.
  // Unlocking hands the scroll over to the offset; locking hands it back,
  // as far as the stage can take it -- which is what makes the padlock a
  // padlock rather than a button that jumps the chart about.
  function setLoose(want) {
    var stage = el("#stage");
    loose = !!want;
    if (loose) {
      holdX = stage ? -stage.scrollLeft : 0;
      holdY = stage ? -stage.scrollTop : 0;
      document.body.classList.add("chart-loose");
      if (stage) { stage.scrollLeft = stage.scrollTop = 0; }
      holdClamp();
    } else {
      var wasX = holdX, wasY = holdY;
      holdX = holdY = 0;
      holdApply();
      document.body.classList.remove("chart-loose");
      if (stage) { stage.scrollLeft = -wasX; stage.scrollTop = -wasY; }
    }
    el("#hold-lock").classList.toggle("on", !loose);
    el("#hold-loose").classList.toggle("on", loose);
    try { localStorage.setItem("flowchart-hold", loose ? "loose" : "locked"); }
    catch (e) { /* storage turned off: it just starts locked next time */ }
  }

  el("#hold-lock").onclick = function () { setLoose(false); };
  el("#hold-loose").onclick = function () { setLoose(true); };

  // Carrying the chart about while it is loose.  Pointer events rather than
  // mouse ones, so a finger works too: loose, the stage does no scrolling of
  // its own, so a touch has nothing else left to drag.
  (function () {
    var stage = el("#stage");
    if (!stage) { return; }
    stage.addEventListener("pointerdown", function (ev) {
      if (!loose || ev.button) { return; }
      // A shape being moved is not the chart being moved.
      if (ev.target.closest &&
          ev.target.closest(".node, .knob, .spot, .grip")) { return; }
      var fromX = ev.clientX, fromY = ev.clientY;
      var wasX = holdX, wasY = holdY;
      glideStop();                       // a hand on it beats a camera
      try { stage.setPointerCapture(ev.pointerId); } catch (e) { /* mouse: fine */ }
      stage.classList.add("grabbing");
      function move(e) {
        holdX = wasX + (e.clientX - fromX);
        holdY = wasY + (e.clientY - fromY);
        holdClamp();
      }
      function drop() {
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", drop);
        stage.classList.remove("grabbing");
      }
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", drop);
    });
    // The wheel, which does one of two things over the chart.
    //
    // Held down with Ctrl it zooms, in on the spot it is pointing at -- the
    // way a wheel zooms anything you can zoom, and the way a trackpad's
    // pinch arrives here too, since a browser sends that as a Ctrl wheel.
    // The page's own Ctrl-zoom is turned away for the chart alone; anywhere
    // else on the page it still works as it always did.
    //
    // On its own it scrolls -- except that loose there is no scrolling left
    // to do, so it carries the chart instead, or the mode would feel broken.
    // A wheel that counts in lines or pages rather than pixels is asking
    // for about this much of each.
    var CLICK = 1.0015;                  // what a notch of wheel is worth
    stage.addEventListener("wheel", function (ev) {
      var by = ev.deltaMode === 1 ? 16 : (ev.deltaMode === 2 ? 320 : 1);
      if (ev.ctrlKey || ev.metaKey) {
        ev.preventDefault();
        glideStop();
        var want = zoomLands(zoom * Math.pow(CLICK, -ev.deltaY * by));
        if (want !== zoom) { zoomAt(ev.clientX, ev.clientY, want); }
        return;
      }
      if (!loose) { return; }
      ev.preventDefault();
      glideStop();
      holdBy(-ev.deltaX * by, -ev.deltaY * by);
    }, { passive: false });
  })();
  // ------------------------------------------------------------- panel --
  // Two sides to it -- the chart, and how it looks -- so that neither is a
  // long scroll, and a way to shut the whole thing when the chart is what
  // you want to look at.  What was open last time is how it opens.
  var side = "chart", shut = false;
  function showSide(which) {
    side = which;
    if (!el("#modes")) { which = side = "colors"; }   // nothing to build here
    el("#side-chart").classList.toggle("on", which === "chart");
    el("#side-colors").classList.toggle("on", which === "colors");
    el("#side-chart-panel").hidden = which !== "chart";
    el("#side-colors-panel").hidden = which === "chart";
    el("#rail-chart").classList.toggle("on", which === "chart");
    el("#rail-colors").classList.toggle("on", which === "colors");
    try { localStorage.setItem("flowchart-side", which); } catch (e) { /* fine */ }
  }
  // On a screen too narrow to hold both, the panel lies over the chart and
  // this sits between them: tapping it puts the panel away, which is what
  // anyone who has used a drawer expects and is far easier to hit than a
  // small chevron.  On a wide screen it is never shown.
  function veil() {
    var there = el(".veil");
    if (there) { return there; }
    var sheet = document.createElement("div");
    sheet.className = "veil";
    sheet.addEventListener("pointerdown", function () { showPanel(false); });
    var room = el("main");
    if (room) { room.appendChild(sheet); }
    return sheet;
  }

  // Is the panel lying over the chart rather than sitting beside it?  On a
  // screen that narrow it hides the thing it was used to make, so anything
  // that produces a chart puts it away afterwards.
  function panelIsOver() {
    try { return matchMedia("(max-width: 899px)").matches; }
    catch (e) { return false; }
  }

  function showPanel(open) {
    veil();
    shut = !open;
    el("#panel").classList.toggle("hide", shut);
    el("#rail").hidden = !shut;
    document.body.classList.toggle("drawer", !shut);   // room beside it on a
    document.body.classList.toggle("railed", shut);    //   narrow screen
    try { localStorage.setItem("flowchart-panel", shut ? "shut" : "open"); }
    catch (e) { /* fine */ }
  }
  el("#side-chart").onclick = function () { showSide("chart"); };
  el("#side-colors").onclick = function () { showSide("colors"); };
  el("#collapse").onclick = function () { showPanel(false); };
  // The panel is put away with the chevron on it and brought back with the
  // rail that takes its place, so there is no third button for it in the bar.
  el("#rail-chart").onclick = function () { showSide("chart"); showPanel(true); };
  el("#rail-colors").onclick = function () { showSide("colors"); showPanel(true); };

  // every named section folds away, and stays folded
  var folded = {};
  try { folded = JSON.parse(localStorage.getItem("flowchart-folded")) || {}; }
  catch (e) { folded = {}; }
  all("#side-colors-panel section.card").forEach(function (card, i) {
    var head = el("h2", card);
    if (!head) { return; }
    card.classList.add("fold");
    var name = "s" + i;
    if (folded[name]) { card.classList.add("shut"); }
    head.onclick = function () {
      card.classList.toggle("shut");
      folded[name] = card.classList.contains("shut");
      try { localStorage.setItem("flowchart-folded", JSON.stringify(folded)); }
      catch (e) { /* fine */ }
    };
  });

  // Drag to move about -- which, locked, means scrolling the stage under a
  // chart that stays put.  Loose, the chart is what moves instead, and
  // 06-chart.js has that; there is nothing to scroll then, so this stands
  // aside rather than the two of them pulling at the same press.
  (function () {
    var stage = el("#stage"), from = null;
    stage.addEventListener("mousedown", function (ev) {
      if (loose) { return; }
      if (ev.target.closest && ev.target.closest(".node")) { return; }
      from = { x: ev.clientX, y: ev.clientY, l: stage.scrollLeft, t: stage.scrollTop };
      stage.classList.add("grabbing");
    });
    window.addEventListener("mousemove", function (ev) {
      if (!from) { return; }
      stage.scrollLeft = from.l - (ev.clientX - from.x);
      stage.scrollTop = from.t - (ev.clientY - from.y);
    });
    window.addEventListener("mouseup", function () {
      from = null; stage.classList.remove("grabbing");
    });
  })();

  // ------------------------------------------------------------ saving it --
  function plain(scale) {
    var copy = chart.cloneNode(true);
    copy.removeAttribute("style");
    copy.removeAttribute("id");
    all(".node.on", copy).forEach(function (g) { g.classList.remove("on"); });
    copy.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    copy.setAttribute("width", Math.round(W * (scale || 1)));
    copy.setAttribute("height", Math.round(H * (scale || 1)));
    return '<?xml version="1.0" encoding="UTF-8"?>\n' +
           new XMLSerializer().serializeToString(copy);
  }
  var svgUrl = null;
  function linkSvg() {
    if (svgUrl) { URL.revokeObjectURL(svgUrl); }
    svgUrl = URL.createObjectURL(
        new Blob([plain(1)], { type: "image/svg+xml;charset=utf-8" }));
    el("#svg-link").href = svgUrl;
  }
  el("#svg-link").addEventListener("click", linkSvg);   // always the latest

  function save(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 20000);
  }

  var MAX_SIDE = 16000, MAX_AREA = 120e6;
  function capped(want) {
    return Math.max(0.25, Math.min(want, MAX_SIDE / W, MAX_SIDE / H,
                                   Math.sqrt(MAX_AREA / (W * H))));
  }
  // Grouped the way the page's own language groups its numbers, not the
  // way the browser happens to: a German page saying 4.664 and an
  // English one saying 4,664 is the point of it having a language.
  function px(n) {
    n = Math.round(n);
    try { return n.toLocaleString(LANG); }
    catch (e) { return n.toLocaleString(); }
  }
  var scaleSel = el("#scale"), note = el("#note");

  // ------------------------------------------------------ how big the PNG --
  // The sizes on offer are settled in Python, which knows what they are;
  // what they come to is settled here, which is the only place that knows
  // what the chart is.  A multiplier on its own says nothing -- four times
  // what? -- and the answer changes every time the chart is drawn again, so
  // the list is written out afresh whenever that happens.
  //
  // A size this browser cannot hold is greyed rather than dropped or
  // quietly saved smaller.  Dropping it leaves no sign of why the biggest
  // sizes are missing from a big chart; saving it smaller means the PNG is
  // not the size that was asked for, which was only ever explained after
  // the fact, by which time the file had already been written.
  var SIZES = [];                        // the values, as Python listed them
  all("option", scaleSel).forEach(function (o) { SIZES.push(o.value); });

  function sizeLabel(value, over) {
    var frame = /^(\d+)x(\d+)$/.exec(value);
    if (frame) { return px(+frame[1]) + " × " + px(+frame[2]); }
    var n = parseFloat(value);
    return n + "× · " + (over ? TXT.png_over
                              : px(W * n) + " × " + px(H * n));
  }

  function sizeList() {
    if (!scaleSel || !W || !H) { return; }
    var was = scaleSel.value, keep = "", biggest = "", anyOf = "";
    var scales = document.createElement("optgroup");
    var frames = document.createElement("optgroup");
    scales.label = TXT.dl_scale;
    frames.label = TXT.dl_frame;
    SIZES.forEach(function (value) {
      var frame = /^\d+x\d+$/.test(value);
      var over = !frame && capped(parseFloat(value)) < parseFloat(value) - 0.005;
      var o = document.createElement("option");
      o.value = value;
      o.textContent = sizeLabel(value, over);
      o.disabled = over;
      if (!over) {
        anyOf = anyOf || value;
        if (!frame) { biggest = value; }
        if (value === was) { keep = value; }
      }
      (frame ? frames : scales).appendChild(o);
    });
    scaleSel.textContent = "";
    if (scales.firstChild) { scaleSel.appendChild(scales); }
    if (frames.firstChild) { scaleSel.appendChild(frames); }
    // A chart redrawn bigger can put what was chosen out of reach.  The
    // biggest that still works is the nearest thing to what was meant; a
    // box left showing a size it will not save at is not.
    scaleSel.value = keep || biggest || anyOf;
    sizeNote();
  }
  function plan() {
    var frame = /^(\d+)x(\d+)$/.exec(scaleSel.value);
    if (frame) {
      var fw = +frame[1], fh = +frame[2], s = Math.min(fw / W, fh / H);
      var dw = Math.round(W * s), dh = Math.round(H * s);
      return { cw: fw, ch: fh, dx: Math.round((fw - dw) / 2),
               dy: Math.round((fh - dh) / 2), dw: dw, dh: dh, scale: s, want: s };
    }
    var want = parseFloat(scaleSel.value), got = capped(want);
    var w = Math.round(W * got), h = Math.round(H * got);
    return { cw: w, ch: h, dx: 0, dy: 0, dw: w, dh: h, scale: got, want: want };
  }
  // The sizes are in the list now, so the tooltip is left to say what the
  // control is for -- it used to be overwritten with the pixel count, which
  // both said it where nobody looks and threw away the wording that the
  // language picker puts back.
  function sizeNote() {
    var p = plan();
    note.textContent = (p.scale < p.want - 0.05)
      ? say("png_capped", { want: p.want, got: Math.round(p.scale * 10) / 10,
                            w: px(p.cw), h: px(p.ch) })
      : "";
  }
  scaleSel.onchange = sizeNote;

  var button = el("#png");
  button.onclick = function () {
    var p = plan();
    button.disabled = true;
    button.textContent = TXT.rendering;
    function done() { button.disabled = false; button.textContent = TXT.dl_png; }
    var url = URL.createObjectURL(
        new Blob([plain(p.scale)], { type: "image/svg+xml;charset=utf-8" }));
    var img = new Image();
    img.onload = function () {
      var canvas = document.createElement("canvas");
      canvas.width = p.cw;
      canvas.height = p.ch;
      var pen = canvas.getContext("2d");
      pen.fillStyle = style.sheet || "#ffffff";
      pen.fillRect(0, 0, canvas.width, canvas.height);
      pen.drawImage(img, p.dx, p.dy, p.dw, p.dh);
      URL.revokeObjectURL(url);
      done();
      canvas.toBlob(function (blob) {
        if (blob) { save(blob, FILE + ".png"); }
        else {
          note.className = "grow bad";
          note.textContent = TXT.png_big;
        }
      }, "image/png");
    };
    img.onerror = function () {
      URL.revokeObjectURL(url);
      done();
      note.className = "grow bad";
      note.textContent = TXT.png_fail;
    };
    img.src = url;
  };

  // Delete and Escape used to be answered here as well as in the keyboard
  // part.  Two handlers for one key is one handler too many: this one ran
  // first, did the deleting itself, and left nothing for the other to undo,
  // so Ctrl+Z after a Delete quietly did nothing.  The keys all live in one
  // place now.

  if (el("#run")) {
    el("#run").onclick = runIt;
    el("#see-code").onclick = function (ev) {
      ev.stopPropagation();              // or the same click shuts the menu
      askWhichCode(el("#see-code"));
    };
  }
  if (el("#save-file")) {
    el("#save-file").onclick = saveProject;
    el("#open-file").onclick = function () { el("#file-in").click(); };
    el("#file-in").onchange = function () {
      var one = el("#file-in").files[0];
      if (!one) { return; }
      var reader = new FileReader();
      reader.onload = function () { openProject(String(reader.result)); };
      reader.readAsText(one);
      el("#file-in").value = "";
    };
  }

  el("#reset").onclick = function () {
    style = { sheet: "", ink: "", words: "", grid: "", gridOff: !el("#grid-on").checked,
              kinds: {}, nodes: {} };
    all(".preset").forEach(function (x) { x.classList.remove("on"); });
    paint(); buildKinds(); buildGlobals(); drawSelection();
  };
  // Two switches, one thing: the one on the chart card and the one in the
  // colours are the same question asked in two places, so they answer
  // together.  Hiding the ruling that is already drawn works in either mode
  // and does not need the chart made again.
  function showTheGrid(on) {
    style.gridOff = !on;
    if (el("#grid-on")) { el("#grid-on").checked = on; }
    if (el("#f-grid")) { el("#f-grid").checked = on; }
    paint();
    keep();
  }
  if (el("#f-grid")) {
    el("#f-grid").onchange = function () { showTheGrid(el("#f-grid").checked); };
  }
  if (el("#f-legend")) {
    // By hand the key is drawn here and there, so the chart is simply drawn
    // again.  From pseudocode it is a setting the drawing is made with, so it
    // takes effect the next time the chart is built.
    el("#f-legend").onchange = function () {
      if (byHand) { drawHand(); }
    };
  }
  el("#grid-on").onchange = function () {
    style.gridOff = !el("#grid-on").checked;
    if (el("#f-grid")) { el("#f-grid").checked = el("#grid-on").checked; }
    paint();
  };

  // ------------------------------------------------------ the studio part --
  // Python, in the browser.  The website version has no server to ask, so
  // it loads Python itself and imports the very same builder.  One set of
  // rules for how a chart is drawn, wherever it is being drawn.
  var python = null;
  function startPython() {
    if (python) { return python; }
    var says = el("#build-note");
    if (says) { says.className = ""; says.textContent = TXT.starting; }
    python = new Promise(function (ready, nope) {
      var tag = document.createElement("script");
      tag.src = PYODIDE + "pyodide.js";
      tag.onload = ready;
      tag.onerror = function () { nope(new Error("pyodide.js")); };
      document.head.appendChild(tag);
    }).then(function () {
      return loadPyodide({ indexURL: PYODIDE });
    }).then(function (py) {
      return fetch(MODULE).then(function (r) { return r.text(); })
        .then(function (src) {
          py.FS.writeFile(MODULE, src);
          py.runPython([
            "import sys, json",
            "sys.path.insert(0, '.')",
            "import " + MODULE.replace(/\.py$/, "") + " as fb",
            "def draw_json(ask):",
            "    try:",
            "        return json.dumps(fb.draw_for_studio(json.loads(ask)))",
            "    except Exception as exc:",
            "        return json.dumps({'ok': False, 'error': str(exc)})"
          ].join("\n"));
          if (says) { says.textContent = TXT.ready; }
          return py;
        });
    }).catch(function (err) {
      python = null;
      if (says) {
        says.className = "bad";
        says.textContent = say("boot_failed", { err: err.message || err });
      }
      throw err;
    });
    return python;
  }

  function askFor(ask) {                 // a drawing, however this page gets one
    if (MODE === "web") {
      return startPython().then(function (py) {
        var fn = py.globals.get("draw_json");
        var out = JSON.parse(fn(JSON.stringify(ask)));
        fn.destroy();
        return out;
      });
    }
    return fetch("build", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ask)
    }).then(function (r) { return r.json(); });
  }

  function drawRoles() {                 // which shape draws which kind
    var box = el("#role-rows");
    if (!box) { return; }
    box.innerHTML = "";
    ROLES.forEach(function (role) {
      var row = document.createElement("div");
      row.className = "row";
      row.innerHTML = keyMark(geom[role] || role) +
                      '<span class="name">' + (TXT["key_" + role] || role) + "</span>";
      var pick = document.createElement("select");
      pick.className = "field";
      pick.style.cssText = "width:auto; padding:4px 6px";
      SHAPE_LIST.forEach(function (kind) {
        var choice = document.createElement("option");
        choice.value = kind;
        choice.textContent = kindName(kind);
        if ((geom[role] || role) === kind) { choice.selected = true; }
        pick.appendChild(choice);
      });
      pick.onchange = function () {
        geom[role] = pick.value;
        drawRoles();
        if (el("#code").value.trim()) { el("#build").click(); }
      };
      row.appendChild(pick);
      box.appendChild(row);
    });
  }

  var tongue = el("#f-lang");
  if (tongue) {
    tongue.onchange = function () {
      LANG = tongue.value;
      if (ALL[LANG]) {                   // the page can change its own words
        TXT = ALL[LANG];
        dress();
        buildPresets(); buildGlobals(); buildKinds(); drawSelection(); sizeList();
        if (el("#code").value.trim()) { el("#build").click(); }
      } else {
        location.search = "?lang=" + LANG;
      }
    };
  }
  var build = el("#build");
  if (build) {
    build.onclick = function () {
      var says = el("#build-note");
      // The button says what it is doing by what colour it is: red while it
      // is drawing, green the moment it is done, then back to blue a second
      // later, ready for the next one.
      build.disabled = true;
      build.classList.remove("done");
      build.classList.add("working");
      // A chart of a few lines is drawn faster than the eye can follow, and a
      // colour that comes and goes inside a frame may as well not have been
      // there.  The red is held long enough to be seen, and everything that
      // follows waits its turn.
      var began = Date.now();
      function afterTheRed(go) {
        var left = 320 - (Date.now() - began);
        if (left > 0) { setTimeout(go, left); } else { go(); }
      }
      says.className = "";
      says.textContent = TXT.drawing;
      remember();
      askFor({
        text: el("#code").value,
        title: el("#f-title").value,
        author: el("#f-author").value,
        shape: el("#f-shape").value,
        seed: "",                      // a fresh one each time, unasked for
        lang: tongue ? tongue.value : "",
        legend: el("#f-legend").checked,
        grid: el("#f-grid").checked,
        shapes: geom
      }).then(function (data) {
        afterTheRed(function () {
          build.disabled = false;
          build.classList.remove("working");
          if (!data.ok) { return; }
          build.classList.add("done");
          setTimeout(function () { build.classList.remove("done"); }, 1300);
        });
        if (!data.ok) {
          says.className = "bad";
          says.textContent = data.error || TXT.failed;
          return;
        }
        el("#sheet").innerHTML = data.svg;
        // On a narrow screen the panel is lying over the chart, so it is put
        // away: you pressed the button to see a chart, not to keep looking at
        // the button.  On a wide screen it stays where it is.
        if (panelIsOver()) { showPanel(false); }
        setTimeout(fitIfItMustBe, 0);    // never show it with its sides cut off
        FILE = data.name || FILE;
        el("#svg-link").download = FILE + ".svg";
        document.title = data.title || FILE;
        el(".brand").firstChild.textContent = data.title || FILE;
        el("#sub").textContent = TXT.flowchart + " · " + data.w + " x " +
                                 data.h + " px";
        AST = data.ast || null;
        lineOf = {};
        if (AST) {
          noteLines(AST.main);
          (AST.modules || []).forEach(function (mod) { noteLines(mod.body); });
        }
        freshTape();               // a new program: nothing of the old one
        bind();
        paint();
        // Nothing is said when it works.  The button goes green and the chart
        // appears, which is two ways of saying it already; a line of text
        // underneath saying it a third time is just something else to read.
        // What goes wrong is still said, because nothing else says that.
        says.textContent = "";
      }).catch(function (err) {
        afterTheRed(function () {
          build.disabled = false;
          build.classList.remove("working");
        });
        says.className = "bad";
        says.textContent = say("not_answering", { err: err });
      });
    };
  }


  // =========================================================== by hand ==
  // Shapes you put where you want them, joined up by hand, and a check that
  // says whether what you have drawn is a flowchart that actually runs:
  // one place it starts, nothing stranded, nothing that can only be left by
  // stopping dead, and an End reachable from everywhere.  The drawing is
  // the same SVG the script writes, so the colours, the downloads and the
  // grid all work on it exactly as they do on a chart built from code.
  var hand = { nodes: [], links: [], next: 1, nextLink: 0 };
  // The paper behind a by-hand chart is ruled every 20, with a heavier line
  // every fifth.  Shapes settle on quarters of that: fine enough to place
  // something just so, coarse enough that things line up with each other
  // without being fiddled into place.
  var HAND_RULE = 20;                    // what is drawn
  var HAND_GRID = HAND_RULE / 4;         // what shapes settle on
  var picked = null, chosen = null, joining = false;

  // Lining things up.  While a shape is being carried, its middle is watched
  // against the middle of every other shape; come within reach of one and it
  // settles onto it exactly and a red line is drawn through both, so you can
  // see what you have lined it up with.  Red because it has to show against
  // white paper and dark paper and against every colour a shape can be
  // painted -- it is not part of the chart, it is only there while you hold
  // the shape, and it should look like it.
  var GUIDE_REACH = 7;                   // how near counts as lined up
  var guides = [];                       // [vertical?, where, from, to]

  function lineUp(node) {
    guides = [];
    var about = turned(node);
    hand.nodes.forEach(function (other) {
      if (other.id === node.id) { return; }
      var its = turned(other);
      if (Math.abs(node.x - other.x) <= GUIDE_REACH) {
        node.x = other.x;
        guides.push([true, other.x,
                     Math.min(node.y - about.h / 2, its.y - its.h / 2) - 14,
                     Math.max(node.y + about.h / 2, its.y + its.h / 2) + 14]);
      }
      if (Math.abs(node.y - other.y) <= GUIDE_REACH) {
        node.y = other.y;
        guides.push([false, other.y,
                     Math.min(node.x - about.w / 2, its.x - its.w / 2) - 14,
                     Math.max(node.x + about.w / 2, its.x + its.w / 2) + 14]);
      }
    });
  }
  // How small a shape is allowed to get before the words stop fitting.  These
  // are also the sizes a shape arrives at, and they are set to what is
  // comfortable to read and to take hold of with the mouse rather than to the
  // least the words need -- a shape you have to squint at is no use.
  var ROOM = { oval: [128, 50], rect: [170, 58], roundrect: [170, 58],
               io: [182, 58], io_back: [182, 58], diamond: [190, 84],
               hex: [182, 62], sub: [170, 58], trap: [182, 58],
               manual: [176, 62], doc: [176, 64], docs: [180, 70],
               note: [176, 62], card: [176, 62], loop: [176, 62],
               store: [170, 72], stored: [176, 62], delay: [170, 58],
               screen: [188, 58], circle: [72, 72], offpage: [170, 70],
               parallel: [170, 64], cloud: [186, 76], arrow: [192, 58],
               text: [120, 34], actor: [110, 96], callout: [180, 76],
               cube: [176, 68], step: [190, 58], table: [180, 76] };

  // Where the words sit in a shape, as a share of its height.  Most shapes
  // are happy with their middle; some have something in the way of it -- the
  // lip on a drum, the point on an off-page marker, the wave at the foot of
  // a page -- so the words step aside rather than sit across it.
  var WORD_SHIFT = { store: 0.09, stored: 0.07, offpage: -0.12, doc: -0.06,
                     docs: -0.05, manual: 0.07, card: 0.06, note: 0.04,
                     actor: 0.34, callout: -0.1, cube: 0.06, table: 0.14 };

  var HAND_TYPE = 12.5;                  // the words on a shape
  var HAND_LINE = 15;                    // and the step from line to line

  function handKinds() {                 // the whole catalogue, by name
    return SHAPE_LIST.map(function (kind) {
      return [kind, TXT["n_" + kind] || kind];
    });
  }
  function kindName(kind) {
    return TXT["n_" + kind] || TXT["key_" + kind] || kind;
  }
  function nodeById(id) {
    return hand.nodes.filter(function (n) { return n.id === id; })[0] || null;
  }
  function outOf(id) {
    return hand.links.filter(function (l) { return l.from === id; });
  }
  function intoOf(id) {
    return hand.links.filter(function (l) { return l.to === id; });
  }

  function measure(node, force) {         // how big the words make it
    if (node.own && !force) { return; }   // unless a size was set by hand
    var lines = String(node.text || " ").split("\n");
    var pen = measure.pen || (measure.pen = document.createElement("canvas")
                              .getContext("2d"));
    pen.font = HAND_TYPE + "px Arial, Helvetica, sans-serif";
    var wide = 0;
    lines.forEach(function (line) { wide = Math.max(wide, pen.measureText(line).width); });
    var room = ROOM[node.kind] || ROOM.rect;
    var STEP = HAND_GRID * 2;          // so half of it is a whole quarter
    node.w = Math.max(room[0], Math.round(wide) + (node.kind === "diamond" ? 84 : 40));
    node.h = Math.max(room[1], lines.length * HAND_LINE +
                               (node.kind === "diamond" ? 38 : 24));
    node.w = Math.ceil(node.w / STEP) * STEP;
    node.h = Math.ceil(node.h / STEP) * STEP;
    if (node.kind === "circle") { node.w = node.h = Math.max(node.w, node.h); }
    node.own = false;
  }

  function shapeSvg(n) {                 // full size, on the paper
    return shapeArt(n.kind, n.x, n.y, n.w, n.h, "#ffffff");
  }

  // --------------------------------------------------------- joining two up --
  // A line used to leave whichever side happened to face the other shape and
  // then get itself there however it could.  That picked the side before it
  // knew what the side would cost, so a line would come out of one face, turn
  // three times getting back round, and think nothing of going straight
  // through whatever else was standing in the way.
  //
  // So: all four sides of each shape are tried, the few square-cornered ways
  // of joining each pair are laid out, and the cheapest is drawn -- where
  // cheap means through nothing, then few turns, then short.  On the ordinary
  // case, one shape under another, that is still the plain straight line down.
  var STAND = 16;                         // how far a line stands off a shape

  // Where a line should actually touch a shape.  Every shape is measured by
  // the box around it, but most of them do not fill that box: a parallelogram
  // leans away from it at the sides, a typed-in box slopes away at the top, a
  // page waves away at the foot.  Meeting the box instead of the shape leaves
  // the arrow stopping in mid-air beside the thing it is pointing at, which
  // is what made it look as though a parallelogram had no sides to come out
  // of.  So each side is brought in to where the outline really is.
  // Turning a shape a quarter turn swaps what is its width and what is its
  // height, as far as anything outside the drawing is concerned: where its
  // sides are, where an arrow should meet it, where its corners are to take
  // hold of.  The drawing itself is turned with a transform, so this is the
  // one place that has to know.
  function turned(n) {
    var quarter = Math.round(((n.turn || 0) % 360) / 90) % 4;
    var over = quarter === 1 || quarter === 3;
    return { kind: n.kind, id: n.id, x: n.x, y: n.y,
             w: over ? n.h : n.w, h: over ? n.w : n.h, sideways: over };
  }

  function ports(node) {
    var n = turned(node);
    var w = n.w, h = n.h, x = n.x, y = n.y;
    var l = x - w / 2, r = x + w / 2, t = y - h / 2, b = y + h / 2;
    var lean = Math.min(12, (n.sideways ? h : w) / 4);
    var top = t, foot = b, left = l, right = r;
    // Sideways, the sides of the shape are its top and foot, so the little
    // corrections belong to the other pair.
    switch (n.sideways ? "" : n.kind) {
      case "io": case "io_back": case "trap":
        left = l + lean / 2; right = r - lean / 2; break;
      case "manual":
        top = t + Math.min(11, h * 0.28) / 2; break;
      case "doc":
        foot = b - Math.min(10, h * 0.18) * 0.2; break;
      case "docs":
        foot = b - Math.min(5, h * 0.12) * 0.4; break;
      case "screen":
        left = l + Math.min(16, w * 0.16) / 4; break;
      case "arrow":
        top = t + h * 0.26; foot = b - h * 0.26; break;
      case "step":                      // the point and the notch are the sides
        left = l + Math.min(22, w * 0.16); right = r - Math.min(22, w * 0.16);
        break;
      case "cube":
        top = t + Math.min(14, h * 0.26, w * 0.14);
        left = l; foot = b; break;
      case "callout":
        foot = b - Math.min(16, h * 0.28); break;
      case "actor":                     // the head is all there is up top
        break;
      case "offpage":
        break;                          // the point is at the middle anyway
      case "cloud":
        break;                          // drawn to touch its box at each side
      default: break;                   // box and outline agree
    }
    return [{ x: x, y: top, dx: 0, dy: -1 },
            { x: x, y: foot, dx: 0, dy: 1 },
            { x: left, y: y, dx: -1, dy: 0 },
            { x: right, y: y, dx: 1, dy: 0 }];
  }

  function tidy(pts) {                    // drop repeats and straight-throughs
    var out = [];
    pts.forEach(function (p) {
      var last = out[out.length - 1];
      if (!last || Math.abs(last[0] - p[0]) > 0.5 || Math.abs(last[1] - p[1]) > 0.5) {
        out.push([p[0], p[1]]);
      }
    });
    for (var i = out.length - 2; i > 0; i--) {
      var a = out[i - 1], b = out[i], c = out[i + 1];
      if ((Math.abs(a[0] - b[0]) < 0.5 && Math.abs(b[0] - c[0]) < 0.5) ||
          (Math.abs(a[1] - b[1]) < 0.5 && Math.abs(b[1] - c[1]) < 0.5)) {
        out.splice(i, 1);
      }
    }
    return out;
  }

  // Out of one side and into the other.  Where both sides face the same way
  // the two runs are joined by a cross lane, which is halfway by default --
  // handing in a lane is what lets a blocked line go round instead.
  function joinPorts(p, q, lane) {
    var a = [p.x + p.dx * STAND, p.y + p.dy * STAND];
    var b = [q.x + q.dx * STAND, q.y + q.dy * STAND];
    var pts = [[p.x, p.y], a];
    if (p.dx === 0 && q.dx === 0) {                 // both up or down
      if (Math.abs(a[0] - b[0]) > 1 || lane != null) {
        var mid = lane == null ? (a[1] + b[1]) / 2 : lane;
        pts.push([a[0], mid], [b[0], mid]);
      }
    } else if (p.dy === 0 && q.dy === 0) {          // both sideways
      if (Math.abs(a[1] - b[1]) > 1 || lane != null) {
        var midx = lane == null ? (a[0] + b[0]) / 2 : lane;
        pts.push([midx, a[1]], [midx, b[1]]);
      }
    } else if (p.dx === 0) {                        // one of each
      pts.push([a[0], b[1]]);
    } else {
      pts.push([b[0], a[1]]);
    }
    pts.push(b, [q.x, q.y]);
    return tidy(pts);
  }

  function cutsThrough(pts, node, from, to) {   // does any leg cross this shape
    var n = turned(node);
    var x0 = n.x - n.w / 2 + 1, x1 = n.x + n.w / 2 - 1;
    var y0 = n.y - n.h / 2 + 1, y1 = n.y + n.h / 2 - 1;
    var first = from == null ? 1 : from;
    var last = to == null ? pts.length - 1 : to;
    for (var i = first; i <= last; i++) {
      var ax = Math.min(pts[i - 1][0], pts[i][0]), bx = Math.max(pts[i - 1][0], pts[i][0]);
      var ay = Math.min(pts[i - 1][1], pts[i][1]), by = Math.max(pts[i - 1][1], pts[i][1]);
      if (ax < x1 && x0 < bx && ay < y1 && y0 < by) { return true; }
    }
    return false;
  }

  function priceOf(pts, a, b) {
    var through = 0, len = 0, bends = 0;
    // What the route covers, so shapes nowhere near it can be passed over
    // without measuring.  On a chart of any size most of them are.
    var x0 = pts[0][0], x1 = x0, y0 = pts[0][1], y1 = y0;
    for (var p = 1; p < pts.length; p++) {
      if (pts[p][0] < x0) { x0 = pts[p][0]; } else if (pts[p][0] > x1) { x1 = pts[p][0]; }
      if (pts[p][1] < y0) { y0 = pts[p][1]; } else if (pts[p][1] > y1) { y1 = pts[p][1]; }
    }
    hand.nodes.forEach(function (n) {
      var t = turned(n);
      if (t.x + t.w / 2 < x0 || t.x - t.w / 2 > x1 ||
          t.y + t.h / 2 < y0 || t.y - t.h / 2 > y1) { return; }
      if (n.id === a.id || n.id === b.id) {
        // A line's own two shapes count too -- it should leave one and
        // arrive at the other without cutting back over either.  The legs
        // that touch their edges on the way out and in are the exception,
        // since that is the line meeting the shape, not running through it.
        if (pts.length > 3 && cutsThrough(pts, n, 2, pts.length - 2)) { through++; }
        return;
      }
      if (cutsThrough(pts, n)) { through++; }
    });
    var was = null;
    for (var i = 1; i < pts.length; i++) {
      var dx = pts[i][0] - pts[i - 1][0], dy = pts[i][1] - pts[i - 1][1];
      len += Math.abs(dx) + Math.abs(dy);
      var way = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "R" : "L") : (dy > 0 ? "D" : "U");
      if (was && way !== was) { bends++; }
      was = way;
    }
    return through * 10000 + bends * 100 + len;
  }

  function linkPath(a, b) {               // corners only, never a diagonal
    var outs = ports(a), ins = ports(b);
    var best = null, bestPrice = Infinity;

    function weigh(pts, i, j) {
      // down out of one and in at the top of the next is how a flowchart
      // reads, so it wins any tie
      var price = priceOf(pts, a, b) - (i === 1 && j === 0 ? 1 : 0);
      if (price < bestPrice) { best = pts; bestPrice = price; }
    }

    for (var i = 0; i < outs.length; i++) {
      for (var j = 0; j < ins.length; j++) {
        weigh(joinPorts(outs[i], ins[j]), i, j);
      }
    }
    if (bestPrice < 10000) { return best; }     // nothing in the way: done

    // Something is in the way of every straight join, so look for a lane to
    // go round by -- just clear of each shape's own edges, which is where a
    // way through is if there is one.  Only ever reached when the simple
    // ways are all blocked, so the usual case pays nothing for it.
    // Just clear of every shape's edges -- its own two included, since a
    // line should not cut back over the shape it came from either.
    var lanesY = [], lanesX = [];
    hand.nodes.forEach(function (n) {
      var t = turned(n);
      lanesY.push(t.y - t.h / 2 - STAND, t.y + t.h / 2 + STAND);
      lanesX.push(t.x - t.w / 2 - STAND, t.x + t.w / 2 + STAND);
    });
    // and halfway between neighbouring edges, which is where a gap is
    [lanesY, lanesX].forEach(function (lanes) {
      var sorted = lanes.slice().sort(function (p, q) { return p - q; });
      for (var i = 1; i < sorted.length; i++) {
        if (sorted[i] - sorted[i - 1] > 6) {
          lanes.push((sorted[i] + sorted[i - 1]) / 2);
        }
      }
    });
    // The way round is nearly always close to the way through, so the lanes
    // are tried nearest-first and the far ones are not tried at all.  On a
    // chart with dozens of shapes that is the difference between a redraw
    // you can feel while dragging and one you cannot.
    var NEAREST = 10;
    function closest(lanes, to) {
      return lanes.sort(function (p, q) {
        return Math.abs(p - to) - Math.abs(q - to);
      }).slice(0, NEAREST);
    }
    lanesY = closest(lanesY, (a.y + b.y) / 2);
    lanesX = closest(lanesX, (a.x + b.x) / 2);
    for (var k = 0; k < lanesY.length; k++) {
      for (var m = 0; m < 2; m++) {             // out of the top or the foot
        weigh(joinPorts(outs[m], ins[1 - m], lanesY[k]), m, 1 - m);
        weigh(joinPorts(outs[m], ins[m], lanesY[k]), m, m);
      }
    }
    for (k = 0; k < lanesX.length; k++) {
      for (m = 2; m < 4; m++) {                 // out of a side
        weigh(joinPorts(outs[m], ins[5 - m], lanesX[k]), m, 5 - m);
        weigh(joinPorts(outs[m], ins[m], lanesX[k]), m, m);
      }
    }
    return best;
  }

  // How far a point is from a line between two points.  Used to work out
  // which arrow somebody meant when they clicked near one rather than on it.
  function offLine(px, py, ax, ay, bx, by) {
    var vx = bx - ax, vy = by - ay;
    var run = vx * vx + vy * vy;
    var t = run ? ((px - ax) * vx + (py - ay) * vy) / run : 0;
    t = Math.max(0, Math.min(1, t));
    var dx = px - (ax + vx * t), dy = py - (ay + vy * t);
    return Math.sqrt(dx * dx + dy * dy);
  }

  // The arrow nearest a point, if one is near enough to have been meant.
  // Clicking exactly on a line is a lot to ask -- an arrow is one pixel wide
  // and there are shapes lying over parts of it -- so a click on bare paper
  // takes the nearest arrow within reach instead of just clearing what was
  // selected.
  function linkNear(x, y, within) {
    var best = null, howNear = within;
    hand.links.forEach(function (link) {
      var a = nodeById(link.from), b = nodeById(link.to);
      if (!a || !b) { return; }
      var pts = linkPath(a, b);
      for (var i = 1; i < pts.length; i++) {
        var off = offLine(x, y, pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1]);
        if (off < howNear) { howNear = off; best = link; }
      }
    });
    return best;
  }

  // A key of the shapes this design actually uses, drawn along the top the
  // way the built charts draw theirs.  Only the kinds that turn up are
  // listed: a design with no diamonds in it does not advertise one.
  var KEY_W = 62, KEY_H = 30, KEY_GAP = 9, KEY_AFTER = 28;

  function keyRow() {
    if (!el("#f-legend") || !el("#f-legend").checked) { return { art: "", tall: 0 }; }
    var used = [];
    hand.nodes.forEach(function (n) {
      if (n.kind !== "text" && used.indexOf(n.kind) < 0) { used.push(n.kind); }
    });
    if (!used.length) { return { art: "", tall: 0 }; }
    var pen = measure.pen || (measure.pen = document.createElement("canvas")
                              .getContext("2d"));
    pen.font = "bold " + HAND_TYPE + "px Arial, Helvetica, sans-serif";
    var out = [], x = 0;
    used.forEach(function (kind) {
      out.push(shapeArt(kind, x + KEY_W / 2, KEY_H / 2, KEY_W, KEY_H, "#ffffff"));
      x += KEY_W + KEY_GAP;
      var name = kindName(kind);
      out.push('<text class="label" x="' + x + '" y="' + (KEY_H / 2 + 4) +
               '" font-weight="bold" stroke="none" fill="#000000">' +
               escaped(name) + "</text>");
      x += Math.round(pen.measureText(name).width) + KEY_AFTER;
    });
    return { art: '<g class="key">' + out.join("") + "</g>", tall: KEY_H + 22,
             wide: x };
  }

  function drawHand() {
    var pad = 40, maxx = 520, maxy = 280, ox = 0, oy = 0;
    hand.nodes.forEach(function (n) {       // the paper keeps its corner, so
      measure(n);                           //   moving one shape moves one
      var room = turned(n);
      n.x = Math.max(room.w / 2 + 20, n.x); //   shape and nothing else
      n.y = Math.max(room.h / 2 + 20, n.y);
      maxx = Math.max(maxx, n.x + room.w / 2);
      maxy = Math.max(maxy, n.y + room.h / 2);
    });
    var key = keyRow();
    oy = key.tall;                     // the chart sits below the key
    var wide = Math.round(Math.max(maxx + pad, (key.wide || 0) + pad));
    var tall = Math.round(maxy + pad + key.tall);

    var out = ['<svg xmlns="http://www.w3.org/2000/svg" id="chart" width="' +
               wide + '" height="' + tall + '" viewBox="0 0 ' + wide + ' ' +
               tall + '">',
               '<rect class="sheet" width="100%" height="100%" fill="#ffffff"/>'];
    var fine = [], major = [], i;
    for (i = 0; i * HAND_RULE <= wide; i++) {
      (i % 5 ? fine : major).push("M" + i * HAND_RULE + ",0V" + tall);
    }
    for (i = 0; i * HAND_RULE <= tall; i++) {
      (i % 5 ? fine : major).push("M0," + i * HAND_RULE + "H" + wide);
    }
    out.push('<path class="grid fine" d="' + fine.join("") +
             '" fill="none" stroke="#e7ebf0" stroke-width="0.7"/>');
    out.push('<path class="grid major" d="' + major.join("") +
             '" fill="none" stroke="#d8dfe8" stroke-width="1"/>');
    out.push('<g font-family="Arial, Helvetica, sans-serif" font-size="' +
             HAND_TYPE + '" ' +
             'fill="none" stroke="#000000" stroke-width="1.3" ' +
             'stroke-linecap="round" stroke-linejoin="round">');

    var tips = [];                     // held back so nothing paints over them
    hand.links.forEach(function (link) {
      var a = nodeById(link.from), b = nodeById(link.to);
      if (!a || !b) { return; }
      if (!link.id) { link.id = hand.nextLink = (hand.nextLink || 0) + 1; }
      var pts = linkPath(a, b).map(function (p) { return [p[0] + ox, p[1] + oy]; });
      var last = pts[pts.length - 1], prev = pts[pts.length - 2];
      var run = Math.hypot(last[0] - prev[0], last[1] - prev[1]) || 1;
      var ux = (last[0] - prev[0]) / run, uy = (last[1] - prev[1]) / run;
      var cx = last[0] - ux * 10, cy = last[1] - uy * 10;
      var d = "M" + pts.map(function (p) { return p[0] + "," + p[1]; }).join("L");
      var look = (link.dash ? ' stroke-dasharray="7 5"' : "") +
                 (link.wide ? ' stroke-width="' + link.wide + '"' : "") +
                 (link.color ? ' stroke="' + link.color + '"' : "");
      out.push('<g class="link' + (chosen === link.id ? " on" : "") +
               '" data-link="' + link.id + '">');
      out.push('<path class="grab" d="' + d + '" fill="none" stroke="transparent" ' +
               'stroke-width="20" pointer-events="stroke" ' +
               'stroke-linecap="round" stroke-linejoin="round"/>');
      out.push('<path class="flow" d="' + d + '" fill="none"' + look + "/>");
      if (link.head !== false) {
        tips.push('<polygon class="head" points="' + last[0] + "," + last[1] + " " +
                 (cx - uy * 4) + "," + (cy + ux * 4) + " " + (cx + uy * 4) + "," +
                 (cy - ux * 4) + '" fill="' + (link.color || "#000000") +
                 '" stroke="' + (link.color || "#000000") + '" ' +
                 'stroke-width="0.6" stroke-linejoin="miter"/>');
      }
      if (link.label) {
        var mid = pts[Math.floor(pts.length / 2)];
        out.push('<rect class="patch" x="' + (mid[0] + 4) + '" y="' + (mid[1] - 16) +
                 '" width="' + (link.label.length * 7 + 8) + '" height="13" ' +
                 'fill="#ffffff" stroke="none"/>');
        out.push('<text class="label" x="' + (mid[0] + 6) + '" y="' + (mid[1] - 6) +
                 '" font-weight="bold" stroke="none" fill="#000000">' +
                 escaped(link.label) + "</text>");
      }
      out.push("</g>");
    });

    hand.nodes.forEach(function (n) {
      var moved = { kind: n.kind, x: n.x + ox, y: n.y + oy, w: n.w, h: n.h };
      var about = turned(n);           // what it takes up, once turned
      out.push('<g class="node' + (picked === n.id ? " on" : "") +
               '" data-kind="' + n.kind + '" data-i="h' + n.id + '"' +
               (n.turn ? ' transform="rotate(' + n.turn + " " + moved.x + " " +
                         moved.y + ')"' : "") + ">");
      out.push(shapeSvg(moved));
      var lines = String(n.text || "").split("\n");
      // The baseline sits below the middle by about a third of the type,
      // which is what puts the body of the letters on the middle line
      // instead of hanging them off it.
      var mid = moved.y + (WORD_SHIFT[n.kind] || 0) * n.h;
      var y0 = mid - (lines.length - 1) * HAND_LINE / 2 + HAND_TYPE * 0.35;
      lines.forEach(function (line, k) {
        out.push('<text x="' + moved.x + '" y="' + (y0 + k * HAND_LINE).toFixed(1) +
                 '" text-anchor="middle" stroke="none" fill="#000000">' +
                 escaped(line) + "</text>");
      });
      out.push("</g>");
      if (joining && picked && n.id !== picked) {
        // Somewhere to aim for.  Once a line is being drawn, every other
        // shape puts its own dots out, so joining two up is click a dot,
        // click a dot -- no holding the button down and no aiming at a
        // one-pixel line.
        ports(n).forEach(function (port) {
          out.push('<circle class="spot" data-i="' + n.id + '" cx="' +
                   (port.x + ox + port.dx * 1.5) + '" cy="' +
                   (port.y + oy + port.dy * 1.5) + '" r="6.5"/>');
        });
      }
      if (picked === n.id) {
        // A dot on each side, sitting where an arrow would actually meet the
        // shape -- on the slant of a parallelogram, on the point of a
        // diamond -- rather than out on the corner of the box round it.
        // Press and drag from one to draw a line, or just click it and then
        // click where it should go.
        ports(n).forEach(function (port) {
          out.push('<circle class="knob' + (joining ? " lit" : "") +
                   '" data-i="' + n.id + '" cx="' +
                   (port.x + ox + port.dx * 1.5) + '" cy="' +
                   (port.y + oy + port.dy * 1.5) + '" r="5.5" fill="#14427c" ' +
                   'stroke="#ffffff" stroke-width="1.5"/>');
        });
        // a corner at every corner, each one anchored to the one opposite,
        // so a shape grows and shrinks from whichever you take hold of
        [["nw", -1, -1], ["ne", 1, -1], ["sw", -1, 1], ["se", 1, 1]]
          .forEach(function (corner) {
            out.push('<rect class="grip" data-i="' + n.id +
                     '" data-corner="' + corner[0] + '" x="' +
                     (moved.x + corner[1] * about.w / 2 - 4.5) + '" y="' +
                     (moved.y + corner[2] * about.h / 2 - 4.5) +
                     '" width="9" height="9" rx="2" fill="#ffffff" ' +
                     'stroke="#14427c" stroke-width="1.6"/>');
          });
      }
    });
    out.push('<g class="tips">' + tips.join("") + "</g>");
    if (key.art) {
      out.push('<g transform="translate(' + (pad / 2) + ',' + (pad / 2) + ')">' +
               key.art + "</g>");
    }
    guides.forEach(function (g) {
      var d = g[0] ? "M" + (g[1] + ox) + "," + (g[2] + oy) + "V" + (g[3] + oy)
                   : "M" + (g[2] + ox) + "," + (g[1] + oy) + "H" + (g[3] + ox);
      out.push('<path class="guide" d="' + d + '" fill="none"/>');
    });
    out.push("</g></svg>");
    el("#sheet").innerHTML = out.join("\n");
    bind();
    paint();
    el("#sub").textContent = TXT.as_chart + " · " + wide + " x " + tall + " px";
    handKeep();
  }

  function escaped(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;");
  }

  // ---- the panel side of it ---------------------------------------------
  function drawAdders() {
    var box = el("#adders");
    if (!box) { return; }
    box.innerHTML = "";
    handKinds().forEach(function (pair) {
      var b = document.createElement("button");
      b.className = "btn small";
      b.title = pair[1];
      b.setAttribute("aria-label", pair[1]);
      b.draggable = true;
      b.innerHTML = keyMark(pair[0]);
      b.onclick = function () { addNode(pair[0]); };
      // Dragged onto the paper it lands where it is dropped, which is what
      // anyone who has used a drawing program will try first.  Clicking it
      // still drops one below whatever is in hand, for anyone who would
      // rather not drag.
      b.ondragstart = function (ev) {
        ev.dataTransfer.setData("text/plain", pair[0]);
        ev.dataTransfer.effectAllowed = "copy";
        dragging_kind = pair[0];
      };
      b.ondragend = function () { dragging_kind = null; };
      box.appendChild(b);
    });
    paperTakesDrops();
  }

  var dragging_kind = null;              // the shape being carried in

  function dropOnPaper(where) {
    var stage = el("#stage"), chart = el("#chart");
    if (!chart || !chart.getScreenCTM) { return false; }
    var frame = chart.getScreenCTM();
    if (!frame) { return false; }
    var spot = chart.createSVGPoint();
    spot.x = where.clientX;
    spot.y = where.clientY;
    spot = spot.matrixTransform(frame.inverse());
    var kind = dragging_kind ||
               (where.dataTransfer && where.dataTransfer.getData("text/plain"));
    if (!kind) { return false; }
    addNode(kind, { x: spot.x, y: spot.y });
    dragging_kind = null;
    return true;
  }

  function paperTakesDrops() {
    var stage = el("#stage");
    if (!stage || stage.dataset.drops) { return; }
    stage.dataset.drops = "yes";
    stage.addEventListener("dragover", function (ev) {
      if (!byHand) { return; }
      ev.preventDefault();
      ev.dataTransfer.dropEffect = "copy";
      stage.classList.add("taking");
    });
    stage.addEventListener("dragleave", function (ev) {
      if (ev.target === stage) { stage.classList.remove("taking"); }
    });
    stage.addEventListener("drop", function (ev) {
      stage.classList.remove("taking");
      if (!byHand) { return; }
      ev.preventDefault();
      dropOnPaper(ev);
    });
  }

  function addNode(kind, at) {
    keepUndo();
    var under = nodeById(picked), x = 260, y = 60;
    if (at) {                           // dropped somewhere in particular
      x = Math.round(at.x / HAND_GRID) * HAND_GRID;
      y = Math.round(at.y / HAND_GRID) * HAND_GRID;
    } else if (under) {                 // under whatever is being worked on
      x = under.x;
      y = under.y + under.h / 2 + 70;
      while (hand.nodes.some(function (n) {
        return Math.abs(n.x - x) < 60 && Math.abs(n.y - y) < 40;
      })) { y += 40; }
    } else if (hand.nodes.length) {
      hand.nodes.forEach(function (n) { y = Math.max(y, n.y + n.h / 2 + 70); });
    }
    var node = { id: hand.next++, kind: kind, text: firstWords(kind),
                 x: x, y: y, w: 140, h: 46 };
    measure(node);
    hand.nodes.push(node);
    picked = node.id;
    drawHand();
    drawHandPanel();
  }

  function firstWords(kind) {
    if (kind === "oval") {
      return hand.nodes.some(function (n) { return n.kind === "oval"; })
             ? TXT.end : TXT.start;
    }
    // A words-only box has no outline, so an empty one would be nothing at
    // all on the paper.  It arrives saying what it is, ready to be typed over.
    if (kind === "text") { return TXT.n_text || "Text"; }
    return "";
  }

  function drawHandPanel() {
    var box = el("#hand-sel");
    if (!box) { return; }
    box.innerHTML = "";
    var link = linkById(chosen);
    if (link) { return arrowPanel(box, link); }
    var node = nodeById(picked);
    if (!node) {
      box.innerHTML = '<p class="hint">' + TXT.pick_shape + "</p>";
      return;
    }
    var name = kindName(node.kind);
    var head = document.createElement("div");
    head.className = "what";
    head.style.cssText = "font-weight:600; margin:10px 0 6px";
    head.textContent = name;
    box.appendChild(head);

    function put(bit) { box.appendChild(bit); }
    var label = document.createElement("label");
    label.style.cssText = "display:block; font-size:11.5px; color:var(--muted)";
    label.textContent = TXT.words_in;
    box.appendChild(label);
    var words = document.createElement("textarea");
    words.className = "field";
    words.style.cssText = "height:56px; font-family:inherit; font-size:13px";
    words.value = node.text || "";
    words.oninput = function () {
      node.text = words.value;
      drawHand();
    };
    box.appendChild(words);

    var go = document.createElement("div");
    go.style.cssText = "display:flex; gap:8px; margin-top:10px";
    var join = document.createElement("button");
    join.className = "btn small" + (joining ? " primary" : "");
    join.textContent = joining ? TXT.connect_now : TXT.connect;
    join.onclick = function () { joining = !joining; drawHandPanel(); };
    var cut = document.createElement("button");
    cut.className = "btn small";
    cut.textContent = TXT.delete;
    cut.onclick = function () {
      hand.nodes = hand.nodes.filter(function (n) { return n.id !== node.id; });
      hand.links = hand.links.filter(function (l) {
        return l.from !== node.id && l.to !== node.id;
      });
      picked = null; joining = false;
      drawHand(); drawHandPanel(); showReport();
    };
    go.appendChild(join);
    go.appendChild(cut);
    put(go);

    // how big, and which way round
    var sizing = document.createElement("div");
    sizing.className = "trio";
    [[TXT.width, "w", 30, 600], [TXT.height, "h", 24, 400],
     [TXT.turn, "turn", 0, 350]].forEach(function (item) {
      var cell = document.createElement("label");
      cell.innerHTML = '<span>' + item[0] + "</span>";
      var spin = document.createElement("input");
      spin.type = "number";
      spin.className = "field";
      spin.step = item[1] === "turn" ? 15 : 10;
      spin.min = item[2];
      spin.max = item[3];
      spin.value = Math.round(node[item[1]] || 0);
      spin.oninput = function () {
        var want = parseFloat(spin.value);
        if (isNaN(want)) { return; }
        if (item[1] === "turn") {
          node.turn = ((want % 360) + 360) % 360;
        } else {
          node.own = true;                 // a size of its own from now on
          node[item[1]] = Math.max(item[2], Math.min(item[3], want));
          if (node.kind === "circle") { node.h = node.w; }
        }
        drawHand();
      };
      cell.appendChild(spin);
      sizing.appendChild(cell);
    });
    put(sizing);
    var back = document.createElement("button");
    back.className = "btn small";
    back.style.marginTop = "6px";
    back.textContent = TXT.fit_words;
    back.onclick = function () {
      node.own = false; node.turn = 0;
      measure(node, true);
      drawHand(); drawHandPanel();
    };
    put(back);

    // and its colors, right here rather than on the other side of the panel
    var paints = document.createElement("div");
    paints.className = "trio";
    var mine = style.nodes["h" + node.id] = style.nodes["h" + node.id] || {};
    var k = style.kinds[node.kind] || {};
    [[TXT.fill, "fill", k.fill || "#ffffff"],
     [TXT.outline, "line", k.line || style.ink || "#000000"],
     [TXT.text, "text", k.text || style.words || style.ink || "#000000"]]
      .forEach(function (item) {
        var cell = document.createElement("label");
        cell.innerHTML = "<span>" + item[0] + "</span>";
        var firstTouch = true;
        cell.appendChild(swatch(mine[item[1]], item[2], function (v) {
          if (firstTouch) { firstTouch = false; keepUndo(); }
          mine[item[1]] = v;
          paint();
        }));
        paints.appendChild(cell);
      });
    var title = document.createElement("div");
    title.className = "small-head";
    title.textContent = TXT.colors_here;
    put(title);
    put(paints);


    var outs = outOf(node.id);
    var list = document.createElement("div");
    list.style.marginTop = "10px";
    list.innerHTML = '<div style="font-size:11.5px; color:var(--muted)">' +
                     TXT.goes_to + "</div>";
    if (!outs.length) {
      list.innerHTML += '<div class="hint">' + TXT.nothing_yet + "</div>";
    }
    outs.forEach(function (link) {
      var to = nodeById(link.to);
      var row = document.createElement("div");
      row.className = "row";
      row.innerHTML = '<span class="name">' +
                      escaped((to && to.text) || (to ? to.kind : "?")).slice(0, 22) +
                      "</span>";
      if (node.kind === "diamond" || outs.length > 1) {
        var tag = document.createElement("input");
        tag.className = "field";
        tag.style.cssText = "width:78px; padding:3px 6px";
        tag.value = link.label || "";
        tag.oninput = function () { link.label = tag.value; drawHand(); };
        row.appendChild(tag);
      }
      var cut = document.createElement("button");
      cut.className = "btn small";
      cut.textContent = "×";
      cut.onclick = function () {
        hand.links = hand.links.filter(function (l) { return l !== link; });
        drawHand(); drawHandPanel();
      };
      row.appendChild(cut);
      list.appendChild(row);
    });
    box.appendChild(list);
  }

  function joinUp(fromId, toId) {         // one shape leads to another
    if (!fromId || !toId || fromId === toId) { return; }
    var already = outOf(fromId).some(function (l) { return l.to === toId; });
    if (already) { return; }
    keepUndo();
    var from = nodeById(fromId);
    var tag = "";
    if (from && from.kind === "diamond") {
      tag = outOf(fromId).length ? TXT.no : TXT.yes;
    }
    hand.links.push({ from: fromId, to: toId, label: tag });
    joining = false;
    drawHand();
    drawHandPanel();
    showReport();
  }

  function linkById(id) {
    return hand.links.filter(function (l) { return l.id === id; })[0] || null;
  }
  function pickLink(id) {
    chosen = id;
    picked = null;
    joining = false;
    drawHand();
    drawHandPanel();
  }

  function arrowPanel(box, link) {       // an arrow has its own few things
    var from = nodeById(link.from), to = nodeById(link.to);
    var head = document.createElement("div");
    head.style.cssText = "font-weight:600; margin:10px 0 6px";
    head.textContent = TXT.an_arrow;
    box.appendChild(head);
    var says = document.createElement("div");
    says.className = "hint";
    says.style.marginBottom = "8px";
    says.textContent = ((from && from.text) || "?").slice(0, 16) + "  \u2192  " +
                       ((to && to.text) || "?").slice(0, 16);
    box.appendChild(says);

    var label = document.createElement("label");
    label.style.cssText = "display:block; font-size:11.5px; color:var(--muted)";
    label.textContent = TXT.word_on_it;
    box.appendChild(label);
    var tag = document.createElement("input");
    tag.className = "field";
    tag.value = link.label || "";
    tag.oninput = function () { link.label = tag.value; drawHand(); };
    box.appendChild(tag);

    var trio = document.createElement("div");
    trio.className = "trio";
    var thick = document.createElement("label");
    thick.innerHTML = "<span>" + TXT.thickness + "</span>";
    var spin = document.createElement("input");
    spin.type = "number";
    spin.className = "field";
    spin.min = 1; spin.max = 6; spin.step = 0.5;
    spin.value = link.wide || 1.3;
    spin.oninput = function () { link.wide = parseFloat(spin.value) || 1.3; drawHand(); };
    thick.appendChild(spin);
    trio.appendChild(thick);
    var paint = document.createElement("label");
    paint.innerHTML = "<span>" + TXT.color_of_it + "</span>";
    paint.appendChild(swatch(link.color, style.ink || "#000000", function (v) {
      link.color = v; drawHand();
    }));
    trio.appendChild(paint);
    box.appendChild(trio);

    var switches = document.createElement("div");
    switches.style.cssText = "display:flex; gap:14px; margin-top:10px; flex-wrap:wrap";
    [[TXT.dashed, "dash", !!link.dash],
     [TXT.with_head, "head", link.head !== false]].forEach(function (item) {
      var one = document.createElement("label");
      one.className = "switch";
      var tick = document.createElement("input");
      tick.type = "checkbox";
      tick.checked = item[2];
      tick.onchange = function () {
        link[item[1]] = item[1] === "head" ? tick.checked : tick.checked;
        drawHand();
      };
      one.appendChild(tick);
      one.appendChild(document.createTextNode(item[0]));
      switches.appendChild(one);
    });
    box.appendChild(switches);

    var go = document.createElement("div");
    go.style.cssText = "display:flex; gap:8px; margin-top:10px";
    var flip = document.createElement("button");
    flip.className = "btn small";
    flip.textContent = TXT.turn_it_round;
    flip.onclick = function () {
      var was = link.from; link.from = link.to; link.to = was;
      drawHand(); drawHandPanel(); showReport();
    };
    var cut = document.createElement("button");
    cut.className = "btn small";
    cut.textContent = TXT.delete;
    cut.onclick = function () {
      hand.links = hand.links.filter(function (l) { return l !== link; });
      chosen = null;
      drawHand(); drawHandPanel(); showReport();
    };
    go.appendChild(flip);
    go.appendChild(cut);
    box.appendChild(go);
  }

  function handClick(id) {                // a shape was clicked on the chart
    chosen = null;
    if (joining && picked && picked !== id) {
      joinUp(picked, id);
      return;
    }
    picked = id;
    joining = false;
    drawHand();
    drawHandPanel();
    var g = el('.node[data-i="h' + id + '"]', chart);  // the colour side of
    if (g) { select(g); }                              //   the panel follows
  }

  // ---- does it actually work? -------------------------------------------
  function checkDesign() {
    var found = [];
    function fault(key, node, fill) {
      found.push({ text: say(key, fill || {}), id: node ? node.id : null });
    }
    if (!hand.nodes.length) { return found; }

    var heads = hand.nodes.filter(function (n) { return !intoOf(n.id).length; });
    if (!heads.length) { fault("p_no_start", null); }
    else if (heads.length > 1) { fault("p_many_starts", null, { n: heads.length }); }
    else if (heads[0].kind !== "oval") { fault("p_start_kind", heads[0]); }

    var ends = hand.nodes.filter(function (n) {
      return n.kind === "oval" && !outOf(n.id).length;
    });
    if (!ends.length) { fault("p_no_end", null); }

    hand.nodes.forEach(function (n) {
      var outs = outOf(n.id), ins = intoOf(n.id);
      if (!String(n.text || "").trim()) { fault("p_empty", n); }
      if (!outs.length && !ins.length) { fault("p_alone", n); }
      else if (!outs.length && n.kind !== "oval") { fault("p_dead_end", n); }
      if (n.kind === "diamond" && outs.length !== 2) {
        fault("p_decision_out", n, { n: outs.length });
      }
      if (n.kind !== "diamond" && outs.length > 1) {
        fault("p_one_out", n, { n: outs.length });
      }
      if (n.kind === "diamond" && outs.length === 2) {
        var one = (outs[0].label || "").trim(), two = (outs[1].label || "").trim();
        if (!one || !two) { fault("p_no_label", n); }
        else if (one.toLowerCase() === two.toLowerCase()) { fault("p_same_labels", n); }
      }
      hand.nodes.forEach(function (m) {
        if (m.id <= n.id) { return; }
        if (Math.abs(m.x - n.x) * 2 < m.w + n.w - 8 &&
            Math.abs(m.y - n.y) * 2 < m.h + n.h - 8) {
          fault("p_overlap", n);
        }
      });
    });

    // a line that runs through a shape on its way past is not wrong, but it
    // is the thing that makes a hand-drawn chart hard to follow
    hand.links.forEach(function (link) {
      var a = nodeById(link.from), b = nodeById(link.to);
      if (!a || !b) { return; }
      var pts = linkPath(a, b);
      hand.nodes.forEach(function (n) {
        if (n.id === a.id || n.id === b.id) { return; }
        for (var i = 0; i < pts.length - 1; i++) {
          if (throughBox(pts[i], pts[i + 1], n)) { fault("p_line_through", n); return; }
        }
      });
    });

    // everything has to be reachable from the start...
    if (heads.length === 1) {
      var seen = {}, stack = [heads[0].id];
      while (stack.length) {
        var id = stack.pop();
        if (seen[id]) { continue; }
        seen[id] = true;
        outOf(id).forEach(function (l) { stack.push(l.to); });
      }
      hand.nodes.forEach(function (n) {
        if (!seen[n.id]) { fault("p_unreached", n); }
      });
    }
    // ...and from everything, an End has to be reachable, or the flow is
    // caught in a loop it can never leave
    if (ends.length) {
      var safe = {};
      ends.forEach(function (n) { safe[n.id] = true; });
      var moved = true;
      while (moved) {
        moved = false;
        hand.links.forEach(function (l) {
          if (safe[l.to] && !safe[l.from]) { safe[l.from] = true; moved = true; }
        });
      }
      hand.nodes.forEach(function (n) {
        if (!safe[n.id] && outOf(n.id).length) { fault("p_trapped", n); }
      });
    }
    return found;
  }

  function throughBox(p, q, n) {         // does this leg cross that shape?
    var l = n.x - n.w / 2 + 4, r = n.x + n.w / 2 - 4;
    var t = n.y - n.h / 2 + 4, b = n.y + n.h / 2 - 4;
    if (Math.abs(p[0] - q[0]) < 0.5) {
      return p[0] > l && p[0] < r &&
             Math.min(p[1], q[1]) < b && Math.max(p[1], q[1]) > t;
    }
    if (Math.abs(p[1] - q[1]) < 0.5) {
      return p[1] > t && p[1] < b &&
             Math.min(p[0], q[0]) < r && Math.max(p[0], q[0]) > l;
    }
    return false;
  }

  function showReport() {
    var box = el("#report");
    var found = checkDesign();
    box.innerHTML = "";
    if (!hand.nodes.length) { return; }
    if (!found.length) {
      box.innerHTML = '<p class="good">' + TXT.checked_good + "</p>";
      return;
    }
    var head = document.createElement("p");
    head.className = "hint bad";
    head.textContent = say("problems", { n: found.length });
    box.appendChild(head);
    found.forEach(function (bit) {
      var row = document.createElement("button");
      row.className = "fault";
      row.textContent = bit.text;
      row.onclick = function () {
        if (bit.id) { picked = bit.id; drawHand(); drawHandPanel(); }
      };
      box.appendChild(row);
    });
  }

  // ---- keeping a design, and switching between the two ways of working --
  function handKeep() {
    try {
      localStorage.setItem("flowchart-hand", JSON.stringify(hand));
    } catch (e) { /* no storage: it lives as long as the tab does */ }
  }
  function handRecall() {
    try {
      var was = JSON.parse(localStorage.getItem("flowchart-hand"));
      if (was && was.nodes && was.nodes.length) { hand = was; return true; }
    } catch (e) { /* nothing kept */ }
    return false;
  }

  var byHand = false;
  function setMode(toHand) {
    byHand = toHand;
    el("#tab-code").classList.toggle("on", !toHand);
    el("#tab-hand").classList.toggle("on", toHand);
    el("#source").hidden = toHand;
    el("#hand").hidden = !toHand;
    // Grid and Key belong to the chart, not to the way it was made, so the
    // one pair of switches goes wherever the chart is being made: above the
    // Build button in one mode, up with the shapes in the other.  Moving the
    // same two rather than having two pairs means they cannot disagree.
    var both = el("#chart-switches");
    if (both) {
      if (toHand) { el("#hand-switches").appendChild(both); }
      else { el("#source").insertBefore(both, el(".build-row")); }
    }
    if (toHand) {
      drawAdders();
      drawHand();
      drawHandPanel();
      showReport();
    } else if (el("#code").value.trim()) {
      el("#build").click();
    }
    try { localStorage.setItem("flowchart-mode", toHand ? "hand" : "code"); }
    catch (e) { /* fine */ }
  }

  if (el("#tab-hand")) {
    el("#tab-code").onclick = function () { setMode(false); };
    el("#tab-hand").onclick = function () { setMode(true); };
    el("#check").onclick = showReport;
    el("#wipe").onclick = function () {
      hand = { nodes: [], links: [], next: 1 };
      picked = null; joining = false;
      drawHand(); drawHandPanel(); showReport();
    };
  }


  // ============================================================== running ==
  // A flowchart that draws nicely can still be wrong.  This runs it: it goes
  // through the program the chart was made from, one statement at a time,
  // lighting up the shape it is on, asking for whatever the program asks a
  // person for, and printing what it prints.  If it never stops, it says so
  // rather than hanging.  That is the test: not "does it look like a
  // flowchart" but "does it do what it is supposed to do".
  var AST = null;                        // the program, as data
  var running = false, stopping = false, waiting = null;
  var STEP_CAP = 200000;                 // past this, it is not going to stop
  var BREATH = 250;                      // steps between letting the page back in
  var breaths = 0;

  // Letting go, properly.  Everything in here is async, but awaiting a value
  // that is already there only yields a microtask -- and the browser does not
  // look at the mouse between microtasks.  So a loop with nothing to type into
  // it used to run flat out with the page frozen: the Stop button had been
  // pressed, the click was sitting in the queue, and nothing read it until the
  // step cap was reached minutes later.  A timeout is a real turn of the loop,
  // which is what gives the click its chance.
  function breathe() {
    return new Promise(function (go) { setTimeout(go, 0); });
  }

  // One step of the program: count it, stop if asked, and every so often hand
  // the page back so it can answer for itself.
  async function tick(where) {
    if (stopping) { throw new Stop(); }
    where.steps++;
    if (where.steps > STEP_CAP) { throw new Error(TXT.r_forever); }
    if (++breaths >= BREATH) {
      breaths = 0;
      await breathe();
      if (stopping) { throw new Stop(); }
    }
  }

  function talk(what, how) {
    var line = document.createElement("div");
    line.className = "said" + (how ? " " + how : "");
    line.textContent = what;
    var box = el("#tape");
    box.appendChild(line);
    box.scrollTop = box.scrollHeight;
    return line;
  }

  // Saying it once.  A button pressed when there is nothing for it to work
  // on answers with a line in the tape -- and pressing it again is the same
  // question asked again, not a second question, so it does not get a second
  // copy of the same answer written underneath the first.  Press As code six
  // times on an empty page and you used to get six identical lines, which
  // reads as six things having gone wrong.  The line that is already there
  // is shaken instead, so the press is still felt.
  function talkOnce(what, how) {
    var box = el("#tape");
    var last = box ? box.lastElementChild : null;
    if (last && last.textContent === what) {
      briefly(last, "again", 420);
      box.scrollTop = box.scrollHeight;
      return last;
    }
    return talk(what, how);
  }

  // The Run button is in two places at once -- in the panel, and in the bar
  // of the full screen -- and they are the one button: whichever was
  // pressed, both say Stop for as long as it runs.
  function runSays(word) {
    all("#run, #tape-run").forEach(function (b) { b.textContent = word; });
  }

  function lightUp(id) {
    all(".node.now", chart).forEach(function (g) { g.classList.remove("now"); });
    markLine(id);
    if (!id) { return; }
    var lit = null;
    all('.node[data-i="' + id + '"]', chart).forEach(function (g) {
      g.classList.add("now");
      if (!lit) { lit = g; }
    });
    if (lit && following()) { followNode(lit); }
  }

  // The line of pseudocode the shape was drawn from, marked where it is
  // written.  Marked, not selected: selecting a line in a box means focusing
  // the box, and focus during a run belongs to whatever the program is
  // sitting there asking to be typed.
  function markLine(id) {
    var code = el("#code");
    if (!code) { return; }
    var at = (id && following()) ? (lineOf || {})[id] : 0;
    var span = at ? lineSpan(code, at) : null;
    if (!span) {
      code.classList.remove("at");
      return;
    }
    // Where the line is and how tall it is, both measured -- a line too long
    // for the column takes two rows or three, and the mark has to be as tall
    // as the line it is marking.  The ten is the box's own top padding, which
    // is where its ruling starts from as well.
    code.style.setProperty("--at-top", (10 + span.top) + "px");
    code.style.setProperty("--at-tall", span.tall + "px");
    code.classList.add("at");
    showLine(code, at);
  }

  // ---- numbers, words and what they mean --------------------------------
  function tokens(src) {
    var out = [], i = 0, s = String(src || "");
    var two = ["<=", ">=", "<>", "!=", "==", ":=", "&&", "||"];
    while (i < s.length) {
      var c = s[i];
      if (/\s/.test(c)) { i++; continue; }
      if (c === '"' || c === "'") {
        var end = s.indexOf(c, i + 1);
        if (end < 0) { end = s.length; }
        out.push({ t: "str", v: s.slice(i + 1, end) });
        i = end + 1;
        continue;
      }
      if (/[0-9]/.test(c) || (c === "." && /[0-9]/.test(s[i + 1] || ""))) {
        var num = /^[0-9]*\.?[0-9]+/.exec(s.slice(i))[0];
        out.push({ t: "num", v: parseFloat(num) });
        i += num.length;
        continue;
      }
      if (/[A-Za-z_]/.test(c)) {
        var name = /^[A-Za-z_]\w*/.exec(s.slice(i))[0];
        out.push({ t: "name", v: name });
        i += name.length;
        continue;
      }
      var pair = s.substr(i, 2);
      if (two.indexOf(pair) >= 0) { out.push({ t: "op", v: pair }); i += 2; continue; }
      out.push({ t: "op", v: c });
      i++;
    }
    return out;
  }

  var RANK = { "or": 1, "||": 1, "and": 2, "&&": 2, "=": 3, "==": 3, "!=": 3,
               "<>": 3, "<": 4, "<=": 4, ">": 4, ">=": 4, "+": 5, "-": 5,
               "*": 6, "/": 6, "mod": 6, "%": 6, "div": 6, "^": 7 };

  function value(src, where) {           // work out what an expression comes to
    var ts = tokens(src), at = 0;
    function peek() { return ts[at]; }
    function take() { return ts[at++]; }
    function word(tok) {
      return tok && tok.t === "name" ? String(tok.v).toLowerCase() : null;
    }
    function primary() {
      var tok = take();
      if (!tok) { throw new Error(say("r_half", { bit: src })); }
      if (tok.t === "num" || tok.t === "str") { return tok.v; }
      if (tok.t === "op" && tok.v === "(") {
        var inside = expr(0);
        if (peek() && peek().v === ")") { take(); }
        return inside;
      }
      if (tok.t === "op" && (tok.v === "-" || tok.v === "+")) {
        var one = primary();
        return tok.v === "-" ? -Number(one) : Number(one);
      }
      if (tok.t === "name") {
        var name = String(tok.v), low = name.toLowerCase();
        if (low === "not") { return !truthy(primary()); }
        if (low === "true") { return true; }
        if (low === "false") { return false; }
        if (peek() && peek().v === "(") {    // a call, ours or a built-in
          take();
          var args = [];
          if (peek() && peek().v !== ")") {
            args.push(expr(0));
            while (peek() && peek().v === ",") { take(); args.push(expr(0)); }
          }
          if (peek() && peek().v === ")") { take(); }
          return callOut(name, args, where);
        }
        if (where.vars.hasOwnProperty(name)) { return where.vars[name]; }
        var seen = Object.keys(where.vars).filter(function (k) {
          return k.toLowerCase() === low;
        })[0];
        if (seen !== undefined) { return where.vars[seen]; }
        throw new Error(say("r_unknown", { name: name }));
      }
      throw new Error(say("r_half", { bit: src }));
    }
    function expr(least) {
      var left = primary();
      while (peek()) {
        var tok = peek();
        var op = tok.t === "op" ? tok.v : word(tok);
        var rank = RANK[op];
        if (!rank || rank < least) { break; }
        take();
        var right = expr(rank + 1);
        left = apply(op, left, right);
      }
      return left;
    }
    var got = expr(0);
    return got;
  }

  function truthy(v) {
    if (typeof v === "boolean") { return v; }
    if (typeof v === "number") { return v !== 0; }
    return String(v || "").length > 0 && String(v).toLowerCase() !== "false";
  }
  function num(v) {
    var n = typeof v === "number" ? v : parseFloat(v);
    return isNaN(n) ? 0 : n;
  }
  function same(a, b) {
    if (typeof a === "number" || typeof b === "number") {
      if (a === "" || b === "" || a === null || b === null) { return false; }
      return num(a) === num(b);
    }
    return String(a).toLowerCase() === String(b).toLowerCase();
  }
  function apply(op, a, b) {
    switch (op) {
      case "+": return (typeof a === "string" || typeof b === "string")
                       ? String(a) + String(b) : num(a) + num(b);
      case "-": return num(a) - num(b);
      case "*": return num(a) * num(b);
      case "/":
        if (num(b) === 0) { throw new Error(TXT.r_zero); }
        return num(a) / num(b);
      case "mod": case "%":
        if (num(b) === 0) { throw new Error(TXT.r_zero); }
        return num(a) % num(b);
      case "div": return Math.floor(num(a) / num(b));
      case "^": return Math.pow(num(a), num(b));
      case "=": case "==": return same(a, b);
      case "!=": case "<>": return !same(a, b);
      case "<": return num(a) < num(b);
      case "<=": return num(a) <= num(b);
      case ">": return num(a) > num(b);
      case ">=": return num(a) >= num(b);
      case "and": case "&&": return truthy(a) && truthy(b);
      case "or": case "||": return truthy(a) || truthy(b);
      default: throw new Error(say("r_odd_op", { op: op }));
    }
  }

  var BUILT = {
    sqrt: Math.sqrt, abs: Math.abs, round: Math.round, floor: Math.floor,
    ceiling: Math.ceil, ceil: Math.ceil, int: function (v) { return Math.trunc(num(v)); },
    integer: function (v) { return Math.trunc(num(v)); },
    length: function (v) { return String(v).length; },
    toupper: function (v) { return String(v).toUpperCase(); },
    tolower: function (v) { return String(v).toLowerCase(); },
    random: function (a, b) {
      if (a === undefined) { return Math.random(); }
      return Math.floor(Math.random() * (num(b) - num(a) + 1)) + num(a);
    },
    pow: Math.pow, min: Math.min, max: Math.max
  };

  function callOut(name, args, where) {
    var mine = (AST.modules || []).filter(function (m) {
      return m.name.toLowerCase() === name.toLowerCase();
    })[0];
    if (mine) { return runModule(mine, args); }
    var built = BUILT[name.toLowerCase()];
    if (built) { return built.apply(null, args.map(function (a) {
      return typeof a === "string" && !isNaN(parseFloat(a)) ? parseFloat(a) : a;
    })); }
    throw new Error(say("r_unknown", { name: name + "()" }));
  }

  // ---- the run itself ---------------------------------------------------
  function ask(prompt) {                 // what a person has to type in
    if (stopping) { return Promise.resolve(""); }
    return new Promise(function (answer) {
      var row = document.createElement("div");
      row.className = "asking";
      var field = document.createElement("input");
      field.className = "field";
      field.placeholder = prompt || "";
      var go = document.createElement("button");
      go.className = "btn small primary";
      go.textContent = TXT.r_enter;
      function done() {
        var typed = field.value;
        row.replaceWith(Object.assign(document.createElement("div"),
                        { className: "said typed", textContent: "> " + typed }));
        waiting = null;
        answer(typed);
      }
      // Stopped while it sat here waiting to be typed into.  Nothing else
      // would ever settle this promise, so the program hung there with the
      // button still saying Stop: the box goes, and the runner is let go to
      // find that it has been stopped.
      function quit() {
        row.remove();
        waiting = null;
        answer("");
      }
      go.onclick = done;
      field.onkeydown = function (ev) { if (ev.key === "Enter") { done(); } };
      row.appendChild(field);
      row.appendChild(go);
      el("#tape").appendChild(row);
      el("#tape").scrollTop = el("#tape").scrollHeight;
      field.focus();
      waiting = quit;
    });
  }

  function Stop() { this.kind = "stop"; }
  function Returned(v) { this.kind = "return"; this.value = v; }

  function runModule(mod, args) {
    var names = String(mod.params || "").split(",").map(function (p) {
      var bits = p.trim().split(/\s+/);
      return bits[bits.length - 1];
    }).filter(Boolean);
    var where = { vars: {}, steps: 0 };
    names.forEach(function (name, i) { where.vars[name] = args[i]; });
    try {
      walk(mod.body, where, true);
    } catch (thrown) {
      if (thrown instanceof Returned) { return thrown.value; }
      throw thrown;
    }
    return "";
  }

  // The body of a module runs without stopping for breath; the main flow is
  // the one that is watched, step by step.
  function walk(items, where, quiet) {
    for (var i = 0; i < items.length; i++) {
      one(items[i], where, quiet);
    }
  }
  function one(item, where, quiet) {
    where.steps++;
    if (where.steps > STEP_CAP) { throw new Error(TXT.r_forever); }
    switch (item.op) {
      case "declare":
        where.vars[item.var] = item.expr ? value(item.expr, where)
                                         : (/int|real|num|float|double/i.test(item.type) ? 0 : "");
        break;
      case "set": where.vars[item.var] = value(item.expr, where); break;
      case "display": break;
      case "input": break;
      case "call": value(item.text.replace(/^call\s+/i, ""), where); break;
      case "return": throw new Returned(item.expr ? value(item.expr, where) : "");
      case "end": throw new Stop();
      default: break;
    }
  }

  function pieces(parts) {               // Display "a: ", x  ->  the bits of it
    var out = [], deep = 0, quote = null, now = "";
    for (var i = 0; i < parts.length; i++) {
      var c = parts[i];
      if (quote) { now += c; if (c === quote) { quote = null; } continue; }
      if (c === '"' || c === "'") { quote = c; now += c; continue; }
      if (c === "(") { deep++; }
      if (c === ")") { deep--; }
      if (c === "," && !deep) { out.push(now); now = ""; continue; }
      now += c;
    }
    if (now.trim()) { out.push(now); }
    return out;
  }

  function readable(v) {
    if (typeof v === "number") {
      return Math.abs(v - Math.round(v)) < 1e-9 ? String(Math.round(v))
                                                : String(Math.round(v * 1e6) / 1e6);
    }
    if (typeof v === "boolean") { return v ? TXT.yes : TXT.no; }
    return String(v);
  }

  async function runSteps(items, where) {
    for (var i = 0; i < items.length; i++) {
      await tick(where);
      var item = items[i];
      if (item.id) { lightUp(item.id); }
      if (slow()) { await hold(); }
      if (stopping) { throw new Stop(); }
      switch (item.op) {
        case "display":
          talk(pieces(item.parts).map(function (bit) {
            return readable(value(bit, where));
          }).join(""));
          break;
        case "input":
          var typed = await ask(item.text);
          if (stopping) { throw new Stop(); }
          var asNum = parseFloat(typed);
          where.vars[item.var] = (typed.trim() !== "" && !isNaN(asNum) &&
                                  String(asNum) === typed.trim()) ? asNum : typed;
          break;
        case "if":
          if (truthy(value(item.cond, where))) { await runSteps(item.then, where); }
          else { await runSteps(item["else"] || [], where); }
          break;
        case "while":
          while (truthy(value(item.cond, where)) !== !!item.until) {
            await tick(where);
            lightUp(item.id);
            if (slow()) { await hold(); }
            await runSteps(item.body, where);
          }
          break;
        case "dowhile":
          do {
            await tick(where);
            await runSteps(item.body, where);
            lightUp(item.id);
            if (slow()) { await hold(); }
          } while (truthy(value(item.cond, where)) !== !!item.until);
          break;
        case "for":
          if (item.init) { one(statementOf(item.init), where); }
          while (!item.cond || truthy(value(item.cond, where))) {
            await tick(where);
            await runSteps(item.body, where);
            if (item.step) { one(statementOf(item.step), where); }
            if (!item.step) { break; }
          }
          break;
        case "select":
          var pick = value(item.expr, where), went = false;
          for (var c = 0; c < item.cases.length; c++) {
            var label = String(item.cases[c].match || "");
            if (/^(default|case else|else)$/i.test(label.trim())) { continue; }
            if (same(pick, value(label, where))) {
              await runSteps(item.cases[c].body, where);
              went = true;
              break;
            }
          }
          if (!went) {
            for (var d = 0; d < item.cases.length; d++) {
              if (/^(default|case else|else)$/i.test(String(item.cases[d].match || "").trim())) {
                await runSteps(item.cases[d].body, where);
                break;
              }
            }
          }
          break;
        default:
          one(item, where);
      }
    }
  }

  function statementOf(text) {           // "Set i = i + 1" as something to do
    var m = /^(?:set\s+|let\s+)?([A-Za-z_]\w*)\s*(?:=|:=|<-)\s*(.+)$/i.exec(text);
    return m ? { op: "set", var: m[1], expr: m[2] } : { op: "other", text: text };
  }

  function slow() { return el("#r-slow") && el("#r-slow").checked; }
  // Only while it is stepping slowly.  At full speed the chart would be a
  // blur of shapes flying past, which is worse to watch than not moving at
  // all -- so the switch is turned off with the one it depends on, rather
  // than left on offering something it would not really do.
  function following() {
    return slow() && el("#r-follow") && el("#r-follow").checked;
  }
  function dressFollow() {
    var box = el("#r-follow"), row = el("#r-follow-row");
    if (box) { box.disabled = !slow(); }
    if (row) { row.classList.toggle("off", !slow()); }
  }
  if (el("#r-slow")) {
    el("#r-slow").onchange = dressFollow;
    dressFollow();
  }
  if (el("#r-follow")) {
    el("#r-follow").onchange = function () {
      try {
        localStorage.setItem("flowchart-follow",
                             el("#r-follow").checked ? "on" : "off");
      } catch (e) { /* storage turned off: it just starts on again */ }
      if (!el("#r-follow").checked) { markLine(null); }
    };
  }
  function hold() {
    return new Promise(function (go) { setTimeout(go, 260); });
  }

  async function runIt() {
    if (running) {
      stopping = true;
      if (waiting) { waiting(); }        // let go of an Input it is sat at
      return;
    }
    if (!AST || !(AST.main || []).length) { talkOnce(TXT.r_nothing, "bad"); return; }
    running = true; stopping = false; breaths = 0;
    tapeShow("run");                     // whatever was being read, watch this
    tapeSays("r_head", TXT.r_head, "");
    if (following()) { keepView(); }     // to give back at the end of it
    runSays(TXT.r_stop);
    el("#tape").innerHTML = "";
    var where = { vars: {}, steps: 0 };
    try {
      await runSteps(AST.main, where);
      talk(TXT.r_done, "good");
    } catch (thrown) {
      if (thrown instanceof Stop || thrown instanceof Returned) {
        talk(TXT.r_done, "good");
      } else {
        talk(thrown.message || String(thrown), "bad");
      }
    }
    lightUp(null);
    backToView();
    running = false; stopping = false;
    runSays(TXT.r_run);
  }

  // ------------------------------------------- the tape, filling the screen --
  // Everything the runner has to show lands in the tape at the foot of the
  // panel: what the program prints, what it stops to be told, and the same
  // program written out in Python or Java.  That box is about three hundred
  // pixels wide and a few lines tall, which is fine for "Finished." and no
  // good at all for either of the other two -- a line of Java is read
  // sideways a word at a time, and a program that asks four questions has
  // scrolled the first one out of sight by the time it asks the fourth.
  //
  // So the tape can be thrown up over the whole page, the same way the
  // pseudocode can, and by the same means: the very same box is moved into
  // the overlay and moved back again afterwards.  Nothing is copied, so
  // whatever was writing into the tape carries on writing into the one tape
  // there is, whichever side of the screen it is sitting on.

  // What the bar says it is showing.  A word of ours is given by its key as
  // well, so that changing the page's language changes it too; a name that
  // is not ours -- Python, JavaScript -- is given without one, and the key
  // is taken off so nothing later writes over it.
  function tapeSays(key, text, count) {
    var head = el("#tape-title"), says = el("#tape-count");
    if (head) {
      if (key) { head.dataset.w = key; }
      else { delete head.dataset.w; }
      head.textContent = text;
    }
    if (says) { says.textContent = count || ""; }
  }

  // Which of the two the sheet is showing.  The run and the code are two
  // boxes, not one box written over twice: going to the code leaves the run
  // exactly where it was, and coming back finds it still there -- the lines
  // it printed, the answers that were typed into it, the point it stopped
  // at.  Before this, asking for the code threw all of that away, and the
  // only way back to it was to run the program again and type the same
  // answers in a second time.
  function tapeShow(what) {
    var slot = el("#tape-slot"), out = el("#code-out"), back = el("#tape-back");
    if (!slot || !out) { return; }
    var code = what === "code";
    slot.hidden = code;
    out.hidden = !code;
    if (back) { back.hidden = !code; }
  }

  // A newly built chart is a new program: neither what the last one printed
  // nor the code the last one was written out as belongs to it.
  function freshTape() {
    if (el("#tape")) { el("#tape").innerHTML = ""; }
    if (el("#code-out")) { el("#code-out").innerHTML = ""; }
    tapeShow("run");
    tapeSays("r_head", TXT.r_head, "");
  }

  function tapeFull(want) {
    var box = el("#tape"), over = el("#tape-over"), home = el("#runner");
    if (!box || !over || !home) { return; }
    if (want && over.hidden) {
      codeFull(false);                   // one screen at a time
      over.hidden = false;
      el("#tape-slot").appendChild(box);
      document.body.classList.add("tape-full");
      // An empty screen with a bar across the top and nothing under it
      // looks broken rather than ready, so it says what it is for.  The
      // line goes again the moment anything real is put there, and is not
      // left behind in the panel afterwards.
      if (!box.firstChild) { talk(TXT.r_hint, "note").classList.add("hint-line"); }
    } else if (!want && !over.hidden) {
      all(".hint-line", box).forEach(function (line) { line.remove(); });
      // The tape is what goes back to the panel, so the tape is what the
      // screen is left on: open it again and you find what the panel was
      // showing, not a page of code you had finished with.  The code is a
      // press away and is written out afresh each time anyway.
      tapeShow("run");
      tapeSays("r_head", TXT.r_head, "");
      over.hidden = true;
      home.appendChild(box);
      document.body.classList.remove("tape-full");
    }
    var button = el("#run-big");
    if (button) {
      button.setAttribute("aria-expanded", want ? "true" : "false");
      button.title = want ? (TXT.code_small || "") : (TXT.code_big || "");
    }
  }

  if (el("#run-big")) {
    el("#run-big").onclick = function () { tapeFull(el("#tape-over").hidden); };
    el("#tape-done").onclick = function () { tapeFull(false); };
    el("#tape-back").onclick = function () {
      tapeShow("run");
      tapeSays("r_head", TXT.r_head, "");
    };
    el("#tape-run").onclick = runIt;
    el("#tape-code").onclick = function (ev) {
      ev.stopPropagation();              // or the same click shuts the menu
      askWhichCode(el("#tape-code"));
    };
    // Escape belongs to the menu while there is one: the language list is
    // opened from this very bar, and pulling the screen out from under it
    // would take away the thing that was being answered.  This part runs
    // before the menu's own part does, so it is this one that stands aside.
    window.addEventListener("keydown", function (ev) {
      if (ev.key !== "Escape" || el(".menu:not(.out)")) { return; }
      if (el("#tape-over") && !el("#tape-over").hidden) { tapeFull(false); }
    });
  }

  // ========================================================= as real code ==
  // The same program, written out in whichever language you are working in.
  // It comes from the same data the runner walks, so what you read here is
  // what you just watched happen.
  function tree(src) {                   // an expression, as a little tree
    var ts = tokens(src), at = 0;
    function peek() { return ts[at]; }
    function take() { return ts[at++]; }
    function primary() {
      var tok = take();
      if (!tok) { return { lit: '""' }; }
      if (tok.t === "num") { return { lit: String(tok.v) }; }
      if (tok.t === "str") { return { str: tok.v }; }
      if (tok.t === "op" && tok.v === "(") {
        var inside = expr(0);
        if (peek() && peek().v === ")") { take(); }
        return { group: inside };
      }
      if (tok.t === "op" && (tok.v === "-" || tok.v === "+")) {
        return { unary: tok.v, of: primary() };
      }
      if (tok.t === "name") {
        var low = String(tok.v).toLowerCase();
        if (low === "not") { return { unary: "not", of: primary() }; }
        if (low === "true" || low === "false") { return { bool: low === "true" }; }
        if (peek() && peek().v === "(") {
          take();
          var args = [];
          if (peek() && peek().v !== ")") {
            args.push(expr(0));
            while (peek() && peek().v === ",") { take(); args.push(expr(0)); }
          }
          if (peek() && peek().v === ")") { take(); }
          return { call: String(tok.v), args: args };
        }
        return { name: String(tok.v) };
      }
      return { lit: "0" };
    }
    function expr(least) {
      var left = primary();
      while (peek()) {
        var tok = peek();
        var op = tok.t === "op" ? tok.v : String(tok.v).toLowerCase();
        var rank = RANK[op];
        if (!rank || rank < least) { break; }
        take();
        left = { op: op, left: left, right: expr(rank + 1) };
      }
      return left;
    }
    return expr(0);
  }

  var CODE_LANG = {
    python: { ext: "py", semi: "", open: ":", shut: "", tab: "    ",
              and: "and", or: "or", not: "not ", eq: "==", ne: "!=",
              pow: "**", mod: "%" },
    java: { ext: "java", semi: ";", open: " {", shut: "}", tab: "    ",
            and: "&&", or: "||", not: "!", eq: "==", ne: "!=",
            pow: null, mod: "%" },
    csharp: { ext: "cs", semi: ";", open: " {", shut: "}", tab: "    ",
              and: "&&", or: "||", not: "!", eq: "==", ne: "!=",
              pow: null, mod: "%" },
    javascript: { ext: "js", semi: ";", open: " {", shut: "}", tab: "  ",
                  and: "&&", or: "||", not: "!", eq: "===", ne: "!==",
                  pow: "**", mod: "%" }
  };
  var TYPES = {
    python: {},
    java: { integer: "int", int: "int", real: "double", float: "double",
            double: "double", string: "String", char: "char",
            boolean: "boolean", bool: "boolean", "": "double" },
    csharp: { integer: "int", int: "int", real: "double", float: "double",
              double: "double", string: "string", char: "char",
              boolean: "bool", bool: "bool", "": "double" },
    javascript: {}
  };

  function asCode(node, lang) {
    var L = CODE_LANG[lang];
    if (node.lit !== undefined) { return node.lit; }
    if (node.str !== undefined) { return '"' + node.str.replace(/"/g, '\\"') + '"'; }
    if (node.bool !== undefined) {
      if (lang === "python") { return node.bool ? "True" : "False"; }
      return node.bool ? "true" : "false";
    }
    if (node.name) { return node.name; }
    if (node.group) { return "(" + asCode(node.group, lang) + ")"; }
    if (node.unary) {
      var mark = node.unary === "not" ? L.not : node.unary;
      return mark + asCode(node.of, lang);
    }
    if (node.call) {
      return node.call + "(" + node.args.map(function (a) {
        return asCode(a, lang);
      }).join(", ") + ")";
    }
    var a = asCode(node.left, lang), b = asCode(node.right, lang);
    var op = node.op;
    if (op === "^") {
      return L.pow ? a + " " + L.pow + " " + b : "Math.pow(" + a + ", " + b + ")";
    }
    var says = { "=": L.eq, "==": L.eq, "!=": L.ne, "<>": L.ne,
                 "and": L.and, "&&": L.and, "or": L.or, "||": L.or,
                 "mod": L.mod, "div": "/" };
    return a + " " + (says[op] || op) + " " + b;
  }

  function saying(parts, lang) {         // the bits of a Display, joined up
    var bits = pieces(parts).map(function (bit) { return tree(bit); });
    if (!bits.length) { return lang === "python" ? '""' : '""'; }
    return bits.map(function (bit, i) {
      var code = asCode(bit, lang);
      if (lang === "python" && bit.str === undefined) { return "str(" + code + ")"; }
      if (lang !== "python" && i === 0 && bit.str === undefined) {
        return '"" + ' + code;
      }
      return code;
    }).join(" + ");
  }

  function codeFor(lang) {
    var L = CODE_LANG[lang], out = [], kinds = {};
    function line(deep, text) { out.push(L.tab.repeat(deep) + text); }

    function typed(name) {
      var want = TYPES[lang][(kinds[name] || "").toLowerCase()];
      return want || TYPES[lang][""] || "";
    }
    function block(items, deep) {
      items.forEach(function (item) { each(item, deep); });
      if (!items.length) {
        line(deep, lang === "python" ? "pass" : "// nothing here");
      }
    }
    function shut(deep) { if (L.shut) { line(deep, L.shut); } }

    function each(item, deep) {
      var semi = L.semi;
      switch (item.op) {
        case "declare":
          kinds[item.var] = item.type || "";
          var start = item.expr ? asCode(tree(item.expr), lang)
                    : (/int|real|num|float|double/i.test(item.type) ? "0" : '""');
          if (lang === "python") {
            line(deep, item.var + " = " + start);
          } else if (lang === "javascript") {
            line(deep, (item.const ? "const " : "let ") + item.var + " = " + start + semi);
          } else {
            line(deep, (item.const ? (lang === "java" ? "final " : "const ") : "") +
                       typed(item.var) + " " + item.var + " = " + start + semi);
          }
          break;
        case "set":
          line(deep, item.var + " = " + asCode(tree(item.expr), lang) + semi);
          break;
        case "display":
          var said = saying(item.parts, lang);
          if (lang === "python") { line(deep, "print(" + said + ")"); }
          else if (lang === "java") { line(deep, "System.out.println(" + said + ");"); }
          else if (lang === "csharp") { line(deep, "Console.WriteLine(" + said + ");"); }
          else { line(deep, "console.log(" + said + ");"); }
          break;
        case "input":
          var kind = (kinds[item.var] || "").toLowerCase();
          var whole = /^(integer|int)$/.test(kind), real = /^(real|float|double|number)$/.test(kind);
          if (lang === "python") {
            var wrap = whole ? "int(input())" : real ? "float(input())" : "input()";
            line(deep, item.var + " = " + wrap);
          } else if (lang === "java") {
            line(deep, item.var + " = in." + (whole ? "nextInt()" : real ? "nextDouble()" : "nextLine()") + ";");
          } else if (lang === "csharp") {
            var read = "Console.ReadLine()";
            line(deep, item.var + " = " + (whole ? "int.Parse(" + read + ")"
                      : real ? "double.Parse(" + read + ")" : read) + ";");
          } else {
            line(deep, item.var + " = " + (whole || real ? "Number(prompt(\"\"))" : "prompt(\"\")") + ";");
          }
          break;
        case "call":
          line(deep, item.name + "(" + item.args + ")" + semi);
          break;
        case "return":
          line(deep, "return" + (item.expr ? " " + asCode(tree(item.expr), lang) : "") + semi);
          break;
        case "if":
          line(deep, "if " + wrapped(item.cond, lang) + L.open);
          block(item.then, deep + 1);
          shut(deep);
          if ((item["else"] || []).length) {
            if (lang === "python") { line(deep, "else:"); }
            else { line(deep, "else" + L.open); }
            block(item["else"], deep + 1);
            shut(deep);
          }
          break;
        case "while":
          var test = item.until ? "not (" + asCode(tree(item.cond), lang) + ")"
                                : asCode(tree(item.cond), lang);
          if (item.until && lang !== "python") { test = L.not + "(" + asCode(tree(item.cond), lang) + ")"; }
          line(deep, "while " + (lang === "python" ? test : "(" + test + ")") + L.open);
          block(item.body, deep + 1);
          shut(deep);
          break;
        case "dowhile":
          if (lang === "python") {
            line(deep, "while True:");
            block(item.body, deep + 1);
            line(deep + 1, "if " + (item.until ? "" : "not ") +
                 "(" + asCode(tree(item.cond), lang) + "):");
            line(deep + 2, "break");
          } else {
            line(deep, "do" + L.open);
            block(item.body, deep + 1);
            line(deep, "} while (" + (item.until ? L.not : "") +
                 "(" + asCode(tree(item.cond), lang) + "));");
          }
          break;
        case "for":
          var set = statementOf(item.init), step = statementOf(item.step);
          if (lang === "python") {
            line(deep, "# " + item.raw);
            each({ op: "set", var: set.var, expr: set.expr }, deep);
            line(deep, "while " + asCode(tree(item.cond), lang) + ":");
            block(item.body, deep + 1);
            each({ op: "set", var: step.var, expr: step.expr }, deep + 1);
          } else {
            line(deep, "for (" + (lang === "javascript" ? "let " : typed(set.var) + " ") +
                 set.var + " = " + asCode(tree(set.expr), lang) + "; " +
                 asCode(tree(item.cond), lang) + "; " + step.var + " = " +
                 asCode(tree(step.expr), lang) + ")" + L.open);
            block(item.body, deep + 1);
            shut(deep);
          }
          break;
        case "select":
          if (lang === "python") {
            item.cases.forEach(function (one, i) {
              var label = String(one.match || "");
              if (/^(default|case else|else)$/i.test(label.trim())) {
                line(deep, "else:");
              } else {
                line(deep, (i ? "elif " : "if ") + item.expr + " == " +
                     asCode(tree(label), lang) + ":");
              }
              block(one.body, deep + 1);
            });
          } else {
            line(deep, "switch (" + asCode(tree(item.expr), lang) + ")" + L.open);
            item.cases.forEach(function (one) {
              var label = String(one.match || "");
              if (/^(default|case else|else)$/i.test(label.trim())) {
                line(deep + 1, "default:");
              } else {
                line(deep + 1, "case " + asCode(tree(label), lang) + ":");
              }
              block(one.body, deep + 2);
              line(deep + 2, "break;");
            });
            shut(deep);
          }
          break;
        case "start": case "end": break;
        default:
          line(deep, (lang === "python" ? "# " : "// ") + item.text);
      }
    }
    function wrapped(cond, lang) {
      var code = asCode(tree(cond), lang);
      return lang === "python" ? code : "(" + code + ")";
    }
    function params(list) {
      return String(list || "").split(",").map(function (p) {
        var bits = p.trim().split(/\s+/).filter(Boolean);
        if (!bits.length) { return ""; }
        var name = bits[bits.length - 1];
        if (lang === "python" || lang === "javascript") { return name; }
        var kind = bits.length > 1 ? bits[0].toLowerCase() : "";
        return (TYPES[lang][kind] || TYPES[lang][""]) + " " + name;
      }).filter(Boolean).join(", ");
    }

    var mods = AST.modules || [];
    if (lang === "python") {
      line(0, "# " + (el("#f-title").value || TXT.untitled));
      mods.forEach(function (mod) {
        line(0, "");
        line(0, "def " + mod.name + "(" + params(mod.params) + "):");
        block(mod.body, 1);
      });
      line(0, "");
      block(AST.main, 0);
    } else if (lang === "javascript") {
      line(0, "// " + (el("#f-title").value || TXT.untitled));
      mods.forEach(function (mod) {
        line(0, "");
        line(0, "function " + mod.name + "(" + params(mod.params) + ") {");
        block(mod.body, 1);
        line(0, "}");
      });
      line(0, "");
      block(AST.main, 0);
    } else {
      var name = (el("#f-title").value || "").replace(/[^A-Za-z0-9]/g, "") || "Program";
      if (lang === "csharp" && name === "Main") { name = "Program"; }
      codeFor.className = name;          // what the file should be called
      if (lang === "java") {
        line(0, "import java.util.Scanner;");
        line(0, "");
        line(0, "public class " + name + " {");
        line(1, "static Scanner in = new Scanner(System.in);");
        line(0, "");
        line(1, "public static void main(String[] args) {");
        block(AST.main, 2);
        line(1, "}");
        mods.forEach(function (mod) {
          line(0, "");
          line(1, "static " + (TYPES.java[(mod.returns || "").toLowerCase()] || "void") +
               " " + mod.name + "(" + params(mod.params) + ") {");
          block(mod.body, 2);
          line(1, "}");
        });
        line(0, "}");
      } else {
        line(0, "using System;");
        line(0, "");
        line(0, "class " + name + " {");
        line(1, "static void Main() {");
        block(AST.main, 2);
        line(1, "}");
        mods.forEach(function (mod) {
          line(0, "");
          line(1, "static " + (TYPES.csharp[(mod.returns || "").toLowerCase()] || "void") +
               " " + mod.name + "(" + params(mod.params) + ") {");
          block(mod.body, 2);
          line(1, "}");
        });
        line(0, "}");
      }
    }
    return out.join("\n");
  }

  // Ask which language, unless the runner is already set to one.  Before
  // this, the only way to see the code was to change what the runner was set
  // to first, which is a strange thing to have to do when all you wanted was
  // the code.  Now the button always gives you it and asks if it needs to.
  function langName(lang) {              // Python, C# -- as the list says it
    var pick = el("#r-lang");
    for (var i = 0; pick && i < pick.options.length; i++) {
      if (pick.options[i].value === lang) { return pick.options[i].text; }
    }
    return lang;
  }

  function askWhichCode(where) {
    if (!AST || !(AST.main || []).length) {
      tapeShow("run");                   // it is said in the tape, so show it
      talkOnce(TXT.r_nothing, "bad");
      return;
    }
    var lang = el("#r-lang") ? el("#r-lang").value : "pseudo";
    if (lang !== "pseudo") { showCode(lang); return; }
    var pick = el("#r-lang");
    var choices = [];
    for (var i = 0; pick && i < pick.options.length; i++) {
      if (pick.options[i].value === "pseudo") { continue; }
      choices.push({ value: pick.options[i].value, name: pick.options[i].text });
    }
    // The button is a switch for its own list: pressed while the list is up
    // it puts it away again, rather than shutting it and opening an
    // identical one in the same place -- which looks like nothing happened.
    if (el(".menu:not(.out)")) { closeMenu(); return; }
    var box = (where || el("#see-code")).getBoundingClientRect();
    openMenu(box.left, box.bottom + 6, choices.map(function (one) {
      return { name: one.name, go: function () { showCode(one.value); } };
    }));
  }

  function showCode(want) {
    var lang = want || (el("#r-lang") ? el("#r-lang").value : "pseudo");
    if (!AST || !(AST.main || []).length) {
      tapeShow("run");
      talkOnce(TXT.r_nothing, "bad");
      return;
    }
    if (lang === "pseudo") {
      tapeShow("run");
      talkOnce(TXT.r_pseudo_only, "note");
      return;
    }
    var text;
    try { text = codeFor(lang); }
    catch (thrown) {
      tapeShow("run");
      talkOnce(thrown.message || String(thrown), "bad");
      return;
    }
    // Into its own box, not over the top of the run.  The tape keeps what
    // the program did; this is only what it says.
    var out = el("#code-out");
    out.innerHTML = "";
    var pre = document.createElement("pre");
    pre.className = "code";
    pre.textContent = text;
    out.appendChild(pre);
    var row = document.createElement("div");
    row.className = "go";
    row.style.cssText = "display:flex; gap:8px; margin-top:8px";
    var copy = document.createElement("button");
    copy.className = "btn small";
    copy.textContent = TXT.r_copy;
    copy.onclick = function () {
      navigator.clipboard.writeText(text).then(function () {
        copy.textContent = TXT.r_copied;
        setTimeout(function () { copy.textContent = TXT.r_copy; }, 1400);
      });
    };
    var down = document.createElement("button");
    down.className = "btn small";
    down.textContent = TXT.r_save_code;
    down.onclick = function () {
      var name = (lang === "java" || lang === "csharp") && codeFor.className
               ? codeFor.className
               : (el("#f-title").value || "flowchart").replace(/[^A-Za-z0-9 _-]/g, "");
      save(new Blob([text], { type: "text/plain;charset=utf-8" }),
           name + "." + CODE_LANG[lang].ext);
    };
    row.appendChild(copy);
    row.appendChild(down);
    out.appendChild(row);
    // Code is the thing the panel has least room for: `pre` does not wrap,
    // so a line of Java in a column that narrow is read sideways a word at
    // a time.  Asking for it is therefore taken as asking to read it, and
    // it is put where it can be read.  Esc or Done gives the panel back.
    tapeFull(true);
    tapeShow("code");
    tapeSays("", langName(lang),
             say("code_lines", { n: text.split("\n").length }));
  }



  // ------------------------------------------------------- keeping a copy --
  // Everything that makes this chart what it is, in one small file: the
  // pseudocode or the shapes you placed, the colours, and which shape draws
  // which kind of step.  Open it again here and you are back where you were.
  function projectJson() {
    return JSON.stringify({
      what: "flowchart-builder", version: 1,
      mode: byHand ? "hand" : "code",
      hand: hand,
      source: el("#code") ? {
        code: el("#code").value, title: el("#f-title").value,
        author: el("#f-author").value, shape: el("#f-shape").value,
        legend: el("#f-legend").checked, grid: el("#f-grid").checked
      } : null,
      style: style, geom: geom
    }, null, 1);
  }

  function saveProject() {
    var name = (el("#f-title") && el("#f-title").value) || FILE || "flowchart";
    save(new Blob([projectJson()], { type: "application/json" }),
         name.replace(/[^A-Za-z0-9 _-]/g, "") + ".flowchart.json");
  }

  function openProject(text) {
    var was;
    try { was = JSON.parse(text); } catch (e) { was = null; }
    if (!was || was.what !== "flowchart-builder") {
      talk(TXT.f_not_ours, "bad");
      return;
    }
    if (was.style) { style = was.style; }
    if (was.geom) { geom = was.geom; drawRoles(); }
    if (was.source && el("#code")) {
      el("#code").value = was.source.code || "";
      el("#f-title").value = was.source.title || "";
      el("#f-author").value = was.source.author || "";
      if (was.source.shape) { el("#f-shape").value = was.source.shape; }
      el("#f-legend").checked = !!was.source.legend;
      el("#f-grid").checked = was.source.grid !== false;
    }
    if (was.hand && was.hand.nodes) { hand = was.hand; }
    picked = chosen = null;
    if (was.mode === "hand") {
      setMode(true);
    } else {
      setMode(false);
      if (el("#code").value.trim()) { el("#build").click(); }
    }
    buildGlobals();
    paint();
  }

  // ----------------------------------------------------- the right button --
  // Everything you can do to a shape or an arrow, where the thing itself is,
  // instead of over in the panel.
  function closeMenu() {
    all(".menu").forEach(function (m) { m.remove(); });
  }
  document.addEventListener("click", function (ev) {
    if (!ev.target.closest || !ev.target.closest(".menu")) { closeMenu(); }
  });
  window.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") { closeMenu(); }
  });

  function openMenu(x, y, items) {
    closeMenu();
    var menu = document.createElement("div");
    menu.className = "menu";
    items.forEach(function (item) {
      if (item === "-") {
        menu.appendChild(document.createElement("hr"));
        return;
      }
      var row = document.createElement("button");
      row.type = "button";
      row.style.position = "relative";
      row.innerHTML = (item.swatch
                       ? '<span class="dot" style="background:' + item.swatch + '"></span>'
                       : (item.mark || "")) +
                      "<span>" + item.name + "</span>";
      row.onclick = function (ev) {
        ev.stopPropagation();
        if (!item.keepOpen) { closeMenu(); }
        item.go(row);
      };
      menu.appendChild(row);
    });
    document.body.appendChild(menu);
    var room = menu.getBoundingClientRect();
    menu.style.left = Math.min(x, innerWidth - room.width - 8) + "px";
    menu.style.top = Math.min(y, innerHeight - room.height - 8) + "px";
  }

  // Picking a colour from the menu.  The row carries a swatch of what it is
  // now; pressing it opens the machine's own colour picker, and the shape
  // takes the colour as you move about in it, so you can see what you are
  // choosing before you settle on it.
  function paintRow(name, now, fallback, onPick) {
    return { swatch: now || fallback, name: name, keepOpen: true,
             go: function (row) {
               var pick = document.createElement("input");
               pick.type = "color";
               pick.value = now || fallback;
               pick.style.cssText = "position:absolute;opacity:0;pointer-events:none";
               // It lives inside the row, so its own click would bubble back
               // to the row and open another one, and another, until the
               // stack gave out.  It stops here.
               pick.addEventListener("click", function (e) { e.stopPropagation(); });
               row.appendChild(pick);
               pick.oninput = function () {
                 onPick(pick.value);
                 var dot = row.querySelector(".dot");
                 if (dot) { dot.style.background = pick.value; }
               };
               pick.onchange = function () { setTimeout(function () { pick.remove(); }, 0); };
               pick.click();
             } };
  }

  function colourRows(which, mine, fallbacks) {
    var first = true;
    function set(key, value) {
      if (first) { first = false; keepUndo(); }   // one step for one choice
      mine[key] = value;
      style.nodes[which] = mine;
      paint();
      keep();
    }
    return [
      paintRow(TXT.c_fill || "Fill", mine.fill, fallbacks.fill,
               function (v) { set("fill", v); }),
      paintRow(TXT.c_line || "Border", mine.line, fallbacks.line,
               function (v) { set("line", v); }),
      paintRow(TXT.c_words || "Words", mine.text, fallbacks.text,
               function (v) { set("text", v); }),
      { name: TXT.c_clear || "No colour of its own", go: function () {
          delete mine.fill; delete mine.line; delete mine.text;
          style.nodes[which] = mine;
          paint();
          keep();
        } }
    ];
  }

  function shapeMenu(node, x, y) {
    picked = node.id;
    chosen = null;
    drawHand();
    drawHandPanel();
    openMenu(x, y, [
      { name: TXT.m_type, go: function () {
          var g = el('.node[data-i="h' + node.id + '"]', chart);
          if (g) { typeInto(g); }
        } },
      { name: TXT.connect, go: function () { joining = true; drawHandPanel(); } },
      { name: TXT.m_copy, go: function () {
          keepUndo();
          var twin = JSON.parse(JSON.stringify(node));
          twin.id = hand.next++;
          twin.x += 30; twin.y += 30;
          hand.nodes.push(twin);
          picked = twin.id;
          drawHand(); drawHandPanel();
        } },
      { name: TXT.m_turn, go: function () {
          keepUndo();
          node.turn = ((node.turn || 0) + 90) % 360;
          drawHand(); drawHandPanel();
        } },
      "-"
    ].concat(colourRows("h" + node.id, style.nodes["h" + node.id] || {},
                        { fill: "#ffffff", line: style.ink || "#000000",
                          text: style.words || style.ink || "#000000" }))
     .concat([
      "-",
      { name: TXT.delete, go: function () {
          hand.nodes = hand.nodes.filter(function (n) { return n.id !== node.id; });
          hand.links = hand.links.filter(function (l) {
            return l.from !== node.id && l.to !== node.id;
          });
          picked = null;
          drawHand(); drawHandPanel(); showReport();
        } }
    ]));
  }

  function arrowMenu(link, x, y) {
    chosen = link.id;
    picked = null;
    drawHand();
    drawHandPanel();
    function tag(word) {
      return { name: word === "" ? TXT.m_no_word : '"' + word + '"',
               go: function () { link.label = word; drawHand(); drawHandPanel(); } };
    }
    openMenu(x, y, [
      tag(TXT.yes), tag(TXT.no), tag(""),
      "-",
      { name: link.dash ? TXT.m_solid : TXT.dashed, go: function () {
          link.dash = !link.dash; drawHand(); drawHandPanel();
        } },
      { name: TXT.turn_it_round, go: function () {
          var was = link.from; link.from = link.to; link.to = was;
          drawHand(); drawHandPanel(); showReport();
        } },
      "-",
      { name: TXT.delete, go: function () {
          hand.links = hand.links.filter(function (l) { return l !== link; });
          chosen = null;
          drawHand(); drawHandPanel(); showReport();
        } }
    ]);
  }

  function paperMenu(x, y) {
    var spots = ["rect", "oval", "io", "diamond", "text"];
    openMenu(x, y, spots.map(function (kind) {
      return { mark: keyMark(kind), name: kindName(kind),
               go: function () { addNode(kind); } };
    }).concat([
      "-",
      { name: TXT.m_fit, go: function () { el("#fit").click(); } }
    ]));
  }

  // ---------------------------------------------- typing straight into it --
  // Double-click a shape and the words in it are there to be typed over:
  // in a chart you drew by hand, in the shape itself; in one built from
  // pseudocode, in the line of pseudocode it came from, because that is
  // where those words actually live.
  var lineOf = {};                       // shape number -> line of pseudocode

  // A box being typed into closes when you go elsewhere.  Leaning on blur
  // alone is not quite enough: a box that never gets focus never loses it,
  // and one left open sits over the chart swallowing everything aimed at
  // what is underneath.  So a press anywhere outside puts it away as well.
  function closeOnOutside(pad, finish) {
    function away(ev) {
      if (ev.target === pad || pad.contains(ev.target)) { return; }
      document.removeEventListener("pointerdown", away, true);
      finish();
    }
    setTimeout(function () {
      document.addEventListener("pointerdown", away, true);
    }, 0);
    return function () { document.removeEventListener("pointerdown", away, true); };
  }

  function noteLines(items) {
    (items || []).forEach(function (item) {
      if (item.id && item.line) { lineOf[item.id] = item.line; }
      ["then", "else", "body"].forEach(function (key) {
        if (item[key]) { noteLines(item[key]); }
      });
      (item.cases || []).forEach(function (one) { noteLines(one.body); });
    });
  }

  // Typing happens in the shape, not in a box floating over it.  The words
  // that were drawn there are taken away and a writing space is put in their
  // place, inside the shape's own group -- so it keeps the shape's size, its
  // middle, its colours and whatever turn it has been given, and what you see
  // while you type is what you will have when you stop.
  function typeInto(g) {
    var node = nodeById(+g.dataset.i.slice(1));
    if (!node) { return; }
    all(".edit-box").forEach(function (old) { old.remove(); });   // one at a time
    var gone = el(".typing-here", el("#chart"));
    if (gone) { gone.remove(); }

    keepUndo();
    var about = turned(node);
    var pad = Math.min(14, about.w * 0.1);
    var wide = Math.max(24, about.w - pad * 2);
    var tall = Math.max(18, about.h - 8);
    var slot = document.createElementNS("http://www.w3.org/2000/svg", "foreignObject");
    slot.setAttribute("class", "typing-here");
    slot.setAttribute("x", node.x - wide / 2);
    slot.setAttribute("y", node.y - tall / 2);
    slot.setAttribute("width", wide);
    slot.setAttribute("height", tall);

    var space = document.createElement("div");
    space.setAttribute("xmlns", "http://www.w3.org/1999/xhtml");
    space.className = "writing";
    space.contentEditable = "true";
    space.spellcheck = false;
    space.textContent = node.text || "";
    var ink = (style.nodes["h" + node.id] || {}).text ||
              (style.kinds[node.kind] || {}).text || style.words || style.ink || "#000000";
    space.style.color = ink;
    slot.appendChild(space);

    all("text", g).forEach(function (t) { t.style.display = "none"; });
    g.appendChild(slot);

    // put the cursor at the end of what is there
    var pick = document.createRange();
    pick.selectNodeContents(space);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(pick);
    space.focus();

    var shut;
    function done() {
      if (!slot.parentNode) { return; }  // already put away
      if (shut) { shut(); }
      node.text = space.textContent.replace(/\s+$/, "");
      slot.remove();
      measure(node);
      drawHand();
      drawHandPanel();
    }
    shut = closeOnOutside(space, done);
    space.onblur = done;
    space.onkeydown = function (ev) {
      ev.stopPropagation();              // the shortcuts stay out of the way
      if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); space.blur(); }
      if (ev.key === "Escape") { space.textContent = node.text || ""; space.blur(); }
    };
  }

  // The same thing for an arrow: double-click it and the word on it -- Yes,
  // No, whatever it should say -- is there to be typed, where the arrow is,
  // rather than hunted for in the panel.
  function typeOnLink(link) {
    if (!link) { return; }
    all(".edit-box").forEach(function (old) { old.remove(); });
    var a = nodeById(link.from), b = nodeById(link.to);
    if (!a || !b) { return; }
    keepUndo();
    var pts = linkPath(a, b);
    var mid = pts[Math.floor(pts.length / 2)];
    var svg = el("#chart");
    var frame = svg.getScreenCTM();
    var spot = svg.createSVGPoint();
    spot.x = mid[0];
    spot.y = mid[1];
    spot = spot.matrixTransform(frame);
    var stage = el("#stage"), room = stage.getBoundingClientRect();
    var pad = document.createElement("input");
    pad.type = "text";
    pad.className = "edit-box on-line";
    pad.value = link.label || "";
    pad.placeholder = TXT.word_on_it || "";
    pad.style.left = (spot.x - room.left + stage.scrollLeft - 54) + "px";
    pad.style.top = (spot.y - room.top + stage.scrollTop - 15) + "px";
    pad.style.width = "108px";
    stage.appendChild(pad);
    pad.focus();
    pad.select();
    var shut;
    function done() {
      if (!pad.parentNode) { return; }
      if (shut) { shut(); }
      link.label = pad.value.trim();
      pad.remove();
      drawHand();
      drawHandPanel();
    }
    shut = closeOnOutside(pad, done);
    pad.onblur = done;
    pad.onkeydown = function (ev) {
      if (ev.key === "Enter") { ev.preventDefault(); pad.blur(); }
      if (ev.key === "Escape") { pad.value = link.label || ""; pad.blur(); }
      ev.stopPropagation();              // the shortcuts stay out of the way
    };
  }

  // Where a line of the pseudocode actually sits in the box, and how tall it
  // is there.  Counting lines and multiplying by the height of one is wrong
  // the moment a line is too long for the column and wraps -- which, in a
  // panel this narrow, is most of them: everything under a wrapped line sits
  // a row lower than the count says, and the further down the further out.
  // It used to be worse than that again, being counted in eighteens against
  // type set on twenty.
  //
  // So the words above the line are laid out a second time, in a box of the
  // same width set in the same type, and the height that comes back is the
  // answer.  One hidden box is kept for it and used over and over; it is
  // measured a few times a second at the very worst, which is nothing.
  var ruler = null;
  function lineSpan(code, at) {
    var lines = code.value.split("\n");
    if (!code.clientWidth || at < 1 || at > lines.length) { return null; }
    var face = getComputedStyle(code);
    if (!ruler) {
      ruler = document.createElement("div");
      ruler.setAttribute("aria-hidden", "true");
      ruler.style.cssText = "position:absolute;left:-9999px;top:0;visibility:hidden";
      document.body.appendChild(ruler);
    }
    ruler.style.font = face.font;
    ruler.style.lineHeight = face.lineHeight;
    ruler.style.letterSpacing = face.letterSpacing;
    ruler.style.whiteSpace = face.whiteSpace;
    ruler.style.overflowWrap = face.overflowWrap;
    ruler.style.wordBreak = face.wordBreak;
    ruler.style.tabSize = face.tabSize;
    ruler.style.width = (code.clientWidth - parseFloat(face.paddingLeft)
                                          - parseFloat(face.paddingRight)) + "px";
    // A zero-width space on the end, so that words ending in a newline still
    // have a last row to be measured by.  Without it the box stops at the row
    // above and every answer comes back one line short.
    var one = parseFloat(face.lineHeight) || 20;
    var above = lines.slice(0, at - 1).join("\n");
    ruler.textContent = (above ? above + "\n" : "") + "​";
    var top = ruler.offsetHeight - one;
    ruler.textContent = (above ? above + "\n" : "") + lines[at - 1] + "​";
    return { top: top, tall: Math.max(one, ruler.offsetHeight - one - top) };
  }

  // A line put in the middle of what can be seen of the box -- as near to the
  // middle as it can be got, there being nothing above the first line to
  // scroll out of the way.
  function showLine(code, at) {
    var span = lineSpan(code, at);
    if (!span) { return; }
    code.scrollTop = Math.max(0, span.top + span.tall / 2 - code.clientHeight / 2);
  }

  function pickLine(id) {
    var at = lineOf[id], code = el("#code");
    if (!at || !code) { return; }
    var lines = code.value.split("\n");
    var from = 0;
    for (var i = 0; i < at - 1 && i < lines.length; i++) { from += lines[i].length + 1; }
    var to = from + (lines[at - 1] || "").length;
    code.focus();
    code.setSelectionRange(from, to);
    showLine(code, at);
  }

/* eslint-disable no-undef */

  // ---------------------------------------------------- which side it sits --
  // The panel starts on the left because that is where a page's furniture
  // usually goes, but a chart is read left to right and grows to the right,
  // so on a wide screen the panel is often in the way of the thing it is
  // describing.  Moving it is one attribute; the stylesheet does the rest.
  var SIDES = ["left", "right"];
  var panelSide = "left";                // which hand the panel sits on

  function wearSide() {
    if (panelSide === "right") { document.body.setAttribute("data-side", "right"); }
    else { document.body.removeAttribute("data-side"); }
    all("#side-seg .seg-btn").forEach(function (b) {
      b.classList.toggle("on", b.dataset.side === panelSide);
    });
    try { localStorage.setItem("flowchart-panel-side", panelSide); }
    catch (e) { /* fine */ }
  }

  function setSide(want) {
    panelSide = SIDES.indexOf(want) >= 0 ? want : "left";
    wearSide();
  }

  try {
    var keptSide = localStorage.getItem("flowchart-panel-side");
    if (SIDES.indexOf(keptSide) >= 0) { panelSide = keptSide; }
  } catch (e) { /* no storage: left it is */ }

  // ------------------------------------------------------- filling the screen --
  // Browsers only grant this from something the person actually pressed, so
  // it is never asked for on the way in and never remembered: it is a thing
  // you do, not a setting you keep.  Where the browser has no full screen at
  // all -- an iPhone, mostly -- the row is taken out rather than left there
  // doing nothing.
  function fullNow() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement);
  }
  function canFull() {
    var root = document.documentElement;
    return !!(root.requestFullscreen || root.webkitRequestFullscreen);
  }

  function wearFull() {
    var on = fullNow();
    var tick = el("#full-on");
    if (tick) { tick.checked = on; }
    var mark = el("#full-mark");
    if (mark) {
      mark.innerHTML = on
        ? '<path d="M2.5 7.5h5v-5M17.5 7.5h-5v-5M2.5 12.5h5v5M17.5 12.5h-5v5"/>'
        : '<path d="M7.5 2.5h-5v5M12.5 2.5h5v5M7.5 17.5h-5v-5M12.5 17.5h5v-5"/>';
    }
    var button = el("#full");
    if (button) {
      button.title = on ? (TXT.full_off || "") : (TXT.full_on || "");
      button.setAttribute("aria-label", button.title);
    }
  }

  function setFull(want) {
    var root = document.documentElement;
    var asked;
    try {
      if (want) {
        var go = root.requestFullscreen || root.webkitRequestFullscreen;
        if (go) { asked = go.call(root); }
      } else {
        var out = document.exitFullscreen || document.webkitExitFullscreen;
        if (out) { asked = out.call(document); }
      }
    } catch (e) { asked = null; }
    // The browser hands back a promise and turns it down whenever it feels
    // it should -- inside a frame that was never allowed full screen, or
    // without a real press behind the ask.  Left alone that refusal lands
    // in the console as an error nobody asked about, so it is caught here
    // and the switch just goes back to showing how things actually are.
    if (asked && asked.catch) { asked.catch(function () { wearFull(); }); }
  }

  ["fullscreenchange", "webkitfullscreenchange"].forEach(function (when) {
    document.addEventListener(when, function () {
      wearFull();
    });
  });

  // ----------------------------------------------------- the sheets themselves --
  // Two of them hang off the bar -- what you can save, and how things look --
  // and they behave the same way: the button opens one and shuts the other,
  // choosing inside leaves it open, anywhere else or Escape shuts it.
  var SHEETS = [["#save-open", "#save-menu"], ["#settings", "#settings-menu"]];

  // "here" is what open means, and it is the class rather than the hidden
  // attribute that says so.  The two part company for as long as a sheet
  // takes to leave: it is still in the page, being watched going, but it is
  // no longer open, and a press of its button while it is on its way out has
  // to bring it back rather than shut it a second time.
  function sheetOpen(which) {
    var sheet = el(which);
    return !!sheet && sheet.classList.contains("here");
  }
  function showSheet(which, want) {
    SHEETS.forEach(function (pair) {
      var on = want && pair[1] === which;
      var sheet = el(pair[1]);
      var button = el(pair[0]);
      if (sheet) { sheet.hidden = !on; sheet.classList.toggle("here", on); }
      if (button) { button.setAttribute("aria-expanded", on ? "true" : "false"); }
    });
  }
  function shutSheets() { showSheet(null, false); }
  function showSettings(want) { showSheet("#settings-menu", want); }

  SHEETS.forEach(function (pair) {
    var button = el(pair[0]), sheet = el(pair[1]);
    if (!button || !sheet) { return; }
    button.onclick = function (ev) {
      ev.stopPropagation();
      showSheet(pair[1], !sheetOpen(pair[1]));
    };
    sheet.addEventListener("click", function (ev) {
      ev.stopPropagation();            // choosing inside it leaves it open
    });
  });
  document.addEventListener("click", shutSheets);
  window.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") { shutSheets(); }
  });

  if (el("#settings")) {

    all("#theme-seg .seg-btn").forEach(function (b) {
      b.onclick = function () { setTheme(b.dataset.theme); };
    });
    all("#side-seg .seg-btn").forEach(function (b) {
      b.onclick = function () { setSide(b.dataset.side); };
    });
    if (el("#full-on")) {
      el("#full-on").onchange = function () { setFull(el("#full-on").checked); };
    }
    if (!canFull() && el("#full-row")) { el("#full-row").hidden = true; }
  }

  if (el("#full")) {
    el("#full").onclick = function () { setFull(!fullNow()); };
    if (!canFull()) { el("#full").hidden = true; }
  }

  // Putting the words on the page happens after this part runs, and again
  // whenever the language changes -- and it works from data-w attributes,
  // which cannot say "whichever of these two it is right now".  So the
  // settings that word themselves are re-applied on the back of it.
  var dressAlone = dress;
  dress = function () {
    dressAlone();
    wearSide();
    wearFull();
  };

  wearSide();
  wearFull();
/* eslint-disable no-undef */

  // A copy of the design is taken before anything that changes it, and the
  // copies are kept in a pile.  Ctrl+Z puts the top one back.
  //
  // This used to be called only from the keyboard, which meant a nudge with
  // an arrow key could be undone but dragging the same shape across the paper
  // could not, and neither could recolouring one, joining two up, or typing
  // in one.  Every one of those goes through keepUndo() now.
  function undoable() {                  // a copy of the design, to go back to
    try { return JSON.parse(JSON.stringify(hand)); } catch (e) { return null; }
  }
  var wasLike = [], willBeLike = [];     // where we came from, and went back from

  function keepUndo() {
    var now = undoable();
    if (!now) { return; }
    wasLike.push(now);
    if (wasLike.length > 60) { wasLike.shift(); }
    willBeLike.length = 0;               // a new move ends the old redo trail
  }

  function stepBack(forward) {
    var from = forward ? willBeLike : wasLike;
    var to = forward ? wasLike : willBeLike;
    if (!from.length) { return; }
    var now = undoable();
    if (now) { to.push(now); }
    hand = from.pop();
    picked = chosen = null;
    drawHand();
    drawHandPanel();
    showReport();
  }

/* eslint-disable no-undef */

  // ------------------------------------------------------- the slider bars --
  // The browser's own bars can be given a colour and not much else, and what
  // each browser then does with that is its own business: Firefox takes a
  // width and ignores the shape, Windows draws arrow buttons on the ends,
  // and the one along the bottom -- the one that gets the most use here,
  // since a chart is usually wider than the room it has -- came out looking
  // like nothing else on the page.  So the real ones are put away and these
  // are drawn instead, out of the same colours as everything else.
  // The bars belong to the stage, not to the row the stage sits in -- put
  // them in the row and they run the width of the panel as well, and the
  // grip comes out the wrong length because it is measuring the wrong thing.
  // So the stage gets a frame of its own to hang them in.
  function frameOf(box) {
    if (box.parentNode.classList.contains("stage-frame")) { return box.parentNode; }
    var frame = document.createElement("div");
    frame.className = "stage-frame";
    box.parentNode.insertBefore(frame, box);
    frame.appendChild(box);
    return frame;
  }

  function slider(box, which) {
    var across = which === "x";
    var bar = document.createElement("div");
    bar.className = "slider " + which;
    var less = document.createElement("button");
    var more = document.createElement("button");
    less.type = more.type = "button";
    less.className = "slider-step less";
    more.className = "slider-step more";
    less.tabIndex = more.tabIndex = -1;
    less.innerHTML = more.innerHTML =
      '<svg viewBox="0 0 10 10"><path d="M3.2 1.6 L6.8 5 L3.2 8.4"/></svg>';
    less.setAttribute("aria-label", across ? (TXT.slide_left || "") : (TXT.slide_up || ""));
    more.setAttribute("aria-label", across ? (TXT.slide_right || "") : (TXT.slide_down || ""));
    var track = document.createElement("div");
    track.className = "slider-track";
    var grip = document.createElement("div");
    grip.className = "slider-grip";
    track.appendChild(grip);
    bar.appendChild(less);
    bar.appendChild(track);
    bar.appendChild(more);
    frameOf(box).appendChild(bar);      // measured against the stage alone

    // The buttons at the ends: one press is one step, held down it keeps
    // going, the way these have always worked.
    var STEP = 56;
    [[less, -1], [more, 1]].forEach(function (pair) {
      pair[0].addEventListener("pointerdown", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var going = null, faster = null;
        function nudge() {
          if (across) { box.scrollLeft += pair[1] * STEP; }
          else { box.scrollTop += pair[1] * STEP; }
        }
        nudge();
        faster = setTimeout(function () { going = setInterval(nudge, 50); }, 330);
        function letGo() {
          clearTimeout(faster);
          if (going) { clearInterval(going); }
          window.removeEventListener("pointerup", letGo);
        }
        window.addEventListener("pointerup", letGo);
      });
    });

    function span() {
      return across ? [box.scrollWidth, box.clientWidth, box.scrollLeft]
                    : [box.scrollHeight, box.clientHeight, box.scrollTop];
    }
    function show() {
      var all = span(), whole = all[0], seen = all[1], at = all[2];
      if (whole - seen < 2) { bar.classList.add("none"); return; }
      bar.classList.remove("none");
      var room = across ? track.clientWidth : track.clientHeight;
      var long = Math.max(28, room * seen / whole);
      var far = (room - long) * (at / (whole - seen));
      if (across) {
        grip.style.width = long + "px";
        grip.style.transform = "translateX(" + far + "px)";
      } else {
        grip.style.height = long + "px";
        grip.style.transform = "translateY(" + far + "px)";
      }
    }

    function slideTo(point, hold) {
      var edge = track.getBoundingClientRect();
      var room = across ? track.clientWidth : track.clientHeight;
      var all = span(), whole = all[0], seen = all[1];
      var long = Math.max(28, room * seen / whole);
      var from = (across ? point - edge.left : point - edge.top) - hold;
      var part = Math.min(1, Math.max(0, from / (room - long)));
      var to = part * (whole - seen);
      if (across) { box.scrollLeft = to; } else { box.scrollTop = to; }
    }

    grip.addEventListener("pointerdown", function (ev) {
      ev.preventDefault();
      var edge = grip.getBoundingClientRect();
      var hold = across ? ev.clientX - edge.left : ev.clientY - edge.top;
      document.body.classList.add("sliding");
      function move(e) { slideTo(across ? e.clientX : e.clientY, hold); }
      function drop() {
        window.removeEventListener("pointermove", move);
        window.removeEventListener("pointerup", drop);
        document.body.classList.remove("sliding");
      }
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", drop);
    });

    track.addEventListener("pointerdown", function (ev) {
      if (ev.target === grip) { return; }
      var room = across ? track.clientWidth : track.clientHeight;
      var all = span(), whole = all[0], seen = all[1];
      slideTo(across ? ev.clientX : ev.clientY,
              Math.max(28, room * seen / whole) / 2);
    });

    box.addEventListener("scroll", show);
    window.addEventListener("resize", show);
    return show;
  }

  if (el("#stage")) {
    var stage = el("#stage");
    stage.classList.add("own-sliders");
    var showAcross = slider(stage, "x");
    var showDown = slider(stage, "y");
    // The same watchers serve the loose chart: a chart that has just been
    // redrawn, or zoomed, may be sitting somewhere it is no longer allowed
    // to sit, and this is where that is noticed.
    var refresh = function () { showAcross(); showDown(); holdClamp(); };
    refresh();
    // The chart changes size whenever it is redrawn or zoomed, and the bars
    // have to know.  Both of those show up here -- a redraw replaces what is
    // inside the sheet, a zoom resizes it -- so there is nothing to poll for.
    var paper = el("#sheet");
    if (window.ResizeObserver) {
      var watcher = new ResizeObserver(refresh);
      watcher.observe(stage);
      if (paper) { watcher.observe(paper); }
    }
    if (window.MutationObserver && paper) {
      new MutationObserver(refresh).observe(paper,
        { childList: true, subtree: true, attributes: true,
          attributeFilter: ["width", "height", "style", "viewBox"] });
    }
  }

  // -------------------------------------------- pseudocode, filling the screen --
  // Anything longer than a few lines is miserable to write in a box the width
  // of the panel, so the same box can be thrown up over the whole page.  It is
  // the very same textarea moved into an overlay and moved back again, so
  // nothing has to be copied about and there is only ever one of it.
  // The numbers down the side, and the count in the bar.  They are drawn from
  // the text itself and scrolled with it, so a long line that wraps does not
  // put them out of step -- each number sits against the line it belongs to.
  function countLines() {
    var box = el("#code");
    if (!box) { return; }
    var rows = box.value.split("\n").length;
    var out = [];
    for (var i = 1; i <= rows; i++) { out.push(i); }
    var numbers = out.join("\n");
    // whichever of the two boxes is on screen, and the count in the big
    // one's bar -- the numbers are the same numbers either way
    all(".code-rule").forEach(function (rule) { rule.textContent = numbers; });
    var says = el("#code-count");
    if (says) { says.textContent = say("code_lines", { n: rows }); }
  }

  function codeFull(want) {
    var box = el("#code"), over = el("#code-over");
    if (!box || !over) { return; }
    var home = el("#code-home");
    if (want) {
      tapeFull(false);                   // one screen at a time
      over.hidden = false;
      el("#code-slot").appendChild(box);
      document.body.classList.add("code-full");
      countLines();
    } else {
      over.hidden = true;
      home.insertBefore(box, home.firstChild);
      document.body.classList.remove("code-full");
      countLines();
    }
    var button = el("#code-big");
    if (button) {
      button.setAttribute("aria-expanded", want ? "true" : "false");
      button.title = want ? (TXT.code_small || "") : (TXT.code_big || "");
    }
    box.focus();
  }

  function followRule() {
    var box = el("#code");
    if (!box) { return; }
    all(".code-rule").forEach(function (rule) { rule.scrollTop = box.scrollTop; });
  }

  // Tab puts four spaces in rather than jumping out of the box, because
  // pseudocode is written with indents and this is where it gets written.
  if (el("#code")) {
    countLines();                        // the panel's box is numbered too
    // A program put there by anything other than typing -- one remembered
    // from last time, one opened from a file -- raises no keystroke, so the
    // numbers are counted again when the page has settled.
    setTimeout(countLines, 0);
    el("#code").addEventListener("input", countLines);
    el("#code").addEventListener("scroll", followRule);
    el("#code").addEventListener("keydown", function (ev) {
      if (ev.key !== "Tab" || ev.ctrlKey || ev.altKey) { return; }
      ev.preventDefault();
      var box = el("#code");
      var from = box.selectionStart, to = box.selectionEnd;
      box.value = box.value.slice(0, from) + "    " + box.value.slice(to);
      box.selectionStart = box.selectionEnd = from + 4;
      countLines();
    });
  }

  if (el("#code-big")) {
    el("#code-big").onclick = function () { codeFull(el("#code-over").hidden); };
    el("#code-done").onclick = function () { codeFull(false); };
    window.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && el("#code-over") && !el("#code-over").hidden) {
        codeFull(false);
      }
    });
  }
/* eslint-disable no-undef */

  // Nothing here is new to learn: they are the keys these things use
  // everywhere else.  They stay out of the way while something is being
  // typed into, which is most of what this page is.
  function typingNow() {
    var on = document.activeElement;
    if (!on) { return false; }
    var tag = (on.tagName || "").toLowerCase();
    return tag === "input" || tag === "textarea" || tag === "select" ||
           on.isContentEditable;
  }

  function keyStep(ev) {                 // a nudge, or a shove with Shift
    return ev.shiftKey ? HAND_GRID * 5 : HAND_GRID;
  }

  window.addEventListener("keydown", function (ev) {
    var ctrl = ev.ctrlKey || ev.metaKey;

    // Ctrl+Enter builds, wherever you are -- including from the pseudocode
    // box, which is exactly where you want it.
    if (ctrl && ev.key === "Enter") {
      ev.preventDefault();
      if (el("#build") && !byHand) { el("#build").click(); }
      else if (el("#check")) { el("#check").click(); }
      return;
    }
    if (ctrl && (ev.key === "s" || ev.key === "S")) {
      ev.preventDefault();               // save the design, not the web page
      if (el("#save-file")) { el("#save-file").click(); }
      return;
    }
    if (ctrl && (ev.key === "o" || ev.key === "O")) {
      ev.preventDefault();
      if (el("#open-file")) { el("#open-file").click(); }
      return;
    }
    if (ctrl && (ev.key === "0" || ev.key === ")")) {
      ev.preventDefault();
      if (el("#actual")) { el("#actual").click(); }
      return;
    }
    if (ctrl && (ev.key === "=" || ev.key === "+")) {
      ev.preventDefault();
      if (el("#in")) { el("#in").click(); }
      return;
    }
    if (ctrl && ev.key === "-") {
      ev.preventDefault();
      if (el("#out")) { el("#out").click(); }
      return;
    }

    if (typingNow()) { return; }         // the rest are for the chart itself

    if (ctrl && (ev.key === "z" || ev.key === "Z") && byHand) {
      ev.preventDefault();
      stepBack(ev.shiftKey);
      return;
    }
    if (ctrl && (ev.key === "y" || ev.key === "Y") && byHand) {
      ev.preventDefault();
      stepBack(true);
      return;
    }
    if (!byHand) { return; }

    var node = nodeById(picked), link = linkById(chosen);

    if (ctrl && (ev.key === "d" || ev.key === "D") && node) {
      ev.preventDefault();               // another one like this one
      keepUndo();
      var twin = JSON.parse(JSON.stringify(node));
      twin.id = hand.next++;
      twin.x += 30;
      twin.y += 30;
      hand.nodes.push(twin);
      picked = twin.id;
      drawHand();
      drawHandPanel();
      return;
    }

    if (ev.key === "Delete" || ev.key === "Backspace") {
      if (!node && !link) { return; }
      ev.preventDefault();
      keepUndo();
      if (link) {
        hand.links = hand.links.filter(function (l) { return l !== link; });
        chosen = null;
      } else {
        hand.nodes = hand.nodes.filter(function (n) { return n.id !== node.id; });
        hand.links = hand.links.filter(function (l) {
          return l.from !== node.id && l.to !== node.id;
        });
        picked = null;
      }
      drawHand();
      drawHandPanel();
      showReport();
      return;
    }

    if (ev.key === "Enter" && node) {    // type in the shape in hand
      ev.preventDefault();
      var g = el('.node[data-i="h' + node.id + '"]', el("#chart"));
      if (g) { typeInto(g); }
      return;
    }
    if (ev.key === "Enter" && link) {
      ev.preventDefault();
      typeOnLink(link);
      return;
    }
    if (ev.key === "Escape") {
      picked = chosen = null;
      joining = false;
      drawHand();
      drawHandPanel();
      return;
    }
    if (ev.key === "Tab") {              // around the shapes, one at a time
      if (!hand.nodes.length) { return; }
      ev.preventDefault();
      var order = hand.nodes.map(function (n) { return n.id; });
      var at = order.indexOf(picked);
      var next = ev.shiftKey ? at - 1 : at + 1;
      picked = order[(next + order.length) % order.length];
      chosen = null;
      drawHand();
      drawHandPanel();
      return;
    }

    var WAYS = { ArrowLeft: [-1, 0], ArrowRight: [1, 0],
                 ArrowUp: [0, -1], ArrowDown: [0, 1] };
    if (WAYS[ev.key] && node) {
      ev.preventDefault();
      keepUndo();
      var by = keyStep(ev);
      node.x = Math.max(node.w / 2 + 20, node.x + WAYS[ev.key][0] * by);
      node.y = Math.max(node.h / 2 + 20, node.y + WAYS[ev.key][1] * by);
      drawHand();
      drawHandPanel();
    }
  });
  // Almost all of the movement on this page is in 07-motion.css, where it
  // belongs: the stylesheet can see a button being pressed or a sheet being
  // shown and needs no help to answer it.  What is left over is the handful
  // of things it cannot see -- that a panel is on its way out rather than
  // simply gone, that this drawing is a new one rather than the same one
  // redrawn, that the chosen side of a switch has moved from the second to
  // the third.  Each of those is a word for the stylesheet to work from, put
  // on here and taken off again.
  //
  // Everything in this part is wrapped around something another part already
  // does, in the same way 19-settings.js wraps dress(): the original still
  // does the work, and this only says how it should look while it happens.
  // Nothing here is required for anything to function -- switch it all off
  // and the page still builds, colours, saves and runs.
  var STILL = false;                     // told to keep still by the system
  try { STILL = matchMedia("(prefers-reduced-motion: reduce)").matches; }
  catch (e) { STILL = false; }

  // A word on something for as long as the move it names takes, and then off
  // again, so the same move can be made to happen twice in a row.  Asking for
  // the width back in the middle is what makes the browser start the run over
  // rather than carry on with the one already going.
  function briefly(node, name, ms) {
    if (!node || STILL) { return; }
    node.classList.remove(name);
    void node.offsetWidth;
    node.classList.add(name);
    clearTimeout(node.motionTimer);
    node.motionTimer = setTimeout(function () {
      node.classList.remove(name);
    }, ms);
  }

  // ---------------------------------------------- the block that slides --
  // The chosen side of a two- or three-way switch is drawn by one block
  // sitting behind all of them, and the stylesheet slides it from where it
  // was to where it is now.  All it needs told is how many there are and
  // which one is on; everything toggles that class already, so rather than
  // ask each place that does to say so, the switch watches itself.
  function segSlide(seg) {
    var buttons = all(".seg-btn", seg), at = -1;
    buttons.forEach(function (b, i) {
      if (b.classList.contains("on")) { at = i; }
    });
    seg.style.setProperty("--seg-n", buttons.length || 1);
    if (at < 0) { seg.setAttribute("data-seg-off", ""); return; }
    seg.removeAttribute("data-seg-off");
    seg.style.setProperty("--seg-i", at);
  }

  function tendSegs() {
    all(".seg").forEach(function (seg) {
      segSlide(seg);
      if (!window.MutationObserver) { return; }
      new MutationObserver(function () { segSlide(seg); })
        .observe(seg, { subtree: true, attributes: true,
                        attributeFilter: ["class"] });
    });
  }

  // ------------------------------------------------- a card folding shut --
  // A height can only be animated from something to something, and "all of
  // it" is not a number the stylesheet knows.  A grid of one row is: it can
  // go from one part of the space to none of it.  So what is in a card that
  // folds is put inside two plain boxes -- the row, and a box inside it that
  // does the hiding -- and the stylesheet does the rest.  Nothing is moved
  // out of the card, so everything that looks things up by name still finds
  // them exactly where they were.
  function wrapFolds() {
    all("section.fold").forEach(function (card) {
      if (el(".fold-body", card)) { return; }
      var head = el("h2", card);
      if (!head) { return; }
      var body = document.createElement("div");
      var inner = document.createElement("div");
      body.className = "fold-body";
      inner.className = "fold-inner";
      body.appendChild(inner);
      Array.prototype.slice.call(card.childNodes).forEach(function (bit) {
        if (bit !== head) { inner.appendChild(bit); }
      });
      card.appendChild(body);
    });
  }

  // ------------------------------------------------------ the two sheets --
  // Shutting one is the awkward case: the plain one hides it the instant it
  // is asked to, and a hidden thing cannot be watched leaving.  So it is
  // left where it is for as long as the going takes and hidden at the end
  // of it -- and because the going is two states rather than a run of
  // keyframes, a sheet asked back halfway out comes back from where it got
  // to, which is all this has to do about it.
  //
  // One sheet replacing the other is not worth watching: they land in the
  // same corner, so the one going would only smear through the one coming.
  // It goes at once, and only the last one open is seen to leave.
  var showSheetPlain = showSheet;
  showSheet = function (which, want) {
    if (STILL) { return showSheetPlain(which, want); }
    SHEETS.forEach(function (pair) {
      var sheet = el(pair[1]), button = el(pair[0]);
      var on = want && pair[1] === which;
      if (button) { button.setAttribute("aria-expanded", on ? "true" : "false"); }
      if (!sheet) { return; }
      clearTimeout(sheet.goingTimer);
      if (on) {
        if (sheet.hidden) {
          sheet.hidden = false;
          aimSheet(button, sheet);     // laid out first, or there is
          void sheet.offsetWidth;      //   nothing for it to move from
        }
        sheet.classList.add("here");
      } else if (!sheet.hidden) {
        sheet.classList.remove("here");
        if (want) { sheet.hidden = true; }
        else {
          sheet.goingTimer = setTimeout(function () { sheet.hidden = true; }, 300);
        }
      }
    });
  };

  // A sheet grows out of the middle of the button that opened it.  Which
  // point that is cannot be written into the styling: it moves with the
  // width of the word on the button, and "Download" and "Herunterladen" are
  // not the same width.  So it is measured, once, as the sheet opens.
  //
  // Measured standing still, at that.  At this moment the sheet is sitting
  // shrunk and shifted, waiting to arrive, and a shrunk box does not have
  // its edges where the laid-out one does -- measure it as it stands and
  // the point comes out by however much the shrinking moved the edge, which
  // is a tenth of an inch of aiming at the wrong button.
  function aimSheet(button, sheet) {
    if (!button) { return; }
    sheet.style.transition = "none";
    sheet.style.transform = "none";
    var b = button.getBoundingClientRect(), s = sheet.getBoundingClientRect();
    sheet.style.transform = "";
    if (b.width && s.width) {
      var x = Math.round(b.left + b.width / 2 - s.left);
      sheet.style.transformOrigin =
        Math.max(0, Math.min(x, Math.round(s.width))) + "px top";
    }
    void sheet.offsetWidth;              // the state it starts from, settled
    sheet.style.transition = "";
  }

  // ------------------------------------------------------ the panel going --
  // The panel closes to nothing rather than disappearing, and what is inside
  // it has to keep its width while it narrows -- otherwise every word in it
  // re-wraps on the way out, which looks like the panel coming apart rather
  // than closing.  How wide it is depends on the screen and is decided in the
  // stylesheets; rather than repeat any of that here, the width it actually
  // has is measured as it starts to close, and given back once it is open
  // again so that resizing the window still moves it.
  var widthTimer = null;
  var showPanelPlain = showPanel;
  showPanel = function (open) {
    var panel = el("#panel");
    if (panel && !STILL) {
      clearTimeout(widthTimer);
      // Only worth noting on the way out of being open.  Asked to shut what
      // is already shut -- which happens, on a narrow screen, every time a
      // chart is drawn -- the width to note would be none, and the panel
      // would open again on nothing.
      if (!open && !panel.classList.contains("hide") && panel.clientWidth > 0) {
        panel.style.setProperty("--panel-w", panel.clientWidth + "px");
      } else if (open) {
        widthTimer = setTimeout(function () {
          panel.style.removeProperty("--panel-w");
        }, 320);
      }
    }
    showPanelPlain(open);
  };

  // ------------------------------------------- the menu on the right button --
  // The rows come in one after another, a sixtieth of a second apart, which
  // is enough to read as a list arriving rather than a block appearing.  The
  // menu is told to grow only after the plain one has measured it and put it
  // where it goes: measuring something mid-move measures the move.
  var openMenuPlain = openMenu;
  openMenu = function (x, y, items) {
    openMenuPlain(x, y, items);
    var here = all(".menu:not(.out)");
    var menu = here[here.length - 1];
    if (!menu) { return; }
    all("button", menu).forEach(function (row, i) {
      row.style.setProperty("--i", i);
    });
    void menu.offsetWidth;
    menu.classList.add("in");
  };

  var closeMenuPlain = closeMenu;
  closeMenu = function () {
    if (STILL) { return closeMenuPlain(); }
    all(".menu:not(.out)").forEach(function (menu) {
      menu.classList.remove("in");
      menu.classList.add("out");
      setTimeout(function () { menu.remove(); }, 140);
    });
  };

  // ------------------------------------------ the pseudocode, full screen --
  // Going out is the same trick as the sheets: the overlay is left where it
  // is until the falling is done, and only then handed to the plain one,
  // which is what hides it and carries the box back to the panel.
  var codeGoing = false;
  var codeFullPlain = codeFull;
  codeFull = function (want) {
    var over = el("#code-over");
    if (STILL || !over) { return codeFullPlain(want); }
    if (want) {
      clearTimeout(over.goingTimer);
      over.classList.remove("going");
      codeGoing = false;
      return codeFullPlain(true);
    }
    if (over.hidden || codeGoing) { return; }
    codeGoing = true;
    over.classList.add("going");
    over.goingTimer = setTimeout(function () {
      over.classList.remove("going");
      codeGoing = false;
      codeFullPlain(false);
    }, 190);
  };

  // ------------------------------------- the run and the code, full screen --
  // The same again for the runner's screen, which comes and goes the same
  // way and for the same reason.
  var tapeGoing = false;
  var tapeFullPlain = tapeFull;
  tapeFull = function (want) {
    var over = el("#tape-over");
    if (STILL || !over) { return tapeFullPlain(want); }
    if (want) {
      clearTimeout(over.goingTimer);
      over.classList.remove("going");
      tapeGoing = false;
      return tapeFullPlain(true);
    }
    if (over.hidden || tapeGoing) { return; }
    tapeGoing = true;
    over.classList.add("going");
    over.goingTimer = setTimeout(function () {
      over.classList.remove("going");
      tapeGoing = false;
      tapeFullPlain(false);
    }, 190);
  };

  // ------------------------------------------------------- the chart pane --
  // A new drawing rises out of the paper.  Only a new one: drawing by hand
  // redraws the same chart on every frame of a drag, and a chart that faded
  // in sixty times a second would be unreadable, so that way round is left
  // alone.
  var bindPlain = bind;
  bind = function () {
    bindPlain();
    if (!byHand) { briefly(el("#sheet"), "fresh", 520); }
  };

  // Zoom glides when a button asked for it.  Not when a drag did: the chart
  // is resized on every frame of one of those, and a width that took a third
  // of a second to arrive would always be a third of a second behind.
  var glideTimer = null;
  function glideZoom() {
    var paper = el("#sheet");
    if (!paper || STILL) { return; }
    paper.classList.add("gliding");
    clearTimeout(glideTimer);
    glideTimer = setTimeout(function () {
      paper.classList.remove("gliding");
    }, 420);
  }

  ["#in", "#out", "#fit", "#actual"].forEach(function (which) {
    var button = el(which);
    if (!button || !button.onclick) { return; }
    var was = button.onclick;
    button.onclick = function (ev) { glideZoom(); return was.call(this, ev); };
  });

  // ------------------------------------------------- and the small things --
  // What is selected, when it becomes something else rather than nothing.
  var selectPlain = select;
  select = function (g) {
    var was = sel;
    selectPlain(g);
    if (sel && sel !== was) { briefly(el("#sel-card"), "swap", 340); }
  };

  // Light to dark.  Every colour on the page fades rather than snaps, but
  // only for as long as the change takes: a page that transitions every
  // colour all the time is a page that lags behind the mouse.
  // The word has to go on before the colours change, not after: a colour
  // only fades if the page was already told to fade colours when it was
  // given the new one.  Which colours they will be is known either way --
  // wearing() answers from the setting, which has already been changed by
  // the time this is asked to put it on.
  var themeWorn = null;
  var wearThemePlain = wearTheme;
  wearTheme = function () {
    var now = wearing();
    if (themeWorn !== null && themeWorn !== now) {
      briefly(document.documentElement, "theming", 400);
    }
    themeWorn = now;
    wearThemePlain();
  };

  tendSegs();
  wrapFolds();

  // What the builder is saying about itself, whenever it changes what it says
  if (window.MutationObserver && el("#build-note")) {
    new MutationObserver(function () {
      briefly(el("#build-note"), "said-in", 320);
    }).observe(el("#build-note"),
               { childList: true, characterData: true, subtree: true });
  }
  // ------------------------------------------------------------- go on --
  recall();
  recallSetup();                       // how it was left set up, not what was in it
  dress();
  drawRoles();
  try {
    showSide(localStorage.getItem("flowchart-side") === "colors" ? "colors" : "chart");
    showPanel(localStorage.getItem("flowchart-panel") !== "shut");
  } catch (e) { showSide("chart"); showPanel(true); }
  if (!el("#modes")) { el("#side-tabs").hidden = true; }
  buildPresets();
  buildGlobals();
  el("#grid-on").checked = !style.gridOff;
  bind();
  paint();
  try { setLoose(localStorage.getItem("flowchart-hold") === "loose"); }
  catch (e) { setLoose(false); }
  if (el("#r-follow")) {                 // on unless it has been turned off
    try {
      el("#r-follow").checked =
        localStorage.getItem("flowchart-follow") !== "off";
    } catch (e) { /* storage turned off: it starts on */ }
  }
  if (el("#tab-hand")) {
    var lastMode = "code";
    try { lastMode = localStorage.getItem("flowchart-mode") || "code"; }
    catch (e) { /* fine */ }
    if (handRecall() && lastMode === "hand") {
      setMode(true);
      return;                            // by hand: nothing to draw from code
    }
  }
  // Whatever is in the box on arrival is drawn.  Nothing is, ordinarily --
  // the box opens empty and stays empty until somebody writes in it -- but
  // a program handed to --serve on the command line arrives already in it,
  // and that was asked for, so it is drawn without being asked for twice.
  if (el("#code")) {
    if (el("#code").value.trim()) { el("#build").click(); }
    else if (MODE === "web") { startPython(); }  // warm it up while they type
  }
})();
</script>
</body>
</html>
"""

# The pseudocode panel, which only the studio gets: the page written beside
# an .svg has no script behind it to redraw anything.
SOURCE_PANEL = r"""    <section class="card" id="modes">
      <div class="tabs">
        <button class="tab on" id="tab-code" data-w="mode_code">__W(mode_code)__</button>
        <button class="tab" id="tab-hand" data-w="mode_hand">__W(mode_hand)__</button>
      </div>
    </section>

    <section class="card" id="hand" hidden>
      <h2 data-w="add_shape">__W(add_shape)__</h2>
      <div class="adders" id="adders"></div>
      <div id="hand-sel"></div>
      <div id="hand-switches"></div>
      <div class="go" style="margin-top:12px">
        <button class="btn primary" id="check" data-w="check">__W(check)__</button>
        <button class="btn" id="wipe" data-w="start_again">__W(start_again)__</button>
      </div>
      <div id="report"></div>
    </section>
    <section class="card" id="source">
      <h2><span data-w="pseudocode">__W(pseudocode)__</span>
        <button class="icon small" id="code-big" data-w-title="code_big"
                title="__W(code_big)__" aria-label="__W(code_big)__"
                aria-expanded="false">
          <svg viewBox="0 0 20 20"><path d="M8 2.5H2.5v5.5M12 2.5h5.5v5.5M8 17.5H2.5V12M12 17.5h5.5V12"/></svg>
        </button>
      </h2>
      <div id="code-home"><textarea id="code" spellcheck="false">__CODE__</textarea></div>
      <div class="fields">
        <div><label for="f-title" data-w="title">__W(title)__</label>
          <input type="text" id="f-title" value="__T__"></div>
        <div><label for="f-author" data-w="your_name">__W(your_name)__</label>
          <input type="text" id="f-author" value="__A__"></div>
        <div><label for="f-shape" data-w="shape">__W(shape)__</label>
          <select id="f-shape">__SHAPES__</select></div>
        <div><label for="f-lang" data-w="language">__W(language)__</label>
          <select id="f-lang">__LANGS__</select></div>
      </div>
      <div class="switches" id="chart-switches">
        <label class="switch"><input type="checkbox" id="f-grid" checked><span data-w="grid">__W(grid)__</span></label>
        <label class="switch"><input type="checkbox" id="f-legend"><span data-w="key_switch">__W(key_switch)__</span></label>
      </div>
      <div class="go build-row">
        <button class="btn primary wide" id="build" data-w="build">__W(build)__</button>
      </div>
      <div id="build-note"></div>
    </section>

    <section class="card" id="runner">
      <h2><span data-w="r_head">__W(r_head)__</span>
        <button class="icon small" id="run-big" data-w-title="code_big"
                title="__W(code_big)__" aria-label="__W(code_big)__"
                aria-expanded="false">
          <svg viewBox="0 0 20 20"><path d="M8 2.5H2.5v5.5M12 2.5h5.5v5.5M8 17.5H2.5V12M12 17.5h5.5V12"/></svg>
        </button>
      </h2>
      <div class="switches">
        <select class="field" id="r-lang">
          <option value="pseudo">__W(r_pseudo)__</option>
          <option value="python">Python</option>
          <option value="java">Java</option>
          <option value="csharp">C#</option>
          <option value="javascript">JavaScript</option>
        </select>
        <div class="stack">
          <label class="switch">
            <input type="checkbox" id="r-slow" checked><span data-w="r_slowly">__W(r_slowly)__</span></label>
          <label class="switch" id="r-follow-row" data-w-title="r_follow_tip"
                 title="__W(r_follow_tip)__">
            <input type="checkbox" id="r-follow" checked><span data-w="r_follow">__W(r_follow)__</span></label>
        </div>
      </div>
      <div class="pair-wide">
        <button class="btn primary" id="run" data-w="r_run">__W(r_run)__</button>
        <button class="btn" id="see-code" data-w="r_code">__W(r_code)__</button>
      </div>
      <div id="tape" class="tape"></div>
    </section>

    <section class="card fold shut" id="roles">
      <h2 data-w="shapes_for">__W(shapes_for)__</h2>
      <div id="role-rows"></div>
    </section>
"""

PNG_SIZES = (1, 2, 3, 4, 6, 8)      # the sizes the page's PNG button offers
PNG_FRAMES = ((1920, 1080), (1080, 1080))   # and the fixed picture sizes it
                                    #   fits the chart inside, centered
SHAPE_NAMES = ("auto", "square", "wide", "page", "tall")
LANGUAGE_NAMES = {"en": "English", "es": "Español",
                  "fr": "Français", "de": "Deutsch"}


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
        pick = " selected" if mult == PNG_SCALE else ""
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
            % (code, " selected" if code == LANGUAGE else "",
               html.escape(LANGUAGE_NAMES.get(code, code)))
            for code in sorted(WORDS))
        panel = (SOURCE_PANEL
                 .replace("__LANGS__", tongues)
                 .replace("__SHAPES__", picks)
                 .replace("__T__", html.escape(source.get("title") or "", True))
                 .replace("__A__", html.escape(source.get("author") or "", True))
                 .replace("__CODE__", html.escape(source.get("code") or "")))

    every = {}                          # every language travels with the
    for code in WORDS:                  #   page, so it can change its own
        full = dict(WORDS["en"])        #   words without asking anybody
        full.update(WORDS[code])
        every[code] = full
    said = every.get(LANGUAGE, every["en"])
    page = re.sub(r"__W\((\w+)\)__",
                  lambda m: html.escape(word(m.group(1))),
                  PAGE_HTML.replace("__SOURCE__", panel))
    return (page
            .replace("__ALLWORDS__", json.dumps(every, ensure_ascii=False))
            .replace("__WORDS__", json.dumps(said, ensure_ascii=False))
            .replace("__LANG__", LANGUAGE)
            .replace("__PYODIDE__", PYODIDE)
            .replace("__MODULE__", MODULE_NAME)
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



# ------------------------------------------------------------- the studio --
def file_name(title):
    """A title, made safe to save under."""
    clean = re.sub(r'[\\/:*?"<>|]+', " ", title or "").strip()
    return re.sub(r"\s+", " ", clean) or "flowchart"


def draw_for_studio(ask):
    """One drawing, from what the studio asked for."""
    global SHAPE, LEGEND, GRID, GEOM
    if ask.get("lang"):
        apply_language(ask["lang"])
    text = ask.get("text") or ""
    if not text.strip():
        raise ValueError(word("no_code"))
    want = str(ask.get("seed") or "").strip()
    seed = style_variety(int(want) if want.isdigit() else None)
    shape = str(ask.get("shape") or "auto").lower()
    SHAPE = "" if shape in ("tall", "off", "none", "") else shape
    LEGEND = bool(ask.get("legend"))
    GRID = bool(ask.get("grid", True))
    GEOM = dict(DEFAULT_GEOM)                  # which shape draws which kind
    for kind, drawn in (ask.get("shapes") or {}).items():
        if kind in GEOM and drawn in SHAPES:
            GEOM[kind] = drawn
    for shape_kind in FILL:                    # tinted, or plain black and white
        FILL[shape_kind] = TINTS[shape_kind] if ask.get("tint") else "#ffffff"
    title = (ask.get("title") or "").strip() or None
    author = (ask.get("author") or "").strip() or None
    svg = make_flowchart(text, title, author)
    box = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    return {"ok": True, "svg": svg.split("\n", 1)[1], "seed": seed,
            "w": box.group(1) if box else "", "h": box.group(2) if box else "",
            "title": title or "Flowchart", "name": file_name(title),
            "ast": program_json(parse_program(text))}


PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"
MODULE_NAME = "flowchart_builder.py"    # the copy the browser imports


def write_site(where):
    """Write the whole thing out as a website that needs no server at all.

    Three files: the page, a copy of this script, and a readme saying how to
    put it online.  The page loads Python into the browser (Pyodide, from a
    CDN) and imports the copy, so the drawing is done by the same code that
    draws it here -- there is one flowchart builder, not two, and a chart
    made on the website is the chart this script makes.

    That is what lets it go on GitHub Pages, which serves files and runs
    nothing: everything happens in whoever's browser is looking at it.
    """
    where = os.path.abspath(where)
    os.makedirs(where, exist_ok=True)
    mine = os.path.abspath(__file__)

    page = to_page(empty_chart(), word("flowchart"), "flowchart",
                   source={"code": "", "title": "", "author": "",
                           "shape": SHAPE}, web=True)
    written = []
    for name, body in ((os.path.join(where, "index.html"), page),
                       (os.path.join(where, MODULE_NAME),
                        io.open(mine, encoding="utf-8").read()),
                       (os.path.join(where, "README.md"), SITE_README),
                       (os.path.join(where, ".nojekyll"), "")):
        with io.open(name, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        written.append(name)
        print(word("wrote", path=name))
    print(word("site_done", dir=where))
    return written


SITE_README = """# Flowchart Builder

Paste textbook-style pseudocode, get a flowchart. Color it in, then save it
as an SVG or a PNG.

This folder is the whole website. It is three files and no server: the page,
the Python that draws the charts, and this readme. The page loads Python
into your browser (Pyodide) and imports `flowchart_builder.py`, so the same
code that runs on a computer runs in the browser, and nothing you type is
sent anywhere.

## Putting it online with GitHub Pages

1. Make a repository on GitHub -- the free kind is fine.
2. Put these files in it. Either drag them onto the web page GitHub shows
   for an empty repository, or, in this folder:

       git init
       git add .
       git commit -m "Flowchart builder"
       git branch -M main
       git remote add origin https://github.com/<you>/<repo>.git
       git push -u origin main

3. On GitHub: **Settings -> Pages**. Under *Build and deployment*, set
   *Source* to **Deploy from a branch**, pick branch **main** and folder
   **/ (root)**, and press Save.
4. Wait a minute, then open `https://<you>.github.io/<repo>/`.

If you keep the files in a `docs/` folder inside a bigger repository, pick
**/docs** as the folder in step 3 instead.

Any other static host works the same way -- Netlify, Cloudflare Pages,
GitLab Pages, or a folder on a school web server. There is nothing to
install and nothing to run.

## Running it on your own computer

    python "Flowchart Builder.py"

opens the same studio, served from your machine. Give it a file instead and
it writes the .svg and .html straight out:

    python "Flowchart Builder.py" mycode.txt -t "My chart"

`--help` lists the rest: the shape to aim at, the language, the seed, and so
on.
"""

def serve(port, text="", title=None, author=None):
    """Run the whole thing as a small website, here on this computer.

    Paste pseudocode in the panel, press the button, and the same code that
    writes the .svg draws it and hands it back.  Nothing leaves the machine:
    the server listens on localhost, and the page it serves is the same one
    that gets written beside an .svg, with the pseudocode panel added.
    """
    import http.server
    import json as _json
    import socketserver

    state = {"code": text, "title": title, "author": author, "shape": SHAPE}

    class Studio(http.server.BaseHTTPRequestHandler):
        server_version = "FlowchartStudio"
        protocol_version = "HTTP/1.1"       # every reply says how long it is

        def log_message(self, *args):
            pass                                # keep the terminal quiet

        def reply(self, body, kind="text/html; charset=utf-8", code=200):
            data = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            path, _, query = self.path.partition("?")
            if path not in ("/", "/index.html"):
                self.reply("Nothing here.", "text/plain; charset=utf-8", 404)
                return
            for bit in query.split("&"):        # ?lang=es, from the picker
                if bit.startswith("lang="):
                    apply_language(bit[5:])
            try:
                drawn = draw_for_studio({"text": state["code"],
                                         "title": state["title"],
                                         "author": state["author"],
                                         "shape": state["shape"], "grid": True})
                svg, seed = drawn["svg"], drawn["seed"]
                shown = drawn["title"]
                name = drawn["name"]
            except Exception:                   # an empty start is fine
                svg, seed = empty_chart(), None
                shown, name = word("flowchart"), "flowchart"
            self.reply(to_page(svg, shown, name, source=state, seed=seed))

        def do_POST(self):
            if self.path.split("?")[0] != "/build":
                self.reply("Nothing here.", "text/plain; charset=utf-8", 404)
                return
            try:
                size = int(self.headers.get("Content-Length") or 0)
                ask = _json.loads(self.rfile.read(size).decode("utf-8"))
                if ask.get("lang"):
                    apply_language(ask["lang"])
                out = draw_for_studio(ask)
                state.update(code=ask.get("text", ""), title=ask.get("title"),
                             author=ask.get("author"), shape=ask.get("shape"))
            except Exception as exc:
                out = {"ok": False, "error": str(exc) or exc.__class__.__name__}
            self.reply(_json.dumps(out), "application/json; charset=utf-8")

    # One connection at a time is not enough.  A browser keeps a spare
    # connection open that it has not sent anything on yet, in case it needs
    # it -- and a server that answers one at a time will sit on that spare
    # waiting for a request that never comes, while every real request behind
    # it fails with nothing more useful than "failed to fetch".  It shows up
    # as the thing working with a short program and breaking with a long one,
    # because the longer the drawing takes the likelier the collision, which
    # is a miserable thing to be told to debug.  A thread per connection costs
    # nothing here and the problem cannot happen.
    class Threaded(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True               # Ctrl+C does not wait for spares

    house = Threaded(("127.0.0.1", port), Studio)
    where = "http://127.0.0.1:%d/" % house.server_address[1]
    print(word("studio_at", url=where))
    print(word("leave_open"))
    webbrowser.open(where)
    try:
        house.serve_forever()
    except KeyboardInterrupt:
        print("\n" + word("stopped"))
    finally:
        house.server_close()


def empty_chart():
    """What the studio shows before there is anything to show."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="430" height="150" '
            'viewBox="0 0 430 150"><rect class="sheet" width="100%" '
            'height="100%" fill="#ffffff"/><text x="215" y="78" '
            'text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
            'font-size="13" fill="#5d6b7a">'
            + html.escape(word("empty_chart")) + "</text></svg>")



# ------------------------------------------------------------------- driver --
def legend_row(elems):
    """A key of the shapes this chart actually uses, laid out in a row.

    Only the shapes that turn up are listed, so a chart with no loops does
    not advertise a loop symbol."""
    present = {e[1] for e in elems if e[0] == "shape"}
    items = [k for k in LEGEND_ORDER if k in present]
    if not items:
        return [], 0.0
    band = SWATCH_H
    out, x = [], 0.0
    for kind in items:
        out.append(("shape", kind, x + SWATCH_W / 2.0, band / 2.0,
                    SWATCH_W, SWATCH_H, [], 0))
        x += SWATCH_W + 9
        name = LEGEND_NAME[kind]
        out.append(("text", x, band / 2.0 + 4, name, "start"))
        x += text_w(name, FONT_SIZE, True) + 28
    return out, band


def with_legend(elems):
    """Put the key above the chart, lined up with its left edge."""
    if not LEGEND:
        return elems
    key, band = legend_row(elems)
    if not key:
        return elems
    minx, miny, _, _ = bbox(elems)
    return shift(key, minx, miny - band - VGAP) + elems



def style_variety(seed=None):
    """Draw the same program a little differently from one run to the next.

    Everything shaken here is a matter of drawing, not of meaning: how long
    an arrow between two shapes is, how much air a box keeps around its
    words, how round a corner is, how fine the grid is, which hand True
    goes out on, and where the line is past which a chain of tests stops
    forking and queues up down the page instead.  Two runs of one file come
    out as two drawings of the same program -- every shape, every word and
    every route the same in meaning, none of it laid out quite the same.

    What is never shaken is anything a reader depends on: the lettering
    stays the size it was, a shape still means what it means, and no arrow
    goes anywhere different.

    The seed is what makes a look repeatable.  Left out, one is picked and
    handed back, and the script prints it; pass it to --seed and that exact
    chart comes back.
    """
    global VGAP, HGAP, PAD_Y, NODE_MIN_H, NODE_W, NODE_MAX_W, DIA_W, DIA_MIN_H
    global OVAL_W, OVAL_H, CORNER_R, SLANT, LOOP_UP, LABEL_PAD
    global GRID_STEP, GRID_MAJOR, FORK_LIMIT, CHAIN_LIMIT, GROUP_MAX
    global TRUE_LEFT, SHAKE
    if seed is None:
        seed = random.randrange(1000, 99999)
    r = random.Random(seed)
    # The gaps down the page are whole grid steps, and the grid is chosen
    # first so they can be.  Everything a shape's height is built from is
    # rounded up to a pair of steps later, so a chart lands on the ruling
    # behind it however these fall out.
    GRID_STEP = r.choice((16, 20, 24))
    GRID_MAJOR = r.choice((4, 5))
    VGAP = GRID_STEP                    # the gaps, and the air inside a shape
    HGAP = r.randint(22, 30)
    PAD_Y = r.randint(8, 11)
    LABEL_PAD = r.randint(10, 14)
    NODE_MIN_H = r.randint(30, 36)
    NODE_W = r.randint(124, 142)
    NODE_MAX_W = r.randint(172, 200)
    DIA_W = r.randint(126, 146)
    DIA_MIN_H = r.randint(44, 54)
    OVAL_W = r.randint(92, 104)
    OVAL_H = r.randint(34, 40)
    CORNER_R = r.randint(3, 9)          # how softly a corner turns
    SLANT = r.randint(10, 14)           # the lean on a parallelogram
    LOOP_UP = GRID_STEP                 # the reach of a loop's way back
    FORK_LIMIT = r.randint(280, 360)    # where the layout changes its mind
    CHAIN_LIMIT = r.randint(780, 1020)
    GROUP_MAX = r.randint(4, 6)
    TRUE_LEFT = r.random() < 0.7        # mostly the usual way round
    SHAKE = r                           # the shape search nudges with this
    return seed


def shape_target(spec):
    """What --shape asked for, as a width / height ratio.

    Takes a name (square, wide, page, screen), a ratio (16:9, 4x3), a size
    (1920x1080) or a plain number.  Anything it cannot read falls back to
    the middling shape, which is what "auto" aims at."""
    key = str(spec or "").strip().lower()
    named = {"square": 1.0, "wide": 16 / 9.0, "screen": 16 / 9.0,
             "16:9": 16 / 9.0, "page": 8.5 / 11.0, "auto": AUTO_SHAPE}
    if key in named:
        return named[key]
    m = re.match(r"^(\d+(?:\.\d+)?)\s*[x:/ ]\s*(\d+(?:\.\d+)?)$", key)
    if m and float(m.group(2)):
        return float(m.group(1)) / float(m.group(2))
    try:
        return max(0.05, float(key))
    except ValueError:
        return AUTO_SHAPE


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
    global CHAIN_LIMIT, MAX_ROW_W
    keep = (CHAIN_LIMIT, MAX_ROW_W)
    target = shape_target(spec)
    head = len(charts) > 1

    def build(max_h, chain, row_w):
        global CHAIN_LIMIT, MAX_ROW_W
        CHAIN_LIMIT, MAX_ROW_W = chain, row_w
        elems = with_legend(arrange([layout_chart(c, max_h, heading=head)
                                     for c in charts]))
        x0, y0, x1, y1 = bbox(elems)
        return elems, x1 - x0, y1 - y0

    try:
        chains = sorted({keep[0], 0.0, 1e9})       # queue up / as set / fork
        rows = sorted({keep[1], 900.0, 2400.0, 4000.0}) if head else [keep[1]]
        plain = {}                                 # one column, per chain style
        for chain in chains:
            plain[chain] = build(0, chain, keep[1])[1:]
        natural = plain[keep[0]]
        if str(spec).strip().lower() == "auto" \
                and AUTO_KEEP[0] <= natural[0] / natural[1] <= AUTO_KEEP[1]:
            return build(0, keep[0], keep[1])[0]   # already a sensible shape

        tallest = max(h for _, h in plain.values())
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
                for max_h in steps:
                    if max_h and max_h < 240:
                        continue
                    elems, w, h = build(max_h, chain, row_w)
                    cols = max(1.0, round(plain[chain][1] / h)) if h else 1.0
                    score = (abs(math.log((w / h) / target))
                             + COLUMN_COST * (cols - 1)
                             + ROUTE_COST * wander(elems, w + h))
                    if SHAKE is not None:       # a nudge, so two runs of the
                        score += SHAKE.uniform(0, 0.05)   # same file differ
                    if best_score is None or score < best_score - 1e-9:
                        best, best_score = elems, score
        return best
    finally:
        CHAIN_LIMIT, MAX_ROW_W = keep

def make_flowchart(text, title=None, author=None, max_h=COLUMN_H):
    """Whole program -> one SVG string (every module side by side)."""
    charts = parse_program(text)
    if SHAPE and not max_h:                 # let the shape pick the layout
        return to_svg(fit_shape(charts, SHAPE), title, author)
    layouts = [layout_chart(c, max_h, heading=len(charts) > 1) for c in charts]
    return to_svg(with_legend(arrange(layouts)), title, author)


def make_flowcharts(text, title=None, author=None, max_h=COLUMN_H):
    """Whole program -> [(module name, SVG string), ...], one per module."""
    charts = parse_program(text)
    result = []
    for c in charts:
        if SHAPE and not max_h:             # each module shaped on its own
            elems = fit_shape([c], SHAPE)
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


def main():
    global FOR_STYLE, LEGEND, GRID, GRID_STEP, PAGE, GROUP_OUTPUT
    global CHAIN_LIMIT, SHAPE, VARIETY
    ap = argparse.ArgumentParser(description="Pseudocode -> flowchart (SVG).")
    ap.add_argument("infile", nargs="?", help="pseudocode text file "
                                             "(reads standard input if omitted)")
    ap.add_argument("-o", "--out", help="output .svg file")
    ap.add_argument("-t", "--title", help="title drawn at the top")
    ap.add_argument("-a", "--author", help="your name, under the title")
    ap.add_argument("--split", action="store_true",
                    help="write one .svg per module / function")
    ap.add_argument("--for-style", choices=["expand", "hexagon"], default=FOR_STYLE,
                    help="how to draw For loops (default: %(default)s)")
    ap.add_argument("--columns-height", type=float, default=COLUMN_H,
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
    ap.add_argument("--shape-for", metavar="KIND=SHAPE", action="append",
                    help="draw one kind of step as a different shape, e.g. "
                         "--shape-for io=trap.  Kinds: " +
                         ", ".join(sorted(DEFAULT_GEOM)) + ".  Shapes: " +
                         ", ".join(SHAPE_ORDER))
    ap.add_argument("--lang", default=LANGUAGE, choices=sorted(WORDS),
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
    ap.add_argument("--shape", default=SHAPE,
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
    args = ap.parse_args()
    apply_language(args.lang)
    for pair in (args.shape_for or []):
        kind, _, drawn = pair.partition("=")
        if kind.strip() in GEOM and drawn.strip() in SHAPES:
            GEOM[kind.strip()] = drawn.strip()
        else:
            print(word("odd_shape", pair=pair))
    FOR_STYLE = args.for_style
    LEGEND = args.legend or LEGEND
    GROUP_OUTPUT = GROUP_OUTPUT and not args.no_group_output
    off = ("tall", "off", "none", "")
    SHAPE = "" if str(args.shape).lower() in off else args.shape
    GRID = GRID and not args.no_grid
    PAGE = PAGE and not args.no_page

    # The varied look goes on first and anything named on the command line
    # over the top of it, so asking for one thing by hand does not hand the
    # rest of the drawing back to the defaults.
    VARIETY = VARIETY and not args.no_variety
    seed = args.seed if args.seed is not None else SEED
    if seed is not None:
        try:
            seed = int(seed)
        except ValueError:                      # a word for a seed is fine
            seed = sum(ord(c) * (i + 7) for i, c in enumerate(str(seed)))
    if VARIETY or seed is not None:
        seed = style_variety(seed)
    if args.roomy:                      # put the old spacing back
        globals().update(ROOMY)
    if args.chain_limit is not None:
        CHAIN_LIMIT = args.chain_limit
    if args.grid_step is not None:
        GRID_STEP = args.grid_step
    if not args.color and (args.mono or MONO):
        for shape in FILL:
            FILL[shape] = "#ffffff"

    title, author = args.title, args.author
    here = os.path.dirname(os.path.abspath(__file__))
    split = args.split or SPLIT_MODULES

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
    if args.serve is not None or (not start.strip() and STUDIO):
        serve(args.serve if args.serve is not None else 8765,
              start, title, author or AUTHOR)
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
    written, pages = [], []
    for path, svg, heading in charts:
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        written.append(path)
        print(word("wrote", path=path))
        if PAGE:                      # the viewer, with the download links
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


if __name__ == "__main__":
    main()

