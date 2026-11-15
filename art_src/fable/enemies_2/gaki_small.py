"""Gaki (small) - hungry ghost child: emaciated grey-green, huge bloated belly, pin neck, sunken glowing eyes."""
from common import *

NAME = 'gaki_small'
CW, CH = 80, 58
OX, OY = 32, 10           # local baseline y = 44
SK = ('u1', 'u2', 'u3')
FAR = ('u0', 'u1', 'u2')

LEG = dict(zip('abcdKEZq', ['u0', 'u1', 'u2', 'u3', 'K', 'e1', 'y3', 'q']))
HEAD = """
.....bbbbbbb......
...bcccccccccb....
..cddccccccccbb...
.cdddccccccccccb..
.cdccccccccccccbb.
cdcccccccccccccbbb
cKKKccccKKKKcccbcb
caaaKKcKKaaaacbbcb
cEZaaacbaaZEaabbbb
caaaabbbaaaaaabba.
.caabcbbbaaaabbba.
.bcaabbbbbcabbba..
.bbqqqqbbbabbba...
..bqqqqabbbbaa....
...baaabbbaaa.....
....bbbbbaa.......
"""

DEF = dict(bob=0, lean=0, head=(0, 0),
           fsh=(15, 23), felb=(10, 28), fwr=(5, 25),
           nsh=(22, 23), nelb=(25, 30), nwr=(21, 36),
           fhip=(19, 34), fknee=(14, 38), fank=(15, 42),
           nhip=(23, 34), nknee=(21, 39), nank=(25, 42),
           air=0)


def P(x, y):
    return (x + OX, y + OY)


def gaki(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, air = S['bob'], S['lean'], S['air']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob - air)

    def G(pt):       # leg points: follow the body only when airborne
        return P(pt[0] + (lean if air else 0), pt[1] - air)

    def arm(s_, e_, w_, ramp):
        s_, e_, w_ = B(s_), B(e_), B(w_)
        p = C()
        p.form(L(*s_, 2.0, *e_, 1.7), ramp, sd=1, hl=1)
        p.form(L(*e_, 1.7, *w_, 1.7), ramp, sd=1, hl=1)
        p.form(E(*e_, 2.0, 2.0), ramp, sd=1, hl=1)                 # knobbly elbow
        # hand: three bony claws fanning toward the wrist direction
        dx, dy = w_[0] - e_[0], w_[1] - e_[1]
        ang = math.atan2(dy, dx)
        for da in (-0.6, 0, 0.6):
            t = (w_[0] + math.cos(ang + da) * 4.2, w_[1] + math.sin(ang + da) * 4.2)
            p.fill(LN([w_, t]), ramp[1])
            p.px(int(round(t[0])), int(round(t[1])), 'b2')
        c.stamp(p, 'u0')

    def leg(h_, k_, a_, ramp):
        h_, k_, a_ = G(h_), G(k_), G(a_)
        p = C()
        p.form(L(*h_, 2.4, *k_, 1.8), ramp, sd=1, hl=1)
        p.form(L(*k_, 1.8, *a_, 1.7), ramp, sd=1, hl=1)
        p.form(E(*k_, 2.2, 2.2), ramp, sd=1, hl=1)                 # knee knob
        foot = PG([(a_[0] + 1, a_[1] - 1), (a_[0] + 2, a_[1] + 2), (a_[0] - 6, a_[1] + 2), (a_[0] - 5, a_[1] + 1), (a_[0] - 2, a_[1] - 1)])
        p.form(foot, ramp, sd=1, hl=1)
        p.pxs([(a_[0] - 6, a_[1] + 2), (a_[0] - 4, a_[1] + 2)], 'b2')
        c.stamp(p, 'u0')

    arm(S['fsh'], S['felb'], S['fwr'], FAR)
    leg(S['fhip'], S['fknee'], S['fank'], FAR)

    # torso: starved ribcage over a drum-tight belly
    p = C()
    chest = L(*B((20, 22)), 4.0, *B((21, 29)), 3.6)
    belly = E(*B((16, 32)), 8.6, 7.0)
    p.form(chest, SK, sd=2, hl=1)
    for i in range(3):                                           # ribs
        p.line([B((15, 22 + i * 2)), B((19, 23 + i * 2)), B((22, 22 + i * 2))], 'u1', only=chest)
    p.line([B((23, 20)), B((24, 24)), B((25, 29))], 'u0', only=chest)   # spine knobs on the back
    c.stamp(p, 'u0')
    p = C()
    p.form(belly, SK, sd=4, hl=1)
    core = belly & ~sh(belly, -2, -2)
    p.a[core & (p.a == I('u1'))] = I('u0')
    p.fill(R(*B((10, 29)), *B((12, 29))), 'u3', only=belly)       # stretched-skin glint
    p.fill(R(*B((9, 33)), *B((10, 34))), 'u1', only=belly)       # popped navel
    p.fill(R(*B((8, 33)), *B((8, 33))), 'u3', only=belly)
    c.stamp(p, 'u0')

    leg(S['nhip'], S['nknee'], S['nank'], SK)

    # pin-thin neck + head
    hx, hy = S['head']
    p = C()
    p.form(L(*B((20, 21)), 1.8, *B((15 + hx, 18 + hy)), 1.7), FAR, sd=1, hl=0)
    c.stamp(p, 'u0')
    p = C()
    H0 = B((2 + hx, 5 + hy))
    # last strands of hair
    for pts in ([(14, 1), (18, 1), (20, 4), (20, 7)],):
        p.line([(H0[0] + a, H0[1] + b_) for a, b_ in pts], 'h1')
    p.grid(H0[0], H0[1], HEAD, LEG)
    # ragged ear
    p.grid(H0[0] + 15, H0[1] + 6, "cc.\ncbc\n.cb\n.bb", LEG)
    c.stamp(p, 'K')

    arm(S['nsh'], S['nelb'], S['nwr'], SK)
    c.blacken()
    return c


WALK = [
    dict(bob=0, fknee=(12, 38), fank=(11, 42), nknee=(23, 39), nank=(28, 42), nelb=(26, 30), nwr=(24, 36), felb=(10, 27), fwr=(4, 24)),
    dict(bob=-1, fknee=(15, 38), fank=(17, 42), nknee=(21, 38), nank=(24, 41)),
    dict(bob=0, fknee=(18, 39), fank=(22, 42), nknee=(18, 39), nank=(17, 42), nelb=(23, 30), nwr=(18, 35), felb=(11, 29), fwr=(6, 27)),
    dict(bob=-1, fknee=(15, 37), fank=(16, 41), nknee=(20, 39), nank=(22, 42)),
]
ATTACK = [
    # crouch: belly sinks, arms cocked back
    dict(bob=3, lean=2, head=(1, 1), felb=(14, 30), fwr=(10, 27), nelb=(25, 29), nwr=(21, 34),
         fknee=(12, 37), fank=(16, 42), nknee=(19, 38), nank=(26, 42)),
    # pounce: airborne, both claws thrown forward, legs trailing
    dict(bob=0, lean=-9, air=6, head=(-2, 1), fsh=(14, 23), felb=(7, 21), fwr=(0, 22), nelb=(13, 27), nwr=(5, 28),
         fhip=(21, 34), fknee=(26, 39), fank=(32, 40), nhip=(24, 34), nknee=(29, 37), nank=(35, 37)),
    # landing
    dict(bob=2, lean=-4, head=(-1, 1), felb=(9, 29), fwr=(3, 30), nelb=(16, 32), nwr=(9, 35),
         fknee=(9, 38), fank=(9, 42), nknee=(18, 39), nank=(22, 42)),
]

if __name__ == '__main__':
    export(NAME, gaki, WALK, ATTACK)
    zoom(NAME)
