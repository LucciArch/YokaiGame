"""Shinigami - death god: floating black hooded robe in tatters, skull face with red eyes, bony hands on a great scythe."""
from kit import *

NAME = 'shinigami'
CW, CH = 184, 148
OX, OY = 66, 32           # local hover line (lowest hem tatter) y=100
ROBE = ('h0', 'h1', 'h2')
BONE = ('b0', 'b1', 'b2')

LEG = dict(zip('KuvwxeZq', ['K', 'b0', 'b1', 'b2', 'b3', 'e1', 'y3', 'q']))
SKULL = """
....vwwwwwv....
..vwxxxwwwwvv..
.vwxxxwwwwwwvu.
.wxxwwwwwwwwvu.
vKKwwwwwwwKKvuu
vKKKKwwwKKKKvuu
vKeZKKwwKeZKKuu
vKKKKKwwKKKKvuu
.vwKKwwKwwKvvu.
.vwwwwKKwwwvuu.
..vwwwwwwwvvu..
..wKwKwKwKwvu..
..vKxKxKxKvuu..
..vwwwwwwwvu...
...vvwwwvvuu...
.....uuuuu.....
"""
HAND = """
..xww..
.xwwvv.
xwKwKvu
wwKwKvu
wwvvvuu
.vvuuu.
"""

DEF = dict(bob=0, sway=0, lean=0, grip=(33, 56), ang=-97, grip2=18, slash=None, head=(0, 0))


def P(x, y):
    return (x + OX, y + OY)


def scythe(c, G, ang, up=52, down=38):
    r_ = math.radians(ang)
    u = (math.cos(r_), math.sin(r_))
    f = (u[1], -u[0])
    T = (G[0] + u[0] * up, G[1] + u[1] * up)
    Bt = (G[0] - u[0] * down, G[1] - u[1] * down)

    def q(a, b):
        return (T[0] + u[0] * a + f[0] * b, T[1] + u[1] * a + f[1] * b)

    def bez(p0, p1, p2, n=14):
        return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
                for t in [i / n for i in range(n + 1)]]
    # shaft
    p = C()
    p.form(L(Bt[0], Bt[1], 1.5, T[0], T[1], 1.5), ('w0', 'w1', 'w2'), sd=1, hl=1)
    for a in (-6, -12):
        m = L(*q(a, 0), 2.1, *q(a - 2, 0), 2.1)
        p.form(m, ('i0', 'i1', 'i2'), sd=1, hl=0)
    p.form(E(Bt[0], Bt[1], 2.2, 2.2), ('i0', 'i1', 'i2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # blade: long crescent, thick spine outside, bright cutting edge inside
    p = C()
    tip = q(-17, 40)
    outer = bez(q(4, -4), q(9, 24), tip)
    inner = bez(q(-6, -3), q(-3, 20), tip)
    blade = PG(outer + inner[::-1])
    p.fill(blade, 'i2')
    spine = tube(outer, 1.6, 0.6) & blade
    p.fill(spine, 'i1')
    edge = tube(inner, 1.1, 0.5) & blade
    p.fill(edge, 'i3')
    p.fill(tube(bez(q(-6, -3), q(-3, 20), tip)[3:9], 0.5, 0.5) & blade, 'v3')
    # nicks + blood-dark stain near the heel
    p.fill(PG([q(4, -4), q(-6, -3), q(-5, -7), q(3, -8)]), 'i1')
    c.stamp(p, 'K')
    return T, tip


def creature(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, sw, lean = S['bob'], S['sway'], S['lean']

    def B(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    G = B(S['grip'])
    r_ = math.radians(S['ang'])
    u = (math.cos(r_), math.sin(r_))
    G2 = (G[0] - u[0] * S['grip2'], G[1] - u[1] * S['grip2'])

    # far sleeve
    p = C()
    fs = B((46, 42))
    m = L(fs[0], fs[1], 5.0, G2[0] + 4, G2[1], 5.6) | PG([(G2[0] + 1, G2[1] + 3), (G2[0] + 9, G2[1] + 2), (G2[0] + 8 + sw, G2[1] + 13)])
    p.form(m, ROBE, sd=3, hl=0)
    c.stamp(p, 'K')

    # robe body: narrow shoulders, long tattered bell that trails back to the right
    p = C()
    hem = [P(34 + sw * 0.5, 84), P(31 + sw, 93), P(38 + sw, 88), P(40 + sw * 1.5, 98), P(46 + sw, 89), P(50 + sw * 1.5, 100), P(55 + sw, 90),
           P(60 + sw * 2, 98), P(64 + sw, 88), P(71 + sw * 2, 95), P(72 + sw, 84), P(80 + sw * 2.5, 86)]
    robe = PG([B((40, 36)), B((62, 34)), B((68, 46)), P(72, 62), P(75 + sw, 76)] + hem[::-1] + [P(35, 70), P(37, 52)])
    p.form(robe, ROBE, sd=6, hl=1)
    # folds: dark creases with a cold light on their left
    for (x0, y0, x1, y1) in ((44, 50, 40, 90), (51, 46, 50, 96), (58, 50, 60, 94), (65, 56, 69, 90)):
        a_, b_ = B((x0, y0)), P(x1 + sw, y1)
        p.line([a_, b_], 'h0', only=erode(robe, 1))
    for (x0, y0, x1, y1) in ((42, 58, 39, 82), (49, 60, 48, 88)):
        a_, b_ = B((x0, y0)), P(x1 + sw, y1)
        p.line([a_, b_], 'h2', only=erode(robe, 2) & (p.a == I('h1')))
    for (x0, y0, x1, y1) in ((56, 62, 57, 86), (63, 66, 66, 84)):
        a_, b_ = B((x0, y0)), P(x1 + sw, y1)
        p.line([a_, b_], 'h2', only=erode(robe, 2) & (p.a == I('h1')))
    # torn holes in the hem
    for (x, y) in ((45, 82), (61, 80)):
        q = P(x + sw, y)
        p.fill(PG([(q[0], q[1]), (q[0] + 2, q[1] + 1), (q[0] + 1, q[1] + 5), (q[0] - 1, q[1] + 3)]) & erode(robe, 2), 'K')
    c.stamp(p, 'K')

    # hood: deep cowl, peak flopping back; skull set in the black opening
    hx, hy = B((37 + S['head'][0], 12 + S['head'][1]))
    p = C()
    hood = E(hx + 9, hy + 9, 13.4, 13.0) | PG([(hx + 6, hy - 4), (hx + 20, hy - 5), (hx + 30, hy + 3), (hx + 26, hy + 6), (hx + 22, hy + 16), (hx + 10, hy + 20)])
    hood |= PG([(hx - 2, hy + 14), (hx + 22, hy + 14), (hx + 27, hy + 27), (hx + 2, hy + 26)])   # mantle over the shoulders
    p.form(hood, ROBE, sd=5, hl=1)
    p.line([(hx + 12, hy - 3), (hx + 21, hy + 2), (hx + 23, hy + 12)], 'h0', only=erode(hood, 1))
    p.line([(hx + 4, hy + 23), (hx + 14, hy + 25), (hx + 24, hy + 23)], 'h0', only=erode(hood, 1))
    opening = E(hx + 7, hy + 9, 9.6, 10.6)
    p.fill(opening & erode(hood, 1), 'K')
    c.stamp(p, 'K')
    p = C()
    p.grid(hx, hy + 1, SKULL, LEG)
    c.stamp(p, ring=False)
    # hood rim casts over the skull top
    c.fill(opening & ~sh(opening, 0, 2) & (c.a != I('K')) & erode(hood, 1), 'b0')

    T, tip = scythe(c, G, S['ang'])

    # near sleeve: wide, drooping cuff
    p = C()
    ns = B((58, 43))
    m = L(ns[0], ns[1], 6.0, G[0] + 5, G[1] + 1, 6.4) | E(ns[0], ns[1], 6.6, 6.2)
    m |= PG([(G[0] + 2, G[1] + 4), (G[0] + 11, G[1] + 3), (G[0] + 12 + sw, G[1] + 17), (G[0] + 8 + sw, G[1] + 12), (G[0] + 6 + sw, G[1] + 15)])
    p.form(m, ROBE, sd=3, hl=1)
    p.line([(ns[0] - 1, ns[1] + 3), (G[0] + 8, G[1] + 3)], 'h0', only=erode(m, 1))
    c.stamp(p, 'K')
    # bony hands on the shaft
    for g in (G2, G):
        p = C()
        p.grid(int(g[0]) - 3, int(g[1]) - 3, HAND, LEG)
        c.stamp(p, 'K')
    c.blacken()
    if S['slash']:
        cx, cy, r, a0, a1 = S['slash']
        qx, qy = P(cx, cy)
        c.fill(arc(qx, qy, r, a0, a1, 3.0) & ~c.m, 'i3')
        c.fill(arc(qx, qy, r + 1, a0 + 6, a1 - 6, 1.2) & ~(c.m & (c.a != I('i3'))), 'v3')
    return c


WALK = [dict(bob=0, sway=0), dict(bob=-1, sway=1, ang=-96), dict(bob=-2, sway=0), dict(bob=-1, sway=-1, ang=-98)]
ATTACK = [
    dict(bob=-2, lean=3, sway=-1, grip=(42, 44), ang=-52, grip2=14, head=(1, -1)),
    dict(bob=1, lean=-5, sway=2, grip=(30, 62), ang=172, grip2=16, head=(-2, 1), slash=(8, 58, 40, 118, 250)),
    dict(bob=0, lean=-2, sway=1, grip=(31, 60), ang=-150, grip2=17, head=(-1, 0)),
]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
