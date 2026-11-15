"""Ponpoko - tanuki shapeshifter adventurer: round ears, leaf on head, straw hat on the back, belly, sake gourd."""
from herolib import *

NAME = 'ponpoko'
FUR = ('s1', 's2', 's3')
FURD = ('s0', 's1', 's2')
BEL = ('b1', 'b2', 'b3')
STRAW = ('c0', 'c1', 'c2')
T = dict(A='s0', B='s1', C='s2', D='s3', p='c2', q='c1', M='h0', K='K', W='v3', N='K', g='g2', G='g3', H='g1', y='y2', r='m2')
HEAD = """
.......GGG..............
.....GGgggGG............
....GgggHgggG...........
.....HggHggH............
..AAA..HHH.......AAA....
.ABCBA..CHCCCC..ABCBA...
.ABDCBCCDDDDCCCCCBDCA...
.ABCCDDDDDDDCCCCCCCBA...
..ACDDDDDDCCCCCCCCCCB...
..CDDDDCCCCCCCCCCCCCBA..
..DKKpDCCCCCpKKKpCCCBA..
..pMKKpCCCpMMMKKKKCCCBA.
.pMWWMMpppMMMWWWMMpCCBA.
.pMWKMMpppMMMWKKMMMpCBA.
.ppMMMpppppMMMMMMMMpCBA.
NNNWpppppppppMMMMppCCBA.
NNNNppppppppppppppCCBA..
.NNpppKpppppppppqCCBA...
..qpKKKKKKppppqqCBBA....
...qqqppppppqqqBBA......
.....qqqqqqqqBBAA.......
"""
LEAF = """
..GG...
.GgGGG.
HggggGG
.HggHH.
..HH...
"""
PAW = """
.BB.
BCCB
ACBA
.AA.
"""

DEF = dict(bob=0, lean=0, nsh=(46, 40), nelb=(47, 48), nwr=(40, 51), fwr=(28, 46), ffoot=29, nfoot=41, flift=0, nlift=0,
           tail=0, gourd=0, leaf=None, hold=False, streak=False)


def ponpoko(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S)
    c, B, P = g.c, g.B, g.P
    tw = S['tail']

    # ---- striped tail
    p = C()
    tl = L(*B((50, 57)), 4, *B((58, 54 + tw)), 5.6) | E(*B((59, 53 + tw)), 5.6, 5.2)
    p.form(tl, FUR, sd=3, hl=1)
    for k in (53, 57, 61):
        p.line([B((k, 46 + tw)), B((k + 3, 62 + tw))], 's0', only=tl)
        p.line([B((k + 1, 46 + tw)), B((k + 4, 62 + tw))], 's0', only=tl)
    c.stamp(p, 'K')

    # ---- conical straw hat hanging on the back (point to the rear)
    p = C()
    hat = E(*B((50, 40)), 4.4, 13.4) | PG([B((50, 27)), B((61, 39)), B((61, 41)), B((50, 53))])
    p.form(hat, STRAW, sd=3, hl=1)
    for k in (3, 7):
        p.line([B((50 + k, 30 + k)), B((51 + k, 40)), B((50 + k, 50 - k))], 'c0', only=hat)
    p.line([B((47, 40)), B((60, 40))], 'c2', only=hat)
    p.line([B((47, 33)), B((60, 39))], 'c0', only=hat)
    p.line([B((47, 47)), B((60, 41))], 'c0', only=hat)
    c.stamp(p, 'K')

    # ---- far arm
    p = C()
    fw = B(S['fwr'])
    p.form(L(*B((35, 40)), 3, fw[0] + 1, fw[1], 2.6), FURD, sd=1, hl=1)
    p.form(E(fw[0], fw[1], 2.6, 2.6), ('K', 's0', 's1'), sd=1, hl=0)
    c.stamp(p, 'K')

    def leg(w_):
        fx, lift = S[w_ + 'foot'], S[w_ + 'lift']
        p = C()
        x0, y0 = P(fx, 66 - lift)
        hip = B((38 if w_ == 'f' else 44, 58))
        p.form(L(hip[0], hip[1], 5, x0 + 5, y0 - 1, 3.2), FURD if w_ == 'f' else FUR, sd=2, hl=1)
        foot = PG([(x0, y0 + 1), (x0 + 2, y0 - 1), (x0 + 8, y0 - 1), (x0 + 8, y0 + 3), (x0, y0 + 3)])
        p.form(foot, ('K', 's0', 's1'), sd=1, hl=1)
        p.pxs([(x0 + 1, y0 + 3), (x0 + 3, y0 + 3)], 's0')
        c.stamp(p, 'K')

    leg('f')
    # ---- body
    p = C()
    body = E(*B((40, 42)), 9.4, 9.4) | E(*B((40, 51)), 11.4, 12.4)
    p.form(body, FUR, sd=4, hl=1)
    c.stamp(p, 'K')
    leg('n')
    # belly patch
    p = C()
    bel = E(*B((35.5, 51)), 7.4, 10.4) & body
    p.form(bel, BEL, sd=3, hl=1)
    p.fill(R(*B((33, 56)), *B((34, 56))), 'b1')            # navel
    c.stamp(p, 's1')
    # ---- indigo travel vest on the back / shoulder
    p = C()
    vest = body & PG([B((40, 34)), B((52, 34)), B((52, 55)), B((46, 56)), B((43, 46)), B((41, 40))])
    p.form(vest, BLU, sd=3, hl=0)
    p.line([B((41, 36)), B((42, 41)), B((44, 47)), B((46, 55))], 'v2', only=vest)
    c.stamp(p, 'K')
    # rope belt + sake gourd on the hip
    gs = S['gourd']
    p = C()
    p.line([B((31, 55)), B((36, 58)), B((44, 58)), B((49, 56))], 'm2', only=body)
    c.stamp(p, ring=False)
    p = C()
    gx, gy = B((30 + gs, 60))
    gd = E(gx, gy + 3, 3.6, 3.8) | E(gx, gy - 2, 2.4, 2.4)
    p.form(gd, ('t0', 't1', 't2'), sd=2, hl=1)
    p.fill(R(gx - 1, gy - 5, gx, gy - 4), 'c2')
    p.fill(R(gx - 2, gy, gx + 2, gy), 'm2', only=gd)
    p.pxs([(gx - 2, gy + 2), (gx - 2, gy + 3)], 'y2')
    c.stamp(p, 'K')
    p = C(); p.line([B((31, 55)), (gx, gy - 5)], 'm2'); c.stamp(p, ring=False)

    # hat cord across the chest
    p = C(); p.line([B((36, 36)), B((46, 37))], 'm2', only=body); c.stamp(p, ring=False)

    # ---- head
    p = C()
    p.grid(*B((22, 13)), HEAD, T)
    c.stamp(p, 'K', skip=())

    # ---- near arm
    sh_, wr = B(S['nsh']), B(S['nwr'])
    if S['hold']:
        p = C(); p.grid(int(wr[0]) - 5, int(wr[1]) - 6, LEAF, T); c.stamp(p, 'K')
    el = B(S['nelb']) if S['nelb'] else None
    p = C()
    if el:
        am = L(*sh_, 3.6, *el, 3.2) | L(*el, 3.2, wr[0] + 1, wr[1], 2.8)
    else:
        am = L(*sh_, 3.6, wr[0] + 1, wr[1], 2.8)
    p.form(am, FUR, sd=2, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.form(E(wr[0], wr[1], 2.9, 2.9), ('K', 's0', 's1'), sd=1, hl=1)
    c.stamp(p, 'K')

    if S['leaf']:
        lx, ly = B(S['leaf'])
        if S['streak']:
            p = C()
            p.fill(R(lx + 9, ly + 1, lx + 16, ly + 1), 'g3'); p.fill(R(lx + 10, ly + 3, lx + 20, ly + 3), 'g4')
            p.fill(R(lx + 9, ly + 5, lx + 14, ly + 5), 'g3')
            c.stamp(p, ring=False)
        p = C(); p.grid(lx, ly, LEAF, T); c.stamp(p, 'K')
    return g.done()


WALK = [
    dict(bob=0, ffoot=25, nfoot=45, tail=0, gourd=1, nelb=(48, 48), nwr=(43, 52), fwr=(26, 45)),
    dict(bob=-1, ffoot=31, nfoot=40, nlift=2, tail=-1, gourd=0),
    dict(bob=0, ffoot=38, nfoot=31, tail=0, gourd=-1, nelb=(45, 48), nwr=(37, 50), fwr=(31, 47)),
    dict(bob=-1, ffoot=32, flift=2, nfoot=39, tail=1, gourd=0),
]
ATTACK = [
    dict(lean=1, nsh=(46, 39), nelb=(53, 38), nwr=(55, 29), hold=True, tail=-1, gourd=1),
    dict(lean=-2, bob=1, nsh=(44, 40), nelb=None, nwr=(30, 40), leaf=(6, 33), streak=True, ffoot=26, nfoot=43, tail=2, gourd=-1, fwr=(31, 47)),
    dict(lean=-1, nelb=(42, 46), nwr=(34, 45), leaf=(-18, 32), streak=False, ffoot=28, nfoot=42, tail=1),
]

if __name__ == '__main__':
    build(NAME, ponpoko, WALK, ATTACK)
