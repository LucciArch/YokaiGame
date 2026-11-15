"""Yuki-onna (~90 px): snow woman, floating, no feet. Head = fixed text grid. Local baseline (hem tip) y=100."""
from k2 import *

NAME = 'boss_yuki_onna'
CW, CH = 176, 124
OX, OY = 78, 16
WH = ('v1', 'v2', 'v3')
WHF = ('v0', 'v1', 'v2')
HAIR = ('h0', 'hb', 'h2')
SKN = ('u1', 'u2', 'u3')
OBI = ('i1', 'i2', 'i3')
ICE = ('a0', 'a1', 'a2')

LEG = dict(zip('mnoabcdKEWAr', ['h0', 'hb', 'h2', 'u0', 'u1', 'u2', 'u3', 'K', 'a2', 'v3', 'a1', 'e0']))
HEAD = """
.......mmmmmmm......
.....mmnnnnnnnmm....
....mnnooonnnnnnm...
...mnnoonnnnnnnnnm..
..mnnoonnnnnnnnnnnm.
..mnnonnnnnnnnnnnnm.
.mnnnnnnnnnnnnnnnnnm
.mnnnnnnnnnnnnnnnnnm
.mnmnnmnnnmnnnnnnnnm
.mdmddmdddmnmnnnnnnm
.mdcccccccdmnmnnnnnm
.KKccccccKKKmnnnnnnm
.dcKKccKKKKbmnnnnnnm
.dEWbccAEWKbmnnnnnnm
.dccbccccbbbmnnnnnnm
..dcccccccbbmnnnnnnm
..dcbcccccbbmnnnnnm.
..ddccccccbamnnnnnm.
...crrrccbbamnnnnnm.
...dccaccbba.mnnnnm.
....dcccbba..mnnnnm.
.....dbbba...mnnnm..
"""
HAND = """
....ccc.
..ccdccb
.cdccccb
cdccbbb.
dcbcb...
cb.b....
d.......
"""
HAND_UP = """
.d.c....
.c.cb...
.cdccb..
.cdccb..
..cccb..
..bcbb..
"""
FLAKE = """
.W.
WEW
.W.
"""
FLAKE_B = """
..W..
.WEW.
WEAEW
.WEW.
..W..
"""

DEF = dict(bob=0, lean=0, hair=0, hem=0, sl=0,
           fsh=(37, 33), felb=(28, 42), fwr=(17, 39),
           nsh=(50, 34), nelb=(56, 46), nwr=(46, 50), nhand_up=False,
           breath=0, fl=0)


def P(x, y):
    return (x + OX, y + OY)


def yuki(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    b = S['bob']; ln = S['lean']; hr = S['hair']; hm = S['hem']; sl = S['sl']

    def B(pt, k=1.0):                       # upper body: bob + lean (lean scaled by height above the waist)
        return P(pt[0] + ln * k, pt[1] + b)

    def T(pt):                              # torso points lean proportionally to height
        k = max(0.0, min(1.0, (60 - pt[1]) / 40.0))
        return P(pt[0] + ln * k, pt[1] + b)

    HX, HY = P(28 + ln, 6 + b)
    HX, HY = int(round(HX)), int(round(HY))

    # ---- back hair: long black curtain streaming to the right
    p = C()
    hp = [(42, 10), (50, 12), (54, 20), (56, 32), (61, 44), (67 + hr, 56), (79 + hr * 2, 63), (69 + hr, 66), (76 + hr * 2, 78),
          (64 + hr, 74), (66 + hr, 87), (57, 77), (53, 62), (50, 44), (46, 28)]
    hair = PG([T(q) for q in hp])
    p.form(hair, HAIR, sd=3, hl=0)
    for a_, b_ in [((52, 22), (64 + hr, 56)), ((52, 36), (60 + hr, 70)), ((57, 42), (72 + hr * 2, 66))]:
        p.line([T(a_), T(lerp(a_, b_, 0.5)), T(b_)], 'h2', only=hair)
    for a_, b_ in [((50, 26), (57, 64)), ((55, 36), (67 + hr, 64))]:
        p.line([T(a_), T(b_)], 'h0', only=hair)
    c.stamp(p, 'K')

    # ---- far arm + its long sleeve
    fs, fe, fw = T(S['fsh']), B(S['felb']), B(S['fwr'])
    p = C()
    drop = 25
    slv = PG([add(fs, (1, -3)), add(fe, (0, -4)), add(fw, (1, -4)), add(fw, (-1, 3)), add(fw, (3 + sl, drop * 0.5)), add(fw, (1 + sl * 2, drop)),
              add(fe, (4 + sl * 2, drop + 3)), add(fe, (7 + sl, 10)), add(fs, (3, 10))])
    p.form(slv, WHF, sd=3, hl=1)
    p.line([add(fe, (0, 2)), add(fe, (2 + sl, drop))], 'v0', only=slv)
    p.line([add(fw, (4, 4)), add(fw, (4 + sl, drop - 4))], 'v0', only=slv)
    p.line([add(fw, (1 + sl * 2, drop - 2)), add(fe, (4 + sl * 2, drop + 1))], 'a1', only=slv)   # icy hem band
    c.stamp(p, 'K')
    p = C()
    p.grid(int(round(fw[0])) - 8, int(round(fw[1])) - 3, HAND, LEG)
    c.stamp(p, 'u0')

    # ---- icy mist curling around the hem (aura)
    for (x, y, a, l_, w, bd) in [(36, 93, 196, 20, 8, 46), (58, 97, 350, 26 + hm, 8, -40), (46, 99, 168, 15, 6, 40)]:
        p = C()
        m = lock(P(x, y + b * 0.5), a + hm * 2, l_, w, bd)
        p.fill(m, 'a0'); p.fill(erode(m, 1), 'a1'); p.fill(erode(m, 2), 'a2')
        c.stamp(p, 'K', skip=('a0', 'a1', 'a2'))

    # ---- kimono skirt: flares, then trails away to the right as a wisp (no feet)
    p = C()
    sk = [(35, 54), (32, 66), (30, 80), (33, 90), (41, 96), (52, 99), (64 + hm, 100), (76 + hm * 2, 97 - abs(hm) * 0.5), (68 + hm, 94), (61, 88),
          (58, 74), (56, 62), (54, 54)]
    skirt = PG([P(x + ln * max(0, (60 - y) / 40.0), y + b * (1 if y < 96 else 0.5)) for x, y in sk])
    p.form(skirt, WH, sd=4, hl=1)
    for (a_, b_) in [((42, 57), (38, 92)), ((47, 57), (48, 96)), ((51, 58), (57 + hm, 96))]:
        p.line([P(a_[0], a_[1] + b), P(lerp(a_, b_, 0.5)[0] - 1, lerp(a_, b_, 0.5)[1] + b), P(b_[0], b_[1] + b)], 'v1', only=skirt)
    p.line([P(39, 60 + b), P(34, 86 + b)], 'v3', only=erode(skirt, 1))
    # frost-blue hem
    hemz = skirt & ~sh(skirt, 0, -3) & (px.Y > OY + 84)
    p.fill(hemz, 'a1')
    c.stamp(p, 'K')
    # front overlap panel (left over right) edge
    c.line([T((43, 55)), P(40, 76 + b), P(43, 95 + b)], 'v0', only=skirt)

    # ---- torso
    p = C()
    torso = PG([T((35, 30)), T((43, 28)), T((51, 30)), T((54, 47)), T((35, 47))])
    p.form(torso, WH, sd=3, hl=1)
    # collar: V of layered lapels + bare throat
    p.fill(PG([T((39, 28)), T((45, 28)), T((42, 38))]) & torso, 'u1')
    p.fill(PG([T((40, 28)), T((43, 28)), T((41, 34))]) & torso, 'u2')
    p.line([T((38, 29)), T((42, 39)), T((44, 46))], 'v0', only=torso)
    p.line([T((46, 29)), T((42, 39))], 'v0', only=torso)
    p.line([T((37, 30)), T((41, 40))], 'a1', only=torso)
    c.stamp(p, 'K')
    # ---- obi
    p = C()
    obi = PG([T((34, 46)), T((54, 45)), T((55, 55)), T((34, 55))])
    p.form(obi, OBI, sd=2, hl=1)
    p.line([T((35, 50)), T((54, 49))], 'a2', only=obi)       # obijime cord
    knot = E(*T((56, 49)), 4.6, 6.4)
    p.form(knot, OBI, sd=2, hl=1)
    c.stamp(p, 'K')

    # ---- near arm + sleeve
    ns, ne, nw = T(S['nsh']), B(S['nelb']), B(S['nwr'])
    p = C()
    drop = 24
    if S['nhand_up']:
        slv = PG([add(ns, (-3, -3)), add(ns, (5, 0)), add(ne, (5, 2)), add(ne, (4 - sl, drop)), add(ne, (-7 - sl, drop - 2)), add(nw, (4, 6)),
                  add(nw, (-3, 3)), add(nw, (-2, -3))])
    else:
        slv = PG([add(ns, (-3, -3)), add(ns, (5, 0)), add(ne, (4, -1)), add(ne, (4 - sl, drop)), add(ne, (-8 - sl * 2, drop + 2)), add(nw, (0, 5)),
                  add(nw, (-3, 2)), add(nw, (-2, -4))])
    p.form(slv, WH, sd=3, hl=1)
    p.line([add(ne, (-1, 3)), add(ne, (-2 - sl, drop - 1))], 'v1', only=slv)
    p.line([add(ns, (0, 4)), add(ne, (-3, 0)), add(nw, (2, 1))], 'v1', only=slv)
    p.line([add(ne, (4 - sl, drop - 2)), add(ne, (-8 - sl * 2, drop))], 'a1', only=slv)
    c.stamp(p, 'K')
    p = C()
    if S['nhand_up']:
        p.grid(int(round(nw[0])) - 5, int(round(nw[1])) - 6, HAND_UP, LEG)
    else:
        p.grid(int(round(nw[0])) - 7, int(round(nw[1])) - 3, HAND, LEG)
    c.stamp(p, 'u0')

    # ---- head
    p = C()
    p.fill(R(HX + 6, HY + 20, HX + 10, HY + 25), 'u1')      # neck
    p.fill(R(HX + 9, HY + 20, HX + 10, HY + 25), 'u0')
    p.fill(R(HX + 6, HY + 21, HX + 9, HY + 21), 'u0')
    c.stamp(p, ring=False)
    p = C()
    p.grid(HX, HY, HEAD, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # long side lock in front of the shoulder
    p = C()
    lk = tube(curve([(HX + 13, HY + 18), (HX + 14 + hr * 0.3, HY + 27), (HX + 13 + hr * 0.5, HY + 35), (HX + 15 + hr, HY + 43)], 6), [(0, 1.5), (0.7, 1.3), (1, 0.6)])
    p.form(lk, HAIR, sd=1, hl=0)
    c.stamp(p, 'K', skip=('h0', 'hb'))

    # ---- freezing breath (attack)
    br = S['breath']
    if br:
        mx, my = HX + 2, HY + 18
        L_ = br
        p = C()
        cone = PG([(mx, my - 1), (mx - L_ * 0.5, my - L_ * 0.2), (mx - L_, my - L_ * 0.34), (mx - L_ * 1.04, my + L_ * 0.02), (mx - L_, my + L_ * 0.36),
                   (mx - L_ * 0.5, my + L_ * 0.24), (mx, my + 2)])
        for (t, dy, r) in [(0.55, -0.2, 0.13), (0.8, -0.26, 0.15), (0.98, -0.05, 0.17), (0.82, 0.27, 0.15), (0.55, 0.2, 0.12), (1.0, 0.2, 0.13)]:
            cone |= E(mx - L_ * t, my + L_ * dy, L_ * r, L_ * r * 0.9)
        p.fill(cone, 'a0')
        c1 = erode(cone, 2)
        p.fill(c1, 'a1')
        c2 = erode(cone, 5) | (L(mx - 2, my, 1.5, mx - L_ * 0.7, my, L_ * 0.12) & c1)
        p.fill(c2, 'a2')
        p.fill(erode(c2, 2) | (L(mx - 3, my, 0.8, mx - L_ * 0.6, my, L_ * 0.05) & c2), 'v3')
        c.stamp(p, 'K')
        # ice shards riding the front of the cloud
        for (t, dy, a, ln_) in [(1.0, -0.3, 200, 0.22), (1.08, 0.0, 180, 0.26), (1.0, 0.3, 160, 0.22), (0.7, -0.3, 215, 0.16), (0.72, 0.32, 145, 0.16)]:
            p = C()
            m = tri((mx - L_ * t, my + L_ * dy), a, L_ * ln_, max(3.2, L_ * 0.07))
            p.form(m, ('a1', 'a2', 'v3'), sd=1, hl=1)
            c.stamp(p, 'K')

    # ---- drifting snow crystals (icy aura)
    fl = S['fl']
    for i, (x, y, g) in enumerate([(14, 18, FLAKE_B), (64, 22, FLAKE), (8, 60, FLAKE), (72, 50, FLAKE_B), (24, 80, FLAKE), (60, 6, FLAKE), (82, 80, FLAKE)]):
        dx, dy = [(0, 0), (-2, 2), (-3, 4), (-1, 6)][(fl + i) % 4]
        if br and x < 30:
            continue
        p = C()
        p.grid(OX + x + dx, OY + y + dy, g, LEG)
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(bob=0, hair=0, hem=0, sl=0, fl=0), dict(bob=-1, hair=2, hem=2, sl=1, fl=1),
        dict(bob=-2, hair=3, hem=3, sl=1, fl=2), dict(bob=-1, hair=1, hem=1, sl=0, fl=3)]
ATTACK = [dict(bob=-2, lean=4, hair=-3, hem=-2, sl=-1, fwr=(22, 44), felb=(31, 44), nelb=(55, 42), nwr=(42, 30), nhand_up=True, fl=1),
          dict(bob=1, lean=-6, hair=5, hem=4, sl=2, fwr=(14, 46), felb=(27, 45), nelb=(57, 45), nwr=(49, 50), breath=60, fl=2),
          dict(bob=0, lean=-3, hair=3, hem=2, sl=1, fwr=(16, 42), felb=(28, 43), breath=26, fl=3)]

if __name__ == '__main__':
    export(NAME, yuki, WALK, ATTACK)
