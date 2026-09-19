"""One drawing, from what the studio asked for."""
import re

from .. import settings
from ..make.chart import make_flowchart
from ..make.shake import style_variety
from ..parse.data import program_json
from ..parse.read import parse_program
from ..shapes import DEFAULT_GEOM, SHAPES
from ..words.lookup import apply_language, word


# ------------------------------------------------------------- the studio --
def file_name(title):
    """A title, made safe to save under."""
    clean = re.sub(r'[\\/:*?"<>|]+', " ", title or "").strip()
    return re.sub(r"\s+", " ", clean) or "flowchart"


def draw_for_studio(ask):
    """One drawing, from what the studio asked for."""
    if ask.get("lang"):
        apply_language(ask["lang"])
    text = ask.get("text") or ""
    if not text.strip():
        raise ValueError(word("no_code"))
    want = str(ask.get("seed") or "").strip()
    seed = style_variety(int(want) if want.isdigit() else None)
    shape = str(ask.get("shape") or "auto").lower()
    settings.SHAPE = "" if shape in ("tall", "off", "none", "") else shape
    settings.LEGEND = bool(ask.get("legend"))
    settings.GRID = bool(ask.get("grid", True))
    settings.GEOM = dict(DEFAULT_GEOM)                  # which shape draws which kind
    for kind, drawn in (ask.get("shapes") or {}).items():
        if kind in settings.GEOM and drawn in SHAPES:
            settings.GEOM[kind] = drawn
    for shape_kind in settings.FILL:                    # tinted, or plain black and white
        settings.FILL[shape_kind] = settings.TINTS[shape_kind] if ask.get("tint") else "#ffffff"
    title = (ask.get("title") or "").strip() or None
    author = (ask.get("author") or "").strip() or None
    svg = make_flowchart(text, title, author)
    box = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    ast = program_json(parse_program(text))
    return {"ok": True, "svg": svg.split("\n", 1)[1], "seed": seed,
            "w": box.group(1) if box else "", "h": box.group(2) if box else "",
            "title": title or "Flowchart", "name": file_name(title),
            "ast": ast, "problems": ast["problems"]}


