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



# ---------------------------------------------------------------- Türen in Hi-Res (doppelte Pixeldichte)
def _grain(s, x, y, w, h, base, seed):
    """Holzmaserung: feine, unterbrochene Längslinien."""
    import random as _r
    rr = _r.Random(seed)
    vertical = h > w
    n = (w if vertical else h) // 3
    for i in range(n):
        if vertical:
            gx = x + 1 + i * 3 + rr.randint(0, 1)
            y0 = y + rr.randint(0, h // 3)
            s.fill(sh(base, 0.8), (gx, y0, 1, rr.randint(h // 3, h - (y0 - y))))
        else:
            gy = y + 1 + i * 3 + rr.randint(0, 1)
            x0 = x + rr.randint(0, w // 3)
            s.fill(sh(base, 0.8), (x0, gy, rr.randint(w // 3, w - (x0 - x)), 1))


def door_hi(accent, state, d, boss=False):
    """Wie door(), aber in Hi-Res (92x52) mit feinem Shōji-Gitter, Maserung und Schloss."""
    key = ('door_hi', accent, state, d, boss)
    if key in _cache:
        return _cache[key]
    W, H = 92, 52
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    wood = (74, 24, 30) if boss else WOOD
    ox, oy, ow, oh = 12, 12, 68, 36
    if state == 'open':
        glow = sh(accent, 0.45)
        for i in range(oh):
            f = i / oh
            c = (int(4 + glow[0] * 0.35 * f), int(3 + glow[1] * 0.3 * f), int(8 + glow[2] * 0.35 * f))
            s.fill(c, (ox, oy + i, ow, 1))
        s.fill((1, 0, 3), (ox, oy, ow, 5))
        s.fill((1, 0, 3), (ox, oy, 3, oh)); s.fill((1, 0, 3), (ox + ow - 3, oy, 3, oh))
        s.fill(sh(wood, 0.5), (ox, oy + oh - 4, ow, 4))                 # Schwelle
        s.fill(sh(wood, 0.8), (ox, oy + oh - 4, ow, 1))
    else:
        paper = (226, 214, 186)
        for i in range(oh):
            f = max(0.0, (i - oh * 0.5) / oh)
            s.fill(sh(paper, 1 - f * 0.55), (ox, oy + i, ow, 1))
        s.fill(sh(paper, 1.1), (ox, oy, ow, 1))
        lat = sh(wood, 1.2)
        mid = ox + ow // 2
        for half in (0, 1):
            x0 = ox + half * (ow // 2)
            for gx in range(x0 + 6, x0 + ow // 2 - 2, 7):
                s.fill(lat, (gx, oy, 1, oh))
                s.fill(sh(lat, 0.7), (gx + 1, oy, 1, oh))
            for gy in (oy + 9, oy + 19, oy + 28):
                s.fill(lat, (x0, gy, ow // 2, 1))
                s.fill(sh(lat, 0.7), (x0, gy + 1, ow // 2, 1))
        s.fill(sh(wood, 0.75), (mid - 2, oy, 4, oh))                     # Rahmen der Schiebetüren
        s.fill(sh(wood, 1.3), (mid - 2, oy, 1, oh))
        for hx in (mid - 8, mid + 6):                                    # runde Griffmulden (hikite)
            pygame.draw.circle(s, sh(wood, 0.5), (hx, oy + 18), 2)
            s.set_at((hx - 1, oy + 17), sh(wood, 1.2))
    # Pfosten, Sturz, Schwelle
    for px_ in (2, W - 12):
        _box(s, px_, 2, 10, H - 2, wood)
        _grain(s, px_ + 2, 4, 6, H - 8, wood, px_)
    _box(s, 0, 0, W, 12, wood)
    _grain(s, 2, 6, W - 4, 5, wood, 7)
    s.fill(accent, (4, 4, W - 8, 4))                                     # farbiges Band = Raumtyp
    s.fill(sh(accent, 1.4), (4, 4, W - 8, 1))
    s.fill(sh(accent, 0.55), (4, 7, W - 8, 1))
    for nx in (6, W - 8):                                                # Nagelköpfe
        s.fill((150, 120, 60), (nx, 4, 3, 3)); s.set_at((nx, 4), (250, 226, 150))
    s.fill(sh(wood, 0.5), (12, H - 3, W - 24, 3))
    if state == 'locked':
        cx, cy = W // 2, oy + 17
        gd, g, gl, gh = (120, 78, 22), (210, 160, 52), (246, 210, 110), (255, 246, 200)
        pygame.draw.arc(s, (90, 90, 110), (cx - 5, cy - 12, 10, 14), 0, math.pi, 2)   # Bügel
        s.fill(gd, (cx - 8, cy - 4, 16, 13))
        s.fill(g, (cx - 7, cy - 3, 14, 11))
        s.fill(gl, (cx - 7, cy - 3, 14, 2)); s.fill(gh, (cx - 6, cy - 3, 4, 1))
        s.fill(sh(g, 0.75), (cx + 4, cy - 1, 3, 9))
        pygame.draw.circle(s, (40, 24, 10), (cx, cy + 1), 2)
        s.fill((40, 24, 10), (cx, cy + 2, 1, 4))
    if boss:                                                             # Shimenawa mit Shide
        rope, rd, rl = (214, 190, 130), (140, 110, 64), (246, 230, 176)
        for x in range(2, W - 2):
            y = 12 + int(5 * math.sin(math.pi * (x - 2) / (W - 4)))
            ph = (x // 3) % 2
            s.fill(rd, (x, y, 1, 5))
            s.fill(rope, (x, y + (0 if ph else 1), 1, 3))
            s.set_at((x, y + (0 if ph else 1)), rl)
        for x in (22, 46, 70):
            y = 12 + int(5 * math.sin(math.pi * (x - 2) / (W - 4))) + 4
            for k in range(4):                                           # Zickzack-Papier
                dx = 0 if k % 2 == 0 else 3
                s.fill((248, 246, 238), (x + dx, y + k * 4, 4, 4))
                s.fill((196, 192, 206), (x + dx, y + k * 4 + 3, 4, 1))
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


def pedestal_hi(taken=False):
    """Steinaltar (Hi-Res, 52x34): Sockel mit Stufe, Schaft, Platte mit rotem Tuch, Shide-Papier, Moos."""
    key = ('ped_hi', taken)
    if key in _cache:
        return _cache[key]
    W, H = 52, 34
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    st = (112, 108, 128)
    _box(s, 6, 24, 40, 9, sh(st, 0.78))                          # Fuß
    _box(s, 10, 20, 32, 5, sh(st, 0.9))                          # Stufe
    _box(s, 14, 10, 24, 11, st)                                  # Schaft
    s.fill(sh(st, 0.7), (32, 11, 5, 9))                          # Schattenseite
    _box(s, 4, 4, 44, 7, sh(st, 1.08))                           # Platte
    s.fill(sh(st, 1.5), (5, 4, 42, 1))
    s.fill(sh(st, 0.6), (4, 10, 44, 1))
    for (x, y, w) in ((18, 15, 3), (27, 27, 4), (12, 29, 2), (40, 7, 3)):   # Risse
        s.fill(sh(st, 0.55), (x, y, w, 1)); s.set_at((x + w, y + 1), sh(st, 0.55))
    moss, mossl = (58, 92, 56), (96, 140, 74)
    for (x, y, w) in ((7, 31, 6), (35, 32, 7), (42, 24, 3), (15, 20, 3)):
        s.fill(moss, (x, y, w, 2)); s.fill(mossl, (x + 1, y, w - 2, 1))
    if not taken:                                                # rotes Tuch mit Goldsaum, hängt vorn über
        s.fill((120, 26, 40), (16, 3, 20, 4))
        s.fill((168, 40, 52), (16, 3, 20, 1))
        s.fill((150, 34, 46), (18, 7, 16, 6))
        s.fill((120, 26, 40), (31, 7, 3, 6))
        s.fill((228, 182, 72), (18, 12, 16, 1))
        s.fill((255, 228, 140), (19, 12, 4, 1))
        for k, x in enumerate((10, 40)):                         # zwei Shide
            for j in range(3):
                dx = 0 if j % 2 == 0 else 2
                s.fill((246, 244, 236), (x + dx, 10 + j * 3, 3, 3))
                s.fill((190, 186, 204), (x + dx, 12 + j * 3, 3, 1))
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


# ---------------------------------------------------------------- Ladentheke des Tanuki-Händlers (2x für Hi-Res-Ebene)
def counter():
    key = ('counter',)
    if key in _cache:
        return _cache[key]
    s = pygame.Surface((48, 16), pygame.SRCALPHA)
    wd = (118, 76, 48)
    _box(s, 1, 4, 46, 11, sh(wd, 0.85))                         # Front
    for x in range(6, 46, 8):
        s.fill(sh(wd, 0.62), (x, 6, 1, 8))
    _box(s, 0, 1, 48, 4, wd)                                    # Platte
    s.fill(sh(wd, 1.4), (1, 1, 46, 1))
    s.fill((40, 52, 104), (3, 6, 42, 4))                        # Noren-Tuch mit Wappen
    s.fill((60, 76, 140), (3, 6, 42, 1))
    for x in (12, 24, 36):
        pygame.draw.circle(s, (232, 222, 196), (x, 8), 1)
    s = _outline(s)
    s = pygame.transform.scale(s, (s.get_width() * 2, s.get_height() * 2))
    _cache[key] = s
    return s


# ---------------------------------------------------------------- Schrein- und Raumobjekte
STONE = (112, 108, 126)


def _get(key, fn):
    s = _cache.get(key)
    if s is None:
        s = _outline(fn())
        _cache[key] = s
    return s


def saisen():
    def mk():
        s = pygame.Surface((28, 18), pygame.SRCALPHA)
        wd = (104, 64, 40)
        _box(s, 1, 6, 26, 11, sh(wd, 0.9))
        _box(s, 0, 3, 28, 4, wd)
        for i in range(6):                                       # Schräg-Latten im Deckel
            s.fill(sh(wd, 0.5), (3 + i * 4, 3, 2, 3))
            s.fill(sh(wd, 1.35), (3 + i * 4, 3, 1, 1))
        s.fill((226, 186, 74), (11, 9, 6, 5))                    # Messingplakette
        s.fill((255, 228, 140), (11, 9, 6, 1))
        s.fill((150, 104, 34), (12, 11, 4, 1))
        for x in (3, 24):
            s.fill(sh(wd, 0.55), (x, 16, 2, 2))
        rope = (214, 190, 130)                                   # Glockenseil
        s.fill(rope, (13, 0, 2, 3)); s.fill((200, 40, 44), (13, 0, 1, 2))
        return s
    return _get(('saisen',), mk)


def omikuji():
    def mk():
        s = pygame.Surface((20, 28), pygame.SRCALPHA)
        red = (186, 44, 40)
        _box(s, 3, 2, 14, 18, red)
        s.fill(sh(red, 1.35), (4, 2, 12, 1))
        s.fill((236, 226, 200), (6, 5, 8, 11))                   # Papierfeld
        s.fill((40, 24, 24), (9, 6, 2, 1)); s.fill((40, 24, 24), (8, 8, 4, 1))
        s.fill((40, 24, 24), (9, 10, 2, 4)); s.fill((40, 24, 24), (7, 12, 6, 1))
        s.fill((30, 18, 20), (9, 0, 2, 2))                       # Losstab
        _box(s, 5, 20, 10, 2, (80, 52, 34))
        _box(s, 2, 22, 16, 5, (96, 62, 40))
        for x in (1, 17):                                        # gebundene Zettel
            s.fill((246, 244, 236), (x, 14, 2, 4)); s.set_at((x, 18), (190, 186, 200))
        return s
    return _get(('omikuji',), mk)


def ema(col, used):
    """Ema: hölzerne Votivtafel (Fünfeck) an roter Kordel, mit gemaltem Zeichen."""
    def mk():
        s = pygame.Surface((22, 26), pygame.SRCALPHA)
        wood = (172, 130, 82) if not used else (110, 90, 70)
        s.fill((150, 30, 36), (10, 0, 2, 5))                      # Kordel
        pts = [(1, 9), (11, 3), (21, 9), (21, 23), (1, 23)]
        pygame.draw.polygon(s, sh(wood, 0.55), pts)
        pygame.draw.polygon(s, wood, [(2, 9), (11, 4), (20, 9), (20, 22), (2, 22)])
        s.fill(sh(wood, 1.2), (3, 10, 16, 1))
        for yy in (14, 18):                                      # Holzmaserung
            s.fill(sh(wood, 0.85), (4, yy, 6, 1)); s.fill(sh(wood, 0.85), (12, yy + 1, 5, 1))
        if not used:
            c = col
            pygame.draw.circle(s, sh(c, 0.6), (11, 15), 5)
            pygame.draw.circle(s, c, (11, 15), 4)
            s.fill(sh(c, 1.4), (9, 13, 2, 1))
        s.fill(sh(wood, 0.45), (1, 23, 21, 2))
        return s
    return _get(('ema', tuple(col), used), mk)


def onsen(used):
    def mk():
        s = pygame.Surface((58, 32), pygame.SRCALPHA)
        pygame.draw.ellipse(s, sh(STONE, 0.7), (0, 2, 58, 29))
        water = (70, 140, 168) if not used else (64, 96, 108)
        pygame.draw.ellipse(s, sh(water, 0.7), (5, 6, 48, 21))
        pygame.draw.ellipse(s, water, (6, 8, 46, 18))
        pygame.draw.ellipse(s, sh(water, 1.3), (14, 11, 22, 6), 1)
        import random as _r
        rng = _r.Random(4)
        for i in range(16):                                      # Randsteine
            a = i / 16 * math.tau
            x = 29 + math.cos(a) * 26 - 3
            y = 16 + math.sin(a) * 12 - 3
            w = rng.randint(6, 9)
            _box(s, int(x), int(y), w, 5, sh(STONE, rng.uniform(0.8, 1.05)))
        return s
    return _get(('onsen', used), mk)


def torii(col):
    def mk():
        s = pygame.Surface((44, 36), pygame.SRCALPHA)
        blk = (30, 22, 30)
        _box(s, 8, 6, 4, 29, col)                                # Pfeiler
        _box(s, 32, 6, 4, 29, col)
        s.fill(blk, (7, 31, 6, 4)); s.fill(blk, (31, 31, 6, 4))   # Kamaki-Sockel
        _box(s, 4, 11, 36, 3, col)                               # Nuki
        _box(s, 20, 6, 4, 6, sh(col, 0.85))                      # Gakuzuka
        _box(s, 2, 4, 40, 3, col)                                # Shimaki
        for x in range(0, 44):                                   # Kasagi, Enden geschwungen
            lift = 2 if x < 3 or x > 40 else (1 if x < 6 or x > 37 else 0)
            s.fill(blk, (x, 1 - lift + 2, 1, 2))
            s.set_at((x, 1 - lift + 2), (70, 56, 70))
        return s
    return _get(('torii', col), mk)


def hokora(oni):
    def mk():
        s = pygame.Surface((32, 32), pygame.SRCALPHA)
        wd = (96, 60, 40) if not oni else (70, 26, 30)
        acc = (230, 196, 90) if not oni else (200, 40, 50)
        _box(s, 5, 26, 22, 5, sh(STONE, 0.9))                    # Steinsockel
        _box(s, 8, 13, 16, 13, wd)                               # Schrein-Körper
        s.fill(sh(wd, 0.45), (12, 16, 8, 10))                    # Öffnung
        s.fill(acc, (15, 18, 2, 4))                              # Spiegel / Flamme
        s.fill(sh(acc, 1.4), (15, 18, 1, 1))
        for i in range(8):                                       # Satteldach
            s.fill(sh((60, 54, 72), 1.1 - i * 0.04), (3 + i, 12 - i, 26 - 2 * i, 1))
        s.fill((40, 36, 52), (2, 12, 28, 2))
        s.fill(acc, (15, 3, 2, 2))
        s.fill((246, 244, 236), (10, 15, 1, 3)); s.fill((246, 244, 236), (21, 15, 1, 3))
        return s
    return _get(('hokora', oni), mk)


def tea_bench():
    def mk():
        s = pygame.Surface((28, 12), pygame.SRCALPHA)
        red = (170, 40, 40)
        _box(s, 0, 2, 28, 4, red)                                # Bank mit rotem Tuch (Hiraki-mōsen)
        s.fill(sh(red, 1.35), (1, 2, 26, 1))
        wd = (90, 58, 38)
        for x in (2, 23):
            _box(s, x, 6, 3, 6, wd)
        _box(s, 9, 0, 10, 3, (60, 44, 34))                       # Tablett
        return s
    return _get(('tea_bench',), mk)


def tea_cup(col):
    def mk():
        s = pygame.Surface((10, 8), pygame.SRCALPHA)
        clay = (200, 190, 170)
        _box(s, 1, 2, 8, 6, clay)
        s.fill(col, (2, 2, 6, 2))
        s.fill(sh(col, 1.4), (2, 2, 3, 1))
        return s
    return _get(('tea_cup', col), mk)


def slots_cab():
    def mk():
        s = pygame.Surface((32, 40), pygame.SRCALPHA)
        fur = (138, 96, 60)
        pygame.draw.circle(s, fur, (16, 8), 7)                   # Tanuki-Kopf oben
        pygame.draw.circle(s, sh(fur, 0.7), (10, 3), 2); pygame.draw.circle(s, sh(fur, 0.7), (22, 3), 2)
        s.fill((40, 30, 30), (10, 7, 12, 3))                     # Maske
        s.fill((250, 240, 220), (12, 8, 2, 1)); s.fill((250, 240, 220), (18, 8, 2, 1))
        s.fill((230, 214, 186), (13, 11, 6, 3))
        red = (176, 46, 44)
        _box(s, 3, 15, 26, 22, red)
        s.fill(sh(red, 1.4), (4, 15, 24, 1))
        s.fill((20, 14, 20), (6, 18, 20, 9))                     # Fenster
        _box(s, 26, 18, 4, 3, (210, 180, 80))                    # Hebel
        s.fill((230, 190, 70), (8, 30, 16, 2))                   # Münzschlitz-Leiste
        s.fill((40, 26, 18), (14, 30, 4, 1))
        _box(s, 2, 36, 28, 3, (70, 46, 34))
        return s
    return _get(('slots',), mk)


def stairs_up():
    def mk():
        s = pygame.Surface((24, 22), pygame.SRCALPHA)
        for i in range(5):
            _box(s, 2 + i * 2, 17 - i * 4, 20 - i * 4, 5, sh(STONE, 0.7 + i * 0.08))
        return s
    return _get(('stairs',), mk)


# ---------------------------------------------------------------- Minimap-Symbole (Hi-Res, 2x)
MAP_COL = {
    'K': (14, 9, 16), 'W': (250, 246, 236), 'w': (196, 190, 200), 'R': (220, 54, 54), 'r': (140, 28, 38),
    'Y': (255, 214, 90), 'y': (200, 140, 40), 'o': (120, 70, 24), 'G': (110, 210, 110), 'g': (40, 120, 60),
    'P': (190, 110, 240), 'p': (100, 50, 150), 'B': (130, 210, 250), 'b': (50, 110, 180), 'O': (255, 150, 60),
    'D': (150, 100, 60), 'd': (90, 56, 34), 'k': (40, 32, 44), 'S': (240, 170, 200),
}
MAP_ICONS = {
    'boss': """
..WWWWWW..
.WWWWWWWW.
WWkkWWkkWW
WWkRWWkRWW
WWWWWWWWWW
.WWWkkWWW.
..WkWkWk..
..WWWWWW..""",
    'treasure': """
.oooooooo.
oyYYYYYYyo
oyyyyyyyyo
oooooooooo
oyyykkyyyo
oyyykYyyyo
oyyyyyyyyo
oooooooooo""",
    'shop': """
..YYYYYY..
.YyyyyyyY.
YyYYkkYYyY
YyYkkkkYyY
YyYkkkkYyY
YyYYkkYYyY
.YyyyyyyY.
..YYYYYY..""",
    'secret': """
..wwwww...
.wW...Ww..
......Ww..
....wWw...
...wW.....
...ww.....
..........
...WW.....""",
    'curse': """
...PPPP...
..PppppP..
.PpPWWPpP.
.PPWkkWPP.
.PpPWWPpP.
..PppppP..
...PPPP...
....pp....""",
    'challenge': """
O........O
.O......O.
..O....O..
...O..O...
....OO....
...O..O...
.dd....dd.
dd......dd""",
    'omikuji': """
...WW.....
..rRRRr...
..RWWWR...
..RWkWR...
..RWkWR...
..RWWWR...
..RRRRR...
..rrrrr...""",
    'hyakki': """
...PPPP...
..PPPPPP..
.PPWPPWPP.
.PPPPPPPP.
.PPpPPpPP.
..PPPPPP..
..P.PP.P..
.p..pp..p.""",
    'ema': """
....RR....
....RR....
...dDDd...
..dDDDDd..
.dDDYYDDd.
.dDYYYYDd.
.dDDYYDDd.
.dddddddd.""",
    'kakurenbo': """
...kkkk...
..kkkkkk..
..kSWWSk..
..kWkWkW..
...WWWW...
..RRRRRR..
.RRrRRrRR.
..RR..RR..""",
    'yomeiri': """
.O......O.
.OO....OO.
.OWWWWWWO.
OWWRWWRWWO
.WWWWWWWW.
..WWWWWW..
...WRRW...
....WW....""",
    'onsen': """
.B..B..B..
B..B..B...
.B..B..B..
..........
bBBBBBBBBb
BWBBBBBBWB
.BBBBBBBB.
..bbbbbb..""",
    'library': """
.pPPPPPPp.
.PWWWWWWP.
.PWkkkkWP.
.PWWWWWWP.
.PWkkkWWP.
.PWWWWWWP.
.pPPPPPPp.
..........""",
    'dojo': """
....RR....
...RRRR...
..RRRRRR..
.RRWRRWRR.
RRRRRRRRRR
..d.dd.d..
..d.dd.d..
.dddddddd.""",
    'teahouse': """
..w.w.....
...w.w....
GGGGGGGG..
GgggggggGG
GgggggggG.G
.GgggggG.G.
..GGGGG...
.gggggggg.""",
    'slots': """
.D......D.
DdD....DdD
DDDDDDDDDD
DkkWDDWkkD
DkWkDDkWkD
DDDDkkDDDD
.DDWWWWDD.
..DDDDDD..""",
}


def map_icon(kind):
    key = ('map', kind)
    if key in _cache:
        return _cache[key]
    g = MAP_ICONS.get(kind)
    if g is None:
        return None
    rows = [r for r in g.strip('\n').split('\n')]
    w = max(len(r) for r in rows)
    s = pygame.Surface((w + 2, len(rows) + 2), pygame.SRCALPHA)
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != '.':
                s.set_at((i + 1, j + 1), MAP_COL[ch])
    s = _outline(s)
    _cache[key] = s
    return s


# ---------------------------------------------------------------- Pfeil und Schwertwelle (Hi-Res, gedreht)
def arrow(ang):
    step = int(round(math.degrees(ang) / 10)) % 36
    key = ('arrow', step)
    if key in _cache:
        return _cache[key]
    s = pygame.Surface((30, 9), pygame.SRCALPHA)
    pygame.draw.line(s, (14, 9, 16), (1, 4), (24, 4), 3)
    pygame.draw.line(s, (196, 150, 96), (2, 4), (23, 4), 1)
    pygame.draw.polygon(s, (14, 9, 16), [(22, 0), (29, 4), (22, 8)])
    pygame.draw.polygon(s, (200, 206, 220), [(23, 2), (28, 4), (23, 6)])
    for dx in (1, 4):
        pygame.draw.line(s, (240, 236, 226), (dx, 1), (dx + 3, 4), 1)
        pygame.draw.line(s, (240, 236, 226), (dx, 7), (dx + 3, 4), 1)
    s = pygame.transform.rotate(s, -step * 10)
    _cache[key] = s
    return s


def crescent(ang):
    step = int(round(math.degrees(ang) / 10)) % 36
    key = ('cres', step)
    if key in _cache:
        return _cache[key]
    s = pygame.Surface((22, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (14, 9, 16), (2, 0, 18, 30))
    pygame.draw.ellipse(s, (200, 230, 255), (3, 1, 16, 28))
    pygame.draw.ellipse(s, (0, 0, 0, 0), (0, 2, 14, 26))
    pygame.draw.ellipse(s, (255, 255, 255), (13, 6, 4, 18), 1)
    s = pygame.transform.rotate(s, -step * 10)
    _cache[key] = s
    return s


# ---------------------------------------------------------------- Hitogata: Papierdiener des Onmyōji (2x)
def hitogata(tilt):
    step = int(round(tilt / 10)) % 36
    key = ('hitogata', step)
    if key in _cache:
        return _cache[key]
    s = pygame.Surface((16, 20), pygame.SRCALPHA)
    ol, pa, sh_ = (14, 9, 16), (240, 236, 226), (196, 188, 176)
    body = [(6, 5), (10, 5), (15, 8), (15, 10), (11, 9), (11, 13), (13, 19), (9, 19), (8, 15),
            (7, 19), (3, 19), (5, 13), (5, 9), (1, 10), (1, 8)]
    pygame.draw.polygon(s, ol, body)
    pygame.draw.polygon(s, pa, [(6, 6), (10, 6), (14, 8), (14, 9), (10, 8), (10, 13), (12, 18), (10, 18),
                                (8, 13), (6, 18), (4, 18), (6, 13), (6, 8), (2, 9), (2, 8)])
    pygame.draw.circle(s, ol, (8, 3), 3)
    pygame.draw.circle(s, pa, (8, 3), 2)
    pygame.draw.line(s, sh_, (9, 7), (9, 13))                       # Falz
    pygame.draw.rect(s, (200, 30, 40), (7, 9, 2, 3))                 # Siegel
    s = pygame.transform.rotate(s, -step * 10)
    _cache[key] = s
    return s
