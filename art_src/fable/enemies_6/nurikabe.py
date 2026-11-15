"""Nurikabe – die unsichtbare Wand, die Nachtwanderern den Weg versperrt. Komplett neu (Runde 105):
ein altes Speicherhaus-Mauerstück (Lehm mit weißem Kalkputz) mit Ziegeldach-Kappe, Mauerstärke als Seitenfläche
sichtbar. Abgeplatzter Putz legt Lehm und Bambusgeflecht frei. Das Gesicht entsteht aus dem Mauerwerk: zwei hohle
Augenlöcher mit Glut, ein gezackter Riss als Maul. Stämmige Steinfüße, Lehmarme stemmen sich aus der Wand.
Angriff: kippt nach vorn und schlägt auf."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 96, 100
OX, OY = 18, 8                     # lokale Grundlinie y = 86
col('pl0', '#2e2a3a'); col('pl1', '#6c6470'); col('pl2', '#aaa29c'); col('pl3', '#dcd4c2'); col('pl4', '#f4eedc')
add_rim('pl0 pl1 pl2', 'pl4'); DARK.update(pl4='pl3', pl3='pl2', pl2='pl1', pl1='pl0')
PL = ('pl1', 'pl2', 'pl3')
PLS = ('pl0', 'pl1', 'pl2')
TILE = ('i0', 'i1', 'i2')
MUD = ('s0', 's1', 's2')


def draw(bob=0, lean=0.0, ll=0, rl=0, arm=0, mouth=0, glow=0, dust=0):
    setsize(CW, CH)
    c = C()

    def B(x, y):                                     # Scherung beim Kippen um den Fußpunkt
        return (x + OX + lean * (78 - y) / 60, y + OY + bob)

    # ---- Steinfüße
    for (fx, lift, ramp) in ((44 + rl, 0, ('z0', 'z0', 'z1')), (16 + ll, 0, ('z1', 'z2', 'z3'))):
        p = C()
        foot = E(*B(fx, 82 - lift), 7.4, 4.4) | R(*B(fx - 5, 76 - lift), *B(fx + 5, 82 - lift))
        p.form(foot, ramp, sd=2, hl=1)
        for k in range(3):
            p.line([B(fx - 5 + k * 3.4, 84), B(fx - 5 + k * 3.4, 86)], ramp[0], only=foot)
        c.stamp(p, 'K')
    # ---- Seitenfläche (Mauerstärke) rechts, leicht nach hinten versetzt
    p = C()
    side = PG([B(54, 14), B(62, 9), B(62, 72), B(54, 78)])
    p.form(side, PLS, sd=2, hl=0)
    for y in range(20, 72, 9):
        p.line([B(54, y + 2), B(62, y - 3)], 'pl0', only=side)
    c.stamp(p, 'K')
    # ---- Vorderfläche: Steinsockel unten, darüber Kalkputz
    p = C()
    front = R(*B(8, 14), *B(54, 78))
    p.form(front, PL, sd=3, hl=2)
    base = R(*B(8, 66), *B(54, 78)) & front
    p.form(base, ('z1', 'z2', 'z3'), sd=1, hl=1)
    for row, y in enumerate((66, 72)):                                  # Bruchsteine im Sockel
        for x in range(8 + (row % 2) * 5, 54, 10):
            p.line([B(x, y), B(x, y + 6)], 'z0', only=base)
        p.line([B(8, y), B(54, y)], 'z0', only=base)
    # abgeplatzter Putz: Lehm + Bambusgeflecht
    for (cx, cy, rx, ry) in ((47, 24, 6, 7), (13, 54, 5, 6), (40, 58, 4, 3.4)):
        rg = __import__('random').Random(int(cx * 7 + cy))
        pts = []
        for k in range(10):
            a = k / 10 * 2 * math.pi
            f = rg.uniform(0.6, 1.15)
            pts.append(B(cx + math.cos(a) * rx * f, cy + math.sin(a) * ry * f))
        hole = PG(pts) & front & ~base
        p.form(hole, MUD, sd=1, hl=0)
        for k in range(-2, 3):
            p.line([B(cx - rx, cy + k * 2.4), B(cx + rx, cy + k * 2.4)], 'o0', only=erode(hole, 1))
        p.line([B(cx - 1, cy - ry), B(cx - 1, cy + ry)], 'o1', only=erode(hole, 1))
        p.line([B(cx - rx, cy - ry), B(cx - rx + 3, cy - ry + 1)], 'pl4', only=sh(hole, 1, 1) & ~hole)
    for x in range(11, 54, 6):                                           # Putzstriche
        p.line([B(x, 22), B(x, 30)], 'pl2', only=front & ~base)
    # Risse
    for pts in (((20, 14), (22, 20), (19, 26)), ((50, 40), (46, 46), (48, 52), (44, 60)), ((10, 30), (14, 34))):
        p.line([B(*q) for q in pts], 'pl0', only=front & ~base)
    # Wasserflecken unter dem Dach
    p.fill((E(*B(26, 18), 10, 2.4) | E(*B(16, 20), 3, 3.4)) & front, 'pl2')
    c.stamp(p, 'K')
    # ---- Gesicht: hohle Augen + Rissmaul
    p = C()
    for (ex, ey) in ((20, 34), (38, 33)):
        eye = E(*B(ex, ey), 4.2, 3.4) | E(*B(ex, ey + 2), 3.0, 2.0)
        p.fill(eye, 'K')
        p.fill(E(*B(ex - 0.6, ey + 0.6), 1.8 + glow * 0.4, 1.2 + glow * 0.3), 'y1')
        p.pxs([B(ex - 1, ey)], 'y3')
        p.line([B(ex - 5, ey - 4), B(ex + 4, ey - 6 + (ex > 30) * 2)], 'pl0')          # Braue aus Rissen
    mo = PG([B(14, 47), B(19, 45), B(23, 48), B(28, 45), B(33, 48), B(38, 45), B(44, 47), B(40, 51 + mouth),
             B(33, 52 + mouth), B(26, 54 + mouth), B(19, 52 + mouth)])
    p.fill(mo, 'K')
    p.fill(erode(mo, 1), 'q')
    for (tx, ty) in ((19, 46), (28, 46), (37, 46)):                     # Putzbrocken als Zähne
        p.fill(PG([B(tx - 1.6, ty), B(tx + 1.6, ty), B(tx, ty + 3)]) & mo, 'pl3')
    for (tx, ty) in ((23, 52 + mouth), (33, 51 + mouth)):
        p.fill(PG([B(tx - 1.4, ty), B(tx + 1.4, ty), B(tx, ty - 2.6)]) & mo, 'pl2')
    c.stamp(p, 'K')
    # ---- Ziegeldach-Kappe: Firstziegel + Rundziegel-Reihe mit Überstand
    p = C()
    cap = PG([B(4, 15), B(56, 15), B(65, 9), B(64, 5), B(12, 5)])
    p.form(cap, TILE, sd=2, hl=1)
    for x in range(8, 58, 5):                                          # Rundziegel-Stirnseiten
        p.form(E(*B(x, 15), 2.6, 2.2), ('i1', 'i2', 'i3'), sd=1, hl=1)
        p.pxs([B(x, 15)], 'i0')
    ridge = L(*B(12, 4), 2.6, *B(63, 3), 2.6)
    p.form(ridge, ('i0', 'i1', 'i2'), sd=1, hl=1)
    p.fill(E(*B(60, 2), 3, 3) & ~ridge, 'i2')                          # Onigawara-Ende
    for (mx, my) in ((22, 6), (40, 7)):                                # Moos auf dem Dach
        p.form(E(*B(mx, my), 4, 1.6), ('g0', 'g1', 'g2'), sd=0, hl=1)
    c.stamp(p, 'K')
    # ---- Lehmarme, die sich aus der Wand stemmen
    for (sx, sy, dx, dy, ramp) in ((54, 50, 8 + arm * 0.5, 10 - arm, ('z0', 'z1', 'z2')), (8, 52, -9 - arm, 6 - arm * 2, ('z1', 'z2', 'z3'))):
        p = C()
        a_ = L(*B(sx, sy), 4.6, *B(sx + dx, sy + dy), 3.6)
        p.form(a_, ramp, sd=1, hl=1)
        hx, hy = B(sx + dx, sy + dy)
        for k in range(3):
            p.form(E(hx - 2 + k * 2.2 * (1 if dx > 0 else -1), hy + 3, 1.4, 2.2), ramp, sd=0, hl=1)
        p.line([lerp(B(sx, sy), (hx, hy), 0.4), lerp(B(sx, sy), (hx, hy), 0.45)], ramp[0], only=a_)
        p.line([B(sx, sy - 3), B(sx, sy + 3)], 'pl0')                  # Ausbruchkante im Putz
        c.stamp(p, 'K')
    # ---- Staub beim Aufschlag
    if dust:
        p = C()
        for (dx, r) in ((-6, 3.4), (0, 4.4), (8, 3.0), (60, 3.6), (66, 2.6)):
            p.form(E(OX + dx, OY + 84, r, r * 0.7), ('z1', 'z2', 'z3'), sd=1, hl=1)
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(ll=-2, rl=2, arm=0), dict(bob=-1, ll=0, rl=0, arm=1), dict(ll=2, rl=-2, arm=0), dict(bob=-1, arm=-1)]
ATTACK = [dict(lean=4, bob=-1, arm=3, glow=1), dict(lean=-9, mouth=2, glow=1, dust=1, arm=-2), dict(lean=-4, mouth=1)]

if __name__ == '__main__':
    export('nurikabe', draw, WALK, ATTACK)
