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
from yokai.entities import Bullet, Pedestal
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
# Prüfungs-Belohnungen: Fūrin, Keppan, Mii-dera, Nademono, Kongō-zue, Hayate
g.start_run('hana', 27); run = g.run; p = run.player
for iid in ('fuurin', 'keppan', 'miidera_kane', 'nademono', 'kongozue', 'hayate_waraji'):
    p.gain_item(iid, silent=True)
p.hp = 6; p.spirit = 0; m0 = sigs.dmg_mult(p); p.hp = 2
if abs(sigs.dmg_mult(p) / m0 - 1.25) > 0.01:
    print('FEHLER Fuurin Glas'); bad += 1
p.hp = 6; nb0 = len(run.pbullets); sigs.on_hurt(p, run)
if len(run.pbullets) != nb0 + 8:
    print('FEHLER Fuurin Splitter'); bad += 1
m0 = sigs.dmg_mult(p); sigs.st(p)['pakt'] = 2
if abs(sigs.dmg_mult(p) / m0 - 1.16) > 0.01:
    print('FEHLER Keppan'); bad += 1
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; e.invuln = False; run.enemies = [e]
b = Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {})
hs = []
for _ in range(10):
    h0 = e.hp; sigs.hit_post(run, e, b, 1); hs.append(h0 - e.hp)
if not (hs[9] > 0 and hs[:9] == [0] * 9 and e.slowed > 0):
    print('FEHLER Mii-dera', hs); bad += 1
p.iframes = 0; eb = Bullet(p.x, p.y, 0, 0, 1, 3, 1, 'e', (255, 0, 0), {})
if not sigs.block(p, run, eb) or sigs.block(p, run, eb):
    print('FEHLER Nademono'); bad += 1
p.hp = 2; sigs.on_floor(run)
if p.hp != 3:
    print('FEHLER Kongozue'); bad += 1
run.room.cleared = False; run.room_enter_time = run.time
if not sigs.rate_mult(p) > 1.29:
    print('FEHLER Hayate'); bad += 1
# Prüfung Verbannung: Susanoo nur mit Geisterherzen; Aokusa-Mino ruft Blitze
g.start_run('susanoo', 28, challenge='verbannung'); run = g.run; p = run.player
if not (p.spirit_only and p.maxhp == 0 and p.spirit == 6 and not p.heal(2)):
    print('FEHLER Verbannung', p.maxhp, p.spirit); bad += 1
p.gain_item('aokusa_mino', silent=True)
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; e.invuln = False; e.x, e.y = p.x + 40, p.y; run.enemies = [e]
nh = len(run.hazards); sigs.on_hurt(p, run)
if len(run.hazards) != nh + 1:
    print('FEHLER Aokusa-Mino'); bad += 1
rw = {a[0]: a[3] for a in data.ACHIEVEMENTS}
if any(not rw['ch_' + c['id']] or rw['ch_' + c['id']][0] != 'item' for c in data.CHALLENGES):
    print('FEHLER Prüfung ohne Item-Belohnung'); bad += 1
# Meister-Siegel: alle Siegel einer Figur → Lauf beginnt mit einem ihrer Siegel-Items (Spielstand danach zurücksetzen)
ach0 = list(g.save['achievements'])
g.save['achievements'].extend('m_okiku_' + m for m in data.CHAR_UNLOCKS['okiku'])
g.start_run('okiku', 26)
if 'meister_okiku' not in g.save['achievements'] or not set(g.run.player.items) & set(data.CHAR_UNLOCKS['okiku'].values()) or g.run.boss_mult != 1.15:
    print('FEHLER Meister'); bad += 1
g.save['achievements'][:] = ach0; g.save.write()
# Quests: aktive Belohnungen sind gesperrt, bis der Erfolg da ist; beide Aktiv-Wirkungen greifen
ach0, it0, st0 = list(g.save['achievements']), list(g.save['items']), dict(g.save['stats'])
g.save['achievements'][:] = [a for a in ach0 if not a.startswith('q_')]
g.save['items'][:] = [i for i in it0 if i not in data.ACTIVES]
g.start_run('hana', 31); run = g.run; p = run.player
if 'mondkine' in run.active_pool:
    print('FEHLER Quest-Sperre'); bad += 1
g.save['stats']['nohit_bosses'] = 4; run.boss_hit = False
for _ in range(2):
    run.save.stat('mochi_good')
run.achieve('q_mochi'); run.achieve('q_nohit5')
if 'mondkine' not in run.active_pool or 'shiomitsu_tama' not in run.active_pool:
    print('FEHLER Quest-Belohnung'); bad += 1
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; e.invuln = False; e.x, e.y = p.x + 40, p.y; run.enemies = [e]
for c in data.CHALLENGES:
    g.save['achievements'].append('ch_' + c['id'])
run.check_meister()
for k in ('yomeiri', 'ema', 'hyakki', 'ema', 'kakurenbo'):
    run.event_done(k)
if 'q_pruefungen' not in g.save['achievements'] or 'q_feste4' not in g.save['achievements'] or 'totsuka' not in run.active_pool:
    print('FEHLER Quests Teil 2'); bad += 1
for a in ('mondkine', 'shiomitsu_tama', 'matsuri_uchiwa', 'totsuka'):
    p.active = a; p.charge = 9; h0 = e.hp
    run.ebullets.append(Bullet(p.x + 60, p.y, 0, 0, 1, 3, 1, 'e', (255, 0, 0), {}))
    run.use_active()
    if not e.hp < h0 or (a == 'shiomitsu_tama' and (run.ebullets or not e.slowed)) or (a == 'mondkine' and not e.frozen):
        print('FEHLER Aktiv', a); bad += 1
# q_geheim3: drei Geheimräume in einem Lauf → Mayoiga-Wan deckt die Ebene auf und gibt zwei Gaben
from yokai.settings import DOOR_POS
sigs.st(p)['geheim_lauf'] = 2
r0 = run.room
for rr in run.rooms.values():
    hid = [d for d, n in rr.doors.items() if run.rooms[n].kind == 'secret' and not run.rooms[n].revealed]
    if hid:
        run.room = rr; run.reveal_near(*DOOR_POS[hid[0]], 999); break
run.room = r0
if 'q_geheim3' not in g.save['achievements'] or 'mayoiga_wan' not in run.active_pool:
    print('FEHLER Quest q_geheim3'); bad += 1
for rr in run.rooms.values():
    rr.revealed = False
p.active = 'mayoiga_wan'; p.charge = 9; n0 = len(run.pickups); run.use_active()
if not all(rr.revealed for rr in run.rooms.values()) or len(run.pickups) != n0 + 2:
    print('FEHLER Aktiv mayoiga_wan'); bad += 1
# Henro (Kongō-zue + Senbazuru): neue Ebene faltet zwei Kraniche
g.start_run('hana', 33); run = g.run; p = run.player
for iid in ('kongozue', 'senbazuru'):
    p.gain_item(iid, silent=True)
sigs.st(p)['cranes'] = 3; sigs.on_floor(run)
if 'henro' not in p.sgs or sigs.st(p)['cranes'] != 5 or not any('Henro' in l for l in sigs.nutz_lines(p)):
    print('FEHLER Henro'); bad += 1
# Misogi (Ōnusa + Reinigungssalz): Salz macht alle Feindgeschosse im Raum zu Shide
g.start_run('hana', 34); run = g.run; p = run.player
for iid in ('onusa', 'kiyome_sack'):
    p.gain_item(iid, silent=True)
run.ebullets[:] = []
run.ebullets += [Bullet(p.x + 200, p.y + k * 3, -50, 0, 1, 3, 5, 'e', (255, 0, 0)) for k in range(15)]
n0 = len(run.pbullets); p.salts = 1; run.use_salt()
if 'misogi' not in p.sgs or run.ebullets or len(run.pbullets) - n0 != 12:
    print('FEHLER Misogi', len(run.pbullets) - n0); bad += 1
# Quests Teil 3: 50 Kami-Gaben → Nusa, Schleife 3 → Yatagarasu-Feder
g.save['stats']['kami_deals'] = 49
pd = Pedestal(data.ITEM_IDS[0], p.x, p.y + 6); pd.shrine = 'kami'; pd.cool = 0; run.pedestals = [pd]; run.collect()
run.depth, run.stage, run.loop = 6, 1, 1; run.go_deeper()
if 'nusa' not in run.active_pool or 'yatagarasu_feder' not in run.active_pool:
    print('FEHLER Quests Teil 3', g.save['stats']['kami_deals'], run.loop); bad += 1
p = run.player; run.curse = 'nebel'; run.ebullets.append(Bullet(p.x + 60, p.y, 0, 0, 1, 3, 1, 'e', (255, 0, 0), {}))
p.active = 'nusa'; p.charge = 9; p.iframes = 0; run.use_active()
if run.curse or run.ebullets or p.iframes < 2.9:
    print('FEHLER Aktiv nusa'); bad += 1
p.active = 'yatagarasu_feder'; p.charge = 9; run.use_active()
if not p.f['homing'] or not p.f['pierce']:
    print('FEHLER Aktiv yatagarasu_feder'); bad += 1
g.save['achievements'][:] = ach0; g.save['items'][:] = it0; g.save['stats'].clear(); g.save['stats'].update(st0); g.save.write()
# Kagura (Hi-ōgi + Uzumes Suzu): Suzu im Tanz wirbelt 6 Sakaki-Blätter, außerhalb nicht
g.start_run('hana', 35); run = g.run; p = run.player
for iid in ('hi_ogi', 'uzume_suzu'):
    p.gain_item(iid, silent=True)
run.time = 20.0; sigs.st(p)['hurt_t'] = 10.0
n0 = len(run.pbullets); sigs._suzu(p, run); n1 = len(run.pbullets)
sigs.st(p)['hurt_t'] = 19.0; sigs._suzu(p, run)
if 'kagura' not in p.sgs or n1 - n0 != 6 or len(run.pbullets) != n1:
    print('FEHLER Kagura', n1 - n0, len(run.pbullets) - n1); bad += 1
# Banchō Sarayashiki (9. + 10. Teller): Okikus Klage zerspringt um dich, der Teller schon beim 9. Kill
g.start_run('hana', 36); run = g.run; p = run.player
for iid in ('neunter_teller', 'zehnter_teller'):
    p.gain_item(iid, silent=True)
sigs.st(p)['shots'] = 9; n0 = len(run.pbullets); sigs.on_fire(p, run, []); n1 = len(run.pbullets)
sigs.st(p)['zt'] = 8; e = make_boss(run, 'shuten_doji'); e.x, e.y = p.x + 40, p.y; sigs.on_kill(run, e)
if 'okiku' not in p.sgs or n1 - n0 < 10 or len(run.pbullets) - n1 != 10:
    print('FEHLER Sarayashiki', n1 - n0, len(run.pbullets) - n1); bad += 1
# Gojō-Ōhashi (Giboshi + Ushiwakas Flöte): Flötenton jeden 4. Wurf, Treffer löst die Naginata aus (1×/s)
g.start_run('hana', 37); run = g.run; p = run.player
for iid in ('gojo_giboshi', 'ushiwaka_fue'):
    p.gain_item(iid, silent=True)
bl = [Bullet(p.x, p.y, 100, 0, 1, 3, 1, 'p', (255, 255, 255))]
sigs.st(p)['shots'] = 3; sigs.on_fire(p, run, bl)
e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; e.x, e.y = p.x + 60, p.y; run.enemies = [e]
run.time = 30.0; h0 = e.hp; sigs.hit_post(run, e, bl[0], 1); h1 = e.hp; sigs.hit_post(run, e, bl[0], 1)
if 'gojo_bashi' not in p.sgs or not bl[0].fl.get('fue') or not h1 < h0 or e.hp != h1:
    print('FEHLER Gojō-Ōhashi', h0 - h1, h1 - e.hp); bad += 1
# Orochi-Taiji (Habakiri + Yashiori): Berauschte zählen doppelt, der Schnitt berauscht gewöhnliche Feinde
g.start_run('hana', 38); run = g.run; p = run.player
for iid in ('habakiri', 'yashiori_sake'):
    p.gain_item(iid, silent=True)
run.time = 30.0; e = make_boss(run, 'shuten_doji'); e.spawn_t = 0; e.x, e.y = p.x + 60, p.y; run.enemies = [e]
sigs.st(p)['hb'] = 0
for _ in range(6):                                   # 1. Treffer berauscht, Schnitt schon beim 6.
    sigs.hit_post(run, e, None, 1)
hb_boss = sigs.st(p)['hb']
from yokai.entities import Enemy
o = Enemy(run, 'gaki', p.x + 30, p.y); sigs.st(p)['hb'] = 7; sigs.hit_post(run, o, None, 1)
if 'yamata_giri' not in p.sgs or hb_boss >= 5 or not getattr(o, 'sg_drunk', 0) > run.time:
    print('FEHLER Orochi-Taiji', hb_boss, getattr(o, 'sg_drunk', 0)); bad += 1
# Seimei-Jinja (Kikyō-Mon + Seimei-Brunnen): Pentagramm-Schluss löst eine Welle um das Ziel aus
g.start_run('hana', 39); run = g.run; p = run.player
for iid in ('kikyo_mon', 'seimei_ido'):
    p.gain_item(iid, silent=True)
from yokai.entities import Enemy
e = Enemy(run, 'gaki', p.x + 60, p.y); o = Enemy(run, 'gaki', p.x + 75, p.y); e.spawn_t = o.spawn_t = 0
e.hp = o.hp = e.maxhp = o.maxhp = 999; run.enemies = [e, o]; e.sg_kk = 4; h0 = o.hp
sigs.hit_post(run, e, None, 1)
if 'kikyo_ido' not in p.sgs or not o.hp < h0 or getattr(o, 'sg_kk', 0) or run._echo:
    print('FEHLER Seimei-Jinja', h0 - o.hp, getattr(o, 'sg_kk', 0)); bad += 1
# Ido no Yūrei (Okikus Brunnen + Eimer): Brunnenwasser trifft je Geisterherz, ½ Geisterherz jeden 2. Raum
g.start_run('hana', 40); run = g.run; p = run.player
for iid in ('okiku_ido', 'tsurube'):
    p.gain_item(iid, silent=True)
e = Enemy(run, 'gaki', p.x + 60, p.y); e.spawn_t = 0; e.hp = e.maxhp = 999; run.enemies = [e]
p.spirit = 2; sigs.st(p)['tsurube'] = 1; sigs.st(p)['tsr'] = 1; h0 = e.hp
sigs.tick(p, run, 0.016)
if 'ido_reikon' not in p.sgs or not e.hp < h0 or p.spirit != 3:
    print('FEHLER Ido no Yūrei', h0 - e.hp, p.spirit); bad += 1
# Shikigami-Tsukai (Hoki Naiden + Jūni-Shinshō): Generäle jeden 8. Wurf als verfolgende Papiervögel
g.start_run('hana', 41); run = g.run; p = run.player
for iid in ('hoki_naiden', 'juni_shinsho'):
    p.gain_item(iid, silent=True)
ns = []
for _ in range(8):
    n0 = len(run.pbullets); sigs.on_fire(p, run, [Bullet(100, 100, 50, 0, 10, 3, 1, 'p', (255, 255, 255), {})])
    ns.append(sum(1 for b in run.pbullets[n0:] if b.fl.get('homing')))
if 'juni_tori' not in p.sgs or ns[7] != 12 or ns[6] != 0:
    print('FEHLER Shikigami-Tsukai', ns); bad += 1
# Yakumo Tatsu (Murakumo + Kushinadas Kamm): Kamm-Stufen beschleunigen die Wolke, ab 4 springt der Blitz weiter
g.start_run('hana', 42); run = g.run; p = run.player
for iid in ('murakumo', 'kushinada_kushi'):
    p.gain_item(iid, silent=True)
e = Enemy(run, 'gaki', p.x + 40, p.y); o = Enemy(run, 'gaki', p.x + 80, p.y)
for x in (e, o):
    x.spawn_t = 0; x.hp = x.maxhp = 999
run.enemies = [e, o]; run.hazards = []; sigs.st(p)['kushi'] = 8; sigs.st(p)['mk'] = 0
for _ in range(12):
    sigs.tick(p, run, 0.1)
if 'yakumo' not in p.sgs or sum(1 for h in run.hazards if h.kind == 'strike') < 2:
    print('FEHLER Yakumo Tatsu', [h.kind for h in run.hazards]); bad += 1
# Koishikuba (Kuzu-Blatt + Shinoda-Blatt): Fuchsnebel in jedem Raum, auch nach Treffern, mit Fuchsfeuer
g.start_run('hana', 43); run = g.run; p = run.player
for iid in ('kuzu_blatt', 'shinoda_blatt'):
    p.gain_item(iid, silent=True)
e = Enemy(run, 'gaki', p.x + 60, p.y); e.spawn_t = 0; run.enemies = [e]; run.room.cleared = False
sigs.st(p)['shinoda'] = False
sigs.on_room_enter(run)
if 'koishikuba' not in p.sgs or not getattr(e, 'sg_conf', 0) > 0 or not e.burn > 0:
    print('FEHLER Koishikuba', getattr(e, 'sg_conf', 0), e.burn); bad += 1
# Yōtō Muramasa (Muramasa + Kesa-giri): im Blutdurst jeden 2. Wurf blutrote Diagonalschnitte
g.start_run('kenji', 44); run = g.run; p = run.player
for iid in ('muramasa', 'kesagiri'):
    p.gain_item(iid, silent=True)
sigs.st(p)['shots'] = 1; sigs.st(p)['bd_t'] = run.time + 2; run.pbullets = []
sigs.on_fire(p, run, [])
if 'yoto' not in p.sgs or sum(1 for b in run.pbullets if b.col == (200, 60, 70)) != 2:
    print('FEHLER Yōtō Muramasa', [b.col for b in run.pbullets]); bad += 1
# Ganryūjima (Tsubame-gaeshi + Ichi-no-tachi): erster Hieb kehrt nach 8 s zurück, Schwalbenschnitte zu zwei Feinden
g.start_run('kenji', 45); run = g.run; p = run.player
for iid in ('tsubame_gaeshi', 'ichi_no_tachi'):
    p.gain_item(iid, silent=True)
es = [Enemy(run, 'gaki', p.x + 40 + 30 * k, p.y) for k in range(3)]
for x in es:
    x.spawn_t = 0; x.hp = x.maxhp = 999
run.enemies = es; run.room.cleared = False; run.pbullets = []; sigs.st(p)['ichi'] = True
b = run.fire_player_bullet(p.x, p.y, 0, 1, 100, 2, 1, {})
sigs.hit_post(run, es[0], b, 1)
n1 = len(run.pbullets) - 1
run.time += 8.1; sigs.tick(p, run, 0.1)
if 'ganryu' not in p.sgs or n1 < 2 or not sigs.st(p).get('ichi'):
    print('FEHLER Ganryūjima', n1, sigs.st(p).get('ichi')); bad += 1
# Senbon-gari (Tausendstes Schwert + Sieben Waffen): Waffe jeden 5. Wurf, Treffer zählen für die Schwertjagd
g.start_run('benkei', 46); run = g.run; p = run.player
for iid in ('tausendstes_schwert', 'nanatsu_dogu'):
    p.gain_item(iid, silent=True)
sigs.st(p)['shots'] = 4; sigs.st(p)['jagd'] = 29
b = run.fire_player_bullet(p.x, p.y, 0, 1, 100, 2, 1, {})
sigs.on_fire(p, run, [b])
e = Enemy(run, 'gaki', p.x + 40, p.y); e.spawn_t = 0; e.hp = e.maxhp = 999; run.enemies = [e]
sigs.hit_post(run, e, b, 1)
if 'senbon' not in p.sgs or not b.fl.get('senbon') or sigs.st(p).get('jagd_b', 0) != 0.2:
    print('FEHLER Senbon-gari', b.fl, sigs.st(p).get('jagd_b')); bad += 1
print('Signaturen/Synergien geprüft:', len(items), 'Fehler:', bad)
sys.exit(1 if bad else 0)
