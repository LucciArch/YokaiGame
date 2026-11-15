"""Shared cat builder for bakeneko (pale ghost cat) and kasha (black fire cat). Poses are joint polylines."""
from common import *

HEAD = """
..K..............K..
.KoK............KnK.
.KonK..........KnnK.
KoopnK.KKKKKK.KnpnmK
KonpnnKnnnnnnKnnpnmK
KonnnnnnnnnnnnnnnnmK
KKKKKnnnnnnnnKKKKKmK
KnKKKKKnnnnKKKKKnnmK
KYYYKYKnnnnKYKYYYnmK
KZYYKYKnnnnKYKYYZnmK
KnYYKYnnppnnYKYYnnmK
mKnnnnnnppnnnnnnnmK.
.KnKKqKKKKKKqKKnnmK.
.mKWqqWqqqqWqqWKmK..
..KqWqqrrrrqqWqKK...
...KqqqrRRrqqqK.....
....KKKKKKKKKK......
"""
for _r in HEAD.strip().split('\n'):
    assert len(_r) == 20, _r


def chain(c, pts, radii, ramp, ln, sd=1, hl=1):
    """limb as stamped segments, drawn tip-first so the upper segment overlaps the lower"""
    n = len(pts) - 1
    for i in range(n - 1, -1, -1):
        p = C()
        p.form(L(pts[i][0], pts[i][1], radii[i], pts[i + 1][0], pts[i + 1][1], radii[i + 1]), ramp, sd=sd if i else sd + 1, hl=hl)
        c.stamp(p, ln)


def paw(c, at, d, ramp, ln, claws=1):
    """paw at point; d = claw direction (deg). claws: 0 none, 1 short, 2 bared long"""
    p = C()
    ctr = pol(at, d, 1.5)
    p.form(E(ctr[0], ctr[1], 3.1, 2.3), ramp, sd=1, hl=1)
    c.stamp(p, ln)
    if claws == 1:
        for da in (-50, -5, 40):
            b = pol(ctr, d + da, 2.9)
            c.px(int(round(b[0])), int(round(b[1])), 'b3')
    if claws == 2:
        for da in (-32, 0, 32):
            b = pol(ctr, d + da, 2.6)
            t = pol(ctr, d + da * 1.2 + (12 if claws == 2 else 0), 2.6 + (4.2 if claws == 2 else 1.5))
            q = C(); q.fill(LN([b, t]), 'b3')
            if claws == 2:
                c.stamp(q, 'K')
            else:
                c.stamp(q, ring=False)


def cat(S, NEAR, FAR, ln, LEG, cell, org, fire=None, bristle=True):
    setsize(*cell)
    c = C()
    ox, oy = org[0] + S['dx'], org[1] + S['dy']

    def B(pt):
        return (ox + pt[0], oy + pt[1])

    if fire:
        fire(c, S, B, 'back')
    # tail
    tp = [B(q) for q in S['tail']]
    p = C()
    tm = np.zeros((px.H, px.W), bool)
    rr = [2.8, 3.6, 3.2, 1.4][:len(tp)]
    for i in range(len(tp) - 1):
        tm |= L(tp[i][0], tp[i][1], rr[i], tp[i + 1][0], tp[i + 1][1], rr[i + 1])
    if bristle:
        for i in range(1, len(tp) - 1):
            for s_ in (-1, 1):
                a = math.degrees(math.atan2(tp[i][1] - tp[i - 1][1], tp[i][0] - tp[i - 1][0]))
                m_ = lerp(tp[i - 1], tp[i], 0.6)
                tm |= L(m_[0], m_[1], 1.6, *pol(m_, a + s_ * 55, 4.6), 0.5)
    p.form(tm, NEAR, sd=2, hl=1)
    c.stamp(p, ln)
    # far legs
    for key in ('fh', 'ff'):
        pts = [B(q) for q in S[key]]
        chain(c, pts, np.linspace(3.2, 2.0, len(pts)), FAR, ln)
        paw(c, pts[-1], S[key + 'd'], FAR, ln, S['claws'])
    # torso
    p = C()
    hq, hump, ch = S['hq'], S['hump'], S['chest']
    torso = E(*B(hq[:2]), hq[2], hq[3]) | E(*B(hump[:2]), hump[2], hump[3]) | E(*B(ch[:2]), ch[2], ch[3])
    torso |= L(*B(hq[:2]), hq[3] - 1.5, *B(ch[:2]), ch[3] - 1.5)
    spikes = np.zeros_like(torso)
    if bristle:
        for k in range(7):
            t = k / 6
            bx = hump[0] - hump[2] * 1.15 + t * hump[2] * 2.6
            by = hump[1] - hump[3] * math.sqrt(max(0.05, 1 - ((bx - hump[0]) / (hump[2] * 1.5)) ** 2)) + 1
            spikes |= L(*B((bx, by + 1)), 1.6, *B((bx + 2.5, by - 3.6)), 0.5)
    p.form(torso | spikes, NEAR, sd=5, hl=1)
    # shoulder + haunch masses
    p.form(E(*B((ch[0] + 1, ch[1] + 1)), ch[2] - 2, ch[3] - 1.6), NEAR, sd=2, hl=0, only=torso)
    if S.get('ribs', True):
        for k in range(4):
            x0 = hump[0] - 6 + k * 5
            y0 = hump[1] - hump[3] + 3
            sm = L(*B((x0, y0)), 1.2, *B((x0 + 2, y0 + 8)), 0.5) & erode(torso, 1)
            darken(p, sm)
    darken(p, torso & ~sh(torso, 0, -3) & ~sh(torso, -2, 0))
    c.stamp(p, ln)
    # near hind leg with haunch
    pts = [B(q) for q in S['nh']]
    chain(c, pts[1:], np.linspace(2.9, 2.1, len(pts) - 1), NEAR, ln)
    p = C()
    p.form(L(pts[0][0], pts[0][1], 6.2, pts[1][0], pts[1][1], 3.6), NEAR, sd=3, hl=1)
    c.stamp(p, ln)
    paw(c, pts[-1], S['nhd'], NEAR, ln, S['claws'])
    # head
    p = C()
    hx, hy = B(S['head'])
    p.grid(int(hx), int(hy), HEAD, LEG)
    c.stamp(p, 'K', ring=False)
    # near front leg
    pts = [B(q) for q in S['nf']]
    chain(c, pts, np.linspace(3.6, 2.2, len(pts)), NEAR, ln)
    paw(c, pts[-1], S['nfd'], NEAR, ln, S['claws'])
    if fire:
        fire(c, S, B, 'front')
    c.blacken()
    return c
