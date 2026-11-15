"""Akago - demon baby: red skin, small horn, bib, oversized head but menacing. Attack: tantrum shockwave."""
from herolib import *

NAME = 'akago'
SK = ('r1', 'r2', 'r3')
FAR = ('r0', 'r1', 'r2')
PELT = ('t0', 't1', 't2')
A_ = dict(zip('abcdeKYZqxwvmno', ['r0', 'r1', 'r2', 'r3', 'r4', 'K', 'y2', 'y3', 'q', 'b3', 'b2', 'b1', 'h0', 'h1', 'h2']))
HEAD = """
........x.................
.......xw.................
.......wwv...mm...........
......xwvv.mmnnmm.........
......wwvvmnnonnnm........
....ccwvvcmnonnnnmcc......
...cdddccccmnnnmcccccc....
..cddeeddccccmmcccccccb...
.cddeedddcccccccccccccbb..
.cdddddddccccccccccccccb..
cdddddddcccccccccccccccbb.
cddKKddccccccKKKccccccccb.
cdddKKKdccKKKKKcccccccccbb
cdaKKKKaccaKKKKKaccccccbbb
cdaYZKaacccaYYZKaaccccbbbb
cddaaadccccdaaaaaccccbbbba
.cdddddcbcccccccccccbbbbba
.cdeedcbbccccccccccbbbbba.
.cKKKKKKKKKKKccccbbbbbbba.
..KxqqxqqqxqKccbbbbbbbba..
..cKqqqqqqqKcbbbbbbbbba...
...cKKKKKKKbbbbbbbbbaa....
....cccbbbbbbbbbaaaa......
......bbbbaaaaaa..........
"""
FIST = """
.cdc.
cddcb
cacbb
ccbba
.bba.
"""
DEF = dict(bob=0, lean=0, nsh=(46, 44), nwr=(40, 52), fsh=(34, 44), fwr=(28, 50), ffoot=30, nfoot=42, flift=0, nlift=0,
           head=(0, 0), wave=None, bib=0)


def akago(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S)
    c, B, P = g.c, g.B, g.P

    def arm(sh_, wr, ramp):
        p = C()
        p.form(L(*sh_, 3.6, *wr, 3.2), ramp, sd=2, hl=1)
        c.stamp(p, 'r0')
        p = C()
        p.grid(int(wr[0]) - 3, int(wr[1]) - 2, FIST, A_ if ramp is SK else dict(A_, d='r2', c='r1', b='r0', a='r0'))
        c.stamp(p, 'r0')

    def leg(w_, ramp):
        fx, lift = S[w_ + 'foot'], S[w_ + 'lift']
        x0, y0 = P(fx, 66 - lift)
        hip = B((37 if w_ == 'f' else 44, 57))
        p = C()
        p.form(L(hip[0], hip[1], 4.6, x0 + 5, y0 - 2, 3.6), ramp, sd=2, hl=1)
        foot = PG([(x0, y0 + 1), (x0 + 2, y0 - 2), (x0 + 8, y0 - 2), (x0 + 8, y0 + 3), (x0, y0 + 3)])
        p.form(foot, ramp, sd=1, hl=1)
        p.pxs([(x0, y0 + 3), (x0 + 2, y0 + 3), (x0 + 4, y0 + 3)], 'b2')
        c.stamp(p, 'r0')

    arm(B(S['fsh']), B(S['fwr']), FAR)
    leg('f', FAR)
    # ---- chubby torso
    p = C()
    body = E(*B((41, 47)), 8.6, 9.0)
    p.form(body, SK, sd=3, hl=1)
    c.stamp(p, 'r0')
    leg('n', SK)
    # ---- tiger-pelt nappy
    p = C()
    nap = E(*B((41, 55)), 9.2, 5.6) & (px.Y >= B((0, 52))[1])
    p.form(nap, PELT, sd=2, hl=1)
    for k in (35, 39, 43, 47):
        p.fill(PG([B((k, 52)), B((k + 2, 52)), B((k + 1, 57))]), 'K', only=nap)
    c.stamp(p, 'K')
    # ---- bib
    bb = S['bib']
    p = C()
    bib = PG([B((30, 37)), B((40, 38)), B((41 + bb, 46)), B((38 + bb, 50)), B((33 + bb, 50)), B((30 + bb, 46))])
    p.form(bib, WH, sd=2, hl=1)
    p.fill(bib & ~sh(bib, 1, -1) | bib & ~sh(bib, -1, -1), 'm2')
    p.fill(R(*B((35 + bb, 43)), *B((36 + bb, 45))), 'm2'); p.fill(R(*B((34 + bb, 44)), *B((37 + bb, 44))), 'm2')
    c.stamp(p, 'K')

    # ---- head
    hx, hy = S['head']
    p = C()
    p.grid(*B((25 + hx, 14 + hy)), HEAD, A_)
    c.stamp(p, 'K', skip=())

    arm(B(S['nsh']), B(S['nwr']), SK)

    if S['wave']:
        cx, cy, rings, bits = S['wave']
        q = P(cx, cy)
        p = C()
        for (r, a0, a1, w_) in rings:
            m = arc(q[0], q[1], r - w_, r, a0, a1, taper=False) & (px.Y <= P(0, 69)[1])
            p.fill(m, 'e1')
            p.fill(arc(q[0], q[1], r - w_ + 1, r - 1, a0, a1, taper=False) & m, 'y3')
        for (bx, by) in bits:
            qq = P(bx, by)
            p.fill(R(qq[0], qq[1], qq[0] + 1, qq[1] + 1), 'y2')
        c.stamp(p, ring=False)
    return g.done()


WALK = [
    dict(bob=0, ffoot=26, nfoot=45, nwr=(43, 52), fwr=(26, 49), bib=1),
    dict(bob=-1, ffoot=31, nfoot=40, nlift=2, head=(0, 0)),
    dict(bob=0, ffoot=37, nfoot=32, nwr=(37, 51), fwr=(31, 51), bib=-1),
    dict(bob=-1, ffoot=31, flift=2, nfoot=40),
]
ATTACK = [
    dict(lean=1, bob=-1, nsh=(47, 42), nwr=(52, 33), fsh=(35, 42), fwr=(27, 33), head=(1, -1), ffoot=29, nfoot=43),
    dict(lean=-2, bob=2, nsh=(45, 46), nwr=(37, 61), fsh=(33, 46), fwr=(27, 60), head=(-1, 1), ffoot=27, nfoot=44, bib=1,
         wave=(31, 69, ((15, 15, 165, 4), (26, 100, 172, 4), (26, 8, 75, 4)), ((8, 50), (54, 52), (20, 40), (2, 62)))),
    dict(lean=-1, bob=0, nwr=(40, 55), fwr=(27, 54), ffoot=28, nfoot=43,
         wave=(31, 69, ((33, 128, 172, 3), (33, 102, 120, 2), (33, 10, 42, 3), (42, 152, 172, 2)), ((-4, 48), (64, 46), (12, 36)))),
]

if __name__ == '__main__':
    build(NAME, akago, WALK, ATTACK)
