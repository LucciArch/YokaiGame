"""Verwandlungs-Kostüme an der Spielfigur (Hi-Res-Teile aus assets/costume, siehe art_src/fable/items/costumes.py)."""
import json
import os
import pygame
from . import gfx, sheets

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'costume')
META = {}
_img = {}
_anchor = {}
try:
    META = json.load(open(os.path.join(DIR, 'costume.json')))
except Exception:
    META = {}


def piece(name, frame, flip):
    key = (name, frame, flip)
    im = _img.get(key)
    if im is None:
        m = META[name]
        if (name, 'strip') not in _img:
            _img[(name, 'strip')] = pygame.image.load(os.path.join(DIR, name + '.png')).convert_alpha()
        st = _img[(name, 'strip')]
        im = st.subsurface((frame * m['w'], 0, m['w'], m['h'])).copy()
        if flip:
            im = pygame.transform.flip(im, True, False)
        _img[key] = im
    return im


def anchors(spr):
    """(Kopf-x, Kopf-oben, Körpermitte-y) in Hi-Res-Pixeln des Sprites."""
    k = id(spr)
    a = _anchor.get(k)
    if a is None:
        bb = spr.get_bounding_rect()
        m = pygame.mask.from_surface(spr, 60)
        # Kopfoberkante = erste Zeile mit genug Masse (dünne Waffen/Haarnadeln ignorieren)
        top = bb.top
        for y in range(bb.top, bb.bottom):
            row = [x for x in range(bb.left, bb.right) if m.get_at((x, y))]
            if len(row) >= 8 and (max(row) - min(row)) <= len(row) + 6:
                top = y
                break
        xs = []
        for y in range(top, min(bb.bottom, top + 10)):
            row = [x for x in range(bb.left, bb.right) if m.get_at((x, y))]
            if row:
                # größter zusammenhängender Block = Kopf
                best, cur = [], [row[0]]
                for x in row[1:]:
                    if x == cur[-1] + 1:
                        cur.append(x)
                    else:
                        best = max(best, cur, key=len); cur = [x]
                best = max(best, cur, key=len)
                xs += best
        hx = sum(xs) / len(xs) if xs else bb.centerx
        a = (hx, top, (bb.top + bb.bottom) / 2)
        if len(_anchor) > 2000:
            _anchor.clear()
        _anchor[k] = a
    return a


# Kopf-Oberkante und Kopfmitte (Hi-Res-Pixel) im ersten Laufbild jeder Figur, von Hand ausgemessen
HEAD0 = {'hana': (56, 11), 'kenji': (72, 11), 'kuzunoha': (63, 12), 'ponpoko': (57, 11), 'benkei': (70, 10),
         'okiku': (75, 12), 'kotaro': (90, 12), 'seimei': (90, 4), 'akago': (48, 9), 'susanoo': (57, 16)}


def head_anchor(player, frame_idx):
    """Kopfanker für ein Bild: Handmessung aus Bild 0 + Verschiebung, die die Automatik zwischen Bild 0 und diesem Bild sieht."""
    base = HEAD0.get(player.char)
    f0 = sheets.frame(player.char, sheets.LEFT, 0)
    ff = sheets.frame(player.char, sheets.LEFT, frame_idx)
    a0, af = anchors(f0), anchors(ff)
    if base is None:
        return af[0], af[1]
    dx = max(-6, min(6, af[0] - a0[0]))
    dy = max(-6, min(6, af[1] - a0[1]))
    return base[0] + dx, base[1] + dy


# Figuren, die das Merkmal schon selbst tragen (Kuzunohas Fuchsschwänze, Kotarōs Flügel …), bekommen es nicht doppelt
OWN = {('kuzunoha', 'kitsune_back'), ('kuzunoha', 'kitsune_head'), ('ponpoko', 'tanuki_back'), ('ponpoko', 'tanuki_head'),
       ('okiku', 'yurei_head'), ('kotaro', 'tengu_back')}


def parts_for(player):
    out = []
    for t in player.transforms:
        for suf in ('back', 'head'):
            nm = '%s_%s' % (t, suf)
            if nm in META and (player.char, nm) not in OWN:
                out.append(nm)
    if player.f['fly'] and 'tengu' not in player.transforms and 'yurei' not in player.transforms and player.char not in ('okiku', 'kotaro'):
        out.append('fly_back')
    return out


def draw(player, spr, x, by, facing_right, t, layer, alpha=255):
    """x, by: Weltposition, an der das Figuren-Sprite (Mitte unten) gezeichnet wird."""
    if not META:
        return
    names = [n for n in parts_for(player) if META[n]['layer'] == layer]
    if not names:
        return
    w, h = spr.get_size()
    _, _, mid = anchors(spr)
    hx, top = head_anchor(player, getattr(player, '_cur_frame', 0))
    if facing_right:
        hx = w - 1 - hx
    left = x - w / 4
    topw = by - h / 2
    for nm in names:
        m = META[nm]
        fr = int(t * 6) % m['n']
        im = piece(nm, fr, facing_right)
        ax = (m['w'] - m['ax']) if facing_right else m['ax']
        if nm.endswith('_head'):
            px_, py_ = left + hx / 2, topw + top / 2
        else:
            px_, py_ = x, topw + mid / 2
        cx = px_ + (m['w'] / 2 - ax) / 2
        bottom = py_ + (m['h'] - m['ay']) / 2
        gfx.hi_blit(im, cx, bottom, alpha)
