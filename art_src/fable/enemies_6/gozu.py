"""Gozu (牛頭) und Mezu (馬頭) – Ochsenkopf und Pferdekopf, die Höllenwächter an Enmas Hof.
Komplett neu (Runde 108): gleicher muskulöser Körperbau wie der Oni-Meister (Brust, Bauch, Bizeps, Waden),
damit sie in die Serie passen, aber mit eigener Haut, grobem Lendentuch mit Strickgürtel, Eisenmanschetten
und eigener Waffe. Gozu: blaugraue Haut, schwarzbrauner Ochsenschädel mit weißen Hörnern, Nasenring,
Sasumata (Fanggabel). Mezu: rotbraune Haut, langer Pferdeschädel mit Stirnlocke, gefletschte Zähne,
Nackenmähne, Lanze mit Hakenklinge. Blick nach links. Angriff: Stoß mit der Stangenwaffe."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
import warden as W

KIND = sys.argv[1] if len(sys.argv) > 1 else 'gozu'


def pole(c, hand, ang, ln=40, back=14, kind='gozu'):
    dx, dy = -math.cos(ang), -math.sin(ang)
    nx, ny = -dy, dx
    hx, hy = hand
    p = C()
    e0 = (hx - dx * back, hy - dy * back)
    tip = (hx + dx * ln, hy + dy * ln)
    p.form(L(*e0, 1.6, *tip, 1.6), ('w0', 'w1', 'w2'), sd=1, hl=1)
    p.form(E(*e0, 2.2, 2.2), ('i0', 'i1', 'i2'), sd=1, hl=1)
    for t in (0.55, 0.62):                                           # Wicklung
        q = lerp(e0, tip, t)
        p.fill(E(*q, 2.0, 2.0), 'w0')
    c.stamp(p, 'K')
    p = C()
    if kind == 'gozu':                                               # Sasumata: U-Gabel mit Dornen
        bar = L(tip[0] + nx * 7, tip[1] + ny * 7, 1.6, tip[0] - nx * 7, tip[1] - ny * 7, 1.6)
        pr = np.zeros_like(bar)
        for s_ in (-1, 1):
            a = (tip[0] + nx * 7 * s_, tip[1] + ny * 7 * s_)
            b = (a[0] + dx * 8 - nx * s_ * 1.5, a[1] + dy * 8 - ny * s_ * 1.5)
            pr |= L(*a, 1.6, *b, 0.6)
            for t in (0.3, 0.7):
                q = lerp(a, b, t)
                pr |= L(*q, 0.9, q[0] - nx * s_ * 2.6, q[1] - ny * s_ * 2.6, 0.4)
        p.form(bar | pr, ('i1', 'i2', 'i3'), sd=1, hl=1)
    else:                                                           # Lanze mit Hakenklinge
        blade = PG([(tip[0] + nx * 2.2, tip[1] + ny * 2.2), (tip[0] + dx * 14, tip[1] + dy * 14),
                    (tip[0] - nx * 2.2, tip[1] - ny * 2.2)])
        hook = PG([(tip[0] - nx * 1.5, tip[1] - ny * 1.5), (tip[0] - nx * 7 + dx * 3, tip[1] - ny * 7 + dy * 3),
                   (tip[0] - nx * 6 + dx * 6, tip[1] - ny * 6 + dy * 6), (tip[0] - nx * 2 + dx * 2, tip[1] - ny * 2 + dy * 2)])
        p.form(blade | hook, ('i1', 'i2', 'i3'), sd=1, hl=1)
        p.line([tip, (tip[0] + dx * 12, tip[1] + dy * 12)], 'i3', only=blade)
        tas = L(tip[0] - dx * 2, tip[1] - dy * 2, 2.0, tip[0] - dx * 2 + 2, tip[1] - dy * 2 + 7, 1.2)
        p.form(tas, ('m1', 'm2', 'm3'), sd=1, hl=1)                   # rote Quaste
    c.stamp(p, 'K')


def ox_head(c, HX, HY, S, k=1.4):
    x0, y0 = HX + 17, HY + 12

    def Q(dx, dy):
        return (x0 + dx * k, y0 + dy * k)

    def r(v):
        return v * k
    FUR = ('ox1', 'ox2', 'ox3'); FURF = ('ox0', 'ox1', 'ox2')
    for (pts, far) in (((Q(6, -7), Q(13, -12), Q(12, -19)), True), ((Q(0, -7), Q(6, -14), Q(-2, -20)), False)):
        p = C()
        a, b, t = pts
        horn = L(*a, r(2.0), *b, r(1.5)) | L(*b, r(1.5), *t, 0.7)
        p.form(horn, ('b1', 'b2', 'b3') if not far else ('b0', 'b1', 'b2'), sd=1, hl=1)
        tipm = L(*lerp(b, t, 0.5), r(1.0), *t, 0.7)
        p.fill(tipm & horn, 'b0')                                     # dunkle Hornspitze
        for f in (0.25, 0.55):
            p.pxs([lerp(a, b, f)], 'b0' if not far else 'K')
        c.stamp(p, 'K')
    p = C()
    skull = E(*Q(2, -2), r(8), r(7.4))
    face = L(*Q(-2, -2), r(6.4), *Q(-11, 7), r(5.0))
    muz = E(*Q(-12, 8), r(4.8), r(4.0))
    jaw = PG([Q(-15, 11), Q(-5, 11), Q(4, 5), Q(3, 11), Q(-9, 14)])
    neck = L(*Q(4, 4), r(6), *Q(8, 11), r(6))
    p.form(neck, FURF, sd=2, hl=0)
    p.form(jaw, FURF, sd=1, hl=1)
    head = skull | face
    p.form(head, FUR, sd=3, hl=1)
    p.form(muz, ('ox1', 'ox3', 'ox4'), sd=1, hl=1)
    p.fill(E(*Q(-15.5, 6.5), 1.6, 1.8), 'K')
    p.pxs([Q(-11.5, 6.5)], 'K')
    p.line([Q(-10, -2), Q(-5, 4)], 'ox1', only=face)
    for kk in range(5):                                              # krauses Stirnhaar
        p.line([Q(-4 + kk * 2.2, -9), Q(-5 + kk * 2.2, -4)], 'ox3' if kk % 2 else 'ox1', only=head)
    p.line([Q(-15, 10.5), Q(-6, 10.5)], 'ox0')
    c.stamp(p, 'K')
    p = C()
    p.fill(E(*Q(-4, 0), r(1.8), r(1.4)), 'K')
    p.fill(E(*Q(-4, 0.3), r(1.2), r(0.7)), 'e1')
    p.pxs([Q(-4.6, 0)], 'y3')
    p.line([Q(-7, -2), Q(-1, -3)], 'ox0')
    ear = E(*Q(9, -2), r(4.0), r(1.7))
    p.form(ear, FUR, sd=1, hl=1)
    p.fill(E(*Q(9, -1.7), r(2.2), 0.8), 'm1')
    rx, ry = Q(-14, 9)                                                # Nasenring
    p.line([(rx, ry), (rx - 1, ry + 3), (rx + 1, ry + 5), (rx + 4, ry + 4), (rx + 4, ry + 1)], 'y1')
    p.pxs([(rx - 1, ry + 3)], 'y2')
    c.stamp(p, 'K')


def horse_head(c, HX, HY, S, k=1.4):
    x0, y0 = HX + 17, HY + 11

    def Q(dx, dy):
        return (x0 + dx * k, y0 + dy * k)

    def r(v):
        return v * k
    FUR = ('hs1', 'hs2', 'hs3'); FURF = ('hs0', 'hs1', 'hs2')
    p = C()                                                            # ferne Ohr
    p.form(PG([Q(4, -6), Q(6, -14), Q(8, -6)]), FURF, sd=1, hl=0)
    c.stamp(p, 'K')
    p = C()
    neck = L(*Q(3, 2), r(6), *Q(8, 12), r(6.4))
    p.form(neck, FURF, sd=2, hl=0)
    skull = E(*Q(2, -2), r(6.4), r(6))
    face = L(*Q(-1, -2), r(5.4), *Q(-14, 7), r(4.0))                 # langer Nasenrücken
    muz = E(*Q(-15, 8), r(3.8), r(3.6))
    jaw = PG([Q(-17, 10), Q(-6, 10), Q(4, 4), Q(4, 9), Q(-6, 13), Q(-15, 13)])
    p.form(jaw, FURF, sd=1, hl=1)
    head = skull | face | muz
    p.form(head, FUR, sd=3, hl=1)
    p.form(E(*Q(2, 3), r(4), r(3.4)) & head, FUR, sd=1, hl=1)       # Ganasche
    p.fill(E(*Q(-17, 6.5), 1.4, 1.8), 'K')                            # Nüster
    p.line([Q(-16, 5), Q(-15, 7)], 'hs1')
    p.line([Q(-13, 1), Q(-5, -2)], 'hs1', only=face)                  # Nasenbein-Schatten
    mo = PG([Q(-18, 9.5), Q(-8, 9.5), Q(-8, 11), Q(-17, 11.5)])        # gefletschte Zähne
    p.fill(mo, 'q')
    p.fill(R(*Q(-17, 9.5), *Q(-9, 10)), 'b3')
    for xx in (-15, -13, -11):
        p.pxs([Q(xx, 10)], 'b1')
    c.stamp(p, 'K')
    p = C()
    p.fill(E(*Q(-3, -0.5), r(1.6), r(1.3)), 'K')
    p.fill(E(*Q(-3.2, -0.8), r(1.0), r(0.6)), 'e1')
    p.pxs([Q(-3.6, -1)], 'y3')
    p.line([Q(-6, -3), Q(0, -3.6)], 'hs0')
    ear = PG([Q(1, -6), Q(2, -15), Q(5, -6)])
    p.form(ear, FUR, sd=1, hl=1)
    p.line([Q(2.4, -7), Q(2.4, -12)], 'hs1', only=ear)
    for kk in range(3):                                               # Stirnlocke zwischen den Ohren
        p.form(L(*Q(1 + kk * 0.8, -6), r(0.9), *Q(-1 + kk * 0.6, -3.5), 0.5), ('h0', 'h1', 'h2'), sd=1, hl=1)
    c.stamp(p, 'K')


if KIND == 'gozu':
    for k_, v in zip(('r0', 'r1', 'r2', 'r3', 'r4'), ('#141428', '#2c3256', '#4c5a88', '#7a8cb8', '#b4c4e4')):
        col(k_, v)
    col('ox0', '#120a10'); col('ox1', '#2e1c1e'); col('ox2', '#553630'); col('ox3', '#86584a'); col('ox4', '#b48a74')
    add_rim('ox0 ox1 ox2', 'xs'); add_rim('r0 r1 r2 r3', 'xz')
    W.CFG.update(head=ox_head, weapon=lambda c, h, a: pole(c, h, a, kind='gozu'), mane=False, cloth=('m0', 'm1', 'm2'))
else:
    for k_, v in zip(('r0', 'r1', 'r2', 'r3', 'r4'), ('#2a0e18', '#5a2226', '#8c4434', '#bc744e', '#e8ae7e')):
        col(k_, v)
    col('hs0', '#221e30'); col('hs1', '#4e4a62'); col('hs2', '#8a869c'); col('hs3', '#c8c4d4')
    add_rim('hs0 hs1 hs2', 'xz'); add_rim('r0 r1 r2 r3', 'xs')
    W.CFG.update(head=horse_head, weapon=lambda c, h, a: pole(c, h, a, kind='mezu'), mane=True, cloth=('s0', 's1', 's2'))


def draw(**kw):
    return W.oni(**kw)


if __name__ == '__main__':
    common.D = os.path.dirname(os.path.abspath(__file__)) + '/'
    px.setsize(W.CW, W.CH)
    export(KIND, draw, W.WALK, W.ATTACK)
