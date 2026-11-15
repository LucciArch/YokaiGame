"""Komainu: steinerner Löwenhund, Wächter vor Schreinen (hier: Himmelsgefilde). Vierbeiner, Blick nach links,
gelockte Mähne, offenes Maul (a-gyō), rotes Lätzchen, Flammenschweif aus Locken. Angriff: Sprung nach vorn."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 96, 76
ST = ('z0', 'z1', 'z2')
STL = ('z1', 'z2', 'z3')
MANE = ('z0', 'z1', 'z2')
FACE = """
.KKK......
KyYK..KK..
.KKK.KbbK.
......KK..
"""
LEG = dict(K='K', y='y2', Y='y3', b='b3')


def curl(p, x, y, r, ramp, line):
    m = E(x, y, r, r)
    p.form(m, ramp, sd=max(1, int(r / 2.5)), hl=1)
    # Spirale: Bogen nach innen
    import math as _m
    pts = []
    for k in range(9):
        a = _m.radians(200 - k * 40)
        rr = r * (0.8 - k * 0.07)
        pts.append((x + _m.cos(a) * rr, y + _m.sin(a) * rr))
    p.line(pts, line, only=m)
    return m


def draw(bob=0, fl=0, fr=0, bl=0, br=0, lean=0, jaw=0, tail=0):
    setsize(CW, CH)
    c = C()
    by = 68
    hx, hy = 27 + lean, 27 + bob
    # --- Schweif: Fächer aus drei großen Locken
    p = C()
    stem = L(68, 42 + bob, 4, 74 + tail, 30 + bob, 3)
    p.form(stem, MANE, sd=1, hl=1)
    for (x, y, r) in ((74, 20, 6.4), (83, 24, 5.4), (80, 33, 5.4), (70, 26, 4.4)):
        curl(p, x + tail, y + bob, r, STL, 'z0')
    c.stamp(p, 'K')
    # --- ferne Beine
    p = C()
    far = L(36 + fr, 46 + bob, 5, 37 + fr, by - 3, 4.4) | L(62 + br, 48 + bob, 6, 64 + br, by - 3, 4.4)
    p.form(far, ('z0', 'z0', 'z1'), sd=1, hl=0)
    p.form(E(36 + fr, by - 2, 5.4, 2.6) | E(63 + br, by - 2, 5.4, 2.6), ('z0', 'z1', 'z1'), sd=1, hl=0)
    c.stamp(p, 'K')
    # --- Rumpf: kräftige Brust, schmale Hüfte
    p = C()
    body = E(52, 45 + bob, 17, 10.4) | E(38 + lean * 0.5, 42 + bob, 13.4, 14.4)
    p.form(body, ST, sd=4, hl=1)
    p.form(E(63, 43 + bob, 8.4, 8.4) & body, STL, sd=3, hl=1)
    for (x, y) in ((58, 36), (50, 38)):
        p.form(E(x, y + bob, 3.4, 2.4) & body, ('g1', 'g2', 'g3'), sd=1, hl=0)   # Moos
    c.stamp(p, 'K')
    # --- nahe Beine mit Lockenbüscheln
    p = C()
    near = (L(44 + fl, 46 + bob, 7.0, 43 + fl, 58 + bob * 0.5, 5.0) | L(43 + fl, 58 + bob * 0.5, 5.0, 42 + fl, by - 3, 4.4)
            | L(66 + bl, 47 + bob, 8.0, 70 + bl, 57 + bob * 0.5, 5.4) | L(70 + bl, 57 + bob * 0.5, 5.4, 70 + bl, by - 3, 4.4))
    p.form(near, ST, sd=2, hl=1)
    paws = E(41 + fl, by - 2, 7.4, 3.4) | E(70 + bl, by - 2, 7.4, 3.4)
    p.form(paws, STL, sd=1, hl=1)
    for x in (36, 40, 44):
        p.line([(x + fl, by - 4), (x + fl, by - 1)], 'z0', only=paws)
    c.stamp(p, 'K')
    # --- Mähne: dunkle Grundmasse, darüber der Lockenkranz
    p = C()
    base = E(hx + 9, hy + 3, 17, 19)
    p.form(base, ('z0', 'z0', 'z1'), sd=2, hl=0)
    c.stamp(p, 'K')
    p = C()
    for (dx, dy, r) in ((2, -14, 6.4), (12, -10, 6.4), (18, -1, 6.4), (18, 10, 6.4), (11, 17, 6.4),
                        (-4, -12, 5.4), (24, 16, 5.4), (2, 19, 5.4)):
        curl(p, hx + dx, hy + dy, r - 0.6, MANE, 'z0')
    c.stamp(p, 'K')
    # --- rotes Lätzchen mit Glocke
    p = C()
    bib = PG([(hx - 4, hy + 13), (hx + 16, hy + 16), (hx + 4, hy + 29)])
    p.form(bib, ('m0', 'm1', 'm2'), sd=2, hl=1)
    p.form(E(hx + 4, hy + 27, 2.6, 2.6), ('y0', 'y1', 'y2'), sd=1, hl=1)
    c.stamp(p, 'm0')
    # --- Kopf: groß, rund, kurze breite Schnauze, Glubschaugen, offenes Maul
    p = C()
    head = E(hx, hy, 12.4, 11.4) | E(hx - 10, hy + 5, 8.4, 7.4)
    p.form(head, STL, sd=4, hl=1)
    mouth = PG([(hx - 19, hy + 5), (hx - 3, hy + 7), (hx - 17, hy + 12 + jaw)]) & E(hx - 10, hy + 8, 10, 7 + jaw)
    p.fill(mouth, 'q')
    p.fill(E(hx - 12, hy + 10 + jaw * 0.5, 3.4, 1.6) & mouth, 'm2')             # Zunge
    for k in range(4):                                                             # Zahnreihe oben
        p.fill(R(hx - 18 + k * 3, hy + 5, hx - 17 + k * 3, hy + 6), 'b3')
    p.fill(R(hx - 16, hy + 10 + jaw, hx - 15, hy + 11 + jaw), 'b2')                 # Fangzahn unten
    p.form(E(hx - 18, hy + 1, 3.4, 2.4), ('z0', 'z1', 'z1'), sd=1, hl=0)            # Nase
    p.form(E(hx + 6, hy - 11, 3.4, 4.4), ('z0', 'z1', 'z2'), sd=1, hl=1)            # Ohr
    eye = E(hx - 6, hy - 2, 3.0, 2.6)
    p.fill(dil(eye), 'K')
    p.fill(eye, 'y2'); p.fill(E(hx - 7, hy - 2, 1.2, 1.4), 'K'); p.pxs([(hx - 5, hy - 3)], 'y3')
    brow = PG([(hx - 12, hy - 4), (hx - 2, hy - 7), (hx + 1, hy - 5), (hx - 3, hy - 4), (hx - 10, hy - 2)])
    p.form(brow, ('z0', 'z1', 'z2'), sd=1, hl=1)                                    # schwere, schräge Braue
    p.line([(hx - 12, hy - 5), (hx - 3, hy - 8)], 'z3')
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(fl=-4, br=-4, fr=4, bl=4), dict(bob=-1, tail=1), dict(fl=4, br=4, fr=-4, bl=-4), dict(bob=-1, tail=-1)]
ATTACK = [dict(lean=4, bob=2, fl=2, fr=2, jaw=1, tail=2), dict(lean=-3, bob=-4, fl=-7, fr=-5, bl=4, br=4, jaw=3, tail=-3),
          dict(lean=-2, bob=-1, fl=-3, jaw=1)]

if __name__ == '__main__':
    export('komainu', draw, WALK, ATTACK)
