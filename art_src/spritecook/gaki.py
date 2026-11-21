"""Gaki und kleiner Gaki aus dem KI-Bogen gaki_sheet.jpg (2×4-Raster: oben 4 Laufbilder, unten Ruhe, Ausholen, Kratzhieb, Nachschnappen)."""
import numpy as np
from PIL import Image
from prep import build, grid_boxes

im = np.array(Image.open('gaki_sheet.jpg').convert('RGB')).astype(int)
from scipy import ndimage
# graugrüne Haut hebt sich klar vom Grund ab
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
top, bottom = grid_boxes(fg)
build('gaki', im, fg, top + bottom[1:], target_h=0, k=1 / (6.1 * 1.5))  # Raster ~6,1 px; Gaki ist ein schwacher Frühgegner, also kleiner
build('gaki_small', im, fg, top + bottom[1:], target_h=0, k=1 / (6.1 * 2))  # gleiche Figur, genau halbes Raster
