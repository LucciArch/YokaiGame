"""Seimei aus dem KI-Bogen seimei_sheet.jpg (3×4-Raster: Laufen; Ruhe, Shikigami beschwören, Wurf, Nachschwung; Ducken, Ball, Ball, Ball)."""
import numpy as np
from PIL import Image
from scipy import ndimage
from prep import build, grid_boxes

im = np.array(Image.open('seimei_sheet.jpg').convert('RGB')).astype(int)
# schwarzer Eboshi-Hut liegt farblich dicht am Grund: niedrigere Schwelle als sonst
fg = ndimage.binary_fill_holes(ndimage.binary_opening(np.abs(im - im[5, 5]).sum(2) > 11, iterations=2))
walk, atk, roll = grid_boxes(fg, rows=3)
# Im 2. Laufbild steht ein fremder Ringstab (aus Kotarōs Bogen) rechts neben ihm: Bild bei x=1101 begrenzt.
# Shikigami steht frei neben der Figur: Angriffsbilder von Hand begrenzt; die Staubwolke hinter ihm (x < 1440) bleibt weg, sie wirkt im Spiel wie ein Stein.
walk[1] = (815, walk[1][1], 1101, walk[1][3])
y0, y1 = atk[0][1], atk[0][3]
atk = [(740, y0, 1160, y1), (1440, y0, 2000, y1), (2050, y0, 2560, y1)]
build('seimei', im, fg, walk + atk, target_h=0, k=1 / 5.36, roll=roll[:3])  # Bogen hat ein ~5,36-px-Kunstpixelraster
