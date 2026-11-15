"""Tsurube-otoshi: riesiger körperloser Kopf mit wirrem schwarzem Haar, der aus den Baumkronen herabfällt.
Eigene Zeichnung im Serienstil. Angriff: fällt herab und schnappt mit dem Riesenmaul."""
import math
from common import *

CW, CH = 112, 120
CX, CY = 56, 70
SK = ('k0', 'k1', 'k2')
FACE = """
KKKKKK........KKKKKK
.KKKKKKK....KKKKKKK.
..KkkKKKK..KKKKkkK..
..KKeeEKK..KKEeeKK..
...KKeeK....KeeKK...
....KKK......KKK....
........kkkk........
.......kKKKKk.......
....................
..KKKKKKKKKKKKKKKK..
.KwKwwKwwKwwKwwKwK..
.KqqqqqqqqqqqqqqqqK.
.KqqqqqqqrrrrqqqqqK.
.KqqqqqqrrrrrrqqqqK.
.KwKwwKwwKwwKwwKwKK.
..KKKKKKKKKKKKKKKK..
"""
LEGF = dict(K='K', k='k0', e='e1', E='y3', w='b3', q='q', r='m2')


def draw(dy=0, mouth=0, sway=0):
    setsize(CW, CH)
    c = C()
    cx, cy = CX + sway, CY + dy
    # Haar: lange Strähnen nach oben (fällt herab) und zu den Seiten
    p = C()
    hair = E(cx, cy - 6, 34, 30)
    for i in range(11):
        a = math.radians(-160 + i * 14)
        L_ = 18 + (i * 5 % 9)
        bx, by = cx + math.cos(a) * 24, cy - 6 + math.sin(a) * 22
        tx = bx + math.cos(a) * L_ + sway * 0.5
        ty = by + math.sin(a) * L_ - 6
        hair |= L(bx, by, 6, tx, ty, 1.2)
    for s_ in (-1, 1):
        hair |= L(cx + s_ * 28, cy, 7, cx + s_ * 34, cy + 26, 2.0)
    p.form(hair, ('h0', 'hb', 'h2'), sd=4, hl=1)
    for i in range(9):
        x = cx - 26 + i * 6.5
        p.line([(x, cy - 30), (x + 2, cy - 8)], 'h0', only=hair)
    c.stamp(p, 'K')
    # Gesicht: breit, fahl, eingefallen
    p = C()
    face = E(cx, cy + 6, 22, 24)
    p.form(face, SK, sd=5, hl=1)
    p.form(E(cx - 14, cy + 12, 6, 7) & face, ('k0', 'k1', 'k1'), sd=1, hl=0)      # eingefallene Wange
    p.form(E(cx + 14, cy + 12, 6, 7) & face, ('k0', 'k0', 'k1'), sd=1, hl=0)
    # Stirnhaar (Pony) über dem Gesicht
    p.form((E(cx, cy - 14, 24, 10) | L(cx - 20, cy - 10, 4, cx - 18, cy + 4, 2)) & ~E(cx, cy + 4, 16, 9), ('h0', 'hb', 'h2'), sd=2, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.grid(int(cx - 10), int(cy - 4), FACE, LEGF)
    c.stamp(p, 'K', ring=False)
    c.blacken()
    return c


col('hb', '#1a1738')
WALK = [dict(dy=0, sway=0), dict(dy=-1, sway=1), dict(dy=-2, sway=0), dict(dy=-1, sway=-1)]
ATTACK = [dict(dy=-8, sway=0), dict(dy=6, mouth=3), dict(dy=3, mouth=1)]

if __name__ == '__main__':
    export('tsurube_otoshi', draw, WALK, ATTACK)
