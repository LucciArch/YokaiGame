"""Kappa aus dem SpriteCook-Bogen (kappa_sheet.png: 4 Laufbilder + 3 Angriffsbilder auf dunklem Grund)
→ kappa_walk.png / kappa_attack.png im Format von import_fable.py (Blick nach links, Hi-Res-Pixeldichte)."""
import numpy as np
from PIL import Image

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
walk_h = max(np.ptp(np.where(fg[:, a:b].any(1))[0]) + 1 for a, b in segs[:4])
k = TARGET_H / walk_h             # Verkleinerung auf Spielgröße

cells = []
for a, b in segs:
    m = fg[top:bot, a:b]
    rgb = im[top:bot, a:b]
    rgba = np.dstack([rgb, m * 255]).astype(np.uint8)
    w, h = int(round((b - a) * k)) + 2, int(round((bot - top) * k)) + 2   # +2: Platz für den Umriss
    # Farben nur aus Vordergrund mitteln (sonst färbt der dunkle Grund die Kanten ein), Deckung als Alpha
    pre = Image.fromarray(np.dstack([rgb * m[..., None], m * 255]).astype(np.uint8)).resize((w, h), Image.BOX)
    p = np.array(pre).astype(float)
    al = p[..., 3:4] / 255
    col = np.where(al > 0, p[..., :3] / np.maximum(al, 1e-6), 0)
    out = np.dstack([np.clip(col, 0, 255), (al[..., 0] > 0.5) * 255]).astype(np.uint8)
    pad = Image.new('RGBA', (w + 2, h + 2)); pad.paste(Image.fromarray(out), (1, 1))
    cells.append(pad.transpose(Image.FLIP_LEFT_RIGHT))   # Spiel-Sprites blicken nach links

# gemeinsame Palette (gleiche Farben in allen Bildern), Pixelkanten hart
sheet = Image.new('RGBA', (sum(c.width for c in cells), max(c.height for c in cells)))
x = 0
for c in cells:
    sheet.paste(c, (x, 0)); x += c.width
pal = sheet.convert('RGB').quantize(48, method=Image.MEDIANCUT)
cells = [Image.merge('RGBA', (*c.convert('RGB').quantize(palette=pal, dither=0).convert('RGB').split(), c.split()[3]))
         for c in cells]

def tidy(c):
    """Einzelpixel-Krümel weg, dann 1-px-Umriss wie bei den übrigen Spielfiguren."""
    a = np.array(c)
    op = a[..., 3] > 0
    nb = sum(np.roll(np.roll(op, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - op
    op &= nb >= 2
    from scipy import ndimage
    lab, n = ndimage.label(op)
    if n > 1:                                         # nur Teile ab 12 px behalten (Figur, Wasserstrahl, Tropfen)
        sizes = ndimage.sum(op, lab, range(1, n + 1))
        op = np.isin(lab, [i + 1 for i, v in enumerate(sizes) if v >= 12])
    a[..., 3] = op * 255
    ring = ~op & (sum(np.roll(np.roll(op, dy, 0), dx, 1) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))) > 0)
    a[ring] = (18, 16, 26, 255)
    return Image.fromarray(a)


cells = [tidy(c) for c in cells]

# Zellen: Körper (Füße) mittig, damit der Wasserstrahl nicht verschiebt
def foot_cx(c):
    a = np.array(c)[..., 3] > 0
    ys = np.where(a.any(1))[0]
    feet = a[ys.max() - 6:ys.max() + 1]
    return int(np.where(feet.any(0))[0].mean())

H = max(c.height for c in cells)
half = max(max(foot_cx(c), c.width - foot_cx(c)) for c in cells) + 2
W = half * 2
out = []
for c in cells:
    cell = Image.new('RGBA', (W, H))
    cell.paste(c, (half - foot_cx(c), H - c.height))
    out.append(cell)
for name, fr in (('kappa_walk.png', out[:4]), ('kappa_attack.png', out[4:])):
    st = Image.new('RGBA', (W * len(fr), H))
    for i, f in enumerate(fr):
        st.paste(f, (i * W, 0))
    st.save(name)
assert all(f.getbbox() for f in out)
print('Zelle', (W, H), 'Maßstab', round(k, 3))
