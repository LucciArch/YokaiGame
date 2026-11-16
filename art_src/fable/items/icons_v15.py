"""Item-Symbole v1.5: Belohnungen aus Yomi no Kuni und Ama-no-Iwato."""
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


def uzume_suzu():
    """Kagura-Suzu der Ame-no-Uzume: Glöckchen in drei Rängen (1-3-5) am Stiel, fünffarbige Bänder."""
    c = Cv()
    for i, (ch, x0, x1) in enumerate((('r', 17, 27), ('w', 17, 25), ('G', 17, 23), ('y', 17, 21), ('a', 17, 19))):
        c.line([(x0, 21), (x0 + (x1 - x0) * .6, 25), (x1, 29 - i // 2)], ch, 1)      # Goshiki-Bänder wehen nach rechts
    c.form(R(14, 18, 17, 29), 'jdD', 1, 1, ring='K')                     # Stiel, rot umwickelt
    for y in (21, 24, 27):
        c.line([(14, y), (17, y)], 'R', 1)
    tiers = ((5, (15.5,)), (10, (11.5, 15.5, 19.5)), (15, (7.5, 11.5, 15.5, 19.5, 23.5)))
    for y, xs in tiers:
        c.line([(15.5, 17), (xs[0], y)], '2', 1)
        c.line([(15.5, 17), (xs[-1], y)], '2', 1)
    for y, xs in tiers:
        for x in xs:
            b = E(x, y, 2.3, 2.3)
            c.form(b, 'ogy', 1, 1, ring='K')
            c.fill(E(x, y + 1.2, 1.2, 0.6), 'o')
            c.a[int(y - 1), int(x - 1)] = 'Y'
    sparkle(c, 25, 6, 'W', 'Y')
    sparkle(c, 5, 8, 'W', 'Y')
    return c


def kaze_bukuro():
    """Fūjins Windsack: prall gefüllter Stoffsack über der Schulter getragen, am Hals verschnürt,
    aus der Öffnung fährt ein Wirbel – Sturmbögen und ein Ahornblatt."""
    c = Cv()
    sack = E(14, 19, 10, 8.5) | E(9, 13, 5, 5) | E(21, 14, 4.5, 4)
    c.form(sack, '456', 3, 1, ring='K')                                   # jadegrünes Tuch
    c.fill(sack & ~E(12, 17, 8.5, 7) & (px.Y > 21), '4')
    for pts in ([(7, 18), (12, 22), (19, 22)], [(10, 25), (16, 26)]):       # Falten
        c.line(pts, '4', 1)
    c.form(E(24, 11, 2.6, 3.4), 'qrR', 1, 1, ring='K')                    # rote Schnur am Hals
    c.line([(22, 13), (26, 9)], 'f', 1)
    c.form(E(27, 7, 2.4, 1.8), '456', 1, 1, ring='K')                     # offene Öffnung
    for i, pts in enumerate(([(27, 5), (25, 2), (20, 2), (17, 5)], [(29, 8), (30, 4), (28, 1)],
                             [(26, 6), (22, 4), (19, 7), (21, 9)])):        # Sturmbögen
        c.line(pts, 'a' if i != 1 else 'W', 1)
    c.g(4, 4, ".7.\n797\n.9.", {})                                       # Ahornblatt im Wind
    sparkle(c, 5, 27, 'W', 'a')
    return c


NAMES = ['yomi_momo', 'uzume_suzu', 'kaze_bukuro']


def build():
    for nm in NAMES:
        save('icons', nm, globals()[nm]())


if __name__ == '__main__':
    build()
    from PIL import Image
    im = Image.open(os.path.join(HERE, 'icons', 'uzume_suzu.png')).convert('RGBA')
    out = Image.new('RGBA', (im.width * 8 + 32, im.height * 8 + 32), (30, 24, 40, 255))
    out.alpha_composite(im.resize((im.width * 8, im.height * 8), Image.NEAREST), (16, 16))
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/momo.png')
    print(WARN)
