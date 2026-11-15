"""Yamauba: Berghexe mit wildem weißem Haar, zerlumptem Kimono, gebeugt, mit Hackmesser.
Blick nach links. Angriff: schleudert Messer."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 76, 80
ROBE = ('s0', 's1', 's2')        # verblichenes Braun
ROBE2 = ('u0', 'u1', 'u2')       # dunkles Violett (Unterkleid)
SKIN = ('k0', 'k1', 'k2')
HAIR = ('v1', 'v2', 'v3')
FACE = """
KKK.
.....
KeK..
.....
.....
KwKwK
"""
LEG = dict(K='K', e='e1', w='b3')


def draw(bob=0, step=0, arm=0, hair=0):
    setsize(CW, CH)
    c = C()
    cx, by = 38, 74
    top = 30 + bob
    # Haarmähne hinten (wild, nach rechts wehend)
    p = C()
    mane = E(cx + 2, top + 2, 9.4, 9.4)
    for k in range(7):
        a = math.radians(-120 + k * 28)
        ln = 13 + (k * 5) % 7
        mane |= L(cx + 2, top + 2, 3.4, cx + 4 + math.cos(a) * ln + hair, top + 4 + math.sin(a) * ln, 1.2)
    p.form(mane, HAIR, sd=3, hl=1)
    for k in range(5):
        p.line([(cx - 2 + k * 3, top - 5), (cx + 2 + k * 4 + hair, top + 10)], 'v1', only=mane)
    c.stamp(p, 'K')
    # Beine/Füße unter dem Saum
    p = C()
    p.form(E(cx + 4 - step, by - 2, 4.4, 2.2) | E(cx - 5 + step, by - 2, 4.6, 2.2), SKIN, sd=1, hl=1)
    c.stamp(p, 'K')
    # gebeugter Körper mit zerlumptem Saum
    p = C()
    body = PG([(cx - 4, top + 6), (cx + 10, top + 8), (cx + 14, by - 4), (cx + 8, by - 8), (cx + 3, by - 3),
               (cx - 3, by - 7), (cx - 9, by - 3), (cx - 12, top + 22)])
    p.form(body, ROBE, sd=3, hl=1)
    p.form(PG([(cx - 2, top + 10), (cx + 4, top + 10), (cx + 2, by - 6), (cx - 6, by - 6)]) & body, ROBE2, sd=1, hl=0)
    for (x, y) in ((cx + 8, top + 20), (cx - 6, top + 28), (cx + 10, top + 34)):        # Flicken
        p.form(R(x, y, x + 3, y + 3) & body, ('w0', 'w1', 'w2'), sd=0, hl=0)
    c.stamp(p, 'K')
    # Kopf, nach vorn gereckt
    hx, hy = cx - 6, top + 4
    p = C()
    p.form(E(hx, hy, 6.4, 7.0) | E(hx - 4, hy + 4, 3.4, 3.0), SKIN, sd=2, hl=1)
    p.line([(hx - 2, hy - 3), (hx + 3, hy - 1)], 'k0'); p.line([(hx - 3, hy + 1), (hx + 1, hy + 2)], 'k0')   # Falten
    c.stamp(p, 'K')
    p = C()
    fr = E(hx + 3, hy - 5, 7.4, 3.0) | L(hx + 6, hy - 3, 2.4, hx + 8, hy + 8, 1.6)
    p.form(fr, HAIR, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    p.grid(hx - 7, hy - 3, FACE, LEG)
    c.stamp(p, ring=False)
    # Arm mit Hackmesser
    p = C()
    ax, ay = hx - 4 - arm * 3, top + 18 - arm * 8
    p.form(L(cx - 2, top + 12, 2.8, ax, ay, 2.2), ROBE, sd=1, hl=1)
    p.form(E(ax, ay, 2.2, 2.2), SKIN, sd=0, hl=1)
    c.stamp(p, 'K')
    p = C()
    blade = PG([(ax - 1, ay - 1), (ax - 10, ay - 6 + arm * 2), (ax - 11, ay - 1 + arm * 2), (ax - 2, ay + 2)])
    p.form(blade, ('i1', 'i2', 'i3'), sd=1, hl=1)
    p.line([(ax - 10, ay - 6 + arm * 2), (ax - 2, ay - 2)], 'v3')
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(step=-2, hair=0), dict(bob=-1, hair=1), dict(step=2, hair=0), dict(bob=-1, hair=-1)]
ATTACK = [dict(arm=1, bob=1, hair=1), dict(arm=2, bob=-1, hair=-2), dict(arm=1)]

if __name__ == '__main__':
    export('yamauba', draw, WALK, ATTACK)
