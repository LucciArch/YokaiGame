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


def _hitboxes(e):
    hb = getattr(e, 'hitboxes', None)
    return hb() if hb else [(e.x, e.y, e.r)]


def melee(run, x, y, ang, radius, arc, dmg, knock=180, kind='w_sword', col=(230, 240, 255)):
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
            run.damage_enemy(e, dmg, None)
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


def beam(run, x, y, ang, dmg, width=4, col=(255, 236, 150)):
    """Lichtstrahl bis zur nächsten Wand; trifft alles auf der Linie."""
    from .entities import tile_at
    from .settings import SOLID_TILES
    dx, dy = math.cos(ang), math.sin(ang)
    L = 0
    while L < 460:
        L += 4
        tx, ty = x + dx * L, y + dy * L
        if tx < RX or tx > RX + RW or ty < RY or ty > RY + RH:
            break
        t, _, _ = tile_at(run.room, tx, ty)
        if t in SOLID_TILES:
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
                run.damage_enemy(e, dmg, None)
                break
    run.slashes.append(dict(kind='w_laser', x=x, y=y, ang=ang, r=L, arc=0, t=0.0, life=0.12, col=col, w=width))


def fire(p, d, wk):
    """Führt den Angriff der Waffe aus. Gibt True zurück, wenn der normale Talisman entfällt."""
    run = p.run
    ang = math.atan2(d[1], d[0])
    dmg = p.damage()
    x, y = p.x, p.y - 4
    if wk == 'w_sword':
        melee(run, x + d[0] * 6, y + d[1] * 6, ang, 30 + 4 * p.s['size'], math.radians(130), dmg * 2.2, kind=wk)
        if p.f['sword_wave']:
            b = run.fire_player_bullet(x, y, ang, dmg * 1.2, p.s['shotspd'] * 1.1, p.s['size'] * 1.6, 0.6, {'pierce': 1})
            b.crescent = True
        audio.play('slash', 0.8)
    elif wk == 'w_club':
        melee(run, x + d[0] * 5, y + d[1] * 5, ang, 26 + 3 * p.s['size'], math.radians(110), dmg * 2.8, knock=320, kind=wk, col=(255, 200, 160))
        audio.play('ehit', 1.0)
    elif wk == 'w_scythe':
        melee(run, x, y, ang, 36 + 4 * p.s['size'], math.tau, dmg * 2.6, kind=wk, col=(200, 170, 255))
        audio.play('slash', 1.0)
    elif wk == 'w_spear':
        melee(run, x + d[0] * 4, y + d[1] * 4, ang, 54 + 4 * p.s['size'], math.radians(26), dmg * 2.0, knock=120, kind=wk, col=(255, 230, 160))
        audio.play('slash', 0.6)
    elif wk == 'w_laser':
        beam(run, x, y, ang, dmg * 1.35, 3 + p.s['size'])
        audio.play('laser', 0.6)
    elif wk == 'w_bow':
        fl = {'pierce': 1}
        for k in ('homing', 'burn', 'poison', 'slow', 'explode'):
            if p.f[k]:
                fl[k] = p.f[k]
        n = 1 + int(p.f['multishot'])
        for i in range(n):
            b = run.fire_player_bullet(x, y, ang + (i - (n - 1) / 2) * 0.12, dmg * 1.6, p.s['shotspd'] * 1.7,
                                       max(2, p.s['size'] * 0.8), p.s['range'] * 1.4 / (p.s['shotspd'] * 1.7), fl)
            b.arrow = True
        audio.play('bow', 0.7)
    elif wk == 'w_fan':
        for i in range(5):
            a = ang + (i - 2) * 0.22
            b = run.fire_player_bullet(x, y, a, dmg * 0.5, p.s['shotspd'] * 1.1, p.s['size'] * 1.2, 0.42, {'knock': 2, 'pierce': 1})
            b.wind = True
            b.col = (190, 240, 210)
        audio.play('gust', 0.5)
    else:
        return False
    return True


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
