"""Hilfen für die Einzel-Item-Symbole: zusätzliche Farbrampen, Umfärben ganzer Materialfamilien, Zierelemente."""
import math
import numpy as np
from common import *
import px

col('t4', '#173f45'); col('t5', '#2f8a7e'); col('t6', '#7fd6bd')     # Jade / Türkis
col('n4', '#141a3a'); col('n5', '#2d3f86'); col('n6', '#5f7fd0')     # Indigo
col('c4', '#5a0f1c'); col('c5', '#a3233a')                            # Karmesin
LEG.update({'4': 't4', '5': 't5', '6': 't6', 'I': 'n4', 'J': 'n5', 'O': 'n6', 'U': 'c4', 'V': 'c5'})

FAM = {
    'red': 'qrRe', 'gold': 'ogyY', 'white': 'nvwW', 'iron': '0123', 'wood': 'jdDt', 'bone': 'ubBi',
    'blue': 'zaAA', 'green': 'FfGl', 'purple': 'xpPX', 'black': 'khHH', 'straw': 'cCss', 'pink': 'mSTT',
    'orange': '7899', 'jade': '4566', 'indigo': 'IJOO', 'crimson': 'UVRe',
}
RAMP3 = {k: v[:3] for k, v in FAM.items()}


def recolor(c, src, dst, only=None):
    a, b = FAM[src], FAM[dst]
    tr = {a[i]: b[min(i, len(b) - 1)] for i in range(len(a))}
    return c.remap(tr, only)


def glow_dots(c, pts, ch='W'):
    for x, y in pts:
        if 0 <= x < c.w and 0 <= y < c.h:
            c.a[y, x] = ch
    return c


def sparkle(c, x, y, ch='W', ch2='Y'):
    c.g(x - 1, y - 1, ".%s.\n%s%s%s\n.%s." % (ch2, ch2, ch, ch2, ch2))
    return c


def disc(c, cx, cy, r, fam, sd=2, hl=1, ring=None):
    return c.form(E(cx, cy, r, r), RAMP3[fam], sd, hl, ring=ring)


def blob(c, cx, cy, rx, ry, fam, sd=2, hl=1):
    return c.form(E(cx, cy, rx, ry), RAMP3[fam], sd, hl)


def tube(pts, fam, c, sd=1, hl=1):
    """Kette aus Kapseln [(x, y, r), ...]"""
    m = np.zeros((c.h, c.w), bool)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        m |= L(x0, y0, r0, x1, y1, r1)
    c.form(m, RAMP3[fam], sd, hl)
    return m


def kanji_plate(c, x, y, glyph, bg='W', fg='q'):
    """kleines Schriftzeichen (5x5 Raster-Glyphe) auf hellem Grund"""
    rows = glyph.strip('\n').split('\n')
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            c.a[y + j, x + i] = fg if ch == '#' else bg
    return c
