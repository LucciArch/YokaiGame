"""Sojobo, king of the tengu of Mount Kurama (boss, ~126 px + wings)."""
from bl import *

NAME = 'boss_sojobo'
CW, CH = 292, 208
OX, OY = 70, 50          # local baseline y=150
BLKF = ('h0', 'h1', 'h2')
PUR = ('p1', 'p2', 'p3')
PFAR = ('p0', 'p1', 'p2')
HAK = ('i0', 'i1', 'i2')
WHT = ('v1', 'v2', 'v3')
GOLD = ('y0', 'y1', 'y2')
SK = ('r1', 'r2', 'r3')

LEG = dict(zip('abcdeKYZVvuUWq', ['r0', 'r1', 'r2', 'r3', 'r4', 'K', 'y2', 'y3', 'v3', 'v2', 'v1', 'v0', 'b3', 'q']))
FACE = """
..........ccccccc.....
........ccdddccccbb...
.......cddddccccccbb..
......cdddcccccccccbb.
.....VVVVVcccVVVVVVbb.
....cvVVVVVKcvVVVVVVb.
.....KKvVVVKcKKvVVVub.
.....cYZKKKccYZYKKubb.
.....caYYaccbaYYaabbb.
....ccdccccccbaabbbb..
cddddddddccccccccbbb..
deedddccccccbccccbbb..
cccccccccbbaccccccba..
.bbbbbbbaaacccccbbba..
......caaaccdcccbbba..
......cKKKKKKKccbba...
......cWqWqWqKcbbba...
......bKKKKKKKbbba....
.......bccccbbbaa.....
........bbbbbaa.......
"""
FIST = """
.cdcc.
cdccbb
caaccb
cccabb
.cbbb.
"""


def P(x, y):
    return (x + OX, y + OY)


def wing(c, sh_, el, wr, a_tip, a_root, lens, n=9, far=False, flap=0):
    """feathers hang from the wing arm; a_tip/a_root = feather direction at wrist/shoulder (deg)"""
    rp = ('K', 'h0', 'h1') if far else BLKF
    pts = []
    for i in range(n):                       # root -> tip so the long primaries overlap the inner ones
        t = i / (n - 1)
        base = lerp(sh_, el, t * 2) if t < 0.5 else lerp(el, wr, t * 2 - 1)
        ang = a_root + (a_tip - a_root) * t + flap * t
        ln_ = lens[0] + (lens[1] - lens[0]) * (t ** 0.8)
        pts.append((base, ang, ln_))
    for base, ang, ln_ in pts:
        tip = pol(base, ang, ln_)
        mid = pol(base, ang, ln_ * 0.55)
        p = C()
        m = L(*base, 3.2, *mid, 4.6) | L(*mid, 4.6, *tip, 1.0)
        p.form(m, rp, sd=2, hl=1)
        p.line([pol(base, ang, 5), pol(base, ang, ln_ - 5)], rp[0], only=m)
        c.stamp(p, 'K')
    for base, ang, ln_ in pts[1:]:           # short coverts
        tip = pol(base, ang - 6, ln_ * 0.36)
        p = C()
        p.form(L(*base, 3.6, *tip, 2.0), rp, sd=1, hl=1)
        c.stamp(p, 'K')
    p = C()
    p.form(L(*sh_, 5.0, *el, 4.2) | L(*el, 4.2, *wr, 2.8), rp, sd=2, hl=1)
    c.stamp(p, 'K')


def fan(c, hand, ang, spread=52, ln=27):
    """hauchiwa: seven golden feathers on a red grip"""
    p = C()
    p.form(L(*pol(hand, ang + 180, 7), 1.8, *pol(hand, ang, 5), 2.0), ('m1', 'm2', 'm3'), sd=1, hl=1)
    c.stamp(p, 'K')
    base = pol(hand, ang, 5)
    order = [-3, 3, -2, 2, -1, 1, 0]
    for k in order:
        a = ang + k * spread / 3.0
        l_ = ln * (1 - abs(k) * 0.06)
        tip = pol(base, a, l_); mid = pol(base, a, l_ * 0.6)
        p = C()
        m = L(*base, 1.6, *mid, 4.2) | L(*mid, 4.2, *tip, 1.2)
        p.form(m, GOLD, sd=2, hl=1)
        p.line([pol(base, a, 3), pol(base, a, l_ - 3)], 'y0', only=m)
        p.fill(E(tip[0], tip[1], 1.6, 1.6) & m, 'y3')
        c.stamp(p, 'K')
    c.fill(E(base[0], base[1], 2.4, 2.4), 'e0'); c.px(int(base[0]), int(base[1]) - 1, 'e1')


def geta_leg(c, knee, ank, far=False):
    rp = ('v0', 'v1', 'v2') if far else WHT
    ax, ay = ank
    p = C()
    p.form(L(*knee, 5.4, ax, ay, 4.2), rp, sd=2, hl=1)                      # white kyahan legging
    for t in (0.3, 0.6):
        q = lerp(knee, ank, t)
        p.line([(q[0] - 5, q[1]), (q[0] + 5, q[1] + 1)], rp[0], only=p.m)
    foot = PG([(ax + 5, ay), (ax + 5, ay + 6), (ax - 12, ay + 6), (ax - 13, ay + 3), (ax - 4, ay - 1)])
    p.form(foot, ('r0', 'r1', 'r2') if far else SK, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    by = ay + 7
    p.form(R(ax - 14, by, ax + 7, by + 2), ('w0', 'w1', 'w2'), sd=1, hl=1)   # geta board
    p.form(R(ax - 6, by + 3, ax - 2, by + 11), ('w0', 'w1', 'w2'), sd=1, hl=1)   # single tall tooth
    c.stamp(p, 'K')
    c.line([(ax - 8, ay + 3), (ax - 5, ay + 6)], 'm2')


DEF = dict(
    bob=0, lean=0, flap=0, beard=0,
    fsh=(86, 64), felb=(70, 78), fhand=(54, 76), fanang=232,
    nsh=(114, 63), nelb=(122, 82), nhand=(110, 92),
    fknee=(86, 120), fank=(86, 131), nknee=(108, 120), nank=(110, 131),
    gust=0, arm_front=True,
)


def sojobo(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, fl = S['bob'], S['lean'], S['flap']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    # ---- wings (far first)
    wing(c, B((96, 60)), B((72, 36 - fl * 0.3)), B((46, 22 - fl * 0.6)), 118, 80, (26, 50), n=8, far=True, flap=-fl)
    wing(c, B((112, 60)), B((142, 36 - fl * 0.3)), B((174, 16 - fl * 0.6)), 62, 96, (30, 66), n=10, flap=fl)

    def sleeve_arm(sh_, el, ha, rp, far):
        p = C()
        up = L(*sh_, 6.4, *el, 6.0)
        p.form(up, rp, sd=2, hl=1)
        c.stamp(p, 'K')
        p = C()
        d = (ha[0] - el[0], ha[1] - el[1]); n_ = math.hypot(*d) or 1
        nx, ny = -d[1] / n_, d[0] / n_
        if ny < 0:
            nx, ny = -nx, -ny
        w = PG([(el[0] - nx * 6, el[1] - ny * 6), (ha[0] - nx * 4, ha[1] - ny * 4), (ha[0] + nx * 5, ha[1] + ny * 5),
                (ha[0] + nx * 17 + d[0] / n_ * 2, ha[1] + ny * 17), (el[0] + nx * 14, el[1] + ny * 14), (el[0] + nx * 2 - d[0] / n_ * 5, el[1] + ny * 4)])
        p.form(w, rp, sd=3, hl=1)
        p.line([(ha[0] + nx * 15, ha[1] + ny * 15), (el[0] + nx * 5, el[1] + ny * 4)], rp[0], only=w)
        p.line([(ha[0] - nx * 4, ha[1] - ny * 4), (ha[0] + nx * 16, ha[1] + ny * 16)], 'v1', only=w)   # white lining at the cuff
        c.stamp(p, 'K')
        p = C()
        p.grid(int(ha[0]) - 4, int(ha[1]) - 3, FIST, LEG)
        c.stamp(p, 'r0')

    fsh, fel, fha = B(S['fsh']), B(S['felb']), B(S['fhand'])
    if not S['arm_front']:
        fan(c, fha, S['fanang'])
        sleeve_arm(fsh, fel, fha, PFAR, True)

    # ---- legs
    geta_leg(c, P(*S['fknee']), P(*S['fank']), far=True)
    geta_leg(c, P(*S['nknee']), P(*S['nank']))
    # hakama
    p = C()
    fk, nk = P(*S['fknee']), P(*S['nknee'])
    hak = PG([B((81, 90)), B((119, 90)), (nk[0] + 13, nk[1] + 1), (nk[0] - 7, nk[1] + 3), B((99, 108)), (fk[0] + 8, fk[1] + 3),
              (fk[0] - 12, fk[1] + 1)])
    p.form(hak, HAK, sd=4, hl=1)
    for a_, b_ in ((B((88, 94)), (fk[0] - 4, fk[1])), (B((96, 94)), (fk[0] + 4, fk[1] + 1)), (B((106, 94)), (nk[0], nk[1] + 1)),
                   (B((114, 94)), (nk[0] + 8, nk[1]))):
        p.line([a_, b_], 'i0', only=hak)
    c.stamp(p, 'K')

    # ---- robe
    p = C()
    robe = PG([B((85, 56)), B((112, 54)), B((122, 63)), B((121, 97)), B((79, 97)), B((77, 66))])
    p.form(robe, PUR, sd=5, hl=1)
    p.line([B((92, 56)), B((98, 76)), B((97, 96))], 'p0', only=robe)
    belt = PG([B((78, 88)), B((121, 87)), B((121, 95)), B((79, 96))])
    p.form(belt, WHT, sd=2, hl=1)
    p.line([B((78, 92)), B((121, 91))], 'v0', only=belt)
    # yuigesa: sash with gold pom-poms
    for a_, b_ in (((90, 56), (104, 86)), ((108, 55), (92, 86))):
        p.line([B(a_), B(b_)], 'c1', only=robe); p.line([B((a_[0] + 1, a_[1])), B((b_[0] + 1, b_[1]))], 'c0', only=robe)
    for (x, y) in ((93, 63), (105, 62), (99, 74), (95, 82)):
        p.form(E(*B((x, y)), 3.4, 3.4), GOLD, sd=1, hl=1)
    c.stamp(p, 'K')

    # ---- white mane behind the head
    hx, hy = B((60, 26))
    p = C()
    hd = S['beard']
    mane = E(hx + 15, hy + 7, 10.4, 9.4)
    for (x, y, a_, l_, w) in ((12, -1, 285, 12, 9), (18, -2, 320, 15, 10), (22, 2, 345, 20, 10), (24, 8, 5, 22, 10), (23, 14, 25, 20, 10),
                              (21, 19, 45, 18, 9), (9, 0, 250, 9, 8)):
        mane |= tri((hx + x, hy + y), a_ + hd * 2, l_, w)
    p.form(mane, WHT, sd=3, hl=1)
    for (x, y, a_) in ((20, 3, 340), (22, 9, 5), (21, 15, 28)):
        q0 = (hx + x, hy + y); p.line([q0, pol(q0, a_, 12)], 'v0', only=mane)
    c.stamp(p, 'K')
    # beard (long, to the belt) and face
    p = C()
    bd = PG([(hx + 6, hy + 15), (hx + 17, hy + 16), (hx + 18, hy + 28), (hx + 15 + hd, hy + 40), (hx + 12 + hd, hy + 52),
             (hx + 9 + hd, hy + 42), (hx + 6, hy + 32), (hx + 4, hy + 22)])
    bd |= tri((hx + 8, hy + 30), 110, 12, 6) | tri((hx + 16, hy + 30), 75, 13, 6)
    p.form(bd, WHT, sd=3, hl=1)
    p.line([(hx + 10, hy + 20), (hx + 11, hy + 34), (hx + 12 + hd, hy + 46)], 'v0', only=bd)
    p.line([(hx + 14, hy + 20), (hx + 15, hy + 34)], 'v1', only=bd)
    c.stamp(p, 'K')
    p = C()
    p.grid(hx, hy, FACE, LEG)
    c.stamp(p, 'K', skip=('v1', 'v2', 'v3'))
    # moustache sweeping back from under the nose
    p = C()
    ms = L(hx + 8, hy + 14, 1.8, hx + 4, hy + 20, 1.4) | L(hx + 4, hy + 20, 1.4, hx + 3 + hd, hy + 27, 0.7)
    p.form(ms, WHT, sd=1, hl=0)
    c.stamp(p, 'K', skip=('v1', 'v2', 'v3'))
    # tokin cap + cord
    p = C()
    p.form(PG([(hx + 9, hy - 4), (hx + 15, hy - 5), (hx + 17, hy + 1), (hx + 8, hy + 2)]), ('K', 'h0', 'h1'), sd=1, hl=1)
    c.stamp(p, 'K')
    c.line([(hx + 17, hy + 1), (hx + 20, hy + 6), (hx + 19, hy + 13)], 'm2')

    # ---- near arm (fist on the hip), then fan arm in front
    sleeve_arm(B(S['nsh']), B(S['nelb']), B(S['nhand']), PUR, False)
    if S['arm_front']:
        fan(c, fha, S['fanang'])
        sleeve_arm(fsh, fel, fha, PUR, True)

    # ---- gust
    g = S['gust']
    if g:
        p = C()
        for (x, y, r, w) in ((30, 84, 26, 3.4), (10, 96, 30, 2.6), (-12, 78, 22, 2.4)) if g == 2 else ((40, 90, 16, 2.0),):
            arc = (E(*P(x, y), r, r * 0.8) & ~E(*P(x + w + 2, y - 1), r, r * 0.8))
            p.form(arc, ('v1', 'v2', 'v3'), sd=1, hl=0)
        if g == 2:
            for (x, y) in ((-4, 110), (-20, 100), (4, 62), (-30, 86)):
                p.fill(R(*P(x, y), *P(x + 3, y)), 'v2')
        c.stamp(p, 'v0')
    c.blacken()
    return c


WALK = [
    dict(),
    dict(bob=-1, flap=5, beard=1, fhand=(54, 75), fanang=236),
    dict(bob=-2, flap=10, beard=1, fhand=(54, 74), fanang=240),
    dict(bob=-1, flap=5, beard=0, fhand=(54, 75), fanang=236),
]
ATTACK = [
    dict(lean=4, bob=-2, flap=16, beard=2, fsh=(88, 62), felb=(82, 42), fhand=(96, 24), fanang=300),
    dict(lean=-6, bob=2, flap=-10, beard=-2, fsh=(86, 66), felb=(66, 80), fhand=(46, 92), fanang=170, gust=2,
         fknee=(80, 121), fank=(78, 131)),
    dict(lean=-3, bob=1, flap=0, beard=1, felb=(68, 82), fhand=(54, 96), fanang=150, gust=1),
]

if __name__ == '__main__':
    export(NAME, sojobo, WALK, ATTACK)
