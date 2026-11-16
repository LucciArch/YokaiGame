"""Spielobjekte: Spielerin, Geschosse, Yokai, Pickups, Sockel, Gefahrenzonen, Partikel."""
import math
import random
import pygame
from collections import defaultdict
from .settings import *
from . import gfx, audio, art, sheets, props, costume, weapons, sigs
from .data import ITEMS, ENEMIES, CHAMPIONS, ACTIVES, CHARS, SYNERGIES, TRANSFORMS, TRINKETS

ONE_TIME = ('hp', 'heal', 'spirit', 'coins', 'keys', 'salts', 'fullheal')


def clamp(v, a, b):
    return a if v < a else b if v > b else v


def norm(x, y):
    d = math.hypot(x, y)
    return (x / d, y / d) if d > 1e-6 else (0.0, 0.0)


def tile_at(room, x, y):
    tx, ty = int((x - RX) // TILE), int((y - RY) // TILE)
    if 0 <= tx < COLS and 0 <= ty < ROWS:
        return room.tiles[ty][tx], tx, ty
    return None, tx, ty


def blocked(room, x, y, r, fly=False):
    if x - r < RX or x + r > RX + RW or y - r < RY or y + r > RY + RH:
        return True
    for cx in (x - r, x + r):
        for cy in (y - r, y + r):
            t, _, _ = tile_at(room, cx, cy)
            if t in SOLID_TILES:
                return True
            if t == T_PIT and not fly:
                return True
    return False


def move_body(room, x, y, r, dx, dy, fly=False):
    """Bewegt einen Kreis mit Gleiten an Hindernissen. Gibt (x, y, blockiert_x, blockiert_y) zurück."""
    bx = by = False
    if dx:
        if not blocked(room, x + dx, y, r, fly):
            x += dx
        else:
            bx = True
    if dy:
        if not blocked(room, x, y + dy, r, fly):
            y += dy
        else:
            by = True
    return x, y, bx, by


def free_tile_pos(room, rng, avoid=None, mind=60, fly=False):
    for _ in range(80):
        tx, ty = rng.randrange(COLS), rng.randrange(ROWS)
        t = room.tiles[ty][tx]
        if t in SOLID_TILES or (t == T_PIT and not fly):
            continue
        x, y = RX + tx * TILE + 16, RY + ty * TILE + 16
        if avoid and math.hypot(x - avoid[0], y - avoid[1]) < mind:
            continue
        return x, y
    return RX + RW / 2, RY + RH / 2


# =========================================================================  Partikel
class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'life', 'max', 'col', 'size', 'grav', 'kind')

    def __init__(self, x, y, vx, vy, life, col, size=2, grav=0.0, kind='dot'):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.life = self.max = life
        self.col, self.size, self.grav, self.kind = col, size, grav, kind

    def update(self, dt):
        self.life -= dt
        self.vy += self.grav * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.98
        return self.life > 0

    def draw(self, s):
        f = self.life / self.max
        if self.kind == 'dot':
            sz = max(1, int(self.size * (0.4 + 0.6 * f)))
            pygame.draw.rect(s, self.col, (int(self.x), int(self.y), sz, sz))
        elif self.kind == 'ring':
            r = int(self.size * (1 - f) + 2)
            pygame.draw.circle(s, self.col, (int(self.x), int(self.y)), r, 1)
        elif self.kind == 'wave':
            r = int(self.size * (1 - f * f) + 3)
            w = max(1, int(4 * f + 1))
            gfx.draw_glow(s, int(self.x), int(self.y), r + 6, self.col, int(60 * f))
            pygame.draw.circle(s, self.col, (int(self.x), int(self.y)), r, w)
            if r > 4:
                pygame.draw.circle(s, (255, 255, 240), (int(self.x), int(self.y)), r - w, 1)
        elif self.kind == 'petal':
            pygame.draw.ellipse(s, self.col, (int(self.x), int(self.y), 3, 2))
        elif self.kind == 'rain':
            pygame.draw.line(s, self.col, (self.x, self.y), (self.x - 2, self.y - 7), 1)
            if self.life < 0.05 or self.y > RY + RH - 4:
                pygame.draw.circle(s, self.col, (int(self.x), int(self.y)), 2, 1)
        elif self.kind == 'soul':
            x, y = int(self.x + math.sin(self.life * 9) * 2), int(self.y)
            gfx.draw_glow(s, x, y, 7, self.col, int(110 * f))
            pygame.draw.circle(s, (240, 250, 255), (x, y), max(1, int(2 * f + 0.5)))
        elif self.kind == 'spark':
            ln = 4 * f + 1
            n = math.hypot(self.vx, self.vy) or 1
            pygame.draw.line(s, self.col, (self.x, self.y), (self.x - self.vx / n * ln, self.y - self.vy / n * ln), 1)


def burst(run, x, y, col, n=8, spd=60, life=0.4, size=2, grav=0):
    for _ in range(n):
        a = random.uniform(0, math.tau)
        v = random.uniform(0.3, 1) * spd
        run.particles.append(Particle(x, y, math.cos(a) * v, math.sin(a) * v, random.uniform(0.5, 1) * life, col, size, grav))


# =========================================================================  Geschosse
class Bullet:
    __slots__ = ('x', 'y', 'vx', 'vy', 'dmg', 'r', 'life', 'maxlife', 'owner', 'fl', 'col', 'bounces', 'hit',
                 't', 'eff', 'acc', 'ay', 'curve', 'returned', 'big', 'gold', 'delay', 'dead', 'kind', 'arrow', 'crescent', 'wind', 'src')

    def __init__(self, x, y, vx, vy, dmg, r, life, owner, col, fl=None, eff=None, acc=0.0, ay=0.0, curve=0.0,
                 delay=0.0, kind='orb'):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.dmg, self.r, self.life, self.maxlife = dmg, r, life, life
        self.owner, self.col, self.fl = owner, col, fl or {}
        self.bounces = 2 if self.fl.get('bounce') else 0
        self.hit = set()
        self.src = None
        self.t = 0.0
        self.eff, self.acc, self.ay, self.curve = eff, acc, ay, curve
        self.returned = False
        self.big = False
        self.gold = False
        self.delay = delay
        self.dead = False
        self.kind = kind
        self.arrow = self.crescent = self.wind = False

    def update(self, dt, run):
        if self.delay > 0:
            self.delay -= dt
            return True
        self.t += dt
        self.life -= dt
        fl = self.fl
        if self.acc:
            f = 1 + self.acc * dt
            self.vx *= f; self.vy *= f
        if self.ay:
            self.vy += self.ay * dt
        if self.curve:
            c, s = math.cos(self.curve * dt), math.sin(self.curve * dt)
            self.vx, self.vy = self.vx * c - self.vy * s, self.vx * s + self.vy * c
        if self.owner == 'p':
            if 'sg' in fl:
                sigs.bullet_tick(self, run, dt)
                fl = self.fl
            if fl.get('homing'):
                tgt = run.nearest_enemy(self.x, self.y, 140)
                if tgt:
                    ang = math.atan2(self.vy, self.vx)
                    want = math.atan2(tgt.y - self.y, tgt.x - self.x)
                    d = (want - ang + math.pi) % math.tau - math.pi
                    ang += clamp(d, -6 * dt, 6 * dt)
                    sp = math.hypot(self.vx, self.vy)
                    self.vx, self.vy = math.cos(ang) * sp, math.sin(ang) * sp
            if fl.get('boomerang') and not self.returned and self.life < self.maxlife * 0.45:
                self.returned = True
                self.life = self.maxlife * 0.6
                self.hit.clear()
            if self.returned:
                p = run.player
                ang = math.atan2(p.y - self.y, p.x - self.x)
                sp = math.hypot(self.vx, self.vy)
                cur = math.atan2(self.vy, self.vx)
                d = (ang - cur + math.pi) % math.tau - math.pi
                cur += clamp(d, -9 * dt, 9 * dt)
                self.vx, self.vy = math.cos(cur) * sp, math.sin(cur) * sp
                if math.hypot(p.x - self.x, p.y - self.y) < 8:
                    return False
        mx, my = self.vx * dt, self.vy * dt
        if fl.get('wave'):
            px, py = norm(-self.vy, self.vx)
            w = math.cos(self.t * 16) * 2.2
            mx += px * w; my += py * w
        nx, ny = self.x + mx, self.y + my
        # Wände
        if nx < RX or nx > RX + RW or ny < RY or ny > RY + RH:
            if self.bounces > 0:
                self.bounces -= 1
                if self.owner == 'p':
                    sigs.bullet_bounce(run, self)
                if nx < RX or nx > RX + RW:
                    self.vx = -self.vx
                if ny < RY or ny > RY + RH:
                    self.vy = -self.vy
                return True
            return False
        t, tx, ty = tile_at(run.room, nx, ny)
        if t in SOLID_TILES and not fl.get('spectral'):
            if t == T_POT:
                run.break_tile(tx, ty)
            if self.bounces > 0:
                self.bounces -= 1
                if self.owner == 'p':
                    sigs.bullet_bounce(run, self)
                t1, _, _ = tile_at(run.room, nx, self.y)
                if t1 in SOLID_TILES:
                    self.vx = -self.vx
                else:
                    self.vy = -self.vy
                return True
            return False
        self.x, self.y = nx, ny
        return self.life > 0

    def draw(self, s, tm):
        x, y = int(self.x), int(self.y)
        if self.owner == 'p':
            ang = math.atan2(self.vy, self.vx)
            r = self.r
            if self.big:
                gfx.draw_glow(s, x, y, int(r * 3), (255, 120, 120), 70)
            col = self.col
            if gfx.HI_MODE and self.delay <= 0 and (getattr(self, 'arrow', False) or getattr(self, 'crescent', False)):
                img = props.arrow(ang) if getattr(self, 'arrow', False) else props.crescent(ang)
                gfx.hi_blit(img, x, y + img.get_height() / 4)
                return
            if gfx.HI_MODE and self.delay <= 0:
                img = props.ofuda(tuple(col), r, ang)
                if img is not None:
                    gfx.hi_blit(img, x, y + img.get_height() / 4)
                    return
            # Ofuda: kleiner Papierstreifen
            c, si = math.cos(ang), math.sin(ang)
            hw, hh = r * 1.5, r * 0.85
            pts = [(x + c * hw - si * hh, y + si * hw + c * hh), (x + c * hw + si * hh, y + si * hw - c * hh),
                   (x - c * hw + si * hh, y - si * hw - c * hh), (x - c * hw - si * hh, y - si * hw + c * hh)]
            pygame.draw.polygon(s, (24, 16, 24), [(px + 1, py + 1) for px, py in pts])
            pygame.draw.polygon(s, col, pts)
            pygame.draw.line(s, (200, 30, 40), (x - c * hw * 0.4, y - si * hw * 0.4), (x + c * hw * 0.4, y + si * hw * 0.4), 1)
        else:
            if self.delay > 0:
                pygame.draw.circle(s, self.col, (x, y), max(1, int(self.r * 0.6)), 1)
                return
            gfx.draw_glow(s, x, y, int(self.r * 2.6), self.col, 80)
            img = props.orb(tuple(self.col), int(self.r))
            s.blit(img, (x - self.r - 2, y - self.r - 2))


def ebullet(run, x, y, ang, speed, col=(240, 80, 120), r=3, eff=None, **kw):
    sp = speed * run.bullet_speed_mult
    b = Bullet(x, y, math.cos(ang) * sp, math.sin(ang) * sp, 1, r, 6.0, 'e', col, eff=eff, **kw)
    b.src = getattr(run, 'cur_src', None)
    run.ebullets.append(b)
    return b


# =========================================================================  Spielerin
class Familiar:
    def __init__(self, idx):
        self.idx = idx
        self.x = self.y = 0
        self.cd = random.uniform(0, 0.5)


class Player:
    def __init__(self, run, char_id):
        self.run = run
        self.char = char_id
        c = CHARS[char_id]
        self.x, self.y = RX + RW / 2, RY + RH / 2 + 30
        self.r = 5
        self.hitr = 3
        self.spirit_only = c.get('spirit_only', False)
        self.maxhp = c['hp']
        self.hp = c['hp']
        self.spirit = c['spirit']
        self.coins, self.keys, self.salts = c['coins'], c['keys'], c['salts']
        self.items = []
        self.active = c['active']
        self.charge = ACTIVES[self.active]['charge'] if self.active else 0
        self.synergies = []
        self.transforms = []
        self.iframes = 1.0
        self.dash_t = 0.0
        self.dash_cd = 0.0
        self.dash_dir = (0, 1)
        self.dash_hit = set()
        self.dash_trail = 0.0
        self.shoot_cd = 0.0
        self.shot_count = 0
        self.sg = {}
        self.sgs = set()
        self.facing = (0, 1)
        self.flip = False
        self.moving = False
        self.anim = 0.0
        self.familiars = []
        self.orb_angle = 0.0
        self.orb_hit_cd = defaultdict(float)
        self.aura_cd = 0.0
        self.shield_ready = False
        self.hurt_buff = 0.0
        self.kagura = 0.0
        self.room_dmg_buff = 0.0
        self.knock = (0.0, 0.0)
        self.wind = (0.0, 0.0)
        self.revives = 0
        self.dead = False
        self.hit_this_floor = False
        self.vx = self.vy = 0.0
        self.s = {}
        self.f = defaultdict(float)
        self.bonus = defaultdict(float)
        self.trinket = None
        self.recoil = 0.0
        self.temp = []   # [fx-dict, rest-zeit]
        self.recalc()
        run.player = self
        for iid in c['items']:
            self.gain_item(iid, silent=True)

    # ---------------------------------------------------------- Werte
    def sources(self):
        out = [CHARS[self.char]['fx']]
        out += [ITEMS[i]['fx'] for i in self.items]
        out += [s['fx'] for s in SYNERGIES if s['id'] in self.synergies]
        out += [TRANSFORMS[t]['fx'] for t in self.transforms]
        out.append(self.bonus)
        if getattr(self, 'trinket', None):
            out.append(TRINKETS[self.trinket]['fx'])
        out += [t[0] for t in getattr(self, 'temp', [])]
        return out

    def recalc(self):
        f = defaultdict(float)
        dm, rm = 1.0, 1.0
        for fx in self.sources():
            for k, v in fx.items():
                if k == 'dmgm':
                    dm *= v
                elif k == 'ratem':
                    rm *= v
                elif k in ONE_TIME:
                    continue
                else:
                    f[k] += v
        sigs.stat_bonus(self, f)
        self.f = f
        self.sgs = sigs.active(self)
        old = dict(self.s) if self.s else None
        self.s = dict(
            dmg=max(0.5, (3.5 + f['dmg']) * dm),
            rate=clamp((2.6 + f['rate']) * rm, 0.8, 12),
            shotspd=clamp(210 + f['shotspd'], 110, 440),
            range=clamp(190 + f['range'], 70, 500),
            spd=clamp(88 + f['spd'], 55, 170),
            size=clamp(3 + f['size'] * 1.0, 1.5, 9),
            luck=f['luck'],
        )
        if old and getattr(self.run, 'stat_delta', None) is not None:
            for k, v in self.s.items():
                dlt = v - old.get(k, v)
                if abs(dlt) > 1e-6:
                    self.run.stat_delta[k] = [dlt, 3.0]
        want = int(f['familiar'])
        while len(self.familiars) < want:
            fm = Familiar(len(self.familiars))
            fm.x, fm.y = self.x, self.y
            self.familiars.append(fm)
        del self.familiars[want:]
        self.revive_flag = int(f['revive'])

    def damage(self):
        d = self.s['dmg']
        if self.f['money_dmg']:
            d += min(6.0, self.coins * 0.1) if 'kaufmann' in self.sgs else min(4.0, self.coins * 0.05)
        if self.f['rage']:
            total = max(1, self.maxhp + self.spirit)
            missing = 1 - (self.hp + self.spirit) / max(total, 1)
            d *= 1 + clamp(missing, 0, 1) * 0.9
        if self.hurt_buff > 0:
            d *= 1.4
        if self.room_dmg_buff > 0:
            d *= 1.5
        if self.kagura > 0:
            d *= 1.3
        return d * sigs.dmg_mult(self)

    def apply_once(self, fx):
        if 'hp' in fx:
            if self.spirit_only:
                self.spirit += int(fx['hp'] * 2)
            else:
                self.maxhp = min(24, self.maxhp + int(fx['hp'] * 2))
                self.hp = min(self.maxhp, self.hp + int(fx['hp'] * 2))
        if 'heal' in fx and not self.spirit_only:
            self.hp = min(self.maxhp, self.hp + int(fx['heal']))
        if fx.get('fullheal') and not self.spirit_only:
            self.hp = self.maxhp
        if 'spirit' in fx:
            self.spirit = min(24 - self.maxhp, self.spirit + int(fx['spirit'])) if self.maxhp < 24 else self.spirit
        if 'coins' in fx:
            self.coins = min(99, self.coins + int(fx['coins']))
        if 'keys' in fx:
            self.keys = min(99, self.keys + int(fx['keys']))
        if 'salts' in fx:
            self.salts = min(9, self.salts + int(fx['salts']))
        if 'revive' in fx:
            self.revives += int(fx['revive'])

    def gain_item(self, iid, silent=False):
        it = ITEMS[iid]
        self.items.append(iid)
        self.apply_once(it['fx'])
        sigs.on_gain(self, iid)
        self.recalc()
        run = self.run
        if not silent:
            from .texts import fx_lines
            run.banner(it['name'], it['desc'], it['col'], fx=', '.join(fx_lines(it['fx'])))
            audio.play('item')
            run.hold = [it['icon'], it['col'], 1.4]
        run.on_item(iid)
        # Synergien
        for s in SYNERGIES:
            if s['id'] not in self.synergies and all(i in self.items for i in s['items']):
                self.synergies.append(s['id'])
                self.apply_once(s['fx'])
                self.recalc()
                from .texts import fx_lines
                run.banner('Synergie: ' + s['name'], s['desc'], (255, 220, 120), big=True, fx=', '.join(fx_lines(s['fx'])))
                audio.play('synergy')
                run.on_synergy(s['id'])
        # Transformationen (3 Items gleichen Themas)
        counts = defaultdict(int)
        for i in self.items:
            for t in ITEMS[i]['tags']:
                counts[t] += 1
        for t, n in counts.items():
            if n >= 3 and t not in self.transforms:
                self.transforms.append(t)
                self.apply_once(TRANSFORMS[t]['fx'])
                self.recalc()
                from .texts import fx_lines
                run.banner('Transformation: ' + TRANSFORMS[t]['name'], TRANSFORMS[t]['desc'], TRANSFORMS[t]['col'], big=True,
                           fx=', '.join(fx_lines(TRANSFORMS[t]['fx'])))
                audio.play('unlock')
                run.on_transform(t)

    # ---------------------------------------------------------- Leben
    def total_hp(self):
        return self.hp + self.spirit

    def hurt(self, amount=1, src=None):
        if self.dead or self.iframes > 0 or self.dash_t > 0 or self.kagura > 0:
            return False
        run = self.run
        if self.shield_ready:
            self.shield_ready = False
            self.iframes = 0.8
            sigs.shield_break(self, run)
            audio.play('bell')
            burst(run, self.x, self.y, (140, 200, 255), 16, 90)
            return False
        self.hit_this_floor = True
        if src:
            self.last_src = src
        run.boss_hit = True
        run.hitstop = 0.07
        while amount > 0 and self.spirit > 0:
            self.spirit -= 1; amount -= 1
        self.hp = max(0, self.hp - amount)
        self.iframes = 1.0
        run.shake(5)
        run.hurt_flash = 0.25
        audio.play('hurt')
        burst(run, self.x, self.y, (230, 50, 60), 14, 90)
        if self.f['hurt_ring']:
            for i in range(12):
                a = i / 12 * math.tau
                run.fire_player_bullet(self.x, self.y, a, self.damage() * 1.2, self.s['shotspd'], self.s['size'], 0.9, {'pierce': 1})
        if self.f['hurt_dmg']:
            self.hurt_buff = 6.0
        sigs.on_hurt(self, run)
        if self.total_hp() <= 0:
            if self.revives > 0:
                self.revives -= 1
                if self.spirit_only:
                    self.spirit = 4
                else:
                    self.maxhp = max(2, self.maxhp)
                    self.hp = min(self.maxhp, 4)
                self.iframes = 2.5
                run.banner('Wiedergeboren!', 'Die Götter geben dir eine zweite Chance', (255, 230, 150), big=True)
                audio.play('unlock')
                run.clear_ebullets()
            else:
                self.dead = True
        return True

    def heal(self, halves):
        if self.spirit_only:
            return False
        if self.hp >= self.maxhp:
            return False
        self.hp = min(self.maxhp, self.hp + halves)
        return True

    def add_spirit(self, halves):
        if self.maxhp + self.spirit >= 24:
            return False
        self.spirit = min(24 - self.maxhp, self.spirit + halves)
        return True

    # ---------------------------------------------------------- Update
    def update(self, dt, inp):
        run = self.run
        self.anim += dt
        for k in ('iframes', 'dash_cd', 'shoot_cd', 'hurt_buff', 'kagura', 'room_dmg_buff', 'aura_cd'):
            setattr(self, k, max(0.0, getattr(self, k) - dt))
        self.recoil = max(0.0, self.recoil - dt)
        if self.temp:
            for tfx in self.temp:
                tfx[1] -= dt
            n = len(self.temp)
            self.temp = [t for t in self.temp if t[1] > 0]
            if len(self.temp) != n:
                self.recalc()
        mvx, mvy = inp['move']
        fly = bool(self.f['fly'])
        self.moving = abs(mvx) + abs(mvy) > 0.1
        # Dash / Rolle
        if inp['dash'] and self.dash_cd <= 0 and self.dash_t <= 0:
            d = norm(mvx, mvy) if self.moving else self.facing
            self.dash_dir = d
            self.dash_t = 0.24
            self.dash_cd = 0.55
            self.dash_hit.clear()
            audio.play('dash')
            sigs.on_dash(self, run)
        sp = self.s['spd']
        if self.dash_t > 0:
            self.dash_t -= dt
            vx, vy = self.dash_dir[0] * sp * 2.9, self.dash_dir[1] * sp * 2.9
            self.dash_trail -= dt
            if self.dash_trail <= 0:
                self.dash_trail = 0.03
                run.particles.append(Particle(self.x, self.y + 4, 0, 0, 0.3, (200, 200, 220), 3))
                if self.f['dash_fire']:
                    run.hazards.append(Hazard(self.x, self.y, 10, 0.0, 1.2, self.damage() * 0.6, 'p', 'fire'))
        else:
            tvx, tvy = mvx * sp, mvy * sp
            if self.run.slow_player > 0:
                tvx *= 0.6; tvy *= 0.6
            a = min(1, dt * (3.5 if getattr(self, 'ice', False) else 14))
            self.vx += (tvx - self.vx) * a
            self.vy += (tvy - self.vy) * a
            vx, vy = self.vx, self.vy
        kx, ky = self.knock
        wx, wy = self.wind
        self.knock = (kx * 0.85, ky * 0.85)
        dx, dy = (vx + kx + wx) * dt, (vy + ky + wy) * dt
        # Tür-Assistent: sanft zur Türmitte lenken
        if self.moving and run.doors_open():
            for d, (px, py) in DOOR_POS.items():
                if d not in run.room.doors or run.door_locked(d):
                    continue
                ddx, ddy = DIRS[d]
                if (mvx * ddx + mvy * ddy) <= 0.3:
                    continue
                if d in 'ns' and abs(self.y - py) < 30 and abs(self.x - px) < 22:
                    dx += clamp(px - self.x, -sp * dt, sp * dt)
                elif d in 'we' and abs(self.x - px) < 30 and abs(self.y - py) < 22:
                    dy += clamp(py - self.y, -sp * dt, sp * dt)
        self.move(dx, dy, fly)
        if self.moving:
            self.flip = mvx < 0 if abs(mvx) > 0.1 else self.flip
            if not fly and random.random() < dt * 9:
                run.particles.append(Particle(self.x + random.uniform(-3, 3), self.y + 4, random.uniform(-10, 10), -8, 0.35,
                                              gfx._c(run.biome['floor'], 1.35), 2))
        # Stacheln
        t, _, _ = tile_at(run.room, self.x, self.y + 3)
        if t == T_SPIKE and not fly and self.dash_t <= 0:
            self.hurt(1, 'Stacheln')
        # Schießen
        sx, sy = inp['shoot']
        if abs(sx) + abs(sy) > 0.1:
            self.facing = norm(sx, sy)
            if abs(sx) > 0.2:
                self.flip = sx < 0
            if self.shoot_cd <= 0 and run.challenge != 'papiermeister':
                self.fire(self.facing)
                self.recoil = 0.08
                wk = weapons.weapon_of(self)
                self.shoot_cd = 1.0 / (self.s['rate'] * sigs.rate_mult(self) * (weapons.RATE[wk] if wk else 1.0))
                run.player_fired = True
        # Begleiter
        self.update_followers(dt, inp)
        sigs.tick(self, run, dt)

    def move(self, dx, dy, fly):
        run = self.run
        room = run.room
        steps = max(1, int(max(abs(dx), abs(dy)) / 4) + 1)
        for _ in range(steps):
            sx, sy = dx / steps, dy / steps
            nx, ny = self.x + sx, self.y + sy
            if not self.collides(nx, self.y, fly):
                self.x = nx
            if not self.collides(self.x, ny, fly):
                self.y = ny

    def collides(self, x, y, fly):
        run = self.run
        r = self.r
        room = run.room
        doors_open = run.doors_open()
        # Tür-Durchgänge
        for d, (px, py) in DOOR_POS.items():
            if d in room.doors and doors_open and not run.door_locked(d):
                if d in 'ns' and abs(x - px) <= 14 - r and (y < RY + r or y > RY + RH - r):
                    if (d == 'n' and y < RY + 8) or (d == 's' and y > RY + RH - 8):
                        return False
                if d in 'we' and abs(y - py) <= 14 - r and (x < RX + r or x > RX + RW - r):
                    if (d == 'w' and x < RX + 8) or (d == 'e' and x > RX + RW - 8):
                        return False
        if x - r < RX or x + r > RX + RW or y - r < RY or y + r > RY + RH:
            return True
        for cx in (x - r, x + r):
            for cy in (y - r + 3, y + r):
                t, _, _ = tile_at(room, cx, cy)
                if t in SOLID_TILES:
                    return True
                if t == T_PIT and not fly:
                    return True
        return False

    def fire(self, d):
        run = self.run
        self.shot_count += 1
        wk = weapons.weapon_of(self)
        if wk and weapons.fire(self, d, wk):
            sigs.on_fire(self, run, [])
            rc = self.f['raijin_chance']
            if rc and random.random() < rc * (1 + self.s['luck'] * 0.08):
                tgt = run.nearest_enemy(self.x, self.y, 400)
                if tgt:
                    run.lightning(tgt.x, tgt.y, self.damage() * 2 + 4)
            return
        n = 1 + int(self.f['multishot'])
        base = math.atan2(d[1], d[0])
        spread = 0.16 if n <= 3 else 0.5 / (n - 1) * 1.6
        dmg = self.damage()
        size = self.s['size']
        big = False
        be = int(self.f['big_every'])
        if be and self.shot_count % be == 0:
            dmg *= 3; size *= 1.8; big = True
        fl = {k: self.f[k] for k in ('homing', 'pierce', 'bounce', 'spectral', 'explode', 'burn', 'slow', 'poison',
                                     'chain', 'split', 'boomerang', 'wave', 'knock') if self.f[k]}
        angs = [base + (i - (n - 1) / 2) * spread for i in range(n)]
        for _ in range(int(self.f['back'])):
            angs.append(base + math.pi)
        for _ in range(int(self.f['side'])):
            angs += [base + math.pi / 2, base - math.pi / 2]
        made = []
        for a in angs:
            b = run.fire_player_bullet(self.x, self.y - 3, a, dmg, self.s['shotspd'], size, self.s['range'] / self.s['shotspd'], fl)
            made.append(b)
            b.big = big
            if self.f['gold_shots'] and random.random() < self.f['gold_shots']:
                b.gold = True
                b.col = (255, 215, 90)
        rc = self.f['raijin_chance']
        if rc and random.random() < rc * (1 + self.s['luck'] * 0.08):
            tgt = run.nearest_enemy(self.x, self.y, 400)
            if tgt:
                run.lightning(tgt.x, tgt.y, dmg * 2 + 4)
        sigs.on_fire(self, run, made)
        audio.play('shoot', 0.6)

    def update_followers(self, dt, inp):
        run = self.run
        # Familiars folgen der Spur
        lx, ly = self.x, self.y
        for i, fm in enumerate(self.familiars):
            tx, ty = lx - self.facing[0] * 0 + math.cos(self.anim * 2 + i * 2.1) * 4, ly + 12
            if i > 0:
                tx, ty = lx, ly + 10
            k = min(1, dt * 7)
            fm.x += (tx - fm.x) * k
            fm.y += (ty - fm.y) * k
            lx, ly = fm.x, fm.y
            fm.cd -= dt
            sx, sy = inp['shoot']
            if (abs(sx) + abs(sy) > 0.1) and fm.cd <= 0:
                herr = 'hyakki_herr' in self.sgs
                fm.cd = 0.3 if herr else 0.6
                a = math.atan2(self.facing[1], self.facing[0])
                fl = {'homing': 1} if (herr or i % 2 == 1 or self.f['homing']) else {}
                run.fire_player_bullet(fm.x, fm.y, a, max(2.5, self.damage() * 0.55), 230, 2.5, 0.9, fl)
        # Orbitale
        self.orb_angle += dt * 3.2
        for k in list(self.orb_hit_cd):
            self.orb_hit_cd[k] -= dt
        # Aura
        if self.f['aura'] and self.aura_cd <= 0:
            self.aura_cd = 0.33
            rad = 30 + 6 * self.f['aura']
            if 'tempelfest' in self.sgs and sigs.st(self).get('glocke', 0) > 0:
                rad *= 2
            for e in run.enemies:
                if e.active() and math.hypot(e.x - self.x, e.y - self.y) < rad + e.r:
                    run.damage_enemy(e, 0.8 * self.f['aura'] + 0.25 * self.damage(), None)

    def orbitals(self):
        n = int(self.f['orbital'])
        out = []
        for i in range(n):
            a = self.orb_angle + i / max(1, n) * math.tau
            rr = 30 if 'riesenmoench' in self.sgs else 21
            out.append((self.x + math.cos(a) * rr, self.y - 3 + math.sin(a) * rr))
        return out

    def draw(self, s, t):
        run = self.run
        dt_ = getattr(run, 'death_t', None)
        if self.dead and dt_ is not None:
            f = 1 - dt_ / 1.6
            if sheets.has(self.char) and sheets.is_hi(self.char):
                key = (self.char, int(min(1, f * 2) * 12))
                cache = Player.__dict__.get('_death_cache')
                if cache is None:
                    cache = {}
                    Player._death_cache = cache
                rot = cache.get(key)
                if rot is None:
                    fr = sheets.frame(self.char, getattr(self, '_last_dir', sheets.RIGHT), 0)
                    rot = pygame.transform.rotate(fr, -90 * key[1] / 12 * (1 if getattr(self, '_last_dir', sheets.RIGHT) == sheets.RIGHT else -1))
                    cache[key] = rot
                gfx.hi_blit(rot, self.x, self.y + 5, int(255 * max(0, 1 - f)))
            else:
                spr = gfx.sprite(self.char, self.flip)
                rot = pygame.transform.rotate(spr, -90 * min(1, f * 2))
                rot.set_alpha(int(255 * max(0, 1 - f)))
                s.blit(rot, (int(self.x) - rot.get_width() // 2, int(self.y) - rot.get_height() + 5))
            gfx.draw_glow(s, int(self.x), int(self.y - 20 * f), 12, (150, 210, 255), int(150 * (1 - f)))
            return
        if self.iframes > 0 and int(t * 20) % 2 == 0 and self.dash_t <= 0:
            vis = False
        else:
            vis = True
        # Aura
        if self.f['aura']:
            rad = int(30 + 6 * self.f['aura'])
            gfx.draw_glow(s, int(self.x), int(self.y), rad, (255, 210, 120), 40)
            pygame.draw.circle(s, (255, 220, 150), (int(self.x), int(self.y)), rad, 1)
        # Schatten
        gfx.shadow(s, (int(self.x) - 8, int(self.y) + 6, 16, 5))
        if vis:
            bob = int(abs(math.sin(self.anim * 9)) * 1.5) if self.moving else 0
            if sheets.has(self.char):
                shooting = getattr(self, 'recoil', 0) > 0 or self.shoot_cd > 0.05
                m = sheets.META[self.char]
                if m['kind'] == 'strip':
                    hx = self.facing[0] if shooting else (self.vx if self.moving else 0)
                    dd = sheets.hdir(hx) if abs(hx) > 0.05 else getattr(self, '_last_dir', sheets.RIGHT)
                    self._last_dir = dd
                    if 'atk' in m and getattr(self, 'recoil', 0) > 0:
                        fr = m['atk'] + 1
                    elif 'atk' in m and self.shoot_cd > 0.12:
                        fr = m['atk'] + 2
                    else:
                        fr = int(self.anim * 8) % 4 if self.moving else 0
                else:
                    if shooting:
                        dd = sheets.dir_from(*self.facing)
                    elif self.moving:
                        dd = sheets.dir_from(self.vx, self.vy)
                    else:
                        dd = getattr(self, '_last_dir', sheets.DOWN)
                    self._last_dir = dd
                    fr = int(self.anim * 9) % 4 if self.moving else 0
                spr = sheets.frame(self.char, dd, fr)
                self._cur_frame = fr
                bob = 0
            else:
                frame = (0, 1, 0, 2)[int(self.anim * 8) % 4] if self.moving and not self.f['fly'] else 0
                spr = gfx.sprite(self.char, self.flip, frame=frame)
            alpha_s = spr
            if 'yurei' in self.transforms or self.char == 'okiku':
                alpha_s = spr.copy()
                alpha_s.set_alpha(190)
            if self.dash_t > 0:
                alpha_s = spr.copy(); alpha_s.set_alpha(150)
            rx = int(-self.facing[0] * 1.5) if self.recoil > 0 else 0
            ry = int(-self.facing[1] * 1.5) if self.recoil > 0 else 0
            if sheets.has(self.char) and sheets.is_hi(self.char):
                al = alpha_s.get_alpha() if alpha_s is not spr and alpha_s.get_alpha() is not None else 255
                fr_right = getattr(self, '_last_dir', None) == sheets.RIGHT
                costume.draw(self, spr, self.x + rx, self.y + 9 - bob + ry, fr_right, t, 'back', al)
                gfx.hi_blit(spr, self.x + rx, self.y + 9 - bob + ry, al)
                costume.draw(self, spr, self.x + rx, self.y + 9 - bob + ry, fr_right, t, 'front', al)
            else:
                s.blit(alpha_s, (int(self.x) - spr.get_width() // 2 + rx, int(self.y) - spr.get_height() + 9 - bob + ry))
        tg = getattr(self, 'transform_glow', 0)
        if tg > 0:
            self.transform_glow = tg - 1 / 60
            col = TRANSFORMS[self.transforms[-1]]['col'] if self.transforms else (255, 255, 255)
            gfx.draw_glow(s, int(self.x), int(self.y) - 8, int(22 + 10 * tg), col, int(80 * min(1, tg)))
        if 'raijin' in self.transforms and random.random() < 0.3:
            run.particles.append(Particle(self.x + random.uniform(-6, 6), self.y - random.uniform(0, 12), 0, -20, 0.2, (255, 240, 120), 1))
        if self.shield_ready:
            pygame.draw.circle(s, (140, 200, 255), (int(self.x), int(self.y) - 3), 10, 1)
        if self.kagura > 0:
            gfx.draw_glow(s, int(self.x), int(self.y) - 4, 18, (255, 220, 120), 90)
        # Familiars
        for i, fm in enumerate(self.familiars):
            fx, fy = int(fm.x), int(fm.y + math.sin(t * 4 + i) * 2)
            pygame.draw.polygon(s, (250, 248, 240), [(fx, fy - 6), (fx + 5, fy - 1), (fx + 3, fy + 5), (fx - 3, fy + 5), (fx - 5, fy - 1)])
            pygame.draw.polygon(s, (30, 20, 30), [(fx, fy - 6), (fx + 5, fy - 1), (fx + 3, fy + 5), (fx - 3, fy + 5), (fx - 5, fy - 1)], 1)
            pygame.draw.circle(s, (220, 40, 40), (fx, fy - 2), 1)
        for ox, oy in self.orbitals():
            gfx.draw_glow(s, int(ox), int(oy), 8, (200, 220, 255), 70)
            pygame.draw.rect(s, (250, 248, 240), (int(ox) - 3, int(oy) - 4, 6, 8))
            pygame.draw.rect(s, (200, 40, 40), (int(ox) - 1, int(oy) - 2, 2, 4))


# =========================================================================  Gefahrenzonen
class Hazard:
    def __init__(self, x, y, r, warn, act, dmg, owner='e', kind='strike', col=None):
        self.x, self.y, self.r = x, y, r
        self.warn, self.act = warn, act
        self.dmg, self.owner, self.kind = dmg, owner, kind
        self.col = col or {'strike': (255, 240, 120), 'fire': (255, 140, 40), 'slam': (230, 220, 200),
                           'ice': (190, 240, 255), 'water': (120, 190, 255), 'meteor': (200, 140, 255),
                           'smoke': (140, 140, 150), 'ink': (60, 20, 40), 'bamboo': (130, 200, 90), 'hands': (160, 70, 110)}.get(kind, (255, 255, 255))
        self.t = 0.0
        self.done = set()
        self.started = False

    def update(self, dt, run):
        self.t += dt
        if self.t < self.warn:
            return True
        if not self.started:
            self.started = True
            if self.kind == 'strike':
                audio.play('thunder', 0.6); run.shake(3)
            elif self.kind in ('slam', 'meteor'):
                audio.play('explode', 0.5); run.shake(4)
                burst(run, self.x, self.y, self.col, 12, 80)
        p = run.player
        if self.kind in ('smoke', 'hands'):
            if math.hypot(p.x - self.x, p.y - self.y) < self.r + p.hitr:
                run.slow_player = max(run.slow_player, 0.3)
            return self.t < self.warn + self.act
        if self.owner == 'e':
            if math.hypot(p.x - self.x, p.y - self.y) < self.r + p.hitr:
                p.hurt(1, getattr(self, 'src', None) or 'eine Falle')
        else:
            tick = int((self.t - self.warn) / 0.3)
            for e in run.enemies:
                key = (id(e), tick)
                if key not in self.done and e.active() and math.hypot(e.x - self.x, e.y - self.y) < self.r + e.r:
                    self.done.add(key)
                    run.damage_enemy(e, self.dmg, None, burn=self.kind == 'fire')
                    if getattr(self, 'sg_conf', False) and not e.is_boss:
                        e.sg_conf = 2.5
        return self.t < self.warn + self.act

    def draw(self, s, tm):
        x, y, r = int(self.x), int(self.y), int(self.r)
        if self.t < self.warn:
            f = self.t / max(0.01, self.warn)
            pygame.draw.circle(s, self.col, (x, y), r, 1)
            pygame.draw.circle(s, self.col, (x, y), max(1, int(r * f)), 1)
        else:
            if self.kind == 'silk':
                f = 1 - (self.t - self.warn) / max(0.01, self.act)
                if f > 0.3:
                    s.set_at((x, y), (230, 240, 255) if f > 0.6 else (150, 170, 210))
                return
            if self.kind == 'smoke':
                f = 1 - (self.t - self.warn) / max(0.01, self.act)
                gfx.draw_glow(s, x, y, int(r * 1.6), (60, 60, 70), int(90 * f))
                return
            if self.kind == 'strike':
                pts = [(x + random.randint(-4, 4), y - 300 + i * 30) for i in range(10)] + [(x, y)]
                pygame.draw.lines(s, (255, 255, 230), False, pts, 2)
                gfx.draw_glow(s, x, y, r * 2, (255, 240, 120), 120)
            elif self.kind == 'bamboo':
                f = min(1, (self.t - self.warn) / 0.12)
                for dx_, hh in ((-5, 16), (0, 22), (5, 13)):
                    h_ = int(hh * f)
                    pygame.draw.rect(s, (40, 70, 34), (x + dx_ - 2, y - h_, 5, h_ + 1))
                    pygame.draw.rect(s, (110, 170, 70), (x + dx_ - 1, y - h_, 3, h_))
                    pygame.draw.line(s, (170, 220, 110), (x + dx_ - 1, y - h_), (x + dx_ - 1, y), 1)
                    for ny_ in range(y - h_ + 6, y, 7):
                        pygame.draw.line(s, (40, 70, 34), (x + dx_ - 1, ny_), (x + dx_ + 1, ny_))
                    if h_ > 2:
                        pygame.draw.polygon(s, (150, 210, 90), [(x + dx_ - 1, y - h_), (x + dx_ + 1, y - h_), (x + dx_, y - h_ - 4)])
            elif self.kind == 'hands':
                pool = pygame.Surface((r * 2 + 4, r + 4), pygame.SRCALPHA)
                pygame.draw.ellipse(pool, (40, 10, 30, 170), pool.get_rect())
                pygame.draw.ellipse(pool, (150, 60, 110, 200), pool.get_rect(), 1)
                s.blit(pool, (x - r - 2, y - r // 2 - 2))
                for k in range(4):
                    a_ = k / 4 * math.tau + 0.6
                    hx, hy = x + int(math.cos(a_) * r * 0.55), y + int(math.sin(a_) * r * 0.3)
                    lift = int(6 + 3 * math.sin(tm * 6 + k))
                    pygame.draw.line(s, (90, 70, 80), (hx, hy), (hx, hy - lift), 3)
                    pygame.draw.line(s, (200, 185, 190), (hx - 1, hy - lift), (hx - 1, hy), 1)
                    for fx_ in (-2, 0, 2):
                        s.set_at((hx + fx_, hy - lift - 2), (220, 205, 210))
                        s.set_at((hx + fx_, hy - lift - 1), (200, 185, 190))
            elif self.kind == 'fire':
                gfx.draw_glow(s, x, y, r + 4, (255, 120, 30), 120)
                for i in range(3):
                    pygame.draw.circle(s, (255, 200, 80), (x + random.randint(-r // 2, r // 2), y + random.randint(-r // 2, r // 2)), 2)
            else:
                gfx.draw_glow(s, x, y, r + 6, self.col, 130)
                pygame.draw.circle(s, self.col, (x, y), r, 2)


# =========================================================================  Yokai
class Enemy:
    is_boss = False

    def __init__(self, run, eid, x, y, champ=None):
        self.run = run
        self.id = eid
        d = ENEMIES[eid]
        if d.get('attack') and d['attack'].get('late') is None and eid == 'onibi' and run.tier < 4:
            d = dict(d, attack=None)                 # Onibi legen erst in den tiefen Kapiteln Feuerspuren
        self.d = d
        self.name = d['name']
        self.x, self.y = x, y
        self.r = d['r']
        if sheets.has(d['sprite']):
            sw, sh = sheets.size_of(d['sprite'])
            self.r = max(self.r, int(min(sw, sh) * 0.3))
        elif d['sprite'] in art.ARTS:
            sp = art.make(d['sprite'])
            self.r = max(self.r, int(min(sp.get_width(), sp.get_height()) * 0.36))
        mult = (1 + 0.3 * (run.tier - 1) + 0.05 * (run.tier - 1) ** 2 + (0.3 if run.depth >= 6 else 0)) * (1.3 if run.hard else 1.0) * run.loop_mult
        self.champ = champ
        cm = CHAMPIONS[champ] if champ else {}
        self.maxhp = self.hp = d['hp'] * mult * cm.get('hp', 1)
        self.speed = d['speed'] * cm.get('speed', 1) * (1.1 if run.hard else 1)
        self.fly = d.get('fly', False) or d['move'] in ('circle', 'bounce')
        self.vx = self.vy = 0.0
        self.kx = self.ky = 0.0
        self.t = random.uniform(0, 3)
        self.spawn_t = 0.55
        self.flash = 0.0
        self.burn = self.poison = self.slowed = self.frozen = 0.0
        self.burn_dps = self.poison_dps = 0.0
        self.dead = False
        self.state = 'idle'
        self.st = random.uniform(0.5, 1.5)
        self.acd = random.uniform(0.8, 2.0)
        self.target = None
        self.flip = False
        self.hidden = False
        self.spawned = []
        a = random.uniform(0, math.tau)
        if d['move'] == 'bounce':
            self.vx, self.vy = math.cos(a) * self.speed, math.sin(a) * self.speed
            if abs(self.vx) < 20: self.vx = 30
            if abs(self.vy) < 20: self.vy = 30
        self.orbit_a = a
        self.charge_dir = None
        self.hop_from = self.hop_to = None
        self.alpha = 255
        self.gold_hit = False
        self.contact = run.enemy_dmg

    def active(self):
        if self.champ == 'geist' and (self.t % 2.4) > 1.6:
            return False
        return not self.dead and self.spawn_t <= 0 and not self.hidden

    def hitboxes(self):
        return ((self.x, self.y, self.r),)

    def update(self, dt):
        run = self.run
        self.t += dt
        self.flash = max(0, self.flash - dt)
        if self.spawn_t > 0:
            self.spawn_t -= dt
            return
        # Statuseffekte
        if self.burn > 0:
            self.burn -= dt
            self.hp -= self.burn_dps * dt
            if random.random() < 0.3:
                run.particles.append(Particle(self.x + random.uniform(-4, 4), self.y - 4, 0, -30, 0.3, (255, 150, 40), 2))
        if self.poison > 0:
            self.poison -= dt
            self.hp -= self.poison_dps * dt
            if random.random() < 0.2:
                run.particles.append(Particle(self.x + random.uniform(-4, 4), self.y - 4, 0, -20, 0.4, (120, 230, 90), 2))
        if self.champ == 'gruen' and self.hp < self.maxhp:
            self.hp = min(self.maxhp, self.hp + self.maxhp * 0.05 * dt)
        if self.hp <= 0:
            run.kill_enemy(self)
            return
        if run.timestop > 0:
            return
        if self.frozen > 0:
            self.frozen -= dt
            return
        if self.slowed > 0:
            self.slowed -= dt
        spd = self.speed * (0.5 if self.slowed > 0 else 1)
        if not sigs.enemy_tick(self, dt):
            self.ai(dt, spd)
        # Rückstoß
        if self.d.get('heavy'):
            self.kx = self.ky = 0
        if abs(self.kx) + abs(self.ky) > 1:
            self.x, self.y, _, _ = move_body(run.room, self.x, self.y, self.r, self.kx * dt, self.ky * dt, self.fly)
            self.kx *= 0.82; self.ky *= 0.82
        # Kontakt
        if not self.hidden:
            p = run.player
            if math.hypot(p.x - self.x, p.y - self.y) < self.r + p.hitr + 1:
                if p.dash_t > 0 and p.f['dash_dmg'] and id(self) not in p.dash_hit:
                    p.dash_hit.add(id(self))
                    run.damage_enemy(self, p.damage() * 2.5, None)
                elif not sigs.contact(p, run, self):
                    p.hurt(self.contact, self.name)

    # -------------------------------------------------------------- KI
    def ai(self, dt, spd):
        run = self.run
        p = run.player
        d = self.d
        mv = d['move']
        dx, dy = p.x - self.x, p.y - self.y
        dist = math.hypot(dx, dy) or 1
        room = run.room
        if mv == 'float':
            wob = math.sin(self.t * 3) * 0.6
            tx, ty = dx / dist, dy / dist
            tx, ty = tx * math.cos(wob) - ty * math.sin(wob), tx * math.sin(wob) + ty * math.cos(wob)
            k = min(1, dt * 2.5)
            self.vx += (tx * spd - self.vx) * k
            self.vy += (ty * spd - self.vy) * k
            self.x, self.y, _, _ = move_body(room, self.x, self.y, self.r, self.vx * dt, self.vy * dt, True)
        elif mv == 'chase':
            tx, ty = run.flow_dir(self.x, self.y)
            if d.get('erratic'):
                ang = math.atan2(ty, tx) + math.sin(self.t * 7) * 0.9
                tx, ty = math.cos(ang), math.sin(ang)
            self.x, self.y, _, _ = move_body(room, self.x, self.y, self.r, tx * spd * dt, ty * spd * dt, self.fly)
            self.vx = tx
        elif mv == 'wander' or mv == 'side':
            self.st -= dt
            if self.target is None or self.st <= 0:
                if mv == 'side':
                    self.target = (clamp(self.x + random.choice([-1, 1]) * random.uniform(50, 140), RX + 20, RX + RW - 20),
                                   clamp(self.y + random.uniform(-30, 30), RY + 20, RY + RH - 20))
                else:
                    self.target = free_tile_pos(room, random)
                self.st = random.uniform(1.2, 2.6)
            tx, ty = norm(self.target[0] - self.x, self.target[1] - self.y)
            if math.hypot(self.target[0] - self.x, self.target[1] - self.y) < 4:
                tx = ty = 0
            self.x, self.y, bx, by = move_body(room, self.x, self.y, self.r, tx * spd * dt, ty * spd * dt, self.fly)
            if bx or by:
                self.target = None
            self.vx = tx
        elif mv == 'hop':
            if self.state == 'idle':
                self.st -= dt
                if self.st <= 0:
                    self.state = 'hop'
                    self.hop_from = (self.x, self.y)
                    tx, ty = norm(dx, dy)
                    L = min(dist, 70)
                    self.hop_to = (self.x + tx * L, self.y + ty * L)
                    self.st = 0.0
            else:
                self.st += dt
                f = min(1, self.st / 0.45)
                nx = self.hop_from[0] + (self.hop_to[0] - self.hop_from[0]) * f
                ny = self.hop_from[1] + (self.hop_to[1] - self.hop_from[1]) * f
                self.x, self.y, _, _ = move_body(room, self.x, self.y, self.r, nx - self.x, ny - self.y, True)
                if f >= 1:
                    self.state = 'idle'
                    self.st = random.uniform(0.5, 1.0)
                    t, _, _ = tile_at(room, self.x, self.y)
                    if t == T_PIT:
                        self.x, self.y = self.hop_from
            self.vx = dx
        elif mv == 'charge':
            if self.state == 'charge':
                cs = spd * (6.5 if d.get('fast_charge') else 4.2)
                self.x, self.y, bx, by = move_body(room, self.x, self.y, self.r, self.charge_dir[0] * cs * dt,
                                                   self.charge_dir[1] * cs * dt, self.fly)
                self.st -= dt
                if bx or by or self.st <= 0:
                    self.state = 'stun'
                    self.st = 0.6
                    if bx or by:
                        run.shake(1)
                    if d.get('charge_ring'):
                        n = d['charge_ring']
                        for i in range(n):
                            ebullet(run, self.x, self.y, i / n * math.tau, 85, (230, 230, 230))
                if random.random() < 0.5:
                    run.particles.append(Particle(self.x, self.y + 4, 0, 0, 0.3, (200, 190, 170), 2))
            elif self.state == 'stun':
                self.st -= dt
                if self.st <= 0:
                    self.state = 'idle'
            elif self.state == 'wind':
                self.st -= dt
                if self.st <= 0:
                    self.state = 'charge'
                    self.st = 1.6
            else:
                aligned = abs(dx) < 10 or abs(dy) < 10
                if aligned and dist < 240:
                    self.state = 'wind'
                    self.st = 0.25
                    self.charge_dir = (math.copysign(1, dx), 0) if abs(dx) > abs(dy) else (0, math.copysign(1, dy))
                    self.vx = self.charge_dir[0] or self.vx
                else:
                    tx, ty = run.flow_dir(self.x, self.y)
                    self.x, self.y, _, _ = move_body(room, self.x, self.y, self.r, tx * spd * 0.6 * dt, ty * spd * 0.6 * dt, self.fly)
                    self.vx = tx
        elif mv == 'teleport':
            self.st -= dt
            if self.state == 'idle' and self.st <= 0:
                self.state = 'fade'
                self.st = 0.3
            elif self.state == 'fade':
                self.alpha = int(255 * max(0, self.st / 0.3))
                if self.st <= 0:
                    self.x, self.y = free_tile_pos(room, random, (p.x, p.y), 95)
                    self.state = 'appear'
                    self.st = 0.3
            elif self.state == 'appear':
                self.alpha = int(255 * (1 - max(0, self.st / 0.3)))
                if self.st <= 0:
                    self.alpha = 255
                    self.state = 'idle'
                    self.st = random.uniform(2.0, 3.2)
                    self.acd = max(0.6, min(self.acd, 0.8))
            self.vx = dx
        elif mv == 'zigzag':
            base = math.atan2(dy, dx) + (0.9 if int(self.t * 1.5) % 2 else -0.9)
            self.x, self.y, bx, by = move_body(room, self.x, self.y, self.r, math.cos(base) * spd * dt, math.sin(base) * spd * dt, self.fly)
            self.vx = dx
        elif mv == 'drop':
            self.st -= dt
            if self.state in ('idle', 'up'):
                self.state = 'up'
                self.hidden = True
                if self.st <= 0:
                    self.state = 'falling'
                    self.st = 0.8
                    self.x, self.y = p.x, p.y
            elif self.state == 'falling':
                if self.st <= 0:
                    self.hidden = False
                    self.state = 'down'
                    self.st = 1.8
                    run.shake(3)
                    self.ring_wait = 0.4                     # kurzes Aufblitzen, dann erst der Ring
            elif self.state == 'down':
                rw = getattr(self, 'ring_wait', 0)
                if rw > 0:
                    self.ring_wait = rw - dt
                    self.flash = 0.06 if int(rw * 20) % 2 else 0
                    if self.ring_wait <= 0:
                        self.do_attack(force=True)
                if self.st <= 0:
                    self.state = 'up'
                    self.st = random.uniform(1.0, 2.0)
        elif mv == 'bounce':
            sp = math.hypot(self.vx, self.vy) or 1
            f = spd / sp
            self.x, self.y, bx, by = move_body(room, self.x, self.y, self.r, self.vx * f * dt, self.vy * f * dt, True)
            if bx:
                self.vx = -self.vx
            if by:
                self.vy = -self.vy
        elif mv == 'circle':
            self.orbit_a += dt * spd / 70
            tx, ty = p.x + math.cos(self.orbit_a) * 75, p.y + math.sin(self.orbit_a) * 60
            vx, vy = norm(tx - self.x, ty - self.y)
            self.x, self.y, _, _ = move_body(room, self.x, self.y, self.r, vx * spd * 1.3 * dt, vy * spd * 1.3 * dt, True)
            self.vx = dx
        elif mv == 'burrow':
            self.st -= dt
            if self.state in ('idle', 'under'):
                self.state = 'under'
                self.hidden = True
                tx, ty = norm(dx, dy)
                self.x, self.y, _, _ = move_body(room, self.x, self.y, self.r, tx * spd * 1.2 * dt, ty * spd * 1.2 * dt, True)
                if random.random() < 0.4:
                    run.particles.append(Particle(self.x + random.uniform(-5, 5), self.y + 3, 0, -15, 0.4, (150, 140, 120), 2))
                if self.st <= 0 or dist < 30:
                    t, _, _ = tile_at(room, self.x, self.y)
                    if t not in SOLID_TILES and t != T_PIT:
                        self.state = 'emerge'
                        self.st = 0.45
            elif self.state == 'emerge':
                if self.st <= 0:
                    self.hidden = False
                    self.state = 'up'
                    self.st = 1.6
                    self.do_attack(force=True)
                    audio.play('splash', 1.0, self.x)
            elif self.state == 'up':
                if self.st <= 0:
                    self.state = 'under'
                    self.st = random.uniform(1.6, 2.4)
        # Angriff
        if d['attack'] and not self.hidden:
            self.do_attack(dt=dt)

    def do_attack(self, dt=0.0, force=False):
        run = self.run
        a = self.d['attack']
        p = run.player
        if not force and sigs.no_attack(self):
            return
        if a['kind'] == 'mirror':
            self.acd -= dt
            if run.player_fired and self.acd <= 0:
                self.acd = a['cd']
                ang = math.atan2(p.y - self.y, p.x - self.x)
                ebullet(run, self.x, self.y, ang, a['speed'], a['col'])
            return
        fire = 1.6 if self.champ == 'blau' else 1.0
        if not force:
            self.acd -= dt * fire
            if self.acd > 0:
                return
            if self.d['move'] == 'teleport' and self.state != 'idle':
                return
            if self.d['move'] == 'charge' and self.state != 'idle':
                return
        self.acd = a['cd'] * random.uniform(0.85, 1.15) * max(0.7, 1 - 0.06 * (self.run.tier - 1))
        self.fire_t = self.t
        audio.play('eshot', 0.45, self.x)
        sp = a['speed'] * (1.15 if self.champ == 'blau' else 1.0)
        k = a['kind']
        ang = math.atan2(p.y - self.y, p.x - self.x)
        if k == 'aimed':
            n = a['n']
            for i in range(n):
                ebullet(self.run, self.x, self.y, ang + (i - (n - 1) / 2) * a['spread'], sp, a['col'], eff=a['eff'])
        elif k == 'ring':
            n = a['n']
            off = random.uniform(0, math.tau)
            for i in range(n):
                ebullet(self.run, self.x, self.y, off + i / n * math.tau, sp, a['col'], eff=a['eff'])
                if a.get('double'):
                    ebullet(self.run, self.x, self.y, off + (i + 0.5) / n * math.tau, sp * 0.75, a['col'], eff=a['eff'], delay=0.35)
        elif k == 'cross':
            off = 0 if int(self.t * 10) % 2 else math.pi / 4
            for i in range(4):
                ebullet(self.run, self.x, self.y, off + i * math.pi / 2, sp, a['col'])
        elif k == 'spiral':
            for i in range(14):
                for j in range(a['n']):
                    ebullet(self.run, self.x, self.y, self.t + i * 0.45 + j / a['n'] * math.tau, sp, a['col'], delay=i * 0.08)
        elif k == 'trail':
            if a.get('smoke'):
                run.hazards.append(Hazard(self.x, self.y, 12, 0.0, 2.5, 0, 'e', 'smoke'))
            else:
                run.hazards.append(Hazard(self.x, self.y + 2, 8, 0.25, 1.8, 1, 'e', 'fire'))
        elif k == 'spawn':
            alive = [s for s in self.spawned if not s.dead]
            self.spawned = alive
            if len(alive) < a['max'] and len(run.enemies) < 22:
                e = run.spawn_enemy(a['what'], self.x + random.uniform(-10, 10), self.y + 8)
                e.spawn_t = 0.2
                self.spawned.append(e)

    def anim_frame(self, name):
        """Wählt Lauf- oder Angriffsbild (Ausholen vor dem Schuss, Zuschlagen, Zurückziehen)."""
        m = sheets.META.get(name, {})
        atk = m.get('atk')
        if atk is not None:
            if self.state == 'wind':
                return atk
            if self.state == 'charge':
                return atk + 1
            since = self.t - getattr(self, 'fire_t', -9)
            if since < 0.14:
                return atk + 1
            if since < 0.32:
                return atk + 2
            a = self.d.get('attack') or {}
            if a.get('kind') not in (None, 'mirror') and 0 < getattr(self, 'acd', 9) < 0.3:
                return atk
            return int(self.t * 8) % m.get('walk', 4)
        return int(self.t * (12 if self.state == 'charge' else 6))

    def draw(self, s, t):
        spawn_alpha = 255
        if self.spawn_t > 0:
            f = 1 - self.spawn_t / 0.55
            x0, y0 = int(self.x), int(self.y) + self.r - 2
            gfx.draw_glow(s, x0, y0 - 4, 16, (150, 90, 255), int(90 * (1 - f) + 20))
            rr = 4 + f * 10                                          # Beschwörungskreis am Boden
            pygame.draw.ellipse(s, (120, 70, 210), (x0 - rr, y0 - rr * 0.4, rr * 2, rr * 0.8), 1)
            if rr > 6:
                pygame.draw.ellipse(s, (200, 160, 255), (x0 - rr + 3, y0 - rr * 0.4 + 1, rr * 2 - 6, rr * 0.8 - 2), 1)
            for i in range(5):                                       # aufsteigende Geisterfunken
                a = i / 5 * math.tau + f * 3
                px_ = x0 + math.cos(a) * rr * 0.8
                py_ = y0 - f * 16 - (i % 2) * 4
                s.set_at((int(px_), int(py_)), (230, 210, 255))
            if f < 0.45:
                return
            spawn_alpha = int(255 * min(1, (f - 0.45) / 0.45))
        if self.hidden:
            if self.state == 'falling':
                f = 1 - self.st / 0.8
                gfx.shadow(s, (int(self.x) - int(4 + 8 * f), int(self.y) + 4, int(8 + 16 * f), int(3 + 4 * f)), 120)
                return
            if self.state == 'up':
                return
            if self.state == 'emerge':
                pygame.draw.circle(s, (120, 110, 90), (int(self.x), int(self.y)), 7, 2)
            else:
                pygame.draw.ellipse(s, (80, 70, 60), (int(self.x) - 6, int(self.y), 12, 4))
            return
        g = self.d.get('glow')
        if g:
            gfx.draw_glow(s, int(self.x), int(self.y), 14, g, 70)
        tint = CHAMPIONS[self.champ]['col'] if self.champ else None
        if self.frozen > 0:
            tint = (170, 220, 255)
        flip = self.vx < 0
        frame = 0
        name = self.d['sprite']
        if sheets.has(name):
            p = self.run.player
            if self.d['move'] == 'charge' and self.state in ('charge', 'wind') and self.charge_dir:
                dd = sheets.dir_from(*self.charge_dir)
            else:
                dd = sheets.dir_from(p.x - self.x, p.y - self.y)
            if sheets.META[name]['kind'] == 'strip':
                dd = sheets.hdir((self.charge_dir[0] if self.d['move'] == 'charge' and self.state in ('charge', 'wind') and self.charge_dir else p.x - self.x))
            sc = sheets.scale_of(name) + (1 if getattr(self, 'mini', False) else 0)
            spr = sheets.frame(name, dd, self.anim_frame(name), sc, self.flash > 0, tint)
        else:
            if not self.fly and self.d['move'] in ('chase', 'wander', 'side', 'charge'):
                frame = (0, 1, 0, 2)[int(self.t * (14 if self.state == 'charge' else 7)) % 4]
            spr = gfx.sprite(name, flip, self.flash > 0, tint, frame=frame, scale=2 if getattr(self, 'mini', False) else 1)
        if getattr(self, 'mini', False):
            gfx.draw_glow(s, int(self.x), int(self.y), 26, (255, 80, 80), 50)
        bob = 0
        if self.fly:
            bob = int(math.sin(self.t * 4) * 2)
        elif self.d['move'] == 'hop' and self.state == 'hop':
            bob = int(math.sin(min(1, self.st / 0.45) * math.pi) * 14)
        gfx.shadow(s, (int(self.x) - self.r, int(self.y) + self.r - 3, self.r * 2, 4))
        alpha = self.alpha
        if self.champ == 'geist':
            ph = self.t % 2.4
            alpha = 60 if ph > 1.6 else 230
        alpha = min(alpha, spawn_alpha)
        hi = sheets.has(name) and sheets.is_hi(name)
        if self.state == 'wind' and int(t * 30) % 2:
            if hi:
                spr = gfx.tinted(spr, 'white')
            else:
                spr = spr.copy()
                spr.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
        if alpha < 255 and not hi:
            spr = spr.copy(); spr.set_alpha(alpha)
        hh = spr.get_height()
        if hi:
            hh //= 2
            gfx.hi_blit(spr, self.x, self.y + hh / 2 - bob - 2, alpha)
        else:
            s.blit(spr, (int(self.x) - spr.get_width() // 2, int(self.y) - spr.get_height() // 2 - bob - 2))
        if self.champ:
            pygame.draw.circle(s, CHAMPIONS[self.champ]['col'], (int(self.x), int(self.y) - hh // 2 - 5 - bob), 2)
        a = self.d.get('attack')
        if a and a['kind'] in ('aimed', 'ring', 'cross', 'spiral') and 0 < self.acd < 0.32 and self.d['move'] not in ('burrow', 'drop'):
            gfx.draw_glow(s, int(self.x), int(self.y) - 2, self.r + 8, (255, 70, 60), int(160 * (1 - self.acd / 0.32)))


# =========================================================================  Pickups & Objekte
class Pickup:
    def __init__(self, kind, x, y, price=0, pop=True):
        self.kind = kind
        self.x, self.y = x, y
        a = random.uniform(0, math.tau)
        v = random.uniform(30, 80) if pop else 0
        self.vx, self.vy = math.cos(a) * v, math.sin(a) * v
        self.price = price
        self.t = random.uniform(0, 3)
        self.age = 0.0
        self.r = 6

    def update(self, dt, run):
        self.t += dt
        self.age += dt
        if abs(self.vx) + abs(self.vy) > 1:
            self.x, self.y, bx, by = move_body(run.room, self.x, self.y, 5, self.vx * dt, self.vy * dt, False)
            if bx: self.vx = -self.vx
            if by: self.vy = -self.vy
            self.vx *= 0.9; self.vy *= 0.9
        if run.player.f['magnet'] and self.kind in ('coin', 'coin5', 'key') and not self.price:
            p = run.player
            d = math.hypot(p.x - self.x, p.y - self.y)
            if d < 110:
                nx, ny = norm(p.x - self.x, p.y - self.y)
                self.x += nx * 120 * dt; self.y += ny * 120 * dt

    def draw(self, s, t):
        x, y = int(self.x), int(self.y + math.sin(self.t * 3) * 1.5)
        D = pygame.draw
        gfx.shadow(s, (x - 5, int(self.y) + 4, 10, 3))
        k = self.kind
        hi = gfx.item_img('pickups', 'soul' if k == 'spirit' else k, int(self.t * 3) % 2)
        if hi is not None:
            if k in ('heart', 'half', 'spirit', 'salt', 'battery'):
                col = {'spirit': (90, 140, 255), 'salt': (200, 220, 255), 'battery': (120, 200, 255)}.get(k, (255, 60, 80))
                gfx.draw_glow(s, x, y - 1, 9, col, int(40 + 35 * math.sin(self.t * 5)))
            gfx.hi_blit(hi, x, y + 8)
            k = None
        if k is None:
            pass
        elif k in ('heart', 'half'):
            gfx.draw_glow(s, x, y - 1, 9, (255, 60, 80), int(40 + 35 * math.sin(self.t * 5)))
            gfx.heart(s, x - 4, y - 5, 'red', 2 if k == 'heart' else 1)
        elif k == 'spirit':
            gfx.draw_glow(s, x, y - 1, 9, (90, 140, 255), int(40 + 35 * math.sin(self.t * 5)))
            gfx.heart(s, x - 4, y - 5, 'spirit', 2)
        elif k in ('coin', 'coin5'):
            c = (232, 190, 70) if k == 'coin' else (200, 210, 230)
            D.circle(s, (40, 26, 10), (x, y), 5)
            D.circle(s, c, (x, y), 4)
            D.rect(s, (60, 40, 20), (x - 1, y - 1, 3, 3))
            if int(self.t * 3) % 3 == 0:
                s.set_at((x - 2, y - 2), (255, 255, 255))
        elif k == 'key':
            D.circle(s, (30, 20, 10), (x - 3, y), 4)
            D.circle(s, (250, 210, 90), (x - 3, y), 3)
            D.circle(s, (30, 20, 10), (x - 3, y), 1)
            D.rect(s, (250, 210, 90), (x, y - 1, 7, 2))
            D.rect(s, (250, 210, 90), (x + 4, y, 2, 3))
        elif k == 'salt':
            D.polygon(s, (230, 200, 160), [(x - 6, y + 3), (x + 6, y + 3), (x + 4, y - 1), (x - 4, y - 1)])
            D.polygon(s, (250, 250, 255), [(x - 4, y), (x + 4, y), (x, y - 6)])
            gfx.draw_glow(s, x, y - 2, 8, (200, 220, 255), 50)
        elif k == 'chest':
            D.rect(s, (30, 10, 10), (x - 9, y - 6, 18, 13))
            D.rect(s, (180, 40, 40), (x - 8, y - 5, 16, 11))
            D.rect(s, (130, 20, 30), (x - 8, y - 5, 16, 4))
            D.rect(s, (240, 200, 90), (x - 2, y - 2, 4, 4))
        elif k == 'trinket':
            tr = TRINKETS[self.tid]
            gfx.draw_glow(s, x, y, 10, tr['col'], 60)
            D.line(s, (230, 60, 60), (x, y - 10), (x, y - 6), 1)
            gfx.draw_icon(s, tr['icon'], tr['col'], x, y)
        elif k == 'battery':
            D.rect(s, (40, 30, 30), (x - 4, y - 7, 9, 14))
            D.rect(s, (250, 240, 220), (x - 3, y - 6, 7, 12))
            D.line(s, (220, 40, 40), (x - 1, y - 4), (x + 2, y), 2)
            D.line(s, (220, 40, 40), (x + 2, y), (x - 1, y + 4), 2)
        if self.price:
            gfx.TEXT.add('%d' % self.price, x, y + 7, 7, (255, 230, 120), 'c')


class Pedestal:
    """Item auf einem Holzsockel (Schatzraum, Laden, Boss, Schrein)."""

    def __init__(self, item, x, y, price=0, hearts=0, group=None):
        self.item = item       # Item-ID oder 'active:<id>'
        self.x, self.y = x, y
        self.price = price
        self.hearts = hearts
        self.group = group
        self.t = random.uniform(0, 3)
        self.cool = 0.6
        self.r = 8
        self.taken = False

    def fxinfo(self):
        from .texts import fx_lines
        if self.item.startswith('active:'):
            a = ACTIVES[self.item[7:]]
            return 'Aktives Item (Taste E) – lädt sich in %d Räumen auf' % a['charge']
        return ', '.join(fx_lines(ITEMS[self.item]['fx']))

    def info(self):
        if self.item.startswith('active:'):
            a = ACTIVES[self.item[7:]]
            return a['name'], a['desc'], a['icon'], a['col']
        it = ITEMS[self.item]
        return it['name'], it['desc'], it['icon'], it['col']

    def draw(self, s, t):
        x, y = int(self.x), int(self.y)
        D = pygame.draw
        img = props.pedestal_hi(self.taken)
        gfx.hi_blit(img, x, y - 3 + img.get_height() / 2)
        if self.taken:
            return
        name, desc, icon, col = self.info()
        bob = math.sin(self.t * 2.5) * 2
        gfx.draw_glow(s, x, int(y - 10 + bob), 14, col, 60)
        gfx.draw_icon(s, icon, col, x, y - 10 + bob)
        if self.item.startswith('active:'):
            D.rect(s, (255, 240, 150), (x - 10, int(y - 20 + bob), 20, 20), 1)
        if self.price:
            gfx.TEXT.add('%d Mon' % self.price, x, y + 13, 7, (255, 230, 120), 'c')
        if self.hearts:
            gfx.TEXT.add('-%d Herz' % self.hearts if self.hearts < 99 else '-3 Geist', x, y + 13, 7, (255, 110, 110), 'c')


_OBJ_HI = {}


class Obj:
    """Interaktive Objekte: Saisen-Kasten, Omikuji, Onsen, Torii-Ausgang, Schrein-Portal."""

    def __init__(self, kind, x, y, **kw):
        self.kind = kind
        self.x, self.y = x, y
        self.t = 0.0
        self.cool = 0.5
        self.data = kw
        self.r = 12
        self.used = False

    def draw(self, s, t):
        x, y = int(self.x), int(self.y)
        D = pygame.draw
        k = self.kind
        if k == 'tanuki':
            run = self.data.get('run')
            pl = run.player if run else None
            last = self.data.get('coins')
            if pl is not None:
                if last is not None and pl.coins < last:
                    self.data['say'] = (random.choice(['Maido ari!', 'Danke sehr!', 'Gute Wahl!']), self.t + 1.6)
                self.data['coins'] = pl.coins
            bob = 1 if int(self.t * 2) % 2 else 0
            if sheets.has('ponpoko'):
                spr = sheets.frame('ponpoko', sheets.RIGHT if pl is not None and pl.x > x else sheets.LEFT, 0)
                gfx.hi_blit(spr, x, y + 9 - bob)
            gfx.hi_blit(props.counter(), x, y + 14)
            say = self.data.get('say')
            if say and self.t < say[1]:
                txt = say[0]
            elif pl is not None and math.hypot(pl.x - x, pl.y - y) < 80:
                txt = 'Irasshai!'
            else:
                txt = None
            if txt:
                gfx.TEXT.add(txt, x, y - 40 - bob, 7, (255, 240, 200), 'c')
            return
        def put(img, bottom):
            hi = _OBJ_HI.get(id(img))                  # Requisiten auf der Hi-Res-Ebene (Scale2x, geglättete Kanten)
            if hi is None or hi[0] is not img:
                hi = _OBJ_HI[id(img)] = (img, gfx.scale2x(img))
            gfx.hi_blit(hi[1], x, bottom)
        if k == 'saisen':
            put(props.saisen(), y + 8)
            gfx.TEXT.add('Saisen', x, y + 9, 6, (230, 210, 170), 'c')
        elif k == 'omikuji':
            put(props.omikuji(), y + 9)
            gfx.TEXT.add('Omikuji 5 Mon', x, y + 10, 6, (230, 210, 170), 'c')
        elif k == 'onsen':
            put(props.onsen(self.used), y + 16)
            if not self.used:
                for i in range(3):
                    yy = y - 8 - ((t * 20 + i * 9) % 26)
                    a_ = 1 - ((t * 20 + i * 9) % 26) / 26
                    c_ = int(170 + 70 * a_)
                    D.circle(s, (c_, c_, min(255, c_ + 8)), (x - 10 + i * 10 + int(math.sin(t * 2 + i) * 3), int(yy)), 2 if a_ > 0.4 else 1)
        elif k in ('torii', 'heaven', 'victory'):
            col = {'torii': (196, 46, 38), 'heaven': (226, 190, 96), 'victory': (236, 234, 228)}[k]
            gfx.draw_glow(s, x, y - 8, 26, col, 70)
            pr = pygame.Surface((22, 20), pygame.SRCALPHA)       # schimmerndes Portal zwischen den Pfeilern
            for i in range(20):
                f_ = 0.5 + 0.5 * math.sin(t * 3 + i * 0.5)
                pr.fill((int(20 + 40 * f_ * (col[0] / 255)), int(10 + 30 * f_ * (col[1] / 255)), int(24 + 40 * f_ * (col[2] / 255))), (0, i, 22, 1))
            s.blit(pr, (x - 11, y - 16))
            put(props.torii(col), y + 5)
            txt = {'torii': 'Tiefer hinab', 'heaven': 'Aufstieg nach Takamagahara', 'victory': 'Die Reise beenden'}[k]
            gfx.TEXT.add(txt, x, y + 8, 6, (255, 240, 200), 'c')
        elif k == 'shrine':
            oni = self.data.get('oni')
            col = (200, 40, 50) if oni else (250, 230, 150)
            gfx.draw_glow(s, x, y - 6, 22, col, 90)
            put(props.hokora(bool(oni)), y + 6)
            gfx.TEXT.add('Oni-Schrein' if oni else 'Kami-Schrein', x, y + 8, 6, col, 'c')
        elif k == 'ema':
            col = tuple(self.data['col'])
            if not self.used:
                gfx.draw_glow(s, x, y - 8, 16, col, 50)
            put(props.ema(col, self.used), y + 4 + (int(math.sin(t * 2 + x) * 1.2) if not self.used else 0))
            if not self.used:
                gfx.TEXT.add(self.data['name'], x, y + 7, 6, (240, 225, 190), 'c')
                gfx.TEXT.add(self.data['desc'], x, y + 15, 6, col, 'c')
        elif k == 'tea':
            nm, price, col = self.data['name'], self.data['price'], self.data['col']
            put(props.tea_bench(), y + 8)
            if not self.used:
                put(props.tea_cup(tuple(col)), y - 1)
                for i in range(2):
                    yy = y - 6 - ((t * 12 + i * 6) % 12)
                    s.set_at((x - 1 + i * 2 + int(math.sin(t * 3 + i)), int(yy)), (220, 220, 230))
                gfx.TEXT.add(nm, x, y + 10, 6, (240, 225, 190), 'c')
                gfx.TEXT.add('%d Mon' % price, x, y + 18, 6, (255, 230, 120), 'c')
        elif k == 'slots':
            put(props.slots_cab(), y + 11)
            icons = ['coin', 'leaf', 'heart', 'flame', 'star']
            for i in range(3):
                ic = icons[int((t * 12 if self.cool > 0.3 else 0) + i * 2 + self.data.get('res', 0)) % len(icons)]
                D.circle(s, {'coin': (230, 190, 70), 'leaf': (90, 170, 80), 'heart': (220, 50, 60), 'flame': (255, 140, 40), 'star': (250, 230, 120)}[ic],
                         (x - 6 + i * 6, y - 8), 2)
            gfx.TEXT.add('Tanuki-Automat 3 Mon', x, y + 12, 6, (240, 225, 190), 'c')
        elif k == 'back':
            put(props.stairs_up(), y + 10)
            gfx.TEXT.add('Zurück', x, y + 12, 6, (230, 210, 170), 'c')
