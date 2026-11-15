"""Zashiki-warashi: Hausgeist in Kindergestalt, roter Kimono, Pagenkopf, Temari-Ball. Blick nach links.
Gutartig in der Sage, hier verspielt-unheimlich: wirft Bälle, die von Wänden springen."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 64, 64
KIM = ('m1', 'm2', 'm3')
OBI = ('y0', 'y1', 'y2')
SKIN = ('k1', 'k2', 'k3')
HAIR = ('h0', 'hb', 'h2')
FACE = """
KK.....
.......
Ke.....
.......
.......
.q.....
"""
LEG = dict(K='K', e='e1', q='m0')


def draw(bob=0, step=0, arm=0, ball=0):
    setsize(CW, CH)
    c = C()
    cx, by = 30, 58
    top = 22 + bob
    # ferner Fuß / Bein
    p = C()
    p.form(L(cx + 3 - step, top + 22, 2.6, cx + 4 - step * 2, by - 2, 2.4), ('k0', 'k1', 'k1'), sd=1, hl=0)
    p.form(E(cx + 3 - step * 2, by - 1, 3.4, 1.8), ('w0', 'w1', 'w1'), sd=1, hl=0)       # Holzsandale
    c.stamp(p, 'K')
    # Kimono-Körper (Glocke) mit Obi
    p = C()
    body = PG([(cx - 6, top + 8), (cx + 7, top + 8), (cx + 11, top + 26), (cx - 10, top + 26)])
    p.form(body, KIM, sd=3, hl=1)
    for (x, y) in ((cx - 4, top + 13), (cx + 4, top + 18), (cx - 6, top + 22), (cx + 6, top + 24)):   # Blütenmuster
        p.pxs([(x, y), (x + 1, y), (x, y + 1)], 'v3')
        p.pxs([(x + 1, y + 1)], 'y2')
    p.form(R(cx - 7, top + 14, cx + 8, top + 17) & body, OBI, sd=1, hl=1)
    p.line([(cx - 2, top + 8), (cx + 1, top + 14)], 'v3')                                 # Kragen weiß
    c.stamp(p, 'm0')
    # nahes Bein
    p = C()
    p.form(L(cx - 3 + step, top + 24, 2.6, cx - 4 + step * 2, by - 2, 2.4), SKIN, sd=1, hl=1)
    p.form(E(cx - 5 + step * 2, by - 1, 3.6, 1.8), ('w0', 'w1', 'w2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # Kopf mit Pagenkopf (okappa)
    p = C()
    head = E(cx, top + 1, 7.4, 7.4)
    p.form(head, SKIN, sd=2, hl=1)
    c.stamp(p, 'k0')
    p = C()
    hair = (E(cx + 1, top - 2, 8.4, 6.4) | R(cx - 8, top - 2, cx + 9, top + 4) | R(cx + 1, top - 2, cx + 9, top + 8)) & ~(R(cx - 8, top + 1, cx - 1, top + 9))
    p.form(hair, HAIR, sd=2, hl=1)
    p.line([(cx - 8, top), (cx - 1, top)], 'h0')                                          # gerader Pony
    c.stamp(p, 'K')
    p = C()
    p.grid(cx - 7, top + 1, FACE, LEG)
    c.stamp(p, ring=False)
    # Arm mit Temari-Ball
    p = C()
    hx, hy = cx - 10 - arm * 2, top + 14 - arm * 6
    p.form(L(cx - 4, top + 10, 3.0, hx + 2, hy + 1, 3.4), KIM, sd=1, hl=1)              # Ärmel
    p.form(E(hx, hy, 1.8, 1.8), SKIN, sd=0, hl=0)
    c.stamp(p, 'm0')
    p = C()
    bx, byy = hx - 3 - ball * 4, hy - 4 - ball * 3
    tm = E(bx, byy, 4.4, 4.4)
    p.form(tm, ('n1', 'n2', 'n3'), sd=1, hl=1)
    p.line([(bx - 4, byy), (bx + 4, byy)], 'y2', only=tm)
    p.line([(bx, byy - 4), (bx, byy + 4)], 'm2', only=tm)
    p.line([(bx - 3, byy - 3), (bx + 3, byy + 3)], 'v3', only=tm)
    c.stamp(p, 'n0')
    c.blacken()
    return c


col('hb', '#1a1738')
WALK = [dict(step=-1), dict(bob=-1, step=0), dict(step=1), dict(bob=-1, step=0)]
ATTACK = [dict(arm=1, bob=1), dict(arm=2, ball=1, bob=-1), dict(arm=1)]

if __name__ == '__main__':
    export('zashiki', draw, WALK, ATTACK)
