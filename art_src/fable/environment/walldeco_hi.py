"""Wanddekos in Hi-Res (wall_deco_hi.png, je 64x32): nur die Deko-Pixel, transparent auf der Wand.
Biome ohne eigene Hi-Res-Zeichnung nutzen wall_decos() mit doppelter Pixeldichte."""
import numpy as np
import core
from core import *
from biomes import *
from props import *


def up(base):
    """Wandstück (SS=1) als SS=2-Leinwand mit verdoppelten Pixeln."""
    o = Cv(base.w, base.h, ss=2)
    o.a = base.a.repeat(2, 0).repeat(2, 1)
    return o


def only_deco(cv, base):
    o = Cv(cv.w, cv.h, ss=2)
    m = np.any(cv.a != base.a, axis=2)
    o.a[m] = cv.a[m]
    return o


def wall_decos_hi(name, base):
    b2 = up(base)
    f = HI.get(name)
    old, core.SS = core.SS, 2
    try:
        cvs = f(name, b2) if f else wall_decos(name, b2)
    finally:
        core.SS = old
    return [only_deco(c, b2) for c in cvs]


HI = {}


# ---- Zeichenhilfen im Hi-Res-Raster (64x32, ganze Hi-Pixel)
def _g(cv):
    return np.mgrid[0:cv.h * 2, 0:cv.w * 2]


def hr(cv, x0, y0, x1, y1, c):
    cv.a[max(0, y0):y1 + 1, max(0, x0):x1 + 1] = hx(c)


def hp(cv, x, y, c):
    if 0 <= x < cv.w * 2 and 0 <= y < cv.h * 2:
        cv.a[y, x] = hx(c)


def he(cv, cx, cy, rx, ry):
    Y, X = _g(cv)
    return ((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2 <= 1.0


def hpoly(cv, pts):
    from PIL import ImageDraw
    im = Image.new('1', (cv.w * 2, cv.h * 2), 0)
    ImageDraw.Draw(im).polygon(pts, fill=1, outline=1)
    return np.array(im, dtype=bool)


def hln(cv, pts, c):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            hp(cv, int(round(x0 + (x1 - x0) * i / n)), int(round(y0 + (y1 - y0) * i / n)), c)


def hfill(cv, m, c):
    cv.a[m] = hx(c)


def edge(m):
    return dil(m) & ~m


# ---- Yashiki: Mokumokuren im zerrissenen Shōji / Schatten einer Frau hinter erleuchtetem Papier
def _eye(cv, cx, cy, w, look=0, lid=0):
    """Auge in einem Riss: zerfranster Papierrand, Lider, Iris mit Pupille."""
    hole = he(cv, cx, cy, w + 1.5, 2.7)
    hole[cy - 3, cx - w // 2] = hole[cy + 3, cx + w // 2] = hole[cy, cx + w + 2] = True   # Risszacken
    hfill(cv, edge(hole) & (cv.a[:, :, 0] > 0x40), '#7a7088')     # aufgerissene Papierfasern
    hfill(cv, hole, K)
    eye = he(cv, cx, cy, w - .5, 1.6 - lid * .5)
    hfill(cv, eye, '#c8bc94')
    hfill(cv, eye & ~np.roll(eye, -1, 0), '#8a7c62')              # Unterlid-Schatten
    ix = cx + look
    hr(cv, ix - 1, cy - 1, ix + 1, cy + 1, '#b07a20')
    hp(cv, ix + 1, cy - 1, '#e8c050')
    hp(cv, ix, cy, K)
    hp(cv, ix - 1, cy + 1, '#7a4a18')
    if lid:
        hr(cv, cx - w + 1, cy - 2, cx + w - 1, cy - 1, '#1c121c')


def yashiki_hi(name, base):
    P = BIOMES[name]
    a, b = base.copy(), base.copy()
    # A: Mokumokuren – Augen starren aus Rissen im Papier
    for (cx, cy, w, look, lid) in ((10, 15, 4, 1, 0), (20, 22, 3, -1, 1), (34, 16, 5, 0, 0),
                                   (44, 21, 3, 1, 0), (51, 15, 3, -1, 1)):
        _eye(a, cx, cy, w, look, lid)
    for x in (38, 41):                                            # Kratzspuren
        hln(a, [(x + 18, 20), (x + 20, 23)], '#2a2636')
    # B: Erleuchtete Papierwand mit dem Schatten einer Langhaarigen
    warm = ('#6a4a38', '#94704a', '#b8945a', '#d8b878')
    Y, X = _g(b)
    paper = (X >= 22) & (X <= 55) & (Y >= 13) & (Y <= 24)        # ein ganzes erleuchtetes Feld
    d = np.abs(X - 39) / 17 + np.abs(Y - 18) / 9
    for t, c in ((9, warm[1]), (.75, warm[2]), (.4, warm[3])):
        hfill(b, paper & (d < t), c)
    sil = he(b, 39, 15, 2.6, 3) | hpoly(b, [(36, 15), (42, 15), (44, 24), (34, 24)]) \
        | hpoly(b, [(33, 21), (45, 21), (48, 24), (30, 24)])
    hfill(b, edge(sil) & paper, warm[0])                          # Halbschatten am Rand
    hfill(b, sil & paper, '#2a1c22')
    for x in (37, 41):                                            # Strähnen fallen bis auf den Boden
        hln(b, [(x, 18), (x + (1 if x > 39 else -1), 24)], '#3a2628')
    hln(b, [(48, 16), (49, 17), (49, 20)], '#2a1c22')             # lange Finger am Papier
    hln(b, [(47, 16), (47, 17)], '#2a1c22')
    lat = ('#33202a', '#50302a')                                  # feines Kumiko-Gitter vor dem Licht
    for x in range(22, 56, 8):
        hr(b, x, 13, x, 24, lat[0])
    hr(b, 22, 18, 55, 18, lat[0])
    hr(b, 22, 13, 55, 13, lat[1])
    hr(b, 22, 24, 55, 24, lat[0])
    hr(b, 55, 13, 55, 24, lat[0])
    return [a, b]


HI['yashiki'] = yashiki_hi


# ---- Kawabe: Rohrkolben mit Libelle / Rinnsal-Wasserfall mit Gischt
def kawabe_hi(name, base):
    lf = BIOMES[name]['leaf']
    a, b = base.copy(), base.copy()
    for (x, top, lean) in ((7, 12, -1), (15, 6, 0), (23, 14, 1), (38, 8, -1), (46, 15, 0), (54, 10, 1)):
        hln(a, [(x, 29), (x + lean, top)], lf[0])                 # Stängel
        hr(a, x + lean - 1, top - 1, x + lean + 1, top + 5, '#4a2e22')   # Kolben
        hr(a, x + lean - 1, top - 1, x + lean - 1, top + 4, '#7a5632')
        hp(a, x + lean + 1, top + 5, '#2e1c18')
        hln(a, [(x + lean, top - 2), (x + lean, top - 4)], lf[0])
    for (x, d, h) in ((10, 3, 12), (19, -4, 10), (30, 4, 14), (42, -3, 11), (50, 3, 9)):   # Blätter
        hln(a, [(x, 29), (x + d // 2, 29 - h // 2), (x + d, 29 - h)], lf[1])
        hln(a, [(x + 1, 29), (x + d // 2 + 1, 30 - h // 2)], lf[0])
    hr(a, 28, 9, 33, 9, '#3a66a8')                                # Libelle (Tonbo)
    hp(a, 34, 9, '#7ab0d8')
    for (wx, wy) in ((29, 7), (31, 7), (29, 11), (31, 11)):
        hln(a, [(30, 9), (wx, wy)], '#a8c8d8')
    # B: Rinnsal in einer moosigen Felsnische
    Y, X = _g(b)
    niche_m = (X >= 22) & (X <= 41) & (Y >= 10) & (Y <= 28) & ~((Y == 10) & ((X == 22) | (X == 41)))
    hfill(b, niche_m, '#0a1018')
    water = (X >= 25) & (X <= 38) & (Y >= 10) & (Y <= 28)
    hfill(b, water, WATER[1])
    for x in range(25, 39):                                       # Strömungsstreifen
        ph = (x * 7) % 5
        for y in range(10 + ph, 28, 5):
            hr(b, x, y, x, y + 1, WATER[2] if x % 3 else WATER[3])
    hr(b, 26, 10, 26, 27, WATER[3])
    hr(b, 37, 10, 37, 27, WATER[0])
    hfill(b, he(b, 31.5, 29, 11, 2.5) & (Y >= 27), WATER[2])      # Becken mit Gischt
    for (x, y) in ((22, 27), (25, 26), (29, 27), (33, 26), (36, 27), (40, 26), (20, 25), (43, 25)):
        hp(b, x, y, '#c8e0f0')
    hr(b, 27, 28, 36, 28, '#a8d0e8')
    for x in range(21, 43):                                       # Moos am Nischenrand
        hp(b, x, 9 + (x % 3 == 0), MOSS[2] if x % 2 else MOSS[1])
    hr(b, 21, 10, 21, 16, MOSS[1])
    hr(b, 42, 10, 42, 13, MOSS[1])
    return [a, b]


HI['kawabe'] = kawabe_hi


# ---- Ōeyama: Schädel auf Pfählen und Kanabō / vergitterte Höhle mit Oni-Augen
def _skull(cv, cx, cy):
    m = he(cv, cx, cy, 5, 4.5) | ((_g(cv)[1] >= cx - 3) & (_g(cv)[1] <= cx + 3) & (_g(cv)[0] >= cy) & (_g(cv)[0] <= cy + 6))
    hfill(cv, edge(m), K)
    hfill(cv, m, BONE[2])
    hfill(cv, m & ~np.roll(m, -2, 0), BONE[1])                   # Schatten unten
    hfill(cv, m & ~np.roll(m, 1, 0) & ~np.roll(m, 1, 1), BONE[3])
    for sx in (-2, 2):
        hr(cv, cx + sx - 1, cy, cx + sx, cy + 2, K)
    hp(cv, cx, cy + 3, K)
    for x in range(cx - 2, cx + 3, 2):
        hp(cv, x, cy + 6, K)
    hln(cv, [(cx + 1, cy - 4), (cx + 2, cy - 2)], BONE[1])       # Riss in der Schädeldecke


def oeyama_hi(name, base):
    a, b = base.copy(), base.copy()
    wd = ('#1c121c', '#3a2428', '#58382c', '#7a5038')
    for (x, top) in ((11, 8), (49, 11)):
        hr(a, x - 1, top + 6, x + 1, 29, wd[2])                   # Pfahl
        hr(a, x + 1, top + 6, x + 1, 29, wd[1])
        hr(a, x - 1, top + 12, x + 1, top + 13, STRAW[2])         # Strohbindung
        _skull(a, x, top)
    kb = hpoly(a, [(25, 29), (30, 7), (38, 7), (36, 29)])         # Kanabō am Fels
    hfill(a, edge(kb), K)
    hfill(a, kb, IRON[1])
    Y, X = _g(a)
    hfill(a, kb & ~np.roll(kb, 2, 1), IRON[2])                    # Lichtkante links
    hfill(a, kb & ~np.roll(kb, -2, 1), IRON[0])
    for (x, y) in ((31, 10), (35, 12), (30, 15), (34, 17), (29, 20), (33, 22)):   # Eisenstacheln
        hp(a, x, y, IRON[3])
        hp(a, x + 1, y + 1, K)
    hr(a, 26, 25, 36, 27, '#6a1c1c')                              # rote Griffwicklung
    hln(a, [(26, 25), (36, 27)], '#9a2a2a')
    # B: vergitterte Höhle, darin glühende Oni-Augen und Hörner
    Y, X = _g(b)
    cave = he(b, 32, 30, 19, 18) & (Y >= 11) & (Y <= 29)
    hfill(b, edge(cave) & (Y >= 10), '#56362e')
    hfill(b, cave, K)
    for sx in (-1, 1):                                            # Hörner im Dunkel
        hln(b, [(32 + sx * 6, 17), (32 + sx * 8, 14), (32 + sx * 8, 12)], '#4a2a2c')
    for ex in (26, 36):
        hr(b, ex, 19, ex + 2, 20, '#ff5a3c')
        hp(b, ex + 1, 19, '#ffd080')
        hp(b, ex - 1, 20, '#8a1c1a')
        hp(b, ex + 3, 20, '#8a1c1a')
    hr(b, 28, 24, 36, 24, '#3a1414')                              # gefletschte Zähne
    for x in range(29, 36, 2):
        hp(b, x, 25, BONE[2])
    for x in (17, 23, 31, 40, 46):                                # Gitterstäbe mit Nieten
        hfill(b, cave & (X >= x) & (X <= x + 1), IRON[2])
        hfill(b, cave & (X == x + 1), IRON[0])
        hp(b, x, 16, IRON[3])
    hfill(b, cave & (Y >= 15) & (Y <= 16), IRON[1])
    hfill(b, cave & (Y == 15), IRON[2])
    return [a, b]


HI['oeyama'] = oeyama_hi


# ---- Shinkai: Chōchin-anko im Felsloch / leuchtender Anemonengarten mit Qualle
def shinkai_hi(name, base):
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    hole = he(a, 31, 20, 19, 9)
    hfill(a, edge(hole), '#22304a')
    hfill(a, hole, K)
    jaw = hpoly(a, [(17, 22), (44, 19), (46, 25), (20, 27)])      # Unterkiefer, kaum sichtbar
    hfill(a, jaw & hole, '#11192b')
    hfill(a, edge(jaw) & hole & (Y < 23), '#22304a')
    for i, x in enumerate(range(20, 44, 3)):                      # Nadelzähne oben und unten
        hln(a, [(x, 21 - (i % 2)), (x + 1, 24)], WHITE[2])
        hp(a, x + 1, 25, WHITE[1])
    hr(a, 19, 17, 22, 19, '#c8ee78')                              # bleiches Auge
    hp(a, 21, 18, K)
    hp(a, 19, 17, '#f0ffc0')
    hln(a, [(27, 13), (32, 9), (38, 8), (43, 10)], '#3a5470')     # Angel
    hfill(a, he(a, 44, 12, 2.2, 2.2), '#ffe24a')                  # Leuchtköder mit Hof
    hfill(a, edge(he(a, 44, 12, 2.2, 2.2)) & ~hole, '#7a7a30')
    hp(a, 43, 11, '#fffbc0')
    for (x, top, h) in ((10, 14, 1), (19, 10, -1), (29, 16, 1), (39, 12, -1), (49, 15, 1)):
        for k in range(3):                                        # Stiele mit Leuchtringen
            hln(b, [(x + k, 29), (x + k + h, top + 3)], GLOW[k])
        cx = x + 1 + h
        hfill(b, he(b, cx, top + 3, 2.5, 1.5), GLOW[2])           # Mundscheibe
        for (dx, dy) in ((-5, 1), (-4, -2), (-2, -4), (0, -5), (2, -4), (4, -2), (5, 1)):   # Tentakelkrone
            hln(b, [(cx, top + 2), (cx + dx * 2 // 3, top + 2 + dy * 2 // 3), (cx + dx, top + 2 + dy)], GLOW[2])
            hp(b, cx + dx, top + 2 + dy, GLOW[3])
    jel = he(b, 56, 9, 3.5, 2.5) & (_g(b)[0] <= 9)                # kleine Qualle
    hfill(b, jel, '#6a4a9a')
    hfill(b, jel & (_g(b)[0] <= 7), '#b090e0')
    for x in (54, 56, 58):
        hln(b, [(x, 10), (x + (1 if x > 56 else 0), 14)], '#8a6ab8')
    return [a, b]


# ---- Enma-chō: Jōhari no Kagami mit Seelenbild / Kohlebecken an Ketten
def enma_hi(name, base):
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    m = he(a, 31.5, 18, 10, 8.5)
    ring = he(a, 31.5, 18, 12.5, 11) & ~m
    hfill(a, edge(ring | m), K)
    hfill(a, ring, GOLD[2])
    hfill(a, ring & (Y > 20), GOLD[1])
    hfill(a, ring & (Y < 12), GOLD[3])
    for ang in range(0, 360, 30):                                 # Flammenzacken im Rahmen
        import math
        x = int(round(31.5 + 12 * math.cos(math.radians(ang))))
        y = int(round(18 + 10.5 * math.sin(math.radians(ang))))
        hp(a, x, y, LAVA[3] if y < 18 else GOLD[0])
    hfill(a, m, WHITE[0])
    hfill(a, m & (X + Y < 46), WHITE[1])
    soul = he(a, 33, 15, 2.5, 2.5) | hpoly(a, [(30, 17), (36, 17), (38, 25), (28, 25)])
    hfill(a, soul & m, '#8a3a4a')                                 # gespiegelte Sünderseele
    hp(a, 32, 15, '#ffd0a0')
    hp(a, 34, 15, '#ffd0a0')
    hln(a, [(25, 19), (31, 12)], WHITE[3])                        # Glanz
    hln(a, [(28, 22), (33, 16)], WHITE[2])
    hr(a, 26, 29, 37, 30, GOLD[0])                                # Sockel
    hr(a, 29, 28, 34, 28, GOLD[1])
    # B: Kohlebecken an zwei Ketten
    for x in (21, 42):
        for y in range(9, 19):
            hp(b, x + (y % 2), y, IRON[2] if y % 2 else IRON[1])
    bowl = hpoly(b, [(20, 19), (43, 19), (40, 25), (23, 25)])
    hfill(b, edge(bowl), K)
    hfill(b, bowl, IRON[1])
    hfill(b, bowl & (Y == 19), IRON[3])
    hfill(b, bowl & (Y >= 23), IRON[0])
    for x in range(24, 40, 4):
        hp(b, x, 21, IRON[3])
    hr(b, 29, 26, 34, 28, IRON[1])                                # Fuß
    fl = hpoly(b, [(22, 19), (25, 11), (27, 15), (30, 6), (33, 13), (36, 8), (38, 14), (41, 19)])
    hfill(b, fl, LAVA[1])
    hfill(b, fl & ~np.roll(fl, 2, 0) | (fl & (Y >= 16)), LAVA[2])
    inner = hpoly(b, [(26, 19), (29, 13), (31, 16), (33, 11), (35, 15), (37, 19)])
    hfill(b, inner, LAVA[3])
    hfill(b, inner & (Y >= 17), '#ffe8a0')
    for (x, y) in ((24, 7), (35, 4), (40, 9)):                    # Funken
        hp(b, x, y, LAVA[3])
    return [a, b]


# ---- Tsukiyomi: Vollmondfenster mit Mochi-Hase / Mondsichel-Wappen mit Suzu
def tsukiyomi_hi(name, base):
    s = SILVER
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    m = he(a, 31.5, 18.5, 11, 9.5)
    hfill(a, edge(edge(m)), K)
    hfill(a, edge(m), s[1])
    hfill(a, m, '#c8d0e0')
    hfill(a, m & ~np.roll(np.roll(m, -1, 1), -1, 0), s[2])       # Schatten unten rechts
    for (cx, cy, r) in ((26, 15, 1.5), (36, 22, 2), (34, 13, 1)):   # Mondmeere
        hfill(a, he(a, cx, cy, r, r) & m, '#a8b4c8')
    rab = he(a, 27.5, 22, 4, 3.5) | he(a, 24, 17.5, 2.6, 2.3) \
        | hpoly(a, [(23, 16), (25, 8), (27, 9), (25, 16)]) | hpoly(a, [(25, 16), (29, 10), (30, 11), (26, 17)])
    hfill(a, rab & m, '#343c5c')                                  # Hase mit langen Ohren
    hp(a, 23, 17, '#c8d0e0')
    usu = hpoly(a, [(33, 22), (40, 22), (39, 27), (34, 27)])       # Mörser
    hfill(a, usu & m, s[0])
    hfill(a, he(a, 36.5, 21.5, 3, 1.3) & m, '#f4f4fa')             # Mochi
    hln(a, [(29, 19), (34, 15)], s[0])                             # Stößel (Kine)
    hln(a, [(30, 19), (35, 15)], s[0])
    hr(a, 33, 13, 37, 15, s[0])
    # B: Mondsichel-Wappen zwischen zwei Suzu an roten Schnüren
    cres = he(b, 32, 18, 9, 9) & ~he(b, 36.5, 16, 8, 8)
    hfill(b, edge(cres), s[0])
    hfill(b, cres, '#d8dcec')
    hfill(b, cres & (X + Y > 50), s[2])
    for x in (12, 51):
        hr(b, x, 9, x, 19, RED[2])
        hp(b, x + 1, 12, RED[3])
        bell = he(b, x, 22, 2.5, 2.5)
        hfill(b, edge(bell), K)
        hfill(b, bell, GOLD[2])
        hp(b, x - 1, 21, GOLD[3])
        hr(b, x - 1, 23, x + 1, 23, GOLD[0])
        hp(b, x, 25, K)
    return [a, b]


HI.update(shinkai=shinkai_hi, enma_cho=enma_hi, tsukiyomi=tsukiyomi_hi)


# ---- Jigoku: Lavafall aus einer Felsspalte / Ketten mit Fußfesseln und Eisenegge
def jigoku_hi(name, base):
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    crack = hpoly(a, [(27, 9), (31, 11), (36, 8), (39, 12), (37, 27), (26, 27), (24, 13)])
    hfill(a, edge(crack), K)
    hfill(a, crack, LAVA[0])
    fall = crack & (X >= 28) & (X <= 35) & (Y >= 11)
    hfill(a, fall, LAVA[1])
    for x in range(28, 36):                                       # fließende Glutstreifen
        for y in range(11 + (x * 5) % 4, 27, 4):
            hr(a, x, y, x, y + 1, LAVA[2] if x % 2 else LAVA[3])
    hr(a, 31, 11, 32, 26, LAVA[3])
    hr(a, 31, 13, 31, 22, '#ffe8a0')
    for (x, y) in ((26, 12), (25, 16), (38, 14), (37, 19)):       # glühende Ränder
        hp(a, x, y, LAVA[2])
    pool = he(a, 32, 28, 12, 3) & (Y >= 26)
    hfill(a, edge(pool) & (Y >= 25), K)
    hfill(a, pool, LAVA[2])
    hfill(a, pool & he(a, 32, 28, 7, 1.5), LAVA[3])
    hr(a, 30, 27, 34, 27, '#ffe8a0')
    for (x, y) in ((22, 23), (25, 20), (40, 21), (43, 24), (29, 6), (36, 5)):   # Funken
        hp(a, x, y, LAVA[3])
    # B: zwei Ketten mit Fußfesseln, dazwischen eine Eisenegge mit blutigen Zinken
    for x in (14, 49):
        for y in range(8, 22, 3):                                 # Kettenglieder abwechselnd quer/hochkant
            if (y // 3) % 2:
                hr(b, x - 1, y, x + 1, y, IRON[3]); hr(b, x - 1, y + 2, x + 1, y + 2, IRON[1])
                hp(b, x - 1, y + 1, IRON[2]); hp(b, x + 1, y + 1, IRON[2])
            else:
                hr(b, x, y, x, y + 2, IRON[2]); hp(b, x, y, IRON[3])
        ring = he(b, x, 25, 3.5, 3) & ~he(b, x, 25, 1.8, 1.4)
        hfill(b, edge(ring | he(b, x, 25, 1.8, 1.4)), K)
        hfill(b, ring, IRON[1])
        hfill(b, ring & (Y <= 24), IRON[3])
        hp(b, x, 28, IRON[0])
    bar = (X >= 21) & (X <= 42) & (Y >= 9) & (Y <= 12)
    hfill(b, edge(bar), K)
    hfill(b, bar, IRON[1])
    hr(b, 21, 9, 42, 9, IRON[3])
    hr(b, 21, 12, 42, 12, IRON[0])
    for x in (23, 40):
        hp(b, x, 10, GOLD[2])                                     # Nieten
    for x in range(23, 42, 4):                                    # Zinken
        sp = hpoly(b, [(x, 13), (x + 2, 13), (x + 1, 22)])
        hfill(b, edge(sp) & (Y >= 13), K)
        hfill(b, sp, IRON[2])
        hr(b, x, 13, x, 18, IRON[3])
        hr(b, x + 1, 19, x + 1, 21, '#7a1622')                    # Blut an der Spitze
    hr(b, 31, 3, 32, 8, IRON[2])                                  # Aufhängung
    return [a, b]


# ---- Iwato: gedrehtes Shimenawa mit Shide / Kagaribi-Feuerkorb der wartenden Götter
def iwato_hi(name, base):
    import math
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    for x in range(3, 61):
        t = (x - 3) / 57
        yc = 9 + 6 * math.sin(math.pi * t)
        th = 4 - abs(t - .5) * 2                                  # in der Mitte dicker
        for y in range(int(yc - th), int(yc + th) + 1):
            tw = (x + y * 2) % 6                                  # Drehung: schräge Strohbündel
            c = STRAW[3] if tw < 2 else STRAW[2] if tw < 4 else STRAW[1]
            if y in (int(yc - th), int(yc + th)):
                c = STRAW[0] if y == int(yc + th) else c
            hp(a, x, y, c)
        hp(a, x, int(yc - th) - 1, K)
        hp(a, x, int(yc + th) + 1, K)
    for (x, ln) in ((14, 7), (32, 9), (50, 7)):                   # Shide: Blitz-Zickzack aus Papier
        yc = int(9 + 6 * math.sin(math.pi * (x - 3) / 57)) + 4
        for i in range(ln):
            sx = x + (2 if (i // 2) % 2 else 0)
            hr(a, sx, yc + i * 2, sx + 3, yc + i * 2 + 1, PAPER[3] if i % 2 == 0 else PAPER[2])
            hp(a, sx + 3, yc + i * 2 + 1, PAPER[1])
    for x in (23, 41):                                            # Strohquasten (Kazari)
        yc = int(9 + 6 * math.sin(math.pi * (x - 3) / 57)) + 4
        for dx in range(-1, 2):
            hr(a, x + dx, yc, x + dx, yc + 5 + (dx == 0), STRAW[2] if dx else STRAW[3])
    # B: Kagaribi auf drei Beinen in einer Felsnische, Licht bei (30, 12)
    nm = (X >= 20) & (X <= 43) & (Y >= 6) & (Y <= 29) & ~(((X == 20) | (X == 43)) & (Y == 6))
    hfill(b, nm, K)
    hfill(b, nm & (Y >= 18) & (abs(X - 31.5) < 9), '#2a1410')       # Feuerschein auf dem Fels
    for (x0, x1) in ((24, 27), (39, 36), (31, 31)):               # Beine
        hln(b, [(x0, 29), (x1, 20)], IRON[2])
    basket = hpoly(b, [(23, 13), (40, 13), (37, 20), (26, 20)])
    hfill(b, edge(basket), IRON[0])
    hfill(b, basket, '#1c1418')
    for x in range(24, 40, 3):                                    # Eisenkorb-Streben
        hln(b, [(x, 13), (x + (1 if x < 31 else -1), 20)], IRON[2])
    hr(b, 23, 13, 40, 13, IRON[3])
    hr(b, 25, 17, 38, 17, IRON[1])
    for x in range(25, 39, 3):                                    # Glut zwischen den Streben
        hp(b, x + 1, 15, LAVA[2]); hp(b, x + 2, 18, LAVA[1])
    fl = hpoly(b, [(24, 13), (26, 7), (28, 10), (30, 2), (33, 9), (35, 5), (37, 10), (39, 13)])
    hfill(b, fl, LAVA[2])
    hfill(b, hpoly(b, [(27, 13), (29, 8), (31, 5), (33, 10), (36, 13)]), LAVA[3])
    hfill(b, hpoly(b, [(29, 13), (31, 8), (34, 13)]), SUN[3])
    for (x, y) in ((25, 3), (36, 1), (40, 6), (22, 8)):           # Funken
        hp(b, x, y, SUN[3])
    return [a, b]


# ---- Yomi no Oku: zerschlissene Misu mit herausgreifender Hand / Tōrō mit kaltem Totenfeuer
def yomi_oku_hi(name, base):
    v = VIOLET
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    blind = (X >= 10) & (X <= 53) & (Y >= 10) & (Y <= 27)
    hfill(a, blind, v[2])
    hfill(a, blind & (Y % 3 == 0), v[1])                          # Bambusstreifen
    hfill(a, blind & (Y % 3 == 1) & (X % 7 == 0), v[3])
    for x in (18, 31, 45):                                        # Bindeschnüre
        hfill(a, blind & (X == x), v[0])
    hr(a, 8, 7, 55, 9, GOLD[1])                                   # Brokatsaum
    hr(a, 8, 7, 55, 7, GOLD[2])
    for x in range(10, 55, 4):
        hp(a, x, 8, RED[2])
    hr(a, 8, 6, 55, 6, K)
    tear = hpoly(a, [(34, 17), (41, 15), (49, 18), (47, 28), (38, 28), (36, 22)])
    hfill(a, tear & blind, K)
    for (x, y) in ((35, 18), (40, 16), (48, 20), (37, 25)):       # Fransen
        hp(a, x, y, v[3])
    hand = hpoly(a, [(38, 28), (40, 22), (44, 21), (45, 28)])     # bleiche Hand aus dem Riss
    for fx in (39, 41, 43, 45):
        hand |= (X == fx) & (Y >= 17 + abs(fx - 42) // 2) & (Y <= 22)
    hfill(a, edge(hand) & tear, '#1a1424')
    hfill(a, hand, '#b8b0c0')
    hfill(a, hand & (X >= 44), '#8a8098')
    for fx in (39, 41, 43, 45):
        hp(a, fx, 17 + abs(fx - 42) // 2, '#5a4a62')              # dunkle Nägel
    hr(a, 18, 10, 18, 22, RED[1])                                 # Quaste
    hfill(a, hpoly(a, [(16, 23), (20, 23), (21, 28), (15, 28)]), RED[2])
    hr(a, 16, 23, 20, 24, GOLD[2])
    hr(a, 17, 25, 17, 28, RED[3])
    # B: hängende Tōrō mit kaltem Totenfeuer in einer Nische, Licht bei (30, 18)
    nm = (X >= 20) & (X <= 42) & (Y >= 10) & (Y <= 29) & ~(((X == 20) | (X == 42)) & (Y == 10))
    hfill(b, nm, K)
    hr(b, 30, 4, 31, 9, IRON[1])                                  # Haken
    roof = hpoly(b, [(23, 13), (31, 8), (38, 13), (36, 14), (25, 14)])
    hfill(b, edge(roof), K)
    hfill(b, roof, IRON[1])
    hln(b, [(23, 13), (31, 8), (38, 13)], IRON[3])
    hp(b, 22, 12, IRON[2]); hp(b, 39, 12, IRON[2])                # aufgebogene Traufen
    cage = (X >= 25) & (X <= 36) & (Y >= 15) & (Y <= 24)
    hfill(b, cage, IRON[0])
    glow = (X >= 26) & (X <= 35) & (Y >= 16) & (Y <= 23)
    hfill(b, glow, ONIBI[1])
    hfill(b, he(b, 30.5, 20, 4, 3.5), ONIBI[2])
    flm = hpoly(b, [(28, 23), (29, 18), (30, 19), (31, 15), (32, 19), (33, 17), (33, 23)])
    hfill(b, flm, ONIBI[3])
    hr(b, 30, 20, 31, 23, '#f4f0ff')
    for x in (28, 33):                                            # Gitterstäbe
        hfill(b, cage & (X == x), IRON[0])
    hfill(b, cage & (Y == 19), IRON[0])
    hr(b, 24, 25, 37, 26, IRON[2])                                # Boden mit Fuß
    hr(b, 24, 25, 37, 25, IRON[3])
    hr(b, 29, 27, 32, 28, IRON[1])
    for (x, y) in ((24, 18), (38, 21), (26, 28), (36, 11)):       # Seelenfunken
        hp(b, x, y, ONIBI[2])
    return [a, b]


HI.update(jigoku=jigoku_hi, iwato=iwato_hi, yomi_oku=yomi_oku_hi)


def _niche(cv, x0, x1, y0, c=K):
    """Dunkle Nische bis zum Wandfuß, oben mit abgerundeten Ecken."""
    hr(cv, x0, y0, x1, 29, c)
    cv.a[y0, x0] = cv.a[y0, x0 - 1]; cv.a[y0, x1] = cv.a[y0, x1 + 1]


# ---- Chikurin: Taketori – leuchtendes Bambusrohr mit der kleinen Kaguya / Ishidōrō in der Nische
def chikurin_hi(name, base):
    a, b = base.copy(), base.copy()
    lf = BIOMES[name]['leaf']
    bam = ('#0e2418', '#1e4a2a', '#3a7a3a', '#7ab060')
    Y, X = _g(a)
    # A: dickes Rohr vorn, schräg angeschnitten, das untere Glied leuchtet golden
    hr(a, 26, 4, 35, 29, bam[1])
    hr(a, 27, 4, 28, 29, bam[2]); hr(a, 27, 4, 27, 29, bam[3])
    hr(a, 35, 4, 35, 29, bam[0])
    for y in (4, 26):                                             # Knoten
        hr(a, 25, y, 36, y + 1, bam[0]); hr(a, 26, y, 34, y, bam[2])
    cut = hpoly(a, [(26, 12), (35, 8), (35, 25), (26, 25)])       # angeschnittenes Glied
    hfill(a, cut, '#8a5a18')
    glow = he(a, 30.5, 19, 4.5, 6) & cut
    hfill(a, glow, '#e8b040')
    hfill(a, he(a, 30.5, 20, 2.8, 4) & cut, '#ffe890')
    hln(a, [(26, 12), (35, 8)], '#fff4c0')                       # Schnittkante
    hln(a, [(26, 13), (35, 9)], bam[3])
    hfill(a, he(a, 30.5, 17.5, 1.1, 1.1), '#2a1a18')             # Kaguya: Kopf mit Haar
    hr(a, 29, 19, 32, 23, '#b03030'); hr(a, 30, 19, 31, 23, '#e05040')   # Jūnihitoe in Rot
    hr(a, 29, 18, 29, 22, '#2a1a18')                              # langes Haar am Rücken
    hp(a, 31, 17, '#f0e0d0')
    for (x, y) in ((24, 10), (38, 14), (22, 20), (40, 7), (37, 22)):   # Lichtfunken
        hp(a, x, y, '#fff4c0')
    for (x, y, d) in ((36, 6, 1), (25, 6, -1), (36, 24, 1)):       # Blätter
        hln(a, [(x, y), (x + d * 3, y - 1), (x + d * 7, y + 1)], lf[1])
        hln(a, [(x + d, y + 1), (x + d * 5, y + 2)], lf[0])
    # B: Ishidōrō in einer Lücke zwischen den Rohren, Licht bei (32, 20)
    _niche(b, 18, 45, 12)
    s = ('#191a28', '#2e3044', '#4a4e66', '#70768e')
    hr(b, 28, 26, 36, 29, s[1]); hr(b, 28, 26, 36, 26, s[2])     # Sockel
    hr(b, 30, 23, 34, 25, s[2]); hr(b, 30, 23, 30, 25, s[3])     # Schaft
    hr(b, 27, 22, 37, 22, s[2])
    hr(b, 28, 17, 36, 21, s[1]); hr(b, 28, 17, 28, 21, s[3])     # Feuerkammer
    hr(b, 30, 18, 34, 20, '#d8961a'); hr(b, 31, 18, 33, 19, '#ffe24a'); hp(b, 32, 18, '#fffbc0')
    hfill(b, hpoly(b, [(24, 16), (40, 16), (36, 13), (28, 13)]), s[2])   # Dach
    hr(b, 24, 16, 40, 16, s[1]); hln(b, [(28, 13), (36, 13)], s[3])
    hr(b, 31, 10, 33, 12, s[2]); hp(b, 32, 9, s[3])                # Hōju
    for (x, y) in ((28, 27), (29, 26), (35, 26), (36, 28), (24, 16), (39, 16)):   # Moos
        hp(b, x, y, MOSS[2])
    hln(b, [(18, 28), (22, 25), (24, 29)], lf[0])                # Farn am Nischenrand
    hln(b, [(45, 28), (42, 24), (40, 29)], lf[1])
    return [a, b]


HI['chikurin'] = chikurin_hi


# ---- Inari: Torii vor dem Senbon-Torii-Gang / Steinfuchs mit Speicherschlüssel und rotem Lätzchen
def _torii(cv, x0, x1, y0, h, c, dark):
    hr(cv, x0, y0, x1, y0 + 1, dark)                              # Kasagi, Enden geschwungen
    hp(cv, x0 - 1, y0 - 1, dark); hp(cv, x1 + 1, y0 - 1, dark)
    hr(cv, x0 + 1, y0 + 2, x1 - 1, y0 + 3, c[2]); hr(cv, x0 + 1, y0 + 2, x1 - 1, y0 + 2, c[3])
    w = x1 - x0
    for px in (x0 + w // 6, x1 - w // 6 - 2):
        hr(cv, px, y0 + 4, px + 2, y0 + h, c[2]); hr(cv, px, y0 + 4, px, y0 + h, c[3])
        hr(cv, px + 2, y0 + 4, px + 2, y0 + h, c[1]); hr(cv, px, y0 + h - 1, px + 2, y0 + h, dark)
    hr(cv, x0 + 2, y0 + 7, x1 - 2, y0 + 8, c[2]); hr(cv, x0 + 2, y0 + 8, x1 - 2, y0 + 8, c[1])   # Nuki


def inari_hi(name, base):
    a, b = base.copy(), base.copy()
    dark = '#16121e'
    _niche(a, 18, 45, 10, '#0c0812')
    for w, top, c in ((3, 20, '#3a0e20'), (5, 18, '#4e1222'), (7, 16, '#6a1a26'), (9, 14, '#86222a')):   # Senbon-Torii-Gang
        for x in (31 - w, 32 + w):
            hr(a, x, top, x, 29, c)
        hr(a, 30 - w, top, 33 + w, top, c)
        hr(a, 31 - w, top + 2, 32 + w, top + 2, c)
    _torii(a, 6, 57, 1, 28, ('#3a0e2a', '#6e1a2c', '#b8322a', '#e05a38'), dark)
    hr(a, 29, 6, 34, 9, dark); hr(a, 30, 7, 33, 8, GOLD[2]); hp(a, 31, 7, GOLD[3])   # Gakuzuka mit Tafel
    for (x, y) in ((31, 27), (33, 25), (32, 22)):                 # Fuchsfeuer tief im Gang
        hp(a, x, y, '#5ab0c8')
    # B: Kitsune-Statue auf Sockel, Schlüssel im Maul, rotes Lätzchen
    _niche(b, 16, 47, 10)
    s = ('#191a28', '#3a3c54', '#5c627e', '#8a90a8')
    hr(b, 22, 26, 41, 29, s[1]); hr(b, 22, 26, 41, 26, s[2]); hr(b, 22, 29, 41, 29, s[0])
    fox = hpoly(b, [(26, 25), (27, 17), (29, 13), (30, 9), (32, 13), (34, 15), (36, 18), (37, 25)]) \
        | he(b, 30.5, 12, 3.2, 2.6) | hpoly(b, [(28, 10), (29, 5), (31, 9)]) | hpoly(b, [(31, 9), (33, 5), (33, 10)])
    tail = hpoly(b, [(36, 24), (40, 20), (41, 14), (43, 10), (44, 15), (42, 22), (38, 25)])
    hfill(b, edge(fox | tail), K)
    hfill(b, fox | tail, s[2])
    hfill(b, (fox | tail) & ~np.roll(fox | tail, -1, 1), s[1])   # Schatten rechts
    hfill(b, (fox | tail) & ~np.roll(fox | tail, 1, 1), s[3])    # Licht links
    hfill(b, he(b, 43, 11, 1.5, 1.5) & tail, '#d0d4e0')          # Schwanzspitze (Hōju)
    hr(b, 26, 13, 27, 14, s[2]); hp(b, 25, 14, K)                 # Schnauze
    hp(b, 29, 11, '#c03030'); hp(b, 30, 11, K)                    # Auge mit rotem Lid
    hr(b, 22, 14, 26, 14, GOLD[1]); hr(b, 21, 13, 22, 15, GOLD[2]); hp(b, 21, 13, GOLD[3])   # Kagi im Maul
    bib = hpoly(b, [(27, 15), (34, 16), (31, 21)])
    hfill(b, bib, RED[2]); hfill(b, bib & ~np.roll(bib, -1, 0), RED[1]); hr(b, 27, 15, 34, 15, RED[3])
    hr(b, 27, 22, 28, 25, s[3]); hr(b, 33, 23, 34, 25, s[1])     # Vorderpfoten
    return [a, b]


HI['inari'] = inari_hi


# ---- Obakedera: Ofuda mit Pinselzeichen, einer halb abgerissen / Yūrei-ga – Rollbild einer Geisterfrau
def obakedera_hi(name, base):
    a, b = base.copy(), base.copy()
    pap = ('#4a4a64', '#8a8ca4', '#c4c6d4', '#e4e4ea')
    ink, red = '#1a1420', '#a82a2a'
    for i, (x, y, h, torn) in enumerate(((8, 11, 13, 0), (20, 13, 11, 0), (33, 9, 15, 1), (47, 12, 12, 0))):
        if torn:                                                  # schräg hängend, eine Ecke flattert
            m = hpoly(a, [(x, y), (x + 6, y + 1), (x + 9, y + h), (x + 3, y + h + 1)])
        else:
            m = (_g(a)[1] >= x) & (_g(a)[1] <= x + 6) & (_g(a)[0] >= y) & (_g(a)[0] <= y + h)
        hfill(a, edge(m) & (_g(a)[0] > y), '#0a0814')            # Schlagschatten
        hfill(a, m, pap[2])
        hfill(a, m & ~np.roll(m, -1, 1), pap[1])
        hfill(a, m & ~np.roll(m, 1, 1), pap[3])
        ox = 2 if torn else 0
        hr(a, x + 2 + ox // 2, y + 2, x + 4 + ox // 2, y + 2, ink)   # Pinselzeichen
        hln(a, [(x + 3 + ox // 2, y + 3), (x + 3 + ox, y + h - 4)], ink)
        hln(a, [(x + 2 + ox // 2, y + 5), (x + 4 + ox // 2, y + 6)], ink)
        hr(a, x + 2 + ox, y + h - 3, x + 4 + ox, y + h - 2, red)  # Siegelstempel
        hp(a, x + 3, y, '#5a5a6a')                                # Nagel
    hln(a, [(43, 24), (45, 26), (44, 28)], pap[2])                # abgerissene Ecke weht davon
    # B: Hängerolle mit Geisterfrau, unten ohne Füße in Nebel verblassend
    hr(b, 20, 5, 43, 6, '#3a2418'); hr(b, 19, 5, 19, 6, '#1a1010'); hr(b, 44, 5, 44, 6, '#1a1010')
    hln(b, [(31, 5), (31, 2)], '#6a5040')
    hr(b, 21, 7, 42, 27, '#5a4a3a')                               # Brokatrand
    hr(b, 23, 8, 40, 26, '#c8c0a8'); hr(b, 23, 8, 23, 26, '#a89e88')
    hr(b, 20, 28, 43, 29, '#3a2418')
    Y, X = _g(b)
    body = hpoly(b, [(29, 12), (34, 12), (36, 18), (35, 23), (28, 23), (27, 18)])
    hfill(b, body & (Y < 20), '#e8e8ee')                          # weißes Totengewand
    hfill(b, body & (Y >= 20) & ((X + Y) % 2 == 0), '#d8d6d8')    # verblasst nach unten
    hln(b, [(31, 13), (33, 17), (32, 19)], '#9a98a8')             # Kragen links über rechts
    hfill(b, he(b, 31.5, 11, 2.4, 2.4), '#e8e4e0')                # Gesicht
    hp(b, 30, 11, ink); hp(b, 33, 11, ink); hr(b, 31, 13, 32, 13, '#7a5a6a')
    for (x0, x1) in ((28, 28), (35, 35), (27, 27), (36, 36)):     # langes offenes Haar
        hln(b, [(29 if x0 < 31 else 34, 8), (x0, 14), (x0 + (1 if x0 < 31 else -1), 22)], ink)
    hr(b, 29, 8, 34, 9, ink)
    hln(b, [(28, 16), (25, 19), (26, 20)], '#e8e8ee')             # hängende Hände
    hln(b, [(35, 16), (37, 18)], '#e8e8ee')
    for (x, y) in ((25, 24), (38, 23), (30, 25), (34, 25)):       # Nebel
        hr(b, x - 1, y, x + 2, y, '#b0aaa0')
    hr(b, 38, 24, 39, 25, red)                                    # Künstlersiegel
    return [a, b]


HI['obakedera'] = obakedera_hi
