"""Kumo – kleine Giftspinne, die in Schwärmen kommt. Komplett neu (Runde 106): Springspinnen-Bauweise,
damit sie trotz geringer Größe lesbar bleibt: hohes Kopfbruststück mit zwei großen glühenden Frontaugen und
kleinen Nebenaugen, Kieferklauen mit Giftzähnen, behaarte Beine mit hellen Gelenken, runder Hinterleib mit
rotem Sanduhr-Fleck und Haarflaum. Angriff: duckt sich und springt mit gespreizten Vorderbeinen."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 60, 46
OX, OY = 4, 6                     # lokale Grundlinie y = 36
BODY = ('u1', 'u2', 'u3')
BODYF = ('u0', 'u1', 'u2')


def P(x, y):
    return (x + OX, y + OY)


def leg(c, hip, knee, foot, ramp, joint):
    p = C()
    m = L(*P(*hip), 1.6, *P(*knee), 1.3) | L(*P(*knee), 1.3, *P(*foot), 0.7)
    p.form(m, ramp, sd=1, hl=1)
    p.pxs([P(*knee)], joint)
    c.stamp(p, 'K')


def draw(bob=0, g=0, crouch=0, air=0, spread=0, fang=0):
    setsize(CW, CH)
    c = C()
    dy = bob + crouch - air
    gy = 36 - air
    lifts = [[0, 2, 0, 2], [2, 0, 2, 0]][g % 2]
    sw = [-1, 1][g % 2]
    # Beine: (Hüfte, Knie, Fuß) für vier Beinpaare, vorn → hinten
    def legs(far):
        out = []
        for i in range(4):
            hx = 20 + i * 2.4 + (1 if far else 0)
            hy = 25 + dy - (1 if far else 0)
            fx = [2, 12, 34, 48][i] + (3 if far else 0) + (sw if (i % 2) ^ far else -sw)
            if i == 0 and spread:
                fx -= spread; ly = gy - spread * 1.6
            else:
                ly = gy - (lifts[i] if not far else lifts[(i + 1) % 4]) - (2 if far else 0)
            kx = hx + (fx - hx) * 0.45
            ky = (hy + 2) if (i < 2 and not far and not spread) else min(hy, ly) - 4 - (i in (0, 3)) * 2
            out.append(((hx, hy), (kx, ky), (fx, ly)))
        return out
    for (h, k, f) in legs(True):
        leg(c, h, k, f, BODYF, 'u2')
    # Hinterleib
    p = C()
    abd = E(*P(38, 22 + dy), 10.4, 8.4)
    p.form(abd, BODY, sd=3, hl=1)
    hg = PG([P(37, 14 + dy), P(43, 14 + dy), P(40, 17 + dy), P(43, 20 + dy), P(37, 20 + dy), P(40, 17 + dy)])
    p.fill(hg & abd, 'm2')
    p.pxs([P(38, 15 + dy)], 'm3')
    for k in range(7):                                               # Haarflaum am Rand
        a = math.radians(200 + k * 25)
        q = P(38 + math.cos(a) * 10, 22 + dy + math.sin(a) * 8)
        p.pxs([q], 'u3')
    p.pxs([P(47, 24 + dy), P(48, 25 + dy)], 'u0')                     # Spinnwarzen
    c.stamp(p, 'K')
    # Kopfbruststück
    p = C()
    ceph = E(*P(21, 21 + dy), 8.4, 6.4) | E(*P(17, 19 + dy), 5.4, 5.4)
    p.form(ceph, BODY, sd=2, hl=1)
    p.line([P(18, 15 + dy), P(26, 16 + dy)], 'u3', only=ceph)          # helle Haarbinde
    c.stamp(p, 'K')
    # Augen: zwei große Frontaugen + Nebenaugen
    p = C()
    for (ex, ey, r) in ((13, 20, 2.2), (17, 20.5, 2.0)):
        p.fill(E(*P(ex, ey + dy), r, r), 'K')
        p.fill(E(*P(ex, ey + dy + 0.3), r - 0.8, r - 0.8), 'e1')
        p.pxs([P(ex - 0.7, ey + dy - 0.7)], 'y3')
    for (ex, ey) in ((20, 17), (23, 17.5)):
        p.fill(E(*P(ex, ey + dy), 1.0, 1.0), 'e0')
    c.stamp(p, 'K')
    # Kieferklauen + Giftzähne
    p = C()
    for (x, far) in ((15, True), (12, False)):
        ch = L(*P(x, 24 + dy), 1.6, *P(x - 0.5, 27 + dy), 1.2)
        p.form(ch, BODYF if far else BODY, sd=1, hl=1)
        p.fill(L(*P(x - 0.5, 28 + dy), 0.7, *P(x - 1.5 - fang, 30 + dy + fang), 0.4), 'b3')
    c.stamp(p, 'K')
    for (h, k, f) in legs(False):
        leg(c, h, k, f, BODY, 'u3')
    c.blacken()
    return c


WALK = [dict(g=0), dict(g=1, bob=-1), dict(g=0, bob=0), dict(g=1, bob=-1)]
ATTACK = [dict(crouch=2, fang=0), dict(air=6, spread=4, fang=1), dict(air=2, spread=2, fang=1)]

if __name__ == '__main__':
    export('kumo', draw, WALK, ATTACK)
