"""Item-Symbole v1.3: Fundstücke aus den Himmelsgefilden und aus Yomi."""
from ihelp import *


def komainu_glocke():
    c = Cv()
    c.line([(8, 6), (16, 9), (24, 6)], 'R', 2)                          # rote Kordel
    c.line([(8, 5), (16, 8), (24, 5)], 'e', 1)
    c.form(E(16, 19, 10, 9.4) | R(9, 19, 23, 25), 'ogy', 3, 1, ring='K')  # Glocke
    c.form(E(16, 26, 11, 2.4), 'ogy', 1, 1, ring='K')                    # Rand
    c.fill(R(10, 21, 22, 22), 'o')                                       # Zierband
    c.line([(16, 26), (16, 29)], 'k', 2)                                 # Schlitz
    c.fill(E(16, 29, 2.4, 1.6), 'k')
    c.fill(E(12, 15, 2.4, 3.4), 'Y')                                     # Glanz
    c.a[13, 11] = 'W'
    for x in (13, 16, 19):                                               # kleine Löwenlocken eingraviert
        c.a[18, x] = 'o'; c.a[17, x + 1] = 'o'
    return c


def tennin_feder():
    c = Cv()
    vane = PG([(5, 28), (9, 19), (15, 11), (22, 5), (27, 3), (26, 9), (21, 16), (14, 23), (8, 27)])
    c.form(vane, 'vwW', 2, 1, ring='K')
    for k in range(6):                                                   # Fahnenäste
        x, y = 9 + k * 3, 24 - k * 3.4
        c.line([(x, y), (x + 3, y + 3)], 'v', 1)
    c.line([(5, 28), (11, 21), (18, 13), (26, 4)], 'g', 1)               # goldener Kiel
    c.line([(4, 28), (6, 26)], 'o', 2)
    for (x, y) in ((24, 12), (13, 8)):
        sparkle(c, x, y, 'W', 'Y')
    return c


def yomi_stein():
    c = Cv()
    c.form(PG([(4, 26), (6, 12), (12, 5), (22, 4), (28, 12), (28, 25), (18, 29)]), '012', 3, 1, ring='K')
    c.form(PG([(8, 11), (13, 6), (21, 6), (16, 12)]), '123', 1, 1)
    c.line([(16, 12), (14, 20), (17, 27)], '0', 1)                       # Riss
    c.line([(14, 20), (9, 22)], '0', 1)
    rope = [(4, 17), (10, 19), (16, 20), (22, 19), (28, 17)]             # Shimenawa
    c.line(rope, 's', 2)
    c.line([(x, y + 1) for x, y in rope], 'c', 1)
    for x in (10, 16, 22):
        c.g(x, 21, "WW\n.W\nWW\nWv")
    c.fill(E(24, 25, 2, 1.4), 'F')                                       # Moos
    return c


def mikaboshi_staub():
    c = Cv()
    c.form(E(16, 22, 9.4, 7.4), 'JOn', 2, 1, ring='K')                   # Beutel
    c.form(PG([(11, 17), (21, 17), (19, 12), (13, 12)]), 'JOn', 1, 1, ring='K')
    c.line([(11, 16), (21, 16)], 'y', 1)                                 # goldene Schnur
    c.line([(20, 16), (24, 19), (23, 22)], 'g', 1)
    c.form(E(16, 11, 4.4, 1.6), 'kkh', 0, 0)                             # Öffnung
    for (x, y) in ((16, 25), (12, 21), (20, 22)):                        # aufgestickte Sterne
        c.a[y, x] = 'Y'; c.a[y - 1, x] = 'y'; c.a[y + 1, x] = 'y'; c.a[y, x - 1] = 'y'; c.a[y, x + 1] = 'y'
    c.g(14, 2, "..Y..\n..y..\nYyWyY\n..y..\n..Y..")
    for (x, y) in ((9, 6), (24, 5), (21, 9)):
        sparkle(c, x, y, 'W', 'Y')
    return c


NAMES = ['komainu_glocke', 'tennin_feder', 'yomi_stein', 'mikaboshi_staub']


def build():
    for nm in NAMES:
        save('icons', nm, globals()[nm]())


if __name__ == '__main__':
    build()
    from PIL import Image
    out = Image.new('RGBA', (len(NAMES) * 40 * 4, 40 * 4), (30, 24, 40, 255))
    for i, nm in enumerate(NAMES):
        im = Image.open(os.path.join(HERE, 'icons', nm + '.png')).convert('RGBA')
        im = im.resize((im.width * 4, im.height * 4), Image.NEAREST)
        out.alpha_composite(im, (i * 160 + 16, 16))
    out.save('/tmp/prev/icons_v13.png')
    print(WARN)
