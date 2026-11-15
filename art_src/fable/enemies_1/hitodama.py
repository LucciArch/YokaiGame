"""Hitodama - floating blue-white soul flame, comma-shaped with a long wispy tail and a faint wailing face."""
from kit import *

NAME = 'hitodama'
CW, CH = 100, 70
OX, OY = 32, 16            # local hover line (lowest point of the idle flame) y=46
COLS = ('a0', 'a1', 'a2', 'v3')

LEG = dict(zip('Kabcw', ['K', 'a0', 'a1', 'a2', 'v3']))
# faint ghost face: slanted hollow sockets, wailing mouth. identical in every frame.
FACE = """
aa.......a.
baa.....aab
.aKa...aKaa
.aKKa.aKKa.
..aa...aa..
...........
...baaab...
..aKKKKKa..
..aKKKKKa..
...aKKKa...
....bab....
"""

DEF = dict(bob=0, sway=0.0, puff=0.0, stretch=0, spit=None, embers=0)


def P(x, y):
    return (x + OX, y + OY)


def wisp(c, x, y, r, tail):
    """small spat soul-fire: ball + short trailing tail (to the right)"""
    p = C()
    m = E(x, y, r, r * 0.9) | tube(curve([(x + 1, y - 1), (x + r + tail * 0.5, y - 2), (x + r + tail, y - 4)]), r * 0.8, 0.6)
    glowlayers(p, m, ('a1', 'a2', 'v3'), (1, 2))
    c.stamp(p, 'a0')


def creature(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    b, sw, pf, st = S['bob'], S['sway'], S['puff'], S['stretch']
    hx, hy = 15 - st, 33 + b
    tip = (49 + sw * 3 + st * 2, 8 + b - pf * 3)
    # loose ember tongues breaking off the tail
    if S['embers'] is not None:
        p = C()
        e = S['embers']
        for (dx, dy, r) in ((3 + e, 9 + e * 2, 1.9), (-9 - e, -2 - e, 1.5)):
            q = P(tip[0] + dx, tip[1] + dy)
            m = L(q[0], q[1], r, q[0] + 3, q[1] - 4, 0.6)
            p.fill(m, 'a1'); p.fill(erode(m, 1), 'a2')
        c.stamp(p, 'a0')
    # main flame: round head + S-curved tapering tail that whips up to the right
    p = C()
    spine = curve([(hx + 3, hy - 2), (hx + 11 + st, hy - 9 - pf * 2), (hx + 20 + sw * 3 + st, hy - 12 - sw * 2 - pf * 3),
                   (hx + 25 - sw * 3 + st * 2, hy - 17 - pf * 3), (hx + 28 + sw * 2 + st * 2, hy - 21 - pf * 3), tip])
    head = E(*P(hx, hy), 10.4 + pf + st * 0.5, 9.6 + pf)
    n = len(spine)
    radii = [max(1.0, (8.4 + pf) * (1 - i / (n - 1)) ** 1.3) for i in range(n)]
    tail = tube([P(*q) for q in spine], 0, 0, radii)
    lick = tube([P(*q) for q in curve([(hx + 5, hy - 6), (hx + 8 - sw, hy - 14 - pf * 2), (hx + 13 - sw * 2, hy - 20 - pf * 4)])], 3.8 + pf, 1.0)
    curl = tube([P(*q) for q in curve([(hx + 14 + st, hy - 5), (hx + 23 + st + sw, hy - 5 - pf), (hx + 29 + st + sw * 2, hy - 10 - pf * 2)])], 3.6, 1.0)
    m = head | tail | lick | curl
    p.fill(m, 'a0')
    p.fill(erode(m, 1), 'a1')
    inner = erode(m, 3) | erode(tail & ~head, 2)
    p.fill(inner, 'a2')
    core = E(*P(hx - 1, hy), 6.8 + pf, 6.2 + pf) | tube([P(*q) for q in spine[:12]], 3.8 + pf, 1.0)
    p.fill(core & erode(m, 4), 'v3')
    for i in (20, 27):
        q = P(*spine[i]); qx, qy = int(q[0]), int(q[1])
        if all(p.a[qy, qx + k] == I('a2') for k in (-1, 0, 1, 2)) and p.a[qy - 1, qx] == I('a2') and p.a[qy + 1, qx] == I('a2'):
            p.pxs([(qx, qy), (qx + 1, qy)], 'v3')
    c.stamp(p, 'a0')
    # face
    p = C()
    p.grid(*P(hx - 8, hy - 6), FACE, LEG)
    c.stamp(p, ring=False)
    if S['spit']:
        wisp(c, *P(*S['spit'][:2]), S['spit'][2], S['spit'][3])
    c.blacken()
    return c


WALK = [dict(bob=0, sway=0.0, embers=0), dict(bob=-1, sway=0.6, embers=1), dict(bob=-2, sway=0.0, embers=2), dict(bob=-1, sway=-0.6, embers=1)]
ATTACK = [dict(bob=-2, puff=1.6, stretch=-3, sway=0.3, embers=None),
          dict(bob=-1, puff=-0.4, stretch=4, sway=-0.4, spit=(-7, 35, 3.6, 5), embers=2),
          dict(bob=-1, puff=0, stretch=1, sway=0.2, spit=(-20, 35, 2.8, 4), embers=0)]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
