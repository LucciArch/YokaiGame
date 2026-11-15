"""Tenome - blind old man (murdered zato) in grey robes; his eyes sit in the palms of his raised, groping hands."""
from common import *

NAME = 'tenome'
CW, CH = 156, 90
OX, OY = 74, 20           # local baseline y = 64
ROBE = ('j1', 'j2', 'j3')
ROBF = ('j0', 'j1', 'j2')
SK = ('l1', 'l2', 'l3')

LEG = dict(zip('abcdKqwhWYZ', ['l0', 'l1', 'l2', 'l3', 'K', 'q', 'b2', 'v2', 'v3', 'y2', 'e0']))
# bald, wrinkled, eyeless: smooth sunken sockets under bristling brows, slack toothless mouth, thin beard
HEAD = """
......bcccccb.....
....bcddcccccbb...
...cdddcccccccbb..
..cddcccccccccccb.
..cdccccccccccccb.
.ccccccccccccccbbb
.hhhcccchhhhhccbcb
.aKKhhchhKKKaacbcb
.caaaKacKaaaaacbcb
.ccbaaccbaaabccbbb
ccccccdcbbcccbbbb.
cdcccdcbbbbccbbba.
.ccabbabbbbbbbba..
..cKKKKKKbbbbba...
..cKqqqqKabbba....
...KqqwqKabba.....
...aKKKKabbb......
....aabbbba.......
....hhhhaa........
.....hh.h.........
"""
# open palm turned toward the enemy, fingers splayed, a living eye in the middle (looks left)
PALM = """
...c.c....
.c.c.c.c..
.c.c.c.c..
.c.c.c.c..
.ccccccc..
cccccccccc
cdKKKKKKcb
cKYZKWWWKb
cKYYKWWWKb
ccKKKKKKbb
.cbbbbbbb.
..bbbbbb..
"""

DEF = dict(bob=0, lean=0,
           fsh=(34, 32), felb=(24, 33), fwr=(11, 25),
           nsh=(41, 33), nelb=(31, 41), nwr=(19, 39),
           toe=(31, 38), hem=0, beam=0, glow=False)


def P(x, y):
    return (x + OX, y + OY)


def tenome(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    def hand(w_):
        p = C()
        p.grid(int(w_[0]) - 5, int(w_[1]) - 12, PALM, LEG)
        if S['glow']:
            p.fill(R(int(w_[0]) - 3, int(w_[1]) - 5, int(w_[0]) - 2, int(w_[1]) - 4), 'y3')
        c.stamp(p, 'K')

    def arm(s_, e_, w_, ramp):
        s_, e_, w_ = B(s_), B(e_), B(w_)
        p = C()                                                    # bare forearm
        p.form(L(*e_, 2.2, w_[0], w_[1] - 1, 1.9), SK if ramp is ROBE else ('l0', 'l1', 'l2'), sd=1, hl=1)
        c.stamp(p, 'l0')
        hand(w_)
        p = C()                                                    # wide sleeve, mouth hanging open below the elbow
        m = lerp(e_, w_, 0.35)
        sl = L(*s_, 4.6, *e_, 4.4) | PG([(e_[0] - 3, e_[1] - 4), (m[0] - 2, m[1] - 3), (m[0] + 1, m[1] + 9), (e_[0] + 5, e_[1] + 8), (e_[0] + 5, e_[1])])
        p.form(sl, ramp, sd=2, hl=1)
        p.line([(e_[0] + 1, e_[1]), (m[0] + 1, m[1] + 7)], ramp[0], only=sl)
        c.stamp(p, 'K')

    def beam(w_):
        w_ = B(w_)
        ex, ey = int(w_[0]) - 3, int(w_[1]) - 5
        ln = S['beam']
        c.fill(R(ex - ln, ey - 1, ex - 3, ey + 2) & ~c.m, 'y2')
        c.fill(R(ex - ln + 3, ey, ex - 3, ey + 1) & ~c.m, 'y3')
        c.fill(R(ex - ln - 4, ey, ex - ln - 1, ey + 1) & ~c.m, 'y1')
        c.fill(R(ex - ln + 6, ey - 2, ex - ln + 14, ey - 2) & ~c.m, 'y1')
        c.fill(R(ex - ln + 20, ey + 3, ex - ln + 27, ey + 3) & ~c.m, 'y1')
        fl = E(ex - 3, ey + 0.5, 3.4, 3.4) & ~c.m
        c.fill(fl, 'y2')

    arm(S['fsh'], S['felb'], S['fwr'], ROBF)

    # ---- toes shuffling out from under the hem
    for i, tx in enumerate(S['toe']):
        p = C()
        t = P(tx, 63)
        p.form(R(t[0] - 4, t[1] - 2, t[0] + 2, t[1]), ('l0', 'l1', 'l2') if i == 0 else SK, sd=1, hl=1)
        p.pxs([(t[0] - 4, t[1]), (t[0] - 2, t[1])], 'l3')
        c.stamp(p, 'l0')

    # ---- robe: bent back, long skirt
    p = C()
    h = S['hem']
    back = L(*B((40, 32)), 8.0, *P(43 + lean * 0.4, 48), 9.0)
    skirt = PG([P(33 + lean * 0.4, 46), P(52 + lean * 0.4, 44), P(57 + h, 61), P(50, 62), P(44, 60), P(38, 62), P(32, 60), P(28 - h, 61), P(30, 52)])
    robe = back | skirt
    p.form(robe, ROBE, sd=5, hl=1)
    core = robe & ~sh(robe, -2, -2)
    p.a[core & (p.a == I('j1'))] = I('j0')
    for a_, b_ in (((37, 48), (33, 60)), ((43, 48), (42, 60)), ((49, 47), (52, 60))):
        p.line([P(a_[0] + lean * 0.4, a_[1]), P(*b_)], 'j1', only=robe & (p.a == I('j2')))
    p.line([B((33, 30)), B((38, 39)), P(38 + lean * 0.4, 47)], 'j3', only=robe)                  # lapel
    p.line([B((34, 30)), B((39, 39)), P(39 + lean * 0.4, 47)], 'j0', only=robe)
    sash = robe & (px.Y >= P(0, 46)[1]) & (px.Y <= P(0, 48)[1]) & (px.X < P(53 + lean * 0.4, 0)[0])
    p.form(sash, ('n0', 'n1', 'n2'), sd=1, hl=1)
    c.stamp(p, 'K')

    # ---- head
    p = C()
    p.form(L(*B((36, 29)), 2.6, *B((33, 24)), 2.4), ('l0', 'l1', 'l2'), sd=1, hl=0)
    c.stamp(p, 'l0')
    p = C()
    hx, hy = B((20, 7))
    p.grid(hx, hy, HEAD, LEG)
    p.grid(hx + 15, hy + 7, "cc.\ncbc\ncbc\n.cb\n.bb", LEG)                                       # long ear
    c.stamp(p, 'K')

    arm(S['nsh'], S['nelb'], S['nwr'], ROBE)

    if S['beam']:
        beam(S['fwr']); beam(S['nwr'])

    c.blacken()
    return c


WALK = [
    dict(bob=0, toe=(28, 40), hem=1, fwr=(10, 25), nwr=(20, 40)),
    dict(bob=-1, toe=(32, 38), hem=0),
    dict(bob=0, toe=(36, 33), hem=-1, fwr=(12, 26), nwr=(18, 38)),
    dict(bob=-1, toe=(33, 37), hem=0),
]
ATTACK = [
    dict(lean=3, bob=-1, felb=(25, 27), fwr=(13, 15), nelb=(32, 38), nwr=(19, 30), glow=True),
    dict(lean=-4, bob=1, felb=(21, 31), fwr=(9, 27), nelb=(28, 40), nwr=(15, 40), glow=True, beam=44, toe=(27, 38), hem=1),
    dict(lean=-2, bob=1, felb=(24, 35), fwr=(12, 29), nelb=(31, 42), nwr=(19, 42), toe=(29, 38)),
]

if __name__ == '__main__':
    export(NAME, tenome, WALK, ATTACK)
    zoom(NAME, 6)
