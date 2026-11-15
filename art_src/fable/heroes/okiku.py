"""Okiku - ghost girl of the well: white burial kimono, long black hair over the face, fading legs (floats), plate."""
from herolib import *

NAME = 'okiku'
# pale ghost skin = bone ramp; eye = spirit blue
L_ = dict(LEG, c='b3', b='b2', a='b1', d='b3', A='a2', B='v3', W='v3', w='v2', q='a1', k='b1')
HEAD = """
......mmmmmm.....
....mmnnWnnnmm...
...mnooWWWnnnnm..
..mnonWWWWWnnnnm.
..mnnwwwwwwwnnnm.
.mnnnnnnnnnnnnnnm
.mnnmnnnnnmnnnnnm
.mnnmnccccnmnnnnm
.mnomccckkkcmnnnm
.mnomccKKKKcmnnnm
.mnomccKABbcmnnnm
.mnommcccccbmnnnm
.mnonmccccbbmnnnm
.mnonmcaacbmmnnnm
.mnonnmccbbmnmnnm
.mnonnnmbbmnnmnnm
.mnnnnnnmmnnnmnm.
"""
PLATE = """
..WWWWW..
.WqqqqqW.
WqWWWWWqW
WqWWqWWqW
WqwwwwwqW
.vqqqqqv.
..vvvvv..
"""
PLATE_E = """
.WWWWWWW.
WqqqqqqqW
.vvvvvvv.
"""
GHAND = """
.ccc
cccb
cbcb
c.b.
"""
WISP = """
..A...
.AA...
.ABA..
ABWBA.
ABWWBA
.ABBA.
..AA..
"""
DEF = dict(bob=0, lean=0, nsh=(44, 29), nelb=(40, 37), nwr=(30, 34), hair=0, tail=0, sleeve=0,
           plate=(-11, -8), flying=None, wisp=(56, 22), ffoot=31, nfoot=43)


def okiku(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S)
    c, B, P = g.c, g.B, g.P
    hs, tw = S['hair'], S['tail']

    # ---- hitodama companion flame
    p = C()
    p.grid(*P(*S['wisp']), WISP, dict(A='a1', B='a2', W='v3'))
    c.stamp(p, 'a0')

    # ---- back hair, very long
    p = C()
    tl = PG([B((42, 16)), B((48, 20)), B((52 + hs, 32)), B((54 + hs * 2, 44)), B((53 + hs * 2, 55)), B((50 + hs * 2, 50)),
             B((48 + hs * 2, 56)), B((46 + hs, 46)), B((43, 34))])
    p.form(tl, HAIR, sd=2, hl=0)
    p.line([B((47, 24)), B((50 + hs, 35)), B((51 + hs * 2, 48))], 'h2', only=tl)
    p.line([B((45, 28)), B((47 + hs, 40)), B((48 + hs * 2, 50))], 'h0', only=tl)
    c.stamp(p, 'K')

    # ---- far sleeve (arm reaching forward)
    p = C()
    fs = PG([B((36, 28)), B((28, 31)), B((27, 35)), B((28, 46)), B((34, 45)), B((40, 32))])
    p.form(fs, WHD, sd=2, hl=1)
    c.stamp(p, 'K')

    # ---- kimono body tapering into the fading tail
    p = C()
    up = PG([B((35, 37)), B((46, 37)), B((48, 48)), B((47 + tw, 57)), B((38, 56)), B((33, 48))])
    p.form(up, WH, sd=3, hl=1)
    p.line([B((38, 40)), B((37, 55))], 'v1', only=up)
    p.line([B((42, 40)), B((42 + tw, 56))], 'v1', only=up)
    c.stamp(p, 'K')
    p = C()
    lo = PG([B((37, 53)), B((47 + tw, 54)), B((50 + tw * 2, 60)), P(55 + tw * 3, 66), P(48 + tw * 2, 64), P(42 + tw, 61), B((38, 58))])
    p.fill(lo, 'v1')
    p.fill(lo & (px.Y >= B((0, 58))[1]), 'v0')
    p.fill(lo & (px.Y >= P(0, 62)[1]), 'a0')
    p.fill(lo & (px.Y < B((0, 55))[1]), 'v2')
    c.stamp(p, ring=False)
    p = C()
    p.fill(R(*P(40 + tw, 64), *P(41 + tw, 65)), 'v0'); p.fill(R(*P(45 + tw * 2, 67), *P(46 + tw * 2, 67)), 'a0')
    c.stamp(p, ring=False)

    # obi (dull) + torso, kimono crossed right-over-left like the dead
    p = C()
    torso = L(*B((40, 30)), 5.6, *B((41, 36)), 5.2)
    p.form(torso, WH, sd=2, hl=1)
    p.line([B((44, 26)), B((38, 34))], 'v0', only=torso)
    p.line([B((36, 26)), B((39, 31))], 'v1', only=torso)
    p.form(R(*B((35, 36)), *B((46, 38))), ('v0', 'v1', 'v2'), sd=1, hl=0, only=None)
    c.stamp(p, 'K')
    p = C()
    p.form(R(*B((38, 24)), *B((41, 26))), ('b1', 'b2', 'b3'), sd=1, hl=0)
    c.stamp(p, 'K', ring=False)

    g.head(HEAD, L_, (30, 9))
    # ---- hair curtain falling over the face and chest
    p = C()
    lk = PG([B((31, 22)), B((36, 22)), B((36, 30)), B((35, 37)), B((33, 33)), B((32, 39)), B((31, 31))])
    p.form(lk, HAIR, sd=1, hl=0)
    p.line([B((33, 23)), B((33, 32))], 'h2', only=lk)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))

    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    if S['plate']:
        p = C()
        p.grid(int(wr[0]) + S['plate'][0], int(wr[1]) + S['plate'][1], PLATE, L_)
        c.stamp(p, 'K')
    g.arm(sh_, el, wr, WH, sv=S['sleeve'], bag=14, hand=GHAND, hleg=L_)
    if S['flying']:
        fx, fy, st = S['flying']
        q = B((fx, fy))
        if st:
            p = C()
            p.fill(R(q[0] + 11, q[1], q[0] + 19, q[1]), 'v2'); p.fill(R(q[0] + 12, q[1] + 2, q[0] + 24, q[1] + 2), 'a2')
            c.stamp(p, ring=False)
        p = C(); p.grid(q[0], q[1], PLATE_E, L_); c.stamp(p, 'K')
    return g.done()


WALK = [
    dict(bob=0, hair=0, tail=0, wisp=(56, 22)),
    dict(bob=-1, hair=1, tail=1, sleeve=1, wisp=(56, 21)),
    dict(bob=-2, hair=0, tail=0, wisp=(57, 20)),
    dict(bob=-1, hair=-1, tail=-1, sleeve=-1, wisp=(57, 21)),
]
ATTACK = [
    dict(lean=1, bob=-1, nelb=(50, 31), nwr=(52, 22), plate=(-3, -8), hair=-1, tail=-1),
    dict(lean=-2, bob=0, nelb=(36, 31), nwr=(26, 33), plate=None, flying=(4, 30, True), hair=2, tail=2, sleeve=2),
    dict(lean=-1, bob=-1, nelb=(38, 35), nwr=(29, 35), plate=None, flying=(-20, 29, False), hair=1, tail=1),
]

if __name__ == '__main__':
    build(NAME, okiku, WALK, ATTACK)
