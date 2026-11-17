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


NAMES = ['mondkine', 'shiomitsu_tama']


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
