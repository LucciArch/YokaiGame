import os, sys, math, random, traceback, time
os.environ['SDL_VIDEODRIVER']='dummy'; os.environ['SDL_AUDIODRIVER']='dummy'; os.environ['APPDATA']=os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_test')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import pygame
from yokai.app import Game
from yokai import data, gfx
from yokai.bosses import make_boss
from yokai.settings import *
g = Game(headless=True)
for depth, pool in data.BOSS_POOL.items():
    for bid in pool:
        g.start_run('hana', 100)
        run = g.run
        run.depth = depth
        run.room.cleared = False
        p = run.player
        for i in range(depth*3):  # ein paar Items, wie in einem echten Lauf
            p.gain_item(run.pick_item('T'), silent=True)
        b = make_boss(run, bid); run.enemies=[b]; run.boss=b
        t=0; dt=1/60; hits=0; maxeb=0
        try:
            while not b.dead and t < 240:
                t+=dt
                hp0 = p.total_hp()
                p.iframes = 0 if int(t)%10 < 5 else 1  # manchmal verwundbar zum Zählen
                inp={'move':[math.cos(t*0.9), math.sin(t*1.3)],'shoot':[b.x-p.x,b.y-p.y],'dash':False,'active':random.random()<0.01,'salt':False}
                run.update(dt, inp)
                if p.total_hp() < hp0: hits += 1
                p.hp = p.maxhp; p.dead=False; run.result=None
                maxeb = max(maxeb, len(run.ebullets))
                if int(t*60)%30==0: run.draw(g.screen, t); gfx.TEXT.clear()
            print('%-12s depth %d  killed=%s  t=%5.1fs  phase=%d hits=%d maxbullets=%d dps=%.1f' % (bid, depth, b.dead, t, b.phase, hits, maxeb, p.damage()*p.s['rate']))
        except Exception:
            traceback.print_exc(); print('CRASH', bid); break
        if depth == 7:   # Endbossin in Yomi: drei Phasen, die Arena wird dunkler
            run.update(1 / 60, {'move': [0, 0], 'shoot': [0, 0], 'dash': False, 'active': False, 'salt': False})
            assert not [h for h in run.hazards if getattr(h, 'boss', None) is b], 'Hände bleiben nach dem Tod'
            assert b.phase == 3 and b.extra_dark > 0 and run.dark_level() == run.biome['dark'], (b.phase, b.extra_dark)

# Göttlicher Schutz: ab Kapitel VI höchstens 2 % pro Treffer und 8 % pro Sekunde
g.start_run('hana', 7)
run = g.run; run.depth = 6; run.room.cleared = False
b = make_boss(run, 'mikaboshi'); run.enemies = [b]; run.boss = b
b.spawn_t = 0
h0 = b.hp
run.damage_enemy(b, 1e9, None)
assert abs((h0 - b.hp) - b.maxhp * 0.02) < 1, (h0, b.hp)
for _ in range(20):
    run.damage_enemy(b, 1e9, None)
assert h0 - b.hp <= b.maxhp * 0.08 + 1, h0 - b.hp
assert b.ward_t > 0
print('Göttlicher Schutz greift: %.1f %% in einem Augenblick' % ((h0 - b.hp) / b.maxhp * 100))

# Yomi-Pforte: nach dem ersten Wahren Sieg führt sie von Kapitel VI nach Kapitel VII zu Izanami
g.start_run('hana', 8); run = g.run
run.save['stats']['true_wins'] = 1
run.depth = 6; run.objs = []; run.boss_room_rewards()
gate = [o for o in run.objs if o.kind == 'yomi']
assert gate, [o.kind for o in run.objs]
run.interact(gate[0])
assert (run.depth, run.biome_id, run.boss_id) == (7, 'yomi_oku', 'izanami'), (run.depth, run.biome_id, run.boss_id)
run.objs = []; run.boss_room_rewards()
assert [o.kind for o in run.objs if o.kind in ('victory', 'yomi')] == ['victory']
g.start_run('hana', 9); run = g.run; run.depth = 6; run.go_deeper()
assert run.depth == 1 and run.loop == 1          # Endlos-Torii führt weiter in die Schleife
print('Yomi-Pforte OK')

# Rückkehr aus Yomi: der erste Sieg über Izanami schaltet den Pfirsich frei
g.start_run('hana', 10); run = g.run; run.depth = 7
run.save['achievements'] = [a for a in run.save['achievements'] if a != 'yomi']
run.end_run(True)
assert 'yomi' in run.save['achievements'] and 'yomi_momo' in run.save['items']
from yokai.epilogue import Epilogue, STORY_YOMI
assert Epilogue(g, run).blocks[0] == STORY_YOMI[0]
# Pfirsich: Treffer wirft drei Pfirsiche und verscheucht nahe Feinde
g.start_run('hana', 11); run = g.run; p = run.player
p.gain_item('yomi_momo', silent=True)
e = run.spawn_enemy('shikome', p.x + 40, p.y); e.spawn_t = 0
nb = len(run.pbullets); p.iframes = 0; p.hurt(1, 'Test')
assert len(run.pbullets) - nb == 3 and getattr(e, 'sg_fear', 0) > 0, (len(run.pbullets) - nb, getattr(e, 'sg_fear', 0))
print('Rückkehr aus Yomi OK')
