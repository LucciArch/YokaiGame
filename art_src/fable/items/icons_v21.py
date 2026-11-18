"""Item-Symbole v2.1: Belohnung für den geheimen Boss Taira no Masakado.
Aufruf: cd art_src/fable/items && PYTHONPATH=.. python3 icons_v21.py [vorschau.png]"""
from ihelp import *


def _kabuto(c, cx, cy, bowl, mask, horns=None, eyes=None):
    """Helm mit Shikoro-Nackenschutz und Menpō; nur die Umrisse eines Kriegers ohne Gesicht."""
    c.form(PG([(cx - 7, cy + 1), (cx + 7, cy + 1), (cx + 9, cy + 7), (cx - 9, cy + 7)]), bowl, 1, 1, ring='K')   # Shikoro
    for y in (cy + 3, cy + 5):
        c.line([(cx - 8, y), (cx + 8, y)], bowl[0], 1)                 # Lamellenreihen
    c.form(E(cx, cy - 1, 6, 5) & (px.Y <= cy + 1), bowl, 1, 1, ring='K')   # Helmglocke
    c.form(R(cx - 4, cy + 1, cx + 4, cy + 6), mask, 1, 0, ring='K')    # Menpō, darunter nur Schatten
    if horns:
        for d in (-1, 1):                                              # Kuwagata, nach außen geschwungen
            c.form(L(cx + 2 * d, cy - 5, 1.0, cx + 6 * d, cy - 7, 1.1) | L(cx + 6 * d, cy - 7, 1.1, cx + 7 * d, cy - 10, 0.9), horns, 0, 1, ring='K')
        c.form(E(cx, cy - 4, 1.4, 1.2), horns, 0, 1, ring='K')
    if eyes:
        c.a[cy + 2, cx - 2] = eyes
        c.a[cy + 2, cx + 2] = eyes


def masakado_kage():
    """Kagemusha: sieben Schattenkrieger – vorne der echte Helm mit goldenen Kuwagata und Onibi-Augen,
    dahinter zwei Doppelgänger ohne Schatten in Indigo, über allem ein Onibi-Funke."""
    c = Cv()
    _kabuto(c, 22, 9, 'III', 'kI', eyes='5')                         # Doppelgänger, schräg dahinter gestaffelt
    _kabuto(c, 18, 15, 'IJJ', 'kI', eyes='6')
    _kabuto(c, 12, 21, 'khH', 'kh', horns='ogY', eyes='W')           # der echte Masakado vorne
    c.line([(3, 29), (21, 29)], 'k', 1)                               # nur er wirft einen Schatten
    c.line([(6, 30), (18, 30)], 'k', 1)
    c.form(E(5, 6, 2.0, 2.4), '456', 0, 1, ring='K')                  # bleiches Onibi
    c.a[3, 5] = '5'
    sparkle(c, 28, 24, 'W', '6')
    return c


NAMES = ['masakado_kage']


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
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v21.png')
    print(WARN)
