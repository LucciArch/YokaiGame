"""Tsuchigumo (土蜘蛛) – Erdspinne aus den Schriftrollen um Minamoto no Raikō. Komplett neu (Runde 104):
Dämonenfratze statt Spinnenkopf (breites Fangmaul, goldene Augen, sechs kleine Spinnenaugen auf der Stirn,
zwei Stummelhörner, struppige Mähne), Beine mit Tigerstreifen, Hinterleib schwarz mit gelben Querbändern und
Erdkrusten. Gleiches Gerüst wie Gyūki. Angriff: bäumt sich auf und reißt das Maul auf."""
import math
from spider import *

col('tg0', '#0c0a14'); col('tg1', '#221c26'); col('tg2', '#3e3438'); col('tg3', '#625250')
DARK.update(tg3='tg2', tg2='tg1', tg1='tg0')
add_rim('tg0 tg1 tg2', 'xt')
BODY = ('tg1', 'tg2', 'tg3')
TIG = ('t0', 't1', 't2')
TIGF = ('s0', 't0', 't1')
RAMPS = dict(leg=TIG, legf=TIGF, joint='tg1', body=BODY, stripe='tg0')


def demon_head(c, o, S, k=1.3):
    x0, y0 = o
    m = S.get('mouth', 0)

    def Q(dx, dy):
        return (x0 + dx * k, y0 + dy * k)

    def r(v):
        return v * k
    # weiße Nō-Mähne, nach hinten über den Leib gestrichen
    for kk in range(9):
        t = kk / 8
        p = C()
        root = Q(1 + t * 7, -8 + t * 10)
        tip = Q(14 + t * 4 + math.sin(kk * 1.7) * 2, 6 + t * 10)
        mid = lerp(root, tip, 0.45); mid = (mid[0] + 2, mid[1] - 2)
        lock = L(*root, r(2.2), *mid, r(1.7)) | L(*mid, r(1.7), *tip, 0.6)
        p.form(lock, ('v1', 'v2', 'v3'), sd=1, hl=1)
        p.line([root, mid], 'v1', only=erode(lock, 1))
        c.stamp(p, 'K')
    p = C()
    for (sx, far) in ((5, True), (0, False)):                          # Stummelhörner
        p.form(L(*Q(sx, -7), r(1.6), *Q(sx - 3, -12), 0.6), ('b0', 'b1', 'b2') if not far else ('b0', 'b0', 'b1'), sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    skull = E(*Q(1, -2), r(8), r(7))
    face = PG([Q(-8, -5), Q(-11, -1), Q(-13, 3), Q(-12, 7 + m), Q(-4, 10 + m), Q(6, 8), Q(8, 2), Q(4, -6)])
    head = skull | face
    p.form(head, ('r1', 'r2', 'r3'), sd=3, hl=1)
    p.form(E(*Q(-10, 1), r(2.6), r(2.2)) & head, ('r1', 'r2', 'r3'), sd=1, hl=1)   # Knollnase
    p.pxs([Q(-12, 2), Q(-10, 2.6)], 'r0')
    mo = PG([Q(-12, 4.5), Q(-4, 5), Q(4, 3), Q(2, 6 + m), Q(-5, 8 + m), Q(-11, 6.5 + m)])
    p.fill(mo, 'q')
    up = mo & ~sh(mo, 0, -2)
    p.fill(up, 'b3')                                                      # obere Zahnreihe
    lo = mo & ~sh(mo, 0, 2)
    p.fill(lo, 'b2')                                                      # untere Zahnreihe
    for xx in (-10, -6, -2, 2):
        p.pxs([Q(xx, 4.6 - (xx > 0) * 1)], 'b1')
    for xx in (-9, 1):                                                    # Fänge
        p.form(L(*Q(xx, 4.5), 1.2, *Q(xx + 0.4, 8 + m * 0.5), 0.5), ('b1', 'b2', 'b3'), sd=0, hl=1)
    p.line([Q(-9, -4), Q(-3, -6), Q(3, -5)], 'r0', only=head)             # Stirnfalte
    p.line([Q(0, 0), Q(3, 3)], 'r1', only=head)                           # Wange
    c.stamp(p, 'K')
    p = C()
    p.fill(E(*Q(-5, -2), r(2.0), r(1.3)), 'K')                         # großes Hauptauge
    p.fill(E(*Q(-5.4, -1.8), r(1.4), r(0.7)), 'y2')
    p.pxs([Q(-5, -1.8)], 'K'); p.pxs([Q(-6.4, -2.3)], 'y3')
    p.line([Q(-9, -4), Q(-1, -4.6)], 'r0')
    for (dx, dy) in ((-3, -8), (0, -9), (3, -8.5), (-1, -6.6), (2, -6.4)):  # Spinnenaugen auf der Stirn
        p.fill(E(*Q(dx, dy), 1.0, 1.0), 'e1')
        p.pxs([Q(dx - 0.3, dy - 0.3)], 'y3')
    c.stamp(p, 'K')


def abdomen(c, o, S):
    x, y = o
    p = C()
    stalk = L(x - 22, y + 8, 3, x - 14, y + 6, 4)
    p.form(stalk, ('tg0', 'tg1', 'tg2'), sd=1, hl=0)
    abd = E(x, y, 22, 17) | E(x + 8, y + 4, 18, 14)
    p.form(abd, BODY, sd=5, hl=2)
    for kk in range(5):                                                 # gelbe Querbänder
        bx = x - 12 + kk * 8
        band = L(bx, y - 14, 1.6, bx + 4, y + 14, 1.6) & erode(abd, 1)
        p.form(band, ('y0', 'y1', 'y2'), sd=1, hl=0)
    for (ex, ey, rx) in ((x + 14, y + 12, 5), (x - 6, y + 13, 4)):      # Erdkrusten unten
        p.form(E(ex, ey, rx, 2.4) & abd, ('s0', 's1', 's2'), sd=1, hl=1)
    c.stamp(p, 'K')


def draw(**S):
    setsize(CW, CH)
    c = C()
    return body(c, S, RAMPS, demon_head, abdomen)


WALK = [dict(gait=0), dict(gait=1, bob=-1), dict(gait=0, bob=0), dict(gait=1, bob=-1)]
ATTACK = [dict(rear=4, mouth=1), dict(rear=8, mouth=3, bob=-1), dict(rear=2, mouth=2)]

if __name__ == '__main__':
    export('tsuchigumo', draw, WALK, ATTACK)
