"""Abura-akago – das Kind aus dem Irrlicht, das in den Häusern das Lampenöl aufleckt. Zweiter Neuentwurf
(Runde 107): schwebendes Kleinkind in Sitzhaltung (Knie angezogen), eingehüllt von einem Irrlicht, dessen
Flammen hinter ihm zum Schweif auslaufen. Warme, vom Feuer angestrahlte Haut, großer Kopf mit Karako-Frisur
(kahl rasiert, Büschel an Stirn und Schläfe), runde dunkle Augen mit Glutpunkt, Pausbacken. Hält mit beiden
Händchen eine Öllampenschale vors Gesicht und leckt daran. Rotes Bauchlätzchen.
Angriff: lässt die Schale sinken, reißt den Mund auf und spuckt Feuer – die Flammen lodern auf."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 92, 72
OX, OY = 8, 8
col('hb', '#1a1738')
SK = ('k1', 'k2', 'k3')
SKD = ('k0', 'k1', 'k2')
LEG = dict(zip('abcdKqWhHeEm', ['k0', 'k1', 'k2', 'k3', 'K', 'q', 'y2', 'h0', 'hb', 'e1', 'y3', 'm2']))
# Kopf im Dreiviertelprofil nach links: rasierter Schädel (Haut), Stirnbüschel + Schläfenbüschel, große Augen
HEAD = """
.......hhhh......
.....hhHHHhccc...
....hHHHhddddcbb.
...hHhhdddddcccbb
...hhddddddccccbb
..cddddddddcccccbh
..ddKKKddKKKcccbbh
.cdKKWKdKKWKcccbhH
.cdKKKKdKKKKccbbhH
.ddcKKcddKKcccbbhh
dddddddcdcccccbb.
.ddmmdcddcccccbbb.
.cddddqqqdcccbbba.
..ccccqmqcccbbbaa.
...ccccccccbbbaa..
....bbbbbbbbaaa...
......aaaaaa......
"""


def P(x, y):
    return (x + OX, y + OY)


def draw(bob=0, flare=0, mouth=0, dish=1, kick=0, wv=0.0):
    setsize(CW, CH)
    c = C()

    def B(x, y):
        return P(x, y + bob)

    # ---- Irrlicht: Flammenzungen steigen hinter dem Rücken auf
    tips = []
    for k in range(4):
        t = k / 3
        base = B(44 + t * 4, 32 + t * 14)
        tip = B(58 + t * 12 + flare * 2 + math.sin(wv + k * 1.7) * 2, 16 + t * 14 - flare * 2)
        tips.append((base, tip, 5.4 - t * 1.4 + flare * 0.3))
    flame(c, None, tips, w=5)
    # ---- fernes Bein (angezogen)
    p = C()
    p.form(L(*B(42, 44), 4.0, *B(34 - kick, 48), 3.2) | L(*B(34 - kick, 48), 3.0, *B(40 - kick, 53), 2.4), SKD, sd=1, hl=0)
    c.stamp(p, 'K')
    # ---- Rumpf: Babybauch
    p = C()
    tor = E(*B(38, 38), 8.4, 9.4)
    p.form(tor, SK, sd=3, hl=1)
    bib = PG([B(31, 32), B(40, 31), B(44, 38), B(40, 47), B(32, 46)]) & sh(tor, 0, 1)
    p.form(bib, ('m1', 'm2', 'm3'), sd=1, hl=1)
    p.line([B(31, 33), B(40, 32)], 'y1', only=bib)
    p.fill(E(*B(37, 39), 1.6, 1.6) & bib, 'y1')
    p.pxs([B(37, 39)], 'm1')
    c.stamp(p, 'K')
    # ---- nahes Bein: Oberschenkel nach vorn, Unterschenkel hängt, Fußsohle sichtbar
    p = C()
    th = L(*B(42, 45), 4.2, *B(33 - kick, 50), 3.4)
    sn = L(*B(33 - kick, 50), 3.2, *B(37 - kick * 0.5, 57), 2.4)
    p.form(th | sn, SK, sd=2, hl=1)
    p.pxs([B(31 - kick, 52), B(32 - kick, 52)], 'k1')                 # Speckfalte in der Kniekehle
    foot = E(*B(39 - kick * 0.5, 58), 3.2, 2.0)
    p.form(foot, SK, sd=1, hl=1)
    for k in range(3):
        p.pxs([B(41 - kick * 0.5, 57 + k)], 'k1')
    c.stamp(p, 'K')
    # ---- Kopf
    p = C()
    p.grid(*[int(v) for v in B(20, 12)], HEAD, LEG)
    if mouth:
        p.fill(E(*B(28, 25), 2.2 + mouth * 0.4, 1.2 + mouth * 0.7), 'q')
        p.pxs([B(28, 25 + mouth * 0.5)], 'm2')
    c.stamp(p, 'K', skip=('h0', 'hb'))
    # ---- Arme + Ölschale
    hy = 31 if dish else 38
    if dish:
        p = C()
        sc = E(*B(19, hy), 6.4, 2.4)
        p.form(sc, ('w0', 'w1', 'w2'), sd=1, hl=1)
        p.fill(E(*B(19, hy - 1), 5.0, 1.0), 'y1')
        p.pxs([B(17, hy - 1)], 'y3')
        c.stamp(p, 'K')
        p = C()                                                          # Zunge leckt über den Rand
        p.form(L(*B(27, 26), 1.3, *B(22, hy - 1.5), 1.0), ('m1', 'm2', 'm3'), sd=0, hl=1)
        c.stamp(p, 'K')
    for (sx, far) in ((36, True), (32, False)):
        p = C()
        sh_ = B(sx, 31)
        el = B(sx - 3, 38 if dish else 40)
        hd = B(22 + (4 if far else 0), hy + 1) if dish else B(sx - 9, 42)
        ramp = SKD if far else SK
        p.form(L(*sh_, 2.4, *el, 2.0) | L(*el, 2.0, *hd, 1.7), ramp, sd=1, hl=1)
        p.form(E(hd[0], hd[1], 2.0, 1.8), ramp, sd=1, hl=1)
        p.pxs([(el[0] + 1, el[1])], ramp[0])
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(wv=0), dict(bob=-1, wv=1.2, kick=1), dict(bob=-2, wv=2.4), dict(bob=-1, wv=3.6, kick=-1)]
ATTACK = [dict(dish=0, mouth=1, flare=2, wv=1), dict(dish=0, mouth=3, flare=4, wv=2, bob=-1), dict(dish=0, mouth=2, flare=2, wv=3)]

if __name__ == '__main__':
    export('abura_akago', draw, WALK, ATTACK)
