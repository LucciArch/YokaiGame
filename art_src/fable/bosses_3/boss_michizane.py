"""Sugawara no Michizane – der verbannte Gelehrte, der als Donnergott (Karai Tenjin) zurückkehrt.
Blick nach links: schwarzes Sokutai des Ministers zur Rechten, Kanmuri mit steil aufragendem Ei, dünner langer Bart,
in der vorderen Hand das Shaku-Zepter, die hintere Hand ruft den Blitz. Er steht auf einer Gewitterwolke, hinter ihm
der Trommelkranz des Donners (Mitsudomoe), um ihn wehen rote Pflaumenblüten – Tobiume, der Baum, der ihm nach Dazaifu folgte."""
from lib3 import *

NAME = 'boss_michizane'
CW, CH = 230, 190
OX, OY = 74, 46            # lokale Fußlinie y=124

col('j0', '#08060e'); col('j1', '#181428'); col('j2', '#302a4c'); col('j3', '#5c5488')    # schwarzes Hofgewand, Lack-Glanz
px.add_rim('j1 j2', 'j3')
col('l0', '#10122a'); col('l1', '#262c54'); col('l2', '#46528a'); col('l3', '#8494c8')    # Gewitterwolke
px.add_rim('l1 l2', 'l3')
ROBE = ('j0', 'j1', 'j2')
CLOUD = ('l0', 'l1', 'l2')
CLOUDL = ('l1', 'l2', 'l3')
RED = ('m0', 'm1', 'm2')
SKIN = ('n2', 'n3', 'b3')            # bleich: das Antlitz eines Toten
BEARD = ('z1', 'z2', 'z3')
IVORY = ('b1', 'b2', 'b3')
GOLD = ('y0', 'y1', 'y2')
PLUM = ('o0', 'o1', 'o2')
DRUM = ('s1', 's2', 's3')


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, ph=0.0, sway=0, cloud=1.0, drums=0.0,
           nel=(22, 62), nwr=(10, 52), shaku=-60,
           fel=(66, 40), fwr=(74, 22), bolt=0.0, fx=None)


def drums(c, ph, rot):
    """Trommelkranz des Donnergottes: ein Halbring aus Taiko mit Mitsudomoe hinter den Schultern"""
    o = P(46, 34)
    p = C()
    ring = tube(curve([pol(o, 200 + 20 * i, 52) for i in range(8)], 6), 2.2, 2.2)
    p.form(ring, ('w0', 'w1', 'w2'), sd=1, hl=1)
    c.stamp(p, 'K')
    for i in range(7):
        a = 205 + 22 * i + rot * 6
        q = pol(o, a, 52)
        p = C()
        d = E(q[0], q[1], 8.4, 8.4)
        p.form(d, DRUM, sd=2, hl=1)
        p.fill(E(q[0], q[1], 6.0, 6.0), 'b2')
        p.fill(E(q[0] + 1, q[1] + 1, 6.0, 6.0) & ~E(q[0], q[1], 6.0, 6.0) & d, 'b1')
        for k in range(3):                                        # Mitsudomoe: drei Kommata, die sich jagen
            aa = a * 2 + k * 120 + ph * 30
            h = pol(q, aa, 2.6)
            p.fill(E(h[0], h[1], 1.8, 1.8), 'm1')
            p.fill(tongue(h, pol(q, aa + 70, 4.2), 1.2, 0.6, tr=0.3), 'm1')
        for k in range(6):
            p.px(*pol(q, k * 60 + 30, 7.4), 'y2')                  # Nagelköpfe am Fell
        c.stamp(p, 'K')


def cloud(c, ph, k, front):
    """Gewitterwolke unter dem Saum: dicke Ballen, unten zerrissen, Blitze zucken darin"""
    p = C()
    m = np.zeros((px.H, px.W), bool)
    balls = ((0, 118, 14), (16, 112, 16), (36, 116, 18), (58, 112, 17), (78, 118, 14), (94, 122, 10)) if not front \
        else ((14, 124, 11), (34, 126, 12), (56, 124, 11))
    for i, (x, y, r) in enumerate(balls):
        rr = r * k + math.sin(ph + i * 1.7)
        m |= E(*P(x, y), rr, rr * 0.72)
    for i in range(5 if not front else 3):
        x = 6 + i * 20 + (6 if front else 0)
        m |= tongue(P(x, 124), P(x + 4 * math.sin(ph + i), 130 + 2 * math.sin(ph * 2 + i)), 4.0, 2 * math.sin(ph + i), tr=0.6)
    ramp = CLOUD if not front else CLOUDL
    p.form(m, ramp, sd=3, hl=2)
    p.fill(erode(m, 3) & (p.a == I(ramp[1])) & ~sh(m, 0, 6), ramp[2])
    if not front:                                                # Blitz im Wolkeninneren
        a = P(30 + 20 * math.sin(ph), 112)
        b = add(a, (8, 10)); d = add(b, (-5, 6))
        p.line([a, b, d], 'y2', only=erode(m, 2))
    c.stamp(p, 'K')


def sleeve(c, sh_, el, wr, drop, ph, ramp):
    """weiter Hofärmel des Sokutai, rot gefüttert"""
    p = C()
    arm = L(*sh_, 6.0, *el, 7.0) | L(*el, 7.0, *wr, 7.5)
    w = math.sin(ph) * 1.5
    bag = PG([add(el, (6, 0)), add(el, (5 + w, drop - 4)), add(lerp(el, wr, .4), (4 + w, drop + 2)),
              add(lerp(el, wr, .7), (2 + w, drop + 4)), add(wr, (3, drop - 6)), add(wr, (-3, 6)), wr])
    m = arm | bag
    p.form(m, ramp, sd=3, hl=1)
    p.fill(m & ~sh(m, 0, -2) & sh(m, 0, -1), 'm1')                  # rotes Futter am Ärmelsaum
    for t in (.35, .7):
        q = lerp(el, wr, t)
        p.line([add(q, (2, 2)), add(q, (3 + w, drop - 4))], ramp[0], only=m)
    c.stamp(p, 'K')


def hand(c, wr, ang, open_=False):
    p = C()
    hp = pol(wr, ang, 4)
    p.form(E(hp[0], hp[1], 3.4, 3.0), SKIN, sd=1, hl=1)
    if open_:                                                   # gespreizte Finger, die den Blitz rufen
        for da in (-30, -10, 10, 30):
            p.fill(L(*pol(hp, ang + da, 2), 1.2, *pol(hp, ang + da, 7), 0.8), SKIN[1])
    c.stamp(p, 'K')


def shaku(c, o, ang):
    """Shaku: das Elfenbein-Zepter des Hofbeamten"""
    p = C()
    a, b = pol(o, ang + 180, 6), pol(o, ang, 20)
    p.form(L(*a, 2.2, *b, 2.6), IVORY, sd=1, hl=1)
    p.line([lerp(a, b, .2), lerp(a, b, .9)], 'b1')
    c.stamp(p, 'K')


def blossom(p, q, s=1.0):
    """Ume-Blüte: fünf runde Blätter, gelbe Mitte"""
    for k in range(5):
        h = pol(q, k * 72 - 90, 1.6 * s)
        p.fill(E(h[0], h[1], 1.3 * s, 1.3 * s), 'o1')
    p.px(*q, 'y2')


def bolt(c, wr, k):
    """Blitz aus der erhobenen Hand: gezackt nach oben, mit Seitenast"""
    p = C()
    pts = [wr]
    q = wr
    for i in range(5):
        q = add(q, (6 if i % 2 else -5, -7 * k))
        pts.append(q)
    m = np.zeros((px.H, px.W), bool)
    for a, b in zip(pts, pts[1:]):
        m |= L(*a, 2.0, *b, 1.4)
    m |= L(*pts[2], 1.2, *add(pts[2], (10, -4)), 0.6)
    m &= R(2, 2, px.W - 3, px.H - 3)
    p.fill(dil(m), 'y1')
    p.fill(m, 'y3')
    c.stamp(p, 'y0')


def michizane(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, ph, sw = S['bob'], S['lean'], S['ph'], S['sway']

    def U(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    drums(c, ph, S['drums'])
    cloud(c, ph, S['cloud'], False)

    # ---- Schleppe (Kyo): lange schwarze Bahn, weht hinter ihm über die Wolke nach rechts
    p = C()
    kyo = PG(curve([U((56, 74), .5), (P(80, 96)[0], P(80, 96)[1] + bob // 2), P(104 + sw, 104), P(116 + 2 * sw, 100), P(112 + sw, 110),
                     P(90, 112), U((54, 96), .3)], 4))
    p.form(kyo, ROBE, sd=3, hl=1)
    for t in (.3, .6):
        p.line([U((60, 80), .5), P(100 + sw, 104 + 4 * t)], 'j0', only=erode(kyo, 1))
    c.stamp(p, 'K')

    # ---- hinterer Arm, erhoben: ruft den Blitz
    sleeve(c, U((52, 40)), U(S['fel'], .6), P(*S['fwr']), 18, ph, ROBE)
    hand(c, add(P(*S['fwr']), (0, -3)), -80, True)
    if S['bolt']:
        bolt(c, add(P(*S['fwr']), (0, -8)), S['bolt'])

    # ---- Hakama (rot) unter dem Hō
    p = C()
    hk = PG([U((26, 82), .4), U((60, 82), .4), P(66 + sw, 116), P(52, 112), P(42 + sw, 118), P(30, 112), P(20 + sw, 116)])
    p.form(hk, RED, sd=3, hl=1)
    for x0, x1 in ((34, 30), (46, 44), (56, 60)):
        p.line([U((x0, 88), .4), P(x1 + sw, 112)], 'm0', only=hk)
    c.stamp(p, 'K')

    HX, HY = U((26, 2))

    def Hh(x, y):
        return (HX + x, HY + y)
    p = C()
    p.form(L(*Hh(13, 24), 2.6, *U((42, 36)), 3.0), ('n0', 'n1', 'n2'), sd=1, hl=0)   # Hals, im Kragen verborgen
    c.stamp(p, 'K')

    # ---- Hō: schwarzes, steifes Obergewand mit Ran (Saumborte) und Sekitai-Gürtel
    p = C()
    robe = PG([U((32, 36)), U((58, 36)), U((66, 54), .8), U((70, 80), .5), U((66, 92), .4), U((22, 92), .4),
               U((20, 70), .6), U((28, 48), .8)])
    p.form(robe, ROBE, sd=4, hl=1)
    ran = robe & ~sh(robe, 0, -4) & R(0, U((0, 86))[1], 999, 999)
    p.fill(ran, 'j2')
    for (a_, b_) in (((40, 56), (34, 90)), ((56, 58), (62, 90)), ((48, 40), (46, 66))):
        p.line([U(a_, .7), U(b_, .4)], 'j0', only=robe)
    # Karakusa-Muster: kleine Rauten im Stoff (Kreuzblumen-Wappen des hohen Rangs)
    for (x, y) in ((36, 70), (50, 74), (60, 70), (30, 80), (44, 84), (58, 84)):
        q = U((x, y), .5)
        p.fill(star(q[0], q[1], 2.2, 1.0, 4, 45) & erode(robe, 1), 'j2')
    # runder Kragen (Agekubi) mit rotem Untergewand im Ausschnitt
    p.fill(E(*U((44, 38)), 9, 4) & robe, 'j2')
    p.fill(E(*U((42, 40)), 6, 3) & robe, 'm1')
    belt = PG([U((28, 62), .8), U((62, 62), .8), U((62, 67), .7), U((28, 67), .7)])
    p.form(belt, ('i0', 'i1', 'i2'), sd=1, hl=1, only=robe)
    for x in (32, 40, 48, 56):
        p.fill(R(*U((x, 63), .75), *U((x + 2, 65), .75)), 'y1', only=belt)
    c.stamp(p, 'K')

    # ---- Kopf
    p = C()
    face = E(*Hh(12, 16), 8.6, 10.4) | E(*Hh(9, 22), 7.2, 6.4)
    p.form(face, SKIN, sd=2, hl=1)
    p.fill(E(*Hh(15, 20), 3.6, 3.0) & face, 'n2')                         # eingefallene Wange des Verbannten
    ear = E(*Hh(19, 16), 2.4, 4.0)
    p.form(ear, SKIN, sd=1, hl=1)
    # Augen: schmal, golden glühend wie Wetterleuchten; Brauen hart zusammengezogen
    for (ex, ey) in ((4, 14), (12, 14)):
        p.fill(R(*Hh(ex, ey), *Hh(ex + 4, ey + 1)), 'K')
        p.fill(R(*Hh(ex + 1, ey), *Hh(ex + 3, ey)), 'y2')
        p.px(*Hh(ex + 2, ey), 'y3')
    p.line([Hh(2, 11), Hh(8, 13)], 'K')
    p.line([Hh(11, 13), Hh(18, 10)], 'K')
    p.line([Hh(8, 9), Hh(9, 12)], 'n1')                                    # Zornesfalte
    p.line([Hh(2, 17), Hh(1, 21), Hh(3, 22)], 'n0')                        # Nase
    p.line([Hh(3, 25), Hh(8, 26)], 'q')                                    # verkniffener Mund
    c.stamp(p, 'K')
    # Haar und Kanmuri: schwarze Lackkappe, Koji (Haarköcher) hinten hoch, das Ei steht steif nach oben und wippt
    p = C()
    hair = E(*Hh(14, 7), 10, 5.6) & ~E(*Hh(6, 13), 7, 4)
    p.form(hair, ('h0', 'h1', 'h2'), sd=1, hl=1)
    cap = PG([Hh(4, 6), Hh(8, 0), Hh(22, -1), Hh(24, 6)]) | E(*Hh(16, -6), 4.4, 7.0)
    p.form(cap, ROBE, sd=2, hl=1)
    ei = tube(curve([Hh(18, -10), Hh(24, -24), Hh(32, -34 + 2 * math.sin(ph)), Hh(38 + sw, -40 + 2 * math.sin(ph + 1))], 5), 2.4, 1.8)
    p.form(ei, ROBE, sd=1, hl=1)
    p.fill(R(*Hh(5, 5), *Hh(23, 5)), 'j2', only=cap)
    c.stamp(p, 'K')

    # ---- vorderer Arm mit dem Shaku
    sleeve(c, U((34, 40)), U(S['nel'], .6), P(*S['nwr']), 24, ph + 1, ROBE)
    hand(c, add(P(*S['nwr']), (-3, 0)), 180)
    shaku(c, add(P(*S['nwr']), (-5, 0)), S['shaku'])

    # Bart: Schnurrbart in zwei dünnen Strähnen und ein langer, schmaler Kinnbart (wie auf den Tenjin-Bildern)
    p = C()
    beard = tongue(Hh(5, 27), Hh(4 + sw * .6, 46), 2.8, 1.4, tr=0.5)
    beard |= tongue(Hh(3, 24), Hh(-3, 33), 1.2, 1.0, tr=0.4) | tongue(Hh(7, 24), Hh(10, 33), 1.0, -0.8, tr=0.4)
    p.form(beard, BEARD, sd=1, hl=1)
    p.line([Hh(5, 30), Hh(4 + sw * .5, 42)], 'z1', only=beard)
    c.stamp(p, 'K')
    cloud(c, ph + 1, S['cloud'] * 0.9, True)

    # ---- Tobiume: rote Pflaumenblüten treiben um ihn
    p = C()
    for i, (x, y) in enumerate(((-6, 40), (4, 96), (78, 60), (88, 30), (70, 102), (-2, 70))):
        q = P(x + 3 * math.sin(ph + i), y + 2 * math.cos(ph * 1.3 + i))
        blossom(p, q, 1.0 if i % 2 else 1.3)
    c.stamp(p, 'o0')
    if S['fx']:
        S['fx'](c)
    c.blacken()
    return c


def fx_storm(k):
    """Blitzschlag: ein Strahl fährt vor ihm in die Wolke, Funken springen nach links"""
    def f(c):
        p = C()
        x = P(-6, 0)[0]
        pts = [(x, P(0, 20)[1])]
        for i in range(6):
            pts.append((x + (5 if i % 2 else -5) * k, pts[-1][1] + 16))
        m = np.zeros((px.H, px.W), bool)
        for a, b in zip(pts, pts[1:]):
            m |= L(*a, 1.8 * k, *b, 1.4 * k)
        m &= R(2, 2, px.W - 3, px.H - 3)
        p.fill(dil(m), 'y1')
        p.fill(m, 'y3')
        c.stamp(p, 'y0')
    return f


T = math.pi / 2
WALK = [dict(ph=0, bob=0, sway=0, drums=0.0), dict(ph=T, bob=-1, sway=1, drums=0.25, nwr=(10, 51)),
        dict(ph=2 * T, bob=-2, sway=2, drums=0.5, nwr=(10, 50)), dict(ph=3 * T, bob=-1, sway=1, drums=0.75, nwr=(10, 51))]
ATTACK = [
    dict(lean=3, bob=-2, ph=1, drums=1.0, cloud=1.1, fel=(66, 30), fwr=(70, 10), bolt=0.6, nel=(24, 56), nwr=(14, 46), shaku=-80),
    dict(lean=-4, bob=0, ph=2, drums=1.5, cloud=1.2, fel=(66, 30), fwr=(70, 10), bolt=1.0, nel=(18, 58), nwr=(2, 52),
         shaku=-150, fx=fx_storm(1.0), sway=2),
    dict(lean=-2, bob=0, ph=3, drums=2.0, cloud=1.05, fel=(66, 36), fwr=(72, 18), bolt=0.3, nel=(20, 60), nwr=(6, 52),
         shaku=-120, fx=fx_storm(0.5), sway=1),
]

if __name__ == '__main__':
    export(NAME, michizane, WALK, ATTACK)
