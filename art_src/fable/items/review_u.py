import sys, importlib
from PIL import Image, ImageDraw
import common
mod = importlib.import_module(sys.argv[1])
names = mod.NAMES
S = 4; cw = 32 * S + 12; per = 8
rows = (len(names) + per - 1) // per
sh = Image.new('RGBA', (per * cw, rows * (cw + 12)), (0x24, 0x20, 0x2c, 255))
d = ImageDraw.Draw(sh)
for i, nm in enumerate(names):
    try:
        im = common.render(getattr(mod, nm)(), nm)[0]
    except Exception as e:
        print('ERR', nm, e); continue
    x, y = (i % per) * cw, (i // per) * (cw + 12)
    sh.alpha_composite(im.resize((32 * S, 32 * S), Image.NEAREST), (x + 6, y + 4))
    d.text((x + 6, y + cw - 4), nm, fill=(220, 210, 190, 255))
sh.save('/tmp/prev/rev_%s.png' % sys.argv[1])
for w in common.WARN: print('WARN', w)
