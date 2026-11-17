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
# Hundert Augen: jeder Treffer öffnet ein Auge (+20 % bis +56 %); Tsunami: Rückflut sucht; Tengu-Flug: vier Federn;
# Tsukumogami: die Rolle wirft zwei Papierpuppen (Runde 97)
g.start_run('hana', 19); run = g.run; p = run.player
for iid in ('mokumoku_auge', 'tengu_auge', 'kanagawa', 'kappa_teller', 'karasu_feder', 'tengu_geta', 'karakasa', 'hitogata'):
    p.gain_item(iid, silent=True)
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; run.enemies = [e]
for _ in range(8):
    sigs.hit_post(run, e, None, 1)
if abs(sigs.hit_pre(run, e, None, 10) - 15.6) > 0.01:
    print('FEHLER Hundert Augen', e.sg_eyes); bad += 1
b = Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {}); n0 = len(run.pbullets)
sigs.bullet_bounce(run, b)
if not b.fl.get('homing') or len(run.pbullets) - n0 != 2 or not all(x.fl.get('homing') for x in run.pbullets[n0:]):
    print('FEHLER Tsunami-Rückflut'); bad += 1
n0 = len(run.pbullets)
sigs.on_dash(p, run)
if len(run.pbullets) - n0 != 2:
    print('FEHLER Tsukumogami-Puppen', len(run.pbullets) - n0); bad += 1
fs = []
for _ in range(5):
    b = Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {}); sigs.on_fire(p, run, [b]); fs.append(b.dmg)
if [d >= 20 for d in fs] != [True] * 4 + [False]:
    print('FEHLER Tengu-Federn', fs); bad += 1
# Figuren-Siegel: Siegel schaltet das Item der Figur frei; Taizan rettet einmal pro Ebene; Haraegushi; Schwertjagd
g.start_run('benkei', 21); run = g.run; p = run.player
if 'tausendstes_schwert' in g.save['items']:
    g.save['items'].remove('tausendstes_schwert')
g.save['achievements'][:] = [a for a in g.save['achievements'] if a != 'm_benkei_boss3']
run.mark('boss3')
if 'tausendstes_schwert' not in g.save['items'] or 'tausendstes_schwert' not in run.pool:
    print('FEHLER Siegel schaltet kein Item frei'); bad += 1
run.challenge = 'bossrush'; g.save['achievements'].remove('m_benkei_boss3'); run.mark('boss3'); run.challenge = None
if 'm_benkei_boss3' in g.save['achievements']:
    print('FEHLER Siegel in Prüfung'); bad += 1
for iid in ('taizan_fukun', 'haraegushi', 'tausendstes_schwert'):
    p.gain_item(iid, silent=True)
p.shield_ready = False; p.iframes = 0; p.hp = 1; p.spirit = 0; p.hurt(2)
if p.dead or p.hp != 2 or not sigs.st(p).get('taizan_pen'):
    print('FEHLER Taizan rettet nicht', p.hp, p.dead); bad += 1
p.iframes = 0; p.hp = 1; p.hurt(2)
if not (p.dead or p.hp <= 0):
    print('FEHLER Taizan rettet zweimal pro Ebene'); bad += 1
p.dead = False; p.hp = p.maxhp
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; run.enemies = [e]; h0 = e.hp
sigs.st(p)['harae'] = 1; sigs.tick(p, run, 1 / 60)
if abs((h0 - e.hp) - e.maxhp * 0.05) > 0.01:
    print('FEHLER Haraegushi', h0 - e.hp); bad += 1
d0 = p.s['dmg']
for _ in range(60):
    sigs.on_kill(run, e)
if sigs.st(p).get('jagd_b') != 0.4 or not p.s['dmg'] > d0:
    print('FEHLER Schwertjagd', sigs.st(p).get('jagd_b'), d0, p.s['dmg']); bad += 1
# Welle „Sieg“: Tachi-ōjō, Masakari, Blutdurst, Fuchs-Trugbild
g.start_run('hana', 22); run = g.run; p = run.player
for iid in ('tachi_ojo', 'masakari', 'muramasa', 'fuchs_trugbild'):
    p.gain_item(iid, silent=True)
p.iframes = 0; p.hp = 2; p.spirit = 0; p.hurt(1)
if p.iframes < 2.9 or sigs.dmg_mult(p) < 1.49:
    print('FEHLER Tachi-ojo', p.iframes, sigs.dmg_mult(p)); bad += 1
fs = []
for _ in range(5):
    b = Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {}); sigs.on_fire(p, run, [b]); fs.append(bool(b.fl.get('boomerang')))
if fs != [False] * 4 + [True]:
    print('FEHLER Masakari', fs); bad += 1
r0 = sigs.rate_mult(p); e = make_boss(run, 'shuten_doji'); sigs.on_kill(run, e)
if not sigs.rate_mult(p) > r0 * 1.29:
    print('FEHLER Blutdurst'); bad += 1
sigs.on_dash(p, run); n0 = len(run.pbullets)
sigs.on_fire(p, run, [Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {})])
if len(run.pbullets) - n0 != 1:
    print('FEHLER Fuchs-Trugbild', len(run.pbullets) - n0); bad += 1
# Welle „Takamagahara“: Kesa-giri, Jūni-Shinshō, Gojō-Brücke, Tamagushi, Murakumo
g.start_run('hana', 23); run = g.run; p = run.player
for iid in ('kesagiri', 'juni_shinsho', 'gojo_giboshi', 'tamagushi', 'murakumo'):
    p.gain_item(iid, silent=True)
ns = []
for _ in range(12):
    n0 = len(run.pbullets); sigs.on_fire(p, run, [Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {})]); ns.append(len(run.pbullets) - n0)
if ns[3] != 2 or ns[11] != 14 or ns[0] != 0:
    print('FEHLER Kesa-giri/Juni', ns); bad += 1
e = make_boss(run, 'shuten_doji'); e.x, e.y = p.x + 30, p.y; e.spawn_t = 0; e.invuln = False; run.enemies = [e]; h0 = e.hp
p.iframes = 0; p.hp = 6; p.spirit = 0; p.hurt(1)
if not e.hp < h0:
    print('FEHLER Gojo'); bad += 1
run.hazards = []
for _ in range(25):
    sigs.tick(p, run, 0.1)
if not any(h.kind == 'strike' for h in run.hazards):
    print('FEHLER Murakumo'); bad += 1
p.hp = 2; sigs.st(p)['room_hit'] = False
for _ in range(3):
    sigs.on_room_clear(run)
if p.hp != 3:
    print('FEHLER Tamagushi', p.hp); bad += 1
# Welle „Yomi / Iwato“: Sieben Waffen, Kikyō, Tokkuri, Kushinada, Oni-Horn
g.start_run('benkei', 24); run = g.run; p = run.player
for iid in ('nanatsu_dogu', 'kikyo_mon', 'tanuki_tokkuri', 'kushinada_kushi', 'oni_tsuno'):
    p.gain_item(iid, silent=True)
big = []
for _ in range(7):
    b = Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {}); sigs.on_fire(p, run, [b]); big.append(b.dmg > 15)
if big != [False] * 6 + [True]:
    print('FEHLER Sieben Waffen', big); bad += 1
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; e.invuln = False; run.enemies = [e]
hs = []
for _ in range(5):
    h0 = e.hp; sigs.hit_post(run, e, None, 1); hs.append(h0 - e.hp)
if not (hs[4] > 0 and hs[:4] == [0] * 4):
    print('FEHLER Kikyo', hs); bad += 1
r0 = sigs.rate_mult(p)
for _ in range(8):
    sigs.on_coin(p, run, 1)
if not sigs.rate_mult(p) > r0 * 1.29:
    print('FEHLER Tokkuri'); bad += 1
p.hp = 6; p.spirit = 0; m0 = sigs.dmg_mult(p)
sigs.on_room_clear(run); sigs.on_room_clear(run)
if abs(sigs.dmg_mult(p) / m0 - 1.08) > 0.01:
    print('FEHLER Kushinada', sigs.dmg_mult(p) / m0); bad += 1
m0 = sigs.dmg_mult(p); p.hp = 2
if abs(sigs.dmg_mult(p) / m0 - 1.3) > 0.01:
    print('FEHLER Oni-Horn'); bad += 1
# Welle „Oni-Modus“: Ichi-no-tachi, Jizō, Sarayashiki-Brunnen, Ōnusa
g.start_run('kenji', 25); run = g.run; p = run.player
for iid in ('ichi_no_tachi', 'tanuki_kesa', 'okiku_ido', 'onusa'):
    p.gain_item(iid, silent=True)
run.room.cleared = False; sigs.on_room_enter(run)
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; e.invuln = False; run.enemies = [e]
b = Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {})
hs = []
for _ in range(2):
    h0 = e.hp; sigs.hit_post(run, e, b, 10); hs.append(h0 - e.hp)
if not (hs[0] >= 30 and hs[1] == 0):
    print('FEHLER Ichi-no-tachi', hs); bad += 1
p.iframes = 0; p.dash_t = 0; hp0 = p.total_hp()
p.hurt(1)
if p.total_hp() != hp0 or p.iframes < 1.9:
    print('FEHLER Jizo'); bad += 1
p.iframes = 0; p.hurt(1)
if p.total_hp() != hp0 - 1:
    print('FEHLER Jizo 2. Treffer'); bad += 1
p.spirit = 0; m0 = sigs.dmg_mult(p); p.spirit = 2
if abs(sigs.dmg_mult(p) / m0 - 1.24) > 0.01:
    print('FEHLER Reikon'); bad += 1
run.ebullets[:] = [Bullet(p.x + 20, p.y, -50, 0, 1, 3, 3, 'e', (255, 0, 0), {})]
nb0 = len(run.pbullets); sigs.on_dash(p, run)
if run.ebullets or len(run.pbullets) != nb0 + 1:
    print('FEHLER Onusa'); bad += 1
print('Signaturen/Synergien geprüft:', len(items), 'Fehler:', bad)
sys.exit(1 if bad else 0)
