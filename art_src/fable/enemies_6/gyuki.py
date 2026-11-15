"""Gyūki (牛鬼) – Ochsenkopf auf Spinnenleib, lauert an Küsten und Flüssen. Komplett neu (Runde 104):
richtiger Rinderschädel im Profil nach links (lange Stirn, breites Flotzmaul mit Nüstern, Nasenring, seitliches
Auge, waagrechtes Ohr, weit ausladende Hörner), aus dem Maul ragende Hauer, zotteliges Stirnhaar. Dunkler
behaarter Spinnenleib mit rotem Winkelmuster und triefendem Seetang. Angriff: bäumt sich auf und stößt zu."""
import math
from spider import *

col('gy0', '#120a12'); col('gy1', '#2e1c22'); col('gy2', '#523638'); col('gy3', '#80564e')
col('xgy', '#c49a8a'); add_rim('gy0 gy1 gy2', 'xgy')
DARK.update(gy3='gy2', gy2='gy1', gy1='gy0')
FUR = ('gy1', 'gy2', 'gy3')
FURF = ('gy0', 'gy1', 'gy2')
RAMPS = dict(leg=FUR, legf=FURF, joint='gy3', body=FUR)


def ox_head(c, o, S, k=1.35):
    x0, y0 = o
    m = S.get('mouth', 0)

    def Q(dx, dy):
        return (x0 + dx * k, y0 + dy * k)

    def r(v):
        return v * k
    # Hörner: oben am Schädel, erst nach außen-oben, dann nach vorn gebogen (ferner Horn dunkler, dahinter)
    for (pts, far) in (((Q(6, -7), Q(13, -14), Q(10, -22)), True), ((Q(0, -7), Q(5, -16), Q(-5, -23)), False)):
        p = C()
        a, b, t = pts
        horn = L(*a, r(2.3), *b, r(1.7)) | L(*b, r(1.7), *t, 0.6)
        p.form(horn, ('b0', 'b1', 'b2') if not far else ('b0', 'b0', 'b1'), sd=1, hl=1)
        for f in (0.3, 0.6):
            p.pxs([lerp(a, b, f)], 'b0')
        c.stamp(p, 'K')
    p = C()
    skull = E(*Q(2, -2), r(8.4), r(8))
    face = L(*Q(-2, -2), r(6.6), *Q(-12, 7), r(5.0))
    muz = E(*Q(-13, 8), r(5.0), r(4.2))
    jaw = PG([Q(-16, 11 + m), Q(-5, 11), Q(4, 5), Q(2, 12 + m), Q(-9, 15 + m)])
    p.form(jaw, FURF, sd=1, hl=1)
    head = skull | face
    p.form(head, FUR, sd=3, hl=1)
    p.form(muz, ('gy1', 'gy2', 'gy3'), sd=1, hl=1)
    p.fill(E(*Q(-16.5, 6.5), 1.3, 1.5), 'K')                          # Nüstern
    p.pxs([Q(-12.5, 6.5)], 'K')
    p.line([Q(-11, -2), Q(-5, 4)], 'gy1', only=face)                  # Nasenrücken-Kante
    for kk in range(5):                                               # zotteliges Stirnhaar
        p.line([Q(-4 + kk * 2.4, -9), Q(-5 + kk * 2.4, -4)], 'gy3' if kk % 2 else 'gy1', only=head)
    if m > 0:
        p.fill(PG([Q(-17, 10), Q(-5, 10), Q(-7, 11 + m), Q(-15, 11 + m)]), 'q')
    c.stamp(p, 'K')
    p = C()
    p.fill(E(*Q(-4, 0), r(2.0), r(1.6)), 'K')                          # Auge mit schwerem Lid
    p.fill(E(*Q(-4, 0.4), r(1.3), r(0.8)), 'e1')
    p.pxs([Q(-5, 0)], 'y3')
    p.line([Q(-7, -2), Q(-1, -3)], 'gy0')
    ear = E(*Q(9, -3), r(4.2), r(1.8))                                # Ohr waagrecht nach hinten
    p.form(ear, FUR, sd=1, hl=1)
    p.fill(E(*Q(9, -2.6), r(2.4), 0.8), 'm1')
    rx, ry = Q(-15.5, 9)                                              # Nasenring
    p.line([(rx, ry), (rx - 1, ry + 3), (rx + 2, ry + 4), (rx + 3, ry + 2)], 'y1')
    p.pxs([(rx - 1, ry + 3)], 'y2')
    c.stamp(p, 'K')
    p = C()
    for (fx, h) in ((-11, 6), (-3, 5)):                               # Hauer aus dem Unterkiefer
        bx, by = Q(fx, 12 + m)
        p.form(L(bx, by, 1.5, bx - 2, by - h, 0.5), ('b1', 'b2', 'b3'), sd=0, hl=1)
    c.stamp(p, 'K')


def abdomen(c, o, S):
    x, y = o
    p = C()
    stalk = L(x - 22, y + 8, 3, x - 14, y + 6, 4)
    p.form(stalk, FURF, sd=1, hl=0)
    abd = E(x, y, 22, 17) | E(x + 8, y + 4, 18, 14)
    p.form(abd, FUR, sd=5, hl=2)
    for k in range(4):                                                # rote Winkel (Chevrons) auf dem Rücken
        cx = x - 10 + k * 8
        p.line([(cx - 3, y - 12 + k), (cx + 1, y - 7 + k), (cx + 5, y - 13 + k)], 'm2', only=erode(abd, 2))
        p.line([(cx - 3, y - 11 + k), (cx + 1, y - 6 + k), (cx + 5, y - 12 + k)], 'm1', only=erode(abd, 2))
    for k in range(9):                                                # Borstenbüschel am Rand
        a = math.radians(200 + k * 20)
        q = (x + 4 + math.cos(a) * 22, y + 3 + math.sin(a) * 16)
        p.line([q, (q[0] + math.cos(a) * 2, q[1] + math.sin(a) * 2)], 'gy3', only=abd)
    rg = __import__('random').Random(3)
    for k in range(40):                                               # Fellstriche
        q = (x - 16 + rg.uniform(0, 40), y - 12 + rg.uniform(0, 26))
        p.line([q, (q[0] + 1, q[1] + 2)], rg.choice(('gy1', 'gy3')), only=erode(abd, 2))
    for (sx, ln) in ((8, 10), (16, 7), (2, 6)):                       # triefender Seetang
        p.form(L(x + sx, y + 13, 1.4, x + sx + 1, y + 13 + ln, 0.8), ('g0', 'g1', 'g2'), sd=0, hl=1)
    c.stamp(p, 'K')


def draw(**S):
    setsize(CW, CH)
    c = C()
    return body(c, S, RAMPS, ox_head, abdomen)


WALK = [dict(gait=0), dict(gait=1, bob=-1), dict(gait=0, bob=0), dict(gait=1, bob=-1)]
ATTACK = [dict(rear=4, mouth=1), dict(rear=8, mouth=3, bob=-1), dict(rear=2, mouth=2)]

if __name__ == '__main__':
    export('gyuki', draw, WALK, ATTACK)
