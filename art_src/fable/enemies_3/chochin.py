"""Chochin-obake: torn paper lantern, one eye, split mouth glowing from inside, long tongue. Floats."""
from kit import *
import px

NAME = 'chochin'
CW, CH = 100, 80
OX, OY = 50, 14            # local hover rest: lowest body point ~y=50
PAPER = ('c0', 'c1', 'c2')
LAQ = ('i0', 'i1', 'i2')

LEG = dict(zip('KWwvRrYZq', ['K', 'v3', 'v2', 'v1', 'e1', 'e0', 'y2', 'y3', 'q']))
EYE = """
KK...........
KKKKKK.......
.KKKKKKKKKK..
.KwWWKKKKKKKK
KwWWYYYWWwKKK
KwWYYKYYWwwvK
KwWYRKRYWwwvK
KwWYYKZYWwvvK
.KwWYYYWwvvK.
..KvwwwvvvK..
...KKKKKKK...
"""
CX, CY, RX, RY = 24, 27, 15.4, 18.4
MY = 31                     # mouth line
HINGE = 35

DEF = dict(bob=0, gape=5, lean=0, tongue=[(-3, 3), (-6, 9), (-5, 15), (-2, 19)], fire=0, flick=0, drip=0)


def P(x, y):
    return (x + OX, y + OY)


def chochin(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    g = S['gape']
    ox, oy = P(S['lean'], S['bob'])
    Xl, Yl = px.X - ox, px.Y - oy                       # local coords
    k = np.clip((HINGE - Xl) / (HINGE - 9.0), 0, 1.3)   # 0 at the hinge, 1 at the lips
    Yt = Yl + g * k                                     # upper half lifts
    Yb = Yl - g * 0.35 * k                              # lower jaw drops a little
    zig = np.abs(((Xl + 2) % 6) - 3) - 1.5              # torn zig-zag edge
    top = (((Xl - CX) / RX) ** 2 + ((Yt - CY) / RY) ** 2 <= 1) & (Yt < MY + zig)
    bot = (((Xl - CX) / RX) ** 2 + ((Yb - CY) / RY) ** 2 <= 1) & (Yb >= MY + zig + 1)
    hull = dil(dil(top | bot))
    inner = (((Xl - CX - 1) / (RX - 1.5)) ** 2 + ((Yl - CY - 2) / (RY - 2)) ** 2 <= 1)
    # close the hull vertically between halves
    span = np.zeros_like(top)
    ty = np.where(top.any(0), top.shape[0] - 1 - top[::-1].argmax(0), -1)
    byy = np.where(bot.any(0), bot.argmax(0), 10 ** 6)
    for x in range(px.W):
        if ty[x] >= 0 and byy[x] < 10 ** 6 and byy[x] > ty[x]:
            span[ty[x]:byy[x], x] = True

    # ---- tongue (far back first so the lower lip overlaps its root)
    lip = (ox + 13, oy + MY + 2 + int(g * 0.3))
    sp = spline([(lip[0] + 6, lip[1] - 1), lip] + [(lip[0] + x, lip[1] + y) for x, y in S['tongue']], 6)
    # ---- inside glow
    p = C()
    glow = span & (Xl < HINGE + 1)
    p.fill(glow, 'y1')
    p.fill(glow & (Xl > HINGE - 6), 'e0')
    fl = (oy + MY - g * 0.3)
    core = E(ox + CX - 5, fl, 9.5, max(1.5, g * 0.6)) & erode(glow, 1)
    p.fill(core, 'y2')
    p.fill(E(ox + CX - 6, fl, 4.5, max(0.8, g * 0.3)) & core, 'y3')
    c.stamp(p, 'K')
    p = C()
    tm = chain(sp, 2.8, 1.5)
    p.form(tm, RD, sd=1, hl=0)
    k_ = len(sp) // 2
    p.line([(x - 1, y - 1) for x, y in sp[k_:k_ + 4]], 'm3', only=erode(tm))
    c.stamp(p, 'K')

    # ---- paper halves
    for half, Yh in ((bot, Yb), (top, Yt)):
        p = C()
        p.form(half, PAPER, sd=5, hl=2)
        # warm light bleeding through the paper next to the torn edge
        nearm = half & (np.abs(Yh - MY) < 3.2) & (Xl < HINGE - 2)
        p.a[nearm & (p.a == I('c1'))] = I('c2')
        p.a[nearm & (p.a == I('c0'))] = I('t1')
        # bamboo ribs
        for ry_ in range(-12, 16, 4):
            rm = half & (np.round(Yh + ((Xl - CX) / RX) ** 2 * 1.5) == CY + ry_) & (np.abs(Yh - MY) >= 3)
            p.a[rm & (p.a == I('c0'))] = I('w1')
            p.a[rm & (p.a != I('w1'))] = I('c0')
        # holes burnt through on the shadow side
        if half is top:
            hm = PG([(ox + 31, oy + 17 - g * 0.1), (ox + 34, oy + 16 - g * 0.1), (ox + 35, oy + 21), (ox + 32, oy + 20)]) & half
            p.fill(hm, 'y1'); p.fill(erode(hm), 'y2')
        else:
            hm = PG([(ox + 27, oy + 38), (ox + 31, oy + 37), (ox + 30, oy + 41)]) & half
            p.fill(hm, 'y1')
        c.stamp(p, 'K')

    # ---- lacquer caps + handle
    tyo = oy - int(round(g * 0.25))
    p = C()
    hd = [(ox + 18, tyo + 8), (ox + 19, tyo + 3), (ox + 24, tyo + 0), (ox + 29, tyo + 3), (ox + 30, tyo + 8)]
    p.line(hd, 'i2')
    c.stamp(p, 'K')
    p = C()
    p.form(R(ox + 16, tyo + 7, ox + 32, tyo + 10), LAQ, sd=2, hl=1)
    p.fill(R(ox + 18, tyo + 8, ox + 22, tyo + 8), 'i3')
    c.stamp(p, 'K')
    p = C()
    byo = oy + int(round(g * 0.1))
    p.form(R(ox + 17, byo + 44, ox + 31, byo + 47), LAQ, sd=2, hl=1)
    c.stamp(p, 'K')
    # red silk tassel under the bottom ring
    d = S['drip']
    p = C()
    p.fill(R(ox + 23, byo + 48, ox + 25, byo + 49), 'y1'); p.fill(R(ox + 23, byo + 48, ox + 24, byo + 48), 'y2')
    ts = PG([(ox + 22, byo + 50), (ox + 26, byo + 50), (ox + 27 + d, byo + 56), (ox + 25 + d, byo + 55), (ox + 24 + d, byo + 57), (ox + 22 + d, byo + 55)])
    p.form(ts, RD, sd=1, hl=0)
    p.line([(ox + 24, byo + 51), (ox + 24 + d, byo + 55)], 'm1', only=ts)
    c.stamp(p, 'K')

    # ---- eye (rides on the upper half)
    p = C()
    p.grid(ox + 10, oy + 15 - int(round(g * 0.72)), EYE, LEG)
    c.stamp(p, ring=False)
    c.blacken()

    # ---- fire breath (drawn after outlining: fire keeps its own red edge)
    if S['fire']:
        f = S['fire']
        p = C()
        m0 = (ox + 12, oy + MY - g * 0.2)
        fk = S['flick']
        if f >= 2:
            flame(p, (m0[0] + 2, m0[1] - 3), (m0[0] - 30, m0[1] - 10 + fk), 5.0, FIRE, bend=3)
            flame(p, (m0[0] + 2, m0[1] + 3), (m0[0] - 34, m0[1] + 9 - fk), 5.0, FIRE, bend=-3)
            flame(p, (m0[0] + 4, m0[1]), (m0[0] - 44, m0[1] + 1), 7.0, FIRE, bend=1)
            p.fill(chain([(m0[0] + 2, m0[1]), (m0[0] - 22, m0[1])], 2.6, 0.8), 'y3')
            for q in ((-38, -9), (-41, 10), (-26, -15)):
                p.fill(E(m0[0] + q[0], m0[1] + q[1], 1.3, 1.3), 'y1')
        else:
            flame(p, (m0[0] + 3, m0[1]), (m0[0] - 9, m0[1] - 7), 3.2, FIRE, bend=2)
            flame(p, (m0[0] + 3, m0[1] + 1), (m0[0] - 12, m0[1] + 2), 2.8, FIRE, bend=-1)
            p.fill(E(m0[0] - 19, m0[1] - 6, 1.3, 1.3), 'y1')
        c.stamp(p, ring=False)
    return c


WALK = [
    dict(bob=0, gape=5, drip=0),
    dict(bob=-1, gape=6, drip=1, tongue=[(-3, 3), (-7, 8), (-7, 14), (-4, 19)]),
    dict(bob=-2, gape=5, drip=0, tongue=[(-3, 3), (-7, 9), (-8, 15), (-6, 20)]),
    dict(bob=-1, gape=4, drip=-1, tongue=[(-3, 3), (-6, 9), (-6, 15), (-3, 20)]),
]
ATTACK = [
    dict(lean=3, bob=-1, gape=1, tongue=[(-2, 2), (-3, 6), (-1, 9)], drip=-1),
    dict(lean=-3, bob=1, gape=13, fire=2, tongue=[(-3, 3), (-4, 9), (-1, 14), (2, 18)], drip=1),
    dict(lean=-1, bob=0, gape=8, fire=1, tongue=[(-3, 3), (-6, 9), (-5, 15), (-2, 19)]),
]

if __name__ == '__main__':
    export(NAME, chochin, WALK, ATTACK)
