"""Kappa-Ō aus dem KI-Bogen boss_kappa_ou_sheet.jpg (2×4-Raster: oben 4 Laufbilder, unten Ruhe, Ausholen, Wasserstrahl, Nachtropfen)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('boss_kappa_ou_sheet.jpg').convert('RGB')).astype(int)
# dunkles Moos am Panzer liegt nah am Grund: etwas niedrigere Schwelle
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 14, iterations=2))
top, bottom = grid_boxes(fg)
build('boss_kappa_ou', im, fg, top + bottom[1:], target_h=0, k=1 / 5.36, colors=96)  # Raster ~5,36 px; 96 Farben, sonst kippt das Blau des Wassers ins Grün
