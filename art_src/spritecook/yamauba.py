"""Yamauba aus dem KI-Bogen yamauba_sheet.jpg (2×4-Raster: oben 4 Laufbilder, unten Ruhe, Ausholen, Hackbeil-Hieb, Nachschwung)."""
import numpy as np
from PIL import Image
from prep import build, grid_boxes

im = np.array(Image.open('yamauba_sheet.jpg').convert('RGB')).astype(int)
from scipy import ndimage
# graue Haare und Haut heben sich klar vom Grund ab
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
top, bottom = grid_boxes(fg)
build('yamauba', im, fg, top + bottom[1:], target_h=0, k=1 / 5.85)  # Bogen hat ein ~5,85-px-Kunstpixelraster
