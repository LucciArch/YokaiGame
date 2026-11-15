"""Kamikiri - the hair-cutter: hunched dusk-skinned imp with a bird beak and scissor blades for hands, trailing stolen hair."""
from common import *

NAME = 'kamikiri'
CW, CH = 124, 84
OX, OY = 44, 18           # local baseline y = 60
SK = ('d1', 'd2', 'd3')
FAR = ('d0', 'd1', 'd2')
CLOTH = ('m0', 'm1', 'm2')

LEG = dict(zip('abcduvwKYZq', ['d0', 'd1', 'd2', 'd3', 'b0', 'b1', 'b2', 'K', 'e1', 'y3', 'q']))
HEAD = """
..............bbbbb.....
............bcccccccb...
..........bcddcccccccb..
.........bcdccccccccccb.
........bccKKKKKcccccbb.
......bKKKKKKccccccccbbb
.....vvaaYZYKacccccbbbb.
..vvwwvvaaYYaaccccbbbba.
vwwwwwwwvvaaaacccbbbba..
uvvvvwwwwwvvbcccbbbbaa..
.uuuKKKKKKKuvbbbbbaa....
....uuvvvvvuubbaaa......
.......uuuu..aa.........
"""

DEF = dict(bob=0, lean=0,
           fsh=(33, 33), felb=(26, 41), fwr=(17, 41), fdeg=6, fopen=36,
           nsh=(40, 33), nelb=(34, 45), nwr=(25, 48), ndeg=-4, nopen=34,
           fknee=(30, 52), fank=(33, 57), nknee=(38, 53), nank=(42, 57),
           hank=True, cut=0, swing=0)


def P(x, y):
    return (x + OX, y + OY)


def scissor(c, wr, deg, opn, ln=17):
    """a pair of shears hinged at the wrist; deg 0 = left, 90 = up; opn = gape in degrees.
    The finger loops sit behind the rivet so the silhouette reads as scissors, not claws."""
    for a in (deg - opn / 2, deg + opn / 2):                   # loops (behind)
        q = pol(wr, -4.0, a + (a - deg) * 1.2)
        p = C()
        ring = E(q[0], q[1], 2.6, 2.6)
        p.fill(ring, 'i1'); p.fill(ring & ~sh(ring, 1, 1), 'i2')
        c.stamp(p, 'K')
        c.fill(E(q[0], q[1], 0.9, 0.9), 'K')
    for k, a in enumerate((deg - opn / 2, deg + opn / 2)):
        t = pol(wr, ln, a)
        p = C()
        m = L(wr[0], wr[1], 2.3, t[0], t[1], 0.6)
        p.fill(m, 'i2')
        p.fill(m & ~sh(m, 0, 1), 'i3')                         # lit upper edge
        p.fill(LN([lerp(wr, t, 0.2), lerp(wr, t, 0.8)]), 'v3' if k else 'i3', only=m)
        p.fill(m & ~sh(m, 0, -1) & ~sh(m, -1, 0), 'i1')        # underside
        c.stamp(p, 'K')
    p = C()
    p.fill(E(wr[0], wr[1], 1.6, 1.6), 'y1'); p.px(int(wr[0]), int(wr[1]), 'y3')   # brass rivet
    c.stamp(p, 'K')


def kamikiri(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    def arm(s_, e_, w_, deg, opn, ramp):
        s_, e_, w_ = B(s_), B(e_), B(w_)
        p = C()
        p.form(L(*e_, 2.2, *w_, 1.9), ramp, sd=1, hl=1)
        c.stamp(p, 'd0')
        p = C()
        p.form(L(*s_, 2.8, *e_, 2.2), ramp, sd=1, hl=1)
        p.form(E(*s_, 3.4, 3.2), ramp, sd=1, hl=1)
        p.form(E(*e_, 2.5, 2.5), ramp, sd=1, hl=1)             # bony elbow
        c.stamp(p, 'd0')
        scissor(c, w_, deg, opn)

    def leg(hip, knee, ank, ramp):
        h_, k_, a_ = P(hip[0] + lean * 0.5, hip[1] + bob), P(*knee), P(*ank)
        p = C()
        p.form(L(*h_, 3.6, *k_, 2.4), ramp, sd=2, hl=1)
        p.form(L(*k_, 2.2, *a_, 1.7), ramp, sd=1, hl=1)
        for dx_ in (-6, -3, 0):                                # three-toed bird foot
            p.fill(LN([(a_[0], a_[1] + 1), (a_[0] + dx_, a_[1] + 3)]), ramp[1])
            p.px(a_[0] + dx_ - 1, a_[1] + 3, 'b2')
        p.fill(LN([(a_[0], a_[1] + 1), (a_[0] + 3, a_[1] + 3)]), ramp[0])
        c.stamp(p, 'd0')

    arm(S['fsh'], S['felb'], S['fwr'], S['fdeg'], S['fopen'], FAR)
    leg((37, 46), S['fknee'], S['fank'], FAR)

    # ---- torso: hunched, ridge of spines down the back, ragged red wrap
    p = C()
    torso = L(*B((37, 33)), 6.2, *P(40 + lean * 0.5, 45 + bob), 6.0)
    p.form(torso, SK, sd=3, hl=1)
    for i in range(4):                                          # knobbly spine
        q = B((43 + (i > 0) + (i > 2) * 0, 29 + i * 4)); p.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 'd1', only=torso)
    for i in range(3):
        p.line([B((33, 36 + i * 3)), B((37, 37 + i * 3))], 'd1', only=torso)      # ribs
    c.stamp(p, 'd0')
    p = C()
    wrap = PG([P(33 + lean * 0.5, 43 + bob), P(47 + lean * 0.5, 42 + bob), P(49, 50), P(45, 48), P(43, 53), P(39, 49), P(36, 52), P(32, 48)])
    p.form(wrap, CLOTH, sd=2, hl=1)
    p.fill(wrap & (px.Y <= P(0, 44 + bob)[1]), 'c1')                               # rope belt
    c.stamp(p, 'K')

    leg((42, 46), S['nknee'], S['nank'], SK)

    # ---- head: thin neck, crest of quills, fixed face grid
    p = C()
    p.form(L(*B((36, 29)), 2.6, *B((31, 23)), 2.4), FAR, sd=1, hl=0)
    c.stamp(p, 'd0')
    hx, hy = B((9, 12))
    p = C()
    for (x, y, dx_, dy_) in [(17, 1, 3, -5), (20, 2, 5, -4), (22, 4, 6, -2), (22, 7, 6, 1)]:
        p.form(PG([(hx + x - 2, hy + y + 2), (hx + x + dx_, hy + y + dy_), (hx + x + 1, hy + y + 4)]), ('h0', 'h1', 'h2'), sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'K')

    # ---- stolen hair: a severed topknot clamped in the beak, still tied with its paper cord
    if S['hank']:
        sw = S['swing']
        p = C()
        top = (hx + 2, hy + 13)
        hk = wisp([top, (top[0] + sw * 0.4, top[1] + 4), (top[0] + sw, top[1] + 8), (top[0] + sw * 1.6 - 1, top[1] + 12)], 2.0, 0.9) \
            | wisp([(top[0] + 1, top[1] + 3), (top[0] + 2 + sw, top[1] + 7), (top[0] + 3 + sw * 1.5, top[1] + 10)], 1.6, 0.9)
        p.form(hk, ('h0', 'h1', 'h2'), sd=1, hl=1)
        p.fill(R(top[0] - 2, top[1] + 1, top[0] + 2, top[1] + 2), 'v2', only=hk)
        c.stamp(p, 'K')

    arm(S['nsh'], S['nelb'], S['nwr'], S['ndeg'], S['nopen'], SK)

    # ---- snipped hair flying (strike)
    for k in range(S['cut']):
        q = B((6 - k * 5, 30 + (k * 7) % 11))
        c.line([q, (q[0] - 3, q[1] + 1), (q[0] - 5, q[1] + 3)], 'h1')
        c.line([(q[0], q[1] + 1), (q[0] - 3, q[1] + 2)], 'h2')

    c.blacken()
    return c


WALK = [
    dict(bob=0, fknee=(27, 52), fank=(27, 57), nknee=(40, 53), nank=(46, 57), nopen=34, fopen=20),
    dict(bob=-1, fknee=(31, 51), fank=(34, 57), nknee=(38, 52), nank=(41, 56), nopen=10, fopen=38, swing=1),
    dict(bob=0, fknee=(35, 52), fank=(40, 57), nknee=(33, 53), nank=(32, 57), nopen=34, fopen=20),
    dict(bob=-1, fknee=(32, 51), fank=(35, 56), nknee=(37, 53), nank=(40, 57), nopen=10, fopen=38, swing=-1),
]
ATTACK = [
    dict(lean=3, bob=-1, swing=-2, felb=(27, 27), fwr=(21, 20), fdeg=50, fopen=80, nelb=(40, 43), nwr=(31, 40), ndeg=8, nopen=80),
    dict(lean=-7, bob=2, felb=(22, 33), fwr=(11, 31), fdeg=4, fopen=4, nelb=(28, 39), nwr=(16, 38), ndeg=-2, nopen=4, cut=3, swing=3,
         fknee=(26, 52), fank=(26, 57), nknee=(40, 53), nank=(45, 57)),
    dict(lean=-3, bob=1, swing=1, felb=(24, 37), fwr=(15, 37), fdeg=-8, fopen=24, nelb=(32, 44), nwr=(22, 46), ndeg=-14, nopen=20,
         fknee=(28, 52), fank=(29, 57)),
]

if __name__ == '__main__':
    export(NAME, kamikiri, WALK, ATTACK)
    zoom(NAME, 6)
