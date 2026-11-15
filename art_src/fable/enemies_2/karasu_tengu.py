"""Karasu-tengu - crow-headed mountain warrior: black wings, red yamabushi robes with white pom-poms, tokin cap, katana."""
from common import *

NAME = 'karasu_tengu'
CW, CH = 150, 104
OX, OY = 44, 22           # local: lowest talon point y = 72
ROBE = ('m1', 'm2', 'm3')
ROBF = ('m0', 'm1', 'm2')
FEA = ('h0', 'h1', 'h2')

LEG = dict(zip('mnouvwKYZqxrEWst', ['h0', 'h1', 'h2', 'b0', 'b1', 'b2', 'K', 'y2', 'y3', 'q', 'v2', 'm2', 'e0', 'b3', 'i1', 'i3']))
HEAD = """
............KKKKKK........
...........KsttttsK.......
...........KssssssK..m....
.........mmxxxxxxxxmmnm...
........mnnnnnxnnnnnnnm.m.
.......mnoonnnnxnnnnnnmnm.
......mnoonnnnnxnnnnnnnnm.
.....KKKKKKKnnnnxnnnnnnm..
....vvKKEYZKKKnnxnnnonnnm.
..vwwwvKEYYKnnnnxnnnnonm..
.vwWwwwvvKKmnnnnxnnnnnnnm.
vwwwwwwwvvvmnnnxnnnnnonm..
vuvvwwwwvvvumnnxnnnnnnm...
u.uuKKKKKKKummxnnnnnnm....
....uuvvvvu..mmnnnnmm.....
......uuuu.....mmmm.......
"""

HAND = """
.nnn.
nnonn
nnnnm
.nnm.
"""


def P(x, y):
    return (x + OX, y + OY)


def wing(c, root, elb, wri, tip, fdir, flen, far=False):
    """feathers are stamped one by one (back to front) so each gets its own dark edge."""
    ramp = ('h0', 'h0', 'h1') if far else FEA
    fa = math.atan2(fdir[1], fdir[0])
    ta = math.atan2(tip[1] - wri[1], tip[0] - wri[0])
    # shortest sweep from feather-hang direction to the wing tip direction
    d = (ta - fa + math.pi) % (2 * math.pi) - math.pi
    feats = []
    for i in range(7):                                    # secondaries along the arm
        t = i / 6
        b = lerp(root, elb, t * 2) if t < 0.5 else lerp(elb, wri, t * 2 - 1)
        ln = flen * (0.55 + 0.45 * t)
        feats.append((b, (b[0] + math.cos(fa) * ln, b[1] + math.sin(fa) * ln), 2.6))
    tl = math.hypot(tip[0] - wri[0], tip[1] - wri[1])
    for i in range(1, 6):                                 # primaries fanning from the wrist
        t = i / 5
        a = fa + d * t
        ln = flen + (tl - flen) * t
        feats.append((wri, (wri[0] + math.cos(a) * ln, wri[1] + math.sin(a) * ln), 2.4))
    for b, e, r in feats:
        p = C()
        p.form(L(b[0], b[1], r, e[0], e[1], 1.2), ramp, sd=1, hl=1)
        c.stamp(p, 'K' if far else 'h0')
    p = C()                                               # wing arm (coverts) on top
    arm_ = L(*root, 3.6, *elb, 3.0) | L(*elb, 3.0, *wri, 2.4)
    p.form(arm_, ramp, sd=2, hl=1)
    for t in (0.25, 0.5, 0.75):
        q = lerp(root, elb, t); p.fill(R(q[0], q[1], q[0] + 1, q[1]), ramp[0], only=arm_)
        q = lerp(elb, wri, t); p.fill(R(q[0], q[1], q[0] + 1, q[1]), ramp[0], only=arm_)
    c.stamp(p, 'K' if far else 'h0')


def katana(c, hand, deg, ln=30):
    """blade through 'hand'; deg: 0 = points left, 90 = up. Slight curve toward the spine."""
    a = math.radians(deg)
    dx, dy = -math.cos(a), -math.sin(a)
    nx, ny = dy, -dx                      # spine side
    hx, hy = hand
    p = C()
    pm = (hx - dx * 5, hy - dy * 5)
    p.form(L(*pm, 1.7, hx + dx * 3, hy + dy * 3, 1.7), ('h0', 'h1', 'h2'), sd=1, hl=0)       # wrapped grip
    p.fill(E(*pm, 1.8, 1.8), 'y1')
    c.stamp(p, 'K')
    g = (hx + dx * 4, hy + dy * 4)
    p = C()
    p.fill(L(g[0] + nx * 3, g[1] + ny * 3, 1.1, g[0] - nx * 3, g[1] - ny * 3, 1.1), 'y1')   # tsuba
    c.stamp(p, 'K')
    p = C()
    b0 = (hx + dx * 5, hy + dy * 5)
    mid = (hx + dx * (ln * 0.55) + nx * 1.6, hy + dy * (ln * 0.55) + ny * 1.6)
    tip = (hx + dx * ln + nx * 0.5, hy + dy * ln + ny * 0.5)
    blade = L(*b0, 1.5, *mid, 1.5) | L(*mid, 1.5, *tip, 0.6)
    p.fill(blade, 'i3')
    spine = sh(blade, int(round(nx * 1.4)), int(round(ny * 1.4))) & blade
    p.fill(blade & ~sh(blade, -int(round(nx)) or 0, -int(round(ny)) or 0), 'i2')            # spine edge
    p.fill(LN([lerp(b0, mid, 0.3), mid, lerp(mid, tip, 0.6)]), 'v3', only=blade)
    c.stamp(p, 'K')


DEF = dict(
    bob=0, lean=0,
    nw=((62, 21), (73, 13), (90, 18)), nf=((0.25, 1), 17),      # near wing: elbow, wrist, tip ; feather dir, len
    fw=((36, 17), (29, 7), (13, 3)), ff=((-0.4, 1), 13),
    nsh=(49, 33), nelb=(42, 42), nwr=(32, 44), kat=24,
    fsh=(42, 33), fwr=(34, 45),
    fknee=(44, 55), fank=(42, 62), nknee=(52, 55), nank=(52, 62),
    slash=None,
)


def tengu(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    def Lg(pt):
        return P(pt[0] + lean * 0.5, pt[1] + bob)

    # ---- wings (behind everything)
    e, w, t = S['fw']
    wing(c, B((45, 31)), B(e), B(w), B(t), *S['ff'], far=True)
    e, w, t = S['nw']
    wing(c, B((53, 31)), B(e), B(w), B(t), *S['nf'])

    # ---- far sleeve (hand on the scabbard side)
    p = C()
    fs, fwp = B(S['fsh']), B(S['fwr'])
    p.form(L(*fs, 3.6, *fwp, 4.4), ROBF, sd=2, hl=0)
    c.stamp(p, 'K')

    def bird_leg(knee, ank, ramp, robe):
        k_, a_ = Lg(knee), Lg(ank)
        p = C()
        p.form(L(*k_, 1.9, *a_, 1.7), ramp, sd=1, hl=0)
        for dx_, dy_ in ((-5, 6), (-2, 8), (2, 7)):                      # three hooked talons
            p.fill(LN([a_, (a_[0] + dx_, a_[1] + dy_ - 2), (a_[0] + dx_ - 1, a_[1] + dy_)]), ramp[1])
            p.px(a_[0] + dx_ - 1, a_[1] + dy_, 'b3')
            p.px(a_[0] + dx_ - 1, a_[1] + dy_ - 1, 'b2')
        c.stamp(p, 'K')
        p = C()                                                          # hakama leg, gathered below the knee
        hip = Lg((49 if robe is ROBE else 46, 46))
        m = L(*hip, 6.2, *k_, 5.0) | L(*k_, 5.0, k_[0] + (a_[0] - k_[0]) * 0.4, k_[1] + (a_[1] - k_[1]) * 0.4, 3.0)
        p.form(m, robe, sd=3, hl=1)
        p.line([(hip[0] - 2, hip[1] + 1), (k_[0] - 2, k_[1] + 1)], robe[0], only=m)
        c.stamp(p, 'K')

    bird_leg(S['fknee'], S['fank'], ('y0', 'y0', 'y1'), ROBF)
    bird_leg(S['nknee'], S['nank'], ('y0', 'y1', 'y2'), ROBE)

    # ---- torso: suzukake robe, white collar, obi, yuigesa sash with pom-poms
    p = C()
    torso = L(*B((46, 32)), 7.0, *Lg((48, 45)), 6.6)
    p.form(torso, ROBE, sd=4, hl=1)
    p.line([B((40, 30)), B((45, 38)), B((45, 44))], 'v2', only=torso)        # collar edge
    p.line([B((41, 30)), B((46, 38)), B((46, 44))], 'v1', only=torso)
    obi = torso & (px.Y >= Lg((0, 43))[1]) & (px.Y <= Lg((0, 46))[1])
    p.form(obi, ('h0', 'h1', 'h2'), sd=1, hl=1)
    p.line([B((51, 26)), B((49, 34)), B((45, 42))], 'y1', only=torso & ~obi)   # yuigesa strap
    c.stamp(p, 'K')
    for q in ((41, 34), (53, 40)):                                           # pom-poms
        p = C()
        x, y = B(q)
        p.form(E(x, y, 2.8, 2.8), ('v1', 'v2', 'v3'), sd=1, hl=1)
        c.stamp(p, 'K')

    # ---- head (identical grid every frame) + neck ruff
    p = C()
    hx, hy = B((25, 10))
    ruff = PG([(hx + 14, hy + 13), (hx + 24, hy + 11), (hx + 27, hy + 16), (hx + 23, hy + 17), (hx + 24, hy + 21), (hx + 19, hy + 19), (hx + 16, hy + 21), (hx + 14, hy + 17)])
    p.form(ruff, FEA, sd=2, hl=0)
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'K')

    # ---- sword arm
    s_, e_, w_ = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    katana(c, w_, S['kat'])
    p = C()
    p.grid(int(w_[0]) - 2, int(w_[1]) - 2, HAND, LEG)
    c.stamp(p, 'K')
    p = C()
    dx, dy = w_[0] - e_[0], w_[1] - e_[1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    cuff = lerp(e_, w_, 0.72)
    sleeve = PG([(e_[0] + nx * 4, e_[1] + ny * 4), (cuff[0] + nx * 4, cuff[1] + ny * 4),
                 (cuff[0] - nx * 7, cuff[1] - ny * 7), (e_[0] - nx * 4, e_[1] - ny * 4)]) | E(*e_, 4, 4)   # wide hanging sleeve
    if ny > 0:   # keep the sleeve bag hanging downward whatever the arm angle
        sleeve = PG([(e_[0] - nx * 4, e_[1] - ny * 4), (cuff[0] - nx * 4, cuff[1] - ny * 4),
                     (cuff[0] + nx * 7, cuff[1] + ny * 7), (e_[0] + nx * 4, e_[1] + ny * 4)]) | E(*e_, 4, 4)
    p.form(sleeve, ROBE, sd=2, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.form(L(*s_, 4.6, *e_, 4.0), ROBE, sd=2, hl=1)
    p.form(E(s_[0], s_[1] - 1, 5.0, 4.6), ROBE, sd=2, hl=1)
    c.stamp(p, 'm0')

    # ---- sword trail (strike frame only)
    if S['slash']:
        cx, cy, r, a0, a1 = S['slash']
        ang = np.degrees(np.arctan2(-(px.Y - P(cx, cy)[1]), -(px.X - P(cx, cy)[0])))
        ring = E(*P(cx, cy), r, r) & ~E(P(cx, cy)[0] + 2, P(cx, cy)[1] - 1, r - 1, r - 1.5) & (ang >= a0) & (ang <= a1) & ~c.m
        c.fill(ring, 'v2')
        c.fill(ring & ~sh(ring, 1, 0), 'v3')

    c.blacken()
    return c


UP = dict(nw=((61, 17), (70, 6), (86, 0)), nf=((0.5, 1), 17), fw=((36, 13), (30, 2), (18, -7)), ff=((-0.55, 1), 13))
DOWN = dict(nw=((64, 25), (76, 22), (90, 34)), nf=((0.1, 1), 16), fw=((32, 21), (22, 17), (9, 28)), ff=((-0.1, 1), 14))
WALK = [
    dict(bob=0),
    dict(bob=1, **UP, fank=(43, 62), nank=(53, 62)),
    dict(bob=0),
    dict(bob=-2, **DOWN, fank=(41, 63), nank=(51, 63)),
]
ATTACK = [
    dict(bob=-1, lean=2, **UP, nsh=(50, 32), nelb=(47, 23), nwr=(51, 14), kat=128, fwr=(36, 43)),
    dict(bob=1, lean=-5, nw=((65, 22), (80, 19), (98, 24)), nf=((0.15, 1), 18), fw=((34, 20), (22, 16), (4, 22)), ff=((-0.15, 1), 16),
         nsh=(47, 34), nelb=(37, 38), nwr=(27, 42), kat=-12, slash=(18, 34, 27, -35, 75),
         fknee=(47, 55), fank=(49, 61), nknee=(55, 54), nank=(58, 60)),
    dict(bob=1, lean=-3, **DOWN, nsh=(48, 33), nelb=(40, 41), nwr=(31, 46), kat=-48,
         fknee=(45, 55), fank=(45, 62), nknee=(53, 55), nank=(55, 61)),
]

if __name__ == '__main__':
    export(NAME, tengu, WALK, ATTACK)
    zoom(NAME, 6)
