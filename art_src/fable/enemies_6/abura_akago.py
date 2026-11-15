"""Abura-akago – Geisterkind, das nachts das Lampenöl aufleckt. Komplett neu (Runde 105): krabbelndes Kleinkind
in richtiger Anatomie (Kopf etwa ein Drittel der Körperlänge, Speckfalten an Hand- und Fußgelenken, Knie auf dem
Boden, Fußsohlen nach oben), fahle Geisterhaut, rotes Bauchlätzchen (haragake), Haarbüschel am Scheitel.
Leckt mit langer Zunge aus einer Öllampenschale; über dem Rücken schwebt ein Irrlicht.
Angriff: richtet sich auf, das Irrlicht lodert, spuckt Feuer."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 80, 72
OX, OY = 8, 14                     # lokale Grundlinie y = 52
col('ab0', '#2e2644'); col('ab1', '#7a6a8e'); col('ab2', '#c0aec0'); col('ab3', '#ece0e2')
add_rim('ab0 ab1 ab2', 'ab3'); DARK.update(ab3='ab2', ab2='ab1', ab1='ab0')
SK = ('ab1', 'ab2', 'ab3')
SKF = ('ab0', 'ab1', 'ab2')


def P(x, y):
    return (x + OX, y + OY)


def limb(c, pts, rs, ramp, crease=True):
    p = C()
    m = None
    for (a, b), (ra, rb) in zip(zip(pts, pts[1:]), zip(rs, rs[1:])):
        s_ = L(*a, ra, *b, rb)
        m = s_ if m is None else m | s_
    p.form(m, ramp, sd=2, hl=1)
    if crease:
        for j in pts[1:-1]:
            p.pxs([(j[0], j[1] + 1), (j[0] + 1, j[1] + 1)], ramp[0])
    c.stamp(p, 'K')
    return m


def draw(bob=0, rise=0, ha=0, hb=0, tongue=1, flare=0, mouth=0, fl=0):
    setsize(CW, CH)
    c = C()

    def B(x, y):
        return P(x, y + bob)
    hx, hy = 18 + rise * 0.6, 28 - rise * 1.6
    # ---- Irrlicht hinter dem Rücken
    flame(c, [B(44, 16 + fl)], [(B(44, 16 + fl), B(42 - flare, 2 - flare * 3 + fl), 4.4 + flare * 0.6),
                                 (B(44, 16 + fl), B(48, 6 - flare * 2 + fl), 3.0)], w=4.4)
    # ---- Öllampenschale
    p = C()
    dish = E(*P(6, 50), 6.4, 2.2)
    p.form(dish, ('w0', 'w1', 'w2'), sd=1, hl=1)
    p.fill(E(*P(6, 49), 4.6, 1.0), 'y0')                               # Öl
    p.pxs([P(4, 49), P(5, 49)], 'y2')
    p.line([P(9, 49), P(12, 47)], 'v2')                                # Docht
    c.stamp(p, 'K')
    # ---- ferne Gliedmaßen
    limb(c, [B(32 - rise * 0.3, 34 - rise), B(30 - ha, 42 - rise * 0.5), B(28 - ha, 50 - rise * 0.8)], [3.4, 2.8, 2.4], SKF)
    limb(c, [B(48, 38), B(46 + hb, 49), B(58 + hb, 49)], [4.4, 3.4, 2.4], SKF)
    # ---- Rumpf: rundlicher Babybauch, Po höher als Schultern
    p = C()
    tor = E(*B(36, 38 - rise * 0.6), 10.4, 7.4) | E(*B(47, 36 - rise * 0.2), 7.4, 7.4)
    p.form(tor, SK, sd=3, hl=1)
    bib = PG([B(27, 34 - rise), B(33, 33 - rise), B(40, 44 - rise * 0.5), B(34, 47 - rise * 0.5), B(28, 45 - rise)]) & sh(tor, 0, 1)
    p.form(bib, ('m1', 'm2', 'm3'), sd=1, hl=1)
    p.line([B(28, 36 - rise), B(34, 35 - rise)], 'y1', only=bib)       # Goldborte
    p.fill(E(*B(34, 41 - rise * 0.7), 1.6, 1.6) & bib, 'y1')            # Glückssymbol
    p.pxs([B(48, 33)], 'ab1')                                           # Grübchen am Po
    c.stamp(p, 'K')
    # ---- nahes Bein: Knie am Boden, Fußsohle nach oben
    lg = limb(c, [B(46, 39), B(42 + hb, 50), B(54 + hb, 50)], [5.0, 3.8, 2.6], SK)
    p = C()
    sole = E(*B(56 + hb, 48), 2.8, 2.2)
    p.form(sole, SK, sd=1, hl=1)
    for k in range(3):
        p.pxs([B(58 + hb, 46 + k * 1.2)], 'ab1')
    c.stamp(p, 'K')
    # ---- Kopf: groß, Hinterkopf rund, Pausbacken
    p = C()
    head = E(*B(hx, hy), 10.4, 9.4)
    cheek = E(*B(hx - 4, hy + 4), 5.4, 4.4)
    p.form(head | cheek, SK, sd=3, hl=1)
    p.pxs([B(hx - 9, hy + 1)], 'ab1')                                   # Stupsnase
    p.pxs([B(hx - 10, hy + 1)], 'ab3')
    # Auge: dunkle Höhle mit fahlem Glimmen
    p.fill(E(*B(hx - 5, hy - 1.5), 2.8, 2.4), 'ab1')                    # Augenringe
    p.fill(E(*B(hx - 5, hy - 2), 2.0, 1.8), 'K')
    p.pxs([B(hx - 5.5, hy - 2.5), B(hx - 4.5, hy - 2.5)], 'a2')
    p.line([B(hx - 8, hy - 5), B(hx - 3, hy - 5.5)], 'ab1')            # Brauenbogen
    p.line([B(hx + 3, hy - 1), B(hx + 4, hy + 2), B(hx + 3, hy + 3)], 'ab1')   # Ohr
    # Mund + Zunge
    mo = E(*B(hx - 7, hy + 5 + mouth * 0.5), 2.2 + mouth * 0.6, 1.4 + mouth * 0.8)
    p.fill(mo, 'q')
    c.stamp(p, 'K')
    if tongue:
        p = C()
        tx, ty = B(hx - 8, hy + 6)
        tp = (P(9, 48)[0], P(9, 48)[1]) if not rise else (tx - 5, ty + 2)
        p.form(L(tx, ty, 1.4, *tp, 0.9), ('m1', 'm2', 'm3'), sd=0, hl=1)
        c.stamp(p, 'K')
    # Haarbüschel am Scheitel
    p = C()
    tuft = L(*B(hx + 1, hy - 9), 2.2, *B(hx - 1, hy - 13), 0.8) | E(*B(hx + 1, hy - 9), 3.0, 1.6)
    p.form(tuft, ('h0', 'hb', 'h2') if 'hb' in px.IDX else ('h0', 'h1', 'h2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # ---- naher Arm: auf die Hand gestützt, Speckfalte am Handgelenk
    limb(c, [B(31 - rise * 0.3, 36 - rise), B(27 + ha, 43 - rise * 0.5), B(24 + ha, 50 - rise * 0.8)], [4.0, 3.2, 2.8], SK)
    p = C()
    hand = E(*B(22 + ha, 50 - rise * 0.8), 3.0, 1.8)
    p.form(hand, SK, sd=1, hl=1)
    p.pxs([B(20 + ha, 51 - rise * 0.8), B(22 + ha, 51 - rise * 0.8)], 'ab1')
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(ha=-2, hb=2), dict(bob=-1, ha=0, hb=0, fl=-1), dict(ha=2, hb=-2), dict(bob=-1, fl=1)]
ATTACK = [dict(rise=3, tongue=0, mouth=1, flare=2), dict(rise=5, tongue=0, mouth=3, flare=4), dict(rise=2, tongue=0, mouth=2, flare=1)]

if __name__ == '__main__':
    export('abura_akago', draw, WALK, ATTACK)
