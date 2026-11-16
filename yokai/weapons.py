"""Besondere Angriffsarten, die Items oder Figuren verleihen: Schwerthieb, Sensenwirbel, Speerstoß, Lichtstrahl,
Pfeile, Windfächer. Alles in der Hi-Res-Ebene gezeichnet."""
import math
import random
import pygame
from . import gfx, audio
from .settings import *

# Vorrang, falls mehrere Waffen-Items gesammelt wurden
ORDER = ['w_laser', 'w_scythe', 'w_sword', 'w_spear', 'w_club', 'w_bow', 'w_fan']
RATE = {'w_laser': 0.85, 'w_scythe': 0.55, 'w_sword': 0.7, 'w_spear': 0.65, 'w_club': 0.6, 'w_bow': 0.75, 'w_fan': 0.8}
NAMES = {'w_laser': 'Lichtstrahl', 'w_scythe': 'Sensenwirbel', 'w_sword': 'Schwerthieb', 'w_spear': 'Speerstoß',
         'w_club': 'Keulenschlag', 'w_bow': 'Pfeile', 'w_fan': 'Windfächer'}


def weapon_of(p):
    for k in ORDER:
        if p.f[k]:
            return k
    return None


FLAGS = ('homing', 'pierce', 'bounce', 'spectral', 'explode', 'burn', 'slow', 'poison', 'chain', 'split',
         'boomerang', 'wave', 'knock')


def shot_flags(p):
    """Wurf-Eigenschaften der Items (Feuer, Gift, Zielsuche ...) – gelten für Talismane und Waffen gleichermaßen."""
    return {k: p.f[k] for k in FLAGS if p.f[k]}


def _carrier(x, y, ang, dmg, fl):
    """Unsichtbares Geschoss, über das Hieb und Strahl die Wurf-Eigenschaften an damage_enemy weitergeben."""
    from .entities import Bullet
    return Bullet(x, y, math.cos(ang) * 200, math.sin(ang) * 200, dmg, 3, 0.1, 'p', (255, 255, 255), fl)


def _hit(run, e, hx, hy, dmg, ang, fl):
    if fl:
        b = _carrier(hx, hy, ang, dmg, fl)
        run.damage_enemy(e, dmg, b)
        if fl.get('explode') and e.hp <= dmg * 3:          # Sprengsiegel: Treffer zerplatzen
            run.explode(hx, hy, 22, dmg * 0.7, 'p')
    else:
        run.damage_enemy(e, dmg, None)


def _aim(run, x, y, ang, cone, reach, taken=None):
    """Zielsuche für Hieb und Strahl: zur nächsten Feindin im Kegel drehen; schon gewählte Ziele (taken) zählen
    als weiter entfernt, damit mehrere Strahlen sich auf verschiedene Feinde verteilen."""
    best, bd = None, reach * 2
    for e in run.enemies:
        if not e.active():
            continue
        d = math.hypot(e.x - x, e.y - y)
        if d > reach:
            continue
        if taken is not None and id(e) in taken:
            d += reach
        da = abs((math.atan2(e.y - y, e.x - x) - ang + math.pi) % math.tau - math.pi)
        if da <= cone and d < bd:
            best, bd = e, d
    if best is None:
        return ang
    if taken is not None:
        taken.add(id(best))
    return math.atan2(best.y - y, best.x - x)


def _hitboxes(e):
    hb = getattr(e, 'hitboxes', None)
    return hb() if hb else [(e.x, e.y, e.r)]


def melee(run, x, y, ang, radius, arc, dmg, knock=180, kind='w_sword', col=(230, 240, 255), fl=None):
    """Trifft alle Gegner in einem Kreissektor und zerschlägt feindliche Geschosse darin."""
    hit = False
    for e in list(run.enemies):
        if not e.active():
            continue
        for hx, hy, hr in _hitboxes(e):
            dx, dy = hx - x, hy - y
            d = math.hypot(dx, dy)
            if d > radius + hr:
                continue
            da = (math.atan2(dy, dx) - ang + math.pi) % math.tau - math.pi
            if arc < math.tau and abs(da) > arc / 2 + math.atan2(hr, max(1, d)):
                continue
            _hit(run, e, hx, hy, dmg, ang, fl)
            kb = knock * (0.15 if e.is_boss else 1)
            nx, ny = (dx / d, dy / d) if d > 0 else (math.cos(ang), math.sin(ang))
            e.kx += nx * kb; e.ky += ny * kb
            hit = True
            break
    for b in list(run.ebullets):
        dx, dy = b.x - x, b.y - y
        d = math.hypot(dx, dy)
        if d > radius:
            continue
        da = (math.atan2(dy, dx) - ang + math.pi) % math.tau - math.pi
        if arc >= math.tau or abs(da) <= arc / 2:
            b.life = 0
    run.slashes.append(dict(kind=kind, x=x, y=y, ang=ang, r=radius, arc=arc, t=0.0, life=0.16, col=col))
    if hit:
        run.shake(1.5)
    return hit


def beam(run, x, y, ang, dmg, width=4, col=(255, 236, 150), fl=None, bounces=None):
    """Lichtstrahl bis zur nächsten Wand; trifft alles auf der Linie. Geisterhaft: durch Felsen,
    Abprall: wird an Wand und Fels gespiegelt."""
    from .entities import solid_hit
    fl = fl or {}
    if bounces is None:
        bounces = int(fl.get('bounce', 0))
    dx, dy = math.cos(ang), math.sin(ang)
    L = 0
    wall = None
    while L < 460:
        L += 4
        tx, ty = x + dx * L, y + dy * L
        if tx < RX or tx > RX + RW or ty < RY or ty > RY + RH:
            wall = (tx < RX or tx > RX + RW, ty < RY or ty > RY + RH)
            break
        if not fl.get('spectral') and solid_hit(run.room, tx, ty):
            px_, py_ = tx - dx * 4, ty - dy * 4
            wall = (bool(solid_hit(run.room, tx, py_)), bool(solid_hit(run.room, px_, ty)))
            break
    for e in list(run.enemies):
        if not e.active():
            continue
        for hx, hy, hr in _hitboxes(e):
            px_, py_ = hx - x, hy - y
            along = px_ * dx + py_ * dy
            if along < 0 or along > L:
                continue
            perp = abs(px_ * dy - py_ * dx)
            if perp <= hr + width:
                _hit(run, e, hx, hy, dmg, ang, fl)
                break
    run.slashes.append(dict(kind='w_laser', x=x, y=y, ang=ang, r=L, arc=0, t=0.0, life=0.12, col=col, w=width))
    if wall and bounces > 0:                                # Spiegelung: Einfallswinkel = Ausfallswinkel
        ex, ey = x + dx * (L - 4), y + dy * (L - 4)
        beam(run, ex, ey, math.atan2(-dy if wall[1] else dy, -dx if wall[0] else dx), dmg * 0.8, width, col, fl, bounces - 1)


def shot_angles(p, base):
    """Wurfrichtungen wie beim Talisman: Mehrfachwurf fächert auf, dazu Rück- und Seitenwürfe."""
    n = 1 + int(p.f['multishot'])
    spread = 0.16 if n <= 3 else 0.5 / (n - 1) * 1.6
    angs = [base + (i - (n - 1) / 2) * spread for i in range(n)]
    angs += [base + math.pi] * int(p.f['back'])
    for _ in range(int(p.f['side'])):
        angs += [base + math.pi / 2, base - math.pi / 2]
    return angs


def fire(p, d, wk):
    """Führt den Angriff der Waffe aus und gibt die erzeugten Geschosse zurück (None: normaler Talisman).
    Alle Wurf-Items wirken mit: Mehrfachwurf, Rück-/Seitenwurf, Zielsuche, Feuer, Gift, Frost, Kettenblitz,
    Sprengsiegel, Teilen, Abprall und Geisterwurf."""
    run = p.run
    if wk not in RATE:
        return None
    base = math.atan2(d[1], d[0])
    dmg = p.damage()
    be = int(p.f['big_every'])
    big = bool(be and p.shot_count % be == 0)
    if big:
        dmg *= 3
    x, y = p.x, p.y - 4
    fl = shot_flags(p)
    col = run.shot_col(fl)
    angs = shot_angles(p, base)
    homing = bool(fl.get('homing'))
    made = []

    def wave(a, f=0.6):                                     # zusätzliche Klingenwelle eines Hiebs (Mehrfachwurf)
        nf = dict(fl); nf['pierce'] = 1
        b = run.fire_player_bullet(x, y, a, dmg * f, p.s['shotspd'] * 1.1, p.s['size'] * 1.6, 0.6, nf)
        b.crescent = True
        made.append(b)

    if wk in ('w_sword', 'w_club', 'w_scythe', 'w_spear'):
        reach = {'w_sword': 30, 'w_club': 26, 'w_scythe': 36, 'w_spear': 54}[wk] + 4 * p.s['size']
        n = 1 + int(p.f['multishot'])
        for i, a in enumerate([base] + angs[n:]):               # Hiebe nach vorn, hinten, zur Seite
            if homing:
                a = _aim(run, x, y, a, 0.8, reach * 1.8)
            if wk == 'w_sword':
                melee(run, x + math.cos(a) * 6, y + math.sin(a) * 6, a, reach, math.radians(130), dmg * 2.2, kind=wk, col=col if fl else (230, 240, 255), fl=fl)
                if p.f['sword_wave'] and i == 0:
                    wave(a, 0.9)
            elif wk == 'w_club':
                melee(run, x + math.cos(a) * 5, y + math.sin(a) * 5, a, reach, math.radians(110), dmg * 2.8, knock=320, kind=wk, col=col if fl else (255, 200, 160), fl=fl)
            elif wk == 'w_scythe':
                if i == 0:
                    melee(run, x, y, a, reach, math.tau, dmg * 2.6, kind=wk, col=col if fl else (200, 170, 255), fl=fl)
            else:
                melee(run, x + math.cos(a) * 4, y + math.sin(a) * 4, a, reach, math.radians(26), dmg * 2.0, knock=120, kind=wk, col=col if fl else (255, 230, 160), fl=fl)
        for a in angs[:n] if n > 1 else ():                 # Mehrfachwurf: jeder weitere Wurf wird zur Klingenwelle
            wave(a)
        audio.play('ehit' if wk == 'w_club' else 'slash', 1.0 if wk in ('w_club', 'w_scythe') else 0.7)
    elif wk == 'w_laser':
        w = 3 + p.s['size'] + (3 if big else 0)
        taken = set()
        for a in angs:
            if homing:
                a = _aim(run, x, y, a, 0.55, 420, taken)
            beam(run, x, y, a, dmg * 1.35, w, col if fl else (255, 236, 150), fl)
        audio.play('laser', 0.6)
    elif wk == 'w_bow':
        bf = dict(fl); bf['pierce'] = 1
        for a in angs:
            b = run.fire_player_bullet(x, y, a, dmg * 1.6, p.s['shotspd'] * 1.7, max(2, p.s['size'] * 0.8),
                                       p.s['range'] * 1.4 / (p.s['shotspd'] * 1.7), bf)
            b.arrow = True
            made.append(b)
        audio.play('bow', 0.7)
    elif wk == 'w_fan':
        wf = dict(fl); wf['knock'] = max(2, fl.get('knock', 0)); wf['pierce'] = 1
        k = 5 + 2 * int(p.f['multishot'])
        for base_a in [base] + angs[1 + int(p.f['multishot']):]:
            for i in range(k):
                b = run.fire_player_bullet(x, y, base_a + (i - (k - 1) / 2) * min(0.22, 1.1 / k), dmg * 0.5,
                                           p.s['shotspd'] * 1.1, p.s['size'] * 1.2, 0.42, wf)
                b.wind = True
                if not fl:
                    b.col = (190, 240, 210)
                made.append(b)
        audio.play('gust', 0.5)
    for b in made:
        b.big = big
    return made


# ------------------------------------------------------------------ Zeichnen
_cache = {}


def _slash_img(kind, r, arc, frac, col):
    """Sichel-Bild (Hi-Res), Spitze zeigt nach rechts (Winkel 0)."""
    q = int(frac * 6)
    key = (kind, int(r), round(arc, 2), q, col)
    im = _cache.get(key)
    if im is not None:
        return im
    R = int(r * 2) + 6
    s = pygame.Surface((R * 2, R * 2), pygame.SRCALPHA)
    if kind == 'w_spear':
        ln = int(r * 2 * (0.6 + 0.4 * (1 - frac)))
        pygame.draw.polygon(s, (20, 14, 20), [(R, R - 4), (R + ln, R), (R, R + 4)])
        pygame.draw.polygon(s, col, [(R, R - 3), (R + ln - 2, R), (R, R + 3)])
        pygame.draw.line(s, (255, 255, 255), (R + ln // 3, R), (R + ln - 6, R), 1)
    else:
        a0 = -arc / 2 if arc < math.tau else 0
        a1 = arc / 2 if arc < math.tau else math.tau
        sweep = a0 + (a1 - a0) * min(1, 0.35 + frac * 1.3)
        n = 28
        outer, inner = [], []
        for i in range(n + 1):
            a = a0 + (sweep - a0) * i / n
            th = (1 - abs(2 * i / n - 1)) ** 0.7
            ro = r * 2
            ri = r * 2 - 5 - 20 * th
            outer.append((R + math.cos(a) * ro, R + math.sin(a) * ro))
            inner.append((R + math.cos(a) * ri, R + math.sin(a) * ri))
        poly = outer + inner[::-1]
        alpha = int(255 * (1 - frac * 0.7))
        pygame.draw.polygon(s, (20, 14, 26, alpha), poly)
        inner2 = [(R + (x - R) * 0.97, R + (y - R) * 0.97) for x, y in outer] + [(R + (x - R) * 1.03, R + (y - R) * 1.03) for x, y in inner[::-1]]
        pygame.draw.polygon(s, col + (alpha,), inner2)
        pygame.draw.lines(s, (255, 255, 255, alpha), False, [(R + (x - R) * 0.985, R + (y - R) * 0.985) for x, y in outer], 2)
    _cache[key] = s
    return s


def draw(run, s):
    for sl in run.slashes:
        frac = sl['t'] / sl['life']
        if sl['kind'] == 'w_laser':
            L = sl['r']
            w = max(2, int((sl.get('w', 4) * 2 + 4) * (1 - frac * 0.6)))
            surf = pygame.Surface((int(L * 2) + 8, w * 2 + 8), pygame.SRCALPHA)
            cy = w + 4
            pygame.draw.rect(surf, (255, 170, 60, 140), (0, cy - w, int(L * 2), w * 2))
            pygame.draw.rect(surf, sl['col'] + (230,), (0, cy - w // 2, int(L * 2), max(2, w)))
            pygame.draw.rect(surf, (255, 255, 255), (0, cy - 1, int(L * 2), 2))
            pygame.draw.circle(surf, (255, 255, 255), (4, cy), w + 2)
            rot = pygame.transform.rotate(surf, -math.degrees(sl['ang']))
            cx = sl['x'] + math.cos(sl['ang']) * L / 2
            cyw = sl['y'] + math.sin(sl['ang']) * L / 2
            gfx.hi_blit(rot, cx, cyw + rot.get_height() / 4, transient=True)
            gfx.draw_glow(s, int(sl['x']), int(sl['y']), 10, (255, 220, 120), 120)
            continue
        im = _slash_img(sl['kind'], sl['r'], sl['arc'], frac, sl['col'])
        rot = pygame.transform.rotate(im, -math.degrees(sl['ang']))
        gfx.hi_blit(rot, sl['x'], sl['y'] + rot.get_height() / 4, transient=True)


def update(run, dt):
    for sl in run.slashes:
        sl['t'] += dt
    run.slashes[:] = [sl for sl in run.slashes if sl['t'] < sl['life']]
