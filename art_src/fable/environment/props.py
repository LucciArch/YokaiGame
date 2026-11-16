"""Obstacles (rock.png, 3 x 32x32, transparent) and top-wall decorations (wall_deco.png, 2 x 32x16).
Built from a small library of shared motifs (boulder, stump, pillar, box, barrel, spires, skull ...)
recoloured and dressed per biome."""
import math
import random
import numpy as np
from core import *
from biomes import *

IRON = ('#14142a', '#262a48', '#444c70', '#7884a8')
BRONZE = ('#14242a', '#264440', '#44685a', '#74947a')
STRAW = ('#3a2e2a', '#6a583e', '#94804e', '#c0b070')
WHITE = ('#3a4070', '#6a74a0', '#a4acc8', '#d8dcec')
WATER = ('#12244a', '#1f3a70', '#3a66a8', '#7ab0d8')


def capsule(cv, x0, y0, r0, x1, y1, r1):
    dx, dy = x1 - x0, y1 - y0
    d2 = dx * dx + dy * dy or 1
    t = np.clip(((cv.X - x0) * dx + (cv.Y - y0) * dy) / d2, 0, 1)
    px, py = x0 + t * dx, y0 + t * dy
    r = r0 + (r1 - r0) * t
    return (cv.X - px) ** 2 + (cv.Y - py) ** 2 <= r * r


def fin(cv, P, shadow=True):
    """K outline + solid ground shadow to the lower right"""
    m = cv.m.copy()
    cv.outline(K)
    if shadow:
        ys, xs = cv.nz(m)
        y1 = ys.max()
        sel = xs[ys >= y1 - 2]
        x0, x1 = sel.min(), sel.max()
        s = cv.E((x0 + x1) / 2 + 2.5, min(y1 + .5, 29.5), (x1 - x0) / 2 + 2.5, 2.3) & ~cv.m
        cv.fill(s, mix(P['f0'], K, .55))
    return cv


GLYPHS = [                                               # 家 之 墓, 7x7 Hi-Res-Pixel
    ["...x...", "xxxxxxx", "x.....x", ".xxxxx.", "..xx.x.", ".x.xx..", "x.x..xx"],
    ["...x...", "....x..", ".xxxxx.", "....x..", "...x...", ".xx....", "x.xxxxx"],
    [".x...x.", "xxxxxxx", ".xxxxx.", ".x...x.", ".xxxxx.", "xxxxxxx", ".x.x.x."],
]


SUIJIN = [                                               # 水 神
    ["...x...", "...x...", "xx.x.x.", ".x.xx..", ".xxx.x.", "x..x..x", "..xx..."],
    [".x....x..", "xxx.xxxxx", "..x.x.x.x", ".xx.xxxxx", "x.x.x.x.x", "..x.xxxxx", "..x...x.."],
]


# ------------------------------------------------------------------ shared motifs
def boulder(cv, rng, ramp, cx=16, by=28, rx=11, ry=9):
    """Felsbrocken mit drei Facetten (Licht oben links), Rissen, Körnung und Kieseln am Fuß."""
    pts = []
    n = 9
    for i in range(n):
        a = 2 * math.pi * i / n + rng.uniform(-.15, .15)
        r = rng.uniform(.82, 1.05)
        pts.append((cx + math.cos(a) * rx * r, by - ry + math.sin(a) * ry * r))
    m = cv.PG(pts) & (cv.Y <= by)
    mid0 = mix(ramp[0], ramp[1], .5)
    cv.fill(m, ramp[1])
    # Schattenflanke rechts: Grat vom Scheitel schräg nach unten
    gx = cx + rng.uniform(-1, 1.5)
    cv.fill(cv.PG([(gx + 1, by - ry * 2.2), (cx + rx * 1.4, by - ry * 2.2), (cx + rx * 1.4, by + 1),
                   (gx + rx * .45, by + 1), (gx + rx * .2, by - ry * .55)]) & m, mid0)
    # Lichtfläche oben
    top = cv.PG([(cx + (x - cx) * .66 - rx * .16, by - ry + (y - by + ry) * .52 - ry * .36) for x, y in pts]) & m
    cv.form(top, (ramp[1], ramp[2], ramp[3]), 1, 1)
    # Bodenkontakt und Schattensichel
    k = max(2, int(rx / 3)) * cv.ss
    cv.fill(m & ~sh(m, -k, -k) & ~top, ramp[0])
    cv.fill(m & (cv.Y > by - 1.6), ramp[0])
    # Risse: dunkle Kerbe mit Lichtkante darunter
    for _ in range(2):
        x0, y0 = cx + rng.uniform(-rx * .55, rx * .35), by - ry * rng.uniform(1.1, 1.5)
        path = [(x0, y0)]
        for _ in range(3):
            x0 += rng.uniform(-1.5, 2.5); y0 += rng.uniform(1.5, 2.6)
            path.append((x0, y0))
        cv.hline(path, mix(K, ramp[0], .35))
        cv.hline([(x + .5, y + .5) for x, y in path], ramp[2])
        cv.a[~m] = 0
    # Körnung
    ys, xs = np.nonzero(m)
    for i in rng.sample(range(len(ys)), min(len(ys), 22)):
        y, x = ys[i], xs[i]
        dark = top[y, x] or rng.random() < .5
        cv.a[y, x] = hx(ramp[0] if dark else ramp[2])
    # Kiesel am Fuß
    for sx in (-1, 1):
        if rng.random() < .75:
            px_, pr = cx + sx * (rx + rng.uniform(.5, 2)), rng.uniform(1.4, 2.2)
            pm = cv.E(px_, by - pr * .6, pr, pr * .7) & ~m
            cv.form(pm, (ramp[0], ramp[1], ramp[2]), .5, 1)
            m = m | pm
    return m


def cover(cv, m, ramp, depth, rng):
    """moss / snow blanket on the upper part of mask m"""
    ys, xs = cv.nz(m)
    top = ys.min()
    q = cv.ss
    lim = np.zeros(cv.w * q)
    for i in range(cv.w * q):
        x = i / q
        lim[i] = top + depth + math.sin(x * .9 + rng.uniform(0, .5)) * 1.3 + (x - xs.mean()) * .12
    c = m & (cv.Y <= lim[np.arange(cv.w * q)][None, :])
    cv.fill(c, ramp[1])
    cv.fill(c & ~sh(c, 1, 1), ramp[2])
    cv.fill(c & ~sh(c, 0, -1) & sh(m, 0, -1), ramp[0])
    return c


def cyl(cv, ramp, cx, by, rx, h, top=None, ry=None):
    """upright cylinder (stump / pillar / barrel): shaded side + lit top ellipse"""
    ry = ry or max(1.6, rx * .42)
    side = (cv.R(cx - rx, by - h, cx + rx, by - ry * .6) | cv.E(cx, by - ry * .6, rx, ry))
    cv.form(side, (ramp[0], ramp[1], ramp[2]), max(2, int(rx * .55)), 1)
    t = cv.E(cx, by - h, rx, ry)
    top = top or (ramp[1], ramp[2], ramp[3])
    cv.fill(dil(t) & side, ramp[0])
    cv.form(t, top, 1, 1)
    return side | t, t


def box(cv, ramp, x0, y0, x1, y1, top=4):
    cv.rect(x0, y0 + top, x1, y1, ramp[1])
    cv.rect(x1 - 2, y0 + top, x1, y1, ramp[0])
    cv.hl(x0, x1, y1, ramp[0])
    cv.vl(x0, y0 + top, y1 - 1, ramp[2])
    cv.rect(x0, y0, x1, y0 + top - 1, ramp[2])
    cv.hl(x0, x1, y0, ramp[3])
    cv.hl(x0, x1, y0 + top - 1, ramp[1])


def spire(cv, ramp, xb, by, w, h, lean=0):
    tip = (xb + w / 2 + lean, by - h)
    m = cv.PG([(xb, by), tip, (xb + w, by)])
    cv.fill(m, ramp[1])
    cv.fill(cv.PG([(xb + w * .55, by), tip, (xb + w, by)]) & m, ramp[0])
    cv.line([(xb, by), tip], ramp[2])
    cv.line([(xb + 1, by - 2), (tip[0], tip[1] + 2)], ramp[2])
    return m


def skull(cv, cx, cy, ramp, r=4.4, eye=None):
    m = cv.E(cx, cy, r, r * .9) | cv.R(cx - r * .55, cy, cx + r * .55, cy + r * 1.15)
    cv.fill(dil(m), ramp[0])
    cv.form(m, (ramp[1], ramp[2], ramp[3]), 2, 1)
    e = eye or K
    for sx in (-1, 1):
        x = int(round(cx + sx * r * .45 - .5))
        cv.rect(x, int(cy), x + 1, int(cy) + 1, K)
        if eye:
            cv.px(x + (1 if sx < 0 else 0), int(cy) + 1, e)
    cv.px(int(cx), int(cy + r * .55), ramp[0])
    for x in range(int(cx - r * .5), int(cx + r * .55) + 1, 2):
        cv.px(x, int(cy + r * 1.15), ramp[0])
    return m


def bone(cv, x0, y0, x1, y1, ramp):
    cv.line([(x0, y0), (x1, y1)], ramp[2])
    cv.line([(x0, y0 + 1), (x1, y1 + 1)], ramp[1])
    for (x, y) in ((x0, y0), (x1, y1)):
        cv.rect(x - 1, y - 1, x, y + 1, ramp[2])
        cv.px(x, y + 1, ramp[1])


def rope(cv, x0, x1, y, sag, shide=()):
    for x in range(x0, x1 + 1):
        t = (x - x0) / max(1, x1 - x0)
        yy = int(round(y + sag * math.sin(math.pi * t)))
        cv.px(x, yy, STRAW[2] if x % 3 else STRAW[1])
        cv.px(x, yy + 1, STRAW[1] if x % 3 else STRAW[0])
    for x in shide:
        t = (x - x0) / max(1, x1 - x0)
        yy = int(round(y + sag * math.sin(math.pi * t))) + 2
        cv.grid(x, yy, "pP\npP\n.pP\n.pP", dict(p=PAPER[2], P=PAPER[3]))


def flame(cv, x, y, ramp=LAVA):
    cv.grid(x, y, "..a..\n.ab..\n.abb.\nabcba\n.bcb.", dict(a=ramp[1], b=ramp[2], c=ramp[3]))


# ------------------------------------------------------------------ obstacles
def rocks(name):
    P = BIOMES[name]
    k = (P['k0'], P['k1'], P['k2'], P['k3'])
    out = []

    def new(i):
        return Cv(32, 32), random.Random('%s-rock-%d' % (name, i))

    def plain_boulder(i, ramp=k, **kw):
        cv, rng = new(i)
        m = boulder(cv, rng, ramp, **kw)
        return cv, rng, m

    def pillar(i, ramp, bands=None, broken=False, r=5.5, h=17):
        cv, rng = new(i)
        m, t = cyl(cv, ramp, 15.5, 28, r, h)
        cyl(cv, ramp, 15.5, 29, r + 1.5, 2)                  # plinth
        if bands:
            for y in (15, 24):
                bm = m & ~t & (cv.Y >= y) & (cv.Y <= y + 1)
                cv.fill(bm, bands[1])
                cv.fill(bm & (cv.X > 17), bands[0])
                cv.fill(bm & (cv.X < 12) & (cv.Y == y), bands[2])
        if broken:
            cv.fill(cv.PG([(8, 6), (24, 6), (24, 13), (19, 10), (16, 14), (12, 11), (8, 14)]), (0, 0, 0, 0))
        return cv

    if name == 'chikurin':
        cv, rng = new(0)                                     # cut bamboo stumps: slanted cut, hollow, nodes
        g = (P['w0'], P['w1'], P['w2'], P['w3'])
        inner = mix(g[0], K, .45)
        for (x, h, r, tilt) in ((10, 13, 3.2, 2.2), (21.5, 9, 3.4, -1.8), (15.5, 19, 3.7, 2.6)):
            yb = 28
            body = cv.R(x - r, yb - h - abs(tilt), x + r, yb) | cv.E(x, yb, r, r * .45)
            cut = cv.PG([(x - r - 1, yb - h - tilt), (x + r + 1, yb - h + tilt), (x + r + 1, 0), (x - r - 1, 0)])
            body &= ~cut
            cv.form(body, (g[0], g[1], g[2]), max(2, int(r * .55)), 1)
            cv.fill(body & (cv.X < x - r * .35) & (cv.X > x - r * .75), g[3])   # Glanzstreifen
            # schräge Schnittfläche: helle Wandung, dunkles hohles Inneres
            rim = cv.PG([(x - r, yb - h - tilt), (x + r, yb - h + tilt), (x + r, yb - h + tilt + 1.6), (x - r, yb - h - tilt + 1.6)])
            ring = (cv.E(x, yb - h, r, r * .5 + abs(tilt) * .5) & (rim | dil(rim)))
            cv.fill(ring, g[3])
            cv.fill(cv.E(x, yb - h + .2, r - 1.7, max(.6, r * .3)) & body, inner)
            # Knoten: helle Wulst über dunkler Kerbe
            for y in range(yb - h + 6, yb - 2, 7):
                nm = body & (cv.Y >= y) & (cv.Y < y + .6)
                cv.fill(nm, g[0])
                cv.fill(sh(nm, 0, -1) & body, g[2])
        for sx, ang in ((5, -1), (26, 1)):                    # kleine Blattzweige am Fuß
            leaf = capsule(cv, sx, 27.5, .4, sx + ang * 4, 25.5, 1.1)
            cv.fill(leaf, g[2]); cv.fill(leaf & sh(leaf, 1, 0) & ~sh(leaf, 0, 1), g[1])
        out.append(fin(cv, P))
        cv, rng, m = plain_boulder(1)
        cover(cv, m, MOSS, 5, rng)
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # takenoko bamboo shoot
        s = ('#261622', '#4a2e26', '#74502c', '#a07c40')
        m = cv.PG([(15, 7), (17, 7), (22, 20), (22, 27), (10, 27), (10, 20)])
        cv.form(m, (s[0], s[1], s[2]), 3, 1)
        for y in (12, 16, 20, 24):
            cv.line([(9, y + 3), (15.5, y - 1), (22, y + 3)], s[0])
            cv.fill(sh(cv.PG([(9, y + 3), (15.5, y - 1), (15.5, y)]) & m, 0, 1) & m & (cv.X < 15), s[3])
        cv.fill(m & (cv.Y < 10), MOSS[2])
        out.append(fin(cv, P))

    elif name == 'inari':
        cv, rng = new(0)                                     # kitsune statue
        box(cv, k, 8, 24, 24, 28, top=2)
        body = cv.E(18, 18.5, 4.6, 6) | cv.R(12, 17, 15, 24)
        tail = capsule(cv, 23, 22, 2, 24.5, 12, 2.6)
        cv.form(tail, (k[0], k[1], k[2]), 2, 1)
        cv.fill(dil(body), k[0])
        cv.form(body, (k[1], k[2], k[3]), 3, 1)
        head = cv.E(13.5, 11, 3.6, 3.2) | cv.PG([(11, 10), (6, 12.5), (11, 14)]) | \
            cv.PG([(12, 9), (12.5, 4), (15, 8)]) | cv.PG([(14, 9), (16.5, 5), (17, 10)])
        cv.fill(dil(head), k[0])
        cv.form(head, (k[1], k[2], k[3]), 2, 1)
        cv.hl(11, 12, 10, K)
        cv.rect(12, 14, 16, 15, RED[2])
        cv.hl(12, 16, 16, RED[1])
        cv.vl(15, 19, 23, k[0])
        out.append(fin(cv, P))
        cv, rng, m = plain_boulder(1)                        # sacred rock with shimenawa
        ys, xs = cv.nz(m & (np.abs(cv.Y - 20) < .3))
        rope(cv, xs.min(), xs.max(), 19, 1.5, shide=(11, 16, 21))
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # hokora mini shrine
        box(cv, k, 9, 23, 23, 28, top=2)
        box(cv, RED, 11, 14, 21, 22, top=0)
        cv.rect(14, 16, 18, 22, K)
        cv.vl(16, 16, 22, RED[1])
        roof = cv.PG([(7, 14), (12, 7), (20, 7), (25, 14)])
        cv.form(roof, ('#12101c', '#22203a', '#3a3a5c'), 2, 1)
        cv.hl(7, 25, 14, '#12101c')
        cv.hl(12, 20, 7, P['lip'])
        out.append(fin(cv, P))

    elif name == 'obakedera':
        cv, rng = new(0)                                     # fallen temple bell
        m = cv.PG([(11, 11), (21, 11), (23, 23), (25, 27), (7, 27), (9, 23)]) | cv.E(16, 11, 5, 3.4)
        cv.form(m, (BRONZE[0], BRONZE[1], BRONZE[2]), 4, 1)
        for y in (14, 22):
            cv.fill(m & (cv.Y == y), BRONZE[0])
            cv.fill(m & (cv.Y == y + 1) & (cv.X < 15), BRONZE[3])
        cv.rect(15, 17, 17, 19, BRONZE[0])
        cv.rect(14, 5, 18, 7, BRONZE[1])
        cv.rect(15, 6, 17, 7, K)
        cv.hl(14, 18, 5, BRONZE[2])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # saisen-bako offering box
        box(cv, k, 6, 13, 26, 28, top=5)
        for x in range(8, 26, 3):
            cv.vl(x, 14, 16, K)
        cv.hl(7, 23, 21, k[0])
        cv.rect(14, 23, 17, 26, k[0])
        cv.rect(6, 27, 8, 28, k[0])
        cv.rect(24, 27, 26, 28, K)
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # weathered jizo
        s = STONE
        box(cv, s, 9, 25, 23, 28, top=2)
        body = cv.PG([(12, 14), (20, 14), (22, 25), (10, 25)])
        cv.form(body, (s[0], s[1], s[2]), 3, 1)
        head = cv.E(16, 10, 4.4, 4.4)
        cv.fill(dil(head), s[0])
        cv.form(head, (s[1], s[2], s[3]), 2, 1)
        cv.hl(13, 14, 10, s[0])
        cv.hl(17, 18, 10, s[0])
        cv.fill(cv.PG([(12, 14), (20, 14), (18, 19), (14, 19)]), RED[2])
        cv.hl(13, 19, 14, RED[3])
        cv.fill(cv.PG([(17, 15), (20, 14), (18, 19)]), RED[1])
        out.append(fin(cv, P))

    elif name == 'hakaba':
        cv, rng = new(0)                                     # Familiengrab: 家之墓, Blumenvasen, Räucherstäbchen
        box(cv, k, 5, 24, 27, 28, top=2)
        box(cv, k, 8, 19, 24, 23, top=2)
        cv.rect(11, 4, 21, 18, k[2])                         # polierter Saoishi
        cv.rect(20, 4, 21, 18, k[1])
        cv.vl(11, 4, 18, k[3])
        cv.hl(11, 20, 3, k[3])
        cv.hl(12, 19, 18, k[1])
        for i, g in enumerate(GLYPHS):                       # eingemeißelte Inschrift, Kerbe mit Lichtkante
            for j, row in enumerate(g):
                for i2, ch in enumerate(row):
                    if ch == 'x':
                        x, y = 14 + i2 * .5, 5.5 + i * 4 + j * .5
                        cv.hpx(x + .5, y + .5, k[3])
                        cv.hpx(x, y, k[0])
        for x in (9, 23):                                    # Hanatate mit Shikimi
            cv.rect(x - 1, 16, x + 1, 19, STONE[2])
            cv.vl(x + 1, 16, 19, STONE[1])
            cv.hl(x - 1, x + 1, 16, STONE[3])
            cv.grid(x - 2, 12, ".a.a.\naaba.\n.aaa.\n..a..", dict(a=MOSS[2], b=MOSS[3]))
        cv.grid(7, 11, "r.r\n.R.", dict(r=RED[2], R=RED[3]))      # Higanbana
        cv.rect(13, 21, 19, 24, IRON[1])                     # Kōro mit drei Räucherstäbchen
        cv.hl(13, 19, 21, IRON[2])
        cv.vl(19, 21, 24, IRON[0])
        for x in (15, 16, 17):                               # dünne Stäbchen auf der Hi-Res-Ebene
            for y in (18.5, 19, 19.5, 20, 20.5):
                cv.hpx(x + .5, y, '#6a4a2a')
            cv.hpx(x + .5, 18, LAVA[3])
        for (x, y) in ((16, 17), (16.5, 16.5), (17, 16), (17, 15.5), (16.5, 15), (16, 14.5), (16, 14), (16.5, 13.5)):
            cv.hpx(x, y, PAPER[3])
        cv.rect(21, 23, 22, 24, PAPER[2])                    # Wasserschale
        cv.hl(21, 22, 23, PAPER[3])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # round-top stele, mossy, cracked
        m = cv.R(10, 12, 22, 28) | cv.E(16, 12, 6.4, 6)
        cv.form(m, (k[0], k[1], k[2]), 3, 1)
        cv.line([(19, 7), (17, 12), (19, 16), (18, 20)], k[0])
        cover(cv, m, MOSS, 4, rng)
        cv.rect(13, 16, 14, 22, k[0])
        cv.fill(m & (cv.Y >= 26) & (cv.X < 15), MOSS[1])
        mk = cv.E(19.5, 26, 2.2, 1.9)                         # Opfergabe: Mikan mit Blatt und Sake-Schälchen
        cv.fill(dil(mk), K)
        cv.form(mk, (LAVA[1], LAVA[2], LAVA[3]), 1, 1)
        cv.px(20, 24, MOSS[2])
        cv.rect(23, 26, 25, 27, PAPER[2])
        cv.hl(23, 25, 26, PAPER[3])
        cv.px(24, 26, RED[1])
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # gorinto five-ring tower
        box(cv, k, 10, 21, 22, 28, top=2)
        m = cv.E(16, 17, 5, 4.2)
        cv.fill(dil(m), k[0])
        cv.form(m, (k[0], k[1], k[2]), 2, 1)
        roof = cv.PG([(8, 13), (13, 9), (19, 9), (24, 13)])
        cv.fill(dil(roof), k[0])
        cv.form(roof, (k[1], k[2], k[3]), 2, 1)
        top = cv.E(16, 6.5, 2.6, 2.8)
        cv.fill(dil(top), k[0])
        cv.form(top, (k[1], k[2], k[3]), 1, 1)
        out.append(fin(cv, P))

    elif name == 'iwato':
        cv, rng = new(0)                                     # Sakaki mit Yata-Spiegel, Magatama und Shide (wie in der Sage)
        tr = ('#1c1012', '#3a2418', '#5a3a22')
        cv.fill(cv.R(15, 14, 17, 28), tr[1])
        cv.vl(15, 14, 28, tr[2])
        cv.vl(17, 16, 28, tr[0])
        cv.line([(16, 18), (11, 13)], tr[1])
        cv.line([(16, 16), (21, 11)], tr[1])
        for (x, y, rx, ry) in ((10, 10, 5, 3.6), (22, 9, 5, 3.4), (16, 6, 5.5, 3.6), (13, 15, 3.6, 2.4), (20, 14, 3.4, 2.2)):
            m = cv.E(x, y, rx, ry)
            cv.fill(dil(m), K)
            cv.form(m, (MOSS[0], MOSS[1], MOSS[2]), 1, 1)
        for (x, y) in ((9, 9), (14, 5), (21, 8), (18, 5), (12, 14)):
            cv.hpx(x, y, MOSS[3])
        mir = cv.E(16, 13, 3.2, 3.2)                         # Yata no Kagami am Stamm
        cv.fill(dil(mir), K)
        cv.form(mir, (SUN[1], SUN[2], SUN[3]), 1, 1)
        cv.fill(cv.E(16, 13, 2, 2), '#f8f0c8')
        cv.hpx(15, 12, '#ffffff')
        cv.hline([(10, 15), (10, 18)], PAPER[2])             # Magatama-Schnur links
        for y in (16, 18):
            cv.fill(cv.E(10, y + .5, .9, .9), '#3ab07a')
            cv.hpx(9.5, y, '#9ae8b8')
        cv.grid(21, 15, "pP\npP\n.pP\n.pP", dict(p=PAPER[2], P=PAPER[3]))   # Shide rechts
        cv.rect(12, 27, 20, 28, STRAW[1])                    # Wurzelballen in Stroh gebunden
        cv.hl(12, 20, 27, STRAW[2])
        out.append(fin(cv, P))

        cv, rng = new(1)                                     # Tokoyo no Nagadori: der Hahn, der die Sonne ruft
        cv.rect(7, 22, 25, 23, '#5a3a22')                    # Sitzstange
        cv.hl(7, 25, 22, '#7a5432')
        for x in (9, 23):
            cv.vl(x, 24, 28, '#3a2418')
        tail = cv.PG([(13, 14), (7, 12), (4, 16), (5, 22), (8, 26), (10, 21), (13, 19)])
        cv.fill(dil(tail), K)
        cv.form(tail, ('#14141e', '#26283a', '#3a4060'), 1, 1)
        for (a, b) in (((12, 15), (5, 17)), ((12, 17), (6, 22)), ((12, 18), (8, 25))):
            cv.hline([a, b], '#7a8ab0')                      # lange, schillernde Schwanzfedern
        body = cv.E(16, 17, 4.6, 3.8)
        cv.fill(dil(body), K)
        cv.form(body, ('#a04a18', '#d0702a', '#f0a040'), 1, 1)
        neck = cv.E(19, 12, 2.4, 3.6)
        cv.fill(dil(neck), K)
        cv.form(neck, (SUN[1], SUN[2], SUN[3]), 1, 1)
        cv.grid(18, 7, "r.r\nrrr", dict(r=RED[2]))         # Kamm
        cv.px(21, 11, '#e8c048')                             # Schnabel
        cv.px(22, 11, '#a88028')
        cv.px(20, 10, K)
        cv.px(20, 13, RED[2])                                # Kehllappen
        cv.vl(15, 21, 21, '#e8c048')
        cv.vl(17, 21, 21, '#e8c048')
        out.append(fin(cv, P))

        cv, rng = new(2)                                     # Ukefune: umgedrehter Bottich, auf dem Ame-no-Uzume tanzte
        m, t = cyl(cv, ('#1c1012', '#4a2e1e', '#6e4a2c', '#8e6a40'), 16, 28, 10, 9)
        for x in (9, 13, 19, 23):
            cv.vl(x, 20, 27, '#2e1c14')
        for y in (21, 26):                                   # Bambusreifen
            cv.hl(6, 26, y, STRAW[2])
            cv.hl(6, 26, y + 1, STRAW[0])
        cv.rect(11, 17, 21, 17, PAPER[2])                    # Sakaki-Zweig mit Glöckchen auf dem Deckel
        cv.line([(11, 16), (21, 14)], '#3a2418')
        for (x, y) in ((13, 14), (17, 13), (20, 12)):
            cv.grid(x, y, "gG\n.g", dict(g=MOSS[1], G=MOSS[2]))
        for (x, y) in ((12, 17), (15, 16), (18, 15)):
            cv.fill(cv.E(x, y, .8, .8), SUN[2])
            cv.hpx(x - .5, y - .5, SUN[3])
        out.append(fin(cv, P))

    elif name == 'kurama':
        cv, rng, m = plain_boulder(0)
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # cedar stump
        w = ('#1c121c', '#3a2428', '#58382c', '#7a5236')
        m, t = cyl(cv, w, 16, 28, 8, 11, top=('#58382c', '#8a6a44', '#a88a58'))
        for x in (10, 13, 19, 22):
            cv.vl(x, 21, 27, w[0])
        cv.fill((cv.E(16, 17, 5, 2) & ~cv.E(16, 17, 4, 1.3)), '#58382c')
        cv.rect(15, 17, 16, 17, '#58382c')
        cv.rect(5, 26, 8, 28, w[1])                          # roots
        cv.rect(24, 27, 27, 28, w[0])
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # cairn
        for (cx, cy, rx, ry) in ((16, 25, 9.4, 3.4), (15, 20, 7.4, 3), (16.5, 15.5, 5.4, 2.6), (16, 11.5, 3.4, 2.2)):
            m = cv.E(cx, cy, rx, ry)
            cv.fill(dil(m), k[0])
            cv.form(m, (k[1], k[2], k[3]), 2, 1)
        out.append(fin(cv, P))

    elif name == 'yukiyama':
        sn = P['snow']
        cv, rng = new(0)                                     # ice crystal cluster
        for (x, w, h, l) in ((5, 7, 14, -2), (19, 8, 16, 3), (11, 9, 23, 0)):
            spire(cv, k, x, 28, w, h, l)
        cv.line([(15, 12), (14, 16)], k[3])
        drift = (cv.E(10, 28, 7, 2.6) | cv.E(21, 28.4, 6, 2.2)) & (cv.Y <= 28.6)
        cv.fill(drift, P['snow'][1])
        cv.fill(drift & ~sh(drift, 0, -1), P['snow'][2])
        out.append(fin(cv, P))
        cv, rng, m = plain_boulder(1, ramp=STONE)            # snow-covered boulder
        cover(cv, m, sn, 7, rng)
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # Eisbrocken: drei Facetten, Risse, Luftblasen, Schneekappe
        top = [(7, 13), (13, 9), (22, 8), (26, 12), (20, 15), (11, 16)]
        m = cv.PG([(7, 13), (13, 9), (22, 8), (26, 12), (26, 25), (20, 29), (9, 28), (5, 24)])
        left = cv.PG([(7, 13), (11, 16), (20, 15), (20, 29), (9, 28), (5, 24)]) & m
        cv.fill(m, k[0])                                     # Schattenseite rechts
        cv.fill(left, k[1])
        cv.fill(left & (cv.X < 9), k[2])                     # Lichtkante links
        cv.fill(cv.PG(top) & m, k[2])
        cv.fill(cv.PG([(13, 10), (21, 9), (23, 11), (15, 12)]), k[3])
        cv.hline([(11, 16), (20, 15), (26, 12)], k[3])       # Kanten fangen das Mondlicht
        cv.hline([(20, 15), (20, 28)], mix(k[1], k[3], .5))
        for path in (((10, 19), (12, 22), (11, 25)), ((15, 17), (17, 21)), ((23, 15), (22, 19), (24, 23))):
            cv.hline(path, mix(k[0], K, .3))
            cv.hline([(x + .5, y) for x, y in path], k[3])
        for bx, by in ((13, 24), (16, 26), (8, 21), (23, 25)):
            cv.hpx(bx, by, k[3])
        sn = P['snow']
        cap = cv.PG([(8, 13), (13, 9), (22, 8), (26, 12), (24, 13), (19, 12), (15, 14), (11, 13)])
        cv.fill(cap, '#d8e8f4')
        cv.fill(cap & (cv.Y > 11.5), sn[2])
        cv.a[~m] = 0
        out.append(fin(cv, P))

    elif name == 'ryugu':
        cv, rng = new(0)                                     # branching coral
        m = np.zeros(cv.a.shape[:2], bool)
        for (a, b, r0, r1) in (((16, 28), (16, 18), 2.6, 2.2), ((16, 19), (9, 10), 2.2, 1.6), ((16, 19), (22, 9), 2.2, 1.6),
                               ((11, 13), (6, 14), 1.6, 1.4), ((13, 14), (14, 6), 1.7, 1.4), ((20, 12), (26, 13), 1.6, 1.4),
                               ((20, 13), (19, 5), 1.5, 1.4)):
            m |= capsule(cv, a[0], a[1], r0, b[0], b[1], r1)
        cv.form(m, (k[0], k[1], k[2]), 2, 1)
        for (x, y) in ((8, 9), (13, 5), (21, 8), (18, 4)):
            cv.rect(x, y, x + 1, y, k[3])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # giant clam with pearl
        s = (P['shell'][0], P['shell'][1], P['shell'][2], '#d8b8a0')
        up = cv.E(16, 16, 10.4, 9) & (cv.Y <= 17)
        cv.form(up, (s[0], s[1], s[2]), 2, 1)
        for x in (9, 12, 16, 20, 23):
            cv.line([(x, 17), (16 + (x - 16) * .55, 8)], s[0])
        cv.rect(7, 18, 25, 21, K)
        lo = cv.E(16, 21, 10.4, 6.4) & (cv.Y >= 21)
        cv.form(lo, (s[0], s[1], s[2]), 2, 1)
        cv.fill(cv.E(16, 20, 2.4, 2.2), WHITE[2])
        cv.rect(15, 19, 15, 19, '#ffffff')
        cv.hl(15, 17, 22, WHITE[1])
        out.append(fin(cv, P))
        out.append(fin(pillar(2, RED, bands=GOLD), P))       # lacquer pillar stub

    elif name == 'uminobe':
        cv, rng = new(0)                                     # driftwood logs
        for (y, x0, x1) in ((24, 5, 26), (17, 8, 24)):
            m = capsule(cv, x0, y, 3.6, x1, y, 3.6)
            cv.fill(dil(m), k[0])
            cv.form(m, (k[0], k[1], k[2]), 2, 1)
            e = cv.E(x0, y, 2.2, 3.2)
            cv.form(e, (k[1], k[2], k[3]), 1, 0)
            cv.px(x0, y, k[1])
            cv.hl(x0 + 6, x0 + 10, y - 1, k[0])
            cv.hl(x0 + 12, x0 + 15, y + 1, k[0])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # barrel
        m, t = cyl(cv, k, 16, 28, 8, 15, top=(K, k[0], k[1]))
        for x in (11, 14, 18, 21):
            cv.vl(x, 16, 27, k[0])
        for y in (17, 25):
            b = m & ~t & (cv.Y >= y) & (cv.Y <= y + 1)
            cv.fill(b, IRON[1])
            cv.fill(b & (cv.X < 12) & (cv.Y == y), IRON[3])
        out.append(fin(cv, P))
        cv, rng, m = plain_boulder(2, ramp=STONE)            # tide rock: barnacles + kelp
        c = cover(cv, m, ('#0e2420', '#18382c', '#28503a'), 4, rng)
        for (x, y) in ((10, 23), (14, 25), (20, 22)):
            cv.grid(x, y, "ss\nsa", dict(s=P['shell'][2], a=P['shell'][0]))
        out.append(fin(cv, P))

    elif name == 'yomi':
        cv, rng = new(0)                                     # skull pile
        bone(cv, 5, 26, 14, 28, k)
        skull(cv, 10, 21, k)
        skull(cv, 21, 21, k)
        bone(cv, 20, 14, 27, 12, k)
        skull(cv, 15.5, 12, k, r=4.8)
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # broken pillar with a skull
        s = ('#14101e', '#28223a', '#3e3654', '#5a5072')
        c2 = Cv(32, 32)
        m, t = cyl(c2, s, 15.5, 28, 6, 14)
        cyl(c2, s, 15.5, 29, 7.5, 2)
        c2.fill(c2.PG([(8, 9), (24, 9), (24, 17), (20, 15), (17, 19), (13, 16), (8, 19)]), (0, 0, 0, 0))
        cv.blit(c2, 0, 0)
        cv.line([(13, 20), (14, 24), (13, 27)], s[0])
        skull(cv, 22, 23, k, r=3.4)
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # rib cage
        for i, x in enumerate((8, 12, 16, 20, 24)):
            h = (10, 14, 16, 14, 10)[i]
            cv.line([(x, 27), (x - 1, 27 - h * .6), (x + 2, 27 - h)], k[2])
            cv.line([(x + 1, 27), (x, 27 - h * .6), (x + 3, 27 - h)], k[1])
        cv.rect(6, 26, 27, 27, k[1])
        cv.hl(6, 26, 26, k[2])
        for x in range(8, 27, 3):
            cv.px(x, 27, k[0])
        out.append(fin(cv, P))

    elif name == 'jigoku':
        cv, rng, m = plain_boulder(0)                        # basalt with lava veins
        cv.line([(9, 17), (13, 20), (12, 24), (15, 27)], LAVA[1])
        cv.line([(13, 20), (19, 18), (22, 21)], LAVA[1])
        cv.rect(13, 20, 14, 20, LAVA[2])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # needle spikes
        for (x, w, h, l) in ((4, 6, 13, -1), (21, 6, 15, 2), (14, 6, 11, 1), (9, 7, 21, 0), (16, 6, 17, 1)):
            spire(cv, IRON, x, 28, w, h, l)
        cv.rect(11, 9, 12, 12, RED[2])                       # old blood
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # iron cauldron
        m = cv.E(16, 20, 10, 8) & (cv.Y >= 14)
        cv.form(m, (IRON[0], IRON[1], IRON[2]), 4, 1)
        rim = cv.E(16, 14, 10.4, 3.4)
        cv.fill(dil(rim), IRON[0])
        cv.form(rim, (IRON[1], IRON[2], IRON[3]), 1, 1)
        cv.fill(cv.E(16, 14, 8, 2), LAVA[1])
        cv.fill(cv.E(15, 14, 5, 1.2), LAVA[2])
        cv.rect(13, 13, 15, 13, LAVA[3])
        cv.rect(8, 27, 10, 28, IRON[1])
        cv.rect(22, 27, 24, 28, IRON[0])
        out.append(fin(cv, P))

    elif name in ('takamagahara', 'tsukiyomi') and False:
        pass

    elif name == 'takamagahara':
        cv, rng = new(0)                                     # Kumo-ishi: Wolkenfels mit eingerollten Wolkenschnecken
        lobes = ((10, 22, 6, 5), (21, 22, 7, 5), (15, 14, 6.5, 5.6), (23, 15, 4.4, 3.8), (7, 17, 3.6, 3.2))
        m = np.zeros(cv.a.shape[:2], bool)
        for cx_, cy_, rx_, ry_ in lobes:
            m |= cv.E(cx_, cy_, rx_, ry_)
        m &= cv.Y <= 27
        cv.form(m, (k[0], k[1], k[2]), 3, 1)
        for cx_, cy_, rx_, ry_ in lobes:                     # jede Wolke ein eigener Bausch mit Lichtkuppe
            lit = cv.E(cx_ - rx_ * .25, cy_ - ry_ * .35, rx_ * .6, ry_ * .45) & m
            cv.fill(lit, k[2])
            cv.fill(lit & ~sh(lit, 1, 1), k[3])
            cv.hline([(cx_ + rx_ * math.cos(a), cy_ + ry_ * math.sin(a)) for a in np.linspace(.15, 1.6, 6)], k[0])
        for cx_, cy_, r in ((15, 15, 3.2), (21, 22, 3.4), (9, 22, 2.6)):   # Kumo-Spiralen
            pts = [(cx_ + r * (1 - t * .8) * math.cos(t * 9.4), cy_ + r * .8 * (1 - t * .8) * math.sin(t * 9.4))
                   for t in np.linspace(0, 1, 18)]
            cv.hline(pts, mix(k[0], K, .3))
        cv.a[~m] = 0
        out.append(fin(cv, P))
        out.append(fin(pillar(1, WHITE, bands=GOLD), P))     # white pillar, gold bands
        cv, rng = new(2)                                     # sacred jewel on a cloud cushion
        m = cv.E(12, 24, 5.4, 3.6) | cv.E(20, 24, 5.4, 3.6) | cv.E(16, 22, 5, 3)
        m &= cv.Y <= 27
        cv.form(m, (k[0], k[1], k[2]), 2, 1)
        # Magatama: runder Kopf oben mit Schnurloch, Schweif rollt rechts herum nach unten
        j = ((cv.E(16, 14, 6, 6.4) & (cv.X >= 16)) | cv.E(16, 10.8, 3.2, 3.2)) & ~cv.E(16, 17.2, 3.2, 3.2)
        cv.fill(dil(j), GOLD[0])
        cv.form(j, (GOLD[0], GOLD[1], GOLD[2]), 2, 1)
        cv.fill(cv.E(18.5, 10.5, 1.4, 1.2), GOLD[3])
        cv.fill(cv.E(16, 10.8, 1.1, 1.1), mix(GOLD[0], K, .5))   # Schnurloch
        for i, (cx_, cy_) in enumerate(((10, 24), (21, 24))):
            cv.hline([(cx_ + 2 * (1 - t * .8) * math.cos(t * 9 + i * 3), cy_ + 1.4 * (1 - t * .8) * math.sin(t * 9 + i * 3))
                      for t in np.linspace(0, 1, 14)], k[0])
        out.append(fin(cv, P))

    elif name == 'kawabe':
        cv, rng, m = plain_boulder(0, rx=11, ry=8)           # Flussfels mit Kappa-Opfergurke, nass am Wasserrand
        cover(cv, m, MOSS, 4, rng)
        for (x, y) in ((9, 22), (10, 23.5), (22.5, 24), (23, 25.5), (13, 26.5)):
            cv.hpx(x, y, WATER[3])
        cu = capsule(cv, 12, 14.5, 1.7, 19, 13.5, 1.5)          # Gurke: Lieblingsspeise der Kappa
        cv.fill(dil(cu), K)
        cv.form(cu, ('#1c4a24', '#2e7a34', '#5aa848'), 1, 1)
        for x in (13.5, 15.5, 17.5):
            cv.hpx(x, 14, '#9ad070')
        cv.hpx(19.5, 12.5, '#c8b040')
        out.append(fin(cv, P))
        for x0, x1, y in ((3, 29, 29), (6, 26, 30.5)):       # Wellenringe um den Fuß
            for i in range(int((x1 - x0) * 2)):
                x = x0 + i * .5
                if (i // 3) % 2 == 0 and not cv.m[int(y * cv.ss), int(x * cv.ss)]:
                    cv.hpx(x, y, WATER[2] if y < 30 else WATER[1])

        cv, rng = new(1)                                     # Gama-Röhricht im Seichtwasser, ein Glühwürmchen
        pool = cv.E(16, 27.5, 11, 2.6)
        cv.fill(pool, WATER[1])
        cv.fill(pool & ~sh(pool, 0, 2 * cv.ss), WATER[0])
        for (x0, x1, h, d) in ((10, 6, 15, 1), (13, 12, 21, 0), (18, 19, 23, 1), (21, 25, 17, 0), (15, 16, 12, 1),
                               (23, 22, 10, 0), (8, 5, 9, 0)):
            bl = cv.PG([(x0 - 1, 28), (x1, 28 - h), (x0 + 1.5, 28)])
            cv.fill(dil(bl), K)
            cv.fill(bl, MOSS[2] if d else MOSS[1])
            cv.hline([(x0 - .5, 27), (x1, 29 - h)], MOSS[3] if d else MOSS[2])
        for (x, y) in ((12, 5), (18, 3), (24, 9)):           # Kolben mit Lichtkante und Spitze
            hd = capsule(cv, x + .5, y + 1, 1.2, x + .5, y + 5, 1.2)
            cv.fill(dil(hd), K)
            cv.form(hd, ('#2e1a16', '#5a3824', '#8a5a32'), 1, 1)
            cv.hline([(x + .5, y - 1.5), (x + .5, y - .2)], MOSS[2])
        for (x, y) in ((6, 28), (25, 27.5), (16, 29)):
            cv.hline([(x, y), (x + 2, y)], WATER[3])
        out.append(fin(cv, P, shadow=False))
        cv.fill(cv.E(27, 8, .9, .9), '#6a8a2a')              # Hotaru
        cv.hpx(27, 8, '#e8f070')
        cv.hpx(26.5, 7.5, '#f8ffc0')

        cv, rng = new(2)                                     # Suijin-Stein: Flussgott, Shimenawa, Gurke und Sake
        m = cv.PG([(10, 28), (9, 15), (11, 7), (15, 4), (20, 5), (23, 10), (23, 20), (24, 28)])
        cv.fill(dil(m), K)
        cv.form(m, (k[1], k[2], k[3]), 3, 1)
        cv.line([(20, 7), (21, 12), (20, 15)], k[1])
        for gi, g in enumerate(SUIJIN):                      # eingemeißelt: 水神
            for j, row in enumerate(g):
                for i2, ch in enumerate(row):
                    if ch == 'x':
                        x, y = 16 - len(row) / 4 + i2 * .5, 12.5 + gi * 4.5 + j * .5
                        cv.hpx(x + .5, y + .5, k[3])
                        cv.hpx(x, y, k[0])
        rope(cv, 8, 24, 9, 1.2, shide=(8, 22))
        cover(cv, m & (cv.Y >= 24), MOSS, 2, rng)
        cu = capsule(cv, 6, 27, 1.3, 10.5, 26.5, 1.2)
        cv.fill(dil(cu), K)
        cv.form(cu, ('#1c4a24', '#2e7a34', '#5aa848'), 1, 1)
        cv.rect(23, 26, 26, 27, PAPER[2])                    # Sakazuki mit Rand
        cv.hl(23, 26, 26, PAPER[3])
        cv.hpx(24.5, 26, RED[2])
        cv.hpx(25, 26, RED[2])
        out.append(fin(cv, P))

    elif name == 'yashiki':
        lac = ('#140c14', '#2a1820', '#46282a', '#663a30')  # dunkles Kiri-Holz, rot lackiert gealtert
        cv, rng = new(0)                                     # Tansu: Eisenbeschläge, Ringgriffe, oberste Lade offen
        box(cv, lac, 6, 7, 26, 28, top=3)
        for y in (13, 19, 24):
            cv.hl(7, 23, y, lac[0])
            cv.hl(7, 23, y + 1, lac[2])
        cv.vl(15, 19, 24, lac[0])
        cv.rect(7, 10, 23, 12, K)                            # die Lade steht einen Spalt offen ...
        cv.hl(7, 23, 10, lac[0])
        for x in (12, 18):                                   # ... und etwas schaut heraus
            cv.hpx(x, 11, GOLD[3])
            cv.hpx(x + .5, 11, GOLD[2])
            cv.hpx(x, 11.5, GOLD[1])
        for (x, y) in ((6, 10), (23, 10), (6, 25), (23, 25)):     # Kanamono an den Ecken
            cv.rect(x, y, x + 2, y + 2, IRON[2])
            cv.hpx(x + .5, y + .5, IRON[3])
            cv.hpx(x + 2, y + 2, IRON[0])
        for (x, y) in ((10.5, 16), (19.5, 16), (10.5, 21.5), (19.5, 21.5), (15.5, 26)):
            cv.hline([(x - 1.5, y - .5), (x + 1.5, y - .5)], IRON[1])     # Warabite-Bügelgriff
            cv.hline([(x - 1.5, y), (x - 1, y + .5), (x + 1, y + .5), (x + 1.5, y)], IRON[2])
            cv.hpx(x - 1, y + .5, IRON[3])
        out.append(fin(cv, P))

        cv, rng = new(1)                                     # Andon: kalt brennt darin ein Totenlicht
        fr = ('#120a10', '#2a1a1a', '#4a3024', '#6a4a30')
        pap = cv.R(10, 8, 22, 24)
        cv.fill(pap, '#6a6478')
        glow = cv.E(16, 17, 6, 7) & pap
        cv.fill(glow, '#7a7aa8')
        cv.fill(cv.E(16, 18, 3.6, 4.4) & pap, ONIBI[2])
        cv.fill(cv.E(16, 18.5, 1.6, 2.4) & pap, ONIBI[3])
        cv.fill(pap & (cv.X >= 19.5), mix('#6a6478', K, .35))
        for x in (10, 16, 22):
            cv.vl(x, 7, 28, fr[2] if x < 22 else fr[1])
        for y in (7, 13, 19, 24):
            cv.hl(9, 23, y, fr[2])
            cv.hl(10, 22, y + 1, fr[0]) if y < 24 else None
        cv.hl(9, 23, 7, fr[3])
        cv.rect(9, 25, 23, 26, fr[2])
        cv.hl(9, 23, 25, fr[3])
        for x in (9, 23):
            cv.vl(x, 26, 28, fr[1])
        tear = cv.PG([(17, 9), (20, 9.5), (19, 11), (19.5, 12.5), (18, 11.5)])
        cv.fill(dil(tear) & pap & ~tear, PAPER[3])
        cv.fill(tear, K)
        cv.hline([(17, 9), (16.5, 10.5)], PAPER[3])           # loser Papierfetzen
        cv.hpx(19, 11, ONIBI[1])
        out.append(fin(cv, P))

        cv, rng = new(2)                                     # Byōbu mit Blattgold, Kiefer und roter Sonne; eine Hand am Rand
        g = (GOLD[0], GOLD[1], GOLD[2], GOLD[3])
        panels = ((4, 11, 9, 6), (11, 18, 6, 9), (18, 25, 9, 6))
        for i, (x0, x1, ya, yb) in enumerate(panels):
            pm = cv.PG([(x0, ya), (x1, yb), (x1, yb + 19), (x0, ya + 19)])
            cv.fill(pm, g[2] if i % 2 == 0 else g[1])
            cv.fill(pm & (cv.Y > (ya + yb) / 2 + 13), g[1] if i % 2 == 0 else g[0])
            cv.line([(x0, ya), (x1, yb)], K)
            cv.line([(x0, ya + 19), (x1, yb + 19)], K)
            cv.vl(x0, min(ya, yb), max(ya, yb) + 19, K)
            cv.hline([(x0 + .5, ya + 1), (x1 - .5, yb + 1)], g[3] if i % 2 == 0 else g[2])
        cv.vl(25, 6, 25, K)
        cv.line([(9, 25), (9, 19), (10, 15), (12, 13)], '#2a1a14')     # Kiefernstamm in Tusche
        cv.line([(10, 15), (7, 14)], '#2a1a14')
        for (x, y) in ((6, 13), (11, 12), (14, 13), (8, 17)):
            cv.grid(x - 1, y - 1, "aaa\n.a.", dict(a='#1c3a2a'))
        cv.line([(13, 20), (16, 17), (19, 21), (22, 18)], '#3a2a20')     # ferne Berge
        sun = cv.E(21.5, 12.5, 2, 2)
        cv.fill(sun, RED[2])
        cv.hpx(21, 12, RED[3])
        for y in (24.5, 25):                                 # Goldwolken
            cv.hline([(5, y + 1), (9, y)], g[3])
        cv.hline([(19, 25.5), (24, 24)], g[3])
        out.append(fin(cv, P))
        for y in (8, 9.5, 11):                               # bleiche Finger greifen um die Kante
            cv.hline([(24.5, y), (26.5, y)], '#c8c0c8')
            cv.hpx(26.5, y + .5, '#8a7a88')
            cv.hpx(24, y, '#6a2a3a')

    elif name == 'oeyama':
        cv, rng, m = plain_boulder(0, rx=11, ry=8)           # Kanabō der Oni, in den Fels gerammt
        for path in ([(15, 17), (12, 20), (12.5, 23)], [(17, 18), (20, 21)]):     # Einschlagrisse
            cv.hline(path, K)
            cv.hline([(x + .5, y + .5) for x, y in path], k[2])
        kb = capsule(cv, 15.5, 18, 1.4, 21.5, 2.5, 2.7)
        cv.fill(dil(kb), K)
        cv.form(kb, IRON[:3], 1, 1)
        cv.hline([(15.5, 17), (20.5, 3.5)], IRON[3])
        for i in range(6):                                   # Eisennieten, versetzt
            t = .12 + i * .16
            x, y = 15.5 + 6 * t, 18 - 15.5 * t
            for sx in ((-1.5, 1.3) if i % 2 else (0,)):
                cv.fill(cv.E(x + sx + .3, y + .3, .7, .7), K)
                cv.fill(cv.E(x + sx, y, .55, .55), '#b0b8d0')
        cv.fill(cv.E(16, 17.5, 3, 1.2) & ~kb, k[0])        # Splitter am Einschlag
        out.append(fin(cv, P))

        cv, rng = new(1)                                     # Komodaru: Strohfass mit Seil, Oni-Mon und Schöpfkelle
        m, t = cyl(cv, STRAW, 16, 28, 9, 15, top=WOOD[1:])
        side = m & ~t
        for x in range(8, 25, 2):                            # Strohhalme
            cv.fill(side & (cv.X >= x) & (cv.X < x + .5), STRAW[1])
        for y in (17, 25):                                   # Seilbänder
            bm = side & (cv.Y >= y) & (cv.Y < y + 1.5)
            cv.fill(bm, STRAW[3])
            cv.fill(bm & (cv.Y >= y + 1), STRAW[1])
            for x in range(8, 25, 2):
                cv.hpx(x, y + .5, STRAW[0])
        lab = cv.R(12, 18.5, 20, 24.5)                       # Etikett: schwarz mit rotem Oni-Mon
        cv.fill(lab, '#1a1018')
        cv.fill(cv.E(16, 21.5, 2.4, 2.4), RED[2])
        cv.fill(cv.E(16, 21.5, 1.2, 1.2), GOLD[3])
        for sx in (-1, 1):
            cv.hline([(16 + sx * 1, 19.6), (16 + sx * 2.2, 18.6)], GOLD[3])     # Hörner im Mon
        for y in (14.5, 15.5):                               # Holzdeckel mit Fugen
            cv.hline([(9, y), (23, y)], WOOD[0]) if y < 15 else None
        cv.hline([(10, 12.5), (22, 12.5)], WOOD[0])
        h = capsule(cv, 10, 11.5, .5, 25, 7, .5)             # Hishaku-Kelle quer über dem Deckel
        cv.fill(dil(h), K)
        cv.fill(h, WOOD[3])
        cup = cv.E(25.5, 7.5, 2, 1.6)
        cv.fill(dil(cup), K)
        cv.form(cup, WOOD[1:], 1, 1)
        cv.fill(cv.E(25.5, 7, 1.2, .6), '#c8b8a0')         # Sake darin
        out.append(fin(cv, P))

        cv, rng = new(2)                                     # Knochenhaufen der Ōeyama-Bande, obenauf eine Oni-Maske
        heap = cv.E(16, 27, 12, 5) & (cv.Y <= 28)
        cv.fill(dil(heap), K)
        cv.form(heap, BONE[:3], 2, 1)
        for (x0, y0, x1, y1) in ((6, 26, 13, 23), (18, 24, 26, 27), (10, 27, 17, 25), (20, 23, 24, 21)):
            bone(cv, x0, y0, x1, y1, BONE)
        skull(cv, 8.5, 22, BONE, r=3)
        skull(cv, 24, 22.5, BONE, r=2.8)
        face = cv.E(16, 15, 5.4, 6.2) & (cv.Y <= 21)          # Hannya-artige Oni-Maske, leicht schräg aufgelegt
        horns = capsule(cv, 12, 10, 1.3, 9.5, 4, .4) | capsule(cv, 20, 10, 1.3, 22.5, 4, .4)
        cv.fill(dil(face | horns), K)
        cv.form(horns, BONE[1:], 1, 1)
        cv.form(face, RED, 2, 1)
        cv.fill(face & (cv.Y < 10.5), '#1a1018')           # Haaransatz
        for sx in (-1, 1):
            br = cv.PG([(16 + sx * 1, 12.5), (16 + sx * 4.2, 11), (16 + sx * 4, 12.5)])
            cv.fill(br, K)
            cv.fill(cv.E(16 + sx * 2.3, 14.2, 1.1, .8), GOLD[3])
            cv.hpx(16 + sx * 2.3, 14.2, K)
        cv.fill(cv.R(13, 18, 19, 19.5), K)                  # Maul mit Hauern
        for x in (13.5, 18):
            cv.hline([(x, 18), (x, 16.5)], BONE[3])
        cv.hline([(14.5, 19), (17.5, 19)], BONE[3])
        cv.hline([(15.5, 15), (16.5, 16)], RED[0])
        out.append(fin(cv, P))

    elif name == 'shinkai':
        cv, rng = new(0)                                     # Riesenmuschel: die Hamaguri atmet ein Shinkirō aus
        lo = cv.E(16, 23, 11, 5.2) & (cv.Y >= 21)
        up = cv.E(16, 21, 11, 7.5) & (cv.Y <= 21) & ~cv.R(0, 0, 32, 13)
        cv.fill(dil(lo | up), K)
        cv.form(up, (k[1], k[2], k[3]), 2, 1)
        cv.form(lo, (k[0], k[1], k[2]), 2, 1)
        for x in range(8, 26, 3):                            # Rippen
            cv.hline([(16 + (x - 16) * .4, 15), (x, 20)], k[1])
            cv.hline([(x, 22.5), (16 + (x - 16) * .9, 27)], k[0])
        gap = cv.E(16, 21.6, 9.5, 1.3)
        cv.fill(gap, K)
        cv.fill(cv.E(16, 21.6, 1.8, 1.4), GLOW[3])         # Perle
        cv.hpx(15.5, 21, '#ffffff')
        cv.fill(cv.E(16, 21.6, 6, .6) & ~cv.E(16, 21.6, 2, 2), GLOW[1])
        out.append(fin(cv, P))
        for i, (x, y) in enumerate(((16, 11), (15, 9), (17, 7), (16, 5), (14, 3.5), (19, 4))):   # Spiegelbild-Dunst
            cv.hpx(x, y, GLOW[2] if i < 3 else GLOW[1])
            cv.hpx(x + .5, y - .5, GLOW[1])

        cv, rng = new(1)                                     # Sango-Koralle mit Leuchtfischen
        rc = ('#3a0e2a', '#7a1a3a', '#b03a4a', '#e07a6a')
        br = np.zeros_like(cv.m)
        for (x0, y0, x1, y1, r) in ((16, 28, 15, 15, 1.6), (15, 15, 10, 8, 1), (15, 17, 21, 9, 1.1), (21, 9, 24, 5, .7),
                                    (12, 11, 8, 13, .7), (19, 12, 18, 6, .7), (16, 22, 24, 17, 1), (24, 17, 26, 13, .6),
                                    (15, 23, 7, 19, .9), (7, 19, 6, 15, .6)):
            br |= capsule(cv, x0, y0, r + .3, x1, y1, r)
        cv.fill(dil(br), K)
        cv.form(br, rc[:3], 1, 1)
        for (x, y) in ((10, 8), (24, 5), (18, 6), (8, 13), (26, 13), (6, 15)):
            cv.hpx(x, y, rc[3])
        rock = cv.E(16, 28, 5, 2) & (cv.Y <= 28)
        cv.form(rock, k[:3], 1, 1)
        out.append(fin(cv, P))
        for (x, y, d) in ((5, 8, 1), (26, 21, -1)):          # Leuchtfische
            f = cv.E(x, y, 1.6, .9) | cv.PG([(x - d * 1.4, y), (x - d * 2.8, y - 1), (x - d * 2.8, y + 1)])
            cv.fill(f, GLOW[2])
            cv.fill(f & (cv.Y > y + .2), GLOW[1])
            cv.hpx(x + d * .8, y - .2, K)
            cv.hpx(x - d * .2, y - .5, GLOW[3])

        cv, rng = new(2)                                     # versunkene Tōrō-Steinlaterne mit Seepocken, Licht noch an
        st = k
        base = cv.R(11, 25, 21, 28)
        post = cv.R(14, 18, 18, 25)
        fbox = cv.R(11.5, 11, 20.5, 17)
        roof = cv.PG([(7, 11), (10, 8), (16, 5.5), (22, 8), (25, 11), (23, 10.5), (9, 10.5)])
        cap = cv.E(16, 5, 1.4, 1.6)
        sil = base | post | fbox | roof | cap | cv.R(12, 17, 20, 18)
        cv.fill(dil(sil), K)
        for part in (base, post, fbox, cv.R(12, 17, 20, 18), roof, cap):
            cv.form(part, (st[0], st[1], st[2]), 1, 1)
        cv.fill(cv.R(13.5, 12.5, 18.5, 15.5), K)            # Lichtfenster
        cv.fill(cv.E(16, 14, 2, 1.4), GLOW[2])
        cv.fill(cv.E(16, 14, 1, .7), GLOW[3])
        cv.hline([(9, 10), (23, 10)], st[3])
        for (x, y) in ((12, 26), (19.5, 25.5), (14.5, 20), (21, 9), (8.5, 10.5), (17.5, 22.5)):   # Seepocken
            cv.hpx(x, y, BONE[3])
            cv.hpx(x + .5, y + .5, BONE[1])
        for (x0, h, s) in ((10, 9, 1), (22, 12, -1), (20, 6, 1)):   # Seetang windet sich hoch
            pts = [(x0 + math.sin(i * .9) * s, 28 - i) for i in range(h)]
            cv.hline(pts, MOSS[2])
            cv.hline([(x + .5, y) for x, y in pts], MOSS[1])
        out.append(fin(cv, P))

    elif name == 'enma_cho':
        cv, rng = new(0)                                     # Bronzenes Kohlebecken auf drei Krallenfüßen
        for (x0, x1) in ((11, 8), (21, 24), (16, 16)):
            leg = capsule(cv, x0, 16, 1.1, x1, 26.5, .9)
            cv.fill(dil(leg), K)
            cv.form(leg, BRONZE[:3], 1, 1)
            cv.fill(cv.E(x1, 27, 1.8, 1), BRONZE[2])        # Klaue
            for dx in (-1.2, 0, 1.2):
                cv.hpx(x1 + dx, 27.6, BRONZE[3])
        bowl = cv.E(16, 13.5, 9.5, 5.2) & (cv.Y >= 12.5)
        cv.fill(dil(bowl), K)
        cv.form(bowl, BRONZE[:3], 2, 1)
        for x in (10, 13, 16, 19, 22):                       # Rankenmuster
            cv.hpx(x, 15.5, BRONZE[3])
            cv.hpx(x + .5, 16, BRONZE[0])
        cv.fill(cv.E(16, 16, 2, 1.6), K)                     # Oni-Fratze vorn
        cv.hpx(15.5, 15.6, LAVA[3]); cv.hpx(16.5, 15.6, LAVA[3])
        rim = cv.E(16, 12.5, 9.6, 2.2) & ~cv.E(16, 12.3, 8.6, 1.4)
        cv.fill(rim, GOLD[2])
        cv.fill(rim & (cv.Y > 12.8), GOLD[1])
        cv.fill(cv.E(16, 12.3, 8.4, 1.4), LAVA[1])           # Glut
        cv.fill(cv.E(16, 12.3, 5, .8), LAVA[2])
        for (x, y) in ((9.5, 6), (15, 4), (19.5, 6.5)):
            flame(cv, x, y)
        for (x, y) in ((12, 3), (20, 2), (17, 1)):           # Funken
            cv.hpx(x, y, LAVA[3])
        out.append(fin(cv, P))

        cv, rng = new(1)                                     # Jōhari no Kagami: der Spiegel, der alle Taten zeigt
        box(cv, k, 8, 24, 24, 28, top=2)
        for x in (10.5, 21.5):                               # Ständer
            post = cv.R(x - .8, 17, x + .8, 24)
            cv.fill(dil(post), K)
            cv.form(post, RED[:3], 1, 1)
        halo = cv.E(16, 12, 9, 9.5) & (cv.Y <= 19)           # Flammenkranz um den Spiegel
        for i in range(9):
            ang = math.pi * (1.1 + i * .1)
            tx, ty = 16 + math.cos(ang) * 11, 12 + math.sin(ang) * 11.5
            halo |= capsule(cv, 16 + math.cos(ang) * 8, 12 + math.sin(ang) * 8, 1.6, tx, ty, .3)
        cv.fill(dil(halo), K)
        cv.form(halo, GOLD[:3], 1, 1)
        frame = cv.E(16, 12, 7, 7)
        cv.fill(frame, RED[1])
        cv.fill(frame & ~sh(frame, 1, 1), RED[3])
        glass = cv.E(16, 12, 5.6, 5.6)
        cv.fill(dil(glass) & frame, K)
        cv.form(glass, ('#3a1a2a', '#6a2a3a', '#b05a4a'), 2, 1)
        soul = cv.E(16, 11, 1.5, 1.6) | (cv.E(16, 15, 2.6, 2.6) & (cv.Y <= 16.5))   # Seele im Spiegel
        cv.fill(soul & glass, '#e8c8b8')
        cv.fill(soul & glass & ~sh(soul, -1, 0), '#c09a90')
        cv.hline([(12.5, 8.5), (14, 7.5)], '#ffe8d0')        # Glanz
        cv.hpx(16, 4.5, GOLD[3])
        cv.fill(cv.E(16, 19.2, 2.2, 1), GOLD[2])
        out.append(fin(cv, P))

        cv, rng = new(2)                                     # Nintōjō: Enmas Stab mit Miru-me und Kagu-hana
        base = cv.E(16, 26.5, 7, 2.5) | cv.R(10, 23, 22, 26.5)
        cv.fill(dil(base), K)
        cv.form(base, k[:3], 2, 1)
        cv.fill(cv.E(16, 23, 6, 1.6), k[3])
        staff = capsule(cv, 16, 23, 1.2, 16, 12, 1)
        cv.fill(dil(staff), K)
        cv.form(staff, WOOD[1:], 1, 1)
        for y in (21, 17):
            cv.fill(staff & (cv.Y >= y) & (cv.Y < y + .8), GOLD[2])
        lotus = cv.E(16, 12, 6, 2)                           # Lotussockel
        cv.fill(dil(lotus), K)
        cv.form(lotus, GOLD[:3], 1, 1)
        for x in (11.5, 14, 16.5, 19):
            cv.hline([(x, 12.5), (x + 1, 11)], GOLD[0])
        for (cx, skin, side) in ((12.4, '#d8c8b8', -1), (19.6, '#9a3a2a', 1)):
            head = cv.E(cx, 7.2, 3.2, 3.7)
            hair = cv.E(cx, 6, 3.6, 3.4) & ~cv.E(cx, 7.6, 2.5, 3)
            if side < 0:                                     # Miru-me: weißes Gesicht, langes schwarzes Haar
                hair |= cv.R(cx - 3.5, 6, cx - 2.3, 11) | cv.R(cx + 2.3, 6, cx + 3.5, 11)
            else:                                            # Kagu-hana: roter Zornkopf mit Haarknoten
                hair |= cv.E(cx, 3, 1.4, 1.3)
            cv.fill(dil(head | hair), K)
            cv.form(head, (mix(skin, K, .45), skin, mix(skin, '#ffffff', .2)), 1, 1)
            cv.fill(hair, '#1a1018')
            cv.fill(hair & ~sh(hair, 1, 1), '#3a2a40')
            for sx in (-1, 1):
                ex = cx + sx * 1.3
                cv.hline([(ex - .8, 6 - sx * side * .4), (ex + .8, 6 + sx * side * .4)], K)   # Brauen
                cv.hpx(ex - .5, 7, '#f0e8d8'); cv.hpx(ex, 7, '#f0e8d8')
                cv.hpx(ex - .5 + side * .5 * 0, 7, K) if side > 0 else cv.hpx(ex, 7, '#b02020')
            if side < 0:
                cv.hline([(cx - .5, 9.5), (cx + .5, 9.5)], '#a02030')
            else:
                cv.fill(cv.E(cx + .3, 8.2, 1, 1.1), mix(skin, '#ffffff', .2))   # die große, witternde Nase
                cv.hpx(cx + .8, 8.8, K)
                cv.hline([(cx - 1, 10), (cx, 9.6), (cx + 1, 10)], K)
        out.append(fin(cv, P))

    elif name == 'tsukiyomi':
        cv, rng, m = plain_boulder(0, rx=8, ry=3.5, by=29)  # Tsuki no Katsura: der silberne Baum auf dem Mond
        trunk = (capsule(cv, 16, 27, 2, 15, 15, 1.1) | capsule(cv, 15.5, 18, .7, 9, 12, .45) | capsule(cv, 15.5, 17, .7, 22, 10.5, .45)
                 | capsule(cv, 15, 15, .6, 14, 7, .4) | capsule(cv, 16.5, 27, .6, 21, 28, .4) | capsule(cv, 15, 27, .6, 10.5, 28.2, .4))
        cv.fill(dil(trunk), K)
        cv.form(trunk, SILVER[:3], 1, 1)
        cv.hline([(16.6, 26), (16, 18)], SILVER[0])
        crown = np.zeros_like(cv.m)
        for (cx, cy, r) in ((7.5, 10.5, 2.6), (11.5, 7, 3), (16, 4.8, 3.2), (20.5, 6.8, 3), (24.5, 10, 2.6), (14, 10.5, 2.2), (19, 11, 2.2)):
            crown |= cv.E(cx, cy, r, r * .75)
        crown &= ~(cv.E(16, 13.5, 4, 2) & ~trunk)
        cv.fill(dil(crown), K)
        cv.form(crown, ('#3a4870', '#6a7cb0', '#a8b8e0'), 2, 1)
        for i in range(18):                                  # herzförmige Katsura-Blätter, mondhell
            x, y = 5 + rng.random() * 22, 2 + rng.random() * 10
            if crown[int(y * cv.ss), int(x * cv.ss)]:
                cv.hpx(x, y, '#e0e8ff'); cv.hpx(x + .5, y, '#e0e8ff'); cv.hpx(x + .25, y + .5, '#c8d4f4')
        for (x, y) in ((6, 15), (24, 16), (13, 19)):         # fallende Blätter
            cv.hpx(x, y, '#c8d4f4')
        out.append(fin(cv, P))

        cv, rng = new(1)                                     # Tsukimi: Sanbō mit Dango-Pyramide und Susuki-Gras
        for (x0, y0, x1, y1) in ((22, 27, 20, 6), (23, 27, 25, 8), (22, 27, 27.5, 12)):
            g = capsule(cv, x0, y0, .45, x1, y1, .3)
            cv.fill(dil(g), K)
            cv.fill(g, STRAW[2])
            plume = capsule(cv, x1, y1, .9, x1 + (x1 - x0) * .15, y1 + 4.5, .5)
            cv.fill(dil(plume), K)
            cv.form(plume, (STRAW[2], '#d8ccb0', '#f0ecdc'), 1, 1)
        box(cv, ('#3a2a20', '#7a5a38', '#a8844c', '#d0b070'), 6, 21, 20, 28, top=2)
        win = cv.E(13, 25.5, 2.2, 1.8) & (cv.Y <= 26.5)        # Fenster im Sanbō-Sockel
        cv.fill(win, K)
        tray = cv.R(5, 19, 21, 21)
        cv.fill(dil(tray), K)
        cv.form(tray, ('#7a5a38', '#a8844c', '#d0b070'), 1, 1)
        for (row, n) in ((17, 4), (13.5, 3), (10, 2), (6.5, 1)):
            for i in range(n):
                cx = 13 - (n - 1) * 1.85 + i * 3.7
                d = cv.E(cx, row, 1.9, 1.75)
                cv.fill(dil(d), K)
                cv.form(d, ('#a8acc8', '#e0e0ea', '#ffffff'), 1, 1)
        out.append(fin(cv, P))

        cv, rng = new(2)                                     # Usu und Kine des Mondhasen, Mochi dampft noch
        w = ('#1e1a2c', '#3a3448', '#585268', '#7a7488')
        m, t = cyl(cv, w, 14, 28, 8, 12, top=(w[0], w[1], w[2]))
        side = m & ~t
        for x in range(8, 21, 3):                            # Holzmaserung und Eisenband
            cv.fill(side & (cv.X >= x) & (cv.X < x + .5) & (cv.Y > 19), w[0])
        band = side & (cv.Y >= 22) & (cv.Y < 23.5)
        cv.fill(band, IRON[2]); cv.fill(band & (cv.Y >= 23), IRON[1])
        cv.fill(cv.E(14, 16, 6, 2.6), K)
        mochi = cv.E(14, 15.3, 4.8, 2.2)
        cv.form(mochi, ('#b0b4cc', '#e4e6f0', '#ffffff'), 1, 1)
        cv.hpx(12, 14.5, '#ffffff')
        for (x, y) in ((12, 11), (15, 9.5), (13, 8)):        # Dampf
            cv.hpx(x, y, WHITE[2])
        kine = capsule(cv, 22, 27.5, .7, 26.5, 10, .7)
        cv.fill(dil(kine), K)
        cv.form(kine, WOOD[1:], 1, 1)
        hm = capsule(cv, 23, 7.5, 2.4, 30, 10.5, 2.4)
        cv.fill(dil(hm), K)
        cv.form(hm, ('#3a2a20', '#7a5a38', '#a8844c'), 1, 1)
        cv.fill(cv.E(23, 7.5, 1.6, 1.6) & hm, '#c8a870')     # Hirnholz
        out.append(fin(cv, P))

    elif name == 'yomi_oku':
        cv, rng = new(0)                                     # Ōkamuzumi: der Pfirsichbaum, dessen Früchte die Shikome vertrieben
        root = cv.E(16, 27.5, 7, 2) & (cv.Y <= 28.5)
        cv.fill(dil(root), K)
        cv.form(root, VIOLET[:3], 1, 1)
        tr = (capsule(cv, 16, 27, 2, 14.5, 17, 1.2) | capsule(cv, 14.5, 18, .9, 8, 10, .5) | capsule(cv, 15, 17, .9, 22, 9, .5)
              | capsule(cv, 14.6, 17, .7, 15.5, 6, .4) | capsule(cv, 10, 12.5, .4, 6, 13, .3) | capsule(cv, 20, 11.5, .4, 25, 13.5, .3)
              | capsule(cv, 15.4, 9, .35, 12, 4.5, .25) | capsule(cv, 21, 10, .35, 23.5, 5, .25))
        cv.fill(dil(tr), K)
        cv.form(tr, ('#140a14', '#2a1824', '#46303a'), 1, 1)
        for (x, y) in ((9, 10), (12.5, 5), (22.5, 6), (24.5, 13), (17, 7.5)):   # verdorrte Blüten
            cv.hpx(x, y, '#8a5a78'); cv.hpx(x + .5, y + .5, '#5a3a58')
        for (x, y) in ((7, 14.5), (18, 10.5), (23, 15)):                         # drei leuchtende Götterpfirsiche
            p = cv.E(x, y, 1.9, 1.8)
            cv.fill(dil(p), K)
            cv.form(p, ('#a0405a', '#f08a8a', '#ffd0b8'), 1, 1)
            cv.hline([(x, y - 1.6), (x + .3, y + 1)], '#c05a6a')
            cv.hpx(x + 1, y - 2, '#3a6a3a'); cv.hpx(x + 1.5, y - 2.2, '#5a8a4a')
        for (x, y) in ((11, 22), (21, 24)):                  # Totenfeuer am Wurzelwerk
            cv.grid(x, y, ".a\nab", dict(a=ONIBI[1], b=ONIBI[2]))
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # Yomotsu-hegui: Herd der Unterwelt mit Eisentopf
        clay = ('#1e1018', '#3a2228', '#56362e', '#74503c')
        m = cv.R(6, 15, 26, 28) | cv.E(16, 15, 10, 3)
        cv.form(m, (clay[0], clay[1], clay[2]), 3, 1)
        mouth = (cv.R(12, 22, 20, 28) | cv.E(16, 22, 4, 3)) & (cv.Y <= 28)
        cv.fill(dil(mouth) & m, clay[0])
        cv.fill(mouth, K)
        cv.fill(cv.E(16, 27, 3.4, 2.2) & mouth, ONIBI[1])
        cv.fill(cv.E(16, 27.5, 1.8, 1.2) & mouth, ONIBI[3])
        cv.grid(15, 23, ".a\naa", dict(a=ONIBI[0]))
        cv.hl(7, 25, 17, clay[3])
        pot = cv.E(16, 11, 7, 4.6) & (cv.Y >= 8)
        cv.fill(dil(pot), K)
        cv.form(pot, IRON[:3], 2, 1)
        cv.fill(cv.E(16, 8, 6.4, 1.6), IRON[0])
        cv.fill(cv.E(16, 8.2, 5, 1), VIOLET[2])                  # was darin brodelt, isst man besser nicht
        for (x, y) in ((12, 5), (18, 3), (21, 6)):
            cv.grid(x, y, ".o\no.", dict(o=ONIBI[0]))
        out.append(fin(cv, P))
        cv, rng, m = plain_boulder(2, rx=12, ry=10)          # Chibiki-iwa: der Fels, der Yomi verschließt
        rope(cv, 4, 28, 13, 3.4, shide=(9, 16, 23))
        cv.a[~dil(dil(m))] = 0
        out.append(fin(cv, P))
    return out


# ------------------------------------------------------------------ wall decorations
def niche(cv, x0, x1, y0=6, c=K):
    cv.rect(x0, y0, x1, 14, c)
    cv.px(x0, y0, cv.get(x0 - 1, y0))
    cv.px(x1, y0, cv.get(x1 + 1, y0))


def wall_decos(name, base):
    P = BIOMES[name]
    w0, w1, w2, w3 = P['w0'], P['w1'], P['w2'], P['w3']
    k = (P['k0'], P['k1'], P['k2'], P['k3'])
    a, b = base.copy(), base.copy()

    if name == 'chikurin':
        rope(a, 1, 30, 6, 2.2, shide=(6, 14, 23))
        niche(b, 10, 22, 6)                                  # hidden jizo-lantern in a gap
        s = STONE
        b.rect(13, 13, 19, 14, s[1])
        b.rect(14, 9, 18, 12, s[1])
        b.vl(14, 9, 12, s[2])
        b.rect(16, 10, 17, 11, GOLD[2])
        b.px(16, 10, GOLD[3])
        b.rect(12, 7, 20, 8, s[2])
        b.hl(12, 20, 8, s[0])
        b.rect(15, 5, 17, 6, s[1])
    elif name == 'inari':
        dark = '#16121e'
        niche(a, 9, 22, 6)                                   # torii gate
        a.rect(2, 1, 29, 2, dark)
        a.rect(1, 0, 3, 1, dark)
        a.rect(28, 0, 30, 1, dark)
        a.rect(3, 3, 28, 4, RED[2])
        a.hl(3, 28, 3, RED[3])
        a.rect(5, 7, 26, 8, RED[2])
        a.hl(5, 26, 8, RED[1])
        for x in (7, 22):
            a.rect(x, 5, x + 2, 13, RED[2])
            a.vl(x, 5, 13, RED[3])
            a.vl(x + 2, 5, 13, RED[1])
            a.rect(x, 13, x + 2, 14, dark)
        a.rect(15, 5, 16, 6, GOLD[1])
        niche(b, 9, 22, 6)                                   # kitsune in an alcove
        s = STONE
        b.rect(11, 13, 21, 14, s[1])
        b.hl(11, 21, 13, s[2])
        b.grid(11, 6, "..a.a.....\n.aaaa.....\naabaa..aa.\n.aabba.aba\n..rrbbaaba\n..abbbbba.\n..ababbba.",
               dict(a=s[2], b=s[3], r=RED[2]))
        b.px(12, 8, K)
    elif name == 'obakedera':
        for (x, y, h) in ((4, 6, 6), (10, 7, 5), (17, 5, 7), (24, 7, 6)):   # ofuda talismans
            a.rect(x, y, x + 3, y + h, PAPER[1])
            a.vl(x, y, y + h, PAPER[2])
            a.vl(x + 2, y + 1, y + h - 2, RED[2])
            a.px(x + 1, y + 2, RED[2])
            a.hl(x, x + 3, y + h + 1, w0)
        b.rect(10, 5, 22, 5, k[2])                           # hanging scroll with enso
        b.rect(11, 6, 21, 13, PAPER[1])
        b.vl(11, 6, 13, PAPER[2])
        b.rect(10, 14, 22, 14, k[2])
        ring = b.E(16, 9.5, 3.4, 3.2) & ~b.E(16, 9.5, 2.1, 1.9)
        b.fill(ring, K)
        b.rect(18, 8, 19, 8, PAPER[1])
        b.rect(19, 12, 20, 12, RED[2])
    elif name == 'hakaba':
        wd = ('#2a2028', '#4a3a38', '#6a5848', '#8a7858')      # sotoba grave tablets
        for (x, top) in ((5, 2), (10, 0), (15, 3), (21, 1), (26, 4)):
            a.rect(x, top + 2, x + 2, 14, wd[1])
            a.vl(x, top + 2, 14, wd[2])
            a.vl(x + 2, top + 2, 14, wd[0])
            a.px(x + 1, top + 1, wd[2])
            a.px(x + 1, top, wd[1])
            a.rect(x - 1, top + 3, x + 3, top + 3, wd[1])
            for y in range(top + 6, 13, 3):
                a.px(x + 1, y, K)
        niche(b, 9, 22, 6)                                   # jizo alcove with candle
        s = k
        b.fill(b.E(15, 8.5, 2.6, 2.4), s[2])
        b.rect(12, 11, 18, 14, s[1])
        b.hl(13, 17, 11, RED[2])
        b.hl(14, 16, 12, RED[1])
        b.rect(14, 8, 14, 8, s[0])
        b.px(16, 8, s[0])
        b.vl(20, 11, 14, PAPER[2])
        b.rect(20, 9, 20, 10, GOLD[2])
        b.px(20, 8, GOLD[1])
    elif name == 'kurama':
        rope(a, 1, 30, 6, 2.2, shide=(6, 14, 23))
        b.grid(10, 5, "..hh....hh..\n.rrrrrrrrrr.\nrrkyrrrrykrr\nrrrrrRRrrrrr\n.rrrRRRRrrr.\n.rrrRRRRrrr.\n"
                      "..rkkRRkkr..\n..rrrRRrrr..\n...rrRRrr...\n.....RR.....",
               dict(h=PAPER[2], r=RED[2], R=RED[3], k=K, y=GOLD[2]))   # tengu mask
    elif name == 'yukiyama':
        for (x, wdt, h) in ((2, 4, 7), (8, 3, 4), (13, 5, 9), (20, 3, 5), (25, 4, 7)):   # icicles
            m = a.PG([(x, 4), (x + wdt, 4), (x + wdt / 2, 4 + h)])
            a.fill(m, ICE[2])
            a.fill(m & ~sh(m, -1, 0), ICE[1])
            a.line([(x, 4), (x + wdt / 2 - 1, 4 + h - 2)], ICE[3])
        m = b.E(16, 14, 8.4, 8) & (b.Y >= 6) & (b.Y <= 14)   # ice cave with watching eyes
        b.fill(m, K)
        b.fill(dil(m) & ~m & (b.Y >= 5) & (b.Y <= 14), ICE[3])
        for x in (10, 14, 19):
            b.vl(x, 7, 8 + (x % 3), ICE[2])
        b.rect(12, 11, 13, 11, ICE[3])
        b.rect(18, 11, 19, 11, ICE[3])
    elif name == 'ryugu':
        m = a.E(16, 9.5, 5.4, 4.6)                           # round window onto the deep
        a.fill(dil(m), GOLD[1])
        a.fill(dil(m) & (a.Y > 10), GOLD[0])
        a.fill(m, WATER[0])
        a.fill(m & (a.Y < 8), WATER[1])
        a.rect(15, 5, 16, 14, GOLD[0])
        a.rect(11, 9, 21, 9, GOLD[0])
        a.rect(13, 11, 13, 11, WATER[3])
        c = (P['k1'], P['k2'], P['k3'])                      # coral growing up the wall
        for (x, y0, y1) in ((8, 14, 8), (11, 14, 6), (14, 14, 9), (19, 14, 7), (23, 14, 9)):
            b.vl(x, y1, y0, c[0])
            b.vl(x + 1, y1 + 1, y0, c[1])
            b.px(x, y1 - 1, c[2])
        b.rect(9, 10, 10, 10, c[1])
        b.rect(20, 10, 22, 10, c[1])
        b.rect(15, 11, 18, 11, c[0])
        b.rect(26, 12, 28, 13, WHITE[2])                     # pearl
        b.px(26, 12, '#ffffff')
    elif name == 'uminobe':
        net = '#5a5058'
        for i in range(-2, 9):                               # fishing net with glass floats
            a.line([(i * 5, 5), (i * 5 + 9, 14)], net)
            a.line([(i * 5 + 9, 5), (i * 5, 14)], net)
        for (x, y) in ((6, 8), (17, 10), (26, 7)):
            m = a.E(x + .5, y + .5, 2.4, 2.4)
            a.fill(dil(m), K)
            a.form(m, (GLOW[0], GLOW[1], GLOW[2]), 1, 1)
        b.vl(16, 4, 6, STRAW[1])                             # ghost-fire lantern
        m = b.E(16, 10, 4.4, 4)
        b.fill(dil(m), K)
        b.form(m, (WATER[1], WATER[2], WATER[3]), 2, 1)
        b.fill(b.E(16, 10.5, 1.6, 2), '#d8f0ff')
        b.rect(13, 6, 19, 6, K)
        b.rect(13, 14, 19, 14, K)
    elif name == 'yomi':
        bn = (P['w0'], P['w1'], P['w2'], P['w3'])
        niche(a, 6, 25, 5)                                   # giant skull staring out
        m = a.E(16, 9, 7.4, 5.4) | a.R(11, 9, 21, 14)
        a.form(m, (bn[0], bn[1], bn[2]), 2, 1)
        for x in (11, 18):
            a.rect(x, 8, x + 3, 10, K)
            a.rect(x + 1, 9, x + 2, 9, '#c81e2a')
        a.rect(15, 11, 16, 12, K)
        for x in (12, 14, 16, 18, 20):
            a.vl(x, 13, 14, bn[0])
        niche(b, 5, 26, 5)                                   # rib cage arch
        for x in (7, 11, 15, 19, 23):
            b.vl(x, 6, 14, bn[1])
            b.vl(x + 1, 6, 13, bn[2])
        b.rect(6, 5, 25, 5, bn[2])
        b.rect(6, 9, 25, 9, bn[0])
    elif name == 'jigoku':
        niche(a, 12, 20, 6)                                  # lava fall from a fissure
        a.rect(13, 6, 19, 14, LAVA[1])
        a.rect(14, 6, 16, 14, LAVA[2])
        a.vl(15, 7, 12, LAVA[3])
        a.rect(10, 14, 22, 15, LAVA[1])
        a.rect(12, 15, 19, 15, LAVA[2])
        a.rect(11, 5, 21, 5, w0)
        for x in (9, 22):                                    # chains and shackles
            for y in range(5, 12, 2):
                b.px(x, y, IRON[3])
                b.px(x, y + 1, IRON[1])
            b.rect(x - 1, 12, x + 1, 13, IRON[2])
            b.px(x, 13, K)
        b.rect(13, 5, 18, 6, IRON[1])
        b.hl(13, 18, 5, IRON[2])
        for x in (13, 15, 17):
            sp = b.PG([(x, 7), (x + 1, 7), (x + .5, 11)])
            b.fill(sp, IRON[2])
    elif name == 'takamagahara':
        for i in range(8):                                   # sun mirror with rays
            ang = i * math.pi / 4
            a.line([(16 + math.cos(ang) * 5, 9.5 + math.sin(ang) * 4.4), (16 + math.cos(ang) * 8.4, 9.5 + math.sin(ang) * 5.6)], GOLD[1])
        m = a.E(16, 9.5, 4.4, 4.2)
        a.fill(dil(m), GOLD[0])
        a.form(m, (GOLD[1], GOLD[2], GOLD[3]), 2, 1)
        b.rect(9, 5, 22, 14, WHITE[1])                       # heavenly doors
        b.rect(9, 5, 22, 5, GOLD[1])
        b.vl(9, 5, 14, GOLD[1])
        b.vl(22, 5, 14, GOLD[0])
        b.rect(10, 6, 14, 14, WHITE[2])
        b.rect(15, 6, 16, 14, WHITE[0])
        b.rect(13, 9, 14, 10, GOLD[2])
        b.rect(17, 9, 18, 10, GOLD[1])
        b.hl(10, 21, 14, WHITE[0])
    elif name == 'kawabe':
        lf = P['leaf']
        for (x, top) in ((4, 6), (8, 3), (12, 7), (19, 4), (23, 8), (27, 5)):   # cattails
            a.vl(x, top, 14, lf[0])
            a.rect(x, top - 1, x + 1, top + 2, '#5a3c2a')
            a.vl(x, top - 1, top + 1, '#7a5632')
        for (x, y) in ((6, 10), (15, 9), (21, 11), (25, 10)):
            a.line([(x, 14), (x + 2, y)], MOSS[1])
        niche(b, 12, 19, 5, WATER[0])                        # trickling waterfall
        b.rect(13, 5, 18, 14, WATER[1])
        b.vl(14, 5, 12, WATER[2])
        b.vl(17, 7, 13, WATER[2])
        b.rect(11, 14, 20, 15, WATER[2])
        b.rect(13, 14, 15, 14, WATER[3])
        b.rect(18, 15, 19, 15, WATER[3])
    elif name == 'yashiki':
        pa = ('#2a2636', '#4a4456', '#5e5666')
        a.fill(a.PG([(9, 7), (15, 7), (17, 9), (14, 11), (10, 10)]), K)     # torn shoji, something looks out
        a.rect(11, 8, 13, 9, GOLD[2])
        a.px(12, 8, K)
        a.px(12, 9, K)
        a.line([(20, 7), (22, 11)], K)
        a.line([(23, 7), (25, 11)], K)
        a.line([(26, 7), (28, 10)], K)
        warm = ('#5a4038', '#8a6a48', '#b09058')
        b.rect(5, 7, 19, 11, warm[1])                        # lit panel with a long-haired shadow
        b.rect(5, 7, 19, 7, warm[2])
        for x in (9, 14, 19):
            b.vl(x, 7, 11, w1)
        b.hl(5, 19, 9, w1)
        sil = b.E(12, 8.5, 2.4, 2) | b.PG([(9, 9), (15, 9), (16, 11), (8, 11)])
        b.fill(sil & b.R(5, 7, 19, 11), '#2a1c22')
    elif name == 'iwato':
        rope(a, 2, 29, 4, 3, shide=(8, 15, 22))              # Shimenawa vor dem Felsentor
        niche(b, 11, 20, 5)                                  # Kagaribi: Feuerkorb der wartenden Götter
        b.vl(13, 10, 14, IRON[1])
        b.vl(18, 10, 14, IRON[1])
        b.rect(12, 8, 19, 10, IRON[2])
        b.hl(12, 19, 8, IRON[3])
        flame(b, 13, 3, LAVA)
        b.px(15, 4, SUN[3])
    elif name == 'oeyama':
        wd = ('#1c121c', '#3a2428', '#58382c')
        for (x, top) in ((6, 3), (24, 5)):                   # skull trophies on stakes
            a.rect(x, top + 4, x + 1, 14, wd[2])
            a.vl(x + 1, top + 4, 14, wd[1])
            skull(a, x + .5, top + 2, BONE, r=2.9)
        kb = a.PG([(12, 14), (15, 4), (19, 4), (18, 14)])    # kanabo leaning on the rock
        a.fill(dil(kb) & (a.Y <= 14), K)
        a.form(kb, (IRON[0], IRON[1], IRON[2]), 2, 1)
        for (x, y) in ((14, 6), (17, 8), (14, 10), (17, 12)):
            a.px(x, y, IRON[3])
        m = b.E(16, 14, 9.4, 8.4) & (b.Y >= 6) & (b.Y <= 14)  # barred cave, eyes inside
        b.fill(m, K)
        b.rect(11, 10, 12, 10, '#ff5a3c')
        b.rect(17, 10, 18, 10, '#ff5a3c')
        for x in (9, 14, 19, 23):
            b.fill(m & (b.X == x), IRON[2])
            b.fill(m & (b.X == x + 1), IRON[0])
        b.fill(m & (b.Y == 8), IRON[1])
    elif name == 'shinkai':
        m = a.E(16, 10, 9.4, 4.6)                            # anglerfish lurking in a hole
        a.fill(m, K)
        a.rect(10, 9, 11, 10, '#c8ee78')
        for x in range(12, 22, 2):
            a.px(x, 12, WHITE[2])
            a.px(x + 1, 13, WHITE[1])
        a.line([(14, 8), (18, 6), (22, 7)], k[2])
        a.rect(22, 7, 23, 8, '#ffe24a')
        a.px(22, 7, '#fffbc0')
        for (x, top) in ((6, 8), (10, 6), (14, 9), (19, 7), (24, 8)):   # glowing anemone garden
            b.vl(x, top, 14, GLOW[0])
            b.vl(x + 1, top + 1, 14, GLOW[1])
            b.rect(x - 1, top - 1, x + 2, top - 1, GLOW[2])
            b.px(x, top - 2, GLOW[3])
    elif name == 'enma_cho':
        m = a.E(16, 9.5, 5.4, 4.8)                           # judgment mirror
        a.fill(dil(m), GOLD[1])
        a.fill(dil(m) & (a.Y > 10), GOLD[0])
        a.fill(m, WHITE[0])
        a.fill(m & (a.X + a.Y < 24), WHITE[1])
        a.line([(13, 10), (16, 7)], WHITE[3])
        a.line([(15, 11), (17, 9)], WHITE[2])
        a.rect(13, 15, 19, 15, GOLD[0])
        b.rect(11, 10, 21, 11, IRON[1])                      # wall brazier
        b.hl(11, 21, 10, IRON[2])
        b.rect(13, 12, 19, 12, IRON[0])
        b.rect(15, 13, 17, 14, IRON[1])
        flame(b, 11, 5)
        flame(b, 16, 5)
        b.rect(12, 9, 20, 9, LAVA[1])
    elif name == 'tsukiyomi':
        s = SILVER
        m = a.E(16, 9.5, 5.4, 4.8)                           # full-moon window with the rabbit
        a.fill(dil(m), s[1])
        a.fill(m, '#c8d0e0')
        a.fill(m & ~sh(m, -2, -1), s[2])
        a.grid(13, 7, "r.r..\nrrr..\n.rrrr\n.rrrr\n.r.r.", dict(r=s[1]))
        b.fill((b.E(16, 9.5, 4.8, 4.6) & ~b.E(18.4, 8.6, 4.2, 4)), '#c8d0e0')   # crescent crest + bells
        for x in (6, 25):
            b.vl(x, 5, 9, s[1])
            b.rect(x - 1, 10, x + 1, 11, s[2])
            b.px(x - 1, 10, s[3])
            b.px(x, 12, s[0])
    elif name == 'yomi_oku':
        v = VIOLET                                           # zerschlissene Misu-Jalousie mit Quaste
        a.rect(5, 5, 26, 13, v[2])
        for y in range(6, 14, 2):
            a.hl(5, 26, y, v[1])
        a.vl(26, 5, 13, v[0])
        a.rect(4, 4, 27, 4, GOLD[0])
        a.hl(4, 27, 3, v[2])
        a.fill(a.PG([(18, 9), (24, 9), (22, 14), (19, 12)]), K)
        a.vl(9, 5, 11, RED[1])
        a.rect(8, 12, 10, 13, RED[2])
        b2 = b
        niche(b2, 10, 21, 5)                                  # Tōrō mit kaltem Totenfeuer
        b2.vl(15, 5, 6, IRON[1])
        b2.rect(13, 7, 18, 7, IRON[2])
        b2.rect(13, 8, 18, 12, IRON[0])
        b2.rect(14, 8, 17, 11, ONIBI[1])
        b2.rect(15, 9, 16, 10, ONIBI[3])
        b2.vl(15, 8, 11, IRON[0])
        b2.rect(12, 13, 19, 13, IRON[2])
    return [a, b]
