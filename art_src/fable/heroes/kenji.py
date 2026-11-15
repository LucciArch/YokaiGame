"""Kenji - young samurai: topknot, white headband, blue kataginu over dark hakama, katana."""
from herolib import *

NAME = 'kenji'
L_ = dict(LEG, e='u1')
HEAD = """
...........mm...
..........mnom..
..........mnnm..
......mmmmnnm...
....mmnnnnnnmm..
...mnoooonnnnnm.
..mnoonnnnnnnnnm
..WWWWWWWWwwwwvm
.mwwwwwwwwwwvvvm
.mnmnnmnnmnnnnnm
.mcmccmccmnmnnnm
.cKccccKKKcmnnnm
.cKKcKKKccbmnnm.
.cKWccKeWbbmnnm.
..ccbcccccbmnm..
..cccccccbbmm...
...caaccbbm.....
...bcccbbb......
....bbbb........
"""

DEF = dict(bob=0, lean=0, nsh=(44, 29), nelb=(39, 37), nwr=(30, 34), wang=122,
           ffoot=30, nfoot=45, flift=0, nlift=0, hair=0, arm_back=False, slash=None, sleeve=0)


def katana(g, wr, ang, back=False):
    c = g.c
    dx, dy = vec(ang)
    nx, ny = -dy, dx
    butt = (wr[0] - dx * 5, wr[1] - dy * 5)
    gd = (wr[0] + dx * 3.5, wr[1] + dy * 3.5)
    b0 = (wr[0] + dx * 5, wr[1] + dy * 5)
    b1 = (wr[0] + dx * 18, wr[1] + dy * 18 + 0.0)
    cdx, cdy = vec(ang + 7)
    tip = (b1[0] + cdx * 11, b1[1] + cdy * 11)
    p = C()
    hd = L(*butt, 1.3, *gd, 1.3)
    p.form(hd, ('i0', 'u1', 'u2'), sd=1, hl=0)
    for t in (0.2, 0.6):
        q = lerp(butt, gd, t)
        p.px(int(round(q[0])), int(round(q[1])), 'c2')
    c.stamp(p, 'K')
    p = C()
    bl = L(*b0, 1.2, *b1, 1.1) | L(*b1, 1.1, *tip, 0.6)
    p.form(bl, ('i2', 'i3', 'v3'), sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.form(L(gd[0] - nx * 2.2, gd[1] - ny * 2.2, 1.0, gd[0] + nx * 2.2, gd[1] + ny * 2.2, 1.0), GOLD, sd=1, hl=0)
    c.stamp(p, 'K')
    return tip


def kenji(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S)
    c, B, P = g.c, g.B, g.P
    hs = S['hair']

    # ---- scabbard at the hip, pointing back
    p = C()
    sc = L(*B((43, 40)), 1.4, *B((60, 47)), 1.2)
    p.form(sc, ('m0', 'm1', 'm2'), sd=1, hl=0)
    p.fill(E(*B((60, 47)), 1.6, 1.6), 'y1', only=sc)
    c.stamp(p, 'K')

    # ---- headband tails
    for k, (dy0, ln_) in enumerate(((0, 11), (3, 8))):
        p = C()
        a_ = B((45, 17 + dy0))
        md = (a_[0] + ln_ * 0.5, a_[1] - 1 - hs + k * 2)
        en = (a_[0] + ln_, a_[1] + 2 + hs * 2 + k * 3)
        tl = L(a_[0], a_[1] + 1, 1.3, *md, 1.2) | L(*md, 1.2, *en, 0.9)
        p.form(tl, WH if k == 0 else WHD, sd=1, hl=0)
        c.stamp(p, 'K')

    # ---- far kataginu wing + far sleeve
    p = C()
    fs = PG([B((36, 28)), B((33, 33)), B((32, 41)), B((38, 43)), B((40, 30))])
    p.form(fs, WHD, sd=2, hl=1)
    c.stamp(p, 'K')
    p = C()
    fw = PG([B((38, 25)), B((30, 25)), B((29, 27)), B((35, 34)), B((39, 30))])
    p.form(fw, ('u0', 'u1', 'u2'), sd=2, hl=1)
    c.stamp(p, 'K')

    g.feet('tabi', strap='u1')
    g.hakama(DARK, 'K', tie=None)
    # obi + hakama knot
    p = C()
    p.form(R(*B((35, 36)), *B((46, 38))), DARK, sd=1, hl=1)
    p.form(R(*B((36, 37)), *B((39, 40))), WHD, sd=1, hl=0)
    c.stamp(p, 'K')

    # ---- torso: pale kimono with the blue kataginu panels
    p = C()
    torso = L(*B((40, 30)), 5.6, *B((41, 36)), 5.2)
    p.form(torso, WH, sd=2, hl=1)
    pan_n = PG([B((41, 24)), B((47, 26)), B((47, 38)), B((42, 38)), B((41, 34))])
    pan_f = PG([B((37, 24)), B((34, 26)), B((34, 38)), B((38, 38)), B((39, 33))])
    p.form(pan_n, BLU, sd=2, hl=0, only=torso)
    p.form(pan_f, ('u0', 'u1', 'u2'), sd=1, hl=1, only=torso)
    p.line([B((41, 25)), B((41, 34)), B((42, 38))], 'u0', only=torso)
    p.line([B((38, 26)), B((40, 33))], 'v1', only=torso)
    c.stamp(p, 'K')
    p = C()
    p.form(R(*B((38, 24)), *B((41, 26))), ('k0', 'k1', 'k2'), sd=1, hl=0)
    c.stamp(p, 'K', ring=False)

    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])

    def near():
        tip = katana(g, wr, S['wang'])
        g.arm(sh_, el, wr, WH, sv=S['sleeve'], bag=7, hleg=L_)
        return tip

    def wing():
        p = C()
        nw = PG([B((41, 25)), B((51, 24)), B((52, 27)), B((47, 35)), B((42, 31))])
        p.form(nw, BLU, sd=2, hl=1)
        p.line([B((43, 27)), B((49, 26))], 'u1', only=nw)
        p.fill(R(*B((46, 29)), *B((47, 30))), 'v2', only=nw)      # mon crest
        c.stamp(p, 'K')

    if S['arm_back']:
        near()
    g.head(HEAD, L_, (30, 6))
    if not S['arm_back']:
        near()
    wing()

    if S['slash']:
        cx, cy, r, a0, a1 = S['slash']
        ctr = B((cx, cy))
        m = arc(ctr[0], ctr[1], r - 7, r, a0, a1)
        m2 = arc(ctr[0], ctr[1], r - 7, r - 2, a0, a1) & m
        p = C()
        p.fill(m, 'a2'); p.fill(m & ~m2 | (m & arc(ctr[0], ctr[1], r - 2, r, a0, a1, taper=False)), 'v3')
        c.stamp(p, ring=False)
    return g.done()


WALK = [
    dict(bob=0, ffoot=26, nfoot=49, hair=1, sleeve=1),
    dict(bob=-1, ffoot=33, nfoot=42, nlift=2, hair=0),
    dict(bob=0, ffoot=40, nfoot=34, hair=1, sleeve=-1),
    dict(bob=-1, ffoot=33, flift=2, nfoot=41, hair=0),
]
ATTACK = [
    dict(lean=1, nelb=(49, 31), nwr=(51, 22), wang=48, hair=-1, ffoot=31, nfoot=46, arm_back=False),
    dict(lean=-3, bob=1, nelb=(36, 33), nwr=(27, 37), wang=200, ffoot=24, nfoot=48, hair=2, sleeve=2,
         slash=(34, 34, 33, 95, 215)),
    dict(lean=-1, nelb=(38, 36), nwr=(30, 38), wang=165, ffoot=27, nfoot=46, hair=1),
]

if __name__ == '__main__':
    build(NAME, kenji, WALK, ATTACK)
