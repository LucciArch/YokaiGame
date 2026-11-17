"""Misst jede Synergie gegen denselben Boss: Kampfzeit und Treffer im Vergleich zu gleich vielen Zufalls-Items.
Aufruf: python tools/synbalance.py [boss] [tiefe] [ids]  –  Ausgabe sortiert nach Tempo (Faktor < 1 = schneller als Zufall).
Mit --tod: Überlebenszeit ohne Gott-Modus gegen einen Boss, der in Phase 2 festgehalten wird (Faktor > 1 = zäher als Zufall).
Mit --raum: statt des Bosses drei Wellen zu je 8 Normalgegnern aus dem Gebiet der Tiefe (für Raum-Synergien).
Mit --leben: ohne Gott-Modus; gemessen wird der Boss-Schaden in % bis zum Tod (Faktor > 1 = mehr Schaden als Zufall),
  damit Effekte „wenn du getroffen wirst“ nur so oft wirken, wie die Herzen reichen.
Mit --waffe=w_laser (w_sword, w_bow ...): alle Kämpfe mit dieser Angriffsart.
Mit Nahkampfwaffe (auch aus Items wie Speer oder Tamahagane) läuft der Bot zum Ziel und umkreist es."""
import os, sys, math, random
os.environ['SDL_VIDEODRIVER'] = 'dummy'; os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['APPDATA'] = os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_syn')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from yokai.app import Game
from yokai import data, gfx, weapons
from yokai.bosses import make_boss, CX, CY

TOD = '--tod' in sys.argv
if TOD:
    sys.argv.remove('--tod')
LEBEN = '--leben' in sys.argv
if LEBEN:
    sys.argv.remove('--leben')
RAUM = '--raum' in sys.argv
if RAUM:
    sys.argv.remove('--raum')
WAFFE = next((a[8:] for a in sys.argv if a.startswith('--waffe=')), None)
sys.argv = [a for a in sys.argv if not a.startswith('--waffe=')]
MELEE = ('w_sword', 'w_spear', 'w_club', 'w_scythe', 'w_fan')
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
    if WAFFE:
        p.bonus[WAFFE] = 1; p.recalc()
    nah = weapons.weapon_of(p) in MELEE   # auch Items wie Speer oder Schwert machen Nahkampf
    if RAUM:
        kinds = data.BIOMES[data.DEPTH_BIOMES[min(DEPTH, 5)][0]]['enemies']
        waves = 3
        run.enemies = []; b = None
    else:
        b = make_boss(run, BOSS); run.enemies = [b]; run.boss = b
    t, dt, hits = 0, 1 / 60, 0
    if TOD and b:
        b._hp = b.maxhp * 0.45   # an der Schadensobergrenze vorbei
    while (RAUM or not b.dead) and t < 180:
        t += dt
        if RAUM:
            alive = sum(not e.dead for e in run.enemies)
            if alive == 0 and waves == 0:
                break
            if alive <= 1 and waves > 0:   # nächste Welle vor dem Säubern, sonst öffnen sich die Türen
                waves -= 1
                for i in range(8):
                    a = i / 8 * math.tau
                    run.spawn_enemy(random.choice(kinds), CX + math.cos(a) * 150, CY + math.sin(a) * 90)
            tgt = run.nearest_enemy(p.x, p.y) or p
        else:
            tgt = b
        hp0 = p.total_hp()
        mv = [math.cos(t * 0.9), math.sin(t * 1.3)]
        if nah:   # auf Hiebweite heran, dann seitlich ausweichen
            dx, dy = tgt.x - p.x, tgt.y - p.y
            mv = [dx, dy] if math.hypot(dx, dy) > 34 + getattr(tgt, 'r', 0) else [-dy, dx]
        inp = {'move': mv, 'shoot': [tgt.x - p.x, tgt.y - p.y], 'dash': int(t * 60) % 120 == 0,
               'active': False, 'salt': False}
        run.update(dt, inp)
        if p.total_hp() < hp0:
            hits += 1
        if TOD:
            if b:
                b.hp = max(b.hp, b.maxhp * 0.3)   # Boss bleibt in Phase 2, nur das Überleben zählt
            if p.dead or run.result:
                break
            continue
        if LEBEN and (p.dead or run.result == 'dead'):
            return 100 * (1 - b.hp / b.maxhp), hits, run.player
        if not LEBEN:
            p.hp = p.maxhp; p.dead = False; run.result = None
        gfx.TEXT.clear(); gfx.HI.clear()
    return (100 * (1 - b.hp / b.maxhp) if LEBEN else t), hits, run.player


SEEDS = tuple(range(11, 23)) if TOD else tuple(range(11, 17)) if RAUM else (11, 12, 13)   # Überleben und Räume streuen stärker
pool = [i for i in data.ITEM_IDS if not data.ITEMS[i].get('active')]
base = {}
for n in (2, 3):
    rs = [fight(random.Random(s * 7 + n).sample(pool, n), s) for s in SEEDS for _ in range(2)]
    base[n] = (sum(r[0] for r in rs) / len(rs), sum(r[1] for r in rs) / len(rs))
    print('Zufall %d Items: %.1f %s, %.1f Treffer' % (n, base[n][0], '%' if LEBEN else 's', base[n][1]))
out = []
for sy in data.SYNERGIES:
    if ONLY and sy['id'] not in ONLY:
        continue
    rs = [fight(sy['items'], s) for s in SEEDS]
    assert sy['id'] in rs[0][2].synergies, sy['id'] + ' wird nicht ausgelöst'
    bt, bh = base[min(3, len(sy['items']))]
    t = sum(r[0] for r in rs) / len(rs); h = sum(r[1] for r in rs) / len(rs)
    out.append((t / bt, h - bh, sy['id'], t))
for f, dh, sid, t in sorted(out, reverse=TOD or LEBEN):
    print('%-16s %s ×%.2f (%5.1f %s)  Treffer %+5.1f' % (sid, 'Schaden' if LEBEN else 'Zeit', f, t, '%' if LEBEN else 's', dh))
