import os, sys
os.environ['SDL_VIDEODRIVER']='dummy'; os.environ['SDL_AUDIODRIVER']='dummy'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from yokai import data, rooms, gfx
from yokai.app import FX_NAMES
import pygame; pygame.init(); pygame.display.set_mode((10,10))
bad=0
for iid,it in data.ITEMS.items():
    for k in it['fx']:
        if k not in FX_NAMES: print('unknown fx',iid,k); bad+=1
    for t in it['tags']:
        if t not in data.TRANSFORMS: print('bad tag',iid,t); bad+=1
for s in data.SYNERGIES:
    for i in s['items']:
        if i not in data.ITEMS: print('syn missing',s['id'],i); bad+=1
    for k in s['fx']:
        if k not in FX_NAMES: print('syn fx',s['id'],k); bad+=1
for i,t in enumerate(rooms.TEMPLATES):
    if len(t)!=7 or any(len(r)!=13 for r in t): print('template',i,[len(r) for r in t]); bad+=1
for name,rows in gfx.SPRITES.items():
    w=len(rows[0])
    for r in rows:
        if len(r)!=w: print('sprite width',name,rows.index(r),len(r),w); bad+=1
    for ch in ''.join(rows):
        if ch!='.' and ch not in gfx.PAL: print('pal',name,ch); bad+=1
for e,d in data.ENEMIES.items():
    if d['sprite'] not in gfx.SPRITES and not __import__('yokai.sheets',fromlist=['x']).has(d['sprite']): print('no sprite',e); bad+=1
for c in data.CHARS:
    if c not in gfx.SPRITES: print('no char sprite',c); bad+=1
for b in data.BIOMES.values():
    for e in b['enemies']:
        if e not in data.ENEMIES: print('biome enemy',e); bad+=1
for a in data.ACHIEVEMENTS:
    if a[3] and a[3][0]=='item' and a[3][1] not in data.ITEMS: print('ach item',a); bad+=1
    if a[3] and a[3][0]=='active' and not data.ACTIVES.get(a[3][1], {}).get('locked'): print('ach active',a); bad+=1
for k,v in data.BOSS_REWARD.items():
    if v and v not in data.ITEMS: print('reward',k,v); bad+=1
import os as _os
_icdir = _os.path.join(_os.path.dirname(data.__file__), 'assets', 'items', 'icons')
for k, it in data.ITEMS.items():
    if len(it['pools']) != 1 or it['pools'][0] not in 'TSBKOY': print('pool', k, it['pools']); bad += 1
    if it['icon'] == k and not _os.path.exists(_os.path.join(_icdir, k + '.png')): print('icon missing', k); bad += 1
for k in ('brautschleier', 'zashiki_temari'):
    if data.ITEMS[k]['pools'] != ['Y']: print('event item not exclusive', k); bad += 1
for a in data.ACHIEVEMENTS:
    if sum(1 for b in data.ACHIEVEMENTS if b[0] == a[0]) > 1: print('ach dup', a[0]); bad += 1
from yokai.audio import Audio, MUSIC_DIR
for k, b in data.BIOMES.items():   # Bossmusik wie Run.boss_music (Tiefe = Biom-Tiefe)
    tr = Audio.track_for(('x', 0, 0, 'boss', b['music'][4] + 100 + b.get('depth', 1)))
    if not _os.path.exists(_os.path.join(MUSIC_DIR, tr + '.ogg')) or (tr == 'amaterasu') != (k == 'iwato'): print('boss music', k, tr); bad += 1
for k in data.BIOMES:   # Wanddekos: Hi-Res-Streifen passt zum einfachen (gleicher Index)
    lo, hi = gfx.env_img(k, 'wall_deco', 32), gfx.env_img(k, 'wall_deco_hi', 64)
    if lo and (not hi or len(hi) != len(lo) or hi[0].get_size() != (64, 32)): print('wall_deco_hi', k); bad += 1
print('items',len(data.ITEMS),'syn',len(data.SYNERGIES),'templates',len(rooms.TEMPLATES),'bad',bad)
sys.exit(1 if bad else 0)
