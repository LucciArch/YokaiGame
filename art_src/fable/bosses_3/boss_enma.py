"""Enma-Daio - king and judge of hell."""
from lib3 import *

NAME = 'boss_enma'
CW, CH = 236, 152
OX, OY = 92, 18            # local baseline y=128
SK = ('r1', 'r2', 'r3')
ROBE = ('m1', 'm2', 'm3')
ROBED = ('m0', 'm1', 'm2')
GOLD = ('y0', 'y1', 'y2')
HAIR = ('h0', 'h1', 'h2')

LEG = dict(zip('KabcdemnowxYZyq', ['K', 'r0', 'r1', 'r2', 'r3', 'r4', 'h0', 'h1', 'h2', 'b2', 'b3', 'y2', 'y3', 'y1', 'q']))
LEG['E'] = 'e0'
MOUTH = """
.KKKKKKKKKKKKKKK.
KxwxxwxxwxxwxxwxK
KxqwqqwqqwqqwqqxK
KxqqqqqqqqqqqqqxK
KqqqqqqqEEEqqqqqK
KxqqqqEEEEEEqqqxK
KxqwqqwqqwqqwqqxK
.KwxxwxxwxxwxxwK.
..KKKKKKKKKKKKK..
"""

FIST = """
..KKKKKK..
.KcdddccK.
KcdeedccbK
KdddddccbK
KaaaadccbK
KdddaccbbK
KaaaadcbaK
KcdddacbaK
.KaaaccbK.
..KKKKKK..
"""


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, hem=0, ffoot=44, nfoot=72,
           fsh=(42, 60), fel=(27, 72), fwr=(16, 62), sang=264,
           nsh=(94, 60), nel=(104, 80), nwr=(88, 90),
           fx=None)


def sleeve_arm(c, sh_, el, wr, ramp, drop, fist_ramp_dark=False):
    p = C()
    up = L(*sh_, 11, *el, 11.5)
    fore = L(*el, 11.5, *wr, 10.5)
    # hanging sleeve bag under the forearm
    bag = PG([add(el, (9, 2)), add(el, (5, drop)), add(lerp(el, wr, .6), (2, drop + 5)), add(wr, (3, drop - 2)), add(wr, (-2, 6)), wr, el])
    m = up | fore | bag
    p.form(m, ramp, sd=4, hl=1)
    for t in (.2, .5, .8):
        q = lerp(el, wr, t)
        p.line([add(q, (3, 1)), add(q, (4 - t * 3, drop + 1))], ramp[0], only=m)
    p.line([lerp(sh_, el, .3), add(el, (-4, -5))], ramp[0], only=m)
    # gold-trimmed cuff
    end = E(*add(wr, (-1, 0)), 8.4, 9.6) & m
    p.form(end, GOLD, sd=2, hl=1)
    p.fill(E(*add(wr, (-1, 0)), 6.0, 7.2) & m, 'v1')
    p.fill(E(*add(wr, (-1, 0)), 4.8, 6.0) & m, 'm0')
    edge = bag & ~sh(bag, 0, -2) & ~up & ~fore
    p.fill(edge, 'y1')
    c.stamp(p, 'K')
    p = C()
    p.grid(int(wr[0]) - 7, int(wr[1]) - 5, FIST, LEG)
    c.stamp(p, 'K', ring=False)


def shaku(c, hand, ang):
    """ritual tablet through the fist; ang = direction of the tip"""
    p = C()
    tip = pol(hand, ang, 36); butt = pol(hand, ang + 180, 10)
    n = pol((0, 0), ang + 90, 1)
    w0, w1 = 2.0, 3.0
    m = PG([add(butt, (n[0] * w0, n[1] * w0)), add(tip, (n[0] * w1, n[1] * w1)),
            add(tip, (-n[0] * w1, -n[1] * w1)), add(butt, (-n[0] * w0, -n[1] * w0))])
    p.form(m, ('b1', 'b2', 'b3'), sd=2, hl=1)
    p.line([lerp(butt, tip, .25), lerp(butt, tip, .9)], 'b1', only=erode(m, 1))
    c.stamp(p, 'K')


def enma(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, hm = S['bob'], S['lean'], S['hem']

    def U(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    fx = S['fx']
    if fx:
        fx(c)

    # ---- boots
    for fx_, ramp in ((S['ffoot'], ('h0', 'h0', 'h1')), (S['nfoot'], HAIR)):
        p = C()
        boot = PG([P(fx_ + 12, 119), P(fx_ + 12, 127), P(fx_ - 6, 127), P(fx_ - 8, 123), P(fx_ - 5, 121), P(fx_ - 1, 122), P(fx_ + 2, 119)])
        p.form(boot, ramp, sd=1, hl=1)
        p.fill(R(*P(fx_ - 6, 126), *P(fx_ + 12, 127)), 'b1')
        c.stamp(p, 'K')

    # ---- robe: great bell
    p = C()
    robe = PG([U((40, 52)), U((96, 52)), U((106, 74), .6), P(114 + hm, 119), P(104 + hm, 123), P(90 + hm, 121), P(74 + hm, 124), P(60 + hm, 122), P(46 + hm, 124), P(34 + hm, 121), P(24 + hm, 123), U((32, 74), .6)])
    robe |= E(*U((68, 62)), 33, 14)
    p.form(robe, ROBE, sd=7, hl=1)
    core = robe & ~sh(robe, -3, -3)
    p.fill(core & (p.a == I('m1')), 'm0')
    for (x0, x1) in ((40, 36), (52, 49), (80, 83), (92, 97), (100, 106)):
        p.line([U((x0, 84), .4), P(x1 + hm, 121)], 'm1', only=robe)
        p.line([U((x0 + 1, 84), .4), P(x1 + 1 + hm, 121)], 'm0', only=robe & ~sh(robe, -7, -7))
    # front panel with gold border (centre-left)
    panel = PG([U((56, 66), .8), U((74, 66), .8), P(77 + hm, 126), P(55 + hm, 126)])
    p.form(panel, ROBED, sd=3, hl=0, only=robe)
    for xa, xb in ((56, 55), (74, 77)):
        p.line([U((xa, 66), .8), P(xb + hm, 126)], 'y1', only=robe)
    # flame-cloud emblems on the panel
    for y in (94, 107):
        q = U((65, y), .3)
        p.fill((E(q[0], q[1], 4.4, 3.4) & ~E(q[0], q[1], 2.2, 1.6)), 'y1', only=panel & robe)
        p.fill(R(q[0] - 1, q[1] - 6, q[0], q[1] - 4), 'y1', only=panel & robe)
    # hem band
    hemb = robe & ~sh(robe, 0, -7) & R(0, OY + 100, 999, 999)
    p.form(hemb, GOLD, sd=2, hl=1)
    p.fill(hemb & sh(~hemb, 0, 3) & sh(hemb, 0, 2), 'y0')
    # sash
    sash = PG([U((30, 80), .6), U((110, 78), .6), U((110, 86), .6), U((30, 88), .6)])
    p.form(sash, HAIR, sd=2, hl=1, only=robe)
    bx, by = U((65, 83), .6)
    p.form(E(bx, by, 5.4, 4.4), GOLD, sd=1, hl=1)
    p.fill(E(bx, by, 2.2, 1.6), 'e0')
    # collar: white inner + gold lapels meeting under the beard
    col_ = PG([U((50, 50)), U((84, 50)), U((66, 74))])
    p.form(col_, ('v1', 'v2', 'v3'), sd=2, hl=0, only=robe)
    p.line([U((50, 50)), U((66, 74)), U((84, 50))], 'y1', only=robe)
    p.line([U((49, 51)), U((66, 75)), U((85, 51))], 'y0', only=robe)
    # shoulder mantle (dark, gold edge)
    for cx_ in (44, 92):
        mm = E(*U((cx_, 58)), 14, 8) & robe
        p.form(mm, ROBE, sd=2, hl=1)
        p.fill(mm & ~sh(mm, 0, -2), 'y1')
    c.stamp(p, 'K')

    # ---- near arm (fist on the sash)
    sleeve_arm(c, U(S['nsh']), U(S['nel'], .6), U(S['nwr'], .6), ROBE, 22)

    # ---- head (built from forms; mouth is a text grid)
    HX, HY = U((45, 6))

    def Hh(x, y):
        return (HX + x, HY + y)
    # back hair
    p = C()
    bh = PG([Hh(22, 4), Hh(42, 8), Hh(47, 26), Hh(50, 44), Hh(44, 40), Hh(42, 48), Hh(36, 40), Hh(30, 30)])
    p.form(bh, HAIR, sd=3, hl=0)
    for a_, b_ in (((40, 14), (46, 38)), ((36, 16), (41, 42))):
        p.line([Hh(*a_), Hh(*b_)], 'h2', only=bh)
    c.stamp(p, 'K')
    # crown wing + board behind
    p = C()
    wing = PG([Hh(30, 0), Hh(56, -5), Hh(58, 0), Hh(34, 6)])
    p.form(wing, HAIR, sd=1, hl=1)
    p.form(E(*Hh(57, -3), 3.4, 3.4), GOLD, sd=1, hl=1)
    c.stamp(p, 'K')
    # face
    p = C()
    face = E(*Hh(21, 21), 18.4, 17.4) | PG([Hh(4, 24), Hh(8, 38), Hh(20, 44), Hh(36, 36), Hh(39, 22)])
    p.form(face, SK, sd=6, hl=1)
    cheek = E(*Hh(27, 27), 7.4, 5.4)
    p.form(cheek, SK, sd=2, hl=1, only=face)
    p.form(E(*Hh(8, 27), 4.4, 4.4), SK, sd=1, hl=1, only=face)
    # forehead furrows
    p.line([Hh(8, 9), Hh(16, 8), Hh(26, 7)], 'r1', only=face)
    p.line([Hh(13, 11), Hh(13, 15)], 'r0', only=face)
    p.line([Hh(15, 10), Hh(15, 14)], 'r0', only=face)
    # nose
    nose = E(*Hh(11, 25), 5.4, 4.4)
    p.form(nose, SK, sd=2, hl=1)
    p.line([Hh(13, 14), Hh(12, 20)], 'r1', only=face)
    p.fill(R(*Hh(8, 23), *Hh(10, 23)), 'r4')
    p.fill(R(*Hh(8, 28), *Hh(9, 28)) | R(*Hh(13, 28), *Hh(14, 28)), 'r0')
    c.stamp(p, 'r0')
    # eyes: bulging, glaring
    for (ex, ey, rx, ry, pd) in ((25, 19, 5.9, 4.4, -2), (6.5, 19, 3.6, 4.2, -1)):
        o = Hh(ex, ey)
        c.fill(E(o[0], o[1], rx + 1.5, ry + 1.5), 'r0')
        c.fill(E(o[0], o[1], rx, ry), 'y2')
        c.fill(E(o[0], o[1], rx, ry) & ~sh(E(o[0], o[1], rx, ry), -1, -2), 'y1')
        c.fill(E(o[0] + pd, o[1] + 1, 2.3, 2.3) & E(o[0], o[1], rx, ry), 'e0')
        c.fill(R(o[0] + pd - 1, o[1], o[0] + pd, o[1] + 1), 'K')
        c.fill(R(o[0] + pd + 2, o[1] + 2, o[0] + pd + 3, o[1] + 2) & E(o[0], o[1], rx, ry), 'y3')
    # brows: thick black flames, inner ends low
    p = C()
    nb = PG([Hh(16, 19), Hh(17, 13), Hh(30, 7), Hh(38, 4), Hh(36, 11), Hh(30, 14), Hh(22, 17)])
    fb = PG([Hh(11, 19), Hh(10, 13), Hh(4, 9), Hh(-1, 8), Hh(1, 14), Hh(6, 17)])
    p.form(nb | fb, HAIR, sd=1, hl=1)
    c.stamp(p, 'K')
    # beard
    p = C()
    beard = PG([Hh(2, 24), Hh(-1, 36), Hh(3, 34), Hh(2, 46), Hh(8, 42), Hh(9, 54), Hh(15, 48), Hh(19, 62), Hh(24, 50), Hh(30, 56),
                Hh(31, 46), Hh(37, 48), Hh(36, 38), Hh(41, 36), Hh(39, 22), Hh(33, 30), Hh(24, 32), Hh(14, 30), Hh(6, 31)])
    p.form(beard, HAIR, sd=4, hl=0)
    for a_, b_ in (((6, 36), (5, 44)), ((11, 42), (12, 51)), ((17, 44), (19, 58)), ((24, 42), (25, 49)), ((29, 40), (30, 52)), ((34, 36), (35, 45))):
        p.line([Hh(*a_), Hh(*b_)], 'h2', only=beard)
    for a_, b_ in (((14, 44), (15, 52)), ((21, 44), (21, 56)), ((32, 38), (33, 44))):
        p.line([Hh(*a_), Hh(*b_)], 'h0', only=beard)
    c.stamp(p, 'K')
    p = C()
    p.grid(*Hh(4, 31), MOUTH, LEG)
    c.stamp(p, 'K', ring=False)
    # moustache sweeping outward
    p = C()
    mst = tube(curve([Hh(13, 29), Hh(22, 29), Hh(29, 33), Hh(34, 31)], 5), 2.6, 0.8) | tube(curve([Hh(10, 29), Hh(4, 30), Hh(0, 34), Hh(-3, 32)], 5), 2.4, 0.8)
    p.form(mst, HAIR, sd=1, hl=1)
    c.stamp(p, 'K')
    # ear with long lobe + ring
    p = C()
    ear = E(*Hh(38, 21), 3.0, 5.4) | E(*Hh(38, 27), 2.2, 3.2)
    p.form(ear, SK, sd=1, hl=1)
    p.line([Hh(38, 18), Hh(39, 22), Hh(38, 25)], 'r0')
    c.stamp(p, 'r0')
    c.fill(E(*Hh(38, 32), 2.2, 2.2) & ~E(*Hh(38, 32), 0.9, 0.9), 'y2')
    # crown: cap, gold band, plaque, board, bead curtains
    p = C()
    cap = E(*Hh(21, 4), 17.4, 9.4) & R(0, 0, 999, HY + 5)
    p.form(cap, HAIR, sd=3, hl=1)
    c.stamp(p, 'K')
    p = C()
    band = PG([Hh(4, 1), Hh(38, -2), Hh(39, 5), Hh(4, 7)])
    p.form(band, GOLD, sd=2, hl=1)
    for x in (22, 28, 34):
        p.fill(R(*Hh(x, 1), *Hh(x + 1, 2)), 'e1')
    c.stamp(p, 'K')
    p = C()
    board = PG([Hh(-8, -10), Hh(46, -15), Hh(48, -11), Hh(-6, -6)])
    p.form(board, HAIR, sd=1, hl=1)
    p.line([Hh(-7, -8), Hh(47, -13)], 'y1', only=board)
    c.stamp(p, 'K')
    for bx_, n_, up in ((-6, 5, 0), (-1, 4, 0), (40, 5, -4), (45, 5, -5)):
        for j in range(n_):
            yy = -4 + up + j * 3 + (bob if j >= n_ - 2 else 0)
            q = Hh(bx_, yy)
            c.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 'y2' if j % 2 == 0 else 'e1')
            if j < n_ - 1:
                c.fill(R(q[0], q[1] + 2, q[0], q[1] + 2), 'y0')
    p = C()
    plq = R(*Hh(6, -9), *Hh(19, 6))
    p.form(plq, GOLD, sd=2, hl=1)
    p.fill(R(*Hh(8, -7), *Hh(17, 4)), 'm1')
    p.fill(star(HX + 12.5, HY - 1.5, 5, 3.2, 4), 'y2')
    p.fill(R(*Hh(12, -2), *Hh(13, -1)), 'e1')
    c.stamp(p, 'K')

    # ---- far arm with the shaku (in front)
    sh_, el, wr = U(S['fsh']), U(S['fel'], .5), P(*S['fwr'])
    shaku(c, wr, S['sang'])
    sleeve_arm(c, sh_, el, wr, ROBE, 24)

    c.blacken()
    return c


def fx_wind(c):
    # gathering light at the raised tablet
    p = C()
    o = P(20, 0)
    p.fill(star(o[0], o[1], 9, 2.2), 'y1'); p.fill(star(o[0], o[1], 5, 1.4), 'y3')
    c.stamp(p, 'y0')


def fx_strike(k=1.0):
    def f(c):
        p = C()
        # falling beam of judgment + ground burst
        x0 = -52
        beam = PG([P(x0, -15), P(x0 + 8 * k, 6), P(x0 + 4 * k, 122), P(x0 - 4 * k, 122), P(x0 - 8 * k, 6)])
        for yy, rr in ((30, 15), (62, 11)):
            beam |= (E(*P(x0, yy), rr * k, 4 * k) & ~E(*P(x0, yy - 1), (rr - 2.5) * k, 2.2 * k)) if k >= 1 else np.zeros_like(beam)
        burst = np.zeros_like(beam)
        for a, r in ((180, 30), (200, 22), (225, 26), (250, 18), (290, 18), (315, 26), (340, 22), (0, 30)):
            burst |= tongue(P(x0, 124), pol(P(x0, 124), a, r * k), 4.5 * k, 0)
        burst &= R(0, 0, 999, OY + 127)
        m = beam | burst
        p.form(m, ('y0', 'y1', 'y2'), sd=1, hl=0)
        inner = erode(m, 2)
        p.fill(inner, 'y2'); p.fill(erode(m, 4), 'y3')
        p.fill(m & ~erode(m, 1), 'e1')
        c.stamp(p, 'K')
        if k >= 1:
            # arc trail of the tablet
            q = C()
            arc = (E(*P(14, 62), 42, 52) & ~E(*P(18, 66), 40, 50)) & R(0, 0, OX + 8, OY + 86)
            q.fill(arc, 'y2'); q.fill(arc & ~sh(arc, 1, 1), 'y3')
            c.stamp(q, 'y1')
    return f


WALK = [
    dict(bob=0, ffoot=38, nfoot=76, hem=0),
    dict(bob=-1, ffoot=46, nfoot=70, hem=1, fwr=(20, 59)),
    dict(bob=0, ffoot=54, nfoot=62, hem=0),
    dict(bob=-1, ffoot=46, nfoot=70, hem=-1, fwr=(20, 59)),
]
ATTACK = [
    dict(lean=3, bob=-2, fsh=(44, 54), fel=(28, 46), fwr=(22, 28), sang=282, fx=fx_wind, hem=-1),
    dict(lean=-4, bob=2, fsh=(44, 58), fel=(26, 70), fwr=(8, 78), sang=172, fx=fx_strike(1.0), hem=2, ffoot=38, nfoot=76),
    dict(lean=-2, bob=1, fsh=(44, 57), fel=(28, 70), fwr=(14, 70), sang=205, fx=fx_strike(0.5), hem=1),
]

if __name__ == '__main__':
    export(NAME, enma, WALK, ATTACK)
