"""Yosuzume: the night sparrow. Small, dark, one glowing eye; follows travellers and dives to peck."""
from kit import *
import px

NAME = 'yosuzume'
CW, CH = 72, 64
OX, OY = 22, 18
DARK = ('h0', 'h1', 'i2')
WING = ('s0', 's1', 's2')
WINGF = ('K', 's0', 's1')

LEG = dict(zip('abcKYZRvwihI', ['s0', 's1', 's2', 'K', 'y2', 'y3', 'e1', 'b1', 'b2', 'i2', 'h0', 'i3']))
HEAD = """
....aaaaaa...
..aabbbbbaa..
.abbccbbbbba.
.aKKKKbbbbbaa
.KRYYRKiibbba
wKYZKYKIiibba
vwKYYKiiiibba
.vvKKiihiibba
..hhhhhhiiba.
...hhhhhiba..
"""

DEF = dict(bob=0, head=(0, 0), tail=(0, 0), wt='up', streak=0)


def P(x, y):
    return (x + OX, y + OY)


POSES = {
    'up': ([(-3, 0), (1, -9), (7, -20), (10, -19), (10, -14), (13, -13), (12, -8), (15, -6), (12, -1), (8, 2)],
           [((1, -3), (10, -14)), ((3, -1), (12, -8))]),
    'level': ([(-3, -1), (5, -5), (17, -7), (21, -5), (17, -3), (19, -1), (13, 0), (14, 2), (8, 3)],
              [((2, -1), (17, -3)), ((4, 1), (13, 0))]),
    'down': ([(-3, 0), (0, 8), (6, 18), (9, 17), (9, 13), (12, 11), (11, 7), (14, 5), (11, 0), (6, -2)],
             [((1, 2), (9, 13)), ((4, 0), (11, 7))]),
    'swept': ([(-3, -1), (5, -8), (16, -16), (19, -14), (16, -10), (19, -8), (14, -5), (15, -2), (8, 2)],
              [((2, -2), (16, -10)), ((4, 0), (14, -5))]),
}


def wing(p, shd, pose, ramp):
    poly, lines = POSES[pose]
    m = PG([(shd[0] + x, shd[1] + y) for x, y in poly])
    p.form(m, ramp, sd=2, hl=1)
    for a, b in lines:
        p.line([(shd[0] + a[0], shd[1] + a[1]), (shd[0] + b[0], shd[1] + b[1])], ramp[0], only=erode(m))
    return m


def bird(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    b = S['bob']
    bx, by_ = P(18, 18 + b)
    hdx, hdy = S['head']; tdx, tdy = S['tail']
    shd = (bx - 1, by_ - 3)
    # far wing
    p = C(); wing(p, (shd[0] + 4, shd[1] - 1), S['wt'], WINGF); c.stamp(p, 'K')
    # tail fan
    p = C()
    tx, ty = bx + 8 + tdx, by_ + tdy
    tl = PG([(bx + 5, by_ - 2), (tx + 8, ty - 2), (tx + 13, ty - 4), (tx + 14, ty - 1), (tx + 10, ty), (tx + 13, ty + 3), (tx + 9, ty + 4), (bx + 5, by_ + 3)])
    p.form(tl, WING, sd=2, hl=1)
    p.line([(bx + 7, by_ + 1), (tx + 9, ty)], 's0', only=tl)
    c.stamp(p, 'K')
    # body
    p = C()
    body = L(bx - 5 + hdx * 0.5, by_ - 1 + hdy * 0.5, 6.4, bx + 5 + tdx * 0.4, by_ + 1 + tdy * 0.4, 5.2)
    p.form(body, DARK, sd=3, hl=1)
    belly = body & ~sh(body, 0, 4) & (px.X < bx + 4)
    p.a[belly & (p.a == I('h1'))] = I('i1')
    # tucked claws
    p.fill(R(bx + 1, by_ + 6, bx + 3, by_ + 6), 's2')
    c.stamp(p, 'K')
    # head
    p = C()
    p.grid(bx - 16 + hdx, by_ - 9 + hdy, HEAD, LEG)
    c.stamp(p, 'K')
    # near wing
    p = C(); wing(p, shd, S['wt'], WING); c.stamp(p, 'K')
    c.blacken()
    if S['streak']:
        for (x, y, n) in ((14, -14, 7), (20, -8, 9), (8, -18, 5)):
            c.line([(bx + x, by_ + y), (bx + x + n, by_ + y - n)], 'i2')
    return c


WALK = [
    dict(bob=1, wt='up'),
    dict(bob=0, wt='level', tail=(0, 1)),
    dict(bob=-1, wt='down', tail=(0, -1)),
    dict(bob=0, wt='level'),
]
ATTACK = [
    dict(bob=-3, head=(2, -2), tail=(-1, 4), wt='up'),
    dict(bob=4, head=(-3, 5), tail=(2, -7), wt='swept', streak=1),
    dict(bob=2, head=(0, 1), tail=(0, -1), wt='down'),
]

if __name__ == '__main__':
    export(NAME, bird, WALK, ATTACK, review=5)
