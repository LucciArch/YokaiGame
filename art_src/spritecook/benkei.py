"""Benkei aus dem KI-Bogen benkei_sheet.jpg (3×4-Raster: Laufen; Ruhe, Ausholen, Naginata-Stoß, Nachschwung; Ducken, –, Ball, –)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('benkei_sheet.jpg').convert('RGB')).astype(int)
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 20, iterations=2))
walk, atk, roll = grid_boxes(fg, rows=3)
# Stoß-Klinge berührt das Nachbarbild: Angriffsreihe von Hand an x=2017 geteilt (shortcut: schneidet die Quaste des Nachschwungs minimal an).
# Nur das mittlere Rollbild ist ein Ball – die übrigen Ballbilder sind seine Vierteldrehungen
y0, y1 = atk[0][1], atk[0][3]
atk = [(644, y0, 1300, y1), (1300, y0, 2017, y1), (2017, y0, 2576, y1)]
build('benkei', im, fg, walk + atk, target_h=0, k=1 / 5.36, roll=[roll[0], roll[2]])  # Bogen hat ein ~5,36-px-Kunstpixelraster
