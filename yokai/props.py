"""Pixel-Art-Requisiten im Stil der Umgebungs-Tiles (1x Pixeldichte), prozedural gezeichnet und gecacht:
Türen (Shōji / offen / verschlossen / Boss mit Shimenawa), Item-Sockel, Gegner-Geschosse."""
import math
import pygame

_cache = {}
OUT = (14, 9, 16)


def sh(c, f):
    """Farbe aufhellen (f>1) oder abdunkeln (f<1), leicht Richtung Violett im Schatten (Mondlicht-Stil)."""
    if f < 1:
        r, g, b = c[0] * f, c[1] * f, c[2] * f
        b += (1 - f) * 18
        r += (1 - f) * 4
    else:
        r, g, b = (c[0] + (255 - c[0]) * (f - 1), c[1] + (255 - c[1]) * (f - 1), c[2] + (255 - c[2]) * (f - 1))
    return (max(0, min(255, int(r))), max(0, min(255, int(g))), max(0, min(255, int(b))))


def _box(s, x, y, w, h, base, hl=True):
    """Gefülltes Rechteck mit Licht oben/links, Schatten unten/rechts."""
    s.fill(base, (x, y, w, h))
    if hl:
        s.fill(sh(base, 1.28), (x, y, w, 1))
        s.fill(sh(base, 1.12), (x, y, 1, h))
    s.fill(sh(base, 0.62), (x, y + h - 1, w, 1))
    s.fill(sh(base, 0.78), (x + w - 1, y, 1, h))


def _outline(s):
    """1px dunkle Kontur um alle deckenden Pixel."""
    w, h = s.get_size()
    m = pygame.mask.from_surface(s, 1)
    o = pygame.Surface((w, h), pygame.SRCALPHA)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        o.blit(m.to_surface(setcolor=OUT + (255,), unsetcolor=(0, 0, 0, 0)), (dx, dy))
    o.blit(s, (0, 0))
    return o


# ---------------------------------------------------------------- Türen
WOOD = (92, 58, 40)


def door(accent, state, d, boss=False):
    """accent: Rahmenfarbe des Raumtyps; state: 'open'|'closed'|'locked'; d: 'n','s','w','e'.
    Liefert Surface (Mittelpunkt = Türmitte)."""
    key = ('door', accent, state, d, boss)
    if key in _cache:
        return _cache[key]
    W, H = 46, 26
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    wood = (70, 22, 26) if boss else WOOD
    # Öffnung
    ox, oy, ow, oh = 6, 6, 34, 18
    if state == 'open':
        for i in range(oh):
            f = i / oh
            c = (int(6 + 14 * f), int(4 + 8 * f), int(10 + 16 * f))
            s.fill(c, (ox, oy + i, ow, 1))
        s.fill((30, 22, 34), (ox, oy + oh - 2, ow, 2))          # Schwelle drinnen
        s.fill((2, 1, 4), (ox, oy, ow, 3))
    else:
        paper = (222, 210, 182)
        s.fill(paper, (ox, oy, ow, oh))
        for i in range(oh):                                      # Papier wird nach unten dunkler
            if i > oh * 0.55:
                s.fill(sh(paper, 1 - (i - oh * 0.55) / oh * 0.5), (ox, oy + i, ow, 1))
        s.fill(sh(paper, 1.08), (ox, oy, ow, 1))
        lat = sh(wood, 1.15)
        for gx in range(ox + 4, ox + ow, 5):                     # Shōji-Gitter
            s.fill(lat, (gx, oy, 1, oh))
        for gy in (oy + 5, oy + 11):
            s.fill(lat, (ox, gy, ow, 1))
        mid = ox + ow // 2
        s.fill(sh(wood, 0.8), (mid - 1, oy, 2, oh))              # Mittelfuge der Schiebetüren
        s.fill(sh(wood, 1.3), (mid - 1, oy, 1, oh))
        for hx in (mid - 4, mid + 3):                            # Griffmulden
            s.fill(sh(wood, 0.55), (hx, oy + 8, 1, 3))
    # Rahmen: Pfosten + Sturz (Kamoi) + Schwelle
    _box(s, 1, 1, 5, H - 1, wood)
    _box(s, W - 6, 1, 5, H - 1, wood)
    _box(s, 0, 0, W, 6, wood)
    s.fill(accent, (2, 2, W - 4, 2))                             # farbiges Band = Raumtyp
    s.fill(sh(accent, 1.35), (2, 2, W - 4, 1))
    s.fill(sh(accent, 0.6), (2, 4, W - 4, 1))
    for nx in (3, W - 4):                                        # Nagelköpfe
        s.set_at((nx, 2), (230, 200, 120))
    s.fill(sh(wood, 0.55), (6, H - 2, W - 12, 2))
    if state == 'locked':
        cx, cy = W // 2, oy + 8
        g, gd, gl = (222, 178, 64), (140, 96, 30), (255, 236, 150)
        pygame.draw.circle(s, gd, (cx, cy - 3), 3, 1)
        s.fill(gd, (cx - 4, cy - 1, 9, 7))
        s.fill(g, (cx - 3, cy, 7, 5))
        s.fill(gl, (cx - 3, cy, 7, 1))
        s.fill((40, 26, 12), (cx, cy + 2, 1, 2))
    if boss:                                                    # Shimenawa-Seil mit Shide-Papier
        rope, rd = (214, 190, 130), (150, 120, 70)
        for x in range(1, W - 1):
            y = 6 + int(2.2 * math.sin(math.pi * (x - 1) / (W - 2)))
            s.fill(rd if (x // 2) % 2 else rope, (x, y, 1, 2))
            s.set_at((x, y), sh(rope, 1.15))
        for x in (11, 23, 35):
            y = 6 + int(2.2 * math.sin(math.pi * (x - 1) / (W - 2))) + 2
            for k, (dx, dy) in enumerate(((0, 0), (1, 1), (0, 2), (1, 3), (0, 4))):
                s.fill((246, 244, 236), (x + dx, y + dy, 2, 1))
            s.set_at((x + 1, y + 4), (190, 186, 200))
    s = _outline(s)
    rot = {'n': 0, 's': 180, 'w': 90, 'e': -90}[d]
    if rot:
        s = pygame.transform.rotate(s, rot)
    _cache[key] = s
    return s


# ---------------------------------------------------------------- Item-Sockel (Steinaltar mit Opferpapier)
def pedestal(taken=False):
    key = ('ped', taken)
    if key in _cache:
        return _cache[key]
    s = pygame.Surface((26, 16), pygame.SRCALPHA)
    st = (112, 108, 126)
    _box(s, 4, 9, 18, 6, sh(st, 0.82))                          # Sockelfuß
    _box(s, 6, 5, 14, 5, st)                                    # Schaft
    _box(s, 2, 2, 22, 4, sh(st, 1.1))                           # Platte
    s.fill(sh(st, 1.45), (3, 2, 20, 1))
    for x, y in ((8, 11), (15, 12), (11, 7)):                   # Risse / Moos
        s.set_at((x, y), sh(st, 0.6))
    s.fill((70, 96, 62), (4, 14, 3, 1)); s.set_at((19, 14), (70, 96, 62))
    if not taken:                                               # rotes Tuch mit Goldrand
        s.fill((150, 34, 44), (9, 2, 8, 6))
        s.fill((196, 60, 64), (9, 2, 8, 1))
        s.fill((226, 180, 70), (9, 7, 8, 1))
    s = _outline(s)
    _cache[key] = s
    return s


# ---------------------------------------------------------------- Gegner-Geschosse
def orb(col, r):
    key = ('orb', col, r)
    if key in _cache:
        return _cache[key]
    R = r + 2
    n = R * 2 + 1
    s = pygame.Surface((n, n), pygame.SRCALPHA)
    pygame.draw.circle(s, OUT, (R, R), r + 1)
    pygame.draw.circle(s, sh(col, 0.6), (R, R), r)
    pygame.draw.circle(s, col, (R - (1 if r > 2 else 0), R - (1 if r > 2 else 0)), max(1, r - 1))
    if r >= 3:
        pygame.draw.circle(s, sh(col, 1.45), (R - 1, R - 1), max(1, r // 2))
    s.set_at((R - max(1, r // 2), R - max(1, r // 2)), (255, 255, 255))
    if r >= 4:
        s.set_at((R - r // 2 + 1, R - r // 2), (255, 255, 255))
    _cache[key] = s
    return s


# ---------------------------------------------------------------- Spieler-Ofuda (Hi-Res, gedreht + eingefärbt)
def ofuda(col, r, ang):
    from . import gfx
    step = int(round(math.degrees(ang) / 15)) % 24
    key = ('ofuda', col, int(r * 2), step)
    if key in _cache:
        return _cache[key]
    base = gfx.item_img('projectiles', 'ofuda', 0)
    if base is None:
        return None
    bb = base.get_bounding_rect()
    im = base.subsurface(bb).copy()
    f = max(0.8, r / 2.3)
    im = pygame.transform.scale(im, (max(4, int(bb.w * f)), max(3, int(bb.h * f))))
    if col != (250, 246, 232):
        im.fill(col + (255,), special_flags=pygame.BLEND_RGBA_MULT)
    im = pygame.transform.rotate(im, -step * 15)
    _cache[key] = im
    return im
