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


def build(dst=DST):
    strip([torii(k) for k in ORDER], os.path.join(dst, 'torii_hi.png'))
    strip([hokora(False), hokora(True)], os.path.join(dst, 'hokora_hi.png'))
    strip([slots()], os.path.join(dst, 'slots_hi.png'))


if __name__ == '__main__':
    build()
    print('ok')
