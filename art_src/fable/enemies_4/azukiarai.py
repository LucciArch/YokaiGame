"""Azukiarai: small hunched old man washing red beans in a straw sieve. Normal (~46 px, hunched).
Attack: flings a handful of red beans."""
from common import *

NAME = 'azukiarai'
CW, CH = 104, 72
OX, BASE = 62, 66
SKIN = ('k0', 'k1', 'k2')
SKINF = ('s1', 'k0', 'k1')
ROBE = ('s0', 's1', 's2')
STRAW = ('o0', 'o1', 'o2')

LEG = dict(zip('KkLjJYZyWqvV', ['K', 'k1', 'k2', 'k0', 's1', 'y2', 'y3', 'y1', 'b3', 'q', 'v1', 'v2']))
HEAD = """
......KKKKKK.......
....KKLLLLkkKK.....
...KLLLLLkkkkkK....
..KLLLLkkkkkkkkK...
..KLLkkkkkkkkkkjK..
.KKKKKKkkkKKKKkjKv.
.KYYYZKKkKKYYYKjjKV
.KYKKYYKkKYKKYKjjKv
.KyYYYKkkkKYYyKjjKV
..KKKKkkkkkKKKkjjKv
.KkkkkLLkkkkkkjjjK.
KLLkkkLkkkkkkjjjJK.
KkkjjkkkjkkkjjjJK..
.KKKKKKKKKjjjjJK...
.KWqWqWWqKjjjJK....
..KqqWqqKkjjJK.....
...KKKKKkjjJK......
.....KjjjjJK.......
"""
FOOT = """
...kkkj
.Lkkkkj
LLkkkjj
"""


def hand(c, w, ang, ramp):
    p = C()
    p.form(E(w[0], w[1], 2.5, 2.3), ramp, sd=1, hl=1)
    for da in (-40, 0, 40):
        p.fill(L(w[0], w[1], 1.0, *pol(w, ang + da, 3.8), 0.6), ramp[1 if da > 0 else 2])
    c.stamp(p, ramp[0] if ramp[0] != 's1' else 's0')


def arm(c, s, e, w, ang, ramp):
    ln = 's0'
    seg(c, e, 2.0, w, 1.8, ramp, ln=ln)
    hand(c, w, ang, ramp)
    # ragged short sleeve over the upper arm
    p = C()
    p.form(L(s[0], s[1], 3.6, *lerp(s, e, 0.8), 3.2), ROBE if ramp is SKIN else ('s0', 's0', 's1'), sd=2, hl=1)
    c.stamp(p, 'K')


def sieve(c, at, tilt=0, beans=True):
    """shallow round straw basket (zaru) seen from the side, heaped with azuki"""
    x, y = at
    p = C()
    if beans:
        heap = E(x, y - 2, 8.4, 3.4) & (px.Y <= y - 1)
        p.form(heap, ('m1', 'm2', 'm3'), sd=2, hl=0)
        for (ox, oy) in [(-5, -3), (-1, -4), (3, -3), (-3, -2), (5, -2), (1, -2)]:
            p.px(x + ox, y + oy, 'm3'); p.px(x + ox + 1, y + oy + 1, 'm0')
    c.stamp(p, 'm0')
    p = C()
    bowl = PG([(x - 10, y - 1 + tilt), (x + 10, y - 1 - tilt), (x + 7, y + 4), (x - 7, y + 4)]) | E(x, y + 2, 8, 2.6)
    p.form(bowl, STRAW, sd=2, hl=0)
    p.fill(bowl & (px.Y <= y), 'o2')
    for k in range(-8, 9, 3):
        p.line([(x + k, y + 1), (x + k * 0.8, y + 5)], 'o0', only=bowl)
    c.stamp(p, 'K')


DEF = dict(dx=0, bob=0, hx=0, hy=0,
           nsh=(-3, -24), nel=(-9, -17), nwr=(-15, -16), nang=200,
           fsh=(-8, -25), fel=(-15, -19), fwr=(-21, -17), fang=170,
           sv=(-20, -11), tilt=0, beans=[],
           nft=-2, fft=-12, nlift=0, flift=0)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx = OX + S['dx']
    b = S['bob']

    def B(pt):
        return (cx + pt[0], BASE + pt[1] + b)

    # far arm
    arm(c, B(S['fsh']), B(S['fel']), B(S['fwr']), S['fang'], SKINF)
    # legs: thin bent shanks and big bare feet
    for (fx, lift, ramp, kx) in ((S['fft'], S['flift'], SKINF, -6), (S['nft'], S['nlift'], SKIN, 3)):
        knee = (cx + kx - 4, BASE - 11 + b)
        ank = (cx + fx + 3, BASE - 3 - lift)
        seg(c, knee, 2.4, ank, 1.9, ramp, ln='s0')
        p = C()
        p.grid(cx + fx - 3, BASE - 2 - lift, FOOT, dict(k=ramp[1], L=ramp[2], j=ramp[0]))
        c.stamp(p, 's0')
    # hunched robe: big rounded back
    p = C()
    robe = E(*B((5, -21)), 11.4, 12.4) | L(*B((-2, -26)), 7, *B((-3, -13)), 7.5) | PG([B((-8, -14)), B((14, -14)), B((13, -5)), B((9, -7)), B((5, -4)), B((0, -7)), B((-4, -4)), B((-8, -7))])
    p.form(robe, ROBE, sd=5, hl=1)
    inner = erode(robe, 1)
    for pts in ([(-1, -30), (-4, -20), (-3, -8)], [(9, -30), (12, -20), (10, -9)], [(4, -14), (5, -6)]):
        p.line([B(q) for q in pts], 's0', only=inner)
    # patch + rope belt
    p.form(R(*B((6, -24)), *B((10, -20))) & inner, ('s1', 's2', 's3'), sd=1, hl=0)
    p.line([B((-8, -15)), B((15, -16))], 'o1', only=robe)
    p.line([B((-8, -14)), B((15, -15))], 'o0', only=robe)
    c.stamp(p, 'K')
    # head
    p = C()
    p.grid(*[int(v) for v in B((-21 + S['hx'], -44 + S['hy']))], HEAD, LEG)
    c.stamp(p, 'K')
    # sieve in front, near arm over its rim
    sieve(c, B(S['sv']), S['tilt'])
    arm(c, B(S['nsh']), B(S['nel']), B(S['nwr']), S['nang'], SKIN)
    c.blacken()
    # thrown beans (after the rim pass so they stay deep red)
    for (bx, by_) in S['beans']:
        p = C()
        q = (cx + bx, BASE + by_)
        p.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 'm2')
        p.px(q[0], q[1], 'm3')
        c.stamp(p, 'K')
    return c


WALK = [
    dict(bob=0, nft=-6, fft=-9, nwr=(-15, -16)),
    dict(bob=-1, nft=-3, fft=-13, flift=2, nwr=(-16, -17), tilt=1),
    dict(bob=0, nft=0, fft=-16, nwr=(-15, -16)),
    dict(bob=-1, nft=-4, nlift=2, fft=-12, nwr=(-14, -17), tilt=-1),
]
ATTACK = [
    # scoops a fistful, arm cocked back
    dict(dx=3, hx=1, nsh=(-2, -25), nel=(6, -31), nwr=(11, -38), nang=300, sv=(-19, -12), tilt=-1),
    # whips the arm forward: beans spray left
    dict(dx=-4, bob=1, hx=-2, hy=1, nsh=(-5, -25), nel=(-14, -27), nwr=(-23, -29), nang=185, sv=(-18, -9), tilt=2,
         beans=[(-33, -34), (-38, -29), (-43, -36), (-47, -30), (-35, -40), (-52, -35), (-41, -24)]),
    dict(dx=-2, hx=-1, nsh=(-4, -24), nel=(-12, -20), nwr=(-19, -22), nang=170, sv=(-19, -10), tilt=1,
         beans=[(-50, -27), (-56, -33)]),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
