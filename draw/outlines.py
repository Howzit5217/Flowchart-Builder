"""Each shape's outline."""
from .. import settings


def shape_art(kind, cx, cy, w, h, paint):
    """One shape, drawn: the outline and whatever goes with it.

    Every kind in SHAPES is here.  The first six are the ones a textbook
    uses; the rest are the ones that turn up in the back of the chapter --
    a document, a drum for a file, a wait, a joining point, a step done by
    hand -- and any of them can stand in for any kind of step.
    """
    l, r = cx - w / 2.0, cx + w / 2.0
    t, b = cy - h / 2.0, cy + h / 2.0
    lean = min(settings.SLANT, w / 4.0)
    out = []
    if kind in ("oval", "circle"):
        out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" '
                   'fill="%s"/>' % (cx, cy, w / 2.0, h / 2.0, paint))
    elif kind in ("rect", "sub"):
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        if kind == "sub":
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                       % (l + settings.BAR, t, l + settings.BAR, b))
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                       % (r - settings.BAR, t, r - settings.BAR, b))
    elif kind == "io":
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l + lean, t, r, t, r - lean, b, l, b, paint))
    elif kind == "trap":
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l + lean, t, r - lean, t, r, b, l, b, paint))
    elif kind == "hex":
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l + lean, t, r - lean, t, r, cy, r - lean, b,
                      l + lean, b, l, cy, paint))
    elif kind == "doc":                       # a page, with a wave at its foot
        wave = min(10.0, h * 0.18)
        out.append('<path d="M%.1f,%.1f H%.1f V%.1f C%.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l, t, r, b - wave,
                      r - w * 0.25, b - wave * 2.2, r - w * 0.4, b + wave * 0.9,
                      cx, b - wave * 0.2,
                      l + w * 0.32, b - wave * 1.6, l + w * 0.18, b + wave * 0.7,
                      l, b - wave, paint))
    elif kind == "store":                     # a drum, for something kept
        lip = min(11.0, h * 0.24)
        out.append('<path d="M%.1f,%.1f V%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f '
                   'V%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z" fill="%s"/>'
                   % (l, t + lip, b - lip, w / 2.0, lip, r, b - lip,
                      t + lip, w / 2.0, lip, l, t + lip, paint))
        out.append('<path class="trim" d="M%.1f,%.1f A%.1f,%.1f 0 0 0 '
                   '%.1f,%.1f" fill="none"/>'
                   % (l, t + lip, w / 2.0, lip, r, t + lip))
    elif kind == "delay":                     # a wait: flat, then a half round
        bulge = min(h / 2.0, w / 2.0)
        out.append('<path d="M%.1f,%.1f H%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f '
                   'H%.1f Z" fill="%s"/>'
                   % (l, t, r - bulge, bulge, h / 2.0, r - bulge, b, l, paint))
    elif kind == "roundrect":
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                   'rx="%.1f" fill="%s"/>'
                   % (l, t, w, h, min(14.0, h / 2.4), paint))
    elif kind == "io_back":                   # leaning the other way
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l, t, r - lean, t, r, b, l + lean, b, paint))
    elif kind == "manual":                    # typed in: a sloping top
        slope = min(11.0, h * 0.28)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (l, t + slope, r, t, r, b, l, b, paint))
    elif kind == "card":                      # a punched card
        nick = min(14.0, h * 0.34)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f" fill="%s"/>'
                   % (l + nick, t, r, t, r, b, l, b, l, t + nick, paint))
    elif kind == "note":                      # a page with a folded corner
        fold = min(14.0, h * 0.34)
        out.append('<path d="M%.1f,%.1f H%.1f L%.1f,%.1f V%.1f H%.1f Z" '
                   'fill="%s"/>' % (l, t, r - fold, r, t + fold, b, l, paint))
        out.append('<path class="trim" d="M%.1f,%.1f V%.1f H%.1f" fill="none"/>'
                   % (r - fold, t, t + fold, r))
    elif kind == "docs":                      # a few pages of it
        step = min(5.0, h * 0.12)
        for back in (2, 1):
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                       'rx="2" fill="%s"/>'
                       % (l + back * step, t + (2 - back) * 0, w - back * step,
                          h - back * step * 2, paint))
        out += shape_art("doc", cx - step, cy + step, w - 2 * step,
                         h - 2 * step, paint)
    elif kind == "screen":                    # shown to somebody
        bow = min(16.0, w * 0.16)
        out.append('<path d="M%.1f,%.1f H%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f '
                   'H%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l + bow, t, r - bow, h / 2.0, h / 2.0, r - bow, b,
                      l + bow, l, cy + h * 0.28, l, cy - h * 0.28, l + bow, t,
                      paint))
    elif kind == "offpage":                   # it carries on somewhere else
        point = min(18.0, h * 0.42)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f" fill="%s"/>'
                   % (l, t, r, t, r, b - point, cx, b, l, b - point, paint))
    elif kind == "loop":                      # a loop's limit: For, mostly
        cut = min(14.0, h * 0.34, w / 5.0)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l + cut, t, r - cut, t, r, t + cut, r, b, l, b,
                      l, t + cut, paint))
    elif kind == "parallel":                  # things happening side by side
        bar = max(2.5, min(5.0, h * 0.11))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        out.append('<path class="trim" d="M%.1f,%.1f H%.1f M%.1f,%.1f H%.1f" '
                   'fill="none"/>' % (l, t + bar * 2, r, l, b - bar * 2, r))
    elif kind == "stored":                    # held somewhere inside
        rule = min(11.0, w * 0.14)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        out.append('<path class="trim" d="M%.1f,%.1f V%.1f M%.1f,%.1f H%.1f" '
                   'fill="none"/>' % (l + rule, t, b, l, t + rule, r))
    elif kind == "cloud":                     # a service, or somewhere else
        # Drawn to touch its box at the middle of all four sides, which is
        # where a line joining it expects to meet it.
        qw, qh = w / 2.0, h / 2.0
        out.append('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l, cy,
                      l, cy - qh * 0.75, cx - qw * 0.72, t - qh * 0.18,
                      cx - qw * 0.34, t + qh * 0.16,
                      cx - qw * 0.1, t - qh * 0.2, cx + qw * 0.34, t - qh * 0.2,
                      cx + qw * 0.42, t + qh * 0.2,
                      cx + qw * 0.85, t + qh * 0.02, r, cy - qh * 0.7, r, cy,
                      r, cy + qh * 0.72, cx + qw * 0.5, b, cx, b,
                      cx - qw * 0.55, b, l, cy + qh * 0.75, l, cy, paint))
    elif kind == "text":                      # words on their own
        # Nothing is drawn but something has to be there to take hold of,
        # so the words sit on a pane of clear glass.
        out.append('<rect class="ghost" x="%.1f" y="%.1f" width="%.1f" '
                   'height="%.1f" fill="none" pointer-events="all"/>'
                   % (l, t, w, h))
    elif kind == "actor":                     # somebody, rather than something
        head = min(h * 0.17, w * 0.17)
        neck = t + head * 2
        hip = t + h * 0.62
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
                   % (cx, t + head, head, paint))
        out.append('<path class="trim" d="M%.1f,%.1f V%.1f M%.1f,%.1f H%.1f '
                   'M%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f" fill="none"/>'
                   % (cx, neck, hip, cx - w * 0.22, neck + h * 0.12, cx + w * 0.22,
                      cx, hip, cx - w * 0.2, b, cx, hip, cx + w * 0.2, b))
    elif kind == "callout":                   # something said about it
        tail = min(16.0, h * 0.28)
        sill = b - tail
        rnd = min(10.0, h / 4.0)
        out.append('<path d="M%.1f,%.1f H%.1f Q%.1f,%.1f %.1f,%.1f V%.1f '
                   'Q%.1f,%.1f %.1f,%.1f H%.1f L%.1f,%.1f L%.1f,%.1f H%.1f '
                   'Q%.1f,%.1f %.1f,%.1f V%.1f Q%.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (l + rnd, t, r - rnd, r, t, r, t + rnd, sill - rnd,
                      r, sill, r - rnd, sill, l + w * 0.34, l + w * 0.2, b,
                      l + w * 0.24, sill, l + rnd, l, sill, l, sill - rnd,
                      t + rnd, l, t, l + rnd, t, paint))
    elif kind == "cube":
        lip = min(14.0, h * 0.26, w * 0.14)
        out.append('<path d="M%.1f,%.1f L%.1f,%.1f H%.1f V%.1f L%.1f,%.1f '
                   'H%.1f Z" fill="%s"/>'
                   % (l, t + lip, l + lip, t, r, b - lip, r - lip, b, l, paint))
        out.append('<path class="trim" d="M%.1f,%.1f H%.1f V%.1f M%.1f,%.1f '
                   'L%.1f,%.1f" fill="none"/>'
                   % (l, t + lip, r - lip, b, r - lip, t + lip, r, t))
    elif kind == "step":                      # one step of several, in a row
        notch = min(22.0, w * 0.16)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l, t, r - notch, t, r, cy, r - notch, b, l, b,
                      l + notch, cy, paint))
    elif kind == "table":
        head = min(16.0, h * 0.3)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                   'fill="%s"/>' % (l, t, w, h, paint))
        out.append('<path class="trim" d="M%.1f,%.1f H%.1f M%.1f,%.1f V%.1f '
                   'M%.1f,%.1f V%.1f" fill="none"/>'
                   % (l, t + head, r, l + w / 3.0, t + head, b,
                      l + w * 2.0 / 3.0, t + head, b))
    elif kind == "arrow":                     # which way it goes
        head = min(26.0, w * 0.3)
        wing = h * 0.26
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   '%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (l, t + wing, r - head, t + wing, r - head, t,
                      r, cy, r - head, b, r - head, b - wing, l, b - wing, paint))
    else:                                     # a decision
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" '
                   'fill="%s"/>' % (cx, t, r, cy, cx, b, l, cy, paint))
    return out


