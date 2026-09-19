"""Select Case, and the lane each branch gets."""
from .. import settings
from ..layout import blocks
from ..layout.blocks import Block, layout_seq, node_block, shift
from ..measure import text_w
from ..parse.nodes import Node


def layout_select(item):
    """Case structure: one diamond, one branch per Case, all merging below."""
    dia = node_block(Node("diamond", item.expr))
    if not item.branches:
        return dia
    branches = []
    for label, items in item.branches:
        b = layout_seq(items)
        need = text_w(label, bold=True) + 14     # room for the label beside the line
        if b.w - b.axis < need:
            b = Block(b.axis + need, b.h, b.axis, b.elems, b.terminal)
        branches.append((label, b))

    # branches side by side, their axes spread under the diamond
    axes, x = [], 0.0
    for i, (label, b) in enumerate(branches):
        if i:
            x += settings.HGAP
        axes.append(x + b.axis)
        x += b.w
    span = x
    center = span / 2.0
    bus_y = dia.h + settings.VGAP / 2.0
    top = dia.h + settings.VGAP + settings.GRID_STEP
    tallest = max(b.h for _, b in branches)
    all_end = all(b.terminal for _, b in branches)
    merge = top + tallest + (0 if all_end else settings.VGAP)

    elems = shift(dia.elems, center - dia.axis, 0)
    elems += [("line", center, dia.h, center, bus_y, len(axes) > 1),
              ("line", min(axes), bus_y, max(axes), bus_y, False)]
    x = 0.0
    for i, (label, b) in enumerate(branches):
        if i:
            x += settings.HGAP
        ax = axes[i]
        elems.append(("text", ax + 5, bus_y + 15, label, "start"))
        if b.h == 0:                              # empty Case: one plain line
            if not all_end:
                elems.append(("line", ax, bus_y, ax, merge, ax != center))
        else:
            elems.append(("line", ax, bus_y, ax, top, True))
            elems += shift(b.elems, x, top)
            if not b.terminal:
                elems.append(("line", ax, top + b.h, ax, merge, ax != center))
        x += b.w
    if not all_end:
        live = [axes[i] for i, (_, b) in enumerate(branches) if not b.terminal]
        lo, hi = min(live + [center]), max(live + [center])
        elems.append(("line", lo, merge, hi, merge, False))

    left = max(center, dia.w / 2.0)
    width = max(span, dia.w)
    return Block(width, merge, left, shift(elems, left - center, 0), all_end)


blocks.LAYOUTS["select"] = layout_select
