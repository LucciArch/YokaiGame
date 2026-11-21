"""Kasha aus dem KI-Bogen kasha_sheet.jpg (2×4-Raster: oben 4 Laufbilder, unten Ruhe, Ausholen, Sprung mit Feuerhieb, Landen)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('kasha_sheet.jpg').convert('RGB')).astype(int)
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
# Bogen zeichnet unter jede Figur eine fast schwarze Bodenlinie: lange waagrechte Läufe in Fast-Schwarz entfernen
line = ndimage.binary_opening(im.sum(2) < 50, structure=np.ones((1, 150)))
fg &= ~ndimage.binary_dilation(line, iterations=3)
fg = ndimage.binary_opening(fg, iterations=2)
top, bottom = grid_boxes(fg)
build('kasha', im, fg, top + bottom[1:], target_h=0, k=1 / 5.36)  # Bogen hat ein ~5,36-px-Kunstpixelraster
