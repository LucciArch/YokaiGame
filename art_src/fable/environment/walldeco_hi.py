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
