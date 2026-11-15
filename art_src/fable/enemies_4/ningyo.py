"""Ningyo: pink fish with a human face and long dark hair. Normal (~56 px long). Attack: spits water jets."""
from common import *

NAME = 'ningyo'
CW, CH = 132, 80
OX, BASE = 78, 70
SC = ('p1', 'p2', 'p3')
FIN = ('m0', 'm1', 'm2')
HAIR = ('h0', 'h1', 'h2')

LEG = dict(zip('KmnokLjJYZWq', ['K', 'h0', 'h1', 'h2', 'k2', 'k3', 'k1', 'k0', 'y2', 'a1', 'v3', 'q']))
HEAD = """
....mmmmmmm....
..mmnnonnnnmm..
.mnnoonnnnnnnm.
.mnmmmmnnnnnnnm
mnmLLLmmmnnnnnm
mmkLLLkkkmnnnnm
mkkkkkkkkkmnnnm
mKKKkkKKKkjmnnm
mkWZKkkWZKjmnnm
mkkkkkkkkkjmnnm
.kLkkkjkkkjmnnm
.kkkkKkkkkjmnnm
.kkkkkkkkjjmnnm
..kkKqqKkjjmnnm
...kkkkkkjJmnm.
....jjjjJmnnm..
"""


def fan(c, o, a0, a1, ln_, ramp, n=5, r0=2.2, ring='m0'):
    """ray fin: n rays between angles a0..a1"""
    p = C()
    m = np.zeros((px.H, px.W), bool)
    tips = []
    for i in range(n):
        a = a0 + (a1 - a0) * i / (n - 1)
        t = pol(o, a, ln_ * (0.82 + 0.18 * ((i % 2) == 0)))
        tips.append(t)
        m |= L(o[0], o[1], r0, t[0], t[1], 1.2)
    m |= PG([o] + [lerp(o, t, 0.8) for t in tips])
    p.form(m, ramp, sd=2, hl=1)
    for t in tips[1:-1]:
        p.line([lerp(o, t, 0.3), t], ramp[0], only=erode(m, 1))
    c.stamp(p, ring)


DEF = dict(dx=0, bob=0, hy=0, hx=0, tail=0, fin=0, hair=0, jet=0, puff=0)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx = OX + S['dx']
    b = S['bob']

    def B(pt):
        return (cx + pt[0], BASE + pt[1] + b)

    hd = B((-16 + S['hx'], -24 + S['hy']))     # head-end centre
    mid = B((4, -15))
    stalk = (cx + 21, BASE - 17 + b - S['tail'])
    tip = (cx + 28, BASE - 28 + b - S['tail'] * 2)
    # tail fin (behind)
    fan(c, tip, 250 - S['tail'] * 4, 350 - S['tail'] * 4, 15, FIN, n=6, r0=2.6)
    # far pectoral fin
    fan(c, B((-8, -10)), 130 + S['fin'], 175 + S['fin'], 10, ('m0', 'm0', 'm1'), n=3)
    # dorsal fin
    p = C()
    df = np.zeros((CH, CW), bool)
    for k in range(6):
        t = k / 5
        bs = lerp(B((-2, -24)), (stalk[0] - 2, stalk[1] - 4), t)
        df |= L(bs[0], bs[1], 2.4, bs[0] + 4, bs[1] - 8 + 3 * t + (k % 2), 0.7)
    p.form(df, FIN, sd=1, hl=1)
    c.stamp(p, 'm0')
    # body
    p = C()
    body = L(hd[0], hd[1], 10.4, mid[0], mid[1], 9.6) | L(mid[0], mid[1], 9.6, stalk[0], stalk[1], 6.2) | L(stalk[0], stalk[1], 6.2, tip[0], tip[1], 4.0)
    p.form(body, SC, sd=4, hl=1)
    darken(p, body & ~sh(body, -2, -2) & ~sh(body, 0, -3))
    inner = erode(body, 1)
    # pale belly
    belly = body & ~sh(body, 0, -4) & (px.X < stalk[0])
    p.fill(belly & inner, 'k3')
    p.fill(belly & ~sh(body, 0, -2) & inner, 'p3')
    # scales: staggered arcs, darker toward the shadow side
    for row in range(-34, 0, 4):
        for k in range(-30, 40, 5):
            x0 = cx + k + (2 if (row // 4) % 2 else 0)
            y0 = BASE + row + b
            arc = (R(x0, y0, x0, y0 + 1) | R(x0 + 1, y0 + 2, x0 + 2, y0 + 2)) & inner & ~belly & (px.X > hd[0] + 4)
            darken(p, arc)
    # glints on the lit back
    p.fill(R(mid[0] - 8, mid[1] - 8, mid[0] - 5, mid[1] - 8) & inner, 'p3')
    p.fill(R(mid[0] + 3, mid[1] - 7, mid[0] + 5, mid[1] - 7) & inner, 'p3')
    c.stamp(p, 'p0')
    # long wet hair streaming back over the body
    p = C()
    hr = np.zeros((CH, CW), bool)
    for (pts, r0) in ([[(-10, -34), (0, -31), (8, -25), (13, -17 + S['hair'])], 2.6],
                      [[(-9, -30), (-4, -24), (-2, -17), (-3, -10 + S['hair'])], 2.4],
                      [[(-12, -36), (0, -37), (9, -34), (16, -31 + S['hair'])], 2.4]):
        q = [B((x + S['hx'], y + S['hy'] if i < 2 else y)) for i, (x, y) in enumerate(pts)]
        for i in range(3):
            hr |= L(q[i][0], q[i][1], r0 - i * 0.6, q[i + 1][0], q[i + 1][1], r0 - (i + 1) * 0.6)
    p.form(hr, HAIR, sd=1, hl=0)
    p.line([B((-6 + S['hx'], -33 + S['hy'])), B((2, -28)), B((8, -20))], 'h2', only=erode(hr, 1))
    c.stamp(p, 'K')
    # near pectoral fin (props the body like an arm)
    fan(c, B((-3, -9)), 95 + S['fin'], 160 + S['fin'], 12, FIN, n=4)
    # face
    p = C()
    fx, fy = int(hd[0]) - 12, int(hd[1]) - 9
    p.grid(fx, fy, HEAD, LEG)
    c.stamp(p, 'K', skip=('h0', 'h1'))
    c.blacken()
    # water jet
    if S['jet']:
        p = C()
        mx, my = fx + 2, fy + 13
        ln_ = S['jet']
        jet = L(mx, my, 1.6, mx - ln_, my - 1, 3.0)
        p.fill(jet, 'a1')
        p.fill(jet & ~sh(jet, 0, 2), 'a2')
        p.fill(jet & ~sh(jet, 0, -1) & ~sh(jet, -2, 0), 'a0')
        p.fill(E(mx - ln_ - 1, my - 1, 4.4, 4.0), 'a1')
        p.fill(E(mx - ln_ - 2, my - 2, 2.6, 2.2), 'a2')
        p.fill(R(mx - ln_ - 3, my - 3, mx - ln_ - 2, my - 3), 'v3')
        for (ox, oy) in [(-ln_ - 7, -6), (-ln_ - 8, 3), (-ln_ + 2, -6), (-ln_ + 4, 5), (-ln_ // 2, -4)]:
            p.fill(R(mx + ox, my + oy, mx + ox + 1, my + oy + 1), 'a2')
        c.stamp(p, 'K')
    if S['puff']:
        p = C()
        mx, my = fx + 1, fy + 13
        p.fill(E(mx - 1, my, 2.4, 2.2), 'a1'); p.px(mx - 2, my - 1, 'a2')
        c.stamp(p, 'K')
    return c


WALK = [
    dict(bob=0, tail=0, fin=0),
    dict(bob=-2, tail=2, fin=18, hair=-1, hy=-1),
    dict(bob=-3, tail=3, fin=30, hair=-2, hy=-1),
    dict(bob=-1, tail=1, fin=12, hair=1),
]
ATTACK = [
    dict(dx=3, hx=2, hy=-3, tail=-2, fin=-10, puff=1),
    dict(dx=-3, hx=-3, hy=1, tail=3, fin=20, jet=30, hair=2),
    dict(dx=-1, hx=-1, tail=1, fin=8, jet=0, puff=1),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
