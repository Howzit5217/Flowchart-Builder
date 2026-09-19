"""flowchart -- turn textbook-style pseudocode into a flowchart.

Every part of this is a file of its own, named for the one job it does, and
flowchart/README.md says what is where.  There is nothing built from it:
the published website loads Python into the browser, fetches these very
modules and runs them there, so what is drawn on the site is drawn by the
files you are reading.

Usage:
    python -m flowchart                     the studio, in your browser
    python -m flowchart pseudocode.txt      one file, straight to .svg
    python -m flowchart code.txt -o out.svg -t "Tip Calculator"
    python -m flowchart --site docs         a website you can publish
    python -m flowchart pseudocode.txt --split          (one .svg per module)

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
once it is there: click it to give it a word, a color, a thickness, a
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
key still says so, and the colors still group by kind -- only what it is
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
on import."""

# `main` when it is asked for, and not before.  Reading the package used
# to read the command line too, and through it the page, and through that
# every .css and .js file the studio is made of -- some hundreds of
# kilobytes to answer a question about a flowchart.  The browser reads this
# package over the network, so that mattered.


def __getattr__(name):                  # PEP 562
    if name == "main":
        from .make.command import main
        return main
    raise AttributeError(name)
