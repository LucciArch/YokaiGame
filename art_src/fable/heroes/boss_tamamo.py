"""Tamamo-no-Mae (abgeleitet von Kuzunoha): neun goldene Schwänze, höfische Robe. Original: kitsune shrine woman: fox ears, fluffy orange tail with white tip, purple-and-white robes, fox-fire."""
from herolib import *

NAME = 'boss_tamamo'
FUR = ('t0', 't1', 't2')
# hair = fox orange; eyes gold; red eye-liner
L_ = dict(LEG, m='t0', n='t1', o='t2', e='y2', E='y3', i='c2', j='b3', x='m2', k='s0')
HEAD = """
...K.........K..
..KnK.......KoK.
..knik.....kojk.
..knjim...mnjjk.
..mnjinmmmnijnm.
..mnninnnnnnnnnm
..mnoooonnnnnnnm
.mnoonnnnnnnnnnm
.mnnnnnnnnnnnnnnm
.mnmnnmnnnmnnnnnm
.mcmccmccmnmnnnnm
.ckkccckkkcmnnnnm
.cKKccKKKKxmnnnnm
.cKEccKeEbcmnnnnm
..ccbcccccbmnonnm
..cccccccbbnmonnm
...carccbbnm.mnnm
...bcccbbnm..mnm.
....bbba.m...mm..
"""
FLAME = """
...A....
..AA....
..ABA.A.
.ABBAAA.
.ABWBBA.
ABWWWBA.
ABWWWBA.
.ABWBA..
..AAA...
"""
FL = dict(A='a1', B='a2', W='v3', a='a0')
FLAME_S = """
..A..
.AA..
.ABA.
ABWBA
ABWBA
.AAA.
"""
FLAME_L = """
.....A......
....AA......
....ABA..A..
...ABBA.AA..
..ABBBAABA..
..ABBBBBBA..
.ABBWWWBBBA.
.ABWWWWWBBA.
ABBWWWWWWBA.
ABWWWWWWWBA.
ABBWWWWWBBA.
.ABBWWWBBA..
..ABBBBBA...
...AAAAA....
"""

DEF = dict(bob=0, lean=0, nsh=(44, 29), nelb=(38, 36), nwr=(30, 31), ffoot=31, nfoot=43, flift=0, nlift=0,
           hair=0, sleeve=0, tail=0, flame='m', fpos=(-6, -12), sparks=())


def tamamo(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S, cw=150, ch=112, ox=40, oy=36)
    c, B, P = g.c, g.B, g.P
    hs, tw = S['hair'], S['tail']

    # ---- neun Schwänze (hinter allem), aufgefächert um den Ansatz
    import math as _m
    for _k, _ang in enumerate((-62, -46, -30, -15, 0, 14, 28, 42, 56)):
        _ca, _sa = _m.cos(_m.radians(_ang)), _m.sin(_m.radians(_ang))
        _B0 = B

        def B(pt, _ca=_ca, _sa=_sa, _B0=_B0):
            dx, dy = pt[0] - 45, pt[1] - 45
            return _B0((45 + dx * _ca - dy * _sa, 45 + dx * _sa + dy * _ca))
        p = C()
        pts = [(45, 45, 3.0), (52, 49 + tw, 5.2), (59, 46 + tw, 7.0), (63, 37 + tw, 7.2), (63, 27 + tw * 2, 5.4), (61, 19 + tw * 2, 2.6),
               (59, 14 + tw * 2, 0.8)]
        tail = np.zeros((px.H, px.W), bool)
        for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
            tail |= L(*B((x0, y0)), r0, *B((x1, y1)), r1)
        for (tx_, ty_, ex, ey) in ((57, 52, 60, 56), (65, 45, 71, 48), (69, 38, 73, 39), (68, 30, 71, 28)):   # fur tufts, outer edge
            tail |= L(*B((tx_, ty_ + tw)), 2.2, *B((ex, ey + tw)), 0.6)
        p.form(tail, FUR, sd=4, hl=1)
        zy = 31 + tw * 2
        tipm = tail & PG([B((50, 0)), B((76, 0)), B((76, zy + 2)), B((70, zy - 1)), B((67, zy + 3)), B((64, zy)), B((61, zy + 4)),
                          B((58, zy)), B((54, zy + 2)), B((50, zy))])
        p.form(tipm, ('c1', 'b2', 'b3'), sd=3, hl=1)
        for a_, b_ in (((50, 47), (57, 49)), ((56, 44), (62, 41)), ((60, 38), (64, 36))):
            p.line([B((a_[0], a_[1] + tw)), B((b_[0], b_[1] + tw))], 't2', only=tail & ~tipm)
        for a_, b_ in (((55, 52), (62, 50)), ((64, 47), (68, 42))):
            p.line([B((a_[0], a_[1] + tw)), B((b_[0], b_[1] + tw))], 't0', only=tail & ~tipm)
        c.stamp(p, 'K')
        B = _B0


    # ---- back hair, long and loose
    p = C()
    tl = PG([B((43, 18)), B((48, 21)), B((51 + hs, 31)), B((52 + hs * 2, 41)), B((50 + hs * 2, 47)),
             B((48 + hs * 2, 43)), B((46 + hs, 46)), B((45 + hs, 38)), B((43, 30))])
    p.form(tl, FUR, sd=2, hl=0)
    p.line([B((47, 24)), B((49 + hs, 33)), B((50 + hs * 2, 42))], 't2', only=tl)
    p.line([B((45, 28)), B((46 + hs, 36)), B((47 + hs * 2, 43))], 't0', only=tl)
    c.stamp(p, 'K')

    # ---- far sleeve
    p = C()
    fs = PG([B((36, 28)), B((33, 33)), B((31, 43)), B((38, 45)), B((40, 30))])
    p.form(fs, ('p0', 'p1', 'p2'), sd=2, hl=1)
    p.line([B((31, 42)), B((38, 44))], 'v1', only=fs)
    c.stamp(p, 'K')

    g.feet('tabi', strap='p2')
    # ---- long white kimono skirt with purple hem
    p, hk = g.hakama(WH, 'v0', split=False, flare=(33, 48), stamp=False)
    hem = hk & (px.Y >= P(0, 60)[1])
    p.form(hem, PUR, sd=3, hl=0)
    p.fill(hk & (px.Y == P(0, 59)[1]), 'p1')
    c.stamp(p, 'K')
    # purple obi with gold cord
    p = C()
    ob = R(*B((35, 35)), *B((46, 39)))
    p.form(ob, RD, sd=2, hl=1)
    p.fill(R(*B((35, 37)), *B((46, 37))), 'y1')
    c.stamp(p, 'K')

    # ---- torso: white kimono, purple collar
    p = C()
    torso = L(*B((40, 30)), 5.6, *B((41, 35)), 5.2)
    p.form(torso, PUR, sd=2, hl=1)
    p.line([B((36, 26)), B((40, 33))], 'v2', only=torso)
    p.line([B((37, 26)), B((41, 33))], 'v3', only=torso)
    p.line([B((35, 27)), B((39, 34))], 'v1', only=torso)
    p.line([B((44, 26)), B((41, 34))], 'p0', only=torso)
    c.stamp(p, 'K')
    p = C()
    p.form(R(*B((38, 24)), *B((41, 26))), ('k0', 'k1', 'k2'), sd=1, hl=0)
    c.stamp(p, 'K', ring=False)

    g.head(HEAD, L_, (30, 6), skip=('t0', 't1', 't2'))

    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    g.arm(sh_, el, wr, PUR, sv=S['sleeve'], bag=13, cuff='v2', hand=PALM, hleg=L_)

    # ---- fox-fire
    fx, fy = S['fpos']
    grid_ = {'s': FLAME_S, 'm': FLAME, 'l': FLAME_L, None: None}[S['flame']]
    if grid_:
        p = C()
        p.grid(int(wr[0]) + fx, int(wr[1]) + fy, grid_, FL)
        c.stamp(p, 'a0')
    for (sx, sy, k) in S['sparks']:
        p = C()
        p.grid(int(wr[0]) + sx, int(wr[1]) + sy, FLAME_S if k else "\n.A.\nABA\nABA\n.A.\n", FL)
        c.stamp(p, 'a0')
    return g.done()


WALK = [
    dict(bob=0, ffoot=27, nfoot=47, hair=1, sleeve=1, tail=0),
    dict(bob=-1, ffoot=33, nfoot=41, nlift=2, hair=0, tail=-1),
    dict(bob=0, ffoot=39, nfoot=34, hair=1, sleeve=-1, tail=0),
    dict(bob=-1, ffoot=33, flift=2, nfoot=41, hair=0, tail=1),
]
ATTACK = [
    dict(lean=1, nelb=(42, 37), nwr=(36, 29), flame='l', fpos=(-13, -15), hair=-1, tail=-2, ffoot=31, nfoot=45),
    dict(lean=-2, bob=1, nelb=(35, 31), nwr=(25, 31), flame='l', fpos=(-22, -8), sparks=((-11, -12, 1), (-12, 8, 1), (-7, 1, 0)),
         ffoot=27, nfoot=47, hair=2, sleeve=2, tail=2),
    dict(lean=-1, nelb=(37, 34), nwr=(28, 33), flame='s', fpos=(-13, -6), sparks=((-20, 2, 0),), ffoot=29, nfoot=45, hair=1, tail=1),
]

if __name__ == '__main__':
    build(NAME, tamamo, WALK, ATTACK)
