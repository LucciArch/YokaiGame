"""Rebuilds every deliverable: <name>.png, <name>_walk.png, <name>_attack.png + 6x previews (+ review GIFs)."""
import sys
sys.path.insert(0, '/home/claude/fable_art')
import numpy as np
from PIL import Image
import px, oni, kappa, hana

D = '/home/claude/fable_art/'
BG = (0x16, 0x28, 0x5c, 255)
for name, mod, fn in (('oni', oni, oni.oni), ('kappa', kappa, kappa.kappa), ('hana', hana, hana.hana)):
    base = px.crop_img(fn().img())
    base.save(D + name + '.png')
    px.preview(base, D + name + '_preview.png', 6)
    for tag, frames, ms in (('walk', mod.WALK, 150), ('attack', mod.ATTACK, 160)):
        cs = [fn(**f) for f in frames]
        ims = [c.img() for c in cs]
        for i, c in enumerate(cs):
            x0, y0, x1, y1 = c.bbox()
            assert x0 >= 1 and y0 >= 1 and x1 <= px.W - 2 and y1 <= px.H - 2, (name, tag, i, c.bbox())
            print(name, tag, i, 'bbox', (x0, y0, x1, y1), 'cell', (px.W, px.H))
        st = px.strip(ims, D + f'{name}_{tag}.png')
        px.preview(st, D + f'{name}_{tag}_preview.png', 6)
        gf = []
        for im in ims:
            b = Image.new('RGBA', im.size, BG); b.alpha_composite(im)
            gf.append(b.resize((im.width * 4, im.height * 4), Image.NEAREST).convert('P', palette=Image.ADAPTIVE))
        gf[0].save(D + f'{name}_{tag}.gif', save_all=True, append_images=gf[1:], duration=ms, loop=0)
    a = np.array(base)
    cols = {tuple(c) for c in a.reshape(-1, 4) if c[3] > 0}
    semi = int(((a[:, :, 3] > 0) & (a[:, :, 3] < 255)).sum())
    print(name, base.size, 'colours', len(cols), 'semi-alpha', semi)

# ---- master reference sheets (6x): style bg and dark dungeon floor
ims = [Image.open(D + f'{n}.png') for n in ('oni', 'kappa', 'hana')]
Hh = max(i.height for i in ims); Ww = sum(i.width for i in ims) + 16
for bg, nm in ((BG, 'masters_preview.png'), ((0x24, 0x20, 0x2c, 255), 'masters_floor_preview.png')):
    o = Image.new('RGBA', (Ww, Hh + 2), bg); x = 2
    for i in ims:
        o.alpha_composite(i, (x, Hh - i.height + 1)); x += i.width + 6
    o.resize((o.width * 6, o.height * 6), Image.NEAREST).save(D + nm)
