"""Oni aus dem KI-Bogen oni_sheet.jpg (2×4-Raster: oben 4 Laufbilder, unten Ruhe, Ausholen, Schlag, Nachschwung)."""
import numpy as np
from PIL import Image
from prep import build, grid_boxes

im = np.array(Image.open('oni_sheet.jpg').convert('RGB')).astype(int)
from scipy import ndimage
# dunkles Haar und schwarze Keule liegen nah am Grund: niedrige Schwelle, JPG-Rauschen per Öffnen weg, Löcher füllen
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
top, bottom = grid_boxes(fg)
build('oni', im, fg, top + bottom[1:], target_h=100)
