"""Titel-Logo „Yōkai no Michi“ (Hi-Res-Ebene, doppelte Dichte) + Hanko-Siegel 妖怪の道.
Schriftzug aus der eigenen Pinselschrift YokaiFude, gestuft vergoldet mit Umriss und Schlagschatten.
Die Kanji sind als Strich-Skelette auf einem 16er-Raster gesetzt (Strichfolge wie geschrieben).
usage: python3 logo.py"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'yokai', 'assets')
DST = os.path.join(ROOT, 'env', '_title')


def hx(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


K, SHADOW = hx('#0a0814'), hx('#170c26')
GOLD = [hx(c) for c in ('#fffbc0', '#ffe24a', '#f0b830', '#d8961a', '#8a4a12')]
V, Vd, Vl, PAPER = hx('#c02634'), hx('#801634'), hx('#ee5a48'), hx('#fff6d8')

KANJI = {   # Striche als Punktfolgen (x, y) im Raster 0..15
    '妖': [[(3, 0), (1, 6), (6, 13)], [(5, 3), (4, 9), (1, 15)], [(0, 6), (7, 6)],
          [(14, 0), (10, 2)], [(8, 5), (15, 5)], [(12, 2), (12, 7), (9, 15)], [(12, 8), (15, 15)]],
    '怪': [[(2, 0), (2, 15)], [(0, 4), (0, 7)], [(4, 4), (3, 6)],
          [(7, 1), (13, 1), (8, 7)], [(9, 2), (15, 8)], [(8, 10), (14, 10)], [(11, 8), (11, 15)], [(6, 15), (15, 15)]],
    'の': [[(8, 3), (7, 9), (4, 13), (2, 12), (1, 8), (3, 4), (7, 2), (11, 2), (14, 5), (15, 9), (13, 13), (10, 15)]],
    '道': [[(1, 0), (2, 1)], [(0, 4), (3, 4), (1, 10)], [(1, 11), (4, 14), (15, 15)],
          [(7, 0), (8, 1)], [(13, 0), (12, 1)], [(5, 2), (15, 2)], [(10, 2), (9, 4)],
          [(7, 4), (7, 12)], [(7, 4), (13, 4), (13, 12)], [(7, 7), (13, 7)], [(7, 10), (13, 10)], [(7, 12), (13, 12)]],
}


def glyph(ch):
    im = Image.new('1', (16, 16), 0)
    d = ImageDraw.Draw(im)
    for st in KANJI[ch]:
        d.line(st, fill=1, width=1)
    return np.array(im, bool)


def grow(m, n=1):
    for _ in range(n):
        o = m.copy()
        o[1:] |= m[:-1]; o[:-1] |= m[1:]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]
        m = o
    return m


def seal():
    """Hanko: roter Stein mit weißen Kanji (rechte Spalte zuerst: 妖怪 | の道), unregelmäßiger Rand."""
    S = 2                       # Kanji-Raster 16 -> 32 Hi-Res-Pixel
    n = 16 * S
    pad, gap = 5, 3
    w = h = pad * 2 + n * 2 + gap
    a = np.zeros((h, w, 4), np.uint8)
    a[:, :] = V
    a[-3:, :] = Vd; a[:, -3:] = Vd                    # Schattenkante unten rechts
    a[:2, :-3] = Vl; a[:-3, :2] = Vl                  # Licht oben links
    # ausgefranste Ecken wie gestempelt
    for y, x in ((0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1), (0, 9), (h - 1, 22), (14, w - 1), (31, 0)):
        a[y, x] = 0
    for (cx, cy), ch in (((pad + n + gap, pad), '妖'), ((pad + n + gap, pad + n + gap), '怪'),
                         ((pad, pad), 'の'), ((pad, pad + n + gap), '道')):
        g = np.kron(glyph(ch), np.ones((S, S), bool))
        sub = a[cy:cy + n, cx:cx + n]
        sub[g] = PAPER
    return a


def title_text():
    f = ImageFont.truetype(os.path.join(ROOT, 'fonts', 'YokaiFude.ttf'), 64)
    txt = 'Yōkai no Michi'
    bb = f.getbbox(txt)
    w, h = bb[2] - bb[0] + 8, bb[3] - bb[1] + 8
    im = Image.new('L', (w, h), 0)
    ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), txt, font=f, fill=255)
    return grow(np.array(im) > 110, 1)          # etwas fetter, damit der Pinselstrich trägt


def build():
    m = title_text()
    sl = seal()
    th, tw = m.shape
    sh_, sw = sl.shape[:2]
    W, H = tw + sw + 18, max(th, sh_) + 8
    out = np.zeros((H, W, 4), np.uint8)
    ty = (H - 8 - th) // 2 + 2
    big = np.zeros((H, W), bool)
    big[ty:ty + th, 2:2 + tw] = m
    ring = grow(big, 2)
    shadow = np.zeros_like(ring)
    shadow[4:, 4:] = ring[:-4, :-4]
    out[shadow] = SHADOW
    out[ring] = K
    # Gold in harten Bändern von oben nach unten, je Buchstabenzeile
    rows = np.where(big.any(1))[0]
    y0, y1 = rows.min(), rows.max()
    for y in range(y0, y1 + 1):
        f = (y - y0) / max(1, y1 - y0)
        c = GOLD[1] if f < 0.38 else GOLD[2] if f < 0.6 else GOLD[3] if f < 0.85 else GOLD[4]
        out[y][big[y]] = c
    # Fase: Oberkanten hell, Unterkanten/rechts dunkel (Licht oben links)
    top = big & ~np.roll(big, 1, 0)
    left = big & ~np.roll(big, 1, 1)
    bot = big & ~np.roll(big, -1, 0)
    out[top | left] = GOLD[0]
    out[bot] = GOLD[4]
    # Siegel rechts daneben, leicht tiefer gesetzt
    sx, sy = 2 + tw + 12, H - 5 - sh_
    out[sy + 3:sy + 3 + sh_, sx + 3:sx + 3 + sw][sl[..., 3] > 0] = SHADOW
    reg = out[sy:sy + sh_, sx:sx + sw]
    reg[sl[..., 3] > 0] = sl[sl[..., 3] > 0]
    os.makedirs(DST, exist_ok=True)
    Image.fromarray(out, 'RGBA').save(os.path.join(DST, 'logo.png'))
    bg = Image.new('RGBA', (W + 20, H + 20), (20, 16, 44, 255))
    bg.alpha_composite(Image.fromarray(out, 'RGBA'), (10, 10))
    bg.resize(((W + 20) * 3, (H + 20) * 3), Image.NEAREST).save(os.path.join(HERE, 'preview_logo.png'))
    print('logo', W, H)


if __name__ == '__main__':
    build()
