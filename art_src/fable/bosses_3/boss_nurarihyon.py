"""Nurarihyon - supreme commander of the yokai. ~90 px."""
from lib3 import *

NAME = 'boss_nurarihyon'
CW, CH = 168, 112
OX, OY = 74, 8             # local baseline y=100
SKIN = ('n1', 'n2', 'n3')
HAORI = ('p0', 'p1', 'p2')
KIM = ('i1', 'i2', 'i3')
SMOKE = ('p2', 'z2', 'z3')

LEG = dict(zip('KabcdYZwuq', ['K', 'n0', 'n1', 'n2', 'n3', 'y2', 'y3', 'v2', 'v1', 'q']))
FACE = """
....................
...bbb.....bbbb.....
..b...bbbbb....bb...
....................
..bbbb....bbbbbbb...
.b....bbbb..........
....................
KK.........KKKK.....
aKKK....KKKKaaaa....
aYZKa..aKKYZYKab....
.aaa.c..aaaaaa.b....
.b..dcb..bbbb..b....
...ddcb.........b...
..dddcab....b...b...
.dddcaa.b....b......
.caaaa..bb...b......
..wwwwwb.....b......
.wwuuwwwwwKK.b......
.wu.KKKKKKwwK.......
.w...ccc...ww.......
.....wwwu...w.......
.....wwu............
.....wu.............
.....w..............
"""

SKULL = """
..ddddd..
.ddddddd.
dDDDdDDDd
dDEDdDEDd
ddddDdddd
.dDdDdDd.
..ddddd..
"""

HAND = """
..KKKK...
.KccddK..
KbcKcddK.
KbcKccdK.
KbbKKccK.
.KbbbbcK.
..KKbbK..
"""


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, hx=0, hy=0,
           ffoot=40, nfoot=56, hem=0,
           sh=(61, 50), el=(45, 61), wr=(27, 42), pang=168,
           wisp=0, puff=None, sway=0, glow=False)


def smoke_cloud(c, blobs, eyes=()):
    p = C()
    m = np.zeros((px.H, px.W), bool)
    for (x, y, rx, ry) in blobs:
        m |= E(*P(x, y), rx + .4, ry + .4)
    p.form(m, SMOKE, sd=3, hl=1)
    inner = np.zeros_like(m)
    for (x, y, rx, ry) in blobs:
        if rx > 5:
            inner |= E(*P(x - 1, y - 1), rx * 0.5, ry * 0.5)
    for (x, y, rx, ry) in blobs:
        if rx > 5:
            mm = E(*P(x - 1.5, y - 1.5), rx * 0.55, ry * 0.55)
            p.fill(mm & ~sh(mm, -1, -1) & erode(m, 2), 'z1')
    for (x, y) in eyes:           # skulls forming in the smoke
        p.grid(*P(x, y), SKULL, dict(d='z3', D='z0', E='e1'))
    c.stamp(p, 'z0')


def nura(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def U(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    # ---- smoke burst behind everything
    if S['puff']:
        smoke_cloud(c, *S['puff'])

    # ---- feet (tabi + zori)
    for fx, ramp in ((S['ffoot'], ('v0', 'v1', 'v2')), (S['nfoot'], ('v1', 'v2', 'v3'))):
        p = C()
        foot = PG([P(fx + 9, 93), P(fx + 9, 97), P(fx - 2, 97), P(fx - 3, 95), P(fx + 1, 93)])
        p.form(foot, ramp, sd=1, hl=1)
        p.fill(R(*P(fx - 4, 98), *P(fx + 10, 99)), 'w1')
        p.fill(R(*P(fx - 4, 98), *P(fx + 10, 98)), 'w2')
        p.line([P(fx + 2, 93), P(fx + 1, 97)], 'm2')          # hanao strap
        c.stamp(p, 'K')

    # ---- haori back panel (behind kimono)
    sw = S['sway']
    p = C()
    back = PG([U((52, 43)), U((69, 44)), U((79, 57), .6), P(85 + sw, 91), P(60 + sw, 92), U((56, 60), .6)])
    p.form(back, HAORI, sd=5, hl=1)
    c.stamp(p, 'K')

    # ---- kimono body
    p = C()
    hm = S['hem']
    body = PG([U((40, 46)), U((60, 44)), U((66, 60), .6), P(68 + hm, 95), P(33 + hm, 95), U((36, 62), .6)])
    p.form(body, KIM, sd=5, hl=1)
    for x0, x1 in ((41, 40 + hm), (52, 53 + hm), (58, 60 + hm)):
        p.line([U((x0 + 2, 72), .5), P(x1, 94)], 'i1', only=body)
    p.line([U((47, 47)), U((44, 64), .7), P(43 + hm, 95)], 'i0', only=body)          # front overlap
    p.line([U((48, 47)), U((45, 64), .7), P(44 + hm, 95)], 'i3', only=body)
    # hem band
    p.fill(R(*P(30, 92), *P(80, 93)), 'i0', only=body)
    # collar: white under-collar V
    col_ = PG([U((43, 45)), U((52, 45)), U((46, 58))])
    p.form(col_, ('v1', 'v2', 'v3'), sd=1, hl=0, only=body)
    p.line([U((44, 45)), U((46, 57))], 'K', only=body)
    # obi
    obi = PG([U((37, 64), .6), U((66, 62), .6), U((66, 69), .6), U((37, 71), .6)])
    p.form(obi, ('w0', 'w1', 'w2'), sd=2, hl=1, only=body)
    p.line([U((37, 67.5), .6), U((66, 65.5), .6)], 'y1', only=body)
    c.stamp(p, 'K')

    # ---- haori front panel (near side) + far lapel
    p = C()
    front = PG([U((53, 43)), U((67, 45)), U((75, 60), .6), P(79 + sw, 90), P(56 + sw, 91), U((52, 62), .6), U((50, 50))])
    p.form(front, HAORI, sd=4, hl=1)
    p.line([U((52, 46)), U((54, 62), .6), P(57 + sw, 90)], 'p3', only=front)       # lapel edge
    p.line([U((60, 62), .6), P(64 + sw, 90)], 'p0', only=front)
    p.line([U((68, 60), .6), P(73 + sw, 90)], 'p0', only=front)
    p.fill(R(*P(40, 88), *P(90, 88)), 'p0', only=front)
    c.stamp(p, 'K')
    p = C()
    lap = PG([U((40, 46)), U((43, 45)), U((40, 62), .6), P(37 + hm, 88), P(33 + hm, 88), U((36, 62), .6)])
    p.form(lap, HAORI, sd=1, hl=1)
    c.stamp(p, 'K')
    # haori-himo (gold cord knot)
    kx, ky = U((49, 59), .7)
    c.line([U((41, 58), .7), (kx, ky + 1), U((54, 58), .7)], 'y1')
    c.fill(R(kx - 1, ky, kx + 1, ky + 2), 'y2'); c.fill(R(kx, ky + 3, kx, ky + 5), 'y1')

    # ---- head
    HX, HY = P(lean + S['hx'], bob + S['hy'])

    def Hh(x, y):
        return (x + HX, y + HY)
    p = C()
    neck = L(*Hh(50, 40), 5, *U((52, 47)), 6)
    p.form(neck, ('n0', 'n1', 'n2'), sd=2, hl=0)
    c.stamp(p, 'K')
    p = C()
    # stringy white hair at the nape
    hair = PG([Hh(56, 31), Hh(70, 29), Hh(73, 38), Hh(69, 36), Hh(68, 44), Hh(64, 39), Hh(62, 46), Hh(58, 38)])
    p.form(hair, ('v0', 'v1', 'v2'), sd=2, hl=0)
    for a_, b_ in (((60, 33), (62, 43)), ((65, 32), (67, 41)), ((69, 31), (71, 36))):
        p.line([Hh(*a_), Hh(*b_)], 'v0', only=hair)
    c.stamp(p, 'K')
    p = C()
    skull = E(*Hh(43, 33), 9.6, 10.6) | E(*Hh(60, 21), 17.4, 12.2) | L(*Hh(45, 28), 9, *Hh(58, 21), 12) | E(*Hh(71, 18), 9.4, 8.4)
    jaw = PG([Hh(34, 36), Hh(36, 43), Hh(41, 45), Hh(50, 42), Hh(54, 34)])
    head = skull | jaw
    p.form(head, SKIN, sd=5, hl=1)
    # gourd waist: soft crease between the face lobe and the swollen cranium
    lobe = E(*Hh(62, 20), 16, 11)
    p.form(lobe, SKIN, sd=3, hl=1, only=head)
    p.line([Hh(49, 14), Hh(47, 19), Hh(47, 24)], 'n1', only=head)
    # veins + age spots on the dome
    p.line([Hh(63, 12), Hh(66, 15), Hh(65, 19), Hh(69, 21)], 'n1', only=head)
    p.line([Hh(66, 15), Hh(70, 14)], 'n1', only=head)
    for (x, y) in ((56, 17), (73, 20), (59, 25)):
        p.fill(R(*Hh(x, y), *Hh(x + 1, y + 1)), 'n1', only=head)
    p.fill(R(*Hh(54, 11), *Hh(58, 11)), 'n3', only=head)
    p.fill(R(*Hh(52, 12), *Hh(53, 12)), 'n3', only=head)
    # ear
    ear = E(*Hh(54, 34), 2.6, 3.8)
    p.form(ear, SKIN, sd=1, hl=1)
    p.line([Hh(54, 32), Hh(55, 34), Hh(54, 36)], 'n0')
    p.line([Hh(51, 30), Hh(51, 38)], 'n0', only=head)
    p.grid(*Hh(32, 21), FACE, LEG)
    c.stamp(p, 'K')

    # ---- pipe arm
    sh_, el, wr = U(S['sh']), U(S['el'], .5), P(*S['wr'])
    wr = (wr[0] + lean * 0, wr[1])
    # kiseru
    p = C()
    tip = pol(wr, S['pang'], 13); butt = pol(wr, S['pang'] + 180, 9)
    p.form(L(*butt, 1.1, *tip, 1.1), ('w0', 'm1', 'm2'), sd=1, hl=0)
    p.fill(L(*butt, 1.1, *lerp(butt, tip, 0.18), 1.1), 'y1')
    p.fill(L(*lerp(butt, tip, 0.8), 1.1, *tip, 1.2), 'y1')
    bowl = pol(tip, S['pang'] + 90, 2.5)
    p.form(E(bowl[0], bowl[1], 2.4, 2.4), ('y0', 'y1', 'y2'), sd=1, hl=1)
    p.pxs([(int(bowl[0]), int(bowl[1] - 2)), (int(bowl[0]) + 1, int(bowl[1] - 2))], 'e1')
    c.stamp(p, 'K')
    bw = pol(bowl, 270, 3)
    if S['glow']:
        g = C(); g.fill(star(bowl[0], bowl[1] - 2, 5.5, 1.6), 'e1'); g.fill(star(bowl[0], bowl[1] - 2, 3, 1), 'y3'); c.stamp(g, 'e0')
    # sleeve
    p = C()
    dr = 13
    slv = PG([add(sh_, (-4, -5)), add(sh_, (5, -2)), add(sh_, (6, 10)), add(el, (8, dr - 2)), add(lerp(el, wr, .55), (4, dr + 4)),
              add(wr, (5, 15)), add(wr, (3, 2)), add(wr, (6, -3)), add(lerp(el, wr, .5), (0, -7)), add(el, (-3, -8))])
    p.form(slv, HAORI, sd=4, hl=1)
    for t in (.15, .45, .75):
        q = lerp(el, wr, t)
        p.line([add(q, (2, -2)), add(q, (6 - t * 4, dr + 2))], 'p0', only=slv)
    # crest (mon)
    mx, my = add(sh_, (0, 4))
    p.fill(E(mx, my, 2.6, 2.6), 'y1', only=slv); p.fill(E(mx, my, 1.2, 1.2), 'p0', only=slv)
    # sleeve mouth: grey lining
    mouth = PG([add(wr, (3, 2)), add(wr, (6, 2)), add(wr, (8, 14)), add(wr, (5, 15))])
    p.fill(mouth, 'p0', only=slv)
    p.fill(mouth & R(0, 0, 999, wr[1] + 5), 'i2', only=slv)
    p.line([add(wr, (6, 2)), add(wr, (8, 14))], 'p0', only=slv)
    c.stamp(p, 'K')
    p = C()
    limb(p, add(wr, (5, 1)), 2.6, wr, 2.4, ('n0', 'n1', 'n2'), sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    p.grid(int(wr[0]) - 5, int(wr[1]) - 4, HAND, LEG)
    c.stamp(p, 'K', ring=False)

    # ---- thin curl of pipe smoke
    if S['wisp'] is not None:
        w = S['wisp']
        pts = curve([bw, add(bw, (-2 + w, -5)), add(bw, (2 - w, -10)), add(bw, (-1 + w, -15)), add(bw, (2, -19))], 5)
        p = C()
        p.fill(tube(pts, 1.2, 0.6), 'z2')
        p.fill(E(*add(bw, (2, -20 - (w % 2))), 2.2, 1.7), 'z3')
        c.stamp(p, 'z0')

    c.blacken()
    return c


WALK = [
    dict(bob=0, ffoot=36, nfoot=58, hem=0, wisp=0, sway=0),
    dict(bob=-1, ffoot=42, nfoot=54, hem=1, wisp=1, sway=1),
    dict(bob=0, ffoot=48, nfoot=46, hem=0, wisp=2, sway=0),
    dict(bob=-1, ffoot=42, nfoot=54, hem=-1, wisp=1, sway=-1),
]
ATTACK = [
    dict(lean=2, bob=-1, hy=-1, hx=1, wr=(29, 41), el=(47, 61), wisp=None, sway=-1, glow=True, hem=-1),
    dict(lean=-3, bob=1, wr=(18, 52), el=(40, 62), pang=176, wisp=None, sway=2, ffoot=35, nfoot=58,
         puff=([(-22, 42, 18, 16), (-42, 34, 14, 13), (-40, 56, 13, 11), (-4, 50, 10, 8), (-20, 24, 10, 9), (-57, 46, 9, 8), (-24, 62, 10, 7), (-60, 28, 5, 4), (-8, 30, 5, 4)],
               [(-29, 37), (-47, 30), (-45, 52)])),
    dict(lean=-1, bob=0, wr=(22, 48), el=(42, 62), pang=172, wisp=None, sway=1,
         puff=([(-30, 36, 10, 8), (-50, 30, 8, 7), (-48, 54, 7, 5), (-14, 30, 5, 4), (-62, 42, 5, 4)], [(-35, 32)])),
]

if __name__ == '__main__':
    export(NAME, nura, WALK, ATTACK)
