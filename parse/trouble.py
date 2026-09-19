"""What the reading had to paper over, and where it happened."""
from ..words.lookup import word


# ----------------------------------------------------- what it had to fix --
# Pseudocode is read forgivingly, and that is right: an If with no End If
# still draws, a line nobody can make sense of still gets a box, and a chart
# you can look at is worth more than a refusal to draw one.  But forgiving is
# not the same as silent.  An If left open swallows every line below it; a
# stray End If closes something that was not meant to close; a Do with no
# Until never stops.  Each of those draws a chart that is not the one that
# was meant, and the only clue is a picture that looks wrong somewhere.
#
# So the reading keeps a note of everything it had to paper over, with the
# line it happened on, and the studio lists them under the button.
PROBLEMS = []


def trouble(key, line, text="", fix=None, **fill):
    """Note something the reading papered over, and where it was.

    `fix` is what would put it right, where there is one right answer:
    {"how": "drop", "at": n} to take a line out, or {"how": "insert",
    "text": "End If", "at": n, "like": n} to put one in.  The studio makes
    a button of it.  Most of these have no such answer -- a Do with no test
    needs a test somebody has to write -- and those carry none, because a
    fix that guesses is worse than a warning that waits.
    """
    fill.setdefault("line", line)
    PROBLEMS.append({"line": line, "text": text, "why": key,
                     "says": word(key, **fill), "fix": fix or {}})


# Which structure was left open, said in its own words.
OPEN_TROUBLE = {"if": "w_open_if", "loop": "w_open_loop",
                "for": "w_open_for", "select": "w_open_select"}
