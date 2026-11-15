"""Animierte Sprites – komplett selbst gezeichnet (Quellcode in art_src/, gebaut mit
pixelstudio). Metadaten in assets/sprites/sprites.json:
  kind 'dir4'  – Zellen cell x cell, Spalten = Blickrichtung (unten, oben, links, rechts),
                 Zeilen = Laufbilder
  kind 'strip' – n gleich breite Bilder nebeneinander, Blick nach links (rechts = gespiegelt)
"""
import json
import os
import sys
import pygame

_here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sprites')
if not os.path.isdir(_here) and hasattr(sys, '_MEIPASS'):
    _here = os.path.join(sys._MEIPASS, 'yokai', 'assets', 'sprites')
BASE = _here

DOWN, UP, LEFT, RIGHT = 0, 1, 2, 3

try:
    with open(os.path.join(BASE, 'sprites.json'), encoding='utf-8') as fh:
        META = json.load(fh)
except (OSError, ValueError):
    META = {}

_raw = {}
_cache = {}


def has(name):
    return name in META


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
    return 1


def is_hi(name):
    return bool(META.get(name, {}).get('hi'))


def size_of(name):
    """Größe in Weltpixeln (Hi-Res-Sprites zählen halb)."""
    m = META.get(name, {})
    w, h = m.get('w', 16), m.get('h', 16)
    if m.get('hi'):
        return w // 2, h // 2
    return w, h


def frame_count(name):
    m = META.get(name, {})
    return m.get('n', 4)


def frame(name, d=DOWN, f=0, scale=None, flash=False, tint=None, alpha=255):
    scale = 1 if scale is None else scale
    key = (name, d, f % 8, scale, flash, tint)
    s = _cache.get(key)
    if s is None:
        raw = _load(name)
        m = META[name]
        w, h = m['w'], m['h']
        n = m.get('n', 4)
        flip = False
        if m['kind'] == 'dir4':
            sub = raw.subsurface((min(3, d) * w, (f % n) * h, w, h))
        else:
            sub = raw.subsurface(((f % n) * w, 0, w, h))
            flip = d == RIGHT
        s = sub if scale == 1 else pygame.transform.scale(sub, (int(w * scale), int(h * scale)))
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


def hdir(dx):
    return RIGHT if dx > 0 else LEFT


def dir_from(dx, dy):
    if abs(dx) > abs(dy):
        return LEFT if dx < 0 else RIGHT
    return UP if dy < 0 else DOWN


def blit_center(surf, name, x, y, d=DOWN, f=0, scale=None, tint=None, flash=False, alpha=255):
    img = frame(name, d, f, scale, flash, tint, 255)
    if is_hi(name):
        from . import gfx
        gfx.hi_blit(img, x, y + img.get_height() / 4, alpha)
        return img
    if alpha < 255:
        img = img.copy(); img.set_alpha(alpha)
    surf.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
    return img
