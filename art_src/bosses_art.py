"""Bosse – eigene, große Pixel-Art (40–64 px), gebaut mit pixelstudio (MIT).

Gleiche Regeln wie bei den Gegnern: Blick nach links, Licht oben links,
hue-verschobene Rampen, gemeinsamer Außenumriss, 2 Bilder pro Animation.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from monsters import (R, blob, flame, legs2, mix, render_with, INK, WHITE, OUT,  # noqa: E402
                      GREEN, BLUE, RED, PINK, PURPLE, BROWN, TAN, GRAY, BONE, CLOTH, FIRE, SOUL, DARK, SKIN)

GOLD = R('#e0b040', hs=20, dark=0.4, light=0.6)
HAIR = R('#2a2236', hs=16, dark=0.4, light=0.45)


def fang_mouth(s, x0, y0, x1, y1, k=0):
    s.ellipse(x0, y0, x1, y1 + k, '#4a1424')
    for x in range(x0 + 1, x1, 2):
        s.px(x, y0, WHITE)
        s.px(x, y1 + k, WHITE)


def big_eye(s, x, y, iris='#ffd84a', w=3, h=2):
    s.ellipse(x, y, x + w, y + h, WHITE)
    s.rect(x + 1, y + h // 2, x + w - 1, y + h // 2 + (1 if h > 2 else 0), iris)
    s.px(x + 1, y + h // 2, INK)


# ------------------------------------------------------------------ Ebene 1
def kappa_ou(s, k):
    """Kappa-König: großer Kappa mit Panzer, Wasserteller, goldener Krone, Schwimmhäuten."""
    G = R('#4f9a4a', hs=18)
    by = k
    # Beine
    for x, d in ((14, 0), (30, 1)):
        yy = 44 - (k if d else 1 - k)
        s.rect(x, 38, x + 5, yy, G[0]); s.polygon([(x - 3, yy + 1), (x + 8, yy + 1), (x + 6, yy - 1), (x - 1, yy - 1)], G[0])
    # Panzer hinten
    blob(s, 24, 14 + by, 47, 42, BROWN)
    for (x0, y0, x1, y1) in ((28, 19, 43, 24), (27, 27, 44, 32), (29, 35, 42, 39)):
        s.line(x0, y0 + by, x1, y1 + by, BROWN[0])
    s.line(35, 16 + by, 34, 41 + by, BROWN[0])
    s.line(26, 20 + by, 26, 36 + by, BROWN[2])
    # Körper
    blob(s, 8, 16 + by, 34, 42, G)
    s.ellipse(12, 24 + by, 26, 40, mix(G[2], '#f0e8a0', 0.55), only=G[1])
    for y in (28, 32, 36):
        s.line(14, y + by, 24, y + by, mix(G[1], '#c8c070', 0.4))
    # Arme mit Schwimmhäuten
    s.polygon([(10, 22 + by), (4, 30 + by + k), (2, 36 + by + k), (8, 34 + by), (13, 27 + by)], G[1])
    s.polygon([(0, 35 + by + k), (2, 39 + by + k), (5, 37 + by + k), (7, 40 + by + k), (8, 34 + by)], G[0])
    s.polygon([(32, 22 + by), (38, 29 + by), (35, 31 + by), (30, 27 + by)], G[0])
    # Kopf
    blob(s, 6, 2 + by, 34, 24 + by, G)
    s.ellipse(8, 14 + by, 22, 23 + by, mix(G[2], '#f0e8a0', 0.4), only=G[1])
    # Schnabel (kurz, breit, gelb)
    s.polygon([(3, 14 + by), (12, 12 + by), (14, 17 + by), (11, 20 + by), (4, 18 + by)], '#e8b030')
    s.line(4, 16 + by, 13, 16 + by, '#a06a14'); s.line(5, 14 + by, 10, 13 + by, '#ffe07a')
    # Augen
    big_eye(s, 10, 7 + by, '#ff8a2a', 4, 3)
    big_eye(s, 19, 7 + by, '#ff8a2a', 4, 3)
    s.line(9, 6 + by, 14, 7 + by, G[0]); s.line(24, 6 + by, 19, 7 + by, G[0])
    # Haarkranz + Wasserteller + Krone
    for x in range(6, 35, 3):
        s.polygon([(x, 6 + by), (x + 1, 1 + by), (x + 3, 6 + by)], '#2a4a3a')
    s.ellipse(10, 0 + by, 30, 6 + by, '#7ac8e8'); s.ellipse(12, 1 + by, 28, 4 + by, '#b8ecff'); s.line(15, 2 + by, 20, 2 + by, WHITE)
    s.polygon([(12, 0 + by), (12, -6 + by), (16, -2 + by), (20, -8 + by), (24, -2 + by), (28, -6 + by), (28, 0 + by)], GOLD[2])
    s.polygon([(20, -8 + by), (24, -2 + by), (28, -6 + by), (28, 0 + by), (20, 0 + by)], GOLD[1])
    s.line(12, 0 + by, 28, 0 + by, GOLD[0])
    s.px(20, -3 + by, '#e04050'); s.px(13, -5 + by, WHITE)


def omukade_head(s, k):
    C = R('#b8483a', hs=16)
    for i, y in enumerate((14, 18)):
        d = (i + k) % 2
        s.line(6, y, 0, y + 3 - d, C[0]); s.line(18, y, 23, y + 3 - d, C[0])
    blob(s, 3, 4, 21, 22, C)
    s.line(5, 13, 19, 13, C[0])
    s.polygon([(5, 18), (2, 24), (8, 21)], '#e8d070'); s.polygon([(19, 18), (22, 24), (16, 21)], '#d8c060')
    s.ellipse(5, 8, 9, 11, '#ffd84a'); s.ellipse(15, 8, 19, 11, '#ffd84a'); s.px(7, 10, INK); s.px(16, 10, INK)
    s.line(8, 4, 3, -1 + 1 + k, C[1]); s.line(16, 4, 21, 0 + k, C[1])


def omukade_seg(s, k):
    C = R('#5a3a4a', hs=16)
    for i, y in enumerate((8, 12)):
        d = (i + k) % 2
        s.line(4, y, -1 + 1, y + 4 - d * 2, '#d8a040'); s.line(15, y, 19, y + 4 - (1 - d) * 2, '#d8a040')
    blob(s, 2, 3, 17, 16, C)
    s.line(4, 9, 15, 9, C[0]); s.line(5, 5, 11, 5, C[2])


def jorogumo(s, k):
    """Spinnenfrau: Oberkörper einer Frau im Kimono auf einem Spinnenleib."""
    B = R('#3a2e4a', hs=18)
    K_ = R('#b83a5a', hs=18)
    for i, (x, dx) in enumerate(((16, -14), (20, -12), (34, 12), (40, 12))):
        d = (i + k) % 2
        mx, my = x + dx, 22 - d * 2
        s.line(x, 30, mx, my, B[0]); s.line(x, 31, mx, my + 1, B[0])
        s.line(mx, my, mx + (3 if dx < 0 else -3), 44, B[0])
        s.px(mx, my, '#e8c040')
    blob(s, 18, 22, 50, 44, B)                                          # Hinterleib
    s.polygon([(30, 26), (34, 30), (38, 26), (34, 38)], '#e8c040'); s.line(34, 30, 34, 37, '#b8402a')
    blob(s, 12, 26, 30, 40, B)
    # Frau
    s.polygon([(12, 14), (28, 14), (30, 30), (10, 30)], K_[1]); s.polygon([(22, 14), (28, 14), (30, 30), (24, 30)], K_[0])
    s.line(20, 14, 14, 30, '#f2e0a0'); s.rect(11, 22, 29, 24, '#2a1e3a')
    for x, y in ((14, 18), (25, 27), (17, 27)):
        s.px(x, y, '#f8c0d0')
    s.polygon([(12, 16), (5, 22 + k), (4, 26 + k), (8, 25), (14, 20)], K_[1])
    s.polygon([(4, 26 + k), (2, 24 + k), (5, 23 + k)], SKIN[1])
    blob(s, 13, 2, 27, 15, SKIN)
    s.ellipse(11, 0, 29, 7, HAIR[1]); s.rect(11, 4, 14, 20, HAIR[1]); s.rect(26, 4, 29, 22, HAIR[0])
    s.line(14, 1, 20, 0, HAIR[2])
    s.polygon([(17, 0), (20, -4), (23, 0)], HAIR[1]); s.px(25, -1, '#e8c040'); s.line(24, -2, 28, -4, '#e8c040')
    s.line(15, 8, 18, 9, INK); s.line(22, 9, 25, 8, INK); s.px(17, 9, '#ff3a5a'); s.px(23, 9, '#ff3a5a')
    s.px(20, 12, '#c83a4a'); s.px(19, 12, '#c83a4a')


def gashadokuro(s, k):
    """Riesenskelett: großer Schädel, Rippen, Knochenarme."""
    B = BONE
    # Rippen/Wirbel
    s.line(32, 36, 32, 60, B[0]); s.line(33, 36, 33, 60, B[1])
    for i, y in enumerate(range(38, 58, 4)):
        w = 14 - abs(i - 2) * 2
        s.ellipse(32 - w, y, 32 + w, y + 5, B[1], fill=False); s.ellipse(32 - w, y + 1, 32 + w, y + 5, B[0], fill=False)
    s.ellipse(22, 57, 42, 63, B[1])
    # Arme
    for side in (-1, 1):
        sx = 32 + side * 16
        ex, ey = 32 + side * 26, 46 - (k * 3 if side < 0 else (1 - k) * 3)
        s.line(sx, 36, ex, ey, B[1]); s.line(sx, 37, ex, ey + 1, B[0])
        s.line(ex, ey, ex - side * 2, ey + 12, B[1]); s.line(ex + 1, ey, ex - side * 2 + 1, ey + 12, B[0])
        for f in range(3):
            s.line(ex - side * 2 + f - 1, ey + 12, ex - side * 2 + f * 2 - 2, ey + 16, B[1])
        s.circle(ex, ey, 2, B[2], fill=True)
    s.ellipse(14, 32, 50, 40, B[1]); s.line(16, 34, 48, 34, B[2]); s.ellipse(14, 37, 50, 40, B[0], only=B[1])
    # Schädel
    blob(s, 10, 0, 54, 34, B)
    s.ellipse(15, 12, 28, 24, '#1a1020'); s.ellipse(36, 12, 49, 24, '#1a1020')
    s.ellipse(19, 16, 24, 21, '#ff5a3a' if k else '#ff8a3a'); s.ellipse(40, 16, 45, 21, '#ff5a3a' if k else '#ff8a3a')
    s.px(20, 17, '#ffe07a'); s.px(41, 17, '#ffe07a')
    s.polygon([(29, 24), (32, 20), (35, 24), (32, 27)], '#1a1020')
    s.rect(18, 29, 46, 33, '#1a1020')
    for x in range(19, 46, 3):
        s.rect(x, 28, x + 1, 30, B[2]); s.rect(x, 32, x + 1, 34, B[1])
    for x0, y0, x1, y1 in ((14, 6, 20, 11), (44, 4, 48, 10)):
        s.line(x0, y0, x1, y1, B[0])


def rokuro_head(s, k):
    """Kopf der Rokurokubi (am langen Hals)."""
    blob(s, 3, 3, 21, 22, SKIN)
    s.ellipse(1, 0, 23, 9, HAIR[1]); s.rect(1, 4, 4, 22, HAIR[1]); s.rect(20, 4, 23, 22, HAIR[0])
    s.ellipse(5, -1 + 1, 19, 4, HAIR[1]); s.line(5, 1, 10, 0, HAIR[2])
    s.rect(9, -3 + 3, 15, 1, HAIR[1]); s.px(16, 0, '#e04a5a'); s.line(16, 0, 20, -2 + 2, '#e8c040')
    s.line(6, 11, 9, 12, INK); s.line(15, 12, 18, 11, INK)
    s.rect(7, 12, 8, 13, INK); s.rect(16, 12, 17, 13, INK); s.px(7, 12, WHITE); s.px(16, 12, WHITE)
    s.ellipse(9, 16, 15, 19 + k, '#7a1a2a'); s.line(10, 16, 14, 16, '#e05a6a')
    s.px(6, 15, '#f08aa0'); s.px(18, 15, '#f08aa0')


def rokuro_body(s, k):
    K_ = R('#a83a5a', hs=18)
    s.polygon([(4, 6), (28, 6), (32, 30), (0, 30)], K_[1]); s.polygon([(18, 6), (28, 6), (32, 30), (20, 30)], K_[0])
    s.line(16, 6, 10, 30, '#f2e0a0'); s.rect(3, 15, 29, 18, '#2a1e3a'); s.rect(13, 14, 19, 19, '#e8c040')
    for x, y in ((7, 10), (24, 24), (12, 25), (26, 11)):
        s.px(x, y, '#f8c0d0'); s.px(x + 1, y + 1, '#f8c0d0')
    s.polygon([(4, 8), (-1 + 1, 18), (4, 20), (7, 12)], K_[1]); s.polygon([(28, 8), (32, 18), (28, 20), (25, 12)], K_[0])
    s.ellipse(11, 0, 21, 8, SKIN[1]); s.ellipse(12, 0, 20, 4, SKIN[2])


def nue(s, k):
    """Nue: Affengesicht, Tanuki-Leib, Tigerbeine, Schlangenschwanz."""
    T = R('#d8a040', hs=18)
    Bd = R('#8a6a4a', hs=14)
    # Schlangenschwanz
    pts = [(40 + i * 2, 18 - int(math.sin(i * 0.9 + k) * 4) - i) for i in range(5)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        s.line(x0, y0, x1, y1, GREEN[1]); s.line(x0, y0 + 1, x1, y1 + 1, GREEN[0])
    hx, hy = pts[-1]
    s.ellipse(hx - 2, hy - 3, hx + 3, hy + 1, GREEN[1]); s.px(hx - 1, hy - 2, '#ff3a3a'); s.line(hx - 3, hy - 1, hx - 4, hy, '#e04a5a')
    # Tigerbeine
    for x, d in ((8, 0), (14, 1), (30, 0), (36, 1)):
        yy = 38 - ((k + d) % 2)
        s.rect(x, 28, x + 4, yy, T[1]); s.line(x, 31, x + 4, 31, INK); s.line(x, 34, x + 4, 34, INK)
        s.rect(x - 1, yy, x + 4, yy + 1, T[0])
    blob(s, 6, 12, 44, 34, Bd)
    s.ellipse(10, 24, 36, 33, mix(Bd[2], '#f0dcc0', 0.5), only=Bd[1])
    # Affenkopf
    blob(s, 0, 2, 20, 22, R('#7a5a4a', hs=14))
    s.ellipse(3, 7, 17, 20, '#e8a888')
    s.polygon([(1, 4), (0, -1 + 1), (4, 3)], R('#7a5a4a')[1]); s.polygon([(16, 3), (20, -1 + 1), (19, 5)], R('#7a5a4a')[0])
    s.rect(5, 10, 7, 12, INK); s.rect(12, 10, 14, 12, INK); s.px(5, 10, '#ffd84a'); s.px(12, 10, '#ffd84a')
    fang = 18 + k
    s.ellipse(6, 15, 14, fang, '#5a1a2a'); s.px(7, 15, WHITE); s.px(13, 15, WHITE)


def sojobo(s, k):
    """Sōjōbō, König der Tengu: rotes Gesicht, lange Nase, weißes Haar, Flügel, Federfächer."""
    Wg = R('#3a3448', hs=18, dark=0.35, light=0.5)
    fl = [0, -3][k]
    for side, x0 in ((1, 30), (-1, 18)):
        tip = (x0 + side * 18, 2 + fl)
        s.polygon([(x0, 16), tip, (x0 + side * 20, 18 + fl), (x0 + side * 14, 30), (x0 + side * 4, 30)], Wg[0] if side > 0 else Wg[1])
        for j in range(3):
            s.line(x0 + side * 2, 18 + j * 4, x0 + side * (16 - j * 2), 6 + j * 6 + fl, Wg[2])
    # Gewand (Yamabushi)
    Cl = R('#e8e4d8', hs=12, dark=0.28, light=0.5)
    s.polygon([(14, 20), (34, 20), (38, 46), (10, 46)], Cl[1]); s.polygon([(26, 20), (34, 20), (38, 46), (28, 46)], Cl[0])
    s.rect(10, 40, 38, 46, R('#6a4a8a')[1])
    for x in (17, 22, 27, 32):
        s.circle(x, 24, 1, '#e0a020', fill=True)
    s.line(13, 32, 35, 32, '#c8a24a')
    # Fächer
    s.line(6, 34, 8, 26, '#6a4a32')
    s.polygon([(8, 26), (0, 12 + k), (6, 9 + k), (12, 10 + k), (14, 20)], '#5a7a4a')
    for x in (2, 6, 10):
        s.line(8, 26, x, 11 + k, '#3a5a2a')
    s.rect(6, 26, 10, 30, R('#d84a3a')[1])
    # Kopf: erst Haar, dann Gesicht, Nase, Bart
    Fc = R('#d84a3a', hs=14)
    s.ellipse(12, 0, 36, 10, '#f2f0f6'); s.rect(12, 4, 16, 20, '#f2f0f6'); s.rect(32, 4, 36, 20, '#d8d8e4')
    s.line(14, 1, 22, 0, WHITE)
    blob(s, 15, 5, 33, 22, Fc)
    s.line(17, 9, 22, 10, WHITE); s.line(26, 10, 31, 9, WHITE)
    s.rect(19, 11, 20, 12, INK); s.rect(27, 11, 28, 12, INK); s.px(19, 11, '#ffd84a'); s.px(27, 11, '#ffd84a')
    s.polygon([(16, 17), (32, 17), (31, 27), (24, 31), (17, 27)], '#f2f0f6')       # Bart
    s.line(20, 20, 21, 28, '#c8c8d8'); s.line(27, 20, 27, 29, '#c8c8d8')
    s.polygon([(20, 13), (2, 15), (2, 17), (20, 17)], Fc[1]); s.line(3, 15, 19, 14, Fc[2]); s.line(3, 17, 19, 17, Fc[0])
    s.rect(21, -2, 27, 3, '#1c1a24'); s.line(22, -1, 25, -1, '#3c3a4c')


def raiju(s, k):
    """Raijū: Donnerwolf aus Blitzen."""
    C = R('#6ab0f0', hs=22, dark=0.45, light=0.8)
    # Schwanz als Blitz
    s.polygon([(36, 14), (44, 4 - k), (41, 11), (46, 10 - k), (38, 20)], '#ffe85a')
    blob(s, 10, 10, 40, 28, C)
    for x in (18, 25, 32):
        s.polygon([(x, 12), (x + 2, 17), (x - 1, 18), (x + 1, 24)], '#ffffff')
    for x, d in ((12, 0), (18, 1), (30, 0), (36, 1)):
        yy = 34 - ((k + d) % 2) * 2
        s.line(x, 24, x - 2, yy, C[0]); s.line(x + 1, 24, x - 1, yy, C[1]); s.line(x - 3, yy, x, yy, '#ffe85a')
    blob(s, 0, 4, 16, 20, C)
    s.polygon([(3, 6), (4, -1 + 1), (8, 5)], C[1]); s.polygon([(10, 5), (14, 0), (15, 8)], C[0])
    s.polygon([(0, 14), (-1 + 1, 12), (6, 12), (6, 16)], C[1])
    s.rect(4, 9, 6, 10, '#ffe85a'); s.px(4, 10, INK)
    s.line(1, 16, 6, 16, INK); s.px(2, 17, WHITE); s.px(5, 17, WHITE)
    for i in range(3):
        x, y = 6 + i * 13, 2 + (i + k) % 2 * 3
        s.line(x, y, x + 2, y + 3, '#fff6a0'); s.line(x + 2, y + 3, x, y + 5, '#fff6a0')


def yuki_onna(s, k):
    """Yuki-onna: Schneefrau mit weißem Kimono, langem schwarzem Haar, eisigem Atem."""
    Ki = R('#e8f0fa', hs=14, dark=0.3, light=0.5)
    Sk = R('#e8eef6', 3, hs=10, dark=0.2, light=0.4)
    sw = [0, 1][k]
    s.rect(6, 6, 26, 32, HAIR[0])                                                     # Haar hinten
    s.polygon([(8, 14), (24, 14), (30, 42), (22 + sw, 46), (16, 42), (10 + sw, 46), (2, 42)], Ki[1])
    s.polygon([(18, 14), (24, 14), (30, 42), (22 + sw, 46), (18, 42)], Ki[0])
    s.line(16, 14, 11, 42, '#a8c8e8'); s.rect(7, 24, 25, 26, '#8ab0d8')
    for x, y in ((10, 30), (22, 36), (14, 38), (20, 20)):
        s.px(x, y, WHITE); s.px(x - 1, y, '#c8e0ff'); s.px(x + 1, y, '#c8e0ff'); s.px(x, y - 1, '#c8e0ff'); s.px(x, y + 1, '#c8e0ff')
    s.polygon([(8, 16), (2, 26 + k), (6, 28 + k), (11, 20)], Ki[1])
    blob(s, 9, 2, 23, 16, Sk)
    s.ellipse(7, 0, 25, 7, HAIR[1]); s.rect(7, 3, 10, 34, HAIR[1]); s.rect(22, 3, 25, 34, HAIR[0])
    s.line(10, 1, 16, 0, HAIR[2])
    s.line(11, 8, 14, 9, '#3a5a8a'); s.line(18, 9, 21, 8, '#3a5a8a'); s.px(12, 9, '#7ac8ff'); s.px(20, 9, '#7ac8ff')
    s.px(16, 12, '#7a9ac8')
    # Eisatem
    for i in range(3):
        s.px(5 - i * 2, 12 + (i + k) % 2, '#c8ecff'); s.px(4 - i * 2, 13, '#ffffff')


def umibozu(s, k):
    """Umibōzu: riesiger schwarzer Meeresmönch, der aus den Wellen steigt."""
    U = R('#2a2c48', hs=18, dark=0.4, light=0.5)
    blob(s, 6, 0, 58, 56, U)
    s.ellipse(14, 18, 26, 26, WHITE); s.ellipse(38, 18, 50, 26, WHITE)
    s.ellipse(17, 20, 23, 25, '#ffe060'); s.ellipse(41, 20, 47, 25, '#ffe060')
    s.rect(19, 21, 21, 24, INK); s.rect(43, 21, 45, 24, INK); s.px(18, 20, WHITE); s.px(42, 20, WHITE)
    s.ellipse(26, 34, 38, 40 + k, '#120c1a')
    # Wellen
    W_ = R('#3a7ab8', hs=18, dark=0.4, light=0.7)
    for i in range(6):
        x = i * 11 - 2 + k * 3
        s.ellipse(x, 46, x + 14, 58, W_[1]); s.ellipse(x + 2, 46, x + 10, 50, W_[2])
        s.line(x + 3, 47, x + 7, 46, WHITE)
    s.rect(0, 54, 64, 58, W_[0])


# ------------------------------------------------------------------ Ebene 2–6
def ryujin_head(s, k):
    """Drachenkopf (Ryūjin): Hörner, Schnurrhaare, Mähne."""
    D_ = R('#3a9a8a', hs=20)
    s.polygon([(20, 6), (30, 2), (32, 10), (28, 22), (20, 22)], '#e8eef6')          # Mähne
    for y in (6, 11, 16):
        s.line(22, y, 31, y - 2 + (k if y == 11 else 0), '#c8d4e4')
    blob(s, 8, 4, 28, 24, D_)
    s.polygon([(10, 10), (0, 12), (0, 19), (11, 21)], D_[1]); s.line(1, 13, 10, 12, D_[2])
    s.line(0, 19, 11, 19, '#5a1a2a'); s.px(2, 20, WHITE); s.px(6, 20, WHITE)
    s.ellipse(1, 13, 3, 14, D_[0])
    s.polygon([(16, 5), (18, -3 + 3), (24, -4 + 4), (20, 3)], '#f2e0a0'); s.polygon([(22, 6), (28, 0), (31, 2), (25, 8)], '#e0c880')
    big_eye(s, 13, 9, '#ff5a3a', 3, 2)
    s.line(4, 18, -1 + 1, 24 + k, '#f2e0a0'); s.line(6, 18, 4, 25 - k, '#f2e0a0')
    for x in range(12, 27, 4):
        s.px(x, 22, '#e8c040')


def bake_kujira(s, k):
    """Bake-kujira: Skelettwal mit glühenden Augen."""
    B = BONE
    s.polygon([(52, 18), (63, 8 - k * 2), (60, 20), (63, 32 + k * 2), (52, 24)], B[1])
    s.line(53, 21, 62, 10 - k * 2, B[0]); s.line(53, 22, 62, 30 + k * 2, B[0])
    s.line(14, 22, 54, 20, B[0]); s.line(14, 21, 54, 19, B[1])                        # Wirbelsäule
    for x in range(20, 52, 5):
        h = 12 - abs(x - 32) // 3
        s.line(x, 20, x - 2, 20 + h, B[1]); s.line(x + 1, 20, x - 1, 20 + h, B[0])
        s.line(x, 19, x + 1, 19 - h // 2, B[1])
    blob(s, 0, 8, 26, 36, B)                                                          # Schädel
    s.polygon([(0, 26), (22, 28), (20, 36), (2, 34)], B[0])
    for x in range(2, 20, 3):
        s.line(x, 27, x + 1, 31, B[2])
    s.ellipse(8, 14, 16, 21, '#1a1020'); s.ellipse(10, 16, 14, 19, '#7ac8ff' if k else '#b8ecff')
    s.polygon([(12, 4), (18, 0), (22, 8)], B[1])
    for i in range(3):
        s.px(18 + i * 3, 4 - (i + k) % 2 * 2, '#c8ecff')


def orochi_head(s, k):
    """Kopf der achtköpfigen Schlange."""
    S = R('#4a8a4a', hs=18)
    blob(s, 4, 2, 22, 18, S)
    s.polygon([(6, 8), (0, 10), (0, 15), (8, 16)], S[1]); s.line(1, 11, 7, 10, S[2])
    s.line(0, 15, 9, 15, '#3a1a1a'); s.px(2, 16, WHITE); s.px(5, 16, WHITE)
    s.polygon([(10, 4), (14, -1 + 1), (16, 4)], '#e8e070')
    big_eye(s, 9, 6, '#ff3a2a', 3, 2)
    for x in range(12, 22, 3):
        s.line(x, 12, x + 1, 17, S[0])
    s.line(0, 13, -1 + 1, 17 + k, '#e04a5a')


def shuten_doji(s, k):
    """Shuten-dōji: Oni-König mit wilder Mähne, Hörnern, Prunkgewand und Sakeschale."""
    Rk = R('#d8503c', hs=16)
    Rb = R('#3a3a8a', hs=18)
    legs2(s, (14, 28), 46, k, Rk[0], h=3)
    s.polygon([(10, 22), (36, 22), (40, 46), (6, 46)], Rb[1]); s.polygon([(26, 22), (36, 22), (40, 46), (28, 46)], Rb[0])
    for x, y in ((12, 30), (22, 38), (32, 32), (16, 42)):
        s.circle(x, y, 2, GOLD[2]); s.px(x, y, GOLD[1])
    s.rect(8, 32, 38, 35, GOLD[1]); s.line(8, 32, 38, 32, GOLD[2])
    s.polygon([(10, 24), (2, 30 + k), (4, 34 + k), (12, 30)], Rb[1])
    s.ellipse(-1 + 1, 30 + k, 8, 34 + k, '#c83a3a'); s.ellipse(1, 30 + k, 7, 32 + k, '#ffe0a0')       # Sakeschale
    s.rect(34, 24, 38, 34, Rk[0])
    s.ellipse(4, 2, 42, 30, '#c8b0a0')                                                      # Mähne
    for x in range(6, 42, 4):
        s.line(x, 26, x - 2 + (x % 8) // 2, 31, '#a89080')
    blob(s, 12, 6, 34, 26, Rk)
    s.polygon([(13, 8), (8, -2 + 2), (17, 6)], '#f8f0d8'); s.polygon([(30, 6), (38, 0), (34, 9)], '#e8dcc0')
    s.line(15, 12, 20, 14, INK); s.line(31, 12, 26, 14, INK)
    s.rect(16, 14, 19, 15, '#ffe070'); s.rect(27, 14, 30, 15, '#ffe070'); s.px(18, 15, INK); s.px(28, 15, INK)
    fang_mouth(s, 17, 19, 29, 22, k)
    s.px(14, 18, Rk[0]); s.px(32, 18, Rk[0])


def tamamo(s, k):
    """Tamamo-no-Mae: Hofdame mit Fuchsohren und neun goldenen Schwänzen."""
    F = R('#f0b040', hs=20, dark=0.4, light=0.7)
    for i in range(9):
        a = math.pi * (1.15 + i / 8 * 0.75) + (0.05 if (i + k) % 2 else -0.05)
        L = 22
        x0, y0 = 26, 30
        x1, y1 = x0 - math.cos(a) * L, y0 + math.sin(a) * L
        s.line(x0, y0, int(x1), int(y1), F[1]); s.line(x0 + 1, y0, int(x1) + 1, int(y1), F[0])
        s.ellipse(int(x1) - 3, int(y1) - 3, int(x1) + 3, int(y1) + 3, F[2])
        s.ellipse(int(x1) - 1, int(y1) - 2, int(x1) + 2, int(y1) + 1, '#fffaf0')
    K_ = R('#c83a6a', hs=18)
    Kb = R('#f2e8d8', hs=10, dark=0.25, light=0.4)
    s.polygon([(16, 20), (32, 20), (38, 46), (10, 46)], K_[1]); s.polygon([(26, 20), (32, 20), (38, 46), (28, 46)], K_[0])
    s.polygon([(14, 26), (34, 26), (36, 46), (12, 46)], Kb[1], only=K_[1])
    s.line(24, 20, 18, 46, GOLD[2]); s.rect(12, 30, 36, 32, GOLD[1])
    s.polygon([(16, 22), (8, 34 + k), (12, 36 + k), (18, 28)], K_[1])
    blob(s, 17, 6, 31, 21, SKIN)
    s.ellipse(14, 4, 34, 12, '#f0d080'); s.rect(14, 8, 17, 26, '#f0d080'); s.rect(31, 8, 34, 26, '#e0c070')
    s.polygon([(15, 6), (16, -2 + 2), (21, 5)], F[1]); s.polygon([(27, 5), (32, 0), (33, 7)], F[0])
    s.px(17, 3, '#f8b0b0'); s.px(31, 3, '#f8b0b0')
    s.line(19, 12, 22, 13, INK); s.line(26, 13, 29, 12, INK); s.px(21, 13, '#c83a3a'); s.px(27, 13, '#c83a3a')
    s.px(24, 17, '#c83a4a')
    s.polygon([(20, 3), (24, -2 + 2), (28, 3)], GOLD[2]); s.px(24, 1, '#e04050')


def oonyudo(s, k):
    """Ō-nyūdō: riesiger Mönch in grauer Robe mit Gebetskette."""
    Rb = R('#6a6a7a', hs=14)
    Sk = R('#d8a888', 3, hs=12)
    s.polygon([(8, 22), (44, 22), (52, 62), (0, 62)], Rb[1]); s.polygon([(32, 22), (44, 22), (52, 62), (34, 62)], Rb[0])
    s.polygon([(16, 22), (30, 22), (22, 44)], R('#d8b070')[1])
    s.line(8, 24, 4, 60, Rb[2])
    for i in range(14):
        a = math.pi * (0.15 + i / 13 * 0.7)
        s.circle(26 + int(math.cos(a) * 14), 22 + int(math.sin(a) * 18), 1, '#7a3a2a' if i % 2 else '#a85a3a', fill=True)
    s.polygon([(8, 26), (0, 42 + k), (6, 46 + k), (14, 34)], Rb[1])
    s.ellipse(0, 42 + k, 8, 48 + k, Sk[1])
    blob(s, 12, 0, 40, 26, Sk)
    s.line(16, 9, 22, 11, INK); s.line(36, 9, 30, 11, INK)
    s.rect(18, 12, 21, 14, WHITE); s.rect(31, 12, 34, 14, WHITE); s.rect(19, 13, 20, 14, INK); s.rect(32, 13, 33, 14, INK)
    s.polygon([(24, 13), (27, 13), (28, 18), (23, 18)], Sk[0])
    s.ellipse(20, 20, 32, 24 + k, '#5a1a2a')
    s.px(26, 3, Sk[2]); s.line(18, 4, 24, 2, Sk[2])


def nurarihyon(s, k):
    """Nurarihyon: alter Herr der Yōkai mit langem kahlem Hinterkopf und edlem Haori."""
    Hk = R('#4a3a7a', hs=18)
    Sk = R('#e8c8a8', 3, hs=12)
    legs2(s, (11, 20), 44, k, '#2a2230', h=3)
    s.polygon([(6, 22), (30, 22), (34, 44), (2, 44)], Hk[1]); s.polygon([(20, 22), (30, 22), (34, 44), (22, 44)], Hk[0])
    s.polygon([(14, 22), (22, 22), (20, 44), (14, 44)], R('#8a7aa0')[1])
    for x, y in ((8, 28), (28, 36), (6, 40)):
        s.circle(x, y, 1, GOLD[2], fill=True)
    s.polygon([(8, 24), (2, 32 + k), (6, 34 + k), (12, 28)], Hk[1])
    s.line(2, 32 + k, -1 + 1, 26 + k, '#6a4a32'); s.rect(-1 + 1, 24 + k, 2, 26 + k, '#c8a040')       # Pfeife
    s.px(1, 22 + k, '#c8c8d0'); s.px(2, 20 + k, '#a8a8b8')
    s.ellipse(10, 0, 34, 16, Sk[1]); s.ellipse(20, 2, 34, 16, Sk[0], only=Sk[1]); s.ellipse(14, 1, 22, 5, Sk[2], only=Sk[1])
    blob(s, 8, 8, 24, 24, Sk)
    s.line(10, 13, 14, 14, '#f0f0f6'); s.line(18, 14, 22, 13, '#f0f0f6')
    s.px(12, 15, INK); s.px(20, 15, INK)
    s.polygon([(9, 18), (24, 18), (20, 26), (13, 26)], '#f0f0f6')
    s.line(13, 19, 19, 19, Sk[0])


def akkorokamui(s, k):
    """Akkorokamui: riesiger roter Krake."""
    O = R('#d8483c', hs=18)
    for i in range(7):
        x0 = 6 + i * 8
        sw = int(math.sin(i * 1.3 + k * 1.5) * 4)
        pts = [(x0, 34), (x0 + 6, 34), (x0 + 5 + sw, 46), (x0 + 3 - sw, 56), (x0 + 1 - sw, 56), (x0 + 1 + sw, 46)]
        s.polygon(pts, O[1] if i % 2 else O[0])
        for y in (40, 46, 52):
            s.px(x0 + 3 + (sw if y < 50 else -sw), y, '#f8c8b8')
    blob(s, 6, 0, 58, 40, O)
    for x, y in ((14, 10), (40, 6), (48, 20), (20, 24)):
        s.circle(x, y, 2, O[0])
    s.ellipse(16, 18, 26, 26, '#ffe070'); s.ellipse(38, 18, 48, 26, '#ffe070')
    s.rect(19, 19, 22, 25, INK); s.rect(41, 19, 44, 25, INK)
    s.ellipse(28, 28, 36, 34, '#5a1a2a')


def enma(s, k):
    """Enma-Daiō: König der Hölle, rotes Gesicht, schwarzer Bart, Richterhut, Shaku-Tafel."""
    Rb = R('#b83a3a', hs=16)
    Fc = R('#d86040', hs=14)
    s.polygon([(8, 24), (40, 24), (46, 54), (2, 54)], Rb[1]); s.polygon([(28, 24), (40, 24), (46, 54), (30, 54)], Rb[0])
    s.polygon([(16, 24), (32, 24), (24, 38)], GOLD[1])
    s.rect(4, 40, 44, 43, GOLD[1]); s.line(4, 40, 44, 40, GOLD[2])
    for x in (10, 22, 34):
        s.rect(x, 46, x + 4, 50, R('#2a2a5a')[1])
    s.polygon([(8, 26), (0, 36 + k), (6, 40 + k), (14, 32)], Rb[1])
    s.rect(0, 26 + k, 3, 40 + k, '#e8dcc0'); s.line(1, 27 + k, 1, 38 + k, '#c8b890')            # Shaku
    blob(s, 12, 8, 36, 30, Fc)
    s.polygon([(12, 20), (36, 20), (34, 32), (24, 36), (14, 32)], '#1e1a22')                   # Bart
    s.ellipse(18, 22, 30, 26, Fc[1])
    s.ellipse(20, 23, 28, 25 + k, '#5a1a1a')
    s.line(14, 13, 20, 15, INK); s.line(34, 13, 28, 15, INK)
    s.rect(16, 15, 19, 17, WHITE); s.rect(29, 15, 32, 17, WHITE); s.rect(17, 16, 18, 17, INK); s.rect(30, 16, 31, 17, INK)
    s.rect(8, 0, 40, 9, '#1c1a24'); s.rect(6, 8, 42, 10, '#1c1a24')                          # Hut
    s.rect(18, 2, 30, 7, GOLD[1])
    s.line(20, 3, 28, 3, '#5a1a1a'); s.line(20, 5, 28, 5, '#5a1a1a'); s.line(24, 3, 24, 7, '#5a1a1a'); s.line(20, 7, 28, 7, '#5a1a1a')


def izanami(s, k):
    """Izanami: Todesgöttin aus Yomi, verfallen, weißes Totengewand, violetter Schleier."""
    Ki = R('#e0dce8', hs=12, dark=0.3, light=0.45)
    Sk = R('#b8a8c0', 3, hs=12)
    sw = [0, 1][k]
    s.rect(8, 4, 32, 40, HAIR[0])
    s.polygon([(8, 16), (32, 16), (38, 48), (28 + sw, 50), (20, 46), (12 + sw, 50), (2, 48)], Ki[1])
    s.polygon([(22, 16), (32, 16), (38, 48), (28 + sw, 50), (24, 46)], Ki[0])
    s.line(20, 16, 14, 48, '#9a8aaa'); s.rect(6, 28, 34, 30, '#5a3a7a')
    s.polygon([(8, 18), (0, 30 + k), (4, 32 + k), (12, 24)], Ki[1])
    for j in range(3):
        s.line(0 + j, 30 + k, -1 + 1 + j, 34 + k, BONE[1])
    blob(s, 12, 3, 28, 18, Sk)
    s.ellipse(9, 0, 31, 8, HAIR[1]); s.rect(9, 4, 12, 40, HAIR[1]); s.rect(28, 4, 31, 42, HAIR[0])
    s.line(12, 1, 20, 0, HAIR[2])
    s.ellipse(14, 9, 18, 12, '#1a1020'); s.ellipse(22, 9, 26, 12, '#1a1020')
    s.px(16, 10, '#d07aff'); s.px(24, 10, '#d07aff')
    s.line(16, 15, 24, 15, '#4a2a4a'); s.px(17, 16, BONE[2]); s.px(23, 16, BONE[2])
    s.line(19, 4, 18, 8, '#7a6a8a')
    for i in range(4):
        s.px(4 + i * 10, 46 - (i + k) % 2 * 3, '#c87aff')


def kagutsuchi(s, k):
    """Kagutsuchi: Feuergott, ein Kind aus Flammen."""
    F2 = R('#f05a2a', hs=24, dark=0.35, light=0.75)
    for x, h in ((6, 18), (14, 26), (24, 32), (34, 26), (42, 18)):
        flame(s, x, 46, 6, h + (2 if (x // 8 + k) % 2 else 0), F2, k)
    Sk = R('#f0a060', 3, hs=14)
    s.polygon([(14, 24), (34, 24), (36, 44), (12, 44)], R('#c8302a')[1])
    s.rect(12, 32, 36, 34, GOLD[2])
    blob(s, 14, 6, 34, 26, Sk)
    for x in range(14, 36, 4):
        flame(s, x, 10, 3, 10 + (x % 3) * 2, F2, k)
    s.line(17, 14, 21, 15, INK); s.line(31, 14, 27, 15, INK)
    s.rect(18, 15, 21, 17, '#fff6a0'); s.rect(27, 15, 30, 17, '#fff6a0'); s.px(20, 16, '#c82a1a'); s.px(28, 16, '#c82a1a')
    s.ellipse(21, 20, 27, 23 + k, '#7a1a1a')
    s.polygon([(14, 26), (6, 30 + k), (8, 34 + k), (16, 30)], Sk[1])
    flame(s, 6, 34 + k, 3, 10, FIRE, k)


# ================================================================ Aufbau
# Name: (Breite, Höhe, Funktion, Extra-Rand oben)
BOSSES = {
    'boss_kappa_ou': (48, 46, kappa_ou, 9),
    'boss_omukade_head': (24, 25, omukade_head, 0),
    'boss_omukade_seg': (20, 18, omukade_seg, 0),
    'boss_jorogumo': (52, 45, jorogumo, 5),
    'boss_gashadokuro': (64, 64, gashadokuro, 0),
    'boss_rokuro_head': (24, 23, rokuro_head, 0),
    'boss_rokuro_body': (32, 31, rokuro_body, 0),
    'boss_nue': (50, 40, nue, 2),
    'boss_sojobo': (52, 47, sojobo, 4),
    'boss_raiju': (48, 36, raiju, 0),
    'boss_yuki_onna': (32, 47, yuki_onna, 0),
    'boss_umibozu': (64, 59, umibozu, 0),
    'boss_ryujin_head': (32, 25, ryujin_head, 4),
    'boss_bake_kujira': (64, 37, bake_kujira, 0),
    'boss_orochi_head': (22, 19, orochi_head, 2),
    'boss_shuten_doji': (42, 48, shuten_doji, 2),
    'boss_tamamo': (48, 47, tamamo, 2),
    'boss_oonyudo': (52, 63, oonyudo, 0),
    'boss_nurarihyon': (34, 46, nurarihyon, 0),
    'boss_akkorokamui': (64, 57, akkorokamui, 0),
    'boss_enma': (46, 54, enma, 0),
    'boss_izanami': (40, 51, izanami, 0),
    'boss_kagutsuchi': (48, 47, kagutsuchi, 8),
}


def render(name, k):
    from monsters import render_with as rw
    w, h, fn, top = BOSSES[name]
    return rw(w, h, fn, k, pad=2, top=top)


def build_all(out_dir):
    from PIL import Image
    meta = {}
    for name in BOSSES:
        frames = [render(name, k) for k in range(2)]
        w, h = frames[0].size
        strip = Image.new('RGBA', (w * 2, h), (0, 0, 0, 0))
        for i, im in enumerate(frames):
            strip.paste(im, (i * w, 0))
        strip.save(os.path.join(out_dir, name + '.png'))
        meta[name] = {'kind': 'strip', 'w': w, 'h': h, 'n': 2}
    return meta


def contact(path, names=None, scale=3):
    from PIL import Image
    names = names or list(BOSSES)
    ims = [[render(n, k) for k in range(2)] for n in names]
    cw = max(sum(i.width for i in fr) + 8 for fr in ims)
    ch = max(fr[0].height for fr in ims) + 6
    cols = 3
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new('RGBA', (cw * cols, ch * rows), (66, 84, 76, 255))
    for i, fr in enumerate(ims):
        x, y = (i % cols) * cw, (i // cols) * ch
        for im in fr:
            sheet.alpha_composite(im, (x, y + ch - 3 - im.height))
            x += im.width + 3
    sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST).save(path)


if __name__ == '__main__':
    contact(sys.argv[1] if len(sys.argv) > 1 else '/tmp/prev/bosses.png', sys.argv[2:] or None)
