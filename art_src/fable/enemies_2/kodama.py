"""Kodama - tree spirit. Small pale mossy humanoid, lumpy round head with three hollow holes."""
from common import *

NAME = 'kodama'
CW, CH = 64, 54
OX, OY = 24, 9            # local baseline y = 40
WH = ('v1', 'v2', 'v3')
WF = ('v0', 'v1', 'v2')
MOSS = ('g0', 'g1', 'g2')

LEG = dict(zip('Kh', ['K', 'h1']))
# three hollow holes; near eye (right) larger, far eye narrower, mouth low and off-centre. Same grid in every walk frame.
HOLES = """
.KK.....KKK.
KKKK...KKKKK
KKKK...KKKKK
KKK....KKKKK
.K......KKK.
.K.......K..
.........K..
...KKK......
..KKKKK.....
..KKKKK.....
...K.K......
"""
# attack: the rattle - holes gape and the whole mask of the face skews
HOLES_WIDE = """
.KKK.....KKK.
KKKKK...KKKKK
KKKKK..KKKKKK
KKKKK..KKKKKK
.KKK...KKKKKK
..K.....KKKK.
..K......KK..
...KKKK...K..
..KKKKKK.....
..KKKKKK.....
..KKKKKK.....
..KKKKKK.....
...K.KK......
"""

DEF = dict(bob=0, head=(0, 0), wide=False, tilt=0,
           fsh=(14, 26), fhand=(7, 32), nsh=(21, 26), nhand=(15, 35),
           ffoot=(12, 39), nfoot=(19, 39), rattle=0)


def P(x, y):
    return (x + OX, y + OY)


def kodama(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    b = S['bob']

    def B(pt):
        return P(pt[0], pt[1] + b)

    def arm(a, h, ramp):
        p = C()
        a_, h_ = B(a), B(h)
        p.form(L(a_[0], a_[1], 2.0, h_[0], h_[1], 1.7), ramp, sd=1, hl=1)
        # three stubby twig fingers
        dx = -1 if h[0] <= a[0] else 1
        p.fill(R(h_[0] + dx * 2 - 1, h_[1] - 2, h_[0] + dx * 2, h_[1] - 2), ramp[1])
        p.fill(R(h_[0] + dx * 2 - 1, h_[1] + 2, h_[0] + dx * 2, h_[1] + 2), ramp[1])
        p.fill(R(h_[0] + dx * 3 - 1, h_[1], h_[0] + dx * 3, h_[1]), ramp[2])
        c.stamp(p, 'v0')

    def leg(hip, foot, ramp):
        p = C()
        h_, f_ = B(hip), P(*foot)
        p.form(L(h_[0], h_[1], 2.4, f_[0], f_[1] - 1, 1.9), ramp, sd=1, hl=1)
        p.fill(R(f_[0] - 4, f_[1] - 1, f_[0] + 1, f_[1]), ramp[1])
        p.fill(R(f_[0] - 3, f_[1], f_[0] + 1, f_[1]), ramp[0])
        c.stamp(p, 'v0')

    arm(S['fsh'], S['fhand'], WF)
    leg((15, 33), S['ffoot'], WF)

    # body: little pot belly, mossy on the back
    p = C()
    body = L(*B((17, 25)), 4.2, *B((18, 32)), 5.4)
    p.form(body, WH, sd=3, hl=1)
    moss = body & (E(*B((23, 26)), 3.6, 4.5) | E(*B((19, 23)), 4, 2.2))
    p.form(moss, MOSS, sd=1, hl=0)
    c.stamp(p, 'v1')

    leg((20, 33), S['nfoot'], WH)

    # head: lumpy, slightly lopsided; moss cap on the shaded crown, a sprout with one leaf
    hx, hy = S['head']
    t = S['tilt']
    H0 = B((15 + hx, 14 + hy))
    p = C()
    # sprout (behind head)
    q = (H0[0] + 5 + t, H0[1] - 9)
    p.line([(q[0], q[1] + 3), (q[0], q[1]), (q[0] + 1, q[1] - 2)], 'g1')
    p.form(PG([(q[0] + 1, q[1] - 3), (q[0] + 5, q[1] - 5), (q[0] + 6, q[1] - 3), (q[0] + 3, q[1] - 1)]), ('g1', 'g2', 'g3'), sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    head = E(H0[0], H0[1], 10.4, 8.2) | E(H0[0] + 2 + t, H0[1] - 2, 8.4, 7.4) | E(H0[0] - 3 - t, H0[1] + 2, 6.6, 6.6)
    p.form(head, WH, sd=4, hl=1)
    core = head & ~sh(head, -2, -2)
    p.a[core & (p.a == I('v1'))] = I('v0')                           # deep shadow rim (4 steps on the big form)
    cap = head & (E(H0[0] + 8 + t, H0[1] - 7, 8.5, 5.2) | E(H0[0] + 11, H0[1] - 1, 3.4, 5.0))
    p.form(cap, MOSS, sd=1, hl=1)
    p.fill(R(H0[0] + 3 + t, H0[1] - 7, H0[0] + 4 + t, H0[1] - 7), 'g3', only=cap)
    p.fill(R(H0[0] + 9, H0[1] + 1, H0[0] + 9, H0[1] + 2), 'g1', only=head)   # moss drip
    p.fill(R(H0[0] - 6, H0[1] - 5, H0[0] - 4, H0[1] - 5), 'v3', only=head)   # glint
    g = HOLES_WIDE if S['wide'] else HOLES
    p.grid(H0[0] - 8, H0[1] - 4 - (1 if S['wide'] else 0), g, LEG)
    p.line([(H0[0] + 1, H0[1] - 8), (H0[0], H0[1] - 6), (H0[0] + 1, H0[1] - 5)], 'v1', only=head)   # hairline crack
    c.stamp(p, 'v0')

    arm(S['nsh'], S['nhand'], WH)

    # ghostly rattle rings (strike only): cold spirit-blue arcs leaving the mouth
    for i in range(S['rattle']):
        cx, cy = H0[0] - 12 - i * 5, H0[1] + 4
        arc = (E(cx + 4, cy, 5.4, 6.4 + i) & ~E(cx + 5.6, cy, 5.4, 6.4 + i)) & (px.Y > cy - 4 - i) & (px.Y < cy + 4 + i)
        c.fill(arc, 'a2' if i == 0 else 'a1')

    c.blacken()
    return c


WALK = [
    dict(bob=0, ffoot=(9, 39), nfoot=(22, 39), fhand=(9, 33), nhand=(18, 35)),
    dict(bob=-1, ffoot=(13, 39), nfoot=(19, 38), fhand=(7, 32), nhand=(15, 35)),
    dict(bob=0, ffoot=(17, 39), nfoot=(14, 39), fhand=(7, 30), nhand=(13, 34)),
    dict(bob=-1, ffoot=(14, 38), nfoot=(18, 39), fhand=(7, 32), nhand=(15, 35)),
]
ATTACK = [
    dict(head=(2, -1), tilt=1, fhand=(9, 24), nhand=(25, 33)),
    dict(head=(-3, 1), tilt=-1, wide=True, rattle=2, fhand=(6, 29), nhand=(12, 32), bob=1, ffoot=(10, 39)),
    dict(head=(-1, 0), wide=True, rattle=0, fhand=(7, 31), nhand=(14, 34)),
]

if __name__ == '__main__':
    export(NAME, kodama, WALK, ATTACK)
    zoom(NAME)
