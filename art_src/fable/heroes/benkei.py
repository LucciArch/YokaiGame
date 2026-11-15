"""Benkei - warrior monk (sohei): white head cowl, dark robes, prayer beads, naginata."""
from herolib import *

NAME = 'benkei'
CW, CH, OX, OY = 144, 100, 52, 26
L_ = dict(LEG, W='v3', w='v2', v='v1', V='v0', e='w0', E='v3')
HEAD = """
......vvvvvv......
....vvWWWWwwvv....
...vWWWWwwwwwwv...
..vWWWwwwwwwwwwv..
..vWWwwwwwwwwwwwv.
.vWWwwwwwwwwwwwwv.
.vWwwvvvvvvwwwwwvV
.vwvccccccccvwwwvV
.vcKKccKKKKccvwwvV
.vccKKccKKKKcvwwvV
.vcKEccKeEbbcvwwvV
..ccbcccccbbcvwwvV
..cccbccccbbvwwwvV
..cbaaaacbbvwwwwvV
..vbbccbbbvwwwwwvV
..vwvbbbvvwwwwwwvV
.vwwwvvvwwwwwwwwvV
"""

DEF = dict(bob=0, lean=0, nsh=(47, 30), nelb=(40, 40), nwr=(27, 37), wang=95, grip=27, two=None,
           ffoot=29, nfoot=45, flift=0, nlift=0, sleeve=0, beads=0, glint=False)
POLE = 58


def naginata(g, wr, ang, grip):
    c = g.c
    dx, dy = vec(ang)
    nx, ny = dy, -dx          # edge side
    if ny > 0 or (abs(ny) < 0.2 and nx > 0):
        pass
    b0 = (wr[0] + dx * grip, wr[1] + dy * grip)
    butt = (b0[0] - dx * POLE, b0[1] - dy * POLE)
    p = C()
    p.form(L(*butt, 1.0, *b0, 1.0), WOOD, sd=0, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.form(L(butt[0], butt[1], 1.5, butt[0] + dx * 3, butt[1] + dy * 3, 1.5), IRON, sd=1, hl=0)
    c.stamp(p, 'K')
    # blade: straight back, bellied edge, swept tip
    p = C()
    tip = (b0[0] + dx * 17 - nx * 2.5, b0[1] + dy * 17 - ny * 2.5)
    bl = PG([(b0[0] - nx * 1.0, b0[1] - ny * 1.0), (b0[0] + nx * 1.4, b0[1] + ny * 1.4),
             (b0[0] + dx * 9 + nx * 3.2, b0[1] + dy * 9 + ny * 3.2), (b0[0] + dx * 14 + nx * 1.6, b0[1] + dy * 14 + ny * 1.6), tip,
             (b0[0] + dx * 10 - nx * 1.6, b0[1] + dy * 10 - ny * 1.6)])
    p.form(bl, IRON, sd=1, hl=0)
    p.line([(b0[0] + nx * 1.4, b0[1] + ny * 1.4), (b0[0] + dx * 9 + nx * 3.2, b0[1] + dy * 9 + ny * 3.2),
            (b0[0] + dx * 14 + nx * 1.6, b0[1] + dy * 14 + ny * 1.6), tip], 'v3', only=bl)
    c.stamp(p, 'K')
    p = C()
    p.form(L(b0[0] - dx * 3, b0[1] - dy * 3, 1.6, b0[0], b0[1], 1.6), GOLD, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    p.form(L(b0[0] - dx * 7, b0[1] - dy * 7, 1.3, b0[0] - dx * 5, b0[1] - dy * 5, 1.3), RD, sd=0, hl=0)
    c.stamp(p, 'K')
    return b0, (dx, dy)


def benkei(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S, CW, CH, OX, OY)
    c, B, P = g.c, g.B, g.P

    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    # ---- cowl knot ends behind the head
    for k, pts in enumerate(([(45, 15), (53 + S['sleeve'], 17), (54 + S['sleeve'], 21), (47, 19)], [(45, 17), (51 + S['sleeve'], 23), (49 + S['sleeve'], 26), (45, 21)])):
        p = C()
        p.form(PG([B(q) for q in pts]), WH if k == 0 else WHD, sd=1, hl=1)
        c.stamp(p, 'K')
    # ---- far sleeve
    if not S['two']:
        p = C()
        fs = PG([B((33, 28)), B((29, 33)), B((27, 44)), B((36, 46)), B((39, 30))])
        p.form(fs, ('K', 'i0', 'i1'), sd=2, hl=1)
        c.stamp(p, 'K')

    g.feet('geta')
    # shins (white kyahan) are hidden: full-length pale hakama
    g.hakama(DARK, 'K', waist=(33, 49), wy=39, flare=(29, 52))
    # sash
    p = C()
    p.form(R(*B((33, 37)), *B((49, 40))), ('t0', 't1', 't2'), sd=1, hl=1)
    p.fill(R(*B((33, 39)), *B((49, 39))), 't0')
    c.stamp(p, 'K')

    # ---- torso: dark robe, white inner collar
    p = C()
    torso = L(*B((40, 29)), 8.0, *B((41, 35)), 7.6)
    p.form(torso, DARK, sd=3, hl=1)
    p.line([B((35, 25)), B((39, 34))], 't2', only=torso)
    p.line([B((36, 25)), B((40, 34))], 't1', only=torso)
    p.line([B((45, 25)), B((41, 35)), B((41, 38))], 'K', only=torso)
    c.stamp(p, 'K')

    # ---- cowl mantle over the shoulders
    p = C()
    mt = PG([B((33, 22)), B((47, 21)), B((53, 27)), B((52, 32)), B((46, 30)), B((41, 32)), B((36, 29)), B((30, 31)), B((30, 26))])
    p.form(mt, WH, sd=2, hl=1)
    p.line([B((41, 23)), B((41, 30))], 'v1', only=mt)
    p.line([B((46, 23)), B((48, 29))], 'v1', only=mt)
    c.stamp(p, 'K')

    def far_hand():
        if S['two']:
            dxy = vec(S['wang'])
            fh = (wr[0] + dxy[0] * S['two'], wr[1] + dxy[1] * S['two'])
            p = C()
            fa = L(*B((35, 29)), 3.4, fh[0] + 3, fh[1] - 1, 3.6)
            p.form(fa, ('K', 'i0', 'i1'), sd=2, hl=1)
            c.stamp(p, 'K')
            p = C(); p.grid(int(fh[0]) - 2, int(fh[1]) - 2, HAND, dict(L_, c='k1', d='k2', b='k0')); c.stamp(p, 'K')

    g.head(HEAD, L_, (29, 5), skip=())
    naginata(g, wr, S['wang'], S['grip'])
    far_hand()
    g.arm(sh_, el, wr, DARK, sv=S['sleeve'], bag=11, hleg=L_, upr=(4.8, 4.6))
    # ---- prayer beads: heavy loop round the neck, lying over mantle and chest
    bs = S['beads']
    for k, (bx, by) in enumerate(((32, 28), (33, 32), (35, 36), (39, 38), (43, 36), (46, 33), (48, 29))):
        q = B((bx + (bs if 1 <= k <= 5 else 0), by))
        p = C()
        big = k == 3
        p.fill(R(q[0], q[1], q[0] + 1 + big, q[1] + 1 + big), 'm2' if big else 'y1')
        p.px(q[0], q[1], 'm3' if big else 'y2')
        c.stamp(p, 'K')
    p = C()
    q = B((40 + bs, 41))
    p.fill(R(q[0], q[1], q[0], q[1] + 3), 'm2'); p.fill(R(q[0] - 1, q[1] + 3, q[0] + 1, q[1] + 4), 'm3')
    c.stamp(p, 'K')
    return g.done()


WALK = [
    dict(bob=0, ffoot=25, nfoot=49, sleeve=1, beads=1),
    dict(bob=-1, ffoot=32, nfoot=42, nlift=2),
    dict(bob=0, ffoot=40, nfoot=33, sleeve=-1, beads=-1),
    dict(bob=-1, ffoot=33, flift=2, nfoot=41),
]
ATTACK = [
    dict(lean=2, nelb=(52, 36), nwr=(47, 39), wang=176, grip=24, two=13, ffoot=30, nfoot=47, beads=1),
    dict(lean=-4, bob=1, nelb=(38, 35), nwr=(28, 38), wang=181, grip=40, two=13, ffoot=20, nfoot=50, sleeve=2, beads=-1),
    dict(lean=-2, nelb=(41, 37), nwr=(33, 39), wang=174, grip=34, two=13, ffoot=24, nfoot=48, sleeve=1),
]

if __name__ == '__main__':
    build(NAME, benkei, WALK, ATTACK)
