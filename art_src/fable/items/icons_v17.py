"""Item-Symbole v1.7: Belohnungen der Herausforderungen (je Prüfung ein Item).
Aufruf: cd art_src/fable/items && PYTHONPATH=.. python3 icons_v17.py [vorschau.png]"""
from ihelp import *


def fuurin():
    """Edo-Glaswindspiel: Glasglocke mit rotem Goldfisch-Muster, Klöppel, Tanzaku-Streifen; ein Sprung im Glas."""
    c = Cv()
    c.line([(16, 1), (16, 5)], '1', 1)                                 # Schnur
    bell = E(16, 13, 8, 8) & R(0, 5, 31, 17)
    c.form(bell, 'zaA', 2, 1, ring='K')
    c.fill(E(16, 13, 6.2, 6.2) & R(0, 7, 31, 17) & ~E(16, 13, 5.4, 5.4), 'A')
    c.fill(REL(12, 12, 2.6, 1.4, 20), 'r')                             # Goldfisch
    c.fill(PG([(14, 12), (16, 10), (16, 14)]), 'R')
    c.a[11, 11] = 'k'
    c.fill(R(10, 15, 22, 16), 'n')                                     # Glasrand
    c.fill(E(13, 9, 1.3, 2.0), 'W')                                    # Glanz
    c.line([(21, 8), (19, 11), (21, 13), (19, 16)], 'W', 1)            # Sprung
    c.line([(16, 15), (16, 21)], '1', 1)                               # Klöppel-Faden
    c.form(E(16, 18, 1.6, 1.4), 'ogy', 0, 1, ring='K')
    strip = PG([(13, 21), (19, 21), (20, 30), (14, 30)])               # Tanzaku, im Wind gedreht
    c.form(strip, 'nvW', 1, 1, ring='K')
    for y in (24, 26, 28):
        c.line([(15, y), (18, y)], 'h', 1)
    for x, y in ((26, 4), (28, 7), (6, 23), (25, 24)):                 # Splitter
        c.fill(PG([(x, y), (x + 2, y + 1), (x, y + 2)]), 'A')
    return c


def abura_age():
    """Abura-age: zwei goldbraune Tofutaschen auf roter Lackschale, dahinter ein Fuchsfeuer."""
    c = Cv()
    fl = E(24, 9, 3.6, 3.6) | PG([(21, 8), (24, 1), (27, 8)])          # Fuchsfeuer
    c.form(fl, 'zaA', 1, 1, ring='K')
    c.fill(E(24, 9.5, 1.6, 1.8), 'W')
    dish = E(16, 24, 13, 4.5)
    c.form(dish, 'qrR', 1, 1, ring='K')
    c.fill(E(16, 23, 10.5, 2.6), 'h')
    for cx, cy, deg in ((11, 18, -12), (20, 17, 10)):
        pouch = REL(cx, cy, 6.5, 4.6, deg)
        c.form(pouch, '78y', 2, 1, ring='K')
        for k in range(-3, 4, 2):                                      # Bratblasen
            c.a[int(cy + (k % 3) - 1), int(cx + k)] = '7'
        c.a[int(cy - 3), int(cx - 2)] = 'Y'
    c.line([(5, 27), (27, 27)], 'q', 1, only=dish)
    return c


def tsukikage():
    """Mondschatten-Klinge: bläulich-fahles Katana vor einer Mondsichel, Klinge halb im Schatten."""
    c = Cv()
    moon = E(19, 12, 10, 10) & ~E(23, 9, 8.5, 8.5)
    c.form(moon, 'ogY', 1, 1, ring='K')
    pts = [(5, 28), (11, 21), (17, 14), (23, 8), (27, 4)]
    bl = np.zeros((c.h, c.w), bool)
    for (x0, y0), (x1, y1) in zip(pts[1:], pts[2:]):
        bl |= L(x0, y0, 1.7, x1, y1, 1.1)
    c.form(bl, 'IJO', 0, 1, ring='K')
    c.line(pts[1:], 'A', 1, only=bl)                                   # Hamon im Mondlicht
    c.fill(bl & (px.X + px.Y < 30), 'J')                               # untere Hälfte im Schatten
    c.form(L(4, 29, 2.0, 9, 23, 2.0), 'khH', 0, 1, ring='K')          # Griff
    for x, y in ((4, 29), (6, 27), (8, 25)):
        c.a[y, x] = 'x'
    c.form(REL(10, 22, 3.4, 1.8, -42), '012', 1, 1, ring='K')         # Tsuba
    sparkle(c, 27, 12, 'W', 'A')
    return c


def hayate_waraji():
    """Waraji: geflochtene Strohsandale mit Riemen, hinter ihr Sturmlinien."""
    c = Cv()
    for y, x0, x1 in ((8, 2, 11), (14, 0, 8), (21, 2, 9)):            # Wind
        c.line([(x0, y), (x1, y)], 'A', 1)
        c.a[y - 1, x1 + 1] = 'A'
    sole = REL(19, 16, 12, 6, -55)
    c.form(sole, 'cCs', 2, 1, ring='K')
    for k in range(-5, 6, 2):                                          # Flechtreihen
        x, y = 19 + k * 0.57, 16 - k * 0.82
        c.line([(x - 4, y - 2.6), (x + 4, y + 2.6)], 'c', 1, only=sole)
    for a, b in (((13, 22), (19, 10)), ((25, 22), (19, 10))):          # Riemen
        c.line([a, b], 'q', 2)
    c.form(E(19, 10, 1.8, 1.8), 'qrR', 0, 1, ring='K')
    c.line([(14, 26), (24, 26)], 'r', 1)
    return c


def senryo_bako():
    """Senryō-bako: Holztruhe mit Eisenbeschlägen, offener Deckel, Koban quellen heraus."""
    c = Cv()
    lid = PG([(5, 7), (27, 7), (25, 13), (7, 13)])
    c.form(lid, 'jdD', 1, 1, ring='K')
    box = R(4, 15, 28, 28)
    for x, y in ((9, 13), (14, 11), (19, 12), (24, 13), (16, 14)):     # Koban
        c.form(E(x, y, 3.2, 2.2), 'ogY', 1, 1, ring='K')
        c.a[y, x] = 'o'
    c.form(box, 'jdD', 2, 1, ring='K')
    for y in (15, 21, 27):
        c.form(R(4, y, 28, y + 1), '012', 0, 1)
    for x in (4, 27):
        c.form(R(x, 15, x + 1, 28), '012', 0, 1)
    c.form(R(14, 18, 18, 23), '012', 1, 1, ring='K')                   # Schloss
    c.a[21, 16] = 'k'
    c.g(10, 24, 'oy\nyo')
    c.g(21, 24, 'yo\noy')
    c.line([(7, 9), (25, 9)], '1', 1, only=lid)
    sparkle(c, 28, 4, 'W', 'Y')
    return c


def keppan():
    """Keppan: Kishōmon-Schwurpapier, darauf ein blutroter Daumenabdruck und Oni-Schriftzeichen."""
    c = Cv()
    paper = PG([(6, 3), (25, 5), (26, 29), (5, 27)])
    c.form(paper, 'nvW', 2, 1, ring='K')
    for x0 in (9, 13):                                                 # Schriftzeilen
        for y in range(7, 17, 3):
            c.line([(x0, y), (x0 + 1, y + 1)], 'k', 1)
    c.form(R(19, 7, 22, 12), 'qrR', 0, 0)                              # Siegel
    c.a[9, 20] = 'W'
    thumb = REL(16, 22, 4.2, 5.4, 15)                                   # Blut-Daumenabdruck
    c.fill(thumb, 'q')
    for r in (3.0, 1.8):
        c.fill(REL(16, 22, r * 0.78, r, 15) & ~REL(16, 22, r * 0.78 - 0.6, r - 0.6, 15), 'r')
    for x, y in ((11, 26), (21, 27), (22, 18)):                         # Tropfen
        c.fill(E(x, y, 1.0, 1.4), 'q')
    c.a[20, 15] = 'R'
    return c


def miidera_kane():
    """Glocke von Mii-dera: grünspanige Bonshō mit Nippelreihen, Drachenöse, Stoßpunkt und Kratzspur."""
    c = Cv()
    c.form(L(13, 4, 1.8, 19, 4, 1.8) | E(16, 3, 4, 2.5), '456', 1, 1, ring='K')   # Ryūzu
    c.a[2, 13] = 'Y'
    bell = R(7, 6, 25, 27) & ~(E(7, 6, 2, 2) & ~R(9, 6, 25, 27)) & ~(E(25, 6, 2, 2) & ~R(7, 6, 23, 27))
    c.form(bell | E(16, 7, 9, 2.5), '456', 2, 1, ring='K')
    c.form(R(6, 26, 26, 28), '456', 1, 1, ring='K')                    # Mundring
    c.line([(7, 11), (25, 11)], '4', 1)
    c.line([(7, 19), (25, 19)], '4', 1)
    c.line([(16, 11), (16, 19)], '4', 1)
    for y in (13, 15, 17):                                             # Chi (Buckel)
        for x in (9, 11, 13, 19, 21, 23):
            c.a[y, x] = '6'
    c.form(E(12, 23, 2.4, 2.2), 'ogy', 1, 1, ring='K')                 # Tsukiza (Stoßpunkt)
    c.line([(18, 21), (22, 25), (21, 27)], '4', 1)                     # Schleifspur vom Berg Hiei
    c.line([(20, 21), (24, 25)], '4', 1)
    for x in (2, 29):
        c.line([(x, 14), (x, 20)], 'Y', 1)                             # Klang
    return c


def nademono():
    """Nademono: Hitogata-Papierpuppe mit Schlitzaugen, um sie dunkler Dunst, der in sie gezogen wird."""
    c = Cv()
    for cx, cy in ((6, 8), (26, 10), (5, 24), (27, 25)):              # Unheil-Dunst
        c.form(E(cx, cy, 2.4, 2.0), 'xpP', 1, 0)
    c.line([(7, 9), (11, 13)], 'p', 1)
    c.line([(25, 11), (21, 14)], 'p', 1)
    c.line([(7, 23), (11, 21)], 'p', 1)
    c.line([(26, 24), (21, 22)], 'p', 1)
    doll = (E(16, 7, 3.6, 3.6) | R(14, 10, 18, 12) | PG([(6, 13), (26, 13), (24, 16), (8, 16)])
            | PG([(11, 16), (21, 16), (20, 24), (12, 24)]) | R(12, 24, 15, 29) | R(17, 24, 20, 29))
    c.form(doll, 'nvW', 2, 1, ring='K')
    c.a[6, 15] = 'k'; c.a[6, 17] = 'k'                                 # Schlitzaugen
    c.line([(15, 9), (17, 9)], 'n', 1)
    c.line([(16, 16), (16, 23)], 'v', 1)                               # Faltlinie
    c.fill(R(12, 17, 20, 17), 'q')                                     # roter Faden
    c.fill(E(16, 20, 1.5, 1.5), 'p')                                   # aufgenommenes Unheil
    return c


def kongozue():
    """Kongō-zue: Pilgerstab mit Gorintō-Kerben, Brokathülle, kleinem Glöckchen."""
    c = Cv()
    st_ = L(20, 29, 1.7, 12, 5, 1.7)
    c.form(st_, 'jdD', 1, 1, ring='K')
    for k, y in enumerate((5, 8, 11, 14)):                              # Gorintō-Kerben
        x = 12 + (y - 4) * 8 / 26
        c.line([(x - 1.5, y), (x + 1.5, y)], 'j', 1)
    c.form(PG([(10, 2), (14, 2), (15, 7), (10, 6)]), 'jdD', 0, 1, ring='K')   # Kopf
    cover = L(17, 18, 2.6, 15, 12, 2.6)                                 # Brokathülle
    c.form(cover, 'xpP', 1, 1, ring='K')
    c.line([(14, 14), (18, 13)], 'g', 1, only=cover)
    c.line([(15, 17), (19, 16)], 'g', 1, only=cover)
    c.line([(18, 18), (22, 22)], 'q', 1)                               # Schnur
    c.form(E(22, 24, 2.4, 2.4), 'ogY', 1, 1, ring='K')                 # Suzu
    c.a[25, 22] = 'k'
    sparkle(c, 25, 7, 'W', 'Y')
    return c


NAMES = ['fuurin', 'abura_age', 'tsukikage', 'hayate_waraji', 'senryo_bako', 'keppan', 'miidera_kane', 'nademono',
         'kongozue']


def build():
    import shutil
    dst = os.path.join(HERE, '..', '..', '..', 'yokai', 'assets', 'items', 'icons')
    for nm in NAMES:
        save('icons', nm, globals()[nm]())
        shutil.copy(os.path.join(HERE, 'icons', nm + '.png'), os.path.join(dst, nm + '.png'))


if __name__ == '__main__':
    build()
    from PIL import Image
    out = Image.new('RGBA', (10 * 36 * 6, (len(NAMES) + 9) // 10 * 36 * 6), (30, 24, 40, 255))
    for i, nm in enumerate(NAMES):
        im = Image.open(os.path.join(HERE, 'icons', nm + '.png')).convert('RGBA')
        out.alpha_composite(im.resize((im.width * 6, im.height * 6), Image.NEAREST), (i % 10 * 216 + 12, i // 10 * 216 + 12))
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v17.png')
    print(WARN)
