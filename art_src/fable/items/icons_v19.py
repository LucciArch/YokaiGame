"""Item-Symbole v1.9: Tsukumogami – beseelte Hausgeräte (Welle 1).
Aufruf: cd art_src/fable/items && PYTHONPATH=.. python3 icons_v19.py [vorschau.png]"""
from ihelp import *


def biwa_bokuboku():
    """Biwa-bokuboku: eine alte Biwa-Laute, deren Wirbelkasten zum Kopf eines blinden Mönchs geworden ist; die Saiten klagen."""
    c = Cv()
    for x, y in ((3, 5), (7, 2), (28, 22)):                            # Klagetöne
        c.g(x, y, 'A.\nAA\nA.')
    neck = L(13, 21, 2.2, 23, 9, 1.8)
    c.form(neck, 'jdD', 1, 1, ring='K')
    body = E(12, 22, 9, 8.5) | E(15, 18, 5.5, 5.5)
    c.form(body, 'jdD', 2, 1, ring='K')                                # birnenförmiger Korpus
    c.fill(E(9, 18, 1.8, 0.8) | E(17, 25, 1.8, 0.8), 'K')              # Halbmond-Schalllöcher
    c.form(R(6, 25, 12, 27), 'khH', 0, 1, ring='K')                    # Steg
    for k in range(4):                                                 # Saiten
        c.line([(7 + k * 1.4, 26), (22 + k * 0.6, 8 + k * 0.5)], 'B', 1, only=body | neck)
    c.form(E(25, 7, 4.6, 4.6), 'ubi', 1, 1, ring='K')                  # kahler Mönchskopf
    c.line([(22, 7), (24, 7)], 'K', 1)                                 # blinde, geschlossene Augen
    c.line([(26, 6), (28, 7)], 'K', 1)
    c.line([(24, 10), (26, 10)], 'u', 1)
    for x, y in ((21, 3), (29, 3), (20, 9)):                           # Wirbel als Ohren/Hörner
        c.form(E(x, y, 1.4, 1.4), 'jdD', 0, 1, ring='K')
    c.form(PG([(22, 23), (30, 19), (29, 27)]), 'ogY', 0, 1, ring='K')  # Bachi
    return c


def chochin_obake():
    """Chōchin-obake: aufgerissene Papierlaterne, ein Auge, aus dem Riss leuchtet die Flamme und hängt die Zunge."""
    c = Cv()
    body = E(16, 16, 10, 12)
    c.form(body, 'Csw', 2, 1, ring='K')
    for y in (8, 12, 16, 20, 24):                                      # Bambusrippen
        c.line([(4, y), (28, y)], 'C', 1, only=body)
    c.form(R(10, 2, 22, 5), 'khH', 0, 1, ring='K')                     # Lackdeckel
    c.form(R(10, 27, 22, 30), 'khH', 0, 1, ring='K')
    c.line([(16, 0), (16, 1)], 'k', 1)
    mouth = PG([(6, 16), (16, 18), (26, 15), (24, 21), (16, 23), (8, 21)])
    c.fill(mouth, 'K')
    c.fill(E(16, 20, 5, 1.6) & mouth, 'y')                             # Flamme im Riss
    c.fill(E(16, 20, 2.4, 1.0) & mouth, 'Y')
    c.g(9, 16, 'W.\nWW')                                               # Zahnfetzen
    c.g(22, 16, '.W\nWW')
    c.form(L(14, 22, 1.8, 11, 30, 1.6), 'qRe', 0, 1, ring='K')         # Zunge
    c.form(E(19, 10, 2.8, 2.4), 'nvW', 0, 1, ring='K')                 # Auge
    c.fill(E(19, 10, 1.0, 1.4), 'k')
    c.a[9, 18] = 'W'
    c.line([(10, 9), (14, 11)], 'K', 1)                                # zugekniffenes zweites Auge
    sparkle(c, 4, 4, 'Y', 'y')
    return c


def bake_zori():
    """Bake-zōri: zerschlissene Strohsandale mit drei Augen und zwei Zähnen, rennt auf dünnen Beinchen davon."""
    c = Cv()
    sole = E(16, 15, 8, 12)
    c.form(sole, 'cCs', 2, 1, ring='K')
    for y in range(6, 26, 3):                                          # Flechtreihen
        c.line([(8, y), (24, y + 1)], 'c', 1, only=sole)
    for x, y in ((9, 3), (23, 26), (7, 22)):                           # abstehende Halme
        c.line([(x, y), (x + 2, y + 2)], 's', 1)
    for x, y in ((12, 9), (20, 9), (16, 5)):                           # drei Augen
        c.form(E(x, y, 2.0, 1.6), 'WWW', 0, 0, ring='K')
        c.a[y, x] = c.a[y, x + 1] = 'R'
    c.fill(R(11, 15, 22, 17), 'K')                                     # Maul
    c.fill(R(13, 16, 14, 18) | R(18, 16, 19, 18), 'W')                 # zwei Zähne
    c.line([(16, 18), (11, 24)], 'q', 2)                               # Hanao-Riemen
    c.line([(16, 18), (21, 24)], 'q', 2)
    c.form(E(16, 18, 1.4, 1.4), 'qrR', 0, 1)
    for a, b in (((11, 27), (8, 31)), ((21, 27), (25, 30)), ((8, 14), (3, 17)), ((24, 14), (29, 11))):
        c.line([a, b], 'K', 1)                                         # Beinchen und Ärmchen
    return c


def ittan_momen():
    """Ittan-momen: ein flatternder Streifen Baumwolle vor dem Mond, oben zwei schmale Augen."""
    c = Cv()
    c.form(E(23, 8, 6, 6), 'ogY', 1, 1, ring='K')                      # Mond
    c.fill(E(21, 7, 1.4, 1.4), 'g')
    pts = [(3 + k * 1.15, 27 - k * 0.8 + math.sin(k * 0.55) * 3.2, 2.0 + k * 0.06) for k in range(22)]
    m = np.zeros((32, 32), bool)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        m |= L(x0, y0, r0, x1, y1, r1)
    c.form(m, 'nvW', 1, 1, ring='K')
    for x0, y0, _ in pts[2::4]:                                        # Webfalten
        c.a[int(round(y0)), int(round(x0))] = 'v'
    hx, hy, _ = pts[-1]
    c.line([(hx - 2, hy - 1), (hx, hy - 1)], 'k', 1)                   # Augen
    c.line([(hx - 2, hy + 1), (hx, hy + 1)], 'k', 1)
    for y, x0, x1 in ((22, 20, 28), (27, 17, 23)):                     # Nachtwind
        c.line([(x0, y), (x1, y)], 'A', 1)
    return c


def kosode_te():
    """Kosode-no-te: ein Seidenkimono auf dem Ikō-Ständer, aus dem Ärmel greift eine bleiche Hand."""
    c = Cv()
    c.form(R(1, 3, 30, 5), 'khH', 0, 1, ring='K')                      # Ikō-Stange
    c.form(R(3, 6, 5, 30) | R(26, 6, 28, 30), 'khH', 0, 1, ring='K')
    kimono = R(6, 6, 25, 15) | R(10, 6, 21, 29)
    c.form(kimono, 'xpP', 2, 1, ring='K')
    c.line([(12, 6), (16, 14), (20, 6)], 'W', 1)                       # Kragen
    c.form(R(10, 16, 21, 18), 'ogy', 0, 1)                             # Obi
    for x, y in ((8, 9), (23, 11), (13, 23), (18, 26)):                # Kiku-Muster
        c.g(x - 1, y - 1, '.S.\nSTS\n.S.')
    hand = L(24, 15, 1.6, 22, 21, 1.4) | E(21, 22, 2.4, 2.0)
    c.form(hand, 'ubi', 0, 1, ring='K')                                # bleiche Hand aus dem Ärmel
    for x0, x1 in ((19, 18), (21, 21), (23, 24)):                      # lange Finger
        c.line([(x0, 23), (x1, 27)], 'B', 1)
    c.fill(R(23, 14, 25, 15), 'x')                                     # Ärmelschatten
    return c


NAMES = ['biwa_bokuboku', 'chochin_obake', 'bake_zori', 'ittan_momen', 'kosode_te']


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
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v19.png')
    print(WARN)
