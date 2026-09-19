"""How wide words come out, and how tall a line of them is."""

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


# Measured once per piece of text, not once per asking.  Laying a chart out
# is not done once: the same program is laid out several ways over, to pick
# the outline that fits best, and inside each of those a line of words is
# measured again for every width it might wrap at.  On a chart of a few
# thousand shapes that came to half a million measurements of a few thousand
# different strings -- the same answers, worked out over and over, adding a
# second to every press of the button.  Keeping them costs a dictionary.
_WIDTHS = {}
_WIDTH_MAX = 200000                 # a long-lived studio should not grow for ever


def text_w(s, size=None, bold=False):
    """How wide s really comes out, in pixels."""
    if size is None:
        size = FONT_SIZE            # in the key: the size can be changed
    key = (s, size, bold)
    got = _WIDTHS.get(key)
    if got is not None:
        return got
    table = _ADV_B if bold else _ADV_N
    total = 0
    for ch in s:
        i = ord(ch) - 32
        total += table[i] if 0 <= i < len(table) else 556
    got = total * size / 1000.0
    if len(_WIDTHS) >= _WIDTH_MAX:
        _WIDTHS.clear()
    _WIDTHS[key] = got
    return got
