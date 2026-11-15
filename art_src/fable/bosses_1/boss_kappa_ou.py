"""Kappa-O, king of the kappa (boss, ~122 px)."""
from bl import *

NAME = 'boss_kappa_ou'
CW, CH = 216, 176
OX, OY = 36, 30          # local baseline y=140
G = ('g1', 'g2', 'g3')
GF = ('g0', 'g1', 'g2')
BL = ('c0', 'c1', 'c2')
GOLD = ('y0', 'y1', 'y2')
BONE = ('b0', 'b1', 'b2')

ELEG = dict(zip('KaeEZgs', ['K', 'g0', 'e0', 'e1', 'y3', 'g1', 'c1']))
EYE = """
..........KKKK.
.......KKKKKKKK
....KKKKKKKKaa.
.KKKKKKeEEEKaa.
KKKKaeEEZZEKa..
.KKaaeEEZEEKa..
...aaaKeeeKaa..
.....aaaaaa....
"""


def P(x, y):
    return (x + OX, y + OY)


def barnacle(p, x, y, r=2.6):
    p.form(E(x, y, r, r - 0.3), BONE, sd=1, hl=1)
    p.fill(E(x, y, max(r - 1.9, 0.6), max(r - 2.1, 0.6)), 'K')


def head(c, o):
    ox, oy = o

    def h(x, y):
        return (ox + x, oy + y)

    def hc(x, y):            # crown / dish sit higher on the skull
        return (ox + x, oy + y - 5)

    # wet hair strands hanging behind the skull
    p = C()
    for (x0, y0, x1, y1, x2, y2, w) in [(44, 12, 50, 28, 49, 46, 2.2), (48, 12, 55, 26, 56, 40, 2.0), (40, 14, 44, 30, 42, 50, 1.9),
                                        (50, 11, 58, 20, 61, 31, 1.8)]:
        m = L(*h(x0, y0), w, *h(x1, y1), w) | L(*h(x1, y1), w, *h(x2, y2), 0.8)
        p.form(m, ('h0', 'h1', 'h2'), sd=1, hl=0)
        p.line([h(x0 + 1, y0 + 6), h(x1 - 1, y1 - 2)], 'h2', only=m)
    c.stamp(p, 'K', skip=('h0', 'h1'))
    # back crown points (behind the dish)
    p = C()
    for x, hh in ((27, 6), (34, 8), (41, 8), (47, 6)):
        p.form(PG([hc(x - 3, 13), hc(x, 13 - hh), hc(x + 3, 13)]), ('y0', 'y0', 'y1'), sd=1, hl=1)
    c.stamp(p, 'K')
    # skull
    p = C()
    skull = E(*h(36, 27), 16.4, 14.4) | E(*h(31, 34), 13.4, 10.6)
    p.form(skull, G, sd=5, hl=1)
    p.form(E(*h(31, 21), 9, 4.4), G, sd=2, hl=1, only=skull)   # heavy brow ridge
    # wrinkles / old skin
    p.line([h(25, 23), h(27, 29), h(25, 36)], 'g1', only=skull)
    p.line([h(38, 33), h(41, 37), h(40, 41)], 'g1', only=skull)
    p.line([h(33, 37), h(35, 41)], 'g1', only=skull)
    p.fill(R(*h(30, 16), *h(33, 16)), 'g4', only=skull)
    for (x, y) in [(41, 24), (44, 29), (39, 28)]:          # warts
        p.pxs([h(x, y), h(x + 1, y)], 'g3'); p.pxs([h(x, y + 1), h(x + 1, y + 1)], 'g1')
    c.stamp(p, 'K')
    # water dish
    p = C()
    dish = E(*hc(36, 13), 13.4, 3.4)
    p.form(dish, ('a0', 'a1', 'a2'), sd=1, hl=1)
    p.fill(R(*hc(29, 12), *hc(34, 12)), 'v3', only=dish)
    c.stamp(p, 'K')
    # crown: front band + points, jewels
    p = C()
    bandm = PG([hc(21, 15), hc(36, 17), hc(51, 14), hc(51, 19), hc(36, 22), hc(21, 20)])
    pts = np.zeros_like(bandm)
    for x, yb, hh in ((22, 15, 6), (29, 16, 5), (36, 17, 7), (43, 16, 5), (50, 14, 6)):
        pts |= PG([hc(x - 2, yb + 1), hc(x, yb - hh), hc(x + 2, yb + 1)])
    p.form(bandm | pts, GOLD, sd=2, hl=1)
    p.line([hc(22, 19), hc(36, 21), hc(50, 18)], 'y0', only=bandm)
    for x, y in ((28, 17), (43, 17)):
        p.pxs([hc(x, y), hc(x + 1, y)], 'y3')
    p.fill(R(*hc(35, 18), *hc(37, 20)), 'e0'); p.pxs([hc(35, 18), hc(36, 18)], 'e1'); p.px(*hc(35, 18), 'y3')
    c.stamp(p, 'K')
    # beak (scarred, hooked)
    p = C()
    low = PG([h(9, 39), h(24, 38), h(26, 44), h(14, 45), h(8, 42)])
    p.form(low, ('y0', 'y0', 'y1'), sd=2, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.fill(PG([h(8, 36), h(25, 35), h(25, 39), h(9, 39)]), 'q')
    for x in (11, 15, 19):                                   # ragged beak teeth
        p.pxs([h(x, 37), h(x, 38), h(x + 1, 38)], 'b2')
    c.stamp(p, 'K')
    p = C()
    up = PG([h(26, 22), h(14, 24), h(5, 29), h(1, 35), h(0, 41), h(3, 42), h(6, 38), h(13, 36), h(26, 36)])
    p.form(up, GOLD, sd=2, hl=1)
    p.line([h(15, 25), h(17, 30), h(15, 33), h(18, 36)], 'y0', only=up)        # old crack
    p.line([h(8, 29), h(9, 32)], 'y0', only=up)
    p.pxs([h(10, 30), h(11, 30)], 'K')                                           # nostril
    p.fill(R(*h(6, 31), *h(8, 31)), 'y3', only=up)
    p.fill(PG([h(20, 35), h(22, 33), h(24, 36)]), 0)                             # chipped notch
    p.pxs([h(1, 41), h(2, 41), h(1, 40)], 'b3')
    c.stamp(p, 'K')
    # eye + brow grid, scar across it
    p = C()
    p.grid(ox + 21, oy + 21, EYE, ELEG)
    c.stamp(p, ring=False)
    c.line([h(33, 17), h(31, 20)], 'c1'); c.line([h(29, 28), h(28, 32)], 'c1')
    c.line([h(34, 17), h(32, 20)], 'g0'); c.line([h(30, 28), h(29, 32)], 'g0')
    # thin ancient chin beard
    p = C()
    for (x0, x1, y1, x2, y2) in ((14, 12, 52, 14, 58), (18, 19, 54, 17, 62), (22, 24, 51, 23, 56)):
        bd = L(*h(x0, 45), 1.7, *h(x1, y1), 1.4) | L(*h(x1, y1), 1.4, *h(x2, y2), 0.6)
        p.form(bd, ('v0', 'v1', 'v2'), sd=1, hl=0)
    c.stamp(p, 'K')


def arm(c, sh_, el, wr, ang, ramp, spread=32, cuff=False, barn=False):
    claw_hand(c, wr, ang, ramp, 'g0', n=3, spread=spread, ln=13, fr=2.6, tr=1.5, palm=5.2, claw='b2', clen=5)
    p = C()
    fa = L(el[0], el[1], 6.4, wr[0], wr[1], 4.4) | E(*lerp(el, wr, 0.3), 7, 6.6)
    p.form(fa, ramp, sd=2, hl=1)
    if barn:
        q = lerp(el, wr, 0.45)
        barnacle(p, q[0] + 1, q[1] - 2, 2.4); barnacle(p, q[0] + 5, q[1], 1.9)
    c.stamp(p, 'g0')
    p = C()
    up = L(sh_[0], sh_[1], 8.6, el[0], el[1], 6.6)
    p.form(up, ramp, sd=3, hl=1)
    p.form(E(*lerp(sh_, el, 0.55), 6.6, 6.2), ramp, sd=2, hl=1, only=up)
    p.form(E(sh_[0], sh_[1] - 1, 10, 9.4), ramp, sd=2, hl=1)
    p.fill(R(sh_[0] - 5, sh_[1] - 7, sh_[0] - 2, sh_[1] - 7), 'g4')
    if cuff:
        cm = band(sh_, el, 0.6, 0.85, 10) & up
        p.form(cm, GOLD, sd=1, hl=1)
    c.stamp(p, 'g0')


def leg(c, hip, knee, ank, toe, ramp):
    p = C()
    p.form(L(hip[0], hip[1], 10.4, knee[0], knee[1], 7.2), ramp, sd=5, hl=1)
    p.form(L(knee[0], knee[1], 6.4, ank[0], ank[1], 4.6), ramp, sd=3, hl=1)
    p.form(E(knee[0] - 1, knee[1], 5.2, 4.8), ramp, sd=1, hl=1)
    ax, ay = ank
    by = ay + 9
    foot = PG([(ax + 5, ay - 2), (ax + 7, by), (toe + 2, by), (toe, by - 2), (toe + 9, by - 7), (ax - 5, ay - 4)])
    p.form(foot, ramp, sd=2, hl=1)
    p.line([(toe + 9, by - 5), (toe + 14, by)], ramp[0], only=foot)
    p.line([(toe + 16, by - 6), (toe + 22, by)], ramp[0], only=foot)
    c.stamp(p, 'g0')
    for i in range(3):
        cx = toe - 2 + i * 8
        c.fill(PG([(cx, by), (cx + 3, by - 2), (cx + 4, by)]), 'b2')
        c.pxs([(cx, by), (cx + 1, by)], 'b3')


DEF = dict(
    bob=0, lean=0, air=0, head=(0, 0),
    fsh=(80, 80), felb=(60, 93), fwr=(42, 86), fang=176, fspread=32,
    nsh=(93, 80), nelb=(84, 104), nwr=(62, 108), nang=170, nspread=30,
    fhip=(92, 112), fknee=(74, 120), fank=(76, 131), ftoe=52,
    nhip=(104, 112), nknee=(100, 124), nank=(110, 131), ntoe=88,
    splash=False,
)


def kappa_ou(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, air = S['bob'], S['lean'], S['air']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob + air)

    def A(pt):
        return P(pt[0], pt[1] + air)

    arm(c, B(S['fsh']), B(S['felb']), B(S['fwr']), S['fang'], GF, S['fspread'])
    leg(c, A(S['fhip']), A(S['fknee']), A(S['fank']), S['ftoe'] + OX, GF)

    # ---- shell: cracked scutes, moss, barnacles
    p = C()
    shell = L(*B((108, 63)), 20, *B((118, 102)), 24)
    seeds = [(110, 66), (114, 84), (118, 104), (124, 56), (130, 70), (134, 88), (134, 104), (126, 118), (100, 52), (114, 46),
             (98, 74), (102, 94), (108, 118), (122, 72), (124, 96)]
    d = np.stack([(px.X - B(q)[0]) ** 2 + (px.Y - B(q)[1]) ** 2 for q in seeds])
    cid = d.argmin(0)
    p.fill(shell, 's0')
    seam = (cid != np.roll(cid, -1, 1)) | (cid != np.roll(cid, -1, 0)) | (cid != np.roll(cid, 1, 1))
    for k in range(len(seeds)):
        cell = shell & (cid == k) & ~seam
        p.form(cell, ('s1', 's2', 's3'), sd=2, hl=1 if k in (0, 1, 3, 8, 9, 13) else 0)
    darken_core(p, shell, 9, (('s1', 's0'), ('s2', 's1'), ('s3', 's2')))
    # cracks
    for pts in ([(112, 50), (117, 60), (113, 68), (120, 78), (117, 86)], [(113, 68), (107, 73)], [(120, 78), (127, 80), (130, 86)],
                [(128, 100), (123, 108), (126, 116)]):
        q = [B(t) for t in pts]
        p.line(q, 'K', only=shell)
    # moss on the top of the shell
    moss = (E(*B((104, 48)), 10, 5.4) | E(*B((116, 45)), 9, 4.4) | E(*B((95, 55)), 6, 5) | tri(B((100, 50)), 80, 13, 6)
            | tri(B((112, 47)), 95, 12, 5) | tri(B((122, 47)), 85, 9, 4) | tri(B((92, 57)), 90, 9, 4) | E(*B((126, 50)), 6, 3.4)) & shell
    p.form(moss, ('g1', 'g2', 'g3'), sd=1, hl=1)
    for (x, y) in [(101, 45), (108, 44), (114, 42), (97, 51)]:
        p.pxs([B((x, y)), B((x + 1, y))], 'g4')
    for (x, y, r) in [(104, 104, 3.2), (110, 110, 2.4), (100, 111, 2.2), (128, 64, 2.6), (133, 70, 2.0), (120, 121, 2.4)]:
        barnacle(p, *B((x, y)), r)
    c.stamp(p, 'K')

    # ---- torso
    p = C()
    torso = L(*B((88, 84)), 15.4, *A((98, 112)), 14.6)
    p.form(torso, G, sd=6, hl=1)
    belly = torso & ~L(*B((110, 72)), 13, *A((118, 118)), 13)
    belly &= sh(torso, 2, 0) & (px.Y > B((0, 78))[1])
    p.form(belly, BL, sd=3, hl=0)
    for y in (88, 96, 104, 112, 120):
        p.line([B((66, y)), B((100, y + 5))], 'c0', only=belly)
    p.line([B((84, 80)), B((87, 100)), A((92, 124))], 'c0', only=belly)
    for (qx, qy) in [(100, 88), (103, 96), (99, 102), (104, 108)]:
        q = B((qx, qy))
        if p.a[q[1], q[0]] == I('g2'):
            p.pxs([q, (q[0] + 1, q[1])], 'g1')
    c.stamp(p, 'g0')

    leg(c, A(S['nhip']), A(S['nknee']), A(S['nank']), S['ntoe'] + OX, G)

    hx, hy = S['head']
    head(c, B((24 + hx, 25 + hy)))

    arm(c, B(S['nsh']), B(S['nelb']), B(S['nwr']), S['nang'], G, S['nspread'], cuff=True, barn=True)

    if S['splash']:
        p = C()
        for (x, y, a_, l_) in [(34, 139, 250, 12), (44, 139, 285, 9), (24, 139, 215, 10), (70, 139, 300, 8), (16, 139, 195, 7)]:
            m = tri(P(x, y), a_, l_, 4)
            p.form(m, ('a0', 'a1', 'a2'), sd=1, hl=1)
        p.fill(R(*P(26, 129), *P(27, 130)), 'a2'); p.fill(R(*P(50, 127), *P(51, 128)), 'a2'); p.fill(R(*P(14, 131), *P(15, 132)), 'a1')
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [
    dict(bob=1, fknee=(72, 121), fank=(72, 131), ftoe=47, nknee=(101, 124), nank=(114, 131), ntoe=92,
         nelb=(90, 104), nwr=(74, 116), nang=140, felb=(60, 96), fwr=(44, 98), fang=165),
    dict(bob=-1, fknee=(80, 120), fank=(86, 131), ftoe=62, nknee=(95, 119), nank=(104, 126), ntoe=82,
         nelb=(86, 104), nwr=(66, 110)),
    dict(bob=1, fknee=(88, 122), fank=(98, 131), ftoe=74, nknee=(88, 122), nank=(90, 131), ntoe=66,
         nelb=(82, 103), nwr=(60, 104), nang=175, felb=(64, 97), fwr=(52, 106), fang=150),
    dict(bob=-1, fknee=(78, 117), fank=(82, 126), ftoe=58, nknee=(96, 123), nank=(104, 131), ntoe=82,
         nelb=(86, 104), nwr=(66, 110)),
]
ATTACK = [
    # wind-up: deep crouch, claws drawn back
    dict(bob=7, lean=4, fhip=(94, 117), nhip=(106, 117), fknee=(72, 121), fank=(78, 131), ftoe=54, nknee=(98, 126), nank=(112, 131), ntoe=90,
         nelb=(108, 68), nwr=(102, 48), nang=235, nspread=40, felb=(66, 98), fwr=(52, 108), fang=150),
    # strike: airborne, diving with both claws spread
    dict(air=-24, lean=-10, bob=2, ftoe=74, ntoe=102,
         fknee=(82, 120), fank=(96, 126), nknee=(108, 122), nank=(124, 124),
         nsh=(92, 82), nelb=(72, 92), nwr=(48, 92), nang=175, nspread=44,
         fsh=(80, 82), felb=(62, 100), fwr=(42, 114), fang=150, fspread=40),
    # recover: crashed down, hands on the ground, water bursts
    dict(bob=9, lean=-6, fhip=(94, 118), nhip=(106, 118), fknee=(74, 123), fank=(76, 131), ftoe=52, nknee=(100, 127), nank=(112, 131), ntoe=90,
         nelb=(78, 106), nwr=(58, 119), nang=188, nspread=34, felb=(56, 100), fwr=(38, 119), fang=190, fspread=34, splash=True),
]

if __name__ == '__main__':
    export(NAME, kappa_ou, WALK, ATTACK)
