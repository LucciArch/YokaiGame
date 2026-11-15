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
