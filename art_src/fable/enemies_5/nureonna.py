"""Nure-onna: Frauenkopf auf einem Schlangenleib, mit nassem, langem Haar. Lauert an Küsten. Blick nach links.
Angriff: richtet sich auf und spuckt Meerwasser."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 90, 70
SC = ('g0', 'g1', 'g2')
BELLY = ('c0', 'c1', 'c2')
SKIN = ('v1', 'v2', 'v3')
HAIR = ('h0', 'hb', 'h2')
FACE = """
KKK...
......
KaK...
......
.......
.qq...
"""
LEG = dict(K='K', a='y2', q='m1')


def draw(wave=0, rise=0, mouth=0):
    setsize(CW, CH)
    c = C()
    by = 62
    # Schlangenleib: Welle am Boden nach rechts, Schwanz läuft spitz aus
    p = C()
    pts = []
    for i in range(40):
        t = i / 39
        x = 30 + t * 52
        y = by - 6 + math.sin(t * 7 + wave) * 4 * (0.4 + t * 0.6)
        pts.append((x, y))
    body = None
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        r = 6.4 * (1 - i / 40) + 1.2
        seg = L(a[0], a[1], r, b[0], b[1], r * 0.97)
        body = seg if body is None else body | seg
    neck = L(30, by - 6, 6.4, 24 - rise * 0.5, by - 26 - rise * 3, 4.4)
    body = body | neck
    p.form(body, SC, sd=3, hl=1)
    p.form(L(29, by - 4, 3.4, 25 - rise * 0.5, by - 24 - rise * 3, 2.4) & body, BELLY, sd=1, hl=0)   # heller Bauch
    for i in range(0, 38, 3):                                   # Schuppenreihe
        x, y = pts[i]
        p.pxs([(int(x), int(y - 2)), (int(x) + 1, int(y - 3))], 'g3')
    c.stamp(p, 'K')
    # Kopf mit langem nassem Haar
    hx, hy = 22 - rise * 0.5, by - 32 - rise * 3
    p = C()
    hair = E(hx + 3, hy - 1, 8.4, 7.4) | L(hx + 4, hy, 5.4, hx + 14, hy + 22, 3.0) | L(hx + 2, hy + 2, 4.4, hx + 8, hy + 18, 2.0)
    p.form(hair, HAIR, sd=2, hl=1)
    for k in range(4):
        p.line([(hx + 4 + k * 2, hy + 2), (hx + 8 + k * 2, hy + 18)], 'h0', only=hair)
    c.stamp(p, 'K')
    p = C()
    face = E(hx - 2, hy + 1, 5.4, 6.4)
    p.form(face, SKIN, sd=2, hl=1)
    c.stamp(p, 'v0')
    p = C()
    p.form((E(hx + 2, hy - 4, 7.4, 3.4) | L(hx - 6, hy - 3, 2.2, hx - 7, hy + 5, 1.6)) & ~E(hx - 3, hy + 3, 4, 4), HAIR, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.grid(int(hx - 7), int(hy - 2), FACE, LEG)
    if mouth:
        p.fill(E(hx - 5, hy + 4, 1.4, 1.2 + mouth * 0.6), 'q')
    c.stamp(p, ring=False)
    # Wassertropfen am Haar
    p = C()
    for (dx, dy) in ((14, 24), (9, 20)):
        p.form(E(hx + dx, hy + dy + (wave % 2), 1.2, 1.8), ('a0', 'a1', 'a2'), sd=0, hl=1)
    c.stamp(p, 'a0')
    c.blacken()
    return c


col('hb', '#1a1738')
WALK = [dict(wave=0), dict(wave=1.5), dict(wave=3.0), dict(wave=4.5)]
ATTACK = [dict(rise=1, wave=1), dict(rise=3, mouth=2, wave=2), dict(rise=1, mouth=1, wave=3)]

if __name__ == '__main__':
    export('nureonna', draw, WALK, ATTACK)
