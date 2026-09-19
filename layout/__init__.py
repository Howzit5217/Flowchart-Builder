"""Where every shape goes.

Reading this reads all of it, which is what fills the table in blocks.py
that says who lays out what.  Import a part of it on its own and you would
get a chart with the Ifs missing.
"""
from . import blocks, branches, loops, cases, columns       # noqa: F401
