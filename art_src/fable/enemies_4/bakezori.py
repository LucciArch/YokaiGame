"""Bake-zori: haunted straw sandal, one big eye, thin arms and legs. Small (~38 px)."""
from common import *

NAME = 'bakezori'
CW, CH = 76, 60
BASE = 49
STRAW = ('o1', 'o2', 'o3')
LIMB = ('s1', 's2', 's3')
LIMBF = ('s0', 's1', 's2')

LEG = dict(zip('KWwYyOZqrRTtb', ['K', 'b3', 'b2', 'y2', 'y1', 'y0', 'y3', 'q', 'm2', 'm3', 'b3', 'b1', 'b0']))
EYE = """
..KKKKKK...
.KwWWWWwKK.
KwWYYYWWWwK
KWYyKKYWWWK
KWYKKKYWWbK
KbWYZKYWwbK
.KbwYYwwbK.
..KKbbbKK..
"""
MOUTH = """
K.........K
KKqTqqTqTKK
.KqqqqqqqK.
..KTqrrTK..
...KKrRK...
.....rRr...
.....rR....
"""


def hand(c, w, ang, ramp):
    p = C()
    p.fill(E(w[0], w[1], 1.7, 1.7), ramp[1])
    for da in (-40, 0, 40):
        t = pol(w, ang + da, 3.2)
        p.fill(LN([w, t]), ramp[2] if da <= 0 else ramp[1])
    c.stamp(p, 's0')


def leg(c, hip, knee, foot, ramp):
    seg(c, hip, 1.8, knee, 1.7, ramp, sd=1, hl=0, ln='s0')
    p = C()
    p.form(L(knee[0], knee[1], 1.7, foot[0], foot[1] - 1.5, 1.7), ramp, sd=1, hl=0)
    f = PG([(foot[0] + 2, foot[1] - 2), (foot[0] + 2, foot[1]), (foot[0] - 5, foot[1]), (foot[0] - 5, foot[1] - 1), (foot[0] - 1, foot[1] - 3)])
    p.form(f, ramp, sd=1, hl=1)
    c.stamp(p, 's0')


DEF = dict(dx=0, bob=0, tilt=0,
           fhip=(-3, 13), fknee=(-6, 16), ffoot=(-5, 0),
           nhip=(4, 13), nknee=(6, 16), nfoot=(7, 0),
           fsh=(-6, 4), felb=(-12, 8), fwr=(-15, 4), fang=200,
           nsh=(8, 5), nelb=(13, 10), nwr=(15, 15), nang=100)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx, cy = 42 + S['dx'], 27 + S['bob']
    tl = S['tilt']

    def B(pt):
        return (cx + pt[0], cy + pt[1])

    def F(pt):  # foot: x relative to body, y relative to baseline
        return (cx + pt[0], BASE + pt[1])

    # far limbs
    seg(c, B(S['fsh']), 1.8, B(S['felb']), 1.7, LIMBF, sd=1, hl=0, ln='s0')
    seg(c, B(S['felb']), 1.7, B(S['fwr']), 1.7, LIMBF, sd=1, hl=0, ln='s0')
    hand(c, B(S['fwr']), S['fang'], LIMBF)
    leg(c, B(S['fhip']), B(S['fknee']), F(S['ffoot']), LIMBF)
    leg(c, B(S['nhip']), B(S['nknee']), F(S['nfoot']), LIMB)

    # sandal sole (upright, toe up), frayed straw ends
    p = C()
    top = (cx - 1 - tl, cy - 7); bot = (cx + 1, cy + 6)
    body = L(top[0], top[1], 8.4, bot[0], bot[1], 9.4)
    fray = np.zeros_like(body)
    for (ox, oy, ex, ey) in [(-7, 12, -10, 16), (5, 14, 8, 17), (9, 9, 12, 12),
                             (4, -15, 6, -18), (-9, 2, -12, 3)]:
        t_ = tl if oy < 0 else 0
        fray |= L(cx + ox - t_, cy + oy, 1.3, cx + ex - t_, cy + ey, 0.5)
    p.form(body | fray, ('s1', 'o0', 'o1'), sd=2, hl=0)
    p.form(body, STRAW, sd=3, hl=1)
    # woven rows + rope border
    for yy in range(-14, 16, 3):
        darken(p, body & (px.Y == cy + yy))
    inner = erode(body, 2)
    darken(p, body & ~inner & ~sh(inner, 1, 1))
    c.stamp(p, 'K')

    # red thong strap: a /\ above the eye, reads as an angry brow
    p = C()
    ap = (cx - 1 - tl, cy - 13)
    lft = (cx - 9, cy - 2); rgt = (cx + 9, cy - 1)
    strap = L(ap[0], ap[1], 1.0, lft[0], lft[1], 0.8) | L(ap[0], ap[1], 1.0, rgt[0], rgt[1], 0.8)
    p.form(strap & body, ('m1', 'm2', 'm3'), sd=1, hl=0)
    p.fill(E(ap[0], ap[1] + 1, 1.5, 1.5), 'm3')
    c.stamp(p, 'm0')

    p = C()
    p.grid(cx - 6 - tl // 2, cy - 5, EYE, LEG)
    p.grid(cx - 6, cy + 5, MOUTH, LEG)
    c.stamp(p, ring=False)

    # near arm
    seg(c, B(S['nsh']), 1.8, B(S['nelb']), 1.7, LIMB, sd=1, hl=0, ln='s0')
    seg(c, B(S['nelb']), 1.7, B(S['nwr']), 1.7, LIMB, sd=1, hl=0, ln='s0')
    hand(c, B(S['nwr']), S['nang'], LIMB)
    c.blacken()
    return c


WALK = [
    dict(bob=1, ffoot=(-9, 0), fknee=(-7, 18), nfoot=(9, 0), nknee=(7, 18), fwr=(-13, 12), felb=(-11, 9), fang=150, nwr=(14, 9), nelb=(13, 10), nang=30),
    dict(bob=0, ffoot=(-1, 0), fknee=(-3, 18), nfoot=(2, -3), nknee=(2, 17)),
    dict(bob=1, ffoot=(5, 0), fknee=(1, 18), nfoot=(-6, 0), nknee=(-2, 18), fwr=(-15, 3), fang=210, nwr=(12, 16), nang=110),
    dict(bob=0, ffoot=(-3, -3), fknee=(-5, 16), nfoot=(4, 0), nknee=(5, 18)),
]
ATTACK = [
    dict(dx=4, bob=4, tilt=-2, fknee=(-8, 15), ffoot=(-5, 0), nknee=(9, 15), nfoot=(7, 0), fwr=(-10, 13), felb=(-12, 8), fang=120, nwr=(16, 1), nelb=(14, 8), nang=300),
    dict(dx=-8, bob=-7, tilt=2, fhip=(-4, 12), fknee=(-12, 13), ffoot=(-22, -13), nknee=(8, 18), nfoot=(13, -4), fwr=(-10, -4), felb=(-11, 3), fang=250, nwr=(17, 4), nelb=(13, 8), nang=20),
    dict(dx=-5, bob=2, fknee=(-8, 17), ffoot=(-8, 0), nknee=(6, 17), nfoot=(6, 0), fwr=(-14, 9), fang=170),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
