"""Omukade, giant centipede of Mount Mikami: head (boss_omukade_head) + chainable body segment (boss_omukade_seg).
Chaining: head neck joint = cell (HJ) ; segment joints = cell (SJ_L) and (SJ_R); spacing 26 px, draw head last (on top)."""
from bl import *

ARM = ('r0', 'r1', 'r2')
GOLD = ('y0', 'y1', 'y2')
GFAR = ('s1', 'y0', 'y1')

# ------------------------------------------------------------------ head
HCW, HCH = 140, 104
HOX, HOY = 34, 20           # local head centre ~ (62, 44); lowest rest point local y=74
HJ = (HOX + 84, HOY + 46)   # neck joint (cell coords) where the first segment attaches

ELEG = dict(zip('KyYZar', ['K', 'y1', 'y2', 'y3', 'r0', 'e1']))
EYES = """
KKK..........
aKKKKK.......
.ayYKKKKK....
.KYZZYyKKKKK.
.KyYZZYKaaKKK
..KyYYKa.yYKK
...KKKa.yZZYK
.........YYK.
"""


def mandible(c, base, a0, bend, ramp, r0=4.6, seg=(10, 9, 8), tipcol='K'):
    p = C()
    pts = [base]; a = a0; rs = [r0, r0 * 0.72, r0 * 0.45, 0.5]
    for i, l_ in enumerate(seg):
        pts.append(pol(pts[-1], a, l_)); a += bend
    m = np.zeros((px.H, px.W), bool)
    for i in range(3):
        m |= L(*pts[i], rs[i], *pts[i + 1], rs[i + 1])
    p.form(m, ramp, sd=2, hl=1)
    p.fill(L(*lerp(pts[2], pts[3], 0.35), 1.2, *pts[3], 0.6) & m, tipcol)          # dark venom tip
    # serration on the inner edge
    for t in (0.3, 0.75):
        q = lerp(pts[1], pts[2], t)
        s_ = 1 if bend > 0 else -1
        e = pol(q, a0 + bend + 90 * s_, rs[1] + 1.5)
        p.fill(L(q[0], q[1], 1.2, e[0], e[1], 0.5), ramp[2])
    c.stamp(p, 'K')
    return pts[3]


def antenna(c, base, a0, bend, n=7, ln=5.2):
    p = C()
    pt = base; a = a0
    for i in range(n):
        nx = pol(pt, a, ln)
        r = 1.9 - i * 0.18
        p.form(L(*pt, r, *nx, max(r - 0.2, 0.7)), ('r0', 'r1', 'r2') if i % 2 == 0 else GFAR, sd=1, hl=0)
        pt = nx; a += bend
    c.stamp(p, 'K')


HDEF = dict(dx=0, dy=0, mopen=0, ant=0, glow=False)


def head(**kw):
    S = dict(HDEF); S.update(kw)
    setsize(HCW, HCH)
    c = C()
    ox, oy = HOX + S['dx'], HOY + S['dy']

    def h(x, y):
        return (ox + x, oy + y)
    mo = S['mopen']
    # antennae (far first)
    antenna(c, h(52, 30), 228 + S["ant"], 15, ln=4.8)
    # collar plate (first tergite) + neck
    p = C()
    neck = E(*h(84, 46), 10, 11.4)
    p.form(neck, ARM, sd=4, hl=1)
    c.stamp(p, 'K')
    p = C()
    collar = E(*h(74, 44), 12.4, 15.4)
    p.form(collar, ARM, sd=4, hl=1)
    p.line([h(80, 31), h(84, 40), h(84, 50), h(80, 58)], 'y0', only=collar)
    p.line([h(79, 31), h(83, 40), h(83, 50), h(79, 58)], 'y1', only=collar)
    c.stamp(p, 'K')
    # small forelegs under the collar
    for (b, k, t, rp) in ((h(78, 56), h(72, 64), h(66, 73), GFAR), (h(72, 57), h(64, 63), h(57, 73), GOLD)):
        p = C()
        p.form(L(*b, 2.6, *k, 2.0), rp, sd=1, hl=1)
        p.form(L(*k, 1.9, *t, 0.8), rp, sd=1, hl=0)
        c.stamp(p, 'K')
    # far mandible (upper)
    mandible(c, h(45, 40), 212 + mo, -36, ('s1', 'y0', 'y1'), r0=4.4, seg=(13, 12, 11))
    # under-jaw (coxosternite) and mouth
    p = C()
    jaw = E(*h(52, 52), 12, 6.4)
    p.form(jaw, ('r0', 'r0', 'r1'), sd=2, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.fill(PG([h(40, 47), h(52, 46), h(52, 51), h(42, 51)]), 'q')
    for x in (42, 45, 48):
        p.pxs([h(x, 47), h(x, 48)], 'b2')
    c.stamp(p, 'K')
    # head shield
    p = C()
    shield = E(*h(58, 38), 18.4, 13.4) | PG([h(42, 32), h(38, 42), h(44, 48), h(54, 44)])
    p.form(shield, ARM, sd=5, hl=1)
    p.form(E(*h(60, 33), 13, 7.4), ARM, sd=2, hl=1, only=shield)                  # raised crown plate
    p.line([h(45, 34), h(52, 28), h(62, 26)], 'r3', only=shield)
    p.fill(R(*h(54, 29), *h(58, 29)), 'r4', only=shield)
    p.line([h(70, 28), h(73, 36), h(72, 46)], 'r0', only=shield)
    p.line([h(48, 45), h(58, 49), h(68, 48)], 'r0', only=shield)
    for (x, y) in ((63, 43), (67, 39), (59, 45)):                                   # pits
        p.pxs([h(x, y), h(x + 1, y)], 'r0')
    # horn-like spines on the rear rim
    c.stamp(p, 'K')
    p = C()
    for (x, y, a_, l_) in ((66, 26, 300, 8), (72, 29, 320, 7)):
        p.form(tri(h(x, y), a_, l_, 5), ARM, sd=1, hl=1)
    c.stamp(p, 'K')
    # eyes (grid, identical every frame)
    p = C()
    p.grid(ox + 41, oy + 33, EYES, ELEG)
    c.stamp(p, ring=False)
    if S['glow']:
        c.pxs([h(40, 36), h(39, 36), h(38, 35)], 'y2')
    # near antenna, near mandible (lower)
    antenna(c, h(48, 32), 205 + S["ant"], 15, n=8, ln=4.8)
    mandible(c, h(45, 50), 146 - mo, 38, GOLD, r0=5.2, seg=(15, 13, 12))
    c.blacken()
    return c


HWALK = [dict(), dict(dy=-1, mopen=4, ant=4), dict(dy=0, mopen=8, ant=7), dict(dy=1, mopen=4, ant=3)]
HATTACK = [dict(dx=5, dy=-1, mopen=30, ant=-12, glow=True), dict(dx=-12, dy=1, mopen=-20, ant=16), dict(dx=-4, mopen=6, ant=6)]

# ------------------------------------------------------------------ segment
SCW, SCH = 60, 60
SOX, SOY = 4, 6             # plate centre local (26, 22); leg tips on local y=48
SJ_L = (SOX + 13, SOY + 22); SJ_R = (SOX + 39, SOY + 22)
SDEF = dict(n=0, f=0, bob=0)


def sleg(c, hip, swing, lift, rp, far=False):
    """jointed walking leg: hip -> knee (out/up) -> ankle -> claw tip on the ground"""
    tipx = hip[0] - 5 + swing
    tip = (tipx, SOY + 48 - lift)
    knee = (hip[0] - 6 + swing * 0.4, hip[1] + (3 if not far else 1) - lift * 0.5)
    ank = (lerp(knee, tip, 0.6)[0] - 2, lerp(knee, tip, 0.6)[1])
    p = C()
    p.form(L(*hip, 2.8, *knee, 2.2), rp, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.form(L(*knee, 2.2, *ank, 1.6), rp, sd=1, hl=1)
    p.form(L(*ank, 1.5, *tip, 0.7), rp, sd=1, hl=0)
    c.stamp(p, 'K')
    c.pxs([(int(tip[0]), int(tip[1])), (int(tip[0]) - 1, int(tip[1]))], 'K')


def seg(**kw):
    S = dict(SDEF); S.update(kw)
    setsize(SCW, SCH)
    c = C()
    b = S['bob']

    def s(x, y):
        return (SOX + x, SOY + y + b)
    # far leg
    sleg(c, s(30, 24), S['f'], max(0, -S['f']) * 0.5 if S.get('flift') is None else S.get('flift', 0), GFAR, far=True)
    # under-body
    p = C()
    p.form(E(*s(26, 27), 14, 7.4), ('r0', 'r0', 'r1'), sd=2, hl=0)
    c.stamp(p, 'K')
    # near leg
    sleg(c, s(24, 30), S['n'], S.get('nlift', 0), GOLD)
    # tergite plate
    p = C()
    plate = E(*s(26, 21), 16.4, 11.4) & (px.Y < s(0, 30)[1])
    p.form(plate, ARM, sd=4, hl=1)
    front = plate & ~sh(plate, 4, 0)
    p.line([s(12, 15), s(18, 12), s(28, 11)], 'r3', only=plate)
    p.fill(R(*s(19, 13), *s(23, 13)), 'r4', only=plate)
    p.line([s(36, 12), s(39, 20), s(38, 28)], 'r0', only=plate)
    p.line([s(11, 28), s(26, 29), s(41, 27)], 'y0', only=plate)                    # gold trim on the lower rim
    p.line([s(11, 27), s(26, 28), s(41, 26)], 'y1', only=plate)
    for (x, y) in ((24, 22), (30, 19), (19, 20)):
        p.pxs([s(x, y), s(x + 1, y)], 'r0')
    c.stamp(p, 'K')
    # dorsal spine
    p = C()
    p.form(tri(s(30, 11), 300, 7, 5), ARM, sd=1, hl=1)
    c.stamp(p, 'K')
    c.blacken()
    return c


SWALK = [dict(n=-5, f=5), dict(n=0, f=0, nlift=4, bob=-1), dict(n=6, f=-5), dict(n=0, f=0, flift=4, bob=-1)]
SATTACK = SWALK[:3]

if __name__ == '__main__':
    export('boss_omukade_head', head, HWALK, HATTACK)
    export('boss_omukade_seg', seg, SWALK, SATTACK)
    # chain demo for review
    setsize(HCW, HCH)
    hd = head().img(); sg = [seg(**SWALK[i % 4]).img() for i in range(4)]
    im = Image.new('RGBA', (260, 100), FLOOR)
    for i in range(5, -1, -1):
        im.alpha_composite(sg[i % 4], (HJ[0] - SJ_L[0] + 8 + i * 26, HJ[1] - SJ_L[1] + 2 + (i % 2)))
    im.alpha_composite(hd, (0, 0))
    im.resize((260 * 4, 400), Image.NEAREST).save('/tmp/rev/omukade_chain.png')
