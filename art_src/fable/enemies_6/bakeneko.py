"""Bakeneko – die alte Hauskatze, die zum Yōkai wurde. Komplett neu (Runde 108): steht auf den Hinterbeinen
wie in den Edo-Holzschnitten, ein Tenugui-Tuch um den Kopf gebunden, gebuckelt mit erhobenen Krallenpfoten.
Katzenanatomie: runder Schädel, kurze Schnauze mit Schnurrhaaren, dreieckige Ohren mit rosa Innenseite,
Halskrause, heller Bauch, Hinterbeine mit Sprunggelenk und langen Pfoten. Getigertes Fell, zwei Schwänze
(schon halb Nekomata), Schlitzpupillen. Begleitet von einem blauen Irrlicht.
Angriff: springt vor und hiebt mit beiden Pfoten."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 100, 88
OX, OY = 16, 2                     # lokale Grundlinie y = 78
col('bk0', '#2a2236'); col('bk1', '#625a6e'); col('bk2', '#a49ca8'); col('bk3', '#dcd4d0'); col('bk4', '#fbf6ec')
add_rim('bk0 bk1 bk2', 'bk4'); DARK.update(bk4='bk3', bk3='bk2', bk2='bk1', bk1='bk0')
FUR = ('bk1', 'bk2', 'bk3')
FURF = ('bk0', 'bk1', 'bk2')
BELLY = ('bk2', 'bk3', 'bk4')


def P(x, y):
    return (x + OX, y + OY)


def stripes(p, m, pts_list, tone=None):
    """Mikeneko-Flecken (orange und schwarz) statt Streifen"""
    for k, pts in enumerate(pts_list):
        x = sum(q[0] for q in pts) / len(pts); y = sum(q[1] for q in pts) / len(pts)
        blob = (E(x, y, 3.4, 2.6) | E(x + 1.5, y + 1.2, 2.4, 2.0)) & m
        if k % 2 == 0:
            p.form(blob, ('t0', 't1', 't2'), sd=1, hl=1)
        else:
            p.form(blob, ('h0', 'h1', 'h2'), sd=1, hl=0)


def draw(bob=0, lean=0, g=0, paw=0, tail=0.0, jump=0, wisp=0):
    setsize(CW, CH)
    c = C()
    sw = [-2, 2][g % 2]

    def B(x, y):
        return P(x + lean, y + bob - jump)

    # ---- zwei Schwänze, s-förmig hochgestellt
    for (k, off, ramp) in ((0, 4, FURF), (1, 0, FUR)):
        p = C()
        pts = [B(44, 52)]
        for i in range(1, 6):
            t = i / 5
            pts.append(B(50 + t * 14 + off * 1.5 + math.sin(t * 4 + tail + k) * 3, 50 - t * 38 + off * 1.5))
        m = None
        for a, b_ in zip(pts, pts[1:]):
            s_ = L(*a, 2.2, *b_, 1.8)
            m = s_ if m is None else m | s_
        m |= E(*pts[-1], 2.0, 2.4)
        p.form(m, ramp, sd=1, hl=1)
        for a in pts[1:-1]:
            p.line([(a[0] - 2, a[1]), (a[0] + 2, a[1] - 1)], 't1' if k else 't0', only=m)
        p.fill(E(*pts[-1], 1.6, 1.8) & m, 'h1')                 # helle Spitze
        c.stamp(p, 'K')
    # ---- fernes Hinterbein
    p = C()
    hip = B(42, 54); kn = P(36 + sw + lean, 64 - jump); hk = P(44 + sw + lean, 70 - jump); ft = P(38 + sw + lean, 78 - jump)
    lg = L(*hip, 6, *kn, 4) | L(*kn, 3.6, *hk, 2.8) | L(*hk, 2.6, *ft, 2.4) | E(ft[0] - 2, ft[1] - 1, 4.4, 2)
    p.form(lg, FURF, sd=1, hl=0)
    c.stamp(p, 'K')
    # ---- ferner Arm (erhoben)
    p = C()
    sh_ = B(32, 36); el = B(26 - paw, 44 - paw); hd = B(18 - paw * 2, 40 - paw * 2)
    p.form(L(*sh_, 3.4, *el, 3.0) | L(*el, 2.8, *hd, 2.6), FURF, sd=1, hl=0)
    p.form(E(*hd, 3.0, 2.6), FURF, sd=1, hl=1)
    for k in range(3):
        p.form(L(hd[0] - 2 + k * 1.6, hd[1] - 2, 0.6, hd[0] - 3 + k * 1.6, hd[1] - 5, 0.3), ('b1', 'b2', 'b3'), sd=0, hl=1)
    c.stamp(p, 'K')
    # ---- Rumpf: gebuckelt, Brust vorn, heller Bauch
    p = C()
    tor = E(*B(36, 42), 10, 12) | E(*B(41, 52), 9, 7.4)
    p.form(tor, FUR, sd=3, hl=1)
    bel = (E(*B(31, 44), 4.6, 9) | E(*B(34, 52), 5, 4)) & tor
    p.form(bel, BELLY, sd=1, hl=1)
    stripes(p, tor & ~bel, [[B(38, 31), B(42, 34), B(41, 38)], [B(42, 38), B(46, 41), B(45, 45)], [B(44, 46), B(48, 49)]])
    c.stamp(p, 'K')
    # ---- nahes Hinterbein: Oberschenkel, Sprunggelenk, lange Pfote
    p = C()
    hip = B(44, 54); kn = P(38 - sw + lean, 64 - jump); hk = P(47 - sw + lean, 70 - jump); ft = P(40 - sw + lean, 78 - jump)
    th = L(*hip, 6, *kn, 3.8) | E(hip[0] + 1, hip[1], 6, 5)
    lw = L(*kn, 4.0, *hk, 3.0) | L(*hk, 2.8, *ft, 2.6)
    p.form(th, FUR, sd=2, hl=1)
    p.form(lw, FUR, sd=1, hl=1)
    pw = E(ft[0] - 3, ft[1] - 1, 5, 2.2)
    p.form(pw, BELLY, sd=1, hl=1)
    for k in range(3):
        p.pxs([(ft[0] - 7 + k * 2, ft[1])], 'bk1')
    stripes(p, th, [[(hip[0] - 4, hip[1] - 4), (hip[0] + 2, hip[1] - 2)], [(hip[0] - 4, hip[1] + 2), (hip[0] + 3, hip[1] + 3)]])
    stripes(p, lw, [[(kn[0] + 2, kn[1] + 2), (kn[0] + 5, kn[1] + 2)]])
    c.stamp(p, 'K')
    # ---- Kopf
    hx, hy = B(21, 21)
    p = C()
    for (ex, far) in ((10, True), (2, False)):                         # Ohren
        ear = PG([(hx + ex - 5, hy - 5), (hx + ex - 1, hy - 17), (hx + ex + 5, hy - 5)])
        p.form(ear, FURF if far else FUR, sd=1, hl=1)
        if not far:
            p.fill(PG([(hx + ex - 2.5, hy - 6), (hx + ex - 1, hy - 13), (hx + ex + 2.5, hy - 6)]), 'p2')
    c.stamp(p, 'K')
    p = C()
    skull = E(hx + 3, hy, 12, 10.4)
    muz = E(hx - 5, hy + 4, 4.4, 3.6)
    cheek = E(hx + 4, hy + 5, 9, 5)
    head = skull | muz | cheek
    p.form(head, FUR, sd=3, hl=1)
    p.form(muz | E(hx - 2, hy + 6, 3.6, 2.4), BELLY, sd=1, hl=1)
    stripes(p, skull, [[(hx + 1, hy - 7), (hx + 2, hy - 3)], [(hx + 5, hy - 7), (hx + 5, hy - 3)], [(hx + 10, hy - 2), (hx + 7, hy)]])
    # Auge: gelb mit Schlitzpupille
    p.fill(E(hx - 2, hy, 2.8, 2.0), 'K')
    p.fill(E(hx - 2, hy, 2.0, 1.3), 'y2')
    p.line([(hx - 2, hy - 1), (hx - 2, hy + 1)], 'K')
    p.pxs([(hx - 3, hy - 1)], 'y3')
    p.fill(E(hx - 10, hy + 3, 1.2, 0.9), 'p2')                            # Nase
    mo = PG([(hx - 10, hy + 6), (hx - 4, hy + 6 + paw * 0.5), (hx + 2, hy + 5), (hx - 2, hy + 8 + paw), (hx - 8, hy + 8 + paw)])
    p.fill(mo, 'q')
    p.fill(L(hx - 8, hy + 6, 0.7, hx - 8, hy + 8, 0.4), 'b3')
    p.fill(L(hx - 2, hy + 6, 0.7, hx - 2, hy + 8, 0.4), 'b3')
    c.stamp(p, 'K')
    p = C()                                                               # Schnurrhaare
    for k in range(3):
        p.line([(hx - 9, hy + 4 + k), (hx - 16, hy + 2 + k * 2.5)], 'bk4')
    c.stamp(p, ring=False)
    # Tenugui um den Kopf, Knoten unter dem Kinn
    p = C()
    cloth = PG([(hx - 5, hy - 6), (hx + 4, hy - 10), (hx + 14, hy - 7), (hx + 14, hy - 1), (hx + 4, hy - 5), (hx - 4, hy - 3)])
    p.form(cloth, ('n1', 'n2', 'n3'), sd=1, hl=1)
    for x in range(-2, 12, 3):
        p.pxs([(hx + x, hy - 5 - (x > 4))], 'v3')
    knot = E(hx + 7, hy + 8, 2.4, 2.0) | tri((hx + 8, hy + 9), 120, 5, 3) | tri((hx + 8, hy + 9), 60, 4, 2.4)
    p.form(knot, ('n1', 'n2', 'n3'), sd=1, hl=1)
    p.line([(hx + 12, hy - 1), (hx + 8, hy + 7)], 'n1')
    c.stamp(p, 'K')
    # Halskrause
    p = C()
    ruff = PG([(hx + 0, hy + 9), (hx + 4, hy + 13), (hx + 9, hy + 11), (hx + 13, hy + 13), (hx + 14, hy + 7), (hx + 4, hy + 6)])
    p.form(ruff, BELLY, sd=1, hl=1)
    c.stamp(p, 'K')
    # ---- naher Arm (erhoben, Krallen ausgefahren)
    p = C()
    sh_ = B(32, 38); el = B(26 - paw, 47 - paw * 0.5); hd = B(14 - paw * 2.5, 42 - paw * 2)
    p.form(L(*sh_, 4, *el, 3.4) | L(*el, 3.2, *hd, 2.8), FUR, sd=1, hl=1)
    p.form(E(*hd, 3.2, 2.8), BELLY, sd=1, hl=1)
    stripes(p, L(*sh_, 4, *el, 3.4), [[(el[0] + 3, el[1] - 3), (el[0] + 5, el[1])]])
    for k in range(4):
        p.form(L(hd[0] - 3 + k * 1.8, hd[1] - 2, 0.6, hd[0] - 4 + k * 1.8, hd[1] - 6, 0.3), ('b1', 'b2', 'b3'), sd=0, hl=1)
    c.stamp(p, 'K')
    # ---- blaues Irrlicht
    if wisp >= 0:
        q = P(4 + math.sin(tail) * 2, 54 + math.cos(tail) * 2)
        flame(c, None, [(q, (q[0] + 1, q[1] - 9), 3.0)], ramp=('a0', 'a1', 'a2'), core='v3', ln='a0', w=3)
    c.blacken()
    return c


WALK = [dict(g=0, tail=0), dict(g=1, bob=-1, tail=1.2), dict(g=0, tail=2.4), dict(g=1, bob=-1, tail=3.6)]
ATTACK = [dict(paw=2, lean=2, bob=1, tail=0.5), dict(paw=5, lean=-5, jump=4, tail=1.5), dict(paw=1, lean=-2, tail=2.5)]

if __name__ == '__main__':
    export('bakeneko', draw, WALK, ATTACK)
