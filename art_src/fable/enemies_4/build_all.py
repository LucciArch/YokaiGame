"""Rebuilds every sprite of enemy batch 4 and the 4x sheet preview of all statics."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
from PIL import Image
from common import D, export

NAMES = ['bakezori', 'nopperabo', 'bakeneko', 'kamaitachi', 'ningyo', 'kumo', 'nurikabe', 'enenra', 'sazae_oni',
         'kasha', 'azukiarai', 'karasu']
for n in NAMES:
    m = importlib.import_module(n)
    export(m.NAME, m.draw, m.WALK, m.ATTACK)

ims = [Image.open(D + n + '.png') for n in NAMES]
Hh = max(i.height for i in ims)
Ww = sum(i.width for i in ims) + 4 * (len(ims) + 1)
o = Image.new('RGBA', (Ww, Hh + 4), (0x24, 0x20, 0x2c, 255))
x = 4
for i in ims:
    o.alpha_composite(i, (x, Hh + 2 - i.height)); x += i.width + 4
o.resize((o.width * 4, o.height * 4), Image.NEAREST).save(D + 'sheet_preview.png')
print('sheet', o.size)
