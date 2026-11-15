"""Nue: monkey face, tanuki body, tiger legs, snake tail, wrapped in storm cloud (boss, ~110 px tall, 170 long)."""
from bl import *

NAME = 'boss_nue'
CW, CH = 300, 184
OX, OY = 62, 42          # local baseline y=130
FUR = ('s1', 's2', 's3')
TIG = ('t0', 't1', 't2')
TFAR = ('s1', 't0', 't1')
SNK = ('g1', 'g2', 'g3')
CLD = ('h0', 'i1', 'i2')

LEG = dict(zip('fFGabcdeKYZWwq', ['b0', 'b1', 'b2', 'r0', 'r1', 'r2', 'r3', 'r4', 'K', 'y2', 'y3', 'b3', 'b2', 'q']))
FACE = """
........fffFFFFff.......
.....ffFFGGFFFFFFff.....
....fFGGFFFFFFFFFFFf....
...fFGFFbbbbbbbFFFFFf...
..fFFFbccdccccccbFFFFf..
..fFFbcdddccccccabFFFf..
.fFFbcKKdccccccKKabFFFf.
.fFbKKKKKKccKKKKKKabFFf.
.fFbaKKKKKKbKKKKKaabFFf.
.fbcYZYYKacbaKYZYYabFFf.
.fbcaYYKaccbbaYYKabbFFf.
..bccaaaccdccbaaabbFFFf.
.bcddccccdcccccbbbFFFFf.
bcdedcKccKcccccbbFFFFf..
bcddcccccccccccbbFFFFf..
bKKKKKKKKKKKKccbbFFFf...
bWqWwqwWqwqqqKcbbFFFf...
.WqWqqqqWqqqqKbbFFFf....
.bqqwqWqwqWqqKbbFFf.....
..bKKKKKKKKKKbbFFf......
..bcccccccbbbbFFf.......
...bbbbbbbbFFff.........
"""


def P(x, y):
    return (x + OX, y + OY)


def tleg(c, J, ramp, far=False):
    """tiger leg: J = (shoulder/hip, elbow/knee, wrist/hock, paw)"""
    a, b, d, e = J
    p = C()
    up = L(*a, 10.4, *b, 7.4)
    lo = L(*b, 6.6, *d, 4.8)
    ft = L(*d, 4.6, e[0] + 2, e[1] - 2, 4.2)
    paw = E(e[0] - 2, e[1], 7.4, 4.4)
    p.form(up, ramp, sd=4, hl=1)
    for i_, t0 in enumerate((0.1, 0.3, 0.5, 0.7)):
        cut = ~sh(up, -7, 0) if i_ % 2 else ~sh(up, 9, 0)
        p.fill(band(a, b, t0, t0 + 0.12, 12) & up & cut, 'K')
    p.form(lo, ramp, sd=2, hl=1)
    for i_, t0 in enumerate((0.15, 0.4, 0.65, 0.9)):
        cut = ~sh(lo, -5, 0) if i_ % 2 else ~sh(lo, 6, 0)
        p.fill(band(b, d, t0, t0 + 0.1, 9) & lo & cut, 'K')
    p.form(ft, ramp, sd=2, hl=1)
    p.form(paw, ramp, sd=2, hl=1)
    p.line([(e[0] - 5, e[1] - 1), (e[0] - 5, e[1] + 3)], ramp[0], only=paw)
    p.line([(e[0] - 1, e[1]), (e[0] - 1, e[1] + 3)], ramp[0], only=paw)
    c.stamp(p, 'K')
    for i in range(3):
        cx = int(e[0] - 9 + i * 4); cy = int(e[1] + 2)
        c.pxs([(cx, cy), (cx + 1, cy), (cx, cy + 1)], 'b3' if not far else 'b2')


def snake(c, pts, mouth=3):
    """pts: control points from the rump to the neck; head faces along the last segment"""
    n = len(pts) - 1
    p = C()
    m = np.zeros((px.H, px.W), bool)
    for i in range(n):
        r0_ = 6.2 - i * 0.45; r1_ = 6.2 - (i + 1) * 0.45
        m |= L(*pts[i], r0_, *pts[i + 1], r1_)
    p.form(m, SNK, sd=3, hl=1)
    # belly scales on the inner side + diamond blotches
    for i in range(n):
        for t in (0.25, 0.75):
            q = lerp(pts[i], pts[i + 1], t)
            p.fill(band(pts[i], pts[i + 1], t - 0.1, t + 0.1, 8) & m & (p.a == I('g2')), 'g1')
    c.stamp(p, 'K')
    # head
    hx, hy = pts[-1]
    d = (pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]); ang = math.degrees(math.atan2(d[1], d[0]))
    p = C()
    up = PG([pol((hx, hy), ang + 100, 6), pol((hx, hy), ang - 100, 6.5), pol((hx, hy), ang - 30 - mouth, 13), pol((hx, hy), ang - 8 - mouth, 19),
             pol((hx, hy), ang + 4 - mouth, 12)])
    lo = PG([pol((hx, hy), ang + 100, 6), pol((hx, hy), ang + 30 + mouth * 3, 10), pol((hx, hy), ang + 14 + mouth * 4, 17),
             pol((hx, hy), ang + 2 + mouth * 3, 9)])
    gap = PG([(hx, hy), pol((hx, hy), ang - 4 - mouth, 16), pol((hx, hy), ang + 12 + mouth * 4, 15)])
    p.fill(gap, 'q')
    p.form(lo, ('g0', 'g1', 'g2'), sd=1, hl=0)
    p.form(up | E(hx, hy, 6.4, 6.0), SNK, sd=2, hl=1)
    c.stamp(p, 'K')
    e = pol((hx, hy), ang - 45, 6)
    c.pxs([(int(e[0]), int(e[1])), (int(e[0]) + 1, int(e[1]))], 'y2'); c.px(int(e[0]), int(e[1]), 'y3')
    c.pxs([(int(e[0]) - 1, int(e[1]) - 1), (int(e[0]), int(e[1]) - 1), (int(e[0]) + 1, int(e[1]) - 1), (int(e[0]) + 2, int(e[1]))], 'K')
    if mouth > 2:
        f0 = pol((hx, hy), ang - 6 - mouth, 15); f1 = pol(f0, ang + 80, 4.5)
        c.fill(L(*f0, 0.9, *f1, 0.4), 'b3')
        t0 = pol((hx, hy), ang + 4, 12); t1 = pol(t0, ang + 2, 9)
        c.line([t0, t1], 'e1'); c.line([t1, pol(t1, ang - 30, 3)], 'e1'); c.line([t1, pol(t1, ang + 30, 3)], 'e1')


def cloud(c, blobs, bolts=()):
    p = C()
    m = np.zeros((px.H, px.W), bool)
    for (x, y, rx, ry) in blobs:
        m |= E(*P(x, y), rx, ry)
    for (x, y, rx, ry) in blobs:                       # scalloped puffs along the top
        for k in (-0.6, 0.0, 0.6):
            m |= E(*P(x + rx * k, y - ry * 0.55), rx * 0.42, ry * 0.6)
    p.form(m, CLD, sd=4, hl=1)
    for (x, y, rx, ry) in blobs[::2]:                  # swirl
        if ry > 6:
            q = P(x, y)
            p.line([(q[0] - rx * 0.5, q[1] + 2), (q[0], q[1] + 4), (q[0] + rx * 0.4, q[1] + 1), (q[0] + rx * 0.3, q[1] - 2), (q[0], q[1] - 2)], 'i0', only=m)
    c.stamp(p, 'K')
    for pts in bolts:
        q = [P(*t) for t in pts]
        c.line(q, 'y2'); c.line([(x_ + 1, y_) for x_, y_ in q[:-1]], 'y3')


DEF = dict(
    dy=0, dx=0, fdy=0, bdy=0, head=(0, 0),
    nf=((88, 94), (82, 110), (76, 121), (68, 126)), ff=((104, 92), (104, 109), (100, 121), (94, 126)),
    nh=((146, 90), (136, 107), (152, 118), (144, 126)), fh=((158, 88), (152, 105), (166, 118), (160, 126)),
    snk=((160, 78), (180, 62), (182, 40), (166, 22), (144, 20), (128, 30), (118, 38)), mouth=3,
    cl=0, bolt=0,
)


def nue(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    dx, dy = S['dx'], S['dy']

    def F(pt):
        return P(pt[0] + dx, pt[1] + dy + S['fdy'])

    def Bk(pt):
        return P(pt[0] + dx, pt[1] + dy + S['bdy'])

    def LJ(J, T):
        return (T(J[0]), P(*J[1]), P(*J[2]), P(*J[3]))

    cl = S['cl']
    # ---- storm cloud behind
    bolts = [[(196, 70), (190, 80), (197, 86), (189, 98)]] if S['bolt'] == 1 else ([[(30, 96), (38, 104), (31, 110), (40, 122)],
             [(204, 60), (198, 72), (206, 78), (200, 92)]] if S['bolt'] == 2 else [])
    cloud(c, [(150 + cl, 58, 22, 13), (176 - cl, 70, 20, 12), (196 + cl, 88, 16, 10), (128 - cl, 52, 16, 9), (168, 50 - cl, 14, 9),
              (190 - cl, 112, 18, 9), (206 + cl, 121, 14, 7)], bolts)

    tleg(c, LJ(S['ff'], F), TFAR, far=True)
    tleg(c, LJ(S['fh'], Bk), TFAR, far=True)
    snake(c, [Bk(q) if i < 2 else P(q[0] + dx, q[1] + dy) for i, q in enumerate(S['snk'])], S['mouth'])

    # ---- tanuki body: shaggy barrel
    p = C()
    ch, ru = F((92, 82)), Bk((144, 84))
    body = L(*ch, 22, *ru, 19)
    tuft = np.zeros_like(body)
    for t, a_, l_ in ((0.0, 80, 10), (0.2, 75, 11), (0.42, 78, 10), (0.64, 72, 10), (0.86, 70, 9)):   # belly fringe
        q = lerp(ch, ru, t); tuft |= tri((q[0], q[1] + 17), a_, l_, 9)
    for t, a_, l_ in ((0.1, 300, 9), (0.3, 305, 10), (0.52, 310, 9), (0.74, 315, 9), (0.96, 330, 10), (1.1, 10, 9)):   # back ridge
        q = lerp(ch, ru, t); tuft |= tri((q[0], q[1] - 17), a_, l_, 9)
    full = body | tuft
    p.form(full, FUR, sd=6, hl=1)
    back = full & ~sh(full, 0, 9) & (px.X > ch[0] - 8)                               # dark dorsal saddle
    p.fill(back & (p.a == I('s2')), 's1'); p.fill(back & (p.a == I('s3')), 's2')
    for t, yo in ((0.1, 2), (0.3, 8), (0.5, 0), (0.7, 7), (0.9, 2), (0.2, -6), (0.6, -7), (0.85, -4)):   # fur ticks
        q = lerp(ch, ru, t); x_, y_ = int(q[0]), int(q[1] + yo)
        p.line([(x_, y_), (x_ + 3, y_ + 3)], 's1', only=body)
    p.form(E(ch[0] - 1, ch[1] + 3, 16, 15) & full, FUR, sd=3, hl=1)                     # shoulder mass
    p.form(E(ru[0] + 3, ru[1] + 1, 15, 15) & full, FUR, sd=3, hl=1)                     # haunch
    p.fill(R(ch[0] - 4, ch[1] - 9, ch[0] + 1, ch[1] - 9), 's3', only=full)
    c.stamp(p, 'K')

    tleg(c, LJ(S['nh'], Bk), TIG)
    tleg(c, LJ(S['nf'], F), TIG)

    # ---- head: mane + chest ruff, then the monkey face grid
    hx, hy = S['head']
    HX, HY = F((40 + hx, 50 + hy))
    p = C()
    cx, cy = HX + 14, HY + 11
    mane = E(cx + 4, cy, 17.4, 16.4)
    for a_, l_ in ((215, 6), (250, 8), (280, 11), (305, 13), (330, 15), (355, 15), (20, 15), (45, 13), (70, 12), (100, 10), (130, 8)):
        mane |= tri(pol((cx + 4, cy), a_, 14), a_ + (25 if a_ > 180 else -15), l_, 10)
    ruff = tri((cx + 10, cy + 12), 75, 20, 16) | tri((cx + 2, cy + 13), 95, 15, 12)
    p.form(mane | ruff, ('b0', 'b1', 'b2'), sd=5, hl=1)
    for a_ in (300, 335, 10, 45, 80):
        q0 = pol((cx + 4, cy), a_, 11); p.line([q0, pol(q0, a_ + 10, 6)], 'b0', only=mane)
    c.stamp(p, 'K')
    p = C()
    p.form(E(HX + 21, HY + 10, 3.4, 4.4), ('r0', 'r1', 'r2'), sd=1, hl=0)                     # ear
    c.stamp(p, 'K')
    p = C()
    p.grid(HX, HY, FACE, LEG)
    c.stamp(p, 'K', skip=('b0', 'b1', 'b2'))

    # ---- low storm cloud in front of the hind feet
    cloud(c, [(178 + cl, 123, 14, 6), (160 - cl, 125, 10, 4.4)], ())
    c.blacken()
    return c


WALK = [
    dict(nf=((88, 94), (78, 108), (70, 120), (60, 126)), ff=((104, 92), (110, 108), (112, 120), (108, 126)),
         nh=((146, 90), (142, 107), (160, 117), (154, 126)), fh=((158, 88), (146, 104), (156, 118), (148, 126)), cl=0),
    dict(dy=-1, nf=((88, 94), (84, 110), (80, 121), (72, 126)), ff=((104, 92), (100, 106), (92, 114), (84, 119)),
         nh=((146, 90), (136, 105), (146, 114), (138, 121)), fh=((158, 88), (154, 105), (170, 117), (164, 126)), cl=1,
         snk=((160, 78), (181, 62), (184, 40), (168, 21), (146, 18), (129, 27), (118, 34)), mouth=5, bolt=1),
    dict(nf=((88, 94), (92, 110), (92, 121), (86, 126)), ff=((104, 92), (96, 108), (88, 120), (78, 126)),
         nh=((146, 90), (132, 106), (144, 118), (134, 126)), fh=((158, 88), (156, 106), (174, 117), (168, 126)), cl=2),
    dict(dy=-1, nf=((88, 94), (80, 106), (72, 114), (64, 119)), ff=((104, 92), (106, 110), (106, 121), (100, 126)),
         nh=((146, 90), (140, 107), (158, 117), (152, 126)), fh=((158, 88), (146, 102), (154, 112), (146, 119)), cl=1,
         snk=((160, 78), (179, 62), (180, 40), (164, 23), (142, 22), (127, 33), (118, 42)), mouth=2),
]
ATTACK = [
    # wind-up: crouch, snake coils back
    dict(dy=8, dx=6, fdy=4, nf=((88, 98), (76, 112), (72, 122), (62, 126)), ff=((104, 96), (98, 112), (98, 122), (90, 126)),
         nh=((146, 96), (128, 108), (150, 120), (140, 126)), fh=((158, 94), (144, 106), (164, 120), (156, 126)),
         snk=((160, 78), (184, 66), (194, 44), (184, 24), (164, 20), (152, 32), (146, 42)), mouth=6, bolt=1),
    # strike: airborne pounce, claws out, snake lunging past the head
    dict(dy=-14, dx=-26, fdy=-4, bdy=3, nf=((88, 92), (70, 100), (54, 104), (38, 108)), ff=((104, 90), (88, 92), (72, 92), (56, 94)),
         nh=((146, 90), (162, 104), (184, 104), (198, 112)), fh=((158, 88), (176, 96), (198, 94), (212, 100)),
         snk=((160, 78), (166, 56), (146, 40), (120, 36), (94, 36), (68, 34), (46, 36)), mouth=9, bolt=2, cl=2),
    # recover: landed
    dict(dy=4, dx=-12, fdy=3, nf=((88, 96), (78, 110), (72, 121), (62, 126)), ff=((104, 94), (100, 110), (96, 121), (88, 126)),
         nh=((146, 92), (140, 108), (158, 118), (150, 126)), fh=((158, 90), (156, 106), (172, 118), (166, 126)),
         snk=((160, 78), (178, 58), (172, 36), (150, 24), (128, 26), (112, 36), (102, 44)), mouth=4, cl=1),
]

if __name__ == '__main__':
    export(NAME, nue, WALK, ATTACK)
