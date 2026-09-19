"""The studio page, and the parts it is poured together from."""
import html
import io
import os
import re

from . import settings


# The page is not one file.  Its styling is seven, its script is twenty-odd,
# and they are separate on purpose: a stylesheet an editor can color and
# fold beats one enormous string, and a script cut into parts is a script
# somebody can find their way around.  They are poured into studio.html
# here, where the @@CSS@@ and @@JS@@ marks are, and the page that comes out
# is the page the studio serves.
#
# The page the studio serves and the page --site writes are both this
# one, poured together here, so there is one answer to what the studio
# looks like and everywhere gets it.
HERE = os.path.dirname(os.path.abspath(__file__))

# The stylesheet, in order.
CSS = ["css/01-base.css", "css/02-bar.css", "css/03-layout.css",
       "css/04-panel.css", "css/05-chart.css", "css/06-screens.css",
       "css/07-motion.css"]

# The script.  These run inside one function and share everything between
# them, so this order is the order they happen in: a later part may use what
# an earlier one made, never the other way round.
JS = ["js/01-start.js", "js/02-paint.js", "js/03-shapes.js",
      "js/04-panel.js", "js/05-keep.js", "js/06-chart.js", "js/07-sides.js",
      "js/08-save.js", "js/09-build.js", "js/10-hand.js",
      "js/11-hand-panel.js", "js/12-check.js", "js/13-hand-keep.js",
      "js/14-run.js", "js/15-sums.js", "js/16-wrong.js", "js/17-tape.js",
      "js/18-code.js", "js/19-files.js", "js/20-menu.js", "js/21-typing.js",
      "js/22-settings.js", "js/23-undo.js", "js/24-scroll.js",
      "js/25-keys.js", "js/26-motion.js", "js/27-mend.js", "js/99-go.js"]

# Each part of the page carries a header saying what it is and that it is
# one part of something; the page itself wants the part, not the header.
JS_HEAD_END = "// " + "-" * 75 + "\n"
CSS_HEAD_END = "   " + "-" * 75 + " */\n"


def read_ui(name):
    """One of the page's own files, as it is written."""
    with io.open(os.path.join(HERE, "ui", name), encoding="utf-8") as f:
        return f.read()


def without_header(text, ending):
    """A part, with the header that explains it taken off."""
    at = text.rfind(ending)
    return text[at + len(ending):] if at >= 0 else text


def page_html():
    """studio.html with its stylesheet and its script poured in."""
    html = read_ui("studio.html")
    for mark, names, ending in (("@@CSS@@", CSS, CSS_HEAD_END),
                                ("@@JS@@", JS, JS_HEAD_END)):
        if mark not in html:
            raise ValueError("ui/studio.html has lost its %s mark" % mark)
        html = html.replace(mark, "".join(
            without_header(read_ui(name), ending) for name in names), 1)
    return html


def clashes():
    """Two parts of the page's script naming the same thing.

    The parts run inside one function and share everything between them,
    which is what lets a later part use what an earlier one made.  The cost
    is that two parts using the same name are not two things: the later
    declaration simply replaces the earlier, silently, and whatever used
    the first one stops working.  tests/run.py refuses to pass over it.
    """
    seen, found = {}, []
    for name in JS:
        text = without_header(read_ui(name), JS_HEAD_END)
        for line in text.split("\n"):
            got = re.match(r"^  (?:async\s+)?(function|var|let|const)\s+(.*)$",
                           line)
            if not got:
                continue
            rest = got.group(2)
            if got.group(1) == "function":
                words = re.findall(r"^([A-Za-z_$][\w$]*)", rest)
            else:               # var a, b = 1, c;  -- every name in the line
                words = re.findall(
                    r"(?:^|,)\s*([A-Za-z_$][\w$]*)\s*(?==|,|;|$)", rest)
            for word in words:
                if word in seen and seen[word] != name:
                    found.append((word, seen[word], name))
                else:
                    seen.setdefault(word, name)
    return found
