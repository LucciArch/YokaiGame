"""Kawauso: Fischotter-Yokai vom Flussufer, steht aufrecht, trägt einen kleinen Strohhut und eine Laterne
– so lockt er Wanderer ans Wasser. Blick nach links. Angriff: schleudert Flusskiesel."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 64, 64
FUR = ('s1', 's2', 's3')
BELLY = ('c0', 'c1', 'c2')
STRAW = ('o0', 'o1', 'o2')
FACE = """
.KKK
.KeK
..K.
"""
LEG = dict(K='K', e='y3')


def draw(bob=0, step=0, arm=0, tail=0):
    setsize(CW, CH)
    c = C()
    cx, by = 30, 58
    t = 26 + bob
    # Schwanz (hinten, dick, spitz zulaufend)
    p = C()
    p.form(L(cx + 5, t + 22, 4.8, cx + 14 + tail, by - 3, 2.2), ('s0', 's1', 's2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # ferner Fuß
    p = C()
    p.form(E(cx + 4 - step, by - 2, 4.4, 2.2), ('s0', 's1', 's1'), sd=1, hl=0)
    c.stamp(p, 'K')
    # Körper: aufrechte Walze mit hellem Bauch
    p = C()
    body = E(cx, t + 16, 8.4, 12.4)
    p.form(body, FUR, sd=3, hl=1)
    p.form(E(cx - 3, t + 18, 4.4, 8.4) & body, BELLY, sd=1, hl=1)
    c.stamp(p, 's0')
    # naher Fuß
    p = C()
    p.form(E(cx - 4 + step, by - 2, 4.6, 2.2), FUR, sd=1, hl=1)
    c.stamp(p, 'K')
    # Kopf: flach, breite Schnauze, kleine Ohren
    p = C()
    head = E(cx - 1, t + 1, 7.4, 6.6) | E(cx - 6, t + 3, 3.6, 3.0)
    p.form(head, FUR, sd=2, hl=1)
    p.form(E(cx - 6, t + 5, 3.0, 1.6) & head, BELLY, sd=0, hl=0)          # helles Kinn
    p.fill(E(cx - 9, t + 2, 1.8, 1.4), 'K')                               # Nase
    p.pxs([(cx - 9, t + 1)], 'z3')
    for k in range(2):                                                    # Schnurrhaare
        p.line([(cx - 8, t + 3 + k), (cx - 13, t + 2 + k * 3)], 'v3')
    c.stamp(p, 's0')
    p = C()
    p.grid(cx - 6, t - 2, FACE, LEG)
    c.stamp(p, ring=False)
    # Strohhut (kasa), schräg
    p = C()
    hat = PG([(cx - 10, t - 3), (cx + 1, t - 10), (cx + 10, t - 4), (cx + 2, t - 2)])
    p.form(hat, STRAW, sd=2, hl=1)
    for k in range(3):
        p.line([(cx + 1, t - 10), (cx - 7 + k * 6, t - 3)], 'o0', only=hat)
    c.stamp(p, 'o0')
    # Arm mit Laterne (ruhend) bzw. Kiesel (Angriff)
    p = C()
    hx, hy = cx - 9 - arm * 2, t + 13 - arm * 6
    p.form(L(cx - 3, t + 10, 2.6, hx + 1, hy, 2.4), FUR, sd=1, hl=1)
    c.stamp(p, 's0')
    p = C()
    if arm == 0:
        lam = E(hx - 1, hy + 6, 3.4, 4.4)
        p.line([(hx, hy), (hx - 1, hy + 2)], 'w0')
        p.form(lam, ('y0', 'y1', 'y2'), sd=1, hl=1)
        p.fill(E(hx - 1, hy + 6, 1.4, 2.4), 'y3')
        c.stamp(p, 'y0')
    else:
        p.form(E(hx - 2, hy - 1, 2.8, 2.4), ('z0', 'z1', 'z2'), sd=1, hl=1)
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(step=-1, tail=0), dict(bob=-1, tail=1), dict(step=1, tail=0), dict(bob=-1, tail=-1)]
ATTACK = [dict(arm=1, bob=1), dict(arm=2, bob=-1, tail=2), dict(arm=1)]

if __name__ == '__main__':
    export('kawauso', draw, WALK, ATTACK)
