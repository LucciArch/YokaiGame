"""Hi-Res-Raumobjekte (direkt in Hi-Res-Pixeln, wie shared_hi): Torii-Pforten, Hokora (Kami/Oni), Tanuki-Automat.
Licht von oben links, Umriss K, Schatten nach unten rechts.
usage: python3 objects_hi.py   (schreibt nach yokai/assets/env/_shared/)"""
import os
import numpy as np
from core import *
from shared_hi import STONE, MOSS, ROPE, PAPER, SHADOW, finish

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, '..', '..', '..', 'yokai', 'assets', 'env', '_shared')

BLACK = ('#0e0a12', '#1e1822', '#342c38', '#544a58')
GOLD = ('#5a3414', '#96661c', '#d8a838', '#f8e08a')
WOOD = ('#1e1216', '#3e2620', '#62402c', '#8a6040')
CU = ('#14302c', '#245448', '#3e8068', '#7ab898')        # Kupferdach mit Grünspan
FUR = ('#2a1810', '#5a3820', '#8a5a30', '#b88a50', '#e0c090')

# Torii-Farben je Pforte: (dunkel, mittel, hell, Glanz)
TORII = {
    'torii': ('#4a0c14', '#8e1a1e', '#c8382a', '#ec7050'),     # Shu-Zinnober
    'heaven': ('#5a3414', '#a0701c', '#e0b040', '#fbe89a'),    # Blattgold
    'victory': ('#6a6878', '#b0aebc', '#e6e4ec', '#ffffff'),   # weißes Holz (Shiraki)
    'yomi': ('#200c2a', '#46204e', '#743c78', '#a870a4'),      # morscher Violettlack
    'iwato': ('#6a2a0c', '#c0601a', '#f0a030', '#ffe080'),     # Sonnenorange
}
ORDER = ['torii', 'heaven', 'victory', 'yomi', 'iwato']


def ramp(c):
    return (c[0], c[1], c[2])


def torii(kind):
    c = TORII[kind]
    cv = Cv(96, 80, ss=1)
    # Pfeiler (hashira), unten etwas breiter
    for x0 in (19, 69):
        p = cv.PG([(x0 + 1, 18), (x0 + 7, 18), (x0 + 8, 70), (x0, 70)])
        cv.form(p, ramp(c), 3, 1)
        cv.vl(x0 + 2, 20, 68, c[3])
    # Nuki (unterer Querbalken), steckt durch die Pfeiler
    nk = cv.R(11, 30, 84, 35)
    cv.form(nk, ramp(c), 2, 1)
    cv.hl(12, 83, 30, c[3])
    for x in (11, 84):
        cv.vl(x, 30, 35, c[0])
    # Kusabi-Keile am Nuki
    for x in (17, 28, 67, 78):
        cv.form(cv.R(x, 29, x + 1, 36), BLACK[1:], 0, 1)
    # Gakuzuka mit Tafel (gaku)
    cv.form(cv.R(45, 20, 50, 30), ramp(c), 1, 1)
    gk = cv.R(40, 19, 55, 33)
    cv.fill(gk, GOLD[1])
    cv.fill(cv.R(41, 20, 54, 32), BLACK[1])
    cv.fill(cv.R(42, 21, 53, 31), BLACK[2])
    for y in (23, 26, 29):                                 # goldene Schriftzeichen
        cv.hl(45, 50, y, GOLD[2])
        cv.px(47, y + 1, GOLD[2]); cv.px(48, y - 1 if y > 23 else y + 1, GOLD[3])
    # Shimaki (oberer Balken in Farbe)
    sm = cv.R(9, 15, 86, 19)
    cv.form(sm, ramp(c), 2, 1)
    cv.hl(10, 85, 15, c[3])
    # Kasagi (schwarzer, geschwungener Abschluss)
    top = [(2, 4), (10, 9), (28, 11), (48, 11.5), (68, 11), (86, 9), (94, 4), (93, 7), (86, 13), (68, 14.5),
           (48, 15), (28, 14.5), (10, 13), (3, 7)]
    ks = cv.PG(top)
    cv.form(ks, BLACK[:3], 2, 1)
    cv.line([(4, 5), (11, 10), (28, 12), (68, 12), (85, 10), (92, 5)], BLACK[3])
    # Kamaki (schwarze Sockelhülsen) und Steinfuß
    for x0 in (17, 67):
        cv.form(cv.R(x0, 62, x0 + 11, 71), BLACK[:3], 2, 1)
        cv.hl(x0, x0 + 11, 62, BLACK[3])
        cv.form(cv.R(x0 - 2, 72, x0 + 13, 75), (STONE[1], STONE[2], STONE[3]), 1, 1)
    if kind == 'yomi':                                     # abblätternder Lack, Risse
        for (x, y) in ((22, 40), (24, 52), (71, 44), (73, 26), (30, 32), (60, 17)):
            cv.fill(cv.E(x, y, 1.6, 2.6) & cv.m, c[0])
            cv.px(x - 1, y - 2, BLACK[3])
    if kind in ('torii', 'heaven', 'iwato'):               # Shimenawa mit Shide unter dem Nuki
        for x in range(21, 76):
            t = (x - 21) / 54
            y = int(round(38 + 4 * np.sin(np.pi * t)))
            cv.px(x, y, ROPE[2] if x % 3 else ROPE[1])
            cv.px(x, y + 1, ROPE[1] if x % 3 else ROPE[0])
        for x in (33, 47, 61):
            t = (x - 21) / 54
            y = int(round(38 + 4 * np.sin(np.pi * t))) + 2
            cv.grid(x, y, "ab\nab\n.ab\n.ab\nab\nab", dict(a=PAPER[1], b=PAPER[2]))
    if kind == 'victory':                                  # silberne Beschläge
        for x0 in (19, 69):
            cv.hl(x0, x0 + 8, 22, '#8a8aa0'); cv.hl(x0, x0 + 8, 24, '#8a8aa0')
    return finish(cv, 48, 75, 42)


def hokora(oni):
    cv = Cv(64, 72, ss=1)
    S = STONE
    # Steinsockel, zweistufig
    cv.form(cv.R(8, 62, 55, 68), (S[0], S[1], S[2]), 2, 1)
    cv.hl(8, 55, 62, S[3])
    cv.form(cv.R(12, 56, 51, 61), (S[1], S[2], S[3]), 2, 1)
    cv.hl(12, 51, 56, S[4])
    wd = WOOD if not oni else ('#1a0c10', '#36141a', '#561e22', '#7a2c28')
    # Körper mit Pfosten
    cv.form(cv.R(16, 30, 47, 55), (wd[0], wd[1], wd[2]), 3, 1)
    for x in (16, 46):
        cv.form(cv.R(x, 28, x + 2, 55), (wd[1], wd[2], wd[3]), 1, 1)
    # Schwelle und Stufe
    cv.form(cv.R(14, 52, 49, 55), (wd[0], wd[1], wd[2]), 1, 1)
    cv.hl(14, 49, 52, wd[3])
    # Öffnung mit halb geöffneten Gittertüren (kitsune-goshi)
    cv.fill(cv.R(21, 33, 42, 51), '#07050a')
    for x0 in (20, 37):
        d = cv.R(x0, 33, x0 + 6, 51)
        cv.fill(d, wd[1])
        for y in range(35, 51, 3):
            cv.hl(x0 + 1, x0 + 5, y, wd[0])
        for x in range(x0 + 1, x0 + 6, 2):
            cv.vl(x, 34, 50, wd[0])
        cv.vl(x0, 33, 51, wd[3])
    if not oni:                                            # Shintai: Bronzespiegel auf Ständer, warm leuchtend
        cv.fill(cv.E(31.5, 46, 6, 7), '#2a1a10')
        cv.form(cv.R(30, 46, 33, 50), GOLD[:3], 1, 1)
        mr = cv.E(31.5, 41, 4.5, 4.5)
        cv.fill(dil(mr), GOLD[0])
        cv.form(mr, (GOLD[1], GOLD[2], GOLD[3]), 2, 1)
        cv.fill(cv.E(30, 39.5, 1.4, 1.4), '#fffbe0')
        for x in (28, 35):                                 # Sakaki-Zweige in Vasen
            cv.form(cv.R(x - 1, 47, x + 1, 51), ('#5a5e72', '#a0a4b8', '#e8ecf4'), 1, 1)
            cv.fill(cv.E(x, 45, 1.8, 2.2), MOSS[1]); cv.px(x - 1, 44, MOSS[2])
    else:                                                  # zwei rote Augen im Dunkel, Knochen an der Schwelle
        for x in (27, 36):
            cv.fill(cv.E(x, 41, 2.2, 1.4), '#8a0c18')
            cv.fill(cv.E(x, 41, 1.2, .8), '#ff4030')
            cv.px(x - 1, 40, '#ffc0a0')
        cv.line([(23, 50), (30, 48)], '#b8a888'); cv.px(22, 50, '#d8ccb0'); cv.px(31, 48, '#d8ccb0')
    # Satteldach mit Giebel
    rf = CU if not oni else BLACK
    roof = cv.PG([(4, 30), (14, 18), (31.5, 9), (49, 18), (59, 30), (56, 31), (31.5, 15), (7, 31)])
    body = cv.PG([(9, 30), (31.5, 13), (54, 30)])
    cv.form(body | roof, (rf[0], rf[1], rf[2]), 3, 1)
    cv.line([(5, 29), (14, 19), (31, 10)], rf[3])
    cv.fill(cv.PG([(15, 29), (31.5, 17), (48, 29)]), wd[1])    # Giebelfeld
    cv.line([(15, 29), (31.5, 17), (48, 29)], wd[0])
    cv.hl(15, 48, 29, wd[0])
    cv.fill(cv.E(31.5, 24, 2.6, 2.6), GOLD[2] if not oni else '#a01820')   # Mon im Giebel
    cv.px(31, 23, GOLD[3] if not oni else '#ff6040')
    if not oni:                                            # Chigi (gekreuzte Giebelbalken) und Katsuogi
        cv.line([(27, 13), (24, 4)], WOOD[2]); cv.line([(28, 13), (25, 4)], WOOD[1])
        cv.line([(36, 13), (39, 4)], WOOD[2]); cv.line([(35, 13), (38, 4)], WOOD[1])
        cv.form(cv.R(28, 8, 35, 10), GOLD[:3], 1, 1)
        # Shimenawa mit Shide
        for x in range(13, 51):
            y = int(round(31 + 2.2 * np.sin(np.pi * (x - 13) / 37)))
            cv.px(x, y, ROPE[2] if x % 3 else ROPE[1]); cv.px(x, y + 1, ROPE[1] if x % 3 else ROPE[0])
        for x in (21, 41):
            cv.grid(x, 33, "ab\nab\n.ab\n.ab\nab", dict(a=PAPER[1], b=PAPER[2]))
    else:                                                  # Oni-Hörner am First, zerrissene Ofuda
        for sx in (-1, 1):
            hm = cv.PG([(31.5 + sx * 5, 13), (31.5 + sx * 3, 12), (31.5 + sx * 10, 2), (31.5 + sx * 9, 7)])
            cv.form(hm, ('#6a5a4a', '#b8a888', '#e0d4bc'), 1, 1)
        for (x, y) in ((18, 36), (44, 38)):
            cv.form(cv.R(x, y, x + 3, y + 8), PAPER, 1, 1)
            cv.vl(x + 1, y + 2, y + 6, '#a01820')
            cv.px(x + 3, y + 8, (0, 0, 0, 0))
        for (x, y) in ((10, 61), (50, 61)):
            cv.grid(x, y, "a.a\n.a.", dict(a='#b8a888'))
    for (x, y, r) in ((10, 62, 2.4), (52, 57, 1.8)):    # Moos am Sockel
        m = cv.E(x, y, r * 1.4, r * .8) & cv.m
        cv.fill(m, MOSS[1]); cv.fill(m & ~sh(m, 1, 1), MOSS[2])
    return finish(cv, 32, 68, 26)


def slots():
    """Tanuki-Automat: rot lackierter Kasten in Form eines Shigaraki-Tanuki mit Strohhut; das Fenster bleibt
    durchsichtig – darunter zeichnet das Spiel die drehenden Walzen."""
    cv = Cv(64, 88, ss=1)
    F = FUR
    red = ('#3a0c14', '#8e1a1e', '#c8382a', '#ec7050')
    # Füße
    for x in (14, 40):
        cv.form(cv.E(x + 5, 82, 7, 4), (F[0], F[1], F[2]), 1, 1)
    # Kasten
    box = cv.R(8, 36, 55, 80) | cv.E(31.5, 36, 23.5, 6)
    cv.form(box, ramp(red), 4, 1)
    cv.hl(9, 54, 37, red[3])
    # goldene Zierleisten
    for y in (42, 73):
        cv.form(cv.R(8, y, 55, y + 2), GOLD[1:], 1, 1)
    # Fenster-Rahmen (das Innere wird später ausgestanzt)
    cv.form(cv.R(12, 45, 51, 61), (GOLD[0], GOLD[1], GOLD[2]), 1, 1)
    # Münzschlitz-Platte mit Kanji-Plakette
    cv.form(cv.R(21, 64, 42, 71), GOLD[:3], 1, 1)
    cv.fill(cv.R(28, 66, 35, 67), '#1a0e0a')
    cv.hl(22, 41, 64, GOLD[3])
    # Hebel rechts mit roter Kugel
    cv.form(cv.R(55, 50, 58, 54), BLACK[1:], 1, 1)
    cv.line([(57, 50), (60, 34)], BLACK[3]); cv.line([(58, 50), (61, 34)], BLACK[2])
    bl = cv.E(60.5, 32, 3, 3)
    cv.form(bl, ('#7a0c14', '#d02a2a', '#ff8a6a'), 1, 1)
    # Kopf: Tanuki mit Augenmaske, weißer Schnauze, Ohren
    head = cv.E(31.5, 24, 14, 11)
    for sx in (-1, 1):
        ear = cv.E(31.5 + sx * 10, 15, 4, 4)
        cv.form(ear, (F[0], F[1], F[2]), 1, 1)
        cv.fill(cv.E(31.5 + sx * 10, 15.5, 2, 2), F[0])
    cv.form(head, (F[1], F[2], F[3]), 3, 1)
    mask = cv.E(24.5, 24, 6, 4) | cv.E(38.5, 24, 6, 4) | cv.R(28, 22, 35, 25)
    cv.fill(mask & head, '#1e120c')
    for x in (25, 38):                                     # schlaue, goldene Tanuki-Augen mit Glanz
        cv.fill(cv.E(x, 23.5, 1.6, 1.4), '#d8a030')
        cv.fill(cv.E(x + .4, 23.8, .9, 1.0), '#100808')
        cv.px(x - 1, 23, '#fff0c0')
    mz = cv.E(31.5, 30, 6.5, 4.5)
    cv.form(mz, (F[3], F[4], '#fff4dc'), 1, 1)
    cv.fill(cv.E(31.5, 27.5, 2, 1.3), '#1a0e0a')          # Nase
    cv.px(31, 27, '#6a5a50')
    cv.line([(29, 32), (31, 33), (34, 32)], F[1])
    # Strohhut (kasa), schräg aufgesetzt
    hat = cv.PG([(14, 15), (31.5, 3), (50, 13), (48, 15), (31.5, 9), (16, 17)])
    cv.form(hat | cv.PG([(18, 14), (31.5, 5), (46, 13)]), ('#5a4428', '#94804e', '#c8b070'), 2, 1)
    for x in range(20, 46, 4):
        cv.line([(31.5, 5), (x, 14 - abs(x - 31.5) * .1)], '#6a583e')
    # Bauch-Sakeflasche (tokkuri) seitlich links
    tk = cv.E(6, 66, 4.5, 6) | cv.R(4, 57, 7, 61)
    cv.form(tk, ('#4a3a2a', '#a08a60', '#d8c49a'), 1, 1)
    cv.fill(cv.R(3, 63, 9, 66), '#2a1a12')
    cv.px(5, 64, '#d8c49a')
    finish(cv, 32, 85, 26)
    cv.a[47:60, 14:50] = 0                                  # Fenster ausstanzen: Walzen liegen darunter
    return cv


def counter():
    """Ladentheke des Tanuki-Händlers: Holzplatte mit Maserung, Lattenfront, indigofarbene Noren mit Mon,
    Soroban und Münzstapel."""
    cv = Cv(96, 36, ss=1)
    W_ = ('#2a1810', '#5a3820', '#8a5a34', '#b88a50')
    cv.form(cv.R(3, 10, 92, 32), (W_[0], W_[1], W_[2]), 3, 1)
    for x in range(10, 90, 10):
        cv.vl(x, 13, 31, W_[0]); cv.vl(x + 1, 13, 31, W_[2])
    cv.form(cv.R(0, 5, 95, 10), (W_[1], W_[2], W_[3]), 1, 1)
    for x0, x1 in ((6, 30), (44, 70), (78, 90)):           # Maserung
        cv.hl(x0, x1, 7, W_[2])
    cv.hl(0, 95, 5, '#d8b070')
    ind = ('#101838', '#1e2c5a', '#34488a', '#5a72b0')
    for i in range(4):                                      # vier Noren-Bahnen mit Schlitzen
        x0 = 5 + i * 22
        nm = cv.R(x0, 11, x0 + 20, 26)
        cv.form(nm, (ind[0], ind[1], ind[2]), 2, 1)
        cv.hl(x0, x0 + 20, 11, ind[3])
        cx = x0 + 10
        ring = cv.E(cx, 19, 5, 5) & ~cv.E(cx, 19, 3.6, 3.6)
        cv.fill(ring, '#e8e0cc')
        cv.fill(cv.E(cx, 19, 1.5, 1.5), '#e8e0cc')          # Mon: Ring mit Punkt (Tanuki-Bauch)
    cv.form(cv.R(8, 0, 30, 4), ('#1a1010', '#3a2418', '#5a3a22'), 1, 1)   # Soroban
    for x in range(10, 29, 3):
        cv.px(x, 1, '#c8b890'); cv.px(x, 3, '#c8b890')
    cv.hl(8, 30, 2, '#1a1010')
    for i, x in enumerate((72, 76, 80, 74, 78)):            # Münzen
        y = 3 - (1 if i > 2 else 0) * 2
        cv.fill(cv.E(x, y + 1, 2.4, 1.2), '#96661c'); cv.fill(cv.E(x, y + .5, 2, .8), '#e0b040')
    return finish(cv, 48, 33, 46)


def saisen():
    """Saisen-bako mit Lattendeckel, Messingbeschlägen, Plakette und rot-weißem Glockenseil."""
    cv = Cv(56, 40, ss=1)
    W_ = ('#1e1216', '#3e2620', '#62402c', '#8a6040')
    cv.form(cv.R(4, 18, 51, 36), (W_[0], W_[1], W_[2]), 3, 1)
    cv.form(cv.PG([(2, 18), (6, 12), (49, 12), (53, 18)]), (W_[1], W_[2], W_[3]), 1, 1)
    for x in range(9, 48, 5):                               # schräge Latten, darunter Dunkel
        cv.line([(x, 13), (x - 2, 17)], W_[0])
        cv.line([(x + 1, 13), (x - 1, 17)], W_[3])
    cv.hl(2, 53, 18, '#c89a30')
    for (x, y) in ((4, 19), (47, 19), (4, 32), (47, 32)):  # Eckbeschläge
        cv.form(cv.R(x, y, x + 4, y + 4), ('#5a3414', '#c89a30', '#f0d070'), 1, 1)
    pl = cv.R(20, 22, 35, 31)                               # Plakette 賽銭 angedeutet
    cv.form(pl, ('#5a3414', '#c89a30', '#f0d070'), 1, 1)
    for x in (24, 31):
        cv.vl(x, 24, 29, '#3a2010'); cv.hl(x - 1, x + 1, 25, '#3a2010'); cv.hl(x - 1, x + 1, 28, '#3a2010')
    for x in range(26, 30):                                 # Glockenseil (suzu no o), gedreht rot-weiß
        for y in range(0, 12):
            cv.px(x, y, '#e8e0d0' if (x + y) % 4 < 2 else '#b02028')
    cv.fill(cv.E(28, 11, 2.5, 1.5), '#b02028')
    return finish(cv, 28, 37, 25)


def omikuji():
    """Omikuji-Stand: rot lackiertes Kästchen mit Dach, Papierfeld 御神籤, Losbüchse oben."""
    cv = Cv(40, 56, ss=1)
    red = ('#3a0c14', '#8e1a1e', '#c8382a', '#ec7050')
    cv.form(cv.R(6, 14, 33, 44), red[:3], 3, 1)
    cv.form(cv.PG([(3, 15), (10, 9), (29, 9), (36, 15)]), BLACK[:3], 1, 1)
    cv.hl(3, 36, 15, BLACK[3])
    cv.form(cv.R(11, 18, 28, 39), ('#a8a090', '#e8e0cc', '#fff8e8'), 1, 1)
    for y in (21, 26, 31, 35):                              # Schrift 御神籤, senkrecht
        cv.hl(17, 22, y, '#2a1818'); cv.vl(19, y - 1, y + 2, '#2a1818')
    cv.fill(cv.R(12, 18, 13, 39), red[1])
    cv.form(cv.R(15, 2, 24, 9), ('#3a2418', '#7a5434', '#a8804c'), 1, 1)   # sechseckige Losbüchse
    cv.vl(19, 0, 2, '#d8c8a0'); cv.px(19, 0, '#b02028')
    cv.form(cv.R(9, 45, 30, 48), ('#2a1810', '#5a3820', '#8a5a34'), 1, 1)
    cv.form(cv.R(4, 49, 35, 53), ('#2a1810', '#5a3820', '#8a5a34'), 1, 1)
    for x in (2, 36):                                       # gebundene Zettel an den Seiten
        cv.form(cv.R(x, 26, x + 2, 33), ('#a8a090', '#e8e0cc', '#fff8e8'), 0, 1)
        cv.px(x + 1, 27, '#b02028')
    return finish(cv, 20, 54, 17)


MUSUBI_SPOTS = [(16, 22), (34, 24), (52, 24), (24, 40), (44, 40), (58, 38), (14, 52), (32, 54), (50, 54)]


def musubi(n):
    """Musubi-dokoro: Holzgestell mit drei Strohseilen, n Unglückslose verknotet."""
    cv = Cv(76, 64, ss=1)
    W_ = ('#1e1216', '#3e2620', '#62402c', '#8a6040')
    for x in (4, 66):
        cv.form(cv.R(x, 6, x + 5, 60), (W_[0], W_[1], W_[2]), 2, 1)
        cv.form(cv.R(x - 2, 2, x + 7, 6), BLACK[:3], 1, 1)
    cv.form(cv.R(2, 8, 73, 11), (W_[1], W_[2], W_[3]), 1, 1)
    for ry in (21, 37, 51):
        for x in range(10, 66):
            y = int(round(ry + 2.2 * np.sin(np.pi * (x - 10) / 56)))
            cv.px(x, y, ROPE[2] if x % 3 else ROPE[1]); cv.px(x, y + 1, ROPE[1] if x % 3 else ROPE[0])
    for i, (x, y) in enumerate(MUSUBI_SPOTS[:n]):
        p = ('#a8a090', '#e8e0cc', '#fff8e8')
        cv.form(cv.E(x, y, 2.6, 2), p, 0, 1)                # Knoten
        cv.form(cv.PG([(x - 2, y + 1), (x - 1, y + 1), (x - 3, y + 9), (x - 4, y + 9)]), p, 0, 1)
        cv.form(cv.PG([(x + 1, y + 1), (x + 2, y + 1), (x + 3, y + 7), (x + 2, y + 7)]), p, 0, 1)
        cv.px(x, y, '#b02028')
    for x in (3, 65):
        cv.form(cv.R(x, 60, x + 8, 62), (STONE[1], STONE[2], STONE[3]), 1, 1)
    return finish(cv, 38, 62, 34)


def ema(used):
    """Ema-Votivtafel (Fünfeck) an roter Kordel; das farbige Wunschzeichen malt das Spiel darauf."""
    cv = Cv(44, 52, ss=1)
    wd = ('#5a3a22', '#a07848', '#c8a070', '#e8c898') if not used else ('#3a2a20', '#6a5440', '#8a7058', '#9a8068')
    cv.form(cv.R(20, 0, 23, 9), ('#5a0c14', '#b02028', '#e04a3a'), 0, 1)
    pent = cv.PG([(2, 18), (21.5, 6), (41, 18), (41, 46), (2, 46)])
    cv.form(pent, (wd[0], wd[1], wd[2]), 3, 1)
    cv.line([(3, 18), (21, 7), (40, 18)], wd[3])
    cv.fill(cv.R(4, 19, 39, 20), wd[0])                     # Dachkante
    for y, (x0, x1) in ((26, (6, 16)), (34, (26, 37)), (40, (7, 20))):
        cv.hl(x0, x1, y, wd[0])
    if used:                                                # beschrieben: Tuschezeilen
        for x in (14, 21, 28):
            cv.vl(x, 24, 40, '#2a1a14')
    return finish(cv, 22, 47, 20)


def onsen(used):
    """Felsen-Onsen: Randsteine, dampfendes Wasser mit Lichtringen, Bambusrinne (kakehi)."""
    cv = Cv(116, 64, ss=1)
    S = STONE
    import random as _r
    rng = _r.Random(7)
    pool = cv.E(58, 34, 50, 22)
    water = ('#14304a', '#2a6a8a', '#4aa0b8', '#a8e0e8') if not used else ('#18242c', '#2a4048', '#3e5a62', '#6a8088')
    cv.fill(pool, water[1])
    cv.fill(pool & ~sh(pool, 0, 4), water[0])
    for (rx, ry) in ((30, 10), (18, 6)):
        ring = cv.E(54, 36, rx, ry) & ~cv.E(54, 36, rx - 1.5, ry - 1)
        cv.fill(ring & pool, water[2])
    cv.fill(cv.E(40, 30, 6, 1.5) & pool, water[3])
    for i in range(22):                                     # Randsteine
        a = i / 22 * 2 * np.pi
        x, y = 58 + np.cos(a) * 52, 34 + np.sin(a) * 25
        rx, ry = rng.uniform(6, 9), rng.uniform(4, 6)
        m = cv.E(x, y, rx, ry)
        cv.fill(dil(m), K)
        cv.form(m, (S[1], S[2], S[3]) if np.sin(a) > -.2 else (S[0], S[1], S[2]), 2, 1)
        cv.px(int(x - rx * .4), int(y - ry * .5), S[4])
    for (x, y) in ((10, 24), (100, 46), (30, 56)):
        m = cv.E(x, y, 4, 2) & cv.m
        cv.fill(m, MOSS[1]); cv.fill(m & ~sh(m, 1, 1), MOSS[2])
    bam = ('#2a4a1c', '#4a7a2c', '#8ab84a')                 # Kakehi: Bambusrinne mit Wasserstrahl
    cv.form(cv.R(84, 4, 87, 14), bam, 1, 1)
    cv.form(cv.PG([(70, 7), (88, 4), (88, 7), (70, 10)]), bam, 1, 1)
    if not used:
        cv.vl(70, 10, 22, '#a8e0e8'); cv.vl(71, 11, 22, '#4aa0b8')
    cv.outline(K)
    return cv


def tea_bench():
    """Teehaus-Bank mit rotem Mōsen-Tuch, Holzbeinen und Lacktablett."""
    cv = Cv(56, 28, ss=1)
    red = ('#4a0c14', '#a01c22', '#d03a30', '#f07050')
    for x in (5, 46):
        cv.form(cv.R(x, 12, x + 4, 26), ('#1e1216', '#3e2620', '#62402c'), 1, 1)
    cv.form(cv.R(0, 6, 55, 12), red[:3], 2, 1)
    cv.hl(0, 55, 6, red[3])
    cv.fill(cv.R(0, 12, 55, 14), red[0])                    # überhängendes Tuch
    cv.form(cv.R(18, 2, 37, 5), BLACK[:3], 1, 1)
    cv.hl(18, 37, 2, '#7a3a2a')
    return finish(cv, 28, 26, 26)


def tea_cup():
    """Chawan in dunkler Raku-Glasur; die Teefarbe setzt das Spiel ein (Fläche oben)."""
    cv = Cv(20, 16, ss=1)
    body = cv.E(10, 8, 8, 6) & (cv.Y >= 5)
    cv.form(body, ('#1a1418', '#3a2e30', '#6a5a50'), 2, 1)
    cv.form(cv.R(7, 13, 12, 14), ('#1a1418', '#3a2e30', '#6a5a50'), 0, 1)
    cv.fill(cv.E(10, 5, 8, 2), '#c0b090')
    cv.fill(cv.E(10, 5, 6.5, 1.3), '#ff00ff')                # Platzhalter für den Tee
    cv.outline(K)
    return cv


def stairs_up():
    """Steintreppe zurück nach oben, mit Moos und Licht von oben."""
    cv = Cv(48, 44, ss=1)
    S = STONE
    for i in range(5):
        x0, x1, y0 = 4 + i * 4, 43 - i * 4, 34 - i * 8
        cv.form(cv.R(x0, y0, x1, y0 + 8), (S[0], S[1], S[2]) if i < 3 else (S[1], S[2], S[3]), 2, 1)
        cv.hl(x0, x1, y0, S[4] if i > 2 else S[3])
    cv.fill(cv.R(20, 0, 27, 2), '#d8d0b0')                  # Lichtschein oben
    m = cv.E(8, 40, 3, 1.5) & cv.m
    cv.fill(m, MOSS[1])
    return finish(cv, 24, 42, 22)


def _cap(cv, x0, y0, r0, x1, y1, r1):
    dx, dy = x1 - x0, y1 - y0
    t = np.clip(((cv.X - x0) * dx + (cv.Y - y0) * dy) / (dx * dx + dy * dy or 1), 0, 1)
    r = r0 + (r1 - r0) * t
    return (cv.X - x0 - t * dx) ** 2 + (cv.Y - y0 - t * dy) ** 2 <= r * r


MOONFUR = ('#3a3a6c', '#7a80b4', '#c4c8e6', '#f4f4ff')
USU = ('#1e1216', '#3e2620', '#62402c', '#8a6040')


def usagi(f):
    """Tsuki no Usagi stampft Mochi: f=0 Kine oben, 1 im Schwung, 2 Schlag ins Usu (Hase rechts, Mörser links)."""
    cv = Cv(64, 60, ss=1)
    # Usu: ausgehöhlter Baumstamm mit Eisenband, Mochi oben
    side = cv.R(7, 42, 31, 56) | cv.E(19, 56, 12, 2.5)
    cv.form(side, USU[:3], 3, 1)
    for x in (11, 16, 22, 27):
        cv.vl(x, 45, 55, USU[0])
    cv.form(cv.R(7, 49, 31, 50), ('#16162e', '#2f3358', '#5a6490'), 0, 1)
    cv.fill(cv.E(19, 42, 12, 3.5), USU[3])
    cv.fill(cv.E(19, 42, 10, 2.6), USU[0])
    mochi = cv.E(19, 41 if f < 2 else 42, 8, 2.6 if f < 2 else 2)
    cv.form(mochi, ('#a8acc8', '#e4e6f0', '#ffffff'), 1, 1)
    # Kine: Griff zu den Pfoten, Kopf quer zum Griff
    paw, head = ((51, 21), (37, 7)) if f == 0 else ((42, 23), (24, 15)) if f == 1 else ((35, 27), (20, 38))
    hx_, hy_ = head
    dx, dy = paw[0] - hx_, paw[1] - hy_
    n = (dx * dx + dy * dy) ** .5
    px_, py_ = -dy / n * 6, dx / n * 6
    kine_h = _cap(cv, hx_, hy_, 1.4, paw[0] + dx / n * 3, paw[1] + dy / n * 3, 1.4)
    kine_k = _cap(cv, hx_ - px_, hy_ - py_, 3.4, hx_ + px_, hy_ + py_, 3.4)
    # Hase: Hinterkeule, Leib, Kopf, Ohren (Licht oben links, kalter Schatten unten rechts)
    far_ear = cv.PG([(46, 21), (50, 3), (53, 4), (50, 22)])
    cv.form(far_ear, MOONFUR[:3], 1, 1)
    body = cv.E(47, 43, 9, 11)
    leg = cv.E(50, 49, 7, 6)
    foot = cv.E(47, 56, 9, 2.5)
    cv.fill(dil(body | leg | foot), K)
    cv.form(body | leg, MOONFUR[:3], 3, 1)
    cv.fill(leg & ~sh(leg, 0, 2) & body, MOONFUR[0])
    cv.form(foot, MOONFUR[:3], 1, 1)
    cv.fill(cv.E(44, 45, 4, 6) & body, MOONFUR[2])              # helle Brust
    cv.fill(dil(kine_h | kine_k), K)
    cv.form(kine_h, ('#33202a', '#653c2a', '#96663a'), 1, 1)
    cv.form(kine_k, ('#3a2a20', '#7a5a38', '#a8844c'), 2, 1)
    cv.fill(cv.E(hx_ - px_, hy_ - py_, 2, 2) & kine_k, '#c8a870')   # Hirnholz
    # Arm vom Schulterbogen zu den Pfoten, vor dem Griff
    arm = _cap(cv, 49, 36, 2.6, paw[0], paw[1], 2.4)
    cv.fill(dil(arm), K)
    cv.form(arm, MOONFUR[:3], 1, 1)
    cv.fill(cv.E(paw[0], paw[1], 2.2, 2.2), MOONFUR[2])
    hd = cv.E(43, 27, 7, 6) | cv.E(38, 29, 3.5, 3)
    ear = cv.PG([(42, 23), (41, 2), (45, 1), (46, 23)])
    cv.fill(dil(hd | ear), K)
    cv.form(hd, MOONFUR[:3], 2, 1)
    cv.form(ear, MOONFUR[:3], 1, 1)
    cv.fill(cv.PG([(43, 19), (42.5, 5), (44, 5), (44.5, 19)]), '#b86a84')   # rosiges Ohrinneres
    cv.px(41, 26, '#ff5a3c'); cv.px(40, 26, '#c81e2a'); cv.px(41, 25, '#fffbc0')
    cv.px(35, 29, '#8a4650'); cv.px(35, 30, '#8a4650')
    cv.hl(44, 46, 32, MOONFUR[0])                               # Kinnlinie
    if f == 2:                                                  # Mochi spritzt beim Schlag
        for (x, y) in ((8, 36), (6, 39), (30, 36), (32, 38), (12, 33)):
            cv.fill(cv.E(x, y, 1.2, 1.2), '#ffffff')
    return finish(cv, 32, 57, 26)


def build(dst=DST):
    strip([usagi(f) for f in range(3)], os.path.join(dst, 'usagi_hi.png'))
    strip([torii(k) for k in ORDER], os.path.join(dst, 'torii_hi.png'))
    strip([hokora(False), hokora(True)], os.path.join(dst, 'hokora_hi.png'))
    strip([slots()], os.path.join(dst, 'slots_hi.png'))
    strip([counter()], os.path.join(dst, 'counter_hi.png'))
    strip([saisen()], os.path.join(dst, 'saisen_hi.png'))
    strip([omikuji()], os.path.join(dst, 'omikuji_hi.png'))
    strip([musubi(n) for n in range(10)], os.path.join(dst, 'musubi_hi.png'))
    strip([ema(False), ema(True)], os.path.join(dst, 'ema_hi.png'))
    strip([onsen(False), onsen(True)], os.path.join(dst, 'onsen_hi.png'))
    strip([tea_bench()], os.path.join(dst, 'teabench_hi.png'))
    strip([tea_cup()], os.path.join(dst, 'teacup_hi.png'))
    strip([stairs_up()], os.path.join(dst, 'stairs_hi.png'))


if __name__ == '__main__':
    build()
    print('ok')
