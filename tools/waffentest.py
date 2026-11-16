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
print('Waffen-Synergien geprüft, Fehler:', bad)
sys.exit(1 if bad else 0)
