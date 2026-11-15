import os, sys, traceback
os.environ['SDL_VIDEODRIVER']='dummy'; os.environ['SDL_AUDIODRIVER']='dummy'; os.environ['APPDATA']=os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_ui')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import pygame
from yokai.app import Game
g = Game()
K = lambda k: pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode='', scancode=0)
def step(ev, n=1):
    for i in range(n): g.frame(1/60, ev if i == 0 else [])
def menu(i):
    g.state='title'; g.sel=i + (1 if 'Fortsetzen' in g.menu_items() else 0); step([K(pygame.K_RETURN)], 20)
try:
    for i in (3,4,5,6,7):
        menu(i); s=g.state
        for k in (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP): step([K(k)], 3)
        step([K(pygame.K_ESCAPE)], 3); print(s, '->', g.state)
    menu(0); print('chars', g.state); step([K(pygame.K_RETURN)], 200); print('play', g.state)
    for k in (pygame.K_e, pygame.K_q, pygame.K_SPACE): step([K(k)], 20)
    step([K(pygame.K_ESCAPE)], 5); print('pause', g.state)
    g.sel = 1; step([K(pygame.K_RETURN)], 5); step([K(pygame.K_RETURN)], 5)
    g.sel = 2; step([K(pygame.K_RETURN)], 5); print('opts', g.state); step([K(pygame.K_ESCAPE)], 5); print('back', g.state)
    g.sel = 3; step([K(pygame.K_RETURN)], 5); step([K(pygame.K_RETURN)], 60); print('over', g.state)
    step([K(pygame.K_r)], 60); print('retry', g.state)
    step([K(pygame.K_ESCAPE)], 5); g.sel = 4; step([K(pygame.K_RETURN)], 5); step([K(pygame.K_RETURN)], 10); print('menu', g.state)
    menu(1); print('daily', g.state, g.run.daily, g.run.char)
    step([], 300)
    print('UI OK')
except SystemExit:
    print('exit')
except Exception:
    traceback.print_exc()
    sys.exit(1)
