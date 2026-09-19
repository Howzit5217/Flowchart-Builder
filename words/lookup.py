"""Which language is on, and looking a word up in it."""
from .. import settings

# =============================================================================
#  Everything the chart and the page say, in one place per language.
#
#  Two sorts of text live in a language file: the few words the chart itself
#  draws (True, False, Start, End, and the names in the key) and everything
#  the page shows around it.  Nothing else in the code has words in it that a
#  reader sees, so a language is one of those files and nothing more.  The
#  pseudocode keywords are not there and are not translated: Display, If,
#  While and the rest are what you type, and they stay as they are whichever
#  language the chart is drawn in.
#
#  To add one: copy words/en.py, change the right-hand side of each line, and
#  end the file the way that one ends --
#
#      speaks("it", "Italiano", IT)
#
#  then add it to words/__init__.py so that it is read at all.  That is the
#  whole of it: the --lang choices, the picker in the studio and the copy
#  that travels with the page all come from what has registered, so there is
#  no second list anywhere to forget.  Anything a language leaves out falls
#  back to US English, so a half-finished translation is a perfectly good
#  one.
# =============================================================================

LANGUAGE = "en"                     # en, es, fr, de -- or --lang on the line

WORDS = {}                          # code -> what it says
NAMES = {}                          # code -> what it calls itself


def speaks(code, name, said):
    """One language, saying so itself at the foot of its own file."""
    WORDS[code] = said
    NAMES[code] = name
    return said


def word(key, **fill):
    """One piece of text, in whichever language is set.

    Anything a language leaves out falls back to US English, so a half
    finished translation still draws a whole chart."""
    said = WORDS.get(LANGUAGE, {}).get(key) or WORDS["en"].get(key, key)
    for name, value in fill.items():
        said = said.replace("{%s}" % name, str(value))
    return said


def in_full(code):
    """One language with English underneath it, so nothing is missing."""
    full = dict(WORDS["en"])
    full.update(WORDS.get(code) or {})
    return full


def apply_language(code):
    """Point the chart's own words at a language."""
    global LANGUAGE
    LANGUAGE = code if code in WORDS else "en"
    settings.YES, settings.NO = word("yes"), word("no")
    for kind in list(settings.LEGEND_NAME):
        settings.LEGEND_NAME[kind] = word("key_" + kind)
    return LANGUAGE
