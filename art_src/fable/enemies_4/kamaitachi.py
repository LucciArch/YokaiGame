"""Kamaitachi: sickle weasel riding a whirlwind, long sickle blades for front claws. Normal (~56 px), floats.
Attack: sickle slash with a wind trail."""
from common import *

NAME = 'kamaitachi'
CW, CH = 128, 92
OX, BASE = 74, 84
FUR = ('t0', 't1', 't2')
FURF = ('s1', 't0', 't1')
BEL = ('c0', 'c1', 'c2')
WIND = ('v0', 'v1', 'v2')
STEEL = ('i1', 'i2', 'i3')

LEG = dict(zip('KmtucCYZWqp', ['K', 't0', 't1', 't2', 'c1', 'c2', 'y2', 'y3', 'b3', 'q', 's0']))
HEAD = """
............KK....
...........KutK...
.......KKKKuttmK..
....KKKuuuttttmK..
..KKuuuKKKKtttttK.
.KuuuumKKYZKttttK.
KpuuummmKYYmtttttK
KKcCCcmmmmmttttttK
.KWqWqCCccttttttmK
..KqqqqcCcctttttK.
..KCWCWCcccttttmK.
...KKKKKccccttmK..
........KKKKKKK...
"""


def sickle(c, wrist, a0, sweep, R=11.0, w0=5.6):
    """curved blade growing from the wrist along an arc (a0 = start direction from arc centre, deg)"""
    ctr = pol(wrist, a0 + 180, R)
    n = 14
    outer = [pol(ctr, a0 + sweep * i / n, R + 1.2) for i in range(n + 1)]
    inner = [pol(ctr, a0 + sweep * i / n, R + 1.2 - (w0 * (1 - i / n) ** 0.8 + 0.3)) for i in range(n + 1)]
    m = PG(outer + inner[::-1])
    p = C()
    p.fill(m, 'i2')
    back = PG(outer + [pol(ctr, a0 + sweep * i / n, R - 0.2) for i in range(n, -1, -1)]) & m
    p.fill(back, 'i1')
    edge = m & ~PG([pol(ctr, a0 + sweep * i / n, R + 3) for i in range(n + 1)] +
                   [pol(ctr, a0 + sweep * i / n, R + 1.2 - (w0 * (1 - i / n) ** 0.8 + 0.3) + 1.1) for i in range(n, -1, -1)])
    p.fill(edge, 'i3')
    c.stamp(p, 'K')
    q = C(); q.form(E(wrist[0], wrist[1], 2.4, 2.4), ('w0', 'w1', 'w2'), sd=1, hl=1); c.stamp(q, 'K')


def arm(c, s, e, w, ramp, a0, sweep, R=11.0):
    sickle(c, w, a0, sweep, R)
    seg(c, e, 2.3, w, 2.0, ramp, ln='s0')
    seg(c, s, 2.9, e, 2.3, ramp, ln='s0')


def whirl(c, cx, ph, layer, lift=0):
    """funnel of wind bands; 'back' halves are drawn before the body, 'front' halves after"""
    bands = [(0, 4.5), (-5, 7.0), (-10, 9.5), (-15, 12.0), (-20, 14.5)]
    for k, (yy, rx) in enumerate(bands):
        off = [0, 3, 1, -3][(k + ph) % 4]
        y = BASE - 2 + yy
        full = E(cx + off, y, rx, 3.1)
        m = full & ((px.Y <= y) if layer == 'back' else (px.Y >= y))
        if layer == 'front' and k == len(bands) - 1:
            m = full
        p = C()
        p.form(m, WIND, sd=1, hl=1)
        # swirl streak
        sx = cx + off - rx * 0.5 + ((k * 5 + ph * 4) % int(rx + 3))
        st = R(sx, y + (0 if layer == 'front' else -1), sx + rx * 0.5, y + (0 if layer == 'front' else -1)) & erode(full, 1) & m
        p.fill(st, 'v3')
        c.stamp(p, 'v0')
    if layer == 'front':
        # loose wisps flung off the funnel
        p = C()
        for k, (ox, oy, ln_) in enumerate([(-19, -12, 6), (17, -7, 5), (-13, -3, 4), (20, -19, 5)]):
            if (k + ph) % 2 == 0:
                x0 = cx + ox + [0, 1, 0, -1][ph % 4]
                p.fill(R(x0, BASE + oy, x0 + ln_, BASE + oy), 'v2')
                p.fill(R(x0 + 1, BASE + oy + 1, x0 + ln_ - 2, BASE + oy + 1), 'v1')
        c.stamp(p, 'v0')


DEF = dict(dx=0, bob=0, ph=0, lean=0,
           nsh=(-6, -41), nel=(-13, -35), nwr=(-20, -40), na0=350, nsw=-165,
           fsh=(-9, -43), fel=(-18, -40), fwr=(-25, -46), fa0=345, fsw=-155,
           tail=[(8, -24), (18, -27), (24, -36), (21, -45)], trail=None)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx = OX + S['dx']
    by = BASE + S['bob']
    ln_ = S['lean']

    def B(pt, k=1.0):
        return (cx + pt[0] + ln_ * k, by + pt[1])

    whirl(c, cx, S['ph'], 'back')
    # tail: bushy, dark tip
    tp = [(cx + q[0], by + q[1]) for q in S['tail']]
    p = C()
    tm = np.zeros((CH, CW), bool)
    rr = [2.4, 3.2, 3.0, 1.5]
    for i in range(3):
        tm |= L(tp[i][0], tp[i][1], rr[i], tp[i + 1][0], tp[i + 1][1], rr[i + 1])
    p.form(tm, FUR, sd=2, hl=1)
    p.fill(tm & E(tp[3][0], tp[3][1], 3.2, 3.2), 't0')
    c.stamp(p, 's0')
    # far arm
    arm(c, B(S['fsh']), B(S['fel']), B(S['fwr']), FURF, S['fa0'], S['fsw'], 10.0)
    # long sinuous body rising out of the funnel
    p = C()
    hip = (cx + 3, by - 17); mid = (cx + 6 + ln_ * 0.4, by - 30); chest = B((-3, -41)); neck = B((-9, -47))
    body = L(*hip, 6.4, *mid, 5.6) | L(*mid, 5.6, *chest, 5.8) | L(*chest, 5.4, *neck, 4.6)
    p.form(body, FUR, sd=4, hl=1)
    belly = body & ~(L(hip[0] + 4, hip[1], 6.4, mid[0] + 4, mid[1], 5.6) | L(mid[0] + 4, mid[1], 5.6, chest[0] + 5, chest[1] + 1, 5.8) |
                     L(chest[0] + 5, chest[1] + 1, 5.4, neck[0] + 5, neck[1] + 2, 4.6))
    p.form(belly & erode(body, 1), BEL, sd=1, hl=0)
    c.stamp(p, 's0')
    # head
    p = C()
    p.grid(int(B((-25, -57))[0]), int(B((-25, -57))[1]), HEAD, LEG)
    c.stamp(p, 'K')
    whirl(c, cx, S['ph'], 'front')
    # slash trail (wind crescent)
    if S['trail']:
        ctr, R0, a0, a1 = S['trail']
        ctr = (cx + ctr[0], by + ctr[1])
        n = 16
        outer = [pol(ctr, a0 + (a1 - a0) * i / n, R0) for i in range(n + 1)]
        inner = [pol(ctr, a0 + (a1 - a0) * i / n, R0 - 4.2 * math.sin(math.pi * i / n) ** 0.7 - 0.4) for i in range(n + 1)]
        m = PG(outer + inner[::-1])
        p = C()
        p.fill(m, 'v1')
        p.fill(m & ~sh(m, 2, 2) & ~sh(m, 2, 0), 'v3')
        p.fill(m & sh(m, 2, 2) & ~sh(m, 1, 1), 'v2')
        c.stamp(p, 'v0')
    # near arm
    arm(c, B(S['nsh']), B(S['nel']), B(S['nwr']), FUR, S['na0'], S['nsw'])
    c.blacken()
    return c


WALK = [
    dict(ph=0, bob=0),
    dict(ph=1, bob=-1, tail=[(8, -24), (18, -28), (25, -36), (23, -45)], nwr=(-20, -41), fwr=(-25, -47)),
    dict(ph=2, bob=-2),
    dict(ph=3, bob=-1, tail=[(8, -24), (18, -26), (23, -35), (19, -44)], nwr=(-20, -39), fwr=(-25, -45)),
]
ATTACK = [
    # both sickles hauled back overhead
    dict(ph=1, dx=5, lean=3, bob=-2, nsh=(-5, -42), nel=(-4, -51), nwr=(3, -58), na0=200, nsw=130,
         fsh=(-9, -44), fel=(-12, -53), fwr=(-8, -61), fa0=195, fsw=120),
    # slash down-left, wind crescent
    dict(ph=2, dx=-8, lean=-5, bob=1, nsh=(-7, -40), nel=(-17, -36), nwr=(-27, -34), na0=300, nsw=-115,
         fsh=(-10, -42), fel=(-20, -43), fwr=(-30, -44), fa0=285, fsw=-105,
         trail=((-22, -40), 29, 150, 262)),
    dict(ph=3, dx=-4, lean=-2, bob=0, nsh=(-6, -40), nel=(-12, -33), nwr=(-20, -29), na0=330, nsw=-110,
         fsh=(-9, -42), fel=(-17, -37), fwr=(-25, -35), fa0=315, fsw=-100),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
