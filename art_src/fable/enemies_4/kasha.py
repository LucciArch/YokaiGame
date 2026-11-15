"""Kasha: black fire cat wreathed in orange flames, descending from the sky. Normal (~52 px), floats. Attack: pounce trailing flames."""
from common import *
import cat as catlib

NAME = 'kasha'
CELL = (136, 92)
ORG = (72, 74)            # body origin x, lowest hover line y
NEAR = ('h0', 'h1', 'h2')
FAR = ('h0', 'h0', 'h1')
LEG = dict(zip('KmnopYZqWrR', ['K', 'h0', 'h1', 'h2', 'r2', 'e1', 'y3', 'q', 'b3', 'f1', 'f2']))

DEF = dict(dx=0, dy=0, claws=1, fl=0, trail=0, ribs=False,
           hq=(14, -24, 8.2, 7.6), hump=(1, -28, 11, 7.2), chest=(-11, -25, 7.6, 7.8),
           head=(-35, -40),
           tail=[(20, -27), (29, -33), (33, -43), (29, -51)],
           nh=[(15, -21), (16, -13), (24, -11), (27, -6)], nhd=60,
           fh=[(11, -19), (9, -12), (16, -8), (17, -3)], fhd=70,
           nf=[(-10, -20), (-17, -13), (-21, -7)], nfd=150,
           ff=[(-15, -21), (-24, -17), (-29, -12)], ffd=160)


def fire(c, S, B, layer):
    fl = S['fl']
    tr = S['trail']
    if layer == 'back':
        hq, hump, ch = S['hq'], S['hump'], S['chest']
        tips = []
        # mane of fire along the spine, leaning back
        spine = [(ch[0] - 2, ch[1] - ch[3] + 2), (ch[0] + 5, ch[1] - ch[3]), (hump[0], hump[1] - hump[3] + 1),
                 (hump[0] + 7, hump[1] - hump[3] + 2), (hq[0] + 1, hq[1] - hq[3] + 1), (hq[0] + 7, hq[1] - 3)]
        for k, b in enumerate(spine):
            h = 8 + 4 * ((k + fl) % 3) + tr // 2
            lean = 5 + 2 * ((k + fl) % 2) + tr
            tips.append((B(b), B((b[0] + lean, b[1] - h)), 3.4))
        # fire under the belly / trailing behind the haunch
        for k, (bx, by) in enumerate([(hq[0] + 6, hq[1] + 4), (hq[0] + 2, hq[1] + 7), (ch[0] + 4, ch[1] + 7)]):
            h = 5 + 3 * ((k + fl + 1) % 3)
            tips.append((B((bx, by)), B((bx + 8 + tr * 2 + h, by + 1 - (k % 2) * 3)), 3.2))
        flame(c, None, tips)
        # tail flame
        t = S['tail'][-1]
        tt = [(B(t), B((t[0] + 3 + tr * 2, t[1] - 10 - 2 * (fl % 2))), 4.2),
              (B((t[0] + 1, t[1] + 2)), B((t[0] + 8 + tr * 2, t[1] - 4 - 2 * ((fl + 1) % 2))), 3.2),
              (B((t[0] - 1, t[1])), B((t[0] - 4 + tr, t[1] - 7 - (fl % 3))), 3.0)]
        flame(c, None, tt)
    else:
        tips = []
        for key in ('nf', 'nh', 'ff', 'fh'):
            q = S[key][-1]
            h = 6 + 2 * ((fl + len(key) + int(q[0])) % 3)
            tips.append((B((q[0] + 2, q[1] - 1)), B((q[0] + 6 + tr * 2, q[1] - h)), 2.7))
            tips.append((B((q[0] + 3, q[1] + 1)), B((q[0] + 9 + tr * 2, q[1] - 1 - (fl % 2))), 2.3))
        flame(c, None, tips)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    return catlib.cat(S, NEAR, FAR, 'K', LEG, CELL, ORG, fire=fire, bristle=False)


WALK = [
    dict(dy=0, fl=0),
    dict(dy=-1, fl=1, nf=[(-10, -20), (-18, -14), (-23, -9)], nh=[(15, -21), (17, -13), (25, -12), (29, -8)],
         tail=[(20, -27), (29, -33), (34, -42), (31, -51)]),
    dict(dy=-2, fl=2),
    dict(dy=-1, fl=3, ff=[(-15, -21), (-23, -15), (-27, -9)], fh=[(11, -19), (10, -12), (17, -9), (19, -4)],
         tail=[(20, -27), (29, -34), (32, -44), (27, -51)]),
]
ATTACK = [
    # rears back, gathering
    dict(dx=8, dy=-6, fl=1, hq=(14, -20, 8.2, 7.8), hump=(3, -27, 10.5, 7.4), chest=(-8, -29, 7.6, 7.8), head=(-31, -46),
         tail=[(20, -22), (30, -25), (37, -33), (37, -43)],
         nh=[(15, -17), (11, -10), (19, -8), (18, -3)], fh=[(11, -15), (6, -9), (13, -6), (11, -1)],
         nf=[(-7, -24), (-13, -17), (-10, -11)], nfd=120, ff=[(-12, -25), (-19, -19), (-18, -13)], ffd=130),
    # dives forward, claws out, flames streaming
    dict(dx=-12, dy=-2, fl=2, trail=4, claws=2, hq=(17, -26, 8, 7.2), hump=(3, -25, 12, 6.8), chest=(-11, -20, 7.6, 7.6), head=(-36, -33),
         tail=[(23, -29), (32, -34), (41, -36), (49, -41)],
         nh=[(18, -23), (25, -18), (33, -19), (39, -16)], nhd=10, fh=[(14, -21), (21, -13), (29, -13), (35, -9)], fhd=20,
         nf=[(-11, -16), (-20, -9), (-29, -8)], nfd=175, ff=[(-15, -17), (-26, -15), (-34, -17)], ffd=190),
    dict(dx=-8, dy=0, fl=3, trail=1, claws=2,
         nf=[(-10, -20), (-15, -12), (-20, -6)], ff=[(-15, -21), (-22, -15), (-27, -10)]),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
