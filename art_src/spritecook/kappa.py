"""Kappa aus dem KI-Bogen kappa_sheet.jpg (2×4-Raster: oben 4 Laufbilder, unten Ruhe, Schale heben, Wasserstrahl, Nachtropfen)."""
import numpy as np
from PIL import Image
from prep import build, grid_boxes

im = np.array(Image.open('kappa_sheet.jpg').convert('RGB')).astype(int)
from scipy import ndimage
# dunkles Haar liegt nah am Grund: niedrige Schwelle, JPG-Rauschen per Öffnen weg, Löcher füllen
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
top, bottom = grid_boxes(fg)
build('kappa', im, fg, top + bottom[1:], target_h=0, k=1 / (5.85 * 1.5))  # Kappa ist klein: 1,5 Kunstpixel je Spielpixel
build('kappa_small', im, fg, top + bottom[1:], target_h=0, k=1 / (5.85 * 2))  # junger Kappa (Kappa-Ōs Gefolge): dieselbe Figur, genau halbes Raster
