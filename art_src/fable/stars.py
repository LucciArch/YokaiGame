"""Mikaboshi: Sternenmuster auf dem dunklen Gewand + Sternenkrone über dem Kopf (Nachbearbeitung der Ableitung)."""
import random, sys
import numpy as np
from PIL import Image
GOLD, WH = (255, 226, 74, 255), (255, 251, 192, 255)
ROBE = [(0x1e, 0x1a, 0x48), (0x3a, 0x34, 0x78), (0x0a, 0x08, 0x20)]


def star(a, x, y, big=False):
    H, W = a.shape[:2]
    pts = [(0, 0, WH)] + [(dx, dy, GOLD) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    if big:
        pts += [(dx, dy, GOLD) for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2))]
    for dx, dy, c in pts:
        if 0 <= x + dx < W and 0 <= y + dy < H:
            a[y + dy, x + dx] = c


def process(path, n, seed=3):
    im = Image.open(path).convert('RGBA'); a = np.array(im)
    w = a.shape[1] // n
    for f in range(n):
        sub = a[:, f * w:(f + 1) * w]
        rng = random.Random(seed)
        robe = np.zeros(sub.shape[:2], bool)
        for c in ROBE:
            robe |= np.all(sub[:, :, :3] == c, axis=2)
        ys, xs = np.nonzero(robe)
        for k in range(min(7, len(ys))):
            i = rng.randrange(len(ys)); star(sub, xs[i], ys[i])
        op = np.nonzero(sub[:, :, 3])
        if len(op[0]):
            top = op[0].min(); cols = op[1][op[0] < top + 6]; cx = int(cols.mean())
            for j, dx in enumerate((-8, -4, 0, 4, 8)):
                star(sub, cx + dx, max(2, top - 4 + abs(dx) // 3), big=(dx == 0))
        a[:, f * w:(f + 1) * w] = sub
    Image.fromarray(a).save(path)


if __name__ == '__main__':
    d = '/home/claude/fable_art/heroes/'
    process(d + 'boss_mikaboshi.png', 1)
    process(d + 'boss_mikaboshi_walk.png', 4)
    process(d + 'boss_mikaboshi_attack.png', 3)
