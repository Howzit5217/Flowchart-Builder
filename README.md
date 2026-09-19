# The parts

This is the code. Every file is named for the one job it does, and it runs
straight from here:

```bash
python -m flowchart                     the studio, in your browser
python -m flowchart program.txt         one file, straight to .svg
python -m flowchart --site docs         a website you can publish
```

Nothing needs installing, and any part of it can be imported on its own:

```python
from flowchart.parse.read import parse_program
from flowchart.make.chart import make_flowchart
```

## What is where

Each folder is one stage of the job.

### The Python

| File | What is in it |
|---|---|
| `__init__.py` | What the whole thing is, and `main` |
| `__main__.py` | `python -m flowchart` |
| `settings.py` | Every knob, in one place |
| `measure.py` | How wide words come out, and how tall a line is |
| `shapes.py` | The catalog of shapes, and which kind is drawn as which |
| `parts.py` | The page's own files, poured together |
| `page.py` | The page around the chart |
| **`words/`** | |
| `words/en.py` `es` `fr` `de` | Every word it says, per language; each registers itself |
| `words/lookup.py` | The table they register in, and looking a word up |
| **`parse/`** — pseudocode in | |
| `parse/nodes.py` | What a step and a block are |
| `parse/clean.py` | Tidying a line into something readable |
| `parse/keywords.py` | The words it recognizes |
| `parse/statements.py` | One line at a time |
| `parse/trouble.py` | What the reading had to paper over, and where |
| `parse/read.py` | The whole thing: blocks, branches, loops |
| `parse/data.py` | The same program as data, for running it and for code |
| **`layout/`** — where everything goes | |
| `layout/blocks.py` | A block of chart, a run of steps, and who lays out what |
| `layout/branches.py` | If/else, and the lanes they need |
| `layout/loops.py` | While and repeat, and the line back up |
| `layout/cases.py` | Select Case, and the lane each branch gets |
| `layout/columns.py` | Wrapping it into columns so it is not a ribbon |
| **`draw/`** — what it looks like | |
| `draw/arrows.py` | Lines with square corners, rounded off, and the heads on them |
| `draw/grid.py` | The faint grid behind it |
| `draw/outlines.py` | Each shape's outline |
| `draw/svg.py` | Putting the SVG together |
| **`studio/`** | |
| `studio/web.py` | What the published website needs to know |
| `studio/drawing.py` | Drawing a chart for the browser to show |
| `studio/site.py` | The website it writes: the page, beside this package |
| `studio/serve.py` | The little server behind `--serve` |
| **`make/`** — putting it together | |
| `make/chart.py` | Making one chart, start to finish |
| `make/fit.py` | Fitting a chart to the shape you asked for |
| `make/shake.py` | The seeded shake, so two charts differ |
| `make/legend.py` | The key beside the chart |
| `make/options.py` | Everything the command line answers to |
| `make/command.py` | And what it does with the answers |

### The page

`ui/` is the studio itself: `studio.html`, the stylesheet in seven parts and
the script in twenty-eight. `parts.py` pours the `.css` and the `.js` into
the `@@CSS@@` and `@@JS@@` marks in `studio.html` and hands back the page.

| File | What is in it |
|---|---|
| `ui/studio.html` | The studio page itself |
| `ui/source-panel.html` | The pseudocode panel, which only the studio gets |
| `ui/css/01-base.css` | Colors, type, dark mode, the shared bits |
| `ui/css/02-bar.css` | The bar across the top |
| `ui/css/03-layout.css` | The rail, the stage, the panel's frame |
| `ui/css/04-panel.css` | Everything inside the panel |
| `ui/css/05-chart.css` | The chart, the menu, the shapes and arrows |
| `ui/css/06-screens.css` | Fitting the screen it is on, whatever size that is |
| `ui/css/07-motion.css` | How it moves, and how it does not |
| `ui/js/01-start.js` | The bits everything else uses |
| `ui/js/02-paint.js` | Painting the colors on |
| `ui/js/03-shapes.js` | The shape catalog, in the browser |
| `ui/js/04-panel.js` | The colors panel |
| `ui/js/05-keep.js` | Remembering what you chose |
| `ui/js/06-chart.js` | Showing a chart, and moving about it |
| `ui/js/07-sides.js` | The rail, the panel, collapsing it |
| `ui/js/08-save.js` | Saving a picture |
| `ui/js/09-build.js` | Building from pseudocode, off the page's own thread |
| `ui/js/10-hand.js` | By hand: placing, dragging, joining |
| `ui/js/11-hand-panel.js` | What the panel shows for a shape or arrow |
| `ui/js/12-check.js` | Checking a design makes sense |
| `ui/js/13-hand-keep.js` | Remembering a design |
| `ui/js/14-run.js` | Running the program |
| `ui/js/15-sums.js` | Working out what an expression comes to |
| `ui/js/16-wrong.js` | Where a run stopped, and why |
| `ui/js/17-tape.js` | The tape at the foot of the panel, and the screen it fills |
| `ui/js/18-code.js` | Writing it out as Python, Java, C# or JavaScript — a block each |
| `ui/js/19-files.js` | Saving a design to a file, and opening it again |
| `ui/js/20-menu.js` | The right button |
| `ui/js/21-typing.js` | Double-click to type in a shape |
| `ui/js/22-settings.js` | The settings sheet: light or dark, which side, full screen |
| `ui/js/23-undo.js` | Stepping back, and stepping forward again |
| `ui/js/24-scroll.js` | Slider bars of our own, and the pseudocode filling the screen |
| `ui/js/25-keys.js` | The keys people already know |
| `ui/js/26-motion.js` | What moves, and what holds still |
| `ui/js/27-mend.js` | Putting right what a warning already worked out |
| `ui/js/99-go.js` | Starting it all up |

## Four things worth knowing

**Names say what the file does.** Every file is one plain word for one
job — `measure.py` measures words, `fit.py` fits a chart to a shape,
`shake.py` is the seeded shake, `trouble.py` is what the reading had to
paper over. If a name stops describing what is in the file, the file has
grown a second job and wants splitting.

**Read the settings, never import them.** `settings.py` holds every knob,
and everything else reaches them as `settings.VGAP`, `settings.GEOM` and so
on. That is not a style rule, it is what makes them work: `--seed` shakes a
dozen of them before a chart is drawn, `--roomy` replaces seven, and the
studio sets four on every request. A name imported by value is a copy of
whatever it was when the module was first read, and would quietly stop
following.

**Who lays out what is a table, not a chain of ifs.** `layout/blocks.py` is
what branches, loops and select all lean on, so it may not lean back on
them. Instead it keeps `LAYOUTS`, and each of those three writes its own
name into it at the foot of its own file. Adding a kind of statement is
adding a file and one line at the end of it.

**The `.js` parts share one scope.** They run inside a single function, in
the order `parts.py` lists them, so a later part may use a name an earlier
one made. Two parts using the same name are not two things — the later
declaration silently replaces the earlier, and whatever used the first stops
working. `tests/run.py` refuses to pass when that happens and says which
two parts to look at. The Python has no such rule — modules are modules.

## The website runs these files

The published website has no server to ask for a drawing, so the page loads
Python into the browser and runs this package there: it fetches the modules
and writes them into Python's own filesystem, then imports them as any
program would.

Which modules, it works out by following the imports from
`studio/drawing.py` — 36 files, about 197 KB — so a module added to the
drawing goes to the browser on its own, and one that is only ever used from
the command line does not. `studio/web.py` does the working out.

There is nothing built and no second copy. Editing a module needs no
rebuild; only `index.html` does, and only when the page's own HTML, CSS or
script changes:

```bash
python -m flowchart --site .
```

## Adding a part

1. Put the file where it belongs — a new stage gets its own folder.
2. Import what it needs; nothing shares a namespace here.
3. A `.js` or `.css` part goes in the `JS` or `CSS` list in `parts.py`,
   then `python -m flowchart --site .` to put it in the page.
4. A Python module needs nothing: the website follows the imports.

## Adding a language

Two different things are called languages here, and each is one place now.

**A language the page speaks** (English, Spanish, …). Copy `words/en.py`,
translate the right-hand side of each line, and end the file the way that
one ends:

```python
speaks("it", "Italiano", IT)
```

then add it to the import line in `words/__init__.py`, which is what reads
it at all. That is the whole of it — `--lang`, the picker in the studio and
the copy that travels with the page all come from what has registered, so
there is no second list to keep in step. Anything left untranslated falls
back to English.

**A language it writes the program out in** (Python, Java, …). Add a block
to `LANGS` in `ui/js/18-code.js` saying what that language calls printing,
how it asks to be typed into, how it declares a variable and what it wraps a
whole program in. Say `like: CURLY` to start from what the brace-and-
semicolon languages share. The picker, the file extension and the name the
Save button uses all follow from the block.

The writer itself knows no language by name. It used to: thirty-one tests of
the form `lang === "python"` through six functions, and the ones somebody
missed when adding a language did not fail — they quietly wrote Python in
the middle of the Java. `tests/run.py` now asks every block for all twelve
of its answers.

## Checking it

```bash
python tests/run.py          run every check
python tests/run.py -q       only say what failed
python tests/run.py --only lines
```

Two of them lift a piece of the page's script out and run it in node: the
by-hand arrow router, and the runner.  The second one runs real pseudocode
-- modules and all -- with a stand-in for the browser, and reads the tape
afterwards.  A chart that draws and a chart that runs are not the same
claim, and only that one checks the second.

Every check in there was a bug once. Rather than fix a chart by eye and
hope, the thing that was wrong was written down as something countable — a
line that doubles back, an arrow point painted over by a label, a shape
sitting off the ruling — so the fix could be shown to work and, far more
usefully, shown to still work later. Nothing needs installing; where `node`
is present a few more checks run that need it.
