"""Wanyūdō (Flammenrad mit Mönchsgesicht) und Katawaguruma (Rad in rosa Flammen mit Frauengesicht).
Eigene Zeichnung im Stil der Serie (px-Engine). Angriff: das Rad holt aus und rollt vorwärts."""
import math
from common import *

col('hb', '#1a1738'); col('pf0', '#7a1458'); col('pf1', '#e0408e'); col('pf2', '#ffa6d2')
CW, CH = 120, 104
CX, CY, RO, RI = 62, 58, 24, 18
MONK = dict(K='K', a='k0', b='k1', c='k2', d='k3', e='e1', E='y3', q='q', w='b3', h='h0')
WOMAN = dict(K='K', a='k1', b='k2', c='k3', d='v3', e='e1', E='y3', q='q', w='b3', h='hb', r='m2')
MONK_FACE = """
.....KKKKKKKK.....
...KKbcccccccbKK..
..KbcccdddccccbaK.
.KbccddccccccccbaK
.KbcccccccccccbbaK
KbKKKKccccccKKKKbaK
KbcKeEKccccKEeKcbaK
KbccKKccccccKKccbaK
KbcccccbccbcccccbaK
KbbccccbbbbcccccbaK
.KbcKKKKKKKKKKcbbaK
.KbcKqwqwqwqwqKbaK.
..KbKqqqqqqqqqKbaK.
..KbbKwqwqwqwKbbaK.
...KbbKKKKKKKbbaK..
....KKbbbbbbbaKK...
......KKKKKKKK.....
"""
WOMAN_FACE = """
....KKKKKKKKKK....
..KKhhhhhhhhhhKK..
.KhhhhhhhhhhhhhhK.
KhhhbbbbbbbbbbhhhK
KhhbcccccccccccbhK
KhbKKKKccccKKKKbhK
KhbcKeEKccKEeKccbhK
KhbcbKKccccKKbccbhK
KhbcccccbbccccccbhK
KhbcccccccccccccbhK
KhhbccKrrrrrKccbhhK
KhhbcccKKKKKcccbhhK
KhhhbccccccccccbhhK
.KhhhbbbbbbbbbbhhK.
.KhhhhhhhhhhhhhhhK.
..KhhhKhhhhhhKhhK..
...KK..KKKKKK.KK...
"""


def wheel(face, legend, fire, ang=0.0, dx=0, dy=0, flare=0, spin=0.0):
    setsize(CW, CH)
    c = C()
    cx, cy = CX + dx, CY + dy
    # Flammenkranz (hinter dem Rad): geschlossener Ring + lodernde Zungen, nach oben gezogen
    tips = []
    for i in range(14):
        a = math.radians(i * (360 / 14) + spin)
        L_ = 7 + (i * 7 % 5) + flare + (3 if (i + int(ang / 11)) % 3 == 0 else 0)
        bx, by = cx + math.cos(a) * (RO - 3), cy + math.sin(a) * (RO - 3)
        up = 5 if math.sin(a) < 0.3 else 2
        tx = cx + math.cos(a) * (RO + L_) + math.sin(a) * 2
        ty = cy + math.sin(a) * (RO + L_) - up
        tips.append(((bx, by), (tx, ty), 6.0))
    ring = E(cx, cy - 1, RO + 5, RO + 5)
    q = C(); q.fill(ring, fire[1]); q.fill(E(cx, cy - 1, RO + 2, RO + 2), fire[2]); c.stamp(q, fire[0])
    flame(c, None, tips, ramp=fire, core='y3', ln=fire[0])
    # Holzrad: Felge
    p = C()
    rim = E(cx, cy, RO, RO) & ~E(cx, cy, RI, RI)
    p.form(rim, ('w0', 'w1', 'w2'), sd=3, hl=1)
    for k in range(12):
        a = math.radians(k * 30 + ang)
        p.line([(cx + math.cos(a) * RI, cy + math.sin(a) * RI), (cx + math.cos(a) * RO, cy + math.sin(a) * RO)], 'w0', only=rim)
    c.stamp(p, 'K')
    # Speichen
    p = C()
    sp = np.zeros((px.H, px.W), bool)
    for k in range(8):
        a = math.radians(k * 45 + ang)
        sp |= L(cx + math.cos(a) * 9, cy + math.sin(a) * 9, 1.6, cx + math.cos(a) * RI, cy + math.sin(a) * RI, 1.4)
    p.form(sp, ('w0', 'w1', 'w2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # Gesicht in der Nabe (handgesetzt)
    p = C()
    rows = face.strip('\n').split('\n')
    p.grid(int(cx - len(rows[0]) / 2), int(cy - len(rows) / 2), face, legend)
    c.stamp(p, 'K', ring=False)
    c.blacken()
    return c


def make(name, face, legend, fire):
    def fn(ang=0.0, dx=0, dy=0, flare=0, spin=0.0):
        return wheel(face, legend, fire, ang, dx, dy, flare, spin)
    WALK = [dict(ang=a, spin=a * 2) for a in (0, 11.25, 22.5, 33.75)]
    ATTACK = [dict(ang=-10, dx=5, dy=-2, flare=3), dict(ang=40, dx=-9, flare=6, spin=90), dict(ang=20, dx=-4, flare=2)]
    export(name, fn, WALK, ATTACK)


if __name__ == '__main__':
    make('wanyudo', MONK_FACE, MONK, ('f0', 'f1', 'f2'))
    make('katawaguruma', WOMAN_FACE, WOMAN, ('pf0', 'pf1', 'pf2'))
