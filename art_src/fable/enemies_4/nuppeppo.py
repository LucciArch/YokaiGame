"""Nuppeppo: ein Klumpen schlaffen, faltigen Fleisches mit verschwommenem Gesicht und Stummelarmen.
Eigene Zeichnung im Serienstil. Angriff: richtet sich auf und lässt sich klatschend fallen."""
from common import *

col('fl0', '#3a1428'); col('fl1', '#7a3a4a'); col('fl2', '#b86a6a'); col('fl3', '#e0a090'); col('xfl', '#f4c8c0')
add_rim('fl0 fl1 fl2', 'xfl')
FL = ('fl1', 'fl2', 'fl3')
FLD = ('fl0', 'fl1', 'fl2')
CW, CH = 100, 100
CX, BASE = 52, 94
FACE = """
.KK......KK.
KqqK....KqqK
KeqK....KqeK
.KK......KK.
............
...KKKKKK...
..KqqqqqqK..
...KKKKKK...
"""
LEGF = dict(K='K', q='q', e='e1')


def draw(sq=0.0, dx=0, rise=0):
    setsize(CW, CH)
    c = C()
    cx = CX + dx
    hw = 25 * (1 + sq * 0.18)
    ht = 34 * (1 - sq * 0.22) + rise
    top = BASE - ht * 2
    # Stummelarm hinten
    p = C(); p.form(L(cx + hw - 6, BASE - ht, 4.2, cx + hw + 4, BASE - ht + 10 - rise * 0.6, 3.4), FLD, sd=2, hl=1); c.stamp(p, 'K')
    # Körper: birnenförmig, unten breit
    p = C()
    body = E(cx, BASE - ht * 0.8, hw, ht * 0.8) | E(cx - 2, BASE - ht * 1.3, hw * 0.72, ht * 0.62)
    body &= (px.Y <= BASE)
    p.form(body, FL, sd=6, hl=2)
    # Hautfalten (hängende Wülste)
    for k, yy in enumerate((0.35, 0.62, 0.9)):
        y = BASE - ht * 2 * (1 - yy) * 0.82
        p.line([(cx - hw * 0.8, y), (cx - hw * 0.3, y + 3), (cx + hw * 0.2, y + 2), (cx + hw * 0.75, y - 1)], 'fl0', only=body)
        p.line([(cx - hw * 0.7, y - 1), (cx - hw * 0.25, y + 2)], 'fl3', only=body)
    # Bauchnabel-Falte und hängende Lappen am Boden
    p.form(E(cx - hw * 0.55, BASE - 4, 7, 4) & body, FLD, sd=1, hl=0)
    p.form(E(cx + hw * 0.5, BASE - 3, 8, 3) & body, FLD, sd=1, hl=0)
    c.stamp(p, 'K')
    # Gesicht (klein, verschwommen, oben)
    p = C(); p.grid(int(cx - 9), int(BASE - ht * 1.6), FACE, LEGF); c.stamp(p, 'K', ring=False)
    # Stummelarm vorn
    p = C(); p.form(L(cx - hw + 7, BASE - ht, 4.6, cx - hw - 4, BASE - ht + 9 - rise * 0.8, 3.6), FL, sd=2, hl=1)
    for d in (-1, 1):
        p.form(L(cx - hw - 4, BASE - ht + 9 - rise * 0.8, 1.6, cx - hw - 8, BASE - ht + 9 + d * 3 - rise * 0.8, 1.2), FL, sd=1, hl=0)
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(sq=0.0), dict(sq=0.35), dict(sq=0.0, dx=-1), dict(sq=-0.2)]
ATTACK = [dict(sq=-0.35, rise=6), dict(sq=0.7, dx=-6), dict(sq=0.25, dx=-3)]

if __name__ == '__main__':
    export('nuppeppo', draw, WALK, ATTACK)
