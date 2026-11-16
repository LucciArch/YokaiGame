"""Kollision mit Requisiten: Grundfläche statt voller Kachel, Felsreihen dicht, Fliegen über Felsen/Krüge."""
import os, sys
os.environ['SDL_VIDEODRIVER'] = 'dummy'; os.environ['SDL_AUDIODRIVER'] = 'dummy'
os.environ['APPDATA'] = os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_test')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from yokai.app import Game
from yokai.settings import *
from yokai.entities import solid_hit, blocked

g = Game()
g.start_run('hana', 7)
run = g.run
room, p = run.room, run.player
room.tiles = [[T_FLOOR] * COLS for _ in range(ROWS)]
bx, by = RX + 5 * TILE, RY + 3 * TILE
room.tiles[3][5] = T_ROCK
assert solid_hit(room, bx + 16, by + 19), 'Felsmitte muss blocken'
assert not solid_hit(room, bx + 2, by + 2), 'leere Kachelecke darf nicht blocken'
assert not blocked(room, bx + 2, by + 4, 3), 'kleiner Körper passt an die Kachelecke'
room.tiles[3][6] = T_ROCK
assert solid_hit(room, bx + 32, by + 19), 'Felsreihe muss dicht bleiben'
room.tiles[3][6] = T_LANTERN
# Zu Fuß stoppt der Fels, fliegend geht es darüber, die Laterne bleibt fest
for fly, want in ((False, False), (True, True)):
    p.x, p.y = bx - 12, by + 19
    for _ in range(40):
        p.move(1.5, 0, fly)
    assert (p.x > bx + 16) == want, ('Flug' if fly else 'Fuß', p.x)
    assert p.x < bx + 32 + 16 - 9, 'Laterne muss auch fliegend blocken'
# Flug über dem Fels verloren: Figur kommt heraus
p.x, p.y = bx + 16, by + 19
for _ in range(40):
    p.move(-1.5, 0, False)
assert not solid_hit(room, p.x, p.y + 1.5, p.r - 0.5), 'Figur bleibt im Fels stecken'
# Grundfläche je Sprite-Variante: schmale Felsen blocken schmal, Reihen bleiben dicht
from yokai import gfx, entities
from yokai.data import BIOMES
entities.FOOT_BIOME = BIOMES['ryugu']
room.tiles = [[T_FLOOR] * COLS for _ in range(ROWS)]
narrow = None
for tx in range(1, COLS - 1):
    fx, hw = gfx.rock_foot(RX + tx * TILE, by, BIOMES['ryugu'])
    if hw <= 8:
        narrow = tx, fx, hw; break
assert narrow, 'Ryūgū braucht eine schmale Variante'
tx, fx, hw = narrow
room.tiles[3][tx] = T_ROCK
x0 = RX + tx * TILE
assert solid_hit(room, x0 + fx, by + 19), 'schmaler Fels muss in der Mitte blocken'
assert not solid_hit(room, x0 + fx + hw + 3, by + 19, 1), 'schmaler Fels darf neben sich nicht blocken'
for b in BIOMES.values():
    for x in range(0, 3 * 32 * 7, 32):
        f = gfx.rock_foot(x, 0, b)
        assert f is None or (5 <= f[1] <= 12 and 4 <= f[0] <= 28), (b.get('_id'), f)
print('Kollisionstest ok')
