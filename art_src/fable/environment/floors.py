"""Floor patterns. Seam rule: nothing is ever cut by a tile edge.
Scatter patterns keep every motif fully inside the tile; structural patterns (tatami, slabs, planks, lava
cracks) put identical joints / crossing points on the tile border in every variant."""
import math
import random
import numpy as np
from core import *
from biomes import *

T = 32


def spr_size(text):
    rows = text.strip('\n').split('\n')
    return max(len(r) for r in rows), len(rows)


def place(occ, rng, w, h, pad=1, lo=0, hi=T, tries=80):
    for _ in range(tries):
        x = rng.randint(lo, hi - w)
        y = rng.randint(lo, hi - h)
        if not occ[max(0, y - pad):min(T, y + h + pad), max(0, x - pad):min(T, x + w + pad)].any():
            occ[y:y + h, x:x + w] = True
            return x, y
    return None


def put(cv, occ, rng, text, legend, pad=1, flip=None):
    w, h = spr_size(text)
    p = place(occ, rng, w, h, pad)
    if p:
        cv.grid(p[0], p[1], text, legend, flip=rng.random() < 0.5 if flip is None else flip)
    return p


def blob(cv, rng, cx, cy, r, c, lo=1, hi=T - 2):
    """soft irregular patch: union of a few ellipses, clipped inside the tile"""
    m = np.zeros((T, T), bool)
    for _ in range(3):
        m |= cv.E(cx + rng.uniform(-r, r) * .5, cy + rng.uniform(-r, r) * .3, r * rng.uniform(.6, 1) + .3,
                  r * rng.uniform(.45, .7) + .3)
    m &= cv.R(lo, lo, hi, hi)
    cv.fill(m, c)
    return m


def new(P, keep=None):
    cv = Cv(T, T, bg=P['f1'])
    occ = np.zeros((T, T), bool)
    if keep:
        x0, y0, x1, y1 = keep
        occ[y0:y1 + 1, x0:x1 + 1] = True
    return cv, occ


def leg(P, **kw):
    d = dict(d=P['f0'], m=P['f2'], l=P['f2'], h=P['f3'], b=P['fb'])
    d.update(kw)
    return d


# ------------------------------------------------------------------ scatter patterns
TUFTS = ["l.l\nlll", ".l..\nll.l\n.lll", "h..\nl.l\nlll", "l.l.\nlll.\n.lll", "ll.\n.ll"]
DTUFTS = ["b.b\nbbb", "bb.\n.bb", "b.b.\nbbbb"]


def grass(P, rng, keep=None):
    cv, occ = new(P, keep)
    for _ in range(3):
        blob(cv, rng, rng.randint(6, 25), rng.randint(6, 25), rng.uniform(3, 5.5), P['fb'])
    L = leg(P)
    for _ in range(4):
        put(cv, occ, rng, rng.choice(DTUFTS), L, pad=2)
    for _ in range(7):
        put(cv, occ, rng, rng.choice(TUFTS), L, pad=2)
    return cv, occ


PEBBLES = [".hm.\nmmmd\n.dd.", "mmd\n.dd", "mm\ndd", ".hmm.\nmmmmd\n.ddd.", "hm.\nmmd\n.dd"]
PITS = ["bb", "bb.\n.bb", "b\nb"]


def gravel(P, rng, keep=None, n=8):
    cv, occ = new(P, keep)
    for _ in range(2):
        blob(cv, rng, rng.randint(6, 25), rng.randint(6, 25), rng.uniform(3, 5), P['fb'])
    L = leg(P)
    for _ in range(n):
        put(cv, occ, rng, rng.choice(PEBBLES), L, pad=2)
    for _ in range(5):
        put(cv, occ, rng, rng.choice(PITS), L, pad=2)
    return cv, occ


DRIFTS = [".lllll..\nlllllll.\n..bbbbb.", ".lll.\nlllll\n.bbbb", "hhlll...\nllllllll\n.lllll..\n...bbbbb", "lll\n.bb"]


def snow(P, rng, keep=None):
    cv, occ = new(P, keep)
    for _ in range(2):
        blob(cv, rng, rng.randint(7, 24), rng.randint(7, 24), rng.uniform(4, 6), P['fb'])
    L = leg(P)
    for _ in range(5):
        put(cv, occ, rng, rng.choice(DRIFTS), L, pad=2, flip=False)
    for _ in range(3):
        put(cv, occ, rng, rng.choice(PITS), L, pad=2)
    return cv, occ


def ripple(cv, occ, rng, P, n):
    for _ in range(n):
        ln = rng.randint(7, 12)
        p = place(occ, rng, ln, 3, pad=1)
        if not p:
            continue
        ph = rng.uniform(0, 6.28)
        for i in range(ln):
            y = p[1] + 1 + int(round(math.sin(ph + i * 0.8) * 0.8))
            cv.px(p[0] + i, y, P['f2'])
            if 1 <= i < ln - 1:
                cv.px(p[0] + i, y + 1, P['fb'])


def sand(P, rng, keep=None, crumbs=0):
    cv, occ = new(P, keep)
    for _ in range(2):
        blob(cv, rng, rng.randint(6, 25), rng.randint(6, 25), rng.uniform(3.5, 5.5), P['fb'])
    ripple(cv, occ, rng, P, 5)
    L = leg(P)
    for _ in range(2):
        put(cv, occ, rng, rng.choice(PEBBLES[1:3]), L, pad=2)
    if crumbs:
        s = P['shell']
        Ls = dict(a=s[0], s=s[1])
        for _ in range(crumbs):
            put(cv, occ, rng, rng.choice(["aa", "aa\n.a"]), Ls, pad=2)
    return cv, occ


def coral(P, rng, keep=None):
    return sand(P, rng, keep, crumbs=1)


def cloud(P, rng, keep=None):
    """flat-bottomed cumulus lumps: lit scalloped top, soft shadow line underneath"""
    cv, occ = new(P, keep)
    for _ in range(2):
        blob(cv, rng, rng.randint(7, 24), rng.randint(7, 24), rng.uniform(4, 6), P['fb'])
    for k in range(5):
        w = rng.choice([9, 12, 12, 15, 18])
        p = place(occ, rng, w, 7, pad=1)
        if not p:
            continue
        x, y = p
        n = max(2, w // 4)
        m = np.zeros((T, T), bool)
        for i in range(n):
            r = rng.uniform(2.3, 3.5)
            m |= cv.E(x + 3 + i * (w - 7) / (n - 1), y + 3.6 + rng.uniform(-.7, .7), r, r)
        m &= cv.R(x, y, x + w - 1, y + 5)
        cv.fill(m, mix(P['f1'], P['f2'], .5))
        cv.fill(m & ~sh(m, 0, 1), P['f2'])
        cv.fill(sh(m & ~sh(m, 0, -1), 1, 1) & ~m & cv.R(0, 0, 31, 31), P['fb'])
    return cv, occ


# ------------------------------------------------------------------ structural patterns
def tatami(P, rng, keep=None, vert=False):
    cv = Cv(T, T, bg=P['f1'])
    occ = np.zeros((T, T), bool)
    hc = mix(P['f0'], P['f1'], .45)
    # weave: every 3rd line lighter, broken by short gaps
    for y in range(4, 28, 3):
        x = 2
        while x < 30:
            ln = rng.randint(5, 11)
            cv.hl(x, min(29, x + ln - 1), y, P['f2'])
            x += ln + rng.randint(1, 3)
    for _ in range(3):   # darker reed streaks
        y = rng.choice([5, 8, 11, 14, 17, 20, 23, 26])
        x = rng.randint(2, 20)
        cv.hl(x, x + rng.randint(4, 8), y, P['fb'])
    # heri cloth borders along the weave, 1 px seam around
    cv.rect(0, 0, 31, 1, hc)
    cv.rect(0, 28, 31, 30, hc)
    cv.hl(0, 31, 2, P['f0'])
    cv.hl(0, 31, 27, P['f0'])
    cv.hl(0, 31, 31, P['f0'])
    cv.vl(31, 0, 31, P['f0'])
    if vert:
        cv.a = np.ascontiguousarray(np.transpose(cv.a, (1, 0, 2)))
    if keep:
        occ[keep[1]:keep[3] + 1, keep[0]:keep[2] + 1] = True
    return cv, occ


SLABS = [
    [(0, 0, 31, 31)],
    [(0, 0, 31, 15), (0, 16, 31, 31)],
    [(0, 0, 15, 31), (16, 0, 31, 31)],
    [(0, 0, 19, 19), (20, 0, 31, 19), (0, 20, 11, 31), (12, 20, 31, 31)],
    [(0, 0, 31, 11), (0, 12, 15, 31), (16, 12, 31, 31)],
    [(0, 0, 11, 31), (12, 0, 31, 17), (12, 18, 31, 31)],
]


def stone(P, rng, keep=None, layout=0):
    cv = Cv(T, T, bg=P['f1'])
    occ = np.zeros((T, T), bool)
    slabs = SLABS[layout]
    for i, (x0, y0, x1, y1) in enumerate(slabs):
        base = P['f1'] if (len(slabs) == 1 or rng.random() < .6) else mix(P['f1'], P['f0'], .3)
        cv.rect(x0, y0, x1, y1, base)
        cv.hl(x0, x1 - 1, y0, P['f2'])
        cv.vl(x0, y0, y1 - 1, P['f2'])
        cv.hl(x0, x1, y1, P['f0'])
        cv.vl(x1, y0, y1, P['f0'])
        # worn corner chip + a faint surface scuff
        if rng.random() < .7:
            cx, cy = rng.choice([(x1 - 2, y1 - 2), (x0 + 1, y1 - 2), (x1 - 2, y0 + 1)])
            cv.rect(cx, cy, cx + 1, cy + 1, P['f0'])
        if x1 - x0 > 9 and y1 - y0 > 6:
            sx, sy = rng.randint(x0 + 3, x1 - 8), rng.randint(y0 + 3, y1 - 4)
            cv.hl(sx, sx + rng.randint(2, 4), sy, P['fb'])
            cv.hl(sx + 1, sx + rng.randint(3, 5), sy + 1, P['fb'])
    if keep:
        occ[keep[1]:keep[3] + 1, keep[0]:keep[2] + 1] = True
    return cv, occ


def wood(P, rng, keep=None):
    cv = Cv(T, T, bg=P['f1'])
    occ = np.zeros((T, T), bool)
    for i in range(4):
        y0 = i * 8
        if rng.random() < .35:
            cv.rect(0, y0, 31, y0 + 6, mix(P['f1'], P['f0'], .3))
        cv.hl(0, 31, y0 + 7, P['f0'])
        # plank end joint
        if rng.random() < .6:
            jx = rng.randint(4, 27)
            cv.vl(jx, y0, y0 + 6, P['f0'])
            cv.vl(jx + 1, y0, y0 + 6, P['f2'])
        # grain
        for _ in range(2):
            gx, gy = rng.randint(1, 20), y0 + rng.randint(1, 5)
            ln = rng.randint(4, 9)
            c = P['f2'] if rng.random() < .6 else P['fb']
            for x in range(gx, gx + ln):
                if cv.get(x, gy)[:3] not in (hx(P['f0'])[:3], hx(P['f2'])[:3]):
                    cv.px(x, gy, c)
    if keep:
        occ[keep[1]:keep[3] + 1, keep[0]:keep[2] + 1] = True
    return cv, occ


def jag(rng, a, b, d=2.2):
    if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 7:
        return [a, b]
    mx = (a[0] + b[0]) / 2 + rng.uniform(-d, d)
    my = (a[1] + b[1]) / 2 + rng.uniform(-d, d)
    mid = (min(29, max(2, mx)), min(29, max(2, my)))
    return jag(rng, a, mid, d)[:-1] + jag(rng, mid, b, d)


def lava(P, rng, keep=None, hot=0):
    cv = Cv(T, T, bg=P['f1'])
    occ = np.zeros((T, T), bool)
    for _ in range(3):
        blob(cv, rng, rng.randint(6, 25), rng.randint(6, 25), rng.uniform(3, 5), P['fb'])
    J = sorted([(rng.randint(7, 13), rng.randint(8, 23)), (rng.randint(18, 25), rng.randint(8, 23))])
    near = lambda p: min(J, key=lambda j: (j[0] - p[0]) ** 2 + (j[1] - p[1]) ** 2)
    segs = [((0, 13), J[0]), (J[0], J[1]), (J[1], (31, 13)), ((16, 0), near((16, 0))), ((16, 31), near((16, 31)))]
    crack = Cv(T, T)
    for a, b in segs:
        crack.line(jag(rng, a, b), LAVA[0])
    cm = crack.m
    cdark = mix(LAVA[0], P['f0'], .45)
    cv.fill(sh(cm, 1, 1) & ~cm, P['f2'])      # plate edge below-right of a crack catches the light
    cv.fill(cm, cdark)
    j = J[rng.randint(0, 1)]                  # one smouldering stretch per tile, away from the border
    cv.fill(cm & cv.E(j[0], j[1], 4.6, 4.6) & cv.R(3, 3, 28, 28), LAVA[0])
    cv.fill(cm & cv.E(j[0], j[1], 1.6, 1.6), LAVA[1])
    if keep:
        occ[keep[1]:keep[3] + 1, keep[0]:keep[2] + 1] = True
    return cv, occ


# ------------------------------------------------------------------ decorated variants
def deco_floor(name, P, rng, which):
    pat = P['floor_pat']
    keep = (8, 8, 23, 23)
    cv, occ = plain(P, rng, 4 + which, keep)
    f0, f1, f2, f3, fb = P['f0'], P['f1'], P['f2'], P['f3'], P['fb']
    if name == 'chikurin':
        a, b = P['leaf']
        leaves = ["...ab\n.aab.\naa...", ".aab.\naabbb\n.aa..", "aa...\n.aab.\n...ab"]
        if which == 0:
            for (x, y, i, fl) in ((9, 9, 0, False), (17, 12, 1, False), (11, 17, 2, False), (19, 19, 0, True)):
                cv.grid(x, y, leaves[i], dict(a=a, b=b), flip=fl)
        else:   # mossy flat stones
            for (cx, cy, rx, ry) in ((13, 13, 4.4, 3.2), (20, 18, 3.4, 2.5), (12, 20, 2.4, 1.8)):
                cv.form(cv.E(cx, cy, rx, ry), (f0, P['k1'], P['k2']), 1, 1)
            cv.grid(11, 11, "aab\n.aa", dict(a=a, b=b))
    elif name == 'inari':
        a, b = P['leaf']
        if which == 0:   # fallen momiji
            for (x, y) in ((9, 10), (18, 9), (13, 16), (20, 19), (10, 21)):
                cv.grid(x, y, ".a.\naba\n.a.", dict(a=a, b=b))
        else:            # stepping stone
            m = cv.E(15.5, 15.5, 8.4, 6.4)
            cv.fill(sh(m, 1, 1), f0)
            cv.form(m, (STONE[0], STONE[1], STONE[2]), 2, 1)
            cv.hl(12, 16, 14, STONE[0])
            cv.hl(15, 19, 17, STONE[0])
    elif name == 'obakedera':
        if which == 0:   # old stain + frayed straw
            blob(cv, rng, 15, 15, 5.5, mix(f1, f0, .6), 6, 25)
            blob(cv, rng, 17, 16, 3, f0, 8, 24)
            cv.hl(9, 13, 22, f3)
            cv.hl(11, 16, 23, f3)
        else:            # fallen ofuda talisman + claw scratches
            cv.rect(10, 11, 14, 19, PAPER[1])
            cv.vl(10, 11, 19, PAPER[2])
            cv.hl(10, 14, 20, f0)
            cv.vl(15, 12, 20, f0)
            cv.vl(12, 13, 17, RED[2])
            cv.hl(11, 13, 14, RED[2])
            for i in range(3):
                cv.line([(18 + i * 2, 10 + i), (21 + i * 2, 20 + i)], f0)
    elif name == 'hakaba':
        if which == 0:   # crack + moss
            cv.line([(9, 8), (12, 12), (11, 16), (15, 19), (14, 23)], f0)
            cv.line([(12, 12), (17, 11), (20, 13)], f0)
            blob(cv, rng, 19, 19, 3.5, MOSS[0], 9, 24)
            cv.grid(18, 18, "aa.\n.aa", dict(a=MOSS[1]))
        else:            # higanbana (red spider lily) growing through the joint
            blob(cv, rng, 15, 20, 4, MOSS[0], 8, 24)
            cv.vl(15, 14, 21, MOSS[1])
            cv.vl(19, 16, 21, MOSS[1])
            cv.grid(12, 10, "r.rr.r\n.rRRr.\nrrRrrr\n.r..r.", dict(r=RED[2], R=RED[3]))
            cv.grid(17, 14, "r.r\nrRr\n.r.", dict(r=RED[2], R=RED[3]))
    elif name == 'kurama':
        if which == 0:   # tengu feather
            cv.grid(10, 10, "........hh\n......hhcc\n....hhccc.\n..qhccc...\n.qhcc.....\nqq........",
                    dict(h='#3a3a5c', c='#16142a', q='#6a6c8c'))
            cv.grid(17, 18, PEBBLES[3], leg(P))
        else:            # half-buried flat rock + cedar twig
            m = cv.PG([(9, 12), (14, 9), (21, 10), (23, 15), (19, 20), (11, 19)])
            cv.fill(sh(m, 1, 1), f0)
            cv.form(m, (P['k0'], P['k1'], P['k2']), 2, 1)
            cv.line([(13, 14), (17, 13), (19, 16)], P['k0'])
            cv.grid(9, 21, "a.a.a\naaaaa\n.a.a.", dict(a=MOSS[1]))
    elif name == 'yukiyama':
        if which == 0:   # clawed tracks
            for (x, y) in ((10, 9), (17, 13), (11, 18), (18, 22)):
                cv.grid(x, y, "b.b.b\n.bbb.\n.bbb.\n..b..", dict(b=f0))
        else:            # bare ice patch
            m = cv.PG([(9, 13), (15, 9), (22, 11), (23, 18), (17, 22), (10, 19)])
            cv.form(m, (ICE[0], ICE[1], ICE[2]), 1, 1)
            cv.line([(13, 13), (16, 12)], ICE[2])
            cv.line([(14, 17), (19, 15)], ICE[0])
            cv.line([(16, 18), (18, 19)], ICE[0])
    elif name == 'ryugu':
        s0, s1, s2 = P['shell']
        if which == 0:   # starfish + crumbs
            cv.grid(11, 10, "....s....\n....s....\n.s.sts.s.\n..sstss..\n...sss...\n..ss.ss..\n.ss...ss.",
                    dict(s=s1, t=s2))
            cv.grid(21, 20, "ss\n.a", dict(s=s1, a=s0))
        else:            # scallop shell + coral twig
            m = cv.E(14, 15, 4.4, 3.6) & cv.R(0, 0, 31, 16)
            cv.fill(sh(m, 1, 1), f0)
            cv.form(m, (s0, s1, s2), 1, 1)
            cv.rect(13, 17, 15, 17, s0)
            for x in (12, 14, 16):
                cv.vl(x, 13, 15, s0)
            cv.grid(19, 17, "r.r.\nrrr.\n.rrr\n.r..", dict(r=RED[1]))
    elif name == 'uminobe':
        s0, s1, s2 = P['shell']
        if which == 0:   # fish skeleton
            cv.grid(9, 12, "..s.s.s.s...s\nsssssssssss.ss\nsts.s.s.s.ssss\n.ss.s.s.s...s", dict(s=s1, t=f0))
            cv.grid(18, 20, "ss\n.a", dict(s=s1, a=s0))
        else:            # driftwood stick + seaweed
            cv.line([(9, 19), (22, 12)], P['k1'])
            cv.line([(9, 20), (22, 13)], P['k0'])
            cv.line([(15, 16), (17, 19)], P['k1'])
            cv.grid(17, 20, "a.a..\naaa.a\n.aaaa\n..aa.", dict(a=MOSS[0]))
    elif name == 'yomi':
        b0, b1, b2, b3 = BONE
        if which == 0:   # scattered bones
            cv.grid(9, 10, "bb......\nbcb.....\n.bccb...\n...bccb.\n.....bcb\n......bb", dict(b=b1, c=b2))
            cv.grid(15, 18, "b.b.b.b\nbcbcbcb\n.b.b.b.", dict(b=b1, c=b2))
        else:            # half-sunk skull + crack
            cv.line([(8, 20), (12, 22), (17, 21), (23, 24)], f0)
            cv.grid(11, 9, ".bccccb.\nbccccccb\nbkkcckkb\nbkkcckkb\n.bcckcb.\n..bbbb..", dict(b=b1, c=b2, k=f0))
    elif name == 'jigoku':
        if which == 0:   # lava pool
            m = cv.PG([(10, 13), (14, 10), (20, 11), (23, 16), (19, 21), (12, 20)])
            cv.fill(dil(m), f0)
            cv.fill(m, LAVA[1])
            cv.fill(cv.E(16, 15.5, 4.4, 3.2), LAVA[2])
            cv.rect(14, 14, 16, 14, LAVA[3])
        else:            # ember vent: bright crack star
            for pts in ([(10, 10), (15, 15), (22, 13)], [(15, 15), (13, 22)], [(15, 15), (20, 21)]):
                cv.line(pts, LAVA[1])
            cv.rect(14, 14, 16, 16, LAVA[2])
            cv.px(15, 15, LAVA[3])
            cv.grid(19, 8, "e.\nee", dict(e=LAVA[2]))
    elif name == 'takamagahara':
        if which == 0:   # gold star inlay
            cv.grid(11, 10, "....g....\n....g....\n...gGg...\n.ggGGGgg.\n...gGg...\n....g....\n....g....",
                    dict(g=GOLD[1], G=GOLD[2]))
            cv.grid(20, 20, ".g.\nggg\n.g.", dict(g=GOLD[1]))
        else:            # kumo curl
            cv.grid(9, 11, "..hhhhh.......\n.h.....h......\nh..hhh..h.....\nh.h...h.h.....\nh.h..hh.h.....\n"
                           "h..hh...hhhhhh\n.h.....h......\n..hhhhh.......", dict(h=f3))
            cv.grid(21, 20, "gg", dict(g=GOLD[1]))
    elif name == 'kawabe':
        a, b = P['leaf']
        if which == 0:   # small flowers + pebbles
            for (x, y) in ((10, 10), (19, 12), (13, 19)):
                cv.grid(x, y, ".w.\nwyw\n.w.\n.a.", dict(w=PAPER[1], y=GOLD[1], a=a))
            cv.grid(18, 19, PEBBLES[3], leg(P, m=P['k1'], h=P['k2']))
        else:            # puddle
            m = cv.PG([(9, 14), (14, 10), (21, 11), (23, 16), (18, 21), (11, 19)])
            cv.fill(dil(m), f0)
            cv.fill(m, '#12244a')
            cv.hl(13, 17, 13, '#1f3a70')
            cv.hl(15, 19, 17, '#1f3a70')
            cv.grid(21, 19, "a.a\naaa", dict(a=a))
    elif name == 'yashiki':
        if which == 0:   # broken plank hole
            m = cv.PG([(10, 10), (21, 9), (22, 13), (18, 14), (20, 20), (11, 21), (12, 15)])
            cv.fill(dil(m), f3)
            cv.fill(m, K)
            cv.line([(12, 12), (15, 13)], f0)
            cv.line([(14, 18), (17, 17)], f0)
        else:            # dark stain + dropped ofuda
            blob(cv, rng, 14, 14, 5, mix(f1, RED[0], .7), 7, 24)
            blob(cv, rng, 15, 15, 2.6, RED[0], 9, 22)
            cv.rect(19, 17, 22, 22, PAPER[1])
            cv.vl(19, 17, 22, PAPER[2])
            cv.vl(21, 18, 21, RED[2])
    elif name == 'oeyama':
        b0, b1, b2, b3 = BONE
        if which == 0:   # gnawed bones
            cv.grid(10, 10, "bb......\nbcb.....\n.bccb...\n...bccb.\n.....bcb\n......bb", dict(b=b1, c=b2))
            cv.grid(17, 18, "bcb\nbcb\n.b.", dict(b=b1, c=b2))
        else:            # dropped sake cup + spill
            blob(cv, rng, 17, 17, 4, P['fb'], 8, 24)
            m = cv.E(13.5, 14, 4.4, 3.2)
            cv.fill(dil(m), f0)
            cv.form(m, (RED[0], RED[1], RED[2]), 1, 1)
            cv.fill(cv.E(13.5, 14, 2.2, 1.4), RED[0])
    elif name == 'shinkai':
        s0, s1, s2 = P['shell']
        if which == 0:   # glowing plankton
            for (x, y, t) in ((10, 10, 0), (19, 12, 1), (13, 19, 1), (21, 21, 0)):
                cv.grid(x, y, [".g.\ngGg\n.g.", "gg\ngg"][t], dict(g=GLOW[1], G=GLOW[2]))
        else:            # tube worms + shell
            for (x, y) in ((11, 12), (14, 10), (17, 13)):
                cv.vl(x, y, y + 6, s1)
                cv.vl(x + 1, y + 1, y + 6, s0)
                cv.hl(x, x + 1, y - 1, GLOW[1])
            cv.grid(19, 19, "ss.\nsts\n.ss", dict(s=s1, t=s2))
    elif name == 'enma_cho':
        if which == 0:   # gold inlay seal
            ring = cv.E(15.5, 15.5, 6.4, 6.4) & ~cv.E(15.5, 15.5, 5.2, 5.2)
            cv.fill(ring, GOLD[0])
            cv.fill(ring & cv.R(0, 0, 15, 15), GOLD[1])
            cv.rect(15, 12, 16, 19, GOLD[0])
            cv.rect(12, 15, 19, 16, GOLD[0])
        else:            # glowing crack across the slab
            cv.line([(8, 11), (12, 14), (15, 13), (19, 18), (23, 19)], LAVA[0])
            cv.line([(12, 14), (15, 13), (19, 18)], LAVA[1])
            cv.line([(15, 13), (17, 9)], LAVA[0])
            cv.rect(15, 14, 16, 14, LAVA[2])
    elif name == 'yomi_oku':
        v0, v1, v2, v3 = VIOLET
        if which == 0:   # Yomotsu-hegui: umgestürzte Lackschale, verschütteter Totenreis
            blob(cv, rng, 17, 18, 4.4, P['fb'], 9, 24)
            m = cv.E(13, 14, 4.6, 3.4) & cv.R(0, 0, 31, 15)
            cv.fill(dil(m), f0)
            cv.form(m, (v0, v1, v2), 1, 1)
            cv.hl(10, 16, 15, RED[1])
            for (x, y) in ((17, 16), (19, 17), (16, 19), (20, 19), (18, 21), (22, 18), (15, 17)):
                cv.px(x, y, BONE[2])
            cv.px(21, 20, BONE[1])
        else:            # Riss, aus dem kaltes Totenfeuer schimmert
            cv.line([(8, 12), (12, 15), (15, 13), (19, 18), (24, 19)], ONIBI[0])
            cv.line([(12, 15), (15, 13), (19, 18)], ONIBI[1])
            cv.line([(15, 13), (16, 8)], ONIBI[0])
            cv.rect(15, 14, 16, 14, ONIBI[2])
            cv.grid(19, 8, "o.\noo", dict(o=ONIBI[1]))
    elif name == 'iwato':
        if which == 0:   # eingelassene Sonnenscheibe aus Blattgold, acht Strahlen
            for i in range(8):
                a = i * math.pi / 4
                cv.line([(15.5 + math.cos(a) * 5, 15.5 + math.sin(a) * 5), (15.5 + math.cos(a) * 9, 15.5 + math.sin(a) * 9)], SUN[1])
            m = cv.E(15.5, 15.5, 4.2, 4.2)
            cv.fill(dil(m), f0)
            cv.form(m, (SUN[1], SUN[2], SUN[3]), 1, 1)
            cv.fill(cv.E(15.5, 15.5, 1.6, 1.6), SUN[1])
        else:            # Sakaki-Blätter und eine lange Hahnenfeder (Tokoyo no Nagadori)
            for (x, y) in ((9, 10), (21, 19), (12, 21)):
                cv.grid(x, y, ".gg\nggG\n.g.", dict(g=MOSS[1], G=MOSS[2]))
            cv.line([(14, 12), (17, 14), (20, 14), (23, 12)], PAPER[2])
            cv.line([(15, 13), (18, 15), (21, 15)], PAPER[1])
            cv.px(23, 12, SUN[2])
    elif name == 'tsukiyomi':
        s0, s1, s2, s3 = SILVER
        if which == 0:   # crescent inlay
            m = cv.E(15.5, 15.5, 6.4, 6.4) & ~cv.E(18, 14, 5.6, 5.6)
            cv.fill(m, s1)
            cv.fill(m & ~sh(m, 1, 1), s2)
        else:            # star dust
            for (x, y, c) in ((10, 10, s2), (19, 11, s1), (13, 18, s1), (20, 20, s2)):
                cv.grid(x, y, ".s.\nsss\n.s.", dict(s=c))
            cv.rect(16, 15, 17, 15, s1)
    return cv


# ------------------------------------------------------------------ dispatch
def plain(P, rng, v, keep=None):
    pat = P['floor_pat']
    if pat == 'tatami':
        return tatami(P, rng, keep, vert=v % 2 == 1)
    if pat == 'stone':
        return stone(P, rng, keep, layout=[0, 1, 3, 2, 0, 0][v])
    return dict(grass=grass, gravel=gravel, snow=snow, sand=sand, coral=coral, cloud=cloud, wood=wood,
                lava=lava)[pat](P, rng, keep)


def floor_tiles(name):
    P = BIOMES[name]
    tiles = []
    for v in range(4):
        rng = random.Random('%s-floor-%d' % (name, v))
        tiles.append(plain(P, rng, v)[0])
    for w in range(2):
        rng = random.Random('%s-deco-%d' % (name, w))
        tiles.append(deco_floor(name, P, rng, w))
    return tiles


if __name__ == '__main__':
    import sys
    names = sys.argv[1:] or ORDER
    cols = 3
    rows = (len(names) + cols - 1) // cols
    W, H = 13 * T, 7 * T
    sheet = Image.new('RGBA', (cols * (W + 8), rows * (H + 8)), (0, 0, 0, 255))
    for n, name in enumerate(names):
        tl = floor_tiles(name)
        rng = random.Random(name)
        room = Cv(W, H)
        for j in range(7):
            for i in range(13):
                t = tl[rng.randint(0, 3)] if rng.random() < .88 else tl[rng.randint(4, 5)]
                room.a[j * T:(j + 1) * T, i * T:(i + 1) * T] = t.a
        sheet.paste(room.img(), ((n % cols) * (W + 8), (n // cols) * (H + 8)))
    sheet.save('_floortest.png')
