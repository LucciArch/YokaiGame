"""Item-Symbole v2.0: Belohnung für den geheimen Boss Sutoku-in.
Aufruf: cd art_src/fable/items && PYTHONPATH=.. python3 icons_v20.py [vorschau.png]"""
from ihelp import *


def sutoku_sutra():
    """Blut-Sutra: schräg entrollte Schriftrolle, die Zeichen mit Blut geschrieben; eine schwarze Tengu-Feder liegt quer darüber."""
    c = Cv()
    paper = PG([(4, 9), (24, 3), (28, 21), (8, 27)])
    c.form(paper, 'cCs', 1, 1, ring='K')                               # vergilbtes Washi
    for k in range(4):                                                 # Blutzeilen, quer zur Rolle
        x0, y0 = 8 + k * 4.4, 9 - k * 1.2
        c.line([(x0, y0), (x0 + 3.6, y0 + 14)], 'q', 1, only=paper)
        c.line([(x0 + 1, y0), (x0 + 4.6, y0 + 14)], 'R', 1, only=paper)
        for j in range(0, 13, 4):
            c.a[int(y0 + j + 1), int(x0 + j * 0.26) + 1] = 'q'         # verlaufende Tropfen in der Schrift
    c.form(L(3, 8, 2.2, 7, 28, 2.2), 'jdD', 1, 1, ring='K')            # unterer Stab
    c.form(L(23, 2, 2.2, 28, 22, 2.2), 'jdD', 1, 1, ring='K')          # oberer Stab
    for x, y in ((2, 6), (8, 29), (23, 0), (29, 24)):
        c.form(E(x, y, 1.2, 1.2), 'ogY', 0, 1, ring='K')               # goldene Knäufe
    feather = PG([(14, 29), (16, 21), (24, 12), (31, 8), (29, 18), (22, 26)])
    c.form(feather, 'khH', 1, 1, ring='K')                             # Tengu-Feder unten rechts
    c.line([(14, 30), (29, 11)], 'x', 1)                               # Kiel
    for x, y in ((20, 22), (23, 19), (26, 15)):                        # Fahnenkerben
        c.line([(x, y), (x + 2, y + 2)], 'K', 1)
    for x, y in ((12, 28), (5, 21)):                                   # Blutstropfen
        c.form(E(x, y, 1.0, 1.4), 'qRe', 0, 1, ring='K')
    return c


NAMES = ['sutoku_sutra']


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
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v20.png')
    print(WARN)
