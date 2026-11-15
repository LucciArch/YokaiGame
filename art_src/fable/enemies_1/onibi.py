"""Onibi - blue-violet demon fire, an upright blaze with a skull burning inside it."""
from kit import *

NAME = 'onibi'
CW, CH = 96, 72
OX, OY = 42, 14           # local hover line y=50

LEG = dict(zip('Kuvwxqgh', ['K', 'b0', 'b1', 'b2', 'b3', 'q', 'a2', 'v3']))
# skull, 3/4 view facing left: big slanted sockets with cold glow pupils, nose pit, bared teeth
SKULL = """
.....vwwwwvv....
...vxxxxxwwvvu..
..vxxxxxwwwwvvu.
.vxxxwwwwwwwvvu.
.wKKwwwwwwKKKvuu
vwKKKKwwwKKKKvuu
vKKhgKKwKKhgKvuu
vwKKKKKwwKKKKvuu
.vwwwKwKKwwvvuu.
..vwwwKKwwvvuu..
..vwwwwwwwvvu...
..xKxKxKxKwvu...
..xKxKwKwKvu....
..x.x.w.w.u.....
"""

DEF = dict(bob=0, fl=0, puff=0.0, lean=0, spit=None, sparks=0)


def P(x, y):
    return (x + OX, y + OY)


def tongue(base, mid, tip, r):
    return tube(curve([base, mid, tip]), r, 0.9)


def fireball(c, x, y, r, tail):
    p = C()
    m = E(x, y, r, r) | tube(curve([(x + 1, y - 1), (x + r + tail * 0.5, y - 3), (x + r + tail, y - 2)]), r * 0.8, 0.8)
    glowlayers(p, m, ('p1', 'p2', 'p3'), (1, 2))
    c.stamp(p, 'p0')


def creature(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    b, fl, pf, ln = S['bob'], S['fl'], S['puff'], S['lean']
    cx, cy = 22 + ln, 35 + b
    # flick pattern per frame: (dx of tips, height factor)
    F = [(0, 0, 0), (2, -2, 1), (0, 1, -1), (-2, -1, 2)][fl % 4]
    # sparks torn off the top
    p = C()
    for i, (dx, dy) in enumerate(((11, -24), (-9, -20), (18, -13))):
        k = (S['sparks'] + i) % 3
        q = P(cx + dx + k, cy + dy - k * 2 - pf * 2)
        m = L(q[0], q[1], 1.7, q[0] + 2, q[1] - 3, 0.6)
        if k != 2 or i == 0:
            p.fill(m, 'p2')
    c.stamp(p, 'p0')
    p = C()
    body = E(*P(cx, cy), 13.2 + pf, 12.4 + pf)
    m = body
    m |= tongue(P(cx - 1, cy - 8), P(cx + 2 + F[0], cy - 19 - pf * 2), P(cx + 7 + F[0] * 2, cy - 28 + F[1] - pf * 4), 6.4 + pf)   # centre
    m |= tongue(P(cx - 8, cy - 6), P(cx - 9 - F[0], cy - 14 - pf), P(cx - 5 - F[0], cy - 21 + F[2] - pf * 3), 4.6)              # front
    m |= tongue(P(cx + 8, cy - 5), P(cx + 13 + F[0], cy - 12 - pf), P(cx + 17 + F[0] * 2, cy - 20 - F[2] - pf * 3), 5.0)       # back
    m |= tongue(P(cx + 9, cy + 4), P(cx + 15, cy + 2 + F[2]), P(cx + 20 + F[0], cy - 3 + F[2]), 3.8)                          # low side lick
    m |= tongue(P(cx - 2, cy + 8), P(cx + 3, cy + 13), P(cx + 8 + F[0], cy + 14), 3.6)                                        # hanging drip-tail
    p.fill(m, 'p0')
    p.fill(erode(m, 1), 'p1')
    p.fill(erode(m, 3), 'p2')
    halo = E(*P(cx - 2, cy), 12.2, 11.6) | tongue(P(cx - 1, cy - 6), P(cx + 1 + F[0], cy - 13), P(cx + 4 + F[0], cy - 19 - pf * 2), 3.4)
    p.fill(halo & erode(m, 3), 'p3')
    p.fill(E(*P(cx - 2, cy), 13.0, 12.4) & erode(m, 2) & ~(halo & erode(m, 3)), 'p2')
    c.stamp(p, 'p0')
    p = C()
    p.grid(*P(cx - 10, cy - 7), SKULL, LEG)
    c.stamp(p, 'p0')
    if S['spit']:
        fireball(c, *P(*S['spit'][:2]), S['spit'][2], S['spit'][3])
    c.blacken()
    return c


WALK = [dict(bob=0, fl=0, sparks=0), dict(bob=-1, fl=1, sparks=1), dict(bob=-2, fl=2, sparks=2), dict(bob=-1, fl=3, sparks=0)]
ATTACK = [dict(bob=-2, fl=1, puff=2.0, lean=3, sparks=1),
          dict(bob=-1, fl=3, puff=-0.6, lean=-4, spit=(-9, 40, 4.4, 5), sparks=2),
          dict(bob=-1, fl=2, puff=0, lean=-1, spit=(-27, 40, 3.4, 5), sparks=0)]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
