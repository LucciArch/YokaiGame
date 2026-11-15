"""Tennin: Himmelsmädchen im Federgewand (hagoromo), schwebt ohne Füße, langes Schwebeband hinter sich.
Hier als strenge Wächterin der Himmelsgefilde: weiße Robe, rosa Unterkleid, goldener Kopfschmuck,
Fächer aus Licht. Blick nach links. Angriff: hebt den Fächer, entlädt Lichtfedern."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 96, 98
ROBE = ('v1', 'v2', 'v3')
UNDER = ('p0', 'p1', 'p2')
SKIN = ('k1', 'k2', 'k3')
HAIR = ('h0', 'hb', 'h2')
GOLD = ('y0', 'y1', 'y2')
FACE = """
KKK....
.......
KYK....
.......
.......
.rr....
"""
LEG = dict(K='K', Y='a2', r='m2')


def smooth(pts, n=6):
    P = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    out.append(pts[-1])
    return out


def ribbon(p, pts, w0, w1, ramp):
    pts = smooth(pts)
    m = None
    for (a, b), t0 in zip(zip(pts, pts[1:]), range(len(pts) - 1)):
        f0 = t0 / (len(pts) - 1)
        f1 = (t0 + 1) / (len(pts) - 1)
        seg = L(a[0], a[1], w0 + (w1 - w0) * f0, b[0], b[1], w0 + (w1 - w0) * f1)
        m = seg if m is None else (m | seg)
    p.form(m, ramp, sd=1, hl=1)
    return m


def draw(bob=0, wave=0, arm=0, glow=0):
    setsize(CW, CH)
    c = C()
    cx, cy = 40, 34 + bob
    # --- Schwebeband hinten (große Schleife über Kopf nach rechts unten)
    p = C()
    pts = [(cx + 8, cy + 10), (cx + 6, cy - 14), (cx + 20, cy - 22 + wave), (cx + 34, cy - 12 - wave),
           (cx + 36, cy + 8 + wave), (cx + 30, cy + 26 - wave), (cx + 42, cy + 40 + wave)]
    ribbon(p, pts, 2.2, 1.4, UNDER)
    c.stamp(p, 'p0')
    # --- Robe: weite Glocke, unten in Wolkenfransen auslaufend (keine Füße)
    p = C()
    robe = PG([(cx - 8, cy + 8), (cx + 10, cy + 8), (cx + 20, cy + 36), (cx + 14, cy + 44 + wave * 0.5),
               (cx + 2, cy + 40), (cx - 10, cy + 45 - wave * 0.5), (cx - 18, cy + 36)])
    p.form(robe, ROBE, sd=4, hl=1)
    p.form(PG([(cx - 2, cy + 10), (cx + 6, cy + 10), (cx + 10, cy + 40), (cx - 6, cy + 40)]) & robe, UNDER, sd=2, hl=1)  # rosa Bahn
    for x in (cx - 12, cx + 14):
        p.line([(x, cy + 20), (x + (2 if x > cx else -2), cy + 40)], 'v1', only=robe)                                  # Falten
    p.fill(R(cx - 9, cy + 18, cx + 11, cy + 19) & robe, 'y1')                                                           # Gürtel
    p.fill(R(cx - 9, cy + 20, cx + 11, cy + 20) & robe, 'y0')
    c.stamp(p, 'v0')
    # --- Wolkenfuß
    p = C()
    cloud = E(cx - 10, cy + 46, 7.4, 3.4) | E(cx + 2, cy + 47, 8.4, 3.6) | E(cx + 14, cy + 45, 6.4, 3.0)
    p.form(cloud, ('v1', 'v2', 'v3'), sd=1, hl=1)
    c.stamp(p, 'v1')
    # --- ferner Arm (Ärmel hängt)
    p = C()
    p.form(L(cx + 8, cy + 10, 4, cx + 14, cy + 26, 6), ('v0', 'v1', 'v2'), sd=2, hl=0)
    c.stamp(p, 'v0')
    # --- Kopf
    p = C()
    head = E(cx - 2, cy - 2, 7.4, 8.4)
    p.form(head, SKIN, sd=3, hl=1)
    c.stamp(p, 'k0')
    p = C()
    hair = (E(cx + 2, cy - 7, 8.4, 6.4) | L(cx + 4, cy - 4, 4, cx + 8, cy + 10, 3)) & ~E(cx - 5, cy + 0, 6, 6)
    p.form(hair, HAIR, sd=2, hl=1)
    bun = E(cx + 2, cy - 15, 4.4, 3.4) | E(cx + 9, cy - 13, 3.4, 3.4)
    p.form(bun, HAIR, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    crown = R(cx - 6, cy - 11, cx + 5, cy - 10)
    for x in (cx - 5, cx - 1, cx + 3):
        crown = crown | PG([(x - 1.5, cy - 11), (x + 0.5, cy - 15), (x + 2.5, cy - 11)])
    p.form(crown, GOLD, sd=1, hl=1)
    p.pxs([(cx - 1, cy - 13)], 'm2')
    c.stamp(p, 'y0')
    p = C()
    p.grid(cx - 8, cy - 5, FACE, LEG)
    c.stamp(p, ring=False)
    # --- vorderer Arm mit Lichtfächer
    p = C()
    ax, ay = cx - 8, cy + 12
    hx, hy = cx - 16, cy + 16 - arm * 5
    p.form(L(ax, ay, 4.4, hx + 3, hy + 3, 5.4), ROBE, sd=2, hl=1)          # Ärmel
    p.form(PG([(hx + 1, hy + 2), (hx + 9, hy + 4), (hx + 4, hy + 20 - arm * 3), (hx - 2, hy + 16 - arm * 3)]),
           ('v1', 'v2', 'v3'), sd=2, hl=1)                                    # hängender Kimonoärmel
    p.form(E(hx + 1, hy + 1, 2.4, 2.4), SKIN, sd=1, hl=1)                 # Hand
    c.stamp(p, 'v0')
    p = C()
    fan = None
    for k in range(5):
        a = math.radians(130 + k * 22 - arm * 25)
        tip = (hx + math.cos(a) * (12 + glow), hy + math.sin(a) * (12 + glow))
        seg = L(hx, hy, 1.0, tip[0], tip[1], 2.4)
        fan = seg if fan is None else (fan | seg)
    p.form(fan, ('y1', 'y2', 'y3'), sd=1, hl=1)
    c.stamp(p, 'y0')
    p = C()                                                                 # vorderes Bandende
    ribbon(p, [(hx + 4, hy + 6), (hx - 6, hy + 18 + wave), (hx - 2, hy + 30 - wave), (hx - 10, hy + 40)], 1.8, 1.2, UNDER)
    c.stamp(p, 'p0')
    c.blacken()
    return c


col('hb', '#1a1738')
WALK = [dict(bob=0, wave=0), dict(bob=-1, wave=2), dict(bob=-2, wave=0), dict(bob=-1, wave=-2)]
ATTACK = [dict(bob=-1, arm=1, wave=1), dict(bob=-2, arm=2, glow=3, wave=-2), dict(bob=-1, arm=1, glow=1)]

if __name__ == '__main__':
    export('tennin', draw, WALK, ATTACK)
