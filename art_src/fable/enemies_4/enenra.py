"""Enenra: a creature of swirling grey smoke with a face. Normal (~58 px), floats. Attack: billows up and blows a smoke cloud."""
from common import *

NAME = 'enenra'
CW, CH = 128, 88
OX, BASE = 80, 82
SM = ('z1', 'z2', 'z3')
SMD = ('z0', 'z1', 'z2')
SML = ('z2', 'z3', 'v2')

LEG = dict(zip('KyYXqz', ['K', 'f1', 'y2', 'y3', 'q', 'z0']))
FACE = """
KK........KK..
zKKK....KKKz..
yYYXK..KYYXy..
.yYYK..KYYy...
..............
..KKqqqqqKK...
.KqqqqqqqqqK..
.zKqqqKKqqKz..
...KKK..KK....
"""


def tendril(o, a0, turn, n, r0, r1=0.9, step=2.3):
    """curling, tapering wisp: returns (mask, end point)"""
    m = np.zeros((px.H, px.W), bool)
    x, y = o
    a = a0
    for i in range(n):
        r = r0 + (r1 - r0) * i / (n - 1)
        nx_, ny_ = x + math.cos(math.radians(a)) * step, y + math.sin(math.radians(a)) * step
        m |= L(x, y, r, nx_, ny_, r)
        x, y = nx_, ny_
        a += turn * (0.6 + 1.2 * i / n)
    return m, (x, y)


def cloud(c, puffs, ramp, extra=None, swirl=()):
    """billows merged in ONE part: the shadow crescent of each billow is the only inner line"""
    p = C()
    if extra is not None:
        p.form(extra, ramp, sd=2, hl=1)
    for (o, rx, ry) in puffs:
        p.form(E(o[0], o[1], rx, ry), ramp, sd=max(1, int(rx / 2.4)), hl=1)
    full = p.m
    for (o, r, d) in swirl:
        pts = [pol(o, 30 + d * i * 45, r * (1 - i / 8)) for i in range(8)]
        p.line(pts, ramp[0], only=erode(full, 2))
    c.stamp(p, 'z0')


DEF = dict(dx=0, bob=0, ph=0, swell=0, blow=0, na=165, fa=200, hx=0, hy=0)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx = OX + S['dx']
    b = S['bob']
    ph = S['ph']
    sw = S['swell']
    wob = lambda k: [0, 1, 0, -1][(k + ph) % 4]

    def B(pt):
        return (cx + pt[0], BASE + pt[1] + b)

    hd = B((-5 + S['hx'], -52 + S['hy']))
    # --- back layer: far arm, rear billows, head plume
    farm, _ = tendril(B((-10, -42)), S['fa'], -9, 10, 4.0, 1.0)
    plume, _ = tendril((hd[0] + 6, hd[1] - 6), 300 + wob(0) * 8, 22, 9, 4.4, 0.9)
    cloud(c, [(B((12 + wob(1), -38)), 7.4 + sw * 0.5, 6.4 + sw * 0.5), (B((10 - wob(2), -26)), 6.0, 5.2),
              (B((15 + wob(3), -31)), 4.0, 3.4)], SMD, extra=farm | plume, swirl=[(B((12, -38)), 4, 1)])
    # --- main layer: curling tail, trunk, head with a lumpy edge
    tail, _ = tendril(B((1 + wob(2), -18)), 78 + wob(1) * 6, 15, 12, 6.6, 1.0, step=2.0)
    cloud(c, [(B((1 + wob(0), -24)), 9.0, 8.0),
              (B((8, -30)), 5.0, 4.6),
              (B((-2, -36)), 12.0 + sw, 10.0 + sw * 0.7),
              (B((-12 - wob(1), -30)), 5.4, 4.6),
              (B((7 + wob(2), -44)), 5.0, 4.4),
              ((hd[0] + 7, hd[1] + 1), 5.0, 5.0),
              ((hd[0] + 3, hd[1] - 7), 5.2, 4.2),
              (hd, 10.4, 9.0),
              ((hd[0] - 6, hd[1] - 7), 3.6, 3.0)],
          SM, extra=tail, swirl=[(B((0, -35)), 6, 1), (B((2, -23)), 4, -1)])
    p = C()
    p.fill(R(hd[0] - 6, hd[1] - 6, hd[0] - 3, hd[1] - 6), 'v2')
    p.grid(int(hd[0]) - 9, int(hd[1]) - 4, FACE, LEG)
    c.stamp(p, ring=False)
    # --- near arm: curling tendril with a clawed puff
    narm, end = tendril(B((-8, -33)), S['na'], 6, 9, 4.8, 1.1)
    cloud(c, [(B((-8, -32)), 5.2, 4.6)], SML, extra=narm)
    c.blacken()
    # blown smoke cloud
    if S['blow']:
        n = S['blow']
        mx, my = int(hd[0]) - 6, int(hd[1]) + 3
        cl = [(-8, 0, 3.4), (-15, -2, 4.6), (-23, 1, 5.6), (-32, -3, 6.6), (-40, 2, 5.0), (-30, 5, 4.4), (-46, -4, 3.4)][:n]
        pc = C()
        cloud(pc, [((mx + ox, my + oy), r, r * 0.85) for (ox, oy, r) in cl[::-1]], SML)
        pc.blacken(rim=False)
        c.stamp(pc, 'K', ring=False)
    return c


WALK = [
    dict(ph=0, bob=0),
    dict(ph=1, bob=-1, na=170, fa=196),
    dict(ph=2, bob=-2, na=175, fa=192),
    dict(ph=3, bob=-1, na=170, fa=196),
]
ATTACK = [
    dict(dx=3, ph=1, swell=3, hx=2, hy=-3, na=120, fa=250),
    dict(dx=-4, ph=2, swell=-1, hx=-3, hy=2, blow=7, na=160, fa=215),
    dict(dx=-2, ph=3, hx=-1, blow=2, na=165, fa=205),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
