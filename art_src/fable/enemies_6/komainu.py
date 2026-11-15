"""Komainu – steinerner Löwenhund vor dem Schrein. Komplett neu (Runde 101): verwitterter Granit mit Moos,
gedrungener Löwenkörper mit tiefer Brust, Schulterblatt/Ellbogen/Handgelenk, Sprunggelenk hinten, Ballenpfoten
mit Krallen. Großer Kopf mit runden Glotzaugen, breiter Nase, offenem Maul (a-gyō) mit Reißzähnen,
gelockte Mähne um Kopf und Hals, Flammenschweif aus Locken, rotes Lätzchen mit Glocke. Blick nach links.
Angriff: duckt sich, springt mit offenem Maul nach vorn."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 108, 88
OX, OY = 8, 8                     # lokale Grundlinie y = 72
ST = ('z1', 'z2', 'z3')
STF = ('z0', 'z1', 'z2')
MOSS = ('g0', 'g1', 'g2')
EYE = """
.KKKK.
KyyyyK
KyYKyK
KyyKyK
.KKKK.
"""
LEG = dict(K='K', y='y2', Y='y3')


def P(x, y):
    return (x + OX, y + OY)


def curl(c, x, y, r, ramp=ST, line='z0'):
    p = C()
    m = E(x, y, r, r)
    p.form(m, ramp, sd=max(1, int(r / 2.6)), hl=1)
    pts = []
    for k in range(10):
        a = math.radians(210 - k * 42)
        rr = r * (0.78 - k * 0.07)
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    if r >= 3.8:
        p.line(pts, line, only=erode(m, 1))
    c.stamp(p, 'K')


def leg_front(c, sh_, elb, wr, paw, ramp, far=False):
    p = C()
    up = L(*sh_, 7.4, *elb, 5.0)
    fo = L(*elb, 4.6, *wr, 3.6)
    pw = E(paw[0], paw[1], 5.6, 3.0) | E(paw[0] + 1, paw[1] - 2, 4.0, 2.6)
    p.form(up | fo, ramp, sd=2, hl=0 if far else 1)
    p.form(pw, ramp, sd=1, hl=1)
    for k in range(3):                                                                    # Zehenfurchen + Krallen
        x = paw[0] - 3 + k * 2.5
        p.line([(x, paw[1] - 1), (x, paw[1] + 2)], ramp[0], only=pw)
    c.stamp(p, 'K')
    p = C()
    if not far:
        curl(c, elb[0] + 3, elb[1] - 1, 3.0)
        p.pxs([(int(paw[0]) - 5, int(paw[1]) + 1), (int(paw[0]) - 3, int(paw[1]) + 2)], 'b2')
    c.stamp(p, 'K')


def leg_hind(c, hip, knee, hock, paw, ramp, far=False):
    p = C()
    th = L(*hip, 8.4, *knee, 4.4) | E(hip[0], hip[1], 10, 9)
    sh = L(*knee, 4.4, *hock, 3.2)
    mt = L(*hock, 3.2, paw[0] + 1, paw[1] - 2, 3.0)
    pw = E(paw[0], paw[1], 5.0, 2.8)
    p.form(th, ramp, sd=3, hl=0 if far else 1)
    p.form(sh | mt, ramp, sd=1, hl=0 if far else 1)
    p.form(pw, ramp, sd=1, hl=1)
    p.line([(hip[0] - 6, hip[1] + 2), (knee[0] + 1, knee[1] - 2)], ramp[0], only=erode(th, 1))   # Oberschenkelmuskel
    p.pxs([(int(hock[0]) + 2, int(hock[1]))], ramp[0])
    for k in range(2):
        x = paw[0] - 2 + k * 2.5
        p.line([(x, paw[1] - 1), (x, paw[1] + 2)], ramp[0], only=pw)
    c.stamp(p, 'K')


def draw(bob=0, lean=0, jaw=0, crouch=0, fl=(0, 0), fr=(0, 0), hl_=(0, 0), hr=(0, 0), tail=0, air=0):
    setsize(CW, CH)
    c = C()

    def B(x, y):
        return P(x + lean, y + bob + crouch - air)

    gy = 72 - air
    # ---- Schweif: aufgerichtete Flamme aus Locken
    p = C()
    stem = L(*B(76, 42), 4.4, *P(82 + tail, 30 + bob + crouch - air), 3.4)
    p.form(stem, ST, sd=1, hl=1)
    c.stamp(p, 'K')
    for (x, y, r) in ((80, 28, 5.6), (89, 24, 5.0), (86, 35, 4.6), (79, 18, 4.4), (90, 14, 3.8), (84, 8, 3.0)):
        curl(c, *P(x + tail, y + bob + crouch - air), r)
    # ---- ferne Beine
    leg_hind(c, B(68, 46), P(62 + hr[0] + lean, 58 + crouch * 0.5 - air), P(72 + hr[0] + lean, 64 - air - hr[1]),
             P(69 + hr[0] + lean, gy - 1 - hr[1]), STF, far=True)
    leg_front(c, B(42, 48), P(46 + fr[0] + lean, 59 + crouch * 0.5 - air), P(42 + fr[0] + lean, 67 - air - fr[1]),
              P(38 + fr[0] + lean, gy - 1 - fr[1]), STF, far=True)
    # ---- Rumpf: Brust tief, Taille schmal, kräftige Kruppe
    p = C()
    body = E(*B(42, 44), 14, 13) | E(*B(56, 46), 13, 10) | E(*B(68, 43), 11, 11)
    p.form(body, ST, sd=4, hl=1)
    p.line([B(50, 51), B(56, 54), B(62, 52)], 'z1', only=erode(body, 1))             # Bauchlinie
    p.line([B(46, 36), B(54, 38)], 'z1', only=body)                                   # Schulterblatt
    p.line([B(54, 38), B(52, 46)], 'z1', only=body)
    for (x, y, rx, ry) in ((58, 37, 5, 2.4), (70, 34, 4.4, 2.2), (46, 33, 3, 1.8)):  # Moos auf dem Rücken
        mm = (E(*B(x, y), rx, ry) | E(*B(x - 1, y - 1.2), rx * 0.6, ry * 0.7)) & sh(body, 0, 2)
        p.form(mm, MOSS, sd=1, hl=1)
    for pts in (((62, 44), (64, 47), (63, 50)), ((72, 46), (74, 49))):                # Risse im Stein
        p.line([B(*q) for q in pts], 'z0', only=erode(body, 1))
    c.stamp(p, 'K')
    # ---- nahe Hinterbein
    leg_hind(c, B(70, 47), P(64 + hl_[0] + lean, 60 + crouch * 0.5 - air), P(75 + hl_[0] + lean, 66 - air - hl_[1]),
             P(72 + hl_[0] + lean, gy - hl_[1]), ST)
    # ---- Mähne hinter dem Kopf: Kranz aus Locken bis zur Brust
    for (x, y, r) in ((40, 10, 5.6), (47, 16, 6.0), (50, 25, 6.0), (49, 34, 5.6), (43, 40, 5.0), (34, 6, 5.0), (26, 4, 4.4), (19, 7, 3.6), (36, 40, 4.2), (29, 39, 4.0)):
        curl(c, *B(x, y), r)
    # ---- nahes Vorderbein
    leg_front(c, B(38, 47), P(41 + fl[0] + lean, 60 + crouch * 0.5 - air), P(37 + fl[0] + lean, 68 - air - fl[1]),
              P(33 + fl[0] + lean, gy - fl[1]), ST)
    # ---- Kopf: Schädel, breite Schnauze, Brauenwulst, Unterkiefer
    p = C()
    skull = E(*B(28, 22), 12, 11)
    muz = E(*B(18, 26), 8.0, 7.0) | R(*B(12, 21), *B(22, 30))
    nose = E(*B(12, 21), 4.6, 3.6)
    jawm = PG([B(12, 30 + jaw), B(25, 30), B(28, 34), B(21, 36 + jaw), B(14, 36 + jaw)])
    p.form(jawm, STF, sd=1, hl=1)
    p.form((skull | muz) & ~sh(jawm, 0, 1), ST, sd=3, hl=1)
    mouth = PG([B(10, 28), B(26, 28), B(24, 33 + jaw * 0.6), B(13, 34 + jaw)])
    p.fill(mouth, 'q')
    p.fill(E(*B(19, 33 + jaw * 0.7), 4.0, 1.6) & mouth, 'm2')                        # Zunge
    p.line([B(11, 28), B(26, 28)], 'z0')                                              # Lefzenkante
    p.form(nose, ('z0', 'z1', 'z2'), sd=1, hl=1)
    p.pxs([B(9, 22), B(12, 23)], 'K')                                                 # Nüstern
    brow = L(*B(17, 15), 2.8, *B(30, 13), 3.0)
    p.form(brow & ~E(*B(22, 12), 3, 1), ST, sd=1, hl=1)
    p.line([B(16, 17), B(26, 17)], 'z0', only=skull | muz)                            # Brauenschatten
    p.line([B(15, 26), B(18, 28), B(23, 28)], 'z1', only=muz)                         # Lefzenfalte
    p.line([B(26, 26), B(30, 30)], 'z1', only=skull)                                  # Wange
    for (x, y) in ((14, 26.5), (17, 27), (20, 27), (15, 25)):                     # Bart-Punkte
        p.pxs([B(x, y)], 'z1')
    # Zähne: obere Reihe + Reißzähne
    p.fill(R(*B(13, 29), *B(23, 29)), 'b3')                                          # obere Zahnreihe
    for x in (16, 19):
        p.pxs([B(x, 29)], 'b1')
    p.fill(L(*B(12.5, 29), 1.3, *B(13, 32), 0.6), 'b3')                             # Reißzähne
    p.fill(L(*B(23.5, 29), 1.1, *B(23.5, 31.5), 0.6), 'b2')
    p.fill(L(*B(16, 35 + jaw), 1.1, *B(16, 32.5 + jaw), 0.6), 'b3')
    # Bart: Locken unter dem Kinn
    c.stamp(p, 'K')
    p = C(); p.grid(*[int(v) for v in B(18, 16)], EYE, LEG); c.stamp(p, 'K')
    for (x, y, r) in ((20, 38 + jaw, 3.4), (26, 37 + jaw * 0.5, 3.6)):
        curl(c, *B(x, y), r)
    # Ohr hinter der Brauenwulst
    p = C()
    ear = PG([B(30, 8), B(36, 6), B(35, 13)])
    p.form(ear, STF, sd=1, hl=1)
    c.stamp(p, 'K')
    # ---- Lätzchen + Glocke
    p = C()
    bib = PG([B(27, 34), B(44, 30), B(42, 40), B(34, 46)])
    p.form(bib, ('m1', 'm2', 'm3'), sd=2, hl=1)
    p.line([B(28, 35), B(43, 31)], 'm0', only=bib)
    c.stamp(p, 'K')
    p = C()
    bell = E(*B(35, 46), 2.6, 2.6)
    p.form(bell, ('y0', 'y1', 'y2'), sd=1, hl=1)
    p.pxs([B(35, 47)], 'K')
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(fl=(-3, 0), fr=(3, 0), hl_=(3, 0), hr=(-3, 0)),
        dict(bob=-1, fl=(0, 2), fr=(1, 0), hl_=(1, 0), hr=(0, 2), tail=1),
        dict(fl=(3, 0), fr=(-3, 0), hl_=(-3, 0), hr=(3, 0)),
        dict(bob=-1, fl=(1, 0), fr=(0, 2), hl_=(0, 2), hr=(1, 0), tail=-1)]
ATTACK = [dict(crouch=3, jaw=1, fl=(2, 0), fr=(3, 0), tail=-1),
          dict(lean=-6, air=5, jaw=3, fl=(-5, 3), fr=(-3, 2), hl_=(5, 2), hr=(6, 3), tail=2),
          dict(lean=-3, jaw=2, fl=(-2, 0), fr=(0, 0))]

if __name__ == '__main__':
    export('komainu', draw, WALK, ATTACK)
