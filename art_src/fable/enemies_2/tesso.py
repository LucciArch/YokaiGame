"""Tesso - the iron rat (vengeful monk Raigo): grey metal quills, red eyes, iron-gnawing incisors, prayer beads."""
from common import *

NAME = 'tesso'
CW, CH = 120, 60
OX, OY = 30, 14           # local baseline y = 40
FUR = ('i1', 'i2', 'i3')
FAR = ('i0', 'i1', 'i2')
TAIL = ('k0', 'k1', 'k2')

LEG = dict(zip('abcdKEZRpkwvq', ['i0', 'i1', 'i2', 'i3', 'K', 'e1', 'y3', 'e0', 'k0', 'k1', 'b3', 'b2', 'q']))
HEAD = """
............bbbb....
..........bbckkcb...
.........bcckkkpb...
.......bbccckkppbb..
.....bccdccccppccbb.
...bccddcccKKKccccb.
..bcddccKKKREKccccbb
.bcdcccccaREZaccccbb
kcccccccccaaacccccbb
kpccccccccccccccccb.
.aaKKKKKcccccccccbb.
.wwvaaaKKbbbcccbbb..
.wwv.....aabbbbb....
.wv.................
"""
JAW = """
.aabbbbba
..wabbba.
...aaaa..
"""

DEF = dict(bob=0, lean=0, head=(0, 0), jaw=0,
           ff=((24, 31), (19, 39)), nf=((29, 32), (26, 39)),        # front legs: elbow, paw
           fh=((44, 33), (41, 39)), nh=((50, 33), (48, 39)),        # hind legs: hock, paw
           tail=((60, 33), (68, 31), (71, 24), (67, 17), (60, 15)), quill=0)


def P(x, y):
    return (x + OX, y + OY)


def tesso(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    # ---- tail: bare, ringed, whipping up behind
    p = C()
    pts = [B((54, 31))] + [P(*q) for q in S['tail']]
    tl = wisp(pts, 2.3, 0.9)
    p.form(tl, TAIL, sd=1, hl=1)
    for i in range(1, len(pts) - 1):
        for t in (0.0, 0.5):
            q = lerp(pts[i], pts[i + 1], t)
            p.fill(R(q[0] - 2, q[1], q[0] + 2, q[1]) if abs(pts[i + 1][1] - pts[i][1]) > abs(pts[i + 1][0] - pts[i][0])
                   else R(q[0], q[1] - 2, q[0], q[1] + 2), 'k0', only=tl)
    c.stamp(p, 'K')

    def paw(p, f):
        p.fill(R(f[0] - 4, f[1] - 1, f[0] + 1, f[1]), 'k1')
        p.fill(R(f[0] - 3, f[1], f[0] + 1, f[1]), 'k0')
        p.pxs([(f[0] - 5, f[1]), (f[0] - 3, f[1] + 0)], 'b3')

    def front(spec, ramp, sh_):
        e_, f_ = P(*spec[0]), P(*spec[1])
        p = C()
        p.form(L(*B(sh_), 3.6, *e_, 2.4), ramp, sd=1, hl=1)
        p.form(L(*e_, 2.2, f_[0], f_[1] - 2, 1.7), ramp, sd=1, hl=0)
        paw(p, f_)
        c.stamp(p, 'i0')

    def hind(spec, ramp, hip):
        k_, f_ = P(*spec[0]), P(*spec[1])
        p = C()
        p.form(E(*B(hip), 7.4, 6.6) | L(*B(hip), 5, *k_, 2.6), ramp, sd=3, hl=1)
        p.form(L(*k_, 2.4, f_[0] + 1, f_[1] - 2, 1.8), ramp, sd=1, hl=0)
        paw(p, f_)
        c.stamp(p, 'i0')

    front(S['ff'], FAR, (27, 27))
    hind(S['fh'], FAR, (44, 27))

    # ---- body: arched back bristling with iron quills
    p = C()
    body = E(*B((41, 24)), 14.4, 9.4) | E(*B((28, 25)), 9.4, 8.2) | L(*B((24, 22)), 6, *B((18, 21)), 5)
    qz = S['quill']
    spikes = np.zeros_like(body)
    for i, (x, y, dx, dy) in enumerate([(24, 16, 3, -6), (29, 14, 4, -7), (35, 13, 5, -8), (41, 13, 6, -7), (47, 15, 7, -6), (52, 19, 8, -3), (55, 24, 8, 0)]):
        b_ = B((x, y)); k = 1 + qz * 0.35
        spikes |= PG([(b_[0] - 3, b_[1] + 3), (b_[0] + dx * k, b_[1] + dy * k), (b_[0] + 4, b_[1] + 4)])
    full = body | spikes
    p.form(full, FUR, sd=4, hl=1)
    core = full & ~sh(full, -2, -2)
    p.a[core & (p.a == I('i1'))] = I('i0')
    # second quill row + steel sheen dashes (clean clusters, no noise)
    for (x, y) in [(31, 19), (37, 18), (43, 19), (49, 22), (34, 24), (41, 25), (47, 27)]:
        b_ = B((x, y))
        p.fill(PG([(b_[0], b_[1] + 2), (b_[0] + 3, b_[1] - 2), (b_[0] + 4, b_[1] + 2)]), 'i1', only=body)
        p.line([(b_[0], b_[1] + 1), (b_[0] + 2, b_[1] - 2)], 'i3', only=body)
    p.fill(R(*B((30, 31)), *B((46, 32))), 'i1', only=body)             # belly in shadow
    c.stamp(p, 'i0')

    hind(S['nh'], FUR, (48, 28))
    front(S['nf'], FUR, (30, 28))

    # ---- head: lower jaw (moves), then the fixed head grid, then juzu beads at the neck
    hx, hy = S['head']
    H0 = B((2 + hx, 14 + hy))
    p = C()
    if S['jaw']:
        p.fill(PG([(H0[0] + 4, H0[1] + 11), (H0[0] + 11, H0[1] + 11), (H0[0] + 11, H0[1] + 12 + S['jaw']), (H0[0] + 5, H0[1] + 12 + S['jaw'])]), 'q')
    p.grid(H0[0] + 3, H0[1] + 12 + S['jaw'], JAW, LEG)
    c.stamp(p, 'K')
    p = C()
    p.grid(H0[0], H0[1], HEAD, LEG)
    c.stamp(p, 'K')
    # whiskers
    c.line([(H0[0] + 3, H0[1] + 9), (H0[0] - 1, H0[1] + 12)], 'i3')
    c.line([(H0[0] + 4, H0[1] + 9), (H0[0] + 1, H0[1] + 14)], 'i3')
    for i, (x, y) in enumerate([(20, 2), (21, 5), (21, 8), (20, 11), (18, 13), (15, 14)]):   # prayer beads
        p = C()
        p.fill(R(H0[0] + x, H0[1] + y, H0[0] + x + 1, H0[1] + y + 1), 'w2' if i % 2 == 0 else 'w1')
        p.px(H0[0] + x, H0[1] + y, 's3')
        c.stamp(p, 'K')

    c.blacken()
    return c


WALK = [
    dict(bob=0, ff=((22, 31), (16, 39)), nf=((31, 32), (30, 39)), fh=((46, 33), (46, 39)), nh=((48, 33), (43, 39)),
         tail=((60, 33), (68, 31), (71, 24), (67, 17), (60, 15))),
    dict(bob=-1, ff=((25, 31), (22, 38)), nf=((29, 32), (25, 39)), fh=((44, 33), (41, 39)), nh=((51, 32), (50, 38)),
         tail=((60, 32), (68, 29), (70, 22), (65, 16), (58, 15))),
    dict(bob=0, ff=((27, 32), (27, 39)), nf=((26, 31), (19, 39)), fh=((43, 33), (38, 39)), nh=((52, 33), (53, 39)),
         tail=((60, 33), (68, 31), (71, 24), (67, 17), (60, 15))),
    dict(bob=-1, ff=((25, 31), (21, 39)), nf=((28, 31), (24, 38)), fh=((45, 32), (43, 38)), nh=((50, 33), (47, 39)),
         tail=((60, 34), (68, 33), (72, 27), (69, 19), (63, 16))),
]
ATTACK = [
    # rears back on its haunches, quills up, jaws opening
    dict(lean=4, bob=-2, head=(1, -3), jaw=2, quill=2, ff=((27, 30), (22, 34)), nf=((32, 32), (28, 37)),
         tail=((61, 34), (70, 35), (76, 31), (78, 24), (75, 18))),
    # charge: whole body shoots forward, jaws wide on the target
    dict(lean=-9, bob=1, head=(-3, 1), jaw=4, quill=1, ff=((11, 31), (4, 37)), nf=((17, 33), (11, 39)),
         fh=((44, 34), (47, 39)), nh=((50, 34), (55, 39)), tail=((52, 32), (61, 30), (69, 31), (76, 28), (81, 23))),
    # bites down
    dict(lean=-5, bob=1, head=(-2, 1), jaw=1, ff=((17, 31), (12, 39)), nf=((23, 32), (19, 39)),
         fh=((44, 33), (44, 39)), nh=((50, 33), (51, 39)), tail=((56, 33), (64, 31), (69, 26), (68, 19), (63, 15))),
]

if __name__ == '__main__':
    export(NAME, tesso, WALK, ATTACK)
    zoom(NAME, 7)
