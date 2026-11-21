"""Susanoo aus dem KI-Bogen susanoo_sheet.jpg (3×4-Raster: Laufen; Ruhe, Ausholen, Blitzhieb, Nachschwung; Ducken, Ball, Ball, Ball)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('susanoo_sheet.jpg').convert('RGB')).astype(int)
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
walk, atk, roll = grid_boxes(fg, rows=3)
# drei Ballbilder im Bogen, zwei genügen (Ball 2/3 = gedreht)
build('susanoo', im, fg, walk + atk[1:], target_h=0, k=1 / 5.36, roll=roll[:3])  # Bogen hat ein ~5,36-px-Kunstpixelraster
