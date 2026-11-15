import os, sys, random, math, time, traceback
os.environ['SDL_VIDEODRIVER']='dummy'; os.environ['SDL_AUDIODRIVER']='dummy'
os.environ['APPDATA']=os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_test')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import pygame
from yokai.app import Game
from yokai.run import Run
from yokai.settings import *
from yokai import data
from yokai.entities import norm

def room_path(run, goal):
    from collections import deque
    start = run.room.pos
    prev = {start: None}
    q = deque([start])
    while q:
        c = q.popleft()
        if c == goal: break
        for d, n in run.rooms[c].doors.items():
            if n not in prev and run.rooms[n].revealed:
                prev[n] = (c, d); q.append(n)
    if goal not in prev: return None
    c = goal; last = None
    while prev[c] is not None:
        pc, d = prev[c]
        last = d; c = pc
    return last

def play(g, char, seed, god=True, dmg=1.0, max_t=2000, verbose=False):
    g.start_run(char, seed)
    run = g.run
    p = run.player
    dt = 1/60
    t = 0
    visited_goal = None
    stuck = 0
    lastpos = None
    while t < max_t and run.result is None:
        t += dt
        if god: p.iframes = 1.0
        if run.room.cleared and run.hidden_doors() and random.random() < 0.02:
            d, n = run.hidden_doors()[0]
            p.salts = max(p.salts, 1)
            dx, dy = DOOR_POS[d]
            p.x, p.y = dx + {'n':(0,20),'s':(0,-20),'w':(20,0),'e':(-20,0)}[d][0], dy + {'n':(0,20),'s':(0,-20),'w':(20,0),'e':(-20,0)}[d][1]
            run.use_salt()
        p.bonus['dmgm'] = 1  # noop
        inp = {'move':[0,0],'shoot':[0,0],'dash':random.random()<0.01,'active':random.random()<0.02,'salt':random.random()<0.003}
        en = run.nearest_enemy(p.x, p.y)
        if en:
            inp['shoot'] = [en.x-p.x, en.y-p.y]
            d = math.hypot(en.x-p.x, en.y-p.y)
            a = math.atan2(en.y-p.y, en.x-p.x) + (1.3 if (int(t)//3)%2 else -1.3)
            if d < 60: a += 0.6
            inp['move'] = [math.cos(a), math.sin(a)]
            if dmg > 1:
                for e in run.enemies:
                    if e.active(): e.hp -= 3*dmg*dt
        elif run.room.cleared and g.state=='play':
            # Items einsammeln (teleport)
            for pd in run.pedestals:
                if not pd.taken and (not pd.price or p.coins>=pd.price) and getattr(pd, '_tries', 0) < 60:
                    pd._tries = getattr(pd, '_tries', 0) + 1
                    p.x, p.y = pd.x, pd.y-6
                    break
            else:
                for pk in run.pickups:
                    if (not pk.price or p.coins >= pk.price) and getattr(pk, '_tries', 0) < 30:
                        pk._tries = getattr(pk, '_tries', 0) + 1
                        p.x, p.y = pk.x, pk.y+3
                        break
                else:
                    objs = [o for o in run.objs if o.kind in ('torii','victory','heaven','back','shrine','onsen','omikuji','saisen')]
                    exitobj = [o for o in objs if o.kind in ('victory','torii','heaven')]
                    other = [o for o in objs if o.kind in ('shrine','back') or (o.kind=='onsen' and not o.used)]
                    for o in run.objs:
                        if o.kind in ('tea', 'slots') and getattr(o, '_tries', 0) < 40:
                            o._tries = getattr(o, '_tries', 0) + 1
                            p.coins = max(p.coins, 12)
                            other = [o]
                            break
                    if other and random.random()<0.5:
                        o = other[0]; p.x, p.y = o.x, o.y
                    elif exitobj and all(r.visited for r in run.rooms.values() if r.kind != 'normal' or True) or (exitobj and t> 60*run.depth):
                        o = sorted(exitobj, key=lambda o: o.kind!='heaven')[0] if random.random()<0.7 else random.choice(exitobj); p.x, p.y = o.x, o.y
                    else:
                        # nächster unbesuchter Raum oder Boss
                        cands = [pos for pos, r in run.rooms.items() if not r.visited and r.revealed]
                        if run.room.kind=='shrine' or run.room.pos==('shrine',):
                            pass
                        goal = None
                        if cands:
                            cands.sort(key=lambda q: abs(q[0]-run.room.pos[0])+abs(q[1]-run.room.pos[1]) if run.room.pos!=('shrine',) else 0)
                            goal = cands[0]
                        else:
                            goal = run.boss_pos
                        if run.room.pos == ('shrine',):
                            o=[o for o in run.objs if o.kind=='back'][0]; p.x,p.y=o.x,o.y
                        elif goal == run.room.pos:
                            exitobj and None
                        else:
                            d = room_path(run, goal)
                            if d:
                                if run.rooms[run.room.doors[d]].locked:
                                    p.keys = max(p.keys, 1)
                                dx, dy = DOOR_POS[d]
                                ox, oy = {'n':(0,10),'s':(0,-10),'w':(10,0),'e':(-10,0)}[d]
                                if math.hypot(p.x-dx, p.y-dy) > 14:
                                    p.x, p.y = dx+ox, dy+oy
                                inp['move'] = list(DIRS[d])
        run.update(dt, inp)
        if int(t*60) % 7 == 0:
            run.draw(g.screen, t)
            from yokai import gfx
            gfx.TEXT.clear()
    return run, t

if __name__ == '__main__':
    g = Game(headless=True)
    # Echte Eingaben ignorieren: frame() ruft st_play -> run.update mit Tastatur (nichts gedrückt) – ok
    res = []
    seeds = list(range(1, int(sys.argv[1]) + 1)) if len(sys.argv)>1 else [1,2,3]
    for i, sd in enumerate(seeds):
        ch = data.CHAR_ORDER[i % len(data.CHAR_ORDER)]
        g.save['chars'] = list(data.CHAR_ORDER)
        g.save.data['heaven_unlocked'] = True
        g.hard = i % 3 == 2
        g.endless = i % 4 == 3
        g.save.data['endless_unlocked'] = True
        g.save.data['hard_unlocked'] = True
        t0 = time.time()
        try:
            run, t = play(g, ch, sd, god=True, dmg=3)
            print('seed', sd, ch, 'hard' if run.hard else '', 'result', run.result, 'depth', run.depth, 'items', len(run.player.items),
                  'syn', len(run.player.synergies), 'loop', run.loop, 'tr', run.player.transforms, 'gt %.0fs'%t, 'real %.1fs'%(time.time()-t0), flush=True)
        except Exception:
            traceback.print_exc()
            print('CRASH seed', sd, ch, 'depth', g.run.depth if g.run else None, 'room', g.run.room.kind if g.run else None)
            break
