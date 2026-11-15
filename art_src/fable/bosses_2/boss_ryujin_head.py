"""Ryujin dragon-king head (~48 px). Upper skull fixed (translates only); lower jaw rotates on its hinge.
Neck joint: round stub at the right, centre = local (60,35) -> cell (OX+60, OY+35), radius ~15 (matches boss_ryujin_seg)."""
from k2 import *

NAME = 'boss_ryujin_head'
CW, CH = 168, 112
OX, OY = 52, 26
J_ = ('j0', 'j1', 'j2')
JL = ('j1', 'j2', 'j3')
BL = ('c0', 'c1', 'c2')
MN = ('v0', 'v1', 'v2')
BN = ('b0', 'b1', 'b2')
BNF = ('s0', 'b0', 'b1')
LEG = dict(zip('KyYZqwxvabcdmVW', ['K', 'y1', 'y2', 'y3', 'q', 'b2', 'b3', 'b1', 'j0', 'j1', 'j2', 'j3', 'm2', 'v2', 'v3']))

EYE = """
......KKKKKKK.
...KKKYYYYYyKK
KKKyYYZZKYYYyK
.KKayYYZKYYyKK
...KKayyKyyKK.
.....KKKKKKa..
"""
FANG_U = """
xww.
xwwv
xwwv
xwv.
xwv.
xv..
xv..
x...
"""
FANG_S = """
xw
xv
x.
"""
FANG_L = """
x..
xw.
xwv
xwv
"""
TOOTH_L = """
x.
xv
"""

DEF = dict(dx=0, dy=0, jaw=12, wh=0, mane=0, pearl=0, tongue=0)


def head(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    ox, oy = OX + S['dx'], OY + S['dy']
    mn = S['mane']

    def P(x, y):
        return (x + ox, y + oy)
    HINGE = P(44, 38)

    def J(x, y):
        return rot(P(x, y), HINGE, -S['jaw'])

    def tuft(base, ang, ln, w, ramp=MN, lnc='K', bend=22):
        p = C()
        m = lock(base, ang, ln, w, bend)
        p.form(m, ramp, sd=2, hl=1)
        c.stamp(p, lnc, skip=('v0', 'v1', 'v2', 'v3') if ramp is MN else ())

    # ---- far antler (darker)
    def antler(o, ramp):
        p = C()
        beam = curve([o, add(o, (4, -9)), add(o, (11, -16)), add(o, (20, -20))], 6)
        m = tube(beam, [(0, 2.4), (0.6, 1.9), (1, 0.8)])
        m |= L(*add(o, (3.5, -7)), 1.7, *add(o, (-3, -14)), 0.6)          # brow tine (forward)
        m |= L(*add(o, (9.5, -14.5)), 1.6, *add(o, (8, -23)), 0.6)        # top tine
        p.form(m, ramp, sd=1, hl=1)
        c.stamp(p, 'K')
    antler(P(46, 16), BNF)

    # ---- mane behind the skull (flows back/right)
    for (x, y, a, ln, w) in [(58, 18, 322, 22, 9), (62, 24, 340, 26, 10), (63, 34, 0, 24, 10), (60, 42, 22, 20, 9), (55, 48, 44, 14, 7)]:
        tuft(P(x, y), a - mn, ln + mn * 0.3, w)

    # ---- neck stub
    p = C()
    neck = L(*P(52, 34), 14.4, *P(61, 35), 14.6)
    p.form(neck, J_, sd=6, hl=1)
    belly = neck & (px.Y > oy + 42)
    p.form(belly, BL, sd=2, hl=0)
    for x in (48, 54, 60, 66, 72):
        p.line([P(x, 42), P(x + 1, 51)], 'c0', only=belly)
    scales(p, neck & ~belly, 'j0', ('j1',), 6, 4, light='j3', lon=('j2',), x0=ox % 6, y0=oy % 4)
    c.stamp(p, 'K')

    # ---- mouth interior + tongue
    p = C()
    mouth = PG([HINGE, P(9, 33), J(9, 37), J(26, 39)])
    p.fill(mouth, 'q')
    p.fill(PG([P(40, 35), P(22, 34), P(32, 37)]) & mouth, 'm0')
    c.stamp(p, 'K')
    if S['tongue']:
        p = C()
        a, b = J(30, 38), J(12 - S['tongue'], 34)
        p.fill(L(a[0], a[1], 2.2, b[0], b[1], 1.2), 'm2')
        p.line([a, b], 'm3')
        c.stamp(p, 'K')

    # ---- lower jaw + beard
    for (x, y, a, ln, w) in [(12, 43, 110, 9, 5), (19, 45, 96, 12, 6)]:
        b_ = J(x, y)
        tuft(b_, a + S['jaw'] * 0.5 - mn * 0.5, ln, w, bend=-30)
    p = C()
    jaw = PG([J(48, 35), J(30, 37), J(9, 36.5), J(4, 38), J(6, 41.5), J(18, 45), J(34, 47.5), J(48, 48)]) | E(*J(44, 42), 7, 6.4)
    p.form(jaw, BL, sd=2, hl=0)
    top = PG([J(48, 34), J(30, 36.5), J(9, 36), J(3, 37.5), J(8, 40.5), J(30, 41.5), J(48, 42)]) & jaw
    p.form(top, J_, sd=1, hl=1)
    for x in (13, 19, 25, 31, 37):
        p.line([J(x, 41), J(x + 1.5, 47.5)], 'c0', only=jaw & ~top)
    c.stamp(p, 'K')
    p = C()
    for x, g in ((7, FANG_L), (14, TOOTH_L), (19, TOOTH_L), (24, TOOTH_L)):
        q_ = J(x, 36.5)
        p.grid(int(round(q_[0])), int(round(q_[1])) - len(g.strip().split('\n')), g, LEG)
    c.stamp(p, 'K')

    # ---- pearl under the chin
    pr = S['pearl']
    pc = J(31, 54)
    p = C()
    p.fill(E(pc[0], pc[1], 6.4 + pr, 6.4 + pr), 'a0')
    p.fill(E(pc[0], pc[1], 5.4, 5.4), 'a1')
    p.fill(E(pc[0] - 1, pc[1] - 1, 3.6, 3.6), 'a2')
    p.fill(E(pc[0] - 2, pc[1] - 2, 1.5, 1.5), 'v3')
    c.stamp(p, 'K')

    # ---- upper skull
    p = C()
    skull = PG([P(2, 31), P(2, 27), P(6, 24), P(14, 24), P(22, 22), P(28, 16), P(38, 13), P(50, 15), P(60, 21), P(64, 30),
                P(60, 40), P(50, 43), P(43, 38), P(30, 36), P(14, 35), P(5, 35)]) | E(*P(7, 28), 6, 6)
    p.form(skull, J_, sd=4, hl=1)
    cheek = E(*P(49, 30), 10.4, 9.4) & skull
    p.form(cheek, J_, sd=3, hl=1)
    # snout top plane
    p.fill(PG([P(11, 25), P(22, 23), P(27, 19), P(28, 22), P(22, 26), P(12, 27)]) & skull, 'j2')
    # nose bulb + nostril
    nose = E(*P(7, 28), 5.6, 5.6) & skull
    p.form(nose, JL, sd=2, hl=1)
    p.fill(R(*P(4, 29), *P(6, 30)), 'K')
    p.pxs([P(5, 25), P(6, 25), P(7, 25)], 'j4')
    p.fill(R(*P(29, 17), *P(33, 17)), 'j4', only=skull)
    # upper lip
    for x in (13, 19, 25, 31, 37):
        p.line([P(x, 31), P(x, 36)], 'j0', only=skull & (px.Y >= oy + 31))
    p.line([P(11, 31), P(30, 32), P(41, 34)], 'j0', only=skull)
    scales(p, skull & ~nose, 'j0', ('j1',), 6, 4, light='j3', lon=('j2',), x0=ox % 6 + 2, y0=oy % 4 + 1)
    # brow ridge
    brow = PG([P(17, 24), P(27, 16), P(40, 14), P(42, 17), P(30, 20), P(20, 27)])
    p.form(brow & skull, ('j0', 'j2', 'j3'), sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.grid(ox + 20, oy + 20, EYE, LEG)
    c.stamp(p, ring=False)
    # fangs
    p = C()
    p.grid(ox + 9, oy + 34, FANG_U, LEG)
    for x in (17, 23, 29, 35):
        p.grid(ox + x, oy + 35, FANG_S, LEG)
    c.stamp(p, 'K')
    # cheek frill + bushy brow tuft (mane, on top of the skull)
    for (x, y, a, ln, w) in [(53, 38, 36, 15, 7), (56, 31, 12, 18, 8), (55, 23, 350, 17, 7)]:
        tuft(P(x, y), a - mn, ln + mn * 0.3, w)
    tuft(P(31, 16), 318 - mn, 13, 5, bend=40)
    # near antler
    antler(P(39, 15), BN)
    # ---- whiskers (gold), from the nose
    w_ = S['wh']
    for (pts, lnc) in [([(8, 32), (0, 38), (-10, 37 + w_), (-18, 30 + w_ * 2), (-22, 22 + w_ * 2)], 'K'),
                       ([(5, 26), (-4, 24), (-12, 17 - w_), (-14, 8 - w_ * 2)], 'K')]:
        p = C()
        cv = curve([P(*q) for q in pts], 8)
        m = tube(cv, [(0, 1.5), (0.5, 1.1), (1, 0.55)])
        p.form(m, ('y0', 'y1', 'y2'), sd=1, hl=0)
        c.stamp(p, lnc)
    c.blacken()
    return c


WALK = [dict(dy=0, jaw=12, wh=0, mane=0), dict(dy=-1, jaw=14, wh=2, mane=5, pearl=1),
        dict(dy=0, jaw=12, wh=0, mane=0, tongue=0), dict(dy=1, jaw=9, wh=-2, mane=-5, pearl=1)]
ATTACK = [dict(dx=14, dy=-4, jaw=26, wh=-3, mane=-8), dict(dx=-22, dy=3, jaw=40, wh=4, mane=10, tongue=3, pearl=1),
          dict(dx=-8, dy=1, jaw=3, wh=1, mane=4)]

if __name__ == '__main__':
    export(NAME, head, WALK, ATTACK)
