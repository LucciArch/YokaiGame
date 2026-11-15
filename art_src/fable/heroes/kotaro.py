"""Kotaro - karasu-tengu youth: crow beak mask, black wings, green yamabushi garb, shakujo staff. Attack: wing gust."""
from herolib import *

NAME = 'kotaro'
GRN = ('g1', 'g2', 'g3')
GRD = ('g0', 'g1', 'g2')
FEA = ('h0', 'h1', 'h2')
FEAD = ('K', 'h0', 'h1')
L_ = dict(LEG, T='i2', t='i3', Y='y2', y='y1', z='y0', e='e1', E='y3', r='m2')
HEAD = """
..........mm.......
.......mmmnnmm..m..
.....mmnnnnnnnmmnm.
....mnooonnnnnnnnm.
...mnooTTTnnnnnnnnm
...mnnTTtTTnnnnnnm.
...mnnrTTTrnnnnnnnm
..mnnmnnnnnnmnnnnnm
..mnmcmccmcnmnnnnm.
..mKKKccKKKKcmnnnnm
..cKWcccKeWccrnnnm.
..cccccccccrrmnnnm.
.YYYYYYYyyrbmmnnm..
YYyyyyyyyzbbmnm....
.zKKKKKyzzbbm.m....
..zzyyyzzbb........
....zzzbb..........
"""

DEF = dict(bob=0, lean=0, nsh=(44, 29), nelb=(39, 38), nwr=(29, 35), wang=93, ffoot=30, nfoot=44, flift=0, nlift=0,
           sleeve=0, wj=(53, 21), wa=(262, 284), wl=34, fj=(49, 19), fa=(270, 292), fl=30, gust=None)


def wing(g, root, joint, a0, a1, ln, ramp, n=7):
    c = g.c
    p = C()
    tips = []
    for i in range(n):
        t = i / (n - 1)
        ang = a0 + (a1 - a0) * t
        ll = ln * (0.62 + 0.38 * t)
        dx, dy = vec(ang)
        tips.append((joint[0] + dx * ll * 0.93, joint[1] + dy * ll * 0.93))
    p.fill(PG([joint] + tips), ramp[0])
    for i in range(n - 1, -1, -1):
        t = i / (n - 1)
        ang = a0 + (a1 - a0) * t
        ll = ln * (0.62 + 0.38 * t)
        dx, dy = vec(ang)
        p.form(L(joint[0], joint[1], 3.0, joint[0] + dx * ll, joint[1] + dy * ll, 1.9), ramp, sd=1, hl=1)
    p.form(L(*root, 3.4, *joint, 3.2), ramp, sd=2, hl=1)
    dx, dy = vec((a0 + a1) / 2)
    for k in (0, 1):            # covert rows
        q = (joint[0] + dx * (4 + k * 5), joint[1] + dy * (4 + k * 5))
        p.form(E(q[0], q[1], 4.2 - k * 0.6, 3.4), ramp, sd=1, hl=1, only=p.m)
    c.stamp(p, 'K')


def shakujo(g, wr, ang):
    c = g.c
    dx, dy = vec(ang)
    top = (wr[0] + dx * 29, wr[1] + dy * 29)
    butt = (wr[0] - dx * 31, wr[1] - dy * 31)
    p = C()
    p.form(L(*butt, 0.9, *top, 0.9), WOOD, sd=0, hl=1)
    c.stamp(p, 'K')
    rc = (top[0] + dx * 4, top[1] + dy * 4)
    p = C()
    ringm = E(rc[0], rc[1], 4.4, 4.4) & ~E(rc[0], rc[1], 2.3, 2.3)
    p.form(ringm, GOLD, sd=1, hl=1)
    p.form(L(top[0] - dx * 2, top[1] - dy * 2, 1.5, top[0], top[1], 1.5), GOLD, sd=1, hl=0)
    c.stamp(p, 'K')
    for sx in (-5, 4):          # small jingling rings
        p = C()
        x0, y0 = int(rc[0]) + sx, int(rc[1]) + 3
        p.fill(R(x0, y0, x0 + 2, y0 + 3), 'y1'); p.fill(R(x0 + 1, y0 + 1, x0 + 1, y0 + 2), None); p.px(x0, y0, 'y2')
        c.stamp(p, 'K')


def kotaro(**kw):
    S = dict(DEF); S.update(kw)
    g = Rig(S)
    c, B, P = g.c, g.B, g.P

    wing(g, B((40, 29)), B(S['fj']), *S['fa'], S['fl'], FEAD, n=6)
    wing(g, B((46, 30)), B(S['wj']), *S['wa'], S['wl'], FEA)

    # far sleeve
    p = C()
    fs = PG([B((36, 28)), B((33, 33)), B((32, 41)), B((38, 43)), B((40, 30))])
    p.form(fs, GRD, sd=2, hl=1)
    c.stamp(p, 'K')

    g.feet('geta', strap=WH)
    p, hk = g.hakama(GRD, 'K', stamp=False)
    kya = hk & (px.Y >= P(0, 59)[1])                 # white leg wraps under the knee-length hakama
    p.form(kya, WHD, sd=3, hl=1)
    p.fill(hk & (px.Y == P(0, 58)[1]), 'K')
    c.stamp(p, 'K')
    p = C()
    p.form(R(*B((35, 36)), *B((46, 39))), WHD, sd=1, hl=1)
    p.fill(R(*B((35, 38)), *B((46, 38))), 'v0')
    c.stamp(p, 'K')

    p = C()
    torso = L(*B((40, 30)), 5.6, *B((41, 35)), 5.2)
    p.form(torso, GRN, sd=2, hl=1)
    p.line([B((36, 26)), B((40, 33))], 'v2', only=torso)
    p.line([B((44, 26)), B((40, 34))], 'g0', only=torso)
    p.line([B((37, 27)), B((37, 35))], 'y1', only=torso)       # yuigesa strap
    c.stamp(p, 'K')
    for (qx, qy) in ((35, 29), (36, 34)):                       # pom-poms
        p = C(); q = B((qx, qy))
        p.fill(R(q[0], q[1], q[0] + 2, q[1] + 2), 't1'); p.fill(R(q[0], q[1], q[0] + 1, q[1] + 1), 't2')
        c.stamp(p, 'K')
    p = C()
    p.form(R(*B((38, 24)), *B((41, 26))), ('k0', 'k1', 'k2'), sd=1, hl=0)
    c.stamp(p, 'K', ring=False)

    g.head(HEAD, L_, (29, 8))
    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    shakujo(g, wr, S['wang'])
    g.arm(sh_, el, wr, GRN, sv=S['sleeve'], bag=9, hleg=L_)

    if S['gust']:
        for (cx, cy, r, a0, a1, w_) in S['gust']:
            q = B((cx, cy))
            m = arc(q[0], q[1], r - w_, r, a0, a1)
            p = C()
            p.fill(m, 'a2'); p.fill(m & arc(q[0], q[1], r - 1.5, r, a0, a1, taper=False), 'v3')
            c.stamp(p, ring=False)
    return g.done()


WALK = [
    dict(bob=0, ffoot=26, nfoot=48, sleeve=1, wa=(262, 286), fa=(270, 294)),
    dict(bob=-1, ffoot=33, nfoot=42, nlift=2),
    dict(bob=0, ffoot=40, nfoot=34, sleeve=-1, wa=(260, 282), fa=(268, 290)),
    dict(bob=-1, ffoot=33, flift=2, nfoot=41),
]
ATTACK = [
    dict(lean=2, bob=-1, wj=(55, 18), wa=(42, 96), wl=27, fj=(49, 15), fa=(62, 112), fl=22, nelb=(41, 38), nwr=(32, 34), wang=100,
         ffoot=31, nfoot=46),
    dict(lean=-3, bob=1, wj=(42, 13), wa=(168, 226), wl=28, fj=(35, 14), fa=(172, 214), fl=22, nelb=(44, 38), nwr=(40, 33), wang=80,
         ffoot=25, nfoot=48, sleeve=2,
         gust=((30, 34, 38, 150, 215, 5), (30, 32, 47, 160, 205, 4), (34, 40, 30, 170, 222, 3))),
    dict(lean=-1, wj=(50, 21), wa=(215, 268), wl=28, fj=(46, 19), fa=(230, 280), fl=25, nelb=(40, 38), nwr=(31, 35), wang=92,
         ffoot=28, nfoot=46, gust=((16, 33, 40, 165, 200, 3),)),
]

if __name__ == '__main__':
    build(NAME, kotaro, WALK, ATTACK)
