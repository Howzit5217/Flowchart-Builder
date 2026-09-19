"""What the published website needs: Python, and the modules to give it."""
import ast
import os

# The website has no server to ask for a drawing, so the page loads Python
# into the browser and runs this very package there.  What it cannot do is
# import a folder it has never heard of, so the page is told which files to
# fetch and writes them into Python's own filesystem before importing.
#
# It used to be handed one enormous file instead -- every module joined end
# to end by a build step, half a megabyte of it -- because one file is
# easy to fetch.  Most of that was the studio's own HTML, CSS and script,
# carried inside a Python string to a browser that was already looking at
# them.  Fetching the modules themselves is a fifth of the size and there
# is no second copy of anything to keep in step.
PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/"

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAWS = "studio/drawing.py"         # the one thing the browser asks us for


def leans_on(where):
    """Which modules of ours that one imports, by path inside the package."""
    out = set()
    text = open(os.path.join(HERE, where), encoding="utf-8").read()
    folder = os.path.dirname(where).split("/") if os.path.dirname(where) else []
    for node in ast.parse(text).body:
        if not isinstance(node, ast.ImportFrom) or not node.level:
            continue
        # level 1 is this module's own folder, 2 is the one above it
        up = folder[:len(folder) - (node.level - 1)]
        parts = up + ((node.module or "").split(".") if node.module else [])
        base = "/".join(p for p in parts if p)
        if base and os.path.exists(os.path.join(HERE, base + ".py")):
            out.add(base + ".py")
        for alias in node.names:        # from ..layout import blocks
            deeper = "/".join([p for p in parts if p] + [alias.name]) + ".py"
            if os.path.exists(os.path.join(HERE, deeper)):
                out.add(deeper)
    return out


def needed():
    """Every module the browser has to have to draw a chart.

    Worked out from the imports rather than listed, so a module added to
    the drawing goes to the browser without anybody remembering a list --
    and one that is only ever used from the command line does not.  The
    package's folders come too, for their __init__ files.
    """
    seen, todo = set(), [DRAWS, "__init__.py"]
    while todo:
        where = todo.pop()
        if where in seen:
            continue
        seen.add(where)
        todo += sorted(leans_on(where))
        # A folder is a package, and its __init__ is read before anything
        # inside it -- which is where layout/ fills the table saying who
        # lays out an If, and where words/ reads the languages.  Leaving
        # them out drew charts with every branch and every word missing.
        folder = os.path.dirname(where)
        while folder:
            todo.append(folder + "/__init__.py")
            folder = os.path.dirname(folder)
    return sorted("flowchart/" + where for where in seen)
