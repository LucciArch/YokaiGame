"""Akkorokamui - gigantic red octopus of the Ainu sea."""
from lib3 import *

NAME = 'boss_akkorokamui'
CW, CH = 260, 140
OX, OY = 100, 14            # local baseline y=120
SK = ('r1', 'r2', 'r3')
FAR = ('r0', 'r1', 'r2')

LEG = dict(zip('KabcdyYZq', ['K', 'r0', 'r1', 'r2', 'r3', 'y1', 'y2', 'y3', 'q']))
EYE_N = """
KKKK...........
KaaaKKKK.......
KaaaaaaaKKKK...
.KKaaaaaaaaaKK.
.KyKKKaaaaaaaaK
KyYYYyKKKKaaaaK
KYZZYYYYYyKKKKK
KYZKKKKKKKKYYyK
KyYYYYYYYYYYyyK
.KyYYYYYYYyyyK.
..KKyyyyyyyKK..
....KKKKKKK....
"""
EYE_F = """
KKK.......
KaaKKK....
KaaaaaKKK.
KyKKaaaaaK
KYYyKKKaaK
KZKKKKKYyK
KYYYYYYyyK
.KyYYyyyK.
..KKKKKK..
"""


def P(x, y):
    return (x + OX, y + OY)


# arms: (control points, r0, far?, sucker side, wave amp)
ARMS_FAR = [
    ([(52, 80), (34, 80), (18, 88), (5, 82), (2, 66), (9, 58), (15, 62)], 6.5, 1),
    ([(88, 78), (108, 82), (126, 90), (140, 80), (141, 64), (133, 58), (128, 63)], 6.5, -1),
    ([(60, 86), (46, 98), (34, 111), (20, 116), (11, 112), (13, 106)], 6.5, 1),
    ([(82, 86), (94, 100), (106, 113), (120, 116), (128, 111), (125, 106)], 6.5, -1),
]
ARMS_NEAR = [
    ([(56, 88), (47, 103), (36, 115), (22, 118), (-2, 117), (-10, 110), (-6, 105)], 7.5, 1),
    ([(66, 90), (67, 103), (60, 114), (50, 117), (43, 112), (46, 107)], 7, 1),
    ([(76, 90), (79, 103), (87, 114), (98, 117), (104, 112), (100, 107)], 7, -1),
    ([(86, 88), (98, 98), (112, 111), (128, 117), (140, 115), (143, 108), (138, 105)], 7.5, -1),
]
DEF = dict(bob=0, ph=0.0, slam=None, splash=0, sx=-40)


def tentacle(c, ctrl, r0, ramp, side, r1=1.3):
    pts = curve(ctrl, 8)
    m = tube(pts, r0, r1)
    p = C()
    p.form(m, ramp, sd=2 if r0 < 7 else 3, hl=1)
    off = offset(pts, side * r0 * 0.75, side * r1 * 0.6)
    um = tube(off, r0 * 0.5, r1 * 0.5) & m
    und = ('o0', 'o1') if ramp is FAR else ('o1', 'o2')
    p.fill(um, und[0])
    # suckers: pale 2 px pads along the underside
    acc = 0.0
    for i in range(1, len(off)):
        acc += math.hypot(off[i][0] - off[i - 1][0], off[i][1] - off[i - 1][1])
        if acc >= 4.2:
            acc = 0
            x, y = int(round(off[i][0])), int(round(off[i][1]))
            mm = R(x, y, x + 1, y) & um
            p.fill(mm, und[1])
    c.stamp(p, 'r0')


def eye(c, o, rx, ry, slant):
    """huge glowing eye, horizontal slit pupil, heavy angry lid (inner end lower). slant=-1: inner end on the left"""
    cx, cy = o
    p = C()
    ball = E(cx, cy, rx, ry)
    p.fill(E(cx, cy, rx + 1.6, ry + 1.6), 'r0')
    p.form(ball, ('y0', 'y1', 'y2'), sd=2, hl=0)
    p.fill(E(cx - 1, cy, rx * 0.62, ry * 0.5), 'y2', only=ball)
    pup = L(cx - rx * 0.62, cy + 1, 1.3, cx + rx * 0.55, cy + 1, 1.3) | E(cx, cy + 1, 2.6, 2.3)
    p.fill(pup, 'K', only=ball)
    p.fill(R(cx - rx * 0.55, cy - 2, cx - rx * 0.55 + 1, cy - 1), 'y3', only=ball)
    # lid
    a = (cx - rx - 3, cy - (0.5 if slant < 0 else ry * 0.75))
    b = (cx + rx + 3, cy - (ry * 0.75 if slant < 0 else 0.5))
    lid = PG([a, b, (b[0], cy - ry - 4), (a[0], cy - ry - 4)]) & E(cx, cy, rx + 1.6, ry + 1.6)
    p.fill(lid, 'r1')
    p.fill(lid & ~sh(lid, 0, -2), 'K')
    p.fill(lid & ~sh(lid, 0, 2) , 'r0')
    c.stamp(p, 'K')


def wave(ctrl, ph, amp, k):
    out = [ctrl[0]]
    n = len(ctrl)
    for i in range(1, n):
        a = ph + i * 1.3 + k
        w = amp * i / (n - 1)
        out.append((ctrl[i][0] + math.cos(a) * w, ctrl[i][1] + math.sin(a) * w * 0.7))
    # keep tips from sinking below the ground line
    return [(x, min(y, 118.5)) for x, y in out]


def akk(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, ph = S['bob'], S['ph']

    def B(x, y):
        return P(x, y + bob)

    def arm_pts(ctrl, k, amp=3.0):
        w = wave(ctrl, ph, amp, k)
        w[0] = (ctrl[0][0], ctrl[0][1] + bob)
        return [P(x, y) for x, y in w]

    for i, (ctrl, r0, side) in enumerate(ARMS_FAR):
        tentacle(c, arm_pts(ctrl, i * 1.7), r0, FAR, side)

    # ---- mantle (sagging sac leaning back) + head
    p = C()
    sac = L(*B(85, 39), 30.4, *B(98, 54), 23) | L(*B(80, 50), 24, *B(70, 70), 20)
    headm = E(*B(68, 70), 24.4, 19.4)
    body = sac | headm
    p.form(body, SK, sd=9, hl=2)
    # deep core shadow on the far bottom-right
    core = body & ~sh(body, -5, -5)
    p.fill(core & (p.a == I('r1')), 'r0')
    # brow bulge over the eyes
    brow = E(*B(60, 62), 20, 9)
    p.form(brow, SK, sd=2, hl=1, only=body)
    # crease where the sac folds over the head
    p.line([B(52, 50), B(62, 53), B(76, 60), B(88, 70), B(94, 80)], 'r1', only=body)
    p.line([B(54, 52), B(64, 55), B(76, 62)], 'r0', only=body)
    # warts: lit ones top-left, dark rings in the shade
    for (x, y) in ((70, 20), (80, 26), (66, 32), (92, 18), (76, 38), (100, 30), (88, 44), (62, 42)):
        p.fill(R(*B(x, y), *B(x + 2, y + 1)), 'r3', only=erode(body, 3))
        p.fill(R(*B(x, y + 2), *B(x + 2, y + 2)), 'r1', only=erode(body, 3))
    for (x, y, r) in ((104, 46, 3.4), (96, 58, 2.6), (110, 58, 2.4), (100, 68, 2.2), (86, 54, 2.4)):
        ring = E(*B(x, y), r, r) & ~E(*B(x, y), r - 1.2, r - 1.2)
        p.fill(ring & (p.a == I('r1')), 'r0', only=erode(body, 2))
        p.fill(ring & (p.a == I('r2')), 'r1', only=erode(body, 2))
    p.fill(R(*B(66, 14), *B(72, 14)), 'r4', only=body)
    p.fill(R(*B(62, 17), *B(65, 17)), 'r4', only=body)
    # siphon
    sip = L(*B(90, 74), 4, *B(100, 80), 3)
    p.form(sip, FAR, sd=1, hl=1)
    p.fill(E(*B(101, 81), 2, 2), 'q')
    c.stamp(p, 'r0')
    eye(c, B(69, 69), 10.4, 8.4, -1)
    eye(c, B(47, 69), 6.0, 7.4, 1)
    # frown crease between the eyes
    c.line([B(55, 62), B(56, 66), B(55, 71)], 'r0')
    c.line([B(57, 61), B(58, 65)], 'r1')

    # ---- skirt web between the arm roots
    p = C()
    web = PG([B(48, 82), B(92, 82), B(90, 92), B(78, 95), B(64, 95), B(52, 91)])
    p.form(web, SK, sd=3, hl=0)
    c.stamp(p, 'r0', ring=False)

    near = list(ARMS_NEAR)
    for i, (ctrl, r0, side) in enumerate(near):
        if i == 0 and S['slam'] is not None:
            continue
        tentacle(c, arm_pts(ctrl, 0.9 + i * 2.1), r0, SK, side)
    if S['slam'] is not None:
        ctrl = [(56, 88 + bob)] + list(S['slam'])
        if S['splash']:
            x0 = S['sx']
            k = S['splash']
            p = C()
            sp = np.zeros((px.H, px.W), bool)
            for dx, hgt, wd in ((-20, 22, 5), (-8, 34, 6), (5, 28, 5.4), (17, 18, 4.6), (-32, 12, 4), (30, 10, 3.6)):
                sp |= tongue(P(x0 + dx, 120), P(x0 + dx * 1.5, 120 - hgt * k), wd * 1.7 * k, bend=-dx * 0.15)
            sp &= R(0, 0, 999, OY + 119)
            p.form(sp, ('a0', 'a1', 'a2'), sd=1, hl=1)
            p.fill(erode(sp, 2) & ~sh(erode(sp, 2), 1, 2), 'v3')
            for dx, dy in ((-30, 30), (-14, 44), (12, 38), (28, 24), (-2, 50)):
                q = P(x0 + dx * (0.6 + 0.5 * k), 118 - dy * k)
                p.fill(E(q[0], q[1], 1.6, 1.6), 'a2')
            c.stamp(p, 'K')
        tentacle(c, [P(x, y) for x, y in ctrl], 9, SK, 1, r1=1.6)

    c.blacken()
    return c


T = math.pi / 2
WALK = [dict(ph=0, bob=0), dict(ph=T, bob=1), dict(ph=2 * T, bob=2), dict(ph=3 * T, bob=1)]
ATTACK = [
    dict(ph=0.5, bob=-2, slam=[(44, 80), (28, 54), (26, 26), (40, 8), (56, 10), (58, 20)]),
    dict(ph=2.0, bob=3, slam=[(40, 100), (14, 114), (-22, 117), (-58, 116), (-72, 110), (-68, 104)], splash=1.0),
    dict(ph=3.0, bob=1, slam=[(44, 98), (26, 104), (4, 98), (-14, 84), (-16, 72), (-9, 69)], splash=0.5, sx=-44),
]

if __name__ == '__main__':
    export(NAME, akk, WALK, ATTACK)
