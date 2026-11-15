"""Gashadokuro: giant skeleton of the starved, rising out of a bone mound (boss, ~128 px)."""
from bl import *

NAME = 'boss_gashadokuro'
CW, CH = 256, 200
OX, OY = 50, 40          # local baseline y=150
BN = ('b0', 'b1', 'b2')
BF = ('s0', 'b0', 'b1')
px.add_rim('s0', 'b1')

SLEG = dict(zip('bcKde', ['b0', 'b1', 'K', 'b2', 'e1']))
MINI = """
.cddc..
cdddcb.
dKdKcb.
ddKdcb.
.dddb..
.KcKc..
"""


def P(x, y):
    return (x + OX, y + OY)


def bone(p, a, b, r, ramp, knob=1.5, sd=2):
    m = L(*a, r, *b, r * 0.85) | E(a[0], a[1], r * knob, r * knob) | E(b[0], b[1], r * knob * 0.9, r * knob * 0.9)
    p.form(m, ramp, sd=sd, hl=1)
    return m


def bone_hand(c, wr, ang, curl, ramp, spread=20, ln=(9, 7, 6), thumb=True):
    p = C()
    palm = pol(wr, ang, 6)
    p.form(L(*wr, 3.6, *palm, 5.0), ramp, sd=2, hl=1)
    for (qx, qy) in (pol(wr, ang + 60, 2), pol(wr, ang - 70, 2)):
        p.pxs([(int(qx), int(qy)), (int(qx) + 1, int(qy))], ramp[0])
    c.stamp(p, 'K')
    das = [-spread * 1.5, -spread * 0.5, spread * 0.5, spread * 1.5]
    for i, da in enumerate(das):
        p = C()
        pt = pol(palm, ang + da * 2.2, 4); a = ang + da
        for j, l_ in enumerate(ln):
            nx = pol(pt, a, l_ * (0.85 if i in (0, 3) else 1))
            r = 2.1 - j * 0.35
            p.form(L(*pt, r, *nx, r - 0.3) | E(pt[0], pt[1], r + 0.5, r + 0.5), ramp, sd=1, hl=1)
            pt = nx; a -= curl
        tip = pol(pt, a + curl, 2.5)
        p.fill(L(*pt, 1.0, *tip, 0.4), ramp[2])
        c.stamp(p, 'K')
    if thumb:
        p = C()
        pt = pol(wr, ang + 75, 4); a = ang + 55
        for j, l_ in enumerate((6, 5)):
            nx = pol(pt, a, l_)
            p.form(L(*pt, 2.0, *nx, 1.5) | E(pt[0], pt[1], 2.4, 2.4), ramp, sd=1, hl=1)
            pt = nx; a -= curl
        c.stamp(p, 'K')


def skull(c, o, jaw=0, glow=0):
    ox, oy = o

    def h(x, y):
        return (ox + x, oy + y)
    # jaw (behind the upper skull)
    j = jaw
    p = C()
    p.fill(PG([h(8, 50), h(28, 50), h(30, 57 + j), h(8, 56 + j)]), 'q')        # mouth dark
    c.stamp(p, 'K')
    p = C()
    jw = PG([h(8, 56 + j), h(26, 58 + j), h(40, 44), h(47, 46), h(44, 58 + j), h(32, 68 + j), h(12, 70 + j), h(6, 64 + j)])
    p.form(jw, BN, sd=4, hl=1)
    for x in range(9, 27, 4):
        p.fill(R(*h(x, 54 + j), *h(x + 2, 58 + j)), 'b2'); p.fill(R(*h(x, 54 + j), *h(x + 1, 55 + j)), 'b3')
        p.fill(R(*h(x + 3, 54 + j), *h(x + 3, 58 + j)), 'K')
    p.line([h(14, 63 + j), h(24, 64 + j)], 'b0', only=jw)
    c.stamp(p, 'K')
    # cranium + face
    p = C()
    cran = E(*h(30, 24), 26.4, 23.4)
    face = PG([h(4, 26), h(30, 30), h(38, 46), h(30, 50), h(6, 50), h(2, 40)])
    m = cran | face
    p.form(m, BN, sd=7, hl=2)
    p.form(L(*h(22, 42), 3.4, *h(42, 38), 3.0), BN, sd=1, hl=1, only=m)           # cheek bone
    p.form(E(*h(14, 20), 12, 4.6), BN, sd=2, hl=1, only=m)                        # brow ridge
    # cracks, sutures, temple hollow
    p.line([h(26, 3), h(30, 10), h(27, 15), h(32, 20)], 'b0', only=m)
    p.line([h(30, 10), h(36, 12)], 'b0', only=m)
    p.line([h(44, 8), h(46, 18), h(42, 26), h(46, 34)], 'b0', only=m)
    p.form(E(*h(40, 30), 6, 7), ('b0', 'b0', 'b1'), sd=2, hl=0, only=m)
    p.fill(R(*h(14, 6), *h(20, 6)), 'b3', only=m); p.fill(R(*h(10, 9), *h(12, 9)), 'b3', only=m)
    # sockets (angry slant), nose
    near = PG([h(11, 24), h(27, 29), h(29, 37), h(21, 42), h(11, 37)])
    far = PG([h(3, 27), h(7, 25), h(8, 36), h(4, 38)])
    p.fill(near | far, 'K')
    p.fill(PG([h(7, 40), h(10, 38), h(12, 47), h(6, 47)]), 'K')
    p.line([h(9, 41), h(9, 46)], 'q')
    # glow in the sockets
    g = glow
    p.fill(E(*h(19, 33), 3.6 + g, 3.2 + g) & near, 'e0'); p.fill(E(*h(19, 33), 2.2 + g, 1.8 + g), 'e1')
    p.pxs([h(18, 32), h(19, 32), h(18, 33)], 'y3')
    p.pxs([h(5, 31), h(5, 32), h(6, 32)], 'e1'); p.px(*h(5, 31), 'y3')
    # upper teeth
    for x in range(7, 29, 4):
        p.fill(R(*h(x, 49), *h(x + 2, 53)), 'b2'); p.fill(R(*h(x, 49), *h(x + 1, 50)), 'b3')
        p.fill(R(*h(x + 3, 49), *h(x + 3, 52)), 'K')
    p.fill(PG([h(27, 49), h(30, 49), h(28, 56)]), 'b2')                             # one long fang
    c.stamp(p, 'K')


DEF = dict(
    bob=0, lean=0, jaw=1, glow=0, flame=0,
    fsh=(100, 82), felb=(66, 102), fwr=(36, 92), fang=165, fcurl=24,
    nsh=(128, 84), nelb=(116, 122), nwr=(84, 136), nang=172, ncurl=8,
    dust=False,
)


def gasha(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        k = max(0.0, min(1.2, (150 - pt[1]) / 100.0))
        return P(pt[0] + lean * k, pt[1] + bob * k)

    def arm(sh_, el, wr, ang, curl, ramp, near):
        p = C()
        bone(p, sh_, el, 4.4 if near else 3.8, ramp, knob=1.5)
        c.stamp(p, 'K')
        d = (wr[0] - el[0], wr[1] - el[1]); n_ = math.hypot(*d); nx, ny = -d[1] / n_ * 2.6, d[0] / n_ * 2.6
        for s_ in (1, -1):
            p = C()
            bone(p, (el[0] + nx * s_, el[1] + ny * s_), (wr[0] + nx * s_ * 0.6, wr[1] + ny * s_ * 0.6), 2.3, ramp, knob=1.3, sd=1)
            c.stamp(p, 'K')
        bone_hand(c, wr, ang, curl, ramp)

    # ---- far arm
    arm(B(S['fsh']), B(S['felb']), B(S['fwr']), S['fang'], S['fcurl'], BF, False)

    # spine points (quadratic bezier neck -> mound)
    def spine(t):
        a, b_, d = (92, 76), (116, 96), (128, 150)
        x = (1 - t) ** 2 * a[0] + 2 * t * (1 - t) * b_[0] + t * t * d[0]
        y = (1 - t) ** 2 * a[1] + 2 * t * (1 - t) * b_[1] + t * t * d[1]
        return B((x, y))

    def rib(sp, i, ramp, far):
        k = 1.0 - abs(i - 2) * 0.09
        off = (7, -4) if far else (0, 0)
        pts = [(0, 0), (-13 * k, -5), (-25 * k, 2), (-31 * k, 11), (-28 * k, 19)]
        pts = [(sp[0] + x + off[0], sp[1] + y + off[1]) for x, y in pts]
        m = np.zeros((px.H, px.W), bool)
        for a_, b_, r0_, r1_ in zip(pts[:-1], pts[1:], (2.6, 2.5, 2.2, 1.9), (2.5, 2.2, 1.9, 1.4)):
            m |= L(*a_, r0_, *b_, r1_)
        p = C()
        p.form(m, ramp, sd=1, hl=1)
        c.stamp(p, 'K')
        return pts[-1]

    ts = [0.12, 0.25, 0.38, 0.5, 0.61, 0.71]
    for i, t in enumerate(ts):
        rib(spine(t), i, BF, True)
    # ghost fire inside the ribcage
    p = C()
    fx, fy = B((100, 106)); fl = S['flame']
    fire = E(fx, fy, 8.4, 9.4) | tri((fx - 2, fy - 6), 265 + fl * 8, 13 + fl, 9) | tri((fx + 4, fy - 5), 290 - fl * 6, 9, 6)
    p.form(fire, ('a0', 'a1', 'a2'), sd=3, hl=0)
    p.fill(E(fx - 1, fy + 1, 4.4, 5.0), 'a2'); p.fill(E(fx - 1, fy + 2, 2.0, 2.6), 'v3')
    c.stamp(p, 'a0')
    # spine
    p = C()
    for k in range(15):
        t = k / 14
        sx, sy = spine(t)
        p.form(E(sx, sy, 4.6, 3.4), BN, sd=1, hl=1)
        p.form(tri((sx + 3, sy), 20, 6, 4), BN, sd=1, hl=0)
        c.stamp(p, 'K'); p = C()
    # near ribs + sternum
    ends = [rib(spine(t), i, BN, False) for i, t in enumerate(ts)]
    p = C()
    st0, st1 = B((84, 86)), B((89, 122))
    p.form(L(*st0, 3.6, *st1, 2.4), BN, sd=2, hl=1)
    c.stamp(p, 'K')
    # collar bones + shoulder blade
    nsh = B(S['nsh'])
    p = C()
    p.form(PG([(nsh[0] - 6, nsh[1] - 6), (nsh[0] + 10, nsh[1] - 2), (nsh[0] + 8, nsh[1] + 18), (nsh[0] - 2, nsh[1] + 8)]), BN, sd=3, hl=1)
    c.stamp(p, 'K')
    p = C()
    bone(p, st0, (nsh[0] - 2, nsh[1] - 3), 2.4, BN, knob=1.3, sd=1)
    c.stamp(p, 'K')

    # ---- bone mound with little skulls of the starved
    p = C()
    mound = (E(*P(130, 156), 44, 27) | E(*P(104, 154), 24, 15) | E(*P(158, 154), 24, 17)) & (px.Y <= P(0, 150)[1])
    p.form(mound, BF, sd=5, hl=1)
    for (x, y, r) in ((118, 146, 5), (144, 148, 4), (158, 137, 4), (128, 139, 4)):
        p.form(E(*P(x, y), r, r - 1) & mound, BF, sd=1, hl=1)
    for (x, y, a_, l_) in ((100, 146, 200, 12), (146, 134, 330, 12), (164, 144, 10, 12), (112, 137, 230, 9), (136, 146, 10, 10)):
        q0 = P(x, y); q1 = pol(q0, a_, l_)
        bone(p, q0, q1, 1.7, BN, knob=1.5, sd=1)
    for (x, y) in ((104, 141), (122, 136), (150, 140), (136, 131), (166, 143)):
        p.grid(*P(x, y), MINI, SLEG)
    c.stamp(p, 'K')

    # ---- skull
    so = B((40, 24))
    skull(c, (int(round(so[0])), int(round(so[1]))), S['jaw'], S['glow'])

    # ---- near arm
    arm(nsh, B(S['nelb']), B(S['nwr']), S['nang'], S['ncurl'], BN, True)

    if S['dust']:
        p = C()
        for (x, y, a_, l_, w) in ((26, 149, 235, 16, 7), (40, 149, 265, 12, 6), (14, 149, 205, 13, 6), (62, 149, 300, 13, 6), (84, 149, 325, 10, 5)):
            p.form(tri(P(x, y), a_, l_, w), ('b0', 'b1', 'b2'), sd=1, hl=1)
        for (x, y) in ((20, 128), (48, 126), (70, 132), (8, 136)):
            p.fill(R(*P(x, y), *P(x + 1, y + 1)), 'b2')
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [
    dict(jaw=1, flame=0),
    dict(jaw=3, bob=1, lean=-1, flame=1, fwr=(35, 94), fcurl=28, glow=0.4),
    dict(jaw=5, bob=2, lean=-2, flame=0, fwr=(34, 96), fcurl=32, glow=0.8),
    dict(jaw=2, bob=1, lean=-1, flame=-1, fwr=(35, 94), fcurl=28, glow=0.4),
]
ATTACK = [
    dict(jaw=6, lean=6, bob=-2, glow=1, nsh=(130, 78), nelb=(150, 46), nwr=(132, 14), nang=250, ncurl=4, fwr=(40, 96), flame=1),
    dict(jaw=3, lean=-9, bob=5, glow=1, nsh=(126, 88), nelb=(96, 116), nwr=(50, 142), nang=180, ncurl=1, fwr=(30, 84), fcurl=30,
         dust=True),
    dict(jaw=2, lean=-4, bob=3, nelb=(108, 120), nwr=(70, 138), nang=176, ncurl=5, flame=-1),
]

if __name__ == '__main__':
    export(NAME, gasha, WALK, ATTACK)
