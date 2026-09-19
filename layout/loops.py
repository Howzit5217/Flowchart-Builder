"""While and Repeat, and the line back up."""
from .. import settings
from ..layout import blocks
from ..layout.blocks import (
    Block, clear_foot, layout_seq, node_block, part_of, shift, tail_shape)
from ..measure import text_w
from ..parse.nodes import Loop
from ..words.lookup import word


def layout_pre(item):
    """While: test first.  (Do Until ... Loop swaps the Yes / No labels.)"""
    shape = "hex" if item.hex else "diamond"
    dia = node_block(part_of(item, shape, item.cond))
    body = layout_seq(item.body)
    half = dia.w / 2.0
    into, out = (settings.NO, settings.YES) if item.until else (settings.YES, settings.NO)
    if item.hex:
        into = out = ""

    elems = shift(dia.elems, -dia.axis, 0)
    y = dia.h
    elems += [("line", 0, y, 0, y + settings.VGAP, True),
              ("text", 5, y + settings.VGAP / 2.0 + 4, into, "start")]
    y += settings.VGAP
    elems += shift(body.elems, -body.axis, y)
    body_top = y
    y += body.h

    back_x = -(max(half, body.axis) + settings.HGAP)
    if not body.terminal:
        # The way back starts by going sideways, so where the body ends on a
        # box it leaves that box's side.  Dropping out of the bottom first
        # only to turn left buys nothing and costs a corner.
        foot = tail_shape(body)
        edge = foot[0] - body.axis if foot else None
        if edge is not None and edge - 2 > back_x:
            turn = foot[2] + body_top
            elems.append(("line", edge, turn, back_x, turn, False))
        elif clear_foot(body, -1):
            # Nothing of the body's lies along its foot on this side, so the
            # way back sets off from the foot itself.  Stepping down first
            # and then turning puts a jog in the line for no reason -- and
            # where what ends the body is a loop, whose own way out arrives
            # at that foot going this way already, the two are one straight
            # line and read as one.
            turn = y
            elems.append(("line", 0, turn, back_x, turn, False))
        else:
            turn = y + settings.VGAP / 2.0
            elems += [("line", 0, y, 0, turn, False),
                      ("line", 0, turn, back_x, turn, False)]
        elems += [("line", back_x, turn, back_x, -settings.LOOP_UP, False),
                  ("line", back_x, -settings.LOOP_UP, 0, -settings.LOOP_UP, False),
                  ("line", 0, -settings.LOOP_UP, 0, 0, True)]

    exit_y = y + settings.VGAP
    right_x = max(half, body.w - body.axis) + max(
        settings.HGAP, text_w(out, bold=True) + settings.LABEL_PAD)
    # The way out is not finished when it reaches the line below: it *is*
    # that line, and carries on down it.  Left as the end of a route it
    # would stop dead there with a head on it, and the turn would come out
    # square, drawn as two strokes meeting rather than one line bending.
    elems += [("line", half, dia.h / 2.0, right_x, dia.h / 2.0, False),
              ("text", half + 6, dia.h / 2.0 - 6, out, "start"),
              ("line", right_x, dia.h / 2.0, right_x, exit_y, False),
              ("line", right_x, exit_y, 0, exit_y, False)]

    left = -back_x
    return Block(left + right_x, exit_y + settings.LOOP_UP, left,
                 shift(elems, left, settings.LOOP_UP), loop=True)


def layout_post(item):
    """Do ... While / Do ... Until / Repeat ... Until: body first, test last."""
    body = layout_seq(item.body)
    dia = node_block(part_of(item, "diamond", item.cond or word("again")))
    half = dia.w / 2.0
    again, done = (settings.NO, settings.YES) if item.until else (settings.YES, settings.NO)

    elems = shift(body.elems, -body.axis, 0)
    y = body.h
    if not body.terminal:
        elems.append(("line", 0, y, 0, y + settings.VGAP, True))
    y += settings.VGAP
    dia_cy = y + dia.h / 2.0
    elems += shift(dia.elems, -dia.axis, y)
    y += dia.h

    back_x = -(max(half, body.axis) + settings.HGAP)
    elems += [("line", -half, dia_cy, back_x, dia_cy, False),
              ("text", -half - 6, dia_cy - 6, again, "end"),
              ("line", back_x, dia_cy, back_x, -settings.LOOP_UP, False),
              ("line", back_x, -settings.LOOP_UP, 0, -settings.LOOP_UP, False),
              ("line", 0, -settings.LOOP_UP, 0, 0, True),
              ("text", 5, y + 13, done, "start")]

    left = -back_x
    right = max(half, body.w - body.axis)
    return Block(left + right, y + settings.LOOP_UP, left, shift(elems, left, settings.LOOP_UP))


def layout_for(item):
    if settings.FOR_STYLE == "expand" and item.cond:
        loop = Loop("pre", item.cond)
        loop.node_id, loop.line = item.node_id, item.line
        step = [part_of(item, "rect", item.step)] if item.step else []
        start = [part_of(item, "rect", item.init)] if item.init else []
        loop.body = list(item.body) + step
        return layout_seq(start + [loop])
    loop = Loop("pre", item.raw)             # one hexagon holding the whole For
    loop.hex = True
    loop.node_id, loop.line = item.node_id, item.line
    loop.body = item.body
    return layout_pre(loop)


def layout_loop(item):
    """A While or a Repeat: which one decides where the test is drawn."""
    return layout_post(item) if item.style == "post" else layout_pre(item)


blocks.LAYOUTS["loop"] = layout_loop
blocks.LAYOUTS["for"] = layout_for
