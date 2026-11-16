"""Grafik: Pixel-Art-Sprites (ASCII), Item-Icons, Biome-Kacheln, Text-Ebene."""
import math
import random
import pygame
from .settings import *
from . import art

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
    'tesso': [
        "............", "...qq..qq...", "..qqqqqqqq..", ".qeqqqqqqqq.", "qqqqqqqqqqql",
        ".mqqqqqqqq.l", "..q.q..q.q..", "............"],
    'abura_akago': [
        "....f..f....", "...fof.ff...", "..ffooooff..", ".fosssssof..", ".oskssksso..",
        ".osssmmsso..", "..ossssso...", ".fooSSSoof..", "..ossssso...", "...os..so...",
        "...ff..ff...", "............"],
    'nurikabe': [
        "..............", ".llllllllllll.", ".lldlllldllll.", ".llllllllllll.", ".llkkllllkkll.",
        ".llkellllkell.", ".llllllllllll.", "sllllkkkkllls.", "slllllllllllls", ".llldllllldll.",
        ".llllllllllll.", ".llllllllllll.", ".dddd....dddd.", ".............."],
    'mokumokuren': [
        "nnnnnnnnnnnn", "nwwwwnwwwwwn", "nwkewnwwwwwn", "nwwwwnwwkewn", "nnnnnnnnnnnn",
        "nwwwwnwwwwwn", "nwwkenwwwwwn", "nwwwwnwkewwn", "nnnnnnnnnnnn", "nwwwwnwwwwwn",
        "nkewwnwwwwwn", "nnnnnnnnnnnn"],
    'jinmenju': [
        "...GGGGGG...", "..GGgGGgGG..", ".GGgGGGGgGG.", ".GsSGGGGsSG.", ".GkkGGGGkkG.",
        "..GGGsSGGG..", "...GGkkGG...", ".....nn.....", ".....nn.....", "....nnnn....",
        "...nn..nn...", "............"],
    'yosuzume': [
        "..nn....", ".nekn...", "nnnnnnyy", ".NnnnN..", "..N..N..", "........"],
    'enenra': [
        "....ll......", "..llllll....", ".lldllll....", ".llllllll...", "lllkllkll...",
        "llllllllll..", ".llldddlll..", "..llllllllll", "...lllllllll", ".....llllll.",
        ".......ll...", "............"],
    'gyuki': [
        "w............w", "ww..kkkkkk..ww", ".wwkkkkkkkkww.", "..kkekkkkekk..", "..kkkkkkkkkk..",
        "k.kkkwwwwkkk.k", ".kkkkkkkkkkkk.", "k.kkkkkkkkkk.k", ".k.kkkkkkkk.k.", "k..k......k..k",
        "..............", ".............."],
    'kamikiri': [
        "....kk......", "...kkkk.....", "..kekkyy....", "..kkkkyyy...", "...kkkk.....",
        "l..kkkk..l..", ".l.kkkk.l...", "..lkkkkl....", "...kkkk.....", "...k..k.....",
        "..yy..yy....", "............"],
    'kerakera_onna': [
        "...hhhhhh...", "..hhhhhhhh..", "..hssssssh..", "..hskssksh..", "..hsrrrrsh..",
        "..hsrwwrsh..", "...ssssss...", "..ppppMppp..", ".sppppMpppps", "..pppppppp..",
        "..PPPPPPPP..", "..PPPPPPPP..", "..PPP..PPP..", "..kk....kk.."],
    'hyosube': [
        "............", "..nnnnnnnn..", ".nnnnnnnnnn.", ".nnwkwnwkwn.", ".nnnnnnnnnn.",
        ".nnrrrrrrnn.", ".nnrwwwwrnn.", "..nnnnnnnn..", ".nnnnnnnnnn.", "..nn....nn..",
        "..yy....yy..", "............"],
    'tenome': [
        "...ssssss...", "..ssssssss..", "..ssSSSSss..", "..ssssssss..", "...ssmmss...",
        "...ssssss...", ".e.dddddd.e.", "skddddddddks", "s.dddddddd.s", "..dddddddd..",
        "..dddddddd..", "..ddd..ddd..", "..ss....ss..", "............"],
    'nekomata': [
        "............", ".w.....w..ow", ".ww...ww.oo.", ".wwwwwww.w..", ".wewwwew.o..",
        ".wwwmwww.w..", "..owwwwwo...", "..wwwwwwww..", "..woowwwww..", "..wwwwwooo..",
        "..ww.ww.ww..", "..kk.kk.kk.."],
    'kasha': [
        "f..........f", "ff.k....k.ff", ".f.kk..kk.f.", "..fkkkkkkf..", "..kekkkkek..",
        "..kkkrrkkk..", "..fkkkkkkf..", ".fokkkkkkof.", ".ofkkkkkkfo.", "..okk..kko..",
        "..rr....rr..", "............"],
    'tsurube_otoshi': [
        "..hhhhhhhh..", ".hhhhhhhhhh.", "hhssssssssh.", "hsskssskssh.", "hssssssssshh",
        "hsrrrrrrrssh", "hsrwkwwkrssh", "hssrrrrrsshh", ".hssssssshh.", "..hhhhhhhh..",
        "...h.hh.h...", "............"],
    'wanyudo': [
        "...ffffff...", "..fonnnnof..", ".fnnoooonnf.", "fnosssssonnf", "fnoskssksonf",
        "fnosssssonnf", "fnosrrrsonnf", "fnoossssonnf", ".fnnoooonnf.", "..fonnnnof..",
        "...ffffff...", "............"],
    'katawaguruma': [
        "....ffff....", "...fhhhhf...", "..fhsssshf..", "..fhskskhf..", "..fhssmshf..",
        "...fhhhhf...", ".nnnnnnnnnn.", "nnffnnnnffnn", "nfoofnnfoofn", "nnffnnnnffnn",
        ".nnnnnnnnnn.", "............"],
    'azukiarai': [
        "...hhhhh....", "..hhhhhhh...", "..hssssshh..", "..hskskshh..", "...sSSSs....",
        "..nnnnnnn...", ".snnnnnnns..", "..nnnnnnn...", ".NNNNNNNNNN.", ".NrrRrrRrrN.",
        "..NNNNNNNN..", "............"],
    'bake_danuki': [
        "....gg......", "...gGg......", "..n.g....n..", "..nnnnnnnn..", ".nkkwnnwkkn.",
        ".nkewnnwekn.", ".nnnnkknnnn.", "..nnSSSSnn..", ".nnSSSSSSnn.", ".nnSnnnnSnn.",
        "..NN....NN..", "............"],
    'nuppeppo': [
        "............", "...SSSSSS...", "..SssssssS..", ".SsSssssSsS.", ".SsssssssssS",
        "SssskssksssS", "SsssssssssSS", "SsssSSSSsssS", ".SssssssssS.", ".SSsssssSSs.",
        "..SS.SS.SS..", "............"],
    'sazae_oni': [
        ".....n......", "....nnn.....", "...nmnmn....", "..nnnnnnn...", ".nmnnmnnmn..",
        "nnnnnnnnnnn.", ".mmmmmmmmm..", ".mkemmkemm..", ".mmmmmmmmm..", "..m.m.m.m...",
        "............", "............"],
}

_cache = {}


def _legs(base, frame):
    """Einfache Laufanimation: hebt den linken bzw. rechten Fuß an."""
    w, h = base.get_size()
    out = base.copy()
    half = w // 2
    x0, x1 = (0, half) if frame == 1 else (half, w)
    rows = max(2, h // 12)
    for y in range(h - rows, h):
        for x in range(x0, x1):
            out.set_at((x, y - 1), base.get_at((x, y)))
            out.set_at((x, y), (0, 0, 0, 0))
    return out


def sprite(name, flip=False, flash=False, tint=None, scale=1, frame=0):
    key = (name, flip, flash, tint, scale, frame)
    s = _cache.get(key)
    if s is not None:
        return s
    if frame:
        b = sprite(name, False, False, None, 1, 0)
        fk = (name, False, False, None, 1, frame)
        if fk not in _cache:
            _cache[fk] = _legs(b, frame)
        s = _cache[fk]
        if tint or flash or flip or scale != 1:
            s = _post(s, flip, flash, tint, scale)
        _cache[key] = s
        return s
    if (name, False, False, None, 1, 0) not in _cache and name in art.ARTS:
        _cache[(name, False, False, None, 1, 0)] = art.make(name)
    if (name, False, False, None, 1, 0) not in _cache:
        rows = SPRITES[name]
        w, h = len(rows[0]), len(rows)
        base = pygame.Surface((w, h), pygame.SRCALPHA)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != '.':
                    base.set_at((x, y), PAL[ch])
        _cache[(name, False, False, None, 1, 0)] = base
    s = _cache[(name, False, False, None, 1, 0)]
    s = _post(s, flip, flash, tint, scale)
    _cache[key] = s
    return s


def _post(s, flip, flash, tint, scale):
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


_aglow = {}


def draw_glow(surf, x, y, radius, color, alpha=90):
    if surf.get_flags() & pygame.SRCALPHA:
        key = (int(radius), color, alpha)
        g = _aglow.get(key)
        if g is None:
            r = max(1, int(radius))
            g = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            for i in range(r, 0, -1):
                a = int(min(190, alpha * 1.4) * (1 - i / r) ** 1.6)
                pygame.draw.circle(g, color + (a,), (r, r), i)
            _aglow[key] = g
        surf.blit(g, (x - radius, y - radius))
        return
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


_ITEMS = _os_items = None
_item_cache = {}
HI_MODE = False


def item_img(group, name, frame=0):
    """Handgesetzte 32x32-Bilder aus assets/items/<group>/<name>.png (Streifen = Animationsbilder)."""
    key = (group, name)
    fr = _item_cache.get(key, 0)
    if fr == 0:
        import os, sys
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'items')
        if not os.path.isdir(base) and hasattr(sys, '_MEIPASS'):
            base = os.path.join(sys._MEIPASS, 'yokai', 'assets', 'items')
        p = os.path.join(base, group, name + '.png')
        fr = None
        if os.path.exists(p):
            im = pygame.image.load(p)
            try:
                im = im.convert_alpha()
            except pygame.error:
                pass
            h = im.get_height()
            fr = [im.subsurface((i * h, 0, h, h)).copy() for i in range(max(1, im.get_width() // h))]
        _item_cache[key] = fr
    if not fr:
        return None
    return fr[frame % len(fr)]


def draw_icon(surf, icon, col, x, y):
    """Zeichnet ein 16x16 Item-Icon an (x,y)=Mitte."""
    hi = item_img('icons', icon)
    if hi is not None:
        if HI_MODE:
            hi_blit(hi, x, y + 8)
        else:
            key = ('icon1x', icon)
            s1 = _cache.get(key)
            if s1 is None:
                s1 = pygame.transform.smoothscale(hi, (16, 16))
                _cache[key] = s1
            surf.blit(s1, (int(x) - 8, int(y) - 8))
        return
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



# =========================================================================  Umgebungs-Tilesets (handgesetzt)
import os as _os
import sys as _sys
_ENV = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'assets', 'env')
if not _os.path.isdir(_ENV) and hasattr(_sys, '_MEIPASS'):
    _ENV = _os.path.join(_sys._MEIPASS, 'yokai', 'assets', 'env')
_env_cache = {}


def env_img(folder, name, fw=None):
    """Lädt assets/env/<folder>/<name>.png und teilt es in Bilder der Breite fw."""
    key = (folder, name, fw)
    if key in _env_cache:
        return _env_cache[key]
    p = _os.path.join(_ENV, folder, name + '.png')
    res = None
    if _os.path.exists(p):
        im = pygame.image.load(p)
        try:
            im = im.convert_alpha()
        except pygame.error:
            pass
        if fw:
            res = [im.subsurface((i * fw, 0, fw, im.get_height())).copy() for i in range(max(1, im.get_width() // fw))]
        else:
            res = [im]
    _env_cache[key] = res
    return res


def env_ok(biome):
    return env_img(biome.get('_id', ''), 'floor', 32) is not None


def env_floor(biome, rng):
    s = pygame.Surface((RW, RH))
    tiles = env_img(biome['_id'], 'floor', 32)
    plain, deco = tiles[:4], tiles[4:] or tiles[:4]
    for ty in range(0, RH, 32):
        for tx in range(0, RW, 32):
            t = rng.choice(deco) if rng.random() < 0.08 else rng.choice(plain)
            s.blit(t, (tx, ty))
    return s


def env_walls(biome, rng):
    bid = biome['_id']
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    top = env_img(bid, 'wall_h')[0]
    bot = (env_img(bid, 'wall_h_bottom') or [top])[0]
    side = env_img(bid, 'wall_v')[0]
    corner = env_img(bid, 'wall_corner')[0]
    deco = env_img(bid, 'wall_deco', 32) or []
    x0, y0 = RX - 16, RY - 16
    for tx in range(RX, RX + RW, 32):
        t = top
        if deco and rng.random() < 0.18:
            t = rng.choice(deco)
        s.blit(t, (tx, y0))
        s.blit(bot, (tx, RY + RH))
    rside = pygame.transform.flip(side, True, False)
    for ty in range(RY, RY + RH, 32):
        s.blit(side, (x0, ty))
        s.blit(rside, (RX + RW, ty))
    s.blit(corner, (x0, y0))
    s.blit(pygame.transform.flip(corner, True, False), (RX + RW, y0))
    s.blit(pygame.transform.flip(corner, False, True), (x0, RY + RH))
    s.blit(pygame.transform.flip(corner, True, True), (RX + RW, RY + RH))
    return s


def scale2x(surf):
    """Scale2x/EPX: verdoppelt Pixelgrafik und glättet Treppenkanten, ohne neue Farben."""
    import numpy as _np
    a = pygame.surfarray.pixels3d(surf).copy().transpose(1, 0, 2)
    al = pygame.surfarray.pixels_alpha(surf).copy().T
    a = _np.dstack([a, al])
    h, w = a.shape[:2]
    p = _np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    B, D, E_, F, H_ = p[0:h, 1:w + 1], p[1:h + 1, 0:w], p[1:h + 1, 1:w + 1], p[1:h + 1, 2:w + 2], p[2:h + 2, 1:w + 1]
    eq = lambda x, y: _np.all(x == y, axis=2)
    c = (~eq(B, H_)) & (~eq(D, F))
    E0 = _np.where((c & eq(D, B))[..., None], D, E_)
    E1 = _np.where((c & eq(B, F))[..., None], F, E_)
    E2 = _np.where((c & eq(D, H_))[..., None], D, E_)
    E3 = _np.where((c & eq(H_, F))[..., None], F, E_)
    out = _np.zeros((h * 2, w * 2, 4), _np.uint8)
    out[0::2, 0::2] = E0; out[0::2, 1::2] = E1; out[1::2, 0::2] = E2; out[1::2, 1::2] = E3
    res = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
    pygame.surfarray.pixels3d(res)[:] = out[:, :, :3].transpose(1, 0, 2)
    pygame.surfarray.pixels_alpha(res)[:] = out[:, :, 3].T
    return res


def hi_tile(t, x, y, biome):
    """Hi-Res-Bild für stehende Requisiten (Fels, Urne, Laterne) oder None."""
    bid = biome.get('_id', '')
    if t == T_ROCK:
        r = env_img(bid, 'rock_hi', 64)
        return r[(x * 7 + y * 13) // 32 % len(r)] if r else None
    if t == T_POT:
        r = env_img('_shared', 'pot_hi', 64)
        return r[0] if r else None
    if t == T_LANTERN:
        r = env_img('_shared', 'lantern_hi', 64)
        return r[0] if r else None
    return None


_foot_cache = {}


def rock_foot(x, y, biome):
    """(x-Mitte, halbe Breite) der Fels-Variante an (x, y), aus dem Alpha ihres Rumpfs (ohne Bodenschatten)."""
    img = hi_tile(T_ROCK, x, y, biome)
    if img is None:
        return None
    key = id(img)
    if key not in _foot_cache:
        xs = [px for py in range(32, 52, 2) for px in range(64) if img.get_at((px, py)).a > 128]
        x0, x1 = (min(xs), max(xs)) if xs else (10, 54)
        fx = (x0 + x1) / 4
        _foot_cache[key] = (fx, min(12, fx, 32 - fx, max(5, (x1 - x0) / 4)))  # bleibt in der Kachel
    return _foot_cache[key]


def env_tile(surf, t, x, y, biome):
    """Gibt True zurück, wenn ein handgesetztes Tile gezeichnet wurde."""
    bid = biome.get('_id', '')
    if hi_tile(t, x, y, biome) is not None:
        return True                     # wird stehend auf der Hi-Res-Ebene gezeichnet
    if t == T_ROCK:
        r = env_img(bid, 'rock', 32)
        if r:
            surf.blit(r[(x * 7 + y * 13) // 32 % len(r)], (x, y))
            return True
    elif t == T_POT:
        r = env_img('_shared', 'pot', 32)
        if r:
            surf.blit(r[0], (x, y)); return True
    elif t == T_LANTERN:
        r = env_img('_shared', 'lantern', 32)
        if r:
            surf.blit(r[0], (x, y)); return True
    elif t == T_SPIKE:
        r = env_img('_shared', 'spikes', 32)
        if r:
            surf.blit(r[-1], (x, y)); return True
    elif t == T_PIT:
        r = env_img('_shared', 'pit_' + biome.get('pit', 'void'), 32)
        if r:
            surf.blit(r[0], (x, y)); return True
    return False


def make_floor(biome, rng):
    """Erzeugt die Bodenfläche für einen Raum (RW x RH)."""
    if env_ok(biome):
        return env_floor(biome, rng)
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
    _decor(s, biome.get('decor'), base, rng)
    # leichte Vignette zum Rand
    v = pygame.Surface((RW, RH), pygame.SRCALPHA)
    for i in range(10):
        pygame.draw.rect(v, (0, 0, 0, 10), (i, i, RW - 2 * i, RH - 2 * i), 1)
    s.blit(v, (0, 0))
    return s


def _decor(s, kind, base, rng):
    D = pygame.draw
    n = rng.randint(10, 22)
    for _ in range(n):
        x, y = rng.randrange(8, RW - 8), rng.randrange(8, RH - 8)
        if kind in ('grass', 'reeds'):
            c = (90, 150, 70) if kind == 'grass' else (120, 150, 80)
            for i in range(rng.randint(3, 6)):
                dx = rng.randint(-4, 4)
                D.line(s, _c(c, rng.uniform(0.8, 1.3)), (x + dx, y), (x + dx + rng.randint(-2, 2), y - rng.randint(3, 8 if kind == 'reeds' else 5)))
            if kind == 'reeds' and rng.random() < 0.3:
                D.ellipse(s, (120, 80, 50), (x - 1, y - 11, 3, 5))
        elif kind == 'petals':
            for i in range(rng.randint(2, 5)):
                D.ellipse(s, (250, 180, 205), (x + rng.randint(-8, 8), y + rng.randint(-6, 6), 3, 2))
        elif kind == 'leaves':
            col = rng.choice([(190, 90, 40), (210, 140, 50), (160, 60, 40)])
            D.ellipse(s, col, (x, y, 5, 3))
            D.line(s, _c(col, 0.6), (x, y + 1), (x + 4, y + 1))
        elif kind == 'cracks':
            pts = [(x, y)]
            for i in range(4):
                pts.append((pts[-1][0] + rng.randint(-7, 7), pts[-1][1] + rng.randint(-7, 7)))
            D.lines(s, _c(base, 0.55), False, pts, 1)
        elif kind == 'graves' and rng.random() < 0.35:
            D.rect(s, (120, 120, 130), (x, y - 8, 7, 10))
            D.rect(s, (90, 90, 100), (x, y - 8, 7, 10), 1)
            D.line(s, (60, 60, 70), (x + 2, y - 5), (x + 4, y - 5))
        elif kind == 'bones':
            c = (220, 212, 190)
            D.line(s, c, (x, y), (x + 7, y + rng.randint(-3, 3)), 2)
            D.circle(s, c, (x, y), 2); D.circle(s, c, (x + 7, y), 2)
            if rng.random() < 0.15:
                D.circle(s, c, (x + 14, y - 3), 4); D.circle(s, (40, 20, 20), (x + 13, y - 4), 1)
        elif kind == 'shells':
            col = rng.choice([(240, 200, 210), (230, 230, 210), (200, 120, 130)])
            D.polygon(s, col, [(x, y), (x + 4, y - 4), (x + 8, y)])
            if rng.random() < 0.4:
                for i in range(3):
                    D.line(s, (40, 120, 70), (x + 12 + i * 2, y + 4), (x + 12 + i * 2 + rng.randint(-2, 2), y - 6), 1)
        elif kind == 'planks' and rng.random() < 0.4:
            D.rect(s, (90, 64, 44), (x, y, rng.randint(12, 24), 4))
        elif kind == 'snow':
            D.ellipse(s, (240, 245, 255), (x, y, rng.randint(6, 14), 4))
        elif kind == 'clouds':
            D.circle(s, (250, 240, 210), (x, y), rng.randint(3, 6))


def make_walls(biome, rng):
    """Wandrahmen (ganzer Bildschirm, transparent in der Mitte)."""
    if env_ok(biome):
        return env_walls(biome, rng)
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
    for cx, cy in ((outer.x, outer.y), (outer.right - 20, outer.y), (outer.x, outer.bottom - 20), (outer.right - 20, outer.bottom - 20)):
        D.rect(s, _c(wc, 0.45), (cx, cy, 20, 20))
        D.rect(s, _c(wc, 1.2), (cx + 3, cy + 3, 14, 14))
        D.rect(s, _c(wc, 0.7), (cx + 6, cy + 6, 8, 8))
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
    if env_tile(surf, t, x, y, biome):
        return
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
        kind = biome.get('pit', 'void')
        if kind == 'water':
            D.rect(surf, (30, 70, 120), (x, y, 32, 32))
            D.rect(surf, (20, 50, 90), (x, y + 18, 32, 14))
            D.rect(surf, _c(biome['floor'], 0.6), (x, y, 32, 4))
            for i in range(3):
                yy = y + 8 + i * 8
                D.line(surf, (120, 180, 230), (x + 4 + (i * 7) % 12, yy), (x + 12 + (i * 7) % 12, yy), 1)
        elif kind == 'lava':
            D.rect(surf, (150, 40, 10), (x, y, 32, 32))
            D.rect(surf, (230, 110, 30), (x + 2, y + 6, 28, 22))
            D.rect(surf, (60, 20, 10), (x, y, 32, 5))
            for i in range(3):
                D.circle(surf, (255, 200, 80), (x + 7 + i * 9, y + 12 + (i % 2) * 8), 2)
        elif kind == 'ice':
            D.rect(surf, (150, 200, 235), (x, y, 32, 32))
            D.rect(surf, (110, 160, 210), (x, y, 32, 32), 1)
            D.line(surf, (240, 250, 255), (x + 5, y + 6), (x + 14, y + 15), 1)
            D.line(surf, (240, 250, 255), (x + 18, y + 20), (x + 26, y + 26), 1)
            D.rect(surf, (20, 40, 70), (x + 6, y + 10, 20, 16))
        elif kind == 'cloud':
            D.rect(surf, (120, 160, 220), (x, y, 32, 32))
            D.circle(surf, (240, 245, 255), (x + 6, y + 26), 7)
            D.circle(surf, (240, 245, 255), (x + 22, y + 8), 5)
        else:
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


_grade = {}


def color_grade(surf, col, strength=26):
    """Leichte Farbstimmung + Vignette über den ganzen Bildschirm."""
    key = (col, strength)
    g = _grade.get(key)
    if g is None:
        g = pygame.Surface((W, H), pygame.SRCALPHA)
        g.fill(col + (strength,))
        for i in range(40):
            a = int((1 - i / 40) ** 2 * 110)
            pygame.draw.rect(g, (0, 0, 0, a), (i * 2, i * 2, W - i * 4, H - i * 4), 2)
        _grade[key] = g
    surf.blit(g, (0, 0))


_edge = {}


def color_grade_edge(surf, col, alpha):
    """Farbiger Bildschirmrand (Treffer / wenig Leben)."""
    e = _edge.get(col)
    if e is None:
        e = pygame.Surface((W, H), pygame.SRCALPHA)
        for i in range(30):
            a = int((1 - i / 30) ** 2 * 255)
            pygame.draw.rect(e, col + (a,), (i * 2, i * 2, W - i * 4, H - i * 4), 2)
        _edge[col] = e
    e.set_alpha(alpha)
    surf.blit(e, (0, 0))


# ---------------------------------------------------------------- Text
FONT_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'assets', 'fonts', 'YokaiFude.ttf')
if not _os.path.exists(FONT_PATH) and hasattr(_sys, '_MEIPASS'):
    FONT_PATH = _os.path.join(_sys._MEIPASS, 'yokai', 'assets', 'fonts', 'YokaiFude.ttf')
if not _os.path.exists(FONT_PATH):
    FONT_PATH = None


PAD_MODE = False          # zuletzt mit Controller gespielt → Tastenhinweise als Controller-Knöpfe
_PAD_SUB = (('Enter – ', 'A – '), ('Enter: ', 'A: '), ('Esc – ', 'B – '), ('Esc: ', 'B: '),
            ('/ Esc –', '/ B –'), ('Beliebige Taste', 'Beliebiger Knopf'), ('R – Nochmal', 'Y – Nochmal'))


def pad_labels(s):
    for a, b in _PAD_SUB:
        s = s.replace(a, b)
    return s


class TextLayer:
    """Texte werden in Spielkoordinaten gesammelt und scharf in Fensterauflösung gezeichnet."""

    def __init__(self):
        self.items = []
        self.fonts = {}

    def add(self, s, x, y, size=10, color=(240, 236, 226), align='l', shadow=True, alpha=255):
        s = str(s)
        if PAD_MODE and ('Enter' in s or 'Esc' in s or 'Beliebige Taste' in s or 'R – ' in s):
            s = pad_labels(s)
        self.items.append((s, x, y, size, color, align, shadow, alpha))

    def clear(self):
        self.items.clear()

    def font(self, px):
        f = self.fonts.get(px)
        if f is None:
            if FONT_PATH:
                f = pygame.font.Font(FONT_PATH, max(6, int(round(px * 0.66))))
                if px * 0.66 <= 19:                 # kleine Schrift kräftiger, damit der Pinselstrich lesbar bleibt
                    f.bold = True
            else:
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
            py = oy + y * scale - h * (0.21 if FONT_PATH else 0.15)
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
    w = f.size(s)[0] / 4
    if FONT_PATH and size <= 7.5:          # kleine Schrift wird fett gezeichnet und läuft etwas breiter
        w = w * 1.12 + 2
    return w


def panel(surf, rect, alpha=210, border=(200, 170, 110)):
    r = pygame.Rect(rect)
    p = pygame.Surface(r.size, pygame.SRCALPHA)
    p.fill((16, 10, 22, alpha))
    surf.blit(p, r.topleft)
    pygame.draw.rect(surf, border, r, 1)
    pygame.draw.rect(surf, _c(border, 0.5), r.inflate(-4, -4), 1)


_panel_cache = {}


def hi_panel(rect, alpha=210, border=(200, 170, 110)):
    """Wie panel(), aber auf der Hi-Res-Ebene – liegt damit über Figuren und Requisiten."""
    r = pygame.Rect(rect)
    key = (r.w, r.h, alpha, tuple(border))
    img = _panel_cache.get(key)
    if img is None:
        tmp = pygame.Surface(r.size, pygame.SRCALPHA)
        panel(tmp, (0, 0, r.w, r.h), alpha, border)
        img = pygame.transform.scale(tmp, (r.w * 2, r.h * 2))
        if len(_panel_cache) > 60:
            _panel_cache.clear()
        _panel_cache[key] = img
    HI.append((img, r.x + r.w / 2, r.bottom, 255, 1.0, True))


_hud_crop = {}


def hud_icon(name, cx, cy):
    """HUD-Symbol aus assets/items/hud als Hi-Res-Bild (Mittelpunkt cx, cy). False wenn nicht verfügbar."""
    if not HI_MODE:
        return False
    im = _hud_crop.get(name)
    if im is None:
        src = item_img('hud', name)
        if src is None:
            return False
        im = src.subsurface(src.get_bounding_rect()).copy()
        _hud_crop[name] = im
    hi_blit(im, cx, cy + im.get_height() / 4)
    return True


def heart(surf, x, y, kind, fill):
    """kind: 'red'/'spirit'/'empty'; fill 0,1,2 Hälften."""
    nm = 'heart_soul' if kind == 'spirit' else ('heart_full' if fill == 2 else 'heart_half' if fill == 1 else 'heart_empty')
    if kind == 'spirit' and fill == 1:
        nm = 'heart_soul'
    if hud_icon(nm, x + 4, y + 4):
        return
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


# =========================================================================  Hi-Res-Sprite-Ebene
# Figuren-Sprites sind mit doppelter Pixeldichte gezeichnet. Sie werden nicht in die 480x320-Welt
# geblittet, sondern gesammelt und beim Darstellen in Fensterauflösung (halbe Größe) gezeichnet.
HI = []
_hi_cache = {}


NOCACHE = set()


def hi_blit(surf, cx, by, alpha=255, transient=False):
    """surf: Hi-Res-Bild; (cx, by): Mittelpunkt unten in Weltkoordinaten.
    transient=True für Bilder, die jedes Bild neu erzeugt werden (nicht cachen)."""
    if transient:
        NOCACHE.add(id(surf))
    HI.append((surf, cx, by, alpha))


_tint_cache = {}
_mult_cache = {}


def tinted_mult(surf, col):
    """Bild mit Farbe multipliziert (Stimmung des Titelhimmels), gecacht."""
    key = (id(surf), col)
    im = _mult_cache.get(key)
    if im is None:
        im = _mult_cache[key] = surf.copy()
        im.fill(col + (255,), special_flags=pygame.BLEND_RGBA_MULT)
    return im



def tinted(surf, mode):
    key = (id(surf), mode)
    tr = id(surf) in NOCACHE
    im = None if tr else _tint_cache.get(key)
    if im is None:
        im = surf.copy()
        if mode == 'flash':
            im.fill((120, 110, 110, 0), special_flags=pygame.BLEND_RGB_ADD)
        elif mode == 'white':
            im.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGB_MAX)
        elif mode == 'shadow':
            im.fill((14, 10, 22, 0), special_flags=pygame.BLEND_RGB_MULT)
        elif mode == 'ghost':
            im.fill((120, 100, 170, 0), special_flags=pygame.BLEND_RGB_MULT)
            im.fill((20, 10, 40, 0), special_flags=pygame.BLEND_RGB_ADD)
        else:
            im.fill((150, 210, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
        if tr:
            NOCACHE.add(id(im))
            return im
        if len(_tint_cache) > 600:
            _tint_cache.clear()
        _tint_cache[key] = im
    return im


def bake_low(surf):
    """Ebenen in einfacher Pixeldichte (Geschosse, HUD) zurück auf die Grundfläche legen – für Menüs über dem Spiel."""
    keep = []
    for e in HI:
        if len(e) > 6 and e[6] == 'low':
            surf.blit(e[0], (0, 0))
        else:
            keep.append(e)
    HI[:] = keep


def dim_hi(f):
    """Alle bisher gesammelten Hi-Res-Bilder abdunkeln (z. B. unter einem Menü-Schleier)."""
    HI[:] = [(e[0], e[1], e[2], e[3], (e[4] if len(e) > 4 else 1.0) * f, True) + tuple(e[6:]) for e in HI]


def hi_flush(win, sc, ox, oy, dim=1.0, light=None):
    for ent in HI:
        surf, cx, by, alpha = ent[:4]
        w, h = surf.get_size()
        k = sc if len(ent) > 6 and ent[6] == 'low' else sc / 2      # 'low': Ebene in einfacher Pixeldichte (Geschosse, Partikel)
        tw, th = max(1, int(w * k)), max(1, int(h * k))
        f = dim * (ent[4] if len(ent) > 4 else 1.0)
        if light is not None and not (len(ent) > 5 and ent[5]):
            f *= light(cx, by)
        fq = round(f * 8) / 8
        key = (id(surf), tw, th, fq)
        tr = id(surf) in NOCACHE
        img = None if tr else _hi_cache.get(key)
        if img is None:
            img = pygame.transform.scale(surf, (tw, th))
            if fq < 1:
                v = int(255 * fq)
                img.fill((v, v, v), special_flags=pygame.BLEND_RGB_MULT)
            if not tr:
                if len(_hi_cache) > 4000:
                    _hi_cache.clear()
                _hi_cache[key] = img
        if alpha < 255:
            img = img.copy()
            img.set_alpha(alpha)
        win.blit(img, (int(ox + cx * sc - tw / 2), int(oy + by * sc - th)))
    HI.clear()
    NOCACHE.clear()


_mini_cache = {}


def mini(surf, h):
    """Verkleinertes Porträt eines Sprites (Ausschnitt auf Inhalt, Pixel-Look erhalten)."""
    key = (id(surf), h)
    im = _mini_cache.get(key)
    if im is None:
        bb = surf.get_bounding_rect()
        src = surf.subsurface(bb)
        f = h / max(1, bb.h)
        w2 = max(1, int(bb.w * f))
        im = pygame.transform.smoothscale(src, (w2, h)) if f < 0.75 else pygame.transform.scale(src, (w2, h))
        _mini_cache[key] = im
    return im
