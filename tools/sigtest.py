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
items = [k for k, it in data.ITEMS.items() if any(f.startswith('sig_') for f in it['fx'])]
for i, iid in enumerate(items):
    random.seed(i)
    orig = bot.play
    try:
        g.start_run('hana', 100 + i)
        g.run.player.gain_item(iid, silent=True)
        # kurzer Lauf mit demselben Bot, aber begrenzter Zeit
        run = g.run
        p = run.player
        dt = 1 / 60
        for step in range(60 * 40):
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
print('Signaturen geprüft:', len(items), 'Fehler:', bad)
sys.exit(1 if bad else 0)
