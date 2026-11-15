"""Rokurokubi: floating head (boss_rokuro_head) + seated headless kimono body with neck stump (boss_rokuro_body).
Neck anchors (cell coords): head HN = where the neck leaves the head sprite; body BN_ = top of the neck stump."""
from bl import *

HAIR = ('h0', 'hb', 'h2')
SKN = ('k1', 'k2', 'k3')
PUR = ('p1', 'p2', 'p3')
PFAR = ('p0', 'p1', 'p2')
RED = ('m1', 'm2', 'm3')

LEG = dict(zip('abcdmnoKEZrqWs', ['k0', 'k1', 'k2', 'k3', 'h0', 'hb', 'h2', 'K', 'e1', 'y3', 'm2', 'q', 'v3', 'm1']))
FACE = """
........mmmmmmmm........
......mmnnnnnnnnmm......
....mmnnoonnnnnnnnmm....
...mnnoonnnnnnnnnnnnm...
..mnnonnnnnnnnnnnnnnnm..
..mnnnnnnnnnnnnnnnnnnm..
.mnnnmnnnnmnnnnnnnnnnnm.
.mnnmcmnnmcmmnnnnnnnnnm.
.mnmcccmmcccccmnnnnnnnm.
.mmdccccccccccmnnnnnnnm.
.cddKKccccccKKcmnnnnnnm.
.cKKKKKccKKKKKbmnnnnnnm.
.cqEZKccKqEEZKbmnnnnnnm.
.cdssccccssscbbmnnnnnnm.
.cdccccccccccbbmnnnnnnm.
..cdcccccccccbamnnnnnnm.
..cbacccccccbbamnnnnnm..
..crrrrrrccbbba.mnnnnm..
...rWqWqWrcbba..mnnnm...
...ccrrrccbbaa...mnnm...
....cccccbbaa.....mm....
.....bbbbaa.............
"""
BITE = """
.crrrrrrrccbbba
.rWqWqWqWrcbba.
.rqqqqqqqqrbba.
.rqqqqqqqqrbba.
.rqqrrrqqqrbaa.
.rWqWqWqWrcba..
..rrrrrrrccaa..
...cccccbbaa...
....bbbbaa.....
"""

# ------------------------------------------------------------------ head
HCW, HCH = 132, 104
HOX, HOY = 32, 34
HDEF = dict(dx=0, dy=0, wave=0, stream=0, bite=False)
HN = (HOX + 30, HOY + 40)


def rhead(**kw):
    S = dict(HDEF); S.update(kw)
    setsize(HCW, HCH)
    c = C()
    ox, oy = HOX + S['dx'], HOY + S['dy']
    wv, st = S['wave'], S['stream']

    def h(x, y):
        return (ox + x, oy + y)
    # flowing hair behind: wavy tapering locks drifting to the right
    p = C()
    p.form(E(*h(22, 12), 9, 10.4), HAIR, sd=3, hl=0)
    c.stamp(p, 'K')
    specs = [(3, -4, 44, 0.0, 3.6), (8, 0, 54, 1.6, 4.2), (13, 5, 60, 3.0, 4.4), (17, 12, 52, 4.4, 4.0), (20, 20, 42, 5.6, 3.4),
             (21, 28, 30, 0.8, 2.6)]
    for i, (y0, dy, ln_, ph, r) in enumerate(specs):
        pts = []
        for k in range(7):
            t = k / 6
            amp = (3.0 + wv) * t * (1 - st / 14.0)
            x = 22 + t * (ln_ + st * 0.6)
            y = y0 + dy * t * (1 - st / 16.0) + amp * math.sin(ph + wv * 0.5 + t * 5.0)
            pts.append(h(x, y))
        m = np.zeros((px.H, px.W), bool)
        for k in range(6):
            r0_ = r * (1 - k / 6.6); r1_ = r * (1 - (k + 1) / 6.6)
            m |= L(*pts[k], max(r0_, 0.8), *pts[k + 1], max(r1_, 0.6))
        p = C()
        p.form(m, HAIR, sd=2, hl=0)
        p.line([(x_, y_ - 1) for x_, y_ in pts[1:5]], 'h2', only=m)
        c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # neck leaving down-right (the game chains the rest)
    p = C()
    nk = L(*h(12, 20), 2.6, *h(18, 31), 2.6) | L(*h(18, 31), 2.6, *h(30, 40), 2.6)
    p.form(nk, SKN, sd=2, hl=1)
    c.stamp(p, 'K')
    # head grid
    p = C()
    p.grid(ox, oy, FACE, LEG)
    if S['bite']:
        p.a[oy + 17:oy + 22, ox:ox + 16] = 0
        p.grid(ox + 1, oy + 17, BITE, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # side lock in front of the ear + loose hair pin
    p = C()
    m = L(*h(15, 9), 1.8, *h(16, 19), 1.6) | L(*h(16, 19), 1.6, *h(14 + wv, 28), 0.7)
    p.form(m, HAIR, sd=1, hl=0)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    c.line([h(13, 1), h(24, -5)], 'y1'); c.fill(R(*h(24, -7), *h(25, -6)), 'y2'); c.fill(R(*h(10, 2), *h(12, 3)), 'm2')
    c.blacken()
    return c


HWALK = [dict(), dict(dy=-1, wave=1), dict(dy=-2, wave=2), dict(dy=-1, wave=1)]
HATTACK = [dict(dx=8, dy=-2, wave=2, stream=-3), dict(dx=-14, dy=1, stream=10, bite=True), dict(dx=-4, wave=1, stream=3)]

# ------------------------------------------------------------------ body
BCW, BCH = 96, 92
BOX, BOY = 12, 16          # local baseline y=70
BDEF = dict(lean=0, neck=0, sl=0, hands=0)
HANDS = """
.ccdc..
cdccccb
.cbccbb
..bbb..
"""


def rbody(**kw):
    S = dict(BDEF); S.update(kw)
    setsize(BCW, BCH)
    c = C()
    ln_ = S['lean']

    def B(x, y):
        k = max(0.0, (52 - y) / 30.0)
        return (BOX + x + int(round(ln_ * k)), BOY + y)

    def Q(x, y):
        return (BOX + x, BOY + y)
    # cushion
    p = C()
    p.form(R(*Q(6, 66), *Q(70, 70)) | E(*Q(38, 68), 34, 2.6), RED, sd=1, hl=1)
    c.stamp(p, 'K')
    # obi bow at the back
    p = C()
    bow = PG([B(60, 36), B(69, 34), B(71, 50), B(62, 53)])
    p.form(bow, RED, sd=2, hl=1)
    p.line([B(62, 43), B(70, 42)], 'm0', only=bow)
    c.stamp(p, 'K')
    # folded legs under the kimono
    p = C()
    lap = PG([Q(10, 68), Q(66, 68), Q(67, 56), Q(60, 47), Q(34, 46), Q(16, 55), Q(8, 63)])
    p.form(lap, PUR, sd=4, hl=1)
    for a_, b_ in (((34, 50), (16, 66)), ((44, 52), (36, 67)), ((56, 52), (58, 67))):
        p.line([Q(*a_), Q(*b_)], 'p0', only=lap)
    p.line([Q(9, 67), Q(66, 67)], 'v1', only=lap)                                  # inner layer at the hem
    for (x, y) in ((22, 60), (48, 60), (30, 54)):                                  # small gold crest
        p.pxs([Q(x, y), Q(x + 1, y), Q(x, y + 1), Q(x - 1, y)], 'y1'); p.px(*Q(x, y), 'y2')
    c.stamp(p, 'K')
    # far sleeve
    p = C()
    fs = PG([B(34, 30), B(42, 30), B(40, 48), Q(30 - S['sl'], 60), Q(22 - S['sl'], 56), B(28, 44)])
    p.form(fs, PFAR, sd=2, hl=1)
    c.stamp(p, 'K')
    # torso
    p = C()
    torso = PG([B(37, 23), B(52, 21), B(61, 28), Q(62, 50), Q(34, 50), B(32, 32)])
    p.form(torso, PUR, sd=4, hl=1)
    p.line([B(41, 22), B(39, 30), B(44, 40)], 'v2', only=torso); p.line([B(42, 22), B(40, 30), B(45, 40)], 'v1', only=torso)
    p.line([B(49, 22), B(47, 32), B(45, 40)], 'p0', only=torso)
    obi = PG([Q(33, 40), Q(62, 39), Q(62, 51), Q(34, 51)])
    p.form(obi, RED, sd=3, hl=1)
    p.line([Q(33, 45), Q(62, 44)], 'y1', only=obi); p.line([Q(33, 46), Q(62, 45)], 'y0', only=obi)
    c.stamp(p, 'K')
    # neck stump, stretching upward and bending toward the front
    p = C()
    n = S['neck']
    n0, n1, n2 = B(44, 22), B(43, 12 - n), (B(40, 3 - n)[0] - n, B(40, 3 - n)[1])
    nk = L(*n0, 3.0, *n1, 2.6) | L(*n1, 2.6, *n2, 2.6)
    p.form(nk, SKN, sd=2, hl=1)
    c.stamp(p, 'K')
    # hands folded on the lap, near sleeve
    p = C()
    p.grid(*Q(29, 48 - S['hands']), HANDS, LEG)
    c.stamp(p, 'K')
    p = C()
    ns = PG([B(50, 25), B(61, 29), B(62, 44), Q(60 + S['sl'], 62), Q(48 + S['sl'], 64), Q(36, 53 - S['hands']), Q(36, 48 - S['hands']), B(46, 40)])
    p.form(ns, PUR, sd=3, hl=1)
    p.line([B(52, 30), B(54, 44), Q(52 + S['sl'], 60)], 'p0', only=ns)
    p.line([Q(60 + S['sl'], 61), Q(48 + S['sl'], 63)], 'v1', only=ns)
    p.pxs([Q(52, 50), Q(53, 50), Q(52, 51), Q(51, 50)], 'y1')
    c.stamp(p, 'K')
    c.blacken()
    return c


BWALK = [dict(), dict(lean=-1, neck=1, sl=1), dict(lean=-2, neck=2, sl=1), dict(lean=-1, neck=1)]
BATTACK = [dict(lean=2, neck=-1, hands=1), dict(lean=-3, neck=4, sl=2, hands=2), dict(lean=-1, neck=2, sl=1)]

if __name__ == '__main__':
    export('boss_rokuro_head', rhead, HWALK, HATTACK)
    export('boss_rokuro_body', rbody, BWALK, BATTACK)
