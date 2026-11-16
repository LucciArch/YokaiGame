"""Misst jede Synergie gegen denselben Boss: Kampfzeit und Treffer im Vergleich zu gleich vielen Zufalls-Items.
Aufruf: python tools/synbalance.py [boss] [tiefe]  –  Ausgabe sortiert nach Tempo (Faktor < 1 = schneller als Zufall)."""
import os, sys, math, random
os.environ['SDL_VIDEODRIVER'] = 'dummy'; os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['APPDATA'] = os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_syn')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from yokai.app import Game
from yokai import data, gfx
from yokai.bosses import make_boss

BOSS = sys.argv[1] if len(sys.argv) > 1 else 'shuten_doji'
DEPTH = int(sys.argv[2]) if len(sys.argv) > 2 else 5
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None   # z. B. onmyodo,feuerwerk
g = Game(headless=True)


def fight(items, seed):
    random.seed(seed)
    g.start_run('hana', seed)
    run = g.run; run.depth = DEPTH; run.room.cleared = False
    p = run.player
    for iid in items:
        p.gain_item(iid, silent=True)
    b = make_boss(run, BOSS); run.enemies = [b]; run.boss = b
    t, dt, hits = 0, 1 / 60, 0
    while not b.dead and t < 180:
        t += dt
        hp0 = p.total_hp()
        inp = {'move': [math.cos(t * 0.9), math.sin(t * 1.3)], 'shoot': [b.x - p.x, b.y - p.y], 'dash': int(t * 60) % 120 == 0,
               'active': False, 'salt': False}
        run.update(dt, inp)
        if p.total_hp() < hp0:
            hits += 1
        p.hp = p.maxhp; p.dead = False; run.result = None
        gfx.TEXT.clear(); gfx.HI.clear()
    return t, hits, run.player


SEEDS = (11, 12, 13)
pool = [i for i in data.ITEM_IDS if not data.ITEMS[i].get('active')]
base = {}
for n in (2, 3):
    rs = [fight(random.Random(s * 7 + n).sample(pool, n), s) for s in SEEDS for _ in range(2)]
    base[n] = (sum(r[0] for r in rs) / len(rs), sum(r[1] for r in rs) / len(rs))
    print('Zufall %d Items: %.1f s, %.1f Treffer' % (n, *base[n]))
out = []
for sy in data.SYNERGIES:
    if ONLY and sy['id'] not in ONLY:
        continue
    rs = [fight(sy['items'], s) for s in SEEDS]
    assert sy['id'] in rs[0][2].synergies, sy['id'] + ' wird nicht ausgelöst'
    bt, bh = base[min(3, len(sy['items']))]
    t = sum(r[0] for r in rs) / len(rs); h = sum(r[1] for r in rs) / len(rs)
    out.append((t / bt, h - bh, sy['id'], t))
for f, dh, sid, t in sorted(out):
    print('%-16s Zeit ×%.2f (%5.1f s)  Treffer %+5.1f' % (sid, f, t, dh))
