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
    hair = E(cx, cy - 4, 31, 28)
    for i in range(13):                                            # wirre Strähnen, vom Fall nach oben gerissen
        a = math.radians(-170 + i * 13 + (7 if i % 2 else -4))
        L_ = 14 + (i * 7 % 11)
        bx, by = cx + math.cos(a) * 22, cy - 4 + math.sin(a) * 20
        mx, my = bx + math.cos(a) * L_ * 0.5 + (3 if i % 3 == 0 else -2), by + math.sin(a) * L_ * 0.5 - 3
        tx, ty = bx + math.cos(a) * L_ + sway * 0.6 + (4 if i % 2 else -3), by + math.sin(a) * L_ - 7
        hair |= L(bx, by, 5.5, mx, my, 3.2) | L(mx, my, 3.2, tx, ty, 0.8)
    for s_ in (-1, 1):                                             # lange Seitensträhnen hängen am Gesicht herab
        hair |= L(cx + s_ * 25, cy - 2, 7, cx + s_ * 30, cy + 20, 3.4) | L(cx + s_ * 30, cy + 20, 3.4, cx + s_ * 27 + sway, cy + 36, 1.0)
    p.form(hair, ('h0', 'hb', 'h2'), sd=4, hl=1)
    hair_p = p
    for i in range(9):
        x = cx - 26 + i * 6.5
        p.line([(x, cy - 30), (x + 2, cy - 8)], 'h0', only=hair)
    c.stamp(p, 'K')
    # Gesicht: breit, fahl, eingefallen
    p = C()
    face = E(cx, cy + 7, 23, 25)
    p.form(face, SK, sd=5, hl=1)
    p.form(E(cx - 14, cy + 12, 6, 7) & face, ('k0', 'k1', 'k1'), sd=1, hl=0)      # eingefallene Wange
    p.form(E(cx + 14, cy + 12, 6, 7) & face, ('k0', 'k0', 'k1'), sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    p.grid(int(cx - 10), int(cy - 4), FACE, LEGF)
    c.stamp(p, 'K', ring=False)
    # zerzauste Stirnsträhnen über der Stirn (gleicher Haarblock, kein Band)
    p = C()
    bangs = np.zeros((px.H, px.W), bool)
    for (ox, ln, ang) in ((-19, 13, 100), (-12, 16, 93), (-4, 12, 86), (4, 15, 96), (12, 13, 82), (19, 11, 72)):
        bangs |= tri((cx + ox, cy - 17), ang, ln, 9)
    bangs &= E(cx, cy + 2, 26, 30)
    p.form(bangs, ('h0', 'hb', 'h2'), sd=2, hl=1)
    c.stamp(p, 'K')
    c.blacken()
    return c


col('hb', '#1a1738')
WALK = [dict(dy=0, sway=0), dict(dy=-1, sway=1), dict(dy=-2, sway=0), dict(dy=-1, sway=-1)]
ATTACK = [dict(dy=-8, sway=0), dict(dy=6, mouth=3), dict(dy=3, mouth=1)]

if __name__ == '__main__':
    export('tsurube_otoshi', draw, WALK, ATTACK)
