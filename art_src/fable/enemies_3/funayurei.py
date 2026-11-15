"""Funayurei: drowned ghost woman, white burial kimono, long wet hair, wooden ladle (hishaku), no legs."""
from kit import *
import px

NAME = 'funayurei'
CW, CH = 124, 100
OX, OY = 62, 22
WHF = ('v0', 'v1', 'v2')
OBI = ('i0', 'i1', 'i2')

LEG = dict(zip('hHK123WwYZq0', ['h0', 'h2', 'K', 'u1', 'u2', 'u3', 'v3', 'v2', 'y2', 'y3', 'q', 'u0']))
HEAD = """
.....hhhhhhh....
...hhhHhhhhhhh..
..hhHhhhhhhhhhh.
.hhWWWWhHhhhhhhh
.hh3WWW3hhhhhhhh
hh33wW33hhHhhhhh
hh33333hhhhhhhhh
h3KKKK3hhhhHhhhh
h3KYZK2hhhhhhhhh
h33KKK2hhhhhhhhh
h333322hhhhhhhhh
h33qqq2hhhhhhhhh
.h3qqq1hhhhhhhh.
.h32qq1hhhhhhhh.
..h221hhhhhhhhh.
..h.1.hhhhhhhh..
"""
HAND = """
.332.
33321
3K321
3.K2.
"""

DEF = dict(bob=0, lean=0, tail=[(22, 46), (30, 55), (40, 58), (46, 53)], hair=0,
           nhand=(2, 33), fhand=(5, 30), lang=112, llen=20, water=0, drops=(), drip=1, droop=0, tipped=0)


def P(x, y):
    return (x + OX, y + OY)


def sleeve(p, shd, hd, ramp, droop):
    """kimono sleeve: arm tube + a long pouch hanging under the wrist"""
    dx = hd[0] - shd[0]
    pouch = PG([shd, (hd[0] + 1, hd[1] - 3), (hd[0] + 2, hd[1] + 2), (hd[0] + 6 + droop, hd[1] + 14), (hd[0] + 11 + droop, hd[1] + 12),
                (shd[0] + 3, shd[1] + 6), (shd[0] + 3, shd[1] - 2)])
    m = pouch | L(shd[0], shd[1], 3.6, hd[0] + 2, hd[1], 3.0)
    p.form(m, ramp, sd=2, hl=1)
    p.line([(hd[0] + 4, hd[1] + 3), (hd[0] + 8 + droop, hd[1] + 12)], ramp[0], only=m)
    p.line([(shd[0], shd[1] + 3), (hd[0] + 6, hd[1] + 3)], ramp[0], only=m)
    return m


def ghost(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(x, y):
        return P(x + lean, y + bob)

    hs = S['hair']
    # ---- back hair: long wet curtain down the back
    p = C()
    bh = PG([B(18, 6), B(30, 10), B(33 + hs, 26), B(34 + hs * 2, 42), B(31 + hs * 2, 50), B(29 + hs * 2, 43), B(27 + hs * 2, 47), B(24 + hs, 36), B(20, 22)])
    p.form(bh, HAIR, sd=2, hl=0)
    p.line([B(27, 14), B(30 + hs, 28), B(30 + hs * 2, 42)], 'h2', only=bh)
    p.line([B(24, 20), B(27 + hs, 36), B(27 + hs * 2, 44)], 'h0', only=bh)
    c.stamp(p, 'K')

    # ---- far sleeve + hand
    fsh, fh = B(14, 24), B(*S['fhand'])
    p = C(); sleeve(p, fsh, fh, WHF, S['droop']); c.stamp(p, 'K')

    # ---- kimono body tapering into a legless wisp
    p = C()
    tl = [B(20, 30), B(21, 38)] + [P(x, y + bob * 0.5) for x, y in S['tail']]
    sp = spline(tl, 6)
    body = chain(sp, 8.2, 0.8) | L(*B(19, 24), 7.0, *B(20, 33), 8.0)
    p.form(body, WH, sd=4, hl=1)
    for off, cc in ((-3, 'v1'), (1, 'v0'), (4, 'v1')):
        p.line([(x + off * (1 - i / len(sp)), y) for i, (x, y) in enumerate(sp[4:-3])], cc, only=erode(body))
    # collar (right over left: dressed for burial) and obi
    p.line([B(13, 20), B(19, 31)], 'v0', only=body)
    p.line([B(14, 20), B(20, 31)], 'v3', only=body)
    p.line([B(24, 19), B(19, 28)], 'v0', only=body)
    obi = body & (px.Y >= B(0, 33)[1]) & (px.Y <= B(0, 37)[1])
    p.form(obi, OBI, sd=2, hl=1)
    c.stamp(p, 'K')

    # ---- head
    p = C()
    hx, hy = B(8, 2)
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'K')
    # wet front strands hanging over the shoulder and chest
    p = C()
    for pts in ([(20, 16), (21, 24), (20 + hs, 33)], [(23, 16), (25, 26), (25 + hs, 38)], [(11, 16), (10, 22), (11 + hs, 27)]):
        q = [B(*a) for a in pts]
        p.line(q, 'h0')
        p.line([(a + 1, b) for a, b in q[:2]], 'hb')
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))

    # ---- ladle (hishaku): long handle through the near hand, cup at the far end
    nsh, nh = B(17, 25), B(*S['nhand'])
    a = math.radians(S['lang'])
    ux, uy = math.cos(a), -math.sin(a)
    tip = (nh[0] + ux * S['llen'], nh[1] + uy * S['llen'])
    butt = (nh[0] - ux * 7, nh[1] - uy * 7)
    p = C()
    p.form(L(butt[0], butt[1], 1.2, tip[0], tip[1], 1.2), WOOD, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    tx, ty = int(round(tip[0])), int(round(tip[1]))
    if S['tipped']:                       # cup thrown forward: opening faces left, water leaves it
        cup = R(tx - 7, ty - 4, tx - 1, ty + 3)
        p.form(cup, WOOD, sd=2, hl=1)
        p.fill(R(tx - 7, ty - 3, tx - 6, ty + 2), 'a0'); p.fill(R(tx - 7, ty - 3, tx - 7, ty + 2), 'w0')
        p.fill(R(tx - 4, ty - 4, tx - 4, ty + 3), 'w0')
        mouth = (tx - 8, ty)
    else:                                 # upright wooden cup, brim full of sea water
        cup = R(tx - 4, ty - 4, tx + 3, ty + 3)
        p.form(cup, WOOD, sd=2, hl=1)
        p.fill(R(tx - 3, ty - 4, tx + 2, ty - 3), 'a0'); p.fill(R(tx - 3, ty - 4, tx, ty - 4), 'a1')
        p.fill(R(tx - 4, ty, tx + 3, ty), 'w0')
        mouth = (tx - 4, ty - 1)
    c.stamp(p, 'K')
    # ---- near sleeve + hand
    p = C(); sleeve(p, nsh, nh, WH, S['droop']); c.stamp(p, 'K')
    for hd in (fh, nh):
        p = C(); p.grid(hd[0] - 3, hd[1] - 2, HAND, LEG); c.stamp(p, 'u0')
    c.blacken()

    # ---- water
    mo = (int(mouth[0]), int(mouth[1]))
    if S['water']:
        p = C()
        for pts, r0_, r1_ in S['water']:
            q = spline([(mo[0] + x, mo[1] + y) for x, y in pts], 5)
            p.fill(chain(q, r0_, r1_), 'a0')
            p.fill(chain(q[1:-1], max(0.8, r0_ - 1.2), max(0.8, r1_ - 1.4)), 'a1')
            p.line([(x - 1, y - 1) for x, y in q[2:-4]], 'a2', only=p.a == I('a1'))
        for x, y, r in S['drops']:
            p.fill(E(mo[0] + x, mo[1] + y, r, r), 'a1')
            p.fill(E(mo[0] + x - 0.5, mo[1] + y - 0.5, r - 1, r - 1), 'a2')
        c.stamp(p, ring=False)
    if S['drip']:
        d = S['drip']
        c.pxs([(mo[0] - 1, mo[1] + 3 + d), (mo[0] - 1, mo[1] + 4 + d)], 'a1')
        c.pxs([(mo[0] - 1, mo[1] + 5 + d)], 'a2')
        t = P(*S['tail'][-1])
        c.pxs([(t[0] - 6, t[1] + 6 + d), (t[0] - 6, t[1] + 7 + d)], 'a1')
    return c


WALK = [
    dict(bob=0, drip=1),
    dict(bob=-1, hair=1, tail=[(22, 46), (31, 54), (41, 56), (47, 50)], drip=3, droop=1),
    dict(bob=-2, hair=0, tail=[(22, 46), (30, 54), (40, 55), (47, 51)], drip=5),
    dict(bob=-1, hair=-1, tail=[(22, 46), (29, 55), (39, 58), (46, 55)], drip=7, droop=-1),
]
ATTACK = [
    dict(lean=2, bob=-2, nhand=(10, 14), fhand=(7, 18), lang=62, hair=-1, droop=-2, drip=0),
    dict(lean=-4, bob=1, nhand=(-2, 34), fhand=(1, 31), lang=186, llen=18, hair=2, droop=2, drip=0, tipped=1,
         tail=[(22, 46), (32, 53), (43, 54), (50, 48)],
         water=[([(0, 0), (-7, -2), (-14, 3), (-18, 12)], 2.2, 4.2)], drops=[(-23, 17, 2.0), (-14, 19, 1.6), (-24, 6, 1.4), (-8, 9, 1.4), (-19, 23, 1.2)]),
    dict(lean=-2, bob=0, nhand=(0, 37), fhand=(3, 34), lang=160, hair=1, drip=2, tipped=1,
         water=[([(0, 1), (-2, 5), (-3, 10)], 1.6, 1.0)], drops=[(-4, 15, 1.4)]),
]

if __name__ == '__main__':
    export(NAME, ghost, WALK, ATTACK)
