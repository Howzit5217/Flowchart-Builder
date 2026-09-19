"""What a program is made of: a shape, an If, a loop, a module."""

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
        self.lines = []                 # a grouped box: a line per statement
        self.scope = ""                 # "global": written outside every
                                        #   module, so every chart can see it


class If:
    kind = "if"

    def __init__(self, cond):
        self.cond = cond
        self.text = ""                  # the line as it was written
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
        self.text = ""                  # the line as it was written
        self.body = []
        self.until = False              # keep looping while cond is FALSE
        self.hex = False                # draw the test as a hexagon (For Each ...)
        self.node_id = 0
        self.line = 0


class For:
    kind = "for"

    def __init__(self, raw, init=None, cond=None, step=None):
        self.raw = self.text = raw      # the For line as written
        self.init, self.cond, self.step = init, cond, step
        self.body = []
        self.node_id = 0
        self.line = 0


class Select:
    kind = "select"

    def __init__(self, expr):
        self.expr = expr
        self.text = ""                  # the line as it was written
        self.branches = []              # list of [label, items]
        self.pre = []                   # statements before the first Case (ignored)
        self.node_id = 0
        self.line = 0


class Module:
    def __init__(self, kind, name, params, header, rtype=""):
        self.kind, self.name, self.params, self.header = kind, name, params, header
        self.rtype = rtype              # "Real" in "Function Real calcTax(...)"
        self.items = []
        self.line = 0                   # the line its header was typed on

    def signature(self):
        return "%s(%s)" % (self.name, self.params)


