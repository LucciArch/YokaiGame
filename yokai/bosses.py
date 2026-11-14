"""Die 16 Bosse – jeder mit eigenen Angriffsmustern (als Koroutinen geschrieben)."""
import math
import random
import pygame
from .settings import *
from . import gfx, audio
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
        hpm = (1.3 if run.hard else 1.0) * (1 + 0.12 * (run.depth - 1))
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
        self.contact = 1 if run.depth <= 3 else 2
        self.invuln = False
        self.attacks = ['ring']
        self.attacks2 = None
        self.rest = 0.9
        self.setup()

    def setup(self):
        pass

    # ------------------------------------------------------------ Hilfen
    @property
    def p(self):
        return self.run.player

    def ang_p(self, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        return math.atan2(self.p.y - y, self.p.x - x)

    def ring(self, n, sp, off=0.0, col=(240, 80, 120), x=None, y=None, r=3, **kw):
        x = self.x if x is None else x
        y = self.y if y is None else y
        for i in range(n):
            ebullet(self.run, x, y, off + i / n * math.tau, sp, col, r, **kw)

    def fan(self, n, spread, sp, col=(240, 80, 120), x=None, y=None, ang=None, r=3, **kw):
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
        if self.phase == 1 and self.hp < self.maxhp * 0.5:
            self.phase = 2
            self.rest *= 0.7
            audio.play('roar')
            run.shake(6)
            self.on_phase2()
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
                        p.hurt(self.contact)
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
        surf = pygame.Surface((W, H), pygame.SRCALPHA) if (self.flash > 0 or self.frozen > 0 or self.alpha < 255) else None
        target = surf if surf is not None else s
        gfx.shadow(s, (int(self.x) - self.r, int(self.y) + self.r - 4, self.r * 2, 7))
        self.render(target, t)
        if surf is not None:
            if self.flash > 0:
                surf.fill((120, 110, 110, 0), special_flags=pygame.BLEND_RGB_ADD)
            elif self.frozen > 0:
                surf.fill((150, 210, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
            if self.alpha < 255:
                surf.set_alpha(self.alpha)
            s.blit(surf, (0, 0))

    def draw_hidden(self, s, t):
        pass

    def render(self, s, t):
        pygame.draw.circle(s, (200, 50, 50), (int(self.x), int(self.y)), self.r)


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
    r = 16

    def setup(self):
        self.attacks = ['jump', 'spit', 'summon']
        self.attacks2 = ['jump', 'spit', 'summon', 'rain', 'triple']
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
    r = 13

    def setup(self):
        self.attacks = ['web', 'eggs', 'spiral', 'dash']
        self.attacks2 = ['web', 'eggs', 'spiral', 'dash', 'webring']
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

    def a_webring(self):
        self.ring(16, 70, 0, (240, 240, 250), eff='slow')
        yield 0.3
        self.fan(5, 0.15, 150, (180, 90, 220))
        yield 0.5

    def render(self, s, t):
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
class Gashadokuro(Boss):
    r = 20

    def setup(self):
        self.y = RY + 45
        self.hands = [[CX - 70, RY + 110], [CX + 70, RY + 110]]
        self.hand_home = [[CX - 70, RY + 110], [CX + 70, RY + 110]]
        self.attacks = ['slam', 'bones', 'jaw']
        self.attacks2 = ['slam', 'double', 'bones', 'jaw']
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


class Rokurokubi(Boss):
    r = 9

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
        D.ellipse(s, (180, 50, 70), (bx - 18, by - 2, 36, 26))
        D.ellipse(s, (240, 180, 190), (bx - 10, by + 2, 20, 10))
        # Hals
        n = 18
        for i in range(n + 1):
            f = i / n
            cx = bx + (self.x - bx) * f + math.sin(f * math.pi * 3 + t * 3) * 10 * (1 - abs(f - 0.5) * 2)
            cy = by + (self.y - by) * f
            D.circle(s, (240, 210, 190), (int(cx), int(cy)), 4)
        x, y = int(self.x), int(self.y)
        D.circle(s, (20, 10, 20), (x, y - 3), 11)
        D.circle(s, (248, 222, 204), (x, y), 8)
        D.rect(s, (20, 10, 20), (x - 9, y - 4, 3, 12)); D.rect(s, (20, 10, 20), (x + 6, y - 4, 3, 12))
        D.circle(s, (20, 10, 20), (x - 3, y - 1), 1); D.circle(s, (20, 10, 20), (x + 3, y - 1), 1)
        D.line(s, (200, 40, 60), (x - 2, y + 4), (x + 2, y + 4))


class Nue(Boss):
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
        D = pygame.draw
        segs = self.seg_pos()
        for i, (x, y) in enumerate(reversed(segs)):
            j = len(segs) - i
            r = 9 if j < 6 else 7 if j < 12 else 5
            D.circle(s, (10, 40, 40), (int(x), int(y)), r + 1)
            D.circle(s, (60, 170, 140), (int(x), int(y)), r)
            D.circle(s, (240, 210, 90), (int(x), int(y) - r + 2), 2)
            if j % 4 == 0:
                for side in (-1, 1):
                    D.line(s, (240, 210, 90), (x, y), (x + side * 9, y + 6), 2)
        hx, hy = int(self.x), int(self.y)
        D.circle(s, (10, 40, 40), (hx, hy), 13)
        D.circle(s, (70, 190, 150), (hx, hy), 12)
        hd = self.heading
        for side in (-1, 1):
            a = hd + math.pi + side * 0.5
            D.line(s, (240, 220, 140), (hx, hy), (hx + math.cos(a) * 16, hy + math.sin(a) * 16), 3)
            a2 = hd + side * 0.9
            D.line(s, (250, 250, 230), (hx, hy), (hx + math.cos(a2) * 20 + math.sin(t * 3) * 3, hy + math.sin(a2) * 20), 1)
        eyes(s, hx + math.cos(hd) * 5, hy + math.sin(hd) * 5 - 2, 4, (255, 80, 60), 2)


class BakeKujira(Boss):
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
        D = pygame.draw
        x, y = int(self.x), int(self.y)
        for i in range(8):
            hx, hy = self.head_pos(i)
            n = 10
            for k in range(n + 1):
                f = k / n
                cx = x + (hx - x) * f + math.sin(f * 6 + t * 3 + i) * 3
                cy = y + (hy - y) * f
                D.circle(s, (40, 90, 50), (int(cx), int(cy)), 5)
                D.circle(s, (80, 150, 80), (int(cx), int(cy)), 4)
            D.circle(s, (30, 60, 30), (int(hx), int(hy)), 9)
            D.circle(s, (100, 170, 90), (int(hx), int(hy)), 8)
            D.polygon(s, (240, 230, 200), [(hx - 3, hy + 5), (hx - 1, hy + 9), (hx, hy + 5)])
            D.polygon(s, (240, 230, 200), [(hx + 3, hy + 5), (hx + 1, hy + 9), (hx, hy + 5)])
            eyes(s, hx, hy - 2, 3, (255, 50, 40), 1)
        D.circle(s, (30, 60, 30), (x, y), 20)
        D.circle(s, (70, 130, 70), (x, y), 19)
        for i in range(6):
            D.arc(s, (50, 100, 50), (x - 16 + i * 4, y - 14, 10, 10), 0, 3.1, 1)


class ShutenDoji(Boss):
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


BOSS_CLASSES = {
    'omukade': Omukade, 'kappa_ou': KappaOu, 'jorogumo': Jorogumo,
    'gashadokuro': Gashadokuro, 'rokurokubi': Rokurokubi, 'nue': Nue,
    'sojobo': Sojobo, 'raiju': Raiju, 'yuki_onna': YukiOnna,
    'umibozu': Umibozu, 'ryujin': Ryujin, 'bake_kujira': BakeKujira,
    'orochi': Orochi, 'shuten_doji': ShutenDoji, 'tamamo': Tamamo,
    'mikaboshi': Mikaboshi,
}


def make_boss(run, bid):
    return BOSS_CLASSES[bid](run, bid, CX, CY - 30)
