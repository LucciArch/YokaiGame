"""Sutoku-in – der verbannte Kaiser, der als großer Onryō und König der Tengu zurückkehrt (Hōgen-Aufstand, Shiramine).
Blick nach links: schwarze Tengu-Schwingen, verwilderte Haare und Bart unter der schief sitzenden Kanmuri,
zerschlissenes Hofgewand über kaiserlichem Purpur, lange Nägel, in der vorderen Hand die mit Blut geschriebenen Sutren.
Er schwebt über dem Groll-Feuer."""
from lib3 import *

NAME = 'boss_sutoku'
CW, CH = 230, 162
OX, OY = 74, 30            # lokale Fußlinie y=126

col('f0', '#0a0a1c'); col('f1', '#1c1c3a'); col('f2', '#363a66'); col('f3', '#6a72a8')   # Rabenfedern, blauschwarz
px.add_rim('f1 f2', 'f3')
WH = ('z1', 'z2', 'z3')
WHD = ('z0', 'z1', 'z2')
PUR = ('p0', 'p1', 'p2')
FIRE = ('r1', 'r2', 'r3')
SKIN = ('n1', 'n2', 'n3')
HAIR = ('h0', 'hb', 'h2')
FEA = ('f1', 'f2', 'f3')
FEAD = ('f0', 'f1', 'f2')
NAIL = ('b1', 'b2', 'b3')


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, ph=0.0, sway=0, wing=0.0, fire=1.0,
           nel=(24, 60), nwr=(10, 62), scr=1.0,
           fel=(70, 46), fwr=(78, 30), fx=None)


def wing(c, root, ang, span, ph, ramp, back, sg=1):
    """Tengu-Schwinge: geschlossene Fläche vom Knochenbogen bis zur gezackten Hinterkante, drei Federlagen"""
    p = C()
    el = pol(root, ang, span * 0.42)
    tip = pol(el, ang - 28 * sg, span * 0.58)

    def base(t):
        return lerp(root, el, t * 2) if t < 0.5 else lerp(el, tip, (t - 0.5) * 2)
    n = 8
    tips = []
    for i in range(n + 1):
        t = i / n
        fa = ang + sg * (100 - 75 * t) + 4 * math.sin(ph + i)        # Federn hängen nach unten, zur Spitze hin nach außen
        tips.append(pol(base(t), fa, span * (0.30 + 0.32 * t)))
    m = PG([root, el, tip] + [lerp(base(i / n), q, 0.62) for i, q in enumerate(tips)][::-1])
    for i, q in enumerate(tips):
        m |= tongue(base(i / n), q, 3.4, 1.0 * math.sin(ph + i), tr=0.5)
    m |= tube(curve([root, el, tip], 6), 4.4, 1.8)
    p.form(m, ramp, sd=3, hl=1)
    # mittlere Lage (Armschwingen) und Deckfedern am Knochen: hellere, kürzere Schuppen
    mid = np.zeros_like(m)
    for i in range(n + 1):
        t = i / n
        mid |= tongue(base(t), pol(base(t), ang + sg * (96 - 70 * t), span * (0.17 + 0.16 * t)), 4.0, 0.6, tr=1.4)
    p.form(mid & m, ramp, sd=2, hl=1)
    cov = np.zeros_like(m)
    for i in range(n + 1):
        t = i / n
        cov |= E(*pol(base(t), ang + sg * 90, 3), 4.2, 3.4)
    p.form(cov & m, (ramp[1], ramp[2], 'f3'), sd=1, hl=1)
    for i, q in enumerate(tips):
        b0 = base(i / n)
        p.line([lerp(b0, q, 0.35), lerp(b0, q, 0.92)], ramp[0], only=m)
    p.form(tube(curve([root, el, tip], 6), 2.6, 1.2), (ramp[0], ramp[1], ramp[2]), sd=1, hl=1)
    c.stamp(p, 'K')


def fire(c, ph, k, front):
    """Groll-Feuer: dunkelrote Zungen unter dem schwebenden Saum und hinter dem Rücken"""
    p = C()
    m = np.zeros((px.H, px.W), bool)
    xs = (8, 20, 34, 48, 60, 72, 84) if not front else (16, 30, 44, 58)
    for i, x in enumerate(xs):
        h = (14 + 10 * ((i * 3 + (1 if front else 0)) % 4) / 3 + 3 * math.sin(ph * 2 + i * 1.9)) * k
        if not front and 2 <= i <= 4:
            h += 30 * k                                    # hinter dem Rücken lodert es hoch
        b = P(x, 126)
        m |= E(b[0], b[1] - 2, 5.6, 3.2)
        m |= tongue((b[0], b[1] - 2), (b[0] + 4 * math.sin(ph + i), b[1] - h * (0.6 if front else 1)), 3.6, 3 * math.sin(ph + i * 2), tr=0.6)
    m &= R(0, 0, 999, OY + 127)
    p.form(m, FIRE, sd=2, hl=1)
    p.fill(m & ~sh(m, 0, -3) & sh(m, 0, -1), 'r0')
    p.fill(erode(m, 2) & (p.a == I('r2')) & ~sh(m, 0, 6), 'r4')
    c.stamp(p, 'r0')


def sleeve(c, sh_, el, wr, drop, ph, ramp):
    """weiter Hofärmel, zerschlissen, purpur gefüttert"""
    p = C()
    arm = L(*sh_, 6.0, *el, 7.0) | L(*el, 7.0, *wr, 7.5)
    w = math.sin(ph) * 1.5
    bag = PG([add(el, (6, 0)), add(el, (5 + w, drop - 4)), add(lerp(el, wr, .35), (4 + w, drop + 2)), add(lerp(el, wr, .55), (1, drop - 6)),
              add(lerp(el, wr, .75), (2 + w, drop + 4)), add(wr, (3, drop - 8)), add(wr, (-3, 6)), wr])
    m = arm | bag
    p.form(m, ramp, sd=3, hl=1)
    p.fill(m & ~sh(m, 0, -2) & sh(m, 0, -1), 'p1')
    for t in (.3, .65):
        q = lerp(el, wr, t)
        p.line([add(q, (2, 2)), add(q, (3 + w, drop - 4))], ramp[0], only=m)
    c.stamp(p, 'K')


def claw(c, wr, ang, spread=26, ln=9.0):
    """hagere Hand, lange gelbliche Nägel – in der Verbannung nie geschnitten"""
    p = C()
    hp = pol(wr, ang, 5)
    p.form(E(hp[0], hp[1], 3.4, 3.0), SKIN, sd=1, hl=1)
    for da in (-spread, -spread / 3, spread / 3, spread):
        k1 = pol(hp, ang + da, ln * 0.5)
        tip = pol(k1, ang + da * 0.4 + 20, ln * 0.45)
        p.fill(tube([hp, k1, tip], 1.4, 1.0), SKIN[1])
        e = pol(tip, ang + da * 0.4 + 40, 4.5)
        p.fill(L(tip[0], tip[1], 1.0, e[0], e[1], 0.4), 'b2')
        p.px(*e, 'b3')
    c.stamp(p, 'K')


def scroll(c, o, k, ph):
    """Sutren in Blut: aufgerollte Schriftrolle, Spalten roter Schrift, unten das lose Ende im Wind"""
    p = C()
    w, h = 18 * k, 26
    sheet = PG([(o[0] - w, o[1] - 4), (o[0] + 2, o[1] - 6), (o[0] + 3, o[1] + h), (o[0] - w + 2 + 2 * math.sin(ph), o[1] + h + 3)])
    p.form(sheet, ('c1', 'c2', 'v2'), sd=2, hl=1)
    cols_ = int(w // 4)
    for i in range(cols_):
        x = o[0] - 2 - i * 4
        for j in range(0, int(h) - 3, 3):
            if (i * 7 + j) % 5:
                p.fill(R(x - 1, o[1] - 2 + j, x, o[1] - 1 + j), 'm1' if (i + j) % 3 else 'e0', only=erode(sheet, 1))
    rod = L(o[0] + 2, o[1] - 8, 1.8, o[0] + 3, o[1] + h + 2, 1.8)
    p.form(rod, ('w0', 'w1', 'w2'), sd=1, hl=1)
    for y in (o[1] - 9, o[1] + h + 3):
        p.form(E(o[0] + 2.5, y, 2.2, 1.6), ('y0', 'y1', 'y2'), sd=1, hl=1)
    c.stamp(p, 'K')


def sutoku(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, ph, sw = S['bob'], S['lean'], S['ph'], S['sway']

    def U(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    # ---- Schwingen hinter allem: die hintere weit nach rechts oben, die vordere hinter dem Kopf nach links oben
    wa = S['wing']
    wing(c, U((60, 40)), -24 - 10 * wa, 62, ph, FEAD, True)
    fire(c, ph, S['fire'], False)
    wing(c, U((50, 38)), -146 + 10 * wa, 50, ph + 1, FEA, False, -1)
    if S['fx']:
        S['fx'](c, 0)

    # ---- Haar: verwildert, fällt bis über die Hüfte, Strähnen stehen ab
    p = C()
    hp = [(30, 8), (50, 4), (62, 12), (68, 30), (74, 52), (80 + sw, 76), (84 + sw, 92), (74 + sw, 86), (70 + sw, 94),
          (64, 76), (58, 56), (46, 34)]
    hair = PG(curve([U(q, max(0, 1 - q[1] / 100)) for q in hp], 4))
    for (a_, b_) in (((70, 46), (82, 50)), ((76, 66), (88 + sw, 74))):
        hair |= tongue(U(a_), U(b_), 3.0, 2, tr=0.8)
    p.form(hair, HAIR, sd=4, hl=0)
    for a_, b_ in (((56, 12), (66, 44)), ((64, 40), (78 + sw, 84)), ((60, 24), (70, 60))):
        p.line([U(a_, .5), U(b_, .2)], 'h2', only=hair)
    c.stamp(p, 'K')

    # ---- hinterer Arm, erhoben, Krallen gespreizt
    sleeve(c, U((54, 42)), U(S['fel'], .6), P(*S['fwr']), 16, ph, WHD)
    claw(c, add(P(*S['fwr']), (0, -4)), -80, 30)

    # ---- Gewand: Purpur darunter, zerschlissener heller Hō darüber, der Saum schwebt und zerfasert ins Feuer
    p = C()
    hem = [(70, 108), (66 + sw, 118), (58, 112), (50 + sw, 120), (42, 112), (34 + sw, 119), (26, 110), (20 + sw, 116), (16, 104)]
    under = PG([U((28, 62), .7), U((64, 62), .7)] + [P(*q) for q in hem])
    p.form(under, PUR, sd=4, hl=1)
    for (x0, x1) in ((34, 26), (44, 40), (54, 54), (62, 66)):
        p.line([U((x0, 68), .6), P(x1 + sw, 112)], 'p0', only=under)
    c.stamp(p, 'K')
    p = C()
    robe = PG([U((32, 36)), U((58, 36)), U((66, 54), .8), U((72, 82), .5), U((74, 100), .3), U((66, 94), .3), U((62, 104), .3),
               U((56, 72), .6), U((38, 72), .6), U((32, 96), .3), U((24, 92), .3), U((18, 102), .3), U((20, 76), .5), U((28, 50), .8)])
    p.form(robe, WH, sd=4, hl=1)
    for (a_, b_) in (((38, 74), (26, 98)), ((58, 76), (68, 98)), ((62, 56), (70, 84)), ((44, 40), (40, 66))):
        p.line([U(a_, .6), U(b_, .3)], 'z1', only=robe)
    # Risse, Brandflecken und Blutspritzer im Stoff
    for (x, y, rx, ry) in ((64, 86, 2.4, 3.6), (24, 86, 2.2, 3.2), (52, 48, 1.6, 2.2)):
        hole = E(*U((x, y), .5), rx, ry) & robe
        p.fill(hole, 'p0')
        p.fill(dil(hole) & ~hole & robe, 'z0')
    for (x, y) in ((40, 50), (46, 56), (36, 60), (60, 66)):
        p.fill(E(*U((x, y), .8), 1.2, 1.2), 'r1', only=robe)
    p.fill(robe & ~sh(robe, 0, -3) & R(0, OY + 84, 999, 999), 'r1')       # Saum vom Feuer angesengt
    # Kragen (Agekubi) und Gürtel mit Jade
    p.line([U((38, 36)), U((44, 52), .9)], 'p2', only=robe)
    p.line([U((52, 36)), U((44, 52), .9)], 'p2', only=robe)
    belt = PG([U((30, 60), .8), U((60, 60), .8), U((60, 66), .7), U((30, 66), .7)])
    p.form(belt, ('s0', 's1', 's2'), sd=1, hl=1, only=robe)
    for x in (36, 45, 54):
        p.fill(R(*U((x, 62), .75), *U((x + 2, 63), .75)), 'y1', only=belt)
    c.stamp(p, 'K')

    # ---- Kopf
    HX, HY = U((24, 4))

    def Hh(x, y):
        return (HX + x, HY + y)
    p = C()
    p.form(L(*Hh(14, 24), 3.6, *U((44, 38)), 4.4), ('n0', 'n1', 'n2'), sd=1, hl=0)   # Hals
    c.stamp(p, 'K')
    p = C()
    back = E(*Hh(20, 14), 12.4, 12.6)
    p.form(back, HAIR, sd=3, hl=0)
    c.stamp(p, 'K')
    p = C()
    face = E(*Hh(12, 15), 8.8, 10.6) | E(*Hh(9, 21), 7.6, 6.8)
    p.form(face, SKIN, sd=2, hl=1)
    p.fill(E(*Hh(14, 19), 4.0, 3.0) & face, 'n1')                         # eingefallene Wange
    # Augen: weit, rot glühend, Brauen zusammengezogen
    for (ex, ey) in ((4, 13), (13, 13)):
        p.fill(R(*Hh(ex, ey), *Hh(ex + 4, ey + 2)), 'K')
        p.fill(R(*Hh(ex + 1, ey + 1), *Hh(ex + 2, ey + 1)), 'e1')
        p.px(*Hh(ex + 1, ey + 1), 'y3')
    p.line([Hh(3, 11), Hh(9, 12)], 'K')
    p.line([Hh(12, 12), Hh(18, 10)], 'K')
    p.line([Hh(2, 17), Hh(3, 21)], 'n0')                                   # Nase
    p.line([Hh(4, 11), Hh(5, 10)], 'n1')                                   # Zornesfalten
    # aufgerissener Mund mit Zähnen
    mo = PG([Hh(2, 24), Hh(10, 23), Hh(9, 28), Hh(3, 28)])
    p.fill(mo, 'q')
    p.fill(R(*Hh(3, 24), *Hh(9, 24)), 'b2')
    p.pxs([Hh(4, 27), Hh(7, 27)], 'b2')
    c.stamp(p, 'K')
    # Bart: struppig, in Strähnen nach unten
    p = C()
    beard = np.zeros((px.H, px.W), bool)
    for (bx, by, ex_, ey_) in ((2, 28, 0, 42), (6, 29, 6, 46), (10, 28, 12, 42), (14, 25, 18, 38)):
        beard |= tongue(Hh(bx, by), Hh(ex_ + sw * .5, ey_), 2.6, 1.0, tr=0.6)
    beard |= L(*Hh(1, 23), 1.2, *Hh(10, 22), 1.0)
    p.form(beard, ('h1', 'h2', 'xh'), sd=1, hl=1)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # Haare über der Stirn, abstehende Strähnen
    p = C()
    fringe = (E(*Hh(14, 6), 12.4, 7.0) & ~E(*Hh(6, 14), 8.4, 5.4))
    fringe |= tube(curve([Hh(2, 6), Hh(-4, 14), Hh(-6, 26)], 5), 2.4, 0.7)
    fringe |= tube(curve([Hh(22, 8), Hh(26, 24), Hh(24, 40)], 5), 3.0, 1.0)
    p.form(fringe, HAIR, sd=2, hl=0)
    p.line([Hh(6, 2), Hh(14, 0), Hh(22, 3)], 'h2', only=fringe)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # Kanmuri: schwarze Hofkappe, schief nach hinten gerutscht, das steife Ei-Band weht hoch
    p = C()
    cap = PG([Hh(6, 3), Hh(22, -3), Hh(27, 2), Hh(12, 7)]) | E(*Hh(19, -6), 5.0, 7.0)
    p.form(cap, ('f1', 'f2', 'f3'), sd=2, hl=1)
    ei = tube(curve([Hh(20, -6), Hh(30, -14), Hh(42, -12 + 2 * math.sin(ph)), Hh(52, -18 + 3 * math.sin(ph + 1))], 5), 2.0, 1.6)
    p.form(ei, ('f0', 'f1', 'f2'), sd=1, hl=1)
    p.fill(R(*Hh(9, 3), *Hh(22, 3)), 'y0', only=cap)
    c.stamp(p, 'K')

    # ---- vorderer Arm mit den Blut-Sutren
    if S['scr']:
        scroll(c, add(P(*S['nwr']), (-4, -6)), S['scr'], ph)
    sleeve(c, U((34, 42)), U(S['nel'], .6), P(*S['nwr']), 22, ph + 1, WH)
    claw(c, add(P(*S['nwr']), (-4, -1)), 170, 22, 7.0)

    fire(c, ph + 1, S['fire'] * 0.8, True)
    if S['fx']:
        S['fx'](c, 1)
    c.blacken()
    return c


def fx_curse(k):
    """Fluchschrift: rote Zeichen lösen sich von der Rolle und fliegen in einem Bogen nach links"""
    def f(c, layer):
        if layer != 1:
            return
        p = C()
        o = P(-4, 54)
        for i in range(7):
            a = 150 + i * 10
            q = pol(o, a, 10 + 36 * k + (i % 2) * 6)
            gl = R(q[0] - 1, q[1] - 2, q[0] + 1, q[1] + 2) | R(q[0] - 2, q[1] - 1, q[0] + 2, q[1])
            p.fill(gl & R(2, 2, px.W - 3, px.H - 3), 'e0' if i % 2 else 'e1')
        c.stamp(p, 'r0')
    return f


T = math.pi / 2
WALK = [dict(ph=0, bob=0, sway=0, wing=0.0), dict(ph=T, bob=-1, sway=1, wing=0.5, nwr=(10, 61)),
        dict(ph=2 * T, bob=-2, sway=2, wing=1.0, nwr=(10, 60)), dict(ph=3 * T, bob=-1, sway=1, wing=0.5, nwr=(10, 61))]
ATTACK = [
    dict(lean=3, bob=-2, ph=1, wing=0.8, fire=1.2, nel=(26, 50), nwr=(14, 42), fel=(72, 40), fwr=(84, 22), sway=-1),
    dict(lean=-4, bob=0, ph=2, wing=-0.4, fire=1.4, nel=(22, 58), nwr=(6, 56), fx=fx_curse(1.0), sway=2),
    dict(lean=-2, bob=0, ph=3, wing=0.2, fire=1.1, nel=(23, 60), nwr=(8, 60), fx=fx_curse(0.5), sway=1),
]

if __name__ == '__main__':
    export(NAME, sutoku, WALK, ATTACK)
