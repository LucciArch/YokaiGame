"""Ein Lauf (Run): Ebenen, Räume, Kampf, Belohnungen, HUD."""
import math
import random
import pygame
from collections import deque, defaultdict
from .settings import *
from . import gfx, props, weapons, audio
from .data import (TRINKETS, BIOMES, DEPTH_BIOMES, BOSS_POOL, ITEMS, ITEM_IDS, ACTIVES, ENEMIES, CHAMPIONS, BOSSES,
                   BOSS_REWARD, CHARS, ACHIEVEMENTS, TRANSFORMS, SYNERGIES, CHAR_ORDER)
from .rooms import generate_floor, build_room_tiles, Room
from .entities import (Player, Bullet, Enemy, Pickup, Pedestal, Obj, Hazard, Particle, burst, clamp, norm,
                       tile_at, free_tile_pos, ebullet)
from .bosses import make_boss, CX, CY
from .yomeiri import Procession

ACH = {a[0]: a for a in ACHIEVEMENTS}
TIPS = ['Esc → „Speichern & Hauptmenü“: Der Lauf geht später ab dieser Ebene weiter.',
        'Gesegnete Ebenen erkennst du am goldenen Banner – nutze den Segen, solange er gilt.',
        'Im Item-Tooltip steht, ob ein Fund eine Synergie vervollständigt.',
        'Jede Yōkai-Begegnung füllt das Lexikon im Hauptmenü.',
        'Tiefere Ebenen bergen wertvollere Items – und gefährlichere Champions.',
        'Reinigungssalz an rissigen Wänden öffnet Geheimräume.', 'Die Ausweichrolle macht dich kurz unverwundbar.',
        'Drei Items eines Themas lösen eine Transformation aus.', 'Ohne Treffer gegen den Boss erscheint öfter ein Schrein.',
        'Oni-Schreine kosten Herzen – Kami-Schreine sind kostenlos.', 'Ab Kapitel II brauchen Schatzräume einen Schlüssel.',
        'Im Codex siehst du, welche Synergien du schon kennst.', 'Rot aufleuchtende Yokai schießen gleich.',
        'Das Teehaus verbessert deine Werte dauerhaft.', 'Champions mit farbigem Punkt sind stärker – und lohnender.',
        'In der Tab-Ansicht siehst du alle Werte und Items.', 'Bosse rasen bei 25 % Leben vor Wut.',
        'Der Tanuki-Automat: 3 Mon für dein Glück.', 'Das tägliche Omikuji ist ein guter Ort für Mon.']
_GRADE = {'chikurin': (40, 90, 30), 'inari': (120, 50, 20), 'kawabe': (20, 70, 80), 'obakedera': (60, 40, 20),
          'hakaba': (40, 50, 80), 'yashiki': (60, 20, 50), 'kurama': (80, 50, 20), 'yukiyama': (60, 90, 130),
          'oeyama': (90, 30, 10), 'ryugu': (10, 70, 90), 'uminobe': (30, 40, 60), 'shinkai': (0, 20, 80),
          'yomi': (90, 0, 30), 'jigoku': (120, 30, 0), 'enma_cho': (110, 20, 10), 'takamagahara': (120, 100, 40), 'tsukiyomi': (60, 70, 140)}
Q_WEIGHT = {0: 1.0, 1: 1.0, 2: 0.8, 3: 0.42, 4: 0.18}
CHAPTER_NAMES = {1: '– Die Grenzlande der Nacht –', 2: '– Die Stätten der Toten –', 3: '– Die heiligen Berge –',
                 4: '– Das Meer der Ertrunkenen –', 5: '– Yomi, das Land der Toten –', 6: '– Die Himmelsgefilde –'}
CHAPTER_LORE = {1: 'In dieser Nacht ziehen die hundert Dämonen durch das Land. Folge ihrer Spur bis zum Anfang.',
                2: 'Wo die Toten keine Ruhe finden, hat sich der Zug versammelt. Laternen flüstern Namen.',
                3: 'In den Bergen herrschen die Tengu. Der Wind trägt Gelächter und Messerklingen.',
                4: 'Unter den Wellen liegt der Palast des Drachenkönigs. Die Ertrunkenen wachen über ihn.',
                5: 'Hinter dem Felsen von Yomotsu beginnt das Land der Toten. Wer hier isst, kehrt nie zurück.',
                6: 'Über den Wolken wartet der böse Stern. Hier endet die Nacht – so oder so.'}
BLESSINGS = {'vollmond': ('Segen des Vollmonds', 'Die ganze Ebene liegt im Mondlicht – die Karte ist aufgedeckt'),
             'fuchs': ('Segen der Füchse', 'Die Tanuki-Händler geben 30 % Rabatt'),
             'reichtum': ('Segen des Reichtums', 'Auf dieser Ebene fallen doppelt so viele Mon'),
             'kami': ('Segen der Kami', 'Ein Herz geheilt und ein Seelenherz geschenkt')}
CURSES = {'dunkel': 'Fluch der Dunkelheit', 'nebel': 'Fluch des Nebels', 'labyrinth': 'Fluch des Labyrinths',
          'verirrt': 'Fluch der Verirrten'}


_CROP = {}


def run_file():
    import os
    from .settings import save_dir
    return os.path.join(save_dir(), 'lauf.json')


def clear_run_file():
    import os
    try:
        os.remove(run_file())
    except OSError:
        pass


def load_run_file():
    import json
    try:
        with open(run_file(), encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


class _TileSpr:
    __slots__ = ('img', 'x', 'top', 'y')

    def __init__(self, img, x, top, kind):
        self.img, self.x, self.top = img, x, top
        self.y = top + TILE * 0.62

    def draw(self, s, t):
        gfx.hi_blit(self.img, self.x, self.top + TILE)


class Run:
    def __init__(self, game, char_id, seed=None, hard=False, daily=False, endless=False, challenge=None, restore=None):
        self.game = game
        self.save = game.save
        self.seed = seed if seed is not None else random.randrange(1, 10 ** 8)
        self.rng = random.Random(self.seed)
        random.seed(self.seed * 7 + 3)
        self.relaxed = bool(game.save['settings'].get('relaxed')) and not challenge and not daily
        self.hard = hard and not self.relaxed
        self.daily = daily
        self.endless = endless
        self.challenge = challenge
        self.loop = 0
        self.hold = None
        self.portrait = None
        self.depth = 1
        self.stage = 0          # 0/1: erster oder zweiter Abschnitt eines Kapitels
        self.floor_no = 0       # fortlaufende Ebenen-Nummer
        self._prev_biome = None
        self._prev_boss = None
        self.time = 0.0
        self.result = None
        self.char = char_id
        unlocked = set(self.save['items'])
        self.pool = [i for i in ITEM_IDS if (not ITEMS[i]['locked'] or i in unlocked)]
        self.active_pool = list(ACTIVES.keys())
        self.particles, self.ambient, self.floats = [], [], []
        self.slashes = []
        self.pbullets, self.ebullets, self.enemies = [], [], []
        self.pickups, self.pedestals, self.objs, self.hazards = [], [], [], []
        self.banners = deque()
        self.banner_t = 0.0
        self.cur_banner = None
        self.shake_amt = 0.0
        self.whiteout = 0.0
        self.hint_txt, self.hint_t = '', 0.0
        self.hurt_flash = 0.0
        self.flash_white = 0.0
        self.timestop = 0.0
        self.slow_player = 0.0
        self.wind = (0, 0, 0)
        self.player_fired = False
        self.boss = None
        self.boss_hit = False
        self.bullet_speed_mult = 1.12 if hard else 1.0
        self.loop_mult = 1.0
        self.kills = 0
        self.rooms_cleared = 0
        self.coins_got = 0
        self.title_t = 0.0
        self.boss_intro = 0.0
        self.flow = {}
        self.flow_t = 0.0
        self.flow_src = None
        self.bg = None
        self.bg_dirty = True
        self.fade = 1.0
        self.pending = None
        self.hitstop = 0.0
        self.slide = None
        self._last = None
        self.shrine_room = None
        self.boss_pos = None
        self.curse = None
        self.blessing = None
        self.last_boss = None
        self.stat_delta = None
        self.player = Player(self, char_id)
        self.stat_delta = {}
        if restore:
            self.restore_state(restore)
        else:
            self.save.stat('runs')
            self.apply_challenge()
            if self.relaxed:
                self.player.maxhp += 2
                self.player.hp += 2
            if not (self.challenge or self.daily):     # Prüfungen überschreiben keinen gespeicherten Lauf
                clear_run_file()
                self.save_run_file()
        self.new_floor()

    # ---------------------------------------------------------------- Lauf speichern / fortsetzen
    RUN_KEYS = ('relaxed', 'depth', 'stage', 'floor_no', 'loop', 'loop_mult', 'time', 'kills', 'rooms_cleared', 'coins_got',
                'pool', 'active_pool', '_prev_biome', '_prev_boss')
    PLAYER_SKIP = {'run', 'x', 'y', 'iframes', 'dash_t', 'dash_cd', 'dash_dir', 'dash_hit', 'dash_trail', 'shoot_cd',
                   'facing', 'flip', 'moving', 'anim', 'familiars', 'orb_angle', 'orb_hit_cd', 'aura_cd', 'knock',
                   'wind', 'vx', 'vy', 'hurt_buff', 'kagura', 'room_dmg_buff', 'recoil', 'temp', 'dead', 's', 'f'}

    def state_dict(self):
        import json
        p = self.player
        pl = {}
        for k, v in p.__dict__.items():
            if k in self.PLAYER_SKIP:
                continue
            try:
                json.dumps(v)
            except (TypeError, ValueError):
                continue
            pl[k] = v
        st = self.rng.getstate()
        d = {k: getattr(self, k) for k in self.RUN_KEYS}
        d.update(version=1, char=self.char, seed=self.seed, hard=self.hard, daily=self.daily, endless=self.endless,
                 challenge=self.challenge, rng=[st[0], list(st[1]), st[2]], player=pl)
        return d

    def restore_state(self, d):
        from collections import defaultdict as _dd
        for k in self.RUN_KEYS:
            if k in d:
                setattr(self, k, d[k])
        st = d['rng']
        self.rng.setstate((st[0], tuple(st[1]), st[2]))
        p = self.player
        for k, v in d['player'].items():
            cur = getattr(p, k, None)
            if isinstance(cur, _dd):
                nv = _dd(cur.default_factory)
                nv.update(v)
                v = nv
            setattr(p, k, v)
        p.recalc()

    def save_run_file(self):
        if self.challenge or self.daily:
            return
        import json, os
        from .settings import save_dir
        try:
            with open(os.path.join(save_dir(), 'lauf.json'), 'w', encoding='utf-8') as f:
                json.dump(self.state_dict(), f)
        except (OSError, TypeError, ValueError) as e:
            print('Lauf nicht gespeichert:', e)

    def apply_challenge(self):
        c = self.challenge
        p = self.player
        if not c:
            return
        if c == 'glaskanone':
            p.maxhp = p.hp = 2
            p.bonus['dmgm'] = 2.0
        elif c == 'fuchspfad':
            for i in ('kyubi_schweif', 'inari_maske'):
                p.gain_item(i, silent=True)
        elif c == 'kaufmann':
            p.coins = 99
        elif c == 'oni_pakt':
            for i in ('kanabo', 'oni_horn', 'hannya'):
                p.gain_item(i, silent=True)
            p.maxhp = 2
            p.hp = 2
        elif c == 'papiermeister':
            p.bonus['familiar'] = 3
            p.bonus['homing'] = 1
        p.recalc()

    # ======================================================================  Ebenen
    TWO_STAGE = (1, 2, 3, 4, 5)        # Kapitel mit zwei Ebenen

    @property
    def tier(self):
        """Schwierigkeitsstufe: Kapitel, zweite Ebene eines Kapitels zählt halb mehr."""
        return self.depth + 0.5 * self.stage

    @property
    def last_stage(self):
        return self.stage == 1 or self.depth not in self.TWO_STAGE or (bool(self.challenge) and self.challenge != 'langer_weg')

    def path_nodes(self):
        """Alle Ebenen des Laufs als (Kapitel, Abschnitt)."""
        out = []
        last = 6 if (self.save['heaven_unlocked'] or self.depth >= 6) and not (self.challenge and self.challenge != 'bossrush') else 5
        for d in range(1, last + 1):
            two = d in self.TWO_STAGE and (not self.challenge or self.challenge == 'langer_weg')
            out += [(d, 0), (d, 1)] if two else [(d, 0)]
        return out

    def draw_path(self, s, cx, y, a=255, dead=False):
        """Fortschrittspfad: ein Punkt je Ebene, Kapitel mit Lücke getrennt, Boss-Ebenen als Raute."""
        nodes = self.path_nodes()
        gaps = len(set(d for d, _ in nodes)) - 1
        wdt = (len(nodes) - 1) * 9 + gaps * 6
        x = cx - wdt / 2
        cur = (self.depth, self.stage)
        surf = pygame.Surface((wdt + 12, 12), pygame.SRCALPHA)
        ox = x - 6
        prev_d = None
        for i, (d, st) in enumerate(nodes):
            if prev_d is not None and d != prev_d:
                x += 6
            prev_d = d
            done = (d, st) < cur
            now = (d, st) == cur
            col = (255, 220, 130) if now else (190, 150, 90) if done else (90, 80, 100)
            px_ = int(x - ox)
            if i + 1 < len(nodes):
                nxt = 9 + (6 if nodes[i + 1][0] != d else 0)
                pygame.draw.line(surf, (70, 60, 80) if not done else (150, 120, 80), (px_ + 3, 6), (px_ + nxt - 3, 6), 1)
            if d == 6:
                pygame.draw.polygon(surf, col, [(px_, 1), (px_ + 4, 6), (px_, 11), (px_ - 4, 6)])
            else:
                pygame.draw.circle(surf, col, (px_, 6), 3 if now else 2)
            if now and dead:
                pygame.draw.line(surf, (230, 60, 60), (px_ - 3, 3), (px_ + 3, 9), 2)
                pygame.draw.line(surf, (230, 60, 60), (px_ + 3, 3), (px_ - 3, 9), 2)
            elif now:
                pygame.draw.circle(surf, (255, 250, 220), (px_, 6), 1)
            x += 9
        surf.set_alpha(a)
        s.blit(surf, (int(ox), y - 6))

    def floor_label(self):
        roman = ['', 'I', 'II', 'III', 'IV', 'V', 'VI']
        return 'Ebene %d  ·  Kapitel %s' % (self.floor_no, roman[min(6, self.depth)])

    @property
    def enemy_dmg(self):
        """Ab Kapitel IV kosten Treffer ein ganzes Herz."""
        return 2 if (self.depth >= 4 or self.loop) and not self.relaxed else 1

    def new_floor(self):
        rng = self.rng
        self.floor_no += 1
        self.bullet_speed_mult = ((1.12 if self.hard else 1.0) + 0.07 * self.loop + 0.045 * (self.tier - 1)) * (0.88 if self.relaxed else 1)
        opts = [b for b in DEPTH_BIOMES[self.depth] if not (self.stage == 1 and b == self._prev_biome)] or DEPTH_BIOMES[self.depth]
        self.biome_id = rng.choice(opts)
        self._prev_biome = self.biome_id
        self.biome = BIOMES[self.biome_id]
        bs = self.save.data.setdefault('biomes_seen', [])
        if self.biome_id not in bs:
            bs.append(self.biome_id)
        self.curse = None
        if self.depth >= 2 and rng.random() < (0.3 if not self.hard else 0.45) and not self.player.f['curse_immune']:
            self.curse = rng.choice(list(CURSES.keys()))
        if self.challenge == 'dunkle_nacht':
            self.curse = 'dunkel'
        self.blessing = None
        if not self.curse and self.floor_no > 1 and rng.random() < 0.18:
            self.blessing = rng.choice(list(BLESSINGS.keys()))
        self.rooms, start, self.boss_pos = generate_floor(rng, self.depth, self.curse == 'labyrinth', self.hard)
        for r in self.rooms.values():
            if self.challenge in ('fuchspfad', 'langer_weg') and r.kind == 'shop':
                r.kind = 'onsen'
            if self.challenge == 'kaufmann' and r.kind == 'treasure':
                r.kind = 'shop'
                r.locked = False
        bopts = [b for b in BOSS_POOL[self.depth] if not (self.stage == 1 and b == self._prev_boss)] or BOSS_POOL[self.depth]
        self.boss_id = rng.choice(bopts)
        self._prev_boss = self.boss_id
        self.rooms[self.boss_pos].boss_id = self.boss_id
        self.room = None
        self.shrine_room = None
        self.player.hit_this_floor = False
        if self.floor_no > 1:
            self.player.salts = min(9, self.player.salts + 1)
        if self.floor_no > self.save['stats'].get('best_floor', 0):
            self.save['stats']['best_floor'] = self.floor_no
        if self.depth >= 5:
            self.achieve('floor5')
        if self.floor_no >= 8:
            self.achieve('floor8')
        if self.floor_no >= 11:
            self.achieve('floor11')
        if self.challenge == 'bossrush':
            self.enter_room(start, None)
            self.enter_room(self.boss_pos, None)
            self.player.x, self.player.y = RX + RW / 2, RY + RH - 30
        else:
            self.enter_room(start, None)
        self.title_t = 3.0
        audio.get().music(self.biome['music'])
        audio.get().prepare(self.boss_music())
        if self.curse:
            self.banner(CURSES[self.curse], '', (190, 120, 255))
        if self.blessing:
            name, sub = BLESSINGS[self.blessing]
            self.banner(name, sub, (255, 225, 140))
            audio.play('unlock', 0.6)
            if self.blessing == 'kami':
                self.player.heal(2)
                self.player.spirit += 2

    def boss_music(self):
        b = self.biome['music']
        return ('iwato' if self.depth >= 4 else b[0], b[1], 132 + self.depth * 4, 'boss', b[4] + 100 + self.depth)

    def go_deeper(self, depth=None):
        if depth is None and self.stage == 0 and not self.last_stage:
            self.stage = 1
        else:
            self.depth = depth or self.depth + 1
            self.stage = 0
        self.descend = 1.3
        if self.depth > 6:
            self.depth = 1
            self.loop += 1
            self.loop_mult = 1 + 0.6 * self.loop
            self.bullet_speed_mult = (1.12 if self.hard else 1.0) + 0.07 * self.loop
            self.achieve('loop1')
            self.banner('Schleife %d' % (self.loop + 1), 'Die Nacht beginnt von vorn – stärker als zuvor', (200, 140, 255), big=True)
        audio.play('stairs')
        self.fade = 1.0
        self.save_run_file()
        self.new_floor()
        p = self.player
        p.x, p.y = RX + RW / 2, RY + RH / 2 + 20

    # ======================================================================  Räume
    def store_room(self):
        if self.room is not None:
            self.room.objects = [o for o in self.pickups + self.pedestals + self.objs]

    def enter_room(self, pos, came_dir, room_obj=None):
        self.store_room()
        prev = self.room
        room = room_obj if room_obj is not None else self.rooms[pos]
        self.room = room
        room.visited = True
        room.seen = True
        if room_obj is None:
            for d, n in room.doors.items():
                if self.rooms[n].revealed:
                    self.rooms[n].seen = True
        if room.tiles is None:
            build_room_tiles(room, random.Random(room.layout_seed))
        self.pickups = [o for o in room.objects if isinstance(o, Pickup)]
        self.pedestals = [o for o in room.objects if isinstance(o, Pedestal)]
        self.objs = [o for o in room.objects if isinstance(o, Obj)]
        self.enemies, self.pbullets, self.ebullets, self.hazards = [], [], [], []
        self.particles = []
        self.slashes = []
        self.bg_dirty = True
        p = self.player
        p.room_dmg_buff = 0
        p.knock = (0, 0)
        p.shield_ready = bool(p.f['shield'])
        if came_dir:
            ent = OPP[came_dir]
            dx, dy = DOOR_POS[ent]
            ox, oy = {'n': (0, 18), 's': (0, -18), 'w': (18, 0), 'e': (-18, 0)}[ent]
            p.x, p.y = dx + ox, dy + oy
            for fm in p.familiars:
                fm.x, fm.y = p.x, p.y
        if not room.populated:
            room.populated = True
            self.populate(room)
        elif not room.cleared:
            self.spawn_room_enemies(room)
        self.fade = 0.6
        self._quirk_t = 3.0
        self.foxfire = None
        self.yomeiri = None
        if room.kind == 'yomeiri' and not room.extra.get('yomeiri_done'):
            self.yomeiri = Procession(self, room)
        rh = {'shop': 'Laden: Mon gegen Items tauschen. Der Saisen-Kasten nimmt Spenden an – manchmal lohnt es sich.',
              'curse': 'Fluchraum: Betreten kostet Leben, dafür lockt ein dunkler Schatz.',
              'yomeiri': 'Fuchshochzeit: Schieß nicht auf den Zug – dann bekommst du ein Geschenk.',
              'challenge': 'Prüfungsraum: Mehrere Wellen überstehen, dann gibt es eine Belohnung.',
              'secret': 'Geheimraum! Rissige Wände lassen sich mit Salz aufsprengen.',
              'boss': 'Der Boss dieser Ebene. Bei 25 % Leben rasen Bosse vor Wut.'}.get(room.kind)
        if rh and room_obj is None:
            self.hint('room_' + room.kind, rh)
        self.boss_intro = 0
        if room.kind == 'boss' and not room.cleared:
            self.boss_intro = 2.2
            audio.play('boss')
            b = self.biome['music']
            audio.get().music(self.boss_music())
        elif prev is not None and prev.kind == 'boss' or (prev and prev.kind.startswith('shrine')):
            audio.get().music(self.biome['music'])
        self.flow_src = None

    def door_locked(self, d):
        n = self.room.doors.get(d)
        if not n or self.room.pos == ('shrine',):
            return False
        r = self.rooms[n]
        return bool(r.locked or not r.revealed or (self.room.kind == 'secret' and False))

    def hidden_doors(self):
        out = []
        if self.room.pos == ('shrine',):
            return out
        for d, n in self.room.doors.items():
            if not self.rooms[n].revealed:
                out.append((d, n))
        return out

    def reveal_near(self, x, y, rad):
        for d, n in self.hidden_doors():
            dx, dy = DOOR_POS[d]
            if math.hypot(dx - x, dy - y) < rad:
                r = self.rooms[n]
                r.revealed = True
                r.seen = True
                audio.play('unlock')
                self.shake(6)
                burst(self, dx, dy, (220, 200, 160), 30, 120, 0.8, 3)
                self.banner('Geheimraum entdeckt!', 'Ein verborgener Pfad öffnet sich', (230, 210, 150))
                self.save.stat('secrets')
                self.achieve('secret')
                if self.save['stats'].get('secrets', 0) >= 10:
                    self.achieve('secret10')

    def doors_open(self):
        return self.room.cleared

    def pick_item(self, pool_letter, active_chance=0.0):
        if active_chance and random.random() < active_chance:
            cands = [a for a in self.active_pool if a != self.player.active]
            if cands:
                a = random.choice(cands)
                self.active_pool.remove(a)
                return 'active:' + a
        luck = self.player.s['luck']
        cands = [i for i in self.pool if pool_letter in ITEMS[i]['pools']]
        if not cands:
            cands = [i for i in self.pool if 'T' in ITEMS[i]['pools']]
        if not cands:                                   # Pool leer (lange Endlos-Läufe): alles Nicht-Getragene kommt zurück
            unlocked = set(self.save['items'])
            have = set(self.player.items)
            self.pool = [i for i in ITEM_IDS if (not ITEMS[i]['locked'] or i in unlocked) and i not in have]
            cands = [i for i in self.pool if pool_letter in ITEMS[i]['pools']] or self.pool or ['onigiri']
        if self.tier >= 4:                              # tief unten kein Kleinkram mehr, solange es Besseres gibt
            good = [i for i in cands if ITEMS[i]['q'] >= 2]
            if good:
                cands = good
        deep = 1 + 0.15 * (self.tier - 1)            # tiefer = wertvollere Funde
        ws = [Q_WEIGHT[ITEMS[i]['q']] * (1 + 0.06 * luck * ITEMS[i]['q']) * deep ** (ITEMS[i]['q'] - 2) for i in cands]
        iid = random.choices(cands, ws)[0]
        if iid in self.pool:
            self.pool.remove(iid)
        return iid

    def champ_roll(self):
        ch = 0.03 + 0.02 * self.depth + 0.03 * self.stage + (0.08 if self.hard else 0) + (0.12 if self.depth == 6 else 0) + 0.1 * self.loop
        if random.random() < ch:
            return random.choice(list(CHAMPIONS.keys()))
        return None

    def spawn_enemy(self, eid, x, y, champ=None):
        e = Enemy(self, eid, x, y, champ)
        self.enemies.append(e)
        base = {'gaki_small': 'gaki', 'nuppeppo_klein': 'nuppeppo', 'kappa_small': 'kappa'}.get(eid, eid)
        if base not in self.save.data.setdefault('enemies_seen', []):
            self.save.data['enemies_seen'].append(base)
            from .bestiary import LORE, SKIP
            total = [k for k in ENEMIES if k in LORE and k not in SKIP]
            n = len([k for k in total if k in self.save.data['enemies_seen']])
            if n * 2 >= len(total):
                self.achieve('lexikon_half')
            if n >= len(total):
                self.achieve('lexikon_all')
        return e

    def spawn_room_enemies(self, room):
        pool = self.biome['enemies']
        fliers = [e for e in pool if ENEMIES[e].get('fly') or ENEMIES[e]['move'] in ('circle', 'bounce')]
        ground = [e for e in pool if e not in fliers]
        rng = random
        spawns = room.spawns or [(rng.randint(2, 10), rng.randint(1, 5), 'x') for _ in range(rng.randint(3, 5))]
        n_extra = (1 if (self.hard or self.depth >= 3) and rng.random() < 0.6 else 0) + (1 if self.depth >= 5 and rng.random() < 0.6 else 0)
        chosen = list(spawns)
        for _ in range(n_extra):
            chosen.append((rng.randint(2, 10), rng.randint(1, 5), 'x'))
        # pro Raum maximal zwei verschiedene Yokai-Arten für klare Muster
        kinds_g = rng.sample(ground, min(2, len(ground))) if ground else []
        kinds_f = rng.sample(fliers, min(1, len(fliers))) if fliers else kinds_g
        p = self.player
        for tx, ty, c in chosen:
            if room.tiles[ty][tx] in SOLID_TILES or room.tiles[ty][tx] == T_PIT:
                continue
            x, y = RX + tx * TILE + 16, RY + ty * TILE + 16
            if math.hypot(x - p.x, y - p.y) < 55:
                continue
            if c == 'f' and kinds_f:
                eid = rng.choice(kinds_f)
            elif c == 'e' and kinds_g:
                eid = rng.choice(kinds_g)
            else:
                eid = rng.choice(kinds_g + kinds_f)
            champ = self.champ_roll()
            for gi in range(ENEMIES[eid].get('group', 1)):
                gx = clamp(x + random.uniform(-14, 14) * (gi > 0), RX + 10, RX + RW - 10)
                gy = clamp(y + random.uniform(-14, 14) * (gi > 0), RY + 10, RY + RH - 10)
                self.spawn_enemy(eid, gx, gy, champ)
        if room.kind == 'normal' and self.depth >= 2 and random.random() < 0.08 + 0.02 * self.loop and self.enemies:
            base = random.choice([e for e in self.enemies])
            big = self.spawn_enemy(base.id, RX + RW / 2, RY + RH / 2 - 20, None)
            big.mini = True
            big.r = int(big.r * 1.5)
            big.hp = big.maxhp = big.maxhp * 6
            big.speed *= 0.8
            big.name = 'Ō-' + big.name
            room.extra['mini'] = True
            self.banner('Mini-Boss: ' + big.name, 'Ein besonders mächtiger Yokai!', (255, 110, 90))
        if not self.enemies:
            room.cleared = True

    def populate(self, room):
        k = room.kind
        cx, cy = RX + RW / 2, RY + RH / 2
        if k == 'normal':
            self.spawn_room_enemies(room)
        elif k == 'boss':
            self.boss = make_boss(self, room.boss_id)
            self.enemies.append(self.boss)
            self.boss_hit = False
        elif k == 'treasure':
            if random.random() < 0.22 + 0.02 * self.player.s['luck']:
                for i, dx in enumerate((-40, 40)):
                    self.pedestals.append(Pedestal(self.pick_item('T', 0.12), cx + dx, cy, group='wahl'))
                self.banner('Wähle weise', 'Nur eines der Items kann genommen werden', (230, 210, 170))
            else:
                self.pedestals.append(Pedestal(self.pick_item('T', 0.14), cx, cy))
        elif k == 'shop':
            disc = (0.66 if self.player.f['discount'] else 1.0) * (0.7 if self.blessing == 'fuchs' else 1.0)
            xs = [-120, -60, 0, 60, 120]
            for i, dx in enumerate(xs[:4] if random.random() < 0.6 else xs):
                if i < 3:
                    iid = self.pick_item('S', 0.1)
                    q = ITEMS[iid]['q'] if not iid.startswith('active:') else 2
                    price = int((10 + q * 4) * disc)
                    self.pedestals.append(Pedestal(iid, cx + dx, cy - 10, price=price))
                else:
                    kind, price = random.choice([('heart', 3), ('key', 5), ('salt', 4), ('spirit', 5), ('battery', 6), ('chest', 6), ('trinket', 8)])
                    if kind == 'trinket':
                        pk = self.spawn_trinket(cx + dx, cy - 6)
                        pk.vx = pk.vy = 0
                        pk.price = max(1, int(price * disc))
                        continue
                    self.pickups.append(Pickup(kind, cx + dx, cy - 6, price=max(1, int(price * disc)), pop=False))
            self.objs.append(Obj('saisen', cx, cy + 60))
            if True:
                tk = Obj('tanuki', cx, cy - 46, run=self)
                tk.r = -100
                self.objs.append(tk)
        elif k == 'curse':
            if random.random() < 0.5:
                self.pedestals.append(Pedestal(self.pick_item('O'), cx, cy))
            else:
                self.pickups.append(Pickup('chest', cx, cy, pop=False))
                self.pickups.append(Pickup('chest', cx + 30, cy, pop=False))
        elif k == 'challenge':
            room.extra['waves'] = 2 + (1 if self.depth >= 3 else 0)
            self.banner('Kampfraum!', 'Überstehe alle Wellen für eine Belohnung', (255, 120, 100))
            self.spawn_room_enemies(room)
            room.extra['waves'] -= 1
        elif k == 'library':
            for dx in (-70, 0, 70):
                self.pedestals.append(Pedestal(self.pick_item('T', 0.08), cx + dx, cy - 6, group='bib'))
            self.banner('Schriftrollenarchiv', 'Drei Schriftrollen – nur eine darfst du nehmen', (200, 180, 140))
            self.achieve('library')
        elif k == 'dojo':
            self.banner('Dōjō', 'Besiege die Champions!', (255, 150, 110))
            pool = self.biome['enemies']
            for i, dx in enumerate((-60, 60) if self.depth < 4 else (-80, 0, 80)):
                e = self.spawn_enemy(random.choice(pool), cx + dx, cy - 20, random.choice(list(CHAMPIONS.keys())))
                e.hp = e.maxhp = e.maxhp * 2
        elif k == 'teahouse':
            self.banner('Teehaus', 'Ein Schluck Stärke – für immer', (150, 200, 120))
            opts = [('Matcha', {'rate': 0.35}, (110, 180, 90)), ('Mochi', {'hp': 1}, (250, 245, 240)),
                    ('Sake', {'dmg': 0.6}, (230, 230, 210)), ('Gyokuro', {'spd': 10, 'shotspd': 25}, (90, 160, 80)),
                    ('Amazake', {'luck': 1, 'heal': 2}, (240, 220, 200)), ('Kombu-Tee', {'range': 40, 'size': 0.5}, (60, 100, 60))]
            random.shuffle(opts)
            for i, (nm, fx, col) in enumerate(opts[:3]):
                self.objs.append(Obj('tea', cx - 80 + i * 80, cy, name=nm, fx=fx, col=col, price=random.randint(6, 10)))
        elif k == 'slots':
            self.objs.append(Obj('slots', cx, cy))
            self.banner('Tanuki-Spielhalle', 'Wage dein Glück!', (230, 150, 90))
        elif k == 'secret':
            r = random.random()
            if r < 0.45:
                self.pedestals.append(Pedestal(self.pick_item('K' if random.random() < 0.3 else 'T', 0.1), cx, cy))
            elif r < 0.75:
                for i in range(random.randint(6, 11)):
                    self.pickups.append(Pickup('coin' if random.random() < 0.8 else 'coin5', cx + random.uniform(-40, 40), cy + random.uniform(-25, 25), pop=False))
                self.pickups.append(Pickup('key', cx, cy + 30, pop=False))
            else:
                self.pickups.append(Pickup('chest', cx - 30, cy, pop=False))
                self.pickups.append(Pickup('chest', cx + 30, cy, pop=False))
                self.pickups.append(Pickup('spirit', cx, cy + 30, pop=False))
        elif k == 'omikuji':
            self.objs.append(Obj('omikuji', cx - 40, cy))
            self.objs.append(Obj('saisen', cx + 40, cy + 6))
        elif k == 'onsen':
            self.objs.append(Obj('onsen', cx, cy))
            self.banner('Heiße Quelle', 'Ein Bad heilt Körper und Geist', (140, 210, 230))
        elif k == 'start' and self.depth == 1:
            room.extra['tutorial'] = True
        elif k.startswith('shrine'):
            oni = k == 'shrine_oni'
            for dx in (-45, 45):
                iid = self.pick_item('O' if oni else 'K')
                if oni:
                    q = ITEMS[iid]['q']
                    pd = Pedestal(iid, cx + dx, cy - 10, hearts=(1 if q < 4 else 2) * (2 if self.challenge == 'langer_weg' else 1))
                else:
                    pd = Pedestal(iid, cx + dx, cy - 10, group='kami')
                pd.shrine = 'oni' if oni else 'kami'
                self.pedestals.append(pd)
            self.objs.append(Obj('back', cx, RY + RH - 24))
        if k == 'curse' and not room.extra.get('hurt'):
            room.extra['hurt'] = True
            self.player.iframes = 0
            self.player.hurt(1, 'den Fluch')

    # ======================================================================  Hilfen
    HINTS_OFF = False

    QUIRK_TEXT = {
        'ice': 'Eisiger Boden: Auf dem Schneeberg rutschst du nach.',
        'gust': 'Tengu-Wind: Auf dem Kurama-Berg treiben Böen dich zur Seite.',
        'lava': 'Glühende Gruben speien im Kampf Funken – Abstand halten!',
        'souls': 'Auf dem Friedhof treiben Irrlichter. Berühre sie für ein Seelenherz.',
        'current': 'Meeresströmung: Unter Wasser treibt dich die Strömung langsam ab.',
        'polter': 'Poltergeist! Im Kampf fliegen dir Töpfe entgegen – zerschlag sie vorher.',
        'star': 'Im Himmel fallen nach dem Kampf manchmal Sternschnuppen voller Mon.',
        'bamboo': 'Bambus schießt aus dem Boden – achte auf die grünen Kreise unter dir!',
        'foxfire': 'Kitsunebi: Fange das Fuchsfeuer, um in diesem Raum stärker zuzuschlagen.',
        'hands': 'In Yomi greifen Hände aus dem Boden und bremsen dich.',
        'cucumber': 'Kappa-Dank: Am Flussufer bleibt nach dem Kampf manchmal ein halbes Herz liegen.',
        'drums': 'Oni-Kriegstrommeln! Bei jedem Schlag stürmen die Yokai auf dich zu.',
        'tide': 'Brandung: Wellen rollen über den Strand und schieben dich mit.',
    }
    QUIRK_SHORT = {'ice': 'Eisiger Boden', 'gust': 'Tengu-Windböen', 'lava': 'Speiende Lavagruben', 'souls': 'Irrlichter',
                   'current': 'Meeresströmung', 'polter': 'Poltergeist', 'star': 'Sternschnuppen', 'bamboo': 'Bambus-Fallen',
                   'foxfire': 'Fuchsfeuer', 'hands': 'Greifende Hände', 'cucumber': 'Kappa-Dank', 'drums': 'Oni-Trommeln',
                   'tide': 'Brandung'}
    QUIRKS = {'yukiyama': 'ice', 'kurama': 'gust', 'jigoku': 'lava', 'enma_cho': 'lava', 'hakaba': 'souls',
              'ryugu': 'current', 'shinkai': 'current', 'obakedera': 'polter', 'yashiki': 'polter',
              'takamagahara': 'star', 'tsukiyomi': 'star', 'chikurin': 'bamboo', 'inari': 'foxfire', 'yomi': 'hands',
              'kawabe': 'cucumber', 'oeyama': 'drums', 'uminobe': 'tide'}

    def biome_quirk(self, dt):
        """Kleine Eigenheit pro Biom (nur in normalen Räumen, nicht in Schreinen)."""
        q = self.QUIRKS.get(self.biome_id)
        p = self.player
        p.ice = q == 'ice'
        qs = getattr(self, 'quirk_snd', None)
        if qs:
            if qs[0] - dt <= 0:
                audio.play(qs[1], 0.7)
                self.quirk_snd = None
            else:
                self.quirk_snd = (qs[0] - dt, qs[1])
        if not q or self.room.kind.startswith('shrine') or self.room.kind == 'boss':
            return
        self.hint('biome_' + q, self.QUIRK_TEXT[q])
        if self.save.data.setdefault('quirks_seen', []) is not None and q not in self.save['quirks_seen']:
            self.save['quirks_seen'].append(q)
            if len(set(self.save['quirks_seen'])) >= len(set(self.QUIRKS.values())):
                self.achieve('quirks_all')
        fighting = any(e.active() for e in self.enemies)
        qt = getattr(self, '_quirk_t', 0.0) - dt
        if q == 'gust' and fighting:
            if qt <= 0:
                d = random.choice((-1, 1))
                self.wind = (d * 75, 0, 1.3)
                for i in range(14):
                    self.particles.append(Particle(RX + (0 if d > 0 else RW), RY + random.uniform(10, RH - 10), d * random.uniform(160, 260), random.uniform(-10, 10), 1.6, (190, 170, 110), 2, kind='petal'))
                audio.play('gust', 0.8)
                qt = random.uniform(6, 9)
        elif q == 'lava' and fighting:
            if qt <= 0:
                pits = [(tx, ty) for ty in range(ROWS) for tx in range(COLS) if self.room.tiles[ty][tx] == T_PIT]
                if pits:
                    tx, ty = random.choice(pits)
                    x, y = RX + tx * TILE + 16, RY + ty * TILE + 16
                    if math.hypot(x - p.x, y - p.y) > 50:
                        burst(self, x, y, (255, 150, 60), 10, 60, 0.5, 2)
                        for i in range(5):
                            ebullet(self, x, y, i / 5 * math.tau + random.random(), 55, (255, 120, 40), r=3)
                qt = random.uniform(2.2, 3.4)
        elif q == 'bamboo' and fighting:
            if qt <= 0:
                self.hazards.append(Hazard(p.x + p.vx * 0.3, p.y + p.vy * 0.3 + 4, 9, 0.9, 0.5, 1, 'e', 'bamboo'))
                self.quirk_snd = (0.9, 'bamboo')
                qt = random.uniform(3.5, 5.5)
        elif q == 'hands' and fighting:
            if qt <= 0:
                for i in range(2):
                    a = random.uniform(0, math.tau)
                    self.hazards.append(Hazard(p.x + math.cos(a) * 40, p.y + math.sin(a) * 30, 14, 0.6, 3.0, 0, 'e', 'hands'))
                self.quirk_snd = (0.6, 'grab')
                qt = random.uniform(4, 6)
        elif q == 'foxfire' and fighting:
            ff = getattr(self, 'foxfire', None)
            if ff is None and qt <= 0 and p.room_dmg_buff <= 0:
                self.foxfire = [RX + random.uniform(40, RW - 40), RY + random.uniform(30, RH - 30), 0.0]
                audio.play('wisp', 0.7)
                qt = 9999
            elif ff is not None:
                ff[2] += dt
                ff[0] += math.cos(ff[2] * 1.7) * 30 * dt
                ff[1] += math.sin(ff[2] * 2.3) * 22 * dt
                if math.hypot(ff[0] - p.x, ff[1] - p.y) < 12:
                    p.room_dmg_buff = 30.0
                    self.achieve('foxfire')
                    burst(self, ff[0], ff[1], (120, 200, 255), 16, 70)
                    audio.play('item', 0.5)
                    self.foxfire = None
                elif ff[2] > 10:
                    self.foxfire = None
        elif q == 'drums' and fighting:
            if qt <= 0:
                audio.play('drum', 0.8)
                self.shake(2)
                for e in self.enemies:
                    if e.active() and not e.is_boss:
                        d = norm(p.x - e.x, p.y - e.y)
                        e.kx += d[0] * 190
                        e.ky += d[1] * 190
                        burst(self, e.x, e.y + 4, (200, 80, 60), 4, 40, 0.3)
                qt = random.uniform(5, 7)
        elif q == 'tide' and fighting:
            if qt <= 0:
                d = random.choice((-1, 1))
                self.wind = (d * 60, 0, 1.0)
                audio.play('wave', 0.8)
                for i in range(22):
                    self.particles.append(Particle(RX + (0 if d > 0 else RW), RY + random.uniform(6, RH - 6), d * random.uniform(180, 260), random.uniform(-6, 6), 1.4, (170, 210, 230), 2))
                qt = random.uniform(6, 8)
        elif q == 'cucumber' and self.room.cleared and not self.room.extra.get('cuc_rolled'):
            self.room.extra['cuc_rolled'] = True
            if random.random() < 0.25:
                x, y = RX + random.uniform(50, RW - 50), RY + random.uniform(40, RH - 40)
                self.spawn_pickup('half', x, y)
        elif q == 'current' and fighting:
            cur = self.room.extra.setdefault('current', random.choice(((28, 0), (-28, 0), (0, 22), (0, -22))))
            if self.wind[2] <= 0:
                self.wind = (cur[0], cur[1], 0.05)
            if random.random() < dt * 6:
                self.particles.append(Particle(RX + random.uniform(0, RW), RY + random.uniform(0, RH), cur[0] * 3, cur[1] * 3, 1.0, (170, 220, 240), 1))
        elif q == 'polter' and fighting:
            if qt <= 0:
                pots = [(tx, ty) for ty in range(ROWS) for tx in range(COLS) if self.room.tiles[ty][tx] == T_POT]
                if pots:
                    tx, ty = random.choice(pots)
                    x, y = RX + tx * TILE + 16, RY + ty * TILE + 16
                    if math.hypot(x - p.x, y - p.y) > 45:
                        self.break_tile(tx, ty)
                        ang = math.atan2(p.y - y, p.x - x)
                        ebullet(self, x, y, ang, 120, (190, 130, 90), r=5)
                        audio.play('dash', 0.5)
                qt = random.uniform(4.5, 6.5)
        elif q == 'star' and self.room.cleared and not self.room.extra.get('star_rolled'):
            self.room.extra['star_rolled'] = True
            if random.random() < 0.3:
                x, y = RX + random.uniform(60, RW - 60), RY + random.uniform(40, RH - 40)
                for i in range(12):
                    self.particles.append(Particle(x - 60 + i * 5, y - 60 + i * 5, 90, 90, 0.6, (255, 240, 170), 2, kind='spark'))
                self.spawn_pickup('coin5', x, y)
                audio.play('coin', 0.6)
        elif q == 'souls' and self.room.cleared:
            lucky = False
            if qt <= 0 and not self.room.extra.get('wisp_rolled'):
                self.room.extra['wisp_rolled'] = True          # nur ein Versuch pro Raum
                lucky = random.random() < 0.35
            if lucky:
                x, y = RX + random.uniform(40, RW - 40), RY + random.uniform(30, RH - 30)
                pk = Pickup('spirit', x, y, pop=False)
                audio.play('wisp', 0.6)
                pk.wisp = True
                self.pickups.append(pk)
                burst(self, x, y, (140, 200, 255), 10, 40, 0.6, 2)
            if qt <= 0:
                qt = 9999                      # einmal pro Raum
        self._quirk_t = qt

    def hint(self, hid, text):
        """Einmaliger Kontext-Tipp (pro Spielstand), unten im Raum eingeblendet."""
        if self.HINTS_OFF or not self.save['settings'].get('hints', True):
            return
        seen = self.save.data.setdefault('hints', [])
        if hid in seen:
            return
        seen.append(hid)
        self.hint_txt, self.hint_t = text, 6.0

    def banner(self, title, sub='', col=(255, 240, 200), big=False, fx=''):
        self.banners.append((title, sub, col, big, fx))

    def shake(self, a):
        if self.save['settings'].get('shake', True):
            self.shake_amt = max(self.shake_amt, a)

    def nearest_enemy(self, x, y, maxd=9999):
        best, bd = None, maxd
        for e in self.enemies:
            if e.active():
                d = math.hypot(e.x - x, e.y - y)
                if d < bd:
                    best, bd = e, d
        return best

    def fire_player_bullet(self, x, y, ang, dmg, spd, size, life, fl, delay=0.0):
        col = (250, 246, 232)
        if fl.get('burn'):
            col = (255, 170, 80)
        elif fl.get('poison'):
            col = (150, 235, 110)
        elif fl.get('slow'):
            col = (170, 230, 255)
        elif fl.get('chain'):
            col = (255, 240, 120)
        elif fl.get('homing'):
            col = (220, 180, 255)
        elif fl.get('spectral'):
            col = (210, 230, 255)
        b = Bullet(x, y, math.cos(ang) * spd, math.sin(ang) * spd, dmg, size, life, 'p', col, fl, delay=delay)
        self.pbullets.append(b)
        return b

    def clear_ebullets(self):
        for b in self.ebullets:
            self.particles.append(Particle(b.x, b.y, 0, -10, 0.3, (220, 220, 255), 2))
        self.ebullets.clear()

    def compute_flow(self):
        p = self.player
        src = (int((p.x - RX) // TILE), int((p.y - RY) // TILE))
        if src == self.flow_src and self.flow_t > 0:
            return
        self.flow_src = src
        self.flow_t = 0.2
        room = self.room
        dist = {src: 0}
        q = deque([src])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in dist:
                    t = room.tiles[ny][nx]
                    if t in (T_FLOOR, T_SPIKE):
                        dist[(nx, ny)] = dist[(x, y)] + 1
                        q.append((nx, ny))
        self.flow = dist

    def flow_dir(self, x, y):
        p = self.player
        tx, ty = int((x - RX) // TILE), int((y - RY) // TILE)
        d0 = self.flow.get((tx, ty))
        if d0 is None or d0 <= 1:
            return norm(p.x - x, p.y - y)
        best, bd = None, d0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            d = self.flow.get((tx + dx, ty + dy))
            if d is not None and d < bd:
                best, bd = (tx + dx, ty + dy), d
        if best is None:
            return norm(p.x - x, p.y - y)
        return norm(RX + best[0] * TILE + 16 - x, RY + best[1] * TILE + 16 - y)

    def spawn_trinket(self, x, y, tid=None):
        pk = Pickup('trinket', x, y)
        pk.tid = tid or random.choice(list(TRINKETS.keys()))
        self.pickups.append(pk)
        return pk

    def spawn_pickup(self, kind, x, y, pop=True):
        if kind == 'trinket':
            return self.spawn_trinket(x, y)
        pk = Pickup(kind, x, y, pop=pop)
        self.pickups.append(pk)
        return pk

    def random_drop(self, x, y, luck_bonus=0.0):
        luck = self.player.s['luck'] + luck_bonus
        table = [('coin', 36 * (2 if self.blessing == 'reichtum' else 1)), ('half', 8), ('heart', 5), ('key', 10), ('salt', 6), ('chest', 5 + luck), ('trinket', 2.5),
                 ('spirit', 3.5 + luck * 0.5), ('battery', 3), ('coin5', 3 + luck)]
        if self.player.spirit_only:
            table = [(k, w * (0.2 if k in ('half', 'heart') else 1)) for k, w in table]
        kinds, ws = zip(*table)
        return self.spawn_pickup(random.choices(kinds, [max(0.5, w) for w in ws])[0], x, y)

    def break_tile(self, tx, ty, rocks=False):
        t = self.room.tiles[ty][tx]
        if t == T_POT or (rocks and t == T_ROCK):
            self.room.tiles[ty][tx] = T_FLOOR
            self.bg_dirty = True
            x, y = RX + tx * TILE + 16, RY + ty * TILE + 16
            burst(self, x, y, (150, 100, 70) if t == T_POT else self.biome['rock'], 12, 70, 0.5, 3)
            audio.play('hit', 0.7)
            if t == T_POT and random.random() < 0.18 + 0.02 * self.player.s['luck']:
                self.random_drop(x, y)
            self.flow_src = None

    def explode(self, x, y, r, dmg, owner='p'):
        audio.play('explode')
        self.shake(4)
        burst(self, x, y, (255, 180, 80), 22, 120, 0.5, 3)
        burst(self, x, y, (90, 80, 80), 12, 60, 0.8, 4)
        self.particles.append(Particle(x, y, 0, 0, 0.25, (255, 230, 160), r, kind='ring'))
        if owner == 'p':
            self.reveal_near(x, y, r + 40)
            for e in list(self.enemies):
                if e.active():
                    for hx, hy, hr in e.hitboxes():
                        if math.hypot(hx - x, hy - y) < r + hr:
                            self.damage_enemy(e, dmg, None)
                            break
            for ty in range(ROWS):
                for tx in range(COLS):
                    if math.hypot(RX + tx * TILE + 16 - x, RY + ty * TILE + 16 - y) < r + 10:
                        self.break_tile(tx, ty, rocks=True)
        elif dmg > 0:
            p = self.player
            if math.hypot(p.x - x, p.y - y) < r + p.hitr:
                p.hurt(1, getattr(self, 'cur_src', None) or 'eine Explosion')

    def lightning(self, x, y, dmg):
        self.hazards.append(Hazard(x, y, 14, 0.0, 0.14, dmg, 'p', 'strike'))
        self.flash_white = max(self.flash_white, 0.06)

    # ======================================================================  Schaden
    def damage_enemy(self, e, dmg, b, burn=False):
        if not e.active():
            return
        p = self.player
        if p.f['crit'] and random.random() < p.f['crit']:
            dmg *= 2
            self.floats.append([e.x, e.y - 14, 'Kritisch!', (255, 220, 90), 0.6])
        e.hp -= dmg
        e.flash = 0.07
        if b is not None:
            for _ in range(3):
                a = math.atan2(-b.vy, -b.vx) + random.uniform(-0.9, 0.9)
                v = random.uniform(60, 140)
                self.particles.append(Particle(b.x, b.y, math.cos(a) * v, math.sin(a) * v, 0.18, (255, 250, 220), 1, kind='spark'))
        if self.save['settings'].get('dmgnums', True) and dmg >= 0.5:
            self.floats.append([e.x + random.uniform(-4, 4), e.y - 10, '%d' % round(dmg) if dmg >= 1 else '%.1f' % dmg, (255, 255, 255), 0.45])
        if burn:
            e.burn = 3.0
            e.burn_dps = max(e.burn_dps, max(1.0, dmg * 0.4))
        if b is not None:
            fl = b.fl
            kb = (55 + 110 * fl.get('knock', 0)) * (0.15 if e.is_boss else 1)
            nx, ny = norm(b.vx, b.vy)
            e.kx += nx * kb
            e.ky += ny * kb
            if fl.get('burn'):
                e.burn = 3.0
                e.burn_dps = max(e.burn_dps, max(1.0, dmg * 0.35))
            if fl.get('poison'):
                e.poison = 4.0
                e.poison_dps = max(e.poison_dps, max(1.2, dmg * 0.4))
            if fl.get('slow'):
                e.slowed = 2.5
            if p.f['freeze'] and random.random() < p.f['freeze']:
                e.frozen = 1.5
            if fl.get('chain') and not fl.get('_chained'):
                done = {id(e)}
                src = e
                for _ in range(2 + int(fl['chain'])):
                    nxt = None
                    bd = 95
                    for o in self.enemies:
                        if o.active() and id(o) not in done:
                            d = math.hypot(o.x - src.x, o.y - src.y)
                            if d < bd:
                                nxt, bd = o, d
                    if not nxt:
                        break
                    done.add(id(nxt))
                    self.zap(src.x, src.y, nxt.x, nxt.y)
                    nxt.hp -= dmg * 0.5
                    nxt.flash = 0.07
                    if nxt.hp <= 0:
                        self.kill_enemy(nxt)
                    src = nxt
            if fl.get('split') and not fl.get('_split'):
                a = math.atan2(b.vy, b.vx)
                sp = math.hypot(b.vx, b.vy) * 0.8
                for da in (-0.7, 0.7):
                    nf = dict(fl); nf['_split'] = 1; nf['_chained'] = 1
                    nb = self.fire_player_bullet(b.x, b.y, a + da, dmg * 0.5, sp, max(1.5, b.r * 0.7), 0.5, nf)
                    nb.hit.add(id(e))
            if b.gold:
                e.gold_hit = True
        audio.play('hit', 0.35)
        if e.hp <= 0:
            self.kill_enemy(e)

    def zap(self, x1, y1, x2, y2):
        n = 6
        for i in range(n + 1):
            f = i / n
            self.particles.append(Particle(x1 + (x2 - x1) * f + random.uniform(-3, 3), y1 + (y2 - y1) * f + random.uniform(-3, 3),
                                           0, 0, 0.18, (255, 250, 160), 2))

    def kill_enemy(self, e):
        if e.dead:
            return
        e.dead = True
        p = self.player
        col = gfx.PAL['w'] if not e.champ else CHAMPIONS[e.champ]['col']
        burst(self, e.x, e.y, col, 14, 90, 0.5, 2)
        burst(self, e.x, e.y, (40, 30, 50), 8, 40, 0.7, 3)
        if not e.is_boss and (e.champ or e.maxhp >= 60):
            self.hitstop = max(self.hitstop, 0.05)     # schwere Gegner fallen mit Gewicht
            self.shake(2)
        self.particles.append(Particle(e.x, e.y - 4, random.uniform(-6, 6), -28, 1.1, (120, 200, 255), 2, kind='soul'))
        audio.play('kill', 0.6)
        self.kills += 1
        self.save.stat('kills')
        base = {'gaki_small': 'gaki', 'nuppeppo_klein': 'nuppeppo', 'kappa_small': 'kappa'}.get(e.id, e.id)
        kc = self.save.data.setdefault('kill_counts', {})
        kc[base] = kc.get(base, 0) + 1
        if self.save['stats']['kills'] >= 1:
            self.achieve('first_blood')
        if self.save['stats']['kills'] >= 500:
            self.achieve('benkei')
        d = e.d
        if not e.is_boss:
            death = d.get('death')
            if death and death[0] == 'split':
                for i in range(death[2]):
                    c = self.spawn_enemy(death[1], e.x + random.uniform(-6, 6), e.y + random.uniform(-6, 6))
                    c.spawn_t = 0.05
            elif death and death[0] == 'explode':
                for i in range(death[1]):
                    ebullet(self, e.x, e.y, i / death[1] * math.tau, 85, (200, 120, 255))
            if e.champ == 'lila':
                for i in range(8):
                    ebullet(self, e.x, e.y, i / 8 * math.tau, 90, (200, 120, 255))
            if e.champ == 'teiler' and e.maxhp > 3:
                for i in range(2):
                    c = self.spawn_enemy(e.id, e.x + random.uniform(-8, 8), e.y + random.uniform(-8, 8))
                    c.maxhp = c.hp = e.maxhp / 2.4 / CHAMPIONS['teiler']['hp']
                    c.spawn_t = 0.05
                    c.d = dict(c.d)
            if e.champ == 'gold':
                for i in range(3):
                    self.spawn_pickup('coin', e.x, e.y)
            elif e.champ and random.random() < 0.4:
                self.random_drop(e.x, e.y)
            if e.gold_hit and random.random() < 0.45:
                self.spawn_pickup('coin', e.x, e.y)
            elif random.random() < 0.025 + 0.004 * p.s['luck']:
                self.random_drop(e.x, e.y)
            if p.f['kill_heal'] and random.random() < p.f['kill_heal']:
                if p.heal(1):
                    audio.play('heal', 0.6)
            if p.f['kill_explode'] and random.random() < p.f['kill_explode']:
                self.explode(e.x, e.y, 30, p.damage() * 1.5, 'p')
        else:
            self.on_boss_killed(e)

    # ======================================================================  Boss besiegt
    def on_boss_killed(self, b):
        self.shake(12)
        audio.play('roar')
        self.whiteout = 0.45
        for k, (sz, lf, c) in enumerate(((150, 0.9, (255, 220, 150)), (100, 0.7, (255, 140, 90)), (210, 1.3, (220, 200, 255)))):
            self.particles.append(Particle(b.x, b.y, 0, 0, lf, c, sz, kind='wave'))
        for i in range(36):
            a = i / 36 * math.tau
            v = random.uniform(120, 260)
            self.particles.append(Particle(b.x, b.y, math.cos(a) * v, math.sin(a) * v, random.uniform(0.4, 0.9), (255, 230, 170), 2, kind='spark'))
        for i in range(5):
            burst(self, b.x + random.uniform(-15, 15), b.y + random.uniform(-15, 15), (255, 230, 160), 20, 140, 1.0, 3)
        for e in self.enemies:
            if e is not b and not e.dead:
                e.dead = True
                burst(self, e.x, e.y, (220, 220, 220), 8, 60)
        self.ebullets.clear()
        self.boss = None
        self.last_boss = b.id
        self.bosses_beaten = getattr(self, 'bosses_beaten', []) + [b.id]
        self.bullet_speed_mult = ((1.12 if self.hard else 1.0) + 0.07 * self.loop + 0.045 * (self.tier - 1)) * (0.88 if self.relaxed else 1)
        s = self.save
        first = s.add_to('bosses', b.id)
        self.achieve('first_boss')
        if self.depth >= 2:
            self.achieve('kenji')
        if b.id == 'sojobo':
            self.achieve('kotaro')
        if self.depth == 6:
            self.achieve('susanoo')
            self.achieve('endless')
        if len(s['bosses']) >= len(BOSSES):
            self.achieve('all_bosses')
        if not self.boss_hit:
            self.achieve('nohit')
            s.stat('nohit_bosses')
        rew = BOSS_REWARD.get(b.id)
        if rew and rew not in s['items']:
            s['items'].append(rew)
            if rew not in self.pool:
                self.pool.append(rew)
            self.game.toast('Neues Item freigeschaltet', ITEMS[rew]['name'], ITEMS[rew]['col'])
        s.write()

    def boss_room_rewards(self):
        cx, cy = RX + RW / 2, RY + RH / 2
        if self.stage == 1:
            self.achieve('chapter2')
        if len(self.player.items) >= 40:
            self.achieve('items40')
        self.pedestals.append(Pedestal(self.pick_item('B'), cx, cy - 30))
        self.spawn_pickup('heart', cx - 30, cy + 10)
        p = self.player
        if self.challenge == 'bossrush':
            self.pedestals.append(Pedestal(self.pick_item('T'), cx + 50, cy - 30))
        if self.challenge and self.depth >= 5 and self.last_stage:
            goal = 6 if self.challenge == 'bossrush' else 5
            if self.depth >= goal:
                self.objs.append(Obj('victory', cx, cy + 40))
            else:
                self.objs.append(Obj('heaven', cx, cy + 40))
        elif self.endless and self.depth in (5, 6) and self.last_stage:
            self.objs.append(Obj('heaven' if self.depth == 5 else 'torii', cx, cy + 40))
        elif self.depth == 5 and self.last_stage:
            self.objs.append(Obj('victory', cx - 70, cy + 40))
            if self.save['heaven_unlocked']:
                self.objs.append(Obj('heaven', cx + 70, cy + 40))
        elif self.depth == 6:
            self.objs.append(Obj('victory', cx, cy + 40))
        else:
            self.objs.append(Obj('torii', cx, cy + 40))
            ch = 1.0 if self.stage == 1 else 0.28 + (0.3 if not p.hit_this_floor else 0) + 0.03 * p.s['luck']   # Kapitelende: immer ein Schrein
            if random.random() < ch:
                oni = random.random() < (0.35 if not p.hit_this_floor else 0.6)
                self.objs.append(Obj('shrine', cx + 110, cy - 30, oni=oni))
                self.banner('Ein Schrein erscheint…', 'Oni-Schrein: Macht gegen Herzen' if oni else 'Kami-Schrein: ein göttliches Geschenk',
                            (255, 120, 120) if oni else (255, 230, 150))

    # ======================================================================  Aktive Items / Salz
    def use_active(self):
        p = self.player
        a = p.active
        if not a:
            return
        need = ACTIVES[a]['charge']
        if p.charge < need:
            audio.play('lock')
            return
        p.charge = 0
        audio.play('item', 0.6)
        dmg = p.damage()
        if a == 'ofuda_sturm':
            for w in range(3):
                for i in range(16):
                    self.fire_player_bullet(p.x, p.y, i / 16 * math.tau + w * 0.2, dmg * 1.2, 220, p.s['size'], 1.0,
                                            {'pierce': 1}, delay=w * 0.2)
        elif a == 'kagura_suzu':
            p.kagura = 4.0
            audio.play('bell')
        elif a == 'tanuki_blatt':
            for pd in self.pedestals:
                if not pd.taken:
                    pool = 'O' if getattr(pd, 'shrine', None) == 'oni' else 'K' if getattr(pd, 'shrine', None) == 'kami' else 'S' if pd.price else 'T'
                    pd.item = self.pick_item(pool, 0.1)
                    burst(self, pd.x, pd.y - 10, (120, 200, 90), 14, 60)
            audio.play('blank', 0.5)
        elif a == 'uchide_kozuchi':
            for i in range(random.randint(4, 7)):
                self.spawn_pickup('coin', p.x, p.y)
            if random.random() < 0.25:
                self.spawn_pickup('key', p.x, p.y)
        elif a == 'tamatebako':
            r = random.random()
            burst(self, p.x, p.y, (240, 240, 240), 30, 80, 1.0, 4)
            if r < 0.35:
                self.pedestals.append(Pedestal(self.pick_item('T'), p.x, p.y - 30))
                self.banner('Tamatebako', 'Ein Schatz!', (255, 220, 120))
            elif r < 0.75:
                for i in range(3):
                    self.random_drop(p.x, p.y, 2)
                self.banner('Tamatebako', 'Ein paar Geschenke', (255, 220, 120))
            else:
                p.bonus['spd'] -= 4
                p.bonus['luck'] += 1
                p.recalc()
                self.banner('Tamatebako', 'Rauch! Du fühlst dich älter… und weiser', (200, 200, 200))
        elif a == 'raijin_taiko':
            for e in list(self.enemies):
                if e.active():
                    self.lightning(e.x, e.y, 14 + dmg * 2)
            self.shake(5)
        elif a == 'tsukuyomi_spiegel':
            self.timestop = 4.0
            audio.play('bell')
        elif a == 'sake_kalebasse':
            p.heal(2)
            p.room_dmg_buff = 999
            audio.play('heal')
        elif a == 'shikigami_ruf':
            for i in range(6):
                self.fire_player_bullet(p.x, p.y, i / 6 * math.tau, dmg * 2.5, 150, 5, 2.5, {'homing': 1, 'pierce': 1})
        elif a == 'onryo_kerze':
            for e in self.enemies:
                if e.active():
                    e.poison = 6; e.poison_dps = max(e.poison_dps, dmg * 0.6); e.slowed = 4
                    self.damage_enemy(e, dmg * 2, None)
            self.flash_white = 0.15
        elif a == 'hyotan_sauger':
            for b in self.ebullets:
                tgt = self.nearest_enemy(b.x, b.y)
                ang = math.atan2(tgt.y - b.y, tgt.x - b.x) if tgt else random.uniform(0, math.tau)
                self.fire_player_bullet(b.x, b.y, ang, dmg, 220, 3, 1.5, {'homing': 1})
            self.ebullets.clear()
        elif a == 'oni_trommel':
            p.temp.append([{'dmgm': 1.8}, 6.0])
            p.recalc()
            self.shake(4)
            audio.play('roar', 0.6)
        elif a == 'kitsune_laterne':
            p.temp.append([{'orbital': 4, 'burn': 1}, 10.0])
            p.recalc()
        elif a == 'horagai':
            for e in self.enemies:
                if e.active():
                    e.frozen = 2.5 if not e.is_boss else 0.6
            audio.play('roar', 0.5)
            self.particles.append(Particle(p.x, p.y, 0, 0, 0.5, (240, 220, 200), 200, kind='ring'))
        elif a == 'tengu_uchiwa':
            for e in self.enemies:
                if e.active():
                    d = norm(e.x - p.x, e.y - p.y)
                    e.kx += d[0] * (500 if not e.is_boss else 60)
                    e.ky += d[1] * (500 if not e.is_boss else 60)
                    self.damage_enemy(e, 5, None)
            self.ebullets = [b for b in self.ebullets if math.hypot(b.x - p.x, b.y - p.y) > 140]
            for i in range(20):
                a2 = i / 20 * math.tau
                self.particles.append(Particle(p.x, p.y, math.cos(a2) * 200, math.sin(a2) * 200, 0.4, (200, 240, 200), 2))

    def use_salt(self):
        p = self.player
        if p.salts <= 0:
            audio.play('lock')
            return
        p.salts -= 1
        audio.play('blank')
        self.reveal_near(p.x, p.y, 75)
        self.clear_ebullets()
        self.flash_white = 0.25
        self.particles.append(Particle(p.x, p.y, 0, 0, 0.4, (255, 255, 255), 140, kind='ring'))
        for i in range(30):
            a = i / 30 * math.tau
            self.particles.append(Particle(p.x, p.y, math.cos(a) * 160, math.sin(a) * 160, 0.5, (250, 250, 255), 2))
        for e in self.enemies:
            if e.active():
                d = math.hypot(e.x - p.x, e.y - p.y)
                if d < 130:
                    n = norm(e.x - p.x, e.y - p.y)
                    k = 300 if not e.is_boss else 30
                    e.kx += n[0] * k; e.ky += n[1] * k
                    self.damage_enemy(e, 4, None)

    # ======================================================================  Update
    def update(self, dt, inp):
        weapons.update(self, dt)
        if getattr(self, 'descend', 0) > 0:
            self.descend -= dt
        if self.player.dead and self.result is None:
            if getattr(self, 'death_t', None) is None:
                self.death_t = 1.6
                self.shake(8)
                audio.play('roar', 0.7)
                audio.get().music(None)
                burst(self, self.player.x, self.player.y, (230, 50, 60), 30, 120, 0.8, 3)
                self.particles.append(Particle(self.player.x, self.player.y - 6, 0, -22, 1.6, (150, 210, 255), 3, kind='soul'))
            self.death_t -= dt
            self.update_fx(dt)
            if self.death_t <= 0:
                self.result = 'dead'
                self.end_run(False)
            return
        if self.slide:
            self.slide[2] += dt
            if self.slide[2] >= 0.24:
                self.slide = None
            return
        if self.hitstop > 0:
            self.hitstop -= dt
            return
        self.time += dt
        self.save['stats']['playtime'] = self.save['stats'].get('playtime', 0) + dt
        p = self.player
        self.player_fired = False
        self.title_t = max(0, self.title_t - dt)
        self.fade = max(0, self.fade - dt * 3)
        self.hurt_flash = max(0, self.hurt_flash - dt)
        self.flash_white = max(0, self.flash_white - dt)
        self.shake_amt = max(0, self.shake_amt - dt * 30)
        self.whiteout = max(0.0, self.whiteout - dt)
        self.hint_t = max(0.0, self.hint_t - dt)
        if self.player.hp <= 2 and not self.player.spirit_only:
            self.hint('lowhp', 'Wenig Leben: Leertaste = Ausweichrolle (kurz unverwundbar). Herzen gibt es im Laden.')
        self.timestop = max(0, self.timestop - dt)
        self.slow_player = max(0, self.slow_player - dt)
        self.flow_t -= dt
        if self.boss_intro > 0:
            self.boss_intro -= dt
            if self.boss_intro > 0.6:
                self.update_fx(dt)
                return
        self.biome_quirk(dt)
        wx, wy, wd = self.wind
        if wd > 0:
            p.wind = (wx, wy)
            self.wind = (wx, wy, wd - dt)
        else:
            p.wind = (0, 0)
        # Eingaben
        if inp['active']:
            self.use_active()
        if inp['salt']:
            self.use_salt()
        p.update(dt, inp)
        self.compute_flow()
        # Türen / Schlösser
        self.check_locks()
        # Raumwechsel
        d = None
        if p.y < RY - 3:
            d = 'n'
        elif p.y > RY + RH + 3:
            d = 's'
        elif p.x < RX - 3:
            d = 'w'
        elif p.x > RX + RW + 3:
            d = 'e'
        if d and d in self.room.doors:
            audio.play('door', 0.6)
            last = self._last
            self.enter_room(self.room.doors[d], d)
            if last is not None:
                self.slide = [last, d, 0.0, list(getattr(self, '_last_hi', []))]
                self.fade = 0
            return
        elif d:
            p.x = clamp(p.x, RX, RX + RW)
            p.y = clamp(p.y, RY, RY + RH)
        # Gegner
        for e in self.enemies:
            if not e.dead:
                self.cur_src = e.name
                nh = len(self.hazards)
                e.update(dt)
                for h in self.hazards[nh:]:
                    h.src = e.name
        self.cur_src = None
        self.enemies = [e for e in self.enemies if not e.dead]
        # Geschosse
        if getattr(self, 'yomeiri', None) is not None and not self.yomeiri.update(dt):
            self.yomeiri = None
        self.update_bullets(dt)
        # Gefahren
        self.hazards = [h for h in self.hazards if h.update(dt, self)]
        # Pickups & Objekte
        for pk in self.pickups:
            pk.update(dt, self)
        self.collect()
        # Raum geschafft?
        if not self.room.cleared and not self.enemies:
            self.on_room_clear()
        for k in list(self.stat_delta):
            self.stat_delta[k][1] -= dt
            if self.stat_delta[k][1] <= 0:
                del self.stat_delta[k]
        if self.hold:
            self.hold[2] -= dt
            if self.hold[2] <= 0:
                self.hold = None
        self.update_fx(dt)
        if self.challenge == 'zeitlauf' and self.time > 900 and not p.dead:
            p.dead = True
            p.last_src = 'die Morgensonne'
            self.banner('Die Sonne geht auf…', 'Zu spät!', (255, 200, 120), True)

    def update_bullets(self, dt):
        p = self.player
        nb = []
        for b in self.pbullets:
            if b.delay <= 0 and random.random() < 0.35 and len(self.particles) < 600:
                fl = b.fl
                if fl.get('burn'):
                    self.particles.append(Particle(b.x, b.y, random.uniform(-8, 8), -25, 0.3, (255, random.randint(120, 200), 40), 2))
                elif fl.get('poison'):
                    self.particles.append(Particle(b.x, b.y, 0, 18, 0.35, (120, 230, 90), 1))
                elif fl.get('chain'):
                    self.particles.append(Particle(b.x + random.uniform(-3, 3), b.y + random.uniform(-3, 3), 0, 0, 0.12, (255, 250, 170), 1))
                elif fl.get('homing') or fl.get('spectral'):
                    self.particles.append(Particle(b.x, b.y, 0, 0, 0.25, b.col, 1))
                elif b.big or b.gold:
                    self.particles.append(Particle(b.x, b.y, 0, 0, 0.3, b.col, 2))
            alive = b.update(dt, self)
            if alive and b.delay <= 0:
                for e in self.enemies:
                    if not e.active() or id(e) in b.hit:
                        continue
                    hit = False
                    for hx, hy, hr in e.hitboxes():
                        if (hx - b.x) ** 2 + (hy - b.y) ** 2 < (hr + b.r) ** 2:
                            hit = True
                            break
                    if hit:
                        b.hit.add(id(e))
                        self.damage_enemy(e, b.dmg, b)
                        if not b.fl.get('pierce'):
                            alive = False
                            break
            if alive:
                nb.append(b)
            else:
                if b.fl.get('explode') and not b.fl.get('_split'):
                    self.explode(b.x, b.y, 26, b.dmg * 1.3, 'p')
                else:
                    burst(self, b.x, b.y, b.col, 4, 40, 0.25, 2)
        self.pbullets = nb
        if self.timestop > 0:
            return
        eb = []
        orbs = p.orbitals()
        for b in self.ebullets:
            if b.fl.get('ehoming') and b.t < 3:
                ang = math.atan2(b.vy, b.vx)
                want = math.atan2(p.y - b.y, p.x - b.x)
                dd = (want - ang + math.pi) % math.tau - math.pi
                ang += clamp(dd, -1.6 * dt, 1.6 * dt)
                sp = math.hypot(b.vx, b.vy)
                b.vx, b.vy = math.cos(ang) * sp, math.sin(ang) * sp
            if not b.update(dt, self):
                continue
            if b.delay > 0:
                eb.append(b)
                continue
            dx, dy = b.x - p.x, b.y - (p.y - 3)
            if dx * dx + dy * dy < (b.r + p.hitr) ** 2:
                if p.dash_t > 0 and p.f['dash_reflect']:
                    burst(self, b.x, b.y, (220, 220, 255), 4, 40)
                    continue
                if p.hurt(self.enemy_dmg, b.src or 'ein Geschoss') and b.eff == 'slow':
                    self.slow_player = 2.0
                elif b.eff == 'slow' and p.iframes > 0:
                    pass
                if p.iframes > 0:
                    continue
                continue
            blocked = False
            for ox, oy in orbs:
                if (b.x - ox) ** 2 + (b.y - oy) ** 2 < (b.r + 5) ** 2:
                    blocked = True
                    burst(self, b.x, b.y, (220, 220, 255), 4, 40)
                    break
            if blocked:
                continue
            eb.append(b)
        self.ebullets = eb
        # Orbitale treffen Gegner
        for ox, oy in orbs:
            for e in self.enemies:
                if e.active():
                    for hx, hy, hr in e.hitboxes():
                        if (hx - ox) ** 2 + (hy - oy) ** 2 < (hr + 5) ** 2:
                            if p.orb_hit_cd[id(e)] <= 0:
                                p.orb_hit_cd[id(e)] = 0.25
                                self.damage_enemy(e, max(2.0, p.damage() * 0.6), None, burn=bool(p.f['burn']) and False)
                            break

    def check_locks(self):
        p = self.player
        if not self.room.cleared:
            return
        for d, n in self.room.doors.items():
            r = self.rooms[n]
            if r.locked:
                dx, dy = DOOR_POS[d]
                if math.hypot(p.x - dx, p.y - dy) < 20:
                    if p.keys > 0:
                        p.keys -= 1
                        r.locked = False
                        audio.play('key')
                        burst(self, dx, dy, (250, 210, 90), 12, 60)

    def on_room_clear(self):
        room = self.room
        if room.kind == 'challenge' and room.extra.get('waves', 0) > 0:
            room.extra['waves'] -= 1
            self.spawn_room_enemies(room)
            room.cleared = False
            if self.enemies:
                self.banner('Nächste Welle!', '', (255, 140, 120))
                return
        room.cleared = True
        self.rooms_cleared += 1
        self.save.stat('rooms')
        audio.play('door', 0.8)
        p = self.player
        if room.kind != 'boss' and room.kind != 'start':
            audio.play('bell', 0.25)                     # Raum gesäubert: kurzer Halt, Welle, Funken an den Türen
            self.hitstop = max(self.hitstop, 0.09)
            self.particles.append(Particle(p.x, p.y - 6, 0, 0, 0.6, (255, 230, 170), 90, kind='wave'))
            for d in room.doors:
                if self.rooms[room.doors[d]].revealed:
                    dx, dy = DOOR_POS[d]
                    burst(self, dx, dy, (255, 215, 140), 6, 45, 0.45, 2)
        if p.active:
            p.charge = min(ACTIVES[p.active]['charge'], p.charge + 1)
        if p.f['clear_heal'] and random.random() < p.f['clear_heal']:
            if p.heal(1):
                audio.play('heal', 0.6)
                self.floats.append([p.x, p.y - 16, '+1/2 Herz', (255, 120, 140), 0.8])
        if p.f['salts_regen'] and random.random() < p.f['salts_regen']:
            p.salts = min(9, p.salts + 1)
        cx, cy = RX + RW / 2, RY + RH / 2
        if room.kind == 'boss':
            self.boss_room_rewards()
            audio.get().music(self.biome['music'])
        elif room.kind == 'dojo':
            self.spawn_pickup('chest', cx, cy)
            if random.random() < 0.35:
                self.pedestals.append(Pedestal(self.pick_item('T', 0.1), cx, cy - 30))
            self.achieve('dojo')
        elif room.kind == 'challenge':
            self.pedestals.append(Pedestal(self.pick_item('T', 0.1), cx, cy))
            self.achieve('challenge')
            self.save.stat('challenges')
        elif room.extra.get('mini'):
            self.spawn_pickup('chest', cx, cy)
            if random.random() < 0.3:
                self.pedestals.append(Pedestal(self.pick_item('T', 0.1), cx, cy - 30))
        elif random.random() < 0.27 + 0.03 * p.s['luck']:
            self.random_drop(cx, cy)

    def collect(self):
        p = self.player
        for pk in list(self.pickups):
            if pk.age < 0.25:
                continue
            if getattr(pk, 'need_leave', False) and math.hypot(pk.x - p.x, pk.y - (p.y - 3)) > 28:
                pk.need_leave = False
            if math.hypot(pk.x - p.x, pk.y - (p.y - 3)) > 10:
                continue
            if pk.price:
                if p.coins < pk.price:
                    continue
            ok = True
            k = pk.kind
            if k in ('heart', 'half'):
                ok = p.heal(2 if k == 'heart' else 1)
                if ok:
                    audio.play('heal', 0.7)
            elif k == 'spirit':
                ok = p.add_spirit(2)
                if ok:
                    audio.play('heal', 0.7)
            elif k in ('coin', 'coin5'):
                if p.coins >= 99:
                    ok = False
                else:
                    v = 1 if k == 'coin' else 5
                    p.coins = min(99, p.coins + v)
                    self.coins_got += v
                    self.save.stat('coins', v)
                    audio.play('coin', 0.6)
                    if self.save['stats']['coins'] >= 300:
                        self.achieve('ponpoko')
                    if p.coins >= 99:
                        self.achieve('rich')
            elif k == 'key':
                p.keys = min(99, p.keys + 1)
                audio.play('key', 0.7)
                self.hint('key', 'Schlüssel öffnen Türen mit Schloss und goldene Truhen.')
            elif k == 'salt':
                if p.salts >= 9:
                    ok = False
                else:
                    p.salts += 1
                    audio.play('pickup', 0.7)
                    self.hint('salt', 'Reinigungssalz (Q): bannt Geschosse und sprengt rissige Wände auf.')
            elif k == 'trinket':
                if pk.age < 0.8 or getattr(pk, 'swapcool', 0) > 0 or getattr(pk, 'need_leave', False):
                    continue
                old = p.trinket
                if pk.price:
                    p.coins -= pk.price
                    pk.price = 0
                    audio.play('buy')
                p.trinket = pk.tid
                p.recalc()
                tr = TRINKETS[pk.tid]
                self.banner(tr['name'], tr['desc'] + '  (Anhänger)', tr['col'])
                self.hint('trinket', 'Anhänger wirken dauerhaft. Ein neuer ersetzt den alten – der bleibt liegen.')
                audio.play('pickup')
                if old:
                    pk.tid = old
                    pk.age = 0
                    pk.x += 18
                    pk.need_leave = True          # erst wieder aufhebbar, wenn man weggegangen ist
                    ok = False
            elif k == 'battery':
                if p.active and p.charge < ACTIVES[p.active]['charge']:
                    p.charge = ACTIVES[p.active]['charge']
                    audio.play('pickup')
                else:
                    ok = False
            elif k == 'chest':
                audio.play('pickup')
                burst(self, pk.x, pk.y, (240, 200, 90), 16, 70)
                if random.random() < 0.1 + 0.015 * p.s['luck']:
                    self.pedestals.append(Pedestal(self.pick_item('T'), pk.x, pk.y))
                else:
                    for i in range(random.randint(2, 4)):
                        self.random_drop(pk.x, pk.y)
            if ok:
                if pk.price:
                    p.coins -= pk.price
                    audio.play('buy')
                self.pickups.remove(pk)
        for pd in self.pedestals:
            pd.t += 1 / 60
            pd.cool = max(0, pd.cool - 1 / 60)
            if pd.taken or pd.cool > 0:
                continue
            if math.hypot(pd.x - p.x, (pd.y - 6) - p.y) > 12:
                continue
            if pd.price:
                if p.coins < pd.price:
                    continue
                p.coins -= pd.price
                audio.play('buy')
                pd.price = 0
            if pd.hearts:
                if p.maxhp >= pd.hearts * 2 and (p.maxhp - pd.hearts * 2 + p.spirit) > 0:
                    p.maxhp -= pd.hearts * 2
                    p.hp = min(p.hp, p.maxhp)
                elif p.spirit >= 6 and (p.maxhp == 0 or p.spirit_only):
                    p.spirit -= 6
                else:
                    continue
                pd.hearts = 0
                self.save.stat('oni_deals')
                if self.save['stats']['oni_deals'] >= 3:
                    self.achieve('akago')
                for o in self.pedestals:
                    if getattr(o, 'shrine', None) == 'oni' and o is not pd:
                        o.hearts = max(o.hearts, 1)
            if getattr(pd, 'shrine', None) == 'kami':
                self.save.stat('kami_deals')
                self.achieve('kami')
            if pd.item.startswith('active:'):
                new = pd.item[7:]
                old = p.active
                old_charge = p.charge
                p.active = new
                self.hint('active', 'Aktives Item: mit E einsetzen. Es lädt sich mit jedem geräumten Raum auf.')
                # abgelegte Items behalten ihre Ladung – sonst ließe sich durch Hin- und Hertauschen endlos aufladen
                stored = getattr(pd, 'stored_charge', None)
                p.charge = ACTIVES[new]['charge'] if stored is None else min(stored, ACTIVES[new]['charge'])
                self.banner(ACTIVES[new]['name'], ACTIVES[new]['desc'] + '  [E]', ACTIVES[new]['col'])
                audio.play('item')
                if old:
                    pd.item = 'active:' + old
                    pd.stored_charge = old_charge
                    pd.cool = 1.0
                else:
                    pd.taken = True
            else:
                pd.taken = True
                p.gain_item(pd.item)
            if pd.group:
                for o in self.pedestals:
                    if o is not pd and o.group == pd.group:
                        o.taken = True
                        burst(self, o.x, o.y - 10, (200, 200, 200), 10, 50)
        self.pedestals = [pd for pd in self.pedestals if not (pd.taken and pd.group)]
        for o in self.objs:
            o.t += 1 / 60
            o.cool = max(0, o.cool - 1 / 60)
            if o.cool > 0 or math.hypot(o.x - p.x, o.y - p.y) > o.r + 6:
                continue
            self.interact(o)

    def interact(self, o):
        p = self.player
        k = o.kind
        o.cool = 0.5
        if k == 'saisen':
            if p.coins <= 0:
                return
            p.coins -= 1
            self.save.stat('donations')
            audio.play('coin', 0.5)
            if self.save['stats']['donations'] >= 30:
                self.achieve('donor')
            r = random.random()
            if r < 0.07:
                p.bonus['luck'] += 1
                p.recalc()
                self.banner('Die Götter lächeln', 'Glück +1', (255, 230, 150))
            elif r < 0.11:
                p.add_spirit(2)
                self.banner('Ein Geist dankt dir', 'Geisterherz', (130, 170, 255))
            elif r < 0.13:
                self.pedestals.append(Pedestal(self.pick_item('K'), o.x, o.y - 30))
                self.banner('Ein Kami erhört dich!', '', (255, 230, 150))
        elif k == 'omikuji':
            if p.coins < 5:
                return
            p.coins -= 5
            o.cool = 1.0
            r = random.random() - 0.02 * p.s['luck']
            if r < 0.10:
                self.banner('Daikichi – Großes Glück!', 'Ein göttliches Geschenk', (255, 220, 120), big=True)
                self.pedestals.append(Pedestal(self.pick_item('K'), o.x + 40, o.y - 30))
                self.achieve('daikichi')
                self.save.stat('daikichi')
                audio.play('unlock')
            elif r < 0.45:
                self.banner('Kichi – Glück', 'Kleine Geschenke', (240, 220, 160))
                for i in range(3):
                    self.random_drop(o.x, o.y + 10)
                audio.play('pickup')
            elif r < 0.7:
                p.bonus['dmg'] += 0.3
                p.recalc()
                self.banner('Chūkichi – Mittleres Glück', 'Schaden +0.3', (240, 220, 160))
                audio.play('pickup')
            elif r < 0.9:
                self.banner('Shōkichi – Kleines Glück', 'Ein paar Münzen', (220, 210, 170))
                for i in range(3):
                    self.spawn_pickup('coin', o.x, o.y + 10)
            else:
                self.banner('Kyō – Pech!', 'Binde den Zettel an den Baum…', (200, 120, 255))
                p.iframes = 0
                p.hurt(1, 'ein Unglückslos')
        elif k == 'tea':
            if o.used or p.coins < o.data['price']:
                return
            p.coins -= o.data['price']
            o.used = True
            self.achieve('teahouse')
            fx = dict(o.data['fx'])
            if 'hp' in fx or 'heal' in fx:
                p.apply_once({kk: vv for kk, vv in fx.items() if kk in ('hp', 'heal')})
            for kk, vv in fx.items():
                if kk not in ('hp', 'heal'):
                    p.bonus[kk] += vv
            p.recalc()
            audio.play('heal')
            self.banner(o.data['name'], ', '.join('%s +%g' % (kk, vv) for kk, vv in fx.items()).replace('rate', 'Feuerrate').replace('hp', 'Herz').replace('dmg', 'Schaden').replace('spd', 'Tempo').replace('shotspd', 'Schussgeschw.').replace('luck', 'Glück').replace('heal', 'Heilung').replace('range', 'Reichweite').replace('size', 'Größe'), o.data['col'])
        elif k == 'slots':
            self.achieve('slots')
            if p.coins < 3:
                return
            p.coins -= 3
            o.cool = 1.0
            o.data['spin'] = 1
            o.data['res'] = random.randint(0, 4)
            audio.play('coin')
            r = random.random() - 0.015 * p.s['luck']
            if r < 0.03:
                self.pedestals.append(Pedestal(self.pick_item('T'), o.x + 50, o.y))
                self.banner('Jackpot!', 'Der Tanuki verneigt sich', (255, 220, 120), True)
                audio.play('unlock')
            elif r < 0.2:
                for i in range(5):
                    self.spawn_pickup('coin', o.x, o.y + 14)
            elif r < 0.35:
                self.random_drop(o.x, o.y + 14)
            elif r < 0.42:
                self.banner('Tanuki-Streich!', 'Blätter verwandeln sich in Yokai', (200, 150, 90))
                pool = self.biome['enemies']
                for i in range(2):
                    self.spawn_enemy(random.choice(pool), o.x + random.choice([-60, 60]), o.y + 30)
                self.room.cleared = False
            else:
                self.floats.append([o.x, o.y - 30, 'Niete…', (200, 190, 180), 0.8])
        elif k == 'onsen':
            if o.used:
                return
            o.used = True
            if p.spirit_only:
                p.add_spirit(6)
            else:
                p.hp = p.maxhp
                p.add_spirit(2)
            audio.play('heal')
            self.achieve('onsen')
            self.save.stat('onsen')
            self.banner('Ahh… herrlich', 'Volle Gesundheit', (140, 210, 230))
        elif k == 'torii':
            self.go_deeper()
        elif k == 'heaven':
            self.go_deeper(6)
            self.banner('Takamagahara', 'Die Himmelsgefilde – hier wartet der böse Stern', (255, 230, 150), big=True)
        elif k == 'victory':
            if self.result is None:
                self.result = 'win'
                self.end_run(True)
        elif k == 'shrine':
            oni = o.data.get('oni')
            if self.shrine_room is None:
                self.shrine_room = Room(('shrine',), 'shrine_oni' if oni else 'shrine_kami')
                self.shrine_room.cleared = True
            self.shrine_from = self.room.pos
            audio.play('bell')
            self.enter_room(None, None, self.shrine_room)
            self.player.x, self.player.y = RX + RW / 2, RY + RH - 50
        elif k == 'back':
            self.enter_room(self.shrine_from, None)
            self.player.x, self.player.y = RX + RW / 2 + 110, RY + RH / 2
            o.cool = 1.0

    def update_fx(self, dt):
        self.particles = [pt for pt in self.particles if pt.update(dt)]
        if len(self.particles) > 700:
            self.particles = self.particles[-700:]
        for f in self.floats:
            f[1] -= 18 * dt
            f[4] -= dt
        self.floats = [f for f in self.floats if f[4] > 0]
        # Banner
        if self.cur_banner is None and self.banners:
            self.cur_banner = self.banners.popleft()
            self.banner_t = 3.4 if (self.cur_banner[3] or self.cur_banner[4]) else 2.2
        if self.cur_banner:
            self.banner_t -= dt
            if self.banner_t <= 0:
                self.cur_banner = None
        # Atmosphäre
        amb = self.biome['ambient']
        if random.random() < dt * 9:
            x = random.uniform(RX, RX + RW)
            if amb in ('leaves', 'petals', 'snow'):
                col = {'leaves': (110, 170, 80), 'petals': (250, 180, 210), 'snow': (250, 250, 255)}[amb]
                self.ambient.append(Particle(x, RY - 4, random.uniform(-10, 20), random.uniform(15, 30), 9, col, 2,
                                             kind='petal' if amb != 'snow' else 'dot'))
            elif amb in ('bubbles', 'embers'):
                col = (180, 220, 255) if amb == 'bubbles' else (255, 140, 60)
                self.ambient.append(Particle(x, RY + RH, random.uniform(-5, 5), -random.uniform(15, 35), 7, col, 2,
                                             kind='ring' if amb == 'bubbles' else 'dot'))
            elif amb in ('fireflies', 'sparkle'):
                col = (230, 255, 140) if amb == 'fireflies' else (255, 240, 180)
                self.ambient.append(Particle(x, random.uniform(RY, RY + RH), random.uniform(-6, 6), random.uniform(-6, 6),
                                             3, col, 1))
        w = self.biome.get('weather')
        if w and not self.room.kind.startswith('shrine'):
            rate = {'rain': 60, 'rain_dark': 30, 'blizzard': 70, 'ash': 18}[w]
            for _ in range(int(rate * dt) + (1 if random.random() < (rate * dt) % 1 else 0)):
                x = random.uniform(RX, RX + RW)
                if w.startswith('rain'):
                    self.ambient.append(Particle(x, RY - 2, 60, 340, 0.8, (150, 170, 210), 1, kind='rain'))
                elif w == 'blizzard':
                    self.ambient.append(Particle(RX - 2, random.uniform(RY, RY + RH), random.uniform(140, 220), random.uniform(10, 40), 2.5, (240, 245, 255), 2))
                else:
                    self.ambient.append(Particle(x, RY - 2, random.uniform(-10, 10), random.uniform(15, 30), 8, (120, 110, 110), 1))
        self.ambient = [pt for pt in self.ambient if pt.update(dt) and RY - 10 < pt.y < RY + RH + 10 and pt.x < RX + RW + 10][-260:]

    # ======================================================================  Erfolge & Ende
    def achieve(self, aid):
        s = self.save
        if aid in s['achievements'] or aid not in ACH:
            return
        s['achievements'].append(aid)
        _, name, desc, reward = ACH[aid]
        sub = desc
        if reward:
            kind, val = reward
            if kind == 'char':
                s.add_to('chars', val)
                sub = 'Neuer Charakter: %s – %s' % (CHARS[val]['name'], CHARS[val]['title'])
            elif kind == 'item':
                s.add_to('items', val)
                if val not in self.pool:
                    self.pool.append(val)
                sub = 'Neues Item: ' + ITEMS[val]['name']
            elif kind == 'mode':
                if val == 'hard':
                    s.data['hard_unlocked'] = True
                    sub = 'Oni-Modus freigeschaltet'
                elif val == 'endless':
                    s.data['endless_unlocked'] = True
                    sub = 'Endlose Nacht freigeschaltet (Taste N bei der Charakterwahl)'
                else:
                    s.data['heaven_unlocked'] = True
                    sub = 'Takamagahara ist nun erreichbar'
        self.game.toast('Erfolg: ' + name, sub, (255, 220, 120))
        if len(s['chars']) >= len(CHAR_ORDER):
            if 'all_chars' not in s['achievements']:
                self.achieve('all_chars')
        s.write()

    def on_item(self, iid):
        self.save.add_to('seen', iid)
        self.save.stat('items')
        if len(self.player.items) >= 10:
            self.achieve('items10')

    def on_synergy(self, sid):
        self.save.stat('synergies')
        self.save.add_to('synergies_seen', sid)
        self.achieve('synergy1')
        if len(self.save['synergies_seen']) >= 10:
            self.achieve('synergy10')
        if len(self.save['synergies_seen']) >= 25:
            self.achieve('synergy25')

    def on_transform(self, t):
        # deutlich sichtbarer Verwandlungsmoment: Lichtsäule, Druckwelle, Funken in der Farbe der Gestalt
        p = self.player
        col = TRANSFORMS[t]['col']
        self.whiteout = 0.3
        self.shake(5)
        for sz, lf in ((70, 0.7), (110, 1.0)):
            self.particles.append(Particle(p.x, p.y, 0, 0, lf, col, sz, kind='wave'))
        for i in range(40):
            a = i / 40 * math.tau
            v = random.uniform(60, 160)
            self.particles.append(Particle(p.x, p.y - 8, math.cos(a) * v, math.sin(a) * v - 40, random.uniform(0.5, 1.0), col, 2, kind='spark'))
        for i in range(18):
            self.particles.append(Particle(p.x + random.uniform(-6, 6), p.y, 0, -random.uniform(80, 200), 0.9, (255, 250, 230), 2, kind='spark'))
        p.transform_glow = 2.0
        self.save.stat('transforms')
        self.save.add_to('transforms_seen', t)
        self.achieve('transform')
        if t == 'kitsune':
            self.achieve('kuzunoha')

    def end_run(self, win):
        import datetime as _dt
        hist = self.save.data.setdefault('history', [])
        hist.append({'date': _dt.date.today().strftime('%d.%m.'), 'char': self.char, 'floor': self.floor_no, 'win': bool(win),
                     'where': self.biome['name'] if self.biome else '', 'time': int(self.time), 'relaxed': self.relaxed,
                     'items': len(self.player.items), 'by': '' if win else (getattr(self.player, 'last_src', '') or '')})
        del hist[:-20]
        if not (self.challenge or self.daily):
            clear_run_file()
        s = self.save
        if win and self.challenge:
            self.achieve('ch_' + self.challenge)
            s.add_to('challenges_done', self.challenge)
        if win:
            s.stat('wins')
            s['char_wins'][self.char] = s['char_wins'].get(self.char, 0) + 1
            if self.depth == 6:
                s.stat('true_wins')
            self.achieve('seimei')
            self.achieve('hard')
            self.achieve('heaven')
            if self.hard:
                s.stat('wins_hard')
                self.achieve('win_hard')
        else:
            s.stat('deaths')
            if s['stats']['deaths'] >= 10:
                self.achieve('okiku')
        if self.daily:
            key = self.daily
            prev = s['daily'].get(key)
            score = self.score()
            if prev is None or score > prev:
                s['daily'][key] = score
        s.write()

    def score(self):
        return int((self.floor_no + self.loop * 11) * 1000 + self.kills * 10 + len(self.player.items) * 50 + (5000 if self.result == 'win' else 0)
                   - self.time * 0.5)

    # ======================================================================  Zeichnen
    def standing_tiles(self):
        """Felsen, Urnen und Laternen als Hi-Res-Requisiten, nach Tiefe sortierbar."""
        out = []
        tiles = self.room.tiles
        for ty in range(ROWS):
            row = tiles[ty]
            for tx in range(COLS):
                t = row[tx]
                if t:
                    x, y = RX + tx * TILE, RY + ty * TILE
                    img = gfx.hi_tile(t, x, y, self.biome)
                    if img is not None:
                        out.append(_TileSpr(img, x + TILE / 2, y, 0 if t != T_LANTERN else 1))
        return out

    def pit_edges(self, bg, room):
        """Gruben bekommen eine Abbruchkante: Felswand oben, Lichtkante am Rand, Schatten links/rechts."""
        kind = self.biome.get('pit', 'void')
        fl = self.biome['floor'] if not room.kind.startswith('shrine') else (90, 80, 70)
        face, face2 = gfx._c(fl, 0.42), gfx._c(fl, 0.3)
        lip = gfx._c(fl, 1.35)
        tiles = room.tiles
        D = pygame.draw

        def pit(x, y):
            return 0 <= x < COLS and 0 <= y < ROWS and tiles[y][x] == T_PIT

        for ty in range(ROWS):
            for tx in range(COLS):
                if tiles[ty][tx] != T_PIT:
                    continue
                x, y = RX + tx * TILE, RY + ty * TILE
                if not pit(tx, ty - 1):
                    depth = 7 if kind in ('void', 'cloud') else 4
                    bg.fill(face, (x, y, TILE, depth))
                    bg.fill(face2, (x, y + depth - 2, TILE, 2))
                    for k in range(3):                       # Gesteinsfugen in der Kante
                        fx = x + 5 + k * 10 + (tx * 3) % 4
                        bg.fill(face2, (fx, y + 1, 1, depth - 3))
                    bg.fill(lip, (x, y, TILE, 1))
                if not pit(tx - 1, ty):
                    bg.fill(face2, (x, y, 2, TILE))
                    bg.fill(lip, (x, y, 1, TILE))
                if not pit(tx + 1, ty):
                    bg.fill(face2, (x + TILE - 2, y, 2, TILE))
                if not pit(tx, ty + 1):
                    bg.fill(gfx._c(lip, 0.8), (x, y + TILE - 1, TILE, 1))

    def render_bg(self):
        room = self.room
        if getattr(room, '_bgcache', None) is None or room._bgcache[0] != self.biome_id:
            rng = random.Random(room.layout_seed if room.pos != ('shrine',) else 7)
            floor = gfx.make_floor(self.biome if not room.kind.startswith('shrine') else
                                   dict(self.biome, floor=(60, 20, 30) if room.kind == 'shrine_oni' else (200, 190, 150),
                                        floor_pat='stone'), rng)
            walls = gfx.make_walls(self.biome, rng)
            room._bgcache = (self.biome_id, floor, walls, gfx.scale2x(walls))
        _, floor, walls, self.walls_hi = room._bgcache
        bg = pygame.Surface((W, H))
        bg.fill((12, 8, 16))
        bg.blit(floor, (RX, RY))
        tl = pygame.Surface((W, H), pygame.SRCALPHA)
        for ty in range(ROWS):
            for tx in range(COLS):
                t = room.tiles[ty][tx]
                if t:
                    gfx.draw_tile(tl, t, RX + tx * TILE, RY + ty * TILE, self.biome)
        bg.blit(tl, (0, 0))
        self.pit_edges(bg, room)
        bg.blit(walls, (0, 0))
        self.bg = bg
        self.bg_dirty = False

    def pedestal_extra(self, iid):
        """Hinweis im Tooltip: vervollständigt dieses Item eine Synergie oder Transformation?"""
        if iid.startswith('active:') or iid not in ITEMS:
            return ''
        have = set(self.player.items)
        for sy in SYNERGIES:
            if iid in sy['items'] and iid not in have and all(i in have for i in sy['items'] if i != iid):
                known = sy['id'] in self.save['synergies_seen']
                return 'Vervollständigt Synergie: ' + (sy['name'] if known else '???')
        p = self.player
        for tg in ITEMS[iid]['tags']:
            if tg in p.transforms or tg not in TRANSFORMS:
                continue
            n = sum(1 for i in p.items if tg in ITEMS[i]['tags'])
            if n == 2:
                return 'Löst Transformation aus: ' + TRANSFORMS[tg]['name']
            if n == 1:
                return '2 / 3 für ' + TRANSFORMS[tg]['name']
        return ''

    def draw_lantern_light(self, s, t):
        """Warmer, leicht flackernder Lichtkreis der Steinlaternen auf dem Boden."""
        tiles = self.room.tiles
        for ty in range(ROWS):
            row = tiles[ty]
            for tx in range(COLS):
                if row[tx] == T_LANTERN:
                    x, y = RX + tx * TILE + 16, RY + ty * TILE + 20
                    fl = 0.85 + 0.15 * math.sin(t * 7.3 + tx * 1.7) * math.sin(t * 3.1 + ty)
                    gfx.draw_glow(s, x, y, 30, (255, 170, 80), int(46 * fl) // 2 * 2)

    def draw_pits(self, s, t):
        kind = self.biome.get('pit', 'void')
        if kind not in ('water', 'lava'):
            return
        tiles = self.room.tiles
        for ty in range(ROWS):
            for tx in range(COLS):
                if tiles[ty][tx] != T_PIT:
                    continue
                x, y = RX + tx * TILE, RY + ty * TILE
                if kind == 'water':
                    for i in range(2):
                        ox = int((t * 14 + i * 13 + tx * 7) % 24)
                        yy = y + 10 + i * 10 + int(math.sin(t * 2 + tx + i) * 1.5)
                        pygame.draw.line(s, (150, 210, 250), (x + 3 + ox // 2, yy), (x + 9 + ox // 2, yy), 1)
                else:
                    ph = (t * 0.8 + tx * 0.37 + ty * 0.61) % 1
                    bx, by = x + 8 + int((tx * 13 + ty * 7) % 16), y + 10 + int((tx * 5 + ty * 11) % 14)
                    r = int(1 + ph * 3)
                    pygame.draw.circle(s, (255, 220, 120), (bx, by), r, 1)
                    gfx.draw_glow(s, x + 16, y + 16, 18, (255, 110, 30), int(40 + 25 * math.sin(t * 3 + tx)))

    def draw_doors(self, s, t):
        room = self.room
        open_ = self.doors_open()
        for d, n in room.doors.items():
            if room.pos == ('shrine',):
                break
            other = self.rooms[n]
            x, y = DOOR_POS[d]
            horiz = d in 'ns'
            if not other.revealed:                       # Risse in der Wand (Hi-Res, liegen über den Wänden)
                key = ('crack', n)
                cr = _CROP.get(key)
                if cr is None:
                    cr = pygame.Surface((40, 28), pygame.SRCALPHA)
                    rr = random.Random(n[0] * 7 + n[1])
                    for i in range(5):
                        a = rr.uniform(0, math.tau)
                        pts = [(20, 14)]
                        for k in range(3):
                            a += rr.uniform(-0.6, 0.6)
                            px_, py_ = pts[-1]
                            pts.append((px_ + math.cos(a) * rr.uniform(4, 7), py_ + math.sin(a) * rr.uniform(3, 5)))
                        pygame.draw.lines(cr, (24, 16, 20), False, pts, 2)
                        pygame.draw.lines(cr, (120, 100, 96), False, [(q[0] + 1, q[1] + 1) for q in pts], 1)
                    _CROP[key] = cr
                gfx.hi_blit(cr, x, y + 7)
                continue
            w, h = (34, 18) if horiz else (18, 34)
            rect = pygame.Rect(0, 0, w, h)
            rect.center = (x, y + (-6 if d == 'n' else 6 if d == 's' else 0)) if horiz else (x + (-6 if d == 'w' else 6), y)
            frame = {'boss': (150, 30, 40), 'treasure': (230, 190, 70), 'shop': (90, 160, 90), 'curse': (110, 40, 120),
                     'challenge': (200, 90, 50), 'omikuji': (210, 60, 50), 'onsen': (120, 190, 220), 'yomeiri': (240, 150, 80),
                     'library': (150, 120, 200), 'dojo': (230, 140, 60), 'secret': (160, 140, 110),
                     'teahouse': (110, 170, 90), 'slots': (230, 120, 70)}.get(other.kind, (110, 70, 45))
            if self.curse == 'verirrt' and not other.visited:
                frame = (110, 70, 45)
            state = 'open' if (open_ and not other.locked) else ('locked' if other.locked else 'closed')
            img = props.door_hi(frame, state, d, other.kind == 'boss')
            off = {'n': (0, 0), 's': (0, 2), 'w': (-2, 0), 'e': (2, 0)}[d]
            if other.kind == 'boss':
                gfx.draw_glow(s, x, y, 18, (255, 50, 50), 50 + int(20 * math.sin(t * 3)))
            cxd, cyd = rect.centerx + off[0], rect.centery + off[1]
            if d == 's':                                # nicht über die Werteleiste ragen
                top = cyd - img.get_height() / 4
                keep = int((RY + RH + 16 - top) * 2)
                if 0 < keep < img.get_height():
                    ck = ('crop', id(img), keep)
                    c = _CROP.get(ck)
                    if c is None:
                        c = _CROP[ck] = img.subsurface((0, 0, img.get_width(), keep)).copy()
                    img = c
                gfx.hi_blit(img, cxd, top + img.get_height() / 2)
            else:
                gfx.hi_blit(img, cxd, cyd + img.get_height() / 4)

    def hi_light(self, x, y):
        """Helligkeit für Hi-Res-Sprites (gleiche Logik wie draw_dark: Lichtkreis um den Spieler)."""
        dark = self.biome['dark'] + (150 if self.curse == 'dunkel' else 0)
        if y < RY or dark <= 0 or self.room.kind.startswith('shrine'):
            return 1.0
        a = min(215, dark) / 255
        d = math.hypot(x - self.player.x, y - 8 - self.player.y)
        rr = min(1.0, d / 90)
        return 1 - a * rr ** 1.5

    def draw(self, s, t):
        gfx.HI.clear(); gfx.NOCACHE.clear()
        gfx.HI_MODE = True
        if self.bg_dirty or self.bg is None:
            self.render_bg()
        s.blit(self.bg, (0, 0))
        self.draw_pits(s, t)
        self.draw_lantern_light(s, t)
        wh = getattr(self, 'walls_hi', None)
        if wh is not None and self.slide is None:
            gfx.HI.append((wh, W / 2, H, 255, 1.0, True))     # Wände in Hi-Res, ohne Lichtabfall
        self.draw_doors(s, t)
        p = self.player
        # Tutorial-Hinweise
        if self.room.extra.get('tutorial') and (self.cur_banner or self.banners or self.title_t > 0):
            self._tut_a = 0.0
        elif self.room.extra.get('tutorial'):
            self._tut_a = min(1.0, getattr(self, '_tut_a', 0.0) + 1 / 40)
            cx = RX + RW / 2
            lines = ['WASD – Bewegen', 'Pfeiltasten / Maus – Ofuda werfen', 'Leertaste – Ausweichrolle',
                     'E – Aktives Item     Q – Reinigungssalz', 'Tab – Items & Werte    Esc – Pause',
                     'Tipp: Salz an rissigen Wänden deckt Geheimräume auf']
            for i, l in enumerate(lines):
                gfx.TEXT.add(l, cx, RY + 22 + i * 13, 8, (230, 220, 190), 'c', alpha=int(170 * self._tut_a))
        for h in self.hazards:
            h.draw(s, t)
        for o in self.objs:
            o.draw(s, t)
        for pk in self.pickups:
            pk.draw(s, t)
        ents = [e for e in self.enemies] + [p] + self.standing_tiles() + list(self.pedestals)
        if getattr(self, 'yomeiri', None) is not None:
            ents += self.yomeiri.foxes
        ents.sort(key=lambda e: e.y)
        for e in ents:
            e.draw(s, t)
        near, nd = None, 42
        for pd in self.pedestals:
            dd = math.hypot(pd.x - p.x, pd.y - p.y)
            if not pd.taken and dd < nd:
                near, nd = pd, dd
        if near and not self.hold:
            name, desc, icon, col = near.info()
            fxs = near.fxinfo()
            extra = self.pedestal_extra(near.item)
            w = max(gfx.text_w(name, 8), gfx.text_w(desc, 6), gfx.text_w(fxs, 6), gfx.text_w(extra, 6) if extra else 0) + 12
            bx = clamp(near.x, RX + w / 2 + 2, RX + RW - w / 2 - 2)
            hh = 31 + (9 if extra else 0)
            by = near.y - 52 - (9 if extra else 0)
            gfx.panel(s, (int(bx - w / 2), int(by), int(w), hh), 215, col)
            gfx.TEXT.add(name, bx, by + 2, 8, col, 'c')
            if not near.item.startswith('active:') and near.item not in self.save['seen']:
                gfx.TEXT.add('Neu!', bx + w / 2 - 4, by + 2, 6, (255, 230, 120), 'r')
            gfx.TEXT.add(desc, bx, by + 12, 6, (230, 225, 210), 'c')
            gfx.TEXT.add(fxs, bx, by + 21, 6, (170, 220, 255), 'c')
            if extra:
                gfx.TEXT.add(extra, bx, by + 30, 6, (255, 215, 110), 'c')
        ff = getattr(self, 'foxfire', None)
        if ff:
            fx_, fy_ = int(ff[0]), int(ff[1] + math.sin(t * 5) * 2)
            gfx.draw_glow(s, fx_, fy_, 14, (90, 170, 255), 140)
            pygame.draw.circle(s, (180, 230, 255), (fx_, fy_), 3)
            pygame.draw.circle(s, (255, 255, 255), (fx_, fy_ - 1), 1)
            if random.random() < 0.4:
                self.particles.append(Particle(fx_, fy_, random.uniform(-8, 8), -30, 0.4, (120, 190, 255), 1))
        if self.hold:
            icon, col, ht = self.hold
            yy = p.y - 28 - (1 - min(1, (1.4 - ht) * 4)) * 6
            gfx.draw_glow(s, int(p.x), int(yy), 16, col, 110)
            gfx.draw_icon(s, icon, col, p.x, yy)
        for b in self.pbullets:
            b.draw(s, t)
        weapons.draw(self, s)
        for b in self.ebullets:
            b.draw(s, t)
        for pt in self.particles:
            pt.draw(s)
        for pt in self.ambient:
            pt.draw(s)
        for f in self.floats:
            gfx.TEXT.add(f[2], f[0], f[1], 6 if f[2] != 'Kritisch!' else 7, f[3], 'c', alpha=int(255 * min(1, f[4] * 3)))
        # Dunkelheit
        dark = self.biome['dark'] + (150 if self.curse == 'dunkel' else 0)
        if dark > 0 and not self.room.kind.startswith('shrine'):
            self.draw_dark(s, min(215, dark))
        gfx.color_grade(s, self.biome.get('grade', _GRADE.get(self.biome_id, (0, 0, 0))), 18)
        if self.timestop > 0:
            ov = pygame.Surface((RW, RH), pygame.SRCALPHA)
            ov.fill((90, 110, 200, 40))
            s.blit(ov, (RX, RY))
        low = p.total_hp() <= 2 and not p.dead
        if self.hurt_flash > 0 or low:
            a = int(self.hurt_flash * 600) if self.hurt_flash > 0 else int(60 + 50 * math.sin(t * 5))
            if self.save['settings'].get('flash', True) is False:
                a = int(a * 0.4) if self.hurt_flash > 0 else 60
            gfx.color_grade_edge(s, (200, 0, 30), min(220, a))
        calm = self.save['settings'].get('flash', True) is False
        if self.flash_white > 0 and not calm:
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((255, 255, 255, int(min(1, self.flash_white * 4) * 150)))
            s.blit(ov, (0, 0))
        self._last = s.subsurface((RX - 16, RY - 16, RW + 32, RH + 32)).copy()
        self._last_hi = list(gfx.HI)
        if self.slide:
            img, d, st, old_hi = self.slide
            f = min(1, st / 0.24)
            f = f * f * (3 - 2 * f)
            dx, dy = DIRS[d]
            ow, oh = RW + 32, RH + 32
            ox, oy = -dx * ow * f, -dy * oh * f
            area = pygame.Rect(RX - 16, RY - 16, ow, oh)
            s.set_clip(area)
            cur = s.subsurface(area).copy()
            s.blit(cur, (area.x + dx * ow * (1 - f), area.y + dy * oh * (1 - f)))
            s.blit(img, (area.x + ox, area.y + oy))
            s.set_clip(None)
            nx, ny = dx * ow * (1 - f), dy * oh * (1 - f)
            def inside(e, sx, sy):
                return area.x - 20 < e[1] + sx < area.right + 20 and area.y - 10 < e[2] + sy < area.bottom + 30
            new = [(e[0], e[1] + nx, e[2] + ny, e[3]) for e in gfx.HI]
            old = [(e[0], e[1] + ox, e[2] + oy, e[3]) for e in old_hi]
            gfx.HI[:] = [e for e in old if inside(e, 0, 0)] + [e for e in new if inside(e, 0, 0)]
        if self.whiteout > 0:
            fl = pygame.Surface((RW, RH)); fl.fill((255, 246, 230))
            fl.set_alpha(int(min(1, self.whiteout / 0.45) * 170 * (0.5 if self.save['settings'].get('flash', True) is False else 1)))
            s.blit(fl, (RX, RY))
        if self.hint_t > 0 and self.hint_txt and self.game.state == 'play':
            a = min(1.0, self.hint_t, (6.0 - self.hint_t) * 3)
            hw = min(RW - 20, 8 + len(self.hint_txt) * 4)
            bx = RX + RW // 2 - hw // 2
            by = RY + 6
            bg = pygame.Surface((hw, 14), pygame.SRCALPHA)
            bg.fill((12, 8, 18, int(190 * a)))
            pygame.draw.rect(bg, (200, 170, 110, int(220 * a)), bg.get_rect(), 1)
            s.blit(bg, (bx, by))
            gfx.TEXT.add(self.hint_txt, RX + RW // 2, by + 3, 6, (250, 236, 200), 'c', alpha=int(255 * a))
        self.draw_hud(s, t)
        if getattr(self, 'descend', 0) > 0:
            f = 1 - self.descend / 1.3
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((6, 2, 8, int(255 * min(1, self.descend * 1.6))))
            s.blit(ov, (0, 0))
            for i in range(5):
                z = (f * 2.2 + i * 0.22) % 1.1
                sc = 0.15 + z * 2.2
                al = int(255 * max(0, min(1, (1.1 - z) * 2)) * min(1, self.descend * 2))
                cx, cy = W // 2, H // 2 + 10
                w, h = int(60 * sc), int(50 * sc)
                col = (210, 50, 40)
                tor = pygame.Surface((W, H), pygame.SRCALPHA)
                pygame.draw.rect(tor, col + (al,), (cx - w // 2, cy - h // 2, w, max(2, int(5 * sc))))
                pygame.draw.rect(tor, col + (al,), (cx - w // 2 + int(6 * sc), cy - h // 2 + int(10 * sc), w - int(12 * sc), max(1, int(3 * sc))))
                pygame.draw.rect(tor, col + (al,), (cx - w // 2 + int(8 * sc), cy - h // 2, max(2, int(4 * sc)), h))
                pygame.draw.rect(tor, col + (al,), (cx + w // 2 - int(12 * sc), cy - h // 2, max(2, int(4 * sc)), h))
                s.blit(tor, (0, 0))
        if self.fade > 0:
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, int(min(1, self.fade) * 255)))
            s.blit(ov, (0, 0))

    _light = {}

    def draw_dark(self, s, a):
        key = a
        L = self._light.get(key)
        if L is None:
            R = 90
            L = pygame.Surface((R * 2, R * 2), pygame.SRCALPHA)
            L.fill((0, 0, 0, a))
            for r in range(R, 0, -2):
                al = int(a * (r / R) ** 1.5)
                pygame.draw.circle(L, (0, 0, 0, al), (R, R), r)
            self._light[key] = L
        ov = pygame.Surface((RW, RH), pygame.SRCALPHA)
        ov.fill((0, 0, 0, a))
        p = self.player
        R = L.get_width() // 2
        ov.blit(L, (p.x - RX - R, p.y - RY - R), special_flags=pygame.BLEND_RGBA_MIN)
        small = pygame.transform.smoothscale(L, (R, R))
        for ty in range(ROWS):
            for tx in range(COLS):
                if self.room.tiles[ty][tx] == T_LANTERN:
                    ov.blit(small, (tx * TILE + 16 - R // 2, ty * TILE + 12 - R // 2), special_flags=pygame.BLEND_RGBA_MIN)
        for e in self.enemies:
            if e.d.get('glow') or e.is_boss:
                ov.blit(small, (e.x - RX - R // 2, e.y - RY - R // 2), special_flags=pygame.BLEND_RGBA_MIN)
        for pd in self.pedestals:
            ov.blit(small, (pd.x - RX - R // 2, pd.y - RY - R // 2), special_flags=pygame.BLEND_RGBA_MIN)
        s.blit(ov, (RX, RY))

    def draw_hud(self, s, t):
        p = self.player
        T = gfx.TEXT
        # Herzen
        x0, y0 = 8, 4
        i = 0
        full = p.hp // 2
        for k in range(p.maxhp // 2):
            fill = 2 if k < full else (1 if k == full and p.hp % 2 else 0)
            gfx.heart(s, x0 + (i % 10) * 12, y0 + (i // 10) * 10, 'red', fill)
            i += 1
        for k in range((p.spirit + 1) // 2):
            fill = 2 if (k * 2 + 2) <= p.spirit else 1
            gfx.heart(s, x0 + (i % 10) * 12, y0 + (i // 10) * 10, 'spirit', fill)
            i += 1
        # Ressourcen
        rx, ry = 130, 4
        if not gfx.hud_icon('coin', rx + 4, ry + 4):
            pygame.draw.circle(s, (232, 190, 70), (rx + 4, ry + 4), 4); pygame.draw.rect(s, (60, 40, 20), (rx + 3, ry + 3, 2, 2))
        T.add('%02d' % p.coins, rx + 11, ry - 1, 8)
        if not gfx.hud_icon('key', rx + 38, ry + 4):
            pygame.draw.circle(s, (250, 210, 90), (rx + 34, ry + 4), 3, 1); pygame.draw.rect(s, (250, 210, 90), (rx + 36, ry + 3, 6, 2))
        T.add('%02d' % p.keys, rx + 45, ry - 1, 8)
        if not gfx.hud_icon('salt', rx + 70, ry + 4):
            pygame.draw.polygon(s, (250, 250, 255), [(rx + 66, ry + 8), (rx + 74, ry + 8), (rx + 70, ry + 1)])
        T.add('%d' % p.salts, rx + 77, ry - 1, 8)
        # Aktives Item
        if p.active:
            a = ACTIVES[p.active]
            ax, ay = 236, 14
            pygame.draw.rect(s, (20, 14, 24), (ax - 11, ay - 11, 22, 22))
            pygame.draw.rect(s, (120, 100, 70), (ax - 11, ay - 11, 22, 22), 1)
            gfx.draw_icon(s, a['icon'], a['col'], ax, ay)
            mx = a['charge']
            bw = 4
            for k in range(mx):
                hh = 20 // mx
                col = (120, 220, 120) if k < p.charge else (50, 40, 50)
                if p.charge >= mx:
                    col = (255, 230, 120) if int(t * 4) % 2 else (180, 240, 140)
                pygame.draw.rect(s, col, (ax + 13, ay + 9 - (k + 1) * hh + 1, bw, hh - 1))
            T.add('E', ax - 15, ay - 12, 7, (200, 190, 160), 'r')
        if p.trinket:
            tr = TRINKETS[p.trinket]
            pygame.draw.rect(s, (20, 14, 24), (262, 5, 18, 18))
            pygame.draw.rect(s, (120, 100, 70), (262, 5, 18, 18), 1)
            gfx.draw_icon(s, tr['icon'], tr['col'], 271, 14)
        # Ebene
        T.add('%s – %s' % (self.biome['jp'], self.biome['name']), 300, 3, 8, (230, 220, 190))
        info = ('Prüfung  •  ' if self.challenge else '') + ('%d:%02d  •  ' % (max(0, 900 - self.time) // 60, max(0, 900 - self.time) % 60) if self.challenge == 'zeitlauf' else '') + self.floor_label() + ('  •  Schleife %d' % (self.loop + 1) if self.endless else '') + ('  •  Oni-Modus' if self.hard else '') + ('  •  Fluch: ' + {'dunkel': 'Dunkelheit', 'nebel': 'Nebel', 'labyrinth': 'Labyrinth', 'verirrt': 'Verirrte'}.get(self.curse, '') if self.curse else '') + ('  •  Segen: ' + BLESSINGS[self.blessing][0].split()[-1] if self.blessing else '')
        T.add(info, 300, 15, 6, (190, 170, 150))
        # Werte-Leiste
        self.draw_statbar(s, t)
        # Minikarte
        if self.curse != 'nebel' and not self.room.kind.startswith('shrine'):
            self.draw_minimap(s, W - 8, RY - 12)
        # Boss-Lebensbalken
        b = self.boss
        if b and not b.dead and b.spawn_t <= 0.6:
            bw = 240
            bx = (W - bw) // 2 + 50
            by = H - 10
            pygame.draw.rect(s, (20, 10, 20), (bx - 2, by - 2, bw + 4, 8))
            f = max(0, b.hp / b.maxhp)
            tr = getattr(self, '_boss_trail', None)
            if tr is None or tr[0] is not b:
                tr = [b, f]
            tr[1] = f if tr[1] < f else max(f, tr[1] - 0.25 * (1 / 60) - (tr[1] - f) * 0.03)
            self._boss_trail = tr
            pygame.draw.rect(s, (90, 20, 30), (bx, by, bw, 4))
            pygame.draw.rect(s, (255, 214, 150), (bx, by, int(bw * tr[1]), 4))          # Schadensspur
            rage = f <= 0.25
            pygame.draw.rect(s, (255, 90, 40) if rage else (220, 50, 60), (bx, by, int(bw * f), 4))
            pygame.draw.rect(s, (255, 150, 140) if not rage else (255, 200, 120), (bx, by, int(bw * f), 1))
            tx_ = bx + int(bw * 0.25)                                                      # Wut-Schwelle
            pygame.draw.line(s, (255, 240, 220), (tx_, by - 2), (tx_, by + 5), 1)
            T.add(b.name, bx - 6, by - 4, 7, (255, 220, 200), 'r')
        # Titelkarte
        if self.title_t > 0 and self.boss_intro <= 0:
            a = int(255 * min(1, self.title_t))
            band = getattr(Run, '_title_band', None)
            if band is None:
                bh = 2 * 118
                band = pygame.Surface((W * 2, bh), pygame.SRCALPHA)
                for yy in range(bh):
                    e = min(yy, bh - 1 - yy) / 40.0
                    band.fill((8, 5, 12, int(150 * min(1.0, e))), (0, yy, W * 2, 1))
                Run._title_band = band
            gfx.HI.append((band, W / 2, 170, int(a * 0.85), 1.0, True))
            T.add(self.floor_label(), W // 2, 92, 9, (230, 210, 170), 'c', alpha=a)
            self.draw_path(s, W // 2, 84, a)
            if self.stage == 0:
                T.add(CHAPTER_NAMES.get(self.depth, ''), W // 2, 66, 8, (240, 190, 150), 'c', alpha=a)
            T.add(self.biome['name'], W // 2, 104, 18, (255, 245, 225), 'c', alpha=a)
            T.add(self.biome['jp'], W // 2, 128, 10, (210, 170, 150), 'c', alpha=a)
            if not hasattr(self, 'tip') or self.tip[0] != self.floor_no:
                self.tip = (self.floor_no, random.choice(TIPS))
            q = self.QUIRKS.get(self.biome_id)
            line2 = ('„' + CHAPTER_LORE[self.depth] + '“') if (self.stage == 0 and self.depth in CHAPTER_LORE and not self.loop) \
                else 'Tipp: ' + self.tip[1]
            col2 = (225, 205, 235) if line2.startswith('„') else (200, 190, 170)
            if q:
                T.add('Eigenheit: ' + self.QUIRK_SHORT[q], W // 2, 142, 8, (255, 200, 140), 'c', alpha=a)
                T.add(line2, W // 2, 155, 7, col2, 'c', alpha=a)
            else:
                T.add(line2, W // 2, 148, 7, col2, 'c', alpha=a)
        if self.boss_intro > 0 and self.boss:
            a = int(255 * min(1, self.boss_intro))
            if self.portrait is None or self.portrait[0] is not self.boss:
                self.portrait = (self.boss, self.make_portrait(self.boss))
                self.remember_boss(self.boss, self.portrait[1])
            img = self.portrait[1]
            slide = min(1, (2.2 - self.boss_intro) * 4)
            ov = pygame.Surface((W, 110), pygame.SRCALPHA)
            ov.fill((10, 4, 14, int(a * 0.8)))
            s.blit(ov, (0, 95))
            pygame.draw.line(s, (200, 60, 60), (0, 95), (W, 95), 2)
            pygame.draw.line(s, (200, 60, 60), (0, 204), (W, 204), 2)
            if img is not None:
                gfx.hi_blit(img, int(-200 + 300 * slide) + 30, 203, a)
            T.add(self.boss.name, W // 2 + 70, 122, 20, (255, 210, 190), 'c', alpha=a)
            T.add(self.boss.title, W // 2 + 70, 152, 9, (230, 190, 170), 'c', alpha=a)
            T.add(self.floor_label(), W // 2 + 70, 170, 7, (190, 160, 150), 'c', alpha=a)
        # Banner
        if self.cur_banner:
            title, sub, col, big, fxs = self.cur_banner
            a = int(255 * min(1, self.banner_t * 3, (3.4 - self.banner_t) * 6 + 0.2))
            a = max(0, min(255, a))
            hh = 44 if fxs else 34
            ov = pygame.Surface((W, hh), pygame.SRCALPHA)
            ov.fill((10, 6, 14, int(a * 0.75)))
            y0 = RY + RH - 10 - hh
            s.blit(ov, (0, y0))
            T.add(title, W // 2, y0 + 2, 12 if big else 10, col, 'c', alpha=a)
            if sub:
                T.add('„%s“' % sub if fxs else sub, W // 2, y0 + 19, 7, (230, 225, 210), 'c', alpha=a)
            if fxs:
                T.add(fxs, W // 2, y0 + 31, 7, (170, 220, 255), 'c', alpha=a)

    def draw_statbar(self, s, t):
        p = self.player
        T = gfx.TEXT
        y = RY + RH + 19
        pygame.draw.rect(s, (14, 9, 18), (0, y - 2, W, 14))
        items = [('dmg', 'Schaden', '%.2f' % p.damage(), (240, 90, 80)), ('rate', 'Feuerrate', '%.2f/s' % p.s['rate'], (250, 200, 90)),
                 ('spd', 'Tempo', '%d' % p.s['spd'], (120, 220, 140)), ('range', 'Reichweite', '%d' % p.s['range'], (120, 180, 250)),
                 ('shotspd', 'Schussgeschw.', '%d' % p.s['shotspd'], (180, 140, 250)), ('luck', 'Glück', '%g' % p.s['luck'], (120, 230, 200))]
        x = 14
        for k, name, val, col in items:
            pygame.draw.circle(s, col, (x + 2, y + 4), 3)
            T.add(name, x + 8, y, 6, (175, 165, 155))
            vx = x + 8 + gfx.text_w(name, 6) + 3
            T.add(val, vx, y, 6, (250, 245, 235))
            d = self.stat_delta.get(k)
            if d:
                T.add(('+' if d[0] > 0 else '') + ('%.2f' % d[0] if k in ('dmg', 'rate') else '%g' % round(d[0], 1)),
                      vx + gfx.text_w(val, 6) + 2, y, 6, (120, 255, 140) if d[0] > 0 else (255, 120, 110), alpha=int(255 * min(1, d[1])))
            x += 78

    def remember_boss(self, b, img):
        """Boss fürs Lexikon merken und sein Porträt einmalig speichern."""
        bid = getattr(b, 'id', None)
        if not bid:
            return
        seen = self.save.data.setdefault('bosses_seen', [])
        if bid not in seen:
            seen.append(bid)

    def make_portrait(self, b):
        """Porträt des Bosses für das Intro: rendert die Hi-Res-Teile auf eine eigene Fläche, vergrößert."""
        tmp = pygame.Surface((W, H), pygame.SRCALPHA)
        n0 = len(gfx.HI)
        old_sp, old_fl = b.spawn_t, b.flash
        b.spawn_t, b.flash = 0, 0
        old_trail = getattr(b, 'trail', None)
        if old_trail is not None:                      # Schlangenleib für das Porträt in eine Welle legen
            b.trail = [(b.x + i * 0.8, b.y + math.sin(i * 0.05) * 14) for i in range(len(old_trail))]
            b.heading = math.pi
        try:
            if getattr(b, 'sheet', None):
                b.render_sheet(tmp, 0.0)
            else:
                b.render(tmp, 0.0)
        except Exception:
            pass
        b.spawn_t, b.flash = old_sp, old_fl
        if old_trail is not None:
            b.trail = old_trail
        ents = gfx.HI[n0:]
        del gfx.HI[n0:]
        hi = pygame.transform.scale(tmp, (W * 2, H * 2))
        for e in ents:
            im, cx, by = e[0], e[1], e[2]
            hi.blit(im, (int(cx * 2 - im.get_width() / 2), int(by * 2 - im.get_height())))
        bb = hi.get_bounding_rect()
        focus = pygame.Rect(0, 0, 300, 220)
        focus.center = ((bb.centerx + int(b.x * 2)) // 2, (bb.centery + int(b.y * 2)) // 2)
        bb = bb.clip(focus)
        if bb.w < 4 or bb.h < 4:
            return None
        crop = hi.subsurface(bb).copy()
        f = min(2.0, 300 / bb.w, 210 / bb.h)
        f = max(0.5, math.floor(f * 2) / 2)
        return pygame.transform.scale(crop, (int(bb.w * f), int(bb.h * f)))

    def draw_minimap(self, s, right, top):
        cw, ch = 11, 7
        rooms = self.rooms
        show_all = bool(self.player.f['map']) or self.blessing == 'vollmond'
        xs = [p[0] for p in rooms]
        ys = [p[1] for p in rooms]
        minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
        w = (maxx - minx + 1) * cw
        h = (maxy - miny + 1) * ch
        x0 = right - w
        y0 = 2
        bg = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
        bg.fill((6, 4, 10, 150))
        pygame.draw.rect(bg, (120, 96, 70, 170), bg.get_rect(), 1)
        s.blit(bg, (x0 - 2, y0 - 2))
        icons = {'secret': (200, 180, 140), 'boss': (230, 50, 50), 'treasure': (240, 200, 70), 'shop': (90, 200, 90), 'curse': (170, 80, 200),
                 'challenge': (230, 120, 60), 'omikuji': (230, 80, 70), 'onsen': (120, 200, 230), 'yomeiri': (255, 170, 90),
                 'library': (170, 140, 230), 'dojo': (240, 160, 60), 'teahouse': (120, 190, 100), 'slots': (240, 140, 80)}
        for pos, r in rooms.items():
            if not (r.seen or show_all) or not r.revealed:
                continue
            rx = x0 + (pos[0] - minx) * cw
            ry = y0 + (pos[1] - miny) * ch
            col = (178, 166, 150) if r.visited else (78, 70, 80)
            cur = pos == self.room.pos
            if cur:
                col = (250, 236, 200)
            pygame.draw.rect(s, col, (rx, ry, cw - 1, ch - 1))
            if r.visited or cur:
                pygame.draw.line(s, (255, 250, 235) if cur else (210, 200, 185), (rx, ry), (rx + cw - 2, ry))
            if cur:
                pa = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 180.0)
                pygame.draw.rect(s, (255, int(180 + 60 * pa), 90), (rx - 1, ry - 1, cw + 1, ch + 1), 1)
            if r.kind in icons and (r.seen or show_all):
                img = props.map_icon(r.kind)
                if img is not None and gfx.HI_MODE:
                    gfx.hi_blit(img, rx + (cw - 1) / 2, ry + (ch - 1) / 2 + img.get_height() / 4)
                else:
                    c = icons[r.kind]
                    pygame.draw.rect(s, c, (rx + cw // 2 - 2, ry + ch // 2 - 2, 3, 3))
