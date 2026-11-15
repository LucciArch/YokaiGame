"""Bake-kujira (~128 px wide): ghostly skeleton whale. Skull = fixed forms (translate only); mandible rotates;
spine, ribs and tail are re-posed from spine control points."""
from k2 import *

NAME = 'boss_bake_kujira'
CW, CH = 192, 160
OX, OY = 36, 70
BN = ('b0', 'b1', 'b2')
BR = ('b0', 'b2', 'b3')
BF = ('s0', 'b0', 'b1')
GH = ('d0', 'd1', 'd2')
FL = ('a0', 'a1', 'a2')

# spine control points relative to the neck joint
SP0 = [(0, 0), (14, -6), (31, -6), (46, 0), (58, 6), (68, 9), (77, 9)]
DEF = dict(dx=0, dy=0, jaw=7, sp=SP0, fl=0, flip=0, burst=0, fph=0)


def whale(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    ox, oy = OX + S['dx'], OY + S['dy']

    def P(x, y):
        return (x + ox, y + oy)
    NECK = P(42, 22)
    sp = curve([add(NECK, q) for q in S['sp']], 10)
    n = len(sp)

    def nrm(t):
        (x, y), (tx, ty) = at(sp, t)
        return (x, y), (ty, -tx)          # normal pointing "up" (dorsal) for a left->right spine

    # ---------- eerie aura: spirit-fire tongues streaming off the back (behind everything)
    f = S['fl']
    for i, (t, ln, w) in enumerate([(0.0, 13, 7), (0.1, 17, 8), (0.21, 14, 7), (0.33, 18, 8), (0.46, 13, 7), (0.6, 15, 7), (0.74, 11, 6), (0.88, 9, 5)]):
        (x, y), (nx, ny) = nrm(t)
        base_ = (x + nx * 4, y + ny * 4)
        k = (1 if (i + S['fph']) % 2 == 0 else -1)
        ang = math.degrees(math.atan2(ny, nx)) + 32 + k * 6
        ln2 = ln + k * 2.5 + S['burst'] * 2
        p = C()
        m = lock(base_, ang, ln2, w, 34 * k)
        p.fill(m, 'a0')
        inner = lock(base_, ang, ln2 - 4, w - 2.6, 34 * k)
        p.fill(inner & m, 'a1')
        p.fill(lock(base_, ang, ln2 - 8, w - 4.6, 34 * k) & m, 'a2')
        c.stamp(p, 'K', skip=('a0', 'a1', 'a2'))

    # ---------- ghost flesh: tattered body the bones glow through
    depth = [(0, 20), (0.15, 30), (0.35, 30), (0.55, 20), (0.75, 9), (0.9, 5), (1, 3)]
    up = [(0, 9), (0.3, 8), (0.6, 6), (0.85, 3.5), (1, 2.5)]
    top_pts, bot_pts = [], []
    K_ = 40
    for i in range(K_ + 1):
        t = i / K_
        (x, y), (nx, ny) = nrm(t)
        u = float(np.interp(t, [k[0] for k in up], [k[1] for k in up]))
        d = float(np.interp(t, [k[0] for k in depth], [k[1] for k in depth]))
        rag = (3.2 if i % 4 == 1 else -1.5 if i % 4 == 3 else 0) * (1 if 0.08 < t < 0.8 else 0)
        top_pts.append((x + nx * u, y + ny * u))
        bot_pts.append((x - nx * (d + rag), y - ny * (d + rag)))
    flesh = PG(top_pts + bot_pts[::-1])
    # head flesh
    flesh |= PG([P(44, 6), P(30, 6), P(12, 12), P(-2, 22), P(0, 29), P(20, 35), P(44, 40), P(50, 20)])
    # flukes
    tail, (tx, ty) = at(sp, 1.0)
    tang = math.degrees(math.atan2(ty, tx))
    fa = S['fl']
    fluke = lock(tail, tang - 52 + fa, 21, 10, 34) | lock(tail, tang + 52 + fa, 19, 9, -34) | E(tail[0], tail[1], 4, 4)
    flesh |= fluke
    # flipper paddle
    (fx, fy), _ = at(sp, 0.2)
    fb = (fx - 2, fy + 22)
    fang = 58 + S['flip']
    paddle = lock(fb, fang, 32, 13, 24)
    p = C()
    p.form(flesh, GH, sd=5, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.form(paddle, GH, sd=3, hl=1)
    c.stamp(p, 'K')
    # fluke bone rays
    for da, ln in ((-64, 13), (-48, 16), (-30, 12), (64, 12), (48, 15), (30, 11)):
        e = pol(tail, tang + da + fa, ln)
        c.line([pol(tail, tang + da + fa, 4), e], 'b0', only=fluke)

    # ---------- far ribs (darker, behind)
    RIBS = [(0.10, 20), (0.16, 25), (0.22, 28), (0.28, 29), (0.34, 28), (0.40, 25), (0.46, 21), (0.52, 17), (0.58, 12)]

    def rib(t, ln, ramp, off=0, r0=1.7):
        (x, y), (nx, ny) = nrm(t)
        x += off
        dnx, dny = -nx, -ny
        txx, tyy = ny, -nx        # toward the tail... (unit tangent)
        txx, tyy = -dny, dnx
        pts = [(x, y), (x + dnx * ln * 0.35 - 4, y + dny * ln * 0.35), (x + dnx * ln * 0.75 - 3, y + dny * ln * 0.75),
               (x + dnx * ln + 2, y + dny * ln + 1)]
        cv = curve(pts, 6)
        p = C()
        p.form(tube(cv, [(0, r0), (0.7, r0 - 0.3), (1, 0.8)]), ramp, sd=1, hl=0)
        c.stamp(p, 'K')

    for t, ln in RIBS:
        rib(t + 0.025, ln - 5, BF, off=2, r0=1.4)

    # ---------- spine: vertebrae + neural spines
    for i in range(0, 30):
        t = i / 29
        (x, y), (nx, ny) = nrm(t)
        sl = float(np.interp(t, [0, 0.3, 0.7, 1], [6.5, 7.5, 4.5, 2]))
        p = C()
        tip = (x + nx * sl + 1.5, y + ny * sl)
        p.form(L(x, y, 1.3, tip[0], tip[1], 0.7), BF, sd=0, hl=0)
        c.stamp(p, 'K')
    p = C()
    spine = tube(sp, [(0, 3.0), (0.5, 2.7), (0.85, 1.7), (1, 1.2)])
    p.form(spine, BN, sd=1, hl=1)
    for i in range(1, 30):
        (x, y), (nx, ny) = nrm(i / 29.5)
        p.line([(x + nx * 4, y + ny * 4), (x - nx * 4, y - ny * 4)], 'b0', only=spine)
    c.stamp(p, 'K')

    # ---------- near ribs
    for t, ln in RIBS:
        rib(t, ln, BR)

    # ---------- flipper bones
    p = C()
    e1 = pol(fb, fang - 8, 9)
    p.form(L(fb[0], fb[1], 2.6, e1[0], e1[1], 2.0), BN, sd=1, hl=1)
    e2 = pol(e1, fang - 2, 8)
    p.form(L(e1[0] + 1, e1[1], 1.5, e2[0] + 1, e2[1], 1.3) | L(e1[0] - 2, e1[1] + 1, 1.5, e2[0] - 2, e2[1] + 1, 1.3), BN, sd=1, hl=0)
    c.stamp(p, 'K')
    for da, ln in ((-16, 12), (-4, 15), (9, 13), (22, 9)):
        a = pol(e2, fang + da, 2)
        b = pol(e2, fang + da + 6, ln)
        mid = lerp(a, b, 0.5)
        c.line([a, lerp(a, b, 0.42)], 'b1', only=paddle)
        c.line([lerp(a, b, 0.58), b], 'b1', only=paddle)

    # ---------- skull
    # far mandible
    HINGE = P(39, 24)

    def J(x, y):
        return rot(P(x, y), HINGE, -S['jaw'])
    p = C()
    cv = curve([J(40, 25), J(28, 32), J(12, 34), J(0, 30)], 8)
    p.form(tube(cv, [(0, 2.6), (0.5, 2.2), (1, 1.4)]), BF, sd=1, hl=0)
    c.stamp(p, 'K')
    # mouth dark between the jaws
    p = C()
    p.fill(PG([HINGE, P(0, 23), J(0, 26), J(20, 29)]), 'K')
    c.stamp(p, ring=False)
    # baleen comb hanging from the upper jaw
    p = C()
    for x in range(3, 30, 3):
        y0 = 21.5 - (x - 3) * 0.2
        p.fill(R(*P(x, y0), *P(x, y0 + 4 + (x % 2))), 'c1')
        p.fill(R(*P(x + 1, y0), *P(x + 1, y0 + 3)), 'c0')
    c.stamp(p, ring=False)
    # near mandible
    p = C()
    cv = curve([J(41, 24), J(29, 30), J(12, 31), J(-3, 26)], 8)
    m = tube(cv, [(0, 3.2), (0.5, 2.6), (1, 1.6)]) | E(*J(41, 23), 4, 4)
    p.form(m, BN, sd=1, hl=1)
    c.stamp(p, 'K')
    # cranium + long arched rostrum (beak)
    p = C()
    cran = E(*P(36, 14), 9.4, 9.0)
    ros = tube(curve([P(32, 11), P(18, 9), P(6, 14), P(-5, 23)], 8), [(0, 5.6), (0.5, 4.2), (1, 1.8)])
    occ = E(*P(43, 20), 5, 5.6)
    sk = cran | ros | occ
    p.form(sk, BN, sd=3, hl=0)
    p.form(cran, BN, sd=3, hl=0)
    # lit top plane (upper-left) + glints
    lit = sk & ~sh(sk, 2, 3)
    p.fill(lit, 'b2')
    p.fill(R(*P(30, 6), *P(35, 6)), 'b3', only=sk)
    p.fill(R(*P(8, 11), *P(13, 11)), 'b3', only=sk)
    # sutures / cracks
    p.line([P(25, 5), P(26, 9), P(24, 13)], 'b0', only=sk)
    p.line([P(39, 5), P(41, 9), P(40, 12), P(43, 14)], 'b0', only=sk)
    p.line([P(10, 15), P(15, 14), P(17, 16)], 'b0', only=sk)
    # blowhole
    p.fill(E(*P(28, 8), 2.2, 1.4), 'K')
    # eye socket (deep, with a bony rim on the lower right)
    p.fill(E(*P(33, 17), 6.2, 5.8), 'b0')
    p.fill(E(*P(33, 17), 5.2, 4.8), 'K')
    c.stamp(p, 'K')
    # glowing eye + wisp trailing back from the socket
    ex, ey = P(33, 17)
    p = C()
    m = lock((ex + 1, ey - 1), 318 + f * 0.3, 12, 4.4, 30)
    p.fill(m, 'a0'); p.fill(erode(m, 1), 'a1')
    c.stamp(p, 'K')
    c.fill(E(ex, ey, 3.4, 3.2), 'a0')
    c.fill(E(ex, ey, 2.5, 2.4), 'a1')
    c.fill(R(ex - 1, ey - 1, ex + 1, ey + 1), 'a2')
    c.fill(R(ex - 1, ey - 1, ex, ey), 'v3')
    if S['burst']:
        for da, ln in ((-75, 18), (-30, 24), (15, 24), (60, 18)):
            b = pol(tail, tang + da, ln)
            flame(c, add(b, (0, 6)), 10 + S['burst'], 6, FL, lean=3, ln='K', core='v3')
    c.blacken()
    return c


def spv(*dy):
    return [(x, y + d) for (x, y), d in zip(SP0, dy)]


WALK = [dict(dy=0, sp=spv(0, 0, 0, 0, 0, 0, 0), fl=0, flip=0, jaw=6),
        dict(dy=-1, sp=spv(0, 0, 1, 2, 0, -4, -8), fl=-14, flip=8, jaw=9, fph=1),
        dict(dy=-2, sp=spv(0, 0, 0, 0, 0, 0, 0), fl=0, flip=14, jaw=6),
        dict(dy=-1, sp=spv(0, 0, -1, -2, 0, 4, 8), fl=14, flip=6, jaw=5, fph=1)]
ATTACK = [dict(dx=4, dy=4, sp=[(0, 0), (14, -8), (30, -14), (43, -22), (53, -33), (60, -44), (65, -53)], fl=-24, flip=-10, jaw=4),
          dict(dx=-8, dy=-6, sp=[(0, 0), (14, -4), (31, 0), (46, 9), (58, 20), (68, 29), (76, 34)], fl=22, flip=24, jaw=24, burst=3, fph=1),
          dict(dx=-3, dy=-2, sp=[(0, 0), (14, -6), (31, -5), (46, 3), (58, 11), (68, 16), (77, 18)], fl=8, flip=12, jaw=12)]

if __name__ == '__main__':
    export(NAME, whale, WALK, ATTACK)
