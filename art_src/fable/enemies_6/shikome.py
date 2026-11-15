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
col('d0', '#1c1230'); col('d1', '#3e2a5a'); col('d2', '#6a5488'); col('d3', '#9c88b4')   # Leichenhaut
add_rim('d0 d1 d2', 'xu')
SKIN = ('d1', 'd2', 'd3')
SKINF = ('d0', 'd1', 'd2')
ROBE = ('v0', 'v1', 'v2')               # schmutzig-weißes Totengewand
HAIR = ('h0', 'hb', 'h2')
col('hb', '#1a1738')

LEG = dict(zip('abcdKeYqWmno', ['d0', 'd1', 'd2', 'd3', 'K', 'e1', 'y3', 'q', 'b3', 'h0', 'hb', 'h2']))
HEAD = """
......mmmmmmm.....
....mmnnnnonnmm...
...mnnnoonnnnnnm..
..mnnnnnnnnnnnnnm.
..mnncddbnnnnnnnm.
.mnncddddbnnnmnnnm
.mnmKKKdcKKnnmnmnm
.mncdeYKcKebnnmnnm
.mncdKKccKKbnmnnnm
.mnKdddccbbaannmnm
.mKdddcccbbaanmnm.
.mKddcbbbbaaanmnm.
..mcKKKKKKKaamnm..
..mKWqWqWqWKaanm..
...KqqqqqqqKaam...
...cKWqWqWKbam....
....cKKKKKbbam....
.....cbbbbaam.....
......aaaa........
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
    th = L(*hip, 3.6, *knee, 2.6)
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
    hair = E(*B((28, 18)), 10, 8)
    strands = [((22, 14), (40 + hs, 40), 4.0), ((28, 12), (50 + hs, 36), 4.4), ((34, 14), (56 + hs, 30), 3.6),
               ((30, 16), (46 + hs, 46), 3.4), ((36, 18), (58 + hs, 42), 3.0), ((26, 18), (34 + hs, 44), 3.0)]
    for (a_, b_, r_) in strands:                                          # einzelne nasse Strähnen mit Spitzen
        a2, b2 = B(a_), B(b_)
        m_ = lerp(a2, b2, 0.55)
        m_ = (m_[0] + 2, m_[1] - 2)
        hair |= L(*a2, r_, *m_, r_ * 0.75) | L(*m_, r_ * 0.75, *b2, 0.6)
    p.form(hair, HAIR, sd=2, hl=1)
    for (a_, b_, r_) in strands[:3]:
        p.line([B((a_[0] + 3, a_[1] + 1)), B(((a_[0] + b_[0]) / 2 + 3, (a_[1] + b_[1]) / 2 - 1))], 'h2', only=hair)
    c.stamp(p, 'K')
    # ---- Totengewand: Oberkörper weit vorgebeugt, zerrissene Fetzen
    p = C()
    torso = PG([B((22, 26)), B((32, 20)), B((44, 28)), B((50, 40)), B((50, 52)), B((46, 56)), B((42, 52)),
                B((38, 58)), B((34, 52)), B((30, 56)), B((30, 44)), B((24, 34))])
    p.form(torso, ROBE, sd=4, hl=1)
    for (a_, b_) in (((30, 26), (34, 50)), ((40, 30), (44, 50))):
        p.line([B(a_), B(b_)], 'v0', only=torso)
    p.line([B((24, 27)), B((33, 40))], 'v0', only=torso)                     # Kragen links über rechts (Totengewand)
    rib = PG([B((24, 27)), B((30, 24)), B((32, 34))]) & torso
    p.form(rib, SKIN, sd=1, hl=0)                                             # eingefallene Brust im Ausschnitt
    p.line([B((26, 29)), B((29, 28))], 'd0'); p.line([B((27, 31)), B((30, 30))], 'd0')
    c.stamp(p, 'K')
    # ---- nahes Bein (Laufschritt)
    leg(c, B((36, 50)), P(S['nf'], 74 - S['nlift']), SKIN, S['nlift'])
    # ---- Kopf weit vorn, tief gesenkt
    p = C()
    p.grid(*B((8, 14)), HEAD, LEG)
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
