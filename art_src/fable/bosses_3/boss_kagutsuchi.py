"""Kagutsuchi - the fire god: a divine child wreathed in roaring flame."""
from lib3 import *

NAME = 'boss_kagutsuchi'
CW, CH = 240, 150
OX, OY = 110, 14            # local baseline y=130
col('f0', '#7a1220'); col('f1', '#d83a1c'); col('f2', '#ff8a24'); col('f3', '#ffd23c'); col('f4', '#fff4b0')   # living fire
col('u0', '#1c0c1c'); col('u1', '#3a1420'); col('u2', '#6a2420')                                                # charred skin
px.add_rim('f0', 'f2'); px.add_rim('f1', 'f3'); px.add_rim('f2', 'f4'); px.add_rim('u0 u1 u2', 'f2')
BODY = ('f2', 'f3', 'f4')
CHAR = ('u0', 'u1', 'u2')

LEG = dict(zip('KabcdDeEZq', ['K', 'u0', 'u1', 'u2', 'f2', 'f3', 'f1', 'f4', 'v3', 'q']))
# round child's face of cooling magma: ember cracks, white-hot eyes, a too-wide furnace grin
FACE = """
.......bbbbbbbbb.......
.....bbcccccccbbbb.....
...bbcccccDcccccbbbb...
..bcccccccDdcccccbbbb..
..bccdccccdDcccdcbbbb..
.bccKKKccccdcccKKKbbbb.
.bcKKKKKKcccccKKKKKKbba
.bcKEZEEKKcccKKEEZEKbba
bccKEEEEEKcccKEEEEEKbba
bcccKEEEKccdccKEEEKbbba
bcdccKKKccdDdccKKKbbbaa
bccdccccccccccccccbbbaa
bcKKccccccccccccKKbbbaa
.bKEKKKccccccKKKEKbbaa.
.bcKEDEKKKKKKEDEKbbbaa.
..bcKKEDEDEDEDKKbbbaa..
...bccKKKKKKKKbbbbaa...
....bbbccccbbbbbaaa....
......bbbbbbbaaa.......
"""


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, ph=0.0, k=1.0, arms=((34, 76), (26, 70), (82, 76), (90, 68)), burst=0, lean=0)


def flames(c, o, ph, k, layers, tongues, base_r):
    """layered flame aura. tongues: (dx, height, width, bend) relative to o; layers: (scale, colour, shadow colour)"""
    for li, (sc, colr, shc) in enumerate(layers):
        m = E(o[0], o[1], base_r[0] * sc, base_r[1] * sc)
        for i, (dx, h, w, bend) in enumerate(tongues):
            fl = math.sin(ph + i * 2.1 + li * 0.7)
            b = (o[0] + dx * sc, o[1] + base_r[1] * 0.2)
            t = (o[0] + dx * sc * 1.15 + bend * sc + fl * 3 * sc, o[1] - (h * k + fl * 5) * sc)
            m |= tongue(b, t, w * sc, bend * 0.5 + fl * 2, tr=0.6)
        p = C()
        p.fill(m, colr)
        if shc:
            p.fill(m & ~sh(m, -2, -2), shc)
        c.stamp(p, 'f0' if li == 0 else colr, ring=(li == 0))


def kagu(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, ph, k, lean = S['bob'], S['ph'], S['k'], S['lean']

    def U(x, y):
        return P(x + lean, y + bob)

    # ---- attack burst (behind)
    if S['burst']:
        b = S['burst']
        o = U(58, 74)
        for sc, colr in ((1.0, 'f1'), (0.8, 'f2'), (0.58, 'f3'), (0.36, 'f4')):
            m = E(o[0] - 30 * b, o[1], 46 * b * sc, 34 * b * sc)
            for i, a in enumerate((180, 160, 200, 140, 220, 120, 240, 100, 260, 30, 330, 0)):
                ln = (64 if 150 < a < 210 else 46 if 110 < a < 250 else 30) * b
                st = pol((o[0] - 30 * b, o[1]), a, 20 * b * sc)
                m |= tongue(st, pol(st, a, ln * sc), 11 * b * sc, (4 if i % 2 else -4) * sc, tr=0.6)
            m &= R(1, 1, CW - 2, OY + 130)
            p = C(); p.fill(m, colr)
            if sc == 1.0:
                p.fill(m & ~sh(m, -2, -2), 'f0')
            c.stamp(p, 'f0', ring=(sc == 1.0))

    # ---- roaring aura
    o = U(58, 92)
    tg = [(-34, 46, 9, -6), (-24, 72, 11, 5), (-10, 92, 12, -5), (4, 104, 13, 4), (18, 86, 12, 6), (30, 64, 10, -4), (40, 40, 8, 5), (-42, 24, 6, -4)]
    flames(c, o, ph, k, ((1.0, 'f1', 'f0'), (0.8, 'f2', 'f1'), (0.6, 'f3', None)), tg, (40, 34))
    # ground pool of fire
    p = C()
    pool = E(*P(58 + lean * .3, 128), 44 + 2 * math.sin(ph), 4.4)
    p.fill(pool, 'f1'); p.fill(E(*P(56 + lean * .3, 127), 32, 2.4), 'f3')
    c.stamp(p, 'f0')
    # sparks
    for i, (x, y) in enumerate(((16, 30), (96, 22), (30, 8), (84, 46), (104, 60), (8, 58))):
        yy = y - ((ph * 6 + i * 5) % 12)
        q = U(x, yy)
        c.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 'f3'); c.ln[R(q[0] - 1, q[1] - 1, q[0] + 2, q[1] + 2)] = False

    # ---- the child: floating, legs folded, body of dark cooling magma veined with fire
    (fe, fh, ne, nh) = S['arms']
    # far arm
    p = C()
    limb(p, U(48, 68), 3.6, U(*fe), 3.2, CHAR, sd=1, hl=1)
    limb(p, U(*fe), 3.2, U(*fh), 2.8, CHAR, sd=1, hl=1)
    c.stamp(p, 'K')
    palm_fire(c, U(*fh), ph)
    # legs (folded, floating)
    p = C()
    far_leg = L(*U(52, 92), 5.5, *U(42, 100), 4.5) | L(*U(42, 100), 4.5, *U(56, 106), 3.4)
    p.form(far_leg, ('u0', 'u0', 'u1'), sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    torso = L(*U(58, 66), 9.4, *U(59, 88), 10.4)
    p.form(torso, CHAR, sd=4, hl=1)
    belly = E(*U(56, 86), 7.4, 6.4)
    p.form(belly, CHAR, sd=2, hl=1, only=torso)
    # glowing cracks
    for pts in ([(52, 66), (55, 72), (53, 78), (57, 84)], [(62, 64), (60, 70), (64, 76)], [(55, 72), (59, 74)], [(57, 84), (62, 88), (60, 94)], [(50, 84), (53, 78)]):
        p.line([U(*q) for q in pts], 'f2', only=torso)
    p.fill(R(*U(54, 73), *U(55, 74)) | R(*U(57, 84), *U(58, 85)), 'f4', only=torso)
    c.stamp(p, 'K')
    p = C()
    near_leg = L(*U(62, 92), 6.4, *U(74, 99), 5.2) | L(*U(74, 99), 5.2, *U(56, 104), 3.8)
    p.form(near_leg, CHAR, sd=2, hl=1)
    foot = E(*U(52, 105), 4.4, 2.6)
    p.form(foot, CHAR, sd=1, hl=1)
    p.line([U(66, 93), U(72, 97), U(68, 101)], 'f2', only=near_leg)
    c.stamp(p, 'K')
    # shimenawa-like rope belt with paper streamer, burning at the edge
    p = C()
    belt = L(*U(48, 89), 2.2, *U(70, 88), 2.2)
    p.form(belt, ('y0', 'y1', 'y2'), sd=1, hl=1)
    for x in (51, 56, 61, 66):
        p.line([U(x, 87), U(x + 1, 91)], 'y0', only=belt)
    c.stamp(p, 'K')

    # ---- head: flame hair behind, then the face
    HX, HY = U(40, 38)
    oh = (HX + 12, HY + 6)
    hair = [(-10, 20, 5, -4), (-4, 32, 6, 3), (4, 40, 7, -3), (11, 30, 6, 4), (16, 18, 5, 3)]
    flames(c, oh, ph + 1, 1.0, ((1.0, 'f2', 'f1'), (0.7, 'f3', None), (0.42, 'f4', None)), hair, (12, 9))
    p = C()
    p.grid(HX, HY, FACE, LEG)
    c.stamp(p, 'K')
    # two small horn-flames at the temples
    # near arm
    p = C()
    limb(p, U(68, 68), 4.2, U(*ne), 3.6, CHAR, sd=1, hl=1)
    limb(p, U(*ne), 3.6, U(*nh), 3.0, CHAR, sd=1, hl=1)
    p.line([U(70, 70), lerp(U(70, 70), U(*ne), .8)], 'f2', only=p.m)
    c.stamp(p, 'K')
    palm_fire(c, U(*nh), ph + 2)

    c.blacken()
    return c


def palm_fire(c, h, ph):
    p = C()
    p.form(E(h[0], h[1], 3.4, 3.2), CHAR, sd=1, hl=1)
    c.stamp(p, 'K')
    fl = math.sin(ph)
    m = E(h[0], h[1] - 6, 5.4, 4.4) | tongue((h[0], h[1] - 6), (h[0] + fl * 2, h[1] - 19 - fl * 2), 4.6, 2 + fl, tr=0.6) | \
        tongue((h[0] - 3, h[1] - 6), (h[0] - 6, h[1] - 13 + fl), 2.6, -1, tr=0.6)
    p = C(); p.fill(m, 'f2'); c.stamp(p, 'f0')
    c.fill(erode(m, 1) & sh(erode(m, 1), 0, 2), 'f3')
    c.fill(E(h[0], h[1] - 6, 2.4, 2.0), 'f4')


T = math.pi / 2
WALK = [dict(ph=0, bob=0), dict(ph=T, bob=-1), dict(ph=2 * T, bob=-2), dict(ph=3 * T, bob=-1)]
ATTACK = [
    dict(ph=1, bob=-3, k=0.72, lean=3, arms=((40, 60), (46, 50), (78, 60), (70, 50))),
    dict(ph=2.4, bob=1, k=1.15, lean=-4, arms=((34, 72), (22, 72), (56, 78), (38, 80)), burst=1.0),
    dict(ph=4, bob=0, k=0.9, lean=-2, arms=((34, 76), (24, 74), (64, 80), (48, 82)), burst=0.45),
]

if __name__ == '__main__':
    export(NAME, kagu, WALK, ATTACK)
