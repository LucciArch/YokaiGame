"""Grafik: Pixel-Art-Sprites (ASCII), Item-Icons, Biome-Kacheln, Text-Ebene."""
import math
import random
import pygame
from .settings import *

PAL = {
    'k': (22, 16, 28), 'w': (240, 236, 226), 'l': (170, 168, 180), 'd': (70, 66, 84),
    'r': (214, 52, 56), 'R': (130, 26, 40), 'o': (240, 140, 50), 'y': (250, 214, 90),
    'g': (96, 190, 90), 'G': (40, 110, 60), 'b': (70, 120, 220), 'B': (36, 56, 130),
    'c': (120, 220, 230), 'p': (160, 90, 210), 'P': (90, 44, 130), 'n': (150, 96, 60),
    'N': (88, 54, 36), 's': (246, 204, 170), 'S': (210, 150, 120), 'h': (44, 34, 58),
    'm': (244, 150, 180), 'M': (190, 80, 120), 'e': (255, 240, 120), 'v': (220, 170, 255),
    't': (70, 180, 170), 'T': (30, 110, 110), 'i': (200, 240, 255), 'f': (255, 190, 70),
    'z': (196, 222, 255), 'x': (232, 190, 70), 'q': (110, 120, 150),
}

SPRITES = {
    # ---------------- Spielfiguren ----------------
    'hana': [
        "....hhhh....", "...hhhhhhr..", "..hhhhhhhrr.", "..hssssssh..", "..hsksskhh..",
        "..hssssssh..", "..hhSssShh..", "..hwwrrwwh..", ".swwwwwwwws.", ".swwwwwwwws.",
        "..rrrrrrrr..", "..rrrrrrrr..", "..rrr..rrr..", "..kk....kk.."],
    'kenji': [
        ".....hh.....", "....hhhh....", "...hhhhhh...", "..hhssssh...", "..hskssks...",
        "..hssssss...", "...sSSSs....", "..qqqwqqqn..", ".sqqqwqqqns.", "..qqqqqqqn..",
        "..NNNNNNNN..", "..NNNNNNNN..", "..NNN..NNN..", "..kk....kk.."],
    'kuzunoha': [
        ".ow......wo.", ".oww....wwo.", "..wwwwwwww..", "..wwwwwwww..", "..wsssssw...",
        "..skssskss..", "..ssssmsss..", "...pppppp...", "..sppppppso.", "..ppppppppoo",
        "..PPPPPPPPow", "..PPPPPPPP..", "..PPP..PPP..", "..kk....kk.."],
    'ponpoko': [
        "....gg......", "..n..g...n..", "..nnnnnnnn..", ".nnnnnnnnnn.", ".nkkwnnwkkn.",
        ".nkewnnwekn.", ".nnnnkknnnn.", "..nnSSSSnn..", ".nnSSSSSSnn.", ".nnSSSSSSnn.",
        ".nnnSSSSnnn.", "..nnnnnnnn..", "..NN....NN..", "..kk....kk.."],
    'benkei': [
        "...wwwwww...", "..wwwwwwww..", ".wwwssssww..", ".wwsksskww..", ".wwssssssw..",
        "..wwSSSSw...", ".dddyyyyddd.", "sddddyydddds", "sdddddddddds", ".dddddddddd.",
        ".dddddddddd.", ".dddddddddd.", "..ddd..ddd..", "..kk....kk.."],
    'okiku': [
        "...hhhhhh...", "..hhhhhhhh..", "..hhzzzzhh..", ".hhzkzzkzhh.", ".hhzzzzzzhh.",
        ".hhhzzzzhhh.", ".hhwwwwwwhh.", "zhwwwwwwwwhz", ".hwwwwwwwwh.", "..wwwwwwww..",
        "..wwwwwwww..", "...wwwwww...", "....wwww....", ".....ww....."],
    'kotaro': [
        ".....kk.....", "....kkkk....", "...rrrrrr...", "..rrkrrkrr..", "..rrrrrrrrrr",
        "..rrrrrr....", "kk.yyyyyy.kk", "kkkyyyyyykkk", "kkyyyyyyyykk", ".kyyyyyyyyk.",
        "..wwwwwwww..", "..wwwwwwww..", "..www..www..", "..NN....NN.."],
    'seimei': [
        "....kkk.....", "....kkkk....", "...kkkkk....", "..hhhhhhh...", "..hssssssh..",
        "..hsksskhh..", "..hssssssh..", "..wwwPPwww..", ".wwwwPPwwww.", ".swwwwwwwws.",
        "..PPPPPPPP..", "..PPPPPPPP..", "..PPP..PPP..", "..kk....kk.."],
    'akago': [
        "..y......y..", "..yy.hh.yy..", "...hhhhhh...", "..hrrrrrrh..", "..rrkrrkrr..",
        "..rrrrrrrr..", "..rrwrrwrr..", "...rrrrrr...", ".rrrrrrrrrr.", ".rr.rrrr.rr.",
        "..yykyykyy..", "..yyyyyyyy..", "..rr....rr..", "..rr....rr.."],
    'susanoo': [
        "..hh.hh.hh..", ".hhhhhhhhhh.", ".hhhhhhhhhh.", "..hssssssh..", "..hsksskshh.",
        "..hssssssh..", "..hhSssShh..", ".xbbbxbbbbx.", "sxbbbxbbbbxs", ".xbbbbbbbbx.",
        "..BBBBBBBB..", "..BBBBBBBB..", "..BBB..BBB..", "..kk....kk.."],
    # ---------------- Yokai ----------------
    'hitodama': [
        "......c.....", ".....cc.....", "....ccz.....", "...cczzc....", "..cczwwzc...",
        "..czwwwwzc..", ".cczwkwkzc..", ".czwwwwwwzc.", ".czwwwwwwzc.", "..czwwwwzc..",
        "...cczzcc...", "....cccc...."],
    'kodama': [
        "...wwwwww...", "..wwwwwwww..", ".wwwkwwkwww.", ".wwwkwwkwww.", ".wwwwwwwwww.",
        ".wwwwkkwwww.", "..wwwwwwww..", "...wwwwww...", "..www..www..", ".www....www.",
        "..ww....ww..", "............"],
    'kappa': [
        "...nnnnnn...", "..nwwwwwwn..", "..gggggggg..", ".gkggggkgg..", ".ggyyyyggg..",
        ".gggyyggggG.", "..ggggggGGG.", ".gggggggGnG.", "gg.gggggGGG.", "...gggggGG..",
        "...gg..gg...", "..yy....yy.."],
    'kasa_obake': [
        ".....r......", "...rrrrrr...", "..rrwrrwrr..", ".rrrrrrrrrr.", "rrrwwwwwwrrr",
        "rrrwwkewrrrr", "rrrrwwwrrrrr", "r.r.rmmr.r.r", ".....mm.....", ".....nn.....",
        ".....nn.....", "....ssss...."],
    'bakezori': [
        "............", "..nnnnnnnn..", ".nyyyyyyyyn.", ".nyywwyyyyn.", ".nywkewyyyn.",
        ".nyywwyyyyn.", ".nyyyyrryyn.", ".nyyyrrmryn.", ".nyyyyrryyn.", ".nyyyyyyyyn.",
        "..nnnnnnnn..", "..r......r.."],
    'tsuchinoko': [
        "............", "............", "...nnnn.....", "..nnnnnn....", ".nnkwnnnnn..",
        ".nnnnnnnnnn.", "nnyyyyyyynnn", "nnyyyyyyyynn", ".nnnnnnnnnnN", "..nnnnnnnnNN",
        "...NNNNNNN..", "............"],
    'kitsunebi_e': [
        "............", ".w...w......", ".ww.ww......", ".wwwww...cc.", ".wkwkw..ccc.",
        ".wwwwrw.cc..", "..wwwwwwwc..", "..wwwwwwww..", "..wwwwwwww..", "..w.w..w.w..",
        "............", "............"],
    'chochin': [
        "....kkkk....", "...wwwwww...", "..ywwwwwwy..", ".yykwwwwkyy.", ".ywwwwwwwwy.",
        ".yykkkkkkyy.", ".ywwwrrwwwy.", ".ywwrmmrwwy.", ".yykkkkkkyy.", "..ywwwwwwy..",
        "...kkkkkk...", "....k..k...."],
    'nopperabo': [
        "...hhhhhh...", "..hhhhhhhh..", "..hssssssh..", "..hssssssh..", "..hssssssh..",
        "...ssssss...", "..qqqwwqqq..", ".sqqqwwqqqs.", "..qqqqqqqq..", "..qqqqqqqq..",
        "..qqq..qqq..", "..kk....kk.."],
    'gaki': [
        "...llll.....", "..llllll....", "..lklkll....", "..llllll....", "..lrrrll....",
        "..llllll....", ".l.lllll.l..", "l.llllllll.l", "..lllllllll.", "..llllllll..",
        "...l....l...", "..ll....ll.."],
    'gaki_small': [
        "..llll..", ".lklkl..", ".llrll..", "llllll.l", ".lllll..", ".llllll.", "..l..l..", ".ll..ll."],
    'ittan_momen': [
        "..www.......", ".wwkw.......", ".wwww.......", "..wwww......", "...wwwww....",
        "....wwwwww..", "......wwwww.", ".......wwwww", "........wwww", ".........www",
        "..........ww", "...........w"],
    'bakeneko': [
        "............", ".p.....p..pp", ".pp...pp.pp.", ".ppppppp.p..", ".pepppep.p..",
        ".ppppppp.p..", ".pppmmppp...", "..ppppppp...", "..pppppppp..", "..pppppppp..",
        "..pp.pp.pp..", "..kk.kk.kk.."],
    'onibi': [
        ".....p......", "....pp......", "...ppv.p....", "...pvvpp....", "..ppvwvpp...",
        "..pvwwwvp...", ".ppvwkwvpp..", ".pvwwwwwvp..", ".pvwwwwwvp..", "..pvwwwvp...",
        "...ppvpp....", "....ppp....."],
    'karasu_tengu': [
        "....kkkk....", "...kkkkkk...", "...kekkek...", "...kkyyyk...", "....kyyk....",
        "kk..kkkk..kk", "kkk.yyyy.kkk", "kkkkyyyykkkk", ".kkkyyyykkk.", "....kkkk....",
        "....kk.kk...", "...yy...yy.."],
    'yuki_warashi': [
        "...iiiiii...", "..iiiiiiii..", "..iwwwwwwi..", "..wkwwwkww..", "..wwwwwwww..",
        "...wwmmww...", "..ciiiiiic..", ".wiiiiiiiiw.", "..iiiiiiii..", "..cccccccc..",
        "..ccc..ccc..", "..ww....ww.."],
    'kamaitachi': [
        "............", "l.........l.", "ll.......ll.", ".l..nnn..l..", ".l.nnnnn.l..",
        "..lnknknl...", "...nnnnn....", "..nnwwwnn...", ".nnnwwwnnn..", "..nnnnnnnnnn",
        "...nn..nn..n", "............"],
    'yamabiko': [
        "..q......q..", "..qq....qq..", "..qqqqqqqq..", ".qqwwqqwwqq.", ".qqwkqqkwqq.",
        ".qqqqqqqqqq.", ".qqqrrrrqqq.", "..qqrmmrqq..", "...qqqqqq...", "..qqqqqqqq..",
        ".qq.qqqq.qq.", "..q......q.."],
    'heikegani': [
        "r..........r", "rr........rr", ".rr.rrrr.rr.", "..rrrrrrrr..", ".rrRkRRkRrr.",
        "rrrRRRRRRrrr", "rrrRRkkRRrrr", ".rrrRRRRrrr.", "..rrrrrrrr..", ".r.r....r.r.",
        "r..r....r..r", "............"],
    'funayurei': [
        "...zzzzzz...", "..zzzzzzzz..", "..zkzzzzkz..", "..zzzzzzzz..", "...zzkkzz...",
        "..zzzzzzzzn.", ".zzzzzzzzznn", "..zzzzzzz..n", "...zzzzzz...", "....zzzz....",
        ".....zz.....", "......z....."],
    'ningyo': [
        "...hhhhh....", "..hhssshh...", "..hskskhh...", "..hssssh....", "..hmmmmhh...",
        ".sstttttss..", "...tttttt...", "....tttttt..", ".....ttttt..", "......tttt..",
        "....tTT.tt..", "...tTT......"],
    'isonade': [
        "............", ".....q......", "....qq......", "...qqq......", "..qqqqqqq...",
        ".qqqqqqqqqq.", "qqkqqqqqqqqq", "qwwwwqqqqqqq", ".qwqwqqqqqq.", "..qqqqqqq...",
        "............", "............"],
    'oni': [
        "..y........y..", "..yy..hh..yy..", "...yhhhhhhy...", "...rrrrrrrr...", "..rrkerrkerr..",
        "..rrrrrrrrrr..", "..rrwrrrrwrr..", "...rrrrrrrr.nn", ".rrrrrrrrrrrnn", "rrrrrrrrrrrrn.",
        "rr.yykyykyy.n.", "...yyyyyyyy...", "...rrr..rrr...", "...rrr..rrr..."],
    'shikome': [
        ".llllllll...", "llllllllll..", "llggggggll..", "lgegggeggl..", "lggggggggl..",
        "lgkkkkkggl..", ".ddddddddd..", "gddddddddg..", "gdddddddddg.", ".dddddddd...",
        ".ddd..ddd...", ".gg....gg..."],
    'tsuchigumo': [
        "..k........k..", "...k......k...", "k...nnnnnn...k", ".k.nnnnnnnn.k.", "..knnrnnrnnk..",
        "kkknnnnnnnnkkk", "...nnnnnnnn...", "kkknnyyyynnkkk", "..knnnnnnnnk..", ".k..nnnnnn..k.",
        "k...........k.", ".............."],
    'kumo': [
        "k.kkkk.k", ".kkrrkk.", "kkkkkkkk", ".kkkkkk.", "k.k..k.k", "........"],
    'shinigami': [
        ".........lll..", "...dddd....ll.", "..dddddd....l.", "..ddwwdd....l.", ".dddkwkdd...l.",
        ".dddwwwdd..n..", ".ddddddddddn..", "dddddddddd.n..", "dddddddddd.n..", ".dddddddd..n..",
        ".dddddddd..n..", "..dddddd...n..", "...dddd.......", ".............."],
    'kappa_small': [
        "..nnnn..", ".gwwwwg.", "gkggkgg.", "gyyyyggG", ".ggggGG.", ".gg..gg.", "yy....yy", "........"],
    'karasu': [
        "...kk...", "..kekk..", "..kkyy..", "k.kkk..k", "kkkkkkkk", ".kkkkkk.", "..k..k..", "........"],
}

_cache = {}


def sprite(name, flip=False, flash=False, tint=None, scale=1):
    key = (name, flip, flash, tint, scale)
    s = _cache.get(key)
    if s is not None:
        return s
    if (name, False, False, None, 1) not in _cache:
        rows = SPRITES[name]
        w, h = len(rows[0]), len(rows)
        base = pygame.Surface((w, h), pygame.SRCALPHA)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != '.':
                    base.set_at((x, y), PAL[ch])
        _cache[(name, False, False, None, 1)] = base
    s = _cache[(name, False, False, None, 1)]
    if scale != 1:
        s = pygame.transform.scale(s, (s.get_width() * scale, s.get_height() * scale))
    if tint:
        s = s.copy()
        t = pygame.Surface(s.get_size(), pygame.SRCALPHA)
        t.fill(tint + (0,))
        s.fill(tint, special_flags=pygame.BLEND_RGB_MULT)
        s.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_ADD)
    if flash:
        s = s.copy()
        s.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_MAX)
    if flip:
        s = pygame.transform.flip(s, True, False)
    _cache[key] = s
    return s


# ---------------------------------------------------------------- Leuchten
_glow = {}


def glow(radius, color, alpha=90):
    key = (radius, color, alpha)
    g = _glow.get(key)
    if g:
        return g
    radius = max(1, radius)
    g = pygame.Surface((radius * 2, radius * 2))
    g.fill((0, 0, 0))
    for i in range(radius, 0, -1):
        f = alpha / 255 * (1 - i / radius) ** 1.6
        pygame.draw.circle(g, tuple(int(c * f) for c in color), (radius, radius), i)
    _glow[key] = g
    return g


def draw_glow(surf, x, y, radius, color, alpha=90):
    surf.blit(glow(int(radius), color, alpha), (x - radius, y - radius), special_flags=pygame.BLEND_RGB_ADD)


_shadow = {}


def shadow(surf, rect, alpha=90):
    r = pygame.Rect(rect)
    key = (r.w, r.h, alpha)
    sh = _shadow.get(key)
    if sh is None:
        sh = pygame.Surface((max(1, r.w), max(1, r.h)), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, alpha), sh.get_rect())
        _shadow[key] = sh
    surf.blit(sh, r.topleft)


# ---------------------------------------------------------------- Item-Icons
def _c(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def draw_icon(surf, icon, col, x, y):
    """Zeichnet ein 16x16 Item-Icon an (x,y)=Mitte."""
    key = ('icon', icon, col)
    s = _cache.get(key)
    if s is None:
        s = pygame.Surface((18, 18), pygame.SRCALPHA)
        _icon(s, icon, col)
        # Umriss
        o = pygame.Surface((18, 18), pygame.SRCALPHA)
        mask = pygame.mask.from_surface(s)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            o.blit(mask.to_surface(setcolor=(18, 12, 24, 255), unsetcolor=(0, 0, 0, 0)), (dx, dy))
        o.blit(s, (0, 0))
        s = o
        _cache[key] = s
    surf.blit(s, (int(x) - 9, int(y) - 9))


def _icon(s, icon, col):
    d = _c(col, 0.6)
    l = _c(col, 1.35)
    D = pygame.draw
    k = (24, 18, 30)
    if icon == 'sword':
        D.line(s, l, (4, 14), (14, 4), 3); D.line(s, (255, 255, 255), (6, 12), (14, 4), 1)
        D.line(s, (200, 160, 60), (3, 11), (7, 15), 2); D.line(s, k, (2, 16), (4, 14), 2)
    elif icon == 'mirror':
        D.circle(s, d, (9, 8), 7); D.circle(s, l, (9, 8), 5); D.line(s, (255, 255, 255), (7, 6), (9, 4), 1)
        D.rect(s, d, (8, 14, 3, 3))
    elif icon == 'magatama':
        D.circle(s, col, (8, 7), 5); D.circle(s, col, (10, 12), 3); D.circle(s, k, (7, 6), 1)
        D.circle(s, l, (6, 5), 1)
    elif icon == 'mask':
        D.ellipse(s, col, (3, 2, 12, 14)); D.ellipse(s, k, (5, 6, 3, 2)); D.ellipse(s, k, (10, 6, 3, 2))
        D.line(s, (210, 40, 40), (6, 12), (12, 12), 1); D.line(s, (210, 40, 40), (4, 4), (7, 5), 1)
        D.line(s, (210, 40, 40), (14, 4), (11, 5), 1)
    elif icon == 'scroll':
        D.rect(s, (236, 226, 196), (4, 3, 10, 12)); D.rect(s, d, (3, 2, 12, 2)); D.rect(s, d, (3, 14, 12, 2))
        for yy in (6, 9, 12):
            D.line(s, col, (6, yy), (12, yy), 1)
    elif icon == 'bell':
        D.polygon(s, col, [(9, 2), (14, 12), (4, 12)]); D.rect(s, d, (3, 12, 12, 2)); D.circle(s, l, (9, 15), 2)
        D.line(s, l, (8, 5), (6, 10), 1)
    elif icon == 'fan':
        D.polygon(s, col, [(9, 15), (2, 6), (5, 3), (9, 2), (13, 3), (16, 6)])
        for a in range(5):
            ang = math.pi * (1.15 + a * 0.17)
            D.line(s, d, (9, 15), (9 + math.cos(ang) * 8, 15 + math.sin(ang) * 11), 1)
    elif icon == 'gourd':
        D.circle(s, col, (9, 12), 5); D.circle(s, col, (9, 6), 3); D.rect(s, (230, 220, 200), (5, 9, 8, 1))
        D.rect(s, (120, 80, 50), (8, 1, 2, 3)); D.circle(s, l, (7, 11), 1)
    elif icon == 'coin':
        D.circle(s, col, (9, 9), 7); D.circle(s, d, (9, 9), 7, 1); D.rect(s, k, (7, 7, 4, 4))
    elif icon == 'flame':
        D.polygon(s, col, [(9, 1), (14, 9), (13, 14), (9, 16), (5, 14), (4, 9)])
        D.polygon(s, l, [(9, 6), (12, 11), (9, 15), (6, 11)])
    elif icon == 'feather':
        D.line(s, d, (4, 15), (14, 3), 1)
        for i in range(8):
            px, py = 5 + i * 1.2, 14 - i * 1.4
            D.line(s, col, (px, py), (px - 3, py - 2), 2); D.line(s, col, (px, py), (px + 2, py + 2), 1)
    elif icon == 'beads':
        for i in range(10):
            a = i / 10 * math.tau
            D.circle(s, col if i % 3 else l, (9 + math.cos(a) * 6, 8 + math.sin(a) * 6), 2)
        D.line(s, d, (9, 14), (9, 17), 2)
    elif icon == 'drum':
        D.ellipse(s, (180, 120, 70), (2, 4, 14, 12)); D.ellipse(s, (240, 230, 210), (3, 4, 12, 6))
        D.circle(s, col, (9, 7), 2)
    elif icon == 'bow':
        D.arc(s, col, (2, 1, 10, 16), -1.5, 1.5, 2); D.line(s, (240, 240, 240), (7, 1), (7, 17), 1)
        D.line(s, l, (4, 9), (16, 9), 1); D.polygon(s, l, [(16, 9), (13, 7), (13, 11)])
    elif icon == 'lantern':
        D.rect(s, k, (7, 1, 4, 2)); D.ellipse(s, col, (3, 3, 12, 12)); D.rect(s, k, (6, 14, 6, 2))
        for yy in (6, 9, 12):
            D.line(s, d, (4, yy), (14, yy), 1)
        D.circle(s, (255, 240, 180), (9, 9), 2)
    elif icon == 'omamori':
        D.rect(s, col, (4, 4, 10, 12)); D.polygon(s, col, [(4, 4), (9, 1), (14, 4)])
        D.rect(s, (240, 210, 90), (6, 7, 6, 6)); D.line(s, l, (9, 0), (9, 3), 1)
    elif icon == 'cup':
        D.polygon(s, col, [(3, 6), (15, 6), (12, 14), (6, 14)]); D.ellipse(s, l, (3, 4, 12, 4))
        D.rect(s, d, (6, 14, 6, 2))
    elif icon == 'fang':
        D.polygon(s, col, [(5, 2), (13, 2), (9, 16)]); D.line(s, l, (7, 3), (9, 12), 1)
    elif icon == 'eye':
        D.ellipse(s, (240, 240, 240), (1, 5, 16, 8)); D.circle(s, col, (9, 9), 3); D.circle(s, k, (9, 9), 1)
    elif icon == 'leaf':
        D.ellipse(s, col, (3, 3, 12, 10)); D.line(s, d, (4, 15), (13, 4), 1)
    elif icon == 'flower':
        for i in range(5):
            a = i / 5 * math.tau - 1.57
            D.circle(s, col, (9 + math.cos(a) * 4, 9 + math.sin(a) * 4), 3)
        D.circle(s, (255, 230, 120), (9, 9), 2)
    elif icon == 'tail':
        D.ellipse(s, col, (2, 5, 14, 8)); D.ellipse(s, (250, 250, 250), (11, 6, 6, 6))
    elif icon == 'cloud':
        for cx, cy, r in ((6, 10, 4), (10, 8, 5), (13, 11, 3)):
            D.circle(s, col, (cx, cy), r)
        D.line(s, l, (5, 13), (14, 13), 1)
    elif icon == 'wave':
        D.circle(s, col, (9, 10), 7); D.circle(s, (0, 0, 0, 0), (12, 12), 5)
        D.circle(s, (255, 255, 255), (13, 7), 2)
    elif icon == 'star':
        pts = []
        for i in range(10):
            a = i / 10 * math.tau - 1.57
            r = 8 if i % 2 == 0 else 3.5
            pts.append((9 + math.cos(a) * r, 9 + math.sin(a) * r))
        D.polygon(s, col, pts); D.polygon(s, l, pts, 1)
    elif icon == 'moon':
        D.circle(s, col, (9, 9), 7); D.circle(s, (0, 0, 0, 0), (12, 7), 6)
    elif icon == 'skull':
        D.circle(s, (230, 226, 210), (9, 7), 6); D.rect(s, (230, 226, 210), (6, 11, 7, 4))
        D.circle(s, k, (7, 7), 2); D.circle(s, k, (11, 7), 2)
    elif icon == 'crystal':
        D.polygon(s, col, [(9, 1), (15, 7), (9, 17), (3, 7)]); D.polygon(s, l, [(9, 1), (11, 7), (9, 17), (7, 7)])
    elif icon == 'doll':
        D.polygon(s, (244, 240, 230), [(9, 2), (12, 5), (16, 8), (12, 9), (13, 16), (9, 13), (5, 16), (6, 9), (2, 8), (6, 5)])
        D.circle(s, col, (9, 5), 2); D.line(s, col, (8, 10), (10, 10), 1)
    elif icon == 'crane':
        D.polygon(s, (250, 250, 250), [(1, 10), (8, 8), (9, 2), (11, 8), (17, 6), (12, 12), (6, 13)])
        D.line(s, col, (8, 8), (11, 8), 1); D.circle(s, col, (2, 10), 1)
    elif icon == 'hammer':
        D.line(s, (150, 100, 60), (4, 15), (11, 8), 2); D.rect(s, col, (8, 2, 9, 7)); D.rect(s, l, (8, 2, 9, 2))
    elif icon == 'bag':
        D.circle(s, col, (9, 11), 6); D.polygon(s, col, [(6, 3), (12, 3), (11, 7), (7, 7)]); D.line(s, d, (6, 6), (12, 6), 1)
    elif icon == 'thread':
        for i in range(4):
            D.arc(s, col, (2 + i, 2 + i * 3, 14 - i, 6), 0, 3.1, 1)
        D.line(s, l, (9, 1), (9, 16), 1)
    elif icon == 'cloth':
        D.polygon(s, col, [(3, 3), (15, 3), (13, 16), (5, 16)]); D.line(s, d, (9, 3), (9, 16), 1)
        D.line(s, l, (3, 3), (9, 9), 1); D.line(s, l, (15, 3), (9, 9), 1)
    elif icon == 'heart':
        D.circle(s, col, (6, 7), 4); D.circle(s, col, (12, 7), 4); D.polygon(s, col, [(2, 8), (16, 8), (9, 16)])
    elif icon == 'daruma':
        D.ellipse(s, col, (2, 2, 14, 15)); D.ellipse(s, (246, 220, 200), (5, 5, 8, 7)); D.circle(s, k, (7, 8), 1)
        D.circle(s, (240, 240, 240), (11, 8), 1)
    elif icon == 'fish':
        D.ellipse(s, col, (2, 5, 12, 8)); D.polygon(s, col, [(13, 9), (17, 5), (17, 13)]); D.circle(s, k, (5, 8), 1)
    elif icon == 'box':
        D.rect(s, col, (2, 5, 14, 10)); D.rect(s, d, (2, 5, 14, 3)); D.rect(s, (240, 210, 90), (8, 8, 2, 3))
    elif icon == 'dango':
        D.line(s, (180, 140, 90), (2, 16), (16, 2), 1)
        for i, cc in enumerate(((240, 160, 190), (250, 250, 240), (140, 200, 120))):
            D.circle(s, cc, (5 + i * 4, 13 - i * 4), 3)
    elif icon == 'rice':
        D.polygon(s, (250, 250, 248), [(9, 2), (16, 14), (2, 14)]); D.rect(s, (30, 50, 40), (5, 10, 8, 5))
    elif icon == 'shell':
        D.polygon(s, col, [(2, 12), (9, 2), (16, 12), (9, 16)]); D.line(s, l, (9, 2), (9, 15), 1)
        D.line(s, l, (9, 2), (5, 13), 1); D.line(s, l, (9, 2), (13, 13), 1)
    elif icon == 'hat':
        D.polygon(s, col, [(1, 12), (9, 3), (17, 12)]); D.line(s, d, (1, 12), (17, 12), 2)
    elif icon == 'claw':
        for i in range(3):
            D.arc(s, col, (2 + i * 4, 2, 8, 14), 0.5, 2.6, 2)
    elif icon == 'staff':
        D.line(s, (150, 110, 60), (9, 4), (9, 17), 2); D.circle(s, col, (9, 4), 4, 1)
        D.circle(s, l, (6, 6), 1); D.circle(s, l, (12, 6), 1)
    else:
        D.circle(s, col, (9, 9), 6)


# ---------------------------------------------------------------- Biome-Kacheln
def _noise(surf, rect, base, amount, count, rng):
    x0, y0, w, h = rect
    for _ in range(count):
        f = 1 + rng.uniform(-amount, amount)
        surf.set_at((x0 + rng.randrange(w), y0 + rng.randrange(h)), _c(base, f))


def make_floor(biome, rng):
    """Erzeugt die Bodenfläche für einen Raum (RW x RH)."""
    s = pygame.Surface((RW, RH))
    base = biome['floor']
    s.fill(base)
    pat = biome['floor_pat']
    D = pygame.draw
    if pat == 'tatami':
        for ty in range(0, RH, 32):
            for tx in range(0, RW, 64):
                off = 32 if (ty // 32) % 2 else 0
                r = pygame.Rect(tx - off, ty, 64, 32)
                D.rect(s, _c(base, 1.05), r)
                for i in range(0, 64, 3):
                    D.line(s, _c(base, 0.93), (r.x + i, r.y + 2), (r.x + i, r.bottom - 3), 1)
                D.rect(s, (60, 70, 40), r, 2)
    elif pat == 'stone':
        for ty in range(0, RH, 32):
            for tx in range(0, RW, 32):
                c = _c(base, rng.uniform(0.9, 1.1))
                D.rect(s, c, (tx + 1, ty + 1, 30, 30))
                D.line(s, _c(base, 1.25), (tx + 1, ty + 1), (tx + 30, ty + 1))
        _noise(s, (0, 0, RW, RH), base, 0.25, 900, rng)
    elif pat == 'wood':
        for ty in range(0, RH, 8):
            c = _c(base, rng.uniform(0.88, 1.08))
            D.rect(s, c, (0, ty, RW, 7))
            for tx in range(rng.randrange(60), RW, 90 + rng.randrange(60)):
                D.line(s, _c(base, 0.7), (tx, ty), (tx, ty + 7))
    else:
        # organisch: gras, sand, schnee, lava, wolken, kies, korallen
        _noise(s, (0, 0, RW, RH), base, 0.18, 2600, rng)
        for _ in range(40):
            x, y = rng.randrange(RW), rng.randrange(RH)
            r = rng.randrange(8, 26)
            pygame.draw.circle(s, _c(base, rng.uniform(0.9, 1.1)), (x, y), r)
        _noise(s, (0, 0, RW, RH), base, 0.22, 1800, rng)
        if pat == 'grass':
            for _ in range(160):
                x, y = rng.randrange(RW), rng.randrange(RH)
                D.line(s, _c(base, 1.35), (x, y), (x + rng.randint(-1, 1), y - 3))
        elif pat == 'lava':
            for _ in range(14):
                x, y = rng.randrange(RW), rng.randrange(RH)
                pts = [(x, y)]
                for i in range(5):
                    x += rng.randint(-14, 14); y += rng.randint(-14, 14)
                    pts.append((x, y))
                D.lines(s, (230, 90, 30), False, pts, 2)
        elif pat == 'cloud':
            for _ in range(30):
                x, y = rng.randrange(RW), rng.randrange(RH)
                D.circle(s, _c(base, 1.08), (x, y), rng.randrange(10, 22))
        elif pat == 'coral':
            for _ in range(18):
                x, y = rng.randrange(RW), rng.randrange(RH)
                D.circle(s, (230, 140, 150), (x, y), 2)
                D.circle(s, _c(base, 1.3), (x + 9, y + 4), 1)
        elif pat == 'snow':
            for _ in range(200):
                s.set_at((rng.randrange(RW), rng.randrange(RH)), (255, 255, 255))
    # leichte Vignette zum Rand
    v = pygame.Surface((RW, RH), pygame.SRCALPHA)
    for i in range(10):
        pygame.draw.rect(v, (0, 0, 0, 10), (i, i, RW - 2 * i, RH - 2 * i), 1)
    s.blit(v, (0, 0))
    return s


def make_walls(biome, rng):
    """Wandrahmen (ganzer Bildschirm, transparent in der Mitte)."""
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    wc = biome['wall']
    D = pygame.draw
    outer = pygame.Rect(RX - 16, RY - 16, RW + 32, RH + 32)
    D.rect(s, _c(wc, 0.5), outer)
    pat = biome['wall_pat']
    # Wand-Band
    for side in range(4):
        if side == 0:
            band = pygame.Rect(outer.x, outer.y, outer.w, 16)
        elif side == 1:
            band = pygame.Rect(outer.x, outer.bottom - 16, outer.w, 16)
        elif side == 2:
            band = pygame.Rect(outer.x, outer.y, 16, outer.h)
        else:
            band = pygame.Rect(outer.right - 16, outer.y, 16, outer.h)
        D.rect(s, wc, band)
        s.set_clip(band)
        horiz = side < 2
        if pat == 'bamboo':
            step = 6
            if horiz:
                for x in range(band.x, band.right, step):
                    D.rect(s, _c(wc, rng.uniform(0.85, 1.15)), (x, band.y, step - 1, 16))
                    D.line(s, _c(wc, 0.6), (x, band.y + 7), (x + step - 2, band.y + 7))
            else:
                for y in range(band.y, band.bottom, step):
                    D.rect(s, _c(wc, rng.uniform(0.85, 1.15)), (band.x, y, 16, step - 1))
                    D.line(s, _c(wc, 0.6), (band.x + 7, y), (band.x + 7, y + step - 2))
        elif pat in ('wood', 'planks', 'torii'):
            if horiz:
                for x in range(band.x, band.right, 24):
                    D.rect(s, _c(wc, 0.7), (x, band.y, 3, 16))
                    if pat == 'wood':
                        D.rect(s, (226, 218, 196), (x + 5, band.y + 3, 16, 10))
                        D.line(s, _c(wc, 0.7), (x + 13, band.y + 3), (x + 13, band.y + 12))
            else:
                for y in range(band.y, band.bottom, 24):
                    D.rect(s, _c(wc, 0.7), (band.x, y, 16, 3))
                    if pat == 'wood':
                        D.rect(s, (226, 218, 196), (band.x + 3, y + 5, 10, 16))
            if pat == 'torii':
                D.rect(s, (30, 20, 20), band, 1)
        else:  # stone, rock, ice, coral, bone, cloud
            for _ in range(band.w * band.h // 40):
                x = rng.randrange(band.x, band.right)
                y = rng.randrange(band.y, band.bottom)
                r = rng.randrange(2, 6)
                c = _c(wc, rng.uniform(0.75, 1.25))
                if pat == 'bone':
                    c = (220, 210, 190) if rng.random() < 0.3 else c
                D.circle(s, c, (x, y), r)
        s.set_clip(None)
    D.rect(s, _c(wc, 0.35), outer, 2)
    inner = pygame.Rect(RX, RY, RW, RH)
    D.rect(s, _c(wc, 0.4), inner.inflate(4, 4), 2)
    s.fill((0, 0, 0, 0), inner)
    # Schatten an der oberen Innenkante
    sh = pygame.Surface((RW, 8), pygame.SRCALPHA)
    for i in range(8):
        pygame.draw.line(sh, (0, 0, 0, 90 - i * 11), (0, i), (RW, i))
    s.blit(sh, (RX, RY))
    return s


def draw_tile(surf, t, x, y, biome, var=0):
    D = pygame.draw
    if t == T_ROCK:
        rc = biome['rock']
        D.ellipse(surf, (0, 0, 0, 60), (x + 2, y + 20, 28, 10))
        pts = [(x + 3, y + 22), (x + 6, y + 8), (x + 14, y + 3), (x + 24, y + 5), (x + 29, y + 14), (x + 28, y + 25), (x + 16, y + 28)]
        D.polygon(surf, rc, pts)
        D.polygon(surf, _c(rc, 1.3), [(x + 7, y + 9), (x + 14, y + 4), (x + 23, y + 6), (x + 15, y + 12)])
        D.polygon(surf, _c(rc, 0.55), pts, 1)
        if biome.get('moss'):
            D.circle(surf, (70, 130, 60), (x + 10, y + 8), 3)
    elif t == T_PIT:
        D.rect(surf, (10, 6, 14), (x, y, 32, 32))
        D.rect(surf, _c(biome['floor'], 0.45), (x, y, 32, 6))
        D.rect(surf, _c(biome['floor'], 0.3), (x, y + 6, 32, 3))
        D.rect(surf, (4, 2, 6), (x + 3, y + 14, 26, 15))
    elif t == T_SPIKE:
        for i in range(3):
            for j in range(3):
                px, py = x + 5 + i * 10, y + 8 + j * 9
                D.polygon(surf, (190, 200, 120), [(px, py - 6), (px + 3, py + 2), (px - 3, py + 2)])
                D.line(surf, (90, 110, 50), (px, py - 6), (px, py + 2))
    elif t == T_POT:
        D.ellipse(surf, (0, 0, 0, 70), (x + 5, y + 23, 22, 7))
        D.ellipse(surf, (150, 90, 60), (x + 6, y + 8, 20, 20))
        D.rect(surf, (120, 70, 50), (x + 11, y + 4, 10, 6))
        D.line(surf, (190, 130, 90), (x + 10, y + 14), (x + 21, y + 14), 2)
        D.ellipse(surf, (60, 34, 24), (x + 12, y + 4, 8, 3))
    elif t == T_LANTERN:
        sc = (150, 150, 150)
        D.rect(surf, _c(sc, 0.7), (x + 9, y + 24, 14, 6))
        D.rect(surf, sc, (x + 13, y + 14, 6, 10))
        D.rect(surf, sc, (x + 9, y + 8, 14, 7))
        D.rect(surf, (255, 210, 120), (x + 12, y + 10, 8, 4))
        D.polygon(surf, _c(sc, 0.8), [(x + 5, y + 8), (x + 16, y + 1), (x + 27, y + 8)])


# ---------------------------------------------------------------- Text
class TextLayer:
    """Texte werden in Spielkoordinaten gesammelt und scharf in Fensterauflösung gezeichnet."""

    def __init__(self):
        self.items = []
        self.fonts = {}

    def add(self, s, x, y, size=10, color=(240, 236, 226), align='l', shadow=True, alpha=255):
        self.items.append((str(s), x, y, size, color, align, shadow, alpha))

    def clear(self):
        self.items.clear()

    def font(self, px):
        f = self.fonts.get(px)
        if f is None:
            f = pygame.font.Font(None, px)
            self.fonts[px] = f
        return f

    def width(self, s, size):
        return self.font(max(6, int(size * 1.45))).size(s)[0] / 1.0 / 1.0

    def flush(self, win, scale, ox, oy):
        for s, x, y, size, color, align, shadow, alpha in self.items:
            f = self.font(max(8, int(size * 1.45 * scale)))
            img = f.render(s, True, color)
            if alpha < 255:
                img.set_alpha(alpha)
            w, h = img.get_size()
            px = ox + x * scale
            py = oy + y * scale - h * 0.15
            if align == 'c':
                px -= w / 2
            elif align == 'r':
                px -= w
            if shadow:
                sh = f.render(s, True, (10, 6, 14))
                if alpha < 255:
                    sh.set_alpha(alpha)
                win.blit(sh, (px + max(1, scale // 2), py + max(1, scale // 2)))
            win.blit(img, (px, py))
        self.items.clear()


TEXT = TextLayer()


def text_w(s, size):
    """Breite in Spielpixeln."""
    f = TEXT.font(max(8, int(size * 1.45 * 4)))
    return f.size(s)[0] / 4


def panel(surf, rect, alpha=210, border=(200, 170, 110)):
    r = pygame.Rect(rect)
    p = pygame.Surface(r.size, pygame.SRCALPHA)
    p.fill((16, 10, 22, alpha))
    surf.blit(p, r.topleft)
    pygame.draw.rect(surf, border, r, 1)
    pygame.draw.rect(surf, _c(border, 0.5), r.inflate(-4, -4), 1)


def heart(surf, x, y, kind, fill):
    """kind: 'red'/'spirit'/'empty'; fill 0,1,2 Hälften."""
    col = {'red': (220, 40, 60), 'spirit': (110, 150, 240), 'empty': (40, 30, 40)}[kind]
    D = pygame.draw
    out = (16, 8, 18)
    D.circle(surf, out, (x + 2, y + 3), 3); D.circle(surf, out, (x + 6, y + 3), 3)
    D.polygon(surf, out, [(x - 1, y + 3), (x + 9, y + 3), (x + 4, y + 9)])
    def shape(c, clip):
        tmp = pygame.Surface((10, 10), pygame.SRCALPHA)
        D.circle(tmp, c, (3, 3), 2); D.circle(tmp, c, (6, 3), 2)
        D.polygon(tmp, c, [(1, 3), (8, 3), (4, 8)])
        if clip:
            tmp.fill((0, 0, 0, 0), (5, 0, 5, 10))
        surf.blit(tmp, (x - 0, y + 0))
    shape((50, 34, 50), False)
    if fill > 0:
        shape(col, fill == 1)
        surf.set_at((x + 2, y + 2), (255, 255, 255))
