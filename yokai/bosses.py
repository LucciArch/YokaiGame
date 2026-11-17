"""Die 16 Bosse – jeder mit eigenen Angriffsmustern (als Koroutinen geschrieben)."""
import math
import random
import pygame
from .settings import *
from . import gfx, audio, art, sheets
from .data import BOSSES
from .entities import Enemy, ebullet, Hazard, Particle, burst, move_body, norm, clamp, free_tile_pos

CX, CY = RX + RW / 2, RY + RH / 2


class Boss(Enemy):
    is_boss = True
    r = 14

    def __init__(self, run, bid, x, y):
        self.run = run
        self.id = bid
        self.d = {'move': 'boss', 'attack': None, 'sprite': None}
        info = BOSSES[bid]
        self.name = info['name']
        self.title = info['title']
        self.x, self.y = x, y
        hpm = (1.3 if run.hard else 1.0) * (1 + 0.3 * (run.tier - 1) + 0.07 * (run.tier - 1) ** 2) * run.loop_mult
        self.maxhp = self.hp = info['hp'] * hpm
        self.speed = 60
        self.fly = True
        self.vx = self.vy = 0.0
        self.kx = self.ky = 0.0
        self.t = 0.0
        self.spawn_t = 1.2
        self.flash = 0.0
        self.burn = self.poison = self.slowed = self.frozen = 0.0
        self.burn_dps = self.poison_dps = 0.0
        self.dead = False
        self.hidden = False
        self.champ = None
        self.state = 'idle'
        self.alpha = 255
        self.spawned = []
        self.co = None
        self.wait = 0.0
        self.idle = 1.0
        self.phase = 1
        self.last = None
        self.contact = 1 if run.depth <= 2 or run.relaxed else 2
        self.invuln = False
        self.attacks = ['ring']
        self.attacks2 = None
        self.rest = 0.9
        self.divine = run.depth >= 6
        self._budget = self.maxhp * self.SEC_CAP
        self.ward_t = 0.0
        self.setup()
        if self.sheet:
            try:
                ww, hh = sheets.size_of(self.sheet[0])
                ww, hh = ww * self.sheet[1], hh * self.sheet[1]
                self.r = max(self.r, int(min(ww, hh) * 0.36))
            except Exception:
                pass

    def setup(self):
        pass

    # ------------------------------------------------------------ Göttlicher Schutz
    # Endbosse (ab Kapitel VI) nehmen pro Treffer höchstens 2 % und pro Sekunde höchstens 8 % ihrer Max-HP.
    HIT_CAP, SEC_CAP = 0.02, 0.08
    P2 = 0.5            # Lebensanteil, ab dem Phase 2 beginnt
    extra_dark = 0      # zusätzliche Dunkelheit im Bossraum (Izanami in Yomi)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, v):
        old = getattr(self, '_hp', None)
        if old is not None and v < old and getattr(self, 'divine', False):
            loss = min(old - v, self.maxhp * self.HIT_CAP, max(0.0, self._budget))
            if loss < old - v - 0.01:
                self.ward_t = 0.8
            self._budget -= loss
            v = old - loss
        self._hp = v

    # ------------------------------------------------------------ Hilfen
    @property
    def p(self):
        return self.run.player

    def ang_p(self, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        return math.atan2(self.p.y - y, self.p.x - x)

    def af(self, name, t, speed=7, off=0):
        """Animationsbild: Laufschleife, nach einem Schuss Zuschlagen/Zurückziehen."""
        m = sheets.META.get(name, {})
        atk = m.get('atk')
        if atk is None:
            return int(t * speed) + off
        since = self.t - getattr(self, 'fire_t', -9)
        if since < 0.16:
            return atk + 1
        if since < 0.42:
            return atk + 2
        if 0 < getattr(self, 'wait', 0) < 0.25 and getattr(self, 'co', None) is not None:
            return atk
        return (int(t * speed) + off) % m.get('walk', 4)

    def ring(self, n, sp, off=0.0, col=(240, 80, 120), x=None, y=None, r=3, **kw):
        self.fire_t = self.t
        audio.play('eshot', 0.7)
        x = self.x if x is None else x
        y = self.y if y is None else y
        for i in range(n):
            ebullet(self.run, x, y, off + i / n * math.tau, sp, col, r, **kw)

    def fan(self, n, spread, sp, col=(240, 80, 120), x=None, y=None, ang=None, r=3, **kw):
        self.fire_t = self.t
        audio.play('eshot', 0.7)
        x = self.x if x is None else x
        y = self.y if y is None else y
        a0 = self.ang_p(x, y) if ang is None else ang
        for i in range(n):
            a = a0 + ((i - (n - 1) / 2) * spread if n > 1 else 0)
            ebullet(self.run, x, y, a, sp, col, r, **kw)

    def summon(self, eid, n, spread=20):
        made = []
        for _ in range(n):
            if len(self.run.enemies) > 16:
                break
            x = clamp(self.x + random.uniform(-spread, spread), RX + 16, RX + RW - 16)
            y = clamp(self.y + random.uniform(-spread, spread), RY + 16, RY + RH - 16)
            e = self.run.spawn_enemy(eid, x, y)
            made.append(e)
        return made

    def hazard(self, x, y, r, warn=0.8, act=0.2, kind='strike'):
        self.run.hazards.append(Hazard(x, y, r, warn, act, 1, 'e', kind))

    def goto(self, tx, ty, sp, dt):
        dx, dy = tx - self.x, ty - self.y
        d = math.hypot(dx, dy)
        if d < 1:
            return True
        st = min(d, sp * dt)
        self.x += dx / d * st
        self.y += dy / d * st
        return d < 3

    def clamp_pos(self, m=None):
        m = self.r if m is None else m
        self.x = clamp(self.x, RX + m, RX + RW - m)
        self.y = clamp(self.y, RY + m, RY + RH - m)

    # ------------------------------------------------------------ Update
    def active(self):
        return not self.dead and self.spawn_t <= 0 and not self.hidden and not self.invuln

    def update(self, dt):
        run = self.run
        self.t += dt
        self.flash = max(0, self.flash - dt)
        self.ward_t = max(0.0, self.ward_t - dt)
        self._budget = min(self.maxhp * self.SEC_CAP, self._budget + self.maxhp * self.SEC_CAP * dt)
        if self.spawn_t > 0:
            self.spawn_t -= dt
            return
        if self.burn > 0:
            self.burn -= dt; self.hp -= self.burn_dps * dt
        if self.poison > 0:
            self.poison -= dt; self.hp -= self.poison_dps * dt
        if self.hp <= 0:
            run.kill_enemy(self)
            return
        if run.timestop > 0:
            return
        if self.frozen > 0:
            self.frozen -= dt * 2.5   # Bosse tauen schnell auf
            return
        sp = 0.75 if self.slowed > 0 else 1.0
        if self.slowed > 0:
            self.slowed -= dt
        if self.phase == 1 and self.hp < self.maxhp * self.P2:
            self.phase = 2
            self.rest *= 0.7
            audio.play('roar')
            run.shake(6)
            self.on_phase2()
        if self.phase == 2 and self.hp < self.maxhp * 0.25 and not getattr(self, 'enraged', False):
            self.enraged = True
            self.rest *= 0.75
            run.bullet_speed_mult *= 1.1
            audio.play('roar')
            run.shake(8)
            run.banner(self.name + ' rast vor Wut!', '', (255, 90, 80))
        if getattr(self, 'enraged', False) and random.random() < 0.3:
            run.particles.append(Particle(self.x + random.uniform(-self.r, self.r), self.y + random.uniform(-self.r, self.r), 0, -40, 0.4, (255, 80, 60), 2))
        self.move(dt * sp)
        # Koroutinen-Angriffe
        if self.co is None:
            self.idle -= dt * sp
            if self.idle <= 0:
                pool = self.attacks2 if (self.phase == 2 and self.attacks2) else self.attacks
                choice = random.choice(pool)
                if choice == self.last and len(pool) > 1:
                    choice = random.choice(pool)
                self.last = choice
                self.co = getattr(self, 'a_' + choice)()
                self.wait = 0.0
        if self.co is not None:
            self.wait -= dt * sp
            guard = 0
            while self.co is not None and self.wait <= 0 and guard < 50:
                guard += 1
                try:
                    self.wait += next(self.co)
                except StopIteration:
                    self.co = None
                    self.idle = self.rest * random.uniform(0.7, 1.2)
        # Kontakt
        if not self.hidden and not self.invuln:
            p = self.p
            for hx, hy, hr in self.hitboxes():
                if math.hypot(p.x - hx, p.y - hy) < hr + p.hitr:
                    if p.dash_t > 0 and p.f['dash_dmg'] and id(self) not in p.dash_hit:
                        p.dash_hit.add(id(self))
                        run.damage_enemy(self, p.damage() * 2.5, None)
                    else:
                        p.hurt(self.contact, self.name)
                    break
        if abs(self.kx) + abs(self.ky) > 1:
            self.kx *= 0.7; self.ky *= 0.7

    def move(self, dt):
        pass

    def on_phase2(self):
        pass

    def a_ring(self):
        self.ring(12, 90)
        yield 0.5

    # ------------------------------------------------------------ Zeichnen
    def draw(self, s, t):
        if self.spawn_t > 0:
            f = 1 - self.spawn_t / 1.2
            gfx.draw_glow(s, int(self.x), int(self.y), int(30 * f) + 4, (255, 255, 255), int(120 * f))
            if f < 0.4:
                return
        if self.hidden:
            self.draw_hidden(s, t)
            return
        surf = pygame.Surface((W, H), pygame.SRCALPHA)
        target = surf
        gfx.shadow(s, (int(self.x) - self.r, int(self.y) + self.r - 4, self.r * 2, 7))
        oy = self.y
        self.y += math.sin(t * 2.2) * 1.2
        n0 = len(gfx.HI)
        try:
            if getattr(self, 'sheet', None):
                self.render_sheet(target, t)
            else:
                self.render(target, t)
        finally:
            self.y = oy
        for i in range(n0, len(gfx.HI)):
            im, cx, by, a = gfx.HI[i]
            if self.flash > 0:
                im = gfx.tinted(im, 'flash')
            elif self.frozen > 0:
                im = gfx.tinted(im, 'frozen')
            gfx.HI[i] = (im, cx, by, min(a, self.alpha))
        if True:
            m = pygame.mask.from_surface(surf, 200)
            ol = m.to_surface(setcolor=(18, 10, 22, 255), unsetcolor=(0, 0, 0, 0))
            base = surf
            surf = pygame.Surface((W, H), pygame.SRCALPHA)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                surf.blit(ol, (dx, dy))
            surf.blit(base, (0, 0))
            if self.flash > 0:
                surf.fill((120, 110, 110, 0), special_flags=pygame.BLEND_RGB_ADD)
            elif self.frozen > 0:
                surf.fill((150, 210, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
            if self.alpha < 255:
                surf.set_alpha(self.alpha)
            s.blit(surf, (0, 0))

    def draw_hidden(self, s, t):
        pass

    sheet = None   # (Name, Skalierung, Tönung)

    def face_dir(self):
        return sheets.hdir(self.p.x - self.x)

    def render_sheet(self, s, t):
        name, sc, tint = self.sheet
        self.render_under(s, t)
        sheets.blit_center(s, name, self.x, self.y - 4, self.face_dir(), self.af(name, t, 7, 0), sc, tint)
        self.render_extra(s, t)

    def render_under(self, s, t):
        pass

    def render_extra(self, s, t):
        pass

    def render(self, s, t):
        pygame.draw.circle(s, (200, 50, 50), (int(self.x), int(self.y)), self.r)


def hi_tube(pts, radii, cols, belly=None, spikes=None, fin=None, extra=None, scales=False):
    """Glatte Röhre (Schlangenleib, Hals, Knochen) in der Hi-Res-Ebene.
    pts: Weltpunkte, radii: Radien (Welt) je Punkt, cols: (Umriss, Schatten, Grund, Licht)."""
    if len(pts) < 2:
        return
    # auf ~0.5 Welt-Pixel nachrastern
    res, rr = [], []
    for (x0, y0), (x1, y1), r0, r1 in zip(pts, pts[1:], radii, radii[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(d / 0.6))
        for k in range(n):
            f = k / n
            res.append((x0 + (x1 - x0) * f, y0 + (y1 - y0) * f))
            rr.append(r0 + (r1 - r0) * f)
    res.append(pts[-1]); rr.append(radii[-1])
    pad = max(rr) + 8
    xs = [p_[0] for p_ in res]; ys = [p_[1] for p_ in res]
    x0, y0 = min(xs) - pad, min(ys) - pad
    w, h = int((max(xs) + pad - x0) * 2), int((max(ys) + pad - y0) * 2)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    D = pygame.draw
    P = [((x - x0) * 2, (y - y0) * 2) for x, y in res]
    R = [r * 2 for r in rr]
    out, dark, base, light = cols
    for (x, y), r in zip(P, R):
        D.circle(surf, out, (int(x), int(y)), int(r + 2))
    for (x, y), r in zip(P, R):
        D.circle(surf, dark, (int(x), int(y)), int(r))
    for (x, y), r in zip(P, R):
        D.circle(surf, base, (int(x - r * 0.2), int(y - r * 0.3)), max(1, int(r * 0.72)))
    if belly:
        for i in range(0, len(P), 2):
            x, y = P[i]; r = R[i]
            D.circle(surf, belly, (int(x + r * 0.25), int(y + r * 0.45)), max(1, int(r * 0.42)))
    if scales:
        for i in range(3, len(P) - 3, 7):                          # Schuppenbögen
            x, y = P[i]; r = R[i]
            if r < 4:
                continue
            (ax, ay), (bx, by) = P[i - 3], P[i + 3]
            ang = math.degrees(math.atan2(-(by - ay), bx - ax))
            rect = pygame.Rect(0, 0, int(r * 1.1), int(r * 1.1)); rect.center = (int(x - r * 0.15), int(y - r * 0.2))
            D.arc(surf, dark, rect, math.radians(ang + 90), math.radians(ang + 270), 2)
    for i in range(0, len(P)):
        x, y = P[i]; r = R[i]
        D.circle(surf, light, (int(x - r * 0.45), int(y - r * 0.6)), max(1, int(r * 0.22)))
    if spikes:
        col, every = spikes
        for i in range(every, len(P) - 2, every):
            x, y = P[i]; r = R[i]
            (ax, ay), (bx, by) = P[i - 1], P[i + 1]
            dx, dy = bx - ax, by - ay
            dl = math.hypot(dx, dy) or 1
            nx, ny = dy / dl, -dx / dl
            if ny > 0:
                nx, ny = -nx, -ny
            tip = (x + nx * (r + 7), y + ny * (r + 7))
            b1 = (x + nx * r - dx / dl * 3, y + ny * r - dy / dl * 3)
            b2 = (x + nx * r + dx / dl * 3, y + ny * r + dy / dl * 3)
            D.polygon(surf, out, [tip, b1, b2]); D.polygon(surf, col, [(tip[0], tip[1] + 1), b1, b2])
    if fin:
        col, col2 = fin
        (ax, ay), (bx, by) = P[-3], P[-1]
        dx, dy = bx - ax, by - ay
        dl = math.hypot(dx, dy) or 1
        dx, dy = dx / dl, dy / dl
        nx, ny = -dy, dx
        tx, ty = P[-1]
        poly = [(tx, ty), (tx + dx * 14 + nx * 12, ty + dy * 14 + ny * 12), (tx + dx * 8, ty + dy * 8),
                (tx + dx * 14 - nx * 12, ty + dy * 14 - ny * 12)]
        D.polygon(surf, out, [(x + (1 if x > tx else -1), y) for x, y in poly])
        D.polygon(surf, col, poly)
        D.line(surf, col2, (tx, ty), (tx + dx * 12 + nx * 9, ty + dy * 12 + ny * 9), 1)
        D.line(surf, col2, (tx, ty), (tx + dx * 12 - nx * 9, ty + dy * 12 - ny * 9), 1)
    if extra:
        extra(surf, lambda x, y: ((x - x0) * 2, (y - y0) * 2))
    gfx.hi_blit(surf, x0 + w / 4, y0 + h / 2, transient=True)


JADE = ((10, 22, 26), (26, 84, 78), (50, 140, 118), (150, 220, 190))
SNAKE = ((10, 20, 12), (30, 66, 36), (62, 112, 56), (150, 196, 120))
BONE = ((20, 16, 14), (150, 140, 120), (226, 218, 196), (255, 250, 236))


def eyes(s, x, y, dx, col=(255, 230, 90), r=2):
    pygame.draw.circle(s, (20, 10, 10), (int(x - dx), int(y)), r + 1)
    pygame.draw.circle(s, (20, 10, 10), (int(x + dx), int(y)), r + 1)
    pygame.draw.circle(s, col, (int(x - dx), int(y)), r)
    pygame.draw.circle(s, col, (int(x + dx), int(y)), r)


# =====================================================================  EBENE 1
class Omukade(Boss):
    r = 10

    def setup(self):
        self.heading = random.uniform(0, math.tau)
        self.trail = [(self.x, self.y)] * 200
        self.segs = 12
        self.speed = 70
        self.attacks = ['spit', 'legs', 'rush']
        self.attacks2 = ['spit', 'legs', 'rush', 'coil']
        self.boost = 0.0

    def move(self, dt):
        want = self.ang_p()
        d = (want - self.heading + math.pi) % math.tau - math.pi
        self.heading += clamp(d, -1.4 * dt, 1.4 * dt) + math.sin(self.t * 2.3) * 0.9 * dt
        sp = (self.speed + (25 if self.phase == 2 else 0)) * (2.2 if self.boost > 0 else 1)
        self.boost = max(0, self.boost - dt)
        nx, ny = self.x + math.cos(self.heading) * sp * dt, self.y + math.sin(self.heading) * sp * dt
        if nx < RX + 12 or nx > RX + RW - 12:
            self.heading = math.pi - self.heading
        if ny < RY + 12 or ny > RY + RH - 12:
            self.heading = -self.heading
        self.x, self.y = clamp(nx, RX + 12, RX + RW - 12), clamp(ny, RY + 12, RY + RH - 12)
        self.trail.insert(0, (self.x, self.y))
        del self.trail[260:]

    def seg_pos(self):
        out = []
        dist_acc, need, i = 0.0, 10.0, 1
        px, py = self.x, self.y
        for (x, y) in self.trail[1:]:
            dist_acc += math.hypot(x - px, y - py)
            px, py = x, y
            if dist_acc >= need:
                out.append((x, y))
                need += 9.0
                if len(out) >= self.segs:
                    break
        return out

    def hitboxes(self):
        return [(self.x, self.y, 10)] + [(x, y, 7) for x, y in self.seg_pos()]

    def a_spit(self):
        for i in range(3 if self.phase == 1 else 5):
            self.fan(3, 0.25, 120, (200, 120, 255))
            yield 0.35

    def a_legs(self):
        for x, y in self.seg_pos()[::2]:
            a = self.heading + math.pi / 2
            ebullet(self.run, x, y, a, 70, (230, 200, 90))
            ebullet(self.run, x, y, a + math.pi, 70, (230, 200, 90))
        yield 0.8

    def a_rush(self):
        audio.play('roar', 0.5)
        self.boost = 1.4
        yield 1.4

    def a_coil(self):
        for k in range(3):
            self.ring(14, 85, k * 0.2, (200, 120, 255))
            yield 0.4

    def render(self, s, t):
        if type(self) is Omukade:
            segs = self.seg_pos()
            for i, (x, y) in enumerate(reversed(segs)):
                sheets.blit_center(s, 'boss_omukade_seg', x, y, sheets.hdir(math.cos(self.heading)), self.af('boss_omukade_seg', t, 8, i))
            sheets.blit_center(s, 'boss_omukade_head', self.x, self.y, sheets.hdir(math.cos(self.heading)), self.af('boss_omukade_head', t, 8, 0))
            return
        segs = self.seg_pos()
        for i, (x, y) in enumerate(reversed(segs)):
            j = len(segs) - i
            a = t * 12 + j
            for side in (-1, 1):
                lx = x + math.cos(self.heading + side * 1.57) * 9
                ly = y + math.sin(self.heading + side * 1.57) * 9 + math.sin(a) * 2
                pygame.draw.line(s, (240, 200, 80), (x, y), (lx, ly), 2)
            pygame.draw.circle(s, (30, 10, 10), (int(x), int(y)), 8)
            pygame.draw.circle(s, (150, 40, 40) if j % 2 else (120, 30, 40), (int(x), int(y)), 7)
            pygame.draw.circle(s, (200, 80, 60), (int(x) - 2, int(y) - 2), 2)
        hx, hy = self.x, self.y
        pygame.draw.circle(s, (30, 10, 10), (int(hx), int(hy)), 11)
        pygame.draw.circle(s, (180, 50, 40), (int(hx), int(hy)), 10)
        for side in (-1, 1):
            a = self.heading + side * 0.5
            pygame.draw.line(s, (240, 220, 120), (hx, hy), (hx + math.cos(a) * 15, hy + math.sin(a) * 15), 3)
        eyes(s, hx + math.cos(self.heading) * 4, hy + math.sin(self.heading) * 4 - 2, 4)


class KappaOu(Boss):
    sheet = ('boss_kappa_ou', 1, None)

    def render_sheet(self, s, t):
        img = sheets.blit_center(s, 'boss_kappa_ou', self.x, self.y - self.z - 6, self.face_dir(), self.af('boss_kappa_ou', t, 7, 0))
        return
        x, y = int(self.x), int(self.y - self.z - 6 - img.get_height() / 2)
        pygame.draw.polygon(s, (245, 205, 70), [(x - 12, y + 6), (x - 13, y - 6), (x - 6, y + 1), (x, y - 9), (x + 6, y + 1), (x + 13, y - 6), (x + 12, y + 6)])
        pygame.draw.polygon(s, (150, 100, 30), [(x - 12, y + 6), (x - 13, y - 6), (x - 6, y + 1), (x, y - 9), (x + 6, y + 1), (x + 13, y - 6), (x + 12, y + 6)], 1)
        pygame.draw.circle(s, (220, 50, 60), (x, y + 2), 2)

    r = 16

    def setup(self):
        self.attacks = ['jump', 'spit', 'summon']
        self.attacks2 = ['jump', 'spit', 'summon', 'rain', 'triple', 'whirlpool']
        self.z = 0.0

    def a_jump(self, n=1):
        for _ in range(n):
            tx, ty = self.p.x, self.p.y
            sx, sy = self.x, self.y
            self.hazard(tx, ty, 26, 0.75, 0.05, 'slam')
            for i in range(15):
                f = (i + 1) / 15
                self.x = sx + (tx - sx) * f
                self.y = sy + (ty - sy) * f
                self.z = math.sin(f * math.pi) * 50
                self.invuln = self.z > 25
                yield 0.05
            self.z = 0
            self.invuln = False
            self.clamp_pos()
            self.ring(14 if self.phase == 1 else 18, 95, random.random(), (110, 190, 255))
            self.run.shake(5)
            yield 0.4

    def a_triple(self):
        yield from self.a_jump(3)

    def a_whirlpool(self):
        for k in range(40):
            for j in range(2):
                ebullet(self.run, self.x, self.y, k * 0.3 + j * math.pi, 80, (110, 190, 255), curve=0.9)
            yield 0.05

    def a_spit(self):
        for i in range(3):
            self.fan(5, 0.2, 130, (110, 190, 255))
            yield 0.4

    def a_summon(self):
        self.summon('kappa_small', 2 if self.phase == 1 else 3, 30)
        yield 0.6

    def a_rain(self):
        for i in range(8):
            x, y = free_tile_pos(self.run.room, random)
            if i % 2 == 0:
                x, y = self.p.x + random.uniform(-30, 30), self.p.y + random.uniform(-30, 30)
            self.hazard(x, y, 14, 0.9, 0.2, 'water')
            yield 0.15
        yield 0.6

    def render(self, s, t):
        art.draw_big(s, 'kappa_ou', self.x, self.y - self.z - 6, 1.55, flip=self.p.x > self.x)
        return
        x, y = int(self.x), int(self.y - self.z)
        D = pygame.draw
        D.circle(s, (20, 40, 20), (x, y), 17)
        D.circle(s, (80, 170, 80), (x, y), 16)
        D.ellipse(s, (110, 80, 40), (x - 12, y - 4, 24, 18))
        D.circle(s, (100, 190, 90), (x, y - 6), 12)
        D.ellipse(s, (230, 240, 250), (x - 9, y - 19, 18, 7))
        D.ellipse(s, (150, 200, 230), (x - 6, y - 18, 12, 4))
        D.polygon(s, (250, 200, 70), [(x - 5, y - 2), (x + 5, y - 2), (x, y + 5)])
        eyes(s, x, y - 8, 5, (255, 255, 255), 2)
        D.circle(s, (0, 0, 0), (x - 5, y - 8), 1); D.circle(s, (0, 0, 0), (x + 5, y - 8), 1)
        # Krone
        D.polygon(s, (240, 200, 70), [(x - 6, y - 20), (x - 4, y - 25), (x, y - 21), (x + 4, y - 25), (x + 6, y - 20)])


class Jorogumo(Boss):
    sheet = ('boss_jorogumo', 1, None)

    r = 13

    def setup(self):
        self.attacks = ['web', 'eggs', 'spiral', 'dash']
        self.attacks2 = ['web', 'eggs', 'spiral', 'dash', 'webring', 'net']
        self.y = RY + 60
        self.tx = self.x

    def move(self, dt):
        self.tx += math.sin(self.t * 0.7) * 30 * dt
        self.x += (self.tx - self.x) * min(1, dt * 2)
        self.clamp_pos(20)

    def a_web(self):
        for i in range(2):
            self.fan(7, 0.18, 90, (240, 240, 250), eff='slow')
            yield 0.5

    def a_eggs(self):
        self.summon('kumo', 3, 25)
        yield 0.8

    def a_spiral(self):
        for i in range(30):
            for k in range(2 if self.phase == 1 else 3):
                ebullet(self.run, self.x, self.y, self.t * 3 + k * math.tau / (2 if self.phase == 1 else 3), 85, (180, 90, 220))
            yield 0.07

    def a_dash(self):
        self.tx = random.uniform(RX + 40, RX + RW - 40)
        yield 0.6
        self.fan(3, 0.3, 140, (180, 90, 220))
        yield 0.3

    def a_net(self):
        for row in range(3):
            y = self.p.y - 40 + row * 40
            for col in range(0, 13, 2):
                ebullet(self.run, RX + 16 + col * 32 + (16 if row % 2 else 0), y, math.pi / 2, 0.0, (240, 240, 250), 3, eff='slow').life = 1.6
        yield 1.2
        self.fan(5, 0.2, 140, (180, 90, 220))
        yield 0.4

    def a_webring(self):
        self.ring(16, 70, 0, (240, 240, 250), eff='slow')
        yield 0.3
        self.fan(5, 0.15, 150, (180, 90, 220))
        yield 0.5

    def render(self, s, t):
        art.draw_big(s, 'jorogumo_b', self.x, self.y - 4, 1.5)
        return
        x, y = int(self.x), int(self.y)
        D = pygame.draw
        for i in range(4):
            for side in (-1, 1):
                a = 0.4 + i * 0.35 + math.sin(t * 6 + i) * 0.08
                kx, ky = x + side * math.cos(a) * 14, y + 4 + math.sin(a) * 6
                fx, fy = x + side * math.cos(a) * 24, y + 14 + i * 3
                D.line(s, (30, 20, 40), (x, y + 6), (kx, ky - 4), 3)
                D.line(s, (30, 20, 40), (kx, ky - 4), (fx, fy), 2)
        D.ellipse(s, (40, 20, 50), (x - 13, y, 26, 20))
        D.ellipse(s, (180, 40, 70), (x - 6, y + 6, 12, 8))
        D.polygon(s, (120, 50, 140), [(x - 7, y + 2), (x + 7, y + 2), (x + 5, y - 12), (x - 5, y - 12)])
        D.circle(s, (246, 220, 210), (x, y - 17), 6)
        D.ellipse(s, (20, 10, 20), (x - 8, y - 25, 16, 10))
        D.rect(s, (20, 10, 20), (x - 8, y - 20, 3, 14)); D.rect(s, (20, 10, 20), (x + 5, y - 20, 3, 14))
        D.circle(s, (200, 30, 40), (x - 2, y - 17), 1); D.circle(s, (200, 30, 40), (x + 2, y - 17), 1)
        D.line(s, (240, 200, 80), (x - 4, y - 25), (x - 9, y - 30), 1)


# =====================================================================  EBENE 2
GASHA_PAL = ((10, 8, 20), (95, 66, 80), (168, 134, 106), (220, 203, 156), (255, 246, 216))
_GASHA_HAND = {}


def gasha_hand(spread, wig):
    """Aus dem Boden ragender Skelettarm mit Hand – Pixelgrafik in Hi-Res (1 Pixel = ½ Weltpixel),
    gleiche Farben wie das Gashadokuro-Sprite. spread 0 = geschlossen, 0.5 = gespreizt zum Zupacken."""
    key = (spread, wig)
    if key in _GASHA_HAND:
        return _GASHA_HAND[key]
    K, D_, M, L, H = GASHA_PAL
    S = 1.9
    w, h = 96, 124
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    dr = pygame.draw

    def bone(p0, p1, wd):
        p0 = (round(p0[0]), round(p0[1])); p1 = (round(p1[0]), round(p1[1]))
        dr.line(surf, K, p0, p1, wd + 3)
        dr.line(surf, D_, p0, p1, wd)
        dr.line(surf, M, (p0[0] - 1, p0[1]), (p1[0] - 1, p1[1]), max(1, wd - 2))
        if wd >= 5:
            dr.line(surf, L, (p0[0] - 2, p0[1]), (p1[0] - 2, p1[1]), max(1, wd - 5))

    def knob(p, r):
        p = (round(p[0]), round(p[1]))
        dr.circle(surf, K, p, r + 2)
        dr.circle(surf, D_, p, r)
        dr.circle(surf, M, (p[0] - 1, p[1] - 1), max(1, r - 1))
        dr.circle(surf, L, (p[0] - 2, p[1] - 2), max(1, r - 3))

    cx = w // 2
    base = h - 3
    wy = 66                                                        # Handgelenk
    bone((cx - 7, base), (cx - 5, wy + 6), 7)                      # Elle
    bone((cx + 7, base), (cx + 5, wy + 6), 6)                      # Speiche
    for (dx, dy, r) in ((-7, 3, 5), (0, 0, 5), (7, 3, 5), (-4, -6, 5), (5, -6, 5)):   # Handwurzel
        knob((cx + dx, wy + dy), r)
    for f in range(5):
        ang = -math.pi / 2 + (f - 2) * (0.24 + spread * 0.45) + (0.05 * wig if f == 4 else 0)
        if f == 0:
            ang = -math.pi / 2 - 1.0 - spread * 0.35                # Daumen seitlich
        x, y = cx + (f - 2) * 5, wy - 10
        lens = [l * S for l in ((8, 7, 6, 4) if f not in (0, 4) else (6, 6, 5, 3))]
        for k, ln in enumerate(lens):
            nx, ny = x + math.cos(ang) * ln, y + math.sin(ang) * ln
            bone((x, y), (nx, ny), 5 if k < 2 else 4)
            if k < 3:
                knob((nx, ny), 2)
            x, y = nx, ny
            ang += 0.2 if f < 2 else (-0.2 if f > 2 else 0.1 * (1 - 2 * wig))
        tip = (x + math.cos(ang) * 6, y + math.sin(ang) * 6)
        dr.polygon(surf, K, [(round(x - 2), round(y)), (round(x + 2), round(y)), (round(tip[0]), round(tip[1]))])
    _GASHA_HAND[key] = surf
    return surf


class Gashadokuro(Boss):
    sheet = ('boss_gashadokuro', 1, None)

    def render_extra(self, s, t):
        """Die Riesenhände wühlen sich durch den Boden: Erdloch, herausragender Unterarm (Elle und Speiche), Knochenhand.
        Keine Verbindung zum Körper – das Skelett hat seine eigenen Arme im Sprite."""
        for i, h in enumerate(self.hands):
            hx, hy = h[0], h[1]
            gy = hy + 26 - (6 if self.busy[i] else 0)          # Bodenhöhe des Lochs
            # Erdloch mit aufgeworfener Erde (niedrige Ebene, unter allem)
            pygame.draw.ellipse(s, (14, 10, 12), (int(hx - 17), int(gy - 5), 34, 10))
            pygame.draw.ellipse(s, (6, 4, 6), (int(hx - 12), int(gy - 3), 24, 6))
            for k in range(7):
                a = k / 7 * math.tau + i
                pygame.draw.circle(s, (95, 66, 80) if k % 2 else (70, 52, 46), (int(hx + math.cos(a) * 17), int(gy + math.sin(a) * 5)), 2)
            # Unterarm (Elle und Speiche) und Knochenhand als Pixelgrafik in Sprite-Farben
            img = gasha_hand(0.5 if self.busy[i] else 0.0, int(t * 4 + i) % 2)
            gfx.hi_blit(img, hx, gy + 2)

    r = 20

    def setup(self):
        self.y = RY + 45
        self.hands = [[CX - 70, RY + 110], [CX + 70, RY + 110]]
        self.hand_home = [[CX - 70, RY + 110], [CX + 70, RY + 110]]
        self.attacks = ['slam', 'bones', 'jaw']
        self.attacks2 = ['slam', 'double', 'bones', 'jaw', 'clap']
        self.busy = [False, False]

    def move(self, dt):
        self.x = CX + math.sin(self.t * 0.6) * 90
        for i, h in enumerate(self.hands):
            if not self.busy[i]:
                hx = self.x + (-70 if i == 0 else 70)
                hy = RY + 110 + math.sin(self.t * 2 + i) * 6
                h[0] += (hx - h[0]) * min(1, dt * 3)
                h[1] += (hy - h[1]) * min(1, dt * 3)

    def hitboxes(self):
        return [(self.x, self.y, 20)] + [(h[0], h[1], 10) for h in self.hands]

    def _slam(self, i):
        self.busy[i] = True
        h = self.hands[i]
        tx, ty = self.p.x, self.p.y
        for k in range(10):
            h[0] += (tx - h[0]) * 0.3
            h[1] += (ty - 30 - h[1]) * 0.3
            yield 0.05
        self.hazard(tx, ty, 22, 0.45, 0.1, 'slam')
        yield 0.45
        h[0], h[1] = tx, ty
        self.ring(10 if self.phase == 1 else 14, 90, random.random(), (230, 220, 200), x=tx, y=ty)
        yield 0.5
        self.busy[i] = False

    def a_slam(self):
        yield from self._slam(random.randint(0, 1))

    def a_double(self):
        yield from self._slam(0)
        yield from self._slam(1)

    def a_clap(self):
        self.busy = [True, True]
        ty = self.p.y
        for k in range(12):
            for i, h in enumerate(self.hands):
                h[0] += ((RX + 30 if i == 0 else RX + RW - 30) - h[0]) * 0.3
                h[1] += (ty - h[1]) * 0.3
            yield 0.04
        for k in range(14):
            for i, h in enumerate(self.hands):
                h[0] += (self.p.x - h[0]) * 0.2
            yield 0.03
        self.ring(16, 100, 0, (230, 220, 200), x=self.hands[0][0], y=ty)
        self.run.shake(6)
        yield 0.4
        self.busy = [False, False]

    def a_bones(self):
        for i in range(16):
            x = random.uniform(RX + 10, RX + RW - 10)
            ebullet(self.run, x, RY + 4, math.pi / 2, 60, (230, 220, 200), 3, acc=0.9)
            yield 0.1

    def a_jaw(self):
        for k in range(3):
            self.ring(16, 100, k * 0.15, (255, 80, 80))
            yield 0.35

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        bone = (232, 226, 206)
        for i, h in enumerate(self.hands):
            hx, hy = int(h[0]), int(h[1])
            D.line(s, bone, (x + (-14 if i == 0 else 14), y + 10), (hx, hy), 4)
            D.circle(s, (40, 30, 30), (hx, hy), 10)
            D.circle(s, bone, (hx, hy), 9)
            for f in range(4):
                a = math.pi / 2 + (f - 1.5) * 0.4
                D.line(s, bone, (hx, hy), (hx + math.cos(a) * 14, hy + math.sin(a) * 14), 2)
        D.circle(s, (40, 30, 30), (x, y), 22)
        D.circle(s, bone, (x, y), 21)
        D.rect(s, bone, (x - 13, y + 12, 26, 10))
        for i in range(5):
            D.line(s, (40, 30, 30), (x - 10 + i * 5, y + 14), (x - 10 + i * 5, y + 21), 1)
        D.ellipse(s, (20, 10, 10), (x - 13, y - 8, 10, 12))
        D.ellipse(s, (20, 10, 10), (x + 3, y - 8, 10, 12))
        gfx.draw_glow(s, x - 8, y - 2, 6, (255, 50, 50), 160)
        gfx.draw_glow(s, x + 8, y - 2, 6, (255, 50, 50), 160)
        D.polygon(s, (20, 10, 10), [(x, y + 4), (x - 3, y + 9), (x + 3, y + 9)])


_NECK_ANCHOR = {}


def _anchor(img, body):
    """Endpunkt des Halsstummels im Sprite (Hautfarbe): beim Körper ganz oben, beim Kopf ganz unten."""
    key = (id(img), body)
    if key in _NECK_ANCHOR:
        return _NECK_ANCHOR[key]
    arr = pygame.surfarray.pixels3d(img)
    al = pygame.surfarray.pixels_alpha(img)
    best = None
    w, h = img.get_size()
    for xx in range(w):
        for yy in range(h):
            if al[xx, yy] == 0:
                continue
            r_, g_, b_ = int(arr[xx, yy, 0]), int(arr[xx, yy, 1]), int(arr[xx, yy, 2])
            if r_ > 190 and g_ > 130 and 100 < b_ < 200 and r_ - b_ > 40:
                sc = -yy if body else yy
                if best is None or sc > best[0]:
                    best = (sc, xx, yy)
    del arr, al
    res = (best[1], best[2]) if best else (w // 2, 0 if body else h)
    _NECK_ANCHOR[key] = (res, w, h)
    return _NECK_ANCHOR[key]


class Rokurokubi(Boss):
    r = 9

    def draw_neck(self, t, bx, by, hx, hy):
        """Langer Hals als glatte Röhre in der Hi-Res-Ebene zwischen Körper- und Kopfstummel."""
        bd = sheets.hdir(self.p.x - bx)
        hd = sheets.hdir(self.p.x - hx)
        bimg = sheets.frame('boss_rokuro_body', bd, self.af('boss_rokuro_body', t, 4, 0))
        himg = sheets.frame('boss_rokuro_head', hd, self.af('boss_rokuro_head', t, 4, 0))
        (ax_, ay_), bw, bh = _anchor(bimg, True)
        (ex_, ey_), hw, hh = _anchor(himg, False)
        A = (bx - bw / 4 + ax_ / 2, by - bh / 4 + ay_ / 2 + 2.0)
        B = (hx - hw / 4 + ex_ / 2, hy - hh / 4 + ey_ / 2)
        side = -1 if hd == sheets.RIGHT else 1          # Kopf schaut zum Spieler, Stummel zeigt nach hinten-unten
        hdx, hdy = 0.6 * side / 1.166, 1.0 / 1.166
        B = (B[0] - hdx * 1.5, B[1] - hdy * 1.5)
        c1 = (A[0], A[1] - 34)
        L = math.hypot(B[0] - A[0], B[1] - A[1]) + 40
        K = max(28, 0.45 * L)                         # Hals führt den Stummel fort und schwingt im Bogen zum Körper
        c2 = (B[0] + hdx * K, B[1] + hdy * K)
        n = max(24, int(L * 1.6))
        pts = []
        for i in range(n + 1):
            u = i / n
            mu = 1 - u
            px_ = mu ** 3 * A[0] + 3 * mu * mu * u * c1[0] + 3 * mu * u * u * c2[0] + u ** 3 * B[0]
            py_ = mu ** 3 * A[1] + 3 * mu * mu * u * c1[1] + 3 * mu * u * u * c2[1] + u ** 3 * B[1]
            pts.append([px_, py_])
        base = [q[:] for q in pts]
        for i in range(1, n):                         # Schlängeln quer zur Laufrichtung
            dx_, dy_ = base[i + 1][0] - base[i - 1][0], base[i + 1][1] - base[i - 1][1]
            dl = math.hypot(dx_, dy_) or 1
            u = i / n
            amp = 7 * math.sin(math.pi * u) * math.sin(u * math.pi * 3 + t * 3)
            pts[i][0] += -dy_ / dl * amp
            pts[i][1] += dx_ / dl * amp
        xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
        m = 4
        x0, y0 = min(xs) - m, min(ys) - m
        sw, shh = int((max(xs) - x0 + m) * 2) + 2, int((max(ys) - y0 + m) * 2) + 2
        surf = pygame.Surface((sw, shh), pygame.SRCALPHA)
        hp = [((q[0] - x0) * 2, (q[1] - y0) * 2) for q in pts]
        D = pygame.draw
        for col, rad, off in (((10, 8, 20), 4.6, 0), ((201, 128, 108), 3.4, 0.6), ((240, 188, 152), 2.4, -0.4), ((255, 230, 204), 0.9, -1.4)):
            for q in hp:
                D.circle(surf, col, (int(q[0] + off), int(q[1] + off * 0.3)), max(1, int(round(rad))))
        gfx.hi_blit(surf, x0 + sw / 4, y0 + shh / 2, transient=True)

    def setup(self):
        self.body = (CX, RY + 40)
        self.x, self.y = CX, RY + 90
        self.attacks = ['lunge', 'spit', 'whip']
        self.attacks2 = ['lunge', 'spit', 'whip', 'hair']
        self.home = (CX, RY + 90)

    def move(self, dt):
        if self.co is None:
            self.x += (self.home[0] + math.sin(self.t * 1.3) * 60 - self.x) * min(1, dt * 2)
            self.y += (self.home[1] + math.cos(self.t * 1.1) * 30 - self.y) * min(1, dt * 2)

    def a_lunge(self):
        for k in range(2 if self.phase == 1 else 3):
            tx, ty = self.p.x, self.p.y
            yield 0.35
            for i in range(10):
                self.x += (tx - self.x) * 0.3
                self.y += (ty - self.y) * 0.3
                yield 0.03
            self.ring(8, 80, 0, (240, 140, 200))
            yield 0.3
            for i in range(10):
                self.x += (self.home[0] - self.x) * 0.25
                self.y += (self.home[1] - self.y) * 0.25
                yield 0.03

    def a_spit(self):
        for k in range(3):
            self.ring(10, 90, k * 0.3, (240, 140, 200))
            yield 0.4

    def a_whip(self):
        for i in range(36):
            a = i / 36 * math.tau
            self.x = CX + math.cos(a) * 140
            self.y = CY + math.sin(a) * 70
            if i % 3 == 0:
                ebullet(self.run, self.x, self.y, self.ang_p(), 60, (200, 100, 180))
            yield 0.04

    def a_hair(self):
        bx, by = self.body
        for i in range(40):
            for k in range(4):
                ebullet(self.run, bx, by + 10, i * 0.25 + k * math.pi / 2, 75, (40, 30, 60), 3)
            yield 0.06

    def render(self, s, t):
        D = pygame.draw
        bx, by = self.body
        if sheets.has('boss_rokuro_body'):
            sheets.blit_center(s, 'boss_rokuro_body', bx, by + 6, sheets.hdir(self.p.x - bx), self.af('boss_rokuro_body', t, 4, 0))
        else:
            D.ellipse(s, (180, 50, 70), (bx - 18, by - 2, 36, 26))
        x, y = int(self.x), int(self.y)
        if sheets.has('boss_rokuro_body') and sheets.has('boss_rokuro_head'):
            self.draw_neck(t, bx, by + 6, x, y)
        x, y = int(self.x), int(self.y)
        sheets.blit_center(s, 'boss_rokuro_head', x, y, sheets.hdir(self.p.x - x), self.af('boss_rokuro_head', t, 4, 0))
        return
        D.circle(s, (20, 10, 20), (x, y - 3), 11)
        D.circle(s, (248, 222, 204), (x, y), 8)
        D.rect(s, (20, 10, 20), (x - 9, y - 4, 3, 12)); D.rect(s, (20, 10, 20), (x + 6, y - 4, 3, 12))
        D.circle(s, (20, 10, 20), (x - 3, y - 1), 1); D.circle(s, (20, 10, 20), (x + 3, y - 1), 1)
        D.line(s, (200, 40, 60), (x - 2, y + 4), (x + 2, y + 4))


class Nue(Boss):
    sheet = ('boss_nue', 1, None)

    r = 14

    def setup(self):
        self.attacks = ['charge', 'thunder', 'cloud', 'tail']
        self.attacks2 = ['charge', 'thunder', 'cloud', 'tail', 'storm']
        self.dir = (1, 0)

    def a_charge(self):
        for k in range(3):
            d = norm(self.p.x - self.x, self.p.y - self.y)
            self.dir = d
            yield 0.35
            for i in range(30):
                self.x, self.y, bx, by = move_body(self.run.room, self.x, self.y, 12, d[0] * 260 * 0.02, d[1] * 260 * 0.02, True)
                if bx or by:
                    self.run.shake(3)
                    self.ring(8, 80, 0, (255, 230, 90))
                    break
                yield 0.02
            yield 0.2

    def a_thunder(self):
        for i in range(5 if self.phase == 1 else 8):
            x = self.p.x + random.uniform(-25, 25)
            y = self.p.y + random.uniform(-25, 25)
            self.hazard(x, y, 16, 0.7, 0.15, 'strike')
            yield 0.25

    def a_cloud(self):
        self.alpha = 120
        self.invuln = True
        burst(self.run, self.x, self.y, (30, 20, 40), 20, 60, 0.6, 4)
        yield 0.4
        self.x, self.y = free_tile_pos(self.run.room, random, (self.p.x, self.p.y), 90, True)
        burst(self.run, self.x, self.y, (30, 20, 40), 20, 60, 0.6, 4)
        self.alpha = 255
        self.invuln = False
        self.ring(12, 95, 0, (160, 100, 220))
        yield 0.4

    def a_tail(self):
        for k in range(4):
            self.fan(3, 0.3, 125, (110, 230, 90), x=self.x - 12 * (1 if self.dir[0] >= 0 else -1), y=self.y - 6)
            yield 0.3

    def a_storm(self):
        for i in range(12):
            a = i * 0.55
            self.hazard(CX + math.cos(a) * (40 + i * 10), CY + math.sin(a) * (20 + i * 6), 14, 0.6, 0.15, 'strike')
            yield 0.08
        yield 0.6

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        f = 1 if self.dir[0] >= 0 else -1
        # Schlangenschwanz
        pts = [(x - f * 12 - f * i * 3, y - 2 + math.sin(t * 6 + i * 0.7) * 3 - i) for i in range(8)]
        D.lines(s, (90, 170, 80), False, pts, 3)
        D.circle(s, (90, 170, 80), (int(pts[-1][0]), int(pts[-1][1])), 3)
        D.ellipse(s, (30, 20, 10), (x - 15, y - 9, 30, 19))
        D.ellipse(s, (230, 170, 60), (x - 14, y - 8, 28, 17))
        for i in range(4):
            D.line(s, (40, 20, 10), (x - 9 + i * 6, y - 8), (x - 7 + i * 6, y + 5), 2)
        for lx in (-10, -4, 4, 10):
            D.rect(s, (200, 140, 50), (x + lx - 1, y + 6, 3, 6))
        hx = x + f * 13
        D.circle(s, (120, 80, 50), (hx, y - 8), 7)
        D.circle(s, (230, 190, 160), (hx + f * 2, y - 7), 4)
        eyes(s, hx + f * 2, y - 9, 2, (255, 60, 60), 1)


# =====================================================================  EBENE 3
class Sojobo(Boss):
    sheet = ('boss_sojobo', 1, None)

    r = 13

    def setup(self):
        self.attacks = ['fan', 'gust', 'crows', 'dive']
        self.attacks2 = ['fan', 'gust', 'crows', 'dive', 'storm']
        self.a = 0.0

    def move(self, dt):
        if self.co is None or self.last != 'dive':
            self.a += dt * 0.7
            tx = CX + math.cos(self.a) * 130
            ty = CY - 30 + math.sin(self.a * 2) * 40
            self.x += (tx - self.x) * min(1, dt * 2)
            self.y += (ty - self.y) * min(1, dt * 2)

    def a_fan(self):
        for k in range(2):
            self.fan(9, 0.16, 40, (240, 240, 240), r=3, acc=1.4)
            yield 0.6

    def a_gust(self):
        audio.play('dash')
        d = norm(self.p.x - self.x, self.p.y - self.y)
        self.run.wind = (d[0] * 110, d[1] * 110, 1.6)
        for i in range(8):
            self.fan(1, 0, 150, (180, 230, 180), ang=self.ang_p() + random.uniform(-0.6, 0.6))
            yield 0.2

    def a_crows(self):
        self.summon('karasu', 3 if self.phase == 1 else 4, 30)
        yield 0.8

    def a_dive(self):
        tx, ty = self.p.x, self.p.y
        yield 0.3
        for i in range(14):
            self.x += (tx - self.x) * 0.22
            self.y += (ty - self.y) * 0.22
            yield 0.03
        self.ring(12, 100, 0, (240, 240, 240))
        yield 0.4

    def a_storm(self):
        for i in range(40):
            for k in range(4):
                ebullet(self.run, self.x, self.y, i * 0.2 + k * math.pi / 2, 90, (200, 240, 200), curve=0.6)
            yield 0.06

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y + math.sin(t * 3) * 2)
        flap = math.sin(t * 8) * 6
        for side in (-1, 1):
            pts = [(x + side * 4, y - 4), (x + side * 30, y - 16 - flap), (x + side * 34, y - 2 - flap), (x + side * 22, y + 8)]
            D.polygon(s, (30, 30, 40), pts)
            for i in range(3):
                D.line(s, (60, 60, 80), (x + side * 6, y), (x + side * (20 + i * 5), y - 10 - flap + i * 5), 1)
        D.polygon(s, (240, 240, 230), [(x - 9, y - 4), (x + 9, y - 4), (x + 11, y + 14), (x - 11, y + 14)])
        D.rect(s, (230, 120, 40), (x - 9, y + 2, 18, 3))
        D.circle(s, (240, 240, 240), (x, y - 6), 10)
        D.circle(s, (220, 50, 40), (x, y - 9), 7)
        D.polygon(s, (220, 50, 40), [(x - 1, y - 9), (x + 1, y - 9), (x, y)])
        D.rect(s, (20, 20, 20), (x - 4, y - 21, 8, 5))
        eyes(s, x, y - 11, 3, (255, 240, 120), 1)


class Raiju(Boss):
    sheet = ('boss_raiju', 2, None)

    r = 12

    def setup(self):
        self.attacks = ['bounce', 'strikes', 'bolt']
        self.attacks2 = ['bounce', 'strikes', 'bolt', 'follow']
        self.v = (0, 0)

    def a_bounce(self):
        a = self.ang_p()
        vx, vy = math.cos(a) * 240, math.sin(a) * 240
        hits = 0
        for i in range(120):
            self.x, self.y, bx, by = move_body(self.run.room, self.x, self.y, 11, vx * 0.02, vy * 0.02, True)
            self.v = (vx, vy)
            if bx: vx = -vx
            if by: vy = -vy
            if bx or by:
                hits += 1
                self.fan(5, 0.35, 110, (255, 240, 120))
                self.run.shake(2)
                if hits >= (4 if self.phase == 1 else 6):
                    break
            if i % 4 == 0:
                ebullet(self.run, self.x, self.y, random.uniform(0, math.tau), 40, (200, 220, 255), r=2)
            yield 0.02
        yield 0.4

    def a_strikes(self):
        horiz = random.random() < 0.5
        for k in range(6):
            if horiz:
                y = RY + 20 + k * 37
                for x in range(int(RX + 20), int(RX + RW), 40):
                    if random.random() < 0.75:
                        self.hazard(x, y, 13, 0.8, 0.15, 'strike')
            else:
                x = RX + 20 + k * 75
                for y in range(int(RY + 20), int(RY + RH), 40):
                    if random.random() < 0.75:
                        self.hazard(x, y, 13, 0.8, 0.15, 'strike')
            yield 0.35

    def a_bolt(self):
        for k in range(3):
            self.ring(18, 140, k * 0.17, (255, 240, 120), r=2)
            yield 0.3

    def a_follow(self):
        for i in range(10):
            self.hazard(self.p.x, self.p.y, 15, 0.55, 0.15, 'strike')
            yield 0.22

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        gfx.draw_glow(s, x, y, 26, (150, 200, 255), 80)
        f = 1 if self.v[0] >= 0 else -1
        D.ellipse(s, (20, 30, 60), (x - 15, y - 8, 30, 17))
        D.ellipse(s, (120, 170, 240), (x - 14, y - 7, 28, 15))
        for i in range(5):
            zx = x - 10 + i * 5
            D.lines(s, (255, 240, 120), False, [(zx, y - 7), (zx + 2, y - 2), (zx - 1, y + 1), (zx + 1, y + 6)], 1)
        D.circle(s, (130, 180, 250), (x + f * 14, y - 6), 7)
        D.polygon(s, (130, 180, 250), [(x + f * 10, y - 12), (x + f * 12, y - 18), (x + f * 15, y - 11)])
        eyes(s, x + f * 15, y - 7, 2, (255, 255, 160), 1)
        tail = [(x - f * 14 - f * i * 4, y - 4 - i * 2 + (i % 2) * 4) for i in range(5)]
        D.lines(s, (255, 240, 120), False, tail, 2)
        for lx in (-9, -3, 3, 9):
            D.rect(s, (90, 140, 220), (x + lx - 1, y + 6, 3, 5))


class YukiOnna(Boss):
    sheet = ('boss_yuki_onna', 1, None)

    def render_extra(self, s, t):
        if random.random() < 0.3:
            self.run.particles.append(Particle(self.x + random.uniform(-14, 14), self.y + 14, random.uniform(-10, 10), 15, 0.6, (230, 250, 255), 1))

    r = 11

    def setup(self):
        self.attacks = ['spiral', 'blizzard', 'breath', 'icicles']
        self.attacks2 = ['spiral', 'blizzard', 'breath', 'icicles', 'teleport']

    def move(self, dt):
        self.y += math.sin(self.t * 2) * 6 * dt

    def a_teleport(self):
        self.alpha = 100
        yield 0.25
        self.x, self.y = free_tile_pos(self.run.room, random, (self.p.x, self.p.y), 100, True)
        self.alpha = 255
        self.ring(14, 90, 0, (200, 240, 255), eff='slow')
        yield 0.3

    def a_spiral(self):
        if self.phase == 2:
            yield from self.a_teleport()
        for i in range(36):
            for k in range(3):
                ebullet(self.run, self.x, self.y, i * 0.22 + k * math.tau / 3, 80, (200, 240, 255), eff='slow' if k == 0 else None)
            yield 0.06

    def a_blizzard(self):
        left = random.random() < 0.5
        for wave in range(5):
            gap = random.randint(1, 5)
            for row in range(7):
                if abs(row - gap) <= 0:
                    continue
                y = RY + 16 + row * 32
                x = RX + 4 if left else RX + RW - 4
                ebullet(self.run, x, y, 0 if left else math.pi, 95, (230, 250, 255), 4)
            yield 0.65

    def a_breath(self):
        a0 = self.ang_p()
        for i in range(24):
            ebullet(self.run, self.x, self.y, a0 + random.uniform(-0.35, 0.35), random.uniform(90, 140), (200, 240, 255), 2, eff='slow')
            yield 0.04

    def a_icicles(self):
        for i in range(6):
            self.hazard(self.p.x + random.uniform(-40, 40), self.p.y + random.uniform(-30, 30), 13, 0.7, 0.15, 'ice')
            yield 0.15
        yield 0.5

    def render(self, s, t):
        gfx.draw_glow(s, int(self.x), int(self.y), 30, (180, 230, 255), 90)
        art.draw_big(s, 'yuki_onna_b', self.x, self.y - 4, 1.2, flip=self.p.x < self.x)
        if random.random() < 0.3:
            self.run.particles.append(Particle(self.x + random.uniform(-14, 14), self.y + 14, random.uniform(-10, 10), 15, 0.6, (230, 250, 255), 1))
        return
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        gfx.draw_glow(s, x, y, 28, (180, 230, 255), 90)
        D.polygon(s, (240, 248, 255), [(x - 6, y - 6), (x + 6, y - 6), (x + 14, y + 16), (x - 14, y + 16)])
        D.line(s, (150, 200, 240), (x, y - 6), (x - 4, y + 16), 1)
        D.rect(s, (140, 190, 240), (x - 8, y, 16, 3))
        D.circle(s, (20, 10, 30), (x, y - 11), 8)
        D.rect(s, (20, 10, 30), (x - 9, y - 12, 4, 22)); D.rect(s, (20, 10, 30), (x + 5, y - 12, 4, 22))
        D.circle(s, (250, 250, 255), (x, y - 10), 5)
        D.circle(s, (120, 200, 255), (x - 2, y - 10), 1); D.circle(s, (120, 200, 255), (x + 2, y - 10), 1)
        if random.random() < 0.3:
            self.run.particles.append(Particle(x + random.uniform(-14, 14), y + 14, random.uniform(-10, 10), 15, 0.6, (230, 250, 255), 1))


# =====================================================================  EBENE 4
class Umibozu(Boss):
    sheet = ('boss_umibozu', 1, None)

    r = 22

    def setup(self):
        self.attacks = ['wall', 'rings', 'rain', 'eyes']
        self.attacks2 = ['wall', 'rings', 'rain', 'eyes', 'dive']
        self.y = CY - 20

    def a_dive(self):
        self.hidden = True
        yield 0.6
        self.x, self.y = free_tile_pos(self.run.room, random, (self.p.x, self.p.y), 120, True)
        self.x = clamp(self.x, RX + 30, RX + RW - 30)
        self.y = clamp(self.y, RY + 30, RY + RH - 30)
        yield 0.5
        self.hidden = False
        audio.play('splash')
        self.ring(20, 90, 0, (110, 170, 230))
        yield 0.4

    def a_wall(self):
        for wave in range(4):
            gap = random.randint(1, 10)
            left = wave % 2 == 0
            for col in range(13):
                if abs(col - gap) <= 1:
                    continue
                x = RX + 16 + col * 32
                ebullet(self.run, x, RY + 4 if left else RY + RH - 4, math.pi / 2 if left else -math.pi / 2, 80, (90, 140, 220), 4)
            yield 0.9

    def a_rings(self):
        for k in range(4):
            self.ring(18, 75 + k * 10, k * 0.1, (90, 140, 220), 4)
            yield 0.45

    def a_rain(self):
        for i in range(10):
            self.hazard(random.uniform(RX + 20, RX + RW - 20), random.uniform(RY + 20, RY + RH - 20), 16, 1.0, 0.2, 'water')
            yield 0.1
        yield 0.5

    def a_eyes(self):
        for k in range(6):
            self.fan(2, 0.06, 190, (255, 255, 255), x=self.x, y=self.y - 6)
            yield 0.25

    def draw_hidden(self, s, t):
        for i in range(3):
            r = int((t * 30 + i * 12) % 36)
            pygame.draw.circle(s, (150, 200, 230), (int(self.x), int(self.y)), r, 1)

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        D.ellipse(s, (60, 100, 140), (x - 32, y + 10, 64, 14))
        D.ellipse(s, (10, 10, 20), (x - 24, y - 30, 48, 50))
        D.rect(s, (10, 10, 20), (x - 24, y - 6, 48, 22))
        for i in range(5):
            D.circle(s, (180, 220, 240), (x - 20 + i * 10, y + 16 + int(math.sin(t * 4 + i) * 2)), 2)
        gfx.draw_glow(s, x - 9, y - 10, 9, (255, 255, 255), 150)
        gfx.draw_glow(s, x + 9, y - 10, 9, (255, 255, 255), 150)
        D.circle(s, (250, 250, 250), (x - 9, y - 10), 4)
        D.circle(s, (250, 250, 250), (x + 9, y - 10), 4)


class Ryujin(Omukade):
    r = 12

    def setup(self):
        super().setup()
        self.segs = 16
        self.speed = 85
        self.attacks = ['pearls', 'breath', 'coil', 'tidal']
        self.attacks2 = ['pearls', 'breath', 'coil', 'tidal', 'rush']

    def hitboxes(self):
        return [(self.x, self.y, 12)] + [(x, y, 8) for x, y in self.seg_pos()]

    def a_pearls(self):
        for k in range(3 if self.phase == 1 else 5):
            b = ebullet(self.run, self.x, self.y, self.ang_p() + random.uniform(-0.8, 0.8), 70, (150, 230, 255), 5)
            b.fl = {'ehoming': 1}
            yield 0.3

    def a_breath(self):
        for i in range(20):
            self.fan(1, 0, 160, (120, 220, 255), ang=self.ang_p() + math.sin(i * 0.5) * 0.25)
            yield 0.05

    def a_coil(self):
        for k in range(3):
            self.ring(20, 80, k * 0.15, (100, 200, 170))
            yield 0.35

    def a_tidal(self):
        for i in range(12):
            a = i / 12 * math.tau
            ebullet(self.run, CX + math.cos(a) * 200, CY + math.sin(a) * 110, a + math.pi, 70, (90, 160, 230), 4)
        yield 1.0

    def render(self, s, t):
        segs = self.seg_pos()
        pts = [(self.x - math.cos(self.heading) * 6, self.y - math.sin(self.heading) * 6)] + list(segs)
        n = len(pts)
        radii = [7.5 - 5.5 * (i / max(1, n - 1)) ** 1.3 for i in range(n)]
        hi_tube(pts, radii, JADE, belly=(150, 140, 96), spikes=((236, 196, 80), 10), fin=((236, 196, 80), (255, 240, 170)), scales=True)
        hx, hy = int(self.x), int(self.y)
        sheets.blit_center(s, 'boss_ryujin_head', hx, hy, sheets.hdir(math.cos(self.heading)), self.af('boss_ryujin_head', t, 8, 0))
        return
        hd = self.heading
        for side in (-1, 1):
            a = hd + math.pi + side * 0.5
            D.line(s, (240, 220, 140), (hx, hy), (hx + math.cos(a) * 16, hy + math.sin(a) * 16), 3)
            a2 = hd + side * 0.9
            D.line(s, (250, 250, 230), (hx, hy), (hx + math.cos(a2) * 20 + math.sin(t * 3) * 3, hy + math.sin(a2) * 20), 1)
        eyes(s, hx + math.cos(hd) * 5, hy + math.sin(hd) * 5 - 2, 4, (255, 80, 60), 2)


class BakeKujira(Boss):
    sheet = ('boss_bake_kujira', 1, None)

    def face_dir(self):
        return sheets.RIGHT if self.face > 0 else sheets.LEFT

    r = 18

    def setup(self):
        self.attacks = ['charge', 'bubbles', 'bones', 'spout']
        self.attacks2 = ['charge', 'bubbles', 'bones', 'spout', 'charge']
        self.face = 1

    def hitboxes(self):
        return [(self.x + self.face * 12, self.y, 16), (self.x - self.face * 14, self.y, 12)]

    def a_charge(self):
        self.face = 1 if self.p.x > self.x else -1
        yield 0.4
        sp = 300 * self.face
        for i in range(80):
            self.x += sp * 0.02
            if i % 3 == 0:
                ebullet(self.run, self.x, self.y + 8, math.pi / 2, 40, (200, 230, 255), 2)
                ebullet(self.run, self.x, self.y - 8, -math.pi / 2, 40, (200, 230, 255), 2)
            if self.x < RX - 60 or self.x > RX + RW + 60:
                break
            yield 0.02
        self.hidden = True
        yield 0.5
        self.y = clamp(self.p.y, RY + 30, RY + RH - 30)
        self.face = -self.face
        self.x = RX - 40 if self.face > 0 else RX + RW + 40
        self.hidden = False
        sp = 280 * self.face
        for i in range(60):
            self.x += sp * 0.02
            if (self.face > 0 and self.x > CX + random.uniform(-60, 60)) or (self.face < 0 and self.x < CX + random.uniform(-60, 60)):
                break
            yield 0.02
        yield 0.3

    def a_bubbles(self):
        for k in range(3):
            self.ring(14, 70, k * 0.2, (180, 220, 255), 4, acc=0.3)
            yield 0.5

    def a_bones(self):
        for i in range(14):
            ebullet(self.run, random.uniform(RX + 10, RX + RW - 10), RY + 4, math.pi / 2, 50, (230, 225, 210), 3, acc=1.0)
            yield 0.1

    def a_spout(self):
        for i in range(18):
            ebullet(self.run, self.x, self.y - 10, -math.pi / 2 + random.uniform(-0.9, 0.9), random.uniform(120, 170), (120, 190, 255), 3, ay=160)
            yield 0.06
        yield 0.5

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        f = self.face
        bone = (230, 226, 210)
        gfx.draw_glow(s, x, y, 34, (40, 70, 110), 120)
        for i in range(6):
            rx = x - f * 22 + f * i * 7
            D.arc(s, bone, (rx - 4, y - 14, 8, 28), -1.5, 1.5, 2) if f > 0 else D.arc(s, bone, (rx - 4, y - 14, 8, 28), 1.6, 4.7, 2)
        D.line(s, bone, (x - f * 30, y), (x + f * 10, y), 3)
        D.polygon(s, bone, [(x - f * 30, y), (x - f * 40, y - 9), (x - f * 40, y + 9)])
        D.ellipse(s, bone, (x + f * 8 - 10, y - 13, 26, 24))
        D.circle(s, (20, 20, 30), (x + f * 16, y - 3), 4)
        gfx.draw_glow(s, x + f * 16, y - 3, 6, (120, 200, 255), 140)


# =====================================================================  EBENE 5
class Orochi(Boss):
    r = 18

    def setup(self):
        self.y = RY + 40
        self.attacks = ['heads', 'breath', 'bite', 'ring']
        self.attacks2 = ['heads', 'breath', 'bite', 'ring', 'spiral']
        self.lunge = -1
        self.lunge_pos = None

    def head_pos(self, i):
        a = math.pi * (0.1 + 0.8 * i / 7)
        L = 62 + math.sin(self.t * 2 + i) * 8
        x = self.x + math.cos(a) * L * 1.6
        y = self.y + math.sin(a) * L
        if i == self.lunge and self.lunge_pos:
            x, y = self.lunge_pos
        return x, y

    def hitboxes(self):
        return [(self.x, self.y, 18)] + [self.head_pos(i) + (8,) for i in range(8)]

    def move(self, dt):
        self.x = CX + math.sin(self.t * 0.4) * 40

    def a_heads(self):
        for i in range(8):
            x, y = self.head_pos(i)
            self.fan(3, 0.25, 110, (255, 120, 60), x=x, y=y)
            yield 0.15

    def a_breath(self):
        for k in range(18):
            for i in range(0, 8, 2 if self.phase == 1 else 1):
                x, y = self.head_pos(i)
                if k % 3 == 0:
                    ebullet(self.run, x, y, math.atan2(self.p.y - y, self.p.x - x) + random.uniform(-0.15, 0.15), 120, (255, 160, 60), 2)
            yield 0.06

    def a_bite(self):
        i = random.randrange(8)
        self.lunge = i
        sx, sy = self.head_pos(i)
        self.lunge_pos = (sx, sy)
        tx, ty = self.p.x, self.p.y
        yield 0.3
        for k in range(10):
            lx, ly = self.lunge_pos
            self.lunge_pos = (lx + (tx - lx) * 0.3, ly + (ty - ly) * 0.3)
            yield 0.03
        x, y = self.lunge_pos
        self.ring(10, 90, 0, (120, 220, 120), x=x, y=y)
        yield 0.35
        self.lunge = -1
        self.lunge_pos = None

    def a_ring(self):
        for k in range(3):
            self.ring(20, 85, k * 0.16, (200, 60, 60), 4)
            yield 0.4

    def a_spiral(self):
        for k in range(40):
            for i in (1, 6):
                x, y = self.head_pos(i)
                ebullet(self.run, x, y, k * 0.3 * (1 if i == 1 else -1), 90, (120, 220, 120))
            yield 0.05

    def render(self, s, t):
        x, y = self.x, self.y
        # zusammengerollter Leib (drei Windungen)
        for k, (rx, ry, rad) in enumerate(((26, 12, 8), (19, 8, 7.5), (11, 5, 7))):
            pts = []
            for j in range(25):
                a = math.pi * 0.15 + j / 24 * math.pi * 1.9
                pts.append((x + math.cos(a) * rx, y + 6 - k * 7 + math.sin(a) * ry))
            hi_tube(pts, [rad] * len(pts), SNAKE, belly=(120, 118, 70), scales=True)
        # acht Hälse
        order = sorted(range(8), key=lambda i: self.head_pos(i)[1])
        for i in order:
            hx, hy = self.head_pos(i)
            pts = []
            for k in range(9):
                f = k / 8
                cx = x + (hx - x) * f + math.sin(f * 5 + t * 3 + i) * 4 * (1 - f)
                cy = y - 10 + (hy - y + 10) * f - math.sin(f * math.pi) * 8
                pts.append((cx, cy))
            hi_tube(pts, [5.5 - 1.8 * k / 8 for k in range(9)], SNAKE, belly=(120, 118, 70), scales=True)
            sheets.blit_center(s, 'boss_orochi_head', hx, hy, sheets.hdir(self.p.x - hx), self.af('boss_orochi_head', t, 6, i))




class ShutenDoji(Boss):
    sheet = ('boss_shuten_doji', 1, None)          # Kalebasse und Sake-Schale sind Teil des Sprites

    r = 15

    def setup(self):
        self.attacks = ['charge', 'gourd', 'summon', 'quake']
        self.attacks2 = ['charge', 'gourd', 'summon', 'quake', 'gourd']
        self.face = 1

    def move(self, dt):
        if self.co is None:
            d = norm(self.p.x - self.x, self.p.y - self.y)
            self.x, self.y, _, _ = move_body(self.run.room, self.x, self.y, 14, d[0] * 30 * dt, d[1] * 30 * dt, True)
            self.face = 1 if d[0] >= 0 else -1

    def a_charge(self):
        for k in range(2 if self.phase == 1 else 3):
            d = norm(self.p.x - self.x, self.p.y - self.y)
            self.face = 1 if d[0] >= 0 else -1
            yield 0.4
            for i in range(40):
                self.x, self.y, bx, by = move_body(self.run.room, self.x, self.y, 14, d[0] * 6, d[1] * 6, True)
                if bx or by:
                    self.run.shake(6)
                    self.ring(12, 90, 0, (255, 90, 60))
                    break
                yield 0.02
            yield 0.3

    def a_gourd(self):
        tx, ty = self.p.x, self.p.y
        self.hazard(tx, ty, 30, 0.9, 0.1, 'fire')
        b = ebullet(self.run, self.x, self.y, math.atan2(ty - self.y, tx - self.x),
                    math.hypot(tx - self.x, ty - self.y) / 0.9 / self.run.bullet_speed_mult, (230, 70, 50), 6)
        b.life = 0.9
        yield 0.9
        self.ring(16, 100, 0, (255, 140, 60), x=tx, y=ty)
        self.run.explode(tx, ty, 26, 0, 'e')
        yield 0.5

    def a_summon(self):
        self.summon('shikome', 2, 30)
        if self.phase == 2:
            self.summon('oni', 1, 20)
        yield 0.8

    def a_quake(self):
        for k in range(3):
            self.ring(24, 70 + k * 15, k * 0.13, (200, 160, 120), 3)
            self.run.shake(5)
            for j in range(3):
                self.hazard(random.uniform(RX + 20, RX + RW - 20), random.uniform(RY + 20, RY + RH - 20), 14, 0.8, 0.15, 'slam')
            yield 0.6

    def render(self, s, t):
        art.draw_big(s, 'shuten', self.x, self.y - 6, 1.6, flip=self.face < 0)
        return
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        f = self.face
        D.ellipse(s, (30, 10, 10), (x - 17, y - 13, 34, 32))
        D.ellipse(s, (200, 50, 40), (x - 16, y - 12, 32, 30))
        D.rect(s, (240, 200, 70), (x - 14, y + 6, 28, 8))
        for i in range(4):
            D.line(s, (30, 20, 10), (x - 12 + i * 8, y + 6), (x - 10 + i * 8, y + 13), 2)
        D.circle(s, (220, 60, 50), (x, y - 14), 11)
        D.ellipse(s, (240, 240, 240), (x - 13, y - 28, 26, 12))
        D.polygon(s, (250, 230, 120), [(x - 7, y - 22), (x - 11, y - 34), (x - 3, y - 23)])
        D.polygon(s, (250, 230, 120), [(x + 7, y - 22), (x + 11, y - 34), (x + 3, y - 23)])
        eyes(s, x, y - 15, 4, (255, 240, 80), 2)
        D.line(s, (240, 240, 240), (x - 4, y - 8), (x + 4, y - 8), 1)
        # Kalebasse
        gx = x + f * 18
        D.circle(s, (220, 60, 50), (gx, y + 2), 5); D.circle(s, (220, 60, 50), (gx, y - 5), 3)


class Tamamo(Boss):
    sheet = ('boss_tamamo', 2, None)

    def render_sheet(self, s, t):
        gfx.draw_glow(s, int(self.x), int(self.y), 34 if self.phase == 1 else 46, (255, 190, 90) if self.phase == 1 else (110, 170, 255), 60)
        if self.phase == 2:                                   # wahre Gestalt: Fuchsfeuer kreist um sie
            for i in range(6):
                a = t * 1.6 + i / 6 * math.tau
                fx, fy = self.x + math.cos(a) * 26, self.y - 6 + math.sin(a) * 12
                gfx.draw_glow(s, int(fx), int(fy), 7, (120, 180, 255), 150)
        sheets.blit_center(s, 'boss_tamamo', self.x, self.y - 6, self.face_dir(), self.af('boss_tamamo', t, 7, 0), 2)

    r = 11

    def setup(self):
        self.attacks = ['foxfire', 'illusion', 'tails', 'blink']
        self.attacks2 = ['foxfire', 'illusion', 'tails', 'blink', 'foxfire']
        self.orbs = []

    def on_phase2(self):
        self.r = 14

    def move(self, dt):
        self.y += math.sin(self.t * 1.7) * 8 * dt
        self.x += math.cos(self.t * 0.9) * 12 * dt
        self.clamp_pos(20)

    def a_foxfire(self):
        n = 9
        for k in range(30):
            pass
        bullets = []
        for i in range(n):
            a = i / n * math.tau
            b = ebullet(self.run, self.x + math.cos(a) * 24, self.y + math.sin(a) * 24, 0, 0.0, (120, 180, 255), 4)
            b.life = 99
            bullets.append((b, a))
        for k in range(25):
            for b, a in bullets:
                aa = a + k * 0.12
                b.x, b.y = self.x + math.cos(aa) * 24, self.y + math.sin(aa) * 24
            yield 0.03
        for b, a in bullets:
            ang = math.atan2(self.p.y - b.y, self.p.x - b.x)
            sp = 140 * self.run.bullet_speed_mult
            b.vx, b.vy = math.cos(ang) * sp, math.sin(ang) * sp
            b.life = 5
            yield 0.1

    def a_illusion(self):
        for i in range(2 if self.phase == 1 else 3):
            self.summon('kitsunebi_e', 1, 60)
        yield 0.6

    def a_tails(self):
        for i in range(30):
            for k in range(9):
                ebullet(self.run, self.x, self.y, i * 0.13 + k * math.tau / 9, 75, (250, 170, 70), 2)
            yield 0.1

    def a_blink(self):
        for k in range(3):
            self.alpha = 80
            yield 0.15
            self.x, self.y = free_tile_pos(self.run.room, random, (self.p.x, self.p.y), 80, True)
            self.alpha = 255
            self.fan(5, 0.25, 130, (250, 120, 160))
            yield 0.3

    def render(self, s, t):
        gfx.draw_glow(s, int(self.x), int(self.y), 34, (255, 190, 90), 60)
        if self.phase == 2:
            art.draw_big(s, 'kitsunebi_e', self.x, self.y - 4, 2.0, flip=self.p.x > self.x)
        else:
            art.draw_big(s, 'tamamo_b', self.x, self.y - 6, 1.3, flip=self.p.x < self.x)
        return
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        big = self.phase == 2
        for i in range(9):
            a = math.pi * (1.1 + i / 8 * 0.8) + math.sin(t * 2 + i) * 0.06
            L = 26 if big else 20
            tx, ty = x + math.cos(a) * L, y + 4 + math.sin(a) * L
            D.line(s, (240, 170, 60), (x, y + 4), (tx, ty), 5)
            D.circle(s, (255, 250, 240), (int(tx), int(ty)), 3)
        gfx.draw_glow(s, x, y, 30, (255, 190, 90), 60)
        if big:
            D.ellipse(s, (250, 200, 120), (x - 14, y - 10, 28, 22))
            D.polygon(s, (250, 200, 120), [(x - 10, y - 6), (x - 12, y - 18), (x - 4, y - 9)])
            D.polygon(s, (250, 200, 120), [(x + 10, y - 6), (x + 12, y - 18), (x + 4, y - 9)])
            eyes(s, x, y - 3, 5, (255, 80, 80), 2)
        else:
            D.polygon(s, (190, 40, 70), [(x - 6, y - 4), (x + 6, y - 4), (x + 12, y + 14), (x - 12, y + 14)])
            D.rect(s, (250, 210, 90), (x - 7, y + 1, 14, 3))
            D.circle(s, (20, 10, 20), (x, y - 9), 7)
            D.circle(s, (250, 230, 220), (x, y - 8), 5)
            D.polygon(s, (250, 250, 250), [(x - 6, y - 12), (x - 8, y - 19), (x - 3, y - 14)])
            D.polygon(s, (250, 250, 250), [(x + 6, y - 12), (x + 8, y - 19), (x + 3, y - 14)])
            D.circle(s, (200, 40, 60), (x - 2, y - 8), 1); D.circle(s, (200, 40, 60), (x + 2, y - 8), 1)


# =====================================================================  EBENE 6
class Mikaboshi(Boss):
    r = 17
    sheet = ('boss_mikaboshi', 2, None)

    def setup(self):
        self.attacks = ['starburst', 'lasers', 'meteor', 'constellation']
        self.attacks2 = ['starburst', 'lasers', 'meteor', 'constellation', 'blackhole']
        self.y = CY - 20

    def move(self, dt):
        self.x = CX + math.sin(self.t * 0.5) * 100
        self.y = CY - 30 + math.sin(self.t * 0.8) * 25

    def a_starburst(self):
        for k in range(3):
            off = self.t + k * 0.3
            for i in range(5):
                a = off + i / 5 * math.tau
                for j in range(7):
                    sp = 60 + j * 14
                    ebullet(self.run, self.x, self.y, a, sp, (200, 150, 255), 3)
            yield 0.6

    def a_lasers(self):
        arms = 3 if self.phase == 1 else 5
        for i in range(60):
            for k in range(arms):
                ebullet(self.run, self.x, self.y, i * 0.05 + k * math.tau / arms, 160, (255, 240, 255), 2)
            yield 0.04

    def a_meteor(self):
        for i in range(10):
            x = self.p.x + random.uniform(-60, 60)
            y = self.p.y + random.uniform(-40, 40)
            self.hazard(x, y, 18, 0.9, 0.2, 'meteor')
            yield 0.12
        yield 0.5

    def a_constellation(self):
        bs = []
        for i in range(8):
            a = i / 8 * math.tau
            b = ebullet(self.run, self.x, self.y, a, 120, (255, 250, 200), 4, acc=-1.5)
            bs.append(b)
        yield 1.0
        for b in bs:
            if b in self.run.ebullets:
                for j in range(6):
                    ebullet(self.run, b.x, b.y, j / 6 * math.tau + random.random(), 90, (255, 220, 120), 2)
                b.life = 0
        yield 0.5

    def a_blackhole(self):
        self.run.wind = (0, 0, 0)
        for i in range(50):
            d = norm(self.x - self.p.x, self.y - self.p.y)
            self.run.wind = (d[0] * 70, d[1] * 70, 0.1)
            if i % 5 == 0:
                self.ring(10, 70, i * 0.1, (150, 80, 220))
            yield 0.05

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        gfx.draw_glow(s, x, y, 46, (160, 100, 255), 90)
        for i in range(8):
            a = t * 0.8 + i / 8 * math.tau
            L = 30 + math.sin(t * 3 + i) * 5
            D.line(s, (230, 210, 255), (x, y), (x + math.cos(a) * L, y + math.sin(a) * L), 2)
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i / 10 * math.tau + t * 0.3
            r = 20 if i % 2 == 0 else 9
            pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        D.polygon(s, (60, 20, 100), pts)
        D.polygon(s, (220, 190, 255), pts, 2)
        D.circle(s, (20, 0, 40), (x, y), 8)
        eyes(s, x, y, 3, (255, 250, 200), 2)
        if self.phase == 2:
            for i in range(3):
                a = -t * 1.3 + i / 3 * math.tau
                D.circle(s, (255, 240, 200), (int(x + math.cos(a) * 40), int(y + math.sin(a) * 24)), 3)


# =====================================================================  RUNDE 1: NEUE BOSSE
class Oonyudo(Boss):
    sheet = ('boss_oonyudo', 2, None)

    def render_sheet(self, s, t):
        gfx.draw_glow(s, int(self.x), int(self.y), int(40 * self.size), (80, 60, 120), 70)
        sheets.blit_center(s, 'boss_oonyudo', self.x, self.y - 8, self.face_dir(), self.af('boss_oonyudo', t, 6, 0), 2 if self.phase == 1 else 3)

    """Ein riesiger Mönch, der immer größer wird."""
    r = 16

    def setup(self):
        self.attacks = ['stomp', 'beads', 'wisps', 'grow']
        self.attacks2 = ['stomp', 'beads', 'wisps', 'grow', 'shadow']
        self.size = 1.0
        self.y = CY - 20

    def move(self, dt):
        if self.co is None:
            d = norm(self.p.x - self.x, self.p.y - self.y)
            self.x += d[0] * 18 * dt
            self.y += d[1] * 12 * dt
            self.clamp_pos(24)

    def on_phase2(self):
        self.size = 1.35
        self.r = 21

    def a_stomp(self):
        for k in range(2 if self.phase == 1 else 3):
            yield 0.35
            self.run.shake(5)
            self.ring(16, 80 + k * 10, k * 0.2, (200, 160, 120))
            yield 0.4

    def a_beads(self):
        bs = []
        for i in range(10):
            a = i / 10 * math.tau
            b = ebullet(self.run, self.x, self.y, 0, 0.0, (190, 140, 90), 4)
            b.life = 99
            bs.append((b, a))
        for k in range(30):
            for b, a in bs:
                aa = a + k * 0.1
                b.x, b.y = self.x + math.cos(aa) * 34, self.y + math.sin(aa) * 26
            yield 0.03
        for b, a in bs:
            ang = math.atan2(b.y - self.y, b.x - self.x)
            sp = 100 * self.run.bullet_speed_mult
            b.vx, b.vy = math.cos(ang) * sp, math.sin(ang) * sp
            b.life = 5
        yield 0.5

    def a_wisps(self):
        self.summon('hitodama', 3, 40)
        yield 0.7

    def a_grow(self):
        for i in range(3):
            self.hazard(self.p.x, self.p.y, 22, 0.8, 0.15, 'slam')
            yield 0.35
        yield 0.5

    def a_shadow(self):
        for i in range(8):
            a = i / 8 * math.tau + self.t
            self.hazard(self.p.x + math.cos(a) * 50, self.p.y + math.sin(a) * 40, 16, 0.9, 0.15, 'slam')
        yield 1.2

    def render(self, s, t):
        gfx.draw_glow(s, int(self.x), int(self.y), int(40 * self.size), (80, 60, 120), 70)
        art.draw_big(s, 'oonyudo_b', self.x, self.y - 8, 1.6 * self.size)
        return
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        k = self.size
        gfx.draw_glow(s, x, y, int(40 * k), (80, 60, 120), 70)
        D.ellipse(s, (30, 20, 40), (x - int(20 * k), y - int(10 * k), int(40 * k), int(34 * k)))
        D.ellipse(s, (70, 50, 90), (x - int(19 * k), y - int(9 * k), int(38 * k), int(32 * k)))
        D.circle(s, (230, 190, 160), (x, y - int(16 * k)), int(12 * k))
        D.circle(s, (250, 210, 180), (x - int(3 * k), y - int(19 * k)), int(4 * k))
        eyes(s, x, y - int(16 * k), int(5 * k), (255, 230, 120), max(1, int(2 * k)))
        D.line(s, (120, 60, 50), (x - int(4 * k), y - int(9 * k)), (x + int(4 * k), y - int(9 * k)), 2)
        for i in range(9):
            a = math.pi * (0.15 + i / 8 * 0.7)
            D.circle(s, (170, 110, 60), (int(x + math.cos(a) * 15 * k), int(y - 4 * k + math.sin(a) * 8 * k)), max(2, int(3 * k)))


class Nurarihyon(Boss):
    sheet = ('boss_nurarihyon', 1, None)

    """Der Herr der Yokai – lässt andere kämpfen."""
    r = 11

    def setup(self):
        self.attacks = ['command', 'fan', 'tea', 'vanish']
        self.attacks2 = ['command', 'fan', 'tea', 'vanish', 'parade']
        self.y = RY + 60

    def move(self, dt):
        self.x += math.sin(self.t * 0.6) * 25 * dt

    def a_command(self):
        pool = self.run.biome['enemies']
        self.summon(random.choice(pool), 2, 50)
        yield 0.6
        for e in self.run.enemies:
            if e is not self and not e.dead and not e.is_boss:
                e.speed *= 1.3
        yield 0.5

    def a_fan(self):
        for k in range(3):
            self.fan(7, 0.2, 110, (220, 190, 120))
            yield 0.45

    def a_tea(self):
        for i in range(24):
            ebullet(self.run, self.x, self.y, i * 0.42, 70, (170, 220, 140), acc=0.6)
            yield 0.05

    def a_vanish(self):
        self.alpha = 60
        self.invuln = True
        yield 0.5
        self.x, self.y = free_tile_pos(self.run.room, random, (self.p.x, self.p.y), 100, True)
        self.alpha = 255
        self.invuln = False
        self.ring(14, 95, 0, (220, 190, 120))
        yield 0.4

    def a_parade(self):
        for i in range(10):
            y = RY + 20 + (i % 5) * 45
            left = i % 2 == 0
            x = RX + 6 if left else RX + RW - 6
            for j in range(3):
                ebullet(self.run, x, y + j * 8, 0 if left else math.pi, 90, (200, 120, 220), delay=j * 0.1)
            yield 0.25

    def render(self, s, t):
        art.draw_big(s, 'nurarihyon_b', self.x, self.y - 4, 1.2, flip=self.p.x < self.x)
        return
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        D.polygon(s, (60, 50, 90), [(x - 8, y - 2), (x + 8, y - 2), (x + 13, y + 15), (x - 13, y + 15)])
        D.polygon(s, (200, 170, 100), [(x - 3, y - 2), (x + 3, y - 2), (x + 2, y + 15), (x - 2, y + 15)])
        D.ellipse(s, (240, 220, 200), (x - 8, y - 22, 16, 22))
        D.circle(s, (240, 210, 190), (x, y - 6), 6)
        eyes(s, x, y - 7, 3, (40, 20, 20), 1)
        D.line(s, (180, 170, 160), (x - 4, y - 2), (x - 1, y + 2)); D.line(s, (180, 170, 160), (x + 4, y - 2), (x + 1, y + 2))
        D.line(s, (150, 110, 60), (x + 6, y), (x + 16, y - 8), 2)
        D.circle(s, (120, 120, 120), (x + 16, y - 9), 2)
        if int(t * 2) % 2:
            D.circle(s, (200, 200, 210), (x + 18, int(y - 14 - (t * 20) % 8)), 2, 1)


class KamaitachiTrio(Boss):
    """Drei Wiesel: eines bringt zu Fall, eines schneidet, eines heilt."""
    r = 8

    def setup(self):
        self.pos = [[CX - 60, CY - 30], [CX, CY - 50], [CX + 60, CY - 30]]
        self.attacks = ['trip', 'slash', 'whirl', 'heal']
        self.attacks2 = ['trip', 'slash', 'whirl', 'heal', 'tornado']
        self.a0 = 0.0

    def hitboxes(self):
        return [(p[0], p[1], 8) for p in self.pos]

    def move(self, dt):
        self.a0 += dt * (1.2 if self.phase == 1 else 1.8)
        if self.co is None:
            for i, p in enumerate(self.pos):
                a = self.a0 + i * math.tau / 3
                tx, ty = CX + math.cos(a) * 110, CY + math.sin(a) * 60
                p[0] += (tx - p[0]) * min(1, dt * 3)
                p[1] += (ty - p[1]) * min(1, dt * 3)
        self.x = sum(p[0] for p in self.pos) / 3
        self.y = sum(p[1] for p in self.pos) / 3

    def a_trip(self):
        p = self.pos[0]
        d = norm(self.p.x - p[0], self.p.y - p[1])
        yield 0.3
        for i in range(30):
            p[0] = clamp(p[0] + d[0] * 6, RX + 10, RX + RW - 10)
            p[1] = clamp(p[1] + d[1] * 6, RY + 10, RY + RH - 10)
            if i % 3 == 0:
                ebullet(self.run, p[0], p[1], math.atan2(d[1], d[0]) + math.pi / 2, 50, (230, 230, 240), 2)
                ebullet(self.run, p[0], p[1], math.atan2(d[1], d[0]) - math.pi / 2, 50, (230, 230, 240), 2)
            yield 0.02

    def a_slash(self):
        for k in range(3):
            p = self.pos[1]
            a = math.atan2(self.p.y - p[1], self.p.x - p[0])
            for j in range(6):
                ebullet(self.run, p[0], p[1], a, 150 + j * 18, (250, 250, 255), 2)
            yield 0.35

    def a_whirl(self):
        for k in range(40):
            for i, p in enumerate(self.pos):
                a = k * 0.16 + i * math.tau / 3
                p[0] = self.p.x + math.cos(a) * 80
                p[1] = self.p.y + math.sin(a) * 60
                p[0] = clamp(p[0], RX + 10, RX + RW - 10)
                p[1] = clamp(p[1], RY + 10, RY + RH - 10)
                if k % 8 == 0:
                    ebullet(self.run, p[0], p[1], math.atan2(self.p.y - p[1], self.p.x - p[0]), 90, (200, 220, 200))
            yield 0.04

    def a_heal(self):
        p = self.pos[2]
        gfx_t = 0
        for i in range(10):
            self.run.particles.append(Particle(p[0] + random.uniform(-8, 8), p[1], 0, -40, 0.6, (120, 255, 140), 2))
            yield 0.08
        self.hp = min(self.maxhp, self.hp + self.maxhp * 0.04)
        self.ring(10, 80, 0, (120, 255, 140), x=p[0], y=p[1])

    def a_tornado(self):
        for k in range(50):
            for i, p in enumerate(self.pos):
                ebullet(self.run, p[0], p[1], k * 0.3 + i * 2.1, 80, (190, 230, 190), 2, curve=0.8)
            yield 0.05

    def render(self, s, t):
        D = pygame.draw
        for i, (x, y) in enumerate(self.pos):
            gfx.shadow(s, (int(x) - 10, int(y) + 10, 20, 5))
            sheets.blit_center(s, 'kamaitachi', x, y, sheets.hdir(self.p.x - x), self.af('kamaitachi', t, 9, i), 1,
                               [(255, 255, 255), (230, 230, 255), (200, 255, 200)][i])
        return
        for i, (x, y) in enumerate(self.pos):
            x, y = int(x), int(y)
            gfx.shadow(s, (x - 8, y + 6, 16, 4))
            D.ellipse(s, (30, 20, 10), (x - 10, y - 6, 20, 13))
            D.ellipse(s, (180, 130, 80), (x - 9, y - 5, 18, 11))
            D.circle(s, (190, 140, 90), (x + 8, y - 6), 5)
            eyes(s, x + 9, y - 7, 2, (255, 255, 255), 1)
            col = [(230, 230, 240), (250, 250, 255), (140, 240, 150)][i]
            D.arc(s, col, (x - 14, y - 12, 16, 16), 1.0, 3.0, 2)
            D.line(s, (150, 100, 60), (x - 9, y), (x - 18, y - 6 + int(math.sin(t * 8 + i) * 3)), 3)


class Akkorokamui(Boss):
    sheet = ('boss_akkorokamui', 1, None)

    """Ein gewaltiger roter Krake aus dem Meer von Uchiura."""
    r = 20

    def setup(self):
        self.y = RY + 50
        self.attacks = ['tentacle', 'ink', 'ring', 'suction']
        self.attacks2 = ['tentacle', 'ink', 'ring', 'suction', 'storm']

    def move(self, dt):
        self.x = CX + math.sin(self.t * 0.5) * 70

    def a_tentacle(self):
        for k in range(4 if self.phase == 1 else 6):
            side = random.choice('lrb')
            if side == 'l':
                y = self.p.y
                for i in range(6):
                    self.hazard(RX + 16 + i * 32, y, 14, 0.7 + i * 0.05, 0.25, 'slam')
            elif side == 'r':
                y = self.p.y
                for i in range(6):
                    self.hazard(RX + RW - 16 - i * 32, y, 14, 0.7 + i * 0.05, 0.25, 'slam')
            else:
                x = self.p.x
                for i in range(5):
                    self.hazard(x, RY + RH - 16 - i * 32, 14, 0.7 + i * 0.05, 0.25, 'slam')
            yield 0.45

    def a_ink(self):
        a0 = self.ang_p()
        for i in range(30):
            ebullet(self.run, self.x, self.y + 10, a0 + random.uniform(-0.6, 0.6), random.uniform(60, 120), (60, 20, 40), 4, eff='slow')
            yield 0.03
        self.run.hazards.append(Hazard(self.p.x, self.p.y, 30, 0.2, 3.0, 0, 'e', 'smoke'))
        yield 0.4

    def a_ring(self):
        for k in range(3):
            self.ring(22, 80, k * 0.14, (230, 70, 80), 4)
            yield 0.4

    def a_suction(self):
        for i in range(40):
            d = norm(self.x - self.p.x, self.y - self.p.y)
            self.run.wind = (d[0] * 60, d[1] * 60, 0.1)
            if i % 6 == 0:
                self.fan(5, 0.3, 90, (230, 70, 80))
            yield 0.05

    def a_storm(self):
        for i in range(45):
            for k in range(4):
                ebullet(self.run, self.x, self.y, i * 0.17 + k * math.pi / 2, 85, (250, 120, 120), curve=-0.5)
            yield 0.05

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        for i in range(8):
            a = math.pi * (0.05 + i / 7 * 0.9)
            pts = []
            for j in range(9):
                f = j / 8
                L = 18 + f * 46
                aa = a + math.sin(t * 2.5 + i + f * 3) * 0.25 * f
                pts.append((x + math.cos(aa) * L * 1.3, y + 6 + math.sin(aa) * L))
            D.lines(s, (150, 30, 40), False, pts, 6)
            D.lines(s, (220, 70, 80), False, pts, 3)
            for j in range(2, 9, 2):
                D.circle(s, (250, 190, 190), (int(pts[j][0]), int(pts[j][1])), 1)
        D.ellipse(s, (120, 20, 30), (x - 24, y - 30, 48, 44))
        D.ellipse(s, (210, 60, 70), (x - 22, y - 28, 44, 40))
        D.ellipse(s, (240, 120, 120), (x - 12, y - 24, 14, 10))
        eyes(s, x, y - 2, 10, (255, 230, 120), 3)
        D.circle(s, (20, 10, 10), (x - 10, y - 2), 1); D.circle(s, (20, 10, 10), (x + 10, y - 2), 1)


class Enma(Boss):
    sheet = ('boss_enma', 1, None)

    """Enma-Daiō, König und Richter der Unterwelt."""
    r = 17

    def setup(self):
        self.y = RY + 55
        self.attacks = ['judgement', 'brush', 'summon', 'mirror']
        self.attacks2 = ['judgement', 'brush', 'summon', 'mirror', 'sentence']
        self.trail = []

    def move(self, dt):
        self.x = CX + math.sin(self.t * 0.35) * 50
        self.trail.append((self.p.x, self.p.y))
        del self.trail[:-240]

    def a_judgement(self):
        cols = random.sample(range(13), 5 if self.phase == 1 else 7)
        for c in cols:
            x = RX + 16 + c * 32
            for r in range(7):
                self.hazard(x, RY + 16 + r * 32, 15, 0.9, 0.2, 'fire')
        yield 1.3

    def a_brush(self):
        for k in range(3):
            a = self.ang_p()
            for j in range(9):
                off = (j - 4) * 8
                px, py = -math.sin(a) * off, math.cos(a) * off
                ebullet(self.run, self.x + px, self.y + py, a, 110, (30, 20, 30), 3, delay=abs(j - 4) * 0.04)
            yield 0.5

    def a_summon(self):
        self.summon('oni', 1, 30)
        self.summon('shikome', 1, 30)
        yield 0.8

    def a_mirror(self):
        pts = self.trail[::30][-8:]
        for (x, y) in pts:
            self.hazard(x, y, 16, 0.6, 0.15, 'strike')
        yield 0.9

    def a_sentence(self):
        for i in range(60):
            for k in range(6):
                ebullet(self.run, self.x, self.y, i * 0.11 * (1 if k % 2 else -1) + k * math.tau / 6, 85, (230, 60, 50), 3)
            yield 0.06

    def render(self, s, t):
        gfx.draw_glow(s, int(self.x), int(self.y), 44, (200, 40, 30), 70)
        art.draw_big(s, 'enma_b', self.x, self.y - 6, 1.6)
        return
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        gfx.draw_glow(s, x, y, 44, (200, 40, 30), 70)
        D.rect(s, (60, 30, 20), (x - 30, y + 6, 60, 14))
        D.rect(s, (180, 140, 60), (x - 30, y + 6, 60, 3))
        D.polygon(s, (130, 20, 30), [(x - 14, y - 6), (x + 14, y - 6), (x + 22, y + 10), (x - 22, y + 10)])
        D.circle(s, (200, 70, 50), (x, y - 14), 12)
        D.rect(s, (20, 20, 30), (x - 12, y - 34, 24, 12))
        D.rect(s, (230, 190, 70), (x - 6, y - 32, 12, 3))
        D.polygon(s, (20, 10, 10), [(x - 10, y - 6), (x + 10, y - 6), (x, y + 6)])
        eyes(s, x, y - 16, 5, (255, 240, 120), 2)
        D.line(s, (20, 10, 10), (x - 9, y - 22), (x - 2, y - 19), 2); D.line(s, (20, 10, 10), (x + 9, y - 22), (x + 2, y - 19), 2)
        D.rect(s, (220, 200, 150), (x + 20, y - 18, 4, 24))


class Izanami(Boss):
    sheet = ('boss_izanami', 1, None)

    """Die Urgöttin, verwandelt durch die Speisen von Yomi."""
    r = 15

    def setup(self):
        self.y = CY - 30
        self.attacks = ['raijin8', 'hags', 'rot', 'veil']
        self.attacks2 = ['raijin8', 'hags', 'rot', 'veil', 'boulder']
        # In ihrem eigenen Reich (Kapitel VII) ist sie die Endbossin: mehr Leben, drei Phasen
        self.final = self.run.depth >= 7
        if self.final:
            self.maxhp = self.hp = self.maxhp * 2.0
            self._budget = self.maxhp * self.SEC_CAP
            self.P2 = 0.66

    def on_phase2(self):
        if self.final:
            self.extra_dark = 35
            self.run.banner('Izanami zeigt ihr wahres Gesicht', 'Maden kriechen aus dem Totengewand', (200, 150, 230), big=True)
            self.summon('shikome', 2, 60)

    def update(self, dt):
        super().update(dt)
        if self.final and self.phase == 2 and not self.dead and self.hp < self.maxhp * 0.33:
            run = self.run
            self.phase = 3
            self.attacks = ['ikazuchi', 'ikazuchi', 'hags', 'rot', 'boulder']
            self.rest *= 0.8
            self.extra_dark = 75
            run.banner('Die acht Donnergötter erwachen', 'Ikazuchi-no-Kami brechen aus ihrem Leib', (190, 170, 255), big=True)
            audio.play('roar'); audio.play('thunder')
            run.shake(10)
            # die Arena wird enger: Hände der Toten greifen vom Rand
            spots = [(RX + 16 + i * 32, y) for i in range(13) for y in (RY + 14, RY + RH - 14)]
            spots += [(x, RY + 16 + j * 32) for j in range(1, 6) for x in (RX + 14, RX + RW - 14)]
            for x, y in spots:
                h = Hazard(x, y, 15, 1.0, 9999, 0, 'e', 'hands')
                h.boss = self
                run.hazards.append(h)
            self.summon('shikome', 3, 60)

    def a_ikazuchi(self):
        """Die acht Donnergötter: acht Blitzbahnen aus ihrem verwesten Leib, dann ein gezielter Großer Donner."""
        off = random.random() * math.tau
        for k in range(2):
            self.fire_t = self.t
            for i in range(8):
                a = off + k * math.pi / 8 + i * math.tau / 8
                for d in range(30, 280, 26):
                    x, y = self.x + math.cos(a) * d, self.y + math.sin(a) * d
                    if RX < x < RX + RW and RY < y < RY + RH:
                        self.hazard(x, y, 9, 0.8 + d / 1000, 0.15, 'strike')
            yield 1.2
        self.hazard(self.p.x, self.p.y, 22, 0.9, 0.2, 'strike')
        yield 0.9

    def move(self, dt):
        self.x = CX + math.sin(self.t * 0.4) * 80
        self.y = CY - 30 + math.cos(self.t * 0.6) * 20

    def a_raijin8(self):
        for i in range(8):
            a = i / 8 * math.tau + self.t
            self.hazard(self.p.x + math.cos(a) * 45, self.p.y + math.sin(a) * 35, 14, 0.7, 0.15, 'strike')
            yield 0.08
        yield 0.6

    def a_hags(self):
        self.summon('shikome', 2, 50)
        yield 0.8

    def a_rot(self):
        for k in range(50):
            for j in range(3):
                ebullet(self.run, self.x, self.y, k * 0.21 + j * math.tau / 3, 80, (150, 220, 120), 3, eff='slow' if j == 0 else None)
            yield 0.05

    def a_veil(self):
        self.alpha = 70
        self.invuln = True
        for k in range(3):
            self.fan(9, 0.14, 120, (200, 120, 230))
            yield 0.4
        self.alpha = 255
        self.invuln = False

    def a_boulder(self):
        for i in range(5):
            x = random.uniform(RX + 30, RX + RW - 30)
            self.hazard(x, self.p.y, 26, 1.0, 0.2, 'slam')
            yield 0.2
        self.ring(24, 90, 0, (180, 160, 140), 4)
        yield 0.6

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        gfx.draw_glow(s, x, y, 46, (120, 40, 140), 80)
        for i in range(7):
            a = math.pi * (0.2 + i / 6 * 0.6)
            D.line(s, (20, 10, 30), (x, y - 14), (x + math.cos(a) * 30, y - 14 + math.sin(a) * 34 + math.sin(t * 2 + i) * 3), 3)
        D.polygon(s, (230, 225, 235), [(x - 9, y - 6), (x + 9, y - 6), (x + 18, y + 22), (x - 18, y + 22)])
        D.polygon(s, (120, 60, 120), [(x - 2, y - 6), (x + 2, y - 6), (x + 3, y + 22), (x - 3, y + 22)])
        D.circle(s, (20, 10, 30), (x, y - 16), 10)
        D.circle(s, (220, 230, 210), (x, y - 14), 7)
        D.line(s, (120, 150, 110), (x - 4, y - 10), (x + 3, y - 17), 1)
        eyes(s, x, y - 15, 3, (255, 90, 90), 1)
        D.ellipse(s, (240, 210, 90), (x - 10, y - 30, 20, 6), 1)


class Kagutsuchi(Boss):
    sheet = ('boss_kagutsuchi', 1, None)

    """Der Feuergott, dessen Geburt die Welt in Brand setzte."""
    r = 16

    def setup(self):
        self.attacks = ['eruption', 'firewall', 'meteor', 'nova']
        self.attacks2 = ['eruption', 'firewall', 'meteor', 'nova', 'inferno']

    def move(self, dt):
        if self.co is None:
            d = norm(self.p.x - self.x, self.p.y - self.y)
            self.x += d[0] * 22 * dt
            self.y += d[1] * 16 * dt
            self.clamp_pos(26)
        if random.random() < 0.5:
            self.run.hazards.append(Hazard(self.x + random.uniform(-10, 10), self.y + 14, 9, 0.2, 1.5, 1, 'e', 'fire'))

    def a_eruption(self):
        for i in range(24):
            ebullet(self.run, self.x, self.y - 10, -math.pi / 2 + random.uniform(-1.2, 1.2), random.uniform(120, 190), (255, 140, 40), 3, ay=170)
            yield 0.05
        yield 0.5

    def a_firewall(self):
        horiz = random.random() < 0.5
        gap = random.randint(1, 4 if horiz else 10)
        for i in range(7 if horiz else 13):
            if abs(i - gap) <= 1:
                continue
            if horiz:
                ebullet(self.run, RX + 4, RY + 16 + i * 32, 0, 85, (255, 110, 40), 5)
            else:
                ebullet(self.run, RX + 16 + i * 32, RY + 4, math.pi / 2, 75, (255, 110, 40), 5)
        yield 1.0

    def a_meteor(self):
        for i in range(9):
            self.hazard(self.p.x + random.uniform(-50, 50), self.p.y + random.uniform(-40, 40), 18, 0.8, 0.3, 'fire')
            yield 0.12
        yield 0.5

    def a_nova(self):
        for k in range(3):
            self.ring(20, 70 + k * 25, k * 0.15, (255, 200, 80), 3)
            yield 0.3

    def a_inferno(self):
        for k in range(60):
            for j in range(5):
                ebullet(self.run, self.x, self.y, k * 0.13 + j * math.tau / 5, 95, (255, 90, 30), 3, curve=0.4)
            yield 0.05

    def render(self, s, t):
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        gfx.draw_glow(s, x, y, 50, (255, 90, 20), 120)
        for i in range(12):
            a = i / 12 * math.tau + t * 2
            L = 22 + math.sin(t * 9 + i * 2) * 6
            D.polygon(s, (255, 150, 40), [(x + math.cos(a - 0.15) * 12, y + math.sin(a - 0.15) * 12),
                                           (x + math.cos(a) * L, y + math.sin(a) * L),
                                           (x + math.cos(a + 0.15) * 12, y + math.sin(a + 0.15) * 12)])
        D.circle(s, (255, 210, 90), (x, y), 14)
        D.circle(s, (255, 250, 210), (x, y), 8)
        eyes(s, x, y - 2, 5, (180, 20, 10), 2)
        D.arc(s, (180, 20, 10), (x - 5, y + 1, 10, 6), 3.4, 6.0, 1)


class Fujin(Boss):
    sheet = ('boss_fujin', 1, None)

    """Fūjin, der Gott des Windes, mit dem Windsack über dem Kopf."""
    r = 17
    WIND = (200, 240, 225)

    def setup(self):
        self.y = CY - 40
        self.attacks = ['gust', 'sickles', 'tatsumaki', 'ring']
        self.attacks2 = ['gust', 'sickles', 'tatsumaki', 'raijin', 'taifun']

    def move(self, dt):
        self.x = CX + math.sin(self.t * 0.45) * 90
        self.y = CY - 40 + math.sin(self.t * 0.9) * 12

    def a_ring(self):
        for k in range(3):
            self.ring(16, 80, k * 0.2, self.WIND, 3, curve=0.6 if k % 2 else -0.6)
            yield 0.45

    def a_gust(self):
        # Der Sack öffnet sich: Sturm drückt vom Gott weg, Blätter fliegen mit
        audio.play('dash')
        for i in range(36):
            d = norm(self.p.x - self.x, self.p.y - self.y)
            self.run.wind = (d[0] * 85, d[1] * 85, 0.1)
            if i % 4 == 0:
                self.fan(3 if self.phase == 1 else 5, 0.35, 105, (110, 190, 90), r=3, curve=random.uniform(-0.8, 0.8))
            yield 0.05
        yield 0.4

    def a_sickles(self):
        # Kamaitachi-Sicheln: gekrümmte Windklingen aus beiden Richtungen
        for k in range(4 if self.phase == 1 else 6):
            c = 1.3 if k % 2 else -1.3
            a = self.ang_p() - c * 0.45
            self.fan(5, 0.22, 120, self.WIND, ang=a, curve=c)
            yield 0.4
        yield 0.3

    def a_tatsumaki(self):
        # Wirbelstürme: Spiralen um die Spielerin, angekündigt durch Umrisse
        n = 3 if self.phase == 1 else 4
        for j in range(n):
            x = clamp(self.p.x + random.uniform(-60, 60), RX + 24, RX + RW - 24)
            y = clamp(self.p.y + random.uniform(-45, 45), RY + 24, RY + RH - 24)
            for i in range(10):
                ebullet(self.run, x, y, i / 10 * math.tau, 60, self.WIND, 3, delay=0.7, curve=2.2)
            yield 0.35
        yield 0.8

    def a_raijin(self):
        # Fūjin ruft seinen Bruder: Blitze schlagen um die Spielerin ein
        for i in range(5):
            a = random.uniform(0, math.tau)
            self.hazard(self.p.x + math.cos(a) * 30, self.p.y + math.sin(a) * 30, 15, 0.75, 0.15, 'strike')
            yield 0.18
        self.hazard(self.p.x, self.p.y, 15, 0.8, 0.15, 'strike')
        yield 0.9

    def a_taifun(self):
        # Taifun: der Sturm kreist um den Gott, vier Arme aus Windgeschossen
        for i in range(55):
            dx, dy = self.p.x - self.x, self.p.y - self.y
            d = norm(-dy, dx)
            self.run.wind = (d[0] * 55, d[1] * 55, 0.1)
            if i % 2 == 0:
                for k in range(4):
                    ebullet(self.run, self.x, self.y, i * 0.12 + k * math.pi / 2, 90, self.WIND, 3, curve=-0.4)
            yield 0.05
        yield 0.5

    def render(self, s, t):
        pygame.draw.circle(s, (60, 140, 90), (int(self.x), int(self.y)), self.r)


class Amaterasu(Boss):
    """Amaterasu-ōmikami, Endbossin von Ama-no-Iwato (Kapitel VII, zweiter Weg).
    Phase 1: Sie hält sich in der Felsenhöhle verborgen – Dunkelheit, nur Lichtbahnen dringen durch die Spalten.
    Phase 2: Ame-no-Uzume tanzt, die Götter lachen, die Sonne tritt hervor: Sonnenscheiben, Yata-Spiegel, Magatama.
    Phase 3: Ōhirume – die volle Sonne: Feuerspirale und Sonnensäulen."""
    sheet = ('boss_amaterasu', 1, None)
    r = 15
    GOLD = (255, 214, 90)
    FIRE = (255, 140, 40)

    def setup(self):
        self.y = CY - 30
        self.P2 = 0.66
        self.extra_dark = 70
        self.alpha = 150
        self.attacks = ['cracks', 'mirror', 'magatama']
        self.attacks2 = ['sunrings', 'mirror', 'magatama', 'pillars']

    def on_phase2(self):
        run = self.run
        self.extra_dark = 0
        self.alpha = 255
        run.banner('Ame-no-Uzume tanzt', 'Die Götter lachen – neugierig tritt die Sonne aus der Höhle', (255, 220, 140), big=True)
        audio.play('unlock')
        self.ring(36, 70, 0, self.GOLD, 3)

    def update(self, dt):
        super().update(dt)
        if self.phase == 2 and not self.dead and self.hp < self.maxhp * 0.33:
            self.phase = 3
            self.attacks = ['spiral', 'pillars', 'sunrings', 'mirror']
            self.rest *= 0.8
            run = self.run
            run.banner('Ōhirume-no-Muchi', 'Die volle Sonne – der Himmel brennt', (255, 190, 90), big=True)
            audio.play('roar')
            run.shake(10)
            self.summon('komainu', 2, 60)

    def a_cracks(self):
        """Licht durch die Spalten der Höhle: vier Bahnen drehen sich zweimal weiter."""
        off = self.ang_p()
        for k in range(3):
            self.fire_t = self.t
            for i in range(4):
                a = off + k * 0.35 + i * math.tau / 4
                for d in range(26, 300, 24):
                    x, y = self.x + math.cos(a) * d, self.y + math.sin(a) * d
                    if RX < x < RX + RW and RY < y < RY + RH:
                        self.hazard(x, y, 10, 0.75 + d / 1200, 0.15, 'strike')
            yield 0.7
        yield 0.5

    def a_mirror(self):
        """Yata no Kagami: ein Fächer zur Spielerin, dann wirft der Spiegel ihn von der Gegenseite zurück."""
        a = self.ang_p()
        px, py = self.p.x, self.p.y
        self.fan(7, 0.16, 120, self.GOLD, r=3)
        yield 0.7
        mx = clamp(2 * px - self.x, RX + 12, RX + RW - 12)
        my = clamp(2 * py - self.y, RY + 12, RY + RH - 12)
        self.run.particles.append(Particle(mx, my, 0, 0, 0.5, (255, 250, 210), 6))
        audio.play('bell', 0.6)
        self.fan(7, 0.16, 110, (255, 250, 210), x=mx, y=my, r=3)
        yield 0.8

    def a_magatama(self):
        """Yasakani no Magatama: Ketten aus Krummjuwelen, die in Bögen fliegen."""
        for k in range(6):
            self.fire_t = self.t
            for j in range(5):
                a = k * 0.5 + j * math.tau / 5
                ebullet(self.run, self.x, self.y, a, 85, (90, 220, 150), 4, curve=1.4 if k % 2 else -1.4)
            yield 0.25
        yield 0.6

    def a_sunrings(self):
        """Sonnenscheiben: drei Ringe, jeder versetzt, der letzte brennt."""
        for k in range(3):
            self.ring(14 + 3 * self.phase, 80 + k * 10, k * 0.17, self.FIRE if k == 2 else self.GOLD, 4 if k == 2 else 3,
                      eff='burn' if k == 2 else None)
            yield 0.45
        yield 0.5

    def a_pillars(self):
        """Sonnensäulen fallen vom Himmel, wo die Spielerin steht."""
        for i in range(4 + self.phase):
            self.hazard(self.p.x + random.uniform(-14, 14), self.p.y + random.uniform(-10, 10), 20, 0.85, 0.25, 'fire')
            yield 0.3
        yield 0.6

    def a_spiral(self):
        """Ōhirume: dreiarmige Feuerspirale aus dem Sonnenkranz."""
        for k in range(48):
            if k % 4 == 0:
                self.fire_t = self.t
            for j in range(3):
                ebullet(self.run, self.x, self.y - 6, k * 0.19 + j * math.tau / 3, 85, self.FIRE, 3)
            yield 0.06
        yield 0.6

    def move(self, dt):
        if self.phase == 1:                     # in der Höhle bleibt sie fast still
            self.x = CX + math.sin(self.t * 0.3) * 20
            self.y = CY - 40
        else:
            self.x = CX + math.sin(self.t * 0.45) * 90
            self.y = CY - 30 + math.sin(self.t * 0.9) * 22

    def render_under(self, s, t):
        k = 0.5 + 0.5 * math.sin(t * 3)
        gfx.draw_glow(s, int(self.x), int(self.y - 14), 40 if self.phase > 1 else 22, (255, 200, 90), int((60 if self.phase > 1 else 30) + 30 * k))


BOSS_CLASSES = {
    'omukade': Omukade, 'kappa_ou': KappaOu, 'jorogumo': Jorogumo,
    'gashadokuro': Gashadokuro, 'rokurokubi': Rokurokubi, 'nue': Nue,
    'sojobo': Sojobo, 'raiju': Raiju, 'yuki_onna': YukiOnna,
    'umibozu': Umibozu, 'ryujin': Ryujin, 'bake_kujira': BakeKujira,
    'orochi': Orochi, 'shuten_doji': ShutenDoji, 'tamamo': Tamamo,
    'mikaboshi': Mikaboshi,
    'oonyudo': Oonyudo, 'nurarihyon': Nurarihyon, 'kamaitachi_trio': KamaitachiTrio,
    'akkorokamui': Akkorokamui, 'enma': Enma, 'izanami': Izanami, 'amaterasu': Amaterasu, 'kagutsuchi': Kagutsuchi, 'fujin': Fujin,
}


def make_boss(run, bid):
    return BOSS_CLASSES[bid](run, bid, CX, CY - 30)
