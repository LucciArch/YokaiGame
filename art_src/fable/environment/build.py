"""Builds every biome folder, the shared props, the 2x mock-room previews and overview.png.
usage: python3 build.py [biome ...]"""
import os
import random
import sys
from core import *
from biomes import *
from floors import floor_tiles
from walls import wall_set
try:
    from props import rocks, wall_decos
except ImportError:
    rocks = wall_decos = None

HERE = os.path.dirname(os.path.abspath(__file__))
T = 32


def room(name, parts, chars=False):
    """13x7 floor + 16 px wall frame, mirrored exactly the way the game does it"""
    fl, ws, rk, dc = parts
    rng = random.Random(name + '-room')
    W, H = 13 * T + 32, 7 * T + 32
    cv = Cv(W, H, bg='#000000')
    for j in range(7):
        for i in range(13):
            t = fl[rng.randint(0, 3)] if rng.random() < .93 else fl[rng.randint(4, 5)]
            cv.blit(t, 16 + i * T, 16 + j * T)
    deco_at = {3: 0, 9: 1}
    for i in range(13):
        seg = dc[deco_at[i]] if (dc and i in deco_at) else ws['h']
        cv.blit(seg, 16 + i * T, 0)
        cv.blit(ws['bottom'], 16 + i * T, H - 16)
    for j in range(7):
        cv.blit(ws['v'], 0, 16 + j * T)
        cv.blit(ws['v'], W - 16, 16 + j * T, flipx=True)
    cv.blit(ws['corner'], 0, 0)
    cv.blit(ws['corner'], W - 16, 0, flipx=True)
    cv.blit(ws['corner'], 0, H - 16, flipy=True)
    cv.blit(ws['corner'], W - 16, H - 16, flipx=True, flipy=True)
    if rk:
        for k, (i, j) in enumerate(((2, 1), (9, 4), (5, 5))):
            cv.blit(rk[k % len(rk)], 16 + i * T, 16 + j * T)
    return cv


def build(name):
    d = os.path.join(HERE, name)
    os.makedirs(d, exist_ok=True)
    fl = floor_tiles(name)
    ws = wall_set(name)
    rk = rocks(name) if rocks else None
    dc = wall_decos(name, ws['h']) if wall_decos else None
    strip(fl, os.path.join(d, 'floor.png'))
    ws['h'].img().save(os.path.join(d, 'wall_h.png'))
    ws['bottom'].img().save(os.path.join(d, 'wall_h_bottom.png'))
    ws['v'].img().save(os.path.join(d, 'wall_v.png'))
    ws['corner'].img().save(os.path.join(d, 'wall_corner.png'))
    if dc:
        strip(dc, os.path.join(d, 'wall_deco.png'))
    if rk:
        strip(rk, os.path.join(d, 'rock.png'))
    r = room(name, (fl, ws, rk, dc))
    im = r.img()
    im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(os.path.join(HERE, 'preview_%s.png' % name))
    return im


if __name__ == '__main__':
    names = sys.argv[1:] or ORDER
    rooms = {n: build(n) for n in names}
    if not sys.argv[1:]:
        try:
            import shared
            shared.build()
        except ImportError:
            pass
        cols = 3
        rws = (len(ORDER) + cols - 1) // cols
        w, h = rooms[ORDER[0]].size
        ov = Image.new('RGBA', (cols * (w + 8) + 8, rws * (h + 8) + 8), (10, 8, 20, 255))
        for i, n in enumerate(ORDER):
            ov.paste(rooms[n], (8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)))
        ov.save(os.path.join(HERE, 'overview.png'))
    print('built', len(names))
