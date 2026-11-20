"""Oni aus dem KI-Bogen oni_sheet.jpg (2×4-Raster: oben 4 Laufbilder, unten Ruhe, Ausholen, Schlag, Nachschwung)."""
import numpy as np
from PIL import Image
from prep import build

im = np.array(Image.open('oni_sheet.jpg').convert('RGB')).astype(int)
from scipy import ndimage
# dunkles Haar und schwarze Keule liegen nah am Grund: niedrige Schwelle, JPG-Rauschen per Öffnen weg, Löcher füllen
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
H, W = im.shape[:2]
cw, ch = W // 4, H // 2
cell = lambda c, r: (c * cw, r * ch, (c + 1) * cw, (r + 1) * ch)
build('oni', im, fg, [cell(c, 0) for c in range(4)] + [cell(c, 1) for c in (1, 2, 3)], target_h=100)
