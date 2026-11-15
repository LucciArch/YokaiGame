"""Nuppeppo – wandelnder Fleischklumpen. Komplett neu (Runde 102): kein Ei mehr, sondern ein gestauchter Haufen
aus hängenden Fettwülsten, die übereinander hängen (Kopfwulst über Brustwulst über Bauchwulst). Kurze
Elefantenbeine mit Zehen, Stummelarme mit drei Fingerwülsten. Gesicht tief in den Falten: verschwollene
Schlitzaugen, zwei Nasenlöcher, hängende nasse Unterlippe. Warzen, Faltenlinien, feuchte Glanzpunkte,
zwei Fliegen. Blick nach links. Angriff: richtet sich auf und lässt sich bäuchlings fallen."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 84, 88
OX, OY = 10, 4                     # lokale Grundlinie y = 72
col('np0', '#2a1630'); col('np1', '#6a3a50'); col('np2', '#ac7680'); col('np3', '#dcaaa4'); col('np4', '#f8e0d4')
col('xnp', '#f8d6c8'); add_rim('np0 np1 np2', 'xnp')
DARK.update(np4='np3', np3='np2', np2='np1', np1='np0')
FL = ('np1', 'np2', 'np3')
FLD = ('np0', 'np1', 'np2')


def P(x, y):
    return (x + OX, y + OY)


def roll(c, m, ramp=FL, sd=3, warts=(), glint=None, folds=()):
    darken(c, sh(m, -1, 2) & ~m & (c.a > 0))           # Schlagschatten der Wulst auf das Darunterliegende
    p = C()
    p.form(m, ramp, sd=sd, hl=1)
    for pts in folds:
        p.line(pts, 'np1', only=erode(m, 1))
    for (x, y) in warts:
        p.pxs([(x, y), (x + 1, y)], 'np1')
        p.pxs([(x, y - 1)], 'np3')
    if glint:
        p.pxs(glint, 'np4')
    c.stamp(p, 'np0')


def draw(sq=1.0, bob=0, sway=0, ll=0, rl=0, arm=0, mouth=0, lift=0):
    setsize(CW, CH)
    c = C()
    st = 1 / sq                         # Breite gegenläufig zur Höhe (Volumen bleibt)

    def B(x, y, k=1.0):                 # k: wie stark ein Punkt mitschwankt/gestaucht wird
        yy = 72 - (72 - y) * sq
        return P(x + sway * k, yy + bob - lift)

    # ---- fernes Bein + ferner Stummelarm
    p = C()
    p.form(L(*P(52 + rl, 62 - lift), 5.6, *P(53 + rl, 70 - lift - max(0, rl) * 0.4), 5.0), FLD, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    p.form(E(*B(58, 40, 0.6), 4.0, 5.0), FLD, sd=1, hl=0)
    c.stamp(p, 'K')
    # ---- nahes Bein (Elefantenbein mit Zehen)
    p = C()
    lg = L(*P(30 + ll, 63 - lift), 6.4, *P(29 + ll, 69 - lift - max(0, ll) * 0.4), 5.8)
    p.form(lg, FL, sd=2, hl=1)
    fy = 70 - lift - max(0, ll) * 0.4
    for k in range(3):
        p.form(E(*P(24 + ll + k * 3.2, fy + 1), 1.8, 1.4), FL, sd=1, hl=1)
        c.stamp(p, 'np0')
    # ---- Bauchwulst (unterster, breitester)
    belly = E(*B(38, 56, 0.3), 23 * st, 11 * sq)
    roll(c, belly, sd=4, warts=[tuple(int(v) for v in B(48, 60, 0.3)), tuple(int(v) for v in B(26, 64, 0.3))],
         folds=[[B(30, 62, 0.3), B(36, 64, 0.3), B(44, 63, 0.3)], [B(38, 57, 0.3), B(40, 58, 0.3)]],
         glint=[B(24, 54, 0.3)])
    # Nabel
    p = C(); p.pxs([B(35, 60, 0.3), B(36, 60, 0.3)], 'np0'); p.pxs([B(35, 59, 0.3)], 'np1'); c.stamp(p, 'np0')
    # ---- Brustwulst (hängt über den Bauch)
    chest = E(*B(37, 43, 0.7), 18 * st, 9.4 * sq)
    roll(c, chest, sd=3, warts=[tuple(int(v) for v in B(46, 42, 0.7))],
         folds=[[B(44, 40, 0.7), B(47, 46, 0.7)]], glint=[B(25, 38, 0.7), B(26, 38, 0.7)])
    # ---- Kopfwulst mit Gesicht, sitzt nach vorn gebeugt
    head = E(*B(30, 27, 1.0), 12 * st, 10 * sq) | E(*B(34, 19, 1.0), 7 * st, 4 * sq)
    chin = E(*B(26, 36, 1.0), 9 * st, 4 * sq)
    roll(c, chin, sd=2, folds=[[B(20, 37, 1.0), B(28, 39, 1.0)]])
    roll(c, head, sd=3, warts=[tuple(int(v) for v in B(38, 23, 1.0)), tuple(int(v) for v in B(36, 33, 1.0))],
         folds=[[B(28, 18, 1.0), B(38, 18, 1.0)], [B(40, 28, 1.0), B(41, 32, 1.0)]],
         glint=[B(24, 19, 1.0), B(25, 18, 1.0)])
    # Gesicht
    p = C()
    for (ex, ey) in ((21, 26), (29, 25)):
        p.fill(E(*B(ex, ey + 0.5, 1.0), 2.4, 1.4), 'np1')                              # Augenhöhle
        p.fill(R(*B(ex - 1, ey, 1.0), *B(ex + 1, ey, 1.0)), 'K')                         # verschwollener Schlitz
        p.pxs([B(ex - 1, ey, 1.0)], 'e1')
        p.line([B(ex - 2, ey + 2, 1.0), B(ex + 1.5, ey + 2, 1.0)], 'np3')                # Tränensack
    p.pxs([B(22, 30, 1.0), B(25, 30, 1.0)], 'np0')                                     # Nasenlöcher
    p.line([B(21, 29, 1.0), B(26, 29, 1.0)], 'np3')
    mo = E(*B(23, 33.5 + mouth * 0.5, 1.0), 4.4, 1.0 + mouth)
    p.fill(mo, 'q')
    p.line([B(19, 35 + mouth, 1.0), B(27, 35 + mouth, 1.0)], 'np2')                     # hängende Unterlippe
    p.pxs([B(21, 36 + mouth, 1.0), B(22, 36 + mouth, 1.0)], 'np1')
    p.pxs([B(25, 35 + mouth, 1.0)], 'np4')                                             # Speichelglanz
    c.stamp(p, 'np0')
    # ---- naher Stummelarm mit Fingerwülsten
    p = C()
    sh_ = B(26, 42, 0.7)
    hd = (sh_[0] - 6 + arm, sh_[1] + 8 - arm * 1.5)
    a_ = L(*sh_, 4.6, *hd, 3.4)
    p.form(a_, FL, sd=2, hl=1)
    for k in range(3):
        p.form(E(hd[0] - 2 + k * 2, hd[1] + 3, 1.3, 1.6), FL, sd=1, hl=1)
    p.line([(sh_[0] - 2, sh_[1] + 3), (sh_[0] + 1, sh_[1] + 4)], 'np1', only=a_)
    c.stamp(p, 'np0')
    # ---- Fliegen
    p = C()
    for (fx, fy) in ((10 + sway, 14 - bob), (54 - sway, 8 + bob)):
        p.pxs([P(fx, fy), P(fx + 1, fy)], 'K')
        p.pxs([P(fx, fy - 1)], 'v1')
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(sway=-1, ll=-2, rl=2), dict(sq=0.95, bob=1, rl=0, ll=0, arm=1),
        dict(sway=1, ll=2, rl=-2), dict(sq=0.95, bob=1, arm=-1)]
ATTACK = [dict(sq=1.12, lift=2, arm=4, mouth=1), dict(sq=0.84, sway=-2, mouth=2, arm=-2), dict(sq=0.92, mouth=1)]

if __name__ == '__main__':
    export('nuppeppo', draw, WALK, ATTACK)
