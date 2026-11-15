"""Kitsune no yomeiri – die Fuchshochzeit: aufrecht gehende Füchse in Festkimono.
Gefolge trägt eine Papierlaterne, die Braut einen weißen Wataboshi-Schleier.
Blick nach links. 'Angriff' = Verbeugung (wird für das Danken benutzt)."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(common.D + '_review', exist_ok=True)

CW, CH = 56, 64
FUR = ('t0', 't1', 't2')
WHITE = ('v1', 'v2', 'v3')
RED = ('m1', 'm2', 'm3')
EYE = """
KK
"""


def make(bride):
    def draw(bob=0, step=0, bow=0, tail=0):
        setsize(CW, CH)
        c = C()
        cx, by = 28, 60
        t = 22 + bob + bow * 2
        hx = cx - 2 - bow * 3                           # Kopf neigt sich bei Verbeugung
        # Schwanz: buschig, weiße Spitze
        p = C()
        tail_m = L(cx + 5, t + 26, 3.6, cx + 15 + tail, t + 14, 5.2) | E(cx + 15 + tail, t + 12, 4.6, 4.4)
        p.form(tail_m, FUR, sd=1, hl=1)
        p.form(E(cx + 16 + tail, t + 10, 3.2, 3.0) & tail_m, WHITE, sd=0, hl=1)
        c.stamp(p, 't0')
        # Füße
        for dx, ramp in ((3 - step, ('s0', 's1', 's1')), (-3 + step, ('s0', 's1', 's2'))):
            p = C()
            p.form(E(cx + dx, by - 1, 3.2, 1.8), ramp, sd=0, hl=1)
            c.stamp(p, 'K')
        # Kimono: Glocke, weiß (Braut) bzw. rot mit weißem Kragen (Gefolge)
        p = C()
        robe = PG([(cx - 6, t + 10), (cx + 6, t + 10), (cx + 10, by - 2), (cx - 10, by - 2)]) | E(cx, t + 12, 6.4, 4.0)
        p.form(robe, WHITE if bride else RED, sd=2, hl=1)
        p.form(PG([(cx - 9, t + 34), (cx + 9, t + 34), (cx + 9, t + 36), (cx - 9, t + 36)]) & robe,
               ('y0', 'y1', 'y2') if bride else ('h0', 'h1', 'h2'), sd=0, hl=1)   # Obi-Saum
        p.form(E(cx, t + 20, 7.0, 2.0) & robe, ('y0', 'y1', 'y2') if bride else ('v0', 'v1', 'v2'), sd=0, hl=1)  # Obi
        if not bride:
            p.line([(cx - 4, t + 10), (cx, t + 17), (cx + 4, t + 10)], 'v2', only=robe)
        c.stamp(p, 'v0' if bride else 'm0')
        # Kopf: spitze Schnauze nach links, große Ohren
        p = C()
        head = E(hx, t + 3, 5.6, 5.0) | PG([(hx - 4, t + 1), (hx - 10, t + 6), (hx - 3, t + 8)])
        p.form(head, FUR, sd=2, hl=1)
        p.form(PG([(hx - 3, t + 6), (hx - 9, t + 6), (hx - 2, t + 8)]) & head, WHITE, sd=0, hl=1)   # helle Kehle
        p.pxs([(hx - 10, t + 6)], 'K')
        c.stamp(p, 't0')
        if not bride:
            for ex in (-3, 3):
                p = C()
                ear = PG([(hx + ex - 2, t - 1), (hx + ex + 2, t - 1), (hx + ex + 1, t - 8)])
                p.form(ear, FUR, sd=1, hl=1)
                c.stamp(p, 't0')
        else:
            p = C()
            hood = E(hx + 1, t + 1, 6.4, 6.0) | PG([(hx + 4, t), (hx + 8, t + 10), (hx + 1, t + 9)])
            hood = hood & ~E(hx - 3, t + 5, 4.2, 3.4)
            p.form(hood, WHITE, sd=2, hl=1)
            c.stamp(p, 'v0')
        p = C()
        p.grid(hx - 5, t + 3, EYE, dict(K='K'))
        p.pxs([(hx - 3, t + 5)], 'm2')                     # rote Kumadori-Linie
        c.stamp(p, ring=False)
        # Arm: Laterne (Gefolge) oder gefaltete Hände (Braut)
        p = C()
        ax, ay = cx - 7 - bow, t + 18 + bow
        p.form(L(cx - 2, t + 12, 2.4, ax, ay, 2.2), WHITE if bride else RED, sd=1, hl=1)
        c.stamp(p, 'v0' if bride else 'm0')
        if not bride:
            p = C()
            lx, ly = ax - 3, ay + 3
            p.line([(ax, ay), (lx, ly - 2)], 'w0')
            lam = E(lx, ly + 3, 3.0, 4.2)
            p.form(lam, ('y0', 'y1', 'y2'), sd=1, hl=1)
            p.fill(E(lx, ly + 3, 1.2, 2.2), 'y3')
            p.line([(lx - 2, ly), (lx + 2, ly)], 'K')
            p.line([(lx - 2, ly + 7), (lx + 2, ly + 7)], 'K')
            c.stamp(p, 'y0')
        c.blacken()
        return c
    return draw


WALK = [dict(step=-1, tail=0), dict(bob=-1, tail=1), dict(step=1, tail=0), dict(bob=-1, tail=-1)]
ATTACK = [dict(bow=1), dict(bow=2, bob=1), dict(bow=1)]

if __name__ == '__main__':
    export('kitsune_gefolge', make(False), WALK, ATTACK)
    export('kitsune_braut', make(True), WALK, ATTACK)
