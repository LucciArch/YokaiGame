"""Hauptprogramm: Fenster, Eingabe, Menüs, Charakterwahl, Codex, Erfolge, Pause, Spielende."""
import datetime
import math
import os
import random
import sys
import pygame
from .settings import *
from . import gfx, audio, sheets, art, bestiary, props
from .save import Save
from .data import (ITEMS, ITEM_IDS, CHARS, CHAR_ORDER, ACHIEVEMENTS, ACTIVES, SYNERGIES, TRANSFORMS, BOSSES,
                   BIOMES, CHALLENGES, ENEMIES)
SYN_BY_ID = {sy['id']: sy for sy in SYNERGIES}
from .run import Run

from .texts import FX_NAMES, TAG_NAMES, fx_lines, star


class Game:
    def __init__(self, headless=False):
        pygame.init()
        self.headless = headless
        self.save = Save()
        st = self.save['settings']
        dw, dh = self.desktop_size()
        sc = max(1, min((dw - 80) // W, (dh - 120) // H)) if dw > 0 else 3
        self.fullscreen = st.get('fullscreen', False) and not headless
        self.win_size = (W * sc, H * sc)
        self.set_mode()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.Surface((W, H))
        self.clock = pygame.time.Clock()
        self.au = audio.get()
        self.au.set_volumes(st.get('sfx', 0.8), st.get('music', 0.55))
        self.state = 'title'
        self.run = None
        self.t = 0.0
        self.sel = 0
        self.toasts = []
        self.pads = []
        self.scan_pads()
        self.char_sel = 0
        self.hard = False
        self.codex_sel = 0
        self.scroll = 0
        self.confirm = None
        self.prev_buttons = set()
        self.parade = []
        self.last_char = 'hana'
        self.mouse_aim = False
        self.au.music(('yo', 220, 76, 'calm', 99))
        try:
            ic = pygame.Surface((32, 32), pygame.SRCALPHA)
            hm = gfx.mini(sheets.frame('hana', 0, 0, 1), 32)
            ic.blit(hm, (16 - hm.get_width() // 2, 0))
            pygame.display.set_icon(ic)
        except Exception:
            pass

    def desktop_size(self):
        try:
            sizes = pygame.display.get_desktop_sizes()
            if sizes and sizes[0][0] > 0:
                return sizes[0]
        except Exception:
            pass
        info = pygame.display.Info()
        return (info.current_w, info.current_h) if info.current_w > 0 else (W * 3, H * 3)

    def set_mode(self):
        """Vollbild = randloses Fenster in Desktop-Größe (kein Wechsel der Bildschirmauflösung)."""
        if self.fullscreen:
            try:
                self.window = pygame.display.set_mode(self.desktop_size(), pygame.FULLSCREEN)
                return
            except pygame.error:
                try:
                    self.window = pygame.display.set_mode(self.desktop_size(), pygame.NOFRAME)
                    return
                except pygame.error:
                    self.fullscreen = False
        self.window = pygame.display.set_mode(self.win_size, pygame.RESIZABLE)

    def scan_pads(self):
        try:
            pygame.joystick.init()
            self.pads = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for p in self.pads:
                p.init()
        except Exception:
            self.pads = []

    def rumble(self, strength, ms):
        """Controller-Vibration (falls der Controller sie kann)."""
        for p in getattr(self, 'pads', []):
            try:
                p.rumble(strength * 0.8, strength, ms)
            except Exception:
                pass

    def toast(self, title, sub='', col=(255, 220, 120), sound=True):
        self.toasts.append([title, sub, col, 3.5])
        if sound:
            audio.play('unlock')

    # ================================================================  Skalierung
    def view(self):
        ww, wh = self.window.get_size()
        sc = min(ww / W, wh / H)
        if sc >= 1:
            sc = max(1, int(sc)) if min(ww / W, wh / H) - int(sc) < 0.5 or int(sc) == 0 else sc
        sc = max(0.5, sc)
        ox = int((ww - W * sc) / 2)
        oy = int((wh - H * sc) / 2)
        return sc, ox, oy

    def mouse_game(self):
        sc, ox, oy = self.view()
        mx, my = pygame.mouse.get_pos()
        return (mx - ox) / sc, (my - oy) / sc

    # ================================================================  Eingabe
    def read_input(self, events):
        keys = pygame.key.get_pressed()
        mv = [0.0, 0.0]
        if keys[pygame.K_a]: mv[0] -= 1
        if keys[pygame.K_d]: mv[0] += 1
        if keys[pygame.K_w]: mv[1] -= 1
        if keys[pygame.K_s]: mv[1] += 1
        sh = [0.0, 0.0]
        if keys[pygame.K_LEFT]: sh[0] -= 1
        if keys[pygame.K_RIGHT]: sh[0] += 1
        if keys[pygame.K_UP]: sh[1] -= 1
        if keys[pygame.K_DOWN]: sh[1] += 1
        mb = pygame.mouse.get_pressed()
        if mb[0] and self.run:
            gx, gy = self.mouse_game()
            p = self.run.player
            sh = [gx - p.x, gy - (p.y - 4)]
        dash = active = salt = False
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_LSHIFT, pygame.K_RSHIFT):
                    dash = True
                elif e.key == pygame.K_e:
                    active = True
                elif e.key == pygame.K_q:
                    salt = True
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                dash = True
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button in (0, 5):
                    dash = True
                elif e.button in (3, 4):
                    active = True
                elif e.button == 2:
                    salt = True
        for p in self.pads:
            try:
                ax = [p.get_axis(i) for i in range(min(6, p.get_numaxes()))]
            except Exception:
                continue
            if len(ax) >= 2 and math.hypot(ax[0], ax[1]) > 0.25:
                mv = [ax[0], ax[1]]
            if len(ax) >= 4:
                rx, ry = ax[2], ax[3]
                if math.hypot(rx, ry) > 0.35:
                    sh = [rx, ry]
            if p.get_numhats():
                hx, hy = p.get_hat(0)
                if hx or hy:
                    sh = [hx, -hy]
        m = math.hypot(*mv)
        if m > 1:
            mv = [mv[0] / m, mv[1] / m]
        return {'move': mv, 'shoot': sh, 'dash': dash, 'active': active, 'salt': salt}

    def menu_keys(self, events):
        """Gibt Navigationsereignisse zurück: up/down/left/right/ok/back/tab."""
        out = []
        for e in events:
            if e.type == pygame.KEYDOWN:
                k = e.key
                if k in (pygame.K_UP, pygame.K_w): out.append('up')
                elif k in (pygame.K_DOWN, pygame.K_s): out.append('down')
                elif k in (pygame.K_LEFT, pygame.K_a): out.append('left')
                elif k in (pygame.K_RIGHT, pygame.K_d): out.append('right')
                elif k in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER): out.append('ok')
                elif k == pygame.K_ESCAPE: out += ['back', 'pause']
                elif k == pygame.K_BACKSPACE: out.append('back')
                elif k == pygame.K_p: out.append('pause')
                elif k == pygame.K_TAB: out.append('tab')
                elif k == pygame.K_h: out.append('hard')
                elif k == pygame.K_n: out.append('endless')
                elif k == pygame.K_r: out.append('retry')
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button == 0: out.append('ok')
                elif e.button == 1: out.append('back')
                elif e.button in (6, 7): out += ['back', 'pause']
                elif e.button == 3: out += ['hard', 'pad_y']
            elif e.type == pygame.JOYHATMOTION:
                hx, hy = e.value
                if hy == 1: out.append('up')
                if hy == -1: out.append('down')
                if hx == -1: out.append('left')
                if hx == 1: out.append('right')
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                out.append(('click', self.mouse_game()))
            elif e.type == pygame.MOUSEWHEEL:
                out.append('up' if e.y > 0 else 'down')
        return out

    # ================================================================  Hauptschleife
    def loop(self):
        errors = 0
        while True:
            dt = min(1 / 30, self.clock.tick(FPS) / 1000)
            try:
                self.frame(dt, pygame.event.get())
                errors = 0
            except SystemExit:
                raise
            except Exception:
                errors += 1
                self.recover(errors)

    def recover(self, n):
        """Fehler im Spiel: Bericht schreiben, zurück ins Titelmenü statt das Fenster zu schließen.
        Der Lauf bleibt ab Beginn der Ebene erhalten (Fortsetzen)."""
        import traceback
        from .settings import save_dir
        txt = traceback.format_exc()
        print(txt)
        try:
            with open(os.path.join(save_dir(), 'fehler.log'), 'a', encoding='utf-8') as f:
                f.write('--- %s  v%s  Zustand: %s\n%s\n' % (datetime.datetime.now().isoformat(timespec='seconds'), VERSION, self.state, txt))
        except OSError:
            pass
        if n > 20:
            raise SystemExit(1)
        gfx.HI.clear(); gfx.TEXT.clear(); gfx.NOCACHE.clear()
        self.run = None
        self.epi = None
        self.confirm = None
        self.state = 'title'
        self.sel = 0
        self.toast('Ein Fehler ist aufgetreten', 'Dein Lauf wurde ab Beginn der Ebene gesichert – „Fortsetzen“.', (240, 150, 140))

    def frame(self, dt, events):
        self.t += dt
        if any(e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN and e.mod & pygame.KMOD_ALT for e in events):
            self.toggle_fullscreen()                                  # Alt+Enter: nur Vollbild, nicht „Bestätigen“
            events = [e for e in events if not (e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN)]
        for e in events:
            if e.type == pygame.QUIT:
                self.quit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                self.toggle_fullscreen()
                continue
            elif e.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.win_size = (max(W, e.w), max(H, e.h))
                self.window = pygame.display.set_mode(self.win_size, pygame.RESIZABLE)
            elif e.type in (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
                self.scan_pads()
            if e.type in (pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION):
                gfx.PAD_MODE = True
            elif e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                gfx.PAD_MODE = False
        nav = self.menu_keys(events)
        getattr(self, 'st_' + self.state)(dt, events, nav)
        for tt in self.toasts:
            tt[3] -= dt
        self.toasts = [tt for tt in self.toasts if tt[3] > 0]
        self.draw_toasts()
        self.present()

    def present(self):
        gfx.HI_MODE = False
        sc, ox, oy = self.view()
        self.window.fill((0, 0, 0))
        shake = (0, 0)
        if self.run and self.state == 'play' and self.run.shake_amt > 0:
            a = self.run.shake_amt
            shake = (random.uniform(-a, a) * sc * 0.4, random.uniform(-a, a) * sc * 0.4)
        if sc == int(sc):
            img = pygame.transform.scale(self.screen, (int(W * sc), int(H * sc)))
        else:
            img = pygame.transform.scale(self.screen, (int(W * sc), int(H * sc)))
        self.window.blit(img, (ox + shake[0], oy + shake[1]))
        r = self.run
        if r and self.state in ('play', 'pause', 'over', 'options'):
            dim = 1.0
            light = r.hi_light if self.state == 'play' else None
            gfx.hi_flush(self.window, sc, ox + shake[0], oy + shake[1], dim, light)
        elif gfx.HI:
            gfx.hi_flush(self.window, sc, ox, oy, 1.0, None)
        else:
            gfx.HI.clear()
        gfx.TEXT.flush(self.window, sc, ox + shake[0], oy + shake[1])
        pygame.display.flip()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.set_mode()                                  # kann bei Fehlern auf Fenster zurückfallen
        self.save['settings']['fullscreen'] = self.fullscreen
        self.save.write()
        pygame.event.clear(pygame.VIDEORESIZE)           # alte Größenänderungen nicht aufs neue Fenster anwenden

    def quit(self):
        self.save.write()
        pygame.quit()
        sys.exit(0)

    def draw_toasts(self):
        r = self.run
        y = 68 if (self.state == 'play' and r is not None and r.hint_t > 0 and r.hint_txt) else 34   # unter der Hinweisbox
        for title, sub, col, t in self.toasts[:3]:
            a = int(255 * min(1, t * 2))
            w = max(gfx.text_w(title, 9), gfx.text_w(sub, 7)) + 20
            key = (title, sub, w, col)
            cache = self.__dict__.setdefault('_toast_bg', {})
            bg = cache.get(key)
            if bg is None:
                tmp = pygame.Surface((w, 28), pygame.SRCALPHA)
                gfx.panel(tmp, (0, 0, w, 28), 220, col)
                bg = pygame.transform.scale(tmp, (w * 2, 56))
                if len(cache) > 30:
                    cache.clear()
                cache[key] = bg
            gfx.HI.append((bg, W / 2, y + 28, a, 1.0, True))           # über den Figuren
            gfx.TEXT.add(title, W // 2, y + 3, 9, col, 'c', alpha=a)
            gfx.TEXT.add(sub, W // 2, y + 16, 7, (230, 225, 210), 'c', alpha=a)
            y += 32

    # ================================================================  Hintergrund (Titel)
    def draw_night(self, s):
        """Titel-Panorama aus art_src/title/panorama.py: Ebenen mit sanfter Parallaxe, Glitzern und Blüten."""
        t = self.t
        sway = math.sin(t * 0.11)
        for name, par in (('sky', 0), ('far', 8), ('mid', 16), ('fog', 24), ('near', 32)):
            im = gfx.env_img('_title', name)
            drift = math.sin(t * 0.07) if name == 'fog' else sway    # Nebel zieht gegen die Berge
            s.blit(im[0], (-par + int(round(drift * par)), 0))
            if name == 'sky':
                rng = random.Random(5)
                for i in range(24):                      # einige Sterne funkeln
                    x, y = rng.randrange(W), rng.randrange(150)
                    if math.hypot(x - 388, y - 64) > 55 and math.sin(t * rng.uniform(1.5, 3) + i) > 0.85:
                        s.set_at((x, y), (255, 255, 255))
                for k in range(0, 72, 3):                # Mondspiegelung: flimmernde Striche unter dem Mond
                    y = 216 + k
                    w_ = max(2, int(14 - k * 0.12 + 5 * math.sin(t * 2.3 + k * 0.7)))
                    x = 388 + int(3 * math.sin(t * 1.7 + k * 0.4) + sway * 8) - w_ // 2
                    s.fill((236, 222, 176) if k < 24 else (150, 140, 150), (x, y, w_, 1))
        lx = 480 - 70 + 32 + int(round(sway * 32))       # Tōrō aus der Vordergrund-Ebene (dort bei Breite-70)
        gfx.draw_glow(s, lx, 273, 22 + 2 * math.sin(t * 5), (255, 170, 80), 60)
        for i in range(22):                              # fallende Kirschblüten vom Zweig oben links
            rr = random.Random(100 + i)
            ph = (t * rr.uniform(0.04, 0.09) + rr.random()) % 1
            px = (rr.uniform(0, 160) + ph * 200 + math.sin(t * 1.3 + i) * 8) % W
            py = 20 + ph * (H - 20)
            s.fill((250, 190, 215), (int(px), int(py), 2, 1 + (i % 2)))
        for i in range(14):                              # Glühwürmchen über dem Schilf
            rr = random.Random(300 + i)
            x = (rr.uniform(0, W) + 18 * math.sin(t * rr.uniform(0.2, 0.5) + i)) % W
            y = rr.uniform(236, 300) + 8 * math.sin(t * rr.uniform(0.3, 0.7) + i * 2)
            b = math.sin(t * rr.uniform(1.2, 2.2) + i * 1.7)
            if b > 0.2:
                gfx.draw_glow(s, int(x), int(y), 5, (200, 240, 110), int(70 * b))
                s.fill((236, 255, 150) if b > 0.7 else (170, 200, 90), (int(x), int(y), 1, 1))
        for i in range(3):                               # Hitodama: Seelenflammen schweben über dem See
            rr = random.Random(500 + i)
            ph = (t * 0.035 + i / 3) % 1
            x = 150 + ph * 220 + 6 * math.sin(t * 0.9 + i)
            y = 214 + 10 * math.sin(t * 0.7 + i * 2) - 6
            a_ = math.sin(ph * math.pi)                  # taucht auf und vergeht wieder
            if a_ < 0.15:
                continue
            gfx.draw_glow(s, int(x), int(y), 16, (110, 170, 255), int(90 * a_))
            for k in range(6):                           # Schweif nach hinten oben, flackernd
                s.fill((70, 120, 220) if k > 2 else (130, 190, 255), (int(x - 2 - k * 2), int(y - 1 - k + math.sin(t * 7 + k) * 1.2), 4 - k // 2, 3 - k // 3))
            s.fill((150, 205, 255), (int(x) - 2, int(y) - 1, 5, 5))
            s.fill((235, 248, 255), (int(x) - 1, int(y), 3, 3))

    # ================================================================  Zustände
    MENU = ['Neuer Lauf', 'Tägliche Prüfung', 'Herausforderungen', 'Codex der Items', 'Yōkai-Lexikon', 'Erfolge', 'Statistik', 'Steuerung', 'Optionen', 'Beenden']

    def st_title(self, dt, events, nav):
        s = self.screen
        gfx.HI_MODE = True
        self.draw_night(s)
        T = gfx.TEXT
        # Einblendung beim Start: erst die Nacht, dann das Logo, dann das Menü; jede Taste kürzt ab
        it = self._intro = self.__dict__.get('_intro', 0) + dt
        if nav:
            it = self._intro = max(it, 2.1)
        if it < 1.4:
            ov = pygame.Surface((W, H)); ov.set_alpha(int(255 * (1 - it / 1.4)))
            s.blit(ov, (0, 0))
        fa = lambda t0, d: max(0.0, min(1.0, (it - t0) / d))
        la = int(255 * fa(0.9, 0.9))
        if la:
            gfx.hi_blit(gfx.env_img('_title', 'logo')[0], W // 2, 56 + int(6 * (1 - fa(0.9, 0.9)) ** 2), la)
        ma = int(255 * fa(1.5, 0.6))
        T.add('– Hyakki Yagyō –', W // 2, 60, 9, (230, 140, 130), 'c', alpha=la)
        items = self.menu_items()
        step = 14 if len(items) <= 10 else 13
        show_news = self.save.data.get('news_seen') != VERSION and not self.headless
        if self.__dict__.get('_bsel') != self.sel:      # Pinselstrich wird bei jeder Auswahl neu gezogen
            self._bsel, self._bt = self.sel, 0.0
        self._bt += dt
        if ma and not show_news:                         # dunkler Schleier hinter dem Menü, an den Seiten auslaufend
            sc_ = self.__dict__.get('_scrim')
            if sc_ is None:
                sc_ = self._scrim = pygame.Surface((200, 160), pygame.SRCALPHA)
                for x in range(200):
                    sc_.fill((8, 6, 18, int(120 * min(1, (100 - abs(x - 100)) / 45))), (x, 0, 1, 160))
            sc_.set_alpha(ma)
            s.blit(sc_, (W // 2 - 100, 78))
        for i, m in enumerate(items if not show_news else []):
            y = 84 + i * step
            sel = i == self.sel
            col = (255, 236, 200) if sel else (205, 196, 200)
            if sel and ma:
                br = gfx.env_img('_title', 'brush')[0]
                bw = max(2, int(br.get_width() * min(1.0, self._bt / 0.14)))
                gfx.hi_blit(br.subsurface((0, 0, bw, br.get_height())), W // 2 - br.get_width() // 4 + bw // 4, y + 11, ma, transient=True)
            T.add(m, W // 2, y, 10, col, 'c', alpha=ma)
        T.add('v' + VERSION + '   •   F11 / Alt+Enter Vollbild', W - 6, H - 12, 6, (140, 130, 150), 'r', alpha=ma)
        if items and items[self.sel % len(items)] == 'Fortsetzen' and not show_news:
            info = getattr(self, '_cont_info', None)
            if info is None:
                from .run import load_run_file
                d = load_run_file() or {}
                roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
                info = self._cont_info = ('%s  ·  Ebene %d  ·  Kapitel %s  ·  %d Items' % (
                    CHARS.get(d.get('char'), {}).get('name', '?'), d.get('floor_no', 0) + 1, roman[min(7, max(1, d.get('depth', 1)))],
                    len(d.get('player', {}).get('items', []))) if d else '')
            T.add(info, W // 2 + 76, 85, 6, (200, 220, 170))
        else:
            self._cont_info = None
        if show_news:
            from . import news
            w = max(gfx.text_w(l, 7) for l in news.LINES) + 30
            h = 34 + len(news.LINES) * 12
            x0, y0 = W // 2 - w // 2, 92
            gfx.hi_panel((x0, y0, w, h), 235, (230, 180, 110))
            T.add(news.TITLE, W // 2, y0 + 5, 10, (255, 225, 150), 'c')
            for i, l in enumerate(news.LINES):
                T.add('•  ' + l, x0 + 12, y0 + 22 + i * 12, 7, (235, 228, 210))
            T.add('Beliebige Taste – weiter', W // 2, y0 + h + 4, 6, (170, 160, 150), 'c')
            if nav:
                self.save.data['news_seen'] = VERSION
                self.save.write()
                audio.play('select')
            return
        for n in nav:
            if n == 'up':
                self.sel = (self.sel - 1) % len(items); audio.play('move')
            elif n == 'down':
                self.sel = (self.sel + 1) % len(items); audio.play('move')
            elif isinstance(n, tuple) and n[0] == 'click':
                mx, my = n[1]
                for i in range(len(items)):
                    if W // 2 - 70 < mx < W // 2 + 70 and 84 + i * step - 2 < my < 84 + i * step + 12:
                        self.sel = i
                        self.title_select(i)
            elif n == 'ok':
                self.title_select(self.sel)
            elif n == 'back':
                pass

    def menu_items(self):
        from .run import run_file
        has = os.path.exists(run_file())
        return (['Fortsetzen'] if has else []) + self.MENU

    def continue_run(self):
        from .run import load_run_file, clear_run_file
        d = load_run_file()
        if not d or d.get('char') not in CHARS:
            clear_run_file()
            self.toast('Kein Spielstand', 'Der gespeicherte Lauf ließ sich nicht laden.', (230, 150, 140))
            return
        try:
            self.run = Run(self, d['char'], d['seed'], d.get('hard', False), d.get('daily', False), d.get('endless', False),
                           None, restore=d)
        except Exception as e:                       # beschädigter Spielstand: lieber verwerfen als abstürzen
            print('Fortsetzen fehlgeschlagen:', e)
            clear_run_file()
            self.run = None
            self.toast('Kein Spielstand', 'Der gespeicherte Lauf ließ sich nicht laden.', (230, 150, 140))
            return
        self.last_char = d['char']
        self.state = 'play'
        self.show_tab = False

    def title_select(self, i):
        audio.play('select')
        m = self.menu_items()[i]
        if m == 'Fortsetzen':
            self.continue_run()
            return
        if m == 'Neuer Lauf':
            self.state = 'chars'
            self.char_sel = CHAR_ORDER.index(self.last_char) if self.last_char in CHAR_ORDER else 0
        elif m == 'Tägliche Prüfung':
            self.start_daily()
        elif m == 'Herausforderungen':
            if not self.save['bosses']:
                self.toast('Noch gesperrt', 'Besiege zuerst einen Boss', (230, 150, 140))
                return
            self.state = 'challenges'
            self.ch_sel = 0
        elif m == 'Codex der Items':
            self.state = 'codex'
        elif m == 'Yōkai-Lexikon':
            self.state = 'lexicon'; self.lex_sel = 0; self.lex_tab = 0
        elif m == 'Erfolge':
            self.state = 'achievements'; self.scroll = 0
        elif m == 'Statistik':
            self.state = 'stats'
        elif m == 'Steuerung':
            self.state = 'controls'
        elif m == 'Optionen':
            self.state = 'options'; self.sel = 0
        elif m == 'Beenden':
            self.quit()

    def start_run(self, char, seed=None, daily=False, challenge=None):
        self.last_char = char
        self.run = Run(self, char, seed, self.hard and not daily and not challenge and self.save['hard_unlocked'], daily,
                       getattr(self, 'endless', False) and not daily and not challenge and self.save.data.get('endless_unlocked', False),
                       challenge)
        self.state = 'play'
        self.show_tab = False

    def start_daily(self):
        today = datetime.date.today()
        seed = int(today.strftime('%Y%m%d'))
        chars = [c for c in CHAR_ORDER if c in self.save['chars']]
        ch = random.Random(seed).choice(chars)
        self.start_run(ch, seed, daily=today.isoformat())
        self.run.banner('Tägliche Prüfung', 'Alle spielen heute denselben Lauf: %s' % CHARS[ch]['name'], (255, 220, 150), True)

    # ---------------------------------------------------------------- Herausforderungen
    def st_challenges(self, dt, events, nav):
        s = self.screen
        self.menu_bg(s)
        T = gfx.TEXT
        done = set(self.save['challenges_done'])
        T.add('Herausforderungen  (%d / %d bestanden)' % (len(done), len(CHALLENGES)), W // 2, 8, 12, (255, 230, 170), 'c')
        for i, c in enumerate(CHALLENGES):
            y = 32 + i * 26
            sel = i == self.ch_sel
            gfx.panel(s, (30, y, W - 60, 23), 210 if sel else 150, (255, 210, 120) if sel else (90, 80, 90))
            spr = gfx.mini(sheets.frame(c['char'], 0, 0, 1), 19)
            s.blit(spr, (46 - spr.get_width() // 2, y + 2))
            T.add(c['name'], 58, y + 2, 9, (255, 230, 150) if sel else (220, 210, 200))
            T.add(c['desc'], 58, y + 13, 6, (210, 200, 190))
            if c['id'] in done:
                star(s, W - 44, y + 11, (255, 220, 100))
            T.add(CHARS[c['char']]['name'], W - 54, y + 7, 7, (180, 170, 160), 'r')
        T.add('Enter – Starten     Esc – Zurück', W // 2, 287, 6, (150, 140, 140), 'c')
        for n in nav:
            if n == 'up': self.ch_sel = (self.ch_sel - 1) % len(CHALLENGES); audio.play('move')
            elif n == 'down': self.ch_sel = (self.ch_sel + 1) % len(CHALLENGES); audio.play('move')
            elif n == 'back': self.state = 'title'
            elif n == 'ok':
                c = CHALLENGES[self.ch_sel]
                audio.play('select')
                self.start_run(c['char'], challenge=c['id'])
                self.run.banner('Prüfung: ' + c['name'], c['desc'], (255, 200, 140), True)
                return

    # ---------------------------------------------------------------- Charakterwahl
    def st_chars(self, dt, events, nav):
        s = self.screen
        gfx.HI_MODE = True
        self.draw_night(s)
        gfx.HI.clear()
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 120))
        s.blit(ov, (0, 0))
        T = gfx.TEXT
        T.add('Wähle deinen Charakter', W // 2, 8, 14, (255, 240, 220), 'c')
        unlocked = self.save['chars']
        n = len(CHAR_ORDER)
        for i, cid in enumerate(CHAR_ORDER):
            col_i, row_i = i % 5, i // 5
            x = 70 + col_i * 85
            y = 42 + row_i * 62
            sel = i == self.char_sel
            gfx.panel(s, (x - 30, y, 60, 54), 200 if sel else 140, (255, 210, 120) if sel else (110, 90, 80))
            hi = sheets.is_hi(cid)
            spr = sheets.frame(cid, sheets.RIGHT, (int(self.t * 8) % 4) if sel else 0, 1 if hi else 2)
            if cid not in unlocked:
                spr = gfx.tinted(spr, 'shadow')
            bob = int(abs(math.sin(self.t * 5)) * 2) if sel else 0
            if hi:
                gfx.hi_blit(spr, x, y + 41 - bob)
            else:
                s.blit(spr, (x - spr.get_width() // 2, y + 7 - bob))
            T.add(CHARS[cid]['name'] if cid in unlocked else '???', x, y + 44, 7, (240, 230, 210) if cid in unlocked else (130, 120, 120), 'c')
            wins = self.save['char_wins'].get(cid, 0)
            if wins:
                for k in range(min(wins, 3)):
                    star(s, x + 24 - k * 7, y + 6, (255, 220, 100))
        c = CHARS[CHAR_ORDER[self.char_sel]]
        cid = CHAR_ORDER[self.char_sel]
        gfx.panel(s, (20, 172, W - 40, 100), 210)
        if cid in unlocked:
            T.add('%s – %s' % (c['name'], c['title']), 32, 178, 12, (255, 230, 170))
            T.add(c['desc'], 32, 196, 8, (230, 225, 210))
            hx = 34
            for k in range(c['hp'] // 2):
                gfx.heart(s, hx, 212, 'red', 2); hx += 10
            for k in range(c['spirit'] // 2):
                gfx.heart(s, hx, 212, 'spirit', 2); hx += 10
            extra = []
            if c['active']:
                extra.append('Aktiv: ' + ACTIVES[c['active']]['name'])
            for it in c['items']:
                extra.append(ITEMS[it]['name'])
            if c['coins']:
                extra.append('%d Mon' % c['coins'])
            T.add('  •  '.join(extra) if extra else 'Keine Startitems', 32, 226, 7, (200, 190, 170))
            fx = fx_lines(c['fx'])
            if fx:
                T.add('  •  '.join(fx), 32, 240, 7, (180, 200, 230))
        else:
            T.add('Gesperrt', 32, 178, 12, (200, 150, 150))
            T.add('Freischalten: ' + c['unlock'], 32, 198, 8, (230, 210, 190))
        if self.save['hard_unlocked']:
            T.add('[H] Oni-Modus: ' + ('AN' if self.hard else 'aus'), W - 32, 258, 8,
                  (255, 110, 100) if self.hard else (190, 180, 170), 'r')
        if self.save.data.get('endless_unlocked'):
            en = getattr(self, 'endless', False)
            T.add('[N] Endlose Nacht: ' + ('AN' if en else 'aus'), W - 32, 244, 8,
                  (200, 140, 255) if en else (190, 180, 170), 'r')
        seed_txt = getattr(self, 'seed_input', None)
        if seed_txt is not None:
            gfx.panel(s, (W // 2 - 90, 132, 180, 30), 235, (200, 200, 140))
            T.add('Seed eingeben:  ' + seed_txt + ('_' if int(self.t * 2) % 2 else ' '), W // 2, 137, 9, (255, 240, 200), 'c')
            T.add('Ziffern  •  Enter – mit Seed starten  •  Esc – abbrechen', W // 2, 151, 6, (200, 190, 170), 'c')
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.unicode and e.unicode.isdigit() and len(seed_txt) < 9:
                        self.seed_input = seed_txt + e.unicode; audio.play('move')
                    elif e.key == pygame.K_BACKSPACE:
                        self.seed_input = seed_txt[:-1]
            for nv in nav:
                if nv == 'ok':
                    sd = int(self.seed_input) if self.seed_input else None
                    self.seed_input = None
                    if cid in unlocked:
                        audio.play('select')
                        self.start_run(cid, sd)
                    return
                if nv == 'back':
                    self.seed_input = None
                    return
            return
        T.add('Enter – Start     E – mit Seed     Esc – Zurück', 32, 258, 7, (170, 160, 150))
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_e and cid in unlocked:
                self.seed_input = ''
                audio.play('select')
                return
        for nv in nav:
            if nv == 'left':
                self.char_sel = (self.char_sel - 1) % n; audio.play('move')
            elif nv == 'right':
                self.char_sel = (self.char_sel + 1) % n; audio.play('move')
            elif nv in ('up', 'down'):
                self.char_sel = (self.char_sel + 5) % n; audio.play('move')
            elif nv == 'hard' and self.save['hard_unlocked']:
                self.hard = not self.hard; audio.play('select')
            elif nv == 'endless' and self.save.data.get('endless_unlocked'):
                self.endless = not getattr(self, 'endless', False); audio.play('select')
            elif nv == 'back':
                self.state = 'title'; audio.play('move')
            elif isinstance(nv, tuple) and nv[0] == 'click':
                mx, my = nv[1]
                for i in range(n):
                    x = 70 + (i % 5) * 85
                    y = 42 + (i // 5) * 62
                    if x - 30 < mx < x + 30 and y < my < y + 54:
                        if self.char_sel == i and CHAR_ORDER[i] in unlocked:
                            audio.play('select'); self.start_run(CHAR_ORDER[i]); return
                        self.char_sel = i; audio.play('move')
            elif nv == 'ok':
                if cid in unlocked:
                    audio.play('select')
                    self.start_run(cid)
                else:
                    audio.play('lock')

    # ---------------------------------------------------------------- Spielen
    def st_play(self, dt, events, nav):
        run = self.run
        if 'pause' in nav:
            self.state = 'pause'
            self.sel = 0
            audio.play('select')
            run.draw(self.screen, self.t)
            return
        inp = self.read_input(events)
        self.show_tab = pygame.key.get_pressed()[pygame.K_TAB]
        run.update(dt, inp)
        run.draw(self.screen, self.t)
        if self.show_tab:
            gfx.HI.clear()
            self.draw_itemlist(self.screen)
        if run.result:
            self.state = 'over'
            self.over_t = 0
            audio.get().music(('in', 196, 70, 'calm', 77) if run.result == 'dead' else ('yo', 262, 90, 'calm', 78))
            if run.result == 'win' and not run.challenge and not run.daily:
                from .epilogue import Epilogue
                self.epi = Epilogue(self, run)
                self.state = 'epilogue'

    def st_epilogue(self, dt, events, nav):
        gfx.HI_MODE = True
        if self.epi.frame(self.screen, dt, nav):
            self.epi = None
            gfx.HI.clear()
            self.state = 'over'
            self.over_t = 0

    def _wrap_c(self, txt, cx, y, w, size, col, alpha=255):
        lines, line = [], ''
        for word in txt.split():
            t = (line + ' ' + word).strip()
            if gfx.text_w(t, size) > w and line:
                lines.append(line)
                line = word
            else:
                line = t
        if line:
            lines.append(line)
        for i, l in enumerate(lines):
            gfx.TEXT.add(l, cx, y + i * size * 1.6, size, col, 'c', alpha=alpha)

    def draw_itemlist(self, s):
        run = self.run
        p = run.player
        gfx.TEXT.clear()
        gfx.panel(s, (20, 30, W - 40, H - 50), 225)
        T = gfx.TEXT
        T.add('%s – %s' % (CHARS[p.char]['name'], CHARS[p.char]['title']), 30, 36, 10, (255, 230, 170))
        st = p.s
        lines = [('Schaden', '%.2f' % p.damage()), ('Feuerrate', '%.2f/s' % st['rate']), ('Tempo', '%d' % st['spd']),
                 ('Reichweite', '%d' % st['range']), ('Schussgeschw.', '%d' % st['shotspd']), ('Glück', '%g' % st['luck']),
                 ('Kills', '%d' % run.kills), ('Zeit', '%d:%02d' % (run.time // 60, run.time % 60)), ('Seed', '%d' % run.seed)]
        for i, (k, v) in enumerate(lines):
            T.add(k, 30, 54 + i * 12, 7, (200, 190, 170))
            T.add(v, 120, 54 + i * 12, 7, (250, 245, 230), 'r')
        x0, y0 = 140, 54
        for i, iid in enumerate(p.items):
            it = ITEMS[iid]
            gx, gy = x0 + (i % 14) * 22, y0 + (i // 14) * 22
            gfx.draw_icon(s, it['icon'], it['col'], gx + 9, gy + 9)
        mx, my = self.mouse_game()
        for i, iid in enumerate(p.items):
            gx, gy = x0 + (i % 14) * 22, y0 + (i // 14) * 22
            if gx <= mx < gx + 20 and gy <= my < gy + 20:
                it = ITEMS[iid]
                T.add(it['name'], 140, 205, 9, it['col'])
                T.add(it['desc'] + '  –  ' + ', '.join(fx_lines(it['fx'])), 140, 219, 7, (230, 225, 210))
        y = 236
        if p.synergies:
            # Namen einzeln setzen, damit die Maus einen Namen treffen und seine Fähigkeit zeigen kann
            x = 30
            T.add('Synergien:', x, y, 7, (255, 220, 120))
            x += gfx.text_w('Synergien: ', 7)
            for sy in [sy for sy in SYNERGIES if sy['id'] in p.synergies]:
                w = gfx.text_w(sy['name'], 7)
                if x + w > W - 40:
                    x, y = 30, y + 11
                hov = x <= mx < x + w and y - 2 <= my < y + 10
                T.add(sy['name'], x, y, 7, (255, 255, 200) if hov else (255, 220, 120))
                if hov:
                    T.add(sy['name'], 140, 194, 9, (255, 220, 120))
                    self._wrap(sy['desc'] + '  –  ' + ', '.join(fx_lines(sy['fx'])), 140, 208, W - 170, 7, (230, 225, 210))
                x += w + gfx.text_w(', ', 7)
            y += 13
        if p.transforms:
            self._wrap('Transformationen: ' + ', '.join(TRANSFORMS[t]['name'] for t in p.transforms), 30, y, W - 70, 7, (180, 220, 255))

    def st_pause(self, dt, events, nav):
        run = self.run
        run.draw(self.screen, self.t)
        gfx.bake_low(self.screen)
        gfx.HI[:] = [(e[0], e[1], e[2], e[3], 0.4) + tuple(e[5:]) for e in gfx.HI]   # Figuren gedimmt unter dem Pause-Schleier
        gfx.TEXT.clear()
        s = self.screen
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150))
        s.blit(ov, (0, 0))
        items = ['Weiter', 'Items & Werte', 'Optionen', 'Lauf aufgeben',
                 'Hauptmenü' if (run.challenge or run.daily) else 'Speichern & Hauptmenü']
        if self.confirm:
            gfx.panel(s, (W // 2 - 110, 110, 220, 60), 230)
            gfx.TEXT.add('Wirklich? Der Lauf geht verloren.', W // 2, 118, 9, (255, 220, 200), 'c')
            gfx.TEXT.add('Enter – Ja      Esc – Nein', W // 2, 142, 8, (220, 210, 190), 'c')
            for n in nav:
                if n == 'ok':
                    act = self.confirm
                    self.confirm = None
                    if act == 'giveup':
                        run.player.dead = True
                        run.result = 'dead'
                        run.end_run(False)
                        self.state = 'over'
                        self.over_t = 0
                    else:
                        run.end_run(False)
                        self.run = None
                        self.state = 'title'
                        self.au.music(('yo', 220, 76, 'calm', 99))
                    return
                elif n == 'back':
                    self.confirm = None
            return
        if getattr(self, 'pause_tab', False):
            gfx.HI.clear()   # Item-Liste deckt alles ab
            self.draw_itemlist(s)
            if nav:
                self.pause_tab = False
            return
        gfx.TEXT.add('Pause', W // 2, 50, 18, (255, 240, 220), 'c')
        run.draw_path(s, W // 2, 84)
        gfx.TEXT.add(run.floor_label() + '  –  ' + run.biome['name'], W // 2, 196, 8, (220, 200, 170), 'c')
        gfx.TEXT.add('Seed %d' % run.seed + ('   •   Entspannt' if run.relaxed else '') + ('   •   Oni-Modus' if run.hard else ''),
                     W // 2, 208, 6, (170, 160, 150), 'c')
        for i, m in enumerate(items):
            y = 100 + i * 18
            if i == self.sel:
                gfx.panel(s, (W // 2 - 70, y - 2, 140, 15), 180, (200, 120, 90))
            gfx.TEXT.add(m, W // 2, y, 10, (255, 230, 150) if i == self.sel else (220, 210, 200), 'c')
        for n in nav:
            if n == 'up':
                self.sel = (self.sel - 1) % len(items); audio.play('move')
            elif n == 'down':
                self.sel = (self.sel + 1) % len(items); audio.play('move')
            elif n == 'back':
                self.state = 'play'
            elif n == 'ok' or (isinstance(n, tuple)):
                if isinstance(n, tuple):
                    mx, my = n[1]
                    hit = [i for i in range(len(items)) if W // 2 - 70 < mx < W // 2 + 70 and 98 + i * 18 < my < 113 + i * 18]
                    if not hit:
                        continue
                    self.sel = hit[0]
                audio.play('select')
                m = items[self.sel]
                if m == 'Weiter':
                    self.state = 'play'
                elif m == 'Items & Werte':
                    self.pause_tab = True
                elif m == 'Optionen':
                    self.opt_return = 'pause'
                    self.state = 'options'
                    self.sel = 0
                elif m == 'Lauf aufgeben':
                    self.confirm = 'giveup'
                elif m == 'Hauptmenü':
                    self.confirm = 'menu'
                elif m == 'Speichern & Hauptmenü':        # Lauf bleibt gespeichert (Stand: Beginn dieser Ebene)
                    self.run = None
                    self.state = 'title'
                    self.sel = 0
                    self.au.music(('yo', 220, 76, 'calm', 99))
                    self.toast('Lauf gespeichert', 'Weiter mit „Fortsetzen“ – ab Beginn der Ebene', (200, 220, 160))

    def st_over(self, dt, events, nav):
        run = self.run
        self.over_t += dt
        run.update_fx(dt)
        run.draw(self.screen, self.t)
        gfx.bake_low(self.screen)
        gfx.HI.clear()
        gfx.TEXT.clear()
        s = self.screen
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        oa = min(190, int(self.over_t * 300))
        ov.fill((0, 0, 0, oa))
        s.blit(ov, (0, 0))
        gfx.dim_hi(1 - oa / 255)
        T = gfx.TEXT
        win = run.result == 'win'
        if win:
            T.add('Sieg!' if run.depth < 6 else 'Wahrer Sieg!' if run.depth == 6 else 'Rückkehr aus Yomi!', W // 2, 30, 22, (255, 230, 150), 'c')
            T.add('Die Nacht der hundert Dämonen ist vorüber.' if run.depth < 6 else 'Der böse Stern ist gefallen. Der Himmel ist frei.' if run.depth == 6
                  else 'Izanami ruht. Der Felsen von Yomotsu Hirasaka schließt sich hinter dir.', W // 2, 60, 9, (240, 230, 210), 'c')
        else:
            T.add('Du bist gefallen…', W // 2, 30, 22, (230, 110, 110), 'c')
            ks = getattr(run.player, 'last_src', None)
            T.add('Ebene %d – %s' % (run.floor_no, run.biome['name']) + ('  (Entspannt)' if run.relaxed else ''), W // 2, 56, 9, (230, 210, 200), 'c')
            if ks:
                T.add('Bezwungen von: ' + ks, W // 2, 68, 7, (220, 150, 140), 'c')
        p = run.player
        gfx.panel(s, (60, 80, W - 120, 150), 200)
        rows = [('Charakter', CHARS[p.char]['name']), ('Zeit', '%d:%02d' % (run.time // 60, run.time % 60)),
                ('Besiegte Yokai', str(run.kills)), ('Räume', str(run.rooms_cleared)), ('Items', str(len(p.items))),
                ('Synergien', str(len(p.synergies))), ('Punkte', str(run.score())), ('Seed', str(run.seed))]
        for i, (k, v) in enumerate(rows):
            T.add(k, 75, 88 + i * 13, 8, (200, 190, 170))
            T.add(v, 200, 88 + i * 13, 8, (250, 245, 230), 'r')
        for i, iid in enumerate(p.items[:40]):
            it = ITEMS[iid]
            gfx.draw_icon(s, it['icon'], it['col'], 225 + (i % 9) * 20, 95 + (i // 9) * 20)
        if sheets.has(run.char) and sheets.is_hi(run.char):           # Porträt der Figur
            won = run.result != 'dead'
            spr = sheets.frame(run.char, sheets.LEFT, 0 if won else 6)
            if not won:
                spr = gfx.tinted(spr, 'frozen')
            gfx.draw_glow(s, 392, 208, 20, (255, 220, 150) if won else (120, 150, 230), 60)
            gfx.hi_blit(spr, 392, 224)
        if run.last_boss or getattr(run, 'bosses_beaten', None):
            bl = getattr(run, 'bosses_beaten', [])
            T.add('Besiegte Bosse: ' + (', '.join(BOSSES[b]['name'] for b in bl) if bl else '–'), W // 2, 233, 7, (240, 200, 170), 'c')
        T.add('R – Nochmal mit %s      Enter – Hauptmenü' % CHARS[p.char]['name'], W // 2, 246, 8, (230, 220, 200), 'c')
        run.draw_path(s, W // 2, 272, dead=not win)
        T.add('Ebene %d von %d' % (run.floor_no, len(run.path_nodes())), W // 2, 282, 7, (190, 170, 150), 'c')
        if self.over_t > 0.8:
            for n in nav:
                if n in ('retry', 'pad_y'):                # R bzw. Y am Controller
                    audio.play('select')
                    self.start_run(p.char)
                    return
                if n in ('ok', 'back') or isinstance(n, tuple):
                    audio.play('select')
                    self.run = None
                    self.state = 'title'
                    self.au.music(('yo', 220, 76, 'calm', 99))
                    return

    # ---------------------------------------------------------------- Codex
    def menu_bg(self, s, a=185):
        """Hintergrund für Menüseiten: Nachthimmel mit Torii, abgedunkelt."""
        # Hintergrund bewusst auf der niedrigen Ebene: Die Menütafeln liegen darüber.
        gfx.HI_MODE = False
        n0 = len(gfx.HI)
        self.draw_night(s)
        del gfx.HI[n0:]
        ov = self.__dict__.get('_menu_ov')
        if ov is None or ov.get_alpha() != a:
            ov = pygame.Surface((W, H))
            ov.fill((8, 5, 14))
            ov.set_alpha(a)
            self._menu_ov = ov
        s.blit(ov, (0, 0))

    def st_codex(self, dt, events, nav):
        s = self.screen
        gfx.HI_MODE = True
        self.draw_night(s)
        gfx.HI.clear()
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((6, 4, 12, 170))
        s.blit(ov, (0, 0))
        T = gfx.TEXT
        seen = set(self.save['seen'])
        unlocked = set(self.save['items'])
        ids = ITEM_IDS
        cols = 16
        gfx.panel(s, (18, 24, W - 36, 172), 200)
        T.add('Codex der Items  (%d / %d entdeckt)' % (len([i for i in ids if i in seen]), len(ids)), W // 2, 6, 11, (255, 230, 170), 'c')
        rows_vis = 7
        sel_row = self.codex_sel // cols
        top = max(0, min(sel_row - 3, (len(ids) - 1) // cols - rows_vis + 1))
        for i, iid in enumerate(ids):
            r, c = divmod(i, cols)
            if r < top or r >= top + rows_vis:
                continue
            x, y = 24 + c * 27, 28 + (r - top) * 24
            sel = i == self.codex_sel
            pygame.draw.rect(s, (60, 44, 60) if sel else (34, 26, 40), (x - 1, y - 1, 24, 22))
            if sel:
                pygame.draw.rect(s, (255, 210, 120), (x - 1, y - 1, 24, 22), 1)
            it = ITEMS[iid]
            if iid in seen:
                gfx.draw_icon(s, it['icon'], it['col'], x + 11, y + 10)
            elif it['locked'] and iid not in unlocked:
                pygame.draw.rect(s, (110, 90, 70), (x + 6, y + 9, 10, 8))
                pygame.draw.circle(s, (110, 90, 70), (x + 11, y + 9), 4, 1)
            else:
                hi = gfx.item_img('icons', it['icon'])
                if hi is not None:
                    gfx.hi_blit(gfx.tinted(hi, 'shadow'), x + 11, y + 18, 150)
                else:
                    T.add('?', x + 11, y + 3, 9, (120, 110, 130), 'c')
        iid = ids[self.codex_sel]
        it = ITEMS[iid]
        gfx.panel(s, (16, 200, W - 32, 92), 220)
        if iid in seen:
            T.add(it['name'], 28, 206, 11, it['col'])
            T.add('„%s“' % it['desc'], 28, 222, 8, (230, 225, 210))
            T.add(', '.join(fx_lines(it['fx'])), 28, 236, 7, (180, 210, 240))
            tags = ', '.join(TAG_NAMES[t] for t in it['tags'])
            pools = {'T': 'Schatz', 'S': 'Laden', 'B': 'Boss', 'K': 'Kami', 'O': 'Oni'}
            T.add('Thema: %s     Fundort: %s     Qualität: %s' % (tags or '–', ', '.join(pools[p] for p in it['pools']), '%d/5' % (it['q'] + 1)),
                  28, 250, 7, (200, 190, 170))
            syn = [sy for sy in SYNERGIES if iid in sy['items']]
            if syn:
                txt = []
                for sy in syn:
                    if sy['id'] in self.save['synergies_seen']:
                        txt.append(sy['name'] + ' (' + ' + '.join(ITEMS[x]['name'] for x in sy['items']) + ')')
                    else:
                        txt.append('??? (unentdeckte Synergie)')
                T.add('Synergien: ' + '; '.join(txt), 28, 264, 7, (255, 220, 120))
        elif it['locked'] and iid not in unlocked:
            T.add('Gesperrt', 28, 206, 11, (200, 150, 150))
            T.add('Wird durch einen Erfolg oder Boss-Sieg freigeschaltet.', 28, 224, 8, (210, 200, 190))
        else:
            T.add('???', 28, 206, 11, (160, 150, 170))
            T.add('Noch nicht entdeckt.', 28, 224, 8, (210, 200, 190))
            where = {'T': 'Schatzräume', 'S': 'Laden', 'B': 'Bosse', 'K': 'Kami-Schreine und Geheimräume', 'O': 'Oni-Schreine und Fluchräume',
                     'Y': 'nur in Ereignisräumen'}
            places = [where[c] for c in it['pools'] if c in where]
            if places:
                T.add('Fundort: ' + ', '.join(places), 28, 240, 7, (190, 180, 150))
        T.add('Esc – Zurück', W - 24, 280, 6, (150, 140, 140), 'r')
        for n in nav:
            if n == 'left': self.codex_sel = (self.codex_sel - 1) % len(ids)
            elif n == 'right': self.codex_sel = (self.codex_sel + 1) % len(ids)
            elif n == 'up': self.codex_sel = (self.codex_sel - cols) % len(ids)
            elif n == 'down': self.codex_sel = (self.codex_sel + cols) % len(ids)
            elif n == 'back': self.state = 'title'
            elif isinstance(n, tuple):
                mx, my = n[1]
                c = int((mx - 23) // 27)
                r = int((my - 27) // 24) + top
                i = r * cols + c
                if 0 <= c < cols and 0 <= i < len(ids):
                    self.codex_sel = i
            if n in ('left', 'right', 'up', 'down'):
                audio.play('move')

    # ------------------------------------------------------------ Yōkai-Lexikon
    LEX_EVENTS = {
        'yomeiri': dict(name='Kitsune no Yomeiri', spr='kitsune_braut',
                        lore='Regnet es bei Sonnenschein, so sagt man, heiraten die Füchse. Ihr Hochzeitszug zieht mit '
                             'Laternen durch die Nacht – wer ihn sieht, soll still bleiben und den Blick senken.',
                        ingame='Schieß nicht auf den Zug. Die Braut verneigt sich und lässt ein Geschenk zurück.'),
        'kakurenbo': dict(name='Kakurenbo', spr='zashiki',
                          lore='Zashiki-warashi ist ein Hausgeist in Kindergestalt. Solange sie bleibt, wohnt das Glück im Haus – '
                               'und manchmal spielt sie Verstecken mit den Bewohnern.',
                          ingame='Zerschlage die Urne, in der sie sich versteckt. Zwei Versuche.'),
        'hyakki': dict(name='Hyakki Yagyō', spr='chochin',
                       lore='In manchen Nächten ziehen hundert Dämonen in einer langen Parade durch die Straßen – Schirme, '
                            'Laternen, Sandalen und Oni. Wer ihr begegnet, versteckt sich besser, bis sie vorbei ist.',
                       ingame='Weiche den Reihen der Parade aus. Ohne Treffer bleiben zwei Truhen zurück.'),
        'ema': dict(name='Ema-Wand', spr=None,
                    lore='Ema sind kleine Holztafeln, auf die man in Schreinen seine Wünsche schreibt. Früher opferte man '
                         'den Göttern Pferde – heute genügt ein gemaltes.',
                    ingame='Drei Tafeln, drei Wünsche – nur einer geht in Erfüllung.'),
    }

    def _lex_entries(self):
        if self.lex_tab == 3:
            return [sy['id'] for sy in SYNERGIES], set(self.save['synergies_seen'])
        if self.lex_tab == 2:
            return list(self.LEX_EVENTS), set(self.save.data.get('events_seen', []))
        if self.lex_tab == 0:
            ids = [e for e in ENEMIES if e in bestiary.LORE and e not in bestiary.SKIP]
            seen = set(self.save.data.get('enemies_seen', []))
            return ids, seen
        ids = [b for b in BOSSES if b in bestiary.BOSS_LORE]
        seen = set(self.save.data.get('bosses_seen', [])) | set(self.save['bosses'])
        return ids, seen

    def _lex_portrait(self, bid):
        cache = self.__dict__.setdefault('_lex_img', {})
        if bid not in cache:
            img = None
            try:
                fn = os.path.join(os.path.dirname(sheets.BASE), 'lexikon', bid + '.png')
                if os.path.exists(fn):
                    img = pygame.image.load(fn).convert_alpha()
            except (OSError, pygame.error):
                img = None
            cache[bid] = img
        return cache[bid]

    def st_lexicon(self, dt, events, nav):
        s = self.screen
        gfx.HI_MODE = True
        self.draw_night(s)
        gfx.HI.clear()
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((6, 4, 12, 150))
        s.blit(ov, (0, 0))
        T = gfx.TEXT
        ids, seen = self._lex_entries()
        n_seen = len([i for i in ids if i in seen])
        T.add('Yōkai-Lexikon', W // 2, 5, 13, (255, 230, 170), 'c')
        for k, name in enumerate(('Yōkai', 'Bosse', 'Ereignisse', 'Synergien')):
            x = W // 2 - 165 + k * 110
            on = k == self.lex_tab
            T.add(('‹ %s ›' if on else '%s') % name, x, 24, 9, (255, 215, 130) if on else (150, 140, 150), 'c')
        T.add('%d / %d %s' % (n_seen, len(ids), 'entdeckt' if self.lex_tab == 3 else 'begegnet'), W - 16, 8, 7, (190, 180, 170), 'r')
        self.lex_sel = max(0, min(self.lex_sel, len(ids) - 1))
        # Liste links
        gfx.panel(s, (10, 38, 128, 252), 200)
        rows = 18
        top = max(0, min(self.lex_sel - rows // 2, len(ids) - rows))
        for r in range(rows):
            i = top + r
            if i >= len(ids):
                break
            eid = ids[i]
            y = 44 + r * 13.5
            sel = i == self.lex_sel
            if sel:
                pygame.draw.rect(s, (70, 48, 60), (13, int(y) - 1, 122, 13))
            nm = (ENEMIES[eid]['name'] if self.lex_tab == 0 else BOSSES[eid]['name'] if self.lex_tab == 1
                  else self.LEX_EVENTS[eid]['name'] if self.lex_tab == 2 else SYN_BY_ID[eid]['name']) if eid in seen else '? ? ?'
            T.add('%2d  %s' % (i + 1, nm), 18, y, 7, (255, 225, 160) if sel else ((225, 215, 200) if eid in seen else (110, 100, 115)))
        # Detail rechts
        gfx.panel(s, (146, 38, W - 156, 252), 200)
        eid = ids[self.lex_sel]
        cx = 146 + (W - 156) // 2
        if self.lex_tab == 3:
            sy = SYN_BY_ID[eid]
            known = eid in seen
            T.add(sy['name'] if known else '? ? ?', cx, 44, 12, (255, 220, 120) if known else (150, 140, 160), 'c')
            if known:
                T.add('„%s“' % sy['desc'], cx, 62, 8, (230, 225, 210), 'c')
            n = len(sy['items'])
            for k, iid in enumerate(sy['items']):
                it = ITEMS[iid]
                ix = cx + (k - (n - 1) / 2) * 80
                pygame.draw.rect(s, (34, 26, 40), (int(ix) - 12, 80, 24, 22))
                if known or iid in self.save['seen']:
                    gfx.draw_icon(s, it['icon'], it['col'], int(ix), 91)
                    T.add(it['name'], ix, 106, 7, it['col'], 'c')
                else:
                    T.add('?', ix, 85, 9, (120, 110, 130), 'c')
                    T.add('? ? ?', ix, 106, 7, (120, 110, 130), 'c')
            if known:
                self._wrap('Fähigkeit: ' + ', '.join(fx_lines(sy['fx'])), 154, 126, W - 172, 8, (170, 205, 240))
            else:
                self._wrap('Noch nicht entdeckt. Trage alle %d Items zugleich, um diese Synergie zu wecken.' % n,
                           154, 126, W - 172, 8, (180, 170, 170))
        elif eid in seen and self.lex_tab == 2:
            ev = self.LEX_EVENTS[eid]
            T.add(ev['name'], cx, 44, 12, (255, 220, 170), 'c')
            if ev['spr'] and sheets.has(ev['spr']):
                fr = sheets.frame(ev['spr'], sheets.RIGHT, int(self.t * 6) % 4, 1)
                key = (ev['spr'], int(self.t * 6) % 4)
                cache = self.__dict__.setdefault('_lex_big', {})
                if key not in cache:
                    cache[key] = pygame.transform.scale(fr, (fr.get_width() * 2, fr.get_height() * 2))
                gfx.hi_blit(cache[key], cx, 128 - int(abs(math.sin(self.t * 3)) * 2))
            else:
                im = props.ema((240, 90, 80), False)
                im = pygame.transform.scale(im, (im.get_width() * 3, im.get_height() * 3))
                s.blit(im, (cx - im.get_width() // 2, 128 - im.get_height()))
            pygame.draw.ellipse(s, (0, 0, 0), (cx - 18, 126, 36, 6))
            y = self._wrap(ev['lore'], 154, 136, W - 172, 8, (230, 225, 210))
            self._wrap('Im Spiel: ' + ev['ingame'], 154, y + 6, W - 172, 7, (170, 205, 240))
        elif eid in seen:
            if self.lex_tab == 0:
                d = ENEMIES[eid]
                kanji, lore, ingame = bestiary.LORE[eid]
                T.add(d['name'], cx, 44, 12, (255, 230, 170), 'c')
                spr = d['sprite']
                if sheets.has(spr):
                    hi = sheets.is_hi(spr)
                    fr = sheets.frame(spr, sheets.RIGHT, int(self.t * 6) % 4, 1 if hi else 2)
                    bob = int(abs(math.sin(self.t * 3)) * 2)
                    if hi:
                        if fr.get_height() < 70:
                            key = (spr, int(self.t * 6) % 4)
                            cache = self.__dict__.setdefault('_lex_big', {})
                            if key not in cache:
                                cache[key] = pygame.transform.scale(fr, (fr.get_width() * 2, fr.get_height() * 2))
                            fr = cache[key]
                        gfx.hi_blit(fr, cx, 128 - bob)
                    else:
                        s.blit(fr, (cx - fr.get_width() // 2, 128 - fr.get_height() - bob))
                elif spr in art.ARTS:
                    im = art.make(spr)
                    im = pygame.transform.scale(im, (im.get_width() * 3, im.get_height() * 3))
                    s.blit(im, (cx - im.get_width() // 2, 128 - im.get_height()))
                pygame.draw.ellipse(s, (0, 0, 0), (cx - 18, 126, 36, 6))
                y = self._wrap(lore, 154, 136, W - 172, 8, (230, 225, 210))
                y = self._wrap('Im Spiel: ' + ingame, 154, y + 6, W - 172, 7, (170, 205, 240))
                biomes = [BIOMES[b]['name'] for b in BIOMES if eid in BIOMES[b]['enemies']]
                if biomes:
                    y = self._wrap('Vorkommen: ' + ', '.join(biomes), 154, y + 4, W - 172, 7, (200, 190, 160))
                n = self.save.data.get('kill_counts', {}).get(eid, 0)
                T.add('Besiegt: %d' % n, 154, y + 4, 7, (230, 170, 150))
            else:
                b = BOSSES[eid]
                kanji, lore = bestiary.BOSS_LORE[eid]
                T.add(b['name'], cx, 44, 12, (255, 200, 170), 'c')
                T.add(b['title'], cx, 60, 8, (220, 180, 160), 'c')
                img = self._lex_portrait(eid)
                if img is not None:
                    f = min(1.0, 290 / img.get_width(), 170 / img.get_height())
                    im = img if f >= 1 else pygame.transform.scale(img, (int(img.get_width() * f), int(img.get_height() * f)))
                    gfx.hi_blit(im, cx, 72 + im.get_height() / 2)
                    y0 = 74 + im.get_height() / 2
                else:
                    y0 = 80
                beaten = eid in self.save['bosses']
                nk = self.save.data.get('kill_counts', {}).get(eid, 0)
                T.add(('Besiegt' + (' (%d×)' % nk if nk > 1 else '')) if beaten else 'Noch nicht besiegt', cx, y0, 7, (150, 220, 150) if beaten else (220, 150, 140), 'c')
                self._wrap(lore, 154, y0 + 14, W - 172, 8, (230, 225, 210))
        else:
            spr = ENEMIES[eid]['sprite'] if self.lex_tab == 0 else None
            if spr and sheets.has(spr) and sheets.is_hi(spr):
                fr = gfx.tinted(sheets.frame(spr, sheets.RIGHT, 0, 1), 'shadow')
                gfx.hi_blit(fr, cx, 128)
            else:
                T.add('? ? ?', cx, 100, 14, (130, 120, 140), 'c')
            T.add('? ? ?', cx, 140, 12, (150, 140, 160), 'c')
            T.add('Noch keine Begegnung.', cx, 160, 8, (180, 170, 170), 'c')
        T.add('Links/Rechts: Seite    Hoch/Runter: Eintrag    Esc: Zurück', W // 2, 300, 6, (150, 140, 140), 'c')
        for nv in nav:
            if nv == 'up': self.lex_sel = (self.lex_sel - 1) % len(ids)
            elif nv == 'down': self.lex_sel = (self.lex_sel + 1) % len(ids)
            elif nv in ('left', 'right'):
                self.lex_tab = (self.lex_tab + (1 if nv == 'right' else -1)) % 4; self.lex_sel = 0
            elif nv == 'back': self.state = 'title'
            elif isinstance(nv, tuple):
                mx, my = nv[1]
                if 10 <= mx <= 138 and my >= 44:
                    i = top + int((my - 44) // 13.5)
                    if 0 <= i < len(ids):
                        self.lex_sel = i
                elif my < 34:
                    self.lex_tab = min(3, max(0, int((mx - (W // 2 - 220)) // 110))); self.lex_sel = 0
            if nv in ('left', 'right', 'up', 'down'):
                audio.play('move')

    def _wrap(self, txt, x, y, w, size, col):
        T = gfx.TEXT
        line = ''
        lh = size * 1.55
        for word in txt.split():
            t = (line + ' ' + word).strip()
            if gfx.text_w(t, size) > w and line:
                T.add(line, x, y, size, col)
                y += lh
                line = word
            else:
                line = t
        if line:
            T.add(line, x, y, size, col)
            y += lh
        return y

    def st_achievements(self, dt, events, nav):
        s = self.screen
        self.menu_bg(s)
        T = gfx.TEXT
        got = set(self.save['achievements'])
        T.add('Erfolge  (%d / %d)' % (len(got), len(ACHIEVEMENTS)), W // 2, 6, 11, (255, 230, 170), 'c')
        per = 11
        self.scroll = max(0, min(self.scroll, len(ACHIEVEMENTS) - per))
        order = [a for a in ACHIEVEMENTS if a[0] in got] + [a for a in ACHIEVEMENTS if a[0] not in got]
        for i, (aid, name, desc, reward) in enumerate(order[self.scroll:self.scroll + per]):
            y = 28 + i * 23
            ok = aid in got
            gfx.panel(s, (24, y, W - 48, 20), 180, (230, 190, 90) if ok else (80, 70, 80))
            if ok:
                star(s, 32, y + 10, (255, 220, 100))
            T.add(name, 40, y + 2, 8, (255, 230, 150) if ok else (170, 160, 170))
            T.add(desc, 40, y + 11, 6, (220, 215, 200) if ok else (140, 130, 140))
            prog = {'ponpoko': ('coins', 300), 'benkei': ('kills', 500), 'okiku': ('deaths', 10),
                    'donor': ('donations', 30)}.get(aid)
            cur = None
            if prog:
                cur = min(prog[1], self.save['stats'].get(prog[0], 0))
            elif aid == 'feste':
                prog = (None, 4); cur = len(self.save.data.get('events_seen', []))
            elif aid == 'synergy10':
                prog = (None, 10); cur = len(self.save['synergies_seen'])
            elif aid in ('lexikon_half', 'lexikon_all'):
                tot = [k for k in ENEMIES if k in bestiary.LORE and k not in bestiary.SKIP]
                n = len([k for k in tot if k in self.save.data.get('enemies_seen', [])])
                prog = (None, (len(tot) + 1) // 2 if aid == 'lexikon_half' else len(tot)); cur = n
            if prog and not ok:
                cur = min(prog[1], cur)
                bx_ = W // 2 + 10
                pygame.draw.rect(s, (40, 32, 44), (bx_, y + 8, 90, 4))
                pygame.draw.rect(s, (200, 170, 90), (bx_, y + 8, int(90 * cur / prog[1]), 4))
                T.add('%d / %d' % (cur, prog[1]), bx_ + 96, y + 6, 6, (190, 180, 160))
            if reward:
                kind, val = reward
                r = {'char': lambda v: 'Charakter: ' + CHARS[v]['name'], 'item': lambda v: 'Item: ' + ITEMS[v]['name'],
                     'mode': lambda v: 'Oni-Modus' if v == 'hard' else 'Takamagahara'}[kind](val)
                T.add(r, W - 32, y + 6, 7, (180, 210, 240) if ok else (120, 120, 140), 'r')
        T.add('Hoch/Runter – blättern     Esc – Zurück', W // 2, 285, 6, (150, 140, 140), 'c')
        for n in nav:
            if n == 'up': self.scroll -= 1
            elif n == 'down': self.scroll += 1
            elif n in ('back', 'ok'): self.state = 'title'

    def st_stats(self, dt, events, nav):
        s = self.screen
        self.menu_bg(s)
        T = gfx.TEXT
        st = self.save['stats']
        T.add('Statistik', W // 2, 6, 12, (255, 230, 170), 'c')
        pt = st.get('playtime', 0)
        rows = [('Läufe', st['runs']), ('Siege', st['wins']), ('Wahre Siege (Takamagahara)', st.get('true_wins', 0)),
                ('Siege im Oni-Modus', st.get('wins_hard', 0)), ('Tode', st['deaths']), ('Besiegte Yokai', st['kills']),
                ('Gesammelte Mon', st['coins']), ('Gesammelte Items', st['items']), ('Entdeckte Items', '%d / %d' % (len(self.save['seen']), len(ITEM_IDS))),
                ('Synergien entdeckt', '%d / %d' % (len(self.save['synergies_seen']), len(SYNERGIES))),
                ('Transformationen', '%d / %d' % (len(self.save['transforms_seen']), len(TRANSFORMS))),
                ('Besiegte Bosse', '%d / %d' % (len(self.save['bosses']), len(BOSSES))), ('Oni-Pakte', st['oni_deals']),
                ('Tiefste Ebene', st.get('best_floor', 0)), ('Ereignisse erlebt', st.get('events', 0)), ('Spielzeit', '%d:%02d h' % (pt // 3600, (pt % 3600) // 60))]
        for i, (k, v) in enumerate(rows):
            col = i // 8
            r = i % 8
            x = 40 + col * 210
            T.add(k, x, 34 + r * 16, 8, (210, 200, 180))
            T.add(str(v), x + 190, 34 + r * 16, 8, (255, 245, 230), 'r')
        y = 172
        page = getattr(self, 'stats_page', 0)
        if page == 0:
            T.add('Bosse:', 40, y, 8, (255, 220, 150))
            for i, (bid, b) in enumerate(BOSSES.items()):
                ok = bid in self.save['bosses']
                T.add(b['name'] if ok else '???', 40 + (i % 4) * 105, y + 14 + (i // 4) * 13, 7, (240, 230, 210) if ok else (120, 110, 120))
        elif page == 2:
            hist = self.save.data.get('history', [])
            T.add('Letzte Läufe', 40, y, 8, (255, 220, 150))
            if not hist:
                T.add('Noch keine Läufe beendet.', 40, y + 16, 7, (170, 160, 160))
            for i, h in enumerate(reversed(hist[-6:])):
                yy = y + 14 + i * 12
                won = h.get('win')
                T.add(h.get('date', ''), 40, yy, 7, (170, 160, 160))
                T.add(CHARS.get(h.get('char'), {}).get('name', '?'), 110, yy, 7, (240, 230, 210))
                T.add('Ebene %d' % h.get('floor', 0), 180, yy, 7, (240, 230, 210))
                txt = ('Sieg' if won else 'Gefallen: ' + h.get('where', '')) + ('  (Entspannt)' if h.get('relaxed') else '')
                if not won and h.get('by'):
                    t2 = txt + ' – ' + h['by']
                    if gfx.text_w(t2, 7) <= W - 80 - 240:
                        txt = t2
                T.add(txt, 240, yy, 7, (150, 230, 150) if won else (230, 150, 140))
                T.add('%d:%02d' % (h.get('time', 0) // 60, h.get('time', 0) % 60), W - 40, yy, 7, (200, 190, 180), 'r')
        else:
            from .run import Run
            seen = self.save.data.get('biomes_seen', [])
            T.add('Biome:  %d / %d besucht' % (len(seen), len(BIOMES)), 40, y, 8, (255, 220, 150))
            order = sorted(BIOMES, key=lambda k: BIOMES[k]['depth'])
            for i, bid in enumerate(order):
                b = BIOMES[bid]
                ok = bid in seen
                q = Run.QUIRKS.get(bid)
                txt = ('%d  %s' % (b['depth'], b['name'])) if ok else '%d  ???' % b['depth']
                if ok and q:
                    txt += '  – ' + Run.QUIRK_SHORT[q]
                T.add(txt, 40 + (i % 3) * 140, y + 14 + (i // 3) * 12, 6, (240, 230, 210) if ok else (120, 110, 120))
        T.add('Links/Rechts – Bosse / Biome / Letzte Läufe', W // 2, 274, 6, (170, 160, 150), 'c')
        dl = self.save['daily']
        if dl:
            best = sorted(dl.items())[-3:]
            T.add('Tägliche Prüfung: ' + '   '.join('%s: %d' % (k, v) for k, v in best), 40, 250, 7, (200, 220, 240))
        T.add('Esc – Zurück', W // 2, 285, 6, (150, 140, 140), 'c')
        for n in nav:
            if n in ('back', 'ok'): self.state = 'title'
            elif n in ('left', 'right'):
                self.stats_page = (getattr(self, 'stats_page', 0) + (1 if n == 'right' else -1)) % 3
                audio.play('move')

    def st_controls(self, dt, events, nav):
        s = self.screen
        self.menu_bg(s)
        T = gfx.TEXT
        T.add('Steuerung', W // 2, 8, 14, (255, 230, 170), 'c')
        rows = [('Bewegen', 'W A S D', 'Linker Stick'), ('Ofuda werfen', 'Pfeiltasten / linke Maustaste', 'Rechter Stick'),
                ('Ausweichrolle', 'Leertaste / Shift / rechte Maustaste', 'A / RB'), ('Aktives Item', 'E', 'Y / LB'),
                ('Reinigungssalz', 'Q', 'X'), ('Items & Werte', 'Tab (halten)', '–'), ('Pause', 'Esc / P', 'Start'), ('Nochmal (nach dem Tod)', 'R', 'Y'),
                ('Vollbild', 'F11 / Alt+Enter', '–'), ('Seed (Figurenwahl)', 'E', '–'),
                ('Oni / Endlos (Figurenwahl)', 'H / N', '–')]
        T.add('Aktion', 40, 34, 8, (200, 180, 150)); T.add('Tastatur / Maus', 150, 34, 8, (200, 180, 150)); T.add('Controller', 360, 34, 8, (200, 180, 150))
        for i, (a, k, c) in enumerate(rows):
            y = 50 + i * 16
            gfx.panel(s, (32, y - 3, W - 64, 15), 140, (80, 70, 90))
            T.add(a, 40, y, 8, (250, 240, 220)); T.add(k, 150, y, 8, (220, 220, 240)); T.add(c, 360, y, 8, (220, 220, 240))
        tips = ['Die Rolle macht dich kurz unverwundbar.', 'Salz löscht alle Geschosse und öffnet Geheimräume an rissigen Wänden.',
                'Rot aufleuchtende Yokai greifen gleich an.']
        for i, t_ in enumerate(tips):
            T.add(t_, W // 2, 232 + i * 12, 7, (200, 190, 170), 'c')
        T.add('Esc – Zurück', W // 2, 285, 6, (150, 140, 140), 'c')
        for n in nav:
            if n in ('back', 'ok'):
                self.state = 'title'

    def st_options(self, dt, events, nav):
        s = self.screen
        if self.run and getattr(self, 'opt_return', None) == 'pause':
            self.run.draw(s, self.t)
            gfx.bake_low(s)
            gfx.HI.clear()
            gfx.TEXT.clear()
            ov = pygame.Surface((W, H), pygame.SRCALPHA); ov.fill((0, 0, 0, 170)); s.blit(ov, (0, 0))
            gfx.dim_hi(1 - 170 / 255)
        else:
            self.menu_bg(s)
        T = gfx.TEXT
        st = self.save['settings']
        opts = [('Musik', '%d%%' % round(st['music'] * 100)), ('Effekte', '%d%%' % round(st['sfx'] * 100)),
                ('Vollbild', 'An' if self.fullscreen else 'Aus'), ('Bildschirmwackeln', 'An' if st.get('shake', True) else 'Aus'),
                ('Schadenszahlen', 'An' if st.get('dmgnums', True) else 'Aus'), ('Tipps', 'An' if st.get('hints', True) else 'Aus'),
                ('Spielweise', 'Entspannt' if st.get('relaxed') else 'Normal'),
                ('Blitzeffekte', 'Reduziert' if st.get('flash', True) is False else 'Voll'),
                ('Spielstand löschen', ''), ('Zurück', '')]
        T.add('Optionen', W // 2, 30, 14, (255, 230, 170), 'c')
        for i, (k, v) in enumerate(opts):
            y = 62 + i * 18
            if i == self.sel:
                gfx.panel(s, (W // 2 - 120, y - 2, 240, 16), 180, (200, 120, 90))
            T.add(k, W // 2 - 110, y, 9, (255, 230, 150) if i == self.sel else (220, 210, 200))
            T.add(v, W // 2 + 110, y, 9, (255, 255, 255), 'r')
        T.add('Links/Rechts – ändern     Esc – Zurück', W // 2, 270, 7, (160, 150, 150), 'c')
        info = {'Spielweise': 'Entspannt: +1 Herz, nur halbe Herzen Schaden, langsamere Geschosse (ab dem nächsten Lauf)',
                'Tipps': 'Einmalige Hinweise beim ersten Betreten besonderer Räume',
                'Blitzeffekte': 'Reduziert: keine Weißblitze, schwächeres rotes Aufleuchten bei Treffern',
                'Spielstand löschen': 'Löscht alle Freischaltungen, Erfolge und Statistiken'}.get(opts[self.sel][0])
        if info:
            T.add(info, W // 2, 254, 7, (200, 210, 170), 'c')
        if self.confirm == 'reset':
            gfx.panel(s, (W // 2 - 120, 120, 240, 50), 240)
            T.add('Wirklich ALLES löschen?  Enter – Ja / Esc – Nein', W // 2, 140, 8, (255, 160, 150), 'c')
            for n in nav:
                if n == 'ok':
                    try:
                        os.remove(self.save.path)
                    except OSError:
                        pass
                    self.save = Save()
                    self.confirm = None
                    self.toast('Spielstand gelöscht', '', (255, 160, 150))
                elif n == 'back':
                    self.confirm = None
            return
        for n in nav:
            if n == 'up': self.sel = (self.sel - 1) % len(opts); audio.play('move')
            elif n == 'down': self.sel = (self.sel + 1) % len(opts); audio.play('move')
            elif n == 'back':
                self.save.write()
                self.state = getattr(self, 'opt_return', None) or 'title'
                self.opt_return = None
                self.sel = 0
            elif n in ('left', 'right', 'ok'):
                d = -1 if n == 'left' else 1
                k = opts[self.sel][0]
                if k == 'Musik':
                    st['music'] = round(min(1, max(0, st['music'] + 0.1 * d)), 2)
                elif k == 'Effekte':
                    st['sfx'] = round(min(1, max(0, st['sfx'] + 0.1 * d)), 2)
                elif k == 'Vollbild':
                    self.toggle_fullscreen()
                elif k == 'Bildschirmwackeln':
                    st['shake'] = not st.get('shake', True)
                elif k == 'Schadenszahlen':
                    st['dmgnums'] = not st.get('dmgnums', True)
                elif k == 'Tipps':
                    st['hints'] = not st.get('hints', True)
                elif k == 'Blitzeffekte':
                    st['flash'] = st.get('flash', True) is False
                elif k == 'Spielweise':
                    st['relaxed'] = not st.get('relaxed', False)
                    if st['relaxed']:
                        self.toast('Entspannt', 'Ab dem nächsten Lauf: +1 Herz, nur halbe Herzen Schaden, langsamere Geschosse',
                                   (170, 220, 170))
                elif k == 'Spielstand löschen' and n == 'ok':
                    self.confirm = 'reset'
                elif k == 'Zurück' and n == 'ok':
                    self.save.write()
                    self.state = getattr(self, 'opt_return', None) or 'title'
                    self.opt_return = None
                    self.sel = 0
                self.au.set_volumes(st['sfx'], st['music'])
                audio.play('select')


def main():
    g = Game()
    g.loop()
