"""Abura-akago: ghost baby that licks lamp oil; arrives as a ball of fire. Floats; spits burning oil."""
from kit import *
import px

NAME = 'abura_akago'
CW, CH = 112, 76
OX, OY = 50, 18
OIL = ('k1', 'k2', 'k3')           # baby skin, slick with oil
OILF = ('k0', 'k1', 'k2')

LEG = dict(zip('KYZqWmMohp', ['K', 'y2', 'y3', 'q', 'b3', 'm2', 'm3', 'y1', 'K', 'm3']))
FACE = """
.............
.............
.KK.....KK...
KYZK...KZYK..
.KK.....KK...
.............
pp.......pp..
.....KK......
...KKqqKK....
..KqmmmmqK...
...KmMmmK....
....KmmK.....
.....KK......
.............
"""
TUFT = """
..h.h..
.hhhhh.
hhhhhhh
"""

DEF = dict(bob=0, lean=0, tail=[(40, 42), (48, 46), (55, 40)], fl=0, hand=(11, 38), dish=1, spit=0, puff=0)


def P(x, y):
    return (x + OX, y + OY)


def baby(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(x, y):
        return P(x + lean, y + bob)

    # ---- fire tail instead of legs
    tl = spline([B(30, 36)] + [P(x, y + bob) for x, y in S['tail']], 6)
    p = C()
    p.fill(chain(tl, 7.0, 0.8), 'e0')
    p.fill(chain(tl[:-4], 5.2, 0.8), 'y1')
    p.fill(chain(tl[:-9], 3.4, 0.8), 'y2')
    # licks of flame peeling off the tail
    t = tl[len(tl) // 2]
    flame(p, (t[0], t[1] - 3), (t[0] + 7, t[1] - 12 + S['fl']), 3.0, FIRE, bend=-2)
    c.stamp(p, ring=False)

    # ---- far arm
    p = C()
    p.form(L(*B(21, 31), 3.0, *B(13, 33), 2.4), OILF, sd=1, hl=0)
    c.stamp(p, 'K')
    # ---- body + bib
    p = C()
    body = E(*B(28, 35), 10.4, 8.6)
    p.form(body, OIL, sd=3, hl=1)
    bx, by_ = B(22, 35)
    bib = PG([(bx - 6, by_ - 6), (bx + 8, by_ - 7), (bx + 7, by_ + 3), (bx, by_ + 9), (bx - 6, by_ + 4)]) & body
    p.form(bib, RD, sd=2, hl=1)
    p.fill(R(bx - 2, by_, bx - 1, by_ + 1), 'y2')
    c.stamp(p, 'K')

    # ---- head: big, bald, with one tuft
    hx, hy = B(15, 19)
    p = C()
    head = E(hx, hy, 12.4, 11.4)
    p.form(head, OIL, sd=4, hl=1)
    p.form(E(hx + 6, hy + 2, 2.2, 3.0), OIL, sd=1, hl=0)            # ear
    p.fill(R(hx - 5, hy - 8, hx - 2, hy - 8), 'b3')                # oily shine
    p.fill(R(hx - 7, hy - 6, hx - 6, hy - 6), 'b3')
    ck = E(hx - 5 - S['puff'], hy + 5, 3.4 + S['puff'], 3.0)       # cheek
    p.form(ck & (head | ck), OIL, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    p.grid(hx - 2, hy - 13, TUFT, LEG)
    c.stamp(p, 'K')
    p = C()
    p.grid(hx - 11, hy - 4, FACE, LEG)
    c.stamp(p, ring=False)

    # ---- near arm + oil dish
    hd = B(*S['hand'])
    if S['dish']:
        p = C()
        dish = PG([(hd[0] - 8, hd[1] - 1), (hd[0] + 2, hd[1] - 1), (hd[0], hd[1] + 2), (hd[0] - 6, hd[1] + 2)])
        p.form(dish, ('i0', 'i1', 'i2'), sd=1, hl=0)
        p.fill(R(hd[0] - 7, hd[1] - 1, hd[0] + 1, hd[1] - 1), 'y1')
        p.fill(R(hd[0] - 6, hd[1] - 1, hd[0] - 4, hd[1] - 1), 'y2')
        c.stamp(p, 'K')
    p = C()
    shd = B(23, 30)
    el = ik(shd, hd, 7.5, 7.5, side=1)
    p.form(chain([shd, el, hd], 2.9, 2.2), OIL, sd=1, hl=1)
    p.form(E(hd[0], hd[1], 2.6, 2.4), OIL, sd=1, hl=1)
    c.stamp(p, 'k0')
    c.blacken()

    # ---- the little flame that hovers over its head
    f = S['fl']
    p = C()
    fb = (hx + 1, hy - 19)
    flame(p, fb, (fb[0] + 1 + f, fb[1] - 10), 3.8, FIRE, bend=1.5 * (1 if f >= 0 else -1))
    p.fill(E(fb[0], fb[1], 3.6, 3.0), 'e0'); p.fill(E(fb[0], fb[1], 2.4, 2.0), 'y1'); p.fill(E(fb[0], fb[1] + 0.5, 1.2, 1.0), 'y3')
    c.stamp(p, ring=False)

    # ---- burning oil
    if S['spit']:
        m0 = (hx - 12, hy + 5)
        p = C()
        for (x, y, r, tx, ty) in S['spit']:
            q = (m0[0] + x, m0[1] + y)
            flame(p, q, (q[0] + tx, q[1] + ty), r, FIRE, bend=1)
            p.fill(E(q[0], q[1], r, r), 'e0'); p.fill(E(q[0], q[1], r - 1.2, r - 1.2), 'y1')
            if r > 2.6:
                p.fill(E(q[0] - 0.5, q[1], r - 2.4, r - 2.4), 'y3')
        c.stamp(p, ring=False)
    return c


WALK = [
    dict(bob=0, fl=0),
    dict(bob=-1, fl=1, tail=[(40, 41), (48, 44), (55, 37)]),
    dict(bob=-2, fl=0, tail=[(40, 42), (49, 43), (56, 38)]),
    dict(bob=-1, fl=-1, tail=[(40, 43), (48, 47), (54, 42)]),
]
ATTACK = [
    dict(lean=3, bob=-1, puff=2, hand=(12, 33), fl=1, tail=[(40, 42), (46, 47), (50, 42)]),
    dict(lean=-3, bob=1, fl=-1, hand=(8, 39), tail=[(41, 41), (50, 43), (58, 37)],
         spit=[(-6, 0, 3.4, 8, -3), (-18, 3, 4.4, 10, -5), (-33, 9, 5.4, 12, -8), (-24, -7, 2.6, 6, -3)]),
    dict(lean=-1, bob=0, fl=0, spit=[(-5, 2, 2.0, 4, -3), (-12, 8, 1.6, 3, -3)]),
]

if __name__ == '__main__':
    export(NAME, baby, WALK, ATTACK)
