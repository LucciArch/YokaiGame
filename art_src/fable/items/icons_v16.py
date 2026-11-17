"""Item-Symbole v1.6: Figuren-Siegel (je Figur ein eigenes Item, freigeschaltet über ihre Siegel).
Aufruf: cd art_src/fable/items && PYTHONPATH=.. python3 icons_v16.py [vorschau.png]"""
from ihelp import *


def haraegushi():
    """Reinigungsstab: Holzstab, oben ein Bündel weißer Zickzack-Shide und Hanffasern."""
    c = Cv()
    c.form(L(6, 28, 1.7, 19, 9, 1.4), 'jdD', 1, 1, ring='K')
    for k, x0 in enumerate((14, 18, 22, 26)):                         # Shide, im Schwung nach rechts geweht
        y0 = 6 + k
        pts = [(x0, y0), (x0 + 3, y0 + 4), (x0, y0 + 8), (x0 + 3, y0 + 12), (x0 + 1, y0 + 16)]
        c.line(pts, 'w' if k % 2 else 'W', 2)
        c.line(pts[2:], 'v', 1)
    for x in (16, 18, 20):                                             # Asa-Hanf
        c.line([(19, 8), (x - 4, 18), (x - 6, 24)], 'C', 1)
    c.form(E(19, 8, 3, 2.4), 'qrR', 1, 1, ring='K')                    # Knoten
    sparkle(c, 5, 6, 'W', 'Y')
    return c


def zanshin_tsuba():
    """Tsuba: eiserne Stichblattscheibe mit Goldrand, Klingenschlitz, zwei Hitsu-Löchern, Welleneinlage."""
    c = Cv()
    disc = E(16, 16, 12.5, 12)
    c.form(disc, '012', 2, 1, ring='K')
    c.fill(disc & ~E(16, 16, 11.3, 10.8), 'g')
    c.fill(disc & ~E(16, 16, 12.1, 11.6), 'o')
    for pts in ([(7, 21), (10, 19), (13, 21), (16, 19)], [(17, 25), (20, 23), (23, 25)]):
        c.line(pts, 'y', 1)                                            # Goldwellen
    c.fill(E(22, 9, 2.6, 2.6) & ~E(23, 8.4, 2.2, 2.2), 'Y')            # Mondsichel
    c.a[R(14.6, 9.5, 17.4, 22.5)] = '.'                                # Klingenschlitz (Nakago-ana)
    c.a[E(9, 13, 1.6, 2.8)] = '.'                                      # Hitsu-ana
    c.a[E(23, 17, 1.6, 2.8)] = '.'
    c.line([(14, 23), (18, 23)], '3', 1)
    sparkle(c, 27, 26, 'W', 'Y')
    return c


def kuzu_blatt():
    """Dreizähliges Kuzu-Blatt mit Ranke, daneben ein Fuchsfeuer."""
    c = Cv()
    c.line([(16, 18), (15, 24), (12, 28), (7, 29)], 'F', 2)            # Ranke
    c.line([(12, 28), (9, 25), (10, 23)], 'f', 1)
    for cx, cy, a, b, deg in ((16, 9, 5.5, 7.5, 0), (9, 17, 7, 4.8, -25), (23, 17, 7, 4.8, 25)):
        m = REL(cx, cy, a, b, deg) if deg else E(cx, cy, a, b)
        c.form(m, 'FfG', 2, 1, ring='K')
    c.line([(16, 17), (16, 4)], 'F', 1)                                # Blattadern
    c.line([(16, 17), (4, 16)], 'F', 1)
    c.line([(16, 17), (28, 16)], 'F', 1)
    c.fill(E(14, 7, 1.5, 2.2), 'l')
    fl = E(25, 26, 3.4, 3.4) | PG([(22, 25), (25, 18), (28, 25)])     # Fuchsfeuer
    c.form(fl, '789', 1, 1, ring='K')
    c.fill(E(25, 26.5, 1.6, 1.8) | PG([(24, 25), (25, 21), (26, 25)]), 'Y')
    return c


def bunbuku_kessel():
    """Bunbuku-Chagama: eiserner Teekessel, aus dem Tanuki-Kopf, Pfoten und geringelter Schwanz ragen."""
    c = Cv()
    c.line([(9, 13), (12, 6), (20, 6), (23, 13)], '1', 1)              # Henkel
    c.form(E(25, 22, 4, 5.5), 'jdD', 1, 1, ring='K')                   # Schwanz
    c.line([(23, 20), (28, 20)], 'j', 1)
    c.line([(23, 24), (28, 24)], 'j', 1)
    for x in (11, 20):                                                 # Pfoten
        c.form(E(x, 28, 2.4, 2), 'jdD', 1, 1, ring='K')
    body = E(16, 20, 9.5, 7.5)
    c.form(body, '012', 2, 1, ring='K')
    c.line([(7, 19), (25, 19)], '0', 1)                                # Gussnaht
    c.form(E(16, 13, 6, 2.2), '0123', 1, 1, ring='K')                  # Deckel
    c.form(E(16, 11, 1.6, 1.4), 'ogy', 0, 1, ring='K')
    head = E(6, 16, 4.6, 4.2)                                          # Tanuki-Kopf statt Ausguss
    c.form(head, 'jdD', 1, 1, ring='K')
    c.form(E(3, 12, 1.6, 1.6) | E(8, 12, 1.6, 1.6), 'jdD', 0, 1, ring='K')
    c.fill(E(5, 16, 3.2, 1.6) & head, 'k')                             # Augenmaske
    c.a[16, 4] = 'W'; c.a[16, 7] = 'W'
    c.fill(E(4, 18.5, 1.6, 1.2), 't')
    c.a[18, 3] = 'K'
    return c


def tausendstes_schwert():
    """Tachi mit Goldtsuba vor zwei gekreuzten dunklen Klingen – Benkeis Sammlung."""
    c = Cv()
    for a, b in (((6, 7), (25, 25)), ((26, 8), (7, 25))):              # Hintergrund-Klingen
        c.form(L(a[0], a[1], 1.0, b[0], b[1], 1.2), 'h12', 0, 1, ring='K')
    pts = [(7, 27), (12, 20), (17, 13), (22, 8), (26, 5)]              # gebogene Klinge
    bl = np.zeros((c.h, c.w), bool)
    for (x0, y0), (x1, y1) in zip(pts[1:], pts[2:]):
        bl |= L(x0, y0, 1.6, x1, y1, 1.2)
    c.form(bl, '23W', 0, 1, ring='K')
    c.line(pts[1:], 'W', 1, only=bl)
    c.form(L(5, 28, 2.0, 10, 23, 2.0), 'khH', 0, 1, ring='K')         # umwickelter Griff
    for x, y in ((6, 27), (8, 25)):
        c.a[y, x] = 'w'
    c.form(REL(11, 22, 3.6, 1.8, -40), 'ogy', 1, 1, ring='K')         # Tsuba
    sparkle(c, 25, 15, 'W', 'Y')
    return c


def neunter_teller():
    """Porzellanteller mit blauem Muster, eine Scherbe bricht heraus; ein Totenlicht schwebt darüber."""
    c = Cv()
    plate = E(15, 19, 12, 8.5)
    cut = PG([(19, 19), (28, 13), (29, 24)])
    c.form(plate & ~cut, 'nvW', 2, 1, ring='K')
    c.fill(E(15, 19, 8.5, 5.8) & ~cut & ~E(15, 19, 7.6, 5.0), 'a')
    c.fill(E(15, 19, 2.4, 1.7), 'z')
    for x0 in (9, 13, 17):
        c.line([(x0, 18), (x0 + 1, 21)], 'a', 1)
    c.line([(19, 19), (16, 22), (17, 26)], 'n', 1)                     # Sprung
    sh = PG([(23, 19), (29, 15), (30, 24)])                            # herausgebrochene Scherbe
    c.form(sh, 'nvW', 1, 1, ring='K')
    c.fill(sh & E(23, 19, 7.6, 5.0) & ~E(23, 19, 7.0, 4.4), 'a')
    wisp = E(8, 7, 3.4, 3.2) | PG([(5, 6), (9, 1), (11, 6)])           # Hitodama
    c.form(wisp, 'zaA', 1, 1, ring='K')
    c.fill(E(8, 7.6, 1.6, 1.4), 'W')
    return c


def tengu_tsubute():
    """Drei Steine fallen aus heiterem Himmel, dahinter Fallstreifen und eine schwarze Tengu-Feder."""
    c = Cv()
    for x in (10, 18, 25):                                             # Fallstreifen
        c.line([(x, 2), (x - 2, 10)], 'w', 1)
    c.form(L(25, 3, 1.4, 19, 13, 2.2), 'khH', 1, 1, ring='K')          # Feder
    c.line([(25, 3), (19, 13)], 'h', 1)
    for cx, cy, r in ((9, 16, 4.6), (19, 21, 5.6), (10, 26, 3.6)):
        m = E(cx, cy, r, r * 0.85) & ~PG([(cx + r * 0.3, cy - r), (cx + r + 1, cy - r), (cx + r + 1, cy)])
        c.form(m, '123', 2, 1, ring='K')
        c.a[int(cy - r * 0.3), int(cx - r * 0.3)] = '3'
    _ = c.line([(16, 28), (24, 28)], '0', 1)                           # Aufprallstaub
    return c


def taizan_fukun():
    """Ritual-Ofuda vor dem heiligen Berg Taizan: weißer Papierstreifen, rotes Siegel, schwarze Pinselschrift."""
    c = Cv()
    c.form(PG([(2, 28), (11, 9), (16, 15), (22, 6), (30, 28)]), 'xpP', 2, 1, ring='K')   # Berg
    c.fill(PG([(9, 13), (11, 9), (13, 12)]) | PG([(20, 10), (22, 6), (24, 10)]), 'w')
    paper = R(11, 4, 20, 29)
    c.form(paper, 'nvW', 1, 1, ring='K')
    c.fill(R(11, 4, 20, 6), 'q')
    c.g(13, 8, """
.k..k.
kkkkkk
..k...
.k.kk.
k...k.
......
.kkkk.
...k..
.kkkkk
..k.k.
.k...k
""", {})                                                        # Pinselzeichen (frei, kein echtes Kanji)
    c.form(E(15.5, 24, 3, 3), 'qrR', 0, 1, ring='K')                  # Siegel
    c.fill(R(14.6, 23, 16.4, 25), 'e')
    sparkle(c, 27, 4, 'W', 'R')
    return c


def ibaraki_arm():
    """Abgeschlagener Oni-Arm: roter Unterarm mit Goldreif, Krallenhand, Schnittstelle mit Knochen."""
    c = Cv()
    arm = L(25, 25, 4.2, 18, 18, 4.8) | L(18, 18, 4.8, 13, 14, 3.4)  # Unterarm mit Muskelwulst
    c.form(arm, 'qrR', 2, 1, ring='K')
    fingers = (((8, 10), (3, 8), (2, 5)), ((9, 8), (6, 4), (6, 1)), ((12, 8), (12, 4), (14, 1)), ((14, 12), (18, 10), (20, 7)))
    for a, b, tip in fingers:
        c.form(L(a[0], a[1], 1.8, b[0], b[1], 1.5), 'qrR', 1, 1, ring='K')   # gekrümmte Finger
        c.form(L(b[0], b[1], 1.3, tip[0], tip[1], 0.5), 'bBi', 0, 1, ring='K')  # Krallen
    c.form(E(11, 11, 4.6, 4.2), 'qrR', 1, 1, ring='K')               # Handfläche
    c.line([(9, 12), (12, 10)], 'q', 1)
    c.form(L(14, 15, 4.4, 15.5, 16.5, 4.4) & arm, 'ogy', 1, 1)        # Goldreif
    c.line([(13, 17), (17, 13)], 'o', 1)
    for x, y in ((20, 22), (22, 19), (18, 24)):                       # Fellbüschel
        c.a[y, x] = 'q'
    c.form(E(25.5, 25.5, 3.6, 3.6), 'UVe', 0, 1, ring='K')            # Schnittstelle
    c.form(E(25.5, 25.5, 1.6, 1.6), 'bBi', 0, 1)
    return c


def yashiori_sake():
    """Tokkuri mit Strohschnur und Schriftband, daneben eine rote Sakazuki-Schale mit Goldrand."""
    c = Cv()
    body = E(13, 21, 8, 8) | R(10, 7, 16, 14) | E(13, 7, 3.6, 1.6)
    c.form(body, 'nvW', 2, 1, ring='K')
    c.fill(R(10, 12, 16, 13), 'C')                                     # Strohschnur
    c.line([(16, 13), (18, 17)], 'C', 1)
    c.fill(R(10, 17, 16, 25) & body, 'z')                              # blaues Schriftband
    for y in (19, 22):
        c.line([(12, y), (14, y)], 'W', 1)
    c.fill(E(13, 7, 1.8, 0.8), 'k')
    cup = E(25, 25, 5.6, 2.6)
    c.form(cup, 'qrR', 1, 1, ring='K')
    c.fill(E(25, 24.3, 4.2, 1.4), 'y')
    c.fill(E(25, 24.3, 2.6, 0.9), 'Y')
    for x, y in ((24, 15), (27, 18)):                                  # Tropfen
        c.form(E(x, y, 1.2, 1.6), 'nvW', 0, 1, ring='K')
    return c


NAMES = ['haraegushi', 'zanshin_tsuba', 'kuzu_blatt', 'bunbuku_kessel', 'tausendstes_schwert', 'neunter_teller',
         'tengu_tsubute', 'taizan_fukun', 'ibaraki_arm', 'yashiori_sake']


def build():
    import shutil
    dst = os.path.join(HERE, '..', '..', '..', 'yokai', 'assets', 'items', 'icons')
    for nm in NAMES:
        save('icons', nm, globals()[nm]())
        shutil.copy(os.path.join(HERE, 'icons', nm + '.png'), os.path.join(dst, nm + '.png'))


if __name__ == '__main__':
    build()
    from PIL import Image
    out = Image.new('RGBA', (len(NAMES) * 36 * 6, 36 * 6), (30, 24, 40, 255))
    for i, nm in enumerate(NAMES):
        im = Image.open(os.path.join(HERE, 'icons', nm + '.png')).convert('RGBA')
        out.alpha_composite(im.resize((im.width * 6, im.height * 6), Image.NEAREST), (i * 216 + 12, 12))
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v16.png')
    print(WARN)
