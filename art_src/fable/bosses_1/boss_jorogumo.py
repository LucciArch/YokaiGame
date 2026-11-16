"""Jorogumo: court lady above, giant joro spider below (boss, ~112 px)."""
from bl import *

NAME = 'boss_jorogumo'
CW, CH = 256, 176
OX, OY = 44, 34          # local baseline y=130
BLK = ('h0', 'h1', 'h2')
BFAR = ('K', 'h0', 'h1')
GOLD = ('y0', 'y1', 'y2')
GFAR = ('s1', 'y0', 'y1')
RED = ('m1', 'm2', 'm3')
HAIR = ('h0', 'hb', 'h2')
SKN = ('k1', 'k2', 'k3')

LEG = dict(zip('abcdmnoKEWrsY', ['k0', 'k1', 'k2', 'k3', 'h0', 'hb', 'h2', 'K', 'e1', 'y3', 'm2', 'm1', 'y2']))
FACE = """
......mmmmmmm....
....mmnnnnnnnmm..
...mnoonnnnnnnnm.
..mnoonnnnnnnnnnm
..mnnnnnnnnnnnnnm
.mnnmnnnmnnnnnnnm
.mnmcmncmmnnnnnnm
.mmdccmcccmmnnnnm
.cddccccccccmnnnm
.cKKKccKKKKsmnnnm
.cKEWccKEWKbmnnnm
.cdccccccsbbmnnnm
..cdccccccbamnnnm
..cbccccccbamnnnm
..crrrccbbba.mnnm
...ccccbbba..mnnm
....bbbaa....mnm.
"""
HAND = """
..ccc.
dccdcc
.dccbb
..cbb.
"""


def P(x, y):
    return (x + OX, y + OY)


def sleg(c, hip, knee, tip, near=True):
    rp = BLK if near else BFAR
    gp = GOLD if near else GFAR
    ank = lerp(knee, tip, 0.62)
    ank = (ank[0] + (2.5 if tip[0] > knee[0] else -2.5), ank[1])
    p = C()
    fem = L(*hip, 3.6, *knee, 2.9)
    p.form(fem, rp, sd=2, hl=1)
    p.form(band(hip, knee, 0.42, 0.62, 5) & fem, gp, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    tib = L(*knee, 2.9, *ank, 2.0)
    tar = L(*ank, 1.9, *tip, 0.7)
    p.form(tib, rp, sd=1, hl=1)
    p.form(tar, rp, sd=1, hl=1)
    p.form(band(knee, ank, 0.4, 0.7, 4) & tib, gp, sd=1, hl=1)
    p.form(band(ank, tip, 0.25, 0.5, 3) & tar, gp, sd=1, hl=0)
    p.form(E(*knee, 3.4, 3.2), rp, sd=1, hl=1)
    c.stamp(p, 'K')


DEF = dict(
    bob=0, lean=0, rear=0, hair=0,
    # spider legs: (hip, knee, tip) near 1-4 then far 1-4
    n1=((92, 102), (58, 74), (34, 130)), n2=((98, 104), (74, 86), (60, 130)),
    n3=((112, 104), (136, 74), (148, 130)), n4=((118, 102), (164, 62), (190, 130)),
    f1=((98, 98), (66, 62), (46, 130)), f2=((104, 100), (84, 76), (74, 130)),
    f3=((118, 100), (146, 64), (162, 130)), f4=((124, 98), (176, 54), (200, 130)),
    nsh=(105, 54), nelb=(106, 71), nwr=(90, 70),
    fsh=(92, 54), felb=(84, 66), fwr=(76, 52),
    web=0, pet=True,
)


def jorogumo(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, rear = S['bob'], S['lean'], S['rear']

    def B(pt):                       # lady
        return P(pt[0] + lean, pt[1] + bob - rear)

    def Bs(pt, k=0.5):               # spider body follows half of the rear-up
        return P(pt[0], pt[1] + bob - rear * k)

    def LG(t, k):
        hip, knee, tip = t
        return (Bs(hip, k), P(*knee), P(*tip))

    for key in ('f4', 'f3', 'f2', 'f1'):
        sleg(c, *LG(S[key], 0.2 if key in ('f3', 'f4') else 0.7), near=False)

    # ---- abdomen
    p = C()
    a0, a1 = Bs((134, 90), 0.1), Bs((164, 80), 0.0)
    abd = L(*a0, 22, *a1, 28)
    p.form(abd, BLK, sd=8, hl=1)
    for t0, t1 in ((0.18, 0.3), (0.5, 0.64), (0.84, 0.96)):                       # joro bands
        bm = band(lerp(a0, a1, -0.6), lerp(a0, a1, 1.8), (t0 + 0.6) / 2.4, (t1 + 0.6) / 2.4, 40) & abd
        p.form(bm, GOLD, sd=3, hl=1)
    darken_core(p, abd, 9, (('y1', 'y0'), ('y2', 'y1')))
    lit = E(*Bs((146, 66), 0.05), 15, 6.4) & abd & (p.a == I('h1'))
    p.fill(lit, 'h2')
    mark = E(*Bs((170, 96), 0), 7, 5.4) & abd                                     # red mark near the spinnerets
    p.form(mark, ('m0', 'e0', 'e1'), sd=2, hl=0)
    p.fill(R(*Bs((150, 58), 0), *Bs((157, 58), 0)), 'v1', only=abd)               # sheen
    p.fill(R(*Bs((128, 72), 0.1), *Bs((132, 72), 0.1)), 'v1', only=abd)
    c.stamp(p, 'K')
    p = C()
    p.form(tri(Bs((186, 98), 0), 30, 9, 8), BLK, sd=1, hl=1)                      # spinneret
    c.stamp(p, 'K')
    # ---- cephalothorax
    p = C()
    ceph = E(*Bs((106, 98), 0.6), 17, 10.4)
    p.form(ceph, BLK, sd=4, hl=1)
    c.stamp(p, 'K')


    # ---- long hair down the back
    p = C()
    hd = S['hair']
    hair = PG([B((98, 28)), B((110, 34)), B((116, 60)), B((122 + hd, 88)), B((128 + hd * 2, 104)), B((118 + hd, 100)),
               B((112 + hd, 108)), B((108, 92)), B((104, 66)), B((98, 44))])
    p.form(hair, HAIR, sd=3, hl=0)
    for a_, b_ in (((106, 44), (114 + hd, 84)), ((110, 60), (120 + hd, 98)), ((104, 56), (110, 96))):
        p.line([B(a_), B(b_)], 'h2', only=hair)
    c.stamp(p, 'K')

    def sleeve(el, wr, far):
        rp = ('m0', 'm1', 'm2') if far else RED
        p = C()
        drop = 30 if not far else 24
        sl = PG([(el[0] + 5, el[1] - 5), (wr[0] + 1, wr[1] - 3), (wr[0] + 2, wr[1] + 4), (wr[0] + 8, wr[1] + drop - 4 + hd),
                 (el[0] + 4 + hd, el[1] + drop), (el[0] + 9, el[1] + 6)])
        p.form(sl, rp, sd=3, hl=1)
        p.line([(wr[0] + 8, wr[1] + drop - 5 + hd), (el[0] + 4 + hd, el[1] + drop - 1)], 'y1', only=sl)
        p.line([(wr[0] + 8, wr[1] + drop - 7 + hd), (el[0] + 4 + hd, el[1] + drop - 3)], 'y0', only=sl)
        p.line([(wr[0] + 6, wr[1] + 4), (el[0] + 5, el[1] + drop - 6)], rp[0], only=sl)
        if not far:                                                               # gold web crest on the sleeve
            cx, cy = lerp(wr, el, 0.55); cy += 13
            for a_ in (0, 60, 120):
                p.line([pol((cx, cy), a_, 4), pol((cx, cy), a_ + 180, 4)], 'y0', only=sl)
            p.px(int(cx), int(cy), 'y2')
        p.fill(PG([(wr[0] + 1, wr[1] - 3), (wr[0] + 4, wr[1] - 3), (wr[0] + 5, wr[1] + 4), (wr[0] + 2, wr[1] + 4)]), 'v2', only=sl)
        c.stamp(p, 'K')
        p = C()
        p.grid(int(wr[0]) - 4, int(wr[1]) - 2, HAND, LEG)
        c.stamp(p, 'K')

    def arm(sh_, el, far):
        rp = ('m0', 'm1', 'm2') if far else RED
        p = C()
        p.form(L(*sh_, 4.6, *el, 4.2), rp, sd=2, hl=1)
        c.stamp(p, 'K')

    fsh, fel, fwr = B(S['fsh']), B(S['felb']), B(S['fwr'])
    arm(fsh, fel, True); sleeve(fel, fwr, True)

    # ---- kimono torso, obi, skirt draped over the spider's front
    p = C()
    skirt = PG([B((89, 84)), B((108, 84)), Bs((126, 99), 0.6), Bs((123, 110), 0.6), Bs((112, 112), 0.6), Bs((99, 115), 0.6),
                Bs((86, 113), 0.6), Bs((76, 109), 0.6), Bs((73, 100), 0.6)])
    p.form(skirt, RED, sd=4, hl=1)
    for a_, b_ in (((93, 88), (82, 110)), ((99, 88), (96, 113)), ((104, 88), (110, 111)), ((107, 88), (120, 108))):
        p.line([B(a_), Bs(b_, 0.6)], 'm0', only=skirt)
    hem = skirt & ~sh(skirt, 0, -2)
    p.fill(hem, 'y1'); p.fill(skirt & ~sh(skirt, 0, -1), 'y0')
    c.stamp(p, 'K')
    # nahe Beine vor Hinterleib und Rocksaum – sie sind dem Betrachter am nächsten
    for key in ('n4', 'n3', 'n2', 'n1'):
        sleg(c, *LG(S[key], 0.2 if key in ('n3', 'n4') else 0.7), near=True)
    p = C()
    torso = PG([B((91, 47)), B((101, 45)), B((109, 51)), B((108, 86)), B((89, 86)), B((86, 58))])
    p.form(torso, RED, sd=4, hl=1)
    p.line([B((93, 47)), B((91, 58)), B((95, 72))], 'v2', only=torso)             # white inner collar
    p.line([B((94, 47)), B((92, 58)), B((96, 72))], 'v1', only=torso)
    p.line([B((100, 47)), B((98, 60)), B((96, 72))], 'y1', only=torso)
    p.fill(PG([B((95, 47)), B((98, 47)), B((96, 52)), B((95, 52))]), 'k1', only=torso)   # throat
    p.line([B((103, 50)), B((104, 72))], 'm1', only=torso)
    obi = PG([B((88, 74)), B((108, 73)), B((108, 87)), B((89, 87))])
    p.form(obi, ('h0', 'h1', 'h2'), sd=3, hl=1)
    p.line([B((88, 80)), B((108, 79))], 'y1', only=obi)
    p.line([B((88, 81)), B((108, 80))], 'y0', only=obi)
    p.fill(R(*B((93, 78)), *B((95, 82))), 'y2', only=obi); p.fill(R(*B((94, 79)), *B((94, 81))), 'e0', only=obi)
    c.stamp(p, 'K')
    # neck
    p = C()
    p.form(L(*B((95, 41)), 2.0, *B((96, 47)), 2.2), SKN, sd=1, hl=0)
    c.stamp(p, 'k0')

    # ---- head: hair-do + face grid + kanzashi pins
    hx, hy = B((82, 24))
    p = C()
    do = E(hx + 11, hy - 3, 6.4, 5.4) | E(hx + 4, hy + 1, 4.4, 3.6) | E(hx + 15, hy + 2, 5.4, 4.4)   # shimada-style loops
    p.form(do, HAIR, sd=2, hl=1)
    c.stamp(p, 'K')
    p = C()
    for (x0, y0, x1, y1) in ((10, -3, 3, -11), (14, -3, 21, -10), (5, 1, -4, -5)):      # gold pins
        p.line([(hx + x0, hy + y0), (hx + x1, hy + y1)], 'y1')
        p.fill(R(hx + x1 - 1, hy + y1 - 1, hx + x1, hy + y1), 'y2')
    p.fill(R(hx + 6, hy - 1, hx + 15, hy), 'm2'); p.fill(R(hx + 6, hy - 1, hx + 9, hy - 1), 'm3')            # red comb
    c.stamp(p, 'K')
    p = C()
    p.grid(hx, hy, FACE, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # dangling pin tassels
    c.pxs([(hx - 4, hy - 4), (hx - 4, hy - 2)], 'y2'); c.pxs([(hx - 4, hy - 3), (hx - 4, hy - 1)], 'e1')

    nsh, nel, nwr = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    arm(nsh, nel, False); sleeve(nel, nwr, False)

    # pet spider dangling on a thread from the far hand
    if S['pet']:
        x, y = int(fwr[0]) - 3, int(fwr[1]) + 2
        c.line([(x, y), (x, y + 12 + hd)], 'v1')
        y += 13 + hd
        c.fill(R(x - 1, y, x + 1, y + 2), 'K'); c.px(x, y + 1, 'y2')
        c.pxs([(x - 2, y - 1), (x + 2, y - 1), (x - 3, y), (x + 3, y), (x - 2, y + 3), (x + 2, y + 3)], 'K')
    # web shot
    w = S['web']
    if w:
        o = (nwr[0] - 5, nwr[1] + 1)
        p = C()
        if w == 1:      # gathering silk
            p.fill(E(o[0] - 2, o[1], 4, 4), 'v2'); p.fill(E(o[0] - 3, o[1] - 1, 2, 2), 'v3')
        else:
            end = (o[0] - 58, o[1] + 16)
            for dy in (-12, -4, 4, 12):
                p.line([o, (end[0], end[1] + dy)], 'v2')
            for t in (0.35, 0.6, 0.82, 1.0):
                a_ = lerp(o, (end[0], end[1] - 12), t); b_ = lerp(o, (end[0], end[1] + 12), t)
                mid = lerp(a_, b_, 0.5)
                p.line([a_, (mid[0] + 3, mid[1]), b_], 'v3' if t > 0.7 else 'v2')
            p.fill(E(o[0], o[1], 2.4, 2.4), 'v3')
        c.stamp(p, 'v0')
    c.blacken()
    return c


def legs(d1=0, d2=0, l1=0, l2=0):
    """group A = n1, n3, f2, f4 ; group B = n2, n4, f1, f3. d = tip shift, l = lift"""
    D0 = DEF
    out = {}
    for key in ('n1', 'n2', 'n3', 'n4', 'f1', 'f2', 'f3', 'f4'):
        a = key in ('n1', 'n3', 'f2', 'f4')
        d, l_ = (d1, l1) if a else (d2, l2)
        hip, knee, tip = D0[key]
        out[key] = (hip, (knee[0] + d * 0.5, knee[1] - l_), (tip[0] + d, tip[1] - l_ * 1.6))
    return out


WALK = [
    dict(bob=0, **legs(-6, 6, 0, 0)),
    dict(bob=-1, hair=1, **legs(0, 0, 5, 0)),
    dict(bob=0, **legs(6, -6, 0, 0)),
    dict(bob=-1, hair=-1, **legs(0, 0, 0, 5)),
]
_up = dict(n1=((92, 102), (60, 58), (30, 66)), f1=((98, 98), (70, 46), (44, 40)),
           n2=((98, 104), (72, 78), (52, 106)), f2=((104, 100), (84, 66), (66, 92)))
ATTACK = [
    dict(rear=6, lean=5, hair=2, nelb=(102, 74), nwr=(92, 62), web=1, pet=False,
         n1=((92, 102), (64, 66), (44, 104)), f1=((98, 98), (72, 56), (56, 88))),
    dict(rear=14, lean=-3, hair=-3, nelb=(94, 64), nwr=(78, 60), fwr=(74, 46), felb=(84, 60), web=2, pet=False, **_up),
    dict(rear=6, lean=0, hair=1, pet=False, n1=((92, 102), (58, 68), (38, 112)), f1=((98, 98), (68, 58), (50, 104))),
]

if __name__ == '__main__':
    export(NAME, jorogumo, WALK, ATTACK)
