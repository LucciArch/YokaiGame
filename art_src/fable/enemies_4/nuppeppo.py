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
.ddddd....ddddd.
dKKKKKd..dKKKKKd
.KeeqK....KqeeK.
..KKK......KKK..
................
.......dd.......
......dKKd......
................
....dKKKKKKd....
...KqqqqqqqqK...
...KqWqqqqWqK...
....KqqqqqqK....
.....KKKKKK.....
"""
LEGF = dict(K='K', q='q', e='v3', d='fl1', W='b3')


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
    # Hautfalten: unregelmäßig hängende Wülste, an den Seiten tiefer
    for k, (yy, x0, x1, sag) in enumerate(((0.42, -0.85, 0.2, 4), (0.55, 0.0, 0.8, 3), (0.72, -0.9, -0.1, 5), (0.8, 0.2, 0.9, 4))):
        y = BASE - ht * 2 * (1 - yy) * 0.82
        xa, xb = cx + hw * x0, cx + hw * x1
        pts = [(xa, y - 2), ((xa + xb) / 2, y + sag), (xb, y - 1)]
        p.line(pts, 'fl0', only=body)
        p.line([(xa + 2, y - 3), ((xa + xb) / 2, y + sag - 1)], 'fl3', only=body)
    for (ox, oy) in ((-0.5, 0.55), (0.45, 0.4), (0.15, 0.75), (-0.2, 0.3)):            # Warzen
        x_, y_ = int(cx + hw * ox), int(BASE - ht * 2 * (1 - oy) * 0.82)
        p.fill(E(x_, y_, 1.4, 1.2) & body, 'fl1'); p.pxs([(x_ - 1, y_ - 1)], 'fl3')
    # Bauchnabel-Falte und hängende Lappen am Boden
    p.form(E(cx - hw * 0.55, BASE - 4, 7, 4) & body, FLD, sd=1, hl=0)
    p.form(E(cx + hw * 0.5, BASE - 3, 8, 3) & body, FLD, sd=1, hl=0)
    c.stamp(p, 'K')
    # Gesicht (klein, verschwommen, oben)
    p = C(); p.grid(int(cx - 10), int(BASE - ht * 1.62), FACE, LEGF); c.stamp(p, 'K', ring=False)
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
