import os, sys, traceback
os.environ['SDL_VIDEODRIVER']='dummy'; os.environ['SDL_AUDIODRIVER']='dummy'; os.environ['APPDATA']=os.path.join(os.environ.get('TEMP', '/tmp'), 'yokai_ui')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import pygame
from yokai.app import Game
from yokai import gfx
from yokai.settings import RX, RY
g = Game()
K = lambda k: pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode='', scancode=0)
def step(ev, n=1):
    for i in range(n): g.frame(1/60, ev if i == 0 else [])
def menu(i):
    g.state='title'; g.sel=i + (1 if 'Fortsetzen' in g.menu_items() else 0); step([K(pygame.K_RETURN)], 20)
try:
    from yokai.settings import VERSION
    g.save.data.pop('news_seen', None)
    g.state = 'title'; step([], 3); step([K(pygame.K_SPACE)], 3)
    assert g.save.data.get('news_seen') == VERSION, 'Neuigkeiten-Fenster lässt sich nicht schließen'
    for i in (3,4,5,6,7):
        menu(i); s=g.state
        for k in (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP): step([K(k)], 3)
        step([K(pygame.K_ESCAPE)], 3); print(s, '->', g.state)
    g.state = 'lexicon'; g.lex_tab = 3; g.lex_sel = 0; g.save['synergies_seen'].append('jingi'); step([], 2)
    for k in (pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT): step([K(k)], 2)
    assert g.lex_tab == 0, 'Lexikon-Seite Synergien blättert nicht weiter'
    g.save['synergies_seen'].remove('jingi')
    from yokai.data import ITEM_IDS, SYNERGIES
    jiid = SYNERGIES[0]['items'][0]; g.save['seen'].append(jiid)
    g.state = 'codex'; g.codex_sel = ITEM_IDS.index(jiid); step([K(pygame.K_RETURN)], 2)
    assert g.state == 'lexicon' and g.lex_tab == 3 and jiid in SYNERGIES[g.lex_sel]['items'], 'Codex springt nicht zur Synergie'
    step([K(pygame.K_ESCAPE)], 2); assert g.state == 'codex', 'Lexikon führt nicht zurück in den Codex'
    g.state = 'lexicon'; g.lex_back = 'title'; g.lex_tab = 3; g.lex_sel = 0; g.save['synergies_seen'].append(SYNERGIES[0]['id']); step([K(pygame.K_RETURN)], 2)
    assert g.state == 'codex' and ITEM_IDS[g.codex_sel] == jiid, 'Lexikon springt nicht zum Item'
    step([K(pygame.K_ESCAPE)], 2); assert g.state == 'lexicon', 'Codex führt nicht zurück ins Lexikon'
    step([K(pygame.K_ESCAPE)], 2); assert g.state == 'title', 'Lexikon/Codex hängen in einer Zurück-Schleife'
    g.save['synergies_seen'].remove(SYNERGIES[0]['id'])
    g.save.data.setdefault('events_seen', []).append('omikuji'); g.save['kuji_seen'][:] = ['kichi', 'kyo']
    g.state = 'lexicon'; g.lex_tab = 2; g.lex_sel = list(g.LEX_EVENTS).index('omikuji'); step([], 2)   # Lose-Zeile zeichnen
    g.save.data['events_seen'].remove('omikuji'); g.save['kuji_seen'][:] = []; g.state = 'title'
    g.save['seen'].remove(jiid)
    menu(0); print('chars', g.state)
    from yokai.data import CHAR_ORDER
    sel0 = g.char_sel; g.char_sel = CHAR_ORDER.index('kenji'); g.save['chars'].append('kenji'); step([], 2); g.st_chars(1 / 60, [], g.menu_keys([]))
    assert any('Zusatzangriff' in t[0] for t in gfx.TEXT.items), 'Figurenwahl nennt Waffen-Brücke nicht'
    g.save['chars'].remove('kenji'); g.char_sel = sel0
    step([K(pygame.K_RETURN)], 200); print('play', g.state)
    run, p = g.run, g.run.player; p.iframes = 999; start = run.room.pos
    def shinkiro():                                     # Ereignis Shinkirō in einem Nachbarraum erzwingen
        pos = next(q for q, r in run.rooms.items() if r.kind in ('normal', 'shinkiro') and q != run.room.pos)
        r = run.rooms[pos]; r.kind = 'shinkiro'; r.cleared = True; r.populated = False; r.objects = []
        run.enter_room(pos, 's'); step([], 40)
        peds = [pd for pd in run.pedestals if pd.group == 'shinkiro']
        assert len(peds) == 3 and sum(not pd.mirage for pd in peds) in ((1,) if run.depth < 4 else (1, 2)), 'Shinkirō: falsche Zahl echter Items'
        return peds
    n0 = len(p.items); mir = next(pd for pd in shinkiro() if pd.mirage); p.x, p.y = mir.x, mir.y - 6; step([], 3)
    assert len(p.items) == n0 and not [pd for pd in run.pedestals if pd.group], 'Trugbild gibt ein Item'
    real = next(pd for pd in shinkiro() if not pd.mirage); p.x, p.y = real.x, real.y - 6; step([], 3)
    assert real.item in p.items, 'echtes Shinkirō-Item fehlt'
    d0, run.depth = run.depth, 4                         # ab Kapitel II: manchmal zwei echte, das zweite kostet ein Herz
    peds = next(pp for pp in (shinkiro() for _ in range(40)) if sum(not pd.mirage for pd in pp) == 2)
    a, b = [pd for pd in peds if not pd.mirage]; hp0 = p.maxhp = max(p.maxhp, 6)
    p.x, p.y = a.x, a.y - 6; step([], 3)
    assert a.item in p.items and b.hearts == 1 and b in run.pedestals and not [pd for pd in run.pedestals if pd.mirage], 'Shinkirō-Zwilling falsch'
    p.x, p.y = b.x, b.y - 6; step([], 3)
    assert b.item in p.items and p.maxhp == hp0 - 2 and not [pd for pd in run.pedestals if pd.group], 'zweites echtes Shinkirō-Item kostet kein Herz'
    run.depth = d0
    shinkiro(); p.x, p.y = RX + 30, RY + 30; step([], 60 * 16)   # Ecke: keine Tür, kein Sockel
    assert not [pd for pd in run.pedestals if pd.group], 'Muschel schließt sich nicht'
    assert 'shinkiro' in g.save.data['events_seen']; g.save.data['events_seen'].remove('shinkiro')
    run.enter_room(start, 'n'); step([], 20); p.iframes = 0
    for k in (pygame.K_e, pygame.K_q, pygame.K_SPACE): step([K(k)], 20)
    step([K(pygame.K_ESCAPE)], 5); print('pause', g.state)
    nsy = next(sy for sy in SYNERGIES if len(sy['items']) >= 2); g.run.player.items[:] = nsy['items'][:-1]
    assert (nsy, nsy['items'][-1]) in g.run.near_synergies(), 'Pausenmenü kennt fast komplette Synergie nicht'
    g.sel = 1; step([K(pygame.K_RETURN)], 5)
    g.draw_itemlist(g.screen); assert any(t[0].startswith('Fast komplett') for t in gfx.TEXT.items), 'Pausenmenü zeigt fast komplette Synergien nicht'
    from yokai import sigs
    pl = g.run.player; pl.sgs = set(pl.sgs) | {'fuchsgeld', 'totenfaehre', 'shinsen'}
    sigs.st(pl)['nutz'] = {'fuchsgeld': 12, 'shinsen_h': 2}; sigs.st(pl)['faehre'] = 23; pl.revives = 0
    nl = sigs.nutz_lines(pl)
    assert 'Fuchsgeld: 12 Mon extra' in nl and 'Totenfähre: 23/40 Kills' in nl and 'Shinsen: 0 Schlüssel, 2 Herzen' in nl, nl
    g.draw_itemlist(g.screen); assert any(t[0] == 'Fuchsgeld: 12 Mon extra' for t in gfx.TEXT.items), 'Pausenmenü zeigt Nutz-Zähler nicht'
    step([K(pygame.K_RETURN)], 5)
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
