"""Animierte Sprites aus dem Ninja-Adventure-Asset-Pack (pixel-boy, CC0).

Spritesheets (64x64): Spalten = Blickrichtung (unten, oben, links, rechts),
Zeilen = Animationsbilder (4). Tier-Sheets (32x16): 2 Bilder.
Boss-Streifen: quadratische Bilder nebeneinander.
"""
import os
import sys
import pygame

_here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sprites')
if not os.path.isdir(_here) and hasattr(sys, '_MEIPASS'):
    _here = os.path.join(sys._MEIPASS, 'yokai', 'assets', 'sprites')
BASE = _here

DOWN, UP, LEFT, RIGHT = 0, 1, 2, 3

# Darstellungsgröße (Vergrößerungsfaktor der 16-px-Pixel-Art)
SCALE = {'kumo': 1, 'gaki_small': 1, 'tesso': 1, 'yosuzume': 1, 'kappa_small': 1, 'nuppeppo_klein': 1,
         'oni': 3, 'tsuchigumo': 3, 'nurikabe': 3, 'gyuki': 3, 'kerakera_onna': 3, 'tsurube_otoshi': 3}

_raw = {}
_cache = {}
_exists = {}


def has(name):
    v = _exists.get(name)
    if v is None:
        v = os.path.exists(os.path.join(BASE, name + '.png'))
        _exists[name] = v
    return v


def _load(name):
    s = _raw.get(name)
    if s is None:
        s = pygame.image.load(os.path.join(BASE, name + '.png'))
        try:
            s = s.convert_alpha()
        except pygame.error:
            pass
        _raw[name] = s
    return s


def scale_of(name):
    return SCALE.get(name, 2)


def frame_count(name):
    raw = _load(name)
    w, h = raw.get_size()
    if name.startswith('boss_'):
        return max(1, w // h)
    if (w, h) == (32, 16):
        return 2
    return 4


def frame(name, d=DOWN, f=0, scale=None, flash=False, tint=None, alpha=255):
    scale = scale_of(name) if scale is None else scale
    key = (name, d, f % 8, scale, flash, tint)
    s = _cache.get(key)
    if s is None:
        raw = _load(name)
        w, h = raw.get_size()
        flip = False
        if name.startswith('boss_'):
            n = max(1, w // h)
            sub = raw.subsurface(((f % n) * h, 0, h, h))
            flip = d == LEFT
        elif (w, h) == (32, 16):
            sub = raw.subsurface(((f % 2) * 16, 0, 16, 16))
            flip = d == RIGHT
        elif w >= 64 and h >= 64:
            sub = raw.subsurface((min(3, d) * 16, (f % 4) * 16, 16, 16))
        else:
            sub = raw
        s = pygame.transform.scale(sub, (int(sub.get_width() * scale), int(sub.get_height() * scale)))
        if flip:
            s = pygame.transform.flip(s, True, False)
        if tint:
            s = s.copy()
            s.fill(tint, special_flags=pygame.BLEND_RGB_MULT)
            s.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_ADD)
        if flash:
            s = s.copy()
            s.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
        _cache[key] = s
    if alpha < 255:
        s = s.copy()
        s.set_alpha(alpha)
    return s


def dir_from(dx, dy):
    if abs(dx) > abs(dy):
        return LEFT if dx < 0 else RIGHT
    return UP if dy < 0 else DOWN


def blit_center(surf, name, x, y, d=DOWN, f=0, scale=None, tint=None, flash=False, alpha=255):
    img = frame(name, d, f, scale, flash, tint, alpha)
    surf.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
    return img
