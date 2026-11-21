"""Kotarō aus dem KI-Bogen kotaro_sheet.jpg (3×4-Raster: Laufen; Ruhe, Ausholen, Fächerstoß, Nachschwung; Ducken, Ball, Ball, –)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('kotaro_sheet.jpg').convert('RGB')).astype(int)
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
walk, atk, roll = grid_boxes(fg, rows=3)
# Windbogen und Staub ragen übers Raster: Angriffsbilder von Hand begrenzt. Letztes Rollbild ist kein Ball.
y0, y1 = atk[0][1], atk[0][3]
atk = [(690, y0, 1200, y1), (1300, y0, 2040, y1), (2040, y0, 2576, y1)]
build('kotaro', im, fg, walk + atk, target_h=0, k=1 / 5.36, roll=roll[:3])  # Bogen hat ein ~5,36-px-Kunstpixelraster
