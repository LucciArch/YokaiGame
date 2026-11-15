"""Sazae-oni: horned turban-snail shell with an oni face peeking out of the opening. Normal (~56 px).
Attack: the head shoots out of the shell on a long neck and bites."""
from common import *

NAME = 'sazae_oni'
CW, CH = 120, 84
OX, BASE = 70, 78
SHELL = ('s1', 's2', 's3')
SKIN = ('r1', 'r2', 'r3')
FOOT = ('c0', 'c1', 'c2')

LEG = dict(zip('abcdemnxwvYZKq', ['r0', 'r1', 'r2', 'r3', 'r4', 'h0', 'h1', 'b3', 'b2', 'b1', 'y2', 'y3', 'K', 'q']))
HEAD = """
..x.........x....
..xw.......xw....
.mwvmmmmmmmwvm...
mnmmddddddmmmnm..
mncdeedddddccnnm.
mcddedddddcccbnm.
mKKKKdddKKKKcbnm.
mZYKKKdKKKYZcbbm.
maYYadddaYYacbbm.
.cdddacaddccbbm..
.cKaaaaaaaKcbbm..
.xKqxqqxqqKxbb...
.xwqqqqqqqwwba...
..bxqxqqxqxbba...
...bccccccbba....
....aaaaaaa......
"""


def claw_arm(c, s, e, w, ang, ramp):
    seg(c, e, 2.3, w, 2.0, ramp, ln='r0')
    p = C()
    p.form(E(w[0], w[1], 2.6, 2.4), ramp, sd=1, hl=1)
    c.stamp(p, 'r0')
    for da in (-35, 0, 35):
        q = C(); q.fill(LN([pol(w, ang + da, 2), pol(w, ang + da, 5.2)]), 'b3'); c.stamp(q, 'K')
    seg(c, s, 2.8, e, 2.3, ramp, ln='r0')


DEF = dict(dx=0, bob=0, tilt=0, out=0, drop=0, ripple=0,
           nel=(-18, -9), nwr=(-25, -6), nang=170,
           fel=(-20, -17), fwr=(-28, -19), fang=190)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx = OX + S['dx']
    b = S['bob']
    tl = S['tilt']

    def B(pt, k=0.0):
        """k = how much the point follows the shell tilt (0 base .. 1 apex)"""
        return (cx + pt[0] + tl * k, BASE + pt[1] + b)

    # slug foot
    p = C()
    rp = S['ripple']
    foot = L(cx - 20 - rp, BASE - 3, 2.8, cx - 2, BASE - 4, 4.4) | L(cx - 2, BASE - 4, 4.4, cx + 19 + rp, BASE - 2, 2.2)
    foot &= (px.Y <= BASE)
    p.form(foot, FOOT, sd=2, hl=1)
    for k in range(-16, 18, 5):
        p.px(cx + k + rp, BASE - 1, 'c0'); p.px(cx + k + 1 + rp, BASE - 1, 'c0')
    c.stamp(p, 'K')
    # far arm
    claw_arm(c, B((-10, -16)), B(S['fel']), B(S['fwr']), S['fang'], ('r0', 'r1', 'r2'))
    # shell: four whorls stacked toward the apex (upper right), horns on every shoulder
    whorls = [((6, -19), 17.4, 14.4, 0.15), ((11, -34), 12.4, 9.0, 0.5), ((15, -44), 8.4, 6.0, 0.8), ((18, -51), 4.6, 3.8, 1.0)]
    for i in range(len(whorls) - 1, -1, -1):
        (wx, wy), rx, ry, k = whorls[i]
        o = B((wx, wy), k)
        p = C()
        m = E(o[0], o[1], rx, ry)
        horns = np.zeros_like(m)
        nh = 4 if i < 2 else 2
        for j in range(nh):
            a = 195 + j * (150 / max(1, nh - 1)) if nh > 2 else 230 + j * 80
            bs = (o[0] + math.cos(math.radians(a)) * (rx - 1.5), o[1] + math.sin(math.radians(a)) * (ry - 1.5))
            if i == 0 and a < 215:
                continue
            horns |= L(bs[0], bs[1], 2.3 - i * 0.3, *pol(bs, a - 8, 6.5 - i), 0.6)
        p.form(horns, ('b0', 'b1', 'b2'), sd=1, hl=1)
        p.form(m, SHELL, sd=max(2, 5 - i), hl=1)
        inner = erode(m, 1)
        # spiral growth ridges
        for j in range(-3, 4):
            x0 = o[0] + j * rx / 3.2
            p.line([(x0 - 2, o[1] - ry), (x0 + 1, o[1]), (x0 - 1, o[1] + ry)], 's1', only=inner & ~sh(m, -3, -3) | (inner & (p.a == I('s2'))))
        # greenish algae band along the top of each whorl
        band = m & ~sh(m, 0, 3) & inner
        p.fill(band & (p.a == I('s2')), 'g1')
        p.fill(R(o[0] - rx * 0.5, o[1] - ry * 0.55, o[0] - rx * 0.5 + 3, o[1] - ry * 0.55) & inner, 's3')
        c.stamp(p, 'K')
    # aperture: dark mouth of the shell with a thick pale lip
    ap = B((-8, -15), 0.1)
    p = C()
    lip = E(ap[0], ap[1], 10.4, 11.4)
    p.form(lip, ('c0', 'c1', 'c2'), sd=2, hl=1)
    hole = E(ap[0] - 1, ap[1], 8.0, 9.2)
    p.fill(hole, 'q')
    p.fill(hole & ~sh(hole, 3, 0), 'r0')
    c.stamp(p, 'K')
    # neck (only when striking out)
    out = S['out']
    hx, hy = int(ap[0]) - 10 - out, int(ap[1]) - 9 + S['drop']
    if out > 4:
        p = C()
        nk = L(ap[0] + 1, ap[1] + 1, 5.0, hx + 12, hy + 9, 4.4)
        p.form(nk, SKIN, sd=2, hl=1)
        for t in (0.3, 0.55, 0.8):
            q = lerp((ap[0] + 1, ap[1] + 1), (hx + 12, hy + 9), t)
            p.line([(q[0], q[1] - 4), (q[0] + 1, q[1] + 4)], 'r1', only=erode(nk, 1))
        c.stamp(p, 'r0')
    # head (clipped by the shell lip when pulled in)
    p = C()
    p.grid(hx, hy, HEAD, LEG)
    if out < 0:
        clip = (px.X < ap[0] + 6 + out * 0.2) | hole
        p.a[~(hole | (px.X < ap[0] - 9 - out))] = 0
    c.stamp(p, 'K')
    # near arm
    claw_arm(c, B((-6, -9)), B(S['nel']), B(S['nwr']), S['nang'], SKIN)
    c.blacken()
    return c


WALK = [
    dict(bob=0, tilt=0, ripple=0),
    dict(bob=-1, tilt=1, ripple=2, nel=(-19, -9), nwr=(-27, -5), fel=(-19, -17), fwr=(-26, -20)),
    dict(bob=0, tilt=0, ripple=3, nel=(-20, -9), nwr=(-29, -5), fel=(-18, -16), fwr=(-24, -20)),
    dict(bob=-1, tilt=-1, ripple=1, nel=(-18, -10), nwr=(-26, -7), fel=(-20, -17), fwr=(-28, -18)),
]
ATTACK = [
    # pulls back into the shell, eyes in the dark
    dict(dx=3, tilt=3, out=-7, nel=(-14, -6), nwr=(-19, -3), nang=160, fel=(-15, -18), fwr=(-19, -22), fang=220),
    # springs out on a long neck
    dict(dx=-4, tilt=-4, out=24, drop=-3, ripple=3, nel=(-17, -5), nwr=(-26, -2), nang=175, fel=(-19, -22), fwr=(-25, -29), fang=215),
    dict(dx=-2, tilt=-1, out=9, drop=1, ripple=1),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
