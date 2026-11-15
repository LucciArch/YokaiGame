"""Einzel-Symbole Teil 3: Wasser, Glück, Essen, Tempel, Allerlei."""
from ihelp import *
import icons_1 as I1, icons_2 as I2, icons_3 as I3


def kanagawa():
    return I3.wave()


def kappa_gurke():
    c = Cv()
    m = REL(16, 16, 13, 4.4, -40)
    c.form(m, 'FfG', 2, 1, ring='K')
    for k in range(7):
        x, y = 8 + k * 2.6, 24 - k * 2.6
        c.a[int(y), int(x)] = 'l'
    c.form(E(25, 6, 2, 2), 'gyY', 0, 1)
    c.line([(6, 26), (4, 29)], 'F', 2)
    return c


def suijin_schale():
    c = I1.cup()
    recolor(c, 'red', 'indigo')
    return c


def umibozu_auge():
    c = Cv()
    c.form(E(16, 17, 13, 11), 'IJO', 2, 1, ring='K')                  # dunkle Wassermasse
    c.form(E(16, 15, 7, 6), 'vwW', 1, 1)
    c.form(E(16, 15, 4, 4), '456', 1, 1)
    c.fill(E(16, 15, 1.8, 3), 'k')
    c.fill(E(14, 13, 1, 1), 'W')
    for x in (5, 10, 22, 27):
        c.line([(x, 25), (x + 2, 29)], 'J')
    return c


def tengu_auge():
    c = I2.eye()
    recolor(c, 'gold', 'red')
    return c


def mokumoku_auge():
    c = Cv()
    c.form(R(4, 4, 27, 27), 'dDt', 1, 1, ring='K')
    c.form(R(6, 6, 25, 25), 'nvW', 1, 1)
    for x in (12, 19):
        c.line([(x, 6), (x, 25)], 'd')
    for y in (12, 19):
        c.line([(6, y), (25, y)], 'd')
    for cx, cy in ((9, 9), (16, 9), (22, 16), (9, 22), (16, 16), (22, 22)):
        c.fill(E(cx, cy, 2.4, 1.6), 'W')
        c.fill(E(cx, cy, 1, 1.2), 'k')
        c.a[cy, cx - 2] = 'k'; c.a[cy, cx + 2] = 'k'
    return c


def tenome_handschuh():
    c = Cv()
    hand = E(16, 19, 8, 9)
    for k in range(4):
        hand |= L(10 + k * 4, 14, 1.8, 9 + k * 4.5, 4, 1.6)
    hand |= L(9, 20, 2, 3, 15, 1.6)
    c.form(hand, 'bBi', 2, 1, ring='K')
    c.form(E(16, 20, 4, 3), 'vwW', 1, 1)
    c.fill(E(16, 20, 2, 2.4), 'q')
    c.fill(E(16, 20, 0.9, 1.4), 'k')
    return c


def ryu_schuppe():
    c = Cv()
    m = PG([(16, 3), (27, 10), (25, 22), (16, 29), (7, 22), (5, 10)])
    c.form(m, '456', 2, 1, ring='K')
    for k in range(3):
        y = 10 + k * 6
        arc = E(16, y, 8 - k, 5) & ~E(16, y - 1.5, 8 - k, 5) & m
        c.fill(arc, '4')
    c.fill(E(13, 8, 2, 1), 'W')
    return c


def yuki_traene():
    c = Cv()
    c.form(PG([(16, 2), (23, 15), (23, 21), (16, 28), (9, 21), (9, 15)]), 'zaA', 2, 1, ring='K')
    c.fill(PG([(16, 6), (19, 15), (16, 13)]), 'W')
    for k in range(6):
        a = k * math.tau / 6
        c.line([(16 + math.cos(a) * 1, 20 + math.sin(a) * 1), (16 + math.cos(a) * 4, 20 + math.sin(a) * 4)], 'W')
    return c


def nurikabe_stein():
    c = Cv()
    c.form(PG([(4, 8), (14, 4), (27, 7), (29, 22), (21, 28), (6, 26), (3, 17)]), '123', 2, 1, ring='K')
    c.line([(10, 10), (14, 16), (12, 22)], '0'); c.line([(20, 9), (23, 18)], '0')
    c.g(12, 13, "k...k\n.....\n.kkk.")                               # stilles Gesicht
    c.fill(E(24, 23, 2, 1.4), 'f')
    return c


def kyubi_juwel():
    c = Cv()
    c.form(PG([(16, 4), (25, 14), (16, 29), (7, 14)]), '789', 2, 1, ring='K')
    c.fill(PG([(16, 4), (25, 14), (16, 14)]), '9')
    c.fill(PG([(16, 14), (25, 14), (16, 29)]), '7')
    c.fill(E(16, 15, 2.4, 3.6), 'Y')
    c.fill(E(16, 15, 1, 2.4), 'k')                                    # Fuchsauge
    for x, y in ((5, 6), (27, 26)):
        sparkle(c, x, y, 'W', 'Y')
    return c


def koban():
    c = Cv()
    c.form(E(16, 16, 9, 13), 'ogy', 2, 1, ring='K')
    for y in range(6, 27, 3):
        c.line([(9, y), (23, y)], 'g')
    c.form(E(16, 11, 3, 3), 'ogy', 0, 1)
    c.form(E(16, 21, 3, 3), 'ogy', 0, 1)
    c.g(14, 15, "kkkk")
    return c


def daikoku_hammer():
    return I2.hammer()


def uchide_kozuchi():
    c = I2.hammer()
    recolor(c, 'gold', 'red')
    c.g(10, 8, "Y...Y\n.YYY.")
    for x, y in ((25, 24), (6, 26)):
        sparkle(c, x, y)
    return c


def daruma_otoshi():
    c = Cv()
    for k, fam in enumerate(('blue', 'green', 'gold', 'red')):
        y = 26 - k * 5
        c.form(R(9, y - 4, 23, y), RAMP3[fam], 1, 1, ring='K')
    c.form(E(16, 6, 5, 4.6), 'qrR', 1, 1)
    c.g(14, 5, "k.k")
    tube([(25, 30, 1.2), (28, 18, 1.2)], 'wood', c)
    c.form(R(23, 14, 31, 18), 'dDt', 1, 1)
    return c


def maneki_neko():
    c = Cv()
    c.form(E(15, 22, 9, 8), 'nvW', 2, 1, ring='K')
    c.form(E(15, 11, 8, 7), 'nvW', 2, 1, ring='K')
    for sx in (-1, 1):
        c.form(PG([(15 + sx * 3, 6), (15 + sx * 8, 1), (15 + sx * 8, 8)]), 'nvW', 1, 1)
    c.form(L(23, 14, 2.2, 26, 5, 2.4), 'nvW', 1, 1)                  # winkende Pfote
    c.g(11, 10, "k.....k\n.......\n...R...")
    c.form(R(9, 16, 21, 17), 'qrR', 0, 1)
    c.form(E(15, 19, 1.6, 1.6), 'gyY', 0, 1)
    c.form(E(15, 24, 4.4, 3.4), 'gyY', 1, 1)                          # Koban in der Hand
    c.fill(R(14, 23, 16, 24), 'g')
    return c


def komainu():
    c = Cv()
    c.form(R(5, 26, 27, 29), '123', 1, 1)
    c.form(E(15, 19, 8, 7), '123', 2, 1, ring='K')
    c.form(E(18, 10, 7, 6), '123', 2, 1, ring='K')
    for k in range(5):
        c.form(E(12 + k * 3, 6 - (k % 2), 2, 2), '012', 0, 1)         # Lockenmähne
    c.g(16, 9, "k...k\n.....\nWWWWW")
    c.form(L(7, 18, 1.8, 4, 10, 2.6), '123', 1, 1)
    return c


def jinmen_frucht():
    c = Cv()
    c.line([(16, 2), (16, 7)], 'd', 2)
    c.form(REL(21, 5, 4, 1.8, -25), 'FfG', 0, 1)
    c.form(E(16, 18, 11, 11), '789', 2, 1, ring='K')
    c.g(10, 13, "kk....kk\n........\n..k..k..\n.kkkkkk.\n..kkkk..")
    c.fill(E(11, 19, 1.4, 1), 'm'); c.fill(E(21, 19, 1.4, 1), 'm')
    return c


def daruma():
    return I1.daruma()


def teru_teru():
    c = Cv()
    c.form(E(16, 11, 8, 8), 'nvW', 2, 1, ring='K')
    c.form(PG([(9, 15), (23, 15), (27, 29), (20, 26), (16, 30), (12, 26), (5, 29)]), 'nvW', 2, 1)
    c.form(R(9, 16, 23, 17), 'qrR', 0, 1)
    c.g(12, 9, "k...k\n.....\n.k.k.\n..k..")
    c.line([(16, 3), (16, 1)], 'd')
    return c


def tanuki_beutel():
    return I1.bag()


def kiyome_sack():
    c = I1.bag()
    recolor(c, 'wood', 'white')
    recolor(c, 'red', 'blue')
    c.fill(PG([(12, 10), (20, 10), (16, 4)]) & ~c.m, 'W')
    sparkle(c, 25, 7)
    return c


def tanuki_blatt_p():
    return I2.leaf()


def tanuki_blatt():
    c = I2.leaf()
    recolor(c, 'green', 'gold')
    c.form(E(9, 25, 3.6, 3), 'jdD', 1, 1)                             # Tanuki-Nase/Gesicht
    c.g(7, 24, "k...k")
    return c


def wasabi():
    c = Cv()
    c.form(L(16, 28, 2.6, 16, 14, 4.6), 'fGl', 2, 1, ring='K')
    for k in range(5):
        c.line([(12, 16 + k * 3), (20, 15 + k * 3)], 'F')
    for a in (-120, -90, -60):
        r = math.radians(a)
        tube([(16, 12, 1), (16 + math.cos(r) * 7, 12 + math.sin(r) * 7, 1)], 'green', c, 0, 0)
        c.form(E(16 + math.cos(r) * 9, 12 + math.sin(r) * 9, 3.4, 3), 'FfG', 1, 1)
    return c


def sakura_zweig():
    return I2.flower()


def onigiri():
    return I3.rice()


def bento():
    c = Cv()
    c.form(R(3, 7, 28, 26), 'khH', 2, 1, ring='K')
    c.form(R(5, 9, 26, 24), 'qrR', 1, 0)
    c.form(R(6, 10, 15, 23), 'nvW', 1, 1)                             # Reis
    c.form(E(10.5, 16.5, 2.2, 2.2), 'qrR', 0, 1)                      # Umeboshi
    c.form(R(17, 10, 25, 16), '789', 1, 1)                            # Tamagoyaki
    c.form(R(17, 18, 25, 23), 'FfG', 1, 1)
    c.fill(E(21, 20.5, 2, 1.4), 'm')
    return c


def mochi():
    c = Cv()
    for x, y in ((10, 20), (21, 21), (16, 12)):
        c.form(E(x, y, 6.5, 5), 'nvW', 2, 1, ring='K')
    c.fill(E(16, 11, 2, 1), 'm')
    c.form(R(4, 25, 27, 28), 'dDt', 1, 1)
    return c


def kagami_mochi():
    c = Cv()
    c.form(R(5, 24, 26, 29), 'dDt', 1, 1, ring='K')                   # Sanbō-Ständer
    c.form(E(16, 20, 10, 4.6), 'nvW', 2, 1)
    c.form(E(16, 14, 7.6, 3.8), 'nvW', 2, 1)
    c.form(E(16, 8, 4, 3.4), '789', 1, 1)                             # Daidai-Orange
    c.form(REL(19, 4, 3, 1.4, -30), 'FfG', 0, 1)
    c.g(6, 17, "q.........q")
    return c


def umeboshi():
    c = Cv()
    c.form(E(16, 19, 10, 9), 'UVR', 2, 1, ring='K')
    for x, y in ((12, 15), (20, 18), (14, 23)):
        c.line([(x, y), (x + 3, y + 1)], 'U')
    c.fill(E(13, 15, 2, 1.2), 'e')
    c.form(REL(20, 8, 5, 2, -30), 'FfG', 1, 1)                        # Shiso-Blatt
    return c


def natto():
    c = Cv()
    c.form(E(16, 21, 12, 8) & (px.Y > 17), 'khH', 1, 1, ring='K')
    c.form(E(16, 18, 12, 3.4), 'qrR', 0, 1)
    for x, y in ((9, 17), (12, 16), (15, 17), (18, 16), (21, 17), (24, 18), (13, 19), (19, 19)):
        c.form(E(x, y, 1.6, 1.3), '789', 0, 1)
    c.line([(12, 15), (14, 8), (20, 3)], 'w'); c.line([(18, 15), (21, 9)], 'w')
    c.line([(6, 5), (13, 15)], 'd', 2); c.line([(9, 4), (15, 14)], 'd', 2)   # Stäbchen
    return c


def dango():
    return I1.dango()


def matcha():
    c = Cv()
    c.form(E(16, 19, 12, 9) & (px.Y > 15), 'jdD', 2, 1, ring='K')
    c.form(E(16, 16, 12, 3.6), 'FfG', 0, 1)
    c.fill(E(14, 15, 5, 1.2), 'l')
    c.form(R(11, 27, 21, 29), 'jdD', 0, 1)
    tube([(25, 2, 1.6), (21, 12, 2.2)], 'straw', c)                   # Chasen (Besen)
    for k in range(4):
        c.line([(19 + k, 11), (19 + k, 15)], 'c')
    return c


def kintsugi():
    c = I1.cup()
    recolor(c, 'red', 'black')
    c.line([(6, 14), (12, 19), (11, 24)], 'Y'); c.line([(20, 15), (24, 21), (21, 26)], 'Y'); c.line([(12, 19), (20, 18)], 'Y')
    return c


def oni_sake_dummy():
    return Cv()


def abura_schale():
    c = Cv()
    c.form(E(16, 22, 12, 5), 'qrR', 2, 1, ring='K')
    c.form(E(16, 20, 10, 2.6), 'gyY', 0, 1)
    c.fill(E(16, 20, 8, 1.6), '9')
    c.form(PG([(19, 6), (23, 14), (20, 19), (16, 17), (16, 12)]), '789', 1, 1)
    c.fill(E(19.5, 15, 1.4, 2), 'Y')
    tube([(19, 19, 0.6), (21, 18, 0.6)], 'white', c, 0, 0)
    return c


def bonsho():
    c = Cv()
    c.form(R(2, 3, 29, 5), 'jdD', 1, 1, ring='K')
    c.form(PG([(10, 6), (22, 6), (25, 27), (7, 27)]), '012', 2, 1, ring='K')
    c.form(E(16, 6, 6, 3), '012', 1, 1)
    for y in (12, 17):
        c.line([(9, y), (23, y)], '0')
    for x in (11, 14, 18, 21):
        for y in (8, 10):
            c.a[y, x] = '3'
    c.form(R(6, 26, 26, 28), '123', 0, 1)
    tube([(29, 21, 1.2), (31, 21, 1.2)], 'wood', c, 0, 0)
    return c


def neko_gloeckchen():
    return I1.bell()


def furin():
    c = Cv()
    c.line([(16, 1), (16, 4)], 'k')
    c.form(E(16, 10, 7, 6) & (px.Y < 13), 'zaA', 1, 2, ring='K')
    c.fill(E(16, 9, 4, 3) & (px.Y < 10), 'W')
    c.g(12, 9, "q.....q")
    c.line([(16, 13), (16, 20)], 'k')
    c.form(R(13, 20, 19, 28), 'nvW', 1, 1, ring='K')                  # Tanzaku
    c.g(15, 22, "q\nq\nq")
    return c


def kagura_suzu():
    c = Cv()
    tube([(16, 30, 1.3), (16, 18, 1.3)], 'red', c)
    for y, n in ((7, 1), (11, 3), (15, 5)):
        for k in range(n):
            x = 16 + (k - (n - 1) / 2) * 4.6
            c.form(E(x, y, 2.2, 2.2), 'ogy', 1, 1, ring='K')
    for x, col_ in ((10, 'q'), (13, 'Y'), (19, 'F'), (22, 'J')):
        c.line([(16, 19), (x, 28)], col_)
    return c


def mokugyo():
    c = Cv()
    c.form(E(15, 17, 12, 10), 'qrR', 2, 1, ring='K')                  # Holzfisch
    c.fill(PG([(5, 18), (25, 18), (25, 20), (5, 20)]), 'k')
    c.g(7, 12, "kk..........kk")
    c.form(E(27, 6, 2.6, 2.6), 'jdD', 1, 1)
    tube([(20, 13, 1), (26, 7, 1)], 'wood', c, 0, 0)
    return c


def horagai():
    c = Cv()
    pts = [(5, 25, 3.6), (10, 22, 4.6), (16, 17, 5.2), (21, 12, 4.4), (25, 8, 3), (28, 5, 1.6)]
    tube(pts, 'pink', c, 2, 1)
    for k in range(4):
        x, y = 11 + k * 4, 21 - k * 3.6
        c.line([(x - 2, y - 3), (x + 2, y + 3)], 'S')
    c.form(E(5, 25, 3.6, 3.6), 'mST', 0, 1)
    c.fill(E(5, 25, 1.8, 1.8), 'U')
    c.line([(12, 25), (22, 29)], 'q')                                 # Kordel
    return c


def horagai_a():
    return horagai()


def sazae_muschel():
    c = Cv()
    m = PG([(16, 3), (25, 18), (22, 27), (10, 27), (7, 18)])
    c.form(m, 'mST', 2, 1, ring='K')
    for k in range(4):
        y = 8 + k * 5
        c.line([(16 - k * 2.4, y), (16 + k * 2.4, y)], 'm')
        c.fill(E(16 - k * 2.6 - 1, y + 1, 1, 1), 'T'); c.fill(E(16 + k * 2.6 + 1, y + 1, 1, 1), 'T')
    c.form(E(16, 24, 4, 2.4), 'ubB', 0, 1)
    return c


def ema():
    c = Cv()
    c.form(PG([(4, 12), (16, 4), (28, 12), (28, 27), (4, 27)]), 'dDt', 2, 1, ring='K')
    c.line([(4, 12), (16, 4), (28, 12)], 'q', 2)
    c.form(E(11, 19, 3.4, 3), '789', 0, 1)                            # gemaltes Pferd/Wunsch
    c.g(17, 15, "kk.k\n.k.k\nkkkk\n.k..")
    c.line([(16, 2), (16, 5)], 'R')
    return c


def tamatebako():
    return I1.box()


def enenra_pfeife():
    c = Cv()
    tube([(4, 28, 1.0), (21, 13, 1.0)], 'iron', c)
    c.form(E(22, 12, 3, 2.4), '012', 1, 1)
    for k, (x, y, r) in enumerate(((22, 7, 2.4), (19, 4, 2), (24, 3, 1.6), (27, 6, 1.8))):
        c.form(E(x, y, r, r), 'vwW', 0, 1)
    c.g(19, 6, "k.k")
    return c


def nurarihyon_pfeife():
    c = Cv()
    tube([(3, 26, 0.9), (24, 9, 0.9)], 'black', c)
    c.form(R(2, 25, 6, 28), 'ogy', 0, 1)
    c.form(E(25, 8, 3.4, 2.4), 'ogy', 1, 1, ring='K')
    c.fill(E(25, 7, 1.6, 0.8), '9')
    for x, y in ((27, 3), (24, 2), (29, 6)):
        c.a[y, x] = 'w'
    return c


def ebisu_angel():
    c = Cv()
    tube([(4, 29, 1.0), (22, 3, 0.7)], 'wood', c)
    c.line([(22, 3), (26, 14), (25, 18)], 'w')
    c.form(REL(22, 22, 6, 3.6, -60), 'qrR', 1, 1, ring='K')           # Tai-Fisch
    c.fill(PG([(19, 27), (16, 30), (21, 29)]), 'R')
    c.a[18, 24] = 'k'
    return c


def koinobori():
    c = Cv()
    tube([(3, 2, 0.9), (3, 30, 0.9)], 'wood', c)
    for k, (y, fam) in enumerate(((7, 'black'), (16, 'red'), (25, 'blue'))):
        body = PG([(5, y - 3), (24, y - 3 + k % 2), (29, y - 4), (26, y), (29, y + 4), (24, y + 3), (5, y + 3)])
        c.form(body, RAMP3[fam], 1, 1, ring='K')
        c.form(E(8, y, 2, 2), 'nvW', 0, 0)
        c.a[y, 8] = 'k'
        for x in (12, 16, 20):
            c.a[y - 1, x] = FAM[fam][2]
    return c


def fugu():
    c = I2.fish()
    recolor(c, 'red', 'gold')
    for k in range(10):
        a = k * math.tau / 10
        x, y = 15 + math.cos(a) * 11, 16 + math.sin(a) * 9
        if 0 <= int(y) < 32 and 0 <= int(x) < 32 and not c.m[int(y), int(x)]:
            c.a[int(y), int(x)] = 'o'
    return c


def omamori_kenko():
    return omamori_v('red', "..#..\n#####\n..#..\n.#.#.\n#...#")


def omamori_kinun():
    return omamori_v('gold', "#####\n#.#.#\n#####\n..#..\n#####")


def omamori_yakuyoke():
    return omamori_v('blue', "#.#.#\n.###.\n##.##\n.###.\n#.#.#")


def omamori_gokaku():
    return omamori_v('green', "..#..\n.###.\n#.#.#\n..#..\n.#.#.")


def omamori_v(fam, glyph):
    c = I3.omamori()
    recolor(c, 'purple', fam)
    rows = glyph.split('\n')
    for j, r_ in enumerate(rows):
        for i, ch in enumerate(r_):
            if ch == '#':
                c.a[16 + j, 14 + i] = 'k'
    return c


def hyakki_rolle():
    c = Cv()
    c.form(R(3, 9, 28, 22), 'cCs', 1, 1, ring='K')
    c.form(R(1, 8, 4, 23), 'jdD', 1, 1); c.form(R(27, 8, 30, 23), 'jdD', 1, 1)
    for k, (x, y) in enumerate(((7, 18), (12, 16), (17, 18), (22, 15))):  # Dämonenparade
        c.form(E(x, y, 2.2, 2.6), 'khH', 0, 0)
        c.a[y - 3, x - 1] = 'k'; c.a[y - 3, x + 1] = 'k'
        c.a[y - 1, x] = 'R'
    c.line([(5, 12), (25, 11)], 'q')
    return c


NAMES = ['kanagawa', 'kappa_gurke', 'suijin_schale', 'umibozu_auge', 'tengu_auge', 'mokumoku_auge', 'tenome_handschuh',
         'ryu_schuppe', 'yuki_traene', 'nurikabe_stein', 'kyubi_juwel', 'koban', 'daikoku_hammer', 'uchide_kozuchi',
         'daruma_otoshi', 'maneki_neko', 'komainu', 'jinmen_frucht', 'daruma', 'teru_teru', 'tanuki_beutel', 'kiyome_sack',
         'tanuki_blatt_p', 'tanuki_blatt', 'wasabi', 'sakura_zweig', 'onigiri', 'bento', 'mochi', 'kagami_mochi', 'umeboshi',
         'natto', 'dango', 'matcha', 'kintsugi', 'abura_schale', 'bonsho', 'neko_gloeckchen', 'furin', 'kagura_suzu', 'mokugyo',
         'horagai', 'sazae_muschel', 'ema', 'tamatebako', 'enenra_pfeife', 'nurarihyon_pfeife', 'ebisu_angel', 'koinobori',
         'fugu', 'omamori_kenko', 'omamori_kinun', 'omamori_yakuyoke', 'omamori_gokaku', 'hyakki_rolle']


def build():
    for nm in NAMES:
        save('icons', nm, globals()[nm]())
