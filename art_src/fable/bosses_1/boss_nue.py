"""Nue: monkey face, tanuki body, tiger legs, snake tail, wrapped in storm cloud (boss, ~110 px tall, 170 long)."""
from bl import *

NAME = 'boss_nue'
CW, CH = 300, 184
OX, OY = 62, 42          # local baseline y=130
FUR = ('s1', 's2', 's3')
TIG = ('t0', 't1', 't2')
col('t2', '#f0b038')
TFAR = ('s1', 't0', 't1')
SNK = ('g1', 'g2', 'g3')
CLD = ('h0', 'i1', 'i2')
col('z0', '#2c2836'); col('z1', '#5e5660'); col('z2', '#958a88'); col('z3', '#c4b8ac'); add_rim('z0 z1 z2', 'z3')

LEG = dict(zip('fFGabcdeKYZWwq', ['z0', 'z1', 'z2', 'r0', 'r1', 'r2', 'r3', 'r4', 'K', 'y2', 'y3', 'b3', 'b2', 'q']))
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
    """Tigerbein: J = (Schulter/Hüfte, Ellbogen/Knie, Fessel, Pfote) – weich verjüngt, geschwungene Streifen, Krallen."""
    a, b, d, e = J
    p = C()
    up = L(*a, 7.6, *b, 5.4)
    lo = L(*b, 4.8, *d, 3.6)
    ft = L(*d, 4.2, e[0] + 1, e[1] - 2, 4.4)
    paw = E(e[0] - 1, e[1] - 0.5, 7.6, 4.6)
    leg = up | lo | ft | paw
    p.form(leg, ramp, sd=4, hl=1)
    # geschwungene Streifen: schmale schräge Keile, abwechselnd von vorn und hinten
    for i_, t0 in enumerate((0.25, 0.5, 0.75)):
        q = lerp(a, b, t0); side = 1 if i_ % 2 else -1
        p.fill(tri((q[0] + side * 8, q[1] - 1), 160 if side > 0 else 20, 10, 3.6) & up, 'K')
    for i_, t0 in enumerate((0.3, 0.7)):
        q = lerp(b, d, t0); side = -1 if i_ % 2 else 1
        p.fill(tri((q[0] + side * 5, q[1]), 160 if side > 0 else 20, 6, 2.6) & lo, 'K')
    c.stamp(p, 'K')
    for i in range(4):                                            # Krallen
        cx = int(e[0] - 8 + i * 3.6); cy = int(e[1] + 3)
        c.pxs([(cx, cy), (cx - 1, cy + 1)], 'b3' if not far else 'b2')


def _spline(pts, k=4):
    """Catmull-Rom: glatte Kurve durch die Kontrollpunkte (k Zwischenpunkte je Abschnitt)."""
    out = []
    P_ = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        for j in range(k):
            t = j / k
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t * t * t) for a in (0, 1)))
    out.append(pts[-1])
    return out


def snake(c, pts, mouth=3):
    """pts: control points from the rump to the neck; head faces along the last segment"""
    ctrl = pts
    pts = _spline(pts, 4)
    n = len(pts) - 1
    p = C()
    m = np.zeros((px.H, px.W), bool)
    belly = np.zeros_like(m)
    for i in range(n):
        r0_ = 7.4 - i * 0.62 / 4; r1_ = 7.4 - (i + 1) * 0.62 / 4
        m |= L(*pts[i], r0_, *pts[i + 1], r1_)
    p.form(m, SNK, sd=3, hl=1)
    for i in range(0, n, 2):                                      # Rautenmuster auf dem Rücken
        for t in (0.5,):
            q = lerp(pts[i], pts[i + 1], t)
            r_ = max(1.6, 3.2 - i * 0.25 / 4)
            p.fill(E(q[0], q[1] - 1.5, r_, r_ * 0.7) & m & ~E(q[0], q[1] + 0.5, r_, r_ * 0.7), 'g0')
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

    # ---- Tanuki-Leib: Brustkorb vorn höher, Bauch hängt, kräftige Hüfte; Rücken dunkler, Bauch heller
    p = C()
    ch, ru = F((92, 82)), Bk((144, 84))
    mid = lerp(ch, ru, 0.5)
    body = (E(ch[0] - 1, ch[1] - 5, 19, 17) | E(mid[0] + 2, mid[1] + 6, 21, 13) | E(ru[0] + 2, ru[1] - 3, 17, 16)
            | L(ch[0], ch[1] - 4, 13, ru[0], ru[1] - 3, 11))          # eingesattelter Rücken, hängender Bauch
    tuft = np.zeros_like(body)
    for t in (0.0, 0.14, 0.28, 0.42, 0.56, 0.7, 0.84, 0.98):                               # weiche Fellbuckel am Rücken
        q = lerp(ch, ru, t); tuft |= tri((q[0] + 1, q[1] - 13 - (6 if t < 0.25 else 2 if t < 0.5 else 0)), 300, 3, 8)
    for t, l_ in ((0.25, 5), (0.45, 6), (0.65, 5)):                                          # Bauchzotteln
        q = lerp(ch, ru, t); tuft |= tri((q[0], q[1] + 19), 100, l_, 6)
    full = body | tuft
    p.form(full, FUR, sd=6, hl=1)
    back = full & ~sh(full, 0, 8)                                                           # dunkler Sattel
    p.fill(back & (p.a == I('s2')), 's1'); p.fill(back & (p.a == I('s3')), 's2')
    bel = full & ~sh(full, 0, -7) & (px.X > ch[0] - 6) & (px.X < ru[0] + 4)                # heller Bauch
    p.fill(bel & (p.a == I('s2')), 's3')
    for (q, rx, ry) in ((ch, 10, 7), (ru, 9, 6)):                                         # Volumen: Licht auf Schulter und Kruppe
        hl_ = E(q[0] - 3, q[1] - 9, rx, ry) & body
        p.fill(hl_ & (p.a == I('s2')), 's3')
    p.fill(E(mid[0] - 4, mid[1] - 9, 7, 4) & body & (p.a == I('s1')), 's2')
    sh_band = L(ch[0] + 8, ch[1] - 16, 3, ch[0] + 12, ch[1] + 8, 3) & body                  # dunkles Schulterband (Tanuki)
    p.fill(sh_band, 's1')
    import random as _r
    rg = _r.Random(7)
    for k in range(34):                                                                    # Fellstriche, schräg nach hinten
        t = rg.random(); q = lerp(ch, ru, t)
        x_, y_ = int(q[0] + rg.uniform(-10, 10)), int(q[1] + rg.uniform(-12, 10))
        if body[min(px.H - 1, max(0, y_)), min(px.W - 1, max(0, x_))]:
            p.line([(x_, y_), (x_ + 3, y_ + 2)], 's1' if k % 3 else 's3', only=body)
    c.stamp(p, 'K')

    tleg(c, LJ(S['nh'], Bk), TIG)
    tleg(c, LJ(S['nf'], F), TIG)

    # ---- head: mane + chest ruff, then the monkey face grid
    hx, hy = S['head']
    HX, HY = F((40 + hx, 50 + hy))
    p = C()
    cx, cy = HX + 14, HY + 11
    mane = E(cx + 4, cy, 15.0, 14.0)                                  # Makakenfell: kürzer, weicher
    for a_, l_ in ((250, 4), (280, 6), (305, 7), (330, 8), (355, 8), (20, 8), (45, 7), (70, 6), (100, 5)):
        mane |= tri(pol((cx + 4, cy), a_, 13), a_ + (25 if a_ > 180 else -15), l_, 9)
    ruff = tri((cx + 10, cy + 12), 75, 20, 16) | tri((cx + 2, cy + 13), 95, 15, 12)
    p.form(mane | ruff, ('z0', 'z1', 'z2'), sd=5, hl=1)
    for a_ in (300, 335, 10, 45, 80):
        q0 = pol((cx + 4, cy), a_, 10); p.line([q0, pol(q0, a_ + 10, 5)], 'z0', only=mane)
    c.stamp(p, 'K')
    p = C()
    p.form(E(HX + 21, HY + 10, 3.4, 4.4), ('r0', 'r1', 'r2'), sd=1, hl=0)                     # ear
    c.stamp(p, 'K')
    p = C()
    p.grid(HX, HY, FACE, LEG)
    c.stamp(p, 'K', skip=('z0', 'z1', 'z2'))

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
