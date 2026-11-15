"""Susanoo - storm god: wild hair, headband, white robes, Kusanagi sword, magatama necklace, crackling lightning."""
from herolib import *

NAME = 'susanoo'
L_ = dict(LEG, e='a1', E='a2', R='m3', r='m2', s='m1')
HEAD = """
......m.....m....m....
.....mnm...mnm..mnm...
.....mnnm.mnnnmmnnm.m.
....mnonnmnnonnnnnmmnm
...mnoonnnnonnnnnnnnnm
..mnoonnnnnnnnnnnnnnnm
..mnnnnnnnnnnnnnnnnnnm
.mRRRRRRRRRrrrrrnnnnm.
.mrrrrrrrrrrrssssnnnnm
.mnmnnmnnnmnnnnnnnnnm.
.mcmccmccmnmnnnnnnnnnm
.cKKcccKKKKcmnnnnnnnm.
.ccKKccKKKccbmnnnnnnnm
.cKEccKeEbbcmnnnnnnm..
..ccbcccccbbmnnnnnnnm.
..cccccccbbmmnnnnnm...
..mcaaccbmmm.mnnnnnm..
..mmcccmmm...mnnnm....
...mmmmm......mnm.....
"""
DEF = dict(bob=0, lean=0, nsh=(46, 29), nelb=(40, 38), nwr=(29, 34), wang=104, ffoot=29, nfoot=45, flift=0, nlift=0,
           hair=0, sleeve=0, bolts=0, slash=None, arm_back=False, big=None)

# small crackle sets around the blade: offsets along (t = distance up the blade, side px)
CRACKLE = [
    [[(8, -3), (11, -5), (13, -3), (16, -6)], [(20, 3), (23, 5), (25, 3), (28, 6)]],
    [[(12, 3), (15, 6), (17, 4), (20, 7)], [(22, -3), (25, -6), (27, -4), (31, -6)]],
]


def bolt(c, pts, core='y3', glow='a2'):
    p = C()
    m = LN(pts)
    p.fill(dil(m), glow)
    p.fill(m, core)
    c.stamp(p, ring=False)


def kusanagi(g, wr, ang, bolts):
    c = g.c
    dx, dy = vec(ang)
    nx, ny = -dy, dx
    pom = (wr[0] - dx * 5, wr[1] - dy * 5)
    gd = (wr[0] + dx * 3.5, wr[1] + dy * 3.5)
    b0 = (wr[0] + dx * 5, wr[1] + dy * 5)
    b1 = (wr[0] + dx * 25, wr[1] + dy * 25)
    tip = (wr[0] + dx * 32, wr[1] + dy * 32)
    p = C()
    p.form(L(*pom, 1.2, *gd, 1.2), GOLD, sd=1, hl=0)
    p.form(E(pom[0] - dx * 1.5, pom[1] - dy * 1.5, 2.3, 2.3), GOLD, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    bl = L(*b0, 1.5, *b1, 2.3) | L(*b1, 2.3, *tip, 0.5)
    p.form(bl, IRON, sd=1, hl=1)
    p.line([b0, tip], 'v3', only=bl)
    c.stamp(p, 'K')
    p = C()
    p.form(L(gd[0] - nx * 2.6, gd[1] - ny * 2.6, 1.2, gd[0] + nx * 2.6, gd[1] + ny * 2.6, 1.2), GOLD, sd=1, hl=0)
    c.stamp(p, 'K')
    if bolts is not None:
        for zz in CRACKLE[bolts % 2]:
            bolt(c, [(wr[0] + dx * t + nx * s_, wr[1] + dy * t + ny * s_) for t, s_ in zz])
    return tip


def susanoo(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S)
    c, B, P = g.c, g.B, g.P
    hs = S['hair']

    # ---- wild mane down the back
    p = C()
    mn = PG([B((43, 14)), B((51, 15)), B((57 + hs, 19)), B((54 + hs, 23)), B((60 + hs * 2, 29)), B((55 + hs * 2, 32)),
             B((61 + hs * 2, 40)), B((55 + hs * 2, 40)), B((57 + hs * 2, 49)), B((51 + hs, 44)), B((50 + hs, 51)), B((46, 44)), B((44, 30))])
    p.form(mn, HAIR, sd=2, hl=0)
    p.line([B((48, 22)), B((52 + hs, 31)), B((53 + hs * 2, 40))], 'h2', only=mn)
    p.line([B((46, 26)), B((48 + hs, 36)), B((50 + hs, 44))], 'h0', only=mn)
    c.stamp(p, 'K')

    # ---- far sleeve
    p = C()
    fs = PG([B((35, 28)), B((31, 32)), B((30, 40)), B((37, 42)), B((40, 30))])
    p.form(fs, WHD, sd=2, hl=1)
    c.stamp(p, 'K')

    # bare shins
    for w_, ramp in (('f', ('k0', 'k1', 'k2')), ('n', SKN)):
        fx, lift = S[w_ + 'foot'], S[w_ + 'lift']
        p = C()
        x0, y0 = P(fx, 66 - lift)
        p.form(L(x0 + 5, y0 - 10, 3.0, x0 + 5, y0, 2.3), ramp, sd=1, hl=1)
        p.fill(R(x0 + 3, y0 - 2, x0 + 7, y0 - 2), 'c1')          # sandal ankle tie
        c.stamp(p, 'K')
    g.feet('waraji')
    # ---- white hakama gathered under the knee with red cords
    p, hk = g.hakama(WH, 'v0', waist=(34, 47), flare=(30, 51), stamp=False, hem=59)
    f_, n_ = S['ffoot'], S['nfoot']
    band = hk & (px.Y >= P(0, 56)[1]) & (px.Y <= P(0, 57)[1])
    p.fill(band, 'm2')
    p.fill(hk & (px.Y == P(0, 55)[1]), 'v1')
    c.stamp(p, 'K')
    # sash + hanging ends
    p = C()
    p.form(R(*B((34, 36)), *B((47, 39))), RD, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    tl = PG([B((43, 39)), B((46, 39)), B((47 + S['sleeve'], 49)), B((44 + S['sleeve'], 48))])
    p.form(tl, RD, sd=1, hl=0)
    c.stamp(p, 'K')

    # ---- torso
    p = C()
    torso = L(*B((40, 29)), 6.6, *B((41, 35)), 6.0)
    p.form(torso, WH, sd=3, hl=1)
    p.line([B((36, 25)), B((40, 33))], 'v0', only=torso)
    p.line([B((44, 25)), B((40, 34)), B((40, 37))], 'v1', only=torso)
    c.stamp(p, 'K')
    p = C()
    p.form(R(*B((38, 23)), *B((41, 25))), ('k0', 'k1', 'k2'), sd=1, hl=0)
    c.stamp(p, 'K', ring=False)
    # ---- magatama necklace
    for k, (bx, by) in enumerate(((34, 26), (34, 29), (36, 32), (39, 34), (42, 32))):
        q = B((bx, by))
        p = C()
        if k == 2:
            p.fill(R(q[0], q[1], q[0] + 2, q[1] + 1), 'g3'); p.fill(R(q[0], q[1] + 2, q[0] + 1, q[1] + 3), 'g3'); p.px(q[0] + 1, q[1], 'g4')
            p.px(q[0], q[1] + 3, 'g2')
        else:
            p.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 'g3' if k % 2 == 0 else 'y1'); p.px(q[0], q[1], 'g4' if k % 2 == 0 else 'y2')
        c.stamp(p, 'K')

    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])

    def near():
        tip = kusanagi(g, wr, S['wang'], S['bolts'])
        # bare forearm with gold bracer, short white sleeve
        p = C()
        fa = L(el[0], el[1], 3.0, wr[0] + 1, wr[1], 2.5)
        p.form(fa, SKN, sd=1, hl=1)
        t = 0.5
        q = lerp(wr, el, t)
        p.form(L(wr[0] + (el[0] - wr[0]) * 0.3, wr[1] + (el[1] - wr[1]) * 0.3, 2.6, q[0], q[1], 2.8), GOLD, sd=1, hl=1, only=fa)
        c.stamp(p, 'K')
        p = C()
        up = L(sh_[0], sh_[1], 4.6, lerp(sh_, el, 0.75)[0], lerp(sh_, el, 0.75)[1], 4.8)
        p.form(up, WH, sd=2, hl=1)
        p.line([(sh_[0] - 2, sh_[1] + 1), (el[0], el[1] - 3)], 'v1', only=up)
        c.stamp(p, 'K')
        p = C(); p.grid(int(wr[0]) - 3, int(wr[1]) - 2, HAND, L_); c.stamp(p, 'K')
        return tip

    tip = None
    if S['arm_back']:
        tip = near()
    g.head(HEAD, L_, (30, 5))
    if not S['arm_back']:
        tip = near()

    if S['slash']:
        cx, cy, r, a0, a1 = S['slash']
        ctr = B((cx, cy))
        m = arc(ctr[0], ctr[1], r - 8, r, a0, a1)
        p = C()
        p.fill(m, 'a2'); p.fill(m & arc(ctr[0], ctr[1], r - 2, r, a0, a1, taper=False), 'v3')
        p.fill(m & arc(ctr[0], ctr[1], r - 8, r - 6, a0, a1, taper=False), 'a1')
        c.stamp(p, ring=False)
    if S['big']:
        for zz in S['big']:
            pts = [tip if q == 'tip' else B(q) for q in zz]
            bolt(c, pts)
    return g.done()


WALK = [
    dict(bob=0, ffoot=25, nfoot=49, hair=1, sleeve=1, bolts=0),
    dict(bob=-1, ffoot=32, nfoot=42, nlift=2, hair=0, bolts=1),
    dict(bob=0, ffoot=40, nfoot=33, hair=1, sleeve=-1, bolts=0),
    dict(bob=-1, ffoot=33, flift=2, nfoot=41, hair=0, bolts=1),
]
ATTACK = [
    dict(lean=1, nelb=(49, 30), nwr=(50, 20), wang=68, hair=-1, ffoot=31, nfoot=46, bolts=1,
         big=([(70, -10), (64, -4), (68, -1), 'tip'], [(52, -11), (56, -6), (53, -3), 'tip'])),
    dict(lean=-3, bob=1, nelb=(36, 33), nwr=(27, 37), wang=198, ffoot=23, nfoot=49, hair=2, sleeve=2, bolts=None,
         slash=(34, 34, 35, 92, 214),
         big=(['tip', (-8, 42), (-11, 38), (-17, 44), (-20, 40)], ['tip', (-7, 51), (-11, 54), (-15, 50), (-20, 56)],
              [(4, 20), (-2, 16), (-5, 21), (-12, 15)])),
    dict(lean=-1, nelb=(38, 36), nwr=(30, 38), wang=165, ffoot=26, nfoot=47, hair=1, bolts=0),
]

if __name__ == '__main__':
    build(NAME, susanoo, WALK, ATTACK)
