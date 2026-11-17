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



# ---------------------------------------------------------------- Welle 2: Siegel „Sieg“
def hi_ogi():
    """Hi-ōgi: aufgefächerter Zypressenfächer mit Sonne und Kiefer, fünffarbige Schnüre hängen herab."""
    c = Cv()
    for i, (ch, x) in enumerate((('r', 4), ('W', 6), ('G', 25), ('y', 27), ('p', 29))):
        c.line([(x, 18), (x - 1 + i % 2, 24), (x + 1, 30)], ch, 1)       # Schnüre
    fan = E(16, 22, 14, 14) & (px.Y < 22) & ~E(16, 22, 4, 4)
    c.form(fan, 'cCs', 1, 1, ring='K')
    for k in range(9):                                                 # Lamellen
        a = math.pi + (k + 0.5) * math.pi / 9
        c.line([(16 + math.cos(a) * 5, 22 + math.sin(a) * 5), (16 + math.cos(a) * 13, 22 + math.sin(a) * 13)], 'c', 1)
    c.form(E(16, 13, 3.2, 3.2), 'qrR', 0, 1)                           # rote Sonne
    c.form(PG([(7, 19), (10, 14), (13, 19)]) | PG([(19, 19), (22, 15), (25, 19)]), 'FfG', 0, 1)   # Kiefern
    c.form(E(16, 23, 2.4, 2.4), 'ogy', 0, 1, ring='K')                 # Niete
    return c


def muramasa():
    """Muramasa: Katana mit welliger Härtelinie, rote Fluchaura, ein Blutstropfen fällt von der Spitze."""
    c = Cv()
    for x, y in ((8, 9), (12, 5), (24, 18), (20, 24), (27, 11), (5, 16)):  # Fluchfunken
        c.form(E(x, y, 1.2, 1.2), 'UVe', 0, 1)
    blade = L(9, 23, 1.9, 25, 6, 1.0)
    c.form(blade, '23W', 0, 1, ring='K')
    c.line([(10, 21), (13, 19), (15, 16), (18, 14), (20, 11), (23, 8)], 'W', 1, only=blade)   # Hamon
    c.form(L(5, 28, 2.0, 8, 24, 2.0), 'UVe', 0, 1, ring='K')           # rot umwickelter Griff
    c.a[27, 5] = 'k'; c.a[25, 7] = 'k'
    c.form(REL(9, 23, 3.4, 1.7, -45), 'khH', 1, 1, ring='K')           # schwarze Tsuba
    c.form(E(27, 9, 1.3, 1.8), 'qrR', 0, 1, ring='K')                  # Blutstropfen
    return c


def fuchs_trugbild():
    """Fuchsgesicht und sein bläuliches Trugbild versetzt dahinter."""
    c = Cv()

    def fox(dx, dy, fam, muzzle):
        head = PG([(6 + dx, 13 + dy), (16 + dx, 9 + dy), (26 + dx, 13 + dy), (16 + dx, 28 + dy)])
        ears = PG([(7 + dx, 14 + dy), (8 + dx, 3 + dy), (14 + dx, 10 + dy)]) | PG([(25 + dx, 14 + dy), (24 + dx, 3 + dy), (18 + dx, 10 + dy)])
        m = head | ears
        c.form(m, fam, 1, 1, ring='K')
        c.form(PG([(10 + dx, 18 + dy), (16 + dx, 28 + dy), (22 + dx, 18 + dy), (16 + dx, 16 + dy)]), muzzle, 0, 1)
        return m
    ghost = fox(4, -1, 'zaA', 'aAW')
    c.fill(ghost & ((px.X + px.Y) % 2 == 0), 'z')                      # durchscheinend gerastert
    fox(-2, 0, '789', 'vwW')
    c.form(PG([(7, 8), (7, 5), (10, 9)]) | PG([(20, 9), (21, 5), (21, 8)]), 'qrR', 0, 0)   # Ohren innen
    for x in (11, 19):                                                 # Augen
        c.line([(x - 2, 16), (x + 1, 15)], 'k', 1)
    c.fill(E(14, 26, 1.4, 1), 'k')
    return c


def shigaraki_tanuki():
    """Shigaraki-Tonfigur: Strohhut, dicker Bauch, Sakeflasche rechts, Schuldbuch links."""
    c = Cv()
    c.form(E(16, 21, 9, 9), 'jdD', 2, 1, ring='K')                     # Körper
    c.form(E(16, 23, 5.6, 5.6), 'cCs', 1, 1, ring='K')                 # Bauch
    c.form(E(16, 11, 5.6, 5), 'jdD', 1, 1, ring='K')                   # Kopf
    c.fill(E(16, 11, 4.2, 1.6), 'k')                                   # Augenmaske
    c.a[11, 14] = 'W'; c.a[11, 18] = 'W'
    c.form(E(16, 14, 1.6, 1.2), 'cCs', 0, 1)
    c.form(E(16, 6.5, 9.5, 2.4) | E(16, 5, 4, 2.4), 'cCs', 1, 1, ring='K')   # Strohhut
    c.form(R(25, 15, 29, 26) | E(27, 14, 1.4, 1.4), 'nvW', 1, 1, ring='K')   # Sakeflasche
    c.line([(26, 20), (28, 20)], 'q', 1)
    c.form(R(2, 17, 8, 26), 'IJO', 1, 1, ring='K')                     # Schuldbuch (Kayoi-chō)
    c.fill(R(4, 18, 6, 25), 'w')
    c.line([(5, 19), (5, 24)], 'k', 1)
    for x in (12, 20):                                                 # Füße
        c.form(E(x, 29, 2.6, 1.6), 'jdD', 0, 1, ring='K')
    return c


def tachi_ojo():
    """Benkeis Naginata aufrecht, mit Pfeilen gespickt."""
    c = Cv()
    c.form(R(15, 9, 17, 30), 'jdD', 1, 1, ring='K')                    # Schaft
    blade = PG([(14, 11), (13, 5), (17, 1), (20, 4), (18, 11)])
    c.form(blade, '23W', 1, 1, ring='K')
    c.form(R(13, 10, 19, 12), 'ogy', 0, 1, ring='K')                   # Habaki
    for (x0, y0), (x1, y1) in (((17, 16), (28, 8)), ((15, 21), (4, 14)), ((17, 25), (28, 22))):
        c.form(L(x0, y0, 0.8, x1, y1, 0.8), 'jdD', 0, 1, ring='K')    # Pfeilschäfte
        dx, dy = (x1 - x0) / 11, (y1 - y0) / 11
        nx, ny = -dy, dx
        for sd in (1, -1):                                             # Federn öffnen sich nach außen
            c.line([(x1 - dx * 3.5, y1 - dy * 3.5), (x1 + nx * sd * 2.2, y1 + ny * sd * 2.2)], 'W' if sd > 0 else 'w', 2)
        c.a[int(round(y1 - dy * 2)), int(round(x1 - dx * 2))] = 'q'
    return c


def tsurube():
    """Hölzerner Brunneneimer mit Eisenreifen und Seil, Wasser schwappt über."""
    c = Cv()
    c.line([(16, 2), (16, 9)], 'C', 1)                                 # Seil
    c.line([(9, 12), (16, 7), (23, 12)], 'c', 1)                       # Bügel
    bucket = PG([(8, 12), (24, 12), (22, 28), (10, 28)])
    c.form(bucket, 'jdD', 2, 1, ring='K')
    for y in (15, 24):
        c.line([(8 + (y - 12) * 0.13, y), (24 - (y - 12) * 0.13, y)], '1', 2)
    for x in (12, 16, 20):
        c.line([(x, 13), (x, 27)], 'j', 1, only=bucket)
    c.form(E(16, 12, 8, 2.2), 'zaA', 0, 1, ring='K')                   # Wasser
    c.form(PG([(22, 12), (28, 14), (27, 21), (25, 16)]), 'zaA', 0, 1, ring='K')   # überschwappend
    for x, y in ((27, 25), (5, 18)):
        c.form(E(x, y, 1.2, 1.6), 'aAW', 0, 1, ring='K')
    return c


def kakuremino():
    """Strohmantel der Tengu: gestufte Strohlagen, oben eine schwarze Feder."""
    c = Cv()
    for k, (y0, y1, w0, w1) in enumerate(((5, 14, 5, 9), (11, 20, 8, 11), (16, 27, 10, 13))):
        m = PG([(16 - w0, y0), (16 + w0, y0), (16 + w1, y1), (16 - w1, y1)])
        c.form(m, 'cCs', 1, 1, ring='K')
        for x in range(16 - w1 + 1, 16 + w1, 2):                       # zottige Halmfransen
            c.line([(x, y1 - 5), (x + (1 if x > 16 else -1), y1 + 1 + (x // 2) % 2)], 'C' if x % 4 else 'c', 1)
    c.form(E(16, 4, 3.6, 2.6), 'khH', 1, 1, ring='K')                  # dunkle Kapuzenöffnung
    c.form(E(16, 7, 4.6, 1.4), 'qrR', 0, 1, ring='K')                  # Kragen-Schnur
    c.form(L(22, 4, 1.6, 28, 13, 0.6), 'khH', 0, 1, ring='K')          # Tengu-Feder
    sparkle(c, 5, 6, 'W', 'w')
    return c


def hoki_naiden():
    """Geheimbuch: indigo Umschlag mit Fadenbindung und Titelstreifen, ein Papiervogel fliegt heraus."""
    c = Cv()
    c.form(R(4, 9, 20, 29), 'IJO', 2, 1, ring='K')
    c.fill(R(5, 28, 20, 29), 'w')                                      # Seitenkante
    for y in (11, 15, 19, 23, 27):                                     # Bindung
        c.a[y, 6] = 'W'
    c.fill(R(12, 11, 16, 24), 'w')
    for y in (13, 16, 19, 22):
        c.line([(13, y), (15, y)], 'k', 1)
    star = [(12 + 3 * math.cos(-math.pi / 2 + k * 4 * math.pi / 5), 6 + 3 * math.sin(-math.pi / 2 + k * 4 * math.pi / 5)) for k in range(6)]
    c.form(PG([(19, 8), (29, 2), (26, 9)]) | PG([(19, 8), (30, 10), (25, 12)]), 'nvW', 0, 1, ring='K')   # Papiervogel
    c.line([(19, 8), (17, 10)], 'v', 1)
    c.line(star, 'q', 1)                                               # Seimei-Kikyō-Stern
    return c


def masakari():
    """Kintarōs Axt: dicker Holzstiel, breiter Eisenkopf mit hellem Schliff, rote Kordel."""
    c = Cv()
    c.form(L(8, 28, 1.9, 22, 5, 1.7), 'jdD', 1, 1, ring='K')
    head = E(22.5, 13, 7.5, 9) & ~E(12, 13, 6, 12) & (px.X > 15)
    c.form(head, '123', 2, 1, ring='K')
    c.fill(head & ~E(22, 13, 7, 8), 'W')                               # Schneide
    c.form(R(16, 6, 20, 12), '012', 1, 1, ring='K')                    # Öhr
    c.line([(11, 24), (8, 27), (9, 30)], 'q', 1)                       # Kordel
    c.form(E(22, 13, 1.8, 1.8), 'qrR', 0, 1)                           # Kintarō-Raute
    sparkle(c, 4, 6, 'W', 'Y')
    return c


def habakiri():
    """Totsuka-Schwert mit gerader Doppelklinge über einem abgeschlagenen Orochi-Schwanz."""
    c = Cv()
    tail = L(5, 25, 2.6, 12, 27, 3.0) | L(12, 27, 3.0, 22, 25, 2.4) | L(22, 25, 2.4, 28, 21, 1.2)
    c.form(tail, 'FfG', 2, 1, ring='K')
    for x in (7, 12, 17, 22):
        c.a[28 if x < 20 else 25, x] = 'l'
    blade = PG([(14, 22), (14, 6), (16, 2), (18, 6), (18, 22)])
    c.form(blade, '23W', 1, 1, ring='K')
    c.line([(16, 4), (16, 21)], '1', 1)                                # Grat
    c.form(R(11, 22, 21, 24), 'ogy', 1, 1, ring='K')                   # Parierstange
    c.form(R(15, 24, 17, 28), 'jdD', 0, 1, ring='K')
    c.form(E(16, 29, 2, 1.6) & ~E(16, 29, 0.8, 0.6), 'ogy', 0, 1, ring='K')
    c.fill(E(26, 22, 1, 1), 'q')
    return c


def tamagushi():
    """Tamagushi: Sakaki-Zweig mit glänzenden Blättern, daran weiße Zickzack-Shide."""
    c = Cv()
    c.form(L(5, 29, 1.4, 25, 5, 1.0), 'jdD', 1, 1, ring='K')         # Zweig
    for cx, cy, deg in ((9, 21, -70), (14, 22, 20), (13, 15, -60), (19, 16, 25), (18, 9, -55), (24, 9, 30), (23, 4, -40)):
        c.form(REL(cx, cy, 4.2, 2.2, deg), 'FfG', 1, 1, ring='K')
    for cx, cy in ((9, 21), (13, 15), (18, 9)):
        c.a[cy - 1, cx] = 'l'
    pts = [(16, 13), (20, 16), (16, 19), (20, 22), (16, 25), (19, 28)]  # Shide
    c.line(pts, 'W', 2)
    c.line(pts[1::2], 'v', 1)
    c.form(E(15, 13, 1.6, 1.4), 'qrR', 0, 1, ring='K')                 # Knoten
    sparkle(c, 27, 22, 'W', 'Y')
    return c


def kesagiri():
    """Kesa-giri-Rolle: halb geöffnete Schriftrolle, quer darüber ein roter Diagonalschnitt."""
    c = Cv()
    c.form(R(6, 7, 26, 24), 'cCs', 1, 1, ring='K')                    # Papier
    c.form(R(3, 5, 7, 26), 'jdD', 1, 1, ring='K')                     # Stäbe
    c.form(R(25, 5, 29, 26), 'jdD', 1, 1, ring='K')
    c.form(R(4, 4, 6, 6) | R(4, 25, 6, 27) | R(26, 4, 28, 6) | R(26, 25, 28, 27), 'ogy', 0, 1, ring='K')
    for x in (10, 13, 16):                                             # Schriftspalten
        for y in range(10, 22, 3):
            c.a[y, x] = 'k'
    c.line([(8, 22), (24, 9)], 'q', 3)                                 # Diagonalschnitt
    c.line([(8, 22), (24, 9)], 'R', 1)
    c.line([(5, 25), (8, 22)], 'W', 1)
    sparkle(c, 24, 9, 'W', 'R')
    return c


def hoshi_tama():
    """Hoshi no Tama: zwiebelförmiges Juwel mit Spitze, darin ein blaues Fuchsfeuer, umweht von Flammen."""
    c = Cv()
    for x0, d in ((6, -1), (26, 1)):                                    # umwehende Flammen
        fl = E(x0, 22, 2.6, 3) | PG([(x0 - 2, 21), (x0 + 2 * d, 13), (x0 + 2, 21)])
        c.form(fl, '789', 0, 1, ring='K')
    jewel = E(16, 20, 8.5, 8) | PG([(9, 17), (16, 3), (23, 17)])
    c.form(jewel, 'nvW', 2, 1, ring='K')
    c.fill(E(16, 21, 6, 5.5), 'w')
    flame = E(16, 23, 3.4, 3.2) | PG([(13, 22), (16, 13), (19, 22)])  # Fuchsfeuer im Inneren
    c.form(flame, 'zaA', 0, 1)
    c.fill(E(16, 24, 1.4, 1.4), 'W')
    c.form(R(11, 27, 21, 29), 'ogy', 0, 1, ring='K')                   # Fassung
    sparkle(c, 21, 8, 'W', 'Y')
    return c


def tanuki_bayashi():
    """Tanuki-bayashi: runder Tanuki-Bauch, zwei Pfoten schlagen die Trommel, Schallbögen, Vollmond."""
    c = Cv()
    c.form(E(26, 5, 3.8, 3.8), 'gyY', 0, 1, ring='K')                  # Mond
    belly = E(16, 22, 9.5, 7.5)
    c.form(belly, 'jdD', 2, 1, ring='K')
    c.form(E(16, 23, 6.5, 5.2), 'cCs', 1, 1)                           # Trommelbauch
    c.a[23, 16] = 'd'
    for x in (11, 21):                                                 # Ohren
        c.form(E(x, 5, 2, 2), 'jdD', 0, 1, ring='K')
    head = E(16, 10, 6, 5)
    c.form(head, 'jdD', 1, 1, ring='K')
    c.fill(E(16, 10, 4.6, 1.6) & head, 'k')                            # Augenmaske
    c.a[10, 14] = 'W'; c.a[10, 18] = 'W'
    c.fill(E(16, 13, 2.2, 1.4), 's')
    c.a[13, 16] = 'K'
    for x, y in ((7, 18), (25, 18)):                                   # trommelnde Pfoten
        c.form(E(x, y, 2.6, 2.2), 'khH', 1, 1, ring='K')
    for r in (0, 3):                                                   # Schallbögen
        c.line([(4 - r * 0.6, 21), (2 - r * 0.6, 24), (4 - r * 0.6, 27)], 'y', 1)
        c.line([(28 + r * 0.6, 21), (30 + r * 0.4, 24), (28 + r * 0.6, 27)], 'y', 1)
    return c


def gojo_giboshi():
    """Giboshi der Gojō-Brücke: zwiebelförmige Bronzekappe auf rot lackiertem Pfosten, dahinter eine Naginata."""
    c = Cv()
    c.line([(4, 29), (27, 4)], 'jdD'[1], 2)                            # Naginata-Schaft
    c.form(PG([(23, 9), (27, 3), (30, 1), (28, 6)]), '23W', 0, 1, ring='K')
    post = R(11, 17, 21, 30)
    c.form(post, 'qrR', 2, 1, ring='K')
    c.form(R(10, 15, 22, 18), 'ogy', 1, 1, ring='K')                   # Kragen
    cap = E(16, 11, 6, 5) | PG([(11, 10), (16, 2), (21, 10)])
    c.form(cap, 'Ffo', 2, 1, ring='K')                                 # Bronze mit Grünspan
    c.fill(E(14, 10, 1.4, 2.4), 'y')
    c.form(E(16, 2.5, 1.5, 1.5), 'ogy', 0, 1, ring='K')
    c.line([(11, 23), (21, 23)], 'q', 1)
    return c


def ido_kagami():
    """Brunnenspiegel: steinerne Brunnenfassung von oben, im Wasser spiegelt ein zerbrochener Teller."""
    c = Cv()
    rim = E(16, 17, 13, 11)
    c.form(rim, '012', 2, 1, ring='K')
    for k in range(8):                                                 # Steinfugen
        a = k * math.pi / 4
        c.line([(16 + 9.5 * math.cos(a), 17 + 7.8 * math.sin(a)), (16 + 12.5 * math.cos(a), 17 + 10.5 * math.sin(a))], '0', 1)
    water = E(16, 17, 9, 7.5)
    c.form(water, 'zaA', 1, 0, ring='K')
    c.fill(water & ~E(16, 18, 8, 6.5), 'z')
    plate = E(16, 17, 5, 3.6)
    c.form(plate, 'nvW', 1, 1)
    c.fill(E(16, 17, 2.6, 1.8), 'a')
    c.line([(15, 14), (17, 17), (16, 20)], 'z', 1)                     # Sprung
    for x, y in ((9, 15), (23, 19)):
        c.a[y, x] = 'W'
    return c


def sojobo_hane():
    """Sōjōbōs Feder: große schwarze Schwungfeder mit hellem Kiel, umweht von Windwirbeln."""
    c = Cv()
    for r, ch in ((11, 'w'), (7, 'v')):                                # Wirbel
        pts = [(16 + r * math.cos(t / 6), 16 + r * 0.8 * math.sin(t / 6)) for t in range(0, 26)]
        c.line(pts, ch, 1)
    vane = REL(15, 17, 13, 4.5, -45) & ~REL(23, 7, 4, 3, -45)
    c.form(vane, 'khH', 2, 1, ring='K')
    for k in range(-3, 4):                                             # Fahnenkerben
        c.a[17 + k * 3 - 1 if 0 <= 17 + k * 3 - 1 < 32 else 0, 15 + k * 3 if 0 <= 15 + k * 3 < 32 else 0] = 'h'
    c.line([(5, 27), (24, 8)], 'B', 1)                                 # Kiel
    c.line([(3, 29), (6, 26)], 'i', 2)
    return c


def juni_shinsho():
    """Jūni-Shinshō: zwölf goldene Generalsflammen im Kreis um Seimeis Kikyō-Stern."""
    c = Cv()
    c.form(E(16, 16, 7, 7), 'IJO', 1, 1, ring='K')
    star = [(16 + 5 * math.cos(-math.pi / 2 + k * 4 * math.pi / 5), 16 + 5 * math.sin(-math.pi / 2 + k * 4 * math.pi / 5)) for k in range(6)]
    c.line(star, 'W', 1)
    for k in range(12):
        a = k * math.pi / 6
        x, y = 16 + 12.5 * math.cos(a), 16 + 12.5 * math.sin(a)
        c.form(E(x, y, 2.1, 2.1), 'ogy' if k % 3 else 'qrR', 0, 1, ring='K')
    return c


def setsubun_mame():
    """Setsubun-Bohnen: hölzerne Masu voller gerösteter Sojabohnen, einige fliegen heraus."""
    c = Cv()
    c.form(PG([(4, 15), (28, 15), (25, 29), (7, 29)]), 'jdD', 2, 1, ring='K')   # Masu
    c.form(PG([(4, 15), (28, 15), (26, 18), (6, 18)]), 'dDt', 0, 1, ring='K')
    for x in range(7, 26, 3):                                          # Bohnenhaufen
        c.form(E(x, 14 - (x % 2), 1.8, 1.5), 'dDt', 0, 1, ring='K')
    for x, y in ((9, 6), (16, 3), (23, 7), (27, 11)):                  # fliegende Bohnen
        c.form(E(x, y, 1.8, 1.5), 'dDt', 0, 1, ring='K')
    c.line([(12, 22), (20, 22)], 't', 1)
    c.form(E(16, 23, 2, 1.6), 'qrR', 0, 1)                             # Glückszeichen
    return c


def murakumo():
    """Ame-no-Murakumo: geballte Gewitterwolke, darunter ein Blitz, der in ein Schwert übergeht."""
    c = Cv()
    cloud = E(9, 11, 6, 5) | E(17, 8, 7, 6) | E(24, 12, 6, 5) | R(5, 11, 28, 16)
    c.form(cloud, '012', 2, 1, ring='K')
    c.fill(cloud & E(16, 15, 13, 2.2), '0')
    bolt = PG([(17, 16), (13, 23), (16, 23), (12, 30), (21, 21), (18, 21), (21, 16)])
    c.form(bolt, 'gyY', 0, 1, ring='K')
    for x, y in ((7, 19), (25, 20), (27, 25), (6, 25)):                # Regen
        c.line([(x, y), (x - 1, y + 3)], 'a', 1)
    return c


def kotodama():
    """Kotodama-Norito: gefaltetes Gebetsblatt (Hōsho) mit Schriftzeilen, aus dem Lichtwellen strömen."""
    c = Cv()
    for r in (12, 9):                                                  # Klangwellen des Gebets
        c.line([(16 + r * math.cos(t / 10), 16 + r * math.sin(t / 10)) for t in range(-30, -3)], 'y' if r > 10 else 'Y', 1)
    c.form(PG([(9, 9), (23, 9), (24, 29), (8, 29)]), 'cCs', 1, 1, ring='K')
    c.form(R(8, 13, 24, 15), 'qrR', 0, 1, ring='K')                    # Mizuhiki-Band
    c.line([(8, 14), (24, 14)], 'W', 1)
    for x in (11, 14, 17, 20):                                         # Schriftspalten
        for y in range(17, 28, 2):
            if (x + y) % 3:
                c.a[y, x] = 'k'
    return c


def tsubame_gaeshi():
    """Tsubame-gaeshi: eine Schwalbe im Wendeflug, dahinter die geschwungene Spur einer Klinge."""
    c = Cv()
    arc = [(4 + t, 26 - 18 * math.sin(t / 26 * math.pi)) for t in range(0, 27, 2)]
    c.line(arc, '2', 2)
    c.line(arc, 'W', 1)
    body = REL(17, 14, 6, 3, -20)
    wings = PG([(14, 13), (5, 5), (9, 13)]) | PG([(19, 13), (27, 4), (23, 14)])
    tail = PG([(22, 16), (30, 22), (25, 17), (29, 26), (21, 18)])
    c.form(wings | tail, 'IJO', 1, 1, ring='K')
    c.form(body, 'IJO', 1, 1, ring='K')
    c.fill(E(15, 16, 3, 1.4), 'W')                                     # weiße Brust
    c.fill(E(12, 13, 1.2, 1), 'q')                                     # rote Kehle
    c.a[12, 13] = 'K'
    return c


def shinoda_blatt():
    """Blatt aus dem Shinoda-Wald: welkes Kuzu-Blatt im Herbstton, daneben ein weißer Fuchsschwanz im Nebel."""
    c = Cv()
    c.form(E(16, 26, 13, 3), 'nvw', 0, 1)                              # Nebel
    tail = REL(9, 17, 8, 3.6, -60)
    c.form(tail, 'nvW', 2, 1, ring='K')
    c.form(REL(5, 24, 2.4, 2, -60), '789', 0, 1, ring='K')
    leaf = REL(20, 13, 7.5, 5.5, 25)
    c.form(leaf, '789', 2, 1, ring='K')
    c.line([(14, 9), (26, 17)], 'N', 1)
    for x, y in ((18, 11), (22, 14)):
        c.line([(x, y), (x - 1, y + 4)], 'N', 1)
        c.line([(x, y), (x + 3, y - 2)], 'N', 1)
    c.line([(26, 17), (28, 22)], 'j', 1)
    return c


def tanuki_tokkuri():
    """Tokkuri des Tanuki: bauchige Sakeflasche aus Ton mit Schnur und Strohhut-Deckel, Tropfen am Hals."""
    c = Cv()
    body = E(16, 21, 9, 8.5) | R(13, 6, 19, 14)
    c.form(body, 'jdD', 2, 1, ring='K')
    c.fill(E(16, 22, 6.5, 6) & ~E(16, 22, 5.5, 5), 'd')
    c.form(R(9, 18, 23, 26) & E(16, 22, 9, 8.5), 'nvW', 1, 1)          # Papieretikett
    for y in (20, 22, 24):
        c.line([(14, y), (18, y)], 'k', 1)
    c.form(PG([(9, 6), (16, 1), (23, 6), (16, 8)]), 'cCs', 1, 1, ring='K')   # Strohhut-Stopfen
    c.line([(12, 11), (6, 15), (5, 22)], 'q', 1)                       # Trageschnur
    c.form(E(24, 6, 1.2, 1.6), 'aAW', 0, 1, ring='K')
    return c


def nanatsu_dogu():
    """Benkeis sieben Waffen: im Fächer gekreuzt – Naginata, Kanabō, Sichel, Säge, Axt, Hammer, Rechen."""
    c = Cv()
    tips = [(3, 6), (8, 2), (14, 1), (20, 2), (26, 4), (30, 9)]
    for k, (x, y) in enumerate(tips):
        c.line([(16, 29), (x, y + 3)], 'jdD'[k % 2 + 1], 2)
    c.form(PG([(1, 9), (3, 2), (6, 7)]), '23W', 0, 1, ring='K')        # Naginata
    c.form(E(8, 4, 2.2, 3), '012', 1, 1, ring='K')                     # Kanabō
    c.form(E(14, 3, 3, 1.6) & ~E(14, 4.5, 2.4, 1.6), '23W', 0, 1, ring='K')   # Sichel
    c.form(R(19, 1, 23, 5), '123', 0, 1, ring='K')                     # Hammer
    c.form(E(27, 6, 3, 2.6) & (px.X > 25), '23W', 0, 1, ring='K')      # Axt
    for x in (28, 30):                                                 # Rechen
        c.a[9, x] = '2'
    c.form(E(16, 28, 4, 2.4), 'qrR', 1, 1, ring='K')                   # Bündelschnur
    return c


def zehnter_teller():
    """Der zehnte Teller: blau bemalter Porzellanteller, ganz – darunter die Scherben der neun anderen."""
    c = Cv()
    for x, y, d in ((5, 25, 1), (11, 28, -1), (22, 28, 1), (27, 24, -1)):
        c.form(PG([(x, y), (x + 3 * d, y - 2), (x + 2 * d, y + 2)]), 'nvW', 0, 1, ring='K')
    plate = E(16, 14, 11.5, 9.5)
    c.form(plate, 'nvW', 2, 1, ring='K')
    c.fill(E(16, 15, 7.5, 5.8) & ~E(16, 15, 6.5, 4.8), 'J')
    c.fill(E(16, 15, 3, 2.2), 'O')
    for k in range(10):                                                # zehn Punkte am Rand
        a = k * math.tau / 10
        c.a[int(round(14 + 8.6 * math.sin(a))), int(round(16 + 10.4 * math.cos(a)))] = 'J'
    sparkle(c, 26, 5, 'W', 'A')
    return c


def hanadaka_men():
    """Hanadaka-Maske: rotes Tengu-Gesicht mit langer Nase, buschigen weißen Brauen, goldenen Augen."""
    c = Cv()
    face = E(13, 16, 9, 11)
    c.form(face, 'qrR', 2, 1, ring='K')
    c.form(L(14, 16, 2.6, 29, 9, 1.6), 'qrR', 1, 1, ring='K')          # Nase
    for x0 in (7, 14):                                                 # Brauen
        c.form(E(x0 + 2, 11, 3.6, 1.6), 'vwW', 0, 1, ring='K')
    for x in (9, 16):
        c.form(E(x, 14, 1.6, 1.2), 'gyY', 0, 1, ring='K')
        c.a[14, x] = 'K'
    c.line([(8, 23), (11, 25), (16, 24)], 'U', 1)                      # Mund
    c.line([(5, 18), (2, 22), (3, 28)], 'k', 1)                        # Maskenschnur
    c.form(E(13, 6, 3, 1.6), 'khH', 0, 1, ring='K')                    # Tokin
    return c


def kikyo_mon():
    """Kikyō-Mon: violette Glockenblume als fünfzackiges Wappen auf schwarzem Lackgrund, Pentagramm in Gold."""
    c = Cv()
    c.form(E(16, 16, 13, 13), 'khH', 1, 1, ring='K')
    for k in range(5):                                                 # fünf Blütenblätter
        a = -math.pi / 2 + k * math.tau / 5
        c.form(E(16 + 6.5 * math.cos(a), 16 + 6.5 * math.sin(a), 4, 4), 'xpP', 1, 1, ring='K')
    c.fill(E(16, 16, 4, 4), 'p')
    star = [(16 + 8 * math.cos(-math.pi / 2 + k * 4 * math.pi / 5), 16 + 8 * math.sin(-math.pi / 2 + k * 4 * math.pi / 5)) for k in range(6)]
    c.line(star, 'y', 1)
    c.fill(E(16, 16, 1.2, 1.2), 'Y')
    return c


def oni_tsuno():
    """Abgebrochenes Oni-Horn: gekrümmtes, beinfarbenes Horn mit Rillen, rote Bruchkante, darüber ein Zornesfunke."""
    c = Cv()
    horn = L(9, 27, 5, 16, 14, 3.8) | L(16, 14, 3.8, 21, 7, 2.6) | L(21, 7, 2.6, 26, 3, 0.8)
    c.form(horn, 'ubB', 2, 1, ring='K')
    for t in (0.2, 0.4, 0.6):                                          # Rillen
        x, y = 9 + 14 * t, 27 - 18 * t
        c.line([(x - 4, y - 2), (x + 3, y + 3)], 'u', 1)
    c.form(E(9, 27, 5, 2.6), 'UVR', 1, 1, ring='K')                    # Bruchkante
    c.fill(E(9, 27, 2.6, 1.2), 'U')
    sparkle(c, 26, 18, 'R', 'q')
    return c


def kushinada_kushi():
    """Kushinadas Kamm: roter Lackkamm mit Goldranke und Kirschblüte, ein Wassertropfen wie eine Träne."""
    c = Cv()
    back = E(16, 13, 12, 7) & (px.Y < 16)
    c.form(back, 'UVR', 2, 1, ring='K')
    c.form(R(4, 15, 28, 17), 'UVR', 1, 1, ring='K')
    for x in range(5, 28, 2):                                          # Zinken
        c.line([(x, 17), (x, 26)], 'U' if x % 4 else 'V', 1)
    c.line([(8, 11), (12, 8), (16, 10), (20, 8), (24, 11)], 'y', 1)    # Goldranke
    for k in range(5):
        a = -math.pi / 2 + k * math.tau / 5
        c.form(E(16 + 2.4 * math.cos(a), 11 + 2.4 * math.sin(a), 1.6, 1.6), 'mST', 0, 1)
    c.fill(E(16, 11, 1, 1), 'y')
    c.form(E(27, 27, 1.6, 2.2) | PG([(26, 26), (27, 22), (28, 26)]), 'aAW', 0, 1, ring='K')
    return c


def onusa():
    """Ōnusa: großer Reinigungsstab aus Sakaki-Holz, dichte Papierschleppe aus Shide und Hanf, schräg geschwungen."""
    c = Cv()
    c.form(L(4, 29, 1.8, 14, 11, 1.6), 'jdD', 1, 1, ring='K')
    for k in range(6):                                                 # breite Papierschleppe
        x0 = 13 + k * 2.4
        pts = [(x0, 8 + k * 0.6), (x0 + 4, 12 + k), (x0 + 1, 16 + k), (x0 + 5, 20 + k), (x0 + 2, 25 + k * 0.6)]
        c.line(pts, 'W' if k % 2 else 'w', 2)
        c.line(pts[3:], 'v', 1)
    for x in (10, 12, 14):                                             # Asa-Hanf
        c.line([(15, 9), (x - 3, 19), (x - 5, 25)], 'C', 1)
    c.form(E(15, 9, 3.4, 2.6), 'qrR', 1, 1, ring='K')                  # roter Knoten
    c.fill(E(15, 9, 1.2, 1), 'e')
    sparkle(c, 6, 6, 'W', 'Y')
    sparkle(c, 28, 4, 'w', 'W')
    return c


def ichi_no_tachi():
    """Ichi-no-tachi: Tachi frisch aus der Saya gerissen, ein einziger weißer Schnitt quer über das Feld."""
    c = Cv()
    c.line([(2, 6), (30, 26)], 'v', 1)                                 # der Schnitt
    c.line([(4, 7), (28, 24)], 'W', 1)
    c.form(L(7, 25, 1.6, 27, 5, 1.0), '23W', 0, 1, ring='K')           # Klinge
    c.line([(9, 23), (26, 6)], 'W', 1)
    c.form(E(7, 25, 3, 3), '012', 1, 1, ring='K')                      # Tsuba
    c.fill(E(7, 25, 1.4, 1.4), 'g')
    c.form(L(6, 26, 1.7, 2, 30, 1.6), 'khH', 0, 1, ring='K')           # Griff mit Wicklung
    for t in (0.3, 0.7):
        c.a[int(26 + 4 * t), int(6 - 4 * t)] = 'W'
    sparkle(c, 27, 4, 'W', 'Y')
    return c


def kitsune_chochin():
    """Kitsune-Chōchin: gerippte Papierlaterne mit Fuchswappen, glühend orange, an einem Bambusstab, Fuchsfeuer drum."""
    c = Cv()
    c.line([(16, 1), (16, 6)], 'd', 1)
    c.form(R(11, 5, 21, 7), 'khH', 0, 1, ring='K')
    c.form(R(11, 25, 21, 27), 'khH', 0, 1, ring='K')
    lamp = E(16, 16, 8.5, 9.5)
    c.form(lamp, '789', 2, 1, ring='K')
    for y in (11, 14, 17, 20, 23):                                     # Rippen
        c.fill(lamp & (px.Y >= y) & (px.Y < y + 1), '8')
    c.form(PG([(12, 19), (13, 12), (15, 16), (17, 16), (19, 12), (20, 19), (16, 22)]), 'nvW', 0, 1, ring='K')
    c.a[17, 14] = 'K'; c.a[17, 18] = 'K'
    for x, y in ((4, 12), (28, 9), (27, 24)):                          # Fuchsfeuer
        c.form(E(x, y, 1.8, 2.4) | PG([(x - 1, y), (x, y - 5), (x + 1, y)]), 'aAW', 0, 1, ring='K')
    return c


def tanuki_kesa():
    """Tanuki-Kesa: ein steinerner Jizō mit rotem Lätzchen und Ocker-Kesa – hinten verrät ihn ein gestreifter Tanuki-Schwanz."""
    c = Cv()
    tail = REL(24, 24, 7, 3.4, -40)
    c.form(tail, '789', 1, 1, ring='K')
    for d in (-2, 2):                                                  # Schwanzringe
        c.fill(REL(24 + d, 24 - d, 1, 3.4, -40) & tail, 'j')
    c.form(E(15, 22, 8, 8) & (px.Y < 29), '123', 2, 1, ring='K')       # Steinleib
    c.form(PG([(8, 16), (22, 16), (15, 28)]), 'jdD', 1, 1, ring='K')    # Kesa schräg über der Brust
    c.line([(9, 17), (15, 27)], 'g', 1)
    c.form(PG([(10, 14), (20, 14), (15, 20)]), 'qrR', 1, 1, ring='K')  # rotes Lätzchen
    c.form(E(15, 9, 5.5, 5.5), '123', 2, 1, ring='K')                  # kahler Kopf
    c.line([(12, 9), (13, 10)], 'K', 1)                                # geschlossene Augen
    c.line([(17, 10), (18, 9)], 'K', 1)
    c.a[12, 15] = '1'
    c.form(R(4, 28, 27, 31), '012', 1, 1, ring='K')                    # Sockel
    return c


def kanjincho():
    """Kanjinchō: aufgerollte, leere Spendenrolle, die Benkei als Liste vorlas – mit Holzstab und Kordel."""
    c = Cv()
    c.form(R(5, 9, 27, 23), 'nvW', 1, 1, ring='K')
    for y in range(12, 22, 2):                                         # nur angedeutete Zeilen (die Liste ist leer)
        c.line([(9, y), (9 + (y * 7) % 11 + 6, y)], 'n', 1)
    c.form(R(3, 7, 7, 25), 'jdD', 1, 1, ring='K')                      # Rollstab links
    c.form(R(25, 7, 29, 25), 'cCs', 1, 1, ring='K')                    # aufgerollter Rest
    c.line([(27, 8), (27, 24)], 'C', 1)
    c.line([(5, 25), (8, 29), (12, 28)], 'q', 1)                       # Kordel
    c.form(E(12, 28, 1.4, 1.4), 'qrR', 0, 1, ring='K')
    c.form(E(21, 17, 2.6, 2.6), 'qrR', 0, 1, ring='K')                 # Siegel
    return c


def okiku_ido():
    """Brunnen von Banchō Sarayashiki: steinerner Brunnenrand in der Nacht, aus dem eine bleiche Hand einen Teller hebt."""
    c = Cv()
    c.form(R(4, 18, 28, 29), '012', 2, 1, ring='K')
    for x, y in ((4, 22), (12, 18), (20, 22), (12, 25), (24, 25)):    # Steinfugen
        c.line([(x, y), (x + 8, y)], '0', 1)
    c.form(E(16, 18, 12, 3), 'IJO', 1, 1, ring='K')                    # Brunnenöffnung
    c.fill(E(16, 18, 10, 2), 'k')
    c.form(L(16, 18, 1.6, 15, 10, 1.4), 'nvW', 0, 1, ring='K')         # Arm
    plate = E(15, 7, 7, 3)
    c.form(plate, 'nvW', 1, 1, ring='K')
    c.fill(E(15, 7, 4, 1.4) & ~E(15, 7, 3, 0.6), 'J')
    for x, y in ((5, 6), (27, 10)):                                    # Hitodama
        c.form(E(x, y, 1.6, 1.8), 'aAW', 0, 1, ring='K')
    return c


def ushiwaka_fue():
    """Ushiwakas Flöte: Ryūteki aus geschwärztem Bambus mit roten Wicklungen, Klangnoten und ein Tengu-Federchen."""
    c = Cv()
    c.form(L(4, 26, 2, 27, 6, 2), 'khH', 1, 1, ring='K')
    for t in (0.12, 0.45, 0.88):                                       # Kabaki-Wicklungen
        x, y = 4 + 23 * t, 26 - 20 * t
        c.form(E(x, y, 2.4, 2.4) & L(4, 26, 2, 27, 6, 2), 'qrR', 0, 1)
    for t in (0.55, 0.63, 0.71, 0.79):                                 # Grifflöcher
        c.a[int(round(26 - 20 * t)), int(round(4 + 23 * t))] = 'K'
    c.form(L(6, 24, 1.4, 10, 31, 0.6), 'vwW', 0, 1, ring='K')          # Feder
    for x, y in ((8, 9), (14, 4), (24, 20)):                           # Klangnoten
        c.form(E(x, y, 1.6, 1.3), 'FfG', 0, 1, ring='K')
        c.line([(x + 1, y), (x + 1, y - 4)], 'K', 1)
    return c


def seimei_ido():
    """Seimei-Brunnen: hölzerner Brunnenrahmen, im Wasser spiegelt sich der fünfzackige Stern, Funken steigen auf."""
    c = Cv()
    c.form(R(4, 15, 28, 28), 'jdD', 2, 1, ring='K')
    c.line([(4, 21), (28, 21)], 'j', 1)
    c.form(R(2, 13, 30, 16), 'jdD', 1, 1, ring='K')                    # Rahmen oben
    c.form(E(16, 14, 11, 2.4), 'IJO', 0, 1)
    star = [(16 + 7 * math.cos(-math.pi / 2 + k * 4 * math.pi / 5), 9 + 6 * math.sin(-math.pi / 2 + k * 4 * math.pi / 5)) for k in range(6)]
    c.line(star, 'P', 1)                                               # aufsteigender Stern
    c.fill(E(16, 9, 1.2, 1.2), 'X')
    for x, y in ((6, 6), (26, 4), (25, 11)):
        sparkle(c, x, y, 'X', 'P')
    c.form(R(13, 22, 19, 26), 'xpP', 0, 1, ring='K')                   # Kikyō-Täfelchen
    c.a[24, 16] = 'X'
    return c


def kodomo_kanabo():
    """Kinder-Kanabō: kurzer, dicker Eisenknüppel mit Nieten, rote Bänder am Griff, ein Kinder-Handabdruck."""
    c = Cv()
    club = L(8, 26, 2.2, 22, 9, 5.2)
    c.form(club, '012', 2, 1, ring='K')
    for t in (0.35, 0.55, 0.75, 0.92):                                 # Nieten
        x, y = 8 + 14 * t, 26 - 17 * t
        for d in (-2.5, 2.5):
            c.form(E(x + d * 0.7, y + d * 0.6, 1, 1), '23W', 0, 1, ring='K')
    c.form(L(8, 26, 2.6, 4, 30, 2.4), 'qrR', 0, 1, ring='K')           # Griffbänder
    c.line([(5, 27), (2, 24)], 'R', 1)
    c.form(E(25, 25, 3, 2.6), 'UVR', 0, 1)                             # Handabdruck
    for k in range(4):
        c.a[22, 23 + k] = 'V'
    return c


def ohabari():
    """Ama-no-Ōhabari: gerades Götterschwert mit Doppelschneide und Goldgriff, von Blitzketten umzuckt."""
    c = Cv()
    c.line([(3, 10), (8, 13), (5, 17), (10, 20)], 'Y', 1)            # Blitzketten
    c.line([(29, 12), (24, 15), (27, 19), (22, 22)], 'Y', 1)
    c.form(R(14, 2, 18, 22) | PG([(14, 2), (16, 0), (18, 2)]), '23W', 0, 1, ring='K')
    c.line([(16, 2), (16, 21)], 'W', 1)
    c.form(R(9, 21, 23, 24), 'ogy', 1, 1, ring='K')                    # Stichblatt
    c.form(R(14, 24, 18, 30), 'ogy', 1, 1, ring='K')                   # Goldgriff
    c.form(E(16, 30, 2.4, 1.6), 'ogY', 0, 1, ring='K')
    c.line([(16, 25), (16, 29)], 'o', 1)
    sparkle(c, 16, 6, 'W', 'Y')
    return c

NAMES = ['haraegushi', 'zanshin_tsuba', 'kuzu_blatt', 'bunbuku_kessel', 'tausendstes_schwert', 'neunter_teller',
         'tengu_tsubute', 'taizan_fukun', 'ibaraki_arm', 'yashiori_sake',
         'hi_ogi', 'muramasa', 'fuchs_trugbild', 'shigaraki_tanuki', 'tachi_ojo', 'tsurube', 'kakuremino', 'hoki_naiden',
         'masakari', 'habakiri',
         'tamagushi', 'kesagiri', 'hoshi_tama', 'tanuki_bayashi', 'gojo_giboshi', 'ido_kagami', 'sojobo_hane',
         'juni_shinsho', 'setsubun_mame', 'murakumo',
         'kotodama', 'tsubame_gaeshi', 'shinoda_blatt', 'tanuki_tokkuri', 'nanatsu_dogu', 'zehnter_teller', 'hanadaka_men',
         'kikyo_mon', 'oni_tsuno', 'kushinada_kushi',
         'onusa', 'ichi_no_tachi', 'kitsune_chochin', 'tanuki_kesa', 'kanjincho', 'okiku_ido', 'ushiwaka_fue',
         'seimei_ido', 'kodomo_kanabo', 'ohabari']


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
    out.save(sys.argv[1] if len(sys.argv) > 1 else '/tmp/v16.png')
    print(WARN)
