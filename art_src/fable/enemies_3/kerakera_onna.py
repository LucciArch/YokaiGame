"""Kerakera-onna: giant cackling woman in a gaudy pink kimono; her laughter rolls out as a shockwave."""
from kit import *
import px

NAME = 'kerakera_onna'
CW, CH = 136, 116
OX, OY = 62, 12            # local baseline y=98
PINKF = ('n0', 'n1', 'n2')
GOLD = ('y0', 'y1', 'y2')

LEG = dict(zip('0123hHoKRZWwmMqtTyY', ['k0', 'k1', 'k2', 'k3', 'h0', 'hb', 'h2', 'K', 'e1', 'y3', 'v3', 'v2', 'm2', 'm3', 'q', 'm1', 'm2', 'y1', 'y2']))
FACE = """
.......hhhhhhhhhhhh....
.....hhhHHhhhhhhhhhhh..
...hhh3333hhhHhhhhhhhh.
..hh333333333hhhhhhhhhh
..h3333KK33333hhhhHhhhh
.h33333KK3333KK3hhhhhhh
.333333333333KK32hhhhhh
.33333333333333222hhhhh
.3KKKKKK333KKKKKK2hhhhh
.33KRRZK2233KRRZK21hhhh
.333KKK223333KKK221hhhh
33333322233333322211hhh
33333222333333222211hhh
.3322K22333332222211hhh
"""
MOUTH_A = """
..mmmmmmmmmmmmmm2211hhh
.mKKKKKKKKKKKKKKm211hhh
mKWwWwWwWwWwWwWqKm11hhh
mKqWqWqWqWqWqWqqKm11hhh
mKqqqqqqqqqqqqqqKm11hhh
mKqqtttttttttqqqKm11hh.
mKqtTTTTTTTTttqqKm11hh.
.mKqtttttttttqqKm211hh.
.mKWqWqWqWqWqqKm2211h..
..mKKKKKKKKKKKm22211...
...mmmmmmmmmmm222110...
....33333322222110.....
.....222222211100......
"""
MOUTH_B = """
..mmmmmmmmmmmmmm2211hhh
.mKKKKKKKKKKKKKKm211hhh
mKWwWwWwWwWwWwWqKm11hhh
mKWqWqWqWqWqWqWqKm11hhh
mKqqqqqqqqqqqqqqKm11hhh
mKqqqqqqqqqqqqqqKm11hhh
mKqqqqqqqqqqqqqqKm11hh.
mKqqqttttttttqqqKm11hh.
mKqqtTTTTTTTTtqqKm11hh.
mKqtTTTTTTTTTTtqKm11hh.
mKqtTTTTTTTTTttqKm11hh.
.mKqtttttttttqqKm211hh.
.mKWqWqWqWqWqWKm2211h..
.mKWwWwWwWwWwWKm2211...
..mKKKKKKKKKKKm22211...
...mmmmmmmmmmm222110...
....33333322222110.....
.....222222211100......
"""
HAND = """
..3.3.3..
.33232323
.32323232
.33333322
..3333221
...33221.
"""
COMB = """
.yYYYy.
yYYYYYy
yKyKyKy
"""

DEF = dict(bob=0, head=(0, 0), mouth='A', hair=0, hand=(4, 52), elbow=(26, 64), ffoot=0, nfoot=0, sway=0, rings=())


def P(x, y):
    return (x + OX, y + OY)


def onna(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob = S['bob']
    hdx, hdy = S['head']
    hs, sw = S['hair'], S['sway']

    def B(x, y):
        return P(x, y + bob)

    def Hd(x, y):
        return P(x + hdx, y + hdy + bob)

    # ---- back hair: heavy black curtain to the hips
    p = C()
    bh = PG([Hd(34, 8), Hd(48, 14), B(54 + hs, 40), B(58 + hs * 2, 66), B(55 + hs * 2, 84), B(51 + hs * 2, 74), B(49 + hs * 2, 86), B(45 + hs, 70),
             B(43 + hs, 78), B(40, 56), Hd(34, 40)])
    bh |= E(*Hd(34, 22), 15.4, 16.4)
    p.form(bh, HAIR, sd=3, hl=0)
    for a_, b_, cc in (((44, 14), (51, 70), 'h2'), ((40, 30), (46, 72), 'h0'), ((48, 24), (55, 76), 'h0'), ((38, 12), (44, 40), 'h2')):
        p.line([Hd(*a_), B(b_[0] + hs * 2, b_[1])], cc, only=erode(bh))
    c.stamp(p, 'K')

    # ---- tabi peeking under the hem
    for fx in (16 + S['ffoot'], 28 + S['nfoot']):
        p = C()
        x0, y0 = P(fx, 98)
        p.form(PG([(x0, y0 - 1), (x0 + 2, y0 - 3), (x0 + 8, y0 - 3), (x0 + 8, y0), (x0, y0)]), WH, sd=1, hl=0)
        c.stamp(p, 'K')

    # ---- far sleeve hanging in front
    p = C()
    fs = PG([B(18, 48), B(11, 56), B(8 + sw, 80), B(20 + sw, 83), B(22, 56)])
    p.form(fs, PINKF, sd=3, hl=1)
    p.line([B(14, 58), B(13 + sw, 80)], 'n0', only=fs)
    c.stamp(p, 'K')

    # ---- kimono body
    p = C()
    body = PG([B(18, 45), B(42, 44), B(45, 58), B(44, 70), P(48, 97), P(11, 97), P(9, 94), B(17, 70), B(17, 58)])
    p.form(body, PINK, sd=6, hl=1)
    for a_, b_, cc in (((22, 70), (16, 96), 'n1'), ((28, 70), (25, 96), 'n1'), ((34, 70), (35, 96), 'n0'), ((39, 70), (42, 96), 'n0'),
                       ((25, 71), (21, 92), 'n3')):
        p.line([B(*a_), P(*b_)], cc, only=body)
    # scattered blossoms
    for (qx, qy) in ((20, 80), (31, 88), (27, 76), (38, 82), (14, 90)):
        q = B(qx, qy)
        p.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 'n3', only=body & (p.a != I('n1')))
        p.fill(R(q[0], q[1], q[0], q[1]), 'v3', only=body & (p.a == I('n3')))
    # hem lining
    hem = body & ~sh(body, 0, -2) & (px.Y > P(0, 93)[1])
    p.a[hem] = I('m2')
    # white collar
    p.fill(PG([B(20, 44), B(30, 44), B(26, 56)]), 'v2', only=body)
    p.line([B(20, 44), B(26, 57)], 'v0', only=body)
    p.line([B(32, 44), B(26, 57)], 'n0', only=body)
    p.line([B(31, 44), B(26, 55)], 'v3', only=body)
    # obi
    obi = body & (px.Y >= B(0, 58)[1]) & (px.Y <= B(0, 69)[1])
    p.form(obi, GOLD, sd=4, hl=1)
    p.fill(obi & (px.Y >= B(0, 63)[1]) & (px.Y <= B(0, 64)[1]), 'm2')
    p.fill(obi & (px.Y == B(0, 58)[1]), 'y0'); p.fill(obi & (px.Y == B(0, 69)[1]), 'y0')
    c.stamp(p, 'K')

    # ---- head
    hx, hy = Hd(10, 6)
    p = C()
    p.grid(hx, hy, FACE, LEG)
    p.grid(hx, hy + 14, MOUTH_A if S['mouth'] == 'A' else MOUTH_B, LEG)
    c.stamp(p, 'K')
    p = C()
    p.grid(hx + 15, hy - 3, COMB, LEG)
    c.stamp(p, 'K')
    # neck shadow under the jaw
    # ---- near arm: sleeve lifted, back of the hand toward the mouth
    shd, el, hd = B(38, 47), B(*S['elbow']), B(*S['hand'])
    p = C()
    slv = PG([shd, (shd[0] + 4, shd[1] + 4), (el[0] + 4, el[1] + 3), (el[0] + 2 + sw, el[1] + 22), (el[0] - 12 + sw, el[1] + 20), (hd[0] + 4, hd[1] + 6),
              (hd[0] + 3, hd[1]), (el[0] - 6, el[1] - 4), (shd[0] - 6, shd[1] + 1)])
    p.form(slv, PINK, sd=4, hl=1)
    p.line([(hd[0] + 5, hd[1] + 5), (el[0] - 6 + sw, el[1] + 18)], 'n1', only=slv)
    p.line([(el[0] - 1, el[1] + 2), (el[0] - 2 + sw, el[1] + 20)], 'n1', only=slv)
    p.line([(shd[0] - 2, shd[1] + 3), (el[0] - 2, el[1] - 1)], 'n3', only=slv)
    low = slv & ~sh(slv, 0, -2) & (px.Y > el[1] + 12)
    p.a[low] = I('m2')
    q = (el[0] - 5 + sw, el[1] + 12)
    p.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 'n3', only=slv); p.fill(R(q[0], q[1], q[0], q[1]), 'v3', only=slv)
    c.stamp(p, 'K')
    p = C()
    p.grid(hd[0] - 4, hd[1] - 3, HAND, LEG)
    c.stamp(p, 'k0')
    c.blacken()

    # ---- laughter: rolling rings of sound
    if S['rings']:
        mx, my = hx - 2, hy + 21
        p = C()
        for r, a0, a1 in S['rings']:
            for rr, cc in ((r, 'n3'), (r + 1, 'v3'), (r + 2, 'n2')):
                pts = [(mx - math.cos(math.radians(a)) * rr, my + math.sin(math.radians(a)) * rr) for a in range(a0, a1 + 1, 4)]
                p.line(pts, cc)
        c.stamp(p, ring=False)
    return c


WALK = [
    dict(bob=0, ffoot=-3, nfoot=2, sway=1, hair=0),
    dict(bob=-1, ffoot=0, nfoot=0, sway=0, hair=1, head=(0, -1)),
    dict(bob=0, ffoot=2, nfoot=-3, sway=-1, hair=0),
    dict(bob=-1, ffoot=0, nfoot=0, sway=0, hair=-1, head=(0, -1)),
]
ATTACK = [
    dict(head=(4, -3), hand=(10, 58), elbow=(28, 68), hair=-1, sway=-1),
    dict(head=(-5, 2), mouth='B', hand=(-2, 62), elbow=(22, 66), hair=2, sway=2, bob=1,
         rings=((12, -40, 40), (22, -34, 34), (32, -28, 28))),
    dict(head=(-2, 1), mouth='B', hand=(2, 56), hair=1, rings=((40, -16, 16), (48, -10, 10))),
]

if __name__ == '__main__':
    export(NAME, onna, WALK, ATTACK, review=3)
