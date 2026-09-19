"""The seeded shake that makes two runs look different."""
import random

from .. import settings


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
    if seed is None:
        seed = random.randrange(1000, 99999)
    r = random.Random(seed)
    # The gaps down the page are whole grid steps, and the grid is chosen
    # first so they can be.  Everything a shape's height is built from is
    # rounded up to a pair of steps later, so a chart lands on the ruling
    # behind it however these fall out.
    settings.GRID_STEP = r.choice((16, 20, 24))
    settings.GRID_MAJOR = r.choice((4, 5))
    settings.VGAP = settings.GRID_STEP                    # the gaps, and the air inside a shape
    settings.HGAP = r.randint(22, 30)
    settings.PAD_Y = r.randint(8, 11)
    settings.LABEL_PAD = r.randint(10, 14)
    settings.NODE_MIN_H = r.randint(30, 36)
    settings.NODE_W = r.randint(124, 142)
    settings.NODE_MAX_W = r.randint(172, 200)
    settings.DIA_W = r.randint(126, 146)
    settings.DIA_MIN_H = r.randint(44, 54)
    settings.OVAL_W = r.randint(92, 104)
    settings.OVAL_H = r.randint(34, 40)
    settings.CORNER_R = r.randint(3, 9)          # how softly a corner turns
    settings.SLANT = r.randint(10, 14)           # the lean on a parallelogram
    settings.LOOP_UP = settings.GRID_STEP                 # the reach of a loop's way back
    settings.FORK_LIMIT = r.randint(280, 360)    # where the layout changes its mind
    settings.CHAIN_LIMIT = r.randint(780, 1020)
    settings.GROUP_MAX = r.randint(4, 6)
    settings.TRUE_LEFT = r.random() < 0.7        # mostly the usual way round
    settings.SHAKE = r                           # the shape search nudges with this
    return seed


