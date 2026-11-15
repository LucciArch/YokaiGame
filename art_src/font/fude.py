"""„Yōkai Fude“ – eigene Pinsel-Schrift für das Spiel.

Jeder Buchstabe ist ein Skelett aus Strichen (Koordinaten: Grundlinie 0, x-Höhe 46, Versalhöhe 68).
Die Striche werden mit einer schräg gehaltenen, ovalen Pinselspitze nachgezogen (dick-dünn wie
Kalligrafie), mit Ansatzdruck am Anfang und wahlweise spitz auslaufendem Ende (harai, Endung '>')
oder kräftigem Halt (tome). Ergebnis: assets/fonts/YokaiFude.ttf
usage: python3 fude.py [vorschau.png]"""
import math
import os
import sys
from shapely.geometry import Polygon, Point, MultiPolygon
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely import affinity

U = 10                      # Font-Einheiten pro Rastereinheit (UPM 1000)
NIB_ANGLE = 42              # Grad
NIB_W, NIB_T = 12.5, 5.2    # Pinselbreite dick / dünn (Rastereinheiten)
GAP = 5                     # Laufweite


# ---------------------------------------------------------------- Glyph-Skelette
# Ein Strich: Punkte "x,y x,y"; Präfix '~' = weiche Kurve durch die Punkte; Endung '>' = harai (spitz)
G = {
    ' ': (22, []),
    # Großbuchstaben
    'A': (60, ['30,68 4,0>', '30,68 56,0', '15,23 46,23']),
    'B': (54, ['8,68 8,0', '~8,68 32,68 43,61 44,50 35,39 8,38', '~8,38 37,38 48,29 48,11 37,1 8,0']),
    'C': (56, ['~51,57 41,66 27,68 13,61 6,42 7,21 15,6 29,0 42,1 52,10>']),
    'D': (60, ['8,68 8,0', '~8,68 30,68 46,58 53,36 47,12 30,0 8,0']),
    'E': (50, ['8,68 8,0', '8,68 45,68', '8,36 37,36', '8,0 47,0>']),
    'F': (48, ['8,68 8,0', '8,68 45,68', '8,36 37,36']),
    'G': (60, ['~52,57 41,66 27,68 13,61 6,42 7,21 15,6 29,0 43,2 52,12 52,30', '36,30 54,30']),
    'H': (60, ['8,68 8,0', '52,68 52,0', '8,36 52,36']),
    'I': (22, ['11,68 11,0']),
    'J': (40, ['~32,68 32,14 26,2 14,0 4,8>']),
    'K': (54, ['8,68 8,0', '48,68 9,28', '21,40 51,0>']),
    'L': (46, ['8,68 8,0', '8,0 45,0>']),
    'M': (72, ['7,0 9,68', '9,68 36,8', '36,8 63,68', '63,68 65,0']),
    'N': (60, ['8,0 8,68', '8,68 52,0', '52,0 52,68']),
    'O': (64, ['~32,68 15,62 6,41 8,18 18,4 32,0 47,4 58,20 58,42 49,62 32,68']),
    'P': (52, ['8,68 8,0', '~8,68 34,68 46,60 46,44 34,34 8,34']),
    'Q': (64, ['~32,68 15,62 6,41 8,18 18,4 32,0 47,4 58,20 58,42 49,62 32,68', '36,12 60,-9>']),
    'R': (54, ['8,68 8,0', '~8,68 34,68 46,60 46,45 34,35 8,34', '26,34 51,0>']),
    'S': (50, ['~44,59 34,67 20,68 9,61 8,49 17,40 32,34 42,26 44,12 34,2 18,0 5,7>']),
    'T': (54, ['4,68 50,68', '27,68 27,0']),
    'U': (60, ['~8,68 8,20 14,6 30,0 46,6 52,20 52,68']),
    'V': (58, ['4,68 29,0', '29,0 54,68']),
    'W': (80, ['4,68 20,0', '20,0 40,56', '40,56 60,0', '60,0 76,68']),
    'X': (56, ['6,68 50,0>', '50,68 6,0>']),
    'Y': (54, ['4,68 27,34', '50,68 27,34 27,0']),
    'Z': (52, ['6,68 46,68 6,0 48,0>']),
    # Kleinbuchstaben
    'a': (48, ['~38,39 30,46 18,46 8,38 6,22 10,8 20,0 30,2 38,12', '38,46 38,6 43,0>']),
    'b': (50, ['8,72 8,0', '~8,32 18,43 30,46 40,38 44,22 40,8 28,0 16,2 8,10']),
    'c': (44, ['~38,39 30,46 18,46 8,38 5,22 9,8 20,0 32,1 40,8>']),
    'd': (50, ['~40,32 32,43 20,46 10,38 6,22 10,8 22,0 34,2 40,10', '40,72 40,6 45,0>']),
    'e': (46, ['~7,23 40,23 38,37 28,46 16,45 7,34 5,20 10,7 22,0 34,1 41,8>']),
    'f': (34, ['~31,69 23,72 15,67 12,56 12,0', '2,44 28,44']),
    'g': (48, ['~38,39 30,46 18,46 8,38 6,22 10,8 20,0 30,2 38,12', '~38,46 38,-8 32,-18 20,-21 7,-16>']),
    'h': (48, ['8,72 8,0', '~8,30 16,42 26,46 36,42 40,30 40,0']),
    'i': (20, ['10,44 10,0', '10,59 10,57']),
    'j': (24, ['~14,44 14,-10 10,-18 2,-20>', '14,59 14,57']),
    'k': (44, ['8,72 8,0', '38,46 9,17', '18,26 40,0>']),
    'l': (20, ['~10,72 10,6 15,0>']),
    'm': (70, ['8,46 8,0', '~8,30 14,42 22,46 30,42 34,30 34,0', '~34,30 40,42 48,46 56,42 60,30 60,0']),
    'n': (48, ['8,46 8,0', '~8,30 16,42 26,46 36,42 40,30 40,0']),
    'o': (48, ['~24,46 12,41 6,24 10,8 24,0 37,6 42,22 37,40 24,46']),
    'p': (50, ['8,46 8,-22', '~8,32 18,43 30,46 40,38 44,22 40,8 28,0 16,2 8,10']),
    'q': (50, ['~40,32 32,43 20,46 10,38 6,22 10,8 22,0 34,2 40,10', '40,46 40,-22']),
    'r': (36, ['8,46 8,0', '~8,29 14,40 22,46 33,44>']),
    's': (40, ['~34,39 26,46 14,46 6,40 8,30 20,24 30,20 35,10 30,2 16,0 4,6>']),
    't': (34, ['~14,62 14,8 18,1 29,0>', '2,44 30,44']),
    'u': (48, ['~8,46 8,14 14,3 24,0 34,4 40,16', '40,46 40,6 45,0>']),
    'v': (44, ['4,46 22,0', '22,0 40,46']),
    'w': (64, ['4,46 16,0', '16,0 32,40', '32,40 48,0', '48,0 60,46']),
    'x': (44, ['6,46 38,0>', '38,46 6,0>']),
    'y': (46, ['4,46 22,2', '~40,46 26,6 18,-12 10,-20 2,-20>']),
    'z': (42, ['6,46 36,46 6,0 38,0>']),
    # Ziffern
    '0': (50, ['~25,66 11,58 6,33 11,8 25,0 39,8 44,33 39,58 25,66']),
    '1': (40, ['8,52 24,66 24,0']),
    '2': (50, ['~8,51 14,62 26,66 38,62 42,50 36,36 6,0 45,0>']),
    '3': (50, ['~8,57 18,66 32,66 41,57 38,44 24,38', '~24,38 38,34 44,22 40,7 28,0 14,0 4,8>']),
    '4': (50, ['34,0 34,66 4,18 46,18']),
    '5': (50, ['42,66 12,66 9,38', '~9,38 22,42 36,40 44,28 42,10 30,0 16,0 4,8>']),
    '6': (50, ['~38,64 26,66 13,58 6,40 6,18 12,5 25,0 38,5 44,18 40,32 28,38 16,36 7,26']),
    '7': (48, ['6,66 44,66 18,0>']),
    '8': (50, ['~25,38 13,44 10,56 17,65 25,66 33,65 40,56 37,44 25,38 11,31 6,18 12,4 25,0 38,4 44,18 39,31 25,38']),
    '9': (50, ['~43,40 34,30 22,28 10,34 6,48 12,62 25,66 38,60 44,44 42,20 34,6 22,0 9,3>']),
    # Satzzeichen
    '.': (18, ['9,3 9,1']),
    ',': (18, ['10,4 9,0 4,-11>']),
    ':': (18, ['9,3 9,1', '9,37 9,35']),
    ';': (18, ['10,4 9,0 4,-11>', '9,37 9,35']),
    '!': (20, ['10,68 10,18>', '10,3 10,1']),
    '?': (40, ['~6,55 12,65 22,68 32,64 36,54 32,44 20,34 20,20>', '20,3 20,1']),
    '-': (34, ['5,26 29,26']),
    '–': (54, ['5,26 49,26']),
    '—': (80, ['5,26 75,26']),
    '_': (50, ['0,-8 50,-8']),
    '…': (54, ['9,3 9,1', '27,3 27,1', '45,3 45,1']),
    '„': (32, ['10,4 9,0 4,-11>', '24,4 23,0 18,-11>']),
    '“': (32, ['13,57 8,68', '27,57 22,68']),
    '”': (32, ['13,68 8,57>', '27,68 22,57>']),
    '"': (30, ['10,70 10,56>', '22,70 22,56>']),
    "'": (18, ['9,70 9,56>']),
    '`': (22, ['6,72 14,62>']),
    '(': (28, ['~22,72 12,56 7,30 11,4 22,-14>']),
    ')': (28, ['~6,72 16,56 21,30 17,4 6,-14>']),
    '[': (26, ['20,72 8,72 8,-14 20,-14']),
    ']': (26, ['6,72 18,72 18,-14 6,-14']),
    '{': (28, ['~22,72 14,66 14,38 6,30 14,22 14,-8 22,-14']),
    '}': (28, ['~6,72 14,66 14,38 22,30 14,22 14,-8 6,-14']),
    '/': (34, ['30,72 4,-10>']),
    '\\': (34, ['4,72 30,-10>']),
    '|': (20, ['10,74 10,-16']),
    '%': (64, ['~16,66 8,60 7,48 14,40 22,42 26,52 22,64 16,66', '~48,26 40,20 39,8 46,0 54,2 58,12 54,24 48,26', '50,66 12,0']),
    '+': (50, ['25,48 25,8', '5,28 45,28']),
    '=': (48, ['6,36 42,36', '6,20 42,20']),
    '<': (44, ['38,48 6,28 38,8']),
    '>': (44, ['6,48 38,28 6,8']),
    '*': (40, ['20,66 20,40', '8,60 32,46', '32,60 8,46']),
    '#': (56, ['20,64 14,4', '40,64 34,4', '6,46 52,46', '4,24 50,24']),
    '&': (58, ['~52,0 30,24 14,40 10,54 16,65 26,67 34,60 32,48 20,38 8,24 8,10 18,1 32,0 44,10 50,24']),
    '@': (72, ['~50,40 42,46 32,44 26,34 28,24 36,20 46,24 50,40 50,22 56,18 64,26 64,44 56,60 40,68 22,64 10,50 8,28 18,10 34,2 52,4 62,12>']),
    '^': (40, ['6,52 20,68 34,52']),
    '~': (48, ['~4,24 12,32 22,30 28,24 36,22 44,30']),
    '×': (46, ['8,46 38,10', '38,46 8,10']),
    '•': (26, ['13,32 13,26']),
    '·': (18, ['9,32 9,29']),
    '‹': (30, ['22,42 8,24 22,6']),
    '›': (30, ['8,42 22,24 8,6']),
    '→': (66, ['4,28 58,28', '40,44 60,28 40,12']),
    '←': (66, ['8,28 62,28', '26,44 6,28 26,12']),
    '↑': (44, ['22,4 22,62', '6,44 22,64 38,44']),
    '↓': (44, ['22,64 22,6', '6,24 22,4 38,24']),
    '½': (66, ['6,58 16,66 16,34', '52,66 14,0', '~38,22 42,30 50,32 58,28 58,20 38,0 60,0']),
    '°': (28, ['~14,68 7,64 6,56 12,51 20,53 22,61 18,67 14,68']),
    'ß': (52, ['~8,0 8,56 14,68 26,72 36,66 38,54 28,44 22,40', '~22,40 36,36 42,22 38,8 26,0 17,2>']),
}

# Akzente: Umlaut-Punkte und Makron
DIA = {'Ä': ('A', 'u', 30), 'Ö': ('O', 'u', 32), 'Ü': ('U', 'u', 30), 'ä': ('a', 'u', 24), 'ö': ('o', 'u', 24), 'ü': ('u', 'u', 24),
       'Ō': ('O', 'm', 32), 'Ū': ('U', 'm', 30), 'Ā': ('A', 'm', 30), 'ō': ('o', 'm', 24), 'ū': ('u', 'm', 24), 'ā': ('a', 'm', 24),
       'ī': ('i', 'm', 10), 'ē': ('e', 'm', 23), 'é': ('e', 'a', 23), 'è': ('e', 'g', 23), 'à': ('a', 'g', 24)}
for ch, (base, kind, cx) in DIA.items():
    adv, strokes = G[base]
    cap = base.isupper()
    y = 80 if cap else 58
    if base == 'i':
        strokes = strokes[:1]
    if kind == 'u':
        add = ['%d,%d %d,%d' % (cx - 9, y + 1, cx - 9, y - 1), '%d,%d %d,%d' % (cx + 9, y + 1, cx + 9, y - 1)]
    elif kind == 'm':
        add = ['%d,%d %d,%d' % (cx - 12, y, cx + 12, y)]
    elif kind == 'a':
        add = ['%d,%d %d,%d>' % (cx + 6, y + 8, cx - 4, y - 2)]
    else:
        add = ['%d,%d %d,%d>' % (cx - 6, y + 8, cx + 4, y - 2)]
    G[ch] = (adv, strokes + add)


# ---------------------------------------------------------------- Pinsel
def parse(st):
    smooth = st.startswith('~')
    harai = st.endswith('>')
    st = st.strip('~>')
    pts = [tuple(float(v) for v in p.split(',')) for p in st.split()]
    return pts, smooth, harai


def catmull(pts, n=10):
    if len(pts) < 3:
        return pts
    closed = pts[0] == pts[-1]
    P = ([pts[-2]] if closed else [pts[0]]) + pts + ([pts[1]] if closed else [pts[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(pts[-1])
    return out


def resample(pts, step=0.5):
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        n = max(1, int(d / step))
        for k in range(1, n + 1):
            out.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    return out


def nib(x, y, p):
    e = Point(0, 0).buffer(1, 8)
    e = affinity.scale(e, NIB_W / 2 * p, NIB_T / 2 * max(.55, p))
    e = affinity.rotate(e, NIB_ANGLE, origin=(0, 0))
    return affinity.translate(e, x, y)


def stroke(st):
    pts, smooth, harai = parse(st)
    if not smooth:                               # Querstriche steigen leicht an (wie mit dem Pinsel)
        q = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            if abs(dy) < 0.15 * abs(dx) and abs(dx) > 8:
                b = (b[0], b[1] + 0.05 * dx)
            q.append(b)
        pts = q
    if smooth:
        pts = catmull(pts)
    pts = resample(pts)
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.dist(a, b))
    tot = L[-1] or 1
    shapes = []
    for (x, y), s in zip(pts, L):
        p = 1.0
        if s < 3:                                   # Ansatzdruck (irikomi)
            p = 1.12 - 0.04 * s
        rest = tot - s
        if harai:
            k = min(tot * .45, 22)
            if rest < k:
                p = 0.14 + 0.86 * (rest / k) ** 0.8
        elif rest < 2.5 and tot > 4:                # kräftiger Halt (tome)
            p = 1.08
        shapes.append(nib(x, y, p))
    if tot > 3:
        x0, y0 = pts[0]                          # Pinselknoten am Ansatz (kiri-komi), nach rechts unten gedrückt
        shapes.append(nib(x0 + 1.4, y0 - 1.2, 1.12))
        if not harai:                            # Halt am Ende (tome): kurzer Druck
            x1, y1 = pts[-1]
            shapes.append(nib(x1 + 0.9, y1 - 0.9, 1.0))
    return unary_union(shapes)


def glyph_shape(ch):
    adv, strokes = G[ch]
    if not strokes:
        return adv, None
    sh = unary_union([stroke(s) for s in strokes]).simplify(0.08)
    return adv, sh


# ---------------------------------------------------------------- Font bauen
def build(path):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    chars = sorted(G.keys())
    names = ['.notdef'] + ['uni%04X' % ord(c) for c in chars]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({ord(c): 'uni%04X' % ord(c) for c in chars})
    glyphs, metrics = {}, {}
    pen = TTGlyphPen(None)
    pen.moveTo((50, 0)); pen.lineTo((50, 680)); pen.lineTo((450, 680)); pen.lineTo((450, 0)); pen.closePath()
    glyphs['.notdef'] = pen.glyph()
    metrics['.notdef'] = (500, 50)
    for c in chars:
        adv, sh = glyph_shape(c)
        pen = TTGlyphPen(None)
        lsb = 0
        if sh is not None and not sh.is_empty:
            polys = list(sh.geoms) if isinstance(sh, MultiPolygon) else [sh]
            for pg in polys:
                pg = orient(pg, sign=-1.0)
                for ring in [pg.exterior] + list(pg.interiors):
                    co = [(int(round((x + GAP / 2) * U)), int(round(y * U))) for x, y in list(ring.coords)[:-1]]
                    dd = []
                    for q in co:
                        if not dd or dd[-1] != q:
                            dd.append(q)
                    if len(dd) < 3:
                        continue
                    pen.moveTo(dd[0])
                    for q in dd[1:]:
                        pen.lineTo(q)
                    pen.closePath()
            lsb = int(round((sh.bounds[0] + GAP / 2) * U))
        glyphs['uni%04X' % ord(c)] = pen.glyph()
        metrics['uni%04X' % ord(c)] = (int((adv + GAP) * U), lsb)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-260)
    fb.setupNameTable({'familyName': 'Yokai Fude', 'styleName': 'Regular'})
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-260, usWinAscent=900, usWinDescent=260, sCapHeight=680, sxHeight=460)
    fb.setupPost()
    fb.save(path)


def preview(ttf, png):
    import pygame
    pygame.init()
    lines = ['Yōkai no Michi', 'Die Nacht der hundert Dämonen', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ÄÖÜŌŪ',
             'abcdefghijklmnopqrstuvwxyz äöüßōū', '0123456789 .,:;!? „Zitat“ – … ‹ › → • × ½ %',
             'Neuer Lauf   Tägliche Prüfung   Yōkai-Lexikon', 'Schaden 3.50  Feuerrate 2.60/s  Glück 0']
    sizes = [64, 40, 36, 36, 32, 28, 22]
    surf = pygame.Surface((1500, 560))
    surf.fill((20, 14, 30))
    y = 10
    for l, sz in zip(lines, sizes):
        f = pygame.font.Font(ttf, sz)
        surf.blit(f.render(l, True, (250, 236, 210)), (16, y))
        y += int(sz * 1.35) + 6
    pygame.image.save(surf, png)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, '..', '..', 'yokai', 'assets', 'fonts')
    os.makedirs(out, exist_ok=True)
    ttf = os.path.join(out, 'YokaiFude.ttf')
    build(ttf)
    print('ok', ttf)
    if len(sys.argv) > 1:
        preview(ttf, sys.argv[1])
