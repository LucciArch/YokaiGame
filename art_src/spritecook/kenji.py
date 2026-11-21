"""Kenji aus dem KI-Bogen kenji_sheet.jpg (3×4-Raster: Laufen; Ruhe, Ausholen, Katana-Hieb, Nachschwung; Ducken, Ball, Ball, –)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('kenji_sheet.jpg').convert('RGB')).astype(int)
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
walk, atk, roll = grid_boxes(fg, rows=3)
# letztes Rollbild des Bogens ist kein Ball (Rückenansicht) – Ball 2/3 entstehen durch Drehen
build('kenji', im, fg, walk + atk[1:], target_h=0, k=1 / 5.65, roll=roll[:3])  # Bogen hat ein ~5,65-px-Kunstpixelraster
