"""Zashiki-warashi – Hausgeist in Kindergestalt. Komplett neu (Runde 100): kleines Mädchen (~5 Jahre) mit
Pagenkopf (okappa), rotem Kimono mit Asanoha-Muster, weißem Kragen, Obi mit Schleife am Rücken, Holzsandalen.
Hält einen Temari-Ball. Blasses Gesicht, große dunkle Augen – verspielt, aber unheimlich. Blick nach links.
Angriff: hebt den Ball über den Kopf und wirft."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 72, 64
OX, OY = 18, 6                          # lokale Grundlinie y = 54
col('hb', '#1a1738')
KIM = ('m1', 'm2', 'm3')
KIMF = ('m0', 'm1', 'm2')
SKIN = ('k1', 'k2', 'k3')

LEG = dict(zip('abcdmnoKWeEp', ['k0', 'k1', 'k2', 'k3', 'h0', 'hb', 'h2', 'K', 'v3', 'a1', 'n2', 'm3']))
# Pagenkopf: gerader Pony knapp über den Augen, Seiten bis zum Kinn; Gesicht im Dreiviertelprofil nach links
HEAD = """
.....mmmmmmm....
...mmnnoonnnnm..
..mnnoonnnnnnnm.
.mnnonnnnnnnnnnm
.mnonnnnnnnnnnnm
mnnnnnnnnnnnnnnm
mnmmmmmmmmnnnnnm
mmdddddcccmnnnnm
.cdKKdccKKbmnnnm
.cdKWdccKWbmnnnm
.cdKKdccKKbmnnnm
.cpddcccccbmnnnm
..cdccccbbbmnnm.
..ccdKKcbbamnnm.
...cccccbbamnm..
....bbbbaa.mm...
"""
HAND = """
.cc.
cddb
cccb
.bb.
"""


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, ff=22, nf=30, flift=0, nlift=0, hd=(12, 34), ball=(6, 32), hold=True)


def temari(c, q):
    p = C()
    m = E(q[0], q[1], 4.6, 4.6)
    p.form(m, ('n1', 'n2', 'n3'), sd=1, hl=1)
    p.line([(q[0] - 4, q[1]), (q[0] + 4, q[1])], 'y2', only=m)                     # Stickfäden
    p.line([(q[0], q[1] - 4), (q[0], q[1] + 4)], 'm2', only=m)
    p.line([(q[0] - 3, q[1] - 3), (q[0] + 3, q[1] + 3)], 'v3', only=m)
    p.line([(q[0] - 3, q[1] + 3), (q[0] + 3, q[1] - 3)], 'y1', only=m)
    p.pxs([(int(q[0]) - 2, int(q[1]) - 3)], 'v3')
    c.stamp(p, 'K')


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    # ---- Obi-Schleife am Rücken
    p = C()
    bow = E(*B((35, 29)), 3.0, 2.2) | E(*B((35, 34)), 2.2, 2.6) | E(*B((34, 31.5)), 1.4, 1.4)
    p.form(bow, ('y0', 'y1', 'y2'), sd=1, hl=1)
    p.pxs([B((34, 31))], 'y0')
    c.stamp(p, 'K')
    # ---- Beine mit weißen Tabi-Socken und Holzsandalen
    for fx, lift, far in ((S['ff'], S['flift'], True), (S['nf'], S['nlift'], False)):
        p = C()
        x0, y0 = P(fx, 50 - lift)
        p.form(L(x0 + 3, y0 - 6, 1.9, x0 + 3, y0, 1.7), ('k0', 'k1', 'k2') if far else SKIN, sd=1, hl=1)
        p.form(R(x0, y0, x0 + 5, y0 + 2), ('v1', 'v2', 'v3') if not far else ('v0', 'v1', 'v2'), sd=1, hl=1)
        p.form(R(x0 - 1, y0 + 3, x0 + 6, y0 + 3), ('w0', 'w1', 'w2'), sd=0, hl=1)
        p.pxs([(x0 + 1, y0 + 4), (x0 + 4, y0 + 4)], 'w0')
        c.stamp(p, 'K')
    # ---- Kimono: kindlich rund, bis über die Waden, Asanoha-Muster (Hanfblatt-Sterne)
    p = C()
    kim = PG([B((22, 22)), B((31, 22)), B((33, 30)), B((35, 46)), B((32, 48)), B((20, 48)), B((18, 44)), B((20, 30))])
    p.form(kim, KIM, sd=3, hl=1)
    for (x, y) in ((22, 34), (29, 31), (27, 41), (33, 42), (21, 44)):
        q = B((x, y))
        star = (L(q[0] - 2, q[1], 0.5, q[0] + 2, q[1], 0.5) | L(q[0], q[1] - 2, 0.5, q[0], q[1] + 2, 0.5)
                | L(q[0] - 1.4, q[1] - 1.4, 0.5, q[0] + 1.4, q[1] + 1.4, 0.5)) & kim
        p.fill(star, 'm0')
        p.pxs([q], 'y2')
    obi = PG([B((19, 29)), B((34, 28)), B((35, 33)), B((19, 34))]) & kim
    p.form(obi, ('y0', 'y1', 'y2'), sd=1, hl=1)
    p.line([B((19, 31)), B((35, 30))], 'y0', only=obi)
    p.line([B((26, 22)), B((23, 28))], 'v3', only=kim)                              # weißer Kragen
    p.line([B((27, 22)), B((24, 28))], 'v2', only=kim)
    p.line([B((31, 34)), B((33, 46))], 'm0', only=kim)
    c.stamp(p, 'K')
    # ---- Kopf
    p = C()
    p.grid(*B((12, 8)), HEAD, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # ---- Arm mit Ball
    hd = B(S['hd'])
    if S['ball']:
        temari(c, B(S['ball']))
    p = C()
    sh_ = B((25, 25))
    sleeve = L(*sh_, 2.6, hd[0] + 3, hd[1] - 1, 2.4) | PG([(sh_[0] + 1, sh_[1] + 2), (hd[0] + 5, hd[1]), (hd[0] + 5, hd[1] + 4), (sh_[0] + 3, sh_[1] + 7)])
    p.form(sleeve, KIM, sd=2, hl=1)
    p.line([(sh_[0] + 1, sh_[1] + 4), (hd[0] + 5, hd[1] + 3)], 'm1', only=sleeve)
    c.stamp(p, 'K')
    p = C(); p.grid(int(hd[0]) - 2, int(hd[1]) - 2, HAND, LEG); c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(ff=19, nf=31), dict(bob=-1, ff=23, nf=28, nlift=2), dict(ff=27, nf=24), dict(bob=-1, ff=24, nf=27, flift=2)]
ATTACK = [dict(bob=1, hd=(18, 18), ball=(16, 13)), dict(bob=-1, lean=-2, hd=(8, 24), ball=(1, 20)),
          dict(hd=(11, 32), ball=None)]

if __name__ == '__main__':
    export('zashiki', draw, WALK, ATTACK)
