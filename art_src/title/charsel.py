"""Charakterauswahl im Titelstil (Hi-Res-Ebene, doppelte Dichte):
pedestal – zweistufiges Steinpodest am Seeufer, Mondlicht von rechts, Moos und Risse
lock     – rotes Hanko-Siegel 封 („versiegelt“) für gesperrte Figuren
ink      – Goldtusche-Strich für die Wertebalken (schwarze Tusche verschwände in der Nacht)
usage: python3 charsel.py"""
import math
import random
import numpy as np
from PIL import Image, ImageDraw
from panorama import Canvas, hx, K
import logo

STONE = [hx(c) for c in ('#1c1a2c', '#2a2840', '#3a3852', '#4c4a66', '#62627e', '#8a8aa4')]
MOSS = [hx(c) for c in ('#1e3424', '#2e4e30', '#4a6e3c')]


def ell(w, h, cx, cy, rx, ry):
    yy, xx = np.mgrid[0:h, 0:w]
    return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1


def pedestal():
    W, H = 148, 64
    c = Canvas(W, H)
    rr = random.Random(3)
    cx = W // 2
    sh = ell(W, H, cx + 4, 54, 70, 8)                    # Schlagschatten auf dem Ufer
    c.a[sh] = (*K, 140)
    for top, bot, rx, ry in ((34, 50, 64, 10), (18, 32, 50, 8)):   # untere, obere Stufe
        face = np.zeros((H, W), bool)
        for y in range(top, bot + 1):
            face |= ell(W, H, cx, y, rx, ry) & (np.mgrid[0:H, 0:W][0] >= top)
        xs = np.mgrid[0:H, 0:W][1]
        f = (xs - (cx - rx)) / (2 * rx)                  # 0 links .. 1 rechts (Mond rechts)
        for lo, hi_, col in ((0, .3, STONE[0]), (.3, .62, STONE[1]), (.62, .86, STONE[2]), (.86, 1.01, STONE[3])):
            c.a[face & (f >= lo) & (f < hi_)] = (*col, 255)
        for k in range(-3, 4):                           # Fugen zwischen den Quadern, perspektivisch gebogen
            x = cx + int(rx * math.sin(k * 0.42))
            for y in range(top + 2, bot + int(ry * math.cos(k * 0.42)) - 1):
                if 0 <= x < W and face[y, x]:
                    c.a[y, x] = (*STONE[0], 255)
        lid = ell(W, H, cx, top, rx, ry)                  # Deckplatte
        c.a[lid] = (*STONE[3], 255)
        c.a[lid & ~ell(W, H, cx - 3, top + 1, rx - 4, ry - 2)] = (*STONE[4], 255)
        c.a[lid & ~ell(W, H, cx - 5, top + 2, rx - 2, ry - 1) & (xs > cx + rx * 0.35)] = (*STONE[5], 255)   # Mondkante
        c.a[ell(W, H, cx - 6, top + 1, rx * 0.55, ry * 0.5)] = (*STONE[2], 255)    # ausgetretene Mulde
        for _ in range(int(rx / 4)):                     # Moos an der Kante, auf der Schattenseite dichter
            a = rr.uniform(math.pi * 0.35, math.pi * 1.1)
            x, y = int(cx + rx * math.cos(a) * 0.96), int(top + ry * math.sin(a) * 0.96)
            for dx in range(rr.randint(2, 5)):
                for dy in range(rr.randint(1, 3)):
                    if 0 <= x + dx < W and 0 <= y + dy < H and c.a[y + dy, x + dx, 3] == 255:
                        c.a[y + dy, x + dx] = (*MOSS[(dy == 0) + (dx % 3 == 0)], 255)
        for _ in range(3):                               # Risse in der Stirnseite
            x, y = rr.randint(cx - rx + 8, cx + rx - 8), rr.randint(top + ry - 2, bot)
            for _ in range(rr.randint(3, 6)):
                if 0 <= y < H and face[y, x]:
                    c.a[y, x] = (*K, 255)
                y += 1; x += rr.choice((-1, 0, 1))
    c.outline()
    c.save('pedestal')


def lock():
    """封: links zwei 土 übereinander (圭), rechts 寸 – als weiße Striche im roten Stein."""
    strokes = [[(3, 0), (3, 6)], [(1, 3), (5, 3)], [(0, 6), (6, 6)],
               [(3, 8), (3, 14)], [(1, 10), (5, 10)], [(0, 14), (6, 13)],
               [(8, 4), (15, 4)], [(13, 0), (13, 15), (11, 14)], [(9, 8), (10, 10)]]
    im = Image.new('1', (16, 16), 0)
    d = ImageDraw.Draw(im)
    for st in strokes:
        d.line(st, fill=1)
    g = np.kron(np.array(im, bool), np.ones((2, 2), bool))
    n, pad = 32, 4
    w = n + pad * 2
    a = np.zeros((w, w, 4), np.uint8)
    a[:, :] = logo.V
    a[-2:, :] = logo.Vd; a[:, -2:] = logo.Vd
    a[:2, :-2] = logo.Vl; a[:-2, :2] = logo.Vl
    for y, x in ((0, 0), (0, w - 1), (w - 1, 0), (w - 1, w - 1), (0, 13), (w - 1, 27), (20, w - 1)):
        a[y, x] = 0
    a[pad:pad + n, pad:pad + n][g] = logo.PAPER
    Image.fromarray(a, 'RGBA').save(f'{logo.DST}/lock.png')


if __name__ == '__main__':
    pedestal()
    lock()
    logo.brush('ink', [hx(c) + (255,) for c in ('#3a2418', '#7a5430', '#b8904c', '#e8c47a')])
