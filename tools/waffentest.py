"""Waffen-Items wirken mit den Wurf-Items zusammen: Mehrfachwurf, Zielsuche, Rückwurf, Feuer, Abprall."""
import os, sys, math
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
print('Waffen-Synergien geprüft, Fehler:', bad)
sys.exit(1 if bad else 0)
