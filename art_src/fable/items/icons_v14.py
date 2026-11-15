"""Item-Symbole v1.4: Geschenke aus den Ereignisräumen."""
from ihelp import *


def brautschleier():
    c = Cv()
    hood = E(16, 15, 11, 11) | PG([(6, 16), (4, 29), (16, 25), (28, 29), (26, 16)])
    hood = hood & ~E(16, 19, 6.4, 6.6)
    c.form(hood, 'nvwW', 3, 1, ring='K')                              # weißer Wataboshi
    c.form(E(16, 20, 5.6, 5.8), 'khH', 1, 0)                           # dunkle Öffnung
    c.form(PG([(12, 21), (16, 27), (20, 21), (16, 23)]), '789', 1, 1, ring='K')   # Fuchsschnauze
    c.a[22, 14] = 'K'; c.a[22, 18] = 'K'                               # Augen
    c.a[27, 16] = 'K'
    c.line([(7, 9), (11, 5)], 'R', 1); c.line([(25, 9), (21, 5)], 'R', 1)  # rote Kordel
    sparkle(c, 25, 4, 'W', 'Y')
    return c


def zashiki_temari():
    c = Cv()
    c.form(E(16, 17, 11, 11), 'qrRe', 3, 1, ring='K')                  # roter Ball
    for k in range(4):                                                 # gestickte Fäden
        a = k * math.pi / 4
        c.line([(16 + math.cos(a) * 10, 17 + math.sin(a) * 10), (16 - math.cos(a) * 10, 17 - math.sin(a) * 10)],
               'Y' if k % 2 else 'W', 1)
    c.form(E(16, 17, 3.2, 3.2), 'ogy', 1, 1)
    c.fill(E(12, 12, 2.4, 2.0), 'e')                                   # Glanz
    c.line([(16, 6), (16, 2)], 'w', 1)                                 # Aufhängeband
    sparkle(c, 27, 6, 'W', 'Y')
    return c


NAMES = ['brautschleier', 'zashiki_temari']


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
    out.save('/tmp/prev/icons_v14.png')
    print(WARN)
