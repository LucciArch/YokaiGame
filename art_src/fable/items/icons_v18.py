"""Item-Symbole v1.8: aktive Quest-Belohnungen (ACHIEVEMENTS 'q_*').
Aufruf: cd art_src/fable/items && PYTHONPATH=.. python3 icons_v18.py [vorschau.png]"""
from ihelp import *


def mondkine():
    """Kine des Mondhasen: schräger Holzstampfer vor dem Vollmond, am Kopf klebt Mochi-Teig, Staubwolke beim Aufschlag."""
    c = Cv()
    c.form(E(12, 11, 9, 9), 'ogY', 1, 1, ring='K')                     # Vollmond
    for x, y, r in ((9, 9, 1.6), (14, 14, 1.2), (8, 14, 0.9)):         # Mondflecken
        c.fill(E(x, y, r, r), 'g')
    c.form(L(26, 3, 1.6, 15, 18, 1.6), 'jdD', 1, 1, ring='K')          # Stiel
    head = REL(12, 21, 9, 5, 36)                                  # Stampferkopf quer zum Stiel
    c.form(head, 'jdD', 2, 1, ring='K')
    c.line([(5, 18), (18, 27)], 'j', 1, only=head)                      # Holzmaserung
    c.line([(8, 15), (19, 23)], 't', 1, only=head)
    c.form(E(6, 26, 3.4, 2.4), 'nvW', 1, 1, ring='K')                  # klebender Mochi
    c.a[26, 5] = 'W'
    for x, y in ((3, 29), (11, 29), (15, 28)):                          # Staub
        c.fill(E(x, y, 1.4, 1.0), 'C')
    sparkle(c, 27, 13, 'W', 'A')
    return c


def shiomitsu_tama():
    """Shiomitsu-Tama: Ryūjins Flutjuwel – leuchtende blaue Perle mit Wellenkamm im Inneren, umspült von einer Woge."""
    c = Cv()
    wave = (E(16, 24, 14, 5.5) & R(0, 22, 31, 30)) | E(6, 21, 4, 3.4)   # Woge unter der Perle
    c.form(wave, 'IJO', 1, 1, ring='K')
    c.form(E(16, 14, 9.5, 9.5), 'zaA', 2, 1, ring='K')                 # Juwel
    c.line([(9, 17), (12, 14), (15, 16), (18, 12), (21, 15), (23, 13)], 'W', 1, only=E(16, 14, 8.4, 8.4))
    c.fill(E(16, 19, 6, 2.6) & E(16, 14, 8.4, 8.4), 'J')               # Wasser im Juwel
    c.fill(E(12, 9, 2.4, 1.6), 'W')                                    # Glanz
    c.a[11, 15] = 'W'
    for x in (3, 9, 22, 28):                                            # Gischtkämme
        c.line([(x, 25), (x + 2, 23), (x + 3, 25)], 'W', 1)
    for x, y in ((4, 6), (27, 5), (28, 18)):
        c.fill(E(x, y, 1.0, 1.0), 'A')
    return c


def matsuri_uchiwa():
    """Matsuri-Uchiwa: runder Festfächer aus Papier mit rotem Mitsudomoe, Bambusgriff, dahinter zerplatzt ein Hanabi."""
    c = Cv()
    for k in range(12):                                                # Feuerwerk hinter dem Fächer
        a = k / 12 * math.tau
        x, y = 22 + math.cos(a) * 8, 9 + math.sin(a) * 7
        c.line([(22 + math.cos(a) * 4, 9 + math.sin(a) * 3.5), (x, y)], 'y' if k % 2 else '9', 1)
        c.a[int(round(y)), int(round(x))] = 'Y' if k % 2 else 'W'
    c.form(L(10, 29, 1.4, 14, 19, 1.4), 'cCs', 0, 1, ring='K')         # Bambusgriff
    c.a[25, 11] = 'C'
    fan = E(14, 13, 9.5, 9)
    c.form(fan, 'nvW', 1, 1, ring='K')
    for k in range(-3, 4):                                             # Rippen
        c.line([(14, 21), (14 + k * 3, 6)], 'v', 1, only=fan & ~E(14, 13, 5, 5))
    for k in range(3):                                                 # Mitsudomoe
        a = k / 3 * math.tau - 0.5
        x, y = 14 + math.cos(a) * 2.2, 13 + math.sin(a) * 2.2
        c.fill(E(x, y, 1.9, 1.9), 'R')
        c.fill(E(14 + math.cos(a + 0.9) * 3.6, 13 + math.sin(a + 0.9) * 3.6, 1.1, 1.1), 'R')
    c.fill(E(14, 13, 0.7, 0.7), 'q')
    c.line([(6, 9), (9, 5)], 'W', 1, only=fan)                          # Glanz
    return c


def totsuka():
    """Totsuka no Tsurugi: gerades Ken mit Doppelschneide aufrecht, am Klingenansatz eine Kerbe (Kusanagi steckte in Orochis Schwanz), Schuppen-Splitter."""
    c = Cv()
    bl = PG([(16, 1), (19, 5), (19, 20), (13, 20), (13, 5)])           # Klinge
    c.form(bl, '123', 0, 1, ring='K')
    c.line([(16, 3), (16, 19)], 'W', 1)                                 # Grat
    c.fill(R(14, 6, 15, 19) & bl, '3')
    c.a[12, 18] = 'K'; c.a[13, 18] = 'K'                                # Scharte
    c.form(R(9, 20, 23, 22), 'ogy', 0, 1, ring='K')                     # Stichblatt
    c.form(R(14, 23, 18, 28), 'khH', 0, 1, ring='K')                    # Griff
    for y in (24, 26):
        c.line([(15, y), (17, y)], 'o', 1)
    c.form(E(16, 29.5, 2.4, 1.4), 'ogy', 0, 1, ring='K')                # Knauf
    for x, y in ((5, 8), (26, 11), (7, 16), (25, 4)):                  # Orochi-Schuppen
        c.form(PG([(x, y), (x + 2, y - 2), (x + 4, y), (x + 2, y + 2)]), 'FfG', 0, 1, ring='K')
    sparkle(c, 21, 3, 'W', 'A')
    return c


NAMES = ['mondkine', 'shiomitsu_tama', 'matsuri_uchiwa', 'totsuka']


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
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v18.png')
    print(WARN)
