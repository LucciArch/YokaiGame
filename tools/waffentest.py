"""Waffen-Items wirken mit den Wurf-Items zusammen: Mehrfachwurf, Zielsuche, Rückwurf, Feuer, Abprall."""
import os, sys, math, random
_rnd = random.random
os.environ['SDL_VIDEODRIVER'] = 'dummy'; os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['APPDATA'] = os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_test')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from yokai.app import Game
from yokai.entities import Enemy
from yokai.settings import *

g = Game(headless=True)
bad = 0


def setup(**f):
    g.start_run('hana', 5)
    r = g.run
    r.enemies = []; r.pbullets = []; r.slashes = []
    for row in r.room.tiles:
        row[:] = [0] * len(row)
    p = r.player
    p.x, p.y = RX + 60, RY + RH / 2
    for k, v in f.items():
        p.f[k] = v
    return r, p


def check(ok, msg):
    global bad
    if not ok:
        print('FEHLER', msg); bad += 1


# Lichtstrahl + Mehrfachwurf: drei Strahlen
r, p = setup(w_laser=1, multishot=2)
p.fire((1, 0))
check(sum(1 for s in r.slashes if s['kind'] == 'w_laser') == 3, 'Laser + Mehrfachwurf gibt nicht 3 Strahlen')
# Lichtstrahl + Zielsuche: Feind schräg neben der Schusslinie wird getroffen
r, p = setup(w_laser=1, homing=1)
e = Enemy(r, 'kodama', p.x + 150, p.y + 50); r.enemies.append(e); e.spawn_t = 0
hp = e.hp
p.fire((1, 0))
check(e.hp < hp, 'Laser + Zielsuche trifft den schrägen Feind nicht')
# Lichtstrahl + Feuer: Feind brennt
r, p = setup(w_laser=1, burn=1)
e = Enemy(r, 'kodama', p.x + 150, p.y); r.enemies.append(e); e.spawn_t = 0
p.fire((1, 0))
check(e.burn > 0, 'Laser + Feuer setzt keinen Brand')
# Lichtstrahl + Abprall: gespiegelter zweiter Strahl
r, p = setup(w_laser=1, bounce=1)
p.fire((1, 0))
check(sum(1 for s in r.slashes if s['kind'] == 'w_laser') == 2, 'Laser + Abprall wird nicht gespiegelt')
# Schwert + Mehrfachwurf + Rückwurf: Klingenwellen und Hieb nach hinten
r, p = setup(w_sword=1, multishot=2, back=1)
p.fire((1, 0))
check(sum(1 for b in r.pbullets if b.crescent) == 3, 'Schwert + Mehrfachwurf erzeugt keine Klingenwellen')
check(sum(1 for s in r.slashes if s['kind'] == 'w_sword') == 2, 'Schwert + Rückwurf schlägt nicht nach hinten')
# Bogen + Gift + Mehrfachwurf
r, p = setup(w_bow=1, multishot=1, poison=1)
p.fire((1, 0))
check(len(r.pbullets) == 2 and all(b.fl.get('poison') for b in r.pbullets), 'Bogen + Gift + Mehrfachwurf')
# Fächer + Zielsuche: Windklingen suchen Ziele
r, p = setup(w_fan=1, homing=1)
p.fire((1, 0))
check(r.pbullets and all(b.fl.get('homing') for b in r.pbullets), 'Fächer + Zielsuche')
# Kreisschild + Feuer: Feind am Schild brennt
NOIN = {'move': [0, 0], 'shoot': [0, 0], 'dash': False, 'active': False, 'salt': False}
r, p = setup(orbital=1, burn=1)
ox, oy = p.orbitals()[0]
e = Enemy(r, 'nurikabe', ox, oy); r.enemies.append(e); e.spawn_t = 0
for _ in range(30):
    e.x, e.y = p.orbitals()[0]
    r.update(1 / 60, NOIN)
check(e.burn > 0, 'Kreisschild + Feuer setzt keinen Brand')
# Aura + Gift
r, p = setup(aura=1, poison=1)
e = Enemy(r, 'nurikabe', p.x + 12, p.y); r.enemies.append(e); e.spawn_t = 0
for _ in range(40):
    r.update(1 / 60, NOIN)
check(e.poison > 0, 'Aura + Gift vergiftet nicht')
# Gefolge + Frost: Gefolge-Würfe tragen die Item-Wirkung
from yokai.entities import Familiar
r, p = setup(slow=1)
p.familiars.append(Familiar(0))
for _ in range(60):
    r.update(1 / 60, dict(NOIN, shoot=[1, 0]))
check(any(b.fl.get('slow') for b in r.pbullets), 'Gefolge wirft ohne Frost')
# Fähigkeits-Geschosse (aktive Items, Signaturen) erben Feuer/Gift/Frost
r, p = setup(poison=1)
b = r.fire_player_bullet(p.x, p.y, 0, 3, 200, 3, 1, {'homing': 1})
check(b.fl.get('poison') and b.fl.get('homing'), 'Fähigkeits-Geschoss erbt kein Gift')
# Wurf-Fähigkeiten (on_fire) wirken auf den Hieb selbst: Nase brennt verdoppelt den Schwerthieb
from yokai import sigs


def sword_hit(sg=(), **f):
    r, p = setup(w_sword=1, **f)
    p.sgs = set(sg)
    e = Enemy(r, 'nurikabe', p.x + 20, p.y - 4); r.enemies.append(e); e.spawn_t = 0
    e.hp = e.maxhp = 999
    p.fire((1, 0))
    return r, p, e, 999 - e.hp


_, _, _, plain = sword_hit()
_, _, _, nase = sword_hit({'nasebrennt'})
check(nase > plain * 1.8, 'Nase brennt verdoppelt den Schwerthieb nicht (%.1f / %.1f)' % (nase, plain))
# Sonne & Mond färbt den Strahl: jeder zweite Angriff brennt
r, p = setup(w_laser=1)
p.sgs = {'sonne_mond'}
e = Enemy(r, 'nurikabe', p.x + 120, p.y - 4); r.enemies.append(e); e.spawn_t = 0
e.hp = e.maxhp = 999
p.fire((1, 0)); p.fire((1, 0))
check(e.burn > 0, 'Sonne & Mond entzündet den Strahl nicht')
# Großer Schlag einer Hiebwaffe weckt die Tempelmusik
r, p, e, _ = sword_hit({'tempelmusik'}, big_every=1)
check('tempelmusik' in sigs.st(p).get('syn_seen', []), 'Großer Schwerthieb weckt die Tempelmusik nicht')
# Goldwurf mit Waffe: Treffer markiert den Feind (Münzen beim Tod)
r, p, e, _ = sword_hit(gold_shots=1)
check(e.gold_hit, 'Goldwurf-Item wirkt nicht beim Schwerthieb')
r, p = setup(w_bow=1, gold_shots=1)
p.fire((1, 0))
check(r.pbullets and all(b.gold for b in r.pbullets), 'Goldwurf-Item wirkt nicht beim Bogen')
# Hit-Sigs bei Waffen: Sichel-Hiebe zählen als gebogen (Mondsichel-Klinge), ferne Strahltreffer als weit (Kyūdō)
r, p, e, _ = sword_hit({'schnitt', 'sichel', 'mondschnitt'})
check(getattr(e, 'sg_bleed', 0) == 2, 'Mondsichel-Klinge: Sichel-Hieb blutet nicht tief')


def laser_dmg(dist, sg):
    r, p = setup(w_laser=1)
    p.sgs = set(sg)
    e = Enemy(r, 'nurikabe', p.x + dist, p.y - 4); r.enemies.append(e); e.spawn_t = 0
    e.hp = e.maxhp = 999
    p.fire((1, 0))
    return 999 - e.hp


check(laser_dmg(250, {'kyudo'}) > laser_dmg(30, {'kyudo'}) * 1.4, 'Kyūdō: ferner Strahltreffer nicht stärker')
# Wurfstern: ein Schwerthieb in eine Gruppe gibt genau einen Abpraller
r, p = setup(w_sword=1)
p.sgs = {'wurfstern'}
for dy in (-14, 0, 14):
    e = Enemy(r, 'nurikabe', p.x + 20, p.y - 4 + dy); r.enemies.append(e); e.spawn_t = 0; e.hp = e.maxhp = 999
e = Enemy(r, 'nurikabe', p.x + 110, p.y); r.enemies.append(e); e.spawn_t = 0; e.hp = e.maxhp = 999
p.fire((1, 0))
check(sum(1 for b in r.pbullets if b.fl.get('_ric')) == 1, 'Wurfstern + Schwert: nicht genau ein Abpraller')
# Laternen-Items vergrößern und färben das Licht der Spielerin
r, p = setup()
p.gain_item('chochin_feuer', silent=True)
lx, ly, lr, lc = r.collect_lights()[0]
check(lr > 90 and lc == (230, 70, 50), 'Chōchin-Feuer leuchtet nicht um die Spielerin')
# Kitsune-Laterne (aktiv) und Feuer-Anhänger leuchten ebenfalls
r, p = setup()
base = r.collect_lights()[0][2]
p.active, p.trinket = 'kitsune_laterne', 'am_hi'
lx, ly, lr, lc = r.collect_lights()[0]
check(lr == base + 32 and lc == (255, 140, 40), 'Kitsune-Laterne/Feuer-Anhänger leuchten nicht')
# Tessos Schwarm: der Strahl durchbohrt von Natur aus, höchstens eine Ratte pro Strahl
random.random = lambda: 0.0
r, p = setup(w_laser=1)
p.sgs = {'rattenschwarm'}
for dx in (40, 80, 120):
    e = Enemy(r, 'nurikabe', p.x + dx, p.y - 4); r.enemies.append(e); e.spawn_t = 0; e.hp = e.maxhp = 999
p.fire((1, 0))
check(sum(1 for b in r.pbullets if b.fl.get('_rat')) == 1, 'Tessos Schwarm + Strahl: nicht genau eine Ratte')
# Spiegelung des Strahls an der Wand weckt Abprall-Fähigkeiten (Kappa-Festmahl, Brandung)
r, p = setup(w_laser=1, bounce=1)
p.sgs = {'kappa_fest', 'brandung'}
p.fire((1, 0))
check('kappa_fest' in sigs.st(p).get('syn_seen', []), 'Strahl-Spiegelung weckt Kappa-Festmahl nicht')
check(sum(1 for b in r.pbullets if b.fl.get('_br')) == 2, 'Strahl-Spiegelung weckt Brandung nicht genau einmal')
random.random = _rnd
# Feuerwerk über Edo: zerplatzende Sprengsiegel-Hiebe sprühen brennende Funken
r, p, e, _ = sword_hit({'feuerwerk'}, explode=1)
check(sum(1 for b in r.pbullets if b.fl.get('burn')) == 0, 'Feuerwerk zündet ohne Explosion')
r, p = setup(w_sword=1, explode=1)
p.sgs = {'feuerwerk'}
e = Enemy(r, 'nurikabe', p.x + 20, p.y - 4); r.enemies.append(e); e.spawn_t = 0; e.hp = 1
p.fire((1, 0))
check(sum(1 for b in r.pbullets if b.fl.get('burn')) == 5, 'Feuerwerk: Sprengsiegel-Hieb sprüht keine fünf Funken')
# Seitenhiebe (Kunai) treffen einen großen Feind direkt daneben nicht ein zweites Mal im selben Angriff
def big_hit(**f):
    r, p = setup(w_sword=1, **f)
    e = Enemy(r, 'nurikabe', p.x + 14, p.y); r.enemies.append(e); e.spawn_t = 0
    e.hp = e.maxhp = 999; e.r = 30                          # bossgroß, reicht bis neben die Spielerin
    p.fire((1, 0))
    return 999 - e.hp


plain, side = big_hit(), big_hit(side=1)
check(plain > 0 and abs(side - plain) < 0.01, 'Schwert + Seitenwurf trifft denselben Feind mehrfach (%.1f / %.1f)' % (side, plain))
# Hannya-Ring bei Treffer: ein großer Feind direkt daneben wird nur einmal getroffen, nicht von allen 12 Geschossen
r, p = setup(hurt_ring=1)
e = Enemy(r, 'nurikabe', p.x + 14, p.y); r.enemies.append(e); e.spawn_t = 0
e.hp = e.maxhp = 999; e.r = 30
p.hp = p.maxhp = 6; p.iframes = 0; p.hurt(1)
for _ in range(30):
    r.update_bullets(1 / 60)
check(0 < 999 - e.hp <= p.damage() * 1.5 + 0.01, 'Hannya-Ring trifft einen großen Feind mehrfach (%.1f)' % (999 - e.hp))
# Figuren-Waffe hat Vorrang vor Waffen-Items; das Item wird zum Zusatzangriff
from yokai import weapons
for ch, item, ok in (('kotaro', 'amaterasu', lambda r: any(s['kind'] == 'w_laser' for s in r.slashes) and any(getattr(b, 'wind', 0) for b in r.pbullets)),
                     ('kenji', 'yumi', lambda r: any(s['kind'] == 'w_sword' for s in r.slashes) and sum(getattr(b, 'arrow', 0) for b in r.pbullets) == 1),
                     ('akago', 'tengu_faecher', lambda r: any(s['kind'] == 'w_club' for s in r.slashes) and sum(getattr(b, 'wind', 0) for b in r.pbullets) == 3),
                     ('benkei', 'hachiman_bogen', lambda r: sum(getattr(b, 'arrow', 0) for b in r.pbullets) == 1)):
    g.start_run(ch, 5)
    r = g.run; p = r.player
    r.enemies = []; r.pbullets = []; r.slashes = []
    p.gain_item(item, silent=True)
    if ch == 'benkei':
        p.gain_item('ame_nuboko', silent=True)              # Göttliches Arsenal: nur ein Pfeil, nicht zwei
    p.fire((1, 0))
    check(weapons.weapon_of(p) == weapons._own(p) and ok(r), '%s + %s: Figuren-Waffe/Zusatzangriff fehlt (%s)' % (ch, item, weapons.weapon_of(p)))
print('Waffen-Synergien geprüft, Fehler:', bad)
sys.exit(1 if bad else 0)
