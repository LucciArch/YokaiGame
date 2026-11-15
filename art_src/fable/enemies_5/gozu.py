"""Gozu und Mezu: Höllenwächter mit Ochsenkopf aus Enmas Hof. Massiger Körper, Lendentuch und Gürtel aus Seil,
gegabelte Fangstange (sasumata). Blick nach links. Angriff: stampft – Schockwelle."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 84, 112
SKIN = ('z1', 'z2', 'z3')       # schiefergraue Haut
SKINF = ('z0', 'z1', 'z2')
HEAD = ('s1', 's2', 's3')       # Ochsenkopf braun
HORN = ('b0', 'b1', 'b2')
CLOTH = ('t0', 't1', 't2')      # Tigerfell
IRON = ('i1', 'i2', 'i3')


HORSE = False


def draw(bob=0, step=0, lift=0, stomp=0):
    setsize(CW, CH)
    c = C()
    cx, by = 42, 106
    hip = by - 30 + bob - stomp
    # ferne Beine
    p = C()
    p.form(L(cx + 6 - step, hip + 2, 6.4, cx + 8 - step, by - 4, 5.0), SKINF, sd=2, hl=0)
    p.form(E(cx + 7 - step, by - 2, 6.4, 3.0), SKINF, sd=1, hl=0)
    c.stamp(p, 'K')
    # Rumpf
    p = C()
    torso = E(cx, hip - 16, 15.4, 16.4) | E(cx + 2, hip - 2, 12.4, 8.4)
    p.form(torso, SKIN, sd=4, hl=1)
    for (ox, oy) in ((-7, -22), (3, -22)):                                       # zwei Brustmuskeln (Vorderansicht)
        p.form(E(cx + ox, hip + oy, 6.6, 5.0) & torso, SKIN, sd=2, hl=1)
    p.line([(cx - 2, hip - 26), (cx - 2, hip - 4)], 'z0', only=torso)             # Mittellinie
    for yy in (-14, -9):                                                         # Bauchmuskeln
        p.line([(cx - 8, hip + yy), (cx + 5, hip + yy)], 'z1', only=torso)
    p.form(E(cx + 9, hip - 26, 6.4, 5.4) & torso, SKINF, sd=2, hl=0)            # ferne Schulter
    c.stamp(p, 'K')
    # Lendentuch aus Tigerfell + Seilgürtel
    p = C()
    loin = PG([(cx - 12, hip - 4), (cx + 14, hip - 4), (cx + 12, hip + 10), (cx - 10, hip + 12)])
    p.form(loin, CLOTH, sd=2, hl=1)
    for k in range(4):
        p.line([(cx - 8 + k * 6, hip - 3), (cx - 6 + k * 6, hip + 9)], 'K', only=loin)
    p.form(R(cx - 13, hip - 6, cx + 15, hip - 3), ('c0', 'c1', 'c2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # nahes Bein
    p = C()
    p.form(L(cx - 6 + step, hip + 4, 7.0, cx - 8 + step, by - 4, 5.4), SKIN, sd=2, hl=1)
    p.form(E(cx - 9 + step, by - 2, 7.4, 3.2), SKIN, sd=1, hl=1)
    c.stamp(p, 'K')
    if HORSE:
        hx, hy = cx - 1, hip - 44 - stomp
        p = C()
        mane = L(hx + 6, hy - 8, 3.4, hx + 12, hy + 12, 3.0) | E(hx + 6, hy - 6, 4.4, 3.4)
        p.form(mane, ('h0', 'hb', 'h2'), sd=1, hl=1)
        c.stamp(p, 'K')
        p = C()
        head = E(hx + 3, hy - 1, 9.0, 8.6) | L(hx, hy + 1, 7.4, hx - 17, hy + 7, 5.0)
        p.form(head, ('v0', 'v1', 'v2'), sd=3, hl=1)
        p.form(E(hx - 17, hy + 8, 4.6, 3.8) & head, ('b0', 'b1', 'b1'), sd=1, hl=0)
        p.fill(E(hx - 19, hy + 6, 1.1, 1.1), 'K'); p.fill(E(hx - 15, hy + 6, 1.0, 1.0), 'K')
        p.line([(hx - 20, hy + 11), (hx - 12, hy + 11)], 'v0')                                                    # Maulspalte
        p.form(PG([(hx + 4, hy - 8), (hx + 7, hy - 15), (hx + 9, hy - 7)]), ('v0', 'v1', 'v2'), sd=1, hl=1)   # Ohr
        for ex in (-5, 3):
            p.fill(E(hx + ex, hy - 2, 1.7, 1.5), 'e1'); p.pxs([(hx + ex, hy - 3)], 'y3')
            p.line([(hx + ex - 3, hy - 5), (hx + ex + 2, hy - 5)], 'v0')
        c.stamp(p, 'K')
    else:
        # Ochsenkopf: breite Schnauze nach links, Hörner, Nasenring
        # Ochsenkopf in Dreiviertelansicht: breite Schnauze, beide Augen, weit ausladende Hörner, Nasenring
        hx, hy = cx - 3, hip - 40 - stomp
        p = C()
        horns = (L(hx + 6, hy - 7, 3.2, hx + 17, hy - 12, 2.4) | L(hx + 17, hy - 12, 2.4, hx + 19, hy - 23, 0.9)
                 | L(hx - 6, hy - 8, 3.2, hx - 15, hy - 14, 2.4) | L(hx - 15, hy - 14, 2.4, hx - 14, hy - 25, 0.9))
        p.form(horns, HORN, sd=1, hl=1)
        c.stamp(p, 'K')
        p = C()
        head = E(hx, hy, 11.4, 10.4) | E(hx - 4, hy + 7, 9.4, 7.4)
        p.form(head, HEAD, sd=3, hl=1)
        p.form(E(hx - 5, hy + 9, 7.4, 5.0) & head, ('k0', 'k1', 'k2'), sd=1, hl=0)    # helle Schnauze
        p.fill(E(hx - 9, hy + 8, 1.3, 1.1), 'K'); p.fill(E(hx - 2, hy + 8, 1.3, 1.1), 'K')   # Nüstern
        ring = E(hx - 5, hy + 13, 3.0, 2.2) & ~E(hx - 5, hy + 13, 1.4, 0.9)
        p.fill(ring, 'y2')
        p.form(E(hx + 12, hy - 3, 4.2, 2.6) | E(hx - 13, hy - 4, 3.6, 2.4), HEAD, sd=1, hl=1)   # Ohren
        for ex in (-8, 2):                                                        # beide glühenden Augen
            p.fill(E(hx + ex, hy - 1, 1.8, 1.5), 'e1'); p.pxs([(hx + ex, hy - 2)], 'y3')
            p.line([(hx + ex - 3, hy - 4), (hx + ex + 2, hy - 4 + (1 if ex < 0 else -1))], 's0')
        c.stamp(p, 'K')
    # Fangstange vorn (sasumata), Stiel steht schräg neben dem Kopf
    hnd = (cx - 17, hip - 12 - lift * 4)
    p = C()
    sx1, sy1 = hnd[0] - 7, hnd[1] - 42
    p.form(L(hnd[0] + 3, hnd[1] + 16, 1.8, sx1, sy1, 1.8), ('w0', 'w1', 'w2'), sd=1, hl=1)
    fork = (L(sx1 - 5, sy1 - 1, 1.4, sx1 + 5, sy1 + 1, 1.4) | L(sx1 - 5, sy1 - 1, 1.3, sx1 - 6, sy1 - 7, 1.1)
            | L(sx1 + 5, sy1 + 1, 1.3, sx1 + 6, sy1 - 5, 1.1))
    p.form(fork, IRON, sd=1, hl=1)
    c.stamp(p, 'K')
    # naher Arm mit Schulter, hält den Stiel
    p = C()
    p.form(E(cx - 9, hip - 27, 6.4, 5.4), SKIN, sd=2, hl=1)
    p.form(L(cx - 10, hip - 24, 5.0, hnd[0] + 1, hnd[1] + 1, 4.0), SKIN, sd=2, hl=1)
    p.form(E(hnd[0], hnd[1], 4.4, 4.0), SKIN, sd=1, hl=1)
    c.stamp(p, 'K')
    c.blacken()
    return c


col('hb', '#1a1738')
WALK = [dict(step=-3), dict(bob=-1), dict(step=3), dict(bob=-1)]
ATTACK = [dict(lift=2, bob=-1), dict(stomp=-2, step=4, lift=0, bob=2), dict(lift=1)]

if __name__ == '__main__':
    export('gozu', draw, WALK, ATTACK)
    HORSE = True
    col('z1', '#4a2a2e'); col('z2', '#7a4440'); col('z3', '#a86a5a'); col('z0', '#2a141c')   # rötliche Haut für Mezu
    export('mezu', draw, WALK, ATTACK)
