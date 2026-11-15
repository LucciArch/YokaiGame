"""Izanami - goddess of death, rotting in Yomi."""
from lib3 import *

NAME = 'boss_izanami'
CW, CH = 264, 150
OX, OY = 140, 18            # local baseline y=126
SK = ('z1', 'z2', 'z3')
SKD = ('z0', 'z1', 'z2')
WH = ('v1', 'v2', 'v3')
WHD = ('v0', 'v1', 'v2')
HAIR = ('h0', 'hb', 'h2')
MIA = ('p1', 'p2', 'p3')

LEG = dict(zip('KabcdEZqwxvVp', ['K', 'z0', 'z1', 'z2', 'z3', 'e1', 'y3', 'q', 'b2', 'b3', 'v2', 'v3', 'p1']))
FACE = """
.......vvvvv.......
.....vvvVVVvvv.....
...ccvVVVVVVVvcc...
..cdddvVVVVVvdccb..
..cdddddvVVvdddccb.
.cddddddddvddddccb.
.cdaaaadddddaaaacbb
.caKKKKaddaKKKKKabb
.cKKEZKKadaKKEZKKab
.caKKKKaccaaKKKKabb
.cdaaaaccdcaaaaabbb
..cddccKcddcccpbbba
..cdccKKKcdccppbbaa
..ccdcccccccbpKpbaa
...cKKKKKKKKKKKKba.
...cxwxwxwxwxKqKaa.
...bKqqqqqqqqKKbaa.
...bwxwxwxwxwbbaa..
....bKKKKKKKbbaa...
.....bccccbbaa.....
.......bbbaa.......
"""


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, ph=0.0, sway=0,
           fsh=(52, 46), fel=(38, 56), fwr=(24, 50), fang=185,
           nsh=(67, 48), nel=(54, 66), nwr=(37, 68), nang=160,
           fx=None, mia=1.0)


def hand(c, wr, ang, ramp, spread=30, ln=13.0):
    """gaunt forearm + bony clawed hand: 4 long two-jointed fingers + thumb. wr = sleeve mouth"""
    hp = pol(wr, ang, 8)
    p = C()
    p.form(L(wr[0] + 2, wr[1], 2.8, hp[0], hp[1], 2.2), ramp, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    th = pol(hp, ang + 80, 5)
    p.fill(tube([hp, th, pol(th, ang + 20, 5)], 1.5, 0.7), ramp[0])
    for i, da in enumerate((-spread, -spread / 3, spread / 3, spread)):
        k1 = pol(hp, ang + da, ln * 0.5)
        tip = pol(k1, ang + da * 0.3 + 30, ln * 0.55)
        f = tube([hp, k1, tip], 1.6, 0.9)
        p.fill(f, ramp[1])
        p.fill(f & ~sh(f, 0, 1) & ~sh(f, 1, 0), ramp[2])
        e = pol(tip, ang + da * 0.3 + 45, 2.6)
        p.fill(L(tip[0], tip[1], 0.9, e[0], e[1], 0.4), 'b3')
        p.fill(E(k1[0], k1[1], 1.5, 1.5), ramp[2])
    p.form(E(hp[0], hp[1], 3.4, 3.2), ramp, sd=1, hl=1)
    c.stamp(p, 'K')


def sleeve(c, sh_, el, wr, ramp, drop, ph):
    p = C()
    arm = L(*sh_, 5.5, *el, 6.5) | L(*el, 6.5, *wr, 7.5)
    w = math.sin(ph) * 1.5
    tat = PG([add(el, (6, 0)), add(el, (5 + w, drop - 6)), add(el, (1, drop - 12)), add(lerp(el, wr, .4), (2 + w, drop + 2)),
              add(lerp(el, wr, .6), (0, drop - 8)), add(lerp(el, wr, .8), (2 + w, drop + 6)), add(wr, (3, drop - 10)),
              add(wr, (0 + w, drop - 2)), add(wr, (-4, 6)), wr])
    m = arm | tat
    p.form(m, ramp, sd=3, hl=1)
    for t in (.25, .6, .9):
        q = lerp(el, wr, t)
        p.line([add(q, (2, 0)), add(q, (3, drop - 4))], ramp[0], only=m)
    # grave stains creeping up from the ragged edge
    st = m & ~sh(m, 0, -4) & sh(m, 0, -1)
    p.fill(st & (p.a != I(ramp[2])), 'v0')
    p.fill(E(*add(wr, (-4, 0)), 2.4, 4.6) & m, 'v0')
    c.stamp(p, 'K')


def miasma(c, base, k, ph, n=7, span=60, seed=0):
    """curling purple wisps rising from the ground"""
    p = C()
    m = np.zeros((px.H, px.W), bool)
    for i in range(n):
        x = base[0] - span / 2 + span * i / (n - 1)
        h = (10 + 9 * ((i * 7 + seed) % 5) / 4) * k + 2 * math.sin(ph + i * 1.9)
        bend = 5 * math.sin(ph * 1.0 + i * 2.3)
        m |= E(x, base[1], 6.4 * k, (4.4 + 1.5 * math.sin(ph + i)) * k)
        if i % 2 == seed % 2:
            m |= tongue((x, base[1] - 1), (x - 2 + bend * 1.6, base[1] - h), 3.0 * k, bend * 1.4, tr=1.1)
    m &= R(0, 0, 999, base[1])
    p.form(m, MIA, sd=2, hl=1)
    c.stamp(p, 'p0')


def iza(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, ph, sw = S['bob'], S['lean'], S['ph'], S['sway']

    def U(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    # ---- miasma behind
    miasma(c, P(70, 126), S['mia'], ph, n=8, span=74, seed=2)
    if S['fx']:
        S['fx'](c, 0)

    # ---- hair curtain down the back to the floor
    p = C()
    hp = [(50, 10), (62, 6), (72, 10), (78, 24), (84, 50), (90, 80), (98 + sw, 104), (104 + sw, 124), (94 + sw, 118), (92 + sw, 125),
          (84 + sw, 116), (80 + sw, 124), (74, 100), (68, 60), (60, 40)]
    hair = PG([U(q, max(0, 1 - q[1] / 110)) for q in hp])
    p.form(hair, HAIR, sd=4, hl=0)
    for a_, b_ in (((70, 14), (80, 50)), ((80, 50), (90 + sw, 100)), ((74, 30), (80, 70)), ((80, 70), (86 + sw, 114)), ((90, 90), (98 + sw, 118))):
        p.line([U(a_, .5), U(b_, .2)], 'h2', only=hair)
    c.stamp(p, 'K')

    # ---- far arm
    sh_, el, wr = U(S['fsh']), U(S['fel'], .6), P(*S['fwr'])
    sleeve(c, sh_, el, wr, WHD, 20, ph)
    hand(c, add(wr, (-5, 0)), S['fang'], SKD)

    # ---- kimono
    p = C()
    hem = [(88, 114), (84 + sw, 124), (78 + sw, 116), (74 + sw, 125), (68, 117), (62 + sw, 124), (56, 116), (50 + sw, 123), (45, 114)]
    kim = PG([U((50, 40)), U((67, 38)), U((75, 56), .8), U((78, 86), .4)] + [P(*q) for q in hem] + [U((51, 88), .4), U((53, 64), .7), U((48, 50))])
    p.form(kim, WH, sd=5, hl=1)
    for (x0, x1) in ((56, 52), (63, 62), (70, 72), (75, 80)):
        p.line([U((x0, 76), .5), P(x1 + sw, 116)], 'v1', only=kim)
    # reversed funeral collar (right over left) and bare sternum
    chest = PG([U((53, 40)), U((62, 39)), U((58, 58), .9)])
    p.form(chest, SKD, sd=2, hl=0, only=kim)
    p.line([U((62, 39)), U((57, 60), .9), U((56, 74), .7)], 'v0', only=kim)
    p.line([U((52, 41)), U((58, 58), .9)], 'v0', only=kim)
    # rotted hole in the side: ribs
    hole = E(*U((66, 56), .8), 4.4, 6.4)
    p.fill(hole, 'q', only=kim)
    for j in (-3, 0, 3):
        p.line([U((63, 56 + j), .8), U((69, 55 + j), .8)], 'b1', only=hole & kim)
    p.fill(dil(hole) & ~hole & kim, 'v0')
    # obi
    obi = PG([U((52, 66), .7), U((77, 64), .7), U((78, 72), .7), U((52, 74), .7)])
    p.form(obi, WHD, sd=2, hl=1, only=kim)
    # grave rot on the tatters
    st = kim & ~sh(kim, 0, -7) & R(0, OY + 100, 999, 999)
    p.fill(st, 'v0')
    p.fill(kim & ~sh(kim, 0, -3) & R(0, OY + 100, 999, 999), 'p1')
    for (x, y) in ((60, 96), (72, 104), (55, 108)):
        p.fill(E(*P(x + sw * .5, y), 2.6, 3.2), 'v1', only=kim)
    # maggots
    for (x, y) in ((64, 84), (71, 94), (58, 100)):
        p.fill(R(*P(x, y), *P(x + 1, y)), 'c2', only=kim)
    c.stamp(p, 'K')

    # ---- head
    HX, HY = U((44, 10))

    def Hh(x, y):
        return (HX + x, HY + y)
    p = C()
    neck = L(*Hh(14, 22), 3.2, *U((57, 42)), 3.6)
    p.form(neck, SKD, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    top = E(*Hh(13, 8), 13.4, 10.4) | PG([Hh(8, 4), Hh(24, 6), Hh(30, 30), Hh(22, 36), Hh(16, 20)])
    p.form(top, HAIR, sd=3, hl=0)
    c.stamp(p, 'K')
    p = C()
    p.grid(*Hh(0, 2), FACE, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # hair over the brow and long front locks
    p = C()
    crown = (E(*Hh(12, 6), 13.4, 9.4) & ~PG([Hh(-4, 20), Hh(9, 0), Hh(16, 20)]) & ~PG([Hh(9, 0), Hh(22, 22), Hh(9, 22)])) & R(0, 0, 999, HY + 12)
    lock1 = tube(curve([Hh(19, 6), Hh(22, 20), Hh(19, 36 ), Hh(21 + sw, 52), Hh(18 + sw, 62)], 6), 3.4, 0.8)
    lock2 = tube(curve([Hh(1, 6), Hh(-2, 18), Hh(1, 32), Hh(-1 + sw, 44)], 6), 2.4, 0.7)
    hm = crown | lock1 | lock2
    p.form(hm, HAIR, sd=2, hl=0)
    p.line([Hh(18, 4), Hh(21, 18), Hh(19, 34)], 'h2', only=hm)
    p.line([Hh(6, 0), Hh(14, -1), Hh(20, 3)], 'h2', only=hm)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))

    # ---- near arm
    sh_, el, wr = U(S['nsh']), U(S['nel'], .6), P(*S['nwr'])
    sleeve(c, sh_, el, wr, WH, 24, ph + 1)
    hand(c, add(wr, (-5, 0)), S['nang'], SK)

    # ---- miasma in front
    miasma(c, P(58, 127), S['mia'] * 0.7, ph + 2, n=6, span=56, seed=1)
    if S['fx']:
        S['fx'](c, 1)
    c.blacken()
    return c


def fx_gather(c, layer):
    if layer == 1:
        p = C()
        o = P(22, 34)
        m = E(o[0], o[1], 8.4, 8.4)
        for a in (200, 250, 300, 350, 60, 130):
            m |= tongue(o, pol(o, a, 15), 3.4, 3)
        p.form(m, MIA, sd=3, hl=1)
        p.fill(E(o[0] - 1, o[1] - 1, 3.4, 3.4), 'p3'); p.fill(E(o[0] - 1, o[1] - 1, 1.6, 1.6), 'v3')
        c.stamp(p, 'p0')


def fx_wave(k):
    def f(c, layer):
        if layer != 1:
            return
        p = C()
        x0 = 6 if k >= 1 else -10
        def W(x, y):
            return P(x0 + x, 126 - (126 - y) * k)
        # great breaking wave of rot, crest curling over toward the hero
        outline = [(4, 127), (2, 100), (-8, 66), (-26, 40), (-50, 30), (-74, 38), (-88, 56), (-86, 70), (-76, 62), (-62, 56), (-48, 64),
                   (-42, 84), (-52, 104), (-76, 114), (-102, 120), (-108, 127)]
        m = PG(curve([W(*q) for q in outline], 6))
        # clawing fingers at the lip, spray along the back
        for (x, y, a, l) in ((-88, 60, 120, 16), (-84, 66, 100, 13), (-78, 64, 85, 10), (-90, 54, 150, 13)):
            m |= tongue(W(x, y), pol(W(x, y), a, l * k), 3.2, 3 * k, tr=0.7)
        for (x, y, a, l) in ((-30, 40, 300, 16), (-12, 62, 320, 14), (-52, 32, 265, 13), (0, 92, 330, 12)):
            m |= tongue(W(x, y), pol(W(x, y), a, l * k), 4.0, -4 * k, tr=0.8)
        inn = np.zeros_like(m)
        for off_ in (8, 18, 28):
            inn |= tube(curve([W(-2 - off_ * .4, 120), W(-10 - off_ * .5, 80), W(-28 - off_ * .3, 48 + off_ * .5), W(-54, 38 + off_ * .6), W(-74, 46 + off_ * .5)], 6), 0.8, 0.8)
        m &= R(0, 0, 999, OY + 126)
        p.form(m, MIA, sd=3, hl=1)
        p.fill(m & ~sh(m, -5, -3) & (p.a == I('p1')) & ~sh(m, -1, -1), 'p0')
        inn &= erode(m, 3)
        p.fill(inn, 'p3')
        if k >= 1:
            # screaming faces in the miasma
            for (x, y) in ((-24, 72), (-14, 100)):
                X0, Y0 = P(x0 + x, y)
                fm = E(X0 + 4, Y0 + 4, 8.4, 9.4) & erode(m, 1)
                p.fill(fm, 'p2'); p.fill(fm & ~sh(fm, 1, 1), 'p3')
                p.fill((E(X0 + 1, Y0 + 2, 2.4, 2.8) | E(X0 + 8, Y0 + 2, 2.4, 2.8) | E(X0 + 4, Y0 + 9, 2.6, 3.4)) & erode(m, 1), 'p0')
                p.fill(R(X0, Y0 + 2, X0 + 1, Y0 + 2) | R(X0 + 7, Y0 + 2, X0 + 8, Y0 + 2), 'e1', only=erode(m, 1))
        c.stamp(p, 'p0')
    return f


T = math.pi / 2
WALK = [dict(ph=0, bob=0, sway=0), dict(ph=T, bob=-1, sway=1, fwr=(24, 49), nwr=(37, 67)),
        dict(ph=2 * T, bob=-2, sway=2, fwr=(23, 48), nwr=(36, 66)), dict(ph=3 * T, bob=-1, sway=1, fwr=(24, 49), nwr=(37, 67))]
ATTACK = [
    dict(lean=3, bob=-2, ph=1, fel=(42, 46), fwr=(34, 32), fang=215, nel=(58, 56), nwr=(46, 42), nang=205, fx=fx_gather, mia=1.3, sway=-2),
    dict(lean=-5, bob=1, ph=2, fel=(36, 52), fwr=(18, 50), fang=180, nel=(50, 62), nwr=(30, 62), nang=175, fx=fx_wave(1.0), mia=0.8, sway=3),
    dict(lean=-2, bob=0, ph=3, fel=(38, 56), fwr=(24, 54), fang=175, nel=(54, 66), nwr=(36, 70), nang=150, fx=fx_wave(0.5), mia=0.9, sway=1),
]

if __name__ == '__main__':
    export(NAME, iza, WALK, ATTACK)
