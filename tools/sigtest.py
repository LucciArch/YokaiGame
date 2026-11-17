"""Prüft jede Item-Signatur einzeln: Lauf starten, nur dieses Item geben, 40 s spielen (Gott-Modus), Speichern/Laden."""
import os, sys, json, random
os.environ['SDL_VIDEODRIVER'] = 'dummy'; os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['APPDATA'] = os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_test')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import pygame
from yokai.app import Game
from yokai import data
import bot

g = Game()
bad = 0
items = [[k] for k, it in data.ITEMS.items() if any(f.startswith('sig_') for f in it['fx'])]
items += [sy['items'] for sy in data.SYNERGIES if any(f.startswith('sig_') for f in sy['fx'])]   # Synergien: alle Teile geben
for i, group in enumerate(items):
    iid = '+'.join(group)
    random.seed(i)
    orig = bot.play
    try:
        g.start_run('hana', 100 + i)
        for one in group:
            g.run.player.gain_item(one, silent=True)
        # kurzer Lauf mit demselben Bot, aber begrenzter Zeit
        run = g.run
        p = run.player
        dt = 1 / 60
        for step in range(60 * (40 if len(group) == 1 else 25)):
            p.iframes = max(p.iframes, 0.5) if step % 600 else 0
            en = run.nearest_enemy(p.x, p.y)
            inp = {'move': [0, 0], 'shoot': [0, 0], 'dash': random.random() < 0.02, 'active': False, 'salt': random.random() < 0.003}
            if en:
                inp['shoot'] = [en.x - p.x, en.y - p.y]
                inp['move'] = [random.uniform(-1, 1), random.uniform(-1, 1)]
            elif run.room.cleared:
                ds = list(run.room.doors.keys())
                if ds:
                    from yokai.settings import DOOR_POS
                    dx, dy = DOOR_POS[ds[step // 300 % len(ds)]]
                    inp['move'] = [dx - p.x, dy - p.y]
            run.update(dt, inp)
            if run.result:
                break
        json.dumps(run.state_dict())
    except Exception:
        import traceback; traceback.print_exc()
        print('FEHLER', iid); bad += 1
# Omikuji: nach vielen Zügen sind alle fünf Lose gezogen und der Erfolg „Alle Lose“ ist da
from yokai.entities import Obj
g.start_run('hana', 7)
for i in range(200):
    o = Obj('omikuji', 100, 100); g.run.player.coins = 99; g.run.player.iframes = 1; g.run.interact(o)
if len(g.save['kuji_seen']) != 5 or 'alle_lose' not in g.save['achievements']:
    print('FEHLER Omikuji', g.save['kuji_seen']); bad += 1
# Uzumes Kagura-Suzu + Yata-Spiegel: die Rolle löscht nahe Geschosse und wirft sie als Sonnenstrahlen zurück
from yokai import sigs
from yokai.entities import ebullet
g.start_run('hana', 12); run = g.run; p = run.player
for iid in ('uzume_suzu', 'yata_kagami'):
    p.gain_item(iid, silent=True)
run.ebullets = []
for k in range(5):
    ebullet(run, p.x + 20, p.y + k, 0, 0)
ebullet(run, p.x + 150, p.y, 0, 0)
sigs.on_dash(p, run)
if len(run.ebullets) != 1 or 'iwato' not in p.sgs:
    print('FEHLER Kagura-Suzu', len(run.ebullets), sorted(p.sgs)); bad += 1
# Onmyōdō: Papierdiener aus der Siegel-Explosion laden das Pentagramm nicht nach (sonst Kettenreaktion, Balance 87)
from yokai.bosses import make_boss
g.start_run('hana', 13); run = g.run; p = run.player
for iid in ('shikigami_papier', 'seimei_stern'):
    p.gain_item(iid, silent=True)
e = make_boss(run, 'shuten_doji'); run.enemies = [e]
e.sg_pent = 4
sigs.hit_post(run, e, None, 1)
shiki = [b for b in run.pbullets if b.fl.get('_shiki')]
for b in shiki:
    sigs.hit_post(run, e, b, 1)
if len(shiki) != 3 or e.sg_pent != 0:
    print('FEHLER Onmyōdō-Kette', len(shiki), e.sg_pent); bad += 1
# Feuerwerk über Edo: die fünf Funken teilen sich eine Trefferliste (Balance 88)
from yokai.entities import Bullet
g.start_run('hana', 14); run = g.run; p = run.player
for iid in ('hanabi', 'chochin_feuer'):
    p.gain_item(iid, silent=True)
run.pbullets = []
sigs.bullet_end(run, Bullet(100, 100, 0, 0, 1, 2, 1, 'p', (255, 255, 255), {'explode': 1}))
if len(run.pbullets) != 5 or len({id(b.hit) for b in run.pbullets}) != 1:
    print('FEHLER Feuerwerk-Funken', len(run.pbullets)); bad += 1
# Göttliches Arsenal: der Speer (Ame-no-Nuboko) verdrängt Hachimans Bogen, also schießt jeder Stoß einen Pfeil mit (Runde 91)
from yokai import weapons
g.start_run('hana', 15); run = g.run; p = run.player
for iid in ('ame_nuboko', 'hachiman_bogen'):
    p.gain_item(iid, silent=True)
run.pbullets = []
weapons.fire(p, (1, 0), weapons.weapon_of(p))
if weapons.weapon_of(p) != 'w_spear' or sum(getattr(b, 'arrow', False) for b in run.pbullets) != 1:
    print('FEHLER Arsenal-Pfeil', weapons.weapon_of(p), len(run.pbullets)); bad += 1
# Sturmfächer: jeder dritte Schlag ruft einen Blitz auf den nächsten Feind (Runde 92)
g.start_run('hana', 16); run = g.run; p = run.player
for iid in ('tengu_faecher', 'raijin_trommel'):
    p.gain_item(iid, silent=True)
e = make_boss(run, 'shuten_doji'); e.x, e.y = p.x + 60, p.y; e.spawn_t = 0; e.invuln = False; run.enemies = [e]; run.hazards = []
for _ in range(3):
    sigs.on_fire(p, run, [])
if sum(h.kind == 'strike' and h.owner == 'p' for h in run.hazards) != 1:
    print('FEHLER Sturmfächer-Blitz', len(run.hazards)); bad += 1
# Mondsichel-Klinge: bei 6 Blutungen reißt der nächste Bogen alles auf (300 %, Runde 93)
g.start_run('hana', 17); run = g.run; p = run.player
for iid in ('tsukuyomi', 'kamaitachi_sichel'):
    p.gain_item(iid, silent=True)
e = make_boss(run, 'shuten_doji'); run.enemies = [e]; e.sg_bleed = 6
b = Bullet(e.x, e.y, 0, 0, 1, 2, 1, 'p', (255, 255, 255), {}); b.curve = 1.7
if sigs.hit_pre(run, e, b, 10) < 29 or e.sg_bleed != 0:
    print('FEHLER Mondschnitt', e.sg_bleed); bad += 1
# Kappa-Festmahl: abgeprallte Talismane treffen einmalig 50 % stärker und bremsen; Mokumokuren: großes Auge +40 % (Runde 94)
g.start_run('hana', 18); run = g.run; p = run.player
for iid in ('kappa_gurke', 'kappa_teller', 'shoji_papier', 'geheimkarte'):
    p.gain_item(iid, silent=True)
b = Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {})
sigs.bullet_bounce(run, b); sigs.bullet_bounce(run, b)
if abs(b.dmg - 15) > 0.01 or not b.fl.get('slow'):
    print('FEHLER Kappa-Festmahl', b.dmg); bad += 1
b = Bullet(100, 100, 50, 0, 10, 4.4, 1, 'p', (255, 255, 255), {'sg': ('gross',)})
for _ in range(10):
    sigs.bullet_tick(b, run, 0.05)
if not b.fl.get('homing') or abs(b.dmg - 14) > 0.01:
    print('FEHLER Mokumokuren', b.dmg, b.r); bad += 1
print('Signaturen/Synergien geprüft:', len(items), 'Fehler:', bad)
sys.exit(1 if bad else 0)
