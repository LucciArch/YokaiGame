"""Mokumokuren - a neglected, torn shoji screen whose paper panes have grown staring eyes."""
from kit import *

NAME = 'mokumokuren'
CW, CH = 136, 80
OX, OY = 76, 12           # local baseline y=62 ; screen spans x 0..45, y 3..62
WOOD = ('w0', 'w1', 'w2')

LEG = dict(zip('KwvuRYZq', ['K', 'v3', 'v2', 'v1', 'e0', 'y2', 'y3', 'q']))
BIG = """
....KKKKKK...
..KKwwwwvvKK.
.KwwRRRRwvvuK
KwwRYYYYRwvuK
KwRYYKKYYRvuK
KwRYZKKYYRvuK
KwwRYYYYRvvuK
.KvwRRRRvvuK.
..KKvvvvuKK..
....KKKKK....
"""
MID = """
..KKKKK..
.KwwwvvK.
KwRYYRvuK
KwYKKYvuK
KwRYYRvuK
.KvvvuuK.
..KKKKK..
"""
SMALL = """
.KKKKK.
KwYYYuK
KwYKYuK
KvYYYuK
.KKKKK.
"""
SLIT = """
KKKKKKK.
KKKKKKKK
KwYKYvuK
.KKKKKK.
"""

DEF = dict(dx=0, dy=0, shear=0, flap=0, flare=0, beam=None)
PW, PH = 13, 12            # pane size
X0, Y0 = 4, 7              # first pane (local)
FW, BASE = 48, 60          # frame width, baseline
# eyes: (pane col, pane row, grid, ox, oy)
EYES = [(1, 1, BIG, 0, 1), (0, 0, MID, 2, 3), (2, 0, SMALL, 4, 5), (1, 0, SLIT, 4, 7), (0, 1, SLIT, 1, 2), (0, 1, SMALL, 5, 6),
        (2, 1, MID, 3, 2), (0, 2, SMALL, 2, 2), (1, 2, MID, 2, 3), (2, 2, SMALL, 3, 5)]
HOLES = {(2, 2): [(1, 0), (10, 1), (12, 5), (11, 11), (4, 10), (0, 5)], (2, 1): [(1, 1), (12, 0), (12, 9), (8, 11), (2, 9)],
         (1, 0): [(0, 0), (9, 0), (6, 4), (2, 5)], (0, 2): [(7, 7), (12, 5), (12, 11), (8, 11)]}


def creature(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    shr = S['shear']

    def Q(x, y):
        return (x + OX + S['dx'] + shr * (BASE - y) / 57.0, y + OY + S['dy'])

    def box(x0, y0, x1, y1):
        return PG([Q(x0, y0), Q(x1, y0), Q(x1, y1), Q(x0, y1)])

    p = C()
    R_ = X0 + 3 * (PW + 1) - 1          # x of the far inner edge
    B_ = Y0 + 3 * (PH + 1) - 1          # y of the divider above the board
    # outer frame (near stile lit, far stile + sill in shadow)
    p.fill(box(0, 3, FW, BASE - 2), 'w1')
    p.fill(box(FW - 2, 3, FW, BASE - 2), 'w0')
    p.fill(box(0, 3, 1, BASE - 2) | box(0, 3, FW, 4), 'w2')
    p.fill(box(2, BASE - 4, FW, BASE - 2), 'w0')
    # paper panes
    for cx in range(3):
        for cy in range(3):
            x, y = X0 + cx * (PW + 1), Y0 + cy * (PH + 1)
            pane = box(x, y, x + PW - 1, y + PH - 1)
            lit = (cx + cy) <= 1
            p.fill(pane, 'c2' if lit else 'c1')
            p.fill(box(x + PW - 2, y, x + PW - 1, y + PH - 1) | box(x, y + PH - 1, x + PW - 1, y + PH - 1), 'c1' if lit else 'c0')
            if (cx, cy) in HOLES:
                hole = PG([Q(x + a, y + b) for a, b in HOLES[(cx, cy)]]) & pane
                p.fill(hole, 'K')
                p.fill(hole & ~sh(hole, 1, 1) & sh(hole, -1, -1), 'h1')
    # water stains
    for (x, y, rx, ry) in ((9, 40, 3.4, 2.2), (38, 10, 2.6, 2.0), (22, 12, 2.2, 1.4), (12, 27, 2.4, 1.6)):
        q = Q(x, y)
        m = E(q[0], q[1], rx, ry)
        p.fill(m & (p.a == I('c1')), 'c0'); p.fill(m & (p.a == I('c2')), 'c1')
    # lattice bars (kumiko); one is snapped
    for cx in (1, 2):
        x = X0 + cx * (PW + 1) - 1
        p.fill(box(x, 6, x, B_), 'w0')
    for cy in (1, 2):
        y = Y0 + cy * (PH + 1) - 1
        p.fill(box(3, y, R_, y), 'w0')
    p.fill(box(X0 + 2 * (PW + 1) - 1, Y0 + PH + 4, X0 + 2 * (PW + 1) - 1, Y0 + PH + 9), 'K')
    p.fill(box(3, 5, R_, 6) | box(2, 5, 3, B_) | box(R_, 5, R_ + 1, B_), 'w1')
    p.fill(box(3, 6, R_, 6) | box(3, 6, 3, B_), 'w0')
    # lower wooden board with plank seam, cracks and feet
    p.fill(box(3, B_, R_, B_), 'w0')
    p.fill(box(3, B_ + 1, R_, BASE - 5), 'w1')
    p.fill(box(3, B_ + 1, 28, B_ + 1), 'w2')
    p.fill(box(24, B_ + 2, 24, BASE - 5), 'w0')
    p.line([Q(8, B_ + 3), Q(11, B_ + 5), Q(10, B_ + 9)], 'w0')
    p.line([Q(36, B_ + 2), Q(34, B_ + 6)], 'w0')
    p.fill(box(1, BASE - 1, 7, BASE) | box(FW - 7, BASE - 1, FW - 1, BASE), 'w0')
    p.fill(box(1, BASE - 1, 7, BASE - 1), 'w1')
    c.stamp(p, 'K')
    # hanging paper flaps (flutter)
    f = S['flap']
    p = C()
    for (x, y, w, l) in ((32, 44, 4, 8), (18, 7, 4, 6), (11, 44, 3, 5)):
        a_ = Q(x, y)
        m = PG([a_, (a_[0] + w, a_[1]), (a_[0] + w - 1 + f, a_[1] + l), (a_[0] + f, a_[1] + l - 2)])
        p.fill(m, 'c1'); p.fill(m & ~sh(m, 1, 0), 'c2')
    c.stamp(p, 'c0')
    # eyes: identical grids every frame, only translated
    big = None
    for i, (cx, cy, g, ox, oy) in enumerate(EYES):
        q = Q(X0 + cx * (PW + 1) + ox, Y0 + cy * (PH + 1) + oy)
        gx, gy = int(round(q[0])), int(round(q[1]))
        if g is BIG:
            gx -= 0
            big = (gx, gy)
        c.grid(gx, gy, g, LEG)
        if S['flare'] and g is not SLIT:
            # flare: iris burns white-hot, four light ticks around the eye
            w_ = len(g.strip('\n').split('\n')[0]); h_ = len(g.strip('\n').split('\n'))
            mx, my = gx + w_ // 2 - 1, gy + h_ // 2
            c.pxs([(mx - 1, my), (mx - 1, my - 1)], 'y3')
            if S['flare'] > 1 or g is BIG:
                c.pxs([(gx - 2, my), (gx - 3, my)], 'y2')
    c.blacken()
    if S['beam']:
        x_end, th = S['beam']
        bx, by = big[0] + 4, big[1] + 5
        x1 = x_end + OX
        if th >= 2:
            c.fill(R(x1 + 2, by - 3, bx, by + 2) | E(x1 + 3, by - 0.5, 4.5, 3.4), 'e0')
            c.fill(R(x1 + 2, by - 2, bx, by + 1) | E(x1 + 3, by - 0.5, 3.4, 2.4), 'y2')
            c.fill(R(x1 + 1, by - 1, bx - 2, by), 'y3')
            c.fill(E(bx - 1, by - 0.5, 4.6, 4.6) & ~E(bx - 1, by - 0.5, 3.4, 3.4), 'y2')
            for k in range(3):
                xx = x1 + 12 + k * 13
                c.pxs([(xx, by - 5), (xx + 1, by - 5), (xx + 6, by + 4), (xx + 7, by + 4)], 'y2')
        else:
            for k in range(4):
                xx = x1 + 4 + k * 11
                c.fill(R(xx, by - 1, xx + 5, by), 'y2')
                c.fill(R(xx, by - 1, xx + 2, by - 1), 'y3')
    return c


WALK = [dict(), dict(dy=-2, shear=-2, flap=1), dict(dx=0, dy=0, shear=0, flap=0), dict(dy=-2, shear=2, flap=-1)]
ATTACK = [dict(shear=3, dy=-1, flare=1, flap=-1),
          dict(shear=-3, dx=-1, flare=2, flap=1, beam=(-66, 2)),
          dict(shear=-1, flare=1, beam=(-70, 1))]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
