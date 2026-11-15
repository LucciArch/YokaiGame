"""Ittan-momen: a long strip of white cotton that flies at night, two slanted eyes, wraps its prey."""
from kit import *
import px

NAME = 'ittan_momen'
CW, CH = 164, 84
OX, OY = 60, 14

LEG = dict(zip('KRZv', ['K', 'e1', 'y3', 'v1']))
FACE = """
KKK.....KKK....
KKKKK...KKKKK..
.KKKKKK..KKKKKK
.KRRZKK..KRRZKK
..KRRK....KRRK.
...KK......KK..
...............
....K.K.K.K....
....KKKKKKK....
.....K.K.K.....
"""

A0, A1, M0, M1 = 172.0, 74.0, 16.0, 12.0
DEF = dict(head=(14, 6), body=[(15, 20), (24, 31), (37, 28), (47, 19), (59, 20), (68, 29), (80, 30), (88, 22), (84, 14)],
           arm1=[(-6, 3), (-10, 8)], arm2=[(-5, 5), (-7, 11)], tw=0.22)


def P(x, y):
    return (x + OX, y + OY)


def ribbon(c, pts, dv0, dv1, tw):
    sp = spline(pts, 8)
    N = len(sp) - 1
    dvs = []
    for i in range(N + 1):
        t = i / N
        k = min(1.0, t / tw)
        k = k * k * (3 - 2 * k)
        w = 1.0 if t < 0.85 else 1.0 - (t - 0.85) * 3.5
        an = math.radians(A0 + (A1 - A0) * k)
        mg = (M0 + (M1 - M0) * k) * w
        dvs.append((math.cos(an) * mg, math.sin(an) * mg))
    quads = []
    for i in range(N):
        a, b = sp[i], sp[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        dv = dvs[i]
        cr = dx * dv[1] - dy * dv[0]
        lit = -dy / ln * abs(dv[1]) / (math.hypot(*dv) or 1)
        side = cr >= 0
        if side and i < N * tw * 0.75:
            tone = 'v2'
        elif side:
            tone = 'v3' if lit > 0.28 else ('v1' if lit < -0.3 else 'v2')
        else:
            tone = 'v1' if lit > 0 else 'v0'
        q = PG([a, b, (b[0] + dvs[i + 1][0], b[1] + dvs[i + 1][1]), (a[0] + dv[0], a[1] + dv[1])])
        quads.append((side, tone, q))
    # tail -> head, one part per run of same-facing quads
    i = N - 1
    while i >= 0:
        j = i
        p = C()
        while j >= 0 and quads[j][0] == quads[i][0]:
            p.fill(quads[j][2], quads[j][1])
            j -= 1
        m = p.m
        if quads[i][0]:
            # thickness: darker selvedge on the near (lower) edge
            edge = m & ~sh(m, 0, -1) & (p.a == I('v2'))
            p.a[edge] = I('v1')
        c.stamp(p, 'K')
        i = j
    return sp


def momen(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    hx, hy = S['head']
    pts = [P(hx, hy)] + [P(*q) for q in S['body']]
    ribbon(c, pts, None, None, S['tw'])
    # face
    p = C()
    p.grid(*P(hx - 15, hy + 4), FACE, LEG)
    c.stamp(p, ring=False)
    c.blacken()
    return c


def wave(ph, amp=3.0):
    b = DEF['body']
    out = [b[0]]
    for i, (x, y) in enumerate(b[1:], 1):
        out.append((x, y + amp * math.sin(i * 1.25 + ph) * min(1.0, i / 3)))
    return out


WALK = [
    dict(body=wave(0.0)),
    dict(body=wave(1.57), head=(14, 5), arm1=[(-6, 3), (-10, 7)]),
    dict(body=wave(3.14), head=(14, 6)),
    dict(body=wave(4.71), head=(14, 7), arm1=[(-5, 5), (-8, 10)]),
]
ATTACK = [
    # coil back
    dict(head=(32, 2), body=[(33, 16), (41, 27), (52, 23), (57, 12), (66, 12), (71, 24), (80, 28), (87, 20), (83, 12)],
         arm1=[(-3, 6), (-2, 12)], arm2=[(-1, 6), (2, 11)]),
    # lash: head shoots forward, body snaps into a wrapping loop
    dict(head=(-22, 16), body=[(-21, 31), (-9, 38), (4, 27), (-3, 13), (-15, 22), (-2, 37), (16, 35), (34, 27), (52, 31), (72, 25), (86, 30)],
         arm1=[(-7, 1), (-13, 0)], arm2=[(-5, 5), (-11, 8)], tw=0.12),
    dict(head=(4, 8), body=[(5, 22), (13, 33), (26, 31), (36, 23), (48, 26), (58, 34), (70, 31), (80, 24), (78, 16)],
         arm1=[(-6, 3), (-10, 6)]),
]

if __name__ == '__main__':
    export(NAME, momen, WALK, ATTACK)
