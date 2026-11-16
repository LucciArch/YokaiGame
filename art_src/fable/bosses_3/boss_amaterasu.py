"""Amaterasu-ōmikami – die Sonnengöttin, zornig (Aramitama) vor der Felsenhöhle Ama-no-Iwato.
Blick nach links: Sonnenkranz hinter dem Kopf, schwarzes Haar bis zum Boden, weißes Obergewand über rotem Hakama,
Magatama-Kette, in der vorderen Hand der Yata no Kagami."""
from lib3 import *

NAME = 'boss_amaterasu'
CW, CH = 200, 150
OX, OY = 60, 18            # lokale Fußlinie y=126

col('u0', '#6a2a0c'); col('u1', '#c8641a'); col('u2', '#f4aa2a'); col('u3', '#fff2a8')   # Sonnenfeuer
px.add_rim('u0 u1', 'u3')
col('j0', '#0c3a30'); col('j1', '#1e7a52'); col('j2', '#52c088'); col('j3', '#b8f4cc')   # Jade (Magatama)
px.add_rim('j1', 'j3')
WH = ('v1', 'v2', 'v3')
WHD = ('v0', 'v1', 'v2')
RED = ('m1', 'm2', 'm3')
REDD = ('m0', 'm1', 'm2')
GOLD = ('y0', 'y1', 'y2')
SKIN = ('k1', 'k2', 'k3')
HAIR = ('h0', 'hb', 'h2')
SUN = ('u1', 'u2', 'u3')


def P(x, y):
    return (x + OX, y + OY)


DEF = dict(bob=0, lean=0, ph=0.0, sway=0, halo=1.0,
           nel=(26, 58), nwr=(14, 52), mir=(8, 46),
           fel=(66, 60), fwr=(62, 74), fx=None)


def halo(c, o, k, ph):
    """Sonnenkranz: Ring mit zwölf Flammenstrahlen, dreht sich mit ph"""
    p = C()
    m = E(o[0], o[1], 25 * k, 25 * k) & ~E(o[0], o[1], 19 * k, 19 * k)
    for i in range(12):
        a = i * 30 + ph * 15
        r0, r1 = 23 * k, (34 if i % 2 == 0 else 29) * k
        m |= tongue(pol(o, a, r0), pol(o, a + 6, r1), 2.6 * k, 1.5)
    p.form(m, SUN, sd=2, hl=1)
    p.fill(E(o[0], o[1], 21 * k, 21 * k) & ~E(o[0], o[1], 20 * k, 20 * k), 'u0')
    c.stamp(p, 'u0')


def sleeve(c, sh_, el, wr, drop, ph, near):
    """weiter Ärmel: weiß, rot gefüttert, hängt schwer nach unten"""
    p = C()
    arm = L(*sh_, 5.5, *el, 6.5) | L(*el, 6.5, *wr, 7.0)
    w = math.sin(ph) * 1.5
    bag = PG([add(el, (5, 0)), add(el, (6 + w, drop)), add(lerp(el, wr, .5), (3 + w, drop + 4)), add(wr, (2 + w, drop - 2)),
              add(wr, (-3, 6)), wr])
    m = arm | bag
    p.form(m, WH if near else WHD, sd=3, hl=1)
    edge = m & ~sh(m, 0, -2) & sh(m, 0, -1)
    p.fill(edge, 'm2')
    p.fill(m & ~sh(m, 0, -1), 'm1')
    for t in (.3, .7):
        q = lerp(el, wr, t)
        p.line([add(q, (2, 2)), add(q, (3 + w, drop - 2))], 'v0' if not near else 'v1', only=m)
    c.stamp(p, 'K')


def mirror(c, o, k=1.0, flare=0.0):
    """Yata no Kagami: Bronzescheibe mit achtfach gezacktem Rand, polierte Fläche"""
    p = C()
    rim = star(o[0], o[1], 9.6 * k, 8.4 * k, n=8, rot=11)
    p.form(rim, ('s1', 's2', 's3'), sd=1, hl=1)
    face = E(o[0], o[1], 6.6 * k, 6.6 * k)
    p.form(face, ('y1', 'y2', 'y3') if flare else ('y0', 'y1', 'y2'), sd=2, hl=1)
    p.line([(o[0] - 3, o[1] + 2), (o[0] + 2, o[1] - 3)], 'y3', only=face)
    p.fill(E(o[0] - 2, o[1] - 2, 1.6, 1.6), 'v3')
    c.stamp(p, 'K')
    if flare:
        p = C()
        m = E(o[0], o[1], 4 * flare, 4 * flare)
        for a in range(0, 360, 45):
            m |= tongue(pol(o, a, 5), pol(o, a, 5 + 12 * flare), 1.8, 0, tr=0.4)
        p.form(m, SUN, sd=1, hl=1)
        p.fill(E(o[0], o[1], 2.4, 2.4), 'u3')
        c.stamp(p, 'u1')


def flames(c, ph, front):
    """Sonnenfeuer züngelt um den Saum: sie berührt den Boden nicht"""
    p = C()
    m = np.zeros((px.H, px.W), bool)
    xs = (18, 30, 42, 54, 66, 76) if not front else (24, 38, 50, 62)
    for i, x in enumerate(xs):
        h = 12 + 6 * ((i * 5 + (3 if front else 0)) % 4) / 3 + 3 * math.sin(ph * 2 + i * 1.7)
        b = P(x, 126)
        m |= E(b[0], b[1] - 2, 5.2, 3.2)
        m |= tongue((b[0], b[1] - 2), (b[0] + 3 * math.sin(ph + i), b[1] - h * (0.7 if front else 1)), 3.2, 2 * math.sin(ph + i * 2), tr=0.6)
    m &= R(0, 0, 999, OY + 127)
    p.form(m, SUN, sd=2, hl=1)
    p.fill(m & ~sh(m, 0, -3) & sh(m, 0, -1), 'u0')
    c.stamp(p, 'u0')


def ama(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean, ph, sw = S['bob'], S['lean'], S['ph'], S['sway']

    def U(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    # ---- Sonnenkranz hinter allem
    halo(c, U((48, 24)), S['halo'], ph)
    if S['fx']:
        S['fx'](c, 0)

    # ---- Haar fällt bis zum Boden, hinten weht es nach rechts
    p = C()
    hp = [(40, 8), (54, 6), (62, 14), (66, 32), (72, 60), (80 + sw, 92), (90 + sw, 118), (94 + sw, 125), (82 + sw, 121),
          (76 + sw, 125), (70 + sw, 112), (64, 80), (58, 52), (50, 32)]
    hair = PG(curve([U(q, max(0, 1 - q[1] / 110)) for q in hp], 4))
    p.form(hair, HAIR, sd=4, hl=0)
    for a_, b_ in (((58, 16), (66, 50)), ((66, 50), (80 + sw, 100)), ((62, 30), (72, 76)), ((72, 76), (86 + sw, 118))):
        p.line([U(a_, .5), U(b_, .2)], 'h2', only=hair)
    p.fill(R(*U((63, 46), .6), *U((69, 49), .6)) & hair, 'm2')      # rotes Haarband
    c.stamp(p, 'K')

    flames(c, ph, False)

    # ---- hinterer Arm
    sleeve(c, U((54, 42)), U(S['fel'], .6), P(*S['fwr']), 18, ph, False)

    # ---- Gewand: rotes Hakama, weißes Obergewand darüber, goldener Gürtel
    p = C()
    hem = [(70, 116), (68 + sw, 125), (56, 122), (46 + sw, 126), (34, 121), (24 + sw, 125), (20, 116)]
    hak = PG([U((30, 66), .7), U((62, 66), .7)] + [P(*q) for q in hem])
    p.form(hak, RED, sd=4, hl=1)
    for (x0, x1) in ((36, 30), (44, 42), (52, 54), (60, 64)):
        p.line([U((x0, 72), .6), P(x1 + sw, 120)], 'm0', only=hak)
    c.stamp(p, 'K')
    p = C()
    robe = PG([U((36, 38)), U((56, 38)), U((64, 56), .8), U((70, 92), .5), U((72, 108), .3), U((58, 104), .3), U((54, 70), .6),
               U((38, 70), .6), U((32, 98), .3), U((22, 104), .3), U((26, 74), .5), U((32, 50), .8)])
    p.form(robe, WH, sd=4, hl=1)
    for (a_, b_) in (((40, 72), (30, 100)), ((58, 74), (66, 104)), ((62, 60), (68, 90))):
        p.line([U(a_, .6), U(b_, .3)], 'v1', only=robe)
    p.fill(robe & ~sh(robe, 0, -2) & R(0, OY + 90, 999, 999), 'm2')    # roter Saum
    # Kragen: Rot, Weiß, Gold übereinander
    p.line([U((42, 38)), U((47, 56), .9)], 'm2', only=robe)
    p.line([U((43, 38)), U((48, 56), .9)], 'y1', only=robe)
    p.line([U((52, 38)), U((47, 56), .9)], 'm2', only=robe)
    obi = PG([U((34, 58), .8), U((60, 58), .8), U((60, 66), .7), U((34, 66), .7)])
    p.form(obi, GOLD, sd=2, hl=1, only=robe)
    for x in (39, 46, 53):
        p.fill(E(*U((x, 62), .75), 1.2, 1.2), 'u0', only=obi)
    c.stamp(p, 'K')

    # ---- Magatama-Kette
    p = C()
    for i, (x, y) in enumerate(((38, 44), (41, 48), (45, 50), (49, 48), (52, 44))):
        q = U((x, y), .9)
        if i == 2:
            m = E(q[0], q[1] + 1, 2.6, 2.6) | L(q[0] + 1, q[1] + 2, 1.6, q[0] + 3, q[1] + 5, 0.7)
            p.form(m, ('j1', 'j2', 'j3'), sd=1, hl=1)
            p.px(q[0] - 1, q[1], 'j0')
        else:
            p.form(E(q[0], q[1], 1.6, 1.6), ('j0', 'j1', 'j2'), sd=1, hl=1)
    c.stamp(p, 'K')

    # ---- Kopf
    HX, HY = U((30, 8))

    def Hh(x, y):
        return (HX + x, HY + y)
    p = C()
    p.form(L(*Hh(14, 24), 3.4, *U((46, 40)), 4.0), ('k0', 'k1', 'k2'), sd=1, hl=0)   # Hals
    c.stamp(p, 'K')
    p = C()
    back = E(*Hh(20, 12), 12.0, 12.4)
    p.form(back, HAIR, sd=3, hl=0)
    c.stamp(p, 'K')
    p = C()
    face = E(*Hh(12, 15), 8.6, 10.4) | E(*Hh(10, 20), 7.4, 6.8)
    p.form(face, SKIN, sd=2, hl=1)
    # Augen: zornig, golden glühend; Brauen schräg
    for (ex, ey) in ((6, 14), (14, 14)):
        p.fill(R(*Hh(ex, ey), *Hh(ex + 3, ey + 1)), 'K')
        p.fill(R(*Hh(ex + 1, ey), *Hh(ex + 2, ey)), 'y2')
        p.px(*Hh(ex + 1, ey + 1), 'y3')
    p.line([Hh(5, 11), Hh(9, 12)], 'K')
    p.line([Hh(14, 12), Hh(18, 11)], 'K')
    p.line([Hh(4, 20), Hh(5, 21)], 'k1')                                # Nase
    p.line([Hh(6, 25), Hh(10, 25)], 'm1')                               # schmaler, strenger Mund
    p.px(*Hh(3, 17), 'm3')                                              # Wangenrot
    p.px(*Hh(16, 17), 'm3')
    c.stamp(p, 'K')
    p = C()
    fringe = (E(*Hh(14, 6), 12, 7.4) & ~E(*Hh(8, 14), 8, 5)) | tube(curve([Hh(4, 6), Hh(1, 18), Hh(2, 32)], 5), 2.6, 0.8)
    fringe |= tube(curve([Hh(22, 8), Hh(24, 24), Hh(22, 40)], 5), 3.0, 1.0)
    fringe |= tube(curve([Hh(18, 22), Hh(16, 34), Hh(14, 48), Hh(15 + sw, 60)], 5), 2.8, 0.8)
    p.form(fringe, HAIR, sd=2, hl=0)
    p.line([Hh(6, 2), Hh(14, 0), Hh(22, 3)], 'h2', only=fringe)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))
    # Krone: goldener Stirnreif mit kleiner Sonnenscheibe
    p = C()
    p.form(PG([Hh(2, 4), Hh(24, 2), Hh(25, 5), Hh(2, 7)]), GOLD, sd=1, hl=1)
    cr = E(*Hh(12, 0), 3.6, 3.6)
    for a in range(0, 360, 45):
        cr |= L(*Hh(12, 0), 0.9, *pol(Hh(12, 0), a, 5.6), 0.5)
    p.form(cr, SUN, sd=1, hl=1)
    p.fill(E(*Hh(12, 0), 1.4, 1.4), 'u3')
    c.stamp(p, 'K')

    # ---- vorderer Arm mit dem Spiegel
    sleeve(c, U((36, 42)), U(S['nel'], .6), P(*S['nwr']), 22, ph + 1, True)
    p = C()
    hnd = E(*add(P(*S['nwr']), (-3, -1)), 3.2, 2.8)
    p.form(hnd, SKIN, sd=1, hl=1)
    c.stamp(p, 'K')
    mirror(c, P(*S['mir']), 1.0, S.get('flare', 0.0))

    flames(c, ph + 1, True)
    if S['fx']:
        S['fx'](c, 1)
    c.blacken()
    return c


def fx_rays(k):
    """Sonnenstrahlen fächern vom Spiegel nach links aus"""
    def f(c, layer):
        if layer != 1:
            return
        p = C()
        o = P(8, 46)
        m = np.zeros((px.H, px.W), bool)
        for a in (160, 175, 190, 205):
            m |= tongue(pol(o, a, 8), pol(o, a, 8 + 46 * k), 3.0, 0, tr=1.0)
        m &= R(1, 1, px.W - 2, px.H - 2)
        p.form(m, SUN, sd=1, hl=1)
        c.stamp(p, 'u1')
    return f


T = math.pi / 2
WALK = [dict(ph=0, bob=0, sway=0), dict(ph=T, bob=-1, sway=1, nwr=(14, 51), mir=(8, 45)),
        dict(ph=2 * T, bob=-2, sway=2, nwr=(14, 50), mir=(8, 44)), dict(ph=3 * T, bob=-1, sway=1, nwr=(14, 51), mir=(8, 45))]
ATTACK = [
    dict(lean=3, bob=-2, ph=1, nel=(30, 44), nwr=(20, 32), mir=(14, 24), halo=1.12, flare=0.6, sway=-1),
    dict(lean=-4, bob=0, ph=2, nel=(24, 52), nwr=(12, 46), mir=(8, 46), halo=1.18, flare=1.0, fx=fx_rays(1.0), sway=2),
    dict(lean=-2, bob=0, ph=3, nel=(25, 56), nwr=(13, 50), mir=(8, 46), halo=1.06, flare=0.5, fx=fx_rays(0.5), sway=1),
]

if __name__ == '__main__':
    export(NAME, ama, WALK, ATTACK)
