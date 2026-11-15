"""Tsuchinoko - fat, flat-bellied brown snake with a thin neck, viper head and a stubby rat tail."""
from kit import *

NAME = 'tsuchinoko'
CW, CH = 136, 68
OX, OY = 44, 18           # local baseline y=44
SK = ('s1', 's2', 's3')

LEG = dict(zip('abcdrRxqYZKe', ['s0', 's1', 's2', 's3', 'c1', 'c2', 'b3', 'q', 'y2', 'y3', 'K', 'e0']))
HEAD = """
.........bbbbbbb.....
.......bcccccccbb....
.....bcddddccccccb...
...bcdddddcccccccbb..
..cddddcccccKKKKccbb.
.cdddccKKKKKKKKcccbbb
cdddcccccYZYKKccccbbb
cdccccccccYYKccbbbbba
ccccKccccccccccbbbbaa
bbKKKKKKKKKKKKbbbbaaa
.xKqqxqqqqqqqKRrraa..
.xKqqqqqqqqKrRrraa...
..KKqqqqqKrrrrraa....
....rRRRRRrrrra......
"""

# spine control points (x, y, radius), head end first. baseline y=44
DEF = dict(sp=[(16, 16, 4.2), (22, 23, 5.0), (30, 29.5, 9.6), (41, 31.4, 12.4), (52, 32.4, 11.4), (60, 37, 6.4), (65, 40.6, 3.0), (71, 39.4, 1.9), (77, 34, 1.3)],
           head=(1, 8), tongue=1)


def P(x, y):
    return (x + OX, y + OY)


def creature(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    sp = S['sp']
    pts = curve([P(x, y) for x, y, r in sp], 6)
    n = len(pts)
    rad = []
    for i in range(n):
        t = i / (n - 1) * (len(sp) - 1)
        k = min(int(t), len(sp) - 2)
        rad.append(sp[k][2] + (sp[k + 1][2] - sp[k][2]) * (t - k))
    p = C()
    body = tube(pts, 0, 0, rad)
    p.form(body, SK, sd=7, hl=1)
    # belly plates: pale underside band with segment lines
    belly = body & ~sh(body, 0, -4)
    belly &= (px.X < pts[int(n * 0.84)][0]) & (px.X > pts[2][0])
    p.fill(belly, 'c1')
    p.fill(belly & ((px.X + px.Y // 2) % 4 == 0), 'c0')
    p.fill(belly & ~sh(body, 0, -1), 'c0')
    p.fill(belly & (px.X > pts[int(n * 0.6)][0]), 'c0')
    # dorsal saddles: dark wedge bands across the back, pale centre scale
    for k, i in enumerate(range(7, int(n * 0.9), 6)):
        x, y = pts[i]; r = rad[i]
        if r < 3.2:
            continue
        w = 2.2 + r * 0.16
        sad = PG([(x - w, y - r - 1), (x + w, y - r - 1), (x + w * 0.45 + 1, y - r * 0.12), (x - w * 0.45 + 1, y - r * 0.12)])
        p.fill(sad & body & sh(body, 0, 1) & sh(body, 1, 0), 's0')
        if r > 6:
            p.fill(R(x, y - r * 0.62, x + 1, y - r * 0.62 + 1) , 's1')
    for i in range(10, int(n * 0.8), 6):
        x, y = pts[i]; r = rad[i]
        if r > 6:
            q = (int(x - 1), int(y + r * 0.2))
            if all(p.a[q[1], q[0] + d] == I('s2') for d in (-1, 0, 1, 2)):
                p.pxs([q, (q[0] + 1, q[1])], 's1')
    # glint on the fat back
    i = int(n * 0.42); x, y = pts[i]
    g = R(x - 5, y - rad[i] + 2, x - 2, y - rad[i] + 2)
    p.fill(g & (p.a == I('s2')), 's3')
    c.stamp(p, 's0')
    # forked tongue
    hx, hy = P(*S['head'])
    if S['tongue']:
        t = S['tongue']
        c.pxs([(hx, hy + 12), (hx - 1, hy + 12), (hx - 2, hy + 12 + (t > 1)), (hx - 3, hy + 11 + (t > 1) * 2), (hx - 3, hy + 13 + (t > 1))], 'e0')
    p = C()
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 's0')
    c.blacken()
    return c


def pose(dy=None, dx=None, **kw):
    sp = [list(q) for q in DEF['sp']]
    for i, v in enumerate(dy or []):
        sp[i][1] += v
    for i, v in enumerate(dx or []):
        sp[i][0] += v
    d = dict(sp=[tuple(q) for q in sp]); d.update(kw)
    return d


# inchworm crawl: a hump travels from tail to head, belly always touches y=44 somewhere
WALK = [
    pose(dy=[0, 0, 0, 0, 0, 0, 0, 0, 0]),
    pose(dy=[0, 0, 0, 0, -2, -4, -2, 0, 2], dx=[0, 0, 0, 0, -1, -3, -4, -4, -4], tongue=2),
    pose(dy=[-1, -1, -1, -3, -2, 0, 0, 0, 1], dx=[0, 0, 1, 0, -1, -2, -2, -2, -2], head=(1, 7)),
    pose(dy=[-1, -2, -2, -1, 0, 0, 0, 0, -1], dx=[-1, -1, 0, 0, 0, -1, -1, -1, -1], head=(0, 7), tongue=2),
]
ATTACK = [
    # coil: head pulled back and up, body bunched into a tight S
    dict(sp=[(33, 8, 4.2), (41, 10, 5.0), (45, 19, 7.4), (37, 27, 10.6), (42, 31, 12.6), (54, 32.6, 11.2), (61, 37.4, 6.2), (67, 41, 2.8), (73, 41.6, 1.6)],
         head=(18, 0), tongue=2),
    # spring: whole body launched flat and long, front half in the air
    dict(sp=[(-14, 20, 4.2), (-5, 22, 5.2), (6, 24, 8.4), (19, 26, 10.6), (32, 28.6, 9.8), (42, 33, 6.0), (49, 37, 3.2), (56, 41, 2.0), (62, 42.4, 1.4)],
         head=(-29, 12), tongue=0),
    # land
    dict(sp=[(4, 21, 4.2), (11, 27, 5.0), (19, 31.4, 9.4), (30, 31.6, 12.2), (41, 32.4, 11.4), (50, 37, 6.4), (56, 40.6, 3.0), (62, 38, 1.9), (66, 32, 1.3)],
         head=(-11, 14), tongue=1),
]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
