"""Taira no Masakado – das fliegende Haupt (Kubizuka-Sage).
Blick nach links: Der abgeschlagene Kopf des „Neuen Kaisers“ fliegt von Kyōto zurück nach Osten, um seinen Körper zu suchen.
Die Augen offen und glühend, die Zähne gefletscht, das Haar weht hinter ihm her; vom Helm sind nur die vergoldeten
Kuwagata und die zerrissenen Shikoro-Lamellen geblieben. In der Schläfe steckt noch der Pfeil, der ihn tötete.
Unter dem Halsstumpf tropft Blut, dahinter zieht ein bleiches Onibi."""
from lib3 import *

NAME = 'boss_masakado'
CW, CH = 230, 166
OX, OY = 16, 28

col('u0', '#0e1a3a'); col('u1', '#1c4c86'); col('u2', '#3ea2d2'); col('u3', '#b4ecf2')   # bleiches Groll-Feuer (Onibi)
px.add_rim('u0 u1', 'u3')
FIRE = ('u0', 'u1', 'u2')
SKIN = ('n0', 'n1', 'n2')
HAIR = ('h0', 'hb', 'h2')
IRON = ('i0', 'i1', 'i2')
GOLD = ('y0', 'y1', 'y2')
LACE = ('m0', 'm1', 'm2')


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, tilt=0, ph=0.0, mouth=0, glare=0, fire=1.0, fx=None)


def onibi(c, ph, k):
    """Schweif aus bleichem Groll-Feuer: Zungen ziehen nach rechts hinten, der Kern glüht weiß"""
    p = C()
    m = np.zeros((px.H, px.W), bool)
    for i in range(7):
        y = 34 + i * 11
        ln = (52 + 26 * ((i * 5) % 3) / 2 + 8 * math.sin(ph * 2 + i * 1.3)) * k
        b = P(96, y)
        m |= tongue(b, P(96 + ln, y - 14 + 6 * math.sin(ph + i)), 5.0 - abs(i - 3) * 0.5, 6 * math.sin(ph + i * 2), tr=0.5)
    m |= E(*P(86, 64), 40, 46)                             # Aura um das ganze Haupt
    p.form(m, FIRE, sd=3, hl=1, sdir=(-1, 1))
    p.fill(erode(m, 4) & (p.a == I('u1')), 'u2')
    p.fill(erode(m, 7) & (p.a == I('u2')), 'u3')
    c.stamp(p, 'u0')


def hair(c, ph, U):
    """Langes, gelöstes Haar: weht in schweren Strähnen hinter dem Kopf her"""
    p = C()
    m = E(*U((86, 52)), 24, 24)
    for i, (y, ln) in enumerate(((30, 58), (40, 74), (52, 80), (64, 70), (76, 54), (86, 38))):
        w = 3 * math.sin(ph * 1.5 + i)
        m |= tongue(U((84, y)), U((84 + ln, y + 4 + w + (i - 2) * 3)), 5.4 - i * 0.4, 4 * math.sin(ph + i * 1.7), tr=0.8)
    p.form(m, HAIR, sd=3, hl=1)
    for i, y in enumerate((36, 48, 60, 72)):
        p.line(curve([U((96, y)), U((120, y + 3 + math.sin(ph + i) * 2)), U((140, y + 6))], 4), 'h2', only=erode(m, 1))
    c.stamp(p, 'K')


def shikoro(c, U):
    """Zerrissener Nackenschutz: vier Reihen lackierter Lamellen mit roter Verschnürung, zwei Reihen abgerissen"""
    p = C()
    for r in range(4):
        y0 = 46 + r * 9
        x0, x1 = 84 + r * 3, 114 + r * 6 - (10 if r == 3 else 0)
        row = PG([U((x0, y0)), U((x1, y0 + 4)), U((x1 - 2, y0 + 11)), U((x0 + 2, y0 + 8))])
        if r == 2:
            row &= ~R(*U((100, y0)), *U((108, y0 + 14)))          # ausgerissenes Stück
        p.form(row, IRON, sd=2, hl=1)
        p.line([U((x0 + 2, y0 + 8)), U((x1 - 2, y0 + 11))], 'i0', only=row)
        for x in range(x0 + 4, x1 - 2, 5):
            p.fill(R(*U((x, y0 + 3 + (x - x0) * 4 // max(1, x1 - x0))), *U((x, y0 + 6 + (x - x0) * 4 // max(1, x1 - x0)))), 'm2', only=row)
    c.stamp(p, 'K')


def arrow(c, U):
    """Der Pfeil in der Schläfe: Schaft schräg nach rechts oben, weiße Adlerfedern am Ende"""
    p = C()
    a, b = U((86, 50)), U((132, 18))
    p.form(L(*a, 1.4, *b, 1.4), ('w0', 'w1', 'w2'), sd=1, hl=1)
    for s in (-1, 1):
        f = PG([lerp(a, b, 0.78), lerp(a, b, 1.0), add(lerp(a, b, 0.96), (4 * s, 4 * s)), add(lerp(a, b, 0.80), (4 * s, 4 * s))])
        p.form(f, ('v0', 'v1', 'v2'), sd=1, hl=1)
        p.line([lerp(a, b, 0.84), add(lerp(a, b, 0.88), (3 * s, 3 * s))], 'K', only=f)
    c.stamp(p, 'K')


def kuwagata(c, U, ph):
    """Vergoldete Helmhörner, aus dem zerschlagenen Helm übrig, mit Drachen-Kuwagata-Dai in der Mitte"""
    p = C()
    m = tube(curve([U((56, 30)), U((44, 18)), U((40, 2)), U((44, -10))], 5), 3.4, 1.2)
    m |= tube(curve([U((66, 28)), U((70, 14)), U((78, 0)), U((88, -8))], 5), 3.4, 1.2)
    p.form(m, GOLD, sd=2, hl=1)
    dai = PG([U((52, 30)), U((70, 26)), U((72, 32)), U((54, 36))])
    p.form(dai, ('s1', 's2', 's3'), sd=1, hl=1)
    p.form(star(*U((61, 30)), 4.4, 1.6, 4, 45), GOLD, sd=1, hl=1)
    c.stamp(p, 'K')


def masakado(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, tl, ph = S['bob'], S['tilt'], S['ph']

    def U(pt, k=1.0):
        # tilt: Kopf neigt sich (oben weiter nach links), Bob: auf und ab
        return P(pt[0] - tl * (70 - pt[1]) / 30 * k, pt[1] + bob)

    onibi(c, ph, S['fire'])
    hair(c, ph, U)
    shikoro(c, U)

    # ---- Halsstumpf: zerfetztes Fleisch, Blut tropft und zieht in Fäden nach hinten
    p = C()
    neck = E(*U((74, 90)), 12, 9)
    p.form(neck, SKIN, sd=2, hl=0)
    cut = PG([U((60, 96)), U((66, 92)), U((74, 96)), U((80, 92)), U((88, 96)), U((84, 102)), U((66, 103))])
    p.form(cut, ('r0', 'r1', 'r2'), sd=1, hl=1)
    p.fill(E(*U((75, 98)), 2.4, 1.6), 'b2')                          # Wirbel
    for i, x in enumerate((66, 78)):
        d = 6 + 4 * i + 2 * math.sin(ph * 2 + i)
        p.fill(tongue(U((x, 102)), U((x + 3, 102 + d)), 1.2, 0.5, tr=0.6), 'r1')
        p.fill(E(*U((x + 3, 104 + d)), 1.4, 1.6), 'r2')                    # Tropfen
    c.stamp(p, 'K')

    # ---- Schädel und Gesicht (Dreiviertelansicht nach links)
    p = C()
    skull = E(*U((76, 56)), 25, 27)
    face = skull | E(*U((60, 66)), 20, 24) | PG([U((40, 64)), U((52, 46)), U((60, 90)), U((48, 86))])
    p.form(face, SKIN, sd=4, hl=1)
    p.fill(E(*U((66, 74)), 6, 7) & face, 'n1')                        # eingefallene Wange
    p.fill(E(*U((88, 70)), 8, 12) & face & ~E(*U((86, 66)), 6, 8), 'n1')
    # Ohr
    ear = E(*U((86, 64)), 4.4, 7)
    p.form(ear, SKIN, sd=1, hl=1)
    p.line([U((86, 60)), U((85, 68))], 'n1', only=ear)
    # Brauen: schwer, zusammengezogen
    p.fill(PG([U((40, 52)), U((54, 54)), U((56, 58)), U((44, 58))]), 'h1')
    p.fill(PG([U((60, 50)), U((76, 46)), U((78, 50)), U((62, 56))]), 'h1')
    p.line([U((56, 50)), U((58, 46))], 'n1')                            # Zornesfalte
    # Augen offen, golden glühend (die Sage: das Haupt verweste nicht, die Augen blieben offen)
    g = S['glare']
    for (ex, ey, w) in ((45, 59, 7), (62, 58, 9)):
        e = PG([U((ex, ey + 2)), U((ex + w // 2, ey)), U((ex + w, ey + 1)), U((ex + w // 2, ey + 4))])
        p.fill(dil(e), 'K')
        p.fill(e, 'y2')
        p.fill(R(*U((ex + w // 2 - 1, ey + 1)), *U((ex + w // 2, ey + 2))), 'e0')
        if g:
            p.px(*U((ex + w // 2 - 1, ey + 1)), 'y3')
    # Nase: kräftig, nach links
    p.form(PG([U((48, 60)), U((38, 72)), U((44, 76)), U((52, 74))]), SKIN, sd=1, hl=1)
    p.line([U((40, 74)), U((46, 76))], 'n0')
    # Mund: gefletschte Zähne, beim Angriff weit aufgerissen
    mo = S['mouth']
    mouth = PG([U((40, 80)), U((62, 80)), U((60, 86 + mo)), U((42, 85 + mo))])
    p.fill(dil(mouth) & face, 'n0')
    p.fill(mouth, 'q')
    for x in range(42, 61, 3):
        p.fill(R(*U((x, 80)), *U((x + 1, 82))), 'b2')
        p.fill(R(*U((x, 84 + mo)), *U((x + 1, 85 + mo))), 'b1')
    if mo:
        p.fill(E(*U((51, 84 + mo // 2)), 4, 1.5) & mouth, 'm1')    # Zunge
    # Narbe quer über die Wange
    p.line([U((68, 66)), U((76, 78))], 'n0', only=face)
    c.stamp(p, 'K')

    # gelöstes Haar fällt über den Hinterkopf (der Helm ist zerschlagen)
    p = C()
    back = (E(*U((88, 52)), 18, 20) | PG([U((72, 42)), U((100, 38)), U((104, 70)), U((94, 84)), U((90, 64))])) & ~E(*U((86, 64)), 5.4, 8)
    p.form(back, HAIR, sd=3, hl=1)
    for i in range(3):
        p.line(curve([U((80 + i * 6, 44)), U((88 + i * 5, 58)), U((92 + i * 4, 76))], 4), 'h2', only=erode(back, 1))
    c.stamp(p, 'K')

    # Schnurrbart und kurzer, struppiger Kinnbart
    p = C()
    beard = np.zeros((px.H, px.W), bool)
    for (bx, by, ex_, ey_) in ((50, 78, 38, 84), (54, 78, 62, 82), (48, 88, 46, 96), (54, 89, 56, 98)):
        beard |= tongue(U((bx, by)), U((ex_, ey_ + (mo if by > 84 else 0))), 2.2, 0.8, tr=0.6)
    p.form(beard, HAIR, sd=1, hl=1)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))

    # ---- Stirnhaar und zerschlagene Helmschale
    p = C()
    bowl = PG([U((50, 44)), U((62, 32)), U((82, 28)), U((100, 36)), U((104, 46)), U((90, 44)), U((74, 40))])
    p.form(bowl, IRON, sd=2, hl=1)
    for x in (66, 76, 86, 96):
        p.line([U((x, 32)), U((x - 4, 42))], 'i0', only=bowl)
        p.px(*U((x - 1, 36)), 'i3')
    p.fill(R(*U((84, 28)), *U((92, 34))) & bowl, 'K')                  # Bruchkante
    p.form(PG([U((50, 44)), U((74, 40)), U((90, 44)), U((88, 48)), U((52, 48))]), LACE, sd=1, hl=1)   # Stirnband
    c.stamp(p, 'K')
    kuwagata(c, U, ph)
    arrow(c, U)

    if S['fx']:
        S['fx'](c, U)
    c.blacken()
    return c


def fx_shout(k):
    """Der Schrei des Hauptes: „Wo ist mein Körper? Kommt, schlagt noch einmal!“ – Schallbögen nach links"""
    def f(c, U):
        p = C()
        for i in range(3):
            r = 10 + i * 9 + 10 * k
            ring = E(*U((44, 82)), r, r * 1.2) & ~E(*U((44, 82)), r - 2, r * 1.2 - 2) & R(0, 0, U((38, 0))[0], 999)
            p.fill(ring & R(2, 2, px.W - 3, px.H - 3), 'u3' if i % 2 else 'u2')
        c.stamp(p, 'u0')
    return f


T = math.pi / 2
WALK = [dict(ph=0, bob=0), dict(ph=T, bob=-1, tilt=1), dict(ph=2 * T, bob=-2, tilt=2), dict(ph=3 * T, bob=-1, tilt=1)]
ATTACK = [
    dict(ph=1, bob=-2, tilt=-3, mouth=2, glare=1, fire=1.2),
    dict(ph=2, bob=0, tilt=3, mouth=5, glare=1, fire=1.4, fx=fx_shout(1.0)),
    dict(ph=3, bob=0, tilt=2, mouth=3, glare=1, fire=1.2, fx=fx_shout(0.4)),
]

if __name__ == '__main__':
    export(NAME, masakado, WALK, ATTACK)
