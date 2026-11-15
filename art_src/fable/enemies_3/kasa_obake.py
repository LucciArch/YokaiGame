"""Kasa-obake: old torn purple paper umbrella, one eye, long tongue, one leg in a geta."""
from kit import *
import px

NAME = 'kasa_obake'
CW, CH = 84, 88
OX, OY = 36, 20            # local baseline y=63

LEG = dict(zip('KWwvRrYZqpPbBm', ['K', 'v3', 'v2', 'v1', 'e1', 'e0', 'y2', 'y3', 'q', 'p0', 'p1', 'b2', 'b3', 'm1']))
EYE = """
KKK..........
KKKKKKK......
.KKKKKKKKKK..
.KwWWKKKKKKKK
KwWWrrrWWwKKK
KwWrRYRrWwwvK
KwWrYKYrWwwvK
KwWrRZRrWwvvK
.KwWrrrWwvvK.
..KvwwwvvvK..
...KKKKKKK...
"""
MOUTH = """
K.................K
KK...............KK
KKKK...........KKKK
.KbKKKKKKKKKKKKKbK.
.KqbqBqbqBqbqBqbqK.
..KqqqqqqqqqqqqqK..
..KqqqqqqqqqqqqqK..
...KbqbqqqqqbqbK...
....KKKKKKKKKKK....
"""

DEF = dict(by=0, lift=0, rx=17.0, apex=0, sway=0,
           tongue=[(-4, 0), (-8, 6), (-9, 13), (-6, 18)], tr=2.6)


def P(x, y):
    return (x + OX, y + OY)


def kasa(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    by, lift, rx = S['by'], S['lift'], S['rx']

    def B(x, y):
        return P(x, y + by)

    # ---- single leg + geta
    hip = B(23, 38)
    ank = P(24, 55 - lift)
    knee = ik(hip, ank, 8.8, 8.8, side=-1)
    p = C()
    fx, fy = ank
    # geta: board + two teeth
    p.form(R(fx - 9, fy + 3, fx + 5, fy + 4), WOOD, sd=1, hl=1)
    p.fill(R(fx - 7, fy + 5, fx - 5, fy + 7), 'w1'); p.fill(R(fx - 5, fy + 5, fx - 5, fy + 7), 'w0')
    p.fill(R(fx + 1, fy + 5, fx + 3, fy + 7), 'w1'); p.fill(R(fx + 3, fy + 5, fx + 3, fy + 7), 'w0')
    c.stamp(p, 'K')
    p = C()
    foot = PG([(fx + 3, fy - 2), (fx + 4, fy + 2), (fx - 8, fy + 2), (fx - 9, fy + 1), (fx - 5, fy - 1), (fx - 2, fy - 3)])
    p.form(foot, SKN, sd=1, hl=1)
    p.line([(fx - 6, fy + 1), (fx - 3, fy - 1), (fx - 1, fy + 1)], 'm2', only=foot)           # hanao strap
    p.form(L(knee[0], knee[1], 2.9, fx, fy - 1, 2.2), SKN, sd=2, hl=1)       # shin
    c.stamp(p, 'k0')
    p = C()
    p.form(L(hip[0], hip[1], 3.8, knee[0], knee[1], 3.1), SKN, sd=2, hl=1)   # thigh
    p.form(E(knee[0] - 0.5, knee[1], 2.7, 2.5), SKN, sd=1, hl=1)             # knee cap
    c.stamp(p, 'k0')

    # ---- umbrella: dark inside, then bell-shaped paper panels between the ribs
    A = B(23 + S['sway'], 6 + S['apex'])
    hc = B(22, 37)
    n = 6
    hem = [(hc[0] - math.cos(math.pi * i / n) * rx, hc[1] + math.sin(math.pi * i / n) * 4.0) for i in range(n + 1)]

    def rib(i, t):
        return (A[0] + (hem[i][0] - A[0]) * t ** 0.62, A[1] + (hem[i][1] - A[1]) * t)

    TS = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
    p = C()
    p.fill(E(hc[0], hc[1], rx - 1, 3.6), 'K')
    c.stamp(p, 'K')
    p = C()
    tones = ['p3', 'p2', 'p2', 'p1', 'p1', 'p0']
    cone = np.zeros((px.H, px.W), bool)
    for i in range(n):
        a_, b_ = hem[i], hem[i + 1]
        mid = ((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2 - 2.4)
        left = [rib(i, t) for t in TS]
        right = [rib(i + 1, t) for t in TS][::-1]
        if i == 4:      # torn panel: a ragged bite out of the hem
            bot = [lerp(a_, A, 0.1), (mid[0] - 2, mid[1] - 8), (mid[0], mid[1] - 3), (mid[0] + 2, mid[1] - 7)]
        elif i == 1:
            bot = [(mid[0] - 2, mid[1]), (mid[0] - 1, mid[1] - 4), (mid[0] + 1, mid[1])]
        else:
            bot = [mid]
        pan = PG(left + bot + right)
        p.fill(pan, tones[i])
        cone |= pan
    # shadow toward the hem (light comes from the top-left), darker on the right half
    low = cone & ~sh(cone, 0, -4)
    for hi_, lo_ in (('p3', 'p2'), ('p2', 'p1'), ('p1', 'p0')):
        p.a[low & (p.a == I(hi_)) & (px.X > hc[0] - rx * 0.55)] = I(lo_)
    for i in range(1, n):
        p.line([rib(i, t) for t in TS], 'p0' if i > 2 else 'p1', only=cone)
    p.line([rib(1, t) for t in TS[1:4]], 'p3', only=cone)
    p.line([(x - 1, y) for x, y in [rib(2, t) for t in TS[1:3]]], 'p3', only=cone)
    # old paper: a pasted patch and a hole
    pt = B(29, 19)
    p.fill(R(pt[0], pt[1], pt[0] + 3, pt[1] + 3), 'c1', only=cone); p.fill(R(pt[0], pt[1], pt[0] + 2, pt[1]), 'c2', only=cone)
    p.fill(R(pt[0] + 3, pt[1] + 1, pt[0] + 3, pt[1] + 3), 'c0', only=cone)
    c.stamp(p, 'K')
    # rib tips (bone) + top knob
    for i in range(n + 1):
        if i in (3, 5):
            continue
        hx_, hy_ = int(round(hem[i][0])), int(round(hem[i][1]))
        c.pxs([(hx_, hy_ + 1)], 'b2'); c.pxs([(hx_, hy_ + 2)], 'b1')
    p = C()
    p.form(R(A[0] - 1, A[1] - 5, A[0], A[1] - 1), WOOD, sd=1, hl=0)
    p.fill(R(A[0] - 2, A[1] - 5, A[0] + 1, A[1] - 4), 'w1'); p.fill(R(A[0] - 2, A[1] - 5, A[0], A[1] - 5), 'w2')
    c.stamp(p, 'K')

    # ---- tongue (behind the mouth grid's teeth)
    mo = B(7, 26)
    tp = [(mo[0] + 6 + x, mo[1] + 6 + y) for x, y in S['tongue']]
    sp = spline([(mo[0] + 9, mo[1] + 6)] + tp, 6)
    p = C()
    tm = chain(sp, S['tr'], 1.6)
    p.form(tm, RD, sd=1, hl=0)
    k_ = len(sp) // 3
    p.line([(x - 1, y - 1) for x, y in sp[k_:k_ + 5]], 'm3', only=erode(tm))
    c.stamp(p, 'K')
    # ---- face: mouth + eye
    p = C()
    p.grid(mo[0], mo[1], MOUTH, LEG)
    # tongue root over lower teeth
    p.fill(R(mo[0] + 4, mo[1] + 5, mo[0] + 10, mo[1] + 7), 'm2'); p.fill(R(mo[0] + 4, mo[1] + 5, mo[0] + 10, mo[1] + 5), 'm1')
    c.stamp(p, ring=False)
    p = C()
    p.grid(*B(9, 13), EYE, LEG)
    c.stamp(p, ring=False)
    c.blacken()
    return c


WALK = [
    dict(by=3, rx=18.5, tongue=[(-4, 0), (-8, 6), (-8, 12), (-5, 16)]),
    dict(by=-2, lift=2, rx=16.0, apex=-1, tongue=[(-4, 0), (-9, 5), (-11, 12), (-9, 18)]),
    dict(by=-3, lift=3, rx=15.5, apex=-1, tongue=[(-4, 0), (-8, 6), (-11, 13), (-10, 19)]),
    dict(by=1, rx=17.5, tongue=[(-4, 0), (-7, 7), (-8, 13), (-5, 18)]),
]
ATTACK = [
    dict(by=6, rx=19.5, apex=1, sway=2, tongue=[(-3, 0), (-5, 4), (-4, 8)], tr=3.0),
    dict(by=-17, lift=13, rx=14.5, apex=-2, sway=-1,
         tongue=[(-6, -1), (-14, 2), (-22, 8), (-29, 5), (-33, -1)], tr=2.8),
    dict(by=3, rx=18.5, tongue=[(-5, 0), (-11, 5), (-15, 12), (-13, 18)]),
]

if __name__ == '__main__':
    export(NAME, kasa, WALK, ATTACK)
