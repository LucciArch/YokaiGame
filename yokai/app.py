"""Hauptprogramm: Fenster, Eingabe, Menüs, Charakterwahl, Codex, Erfolge, Pause, Spielende."""
import datetime
import math
import os
import random
import sys
import pygame
from .settings import *
from . import gfx, audio
from .save import Save
from .data import (ITEMS, ITEM_IDS, CHARS, CHAR_ORDER, ACHIEVEMENTS, ACTIVES, SYNERGIES, TRANSFORMS, BOSSES,
                   BIOMES)
from .run import Run

FX_NAMES = {
    'dmg': ('Schaden', '+'), 'dmgm': ('Schaden', '×'), 'rate': ('Feuerrate', '+'), 'ratem': ('Feuerrate', '×'),
    'spd': ('Tempo', '+'), 'shotspd': ('Schussgeschw.', '+'), 'range': ('Reichweite', '+'), 'luck': ('Glück', '+'),
    'size': ('Talismangröße', '+'), 'hp': ('Herzcontainer', '+'), 'heal': ('Heilung (½)', '+'),
    'spirit': ('Geisterherzen (½)', '+'), 'coins': ('Mon', '+'), 'keys': ('Schlüssel', '+'), 'salts': ('Salz', '+'),
    'fullheal': ('Volle Heilung', ''), 'homing': ('Zielsuchend', ''), 'pierce': ('Durchbohrend', ''),
    'bounce': ('Abprallend', ''), 'spectral': ('Durch Wände', ''), 'explode': ('Explosiv', ''), 'burn': ('Brennen', ''),
    'slow': ('Verlangsamen', ''), 'poison': ('Gift', ''), 'chain': ('Kettenblitz', ''), 'split': ('Teilen sich', ''),
    'boomerang': ('Bumerang', ''), 'wave': ('Wellenflug', ''), 'knock': ('Rückstoß', ''), 'crit': ('Krit-Chance', '%'),
    'freeze': ('Einfrieren', '%'), 'multishot': ('Zusatzschüsse', '+'), 'back': ('Schuss nach hinten', '+'),
    'side': ('Seitenschüsse', '+'), 'orbital': ('Umkreisende Schilde', '+'), 'familiar': ('Shikigami-Begleiter', '+'),
    'aura': ('Schadensaura', '+'), 'fly': ('Fliegen', ''), 'dash_fire': ('Feuerspur beim Rollen', ''),
    'dash_dmg': ('Rolle verletzt Feinde', ''), 'dash_reflect': ('Rolle löscht Geschosse', ''),
    'hurt_ring': ('Talismanring bei Treffer', ''), 'hurt_dmg': ('Wut bei Treffer', ''),
    'kill_heal': ('Heilung bei Kill', '%'), 'kill_explode': ('Explosion bei Kill', '%'),
    'clear_heal': ('Heilung bei Raumende', '%'), 'money_dmg': ('Schaden durch Mon', ''), 'shield': ('Schild pro Raum', ''),
    'revive': ('Extra-Leben', '+'), 'map': ('Zeigt die Karte', ''), 'magnet': ('Münzmagnet', ''),
    'discount': ('Rabatt im Laden', ''), 'gold_shots': ('Goldene Talismane', '%'), 'big_every': ('Jeder N. Schuss mächtig', ''),
    'rage': ('Stärker bei wenig Leben', ''), 'salts_regen': ('Salz bei Raumende', '%'), 'curse_immune': ('Immun gegen Flüche', ''),
    'raijin_chance': ('Blitz-Chance', '%'),
}
TAG_NAMES = {'kitsune': 'Kitsune', 'raijin': 'Donner', 'oni': 'Oni', 'shikigami': 'Shikigami', 'yurei': 'Yūrei',
             'tengu': 'Tengu', 'ryu': 'Drache', 'kami': 'Kami', 'tanuki': 'Tanuki'}


def star(s, x, y, col):
    pts = []
    for i in range(10):
        a = i / 10 * math.tau - math.pi / 2
        r = 3.5 if i % 2 == 0 else 1.5
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
    pygame.draw.polygon(s, col, pts)


def fx_lines(fx):
    out = []
    for k, v in fx.items():
        if k not in FX_NAMES:
            continue
        n, m = FX_NAMES[k]
        if m == '+':
            out.append('%s %s%s' % (n, '+' if v > 0 else '', ('%g' % v)))
        elif m == '×':
            out.append('%s ×%g' % (n, v))
        elif m == '%':
            out.append('%s %d%%' % (n, round(v * 100)) if v < 1 else n)
        else:
            out.append(n if k != 'big_every' else 'Jeder %d. Schuss ist mächtig' % v)
    return out


class Game:
    def __init__(self, headless=False):
        pygame.init()
        self.headless = headless
        self.save = Save()
        st = self.save['settings']
        info = pygame.display.Info()
        sc = max(1, min((info.current_w - 80) // W, (info.current_h - 120) // H)) if info.current_w > 0 else 3
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
            ic.blit(pygame.transform.scale(gfx.sprite('hana'), (24, 28)), (4, 2))
            pygame.display.set_icon(ic)
        except Exception:
            pass

    def set_mode(self):
        if self.fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(self.win_size, pygame.RESIZABLE)

    def scan_pads(self):
        try:
            pygame.joystick.init()
            self.pads = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for p in self.pads:
                p.init()
        except Exception:
            self.pads = []

    def toast(self, title, sub='', col=(255, 220, 120)):
        self.toasts.append([title, sub, col, 3.5])
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
                elif e.button == 3: out.append('hard')
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
        while True:
            dt = min(1 / 30, self.clock.tick(FPS) / 1000)
            self.frame(dt, pygame.event.get())

    def frame(self, dt, events):
        self.t += dt
        for e in events:
            if e.type == pygame.QUIT:
                self.quit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_F11:
                self.toggle_fullscreen()
            elif e.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.win_size = (max(W, e.w), max(H, e.h))
                self.window = pygame.display.set_mode(self.win_size, pygame.RESIZABLE)
            elif e.type in (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
                self.scan_pads()
        nav = self.menu_keys(events)
        getattr(self, 'st_' + self.state)(dt, events, nav)
        for tt in self.toasts:
            tt[3] -= dt
        self.toasts = [tt for tt in self.toasts if tt[3] > 0]
        self.draw_toasts()
        self.present()

    def present(self):
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
        gfx.TEXT.flush(self.window, sc, ox + shake[0], oy + shake[1])
        pygame.display.flip()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.save['settings']['fullscreen'] = self.fullscreen
        self.set_mode()

    def quit(self):
        self.save.write()
        pygame.quit()
        sys.exit(0)

    def draw_toasts(self):
        y = 34
        for title, sub, col, t in self.toasts[:3]:
            a = int(255 * min(1, t * 2))
            w = max(gfx.text_w(title, 9), gfx.text_w(sub, 7)) + 20
            gfx.panel(self.screen, (W // 2 - w // 2, y, w, 28), int(a * 0.85), col)
            gfx.TEXT.add(title, W // 2, y + 3, 9, col, 'c', alpha=a)
            gfx.TEXT.add(sub, W // 2, y + 16, 7, (230, 225, 210), 'c', alpha=a)
            y += 32

    # ================================================================  Hintergrund (Titel)
    def draw_night(self, s):
        t = self.t
        for y in range(H):
            f = y / H
            c = (int(14 + 30 * f), int(10 + 14 * f), int(36 + 30 * f))
            pygame.draw.line(s, c, (0, y), (W, y))
        rng = random.Random(5)
        for i in range(90):
            x, y = rng.randrange(W), rng.randrange(150)
            if (t * 2 + i) % 7 > 0.4:
                s.set_at((x, y), (220, 220, 255))
        gfx.draw_glow(s, 418, 52, 60, (255, 230, 190), 70)
        pygame.draw.circle(s, (250, 240, 215), (418, 52), 20)
        pygame.draw.circle(s, (230, 220, 195), (411, 47), 4)
        pygame.draw.circle(s, (230, 220, 195), (425, 58), 3)
        # Berge
        pts = [(0, 210)]
        for x in range(0, W + 20, 20):
            pts.append((x, 190 - 40 * math.sin(x * 0.013) - 18 * math.sin(x * 0.041)))
        pts += [(W, H), (0, H)]
        pygame.draw.polygon(s, (26, 20, 44), pts)
        pygame.draw.rect(s, (18, 12, 26), (0, 232, W, H))
        # Torii
        tx = 90
        col = (170, 30, 36)
        pygame.draw.rect(s, col, (tx - 30, 150, 7, 85))
        pygame.draw.rect(s, col, (tx + 23, 150, 7, 85))
        pygame.draw.rect(s, (30, 16, 20), (tx - 42, 142, 84, 8))
        pygame.draw.rect(s, col, (tx - 38, 160, 76, 5))
        # Laternen
        for i, lx in enumerate((160, 240, 320, 420)):
            gfx.draw_glow(s, lx, 220, 18, (255, 170, 80), 80)
            pygame.draw.rect(s, (90, 90, 100), (lx - 2, 222, 4, 12))
            pygame.draw.rect(s, (120, 120, 130), (lx - 6, 212, 12, 10))
            pygame.draw.rect(s, (255, 200, 120), (lx - 4, 214, 8, 5))
        # Hyakki Yagyō – die Parade der hundert Dämonen
        names = ['hitodama', 'kasa_obake', 'chochin', 'kappa', 'bakeneko', 'nopperabo', 'oni', 'karasu_tengu',
                 'onibi', 'gaki', 'ittan_momen', 'kitsunebi_e', 'heikegani', 'yamabiko', 'shikome', 'bakezori']
        for i in range(16):
            x = (t * 18 + i * 34) % (W + 60) - 40
            nm = names[i % len(names)]
            spr = gfx.sprite(nm, False)
            bob = abs(math.sin(t * 6 + i)) * 3
            s.blit(spr, (int(x), int(250 - spr.get_height() - bob)))

    # ================================================================  Zustände
    MENU = ['Neuer Lauf', 'Tägliche Prüfung', 'Codex der Items', 'Erfolge', 'Statistik', 'Optionen', 'Beenden']

    def st_title(self, dt, events, nav):
        s = self.screen
        self.draw_night(s)
        T = gfx.TEXT
        T.add('Yōkai no Michi', W // 2, 30, 28, (255, 240, 220), 'c')
        T.add('– Hyakki Yagyō –', W // 2, 66, 11, (230, 140, 130), 'c')
        items = self.MENU
        for i, m in enumerate(items):
            y = 92 + i * 17
            sel = i == self.sel
            col = (255, 230, 150) if sel else (210, 200, 190)
            if sel:
                gfx.panel(s, (W // 2 - 70, y - 2, 140, 15), 170, (200, 120, 90))
            T.add(m, W // 2, y, 10, col, 'c')
        T.add('v' + VERSION + '   •   F11 Vollbild', W - 6, H - 12, 6, (140, 130, 150), 'r')
        for n in nav:
            if n == 'up':
                self.sel = (self.sel - 1) % len(items); audio.play('move')
            elif n == 'down':
                self.sel = (self.sel + 1) % len(items); audio.play('move')
            elif isinstance(n, tuple) and n[0] == 'click':
                mx, my = n[1]
                for i in range(len(items)):
                    if W // 2 - 70 < mx < W // 2 + 70 and 92 + i * 17 - 2 < my < 92 + i * 17 + 13:
                        self.sel = i
                        self.title_select(i)
            elif n == 'ok':
                self.title_select(self.sel)
            elif n == 'back':
                pass

    def title_select(self, i):
        audio.play('select')
        m = self.MENU[i]
        if m == 'Neuer Lauf':
            self.state = 'chars'
            self.char_sel = CHAR_ORDER.index(self.last_char) if self.last_char in CHAR_ORDER else 0
        elif m == 'Tägliche Prüfung':
            self.start_daily()
        elif m == 'Codex der Items':
            self.state = 'codex'
        elif m == 'Erfolge':
            self.state = 'achievements'; self.scroll = 0
        elif m == 'Statistik':
            self.state = 'stats'
        elif m == 'Optionen':
            self.state = 'options'; self.sel = 0
        elif m == 'Beenden':
            self.quit()

    def start_run(self, char, seed=None, daily=False):
        self.last_char = char
        self.run = Run(self, char, seed, self.hard and not daily and self.save['hard_unlocked'], daily,
                       getattr(self, 'endless', False) and not daily and self.save.data.get('endless_unlocked', False))
        self.state = 'play'
        self.show_tab = False

    def start_daily(self):
        today = datetime.date.today()
        seed = int(today.strftime('%Y%m%d'))
        chars = [c for c in CHAR_ORDER if c in self.save['chars']]
        ch = random.Random(seed).choice(chars)
        self.start_run(ch, seed, daily=today.isoformat())
        self.run.banner('Tägliche Prüfung', 'Alle spielen heute denselben Lauf: %s' % CHARS[ch]['name'], (255, 220, 150), True)

    # ---------------------------------------------------------------- Charakterwahl
    def st_chars(self, dt, events, nav):
        s = self.screen
        self.draw_night(s)
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
            spr = pygame.transform.scale(gfx.sprite(cid), (36, 42))
            if cid not in unlocked:
                spr = spr.copy()
                spr.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
            bob = int(abs(math.sin(self.t * 5)) * 2) if sel else 0
            s.blit(spr, (x - 18, y + 4 - bob))
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
        T.add('Enter – Start     Esc – Zurück', 32, 258, 7, (170, 160, 150))
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
            self.draw_itemlist(self.screen)
        if run.result:
            self.state = 'over'
            self.over_t = 0
            audio.get().music(('in', 196, 70, 'calm', 77) if run.result == 'dead' else ('yo', 262, 90, 'calm', 78))

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
            T.add('Synergien: ' + ', '.join(sy['name'] for sy in SYNERGIES if sy['id'] in p.synergies), 30, y, 7, (255, 220, 120))
            y += 11
        if p.transforms:
            T.add('Transformationen: ' + ', '.join(TRANSFORMS[t]['name'] for t in p.transforms), 30, y, 7, (180, 220, 255))

    def st_pause(self, dt, events, nav):
        run = self.run
        run.draw(self.screen, self.t)
        gfx.TEXT.clear()
        s = self.screen
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150))
        s.blit(ov, (0, 0))
        items = ['Weiter', 'Items & Werte', 'Optionen', 'Lauf aufgeben', 'Hauptmenü']
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
            self.draw_itemlist(s)
            if nav:
                self.pause_tab = False
            return
        gfx.TEXT.add('Pause', W // 2, 60, 18, (255, 240, 220), 'c')
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

    def st_over(self, dt, events, nav):
        run = self.run
        self.over_t += dt
        run.update_fx(dt)
        run.draw(self.screen, self.t)
        gfx.TEXT.clear()
        s = self.screen
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, min(190, int(self.over_t * 300))))
        s.blit(ov, (0, 0))
        T = gfx.TEXT
        win = run.result == 'win'
        if win:
            T.add('Sieg!' if run.depth < 6 else 'Wahrer Sieg!', W // 2, 30, 22, (255, 230, 150), 'c')
            T.add('Die Nacht der hundert Dämonen ist vorüber.' if run.depth < 6 else 'Der böse Stern ist gefallen. Der Himmel ist frei.',
                  W // 2, 60, 9, (240, 230, 210), 'c')
        else:
            T.add('Du bist gefallen…', W // 2, 30, 22, (230, 110, 110), 'c')
            T.add('Ebene %d – %s' % (run.depth, run.biome['name']), W // 2, 60, 9, (230, 210, 200), 'c')
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
        T.add('R – Nochmal mit %s      Enter – Hauptmenü' % CHARS[p.char]['name'], W // 2, 246, 8, (230, 220, 200), 'c')
        if self.over_t > 0.8:
            for n in nav:
                if n == 'retry':
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
    def st_codex(self, dt, events, nav):
        s = self.screen
        s.fill((18, 12, 24))
        T = gfx.TEXT
        seen = set(self.save['seen'])
        unlocked = set(self.save['items'])
        ids = ITEM_IDS
        cols = 16
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

    def st_achievements(self, dt, events, nav):
        s = self.screen
        s.fill((18, 12, 24))
        T = gfx.TEXT
        got = set(self.save['achievements'])
        T.add('Erfolge  (%d / %d)' % (len(got), len(ACHIEVEMENTS)), W // 2, 6, 11, (255, 230, 170), 'c')
        per = 11
        self.scroll = max(0, min(self.scroll, len(ACHIEVEMENTS) - per))
        for i, (aid, name, desc, reward) in enumerate(ACHIEVEMENTS[self.scroll:self.scroll + per]):
            y = 28 + i * 23
            ok = aid in got
            gfx.panel(s, (24, y, W - 48, 20), 180, (230, 190, 90) if ok else (80, 70, 80))
            if ok:
                star(s, 32, y + 10, (255, 220, 100))
            T.add(name, 40, y + 2, 8, (255, 230, 150) if ok else (170, 160, 170))
            T.add(desc, 40, y + 11, 6, (220, 215, 200) if ok else (140, 130, 140))
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
        s.fill((18, 12, 24))
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
                ('Tiefste Ebene', st.get('best_floor', 0)), ('Spielzeit', '%d:%02d h' % (pt // 3600, (pt % 3600) // 60))]
        for i, (k, v) in enumerate(rows):
            col = i // 8
            r = i % 8
            x = 40 + col * 210
            T.add(k, x, 34 + r * 16, 8, (210, 200, 180))
            T.add(str(v), x + 190, 34 + r * 16, 8, (255, 245, 230), 'r')
        y = 172
        T.add('Bosse:', 40, y, 8, (255, 220, 150))
        for i, (bid, b) in enumerate(BOSSES.items()):
            ok = bid in self.save['bosses']
            T.add(b['name'] if ok else '???', 40 + (i % 4) * 105, y + 14 + (i // 4) * 13, 7, (240, 230, 210) if ok else (120, 110, 120))
        dl = self.save['daily']
        if dl:
            best = sorted(dl.items())[-3:]
            T.add('Tägliche Prüfung: ' + '   '.join('%s: %d' % (k, v) for k, v in best), 40, 250, 7, (200, 220, 240))
        T.add('Esc – Zurück', W // 2, 285, 6, (150, 140, 140), 'c')
        for n in nav:
            if n in ('back', 'ok'): self.state = 'title'

    def st_options(self, dt, events, nav):
        s = self.screen
        if self.run and getattr(self, 'opt_return', None) == 'pause':
            self.run.draw(s, self.t)
            gfx.TEXT.clear()
            ov = pygame.Surface((W, H), pygame.SRCALPHA); ov.fill((0, 0, 0, 170)); s.blit(ov, (0, 0))
        else:
            s.fill((18, 12, 24))
        T = gfx.TEXT
        st = self.save['settings']
        opts = [('Musik', '%d%%' % round(st['music'] * 100)), ('Effekte', '%d%%' % round(st['sfx'] * 100)),
                ('Vollbild', 'An' if self.fullscreen else 'Aus'), ('Bildschirmwackeln', 'An' if st.get('shake', True) else 'Aus'),
                ('Schadenszahlen', 'An' if st.get('dmgnums', True) else 'Aus'), ('Spielstand löschen', ''), ('Zurück', '')]
        T.add('Optionen', W // 2, 30, 14, (255, 230, 170), 'c')
        for i, (k, v) in enumerate(opts):
            y = 70 + i * 20
            if i == self.sel:
                gfx.panel(s, (W // 2 - 120, y - 2, 240, 16), 180, (200, 120, 90))
            T.add(k, W // 2 - 110, y, 9, (255, 230, 150) if i == self.sel else (220, 210, 200))
            T.add(v, W // 2 + 110, y, 9, (255, 255, 255), 'r')
        T.add('Links/Rechts – ändern     Esc – Zurück', W // 2, 240, 7, (160, 150, 150), 'c')
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
