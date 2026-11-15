"""Kitsune no yomeiri – die Fuchshochzeit.

Ein Ereignisraum: Ein Hochzeitszug aus Füchsen zieht durch den Raum. Wer ihn nicht
stört, bekommt von der Braut ein Geschenk. Wer auf die Füchse schießt, erzürnt sie –
dann erscheinen Fuchsfeuer.
"""
import math
import random

from . import gfx, sheets, audio
from .settings import RX, RY, RW, RH
from .entities import Pedestal, Pickup, burst, Particle

SPEED = 24.0
ORDER = ('kitsune_gefolge', 'kitsune_gefolge', 'kitsune_braut', 'kitsune_gefolge', 'kitsune_gefolge')


class Fox:
    def __init__(self, proc, name, x, y, i):
        self.proc, self.name, self.x, self.y0, self.i = proc, name, x, y, i
        self.y = y
        self.t = random.uniform(0, 1)

    def draw(self, s, t):
        pr = self.proc
        if pr.state == 'bow':
            f = 4 + min(2, int((1.8 - pr.bow_t) * 3))
        else:
            f = int(self.t * 6) % 4
        spr = sheets.frame(self.name, sheets.LEFT, f)
        edge = min((RX + RW - 6 - self.x) / 18.0, (self.x - RX - 2) / 18.0)
        a = int(255 * max(0.0, min(1.0, pr.fade, edge)))
        if a <= 0:
            return
        gfx.shadow(s, (int(self.x) - 7, int(self.y) - 2, 14, 4))
        if self.name == 'kitsune_gefolge':
            gfx.draw_glow(s, int(self.x) - 7, int(self.y) - 12, 14, (255, 190, 90), int(60 * a / 255))
        gfx.hi_blit(spr, self.x, self.y + 1, a)


class Procession:
    def __init__(self, run, room):
        self.run, self.room = run, room
        cy = RY + RH / 2 - 6
        self.foxes = [Fox(self, n, RX + RW + 24 + i * 30, cy + (6 if i % 2 else -6), i) for i, n in enumerate(ORDER)]
        self.state = 'walk'
        self.bow_t = 0.0
        self.gifted = False
        self.fade = 1.0
        self.rain = 0.0
        self.beat = 0.4
        self.nbeat = 0
        run.banner('Kitsune no Yomeiri', 'Eine Fuchshochzeit zieht vorbei – störe sie nicht!', (255, 190, 120))

    @property
    def bride(self):
        return self.foxes[2]

    def update(self, dt):
        run = self.run
        if self.state == 'angry':
            self.fade -= dt * 3
            return self.fade > 0
        # Sonnenregen: feine, goldene Tropfen
        self.rain += dt
        while self.rain > 0.05 and len(run.particles) < 500:
            self.rain -= 0.05
            run.particles.append(Particle(random.uniform(RX, RX + RW), RY + 4, -6, 150, 0.9, (255, 226, 160), 1))
        for f in self.foxes:
            f.t += dt
            f.y = f.y0 + math.sin(f.t * 5 + f.i) * 0.8
        self.beat -= dt
        if self.beat <= 0 and any(RX < f.x < RX + RW for f in self.foxes):
            self.beat = 0.8
            self.nbeat += 1
            audio.play('bell' if self.nbeat % 4 == 1 else 'drum', 0.18 if self.nbeat % 4 == 1 else 0.1)
        if self.state == 'walk':
            for f in self.foxes:
                f.x -= SPEED * dt
            if not self.gifted and self.bride.x <= RX + RW / 2:
                self.state = 'bow'
                self.bow_t = 1.8
        elif self.state == 'bow':
            self.bow_t -= dt
            if self.bow_t <= 0:
                self.state = 'walk'
                self.gift()
        # Schüsse auf den Zug?
        for b in run.pbullets:
            if b.life <= 0 or getattr(b, 'delay', 0) > 0:
                continue
            for f in self.foxes:
                if abs(b.x - f.x) < 9 and f.y - 22 < b.y < f.y + 2:
                    b.life = 0
                    self.anger()
                    return True
        for sl in run.slashes:
            if sl['kind'] == 'w_laser' or sl['t'] > 0.05:
                continue
            for f in self.foxes:
                dx, dy = f.x - sl['x'], f.y - 8 - sl['y']
                if math.hypot(dx, dy) < sl['r'] + 4:
                    da = (math.atan2(dy, dx) - sl['ang'] + math.pi) % (2 * math.pi) - math.pi
                    if abs(da) < sl['arc'] / 2 + 0.3:
                        self.anger()
                        return True
        if all(f.x < RX - 24 for f in self.foxes):
            self.room.extra['yomeiri_done'] = True
            return False
        return True

    def gift(self):
        run = self.run
        self.gifted = True
        self.room.extra['yomeiri_done'] = True
        b = self.bride
        from .data import ITEMS
        fox = [i for i in run.pool if 'kitsune' in ITEMS[i]['tags'] and ITEMS[i]['q'] <= 3]
        if 'brautschleier' in run.pool:
            iid = 'brautschleier'
            run.pool.remove(iid)
        elif fox and random.random() < 0.7:
            iid = random.choice(fox)
            run.pool.remove(iid)
        else:
            iid = run.pick_item('T', 0.12)
        run.pedestals.append(Pedestal(iid, b.x, b.y + 22))
        burst(run, b.x, b.y + 10, (255, 220, 150), 18, 70)
        audio.play('unlock', 0.6)
        run.banner('Die Braut dankt dir', 'Ein Geschenk der Füchse', (255, 210, 150))
        run.achieve('yomeiri')
        run.event_done('yomeiri')

    def anger(self):
        run = self.run
        self.state = 'angry'
        self.room.extra['yomeiri_done'] = True
        audio.play('roar', 0.5)
        run.banner('Die Füchse sind gekränkt!', 'Fuchsfeuer erscheinen', (255, 120, 90))
        run.event_done('yomeiri')
        for f in self.foxes[:3 if run.depth < 4 else 5]:
            burst(run, f.x, f.y - 10, (120, 180, 255), 12, 60)
            run.spawn_enemy('kitsunebi_e', f.x, f.y - 10)
        if run.enemies:
            self.room.cleared = False


# ---------------------------------------------------------------- Kakurenbo (Versteckspiel)
class Apparition:
    """Kurz sichtbare Figur (z. B. Zashiki-warashi, die aus der Urne hüpft)."""

    def __init__(self, name, x, y, life=2.4, frame0=0):
        self.name, self.x, self.y, self.life, self.t = name, x, y, life, 0.0
        self.frame0 = frame0

    def update(self, dt):
        self.t += dt
        return self.t < self.life

    def draw(self, s, t):
        a = int(255 * max(0.0, min(1.0, self.t * 4, (self.life - self.t) * 2)))
        hop = math.sin(min(1.0, self.t / 0.4) * math.pi) * 8
        f = self.frame0 + int(self.t * 6) % 3 if self.frame0 else int(self.t * 6) % 4
        spr = sheets.frame(self.name, sheets.LEFT, f)
        gfx.shadow(s, (int(self.x) - 6, int(self.y) - 2, 12, 4))
        gfx.hi_blit(spr, self.x, self.y + 1 - hop, a)


POTS = [(3, 1), (9, 1), (3, 5), (9, 5)]


def kakurenbo_start(run, room):
    if room.extra.get('kak_done'):
        return
    if 'kak_hide' not in room.extra:
        room.extra['kak_hide'] = random.choice(POTS)
        room.extra['kak_tries'] = 0
    run.banner('Kakurenbo', 'Sie versteckt sich in einer Urne und kichert manchmal – zwei Versuche!', (240, 200, 220))


def kakurenbo_update(run, dt):
    """Ab und zu ein leises Kichern: ein rosa Funke über der richtigen Urne – wer genau hinsieht, findet sie."""
    room = run.room
    if room.extra.get('kak_done') or 'kak_hide' not in room.extra:
        return
    t = room.extra.get('kak_t', 2.5) - dt
    if t <= 0:
        t = random.uniform(3.0, 5.0)
        hx, hy = room.extra['kak_hide']
        x, y = RX + hx * 32 + 16 + random.uniform(-6, 6), RY + hy * 32 + 4
        for i in range(3):
            run.particles.append(Particle(x + i * 3 - 3, y, random.uniform(-6, 6), -18 - i * 4, 0.9, (255, 170, 210), 1))
        audio.play('wisp', 0.12)
    room.extra['kak_t'] = t


def kakurenbo_break(run, tx, ty):
    room = run.room
    if room.kind != 'kakurenbo' or room.extra.get('kak_done') or (tx, ty) not in POTS:
        return
    x, y = RX + tx * 32 + 16, RY + ty * 32 + 16
    if (tx, ty) == tuple(room.extra.get('kak_hide', ())):
        room.extra['kak_done'] = True
        p = run.player
        p.bonus['luck'] += 1
        p.recalc()
        run.apparitions.append(Apparition('zashiki', x, y + 10, 2.6, frame0=4))
        burst(run, x, y, (255, 200, 230), 20, 80)
        if 'zashiki_temari' in run.pool:
            run.pool.remove('zashiki_temari')
            run.pedestals.append(Pedestal('zashiki_temari', RX + RW / 2, RY + RH / 2))
        else:
            for i in range(4):
                run.spawn_pickup('coin', x + random.uniform(-12, 12), y + random.uniform(-6, 10))
        audio.play('unlock', 0.6)
        run.banner('Gefunden!', 'Zashiki-warashi lässt dir ihr Spielzeug da – Glück +1', (255, 220, 240))
        run.achieve('kakurenbo')
        run.event_done('kakurenbo')
    else:
        room.extra['kak_tries'] = room.extra.get('kak_tries', 0) + 1
        if room.extra['kak_tries'] >= 2:
            room.extra['kak_done'] = True
            hx, hy = room.extra['kak_hide']
            run.apparitions.append(Apparition('zashiki', RX + hx * 32 + 16, RY + hy * 32 + 26, 1.6))
            run.banner('Kichern…', 'Sie ist entwischt', (200, 180, 220))
            run.event_done('kakurenbo')
        else:
            run.banner('Leer…', 'Noch ein Versuch', (220, 200, 210))


# ---------------------------------------------------------------- Hyakki Yagyō (Nachtparade)
PARADE = ['kasa_obake', 'chochin', 'oni', 'bakezori', 'nopperabo', 'ittan_momen', 'karasu_tengu', 'kappa', 'gozu',
          'bakeneko', 'yamauba', 'heikegani', 'mezu', 'hitodama']


class Marcher:
    def __init__(self, parade, name, x, y, vx):
        self.parade, self.name, self.x, self.y, self.vx = parade, name, x, y, vx
        self.t = random.uniform(0, 1)

    def draw(self, s, t):
        edge = min((RX + RW - 6 - self.x) / 18.0, (self.x - RX - 2) / 18.0)
        a = int(210 * max(0.0, min(1.0, edge, self.parade.fade)))
        if a <= 0:
            return
        spr = sheets.frame(self.name, sheets.RIGHT if self.vx > 0 else sheets.LEFT, int(self.t * 7) % 4)
        spr = gfx.tinted(spr, 'ghost')
        gfx.draw_glow(s, int(self.x), int(self.y) - 10, 16, (150, 110, 220), int(40 * a / 210))
        gfx.hi_blit(spr, self.x, self.y + 1, a)


class Parade:
    """Die Parade der hundert Dämonen zieht in Reihen durch den Raum. Wer ausweicht, findet danach eine Truhe."""

    def __init__(self, run, room):
        self.run, self.room = run, room
        self.fade = 1.0
        self.hits = 0
        self.beat = 0.3
        self.nbeat = 0
        self.dark = 0.0
        self.marchers = []
        names = [n for n in PARADE if sheets.has(n) and sheets.is_hi(n)]
        random.shuffle(names)
        cy = RY + RH / 2
        lanes = [(cy - 44, 1, 0), (cy + 40, -1, 3.0), (cy - 4, 1, 7.5)]           # (y, Richtung, Verzögerung in s)
        self.lanes = [ly for ly, _, _ in lanes]
        k = 0
        for ly, d, delay in lanes:
            for i in range(5):
                x0 = (RX - 30 - i * 40 - delay * 46) if d > 0 else (RX + RW + 30 + i * 40 + delay * 46)
                self.marchers.append(Marcher(self, names[k % len(names)], x0, ly, 46 * d))
                k += 1
        run.banner('Hyakki Yagyō', 'Die Parade der hundert Dämonen zieht vorbei – weiche ihr aus!', (190, 150, 255))

    @property
    def foxes(self):                     # für die Zeichen-Sortierung wie beim Hochzeitszug
        return self.marchers

    def draw_under(self, s):
        """Violetter Schleier über dem Raum, solange die Parade durchzieht."""
        if self.dark <= 0:
            return
        ov = getattr(Parade, '_ov', None)
        if ov is None:
            import pygame
            ov = pygame.Surface((RW, RH), pygame.SRCALPHA)
            ov.fill((40, 20, 70, 255))
            Parade._ov = ov
        ov.set_alpha(int(70 * self.dark))
        s.blit(ov, (RX, RY))

    def draw_lanes(self, s, t):
        """Vorwarnung: Eine Reihe kündigt sich als violette Spur am Boden an, bevor sie den Raum betritt."""
        import pygame
        for ly in self.lanes:
            ms = [m for m in self.marchers if m.y == ly]
            near = [m for m in ms if (m.vx > 0 and RX - 140 < m.x < RX + RW + 20) or (m.vx < 0 and RX - 20 < m.x < RX + RW + 140)]
            if not near:
                continue
            a = 0.5 + 0.5 * math.sin(t * 6)
            col = (int(110 + 60 * a), int(70 + 30 * a), int(170 + 60 * a))
            off = int(t * 40 * (1 if ms[0].vx > 0 else -1)) % 12
            for x in range(RX + off, RX + RW, 12):
                pygame.draw.line(s, col, (x, int(ly) - 2), (x + 5, int(ly) - 2), 1)

    def update(self, dt):
        run, p = self.run, self.run.player
        inside = any(RX < m.x < RX + RW for m in self.marchers)
        self.dark = min(1.0, self.dark + dt) if inside else max(0.0, self.dark - dt)
        self.beat -= dt
        if self.beat <= 0 and inside:
            self.beat = 0.6
            self.nbeat += 1
            audio.play('drum' if self.nbeat % 2 else 'wisp', 0.16 if self.nbeat % 2 else 0.08)
        for m in self.marchers:
            m.x += m.vx * dt
            m.t += dt
            if RX < m.x < RX + RW and abs(m.x - p.x) < 9 and abs(m.y - 6 - p.y) < 11:
                if p.hurt(1, 'die Dämonenparade'):
                    self.hits += 1
        if all((m.vx > 0 and m.x > RX + RW + 24) or (m.vx < 0 and m.x < RX - 24) for m in self.marchers):
            self.room.extra['parade_done'] = True
            cx, cy = RX + RW / 2, RY + RH / 2
            run.pickups.append(Pickup('chest', cx, cy, pop=False))
            if self.hits == 0:
                run.pickups.append(Pickup('chest', cx + 30, cy, pop=False))
                run.banner('Die Parade ist vorüber', 'Unberührt – zwei Truhen bleiben zurück', (210, 180, 255))
                run.achieve('hyakki')
            else:
                run.banner('Die Parade ist vorüber', 'Eine Truhe bleibt zurück', (210, 180, 255))
            audio.play('bell', 0.5)
            run.event_done('hyakki')
            return False
        return True
