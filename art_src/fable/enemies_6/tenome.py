"""Tenome – der blinde Alte mit den Augen in den Handflächen. Komplett neu (Runde 99): hagerer, kahler Greis
in zerschlissenem grauem Kimono, leere geschlossene Augenhöhlen, beide Arme nach vorn gestreckt, in jeder
Handfläche ein großes, starrendes Auge. Blick nach links. Angriff: reißt die Hände hoch, die Augen feuern."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

col('j0', '#1e1c34'); col('j1', '#3c3c5a'); col('j2', '#66688a'); col('j3', '#9a9eb8')      # graue Mönchskutte
col('l0', '#2a2440'); col('l1', '#6e5a62'); col('l2', '#a89080'); col('l3', '#d8c8a8')      # leichenblasse alte Haut
add_rim('j0 j1 j2', 'xz'); add_rim('l0 l1 l2', 'xs')
CW, CH = 112, 92
OX, OY = 34, 8                         # lokale Grundlinie y = 80
SKIN = ('l1', 'l2', 'l3')
SKINF = ('l0', 'l1', 'l2')
ROBE = ('j1', 'j2', 'j3')
ROBEF = ('j0', 'j1', 'j2')

LEG = dict(zip('abcdKqWhg', ['l0', 'l1', 'l2', 'l3', 'K', 'q', 'b3', 'v2', 'v1']))
# kahler Schädel, eingefallene Wangen, zugenähte/geschlossene Lider, schütterer weißer Bart
HEAD = """
.......bbbbbb.......
.....bcddddccbb.....
....bcddddcccccb....
...bcdddccccccccb...
...cddcccccccccccb..
..bcdccccccccccccbh.
..cccbbbcccccccccbhh
.bcbaaaabccccbabcbhh
.bcKcKcKbcccbcbabbbh
..cbaaabcccccbcbbbbh
.ddcbbbcccccccbbbbh.
dddccccbbbcccbbbbbh.
.cccbccbbaabccccbb..
..bbcccbaabcccccbb..
..aKKKbcbbbccccbb...
..hbbbbbbbbbbcbb....
..hhhbbbbbbbbbb.....
..hhhhhgbbbb........
...hhhhgg...........
....hhgg............
.....hg.............
"""
# Handfläche nach vorn: vier knochige Finger mit Knöcheln, Daumen seitlich, mandelförmiges Auge mit Lidern
PALM = """
..c..c..c.......
.cd.cd.cd.......
.cd.cd.cd..c....
.cb.cb.cb.cd....
.cd.cd.cd.cd....
.cd.cd.cd.cb....
.cdccdccdccd....
cddddddddddddc..
cdaKKKKKKKadcc..
cdKWWWeeWWWKdcd.
cKWWWeEEeWWWKcd.
cKWWeEZYEeWWKcb.
cKWWWeEEeWWWKb..
cdKWWWeeWWWKdb..
cddaKKKKKKaddb..
.cddddddddddb...
..cbbbbbbbbb....
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


DEF = dict(bob=0, lean=0, ff=36, nf=24, flift=0, nlift=0, nhd=(2, 36), fhd=(10, 31), glow=0)


def arm(c, sh_, hd, ramp, robe, glow, far=False):
    el = ik(sh_, hd, 12, 11, side=-1)
    p = C()
    sl = L(*sh_, 4.4, *el, 3.8) | PG([el, (el[0] + 4, el[1] + 7), (el[0] + 8, el[1] + 4), sh_])
    p.form(sl, robe, sd=2, hl=1)                                          # weiter Ärmel bis zum Ellbogen
    c.stamp(p, 'K')
    p = C()
    p.form(L(*el, 2.2, *hd, 1.8), ramp, sd=1, hl=1)                        # dürrer Unterarm
    c.stamp(p, 'K')
    lg = dict(LEG, c=ramp[1], d=ramp[2], b=ramp[0], a=ramp[0], e='e0', E='e1' if glow else 'e0', Z='y3', Y='K')
    p = C(); p.grid(int(hd[0]) - 7, int(hd[1]) - 11, PALM, lg); c.stamp(p, 'K')


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    # ---- ferner Arm
    arm(c, B((26, 28)), B(S['fhd']), SKINF, ROBEF, S['glow'], far=True)
    # ---- Beine und Füße (bloß, knochig)
    for fx, lift, ramp in ((S['ff'], S['flift'], SKINF), (S['nf'], S['nlift'], SKIN)):
        p = C()
        kx, ky = P(fx + 4, 66 - lift)
        ax, ay = P(fx + 2, 77 - lift)
        p.form(L(kx, ky, 2.4, ax, ay, 1.8), ramp, sd=1, hl=1)
        ft = PG([(ax + 2, ay - 1), (ax + 2, ay + 3), (ax - 6, ay + 3), (ax - 7, ay + 1), (ax - 3, ay - 1)])
        p.form(ft, ramp, sd=1, hl=1)
        c.stamp(p, 'K')
    # ---- Kimono: hager, gerade, zerschlissener Saum, Strick als Gürtel
    p = C()
    robe = PG([B((24, 24)), B((34, 22)), B((40, 30)), B((42, 50)), B((44, 66)), B((40, 70)), B((36, 66)), B((32, 71)),
               B((27, 67)), B((22, 70)), B((20, 64)), B((22, 46)), B((20, 32))])
    p.form(robe, ROBE, sd=4, hl=1)
    for (a_, b_) in (((30, 30), (28, 66)), ((36, 34), (38, 66)), ((24, 50), (23, 64))):
        p.line([B(a_), B(b_)], 'j0', only=robe)
    p.form(PG([B((21, 44)), B((41, 42)), B((41, 46)), B((21, 48))]) & robe, ('w0', 'w1', 'w2'), sd=1, hl=1)
    p.line([B((24, 24)), B((31, 38))], 'j0', only=robe)                   # Kragen
    neck = PG([B((24, 24)), B((30, 23)), B((29, 30))]) & robe
    p.form(neck, SKIN, sd=1, hl=0)
    for k in range(9):                                                     # Gebetskette
        t = k / 8
        q = B((24 + t * 8 + math.sin(t * 3.1) * -3, 25 + t * 14))
        p.form(E(q[0], q[1], 1.3, 1.3), ('w0', 'w1', 'w2'), sd=0, hl=1)
    p.form(E(*B((30, 41)), 1.6, 2.2), ('m1', 'm2', 'm3'), sd=0, hl=1)       # Quaste
    c.stamp(p, 'K')
    # ---- Hals (sehnig), dann Kopf leicht vorgereckt
    p = C()
    p.form(L(*B((25, 22)), 3.0, *B((22, 16)), 2.8), SKIN, sd=1, hl=0)
    p.line([B((24, 22)), B((22, 17))], 'l1')
    c.stamp(p, 'K')
    p = C()
    p.grid(*B((9, 3)), HEAD, LEG)
    c.stamp(p, 'K')
    # ---- naher Arm
    arm(c, B((28, 30)), B(S['nhd']), SKIN, ROBE, S['glow'])
    c.blacken()
    return c


WALK = [dict(nf=22, ff=36), dict(bob=-1, nf=28, ff=32, nlift=2, nhd=(3, 37), fhd=(11, 32)),
        dict(nf=34, ff=24), dict(bob=-1, nf=28, ff=30, flift=2, nhd=(1, 35), fhd=(9, 30))]
ATTACK = [dict(lean=3, bob=1, nhd=(8, 22), fhd=(16, 18)),                     # hebt die Hände vors Gesicht
          dict(lean=-3, nhd=(-4, 30), fhd=(2, 25), glow=1),                     # stößt sie vor, Augen glühen
          dict(lean=-1, nhd=(0, 34), fhd=(8, 29))]

if __name__ == '__main__':
    export('tenome', draw, WALK, ATTACK)
