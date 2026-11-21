"""Okiku aus dem KI-Bogen okiku_sheet.jpg (3×4-Raster: Schweben; Ruhe, Teller heben, Tellerwurf, Nachschwung; Sinken, –, Ball, –)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('okiku_sheet.jpg').convert('RGB')).astype(int)
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
walk, atk, roll = grid_boxes(fg, rows=3)
# Der geworfene Teller steht frei neben der Figur: Angriffsbilder von Hand begrenzt. Nur das mittlere Rollbild ist ein Ball.
y0, y1 = atk[0][1], atk[0][3]
atk = [(740, y0, 1120, y1), (1340, y0, 2014, y1), (2016, y0, 2560, y1)]
build('okiku', im, fg, walk + atk, target_h=0, k=1 / 5.36, roll=[roll[0], roll[2]])  # Bogen hat ein ~5,36-px-Kunstpixelraster
