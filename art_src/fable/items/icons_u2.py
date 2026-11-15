"""Einzel-Symbole Teil 2: Kitsune, Donner, Tengu, Onmyōji, Yūrei, Oni."""
from ihelp import *
import icons_1 as I1, icons_2 as I2, icons_3 as I3


def inari_maske():
    return I2.mask()


def tengu_maske():
    c = Cv()
    c.form(E(14, 15, 10, 11), 'qrR', 2, 1, ring='K')
    c.form(L(16, 17, 3.2, 28, 21, 1.6), 'qrR', 1, 1)                 # lange Nase
    c.g(7, 10, "kkkk....kkk\n.kWk....kWk.\n")
    c.g(6, 7, "HHHH.....HHH")                                         # buschige Brauen
    c.fill(R(8, 24, 18, 25), 'U')
    c.form(E(14, 4, 3, 2), 'khH', 0, 1)                               # Tokin-Kappe
    return c


def hannya():
    c = Cv()
    c.form(E(16, 18, 10, 11), 'bBi', 2, 1, ring='K')
    for sx in (-1, 1):
        c.form(L(16 + sx * 6, 9, 2.2, 16 + sx * 11, 2, 0.5), 'cCs', 1, 1)   # Hörner
    c.g(9, 13, "kk......kk\n.kYk..kYk.\n..kk..kk..")
    c.fill(PG([(9, 23), (23, 23), (20, 27), (12, 27)]), 'U')
    c.g(10, 23, "W.W.W.W.W.W.W")
    c.g(11, 26, ".W....W.")
    c.line([(12, 11), (14, 13)], 'k'); c.line([(20, 11), (18, 13)], 'k')
    return c


def noh_maske():
    c = Cv()
    c.form(E(16, 16, 9, 12), 'nvW', 2, 1, ring='K')
    c.fill(R(7, 5, 25, 8) & E(16, 16, 9, 12), 'k')                    # Haarlinie
    c.line([(12, 6), (16, 9), (20, 6)], 'h')
    c.g(10, 13, "kkk...kkk\n")
    c.g(12, 11, "k.......k")
    c.form(E(16, 22, 2.4, 1.2), 'qrR', 0, 0)
    c.g(15, 22, "kk")
    c.fill(E(11, 19, 1.3, 1, ) , 'm'); c.fill(E(21, 19, 1.3, 1), 'm')
    return c


def kitsunebi():
    return I2.flame()


def onibi_ring():
    c = Cv()
    for k in range(6):
        a = k * math.tau / 6 - math.pi / 2
        x, y = 16 + math.cos(a) * 10, 17 + math.sin(a) * 10
        c.form(PG([(x, y - 5), (x + 2.6, y + 1), (x, y + 3), (x - 2.6, y + 1)]), 'xpP', 1, 1)
        c.fill(E(x, y + 1, 1, 1.2), 'X')
    c.fill(E(16, 17, 4, 4) & ~E(16, 17, 2.6, 2.6), 'p')
    return c


def yomi_feuer():
    c = Cv()
    c.form(PG([(16, 2), (24, 14), (25, 22), (20, 29), (12, 29), (7, 22), (9, 13), (12, 17)]), 'UVR', 2, 1)
    c.form(PG([(16, 11), (20, 19), (19, 26), (13, 26), (12, 20)]), 'khH', 1, 0)
    c.fill(E(16, 22, 2, 3), 'R')
    return c


def kasha_rad():
    c = Cv()
    ring = E(16, 16, 9, 9) & ~E(16, 16, 6, 6)
    c.form(ring, 'jdD', 1, 1)
    for k in range(6):
        a = k * math.tau / 6
        c.fill(L(16, 16, 0.8, 16 + math.cos(a) * 7, 16 + math.sin(a) * 7, 0.8), 'd')
    c.form(E(16, 16, 2.2, 2.2), '123', 0, 1)
    for k in range(10):
        a = k * math.tau / 10
        x, y = 16 + math.cos(a) * 12, 16 + math.sin(a) * 12
        c.form(E(x, y, 2, 2), '789', 0, 1)
        c.a[int(round(y)), int(round(x))] = 'Y'
    return c


def kagutsuchi_glut():
    c = Cv()
    c.form(PG([(5, 24), (11, 15), (20, 13), (27, 19), (25, 27), (9, 28)]), 'khH', 2, 1)
    for x, y in ((10, 22), (14, 18), (19, 17), (22, 22), (16, 24), (24, 20)):
        c.fill(L(x - 1, y, 0.6, x + 2, y + 1, 0.6), '9')
        c.a[y, x] = 'Y'
    c.form(PG([(16, 3), (20, 11), (16, 14), (12, 11)]), '789', 1, 1)
    c.fill(E(16, 10, 1.2, 2), 'Y')
    return c


def onryo_kerze():
    c = Cv()
    c.form(R(12, 13, 20, 28), 'nvW', 2, 1, ring='K')
    c.fill(PG([(12, 13), (14, 17), (15, 13)]), 'v'); c.fill(PG([(18, 13), (19, 19), (20, 13)]), 'v')
    c.form(R(9, 28, 23, 30), 'khH', 0, 1)
    c.form(PG([(16, 3), (19, 9), (16, 12), (13, 9)]), 'xpP', 1, 1)
    c.fill(E(16, 9, 1, 1.5), 'X')
    c.line([(16, 12), (16, 14)], 'k')
    return c


def kyubi_schweif():
    return I3.tail()


def nekomata_schweif():
    c = Cv()
    for off, fam in ((-5, 'white'), (5, 'white')):
        pts = [(16 + off * 0.4, 29, 2.2), (16 + off * 0.8, 22, 2.4), (16 + off, 15, 2.4), (16 + off * 1.4, 9, 2.2), (16 + off * 1.1, 4, 2)]
        tube(pts, fam, c, 1, 1)
        c.form(E(16 + off * 1.1, 4, 2.2, 2.2), 'khH', 0, 1)
    c.fill(E(16, 29, 3, 1.6), 'v')
    for x, y in ((11, 19), (21, 19), (13, 12), (19, 12)):
        c.a[y, x] = 'p'
    return c


def nue_schweif():
    c = Cv()
    pts = [(5, 28, 2.6), (10, 24, 2.8), (14, 18, 2.8), (12, 12, 2.6), (16, 7, 2.6), (22, 6, 2.8)]
    m = tube(pts, 'green', c, 1, 1)
    for i in range(0, 28, 3):
        for j in range(32):
            if m[j, i] and (i + j) % 4 == 0:
                c.a[j, i] = 'F'
    c.form(E(25, 6, 4, 3), 'FfG', 1, 1)                               # Schlangenkopf
    c.a[5, 26] = 'Y'; c.a[5, 27] = 'k'
    c.line([(29, 7), (31, 8)], 'R')
    return c


def fuchsschrein():
    c = Cv()
    c.form(PG([(4, 13), (16, 4), (28, 13)]), 'qrR', 1, 1, ring='K')   # Dach
    c.form(R(7, 13, 25, 26), 'dDt', 2, 1)
    c.form(R(11, 15, 21, 26), 'khH', 0, 0)
    c.g(13, 17, "W...W\nWW.WW\nWWWWW\n.WRW.\n..W..")                    # Fuchsfigur
    c.form(R(5, 26, 27, 29), 'qrR', 1, 1)
    c.g(14, 22, "YYYYY")
    return c


def raijin_trommel():
    c = Cv()
    for k, (x0, y0, x1, y1) in enumerate(((6, 27, 22, 6), (26, 27, 10, 6))):
        tube([(x0, y0, 1.3), (x1, y1, 1.7)], 'wood', c)
        c.form(E(x1, y1, 2.8, 2.8), 'ogy', 1, 1)
    c.line([(15, 3), (13, 7), (17, 7), (14, 12)], 'Y', 2)
    c.line([(15, 3), (13, 7), (17, 7), (14, 12)], 'W')
    return c


def raijin_taiko():
    c = Cv()
    for k in range(8):                                                # Trommelkranz
        a = k * math.tau / 8
        x, y = 16 + math.cos(a) * 11, 16 + math.sin(a) * 11
        c.form(E(x, y, 3.4, 3.4), 'qrR', 1, 1, ring='K')
        c.form(E(x, y, 2, 2), 'bBi', 0, 1)
    c.line([(15, 9), (12, 16), (18, 16), (14, 24)], 'Y', 2)
    return c


def oni_trommel():
    c = Cv()
    c.form(E(16, 17, 12, 11), 'qrR', 2, 1, ring='K')
    c.form(E(16, 13, 11, 6), 'bBi', 1, 1)
    for x in (6, 11, 16, 21, 26):
        c.a[19, x] = 'Y'
    c.g(12, 10, "k.....k\n.k...k.\n")                                # Oni-Gesicht auf dem Fell
    c.fill(E(16, 15, 3, 1), 'k')
    c.line([(3, 6), (9, 10)], 'd', 2); c.line([(29, 6), (23, 10)], 'd', 2)
    return c


def inazuma():
    c = Cv()
    c.form(PG([(19, 2), (9, 16), (16, 16), (11, 30), (24, 12), (17, 12), (23, 2)]), 'gyY', 1, 1, ring='K')
    c.line([(20, 3), (12, 15)], 'W')
    sparkle(c, 26, 22)
    return c


def raiju_klaue():
    c = Cv()
    for k in range(3):
        x0 = 9 + k * 6
        pts = [(x0, 8, 2.4), (x0 + 1, 17, 2.4), (x0 + 3, 25, 1.4), (x0 + 6, 28, 0.5)]
        tube(pts, 'gold', c, 1, 1)
    c.form(R(7, 4, 26, 10), 'IJO', 1, 1)
    c.line([(4, 14), (7, 17), (5, 20)], 'A'); c.line([(28, 13), (25, 17), (28, 20)], 'A')
    return c


def bakeneko_kralle():
    c = Cv()
    c.form(E(14, 12, 9, 8), 'xpP', 2, 1, ring='K')                    # Pfote
    for k in range(4):
        a = math.radians(-150 + k * 30)
        x, y = 14 + math.cos(a) * 9, 12 + math.sin(a) * 8
        c.form(E(x, y, 2.4, 2.4), 'xpP', 1, 1)
        tube([(x, y, 1.0), (x + math.cos(a) * 5, y + math.sin(a) * 5, 0.3)], 'white', c, 0, 0)
    c.form(E(14, 14, 3.4, 2.6), 'mST', 0, 1)
    for x, y, x2, y2 in ((16, 22, 26, 30), (20, 20, 29, 27)):
        c.line([(x, y), (x2, y2)], 'X')
    return c


def kamaitachi_sichel():
    c = Cv()
    tube([(6, 28, 1.3), (14, 15, 1.3)], 'wood', c)
    blade = E(19, 13, 10, 7) & ~E(21, 16, 9, 6) & (px.Y < 16)
    c.form(blade, '123', 1, 1)
    c.line([(24, 22), (29, 18)], 'W'); c.line([(22, 25), (28, 23)], 'w')
    return c


def kamaitachi_klingen():
    c = Cv()
    for k in range(3):
        a = math.radians(-40 + k * 40)
        x0, y0 = 16 + math.cos(a + math.pi) * 3, 24
        x1, y1 = 16 + math.sin(a) * 13, 24 - math.cos(a) * 18
        tube([(x0, y0, 1.6), (x1, y1, 0.4)], 'white', c, 1, 1)
    c.form(E(16, 26, 4, 2.6), '789', 1, 1)
    c.g(14, 25, "k.k")
    return c


def fujin_sack():
    c = I1.bag()
    recolor(c, 'wood', 'green')
    recolor(c, 'red', 'white')
    for y, x0 in ((6, 22), (10, 25), (14, 23)):
        c.line([(x0, y), (x0 + 5, y)], 'W')
    return c


def tengu_faecher():
    c = Cv()
    tube([(16, 30, 1.2), (16, 18, 1.2)], 'wood', c)
    for k in range(7):
        a = math.radians(-90 + (k - 3) * 22)
        x, y = 16 + math.cos(a) * 10, 15 + math.sin(a) * 10
        c.form(REL(x, y, 3.2, 5.6, math.degrees(a) + 90), 'FfG', 1, 1)
    c.form(E(16, 17, 2.4, 2.4), 'ogy', 0, 1)
    return c


def tengu_uchiwa():
    c = Cv()
    tube([(16, 30, 1.3), (16, 19, 1.3)], 'red', c)
    c.form(E(16, 11, 10, 9.4), 'FfG', 2, 1, ring='K')
    for k in range(5):
        a = math.radians(-90 + (k - 2) * 30)
        c.line([(16, 19), (16 + math.cos(a) * 9, 11 + math.sin(a) * 8.4)], 'F')
    c.g(13, 8, "kkkkk\n..k..\n.kkk.")
    return c


def sensu():
    c = I2.fan()
    return c


def kerakera_faecher():
    c = I2.fan()
    recolor(c, 'gold', 'purple')
    recolor(c, 'red', 'pink')
    c.g(13, 9, "kk.kk\n.....\nkkkkk")
    return c


def karasu_feder():
    return I2.feather()


def suzume_feder():
    c = Cv()
    c.form(REL(17, 13, 5.2, 11, -30), '789', 2, 1)
    c.fill(REL(19, 9, 2.2, 5, -30), 'j')
    c.line([(9, 28), (14, 20), (21, 6)], 'd')
    for k in range(4):
        y = 10 + k * 4
        c.line([(14 + k, y + 2), (19 + k, y - 1)], '7')
    return c


def sojobo_feder():
    c = Cv()
    tube([(16, 30, 1.2), (16, 20, 1.2)], 'black', c)
    for k in range(9):
        a = math.radians(-90 + (k - 4) * 17)
        x, y = 16 + math.cos(a) * 9, 18 + math.sin(a) * 9
        c.form(REL(x, y, 2.2, 6, math.degrees(a) + 90), 'vwW', 1, 1)
        c.a[int(round(y + math.sin(a) * 4)), int(round(x + math.cos(a) * 4))] = 'k'
    c.form(E(16, 19, 2.4, 2.4), 'qrR', 0, 1)
    return c


def yatagarasu():
    c = Cv()
    c.form(E(16, 16, 11, 11), '789', 0, 1)                            # Sonne dahinter
    c.form(E(16, 15, 6, 7), 'khH', 2, 1, ring='K')                    # Krähenkörper
    c.form(PG([(10, 12), (2, 7), (5, 14), (10, 18)]), 'khH', 1, 1)
    c.form(PG([(22, 12), (30, 7), (27, 14), (22, 18)]), 'khH', 1, 1)
    c.form(E(16, 8, 3, 3), 'khH', 1, 1)
    c.a[7, 17] = 'R'
    c.fill(PG([(18, 8), (22, 9), (18, 10)]), 'Y')
    for x in (13, 16, 19):                                            # drei Beine
        c.line([(x, 21), (x, 27)], 'h')
        c.line([(x - 1, 27), (x + 1, 27)], 'h')
    return c


def tengu_geta():
    c = Cv()
    c.form(PG([(5, 12), (26, 9), (28, 14), (7, 17)]), 'dDt', 2, 1, ring='K')   # Brett
    c.form(R(14, 15, 18, 26), 'jdD', 1, 1)                                     # ein Zahn
    c.line([(9, 12), (16, 7), (23, 11)], 'R', 2)                               # Riemen
    c.form(E(16, 8, 1.5, 1.5), 'qrR', 0, 1)
    return c


def strohhut():
    return I2.hat()


def karakasa():
    c = Cv()
    c.form(PG([(2, 15), (16, 3), (30, 15)]), 'qrR', 2, 1, ring='K')
    for k in range(5):
        x = 4 + k * 6
        c.line([(16, 4), (x, 15)], 'U')
    c.fill(R(2, 15, 30, 16), 'R')
    tube([(16, 15, 1.1), (16, 28, 1.1)], 'wood', c)
    c.line([(16, 28), (18, 30)], 'd')
    c.g(9, 8, "W.....W\n.......\n...W...")
    return c


def shikigami_papier():
    c = I1.doll()
    recolor(c, 'straw', 'white')
    recolor(c, 'wood', 'white')
    c.g(14, 12, "qqq\n.q.\nqqq")
    return c


def hitogata():
    c = Cv()
    body = PG([(16, 3), (19, 6), (18, 9), (26, 11), (26, 14), (19, 14), (21, 28), (17, 28), (16, 21), (15, 28), (11, 28), (13, 14), (6, 14), (6, 11), (14, 9), (13, 6)])
    c.form(body, 'JOW', 1, 1, ring='K')
    c.form(body & (px.Y > 8), 'vwW', 1, 1)
    c.line([(16, 11), (16, 19)], 'J')
    c.line([(12, 12), (20, 12)], 'J')
    for k in range(3):
        a = k * math.tau / 3 + 0.4
        c.fill(E(16 + math.cos(a) * 13, 17 + math.sin(a) * 13, 1.2, 1.2), 'O')
    return c


def shikigami_ruf():
    c = Cv()
    for k, (x, y, r) in enumerate(((10, 18, 1.0), (16, 14, 1.0), (22, 18, 1.0))):
        body = PG([(x, y - 9), (x + 3, y - 6), (x + 7, y - 4), (x + 3, y - 3), (x + 4, y + 7), (x, y + 3), (x - 4, y + 7), (x - 3, y - 3), (x - 7, y - 4), (x - 3, y - 6)])
        c.form(body, 'nvW', 1, 1, ring='K')
    c.g(14, 9, "q.q\n.q.")
    c.form(R(6, 26, 26, 28), 'qrR', 0, 1)
    return c


def ofuda_buendel():
    c = Cv()
    for k, ang in enumerate((-25, -8, 9, 26)):
        a = math.radians(ang)
        cx, cy = 16 + math.sin(a) * 6, 17
        pts = []
        for dx, dy in ((-3, -10), (3, -10), (3, 10), (-3, 10)):
            pts.append((cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)))
        c.form(PG(pts), 'nvW', 1, 1, ring='K')
        for j in range(4):
            yy = -6 + j * 3.5
            c.a[int(round(cy + yy * math.cos(a))), int(round(cx - yy * math.sin(a)))] = 'q'
    c.form(R(9, 20, 23, 22), 'qrR', 0, 1)
    return c


def ofuda_sturm():
    c = Cv()
    for k in range(7):
        a = k * math.tau / 7
        r = 7 + k * 1.1
        x, y = 16 + math.cos(a) * r, 16 + math.sin(a) * r
        pts = [(x + math.cos(a + 1.57) * 2 - math.cos(a) * 3, y + math.sin(a + 1.57) * 2 - math.sin(a) * 3),
               (x - math.cos(a + 1.57) * 2 - math.cos(a) * 3, y - math.sin(a + 1.57) * 2 - math.sin(a) * 3),
               (x - math.cos(a + 1.57) * 2 + math.cos(a) * 3, y - math.sin(a + 1.57) * 2 + math.sin(a) * 3),
               (x + math.cos(a + 1.57) * 2 + math.cos(a) * 3, y + math.sin(a + 1.57) * 2 + math.sin(a) * 3)]
        c.form(PG(pts), 'nvW', 1, 0, ring='K')
        c.a[int(round(y)), int(round(x))] = 'q'
    c.fill(E(16, 16, 2.4, 2.4), 'R')
    return c


def kuji_in():
    c = Cv()
    c.form(R(5, 6, 26, 26), 'xpP', 2, 1, ring='K')
    for k in range(5):
        c.line([(7 + k * 4.5, 8), (7 + k * 4.5, 24)], 'X')
    for k in range(4):
        c.line([(7, 9 + k * 5), (24, 9 + k * 5)], 'X')
    c.form(E(16, 16, 3, 3), 'qrR', 0, 1)
    return c


def bushido():
    return I3.scroll()


def tanabata():
    c = Cv()
    tube([(8, 30, 1.2), (12, 2, 1.0)], 'green', c)
    for x, y in ((12, 8), (10, 18)):
        c.line([(x, y), (x + 7, y - 3)], 'f')
    for k, (x, y, fam) in enumerate(((17, 6, 'blue'), (21, 12, 'pink'), (15, 16, 'gold'))):
        c.form(R(x, y, x + 3, y + 9), RAMP3[fam], 1, 1, ring='K')
        c.line([(x + 1, y), (x + 1, y - 2)], 'W')
    return c


def shoji_papier():
    c = Cv()
    c.form(R(4, 4, 27, 27), 'dDt', 1, 1, ring='K')
    c.form(R(6, 6, 25, 25), 'nvW', 1, 1)
    for x in (12, 19):
        c.line([(x, 6), (x, 25)], 'd')
    for y in (11, 16, 21):
        c.line([(6, y), (25, y)], 'd')
    c.fill(E(22, 23, 2, 2) & R(19, 21, 25, 25), 'k')                   # Loch im Papier
    return c


def geheimkarte():
    c = Cv()
    c.form(PG([(3, 6), (12, 4), (20, 7), (29, 5), (29, 26), (20, 28), (12, 25), (3, 27)]), 'cCs', 2, 1, ring='K')
    c.line([(12, 4), (12, 25)], 'c'); c.line([(20, 7), (20, 28)], 'c')
    c.line([(6, 22), (10, 18), (15, 19), (19, 14), (24, 12)], 'q')
    c.g(23, 9, "R.R\n.R.\nR.R")
    c.g(5, 9, "kk\nkk")
    return c


def senbazuru():
    c = Cv()
    for y in (6, 14, 22):
        c.line([(16, y - 4), (16, y + 4)], 'R')
    cols = ['red', 'gold', 'blue', 'pink']
    for k, (y) in enumerate((6, 13, 20, 27)):
        fam = cols[k]
        c.form(PG([(10, y), (16, y - 3), (22, y), (16, y + 2)]), RAMP3[fam], 1, 1, ring='K')
        c.fill(PG([(15, y - 1), (17, y - 1), (16, y - 5)]), FAM[fam][2])
    return c


def origami_kranich():
    c = I1.crane()
    recolor(c, 'white', 'blue')
    return c


def am_dummy():
    return Cv()


def yurei_laterne():
    c = I2.lantern()
    recolor(c, 'red', 'blue')
    recolor(c, 'orange', 'blue')
    recolor(c, 'gold', 'white')
    c.g(13, 12, "k...k\n.....\n.kkk.")
    return c


def chochin_feuer():
    return I2.lantern()


def hozuki():
    c = Cv()
    c.line([(16, 2), (16, 6)], 'f', 2)
    c.form(PG([(16, 5), (25, 12), (24, 22), (16, 29), (8, 22), (7, 12)]), '789', 2, 1, ring='K')
    for x in (12, 16, 20):
        c.line([(16, 6), (x, 28)], '7')
    c.fill(E(16, 19, 3, 3), 'Y')
    c.fill(E(15, 18, 1, 1), 'W')
    return c


def kitsune_laterne():
    c = I2.lantern()
    recolor(c, 'red', 'white')
    recolor(c, 'orange', 'blue')
    c.g(13, 11, "q...q\nqq.qq\n.qqq.")
    return c


def onryo_haar():
    c = Cv()
    for k in range(7):
        x0 = 8 + k * 2.6
        pts = [(x0, 4)] + [(x0 + math.sin(j * 0.9 + k) * 2.2 + j * 0.4, 4 + j * 3.6) for j in range(1, 8)]
        c.line(pts, 'h' if k % 2 else 'k', 2)
        c.line(pts, 'H')
    c.form(R(6, 2, 25, 5), 'qrR', 1, 1)
    return c


def jorogumo_seide():
    c = Cv()
    for k in range(8):
        a = k * math.tau / 8
        c.line([(16, 16), (16 + math.cos(a) * 14, 16 + math.sin(a) * 14)], 'w')
    for r in (4, 7.5, 11, 14):
        pts = [(16 + math.cos(k * math.tau / 8) * r, 16 + math.sin(k * math.tau / 8) * r) for k in range(9)]
        c.line(pts, 'W')
    c.form(E(21, 21, 3, 3.4), 'qrR', 1, 1)
    c.form(E(21, 17, 2, 2), 'khH', 0, 1)
    return c


def ryujin_bart():
    c = Cv()
    pts = [(3, 6), (9, 12), (15, 10), (21, 15), (25, 22), (29, 28)]
    c.line(pts, 'a', 3)
    c.line(pts, 'A')
    c.line([(5, 9), (11, 14), (17, 12), (22, 18), (26, 26)], 'z')
    sparkle(c, 25, 7, 'W', 'A')
    return c


def hyosube_haar():
    c = Cv()
    for k in range(9):
        a = math.radians(-150 + k * 15)
        c.line([(16, 24), (16 + math.cos(a) * 13, 24 + math.sin(a) * 15)], 'D' if k % 2 else 'd', 2)
    c.form(R(12, 23, 20, 28), 'qrR', 1, 1)
    return c


def sanzu_muenze():
    c = I1.coin()
    recolor(c, 'gold', 'iron')
    c.g(6, 25, "AAAA")
    return c


def kappa_teller():
    c = Cv()
    c.form(E(16, 17, 12, 8), 'fGl', 2, 1, ring='K')
    c.form(E(16, 16, 9, 5.4), 'zaA', 1, 1)
    c.fill(E(13, 15, 3, 1.4), 'W')
    for x in (6, 26):
        c.a[17, x] = 'F'
    return c


def shiro_kimono():
    c = Cv()
    body = PG([(10, 5), (22, 5), (29, 12), (25, 15), (23, 12), (23, 28), (9, 28), (9, 12), (7, 15), (3, 12)])
    c.form(body, 'nvW', 2, 1, ring='K')
    c.line([(13, 5), (18, 15), (18, 28)], 'v')
    c.line([(19, 5), (14, 15)], 'n')
    c.form(R(9, 16, 23, 18), 'vwW', 0, 1)
    c.form(PG([(14, 1), (18, 1), (19, 4), (13, 4)]), 'nvW', 0, 1)      # dreieckige Stirnbinde (Hitaikakushi)
    return c


def tigerfell():
    c = Cv()
    pelt = PG([(6, 6), (12, 3), (20, 3), (26, 6), (29, 14), (26, 24), (22, 29), (10, 29), (6, 24), (3, 14)])
    c.form(pelt, 'gyY', 2, 1, ring='K')
    for k in range(6):
        y = 7 + k * 4
        c.line([(6 + (k % 2) * 2, y), (12, y + 2)], 'k', 2)
        c.line([(26 - (k % 2) * 2, y), (20, y + 2)], 'k', 2)
    return c


def tenugui():
    c = Cv()
    c.form(PG([(4, 9), (28, 6), (27, 20), (5, 24)]), 'IJO', 2, 1, ring='K')
    for x in (8, 12, 16, 20, 24):
        for y in (11, 15, 19):
            c.a[y - (x - 4) // 8, x] = 'W'
    c.form(PG([(5, 24), (27, 20), (28, 25), (6, 29)]), 'IJO', 1, 1)
    return c


def hagoromo():
    c = Cv()
    pts = [(3, 26), (9, 18), (14, 22), (19, 12), (25, 8), (29, 3)]
    c.line(pts, 'w', 5)
    c.line(pts, 'W', 2)
    pts2 = [(5, 30), (12, 24), (18, 27), (23, 19), (29, 16)]
    c.line(pts2, 'A', 3)
    c.line(pts2, 'W')
    for x, y in ((8, 10), (24, 26), (13, 6)):
        sparkle(c, x, y, 'W', 'A')
    return c


def izanami_schleier():
    c = Cv()
    c.form(PG([(10, 3), (22, 3), (28, 28), (4, 28)]), 'xpP', 2, 1, ring='K')
    for x in range(6, 27, 4):
        c.line([(16, 4), (x, 28)], 'x')
    c.form(E(16, 11, 3.6, 4.2), 'bBi', 1, 1)
    c.g(14, 10, "k.k\n...\n.k.")
    return c


def izanami_kamm():
    c = Cv()
    c.form(PG([(4, 10), (28, 10), (27, 15), (5, 15)]), 'khH', 1, 1, ring='K')
    c.form(E(16, 10, 12, 4) & (px.Y < 11), 'khH', 1, 1)
    for x in range(6, 27, 2):
        c.line([(x, 15), (x, 24)], 'h')
    c.form(E(16, 9, 3, 2), 'xpP', 0, 1)
    c.g(10, 8, "X.......X")
    return c


def otohime_kamm():
    c = izanami_kamm()
    recolor(c, 'black', 'pink')
    recolor(c, 'purple', 'gold')
    c.fill(E(16, 9, 2.2, 1.6), 'A')
    return c


def gashadokuro_knochen():
    c = Cv()
    tube([(8, 24, 2.4), (24, 8, 2.4)], 'bone', c, 1, 1)
    for x, y in ((6, 26), (9, 27), (26, 6), (23, 5)):
        c.form(E(x, y, 3, 3), 'bBi', 1, 1)
    c.form(E(25, 25, 4, 4), 'bBi', 1, 1, ring='K')
    c.g(23, 24, "k.k\n...\n.k.")
    return c


def oni_horn():
    return I2.fang()


def gyuki_horn():
    c = Cv()
    pts = [(8, 28, 4), (9, 21, 3.5), (12, 14, 2.6), (17, 9, 1.8), (23, 6, 0.8)]
    tube(pts, 'black', c, 1, 1)
    c.form(R(4, 27, 13, 30), 'qrR', 1, 1)
    for k in range(3):
        c.line([(6 + k, 22 - k * 4), (11 + k, 23 - k * 4)], 'H')
    return c


def yamata_zahn():
    c = Cv()
    c.form(PG([(9, 4), (23, 4), (20, 18), (16, 29), (12, 18)]), 'bBi', 2, 1, ring='K')
    c.form(R(8, 2, 24, 6), 'fGl', 1, 1)
    c.line([(14, 8), (16, 24)], 'G')
    glow_dots(c, [(16, 27), (17, 29)], 'l')
    return c


def tesso_zahn():
    c = Cv()
    for x in (11, 18):
        c.form(PG([(x, 6), (x + 5, 6), (x + 5, 26), (x + 2.5, 29), (x, 26)]), '123', 2, 1, ring='K')
    c.form(R(9, 4, 25, 9), 'mST', 1, 1)
    return c


def omukade_gift():
    c = Cv()
    c.form(PG([(12, 3), (20, 3), (20, 9), (25, 16), (25, 28), (7, 28), (7, 16), (12, 9)]), 'zaA', 2, 1, ring='K')
    c.form(PG([(8, 17), (24, 17), (24, 27), (8, 27)]), 'xpP', 1, 1)
    c.form(R(11, 1, 21, 4), 'jdD', 1, 1)
    c.g(11, 20, "k.k.k.k.k\n.kkkkkkk.\nk.k.k.k.k")
    return c


def oni_sake():
    c = Cv()
    c.form(E(16, 15, 13, 5), 'qrR', 2, 1, ring='K')                    # flache Sakazuki
    c.form(E(16, 13, 10, 2.6), 'gyY', 0, 1)
    c.fill(E(16, 13, 8, 1.8), 'n')
    c.form(PG([(12, 19), (20, 19), (22, 24), (10, 24)]), 'qrR', 1, 1)
    c.g(13, 15, "kk.kk")
    return c


def shuten_schale():
    c = Cv()
    c.form(E(16, 16, 14, 8), 'UVR', 2, 1, ring='K')
    c.form(E(16, 13, 12, 4), 'qrR', 0, 1)
    c.fill(E(16, 13, 10, 3), 'U')
    c.fill(E(13, 12, 3, 0.8), 'R')
    c.form(R(10, 22, 22, 27), 'khH', 1, 1)
    for x in (8, 24):
        c.form(E(x, 16, 1.2, 1.2), 'gyY', 0, 1)
    return c


def shuten_kalebasse():
    return I2.gourd()


def sake_kalebasse():
    c = I2.gourd()
    recolor(c, 'straw', 'white')
    recolor(c, 'wood', 'white')
    recolor(c, 'gold', 'white')
    c.g(14, 19, "kkk\n.k.\nkkk")
    return c


def hyotan_sauger():
    c = I2.gourd()
    recolor(c, 'straw', 'orange')
    recolor(c, 'gold', 'orange')
    for k in range(5):
        a = k * math.tau / 5
        c.a[int(16 + math.sin(a) * 13), int(16 + math.cos(a) * 13)] = 'A'
    c.line([(16, 3), (12, 1)], 'A')
    return c


def akkoro_tinte():
    c = Cv()
    c.form(E(16, 20, 10, 8), 'khH', 2, 1, ring='K')
    c.form(E(16, 14, 6, 2.4), 'UVR', 0, 1)
    for k in range(4):
        x = 9 + k * 5
        c.line([(x, 14), (x - 2, 8), (x + 1, 4)], 'R', 2)
    c.form(R(13, 23, 19, 26), 'qrR', 0, 1)
    return c


NAMES = [n for n in dir() if not n.startswith('_') and callable(globals()[n]) and n not in (
    'recolor', 'glow_dots', 'sparkle', 'disc', 'blob', 'tube', 'kanji_plate', 'G', 'Cv', 'REL', 'STROKE', 'E', 'L', 'PG', 'R',
    'LN', 'sh', 'dil', 'col', 'render', 'save', 'am_dummy') and globals()[n].__module__ == __name__]


def build():
    for nm in NAMES:
        save('icons', nm, globals()[nm]())
