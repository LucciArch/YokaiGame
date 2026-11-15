"""Jinmenju - gnarled tree whose fruits are laughing human heads. Walks on its roots; the heads scream and spit seeds."""
from common import *

NAME = 'jinmenju'
CW, CH = 148, 116
OX, OY = 46, 20           # local baseline y = 92
BARK = ('w0', 'w1', 'w2')
BARKF = ('s0', 'w0', 'w1')
LEAF = ('g0', 'g1', 'g2')

LEG = dict(zip('abcdKqw', ['k0', 'k1', 'k2', 'k3', 'K', 'q', 'b3']))
# head-fruit, looking left: slit eyes under heavy lids, fixed grin. Same grid on every fruit and every walk frame.
FRUIT = """
...bcccb...
..cddccccb.
.cdcccccccb
.cKKKcKKKcb
.cKKacaKKcb
.ccccacccba
.KccccccKba
.KwKwKwKKba
.cKKKKKKbba
..cbbbbbba.
...baaaa...
"""
# attack: the heads scream
FRUIT_SCREAM = """
...bcccb...
..cddccccb.
.cdcccccccb
.cKKKcKKKcb
.cKKacaKKcb
.ccccacccba
.cKwwwwKcba
.cKqqqqKbba
.cKqqqqKba.
..bKKKKba..
...baaa....
"""

FR = [(8, 37), (25, 45), (56, 27), (62, 45), (78, 36)]       # stem tops of the five fruits

DEF = dict(bob=0, lean=0, scream=False, seeds=0, sway=(0, 0, 0, 0, 0),
           roots=((20, 91), (31, 92), (57, 92), (68, 91)))


def P(x, y):
    return (x + OX, y + OY)


def ragged(m, ctr, rx, ry):
    """hanging leaf points along the lower rim of a foliage clump"""
    for i, a in enumerate((200, 225, 250, 275, 300, 325, 350)):
        b_ = (ctr[0] - math.cos(math.radians(a)) * rx * 0.8, ctr[1] - math.sin(math.radians(a)) * ry * 0.8)
        ln = 4.5 if i % 2 else 3
        m = m | PG([(b_[0] - 2, b_[1]), (b_[0] + 2, b_[1]), (b_[0] + (1 if i % 2 else -1), b_[1] + ln)])
    return m


def tree(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):       # the crown sways more than the base
        k = max(0.0, (88 - pt[1]) / 60.0)
        return P(pt[0] + lean * k, pt[1] + (bob if pt[1] < 80 else 0))

    def W(pts, r0, r1):
        return wisp([B(q) for q in pts], r0, r1)

    # ---- far foliage (behind the branches)
    for (x, y, rx, ry) in [(47, 15, 12.4, 8.4), (22, 22, 10.4, 7.4), (66, 18, 10.4, 7.4)]:
        p = C()
        p.form(ragged(E(*B((x, y)), rx, ry), B((x, y)), rx, ry), ('g0', 'g0', 'g1'), sd=2, hl=1)
        c.stamp(p, 'K')

    # ---- roots: far pair, then near pair after the trunk
    def root(tip, ramp, base):
        p = C()
        t = P(*tip)
        mid = ((P(*base)[0] + t[0]) / 2, t[1] - 5)
        m = wisp([P(*base), mid, (t[0], t[1] - 1)], 4.2, 1.3)
        p.form(m, ramp, sd=1, hl=1)
        c.stamp(p, 'K')

    root(S['roots'][1], BARKF, (40, 82)); root(S['roots'][2], BARKF, (48, 82))

    # ---- branches
    p = C()
    br = W([(43, 44), (31, 37), (18, 32), (8, 34)], 4.2, 1.6) | W([(42, 42), (38, 28), (34, 15)], 4.0, 1.5) \
        | W([(45, 44), (58, 35), (70, 29), (79, 32)], 4.2, 1.6) | W([(44, 36), (52, 24), (57, 13)], 3.2, 1.4) \
        | W([(18, 32), (12, 24)], 2.2, 1.2) | W([(70, 29), (74, 20)], 2.2, 1.2) | W([(31, 37), (26, 41)], 2.0, 1.3) \
        | W([(58, 35), (60, 40)], 2.0, 1.3) | W([(34, 15), (31, 6), (27, 1)], 1.6, 0.8) | W([(57, 13), (62, 5), (67, 2)], 1.6, 0.8) \
        | W([(8, 34), (2, 37), (-2, 42)], 1.6, 0.8) | W([(79, 32), (85, 36), (88, 42)], 1.6, 0.8) | W([(44, 36), (45, 24), (43, 12)], 2.0, 0.9)
    p.form(br, BARK, sd=2, hl=1)
    c.stamp(p, 'K')

    # ---- trunk: twisted S-curve with deep bark furrows and a gaping knot
    p = C()
    spine = [(45, 82), (41, 74), (47, 63), (42, 50), (44, 40)]
    tr = W(spine, 9.0, 5.6) | W([(45, 82), (45, 80)], 9.6, 9.0)
    p.form(tr, BARK, sd=4, hl=1)
    core = tr & ~sh(tr, -2, -2)
    p.a[core & (p.a == I('w0'))] = I('s0')
    for off in (-4, 0, 4):                                          # furrows follow the twist
        pts = [B((x + off + (1 if i % 2 else -1), y)) for i, (x, y) in enumerate(spine)]
        p.line(pts, 'w0', only=erode(tr, 1))
    for off in (-3, 1):
        pts = [B((x + off, y)) for (x, y) in spine[1:4]]
        p.line(pts, 'w2', only=erode(tr, 2) & (p.a == I('w1')))
    kx, ky = B((43, 62))
    knot = E(kx, ky, 3.4, 4.2)
    p.fill(knot, 'w0', only=tr); p.fill(E(kx + 0.5, ky + 0.5, 2.0, 2.8), 'K', only=tr)
    c.stamp(p, 'K')

    root(S['roots'][0], BARK, (38, 84)); root(S['roots'][3], BARK, (52, 84))
    # root knuckles catching the light
    c.fill(R(*P(36, 83), *P(38, 83)), 'w2', only=c.a == I('w1'))

    # ---- near foliage clumps on the branch ends
    for (x, y, rx, ry) in [(9, 27, 9.4, 6.4), (33, 11, 10.4, 6.6), (58, 9, 9.4, 6.4), (78, 25, 9.4, 6.6)]:
        p = C()
        m = E(*B((x, y)), rx, ry) | E(*B((x - 5, y + 3)), rx * 0.55, ry * 0.6) | E(*B((x + 5, y + 2)), rx * 0.6, ry * 0.65)
        m = ragged(m, B((x, y)), rx, ry)
        p.form(m, LEAF, sd=3, hl=1)
        b_ = B((x, y))
        for dx_, dy_ in ((-4, -1), (2, -2), (-1, 2)):               # leaf-cluster notches
            p.fill(R(b_[0] + dx_, b_[1] + dy_, b_[0] + dx_ + 2, b_[1] + dy_), 'g0', only=m & (p.a == I('g1')))
        c.stamp(p, 'K')

    # ---- the head fruits
    g = FRUIT_SCREAM if S['scream'] else FRUIT
    for i, (x, y) in enumerate(FR):
        sx = S['sway'][i]
        top = B((x, y)); fx, fy = top[0] + sx, top[1] + 3
        c.line([top, (fx + 1, fy)], 'w0')
        c.line([(top[0] + 1, top[1]), (fx + 2, fy)], 'K')
        p = C()
        p.grid(fx - 5, fy, g, LEG)
        p.fill(R(fx, fy, fx + 2, fy), 'g2')                         # calyx
        p.fill(R(fx + 3, fy, fx + 3, fy), 'g1')
        c.stamp(p, 'K')

    # ---- spat seeds (strike frame)
    for k in range(S['seeds']):
        x, y = FR[k % 5]
        q = B((x - 14 - (k * 7) % 9, y + 10 + (k * 5) % 7))
        p = C()
        p.fill(E(q[0], q[1], 1.9, 1.5), 's2'); p.fill(R(q[0] - 1, q[1] - 1, q[0], q[1] - 1), 'b2')
        c.stamp(p, 'K')
        c.fill(R(q[0] + 4, q[1] - 1, q[0] + 8, q[1] - 1), 'b1')     # motion streak
        c.fill(R(q[0] + 5, q[1], q[0] + 7, q[1]), 'b0')

    c.blacken()
    return c


WALK = [
    dict(bob=0, lean=-1, roots=((17, 91), (33, 92), (55, 92), (70, 91)), sway=(1, 0, 0, 1, 0)),
    dict(bob=-1, lean=0, roots=((21, 89), (30, 92), (58, 92), (67, 89)), sway=(0, 0, 0, 0, 0)),
    dict(bob=0, lean=1, roots=((24, 91), (28, 92), (60, 92), (64, 91)), sway=(-1, 0, -1, 0, -1)),
    dict(bob=-1, lean=0, roots=((20, 91), (31, 90), (57, 90), (68, 91)), sway=(0, 0, 0, 0, 0)),
]
ATTACK = [
    dict(lean=5, bob=1, sway=(2, 1, 1, 2, 1)),
    dict(lean=-6, bob=0, scream=True, seeds=5, sway=(-2, -1, -1, -2, -1), roots=((17, 91), (30, 92), (57, 92), (69, 91))),
    dict(lean=-2, bob=0, scream=True, sway=(-1, 0, 0, -1, 0)),
]

if __name__ == '__main__':
    export(NAME, tree, WALK, ATTACK)
    zoom(NAME, 5)
