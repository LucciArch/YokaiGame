"""Yamauba – die Berghexe. Komplett neu (Runde 99): gebeugte alte Frau, wildes weißes Haar bis zur Hüfte,
zerlumpter brauner Kimono, knochige Arme mit Krallen, ein großes Küchenmesser (deba). Blick nach links.
Angriff: holt mit dem Messer aus und sticht nach vorn."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 104, 88
OX, OY = 30, 8                         # lokale Grundlinie y = 76
col('o0', '#3a2228'); col('o1', '#6e4a46'); col('o2', '#a07a66'); col('o3', '#c8a68a')   # alte, fahle Haut
add_rim('o0 o1 o2', 'xs')
SKIN = ('o1', 'o2', 'o3')
SKINF = ('o0', 'o1', 'o2')
HAIR = ('v1', 'v2', 'v3')
KIM = ('s1', 's2', 's3')
KIMF = ('s0', 's1', 's2')

LEG = dict(zip('abcdKeYqWwvxV', ['o0', 'o1', 'o2', 'o3', 'K', 'e1', 'y3', 'q', 'b3', 'v2', 'v1', 'v3', 'v0']))
HEAD = """
.......xxxwwwww.....
.....xxwwwwwwvwww...
....xwwwwwvvwwwwvw..
...xwwwwcddbwwwwwvw.
..xwwwcdddddbwwvwwv.
..wwwcddddccbbwwvwwv
..wwvKKKdcKKKbwwvwwv
..wvdeYKccceKbawvwwv
..wvdKKccbbKbaawvwwv
..KdddcccbbbaawwvwwV
.Kddddccbbbbaawvwwvv
Kdddccbbbbbaawwvwwv.
.KKccbbbabbaa.wvwwv.
...cKKKKKbaa..wvwv..
...KWqWqKbaa..wwvv..
...cKqqKbaa...wvw...
....cbbbba....vv....
.....cbba......v....
......ba............
"""
CLAW = """
.cc.
cddb
cccb
bbba
aKaK
K.K.
"""


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, ff=36, nf=50, flift=0, nlift=0,
           ksh=(34, 30), kel=(26, 40), khd=(18, 36), kang=150,      # Messerarm: Schulter, Ellbogen, Hand, Klingenwinkel
           fsh=(44, 31), fel=(40, 44), fhd=(32, 50), hair=0)


def knife(c, hd, ang):
    a = math.radians(ang)
    dx, dy = math.cos(a), -math.sin(a)
    p = C()
    butt = (hd[0] - dx * 5, hd[1] - dy * 5)
    p.form(L(*butt, 1.8, hd[0] + dx * 2, hd[1] + dy * 2, 1.8), ('w0', 'w1', 'w2'), sd=1, hl=1)
    b0 = (hd[0] + dx * 3, hd[1] + dy * 3)
    b1 = (hd[0] + dx * 17, hd[1] + dy * 17)
    nx, ny = -dy, dx
    if ny > 0:
        nx, ny = -nx, -ny
    blade = PG([(b0[0] - nx * 1.5, b0[1] - ny * 1.5), (b0[0] + nx * 4.5, b0[1] + ny * 4.5),
                (b1[0] + nx * 2.0, b1[1] + ny * 2.0), (b1[0] + dx * 2, b1[1] + dy * 2), (b1[0] - nx * 1.0, b1[1] - ny * 1.0)])
    p.form(blade, ('i1', 'i2', 'i3'), sd=1, hl=1)
    p.line([(b0[0] - nx * 1, b0[1] - ny * 1), (b1[0] - nx * 0.5, b1[1] - ny * 0.5)], 'i3', only=blade)
    c.stamp(p, 'K')


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    hs = S['hair']
    # ---- Haarmähne hinten: fällt über den gebeugten Rücken bis zur Hüfte
    p = C()
    mane = PG([B((30, 10)), B((44, 8)), B((52, 16)), B((58 + hs, 30)), B((60 + hs, 44)), B((56 + hs, 52)),
               B((52, 46)), B((50 + hs, 54)), B((46, 44)), B((44, 30)), B((36, 22))])
    p.form(mane, HAIR, sd=3, hl=1)
    for (a_, b_) in (((40, 12), (54 + hs, 40)), ((46, 14), (57 + hs, 46)), ((38, 18), (49 + hs, 48))):
        p.line([B(a_), B(b_)], 'v1', only=mane)
    p.line([B((42, 11)), B((52 + hs, 30))], 'v3', only=mane)
    c.stamp(p, 'K')
    # ---- ferner Arm (hängt nach vorn, Kralle)
    fs, fe, fh = B(S['fsh']), B(S['fel']), B(S['fhd'])
    p = C()
    p.form(L(*fs, 3.2, *fe, 2.4) | L(*fe, 2.4, *fh, 2.0), SKINF, sd=1, hl=0)
    p.form(E(fe[0], fe[1], 2.6, 2.4), SKINF, sd=1, hl=0)                  # knochiger Ellbogen
    c.stamp(p, 'K')
    p = C(); p.grid(int(fh[0]) - 2, int(fh[1]) - 1, CLAW, dict(LEG, c='o1', d='o2', b='o0', a='o0')); c.stamp(p, 'K')
    # ---- Beine: dünne, knochige Schienbeine unter dem Saum, nackte Füße
    for fx, lift, ramp in ((S['ff'], S['flift'], SKINF), (S['nf'], S['nlift'], SKIN)):
        p = C()
        kx, ky = P(fx + 3, 62 - lift)
        ax, ay = P(fx + 1, 73 - lift)
        p.form(L(kx, ky, 2.6, ax, ay, 1.9), ramp, sd=1, hl=1)
        p.form(E(kx - 1, ky + 1, 2.2, 2.0), ramp, sd=0, hl=1)                # Knie
        foot = PG([(ax + 2, ay - 1), (ax + 2, ay + 3), (ax - 7, ay + 3), (ax - 8, ay + 1), (ax - 3, ay - 1)])
        p.form(foot, ramp, sd=1, hl=1)
        for t in range(3):
            p.pxs([(ax - 8 + t * 2, ay + 3)], 'b2')                             # Zehennägel
        c.stamp(p, 'K')
    # ---- Kimono: gebeugter Oberkörper, zerfetzter Saum
    p = C()
    hem = [B((26, 62)), B((30, 66)), B((33, 63)), B((37, 67)), B((41, 63)), B((46, 68)), B((50, 64)), B((55, 67)), B((58, 62))]
    body = PG([B((32, 26)), B((40, 24)), B((48, 30)), B((54, 42)), B((58, 54))] + hem[::-1] + [B((28, 50)), B((28, 36))])
    p.form(body, KIM, sd=5, hl=1)
    for (a_, b_) in (((40, 34), (36, 64)), ((48, 40), (50, 64)), ((34, 40), (30, 60))):
        p.line([B(a_), B(b_)], 's1', only=body)                                  # Falten
    obi = PG([B((29, 44)), B((52, 40)), B((54, 45)), B((29, 49))]) & body
    p.form(obi, ('w0', 'w1', 'w2'), sd=1, hl=1)                                  # Strick als Gürtel
    for k in range(5):
        p.pxs([B((32 + k * 4, 46 - k * 0.8))], 'w0')
    for (x, y) in ((44, 54), (36, 57)):                                           # Risse im Stoff
        p.line([B((x, y)), B((x + 2, y + 3)), B((x + 1, y + 5))], 's0', only=body)
    # Kragen: Haut im Ausschnitt, weißes Untergewand
    neck = PG([B((32, 26)), B((38, 25)), B((36, 32)), B((33, 33))]) & body
    p.form(neck, SKIN, sd=1, hl=0)
    p.line([B((37, 25)), B((34, 34))], 'v2', only=body)
    c.stamp(p, 'K')
    # ---- Kopf: weit nach vorn gereckt
    p = C()
    p.grid(*B((14, 10)), HEAD, LEG)
    c.stamp(p, 'K', skip=('v1', 'v2', 'v3'))
    # ---- Messerarm vorn
    ks, ke, kh = B(S['ksh']), B(S['kel']), B(S['khd'])
    knife(c, kh, S['kang'])
    p = C()
    sleeve = L(*ks, 4.6, *ke, 4.0)
    p.form(sleeve, KIM, sd=2, hl=1)
    p.line([(ks[0] - 1, ks[1] + 2), (ke[0] + 1, ke[1] + 1)], 's1', only=sleeve)
    c.stamp(p, 'K')
    p = C()
    p.form(L(*ke, 2.4, *kh, 2.0), SKIN, sd=1, hl=1)                              # dürrer Unterarm
    p.form(E(kh[0], kh[1], 2.4, 2.2), SKIN, sd=1, hl=1)                          # Faust ums Heft
    p.pxs([(kh[0] - 1, kh[1] - 1), (kh[0] + 1, kh[1] - 1)], 'o1')
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(ff=34, nf=52, nlift=0), dict(bob=-1, ff=38, nf=48, flift=2, hair=1),
        dict(ff=42, nf=44), dict(bob=-1, ff=38, nf=48, nlift=2, hair=-1)]
ATTACK = [dict(lean=4, bob=1, ksh=(36, 30), kel=(38, 20), khd=(30, 14), kang=95, hair=2),          # ausholen
          dict(lean=-6, bob=-1, ksh=(32, 31), kel=(20, 34), khd=(8, 34), kang=178, hair=-2),        # Stich nach vorn
          dict(lean=-2, ksh=(34, 30), kel=(24, 38), khd=(16, 36), kang=160)]

if __name__ == '__main__':
    export('yamauba', draw, WALK, ATTACK)
