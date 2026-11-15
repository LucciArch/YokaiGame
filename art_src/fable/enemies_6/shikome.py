"""Yomotsu-shikome – die Schreckensweiber von Yomi. Komplett neu (Runde 99): ausgezehrte Leiche mit
bläulich-violetter Haut, zerrissenes weißes Totengewand, strähniges schwarzes Haar, lange Arme mit Krallen.
Läuft geduckt vorgebeugt. Blick nach links. Angriff: Sprung mit beiden Klauen voran."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 112, 88
OX, OY = 34, 8                          # lokale Grundlinie y = 76
col('d0', '#1c1230'); col('d1', '#3e2a5a'); col('d2', '#6a5488'); col('d3', '#9c88b4'); col('d4', '#c8b8dc')   # Leichenhaut
add_rim('d0 d1 d2', 'xu')
SKIN = ('d1', 'd2', 'd3')
SKINF = ('d0', 'd1', 'd2')
ROBE = ('v0', 'v1', 'v2')               # schmutzig-weißes Totengewand
HAIR = ('h0', 'hb', 'h2')
col('hb', '#1a1738')

LEG = dict(zip('abcdeKrYqWmnoz', ['d0', 'd1', 'd2', 'd3', 'd4', 'K', 'e1', 'y3', 'q', 'b3', 'h0', 'hb', 'h2', 'v1']))
# hohle Wangen, tiefe Augenhöhlen mit rotem Glühen, breiter Kiefer voller spitzer Zähne, nasse Strähnen übers Gesicht
HEAD = """
.......mmmmmmmmm.....
.....mmnnnonnnnnmm...
....mnnoonnnnonnnnm..
...mnnonnnnnonnnnnnm.
..mnnnndddnnnnmnnnnm.
..mnnddeeddnnnnmnnnnm
.mnmddeddddbnnnmnmnnm
.mnmdKKKdcKKKnmnnmnnm
.mncKKrYKcKrKbnmnnmnm
.mndKKKKccKKKbbnmnmnm
.mncdddcccbbbaanmnnm.
.mKdddccbcbbaaamnmnm.
mKdeddccbbbaaaanmnm..
mKddccKKKKKKKaamnm...
.mccKWqWqWqWqKamnm...
..mcKqqqqqqqqKamm....
..mcKWqWqWqWqKam.....
...mcKKKKKKKKam......
....mccbbbbaaam......
.....maaaaaaam.......
"""
CLAW = """
cc.....
cddc...
.cddcc.
.cdddcb
..bccbb
.Kb.Kb.
K..K...
"""


def P(x, y):
    return (x + OX, y + OY)


def ik(a, c_, l1, l2, side=1):
    dx, dy = c_[0] - a[0], c_[1] - a[1]
    d = max(0.01, min(math.hypot(dx, dy), l1 + l2 - 0.01))
    t = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - t * t))
    ux, uy = dx / d, dy / d
    return (a[0] + ux * t - uy * h * side, a[1] + uy * t + ux * h * side)


DEF = dict(bob=0, lean=0, ff=40, nf=26, flift=0, nlift=0,
           nhd=(6, 40), fhd=(14, 46), hair=0)


def leg(c, hip, foot, ramp, lift):
    knee = ik(hip, foot, 12, 12, side=1)                     # Knie zeigt nach vorn (links)
    p = C()
    th = L(*hip, 2.9, *knee, 2.3)
    sh_ = L(*knee, 2.4, *foot, 1.8)
    p.form(th | sh_, ramp, sd=1, hl=1)
    p.form(E(knee[0], knee[1], 2.4, 2.2), ramp, sd=0, hl=1)
    fx, fy = foot
    ft = PG([(fx + 2, fy - 1), (fx + 2, fy + 2), (fx - 6, fy + 2), (fx - 7, fy), (fx - 3, fy - 2)])
    p.form(ft, ramp, sd=1, hl=1)
    for t in range(3):
        p.pxs([(fx - 7 + t * 2, fy + 2)], 'b2')
    c.stamp(p, 'K')


def arm(c, sh_, hd, ramp, lg):
    el = ik(sh_, hd, 13, 12, side=-1)                        # Ellbogen nach hinten-unten
    p = C()
    p.form(L(*sh_, 3.0, *el, 2.2) | L(*el, 2.2, *hd, 1.8), ramp, sd=1, hl=1)
    p.form(E(el[0], el[1], 2.4, 2.2), ramp, sd=0, hl=1)
    c.stamp(p, 'K')
    p = C(); p.grid(int(hd[0]) - 2, int(hd[1]) - 3, CLAW, lg); c.stamp(p, 'K')


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    hs = S['hair']
    hip = B((40, 46))
    # ---- ferner Arm und fernes Bein
    arm(c, B((28, 30)), B(S['fhd']), SKINF, dict(LEG, c='d1', d='d2', b='d0'))
    leg(c, B((42, 48)), P(S['ff'], 74 - S['flift']), SKINF, S['flift'])
    # ---- Strähnenhaar hinten: lang, nass, über den Rücken
    p = C()
    p = C()
    c.stamp(p, 'K')
    # ---- Totengewand: Oberkörper weit vorgebeugt, zerrissene Fetzen
    p = C()
    torso = PG([B((22, 26)), B((32, 20)), B((44, 28)), B((50, 40)), B((51, 54)), B((47, 60)), B((43, 55)),
                B((39, 62)), B((35, 56)), B((31, 61)), B((28, 52)), B((28, 44)), B((24, 34))])
    p.form(torso, ROBE, sd=4, hl=1)
    for (a_, b_) in (((30, 26), (34, 50)), ((40, 30), (44, 50))):
        p.line([B(a_), B(b_)], 'v0', only=torso)
    p.line([B((24, 27)), B((33, 40))], 'v0', only=torso)                     # Kragen links über rechts (Totengewand)
    for (x, y, rx, ry) in ((44, 44, 3.4, 2.2), (34, 48, 2.6, 2.0), (46, 34, 2.2, 1.6)):     # Erd- und Moderflecken
        p.fill(E(*B((x, y)), rx, ry) & torso, 'v0')
        p.fill(E(*B((x - 1, y - 0.5)), rx * 0.5, ry * 0.5) & torso, 's1')
    for (x, y) in ((40, 40), (36, 30)):                                          # Risse
        p.line([B((x, y)), B((x + 2, y + 2)), B((x + 1, y + 4))], 'K', only=torso)
    p.form(PG([B((26, 34)), B((32, 37)), B((31, 44))]) & torso, SKIN, sd=1, hl=0)   # Haut durch den Riss
    p.pxs([B((28, 37)), B((29, 39))], 'd0')
    rib = PG([B((24, 27)), B((30, 24)), B((32, 34))]) & torso
    p.form(rib, SKIN, sd=1, hl=0)                                             # eingefallene Brust im Ausschnitt
    p.line([B((26, 29)), B((29, 28))], 'd0'); p.line([B((27, 31)), B((30, 30))], 'd0')
    c.stamp(p, 'K')
    import random as _r
    rg = _r.Random(5)
    for i in range(10):
        t = i / 9
        root = (16 + t * 20, 12 + t * 6)
        ln = 22 + rg.uniform(0, 12) - t * 4
        ang = math.radians(100 - t * 40 + rg.uniform(-8, 8))
        wob = rg.choice((-1, 1)) * rg.uniform(1.5, 3.5)
        Q = [B((root[0] + math.cos(ang) * ln * f + math.sin(f * 4) * wob + hs * f, root[1] + math.sin(ang) * ln * f)) for f in (0, 0.35, 0.7, 1)]
        q = C()
        r_ = 3.4 - (i % 3) * 0.4
        lock = L(*Q[0], r_, *Q[1], r_ * 0.9) | L(*Q[1], r_ * 0.9, *Q[2], r_ * 0.6) | L(*Q[2], r_ * 0.6, *Q[3], 0.7)
        q.form(lock, HAIR, sd=1, hl=1)
        q.line([lerp(Q[0], Q[1], 0.3), Q[1], lerp(Q[1], Q[2], 0.6)], 'h2' if i % 2 else 'h0', only=erode(lock, 1))
        c.stamp(q, 'K')
    # ---- nahes Bein (Laufschritt)
    leg(c, B((36, 50)), P(S['nf'], 74 - S['nlift']), SKIN, S['nlift'])
    # ---- Kopf weit vorn, tief gesenkt
    p = C()
    p.grid(*B((6, 12)), HEAD, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # ---- naher Arm mit Klaue voran, weiter zerrissener Ärmel
    arm(c, B((26, 32)), B(S['nhd']), SKIN, LEG)
    sh_ = B((26, 32)); el = ik(sh_, B(S['nhd']), 13, 12, side=-1)
    p = C()
    sl = L(*sh_, 4.6, *lerp(sh_, el, 0.8), 4.0) | PG([lerp(sh_, el, 0.3), lerp(sh_, el, 0.9), (el[0] + 2, el[1] + 7), (el[0] + 5, el[1] + 4),
                                                    (el[0] + 7, el[1] + 8), (sh_[0] + 3, sh_[1] + 6)])
    p.form(sl, ROBE, sd=2, hl=1)
    p.line([lerp(sh_, el, 0.2), (el[0] + 3, el[1] + 5)], 'v0', only=sl)
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(nf=22, ff=44, nhd=(4, 42), fhd=(16, 44)),
        dict(bob=-2, nf=30, ff=38, nlift=3, nhd=(8, 38), fhd=(12, 46), hair=1),
        dict(nf=40, ff=26, nhd=(10, 44), fhd=(6, 40)),
        dict(bob=-2, nf=34, ff=32, flift=3, nhd=(8, 40), fhd=(10, 44), hair=-1)]
ATTACK = [dict(lean=4, bob=3, nf=28, ff=42, nhd=(18, 26), fhd=(22, 28), hair=2),                  # duckt sich
          dict(lean=-8, bob=-6, nf=36, ff=50, flift=4, nlift=6, nhd=(-6, 34), fhd=(-2, 40), hair=-3),  # Sprung, Klauen vorn
          dict(lean=-4, bob=0, nf=24, ff=42, nhd=(2, 44), fhd=(10, 46))]

if __name__ == '__main__':
    export('shikome', draw, WALK, ATTACK)
