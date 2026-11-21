"""Akago aus dem KI-Bogen akago_sheet.jpg (3×4-Raster: Laufen; Ruhe, Ausholen, Keulenschlag, Nachschwung; Ducken, Ball, Ball, Ball)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('akago_sheet.jpg').convert('RGB')).astype(int)
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
walk, atk, roll = grid_boxes(fg, rows=3)
# Akago ist ein Kleinkind: 1,5 Kunstpixel je Pixel, damit er kleiner als die übrigen Figuren bleibt
build('akago', im, fg, walk + atk[1:], target_h=0, k=1 / (5.36 * 1.5), roll=roll[:3], resample=Image.NEAREST)  # Raster ~5,36 px; NEAREST, sonst mittelt der Umriss das kleine grüne Büschel dunkel
