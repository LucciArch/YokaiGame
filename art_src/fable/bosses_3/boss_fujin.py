"""Fūjin - the wind god: green-skinned oni-like kami crouching on a storm cloud,
holding the great wind bag (kaze-bukuro) arched over his head; red hair whipped by his own gale."""
from lib3 import *

NAME = 'boss_fujin'
CW, CH = 262, 184
OX, OY = 112, 44            # local baseline y=130
col('j0', '#0e2a30'); col('j1', '#1d5a4a'); col('j2', '#3a8a5c'); col('j3', '#7cc07a')    # wind-god green skin
px.add_rim('j0 j1 j2', 'xg')
SKIN = ('j1', 'j2', 'j3')
FAR = ('j0', 'j1', 'j2')
BAG = ('v0', 'v1', 'v2')
CLOUD = ('z0', 'z1', 'z2')
HAIR = ('m1', 'm2', 'm3')


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, ph=0.0, k=1.0, gust=0, lean=0, arms=None)


def kami(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, ph, k, lean, gust = S['bob'], S['ph'], S['k'], S['lean'], S['gust']

    def U(x, y):
        return P(x + lean, y + bob)

    fl = math.sin(ph)

    # ---- the wind bag: one fat cloth tube arching over the head, both mouths tied in his fists
    bag_pts = [U(-14, 66), U(-24, 34), U(-10, 4), U(22, -10), U(58, -6), U(86, 12), U(100, 40), U(92, 66)]
    bag_pts = curve(bag_pts, 6)
    n = len(bag_pts)
    bm = np.zeros((px.H, px.W), bool)
    for i in range(n - 1):
        f = i / (n - 1)
        r = (7 + 12 * k * math.sin(math.pi * f) ** 0.6) * (1 + 0.1 * abs(math.sin(f * 11 + ph * 0.5)))   # puffy cloth lumps
        bm |= L(bag_pts[i][0], bag_pts[i][1], r, bag_pts[i + 1][0], bag_pts[i + 1][1], r)
    p = C()
    p.form(bm, BAG, sd=3, hl=2)
    # cloth seams and wrinkles running across the bag
    for f in (0.16, 0.3, 0.46, 0.62, 0.78):
        i = int(f * (n - 1))
        a = bag_pts[max(0, i - 1)]; b = bag_pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        o = bag_pts[i]
        p.line([(o[0] + dy / l * 4, o[1] - dx / l * 4), (o[0] + dx / l * 4 - dy / l * 6, o[1] + dy / l * 4 + dx / l * 6),
                (o[0] - dy / l * 18, o[1] + dx / l * 18)], 'v0', only=bm)   # crease on the shadow side
    # tied cords at both ends
    for o in (U(-14, 62), U(92, 62)):
        p.fill(E(o[0], o[1], 7, 2.4) & bm, 'y1')
        p.fill(E(o[0] - 1, o[1] - 1, 5, 1) & bm, 'y2')
    c.stamp(p, 'K')

    # ---- gust pouring out of the near mouth of the bag (attack)
    if gust:
        for j, (yy, ln, w) in enumerate(((60, 70, 3.2), (70, 84, 4.0), (80, 64, 3.0), (52, 46, 2.4))):
            ln *= gust
            base = U(-18, yy)
            pts = [(base[0] - t_ * ln, base[1] + math.sin(ph * 3 + t_ * 6 + j) * 4 * gust) for t_ in (0, .25, .5, .75, 1)]
            m = tube(curve(pts, 5), w * gust, 0.6)
            m &= R(2, 2, CW - 3, CH - 3)
            q = C(); q.fill(m, 'a2' if j % 2 else 'v2'); c.stamp(q, 'a1')
            # curl at the tip
            tip = pts[-1]
            curl = E(tip[0], tip[1], 6 * gust, 5 * gust) & ~E(tip[0] + 1, tip[1] - 1, 3.6 * gust, 2.8 * gust)
            curl &= R(2, 2, CW - 3, CH - 3)
            q = C(); q.fill(curl, 'v2'); c.stamp(q, 'a1')

    # ---- flowing sash (hire / tennin scarf) behind the body
    sash = [U(52, 54), U(70, 50 + fl * 3), U(92, 58 - fl * 4), U(110, 52 + fl * 5), U(124, 60 - fl * 4)]
    sm = tube(curve(sash, 6), 4.6, 2.0) & R(2, 2, CW - 3, CH - 3)
    p = C(); p.form(sm, ('m0', 'm1', 'm2'), sd=1, hl=1); c.stamp(p, 'K')

    # ---- storm cloud he rides on
    cl = np.zeros((px.H, px.W), bool)
    for (x, y, rx, ry) in ((20, 118, 22, 12), (44, 112, 24, 15), (70, 116, 24, 13), (92, 120, 18, 10),
                           (6, 124, 14, 8), (56, 124, 34, 9)):
        cl |= E(*U(x + fl * (1 if x % 2 else -1), y), rx, ry)
    p = C()
    p.form(cl, CLOUD, sd=3, hl=2)
    for (x, y) in ((20, 114), (44, 106), (70, 112)):          # inner curls
        q = U(x, y)
        p.line([(q[0] - 8, q[1] + 2), (q[0] - 3, q[1] - 2), (q[0] + 3, q[1] - 1), (q[0] + 5, q[1] + 3)], 'z0', only=cl)
    c.stamp(p, 'K')

    # ---- far leg (bent under him, foot on the cloud)
    p = C()
    p.form(L(*U(56, 84), 7, *U(70, 98), 6) | L(*U(70, 98), 6, *U(62, 108), 4.5), FAR, sd=2, hl=1)
    p.form(E(*U(58, 109), 6, 3), FAR, sd=1, hl=1)
    c.stamp(p, 'K')

    # ---- arms reaching up to the bag ends
    fa, na = S['arms'] or (((80, 66), (90, 60)), ((12, 68), (-10, 60)))
    p = C()
    limb(p, U(60, 52), 5.6, U(*fa[0]), 4.8, FAR, sd=2, hl=1)
    limb(p, U(*fa[0]), 4.8, U(*fa[1]), 4.0, FAR, sd=1, hl=1)
    p.form(E(*U(*fa[1]), 5.4, 5), FAR, sd=1, hl=1)
    c.stamp(p, 'K')

    # ---- torso: broad, hunched forward
    p = C()
    torso = L(*U(44, 56), 15, *U(50, 80), 13)
    p.form(torso, SKIN, sd=4, hl=2)
    p.form(E(*U(40, 58), 8, 6) & torso, SKIN, sd=2, hl=1)          # pectoral
    for y in (72, 78):                                          # belly muscles
        p.line([U(38, y), U(46, y + 1)], 'j1', only=torso)
    p.line([U(42, 66), U(43, 86)], 'j1', only=torso)
    c.stamp(p, 'K')
    # tiger-pelt loincloth with black stripes
    p = C()
    loin = PG([U(30, 80), U(64, 78), U(70, 94), U(54, 100), U(40, 96), U(28, 98)])
    p.form(loin, ('t0', 't1', 't2'), sd=2, hl=1)
    for x in (34, 42, 50, 58, 64):
        p.line([U(x, 80), U(x + 2, 86), U(x - 1, 92)], 'K', only=loin)
    belt = L(*U(30, 80), 2.6, *U(64, 78), 2.6)
    p.form(belt, ('m0', 'm1', 'm2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # near leg: thigh forward, knee up, clawed foot gripping cloud
    p = C()
    p.form(L(*U(36, 90), 8, *U(16, 92), 7) | L(*U(16, 92), 7, *U(22, 108), 5.4), SKIN, sd=2, hl=1)
    p.form(E(*U(18, 110), 7, 3.4), SKIN, sd=1, hl=1)
    c.stamp(p, 'K')
    for x in (12, 16, 20):
        c.fill(R(*U(x, 111), *U(x + 1, 113)), 'b2')

    # ---- head: wild red hair streaming back (to the right), small horns, glaring face
    HX, HY = U(30, 34)
    hm = np.zeros((px.H, px.W), bool)
    for i, (a, ln, w) in enumerate(((-40, 30, 6), (-15, 38, 7), (5, 40, 7), (25, 34, 6), (50, 24, 5), (-70, 20, 5))):
        st = (HX + 6, HY - 2)
        tip = pol(st, a + fl * 6 * (1 if i % 2 else -1), ln)
        hm |= tongue(st, tip, w, 4 * (1 if i % 2 else -1) + fl * 2, tr=0.7)
    hm |= E(HX + 4, HY - 4, 15, 13)
    hm &= R(2, 2, CW - 3, CH - 3)
    p = C(); p.form(hm, HAIR, sd=2, hl=1)
    for (a, ln) in ((-15, 30), (5, 32), (25, 26)):
        p.line([(HX + 10, HY - 4), pol((HX + 10, HY - 4), a + fl * 4, ln)], 'm1', only=hm)
    c.stamp(p, 'K')
    # horns
    p = C()
    p.form(tongue((HX - 2, HY - 12), (HX - 8, HY - 22), 2.6, -2, tr=0.5), ('b0', 'b1', 'b2'), sd=1, hl=1)
    p.form(tongue((HX + 8, HY - 13), (HX + 6, HY - 24), 2.4, 2, tr=0.5), ('b0', 'b1', 'b2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # face (faces left): heavy brow, flat nose, wide fanged mouth
    p = C()
    face = E(HX - 2, HY + 2, 13, 14) | E(HX - 11, HY + 7, 7, 6)
    p.form(face, SKIN, sd=3, hl=1)
    c.stamp(p, 'K')
    brow = L(HX - 16, HY - 4, 2.2, HX + 2, HY - 7, 2.6)
    c.fill(brow, 'K')
    c.fill(E(HX - 8, HY + 0, 4, 2.6), 'y2')                     # near eye
    c.fill(R(HX - 9, HY - 1, HX - 8, HY), 'y3')
    c.fill(E(HX + 1, HY - 1, 2.2, 1.8), 'y1')                     # far eye
    c.fill(R(HX - 17, HY + 3, HX - 13, HY + 7), 'j1')             # nose
    mouth = E(HX - 7, HY + 11, 9, 4) & ~R(HX - 20, HY + 6, HX + 10, HY + 7)
    c.fill(mouth, 'q')
    for x in (HX - 13, HX - 2):                                   # fangs
        c.fill(R(x, HY + 7, x + 1, HY + 11), 'b3')
    c.fill(R(HX - 11, HY + 13, HX - 3, HY + 14), 'b2')             # lower teeth
    # ear ring
    c.fill(E(HX + 6, HY + 6, 2.2, 2.2) & ~E(HX + 6, HY + 6, 1, 1), 'y1')

    # ---- near arm raised to the near bag end
    p = C()
    limb(p, U(34, 52), 6.4, U(*na[0]), 5.6, SKIN, sd=2, hl=1)
    limb(p, U(*na[0]), 5.6, U(*na[1]), 4.4, SKIN, sd=1, hl=1)
    p.form(E(*U(*na[1]), 6, 5.6), SKIN, sd=1, hl=1)
    c.stamp(p, 'K')
    h = U(*na[1])
    for dy in (-3, 0, 3):                                         # claws digging into the bag cloth
        c.fill(R(h[0] - 8, h[1] + dy, h[0] - 6, h[1] + dy), 'b2')

    c.blacken()
    return c


T = math.pi / 2
WALK = [dict(ph=0, bob=0), dict(ph=T, bob=-1, k=1.04), dict(ph=2 * T, bob=-2, k=1.08), dict(ph=3 * T, bob=-1, k=1.04)]
ATTACK = [
    dict(ph=1, bob=-3, k=1.18, lean=3, arms=(((84, 58), (92, 56)), ((16, 60), (-8, 54)))),
    dict(ph=2.4, bob=1, k=0.8, lean=-3, gust=1.0, arms=(((80, 70), (90, 64)), ((8, 70), (-12, 64)))),
    dict(ph=4, bob=0, k=0.88, lean=-1, gust=0.55),
]

if __name__ == '__main__':
    export(NAME, kami, WALK, ATTACK)
