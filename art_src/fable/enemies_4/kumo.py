"""Kumo: small dark purple spider with red eyes. Small (~32 px). Attack: jumps and bites."""
from common import *

NAME = 'kumo'
CW, CH = 96, 64
BASE = 57
NEAR = ('u1', 'u2', 'u3')
FAR = ('u0', 'u1', 'u2')

LEG = dict(zip('KeEZwWbmno', ['K', 'e0', 'e1', 'y3', 'b2', 'b3', 'b0', 'u0', 'u1', 'u2']))
FACE = """
..e...e....
KKKK.KKKK..
KeEEKeEEK.e
KEZEKEZEK..
KeEeKeEeK..
.KKK.KKK...
"""
FANGS = """
mnn.mnn
mwn.mwn
.wm..wm
.W...W.
"""
FANGS_OPEN = """
mnn...mnn
mwn...mwn
wm.....wm
W.......W
W.......W
"""
MARK = """
.ee...ee.
eEEe.eEEe
.ee.e.ee.
...eEe...
..e.e.e..
..e...e..
"""

# near legs: hip offset from body centre, foot x offset, foot lift, knee height
DEF = dict(dx=0, bob=0, rear=0, open=False,
           nf=[(-25, 0), (-4, 0), (12, 0), (23, 0)],
           ff=[(-21, 0), (0, 0), (16, 0), (26, 0)],
           kh=[11, 14, 14, 11])
HIPS = [(-4, 1), (-1, 3), (2, 3), (5, 2)]


def leg(c, hip, foot, kh, ramp, bend):
    mid = lerp(hip, foot, 0.45)
    knee = (mid[0] + bend, min(hip[1], foot[1]) - kh)
    p = C()
    p.form(L(knee[0], knee[1], 1.3, foot[0], foot[1], 0.7), ramp, sd=1, hl=0)
    c.stamp(p, 'u0')
    p = C()
    p.form(L(hip[0], hip[1], 1.6, knee[0], knee[1], 1.3), ramp, sd=1, hl=0)
    p.form(E(knee[0], knee[1], 1.7, 1.7), ramp, sd=0, hl=1)
    c.stamp(p, 'u0')


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx, cy = 52 + S['dx'], 45 + S['bob']
    rr = S['rear']                     # head end lifts by rr px
    hc = (cx - 10, cy + 1 - rr)         # cephalothorax centre
    ab = (cx + 9, cy - 3 + rr // 2)    # abdomen centre

    def hip(i, far=False):
        h = HIPS[i]
        return (cx + h[0] - (2 if far else 0), cy + h[1] - (2 if far else 0) - (rr if i < 2 else 0))

    bends = [-3, 1, 2, 5]
    for i in (3, 2, 1, 0):
        f = S['ff'][i]
        leg(c, hip(i, True), (cx + f[0], BASE + f[1]), S['kh'][i] - 2, FAR, bends[i])

    # abdomen
    p = C()
    abd = E(ab[0] + 2, ab[1], 11.4, 10.4)
    p.form(abd, NEAR, sd=4, hl=1)
    p.fill(E(ab[0] - 4, ab[1] - 5, 2.4, 1.4), 'u3', only=abd)
    p.grid(ab[0] + 2, ab[1] - 2, MARK, LEG)
    # bristles on the silhouette
    for (ox, oy, ex, ey) in [(7, -7, 10, -10), (10, -2, 14, -3), (9, 4, 12, 6), (2, -9, 3, -12)]:
        p.fill(L(ab[0] + ox, ab[1] + oy, 1.2, ab[0] + ex, ab[1] + ey, 0.5), 'u1')
    c.stamp(p, 'K')

    # cephalothorax + head
    p = C()
    ct = E(hc[0], hc[1], 8.4, 7.0) | E(hc[0] + 6, hc[1], 6, 5.4)
    p.form(ct, NEAR, sd=2, hl=1)
    p.grid(hc[0] - 8, hc[1] - 4, FACE, LEG)
    c.stamp(p, 'u0')
    p = C()
    if S['open']:
        p.grid(hc[0] - 9, hc[1] + 4, FANGS_OPEN, LEG)
    else:
        p.grid(hc[0] - 8, hc[1] + 4, FANGS, LEG)
    c.stamp(p, 'u0')

    for i in (3, 2, 1, 0):
        f = S['nf'][i]
        leg(c, hip(i), (cx + f[0], BASE + f[1]), S['kh'][i], NEAR, bends[i])
    c.blacken()
    return c


def gait(a, b):
    """a: legs 0,2 forward (+lift) / b: legs 1,3"""
    return [(-21 + a, 0), (-13 + b, 0), (11 + a, 0), (22 + b, 0)]


WALK = [
    dict(bob=0, nf=[(-27, 0), (-2, 0), (9, 0), (26, 0)], ff=[(-19, 0), (-3, 0), (19, 0), (23, 0)]),
    dict(bob=-1, nf=[(-24, -4), (-4, 0), (13, -4), (24, 0)], ff=[(-21, 0), (1, -4), (17, 0), (27, -4)]),
    dict(bob=0, nf=[(-22, 0), (-7, 0), (15, 0), (20, 0)], ff=[(-24, 0), (3, 0), (13, 0), (29, 0)]),
    dict(bob=-1, nf=[(-25, 0), (-4, -4), (11, 0), (24, -4)], ff=[(-22, -4), (0, 0), (15, -4), (26, 0)]),
]
ATTACK = [
    dict(dx=5, bob=3, rear=4, nf=[(-25, -17), (-9, -3), (10, 0), (20, 0)], ff=[(-21, -13), (-4, 0), (13, 0), (23, 0)], kh=[5, 9, 12, 10]),
    dict(dx=-12, bob=-12, rear=2, open=True, nf=[(-28, -8), (-10, -3), (14, -5), (25, -10)], ff=[(-25, -14), (-4, -6), (18, -6), (28, -13)], kh=[11, 10, 8, 6]),
    dict(dx=-8, bob=2, nf=[(-26, 0), (-5, 0), (11, 0), (22, 0)], ff=[(-21, 0), (-1, 0), (15, 0), (25, 0)], kh=[10, 12, 12, 10]),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
