"""Kawauso – der Fischotter, der Wanderer mit einem Laternenlicht ans Wasser lockt. Komplett neu (Runde 109):
echte Otteranatomie, nur aufgerichtet: langer, geschmeidiger Leib, kleiner flacher Kopf mit breiter Schnauze,
Schnurrhaaren und winzigen Ohren, helle Kehle, kurze Beine mit Schwimmhautfüßen, dicker spitz zulaufender
Ruderschwanz. Nasses, glänzendes Fell. Trägt einen breiten Strohhut (kasa) mit Kinnband und hält an einem
Stecken eine Papierlaterne. Angriff: schwingt die Laterne vor, ihr Licht flammt auf."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 96, 84
OX, OY = 14, 4                     # lokale Grundlinie y = 76
col('kw0', '#160e16'); col('kw1', '#3a2220'); col('kw2', '#68402c'); col('kw3', '#9a6a40'); col('kw4', '#d0b088')
add_rim('kw0 kw1 kw2', 'xt'); DARK.update(kw4='kw3', kw3='kw2', kw2='kw1', kw1='kw0')
FUR = ('kw1', 'kw2', 'kw3')
FURF = ('kw0', 'kw1', 'kw2')
THR = ('kw2', 'kw3', 'kw4')
STRAW = ('o0', 'o1', 'o2')


def P(x, y):
    return (x + OX, y + OY)


def draw(bob=0, g=0, swing=0, glow=0, tw=0.0):
    setsize(CW, CH)
    c = C()
    sw = [-2, 2][g % 2]

    def B(x, y):
        return P(x, y + bob)

    # ---- ferner Arm: Pfote vor dem Bauch
    p = C()
    p.form(L(*B(34, 42), 2.6, *B(30, 50), 2.2) | L(*B(30, 50), 2.2, *B(26, 52), 1.8), FURF, sd=1, hl=0)
    c.stamp(p, 'K')
    # ---- Schwanz: dick, lang, am Boden geschwungen
    p = C()
    pts = [B(40, 60), P(48, 68), P(58 + math.sin(tw) * 2, 73), P(70 + math.sin(tw + 1) * 3, 74)]
    tail = L(*pts[0], 6, *pts[1], 5) | L(*pts[1], 5, *pts[2], 3.6) | L(*pts[2], 3.6, *pts[3], 1.2)
    p.form(tail, FUR, sd=2, hl=1)
    p.line([pts[1], pts[2]], 'kw3', only=erode(tail, 1))
    c.stamp(p, 'K')
    # ---- fernes Bein
    p = C()
    hip = B(38, 62); kn = P(34 + sw, 70); ft = P(30 + sw, 76)
    p.form(L(*hip, 5, *kn, 3.4) | L(*kn, 3.2, ft[0] + 2, ft[1] - 1, 2.4), FURF, sd=1, hl=0)
    p.form(E(ft[0], ft[1] - 1, 4.4, 1.8), FURF, sd=1, hl=1)
    c.stamp(p, 'K')
    # ---- Leib: lang und geschmeidig, leicht vorgebeugt
    p = C()
    body = E(*B(30, 42), 8, 11) | E(*B(35, 56), 10, 11) | L(*B(30, 34), 6, *B(36, 60), 9)
    p.form(body, FUR, sd=4, hl=1)
    thr = (E(*B(24, 40), 4.6, 9) | E(*B(28, 54), 5.4, 8)) & body           # helle Kehle und Bauch
    p.form(thr, THR, sd=1, hl=1)
    for (x, y) in ((40, 46), (42, 54), (38, 38)):                          # nasse Fellsträhnen
        p.line([B(x, y), B(x + 1, y + 3)], 'kw1', only=erode(body, 1))
    p.pxs([B(32, 36), B(33, 36), B(31, 37)], 'kw4')                        # Nässeglanz
    c.stamp(p, 'K')
    # ---- nahes Bein
    p = C()
    hip = B(36, 64); kn = P(32 - sw, 71); ft = P(26 - sw, 76)
    lg = L(*hip, 6, *kn, 3.8) | L(*kn, 3.6, ft[0] + 3, ft[1] - 1, 2.6)
    p.form(lg, FUR, sd=2, hl=1)
    foot = E(ft[0], ft[1] - 1, 5.0, 2.0)
    p.form(foot, FUR, sd=1, hl=1)
    for k in range(4):                                                     # Zehen mit Schwimmhaut
        p.pxs([(ft[0] - 4 + k * 2.2, ft[1])], 'kw0')
    c.stamp(p, 'K')
    # ---- Kopf: flach, breite Schnauze
    p = C()
    head = E(*B(26, 25), 8.0, 6.6) | E(*B(19, 28), 5.4, 4.0)
    neck = L(*B(28, 28), 5.4, *B(30, 36), 6.4)
    p.form(neck, FUR, sd=2, hl=1)
    p.form(head, FUR, sd=2, hl=1)
    p.form(E(*B(19, 30), 4.4, 2.6) & head, THR, sd=1, hl=1)               # helle Schnauzenunterseite
    p.fill(E(*B(14.5, 27), 1.6, 1.3), 'K')                                 # Nase
    p.pxs([B(14, 26)], 'kw3')
    p.line([B(15, 30), B(19, 31)], 'kw0')                                  # Maulspalte
    p.fill(E(*B(22, 24), 1.6, 1.4), 'K')                                   # Auge
    p.pxs([B(21.4, 23.4)], 'v3')
    p.fill(E(*B(31, 22), 1.6, 1.4), 'kw1')                                 # kleines Ohr
    c.stamp(p, 'K')
    p = C()
    for k in range(3):                                                     # Schnurrhaare
        p.line([B(17, 28 + k), B(10, 26 + k * 2.4)], 'kw4')
    c.stamp(p, ring=False)
    # ---- Strohhut mit Kinnband
    p = C()
    hat = PG([B(12, 18), B(28, 8), B(45, 18), B(40, 19), B(16, 19)])
    p.form(hat, STRAW, sd=2, hl=1)
    for k in range(1, 6):                                                  # Flechtrippen
        p.line([B(28, 9), B(12 + k * 5.5, 18)], 'o0', only=hat)
    p.line([B(14, 17), B(43, 17)], 'o0', only=hat)
    p.pxs([B(28, 8)], 'o3')
    c.stamp(p, 'K')
    p = C()
    p.line([B(30, 19), B(30, 27), B(27, 31)], 'm1')                        # Kinnband
    c.stamp(p, ring=False)
    # ---- naher Arm mit Laternenstecken
    p = C()
    sh_ = B(30, 40); el = B(26, 47 - swing); pw = B(20 - swing * 2, 44 - swing * 2)
    p.form(L(*sh_, 3.4, *el, 2.8) | L(*el, 2.6, *pw, 2.2), FUR, sd=1, hl=1)
    tip = (pw[0] - 12 - swing * 2, pw[1] - 10 + swing)
    stick = L(pw[0] + 3, pw[1] + 2, 0.8, *tip, 0.7)
    p.form(stick, ('w0', 'w1', 'w2'), sd=0, hl=1)
    p.form(E(*pw, 2.4, 2.0), FUR, sd=1, hl=1)
    c.stamp(p, 'K')
    # ---- Papierlaterne (chōchin) am Stecken
    lx, ly = tip[0] - 1, tip[1] + 11 + swing * 0.5
    p = C()
    p.line([tip, (lx, ly - 7)], 'w0')
    c.stamp(p, ring=False)
    p = C()
    lan = E(lx, ly, 5.4, 6.4)
    p.form(lan, ('y1', 'y2', 'y3') if glow else ('y0', 'y1', 'y2'), sd=2, hl=1)
    for k in (-3, 0, 3):                                                   # Bambusrippen
        p.line([(lx - 5, ly + k), (lx + 5, ly + k)], 'y0' if not glow else 'y1', only=lan)
    p.fill(R(lx - 3, ly - 7, lx + 3, ly - 6), 'm1')                        # Kappen oben/unten
    p.fill(R(lx - 3, ly + 6, lx + 3, ly + 7), 'm1')
    p.line([(lx - 1, ly - 2), (lx + 1, ly + 2)], 'm2', only=lan)           # Schriftzeichen
    p.line([(lx + 1, ly - 2), (lx - 1, ly + 1)], 'm2', only=lan)
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(g=0, tw=0), dict(g=1, bob=-1, tw=1), dict(g=0, tw=2), dict(g=1, bob=-1, tw=3)]
ATTACK = [dict(swing=-2, tw=0.5), dict(swing=3, glow=1, tw=1), dict(swing=1, glow=1, tw=1.5)]

if __name__ == '__main__':
    export('kawauso', draw, WALK, ATTACK)
