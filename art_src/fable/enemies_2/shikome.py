"""Shikome - hag of Yomi: wild white hair, purple corpse-skin, red eyes, tattered dark robe, long claws."""
from common import *

NAME = 'shikome'
CW, CH = 132, 92
OX, OY = 44, 22           # local baseline y = 64
SK = ('p1', 'p2', 'p3')
FAR = ('p0', 'p1', 'p2')
ROBE = ('n0', 'n1', 'n2')
HAIR = ('v1', 'v2', 'v3')

LEG = dict(zip('abcdKEZqwv', ['p0', 'p1', 'p2', 'p3', 'K', 'e1', 'y3', 'q', 'b3', 'v2']))
HEAD = """
......bccccccb....
....bccccccccccb..
...cddcccccccccbb.
..cddcccccccccccb.
..cdccccccccccccbb
.KKKKccccKKKKKccbb
.aaaKKKcKKKaaaacbb
.aEZaaKcKaaZEEacbb
.caaaaccbaaaaaccbb
cdccccdcbbccccbbba
ddcccdcbbbbccbbbba
dccabbabbbbbbbbba.
.caKKKKKKKKbbbbba.
.cKwqwqwqwKabbba..
..KwqqqqqqKabbb...
..aKqqwqqwKabba...
...aKKKKKKabba....
...aabbbbbbaa.....
.....aaaaaa.......
"""

HAND = """
.cc.
cdcc
ccca
.ca.
"""

DEF = dict(bob=0, lean=0, flare=0.0,
           fsh=(33, 30), felb=(23, 33), fwr=(13, 28), fang=18,
           nsh=(40, 31), nelb=(30, 40), nwr=(19, 38), nang=-4,
           ffoot=(30, 63), nfoot=(42, 63), hem=0)


def P(x, y):
    return (x + OX, y + OY)


def claws(c, wr, deg, ramp, spread=30, n=3):
    """bony hand with long talons; deg 0 = left, 90 = up"""
    p = C()
    for i in range(n):
        a = deg + (i - (n - 1) / 2) * spread
        k = pol(wr, 4.0, a); t = pol(wr, 12.0, a + (5 if i == 0 else -5 if i == n - 1 else 0))
        p.fill(L(wr[0], wr[1], 1.2, k[0], k[1], 1.0), ramp[1])
        p.fill(L(k[0], k[1], 1.0, t[0], t[1], 0.5), 'b2')
        p.fill(LN([lerp(k, t, 0.6), t]), 'b3')
    p.fill(E(wr[0], wr[1], 2.6, 2.6), ramp[1])
    p.fill(E(wr[0] - 0.6, wr[1] - 0.6, 1.4, 1.4), ramp[2])
    c.stamp(p, 'K')


def arm(c, s_, e_, w_, deg, ramp):
    claws(c, w_, deg, ramp)
    p = C()
    p.form(L(*e_, 2.1, *w_, 1.7), ramp, sd=1, hl=1)
    c.stamp(p, 'p0')
    p = C()
    p.form(L(*s_, 2.6, *e_, 2.0), ramp, sd=1, hl=1)
    p.form(E(*e_, 2.3, 2.3), ramp, sd=1, hl=1)
    c.stamp(p, 'p0')
    # torn sleeve stub over the shoulder
    p = C()
    m = lerp(s_, e_, 0.55)
    sl = L(*s_, 4.2, *m, 3.6) | PG([(m[0] - 3, m[1] - 2), (m[0] + 1, m[1] + 6), (m[0] + 4, m[1] + 1)])
    p.form(sl, ROBE if ramp is SK else ('n0', 'n0', 'n1'), sd=2, hl=1)
    c.stamp(p, 'K')


def shikome(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, fl = S['bob'], S['lean'], S['flare']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    HC = B((36, 18))          # hair root = back of the skull

    def hair(specs, r0, ramp, ln='v0'):
        """one cel-shaded mass built from tapering locks; lock centre-lines become the strand shadows"""
        p = C()
        mass = np.zeros((px.H, px.W), bool)
        lines = []
        for a, ln_, bend in specs:
            a2 = a - fl * (a - 135) * 0.45 - fl * 28          # flare lifts and fans the mane
            l2 = ln_ * (1 + fl * 0.35)
            pts = [pol(HC, 2, a2), pol(HC, l2 * 0.5, a2 + bend), pol(HC, l2 * 0.82, a2 + bend * 0.3), pol(HC, l2, a2 - bend * 0.8)]
            mass |= wisp(pts, r0, 1.0)
            lines.append(pts)
        p.form(mass, ramp, sd=3, hl=1)
        inner = erode(mass, 1)
        for pts in lines:
            p.line([(x + 1, y + 1) for x, y in pts[1:]], ramp[0], only=inner)
        c.stamp(p, ln)

    # ---- back mane (behind the body)
    hair([(252, 30, 8), (236, 35, -6), (220, 31, 8), (203, 29, -7), (186, 24, 8), (166, 19, -8), (142, 14, 8)], 5.0, HAIR)

    # ---- far arm
    arm(c, B(S['fsh']), B(S['felb']), B(S['fwr']), S['fang'], FAR)

    # ---- feet: bare, clawed
    for (fx, fy), ramp in ((S['ffoot'], FAR), (S['nfoot'], SK)):
        p = C()
        f = P(fx, fy)
        p.form(L(f[0] + 2, f[1] - 8, 2.0, f[0] + 1, f[1] - 2, 1.8), ramp, sd=1, hl=0)
        p.form(PG([(f[0] + 3, f[1] - 3), (f[0] + 3, f[1]), (f[0] - 5, f[1]), (f[0] - 3, f[1] - 2)]), ramp, sd=1, hl=1)
        p.pxs([(f[0] - 6, f[1]), (f[0] - 4, f[1]), (f[0] - 2, f[1])], 'b2')
        c.stamp(p, 'p0')

    # ---- robe: hunched back, ragged hem
    p = C()
    h = S['hem']
    back = L(*B((39, 31)), 7.6, *P(43 + lean * 0.4, 46), 8.4)
    pts = [P(34 + lean * 0.4, 44), P(52 + lean * 0.4, 42), P(58 + h, 58), P(54 + h, 55), P(52, 61), P(48, 56), P(45, 62), P(41, 57), P(37, 61),
           P(34, 56), P(30 - h, 60), P(29 - h, 54)]
    skirt = PG(pts)
    robe = back | skirt
    p.form(robe, ROBE, sd=5, hl=1)
    for a_, b_ in (((38, 46), (33, 57)), ((44, 46), (43, 58)), ((50, 45), (54, 55))):          # fold lines
        p.line([P(a_[0] + lean * 0.4, a_[1]), P(*b_)], 'n0', only=robe)
    p.line([B((33, 31)), B((38, 38)), P(39 + lean * 0.4, 44)], 'n3', only=robe)                  # lapel edge catches light
    rope = robe & (px.Y >= P(0, 44)[1]) & (px.Y <= P(0, 45)[1]) & skirt
    p.fill(rope, 'c0')                                                                           # straw rope belt
    # exposed chest: ribs of the dead
    chest = PG([B((31, 29)), B((36, 29)), B((38, 38)), P(37 + lean * 0.4, 43), B((32, 38))]) & robe
    p.form(chest, SK, sd=1, hl=0)
    for i in range(3):
        p.line([B((32, 33 + i * 3)), B((36, 34 + i * 3))], 'p0', only=chest)
    c.stamp(p, 'K')

    # ---- head: scrawny neck, face grid (identical every frame)
    p = C()
    p.form(L(*B((35, 28)), 2.4, *B((32, 22)), 2.2), FAR, sd=1, hl=0)
    c.stamp(p, 'p0')
    p = C()
    hx, hy = B((19, 8))
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'K')
    # ---- front hair: crown tufts and strands falling over the brow
    hair([(118, 11, 10), (96, 9, -8)], 2.8, HAIR)
    p = C()
    crown = E(hx + 11, hy + 1, 7.4, 3.2) | E(hx + 15, hy + 5, 3.4, 5.4)
    p.form(crown, HAIR, sd=1, hl=1)
    for sx in (5, 8):
        p.fill(R(hx + sx, hy + 2, hx + sx, hy + 5), 'v2')                       # lank strands over the forehead
    c.stamp(p, 'v0')

    # ---- near arm
    arm(c, B(S['nsh']), B(S['nelb']), B(S['nwr']), S['nang'], SK)

    c.blacken()
    return c


WALK = [
    dict(bob=0, ffoot=(26, 63), nfoot=(46, 63), nelb=(31, 40), nwr=(21, 40), felb=(23, 32), fwr=(12, 26), hem=1),
    dict(bob=-1, ffoot=(32, 63), nfoot=(42, 62), flare=0.08),
    dict(bob=0, ffoot=(38, 63), nfoot=(34, 63), nelb=(29, 40), nwr=(18, 36), felb=(24, 34), fwr=(14, 31), hem=-1),
    dict(bob=-1, ffoot=(33, 62), nfoot=(40, 63), flare=0.08),
]
ATTACK = [
    dict(lean=4, bob=-1, flare=-0.15, fsh=(34, 29), felb=(31, 20), fwr=(24, 12), fang=62,
         nsh=(41, 30), nelb=(46, 22), nwr=(40, 12), nang=72, ffoot=(32, 63), nfoot=(45, 63)),
    dict(lean=-8, bob=2, flare=1.0, fsh=(33, 30), felb=(20, 29), fwr=(8, 26), fang=4,
         nsh=(40, 31), nelb=(26, 35), nwr=(13, 34), nang=-6, ffoot=(22, 63), nfoot=(44, 63), hem=2),
    dict(lean=-4, bob=1, flare=0.4, felb=(21, 35), fwr=(12, 34), fang=-12, nelb=(29, 42), nwr=(18, 43), nang=-20,
         ffoot=(26, 63), nfoot=(43, 63), hem=1),
]

if __name__ == '__main__':
    export(NAME, shikome, WALK, ATTACK)
    zoom(NAME, 6)
