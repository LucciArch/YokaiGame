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


# ---- Hakaba: Sotoba mit Bonji und Higanbana / Jizō mit rotem Lätzchen und Mütze, Kerze und Steinhäufchen
def _higanbana(cv, x, y):
    """Rote Totenblume: Stängel, sechs gebogene Blütenblätter mit langen Staubfäden."""
    hln(cv, [(x, 29), (x, y + 2)], '#2e5a2a')
    for dx, dy in ((-3, -1), (-2, -3), (0, -4), (2, -3), (3, -1), (0, 1)):
        hln(cv, [(x, y), (x + dx, y + dy)], '#c82a2a')
        hp(cv, x + dx + (1 if dx > 0 else -1 if dx < 0 else 0), y + dy - 1, '#ff6a4a')
    hp(cv, x, y, '#7a1018')


def hakaba_hi(name, base):
    a, b = base.copy(), base.copy()
    wd = ('#1e1618', '#4a3a38', '#6e5a48', '#9a8460')
    for i, (x, top, lean) in enumerate(((7, 4, 0), (17, 1, 0), (28, 6, 1), (39, 2, 0), (50, 5, -1))):
        m = hpoly(a, [(x + lean * 2, top + 4), (x + 4 + lean * 2, top + 4), (x + 4, 29), (x, 29)])
        for k in range(3):                                        # Gorintō-Kerben am Kopf
            m |= hpoly(a, [(x + lean * 2 - (k == 1), top + k), (x + 4 + lean * 2 + (k == 1), top + k),
                           (x + 4 + lean * 2, top + k + 1), (x + lean * 2, top + k + 1)])
        m |= he(a, x + 2 + lean * 2, top + .5, 1.2, 1.4)
        hfill(a, edge(m), K)
        hfill(a, m, wd[2])
        hfill(a, m & ~np.roll(m, 1, 1), wd[3])
        hfill(a, m & ~np.roll(m, -1, 1), wd[1])
        for k in (1, 3):                                          # Kerben
            hp(a, x + lean * 2, top + k + 1, K); hp(a, x + 4 + lean * 2, top + k + 1, K)
        for y in range(top + 7, 27, 4):                           # Bonji in Tusche, verwittert
            hr(a, x + 2 + lean, y, x + 2 + lean, y + 1, '#1a1214')
            hp(a, x + 1 + lean, y + 2, '#1a1214')
        if i == 3:
            hr(a, x + 1, 18, x + 3, 18, wd[0])                     # Riss im Holz
    for (x, y) in ((13, 22), (34, 24), (47, 21)):
        _higanbana(a, x, y)
    # B: Jizō in der Nische, Kerze rechts (Licht bei (19, 9))
    _niche(b, 12, 47, 9)
    s = ('#191a28', '#3a3c54', '#5c627e', '#8a90a8')
    body = hpoly(b, [(22, 18), (32, 18), (34, 29), (20, 29)])
    head = he(b, 27, 14, 4.2, 4.4)
    hfill(b, edge(body | head), K)
    hfill(b, body | head, s[2])
    hfill(b, (body | head) & ~np.roll(body | head, 1, 1), s[3])
    hfill(b, (body | head) & ~np.roll(body | head, -1, 1), s[1])
    cap = he(b, 27, 12, 4.4, 3.2) & (_g(b)[0] <= 12)
    hfill(b, cap, '#a82a2a'); hfill(b, cap & ~np.roll(cap, 1, 0), '#d84a3a')   # rote Strickmütze
    hr(b, 25, 15, 26, 15, s[0]); hr(b, 28, 15, 29, 15, s[0])     # geschlossene Augen
    hp(b, 27, 17, s[1])
    bib = hpoly(b, [(22, 19), (32, 19), (27, 25)])
    hfill(b, bib, '#b8302a'); hfill(b, bib & ~np.roll(bib, -1, 0), '#7a1a20'); hr(b, 22, 19, 32, 19, '#e05a40')
    hr(b, 26, 22, 28, 25, s[3]); hp(b, 27, 21, s[3])             # gefaltete Hände
    for (x, y, c) in ((15, 28, 1), (17, 28, 2), (16, 27, 3), (16, 26, 2)):   # Steinhäufchen (Sai no Kawara)
        hr(b, x - 1, y, x + 1, y, s[c]); hp(b, x - 1, y, K)
    hr(b, 37, 26, 41, 29, s[1]); hr(b, 37, 26, 41, 26, s[2])     # Kerzenständer
    hr(b, 38, 20, 40, 25, '#e0dcd0'); hr(b, 40, 20, 40, 25, '#a8a49c')   # Kerze
    hp(b, 39, 19, K)
    hr(b, 38, 16, 40, 18, '#e89020'); hp(b, 39, 15, '#ffcc40'); hp(b, 39, 17, '#fff4c0')
    hp(b, 37, 24, '#e0dcd0')                                      # Wachstropfen
    return [a, b]


HI['hakaba'] = hakaba_hi


# ---- Kurama: Shimenawa mit Shide am Zedernfelsen / Hanadaka-Tengu-Maske am Nagel
def kurama_hi(name, base):
    a, b = base.copy(), base.copy()
    st_ = ('#6a5428', '#a88a48', '#d4b870', '#f0dca0')
    sag = lambda x: 11 + 4 * math.sin(math.pi * (x - 2) / 59)
    for x in range(2, 62):                                        # dicke, gedrehte Strohkordel
        y = int(round(sag(x)))
        hr(a, x, y - 2, x, y + 2, st_[1])
        hp(a, x, y - 2 + (x // 2) % 4, st_[3]); hp(a, x, y - 1 + (x // 2) % 4, st_[2])
        hp(a, x, y + 3, K); hp(a, x, y - 3, K)
    for x in (2, 61):                                             # Enden gebunden
        hr(a, x - 1, 7, x + 1, 13, st_[0])
    for x in (12, 32, 52):                                        # Shide im Zickzack
        y = int(round(sag(x))) + 3
        for k, (dx0, dx1) in enumerate(((0, 3), (-2, 1), (0, 3), (-2, 1))):
            hr(a, x + dx0, y + k * 3, x + dx1, y + k * 3 + 2, PAPER[3])
            hr(a, x + dx0, y + k * 3 + 2, x + dx1, y + k * 3 + 2, PAPER[1])
    for x in (22, 42):                                            # herabhängende Strohbüschel
        y = int(round(sag(x))) + 3
        for dx in range(-1, 2):
            hln(a, [(x + dx, y), (x + dx * 2, y + 5)], st_[2])
        hp(a, x, y + 6, st_[1])
    # B: rote Tengu-Maske mit langer Nase, weißen Brauen und Bart, Tokin auf der Stirn
    hln(b, [(32, 2), (27, 7)], '#3a2418'); hln(b, [(32, 2), (37, 7)], '#3a2418'); hr(b, 31, 1, 33, 2, '#7a7a8a')
    face = he(b, 32, 15, 8.5, 9.5)
    nose = hpoly(b, [(30, 14), (34, 14), (33, 27), (31, 27)])
    hfill(b, edge(face | nose), K)
    hfill(b, face, '#a82424')
    hfill(b, face & ~np.roll(face, 1, 1) & ~np.roll(face, 2, 1), '#d84a32')
    hfill(b, face & ~np.roll(face, -1, 1), '#6e1420')
    hfill(b, nose, '#c03428'); hr(b, 31, 14, 31, 26, '#f06a40'); hr(b, 33, 15, 33, 26, '#7a1820')
    hr(b, 30, 4, 34, 7, K); hr(b, 31, 5, 33, 6, '#2a2430')        # Tokin
    for sx in (-1, 1):
        hln(b, [(32 + sx * 2, 10), (32 + sx * 5, 9), (32 + sx * 9, 11)], '#e8e8ee')   # buschige Brauen
        hln(b, [(32 + sx * 2, 11), (32 + sx * 6, 10)], '#b8b8c4')
        ex = 32 + sx * 4
        hr(b, ex - 1, 12, ex + 1, 13, '#e8c040'); hp(b, ex, 13, K)   # goldene Augen
        hp(b, ex - sx, 12, '#fff4a0')
        hln(b, [(32 + sx * 4, 21), (32 + sx * 7, 23), (32 + sx * 6, 26)], '#e8e8ee')   # Bart
        hln(b, [(32 + sx * 3, 22), (32 + sx * 5, 26)], '#b8b8c4')
    hr(b, 29, 19, 30, 19, K); hr(b, 34, 19, 35, 19, K)            # Mundwinkel unter der Nase
    return [a, b]


HI['kurama'] = kurama_hi


# ---- Yukiyama: Eiszapfen mit Reifkante / Eishöhle, in der Yuki-onna wartet
def yukiyama_hi(name, base):
    a, b = base.copy(), base.copy()
    hr(a, 0, 8, 63, 9, ICE[3]); hr(a, 0, 10, 63, 10, ICE[2])     # Reifkante
    for x in range(0, 64, 5):
        hp(a, x, 7, '#e8f6ff')
    for (x, w, h) in ((3, 6, 12), (11, 4, 7), (17, 7, 17), (26, 3, 6), (31, 6, 13), (39, 4, 8), (45, 7, 18), (54, 5, 10), (60, 3, 6)):
        m = hpoly(a, [(x, 10), (x + w, 10), (x + w // 2, 10 + h)])
        hfill(a, edge(m) & (_g(a)[0] > 10), ICE[0])
        hfill(a, m, ICE[3])
        hfill(a, m & ~np.roll(m, -1, 1), ICE[2])
        hln(a, [(x + 1, 11), (x + w // 2, 8 + h)], '#e8f6ff')
        hp(a, x + w // 2, 11 + h, ICE[3])                         # Tropfen an der Spitze
    # B: Höhle, Eiszapfen als Zähne, darin ein bleiches Gesicht mit schwarzem Haar und kalten Augen
    Y, X = _g(b)
    cave = he(b, 32, 29, 17, 17) & (Y >= 12) & (Y <= 29)
    hfill(b, edge(cave) & (Y <= 29), ICE[3])
    hfill(b, cave, K)
    hfill(b, cave & ~he(b, 32, 30, 14, 14), '#101830')
    for (x, h) in ((21, 5), (26, 7), (31, 4), (36, 8), (42, 5)):  # Zähne
        m = hpoly(b, [(x - 1, 13), (x + 2, 13), (x, 13 + h)])
        hfill(b, m, ICE[2]); hln(b, [(x - 1, 13), (x, 12 + h)], ICE[3])
    hair = hpoly(b, [(27, 18), (37, 18), (39, 29), (25, 29)])
    hfill(b, hair, '#26223c')
    for x in (26, 28, 36, 38):                                    # Strähnen
        hln(b, [(x if x < 32 else x - 1, 20), (x - 1 if x < 32 else x, 29)], '#3a3656')
    face = he(b, 32, 22, 3.3, 4.2)
    hfill(b, face, '#c8d4e8'); hfill(b, face & ~np.roll(face, -1, 1), '#8a9ab8')
    hr(b, 29, 18, 35, 19, '#141020')                              # Mittelscheitel, Haar übers Gesicht
    hp(b, 30, 21, '#a0f0ff'); hp(b, 34, 21, '#a0f0ff')            # kalte Augen
    hp(b, 32, 25, '#5a6a8a')
    for (x, y) in ((36, 25), (39, 24), (42, 25), (44, 23)):       # eisiger Atem
        hp(b, x, y, '#d0e8f8')
    for (x, y) in ((23, 28), (41, 28)):
        hp(b, x, y, ICE[3])
    return [a, b]


HI['yukiyama'] = yukiyama_hi


# ---- Ryūgū: Rundfenster in die Tiefe, durch das ein Ryūgū no tsukai zieht / Otohimes Tamatebako auf Korallen
def ryugu_hi(name, base):
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    win = he(a, 32, 16, 12, 11)
    ring = he(a, 32, 16, 14.5, 13.5) & ~win
    hfill(a, edge(ring | win), K)
    hfill(a, ring, GOLD[2])
    hfill(a, ring & (Y > 18), GOLD[1])
    hfill(a, ring & (Y < 8), GOLD[3])
    hfill(a, win, '#0a1a34')
    hfill(a, win & (Y < 12), '#123058')
    for x in (25, 33, 40):                                        # Lichtstreifen von oben
        hln(a, [(x, 6), (x - 3, 18)], '#1a4070')
    for (x, h) in ((24, 7), (27, 5), (38, 8), (41, 5)):           # Seetang am Fenstergrund
        for k in range(h):
            hp(a, x + (k // 2) % 2, 26 - k, '#1c4a34')
    for i in range(23):                                           # Riemenfisch: silbern, lange rote Rückenflosse
        x = 21 + i
        y = int(round(15 + 2.2 * math.sin(i / 3.6)))
        hr(a, x, y, x, y + 1, SILVER[3] if i % 3 else SILVER[2])
        hp(a, x, y + 2, SILVER[1])
        hp(a, x, y - 1, '#e83a3a' if i % 2 else '#a82030')
    hp(a, 21, 14, '#ff6a50'); hp(a, 20, 13, '#ff6a50'); hp(a, 22, 15, K)    # Kopfkamm, Auge
    hfill(a, win & ~he(a, 32, 16, 11, 10), '#05101e')             # Glasrand dunkel
    hfill(a, edge(win) & ~win & (X < 30) & (Y < 10), GOLD[3])
    hp(a, 26, 8, '#9ad0ff'); hp(a, 25, 9, '#9ad0ff')               # Glanz auf dem Glas
    # B: Tamatebako – schwarzer Lack, goldene Wellen, rote Schnur, weißer Rauch steigt auf
    c = ('#3a1020', '#a83a4a', '#d8686a', '#f4a890')              # Edelkoralle, heller als der Lack
    for (x, y1, h) in ((9, 12, -1), (15, 15, 1), (50, 13, 1), (56, 11, -1)):
        mid = (y1 + 29) // 2
        m = np.zeros(a.a.shape[:2], bool)
        for dx in (0, 1):
            for (p0, p1) in (((x, 29), (x + h, mid)), ((x + h, mid), (x, y1)), ((x + h, mid), (x - 4 * h, mid - 4)),
                             ((x, y1 + 4), (x + 3 * h, y1 + 1))):
                n = max(abs(p1[0] - p0[0]), abs(p1[1] - p0[1]), 1)
                for i in range(n + 1):
                    m[int(round(p0[1] + (p1[1] - p0[1]) * i / n)), int(round(p0[0] + (p1[0] - p0[0]) * i / n)) + dx] = True
        hfill(b, edge(m), K)
        hfill(b, m, c[1]); hfill(b, m & ~np.roll(m, 1, 1), c[2])
        for (px, py) in ((x, y1), (x - 4 * h, mid - 4), (x + 3 * h, y1 + 1)):
            hp(b, px, py, c[3])
    hr(b, 22, 26, 42, 29, '#2a1418'); hr(b, 22, 26, 42, 26, '#5a2a2a')   # Korallenbank
    box = hpoly(b, [(23, 17), (41, 17), (41, 26), (23, 26)])
    lid = hpoly(b, [(22, 14), (42, 14), (42, 17), (22, 17)])
    hfill(b, edge(box | lid), K)
    hfill(b, box, '#14101c'); hfill(b, lid, '#1e1828')
    hr(b, 22, 14, 42, 14, '#3a3048')
    for x in range(24, 41, 4):                                    # Maki-e-Wellen in Gold
        hp(b, x, 22, GOLD[2]); hp(b, x + 1, 21, GOLD[3]); hp(b, x + 2, 22, GOLD[2]); hp(b, x + 3, 23, GOLD[1])
    hr(b, 31, 14, 33, 26, '#c82a2a'); hr(b, 22, 19, 42, 19, '#c82a2a')   # Schnur über Kreuz
    hr(b, 33, 14, 33, 26, '#7a1018')
    hfill(b, he(b, 32, 13, 2.2, 1.5), '#e83a3a'); hp(b, 31, 12, '#ff8a6a')   # Knoten
    hln(b, [(32, 14), (29, 18), (30, 21)], '#e83a3a'); hln(b, [(33, 14), (36, 18), (35, 21)], '#e83a3a')
    for k, (x, y) in enumerate(((35, 11), (37, 9), (36, 6), (38, 4), (40, 3), (39, 1))):   # Rauch, der altern lässt
        hfill(b, he(b, x, y, 2 - k * .2, 1.4), '#c8c8d8' if k % 2 else '#e8e8f0')
    return [a, b]


HI['ryugu'] = ryugu_hi


# ---- Uminobe: Fischernetz mit gläsernen Ukidama / Funayūrei-Hände mit bodenloser Schöpfkelle unter dem Totenlicht
def uminobe_hi(name, base):
    a, b = base.copy(), base.copy()
    net = ('#2a2630', '#5a5058', '#7a7068')
    sag = lambda x: 7 + 3 * math.sin(math.pi * x / 63)
    for x in range(0, 64):                                        # Leine oben
        hp(a, x, int(round(sag(x))) - 1, '#8a7a5a'); hp(a, x, int(round(sag(x))), '#5a4a3a')
    for i in range(-2, 8):                                        # Maschen
        hln(a, [(i * 10, int(sag(max(0, i * 10)))), (i * 10 + 18, 27)], net[1])
        hln(a, [(i * 10 + 18, int(sag(min(63, i * 10 + 18)))), (i * 10, 27)], net[1])
    for x in range(0, 64, 3):
        hp(a, x, 27, net[2]); hp(a, x, 28, net[0])
    for (x, y, r, cs) in ((12, 15, 3.6, ('#0e4a3a', '#2a8a6a', '#7ad0a8')), (31, 19, 4.2, ('#0e3a5a', '#2a6a9a', '#8ac0e8')),
                          (49, 14, 3.4, ('#3a4a10', '#7a8a2a', '#d0d88a'))):
        m = he(a, x, y, r, r)
        hfill(a, edge(m), K)
        hfill(a, m, cs[1])
        hfill(a, m & he(a, x + 1, y + 1, r - 1, r - 1) & ~he(a, x - 1, y - 1, r - 1, r - 1), cs[0])
        hp(a, x - 1, y - 2, cs[2]); hp(a, x - 2, y - 1, cs[2]); hp(a, x - 1, y - 1, '#ffffff')
        hln(a, [(x - int(r), y), (x + int(r), y)], '#3a3028')     # Schnurnetz um die Kugel
        hln(a, [(x, y - int(r)), (x, y + int(r))], '#3a3028')
    # B: blasses Totenlicht (Licht bei (32, 20)), darunter greifen Hände mit einer bodenlosen Hishaku aus der Gischt
    hln(b, [(32, 2), (32, 13)], '#5a4a3a')
    lan = he(b, 32, 19, 5.5, 6)
    hfill(b, edge(lan), K)
    hfill(b, lan, '#5a8ab0'); hfill(b, lan & he(b, 31, 18, 3.5, 4), '#b0d8f0')
    hfill(b, he(b, 32, 19, 1.5, 2.2), '#f0faff')
    for y in (15, 19, 23):                                        # Rippen der Laterne
        hfill(b, lan & (_g(b)[0] == y), '#3a5a7a')
    hr(b, 29, 12, 35, 13, K); hr(b, 29, 25, 35, 26, K)
    skin, sh = '#a8b8c0', '#6a7a88'
    for (x0, lean, top) in ((12, 1, 19), (22, -1, 22), (50, 1, 18)):   # Arme aus der Gischt, Finger gespreizt
        m = hpoly(b, [(x0, 29), (x0 + 3, 29), (x0 + 3 + lean, top + 3), (x0 + lean, top + 3)])
        m |= he(b, x0 + 1.5 + lean, top + 2, 2.6, 2)
        for f, dx in enumerate((-3, -1, 1, 3)):
            ln = 4 if f in (1, 2) else 3
            for k in range(ln):
                m[top - k, x0 + 1 + lean + dx + (dx * k) // 4] = True
        hfill(b, edge(m), K)
        hfill(b, m, skin); hfill(b, m & ~np.roll(m, -1, 1), sh)
        hp(b, x0 + 1 + lean, top + 6, sh)
    hln(b, [(52, 17), (57, 10)], '#6e5a40')                       # Schöpfkelle ohne Boden
    m = he(b, 58, 8, 2.6, 2) & ~he(b, 58, 8, 1.2, .8)
    hfill(b, m, '#8a7050'); hp(b, 58, 8, K)
    for x in range(8, 58, 3):                                     # Gischt am Wandfuß
        hp(b, x, 28, '#c8e0f0'); hp(b, x + 1, 29, '#7aa0c0')
    return [a, b]


HI['uminobe'] = uminobe_hi


# ---- Yomi: Chibiki-iwa versperrt Yomotsu-Hirasaka (Shimenawa, Shikome-Augen im Spalt) / Ikazuchi auf Izanamis Gebeinen
def _shide(cv, x, y):
    for k, dx in enumerate((0, 1, 0, 1, 0)):                      # Zickzack-Papierstreifen
        hr(cv, x + dx, y + k * 2, x + dx + 1, y + k * 2 + 1, '#e8e4d8' if k % 2 else '#c8c0b0')
    hp(cv, x + 2, y + 9, '#8a8478')


def yomi_hi(name, base):
    st = ('#1a1622', '#3a3440', '#5a5260', '#80788a', '#a8a0b0')
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    cave = hpoly(a, [(8, 29), (10, 12), (16, 7), (32, 5), (48, 7), (54, 12), (56, 29)])
    hfill(a, edge(cave), '#2a2430')
    hfill(a, cave, '#05040a')
    for (x, y) in ((14, 13), (17, 12)):                           # Yomotsu-shikome lauert im Spalt
        hp(a, x, y, '#e02a2a'); hp(a, x + 1, y, '#ff6a50')
    rock = he(a, 33, 20, 19, 10) & (Y <= 29)
    hfill(a, edge(rock), K)
    hfill(a, rock, st[3])
    hfill(a, rock & he(a, 37, 24, 18, 8), st[2])                  # Schattenseite unten rechts
    hfill(a, rock & he(a, 27, 15, 11, 4.5), st[4])
    hfill(a, rock & he(a, 24, 14, 5, 2), st[4])
    hln(a, [(40, 12), (43, 17), (41, 22), (45, 27)], st[0])        # Risse
    hln(a, [(22, 22), (26, 26)], st[0])
    for (x, y) in ((16, 26), (19, 27), (50, 25), (47, 28)):       # Flechten
        hp(a, x, y, '#4a5a3a')
    rope = lambda x: int(round(15 + 3 * math.sin(math.pi * (x - 14) / 38)))
    for x in range(14, 53):                                       # gedrehtes Seil
        y = rope(x)
        hp(a, x, y - 2, K); hp(a, x, y + 2, K)
        for d in (-1, 0, 1):
            hp(a, x, y + d, STRAW[3] if (x + d) % 4 < 2 else STRAW[1])
    for x in (21, 33, 45):
        _shide(a, x, rope(x) + 3)
    # B: Nische, unten Izanamis Gebeine; darauf hockt ein Ikazuchi, Blitze knistern um ihn
    _niche(b, 14, 50, 6)
    for x in range(16, 49, 3):                                    # Rippen
        hln(b, [(x, 29), (x + 2, 24)], BONE[2]); hp(b, x + 2, 24, BONE[3])
    hfill(b, he(b, 20, 26, 3.5, 2.6), BONE[3]); hp(b, 19, 26, K); hp(b, 21, 26, K)   # Schädel
    for (x, y) in ((27, 27), (38, 28), (44, 26)):                 # Maden
        hp(b, x, y, '#d8d0b8')
    body = hpoly(b, [(26, 25), (27, 17), (31, 13), (36, 13), (40, 17), (41, 25), (37, 23), (33, 25), (30, 23)])
    head = he(b, 33.5, 11, 4.5, 4)
    arm = hpoly(b, [(39, 17), (46, 14), (47, 16), (40, 20)]) | hpoly(b, [(28, 17), (22, 20), (22, 22), (29, 20)])
    m = body | head | arm
    hfill(b, edge(m), '#3a2a50')
    hfill(b, m, '#1e1428')
    hfill(b, m & (X < 31), '#2c1e3a')
    for (x0, x1) in ((29, 27), (38, 40)):                         # Hörner
        hln(b, [(x0, 9), (x1, 5)], BONE[3])
    hp(b, 31, 11, '#ffe24a'); hp(b, 32, 11, '#ffe24a'); hp(b, 35, 11, '#ffe24a'); hp(b, 36, 11, '#ffe24a')
    hr(b, 31, 13, 36, 14, K); hp(b, 32, 14, BONE[3]); hp(b, 35, 14, BONE[3])   # Maul mit Fängen
    hfill(b, edge(m) & np.roll(m, 1, 1) & ~np.roll(m, -1, 1) | (edge(m) & np.roll(m, -1, 0) & (Y < 20)), '#7a5ab0')   # Blitzschein am Rand
    for f in (0, 2):                                              # Krallen
        hp(b, 47 + f // 2, 13 + f, BONE[3]); hp(b, 21, 21 + f // 2, BONE[3])
    for pts in (((47, 12), (51, 8), (49, 7), (53, 3)), ((22, 19), (18, 15), (20, 14), (16, 9)),
                ((36, 7), (39, 4), (37, 3), (40, 0))):            # Blitze
        hln(b, list(pts), '#fff6a0')
        hln(b, [(x + 1, y) for (x, y) in pts], '#b89a2a')
    return [a, b]


HI['yomi'] = yomi_hi


# ---- Takamagahara: Wolkenpalast mit goldenem Chigi und leuchtendem Tor / Ame-no-Ukihashi mit der Juwelenhellebarde
def _cloud(cv, cx, cy, w):
    m = np.zeros(cv.a.shape[:2], bool)
    for i in range(-w, w + 1, 3):
        m |= he(cv, cx + i, cy - (2 if i % 2 else 0) + abs(i) // 4, 3.2, 2.6)
    hfill(cv, edge(m), '#6c70a2')
    hfill(cv, m, '#d8dcec')
    hfill(cv, m & ~np.roll(m, 2, 0), '#a4acc8')
    return m


def takamagahara_hi(name, base):
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    hall = (X >= 18) & (X <= 46) & (Y >= 14) & (Y <= 25)          # weiße Halle mit Pfosten
    hfill(a, edge(hall), K)
    hfill(a, hall, WHITE[3])
    for x in (18, 25, 39, 46):
        hfill(a, hall & (X >= x) & (X <= x + 1), '#b89060')
    door = (X >= 29) & (X <= 35) & (Y >= 15) & (Y <= 25)          # Licht bei (32, 16)
    hfill(a, door, SUN[2]); hfill(a, door & (X >= 31) & (X <= 33), SUN[3])
    roof = hpoly(a, [(14, 15), (24, 7), (40, 7), (50, 15)])
    hfill(a, edge(roof), K)
    hfill(a, roof, '#3a3048')
    hfill(a, roof & (Y >= 13), '#5a4a62')
    hln(a, [(14, 15), (50, 15)], GOLD[3])
    hr(a, 23, 6, 41, 6, GOLD[2])                                  # First
    for x in (26, 30, 34, 38):                                    # Katsuogi
        hr(a, x, 4, x + 1, 5, GOLD[3]); hp(a, x, 5, GOLD[1])
    for s in (-1, 1):                                             # Chigi gekreuzt an beiden Enden
        x = 32 + s * 9
        hln(a, [(x - 3 * s, 7), (x + 2 * s, 1)], GOLD[3])
        hln(a, [(x - 2 * s, 7), (x + 3 * s, 1)], GOLD[1])
    hr(a, 16, 26, 48, 27, '#b89060')                              # Veranda
    _cloud(a, 32, 28, 22)
    # B: zinnoberrote Himmelsbrücke über dem Wolkenmeer; die Juwelenhellebarde tropft Onogoro ins Meer
    arc = lambda x: int(round(25 - 11 * math.sin(math.pi * (x - 4) / 56)))
    for x in range(4, 61):
        y = arc(x)
        hr(b, x, y, x, y + 2, RED[2]); hp(b, x, y, RED[3]); hp(b, x, y + 3, K)
        hp(b, x, y - 4, RED[3] if x % 2 else RED[2])              # Geländer
        if x % 8 == 4:
            hr(b, x, y - 4, x, y - 1, RED[1]); hp(b, x, y - 5, GOLD[3])   # Pfosten mit Giboshi
    for x in (16, 48):                                            # Brückenpfeiler in die Wolken
        hr(b, x, arc(x) + 3, x + 1, 27, RED[1])
    _cloud(b, 8, 27, 7); _cloud(b, 56, 27, 7)
    hln(b, [(41, 2), (35, 20)], WOOD[3])                          # Ame-no-Nuboko
    hln(b, [(42, 2), (36, 20)], WOOD[1])
    tip = hpoly(b, [(34, 20), (37, 20), (34, 25)])
    hfill(b, edge(tip), K); hfill(b, tip, SILVER[3])
    for (x, y) in ((38, 8), (39, 6)):                             # Juwelen am Schaft
        hp(b, x, y, '#5ae0c0')
    hp(b, 34, 27, '#9ad0ff'); hp(b, 34, 28, '#d8f0ff')            # Tropfen
    return [a, b]


HI['takamagahara'] = takamagahara_hi


# ---- Shiramine: zerrissene Blut-Sutren am Querbalken mit Krähen-Tengu / Gorintō des Verbannten mit Groll-Feuer
BLOOD = ('#3a0812', '#5a0e1a', '#8a1c2a', '#c03040', '#ff8a7a')


def shiramine_hi(name, base):
    import random
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    r = random.Random('shiramine-hi')
    hr(a, 4, 8, 59, 8, K); hr(a, 4, 9, 59, 12, WOOD[2]); hr(a, 4, 9, 59, 9, WOOD[3]); hr(a, 4, 13, 59, 13, K)
    for x in range(6, 58, 7):                                     # Maserung
        hr(a, x, 11, x + 2, 11, WOOD[1])
    for (x0, ln) in ((8, 13), (19, 8), (30, 16), (41, 10)):     # Sutren-Streifen, unten ausgerissen
        bot = [14 + ln - (1 if (i * 5 + x0) % 3 == 0 else 0) - (2 if i == 2 else 0) for i in range(7)]
        for i in range(7):
            x = x0 + i
            hr(a, x, 14, x, bot[i], PAPER[3] if i < 5 else PAPER[2])
            hp(a, x, bot[i] + 1, K)
        hr(a, x0 - 1, 14, x0 - 1, max(bot), K); hr(a, x0 + 7, 14, x0 + 7, max(bot), K)
        hr(a, x0, 14, x0 + 6, 14, PAPER[1])                         # Knick am Balken
        for y in range(16, min(bot) - 1, 3):                      # mit Blut geschriebene Zeilen
            hr(a, x0 + 2, y, x0 + 4, y, BLOOD[2])
            hp(a, x0 + 3 + r.choice((-1, 0, 1)), y + 1, BLOOD[2])
            hp(a, x0 + 3, y, BLOOD[3])
    for y in range(24, 31):                                       # Blut tropft vom längsten Streifen
        hp(a, 33, y, BLOOD[2] if y < 29 else BLOOD[3])
    hp(a, 33, 31, BLOOD[1])
    # Krähen-Tengu auf dem Balkenende
    body = he(a, 54, 4, 5, 3) | he(a, 49, 5, 3, 2)
    hfill(a, edge(body), K); hfill(a, body, '#141020')
    hfill(a, body & (Y <= 3), '#2a2a48')
    hpoly_m = hpoly(a, [(58, 3), (62, 4), (58, 5)])
    hfill(a, hpoly_m, '#3a3428')
    hp(a, 56, 3, BLOOD[4]); hp(a, 55, 3, BLOOD[3])                # rotes Auge
    for x in (52, 55):
        hr(a, x, 7, x, 7, '#3a3428')
    for x in (46, 47, 48):                                        # Schwanzfedern
        hp(a, x, 6 + (x == 46), '#2a2a48')
    # B: Gorintō in der Felsnische, daneben ein schwebendes Groll-Feuer (Licht bei 40, 10)
    nm = (X >= 16) & (X <= 46) & (Y >= 6) & (Y <= 29) & ~(((X == 16) | (X == 46)) & (Y == 6))
    hfill(b, nm, K)
    hfill(b, nm & (abs(X - 40) + abs(Y - 11) < 9) & ~(abs(X - 40) + abs(Y - 11) < 5), '#200a12')
    s = STONE
    chi = (X >= 22) & (X <= 35) & (Y >= 23) & (Y <= 29)           # Chi: Würfel
    sui = he(b, 28.5, 19.5, 6, 3.6)                               # Sui: Kugel
    ka = hpoly(b, [(20, 16), (24, 12), (33, 12), (37, 16)])        # Ka: Dach mit aufgebogenen Traufen
    fu = he(b, 28.5, 11, 3.5, 2.2) & (Y >= 10)                    # Fū: Halbmond
    ku = he(b, 28.5, 8, 2, 2.5)                                   # Kū: Juwel
    allm = chi | sui | ka | fu | ku
    hfill(b, edge(allm), K)
    hfill(b, allm, s[2])
    hfill(b, allm & (X <= 25), s[3])                              # Mondlicht von links
    hfill(b, allm & (X >= 33), s[1])
    hfill(b, chi & (Y == 23), s[3]); hfill(b, ka & (Y == 16), s[1])
    hfill(b, edge(sui) & chi, K)
    hfill(b, chi & (Y >= 28) & ((X + Y) % 3 > 0), MOSS[1])        # Moos am Sockel
    hp(b, 23, 27, MOSS[2]); hp(b, 34, 26, MOSS[1])
    hr(b, 27, 24, 30, 28, PAPER[3]); hr(b, 30, 24, 30, 28, PAPER[1])   # Ofuda mit Blutsiegel
    hr(b, 28, 25, 29, 25, BLOOD[2]); hr(b, 28, 27, 29, 27, BLOOD[2]); hp(b, 28, 26, BLOOD[3])
    fire = hpoly(b, [(37, 13), (38, 8), (40, 10), (41, 4), (43, 9), (44, 7), (44, 13), (40, 15)])
    hfill(b, edge(fire), BLOOD[0])
    hfill(b, fire, BLOOD[2])
    hfill(b, hpoly(b, [(38, 13), (40, 9), (41, 7), (43, 12), (40, 14)]), BLOOD[3])
    hfill(b, he(b, 40.5, 12, 1.5, 1.5), BLOOD[4])
    for (x, y) in ((36, 6), (45, 3), (42, 1)):                    # Funken
        hp(b, x, y, BLOOD[3])
    return [a, b]


HI['shiramine'] = shiramine_hi


# ---- Kubizuka: Sotoba-Bretter mit Bonji-Schrift und Shide / Nische mit Steinfrosch (kaeru = heimkehren), darüber Onibi
PALE = ('#1a3a4a', '#3a7a86', '#8ad0c8', '#e0fff4')


def kubizuka_hi(name, base):
    import random
    a, b = base.copy(), base.copy()
    Y, X = _g(a)
    r = random.Random('kubizuka-hi')
    ink = '#160c14'
    for i, (x, top) in enumerate(((7, 5), (19, 2), (31, 6), (43, 3))):   # Sotoba, leicht verschieden hoch
        w = 8
        board = (X >= x) & (X <= x + w) & (Y >= top + 5) & (Y <= 31)
        head = (X >= x) & (X <= x + w) & (Y >= top + 2) & (Y < top + 5)
        tip = hpoly(a, [(x, top + 2), (x + w // 2, top - 1), (x + w, top + 2)])
        allm = board | head | tip
        hfill(a, edge(allm), K)
        hfill(a, allm, WOOD[2])
        hfill(a, allm & (X <= x + 1), WOOD[3])                    # Mondlicht von links
        hfill(a, allm & (X >= x + w - 1), WOOD[1])
        hr(a, x, top + 4, x + w, top + 4, K)                      # Kerben des Fünf-Elemente-Kopfes
        hr(a, x, top + 7, x + w, top + 7, K)
        hp(a, x, top + 5, K); hp(a, x + w, top + 5, K)
        for y in range(top + 9, 28, 4):                           # Bonji-Zeichen, verwittert
            c = ink if r.random() > .25 else WOOD[1]
            hr(a, x + 3, y, x + 5, y, c); hp(a, x + 4, y + 1, c)
            hp(a, x + 3 + r.choice((0, 2)), y + 2, c)
        for y in range(top + 10, 31, 5):                          # Maserung
            hp(a, x + 2 + (y % 3), y, WOOD[1])
    for x0 in (28, 52):                                           # Shide-Papierstreifen zwischen den Brettern, im Wind geknickt
        for k, (dx, dy) in enumerate(((0, 0), (1, 2), (-1, 4), (0, 6))):
            hr(a, x0 + dx, 12 + dy, x0 + dx + 2, 13 + dy, PAPER[3] if k % 2 == 0 else PAPER[2])
        hp(a, x0 + 3, 11, K)
    # B: Felsnische mit Steinfrosch auf Sockel, Onibi schwebt darüber (Licht bei 40, 4)
    nm = (X >= 14) & (X <= 48) & (Y >= 4) & (Y <= 29) & ~(((X == 14) | (X == 48)) & (Y == 4))
    hfill(b, nm, K)
    hfill(b, nm & (abs(X - 40) + abs(Y - 7) < 10) & ~(abs(X - 40) + abs(Y - 7) < 6), '#0c1e24')
    s = STONE
    ped = (X >= 18) & (X <= 41) & (Y >= 25) & (Y <= 29)
    hfill(b, edge(ped), K); hfill(b, ped, s[1]); hr(b, 18, 25, 41, 25, s[2])
    hfill(b, ped & (Y >= 28) & ((X + Y) % 3 > 0), MOSS[1])
    body = he(b, 29.5, 20, 9, 5.5) & (Y <= 24)                    # gedrungener Leib
    legs = he(b, 22, 23, 3, 2) | he(b, 37, 23, 3, 2)              # Hinterschenkel
    eyes = he(b, 24.5, 14, 2.6, 2.4) | he(b, 34.5, 14, 2.6, 2.4)  # vorstehende Augenhöcker
    frog = body | legs | eyes
    hfill(b, edge(frog), K)
    hfill(b, frog, s[2])
    hfill(b, frog & (X <= 25), s[3])
    hfill(b, frog & (X >= 36), s[1])
    hfill(b, he(b, 29.5, 22.5, 5, 1.6), s[3])                     # helle Kehle
    hln(b, [(22, 19), (25, 21), (34, 21), (37, 19)], K)           # breites Maul
    for cx in (24, 34):
        hp(b, cx, 14, PALE[2]); hp(b, cx + 1, 14, PALE[3]); hp(b, cx, 13, K)   # Onibi spiegelt sich im Steinauge
    hr(b, 21, 24, 24, 24, K); hr(b, 35, 24, 38, 24, K)            # Zehen
    for (x, y) in ((27, 17), (31, 18), (33, 16), (21, 21)):       # Flechten
        hp(b, x, y, MOSS[2])
    bib = hpoly(b, [(25, 22), (34, 22), (29, 25)])                # roter Latz unter dem Maul, wie ihn Pilger umbinden
    hfill(b, bib, '#8a1c2a'); hfill(b, bib & (Y == 22), '#c03040'); hfill(b, bib & (X >= 32), '#5a0e1a')
    fire = hpoly(b, [(37, 9), (38, 4), (40, 6), (41, 0), (43, 5), (44, 3), (44, 9), (40, 11)])
    hfill(b, edge(fire), PALE[0])
    hfill(b, fire, PALE[1])
    hfill(b, hpoly(b, [(38, 9), (40, 5), (41, 3), (43, 8), (40, 10)]), PALE[2])
    hfill(b, he(b, 40.5, 8, 1.5, 1.5), PALE[3])
    for (x, y) in ((36, 2), (46, 6), (35, 7)):
        hp(b, x, y, PALE[2])
    return [a, b]


HI['kubizuka'] = kubizuka_hi
