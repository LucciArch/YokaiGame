"""Heikegani - crab carrying the furious face of a drowned Heike samurai on its shell; huge pincers."""
from common import *

NAME = 'heikegani'
CW, CH = 136, 78
OX, OY = 40, 18           # local baseline y = 56
SK = ('r1', 'r2', 'r3')
FAR = ('r0', 'r1', 'r2')

LEG = dict(zip('abcdeKYZqwv', ['r0', 'r1', 'r2', 'r3', 'r4', 'K', 'y2', 'y3', 'q', 'b2', 'b1']))
# relief face on the carapace: knotted brows, sunken glowing eyes glaring left, flared nose, clenched grimace
FACE = """
....dd...............dd....
..aaaddd...........dddaaa..
.aKKKaaddd.......dddaaKKKa.
..aaKKKKaadd...ddaaKKKKaa..
....aaKKKKKad.daKKKKKaa....
....aZYYaaKKa.aKKaZYYaa....
....aaYYYaaa.d.aaaYYYa.....
......aaa...ddd...aaa......
...........adddd...........
..d.......aaddddaa......d..
..da......aaaaaaa......ad..
..aa.aKKKKKKKKKKKKKKKa.aa..
..a.aKwvwwvwwvwwvwwvwKa.a..
...aKKa.KKKKKKKKKKK.aKKa...
...aa....aaaaaaaaa....aa...
"""

DEF = dict(bob=0, lean=0,
           lel=(9, 33), lcl=(5, 23), ldeg=62, lopen=38,           # big left (front) pincer: elbow, claw base, direction, gape
           rel=(70, 31), rcl=(74, 21), rdeg=100, ropen=30,
           lt=((7, 56), (14, 56), (22, 56)), rt=((73, 56), (66, 56), (58, 56)))


def P(x, y):
    return (x + OX, y + OY)


def claw(c, base, deg, opn, sz, ramp):
    a = math.radians(deg)
    d = (-math.cos(a), -math.sin(a)); up = (-d[1], d[0])
    if up[1] > 0:
        up = (-up[0], -up[1])
    a2 = math.radians(deg - opn if d[0] <= 0 else deg + opn)
    d2 = (-math.cos(a2), -math.sin(a2)); up2 = (-d2[1], d2[0])
    if up2[1] > 0:
        up2 = (-up2[0], -up2[1])
    ctr = (base[0] + d[0] * sz * 0.8, base[1] + d[1] * sz * 0.8)

    def q(dd, uu, f, s):
        return (ctr[0] + dd[0] * sz * f + uu[0] * sz * s, ctr[1] + dd[1] * sz * f + uu[1] * sz * s)

    p = C()                                                             # movable lower finger
    low = wisp([q(d2, up2, 0.0, -0.35), q(d2, up2, 1.1, -0.5), q(d2, up2, 2.0, -0.2), q(d2, up2, 2.5, 0.25)], sz * 0.42, 0.8)
    p.form(low, (ramp[0], ramp[0], ramp[1]) if ramp is SK else ramp, sd=1, hl=1)
    tp = q(d2, up2, 2.5, 0.25); p.px(int(round(tp[0])), int(round(tp[1])), 'b2')
    c.stamp(p, 'r0')
    p = C()                                                             # palm bulb + fixed upper finger
    upf = wisp([q(d, up, 0.2, 0.3), q(d, up, 1.2, 0.5), q(d, up, 2.1, 0.15), q(d, up, 2.7, -0.35)], sz * 0.58, 0.8)
    bulb = E(ctr[0], ctr[1], sz * 1.05, sz * 0.95)
    m = upf | bulb
    p.form(m, ramp, sd=3 if sz > 5 else 2, hl=1)
    g = q(d, up, 0.4, 0.55)
    p.fill(R(g[0] - 1, g[1], g[0] + 1, g[1]), 'r4', only=m)             # wet glint
    for f in (1.0, 1.5, 2.0):                                           # bone teeth on the cutting edge
        t = q(d, up, f, -0.15 if f < 1.9 else -0.2)
        p.px(int(round(t[0])), int(round(t[1])), 'b2')
    tp = q(d, up, 2.7, -0.35); p.px(int(round(tp[0])), int(round(tp[1])), 'b3')
    c.stamp(p, 'r0')


def crab(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    # ---- walking legs: 3 jointed pairs, drawn behind the shell
    hips_l = [(27, 45), (30, 47), (33, 48)]
    hips_r = [(53, 45), (50, 47), (47, 48)]
    for side, hips, tips in ((-1, hips_l, S['lt']), (1, hips_r, S['rt'])):
        for i in (2, 1, 0):
            h_, t_ = B(hips[i]), P(*tips[i])
            kn = (h_[0] + side * (11 - i * 3.5), h_[1] - 5 + i * 1.5)
            ramp = FAR if i == 2 else SK
            p = C()
            p.form(L(*h_, 2.6, *kn, 2.1), ramp, sd=1, hl=1)
            p.form(L(*kn, 2.1, t_[0], t_[1] - 1, 0.9), ramp, sd=1, hl=1)
            p.px(t_[0], t_[1], 'b2')
            c.stamp(p, 'r0')

    # ---- right pincer (smaller, raised)
    sh_r = B((57, 37)); el, cl = B(S['rel']), B(S['rcl'])
    p = C()
    p.form(L(*sh_r, 3.4, *el, 3.0), SK, sd=2, hl=1); p.form(L(*el, 3.0, *cl, 2.6), SK, sd=1, hl=1)
    c.stamp(p, 'r0')
    claw(c, cl, S['rdeg'], S['ropen'], 5.0, SK)

    # ---- carapace
    p = C()
    cx, cy = B((40, 35))
    shell = E(cx, cy, 20.4, 13.4) | PG([(cx - 21, cy - 6), (cx - 13, cy - 13), (cx + 13, cy - 13), (cx + 21, cy - 6), (cx + 12, cy + 12), (cx - 12, cy + 12)])
    spikes = PG([(cx - 19, cy - 8), (cx - 25, cy - 11), (cx - 20, cy - 3)]) | PG([(cx + 19, cy - 8), (cx + 25, cy - 11), (cx + 20, cy - 3)]) \
        | PG([(cx - 21, cy - 1), (cx - 25, cy - 1), (cx - 20, cy + 3)]) | PG([(cx + 21, cy - 1), (cx + 25, cy - 1), (cx + 20, cy + 3)])
    full = shell | spikes
    p.form(full, SK, sd=4, hl=1)
    core = full & ~sh(full, -2, -2)
    p.a[core & (p.a == I('r1'))] = I('r0')
    p.grid(cx - 15, cy - 10, FACE, LEG)
    # topknot ridge + forehead glint
    p.fill(R(cx - 10, cy - 11, cx - 5, cy - 11), 'r4', only=shell)
    for i in range(3):   # shell grooves on the shaded flank
        p.line([(cx + 14 + i * 2, cy - 6 + i * 3), (cx + 17 + i, cy - 4 + i * 3)], 'r0', only=shell)
    c.stamp(p, 'r0')
    # stalk eyes peeking over the shell rim
    for ex in (-5, 4):
        p = C()
        p.fill(R(cx + ex, cy - 17, cx + ex + 1, cy - 14), 'r1')
        p.fill(R(cx + ex, cy - 18, cx + ex + 1, cy - 17), 'K')
        p.px(cx + ex, cy - 18, 'v3')
        c.stamp(p, 'r0')
    # mouth plates under the chin
    p = C()
    p.form(PG([(cx - 6, cy + 12), (cx + 6, cy + 12), (cx + 4, cy + 16), (cx - 4, cy + 16)]), ('c0', 'c1', 'c2'), sd=1, hl=0)
    p.line([(cx, cy + 12), (cx, cy + 16)], 'c0')
    c.stamp(p, 'r0')

    # ---- big left pincer, in front of everything
    sh_l = B((23, 38)); el, cl = B(S['lel']), B(S['lcl'])
    p = C()
    p.form(L(*sh_l, 4.2, *el, 3.8), SK, sd=2, hl=1); p.form(L(*el, 3.8, *cl, 3.2), SK, sd=2, hl=1)
    p.form(E(*el, 4.2, 4.0), SK, sd=2, hl=1)
    c.stamp(p, 'r0')
    claw(c, cl, S['ldeg'], S['lopen'], 7.4, SK)

    c.blacken()
    return c


WALK = [
    dict(bob=0, lt=((5, 56), (15, 55), (21, 56)), rt=((75, 56), (65, 55), (59, 56))),
    dict(bob=-1, lt=((8, 55), (12, 56), (23, 55)), rt=((72, 55), (68, 56), (57, 55)), lopen=30),
    dict(bob=0, lt=((9, 56), (13, 55), (24, 56)), rt=((71, 56), (67, 55), (56, 56))),
    dict(bob=-1, lt=((6, 55), (16, 56), (22, 55)), rt=((74, 55), (64, 56), (58, 55)), lopen=44),
]
ATTACK = [
    dict(lean=3, bob=-1, lel=(13, 28), lcl=(14, 16), ldeg=80, lopen=62, ropen=50, rdeg=95),
    dict(lean=-5, bob=2, lel=(5, 38), lcl=(-6, 36), ldeg=6, lopen=3, rel=(69, 35), rcl=(66, 25), rdeg=140, ropen=4,
         lt=((3, 56), (12, 56), (20, 56))),
    dict(lean=-2, bob=1, lel=(7, 35), lcl=(0, 28), ldeg=35, lopen=22, ropen=20),
]

if __name__ == '__main__':
    export(NAME, crab, WALK, ATTACK)
    zoom(NAME, 6)
