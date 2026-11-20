"""Kappa aus dem SpriteCook-Bogen (kappa_sheet.png: 4 Laufbilder + 3 Angriffsbilder auf dunklem Grund)
→ kappa_walk.png / kappa_attack.png im Format von import_fable.py (Blick nach links, Hi-Res-Pixeldichte)."""
import numpy as np
from PIL import Image
from prep import build

SRC = 'kappa_sheet.png'
TARGET_H = 56                     # Höhe der Laufbilder in Hi-Res-Pixeln (wie der bisherige Kappa)
BG_TOL = 34

im = np.array(Image.open(SRC).convert('RGB')).astype(int)
bg = im[2, 2]
fg = np.abs(im - bg).sum(2) > BG_TOL
fg[:, 1015:] = False             # shortcut: Randrauschen des Screenshots rechts, bei echtem SpriteCook-PNG entfernen

# Bildgrenzen an Spaltenlücken; die beiden mittleren Angriffsbilder berühren sich (Wasserstrahl) → an der dünnsten Stelle trennen
occ = fg.sum(0)
segs, s = [], None
for x, v in enumerate(occ):
    if v and s is None:
        s = x
    if not v and s is not None:
        segs.append([s, x]); s = None
if s is not None:
    segs.append([s, len(occ)])
segs = [g for g in segs if g[1] - g[0] > 20]
if len(segs) == 6:
    i = max(range(6), key=lambda k: segs[k][1] - segs[k][0])
    a, b = segs[i]
    cut = a + 100 + int(np.argmin(occ[a + 100:b - 100]))
    segs[i:i + 1] = [[a, cut], [cut, b]]
assert len(segs) == 7, segs

rows = np.where(fg.any(1))[0]
top, bot = rows.min(), rows.max() + 1
build('kappa', im, fg, [(a, top, b, bot) for a, b in segs], TARGET_H)
