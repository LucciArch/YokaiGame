"""Karasu: black crow with red eyes, wings spread. Small flyer (~36 px). Attack: dive peck."""
from common import *

NAME = 'karasu'
CW, CH = 88, 84
FEA = ('h0', 'h1', 'h2')
FEAF = ('h0', 'h0', 'h1')

LEG = dict(zip('KmnojJiIeEZq', ['K', 'h0', 'h1', 'h2', 'i2', 'i3', 'i1', 'i0', 'e0', 'e1', 'y3', 'q']))
HEAD = """
........mnnnm.....
......mnoonnnnm...
.....mnonnnnnnnm..
....KKnnKKKnnnnnm.
.jJJjinnKeEKnnnnm.
jJjjjiinKEZKnnnnnm
KIIIIIIinKKnnnnnnm
.KiiiiiKmnnnnnnnm.
...KKKKmmnnnnnnm..
.......mmmnnnnm...
"""
HEAD_OPEN = """
........mnnnm.....
......mnoonnnnm...
.....mnonnnnnnnm..
.jJ.KKnnKKKnnnnnm.
jJjjjinnKeEKnnnnm.
.KKKjiinKEZKnnnnnm
....KKqinKKnnnnnnm
..KiiiiKmnnnnnnnm.
.KiiKKKmmnnnnnnm..
.KK....mmmnnnnm...
"""


def adiff(a, b, t):
    return a + (b - a) * t


def wing(c, s, tip, trail, ramp, scale=1.0, n=7):
    """fan of flight feathers; tip / trail = directions (deg) of the outermost primary and innermost secondary"""
    wrist = pol(s, tip + (trail - tip) * 0.25, 8 * scale)
    p = C()
    masks = []
    for i in range(n):
        t = i / (n - 1)                      # 0 = innermost secondary, 1 = outer primary
        base = lerp(s, wrist, min(1.0, t * 1.3))
        d = adiff(trail, tip, t)
        ln_ = (10 + 12 * t) * scale
        masks.append(L(base[0], base[1], 2.2, *pol(base, d, ln_), 0.8))
    allm = np.zeros_like(masks[0])
    for m in masks:
        allm |= m
    arm = L(s[0], s[1], 3.0, wrist[0], wrist[1], 2.4)
    p.form(allm | arm, ramp, sd=2, hl=0)
    # feather separation: each feather keeps a 1px dark edge on its trailing side
    for i in range(n - 1, 0, -1):
        m = masks[i]
        e = m & ~erode(m, 1) & ~sh(m, 1, 1) & allm
        over = e
        for j in range(i + 1, n):
            over = over & ~masks[j]
        p.fill(over, ramp[0])
    p.form(arm, ramp, sd=1, hl=1)
    cov = L(s[0], s[1], 2.0, *lerp(s, wrist, 0.8), 1.4)
    p.fill(sh(cov, 0, -1) & arm, ramp[2])
    c.stamp(p, 'K')


DEF = dict(fsp=30, dx=0, dy=0, tip=272, trail=350, scale=1.0, hx=0, hy=0, open=False, tail=0, pitch=0, feet=0)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx, cy = 46 + S['dx'], 46 + S['dy']
    pt = S['pitch']                      # tail end moves by pitch px (positive = tail down)
    shd = (cx - 1, cy - 3)
    # far wing (behind body, a bit forward and darker)
    wing(c, (shd[0] - 4, shd[1] - 1), S['tip'] - S['fsp'], S['trail'] - S['fsp'], FEAF, S['scale'] * 0.92)
    # tail fan
    p = C()
    tb = (cx + 8, cy + 2 + pt // 2)
    tm = np.zeros((CH, CW), bool)
    for a in (-8, 6, 20):
        tm |= L(tb[0], tb[1], 2.6, *pol(tb, a + S['tail'] + pt * 3, 13), 1.6)
    p.form(tm, FEA, sd=2, hl=1)
    for a in (-1, 13):
        p.line([tb, pol(tb, a + S['tail'] + pt * 3, 13)], 'h0', only=tm)
    c.stamp(p, 'K')
    # feet: tucked talons
    p = C()
    fb = (cx + 1, cy + 5 + pt // 3)
    fa = 150 + S['feet']
    for o in (0, 4):
        k = pol((fb[0] + o, fb[1]), fa, 4)
        p.fill(L(fb[0] + o, fb[1], 1.2, k[0], k[1], 1.0), 'i1')
        for da in (-35, 10):
            p.fill(LN([k, pol(k, fa + da, 3)]), 'i2')
    c.stamp(p, 'K')
    # body
    p = C()
    body = L(cx - 6, cy - 1 + S['hy'] // 2, 5.4, cx + 6, cy + 2 + pt // 2, 4.6)
    p.form(body, FEA, sd=3, hl=1)
    # breast feather ticks
    for (ox, oy) in [(-6, 2), (-2, 4), (2, 5)]:
        p.pxs([(cx + ox, cy + oy), (cx + ox + 1, cy + oy)], 'h0')
    c.stamp(p, 'K')
    # head
    p = C()
    p.grid(cx - 23 + S['hx'], cy - 10 + S['hy'], HEAD_OPEN if S['open'] else HEAD, LEG)
    c.stamp(p, 'K', skip=('h1', 'h0'))
    # near wing
    wing(c, shd, S['tip'], S['trail'], FEA, S['scale'])
    c.blacken()
    return c


WALK = [
    dict(dy=1, tip=272, trail=350),
    dict(dy=-1, tip=312, trail=375, scale=0.85, fsp=22),
    dict(dy=-2, tip=62, trail=5, feet=-10, fsp=-18),
    dict(dy=0, tip=22, trail=-30, scale=0.9, fsp=-20),
]
ATTACK = [
    dict(dx=6, dy=-6, tip=255, trail=325, fsp=28, pitch=3, hy=-1, hx=1, tail=10, open=True),
    dict(dx=-10, dy=9, tip=322, trail=368, scale=0.95, fsp=16, pitch=-4, hy=3, hx=-2, tail=-10, feet=-40),
    dict(dx=-5, dy=4, tip=45, trail=0, hy=1, open=True, fsp=-16),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
