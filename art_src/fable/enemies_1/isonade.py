"""Isonade - deep-blue sea-monster shark; its tail fin is studded with iron-hard hooks that drag sailors under."""
from kit import *

NAME = 'isonade'
CW, CH = 152, 92
OX, OY = 44, 22           # local low line y=58
SK = ('d1', 'd2', 'd3')
FARR = ('d0', 'd1', 'd2')

LEG = dict(zip('abcdvwxqKYZm', ['d0', 'd1', 'd2', 'd3', 'v1', 'v2', 'v3', 'q', 'K', 'y2', 'y3', 'm1']))
HEAD = """
..............bbbbbbbbbbbb
..........bbbccccccccccccc
.......bbcccddddcccccccccc
.....bccdddddddccccccccccc
...bccdddddccccKKKKccccccc
..bcdddccccccKKKKKcccccccc
.bcddcccccccccKYZKcccccccc
bcdcccccccccccaKKccccccccc
bcccKcccccccccccccccccbbbb
.bKKKKKKKKKKKKKKKKKccbbbbb
..KxxqqxxqqxxqqxxqqKKbbbbb
..KqxqqqxqqqxqqqxqqqmKbbbb
...KqqqqqqqqqqqqqqqmmKbbbb
...KqqwqqqwqqqwqqqwmmKbbbb
....KwwqqwwqqwwqqwwKKvvvbb
....vKKKKKKKKKKKKKKvvvvvvv
.....vwwwwwwwwwwwvvvvvvvvv
.......vvwwwwwwvvvvvvvvvv.
"""

DEF = dict(sp=[(18, 31, 8.0), (28, 30.5, 10.2), (40, 30, 10.4), (50, 28.5, 8.6), (58, 24.5, 5.6), (64, 18.5, 3.6), (68, 12, 2.6)],
           head=(0, 22), tf=-62, pec=0, drops=0)


def P(x, y):
    return (x + OX, y + OY)


def tailfin(c, T, th, ramp):
    """crescent caudal fin + iron hooks on the leading edge of the long upper lobe"""
    def pt(d, a):
        r_ = math.radians(th + a)
        return (T[0] + math.cos(r_) * d, T[1] + math.sin(r_) * d)
    U, N, Lw = pt(22, -36), pt(6, 6), pt(14, 54)
    p = C()
    fin = PG([pt(3, -95), pt(12, -62), U, pt(12, -10), N, pt(8, 30), Lw, pt(8, 78), pt(3, 95)])
    p.form(fin, ramp, sd=2, hl=1)
    p.line([pt(3, -10), pt(15, -34)], ramp[0], only=erode(fin, 1))
    p.line([pt(3, 25), pt(10, 54)], ramp[0], only=erode(fin, 1))
    c.stamp(p, 'd0')
    # bone hooks: thorn barbs on the outer edge of the long lobe, tips curling back toward the body
    p = C()
    for d, a, ln_ in ((9, -74, 5.0), (15, -55, 5.5), (21, -42, 5.5), (12, 66, 4.0)):
        b_ = pt(d, a)
        sgn = -1 if a < 0 else 1
        r_ = math.radians(th + a + sgn * 62)
        t1 = (b_[0] + math.cos(r_) * ln_ * 0.6, b_[1] + math.sin(r_) * ln_ * 0.6)
        r2 = math.radians(th + a + sgn * 128)
        t2 = (t1[0] + math.cos(r2) * ln_ * 0.6, t1[1] + math.sin(r2) * ln_ * 0.6)
        m = L(b_[0], b_[1], 1.9, t1[0], t1[1], 1.2) | L(t1[0], t1[1], 1.2, t2[0], t2[1], 0.5)
        p.fill(m, 'b2'); p.fill(m & ~sh(m, -1, -1), 'b1'); p.fill(m & ~sh(m, 1, 1) & sh(m, -1, -1), 'b3')
    c.stamp(p, 'K')


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
    hx, hy = P(*S['head'])
    pc = S['pec']
    # far pectoral fin
    p = C()
    fx, fy = pts[5][0] + 2, pts[5][1] + 6
    p.form(PG([(fx - 4, fy), (fx + 3, fy - 1), (fx + 13, fy + 9 + pc), (fx + 6, fy + 7 + pc)]), FARR, sd=1, hl=0)
    c.stamp(p, 'd0')
    tailfin(c, pts[-1], S['tf'], SK)
    # dorsal fins
    p = C()
    i = int(n * 0.36); dx_, dy_ = pts[i][0], pts[i][1] - rad[i] + 2
    p.form(PG([(dx_ - 6, dy_ + 1), (dx_ + 5, dy_ - 13), (dx_ + 9, dy_ - 13), (dx_ + 8, dy_ - 5), (dx_ + 11, dy_ + 2)]), SK, sd=2, hl=1)
    p.line([(dx_ + 3, dy_ - 8), (dx_ + 5, dy_)], 'd1')
    i = int(n * 0.72); ex, ey = pts[i][0], pts[i][1] - rad[i] + 1
    p.form(PG([(ex - 3, ey + 1), (ex + 3, ey - 5), (ex + 5, ey - 4), (ex + 5, ey + 3)]), SK, sd=1, hl=1)
    c.stamp(p, 'd0')
    # body + head in one part so the jaw line belongs to the silhouette
    p = C()
    body = tube(pts, 0, 0, rad)
    p.form(body, SK, sd=4, hl=1)
    up = tube([(x, y - 6) for x, y in pts], 0, 0, [r + 1 for r in rad])
    belly = body & ~up
    p.fill(belly, 'v1')
    p.fill(belly & ~sh(body, -2, -2), 'v0')
    p.fill(belly & sh(~belly, 0, 1) & sh(belly, 0, -1) & sh(belly, 1, 0), 'v2')
    # rough-skin dashes + back glint
    for i in (10, 16, 22, 27):
        if i < n:
            x, y = int(pts[i][0]), int(pts[i][1] - rad[i] * 0.3)
            if all(p.a[y, x + d] == I('d2') for d in (-1, 0, 1, 2)):
                p.pxs([(x, y), (x + 1, y)], 'd1')
    i = int(n * 0.2); x, y = int(pts[i][0]), int(pts[i][1] - rad[i] + 2)
    p.fill(R(x, y, x + 4, y) & (p.a == I('d2')), 'd3')
    p.grid(hx, hy, HEAD, LEG)
    # gill slits
    for k in range(3):
        gx = hx + 24 + k * 3
        p.line([(gx + 1, hy + 4), (gx, hy + 7), (gx + 1, hy + 11)], 'd0', only=body)
    c.stamp(p, 'd0')
    # near pectoral fin
    p = C()
    fx, fy = hx + 27, hy + 14
    fin = PG([(fx - 4, fy - 1), (fx + 5, fy - 2), (fx + 15, fy + 10 + pc), (fx + 12, fy + 12 + pc), (fx + 3, fy + 7 + pc // 2)])
    p.form(fin, SK, sd=2, hl=1)
    p.line([(fx + 2, fy + 2), (fx + 11, fy + 9 + pc)], 'd1', only=erode(fin, 1))
    c.stamp(p, 'd0')
    # brine drops shaken off the tail
    if S['drops']:
        p = C()
        for (dx, dy) in ((58, 44), (66, 38))[:S['drops']]:
            q = P(dx, dy + S['drops'])
            m = E(q[0], q[1], 1.5, 1.9)
            p.fill(m, 'a1'); p.fill(m & ~sh(m, 1, 1), 'a2')
        c.stamp(p, 'a0')
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


WALK = [
    pose(),
    pose(dy=[0, 0, 0, 1, 2, 2, 2], dx=[0, 0, 0, 0, 1, 2, 4], tf=-50, pec=1, head=(0, 21), drops=1),
    pose(dy=[0, 0, 0, 0, 0, 0, 0], head=(0, 21), pec=2, drops=2),
    pose(dy=[0, 0, 0, -1, -2, -2, -3], dx=[0, 0, 0, 0, -1, -2, -4], tf=-74, pec=1),
]
ATTACK = [
    # rear back: body bunches, tail cocked high and back
    pose(dx=[6, 6, 5, 4, 5, 8, 12], dy=[-2, -1, 0, 0, 0, -1, -2], head=(6, 19), tf=-40, pec=-2),
    # lunge: jaws thrown forward, hooked tail whipped over the back
    pose(dx=[-14, -13, -12, -12, -14, -19, -27], dy=[2, 1, 0, -2, -6, -11, -13], head=(-14, 24), tf=-150, pec=3, drops=2),
    pose(dx=[-6, -6, -5, -5, -6, -7, -9], dy=[1, 0, 0, 0, -1, -2, -3], head=(-6, 23), tf=-95, pec=1, drops=1),
]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
