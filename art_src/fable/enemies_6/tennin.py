"""Tennin (天人) – Himmelsmädchen, wie sie auf Tempeldecken und Schreinbildern fliegen. Komplett neu
(Runde 109): fliegt waagrecht nach links, der Körper geneigt, das Gewand weht nach hinten in einen langen
Schweif aus Stoff aus (keine Füße). Hohe Doppel-Haarschlaufe mit Goldschmuck, ruhiges Gesicht mit roten Lippen
und Stirnpunkt, weißes Obergewand mit weiten Ärmeln, roter Faltenrock, Goldgürtel. Die Hagoromo-Schärpe
schlingt sich in zwei Bögen um sie. In der vorderen Hand eine goldene Lotosblüte.
Angriff: hebt die Lotosblüte, die aufleuchtet und Lichtblätter streut."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 120, 84
OX, OY = 8, 8
col('hb', '#1a1738')
col('hg0', '#1c3448'); col('hg1', '#3c7088'); col('hg2', '#7cb8bc'); col('hg3', '#c8ecdc')
add_rim('hg0 hg1 hg2', 'hg3'); DARK.update(hg3='hg2', hg2='hg1', hg1='hg0')
SK = ('k1', 'k2', 'k3')
WH = ('v1', 'v2', 'v3')
RED = ('m1', 'm2', 'm3')
SCARF = ('hg1', 'hg2', 'hg3')
SCARFF = ('hg0', 'hg1', 'hg2')
GOLD = ('y0', 'y1', 'y2')
LEG = dict(zip('abcdKqrhHyY', ['k0', 'k1', 'k2', 'k3', 'K', 'q', 'm2', 'h0', 'hb', 'y1', 'y2']))
# Gesicht im Dreiviertelprofil nach links, Augen gesenkt, Haaransatz in der Mitte gescheitelt
FACE = """
....hhhhhh..
..hhHHHHHHh.
.hHHHhhHHHHh
.hHdddcchHHh
hHddrdccchHh
hHdKKdcKKhHh
.hddddcccbhH
.cdddcdccbhH
.cddddccbbhh
..cdrrccbbh.
...cdccbbb..
....bbbaa...
"""


def P(x, y):
    return (x + OX, y + OY)


def ribbon(c, pts, w, ramp, ln='K'):
    p = C()
    m = None
    n = len(pts)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        wa = w * (1 - 0.5 * i / n); wb = w * (1 - 0.5 * (i + 1) / n)
        s_ = L(*a, wa, *b, wb)
        m = s_ if m is None else m | s_
    p.form(m, ramp, sd=1, hl=1)
    c.stamp(p, ln)
    return m


def draw(bob=0, ph=0.0, lift=0, glow=0):
    setsize(CW, CH)
    c = C()

    def B(x, y):
        return P(x, y + bob)

    def wave(x0, y0, x1, y1, amp, n=10, k=1.0):
        return [B(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + math.sin(t * math.pi * 2 * k + ph) * amp) for t in [i / n for i in range(n + 1)]]

    # ---- hinterer Schärpenbogen (über dem Rücken hoch, hinten hinaus)
    pts = wave(30, 20, 96, 6, 5, k=1.0)
    ribbon(c, pts, 2.2, SCARFF)
    # ---- ferner Arm mit weitem Ärmel, Hand vor der Brust
    p = C()
    sleeve = PG([B(34, 30), B(30, 38), B(36, 46 + math.sin(ph) * 1.5), B(44, 44), B(40, 32)])
    p.form(sleeve, ('v0', 'v1', 'v2'), sd=1, hl=1)
    c.stamp(p, 'K')
    # ---- Rock: roter Faltenrock, der in eine lange Stoffbahn ausläuft
    p = C()
    sk = [B(38, 32), B(52, 34), B(66, 38 + math.sin(ph) * 2), B(82, 42 + math.sin(ph + 1) * 3), B(98, 44 + math.sin(ph + 2) * 4)]
    skirt = (L(*sk[0], 8, *sk[1], 9) | L(*sk[1], 9, *sk[2], 8) | L(*sk[2], 8, *sk[3], 5.4) | L(*sk[3], 5.4, *sk[4], 1.8))
    p.form(skirt, RED, sd=3, hl=1)
    for k in range(4):                                                   # Längsfalten
        off = -5 + k * 3.4
        p.line([(q[0], q[1] + off * (1 - i / 5)) for i, q in enumerate(sk[:4])], 'm1', only=erode(skirt, 1))
    hem = skirt & ~sh(skirt, 0, -2)
    p.fill(hem & sh(skirt, 0, 2), 'y1')                                  # Goldborte am Saum
    c.stamp(p, 'K')
    # weißes Untergewand blitzt an der Spitze heraus
    p = C()
    under = L(*sk[3], 3, *(sk[4][0] + 6, sk[4][1] + 3), 0.8)
    p.form(under & ~skirt, WH, sd=1, hl=1)
    c.stamp(p, 'K')
    # ---- Oberkörper: weißes Gewand, über Kreuz geschlossen, Goldgürtel
    p = C()
    tor = E(*B(34, 29), 7.4, 7) | L(*B(30, 26), 5, *B(40, 33), 6)
    p.form(tor, WH, sd=2, hl=1)
    p.line([B(28, 23), B(34, 32)], 'v0', only=tor)                       # Kragen
    p.line([B(29, 23), B(35, 32)], 'm2', only=tor)                       # rotes Untergewand am Kragen
    belt = L(*B(35, 34), 2.0, *B(43, 31), 2.0)
    p.form(belt, GOLD, sd=1, hl=1)
    p.form(E(*B(38, 36), 1.6, 3.0), GOLD, sd=1, hl=1)                    # Gürtelquaste
    c.stamp(p, 'K')
    # ---- Kopf: Hals, Gesicht, Haar mit hoher Doppelschlaufe
    p = C()
    p.form(L(*B(27, 22), 2.0, *B(29, 26), 2.2), SK, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    for (cx, cy, far) in ((26, 2, True), (20, 4, False)):                # Haarschlaufen
        loop = E(*B(cx, cy), 3.6, 4.4) & ~E(*B(cx, cy), 1.4, 2.2)
        p.form(loop, ('h0', 'h1', 'h2') if not far else ('h0', 'h0', 'h1'), sd=1, hl=1)
    p.form(E(*B(23, 9), 4.4, 2.6), ('h0', 'hb', 'h2'), sd=1, hl=1)        # Knoten
    c.stamp(p, 'K')
    p = C()
    p.grid(*[int(v) for v in B(14, 9)], FACE, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb'))
    p = C()
    p.form(E(*B(23, 8), 4.4, 1.2), GOLD, sd=0, hl=1)                     # Goldreif
    for (x, y) in ((19, 7), (23, 6), (27, 7)):
        p.pxs([B(x, y)], 'y3')
    p.form(L(*B(27, 8), 0.8, *B(30, 14), 0.6), GOLD, sd=0, hl=1)          # Haarnadel-Gehänge
    p.pxs([B(30, 15)], 'm3')
    p.pxs([B(16, 13)], 'm2')                                             # Stirnpunkt
    c.stamp(p, 'K')
    for k in range(3):                                                   # Haarsträhnen nach hinten
        ribbon(c, wave(26, 12 + k * 2, 40 + k * 3, 16 + k * 3, 1.0, n=5, k=0.7), 1.4, ('h0', 'hb', 'h2'))
    # ---- naher Arm: nach vorn gestreckt, weiter Ärmel hängt, Lotos in der Hand
    p = C()
    hx, hy = B(12, 26 - lift)
    sl = PG([B(30, 26), B(18, 26 - lift * 0.6), B(16, 34 - lift * 0.5 + math.sin(ph + 0.5) * 1.5), B(24, 38), B(32, 32)])
    p.form(sl, WH, sd=2, hl=1)
    p.line([B(18, 27 - lift * 0.6), B(17, 33 - lift * 0.5)], 'v1', only=sl)
    c.stamp(p, 'K')
    p = C()
    p.form(L(*B(18, 27 - lift * 0.6), 1.6, hx + 2, hy + 1, 1.4), SK, sd=1, hl=1)
    c.stamp(p, 'K')
    p = C()
    lot = (tri((hx, hy), -90, 6 + glow, 3.4) | tri((hx - 1, hy), -130, 5 + glow, 3) | tri((hx + 1, hy), -50, 5 + glow, 3)
           | E(hx, hy + 1, 3.0, 1.4))
    p.form(lot, ('y1', 'y2', 'y3') if glow else ('m2', 'm3', 'p3'), sd=1, hl=1)
    p.fill(E(hx, hy, 1.2, 1.0), 'y2')
    c.stamp(p, 'y0' if glow else 'K')
    if glow:
        p = C()
        for (dx, dy) in ((-8, -6), (-11, 0), (-6, -11), (2, -12)):
            q = (hx + dx, hy + dy)
            p.fill(tri(q, -90, 3, 2) | tri((q[0], q[1] + 1), 90, 2, 2), 'y3')
        c.stamp(p, 'y1')
    # ---- vorderer Schärpenbogen: von der Schulter unter dem Körper hindurch nach hinten
    pts = [B(20, 34)] + wave(26, 44, 104, 54, 3, n=9, k=1.2)[1:]
    ribbon(c, pts, 1.9, SCARF)
    c.blacken()
    return c


WALK = [dict(ph=0), dict(ph=1.6, bob=-1), dict(ph=3.2, bob=-2), dict(ph=4.8, bob=-1)]
ATTACK = [dict(ph=0.5, lift=4), dict(ph=1.0, lift=8, glow=1, bob=-1), dict(ph=1.5, lift=5, glow=1)]

if __name__ == '__main__':
    export('tennin', draw, WALK, ATTACK)
