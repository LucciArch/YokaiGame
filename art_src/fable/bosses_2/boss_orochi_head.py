"""Yamata-no-Orochi head (~40 px). Upper skull is fixed (only translates); the lower jaw rotates on its hinge.
Neck joint: the round stub at the right end, centre = local (52,27) -> cell (OX+52, OY+27), radius ~12."""
from k2 import *

NAME = 'boss_orochi_head'
CW, CH = 128, 80
OX, OY = 36, 18
G = ('g0', 'g1', 'g2')
GD = ('K', 'g0', 'g1')
BL = ('c0', 'c1', 'c2')
LEG = dict(zip('KeEZqwxvabcdm', ['K', 'e0', 'e1', 'y3', 'q', 'b2', 'b3', 'b1', 'g0', 'g1', 'g2', 'g3', 'm2']))

EYE = """
......KKKKKKK.
...KKKEEEEEeKK
KKKeEEZZKEEEeK
.KKaeEEZKEEeKK
...KKaeeKeeKK.
.....KKKKKKa..
"""
FANG_U = """
xww.
xwwv
xwwv
xwwv
xwv.
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
"""

DEF = dict(dx=0, dy=0, jaw=13, tongue=0, crest=0)


def head(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    ox, oy = OX + S['dx'], OY + S['dy']

    def P(x, y):
        return (x + ox, y + oy)
    HINGE = P(41, 30)

    def J(x, y):          # lower-jaw point, rotated about the hinge (jaw>0 opens)
        return rot(P(x, y), HINGE, -S['jaw'])

    # ---- neck stub (joint to the neck the game draws)
    p = C()
    neck = L(*P(44, 26), 12.4, *P(53, 27), 11.6)
    p.form(neck, G, sd=5, hl=1)
    belly = neck & (px.Y > oy + 32 + (px.X - ox - 40) * 0.05)
    p.form(belly, BL, sd=2, hl=0)
    for x in (42, 47, 52, 57):
        p.line([P(x, 31), P(x + 1, 40)], 'c0', only=belly)
    scales(p, neck & ~belly, 'g0', ('g1',), 5, 4, x0=ox % 5, y0=oy % 4)
    c.stamp(p, 'K')

    # ---- mouth interior + tongue
    p = C()
    mouth = PG([HINGE, P(8, 26), J(8, 28), J(24, 31)])
    p.fill(mouth, 'q')
    p.fill(PG([P(38, 27), P(22, 27), P(30, 29)]) & mouth, 'm0')           # palate glow
    c.stamp(p, 'K')
    t = S['tongue']
    if t:
        p = C()
        a, b = J(26, 29), J(8 - t, 27)
        mid = lerp(a, b, 0.7)
        p.fill(L(a[0], a[1], 1.6, mid[0], mid[1], 1.2), 'm2')
        p.fill(L(mid[0], mid[1], 1.0, b[0] - 3, b[1] - 3, 0.6) | L(mid[0], mid[1], 1.0, b[0] - 3, b[1] + 3, 0.6), 'm2')
        p.line([a, mid], 'm3')
        c.stamp(p, 'K')

    # ---- lower jaw
    p = C()
    jaw = PG([J(46, 27), J(30, 29), J(8, 28), J(4, 29.5), J(6, 32), J(16, 35), J(32, 38), J(46, 39)]) | \
        E(*J(42, 33), 6.5, 6)
    p.form(jaw, BL, sd=2, hl=0)
    lip = jaw & ~sh(jaw, 0, 3)
    top = PG([J(46, 26), J(30, 28.5), J(8, 27.5), J(3, 29), J(8, 31.5), J(30, 32.5), J(46, 33)]) & jaw
    p.form(top, G, sd=1, hl=1)
    for x in (12, 18, 24, 30, 36):
        a, b = J(x, 32), J(x + 1.5, 38)
        p.line([a, b], 'c0', only=jaw & ~top)
    c.stamp(p, 'K')
    # lower teeth (stand up from the jaw line)
    p = C()
    for x, g in ((7, FANG_L), (13, FANG_S), (19, FANG_S)):
        q_ = J(x, 28)
        hgt = len(g.strip().split('\n'))
        p.grid(int(round(q_[0])), int(round(q_[1])) - hgt, g[::-1] if False else '\n'.join(g.strip().split('\n')[::-1]) if g is FANG_S else g, LEG)
    c.stamp(p, 'K')

    # ---- upper skull
    p = C()
    skull = PG([P(1, 24), P(2, 20), P(7, 17), P(15, 15), P(22, 10), P(32, 7), P(44, 8), P(54, 13), P(58, 20),
                P(56, 30), P(46, 33), P(40, 30), P(30, 28), P(14, 27), P(4, 27)])
    p.form(skull, G, sd=4, hl=1)
    # cheek / jaw muscle bulge behind the eye
    cheek = E(*P(43, 23), 10.4, 8.4) & skull
    p.form(cheek, G, sd=3, hl=1)
    # snout top plane light + nostril
    p.fill(PG([P(4, 20), P(9, 17), P(16, 16), P(15, 18), P(8, 20)]) & skull, 'g2')
    p.fill(R(*P(5, 21), *P(6, 22)), 'K')
    p.pxs([P(7, 20)], 'g3')
    # upper lip plates
    lipm = skull & (px.Y >= oy + 24) & (px.X < ox + 36) & ~sh(skull, 0, -4)
    p.fill(lipm & ~sh(skull, 0, -2), 'g0')
    for x in (10, 16, 22, 28, 34):
        p.line([P(x, 23), P(x, 28)], 'g0', only=skull & (px.Y >= oy + 23))
    # scales
    scales(p, skull, 'g0', ('g1',), 5, 4, light='g1', lon=('g2',), x0=ox % 5 + 1, y0=oy % 4)
    # brow ridge: heavy dark plate over the eye
    brow = PG([P(12, 17), P(21, 11), P(32, 9), P(34, 12), P(24, 15), P(15, 20)])
    p.form(brow & skull, ('g0', 'g2', 'g3'), sd=1, hl=1)
    p.fill(R(*P(23, 11), *P(27, 11)), 'g3', only=skull)
    c.stamp(p, 'K')
    # eye
    p = C()
    p.grid(ox + 14, oy + 14, EYE, LEG)
    c.stamp(p, ring=False)
    # upper fangs
    p = C()
    p.grid(ox + 8, oy + 27, FANG_U, LEG)
    p.grid(ox + 16, oy + 28, FANG_S, LEG)
    p.grid(ox + 22, oy + 28, FANG_S, LEG)
    p.grid(ox + 28, oy + 28, FANG_S, LEG)
    c.stamp(p, 'K')

    # ---- scale crest: back-swept plates along the skull top
    cr = S['crest']
    for (x, y, ln, w, ang) in [(52, 14, 13, 7, 318), (45, 10, 15, 8, 306), (37, 8, 13, 7, 296), (29, 9, 9, 5, 288)]:
        p = C()
        m = tri(P(x, y + 1), ang - cr, ln + cr * 0.4, w)
        p.form(m, ('g0', 'g1', 'g3'), sd=2, hl=1)
        tip = pol(P(x, y + 1), ang - cr, ln + cr * 0.4 - 2)
        p.fill(E(tip[0], tip[1], 1.6, 1.6) & m, 'c2')
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(dy=0, jaw=13, tongue=0), dict(dy=-1, jaw=16, tongue=5, crest=3), dict(dy=0, jaw=13, tongue=9), dict(dy=1, jaw=10, tongue=0, crest=-2)]
ATTACK = [dict(dx=10, dy=-3, jaw=34, crest=10), dict(dx=-22, dy=3, jaw=4, crest=-6), dict(dx=-6, dy=1, jaw=18, tongue=6)]

if __name__ == '__main__':
    export(NAME, head, WALK, ATTACK)
