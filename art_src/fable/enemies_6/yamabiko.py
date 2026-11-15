"""Yamabiko – der Bergecho-Geist aus Sekiens Bilderrolle: zotteliges Wesen zwischen Affe und Hund.
Komplett neu (Runde 107): Knöchelgang wie ein Menschenaffe (hohe Schultern, lange Arme, kurze gebeugte Beine,
abfallender Rücken), langes graubraunes Zottelfell, das in Strähnen von Armen, Bauch und Rücken hängt.
Kopf mit kurzer Hundeschnauze, Schlappohren, Brauenwulst, kleinen gelben Augen und weit aufreißbarem Maul.
Angriff: richtet sich auf und brüllt – Schallringe."""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 104, 92
OX, OY = 14, 6                     # lokale Grundlinie y = 72
col('yb0', '#1c1622'); col('yb1', '#40343a'); col('yb2', '#6e5e58'); col('yb3', '#a0907a'); col('yb4', '#c8b898')
add_rim('yb0 yb1 yb2', 'yb4'); DARK.update(yb4='yb3', yb3='yb2', yb2='yb1', yb1='yb0')
FUR = ('yb1', 'yb2', 'yb3')
FURF = ('yb0', 'yb1', 'yb2')
SKN = ('s0', 's1', 's2')


def P(x, y):
    return (x + OX, y + OY)


def shag(p, m, rg, n, ang=90, ln=(3, 6), w=2.6, ramp=FUR, edge_dy=1):
    """hängende Fellsträhnen an der Unterkante einer Maske"""
    ys, xs = np.nonzero(m & ~sh(m, 0, -edge_dy))
    if len(xs) == 0:
        return
    for _ in range(n):
        i = rg.randrange(len(xs))
        o = (xs[i], ys[i] - 1)
        t = tri(o, ang + rg.uniform(-14, 14), rg.uniform(*ln), w)
        p.fill(t, ramp[rg.randrange(2)])


def draw(bob=0, rise=0, g=0, mouth=0, ring=0):
    setsize(CW, CH)
    c = C()
    rg = random.Random(9)
    sw = [-3, 3][g % 2]
    ry = rise

    def B(x, y, k=1.0):
        return P(x + ry * 0.6 * k, y + bob - ry * k)

    # ---- ferner Arm (Knöchel auf dem Boden)
    p = C()
    sh_ = B(34, 34); el = B(26 - sw * 0.5, 48, 0.6); kn = P(22 - sw + ry, 69 - ry * 1.2)
    arm = L(*sh_, 5.0, *el, 4.0) | L(*el, 4.0, *kn, 3.4)
    p.form(arm, FURF, sd=1, hl=0)
    p.form(E(kn[0], kn[1] + 1, 3.6, 2.4), ('s0', 's0', 's1'), sd=0, hl=1)
    c.stamp(p, 'K')
    # ---- fernes Bein
    p = C()
    hip = B(62, 46, 0.3); kn2 = P(54 + sw, 60); an = P(62 + sw, 68); ft = P(56 + sw, 72)
    lg = L(*hip, 6, *kn2, 4) | L(*kn2, 4, *an, 3) | E(ft[0], ft[1] - 1, 5, 2)
    p.form(lg, FURF, sd=1, hl=0)
    c.stamp(p, 'K')
    # ---- Rumpf: hohe Schultern, abfallender Rücken
    p = C()
    tor = E(*B(40, 38), 15, 13) | E(*B(56, 44, 0.4), 12, 10) | L(*B(40, 32), 9, *B(60, 42, 0.4), 7)
    p.form(tor, FUR, sd=4, hl=1)
    for k in range(18):                                              # Fellstriche
        q = B(30 + rg.uniform(0, 34), 30 + rg.uniform(0, 18), 0.7)
        p.line([q, (q[0] + 1, q[1] + 3)], rg.choice(('yb1', 'yb3')), only=erode(tor, 2))
    shag(p, tor, rg, 26, ln=(3, 7))
    shag(p, tor, rg, 10, ang=-60, ln=(2, 5), edge_dy=-1)              # Rückenzotteln nach oben-hinten
    c.stamp(p, 'K')
    # ---- nahes Bein
    p = C()
    hip = B(58, 50, 0.3); kn2 = P(50 - sw, 61); an = P(58 - sw, 68); ft = P(52 - sw, 72)
    lg = L(*hip, 7, *kn2, 4.6) | L(*kn2, 4.4, *an, 3.2)
    p.form(lg, FUR, sd=2, hl=1)
    foot = E(ft[0], ft[1] - 1, 5.4, 2.2)
    p.form(foot, SKN, sd=1, hl=1)
    for k in range(3):
        p.pxs([(ft[0] - 4 + k * 2, ft[1])], 's0')
    shag(p, lg, rg, 8, ln=(2, 5))
    c.stamp(p, 'K')
    # ---- Kopf
    hx, hy = B(20, 26, 1.2)
    p = C()
    ear_f = E(hx + 9, hy + 2, 3.0, 6.0)
    p.form(ear_f, FURF, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    cran = E(hx + 2, hy - 1, 9, 8)
    muz = E(hx - 7, hy + 4, 6, 4.4)
    jaw = PG([(hx - 12, hy + 6 + mouth), (hx - 2, hy + 6), (hx + 4, hy + 8), (hx - 4, hy + 11 + mouth), (hx - 11, hy + 9 + mouth)])
    p.form(jaw, FURF, sd=1, hl=1)
    head = cran | muz
    p.form(head, FUR, sd=3, hl=1)
    p.form(E(hx - 9, hy + 3, 3.6, 2.6) & head, SKN, sd=1, hl=1)       # nackte Schnauzenspitze
    p.fill(E(hx - 12, hy + 2, 1.6, 1.4), 's0')                         # Nase
    p.pxs([(hx - 12, hy + 1)], 's2')
    if mouth:
        mo = PG([(hx - 12, hy + 5.5), (hx - 2, hy + 5.5), (hx - 3, hy + 6 + mouth), (hx - 11, hy + 7 + mouth)])
        p.fill(mo, 'q')
        p.fill(E(hx - 7, hy + 6.5 + mouth, 3, 1) & mo, 'm2')
        p.fill(L(hx - 11, hy + 5.5, 0.8, hx - 11, hy + 8, 0.4), 'b3')
        p.fill(L(hx - 4, hy + 5.5, 0.8, hx - 4, hy + 8, 0.4), 'b3')
    else:
        p.line([(hx - 12, hy + 6), (hx - 2, hy + 6)], 's0')
    brow = L(hx - 6, hy - 3, 2.2, hx + 4, hy - 4, 2.4)
    p.form(brow, FUR, sd=1, hl=1)
    p.fill(E(hx - 3, hy - 0.5, 1.6, 1.2), 'K')                          # Auge
    p.pxs([(hx - 3.5, hy - 0.5)], 'y2')
    shag(p, cran, rg, 10, ln=(2, 4), w=2.2)
    c.stamp(p, 'K')
    p = C()
    ear = E(hx + 6, hy + 3, 3.0, 6.4)                                  # Schlappohr
    p.form(ear, FUR, sd=1, hl=1)
    p.line([(hx + 6, hy - 1), (hx + 5, hy + 7)], 'yb1', only=ear)
    c.stamp(p, 'K')
    # ---- naher Arm, lange Zotteln
    p = C()
    sh_ = B(38, 38); el = B(32 + sw * 0.5, 52, 0.6); kn = P(28 + sw + ry * 0.5, 70 - ry * 1.4)
    arm = L(*sh_, 6.0, *el, 4.6) | L(*el, 4.4, *kn, 3.6)
    p.form(arm, FUR, sd=2, hl=1)
    hand = E(kn[0], kn[1], 4.0, 2.6)
    p.form(hand, SKN, sd=1, hl=1)
    for k in range(3):
        p.pxs([(kn[0] - 3 + k * 2, kn[1] + 1)], 's0')
    shag(p, arm, rg, 12, ang=100, ln=(3, 6))
    c.stamp(p, 'K')
    # ---- Schallringe
    if ring:
        p = C()
        for k in range(ring):
            r = 6 + k * 5
            arc = E(hx - 14, hy + 6, r, r * 1.3) & ~E(hx - 14, hy + 6, r - 1.2, r * 1.3 - 1.2) & \
                (np.indices((px.H, px.W))[1] < hx - 14)
            p.fill(arc, 'v2' if k % 2 == 0 else 'v1')
        c.stamp(p, 'v0')
    c.blacken()
    return c


WALK = [dict(g=0), dict(g=1, bob=-1), dict(g=0, bob=0), dict(g=1, bob=-1)]
ATTACK = [dict(rise=4, mouth=2), dict(rise=6, mouth=4, ring=2), dict(rise=3, mouth=3, ring=3)]

if __name__ == '__main__':
    export('yamabiko', draw, WALK, ATTACK)
