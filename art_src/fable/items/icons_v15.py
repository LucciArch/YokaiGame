"""Item-Symbole v1.5: Belohnungen aus Yomi no Kuni."""
from ihelp import *


def yomi_momo():
    c = Cv()
    body = E(16, 19, 10.5, 10) | E(17, 12, 6, 5)                       # Pfirsich mit Spitze
    c.form(body, '789', 3, 1, ring='K')                                # orange Grundfarbe
    blush = E(20, 20, 6, 6.5) & body & ((px.X + px.Y) % 2 == 0)       # rosige Backe, gerastert
    c.fill(blush & E(20, 20, 4.5, 5), 'S')
    c.fill(blush & ~E(20, 20, 4.5, 5), 'm')
    c.line([(16, 10), (14, 17), (15, 27)], '7', 1)                     # Naht
    c.form(PG([(16, 9), (8, 4), (5, 9), (12, 11)]), 'FfG', 1, 1, ring='K')    # Blätter
    c.form(PG([(17, 9), (24, 3), (27, 7), (21, 11)]), 'FfG', 1, 1, ring='K')
    c.line([(16, 10), (16, 5)], 'j', 1)                                # Stiel
    c.fill(E(12, 15, 2.2, 1.6), 'T')                                   # Glanz
    for x, y in ((4, 24), (27, 27), (26, 15)):                         # Totenlichter aus Yomi
        c.a[y, x] = 'p'
    sparkle(c, 6, 17, 'X', 'P')
    return c


NAMES = ['yomi_momo']


def build():
    for nm in NAMES:
        save('icons', nm, globals()[nm]())


if __name__ == '__main__':
    build()
    from PIL import Image
    im = Image.open(os.path.join(HERE, 'icons', 'yomi_momo.png')).convert('RGBA')
    out = Image.new('RGBA', (im.width * 8 + 32, im.height * 8 + 32), (30, 24, 40, 255))
    out.alpha_composite(im.resize((im.width * 8, im.height * 8), Image.NEAREST), (16, 16))
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/momo.png')
    print(WARN)
