"""Einzel-Symbole Teil 1: Götter, Heiliges, Waffen."""
from ihelp import *
import icons_1 as I1, icons_2 as I2, icons_3 as I3


def blade_diag(c, x0, y0, x1, y1, w0=2.2, w1=0.6, steel='iron', curve=0.0):
    """Klinge als Folge von Kapseln von (x0,y0) (Heft) nach (x1,y1) (Spitze), optional gekrümmt."""
    pts = []
    n = 8
    for i in range(n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        nx, ny = -(y1 - y0), (x1 - x0)
        ln = math.hypot(nx, ny) or 1
        bend = curve * math.sin(math.pi * t)
        pts.append((x + nx / ln * bend, y + ny / ln * bend, w0 + (w1 - w0) * t))
    m = tube(pts, steel, c, sd=1, hl=1)
    return m


def hilt(c, x0, y0, x1, y1, w=1.6, wrap='black', tsuba=None, tsuba_fam='gold'):
    tube([(x0, y0, w), (x1, y1, w)], wrap, c, 1, 1)
    # Wicklung (Rautenmuster)
    for k in range(1, 4):
        t = k / 4
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        c.a[int(round(y)), int(round(x))] = 'W'
    if tsuba:
        tx, ty, r = tsuba
        c.form(E(tx, ty, r, r), RAMP3[tsuba_fam], 1, 1, ring='K')


# ------------------------------------------------------------------ Schwerter & Waffen
def kusanagi():
    c = Cv()
    blade_diag(c, 9, 23, 27, 4, 2.4, 1.2, 'white')          # gerades zweischneidiges Tsurugi
    c.line([(10, 22), (26, 5)], 'W')
    hilt(c, 4, 28, 8, 24, 1.5, 'gold', (9.5, 22.5, 2.6), 'jade')
    disc(c, 3.5, 28.5, 1.8, 'gold', 0, 1)
    glow_dots(c, [(28, 2), (24, 9), (20, 13)], 'A')
    return c


def ame_nuboko():
    c = Cv()
    tube([(5, 28, 1.2), (21, 10, 1.2)], 'wood', c)                 # Schaft
    blade_diag(c, 20, 11, 28, 3, 2.6, 0.4, 'gold')                  # breite Speerspitze
    c.form(E(19.5, 11.5, 2.4, 2.4), RAMP3['jade'], 1, 1, ring='K')
    for x, y in ((14, 18), (10, 22)):
        c.form(E(x, y, 1.5, 1.5), RAMP3['red'], 0, 1)
    c.line([(6, 27), (5, 30), (3, 30)], 'R')                       # Quaste
    return c


def shinigami_sense():
    c = Cv()
    tube([(8, 30, 1.3), (14, 3, 1.3)], 'black', c)
    blade = PG([(14, 3), (27, 6), (31, 13), (26, 9), (17, 8)])
    c.form(blade, 'khH', 1, 1)
    c.fill(blade & (px.Y <= 6 + (px.X - 14) * 0.2), '3')
    c.line([(16, 5), (27, 7)], '3')
    glow_dots(c, [(28, 9), (24, 7)], 'X')
    c.g(10, 16, "x\nx\np")
    return c


def tamahagane():
    c = Cv()
    blade_diag(c, 7, 25, 28, 3, 2.1, 0.7, 'iron', curve=1.6)
    # Hamon (Härtelinie)
    for i in range(10):
        t = i / 10
        x, y = 9 + 18 * t, 23 - 19 * t
        c.a[int(round(y + math.sin(i) * 0.6)), int(round(x))] = 'W'
    hilt(c, 2, 30, 6, 26, 1.5, 'black', (7.5, 24.5, 2.4), 'gold')
    return c


def kunai():
    c = Cv()
    for k, (bx, ang) in enumerate(((10, -112), (16, -90), (22, -68))):
        a = math.radians(ang)
        x0, y0 = bx, 22
        x1, y1 = x0 + math.cos(a) * 12, y0 + math.sin(a) * 12
        c.form(PG([(x0 - 2.2, y0), (x0 + 2.2, y0), (x1, y1)]), '123', 1, 1)
        c.line([(x0, y0 - 1), (x1, y1 + 1)], 'W')
        tube([(x0, y0, 0.9), (x0, y0 + 4, 0.9)], 'black', c, 0, 0)
        ring = E(x0, y0 + 6.2, 1.8, 1.8) & ~E(x0, y0 + 6.2, 0.8, 0.8)
        c.fill(ring, '2')
    c.form(R(4, 23, 28, 26), 'jdD', 1, 1)
    c.fill(R(4, 24, 28, 24), 't')
    return c


def ronin_schwur():
    c = Cv()
    blade_diag(c, 10, 22, 27, 5, 1.9, 0.6, 'iron', curve=1.3)
    c.fill(PG([(20, 10), (23, 8), (24, 10)]), '0')                    # Scharte
    hilt(c, 5, 27, 9, 23, 1.4, 'wood', (10, 22, 2.2), 'iron')
    c.line([(5, 27), (3, 30)], 'h')                                    # zerrissene Kordel
    c.g(1, 29, "h.\n.h")
    return c


def am_ken():
    return amulet('sword')


def hachiman_bogen():
    c = I1.bow()
    recolor(c, 'wood', 'gold')
    recolor(c, 'red', 'crimson')
    sparkle(c, 6, 6)
    return c


def yumi():
    c = Cv()
    pts = [(9, 2), (13, 7), (15, 14), (14, 20), (11, 26), (8, 30)]   # asymmetrisch, oberer Teil länger
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        c.form(L(x0, y0, 1.3, x1, y1, 1.3), 'dDt', 1, 1)
    c.line([(9, 2), (8, 30)], 'W')
    c.form(R(13, 17, 16, 21), 'qrR', 1, 1)                             # Griffwicklung
    return c


def hamaya():
    c = Cv()
    tube([(5, 27, 1.0), (25, 6, 1.0)], 'white', c)
    c.form(PG([(25, 3), (29, 3), (27, 8)]), '123', 1, 1)
    for k in range(3):
        c.fill(PG([(5 + k, 25 - k * 2), (2 + k, 23 - k * 2), (4 + k, 28 - k * 2)]), 'W')
    c.form(PG([(14, 15), (21, 15), (21, 22), (17.5, 25), (14, 22)]), 'dDt', 1, 1)   # Ema-Tafel
    c.g(16, 17, "qq\nq.\nqq")
    c.form(E(9, 23, 1.8, 1.8), 'gyY', 1, 1)                           # Glöckchen
    return c


def shamisen():
    c = Cv()
    body = PG([(4, 19), (13, 19), (14, 29), (3, 29)])
    c.form(body, 'dDt', 1, 1, ring='K')
    c.form(PG([(5, 20), (12, 20), (12.6, 28), (4.4, 28)]), 'vwW', 1, 1)
    tube([(9, 19, 1.0), (24, 4, 1.0)], 'black', c)
    c.form(PG([(23, 5), (28, 1), (30, 3), (25, 7)]), 'khH', 1, 1)
    for x, y in ((25, 2), (28, 5)):
        c.a[y, x] = 'Y'
    c.line([(8, 27), (24, 5)], 'Y')
    c.form(PG([(6, 24), (10, 22), (11, 24), (7, 26)]), 'ogy', 0, 1)  # Bachi-Schutz
    return c


def shuriken():
    c = Cv()
    pts = []
    for k in range(8):
        a = k * math.pi / 4 - math.pi / 2
        r = 12 if k % 2 == 0 else 3.6
        pts.append((16 + math.cos(a) * r, 16 + math.sin(a) * r))
    c.form(PG(pts), '123', 2, 1)
    ring = E(16, 16, 2.4, 2.4)
    c.fill(ring, 'k')
    c.fill(E(15.4, 15.4, 0.8, 0.8), '2')
    return c


def kanabo():
    c = Cv()
    m = L(6, 27, 1.6, 22, 8, 4.4)
    c.form(m, 'khH', 2, 1)
    for i in range(6):
        t = 0.35 + i * 0.11
        x, y = 6 + 16 * t, 27 - 19 * t
        for dx, dy in ((-3, -2), (2, 3)):
            c.form(E(x + dx * t, y + dy * t, 1.0, 1.0), '123', 0, 1)
    c.form(R(4, 27, 7, 30), '012', 0, 1)
    return c


# ------------------------------------------------------------------ Götter & Heiliges
def amaterasu():
    c = Cv()
    for k in range(12):
        a = k * math.tau / 12
        x0, y0 = 16 + math.cos(a) * 9, 16 + math.sin(a) * 9
        x1, y1 = 16 + math.cos(a) * (14 if k % 2 == 0 else 12), 16 + math.sin(a) * (14 if k % 2 == 0 else 12)
        c.form(L(x0, y0, 1.6, x1, y1, 0.4), 'gyY', 0, 1)
    disc(c, 16, 16, 8.5, 'orange', 2, 1)
    c.form(E(16, 16, 6, 6), 'gyY', 2, 1)
    c.fill(E(14, 14, 1.8, 1.8), 'W')
    return c


def tsukuyomi():
    c = I3.moon()
    recolor(c, 'gold', 'white')
    c.form(E(9, 9, 2.6, 2.6), RAMP3['indigo'], 0, 1)
    sparkle(c, 25, 24, 'W', 'O')
    return c


def am_tsuki():
    return amulet('moon')


def seimei_stern():
    c = Cv()
    ring = E(16, 16, 13, 13) & ~E(16, 16, 11.4, 11.4)
    c.fill(ring, 'p')
    c.fill(ring & (px.Y < 14), 'P')
    pts = [(16 + math.cos(-math.pi / 2 + k * 2 * math.tau / 5) * 11.5, 16 + math.sin(-math.pi / 2 + k * 2 * math.tau / 5) * 11.5) for k in range(6)]
    c.line(pts, 'X', 2)
    c.fill(E(16, 16, 2.2, 2.2), 'Y')
    return c


def hoshi_splitter():
    c = Cv()
    c.form(PG([(16, 2), (21, 12), (19, 29), (12, 22), (11, 9)]), 'xpP', 2, 1)
    c.line([(16, 4), (15, 22)], 'X')
    for x, y in ((25, 6), (6, 25), (26, 22)):
        sparkle(c, x, y, 'X', 'P')
    return c


def hanabi():
    c = Cv()
    cols = ['R', 'Y', 'S', 'A', 'l', 'X']
    for k in range(16):
        a = k * math.tau / 16
        for r in (5, 8, 11):
            x, y = 16 + math.cos(a) * r, 15 + math.sin(a) * r
            if r == 11 and k % 2:
                continue
            c.form(E(x, y, 1.3 if r < 11 else 1.0, 1.3 if r < 11 else 1.0), None or 'gyY', 0, 0)
            c.a[int(round(y)), int(round(x))] = cols[k % len(cols)]
    c.fill(E(16, 15, 2, 2), 'W')
    c.line([(16, 30), (16, 21)], 'o')
    return c


def kamikaze():
    c = Cv()
    for r, y, ln in ((9, 9, 20), (7, 17, 24), (6, 24, 16)):
        x0 = 4
        c.line([(x0, y), (x0 + ln, y)], 'W', 3)
        cx = x0 + ln
        arc = E(cx, y - r / 2, r / 2, r / 2) & ~E(cx, y - r / 2, r / 2 - 1.6, r / 2 - 1.6) & (px.X >= cx)
        c.fill(arc, 'W')
        c.line([(x0, y + 1), (x0 + ln, y + 1)], 'v')
    glow_dots(c, [(28, 26), (26, 28)], 'A')
    return c


def susanoo_zorn():
    c = I1.cloud()
    recolor(c, 'white', 'indigo')
    c.line([(15, 20), (12, 25), (16, 25), (12, 31)], 'Y', 2)
    c.line([(15, 20), (12, 25), (16, 25), (12, 31)], 'W', 1)
    for x, y in ((22, 24), (24, 27), (8, 24)):
        c.a[y, x] = 'A'
    return c


def yasakani():
    return I2.magatama()


def raijin_magatama():
    c = I2.magatama()
    recolor(c, 'green', 'gold')
    c.line([(26, 6), (23, 10), (26, 11), (23, 15)], 'Y')
    c.line([(5, 22), (8, 25)], 'Y')
    return c


def yata_kagami():
    return I3.mirror()


def enma_spiegel():
    c = Cv()
    c.form(R(7, 25, 25, 28), 'khH', 1, 1)                            # Ständer
    c.form(L(16, 27, 2.2, 16, 18, 2.2), 'qrR', 1, 1)
    c.form(E(16, 12, 10, 10), 'UVR', 2, 1, ring='K')
    c.form(E(16, 12, 7, 7), 'IJO', 1, 1)
    c.fill(E(16, 12, 3, 4) & ~E(16, 12, 1.6, 2.6), 'R')               # brennendes Auge im Spiegel
    c.fill(E(16, 12, 1, 1.6), 'Y')
    for k in range(8):
        a = k * math.tau / 8
        c.form(E(16 + math.cos(a) * 9.4, 12 + math.sin(a) * 9.4, 1.4, 1.4), 'ogy', 0, 1)
    return c


def tsukuyomi_spiegel():
    c = I3.mirror()
    recolor(c, 'gold', 'iron')
    c.fill(E(16, 15, 4, 4) & ~E(18, 13, 4, 4), 'W')
    return c


def shimenawa():
    c = Cv()
    for i in range(30):
        x = 1 + i
        y = 10 + 3 * math.sin(i / 29 * math.pi)
        c.form(E(x, y, 1.5, 3.2 - abs(i - 15) / 15), 'cCs', 1, 1)
        if i % 3 == 0:
            c.a[int(y) - 1, x] = 'd'
    for x in (8, 16, 24):                                              # Shide-Zickzackpapier
        y0 = int(13 + 2 * math.sin((x - 1) / 29 * math.pi))
        c.g(x - 1, y0, "WW.\n.WW\nWW.\n.WW\nWW.\n.vv\n")
    for x in (12, 20):
        y0 = int(13 + 2 * math.sin((x - 1) / 29 * math.pi))
        c.line([(x, y0), (x, y0 + 8)], 'c')
    return c


def shakujo():
    c = I3.staff()
    return c


def juzu():
    return I1.beads()


def onyudo_kette():
    c = Cv()
    for k in range(7):
        a = math.radians(-160 + k * 30)
        x, y = 16 + math.cos(a) * 11, 18 + math.sin(a) * 11
        disc(c, x, y, 3.2, 'wood', 2, 1)
    disc(c, 16, 26, 4, 'gold', 2, 1)
    c.line([(16, 29), (16, 31)], 'q', 2)
    return c


def hoshi_no_tama():
    c = Cv()
    for k in range(10):
        a = k * math.tau / 10
        c.fill(L(16, 17, 0.3, 16 + math.cos(a) * 13, 17 + math.sin(a) * 13, 0.3), 'n' if k % 2 else 'w')
    disc(c, 16, 17, 7.5, 'white', 2, 2)
    c.fill(PG([(16, 9), (20, 12), (16, 10.5), (12, 12)]), 'Y')        # Hōju-Spitze (Flamme)
    c.form(PG([(16, 4), (19, 10), (13, 10)]), 'gyY', 0, 1)
    c.fill(E(14, 15, 2, 2), 'W')
    return c


def ryu_perle():
    c = hoshi_no_tama()
    recolor(c, 'white', 'blue')
    for k in range(5):
        a = k * math.tau / 5 + 0.3
        c.form(E(16 + math.cos(a) * 10, 19 + math.sin(a) * 10, 1.5, 1.5), 'zaA', 0, 1)
    return c


def build():
    import sys
    me = sys.modules[__name__]
    for nm in NAMES:
        save('icons', nm, getattr(me, nm)())


def amulet(sym):
    """Omamori-Anhänger (Netsuke): Kordel + runde Holzscheibe mit Symbol."""
    c = Cv()
    c.line([(16, 2), (16, 6)], 'R', 2)
    c.form(E(16, 7, 2, 1.6), 'ogy', 0, 1)
    ring = c.form(E(16, 18, 10, 10), 'dDt', 2, 1, ring='K')
    c.form(E(16, 18, 7.6, 7.6), 'jdD', 1, 1)
    inner = E(16, 18, 7, 7)
    c.fill(L(16, 27, 1, 16, 30, 0.5), 'R')
    rows = SYMBOLS[sym].strip('\n').split('\n')
    big = []
    for r_ in rows:
        rr = ''.join(ch * 2 for ch in r_)
        big += [rr, rr]
    x0, y0 = 16 - len(big[0]) // 2, 18 - len(big) // 2
    c.g(x0, y0, '\n'.join(big))
    return c


SYMBOLS = {
    'sword': ".....W\n....W.\n...W..\n..W...\nYY....\n.Y....",
    'moon': "..WW..\n.W....\nW.....\nW.....\n.W....\n..WW..",
    'fox': "W...W\nWW.WW\nWWWWW\n.WRW.\n..W..",
    'tiger': "Y.Y.Y\nYYYYY\nkYkYk\nYYYYY\n.Y.Y.",
    'rabbit': ".W.W.\n.W.W.\n.WWW.\nWWRWW\n.WWW.",
    'turtle': ".fGf.\nfGlGf\nGlGlG\nfGlGf\nf...f",
    'crane': "W...W\n.W.W.\n..R..\n.WWW.\n..W..",
    'koi': ".88..\n8998.\n89998\n.8998\n..8.8",
    'snake': ".GGG.\nG....\n.GGG.\n....G\nGGG.R",
    'cloud': ".WW..\nWWWW.\nWWWWW\n.WWW.",
    'fire': "..Y..\n.YY..\n.YRY.\nYRRRY\n.RRR.",
    'pearl': ".AA.\nAWAA\nAAAA\n.AA.",
    'coin': ".YYY.\nY...Y\nY.k.Y\nY...Y\n.YYY.",
    'mountain': "..W..\n.WWW.\n.vWv.\nvvvvv\n1111W",
}


def am_kitsune(): return amulet('fox')
def am_tora(): return amulet('tiger')
def am_usagi(): return amulet('rabbit')
def am_kame(): return amulet('turtle')
def am_tsuru(): return amulet('crane')
def am_koi(): return amulet('koi')
def am_hebi(): return amulet('snake')
def am_kumo(): return amulet('cloud')
def am_hi(): return amulet('fire')
def am_tama(): return amulet('pearl')
def am_kane(): return amulet('coin')
def am_yama(): return amulet('mountain')


NAMES = ['kusanagi', 'ame_nuboko', 'shinigami_sense', 'tamahagane', 'kunai', 'ronin_schwur', 'hachiman_bogen', 'yumi',
         'hamaya', 'shamisen', 'shuriken', 'kanabo', 'amaterasu', 'tsukuyomi', 'seimei_stern', 'hoshi_splitter', 'hanabi',
         'kamikaze', 'susanoo_zorn', 'yasakani', 'raijin_magatama', 'yata_kagami', 'enma_spiegel', 'tsukuyomi_spiegel',
         'shimenawa', 'shakujo', 'juzu', 'onyudo_kette', 'hoshi_no_tama', 'ryu_perle',
         'am_kitsune', 'am_tora', 'am_usagi', 'am_kame', 'am_tsuru', 'am_koi', 'am_hebi', 'am_kumo', 'am_hi', 'am_tama',
         'am_kane', 'am_tsuki', 'am_yama', 'am_ken']
