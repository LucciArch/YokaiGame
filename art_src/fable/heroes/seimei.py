"""Seimei - onmyoji: tall black eboshi hat, white hunting robe (kariginu), ofuda talismans. Attack: talisman throw."""
from herolib import *

NAME = 'seimei'
L_ = dict(LEG, I='K', J='i1', j='i2', H='i0', e='p2', P='b3', p='b2', r='m2')
HEAD = """
.........IIII......
........IJJJJI.....
........IJjJJHI....
.......IJjJJJHI....
.......IJjJJJHHI...
......IJJjJJJJHI...
......IJJJJJJJHI...
.....IJJJJJJJJHHI..
....IHHHHHHHHHHHI..
...mnnnnnnnnnnnnnm.
..mnmnnmnnnmnnnnnm
..mcmccmccmnmnnnnm
..cKKcccKKKKmnnnm.
..cccccccccbmnnnm.
..cKWccKeWbcmnnm..
..ccbcccccbbmnm...
...cccccccbbmm....
...ccaaccbbm......
....bcccbb........
.....bbbb.........
"""
OFUDA = """
PPPP
PrrP
PPrP
PrrP
PrPP
PrrP
PPPP
pppp
"""
OFUDA_H = """
PPPPPPPP
PrPrrPrP
PrrPrrPP
pppppppp
"""

DEF = dict(bob=0, lean=0, nsh=(44, 29), nelb=(39, 38), nwr=(27, 35), ffoot=30, nfoot=45, flift=0, nlift=0,
           hair=0, sleeve=0, fan=True, fly=None, arm_back=False)


def seimei(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S)
    c, B, P = g.c, g.B, g.P
    hs = S['hair']

    # ---- tied hair + hat cords at the back
    p = C()
    tl = PG([B((44, 19)), B((48, 21)), B((50 + hs, 29)), B((49 + hs, 36)), B((47 + hs, 32)), B((45, 27))])
    p.form(tl, HAIR, sd=1, hl=0)
    p.line([B((47, 23)), B((48 + hs, 31))], 'h2', only=tl)
    c.stamp(p, 'K')

    # ---- far sleeve (wide)
    p = C()
    fs = PG([B((36, 28)), B((31, 32)), B((29, 45)), B((37, 47)), B((40, 30))])
    p.form(fs, WHD, sd=2, hl=1)
    p.line([B((29, 44)), B((37, 46))], 'm1', only=fs)
    c.stamp(p, 'K')

    g.feet('dark', strap='i2')
    g.hakama(PUR, 'p0', flare=(31, 50))

    # ---- kariginu: long white front panel over the hakama + belt
    p = C()
    torso = L(*B((40, 30)), 5.8, *B((41, 36)), 5.4)
    fr = PG([B((35, 36)), B((46, 36)), B((47, 47)), B((44, 49)), B((36, 48)), B((34, 45))])
    p.form(torso | fr, WH, sd=2, hl=1)
    p.line([B((40, 37)), B((40, 48))], 'v1', only=fr)
    p.line([B((36, 26)), B((40, 33))], 'p2', only=torso)           # under-robe collar
    p.line([B((37, 26)), B((41, 33))], 'v1', only=torso)
    p.fill(R(*B((35, 37)), *B((46, 38))), 'v0')
    p.fill(R(*B((35, 37)), *B((46, 37))), 'v1')
    c.stamp(p, 'K')
    p = C()
    p.form(R(*B((38, 24)), *B((41, 26))), ('k0', 'k1', 'k2'), sd=1, hl=0)
    c.stamp(p, 'K', ring=False)

    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])

    def near():
        if S['fan']:
            for k, (ox_, oy_) in enumerate(((0, -9), (-4, -10), (-8, -9))):
                p = C()
                p.grid(int(wr[0]) + ox_, int(wr[1]) + oy_ + (k == 1) * -1, OFUDA, L_)
                c.stamp(p, 'K')
        g.arm(sh_, el, wr, WH, sv=S['sleeve'], bag=14, cuff='m2', hleg=L_)
        # shoulder slit of the kariginu shows the purple under-robe
        p = C()
        p.fill(PG([(sh_[0] - 2, sh_[1] - 2), (sh_[0] + 1, sh_[1] - 3), (sh_[0] + 2, sh_[1]), (sh_[0] - 1, sh_[1] + 2)]), 'p2')
        p.fill(R(sh_[0] - 1, sh_[1] - 2, sh_[0], sh_[1] - 2), 'p3')
        c.stamp(p, ring=False)

    if S['arm_back']:
        near()
    g.head(HEAD, L_, (29, 5))
    if not S['arm_back']:
        near()

    if S['fly']:
        for (fx, fy, st) in S['fly']:
            q = B((fx, fy))
            if st:
                p = C()
                p.fill(R(q[0] + 9, q[1], q[0] + 9 + st, q[1]), 'y2'); p.fill(R(q[0] + 9, q[1] + 2, q[0] + 13 + st, q[1] + 2), 'y3')
                c.stamp(p, ring=False)
            p = C(); p.grid(q[0], q[1], OFUDA_H, L_); c.stamp(p, 'K')
    return g.done()


WALK = [
    dict(bob=0, ffoot=26, nfoot=49, hair=1, sleeve=1),
    dict(bob=-1, ffoot=33, nfoot=42, nlift=2, hair=0),
    dict(bob=0, ffoot=40, nfoot=34, hair=1, sleeve=-1),
    dict(bob=-1, ffoot=33, flift=2, nfoot=41, hair=0),
]
ATTACK = [
    dict(lean=1, nelb=(50, 31), nwr=(53, 23), hair=-1, ffoot=31, nfoot=45),
    dict(lean=-2, bob=1, nelb=(36, 31), nwr=(26, 32), fan=False, fly=((6, 21, 5), (0, 30, 8), (7, 39, 5)),
         ffoot=26, nfoot=47, hair=2, sleeve=2),
    dict(lean=-1, nelb=(38, 35), nwr=(29, 34), fan=False, fly=((-14, 16, 0), (-22, 29, 0), (-13, 43, 0)), ffoot=28, nfoot=46, hair=1),
]

if __name__ == '__main__':
    build(NAME, seimei, WALK, ATTACK)
