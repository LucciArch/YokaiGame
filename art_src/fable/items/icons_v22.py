"""Item-Symbole v2.2: Belohnung für den geheimen Boss Sugawara no Michizane.
Aufruf: cd art_src/fable/items && PYTHONPATH=.. python3 icons_v22.py [vorschau.png]"""
from ihelp import *


def _ume(c, cx, cy, r=3.2, ramp='mST'):
    """Fünfblättrige Pflaumenblüte mit roter Mitte."""
    m = E(cx, cy, r * 0.7, r * 0.7)
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        m = m | E(cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a), r * 0.55, r * 0.55)
    c.form(m, ramp, 1, 1, ring='U')
    x, y = int(round(cx)), int(round(cy))
    c.a[y, x] = 'y'
    for dx, dy in ((-1, 0), (1, 0), (0, -1)):        # rote Staubblätter
        c.a[y + dy, x + dx] = 'R'


def tenjin_ume():
    """Tobiume-Zweig: knorriger schwarzer Pflaumenast, drei Blüten (eine weiße), dahinter ein goldener Blitz."""
    c = Cv()
    bolt = [(28, 1), (21, 10), (25, 12), (18, 20), (22, 21), (15, 30)]
    c.line(bolt, 'K', 4)                             # Seiryōden-Blitz mit dickem Umriss
    c.line(bolt, 'y', 2)
    c.line(bolt[:2], 'Y', 1)
    tube([(3, 29, 1.8), (9, 22, 1.5), (14, 17, 1.2), (21, 12, 0.9), (27, 9, 0.6)], 'wood', c)   # Hauptast
    tube([(9, 22, 1.0), (7, 15, 0.8), (8, 10, 0.5)], 'wood', c)                                  # Nebenast
    _ume(c, 8, 9, 3.0, 'vwW')                         # die weiße Blüte von Kitano
    _ume(c, 15, 15, 3.6)
    _ume(c, 25, 9, 3.0)
    _ume(c, 5, 20, 2.4)
    for x, y in ((21, 17), (27, 15)):                 # fallende Blütenblätter
        c.a[y, x] = 'S'
    c.a[19, 21] = 'm'
    return c


NAMES = ['tenjin_ume']


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
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v22.png')
    print(WARN)
