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
        cv, rng = new(0)                                     # family grave pillar
        box(cv, k, 7, 24, 25, 28, top=2)
        box(cv, k, 10, 19, 22, 23, top=2)
        box(cv, k, 12, 4, 20, 18, top=2)
        for y in (8, 11, 14):
            cv.rect(15, y, 16, y + 1, k[0])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # round-top stele, mossy, cracked
        m = cv.R(10, 12, 22, 28) | cv.E(16, 12, 6.4, 6)
        cv.form(m, (k[0], k[1], k[2]), 3, 1)
        cv.line([(19, 7), (17, 12), (19, 16), (18, 20)], k[0])
        cover(cv, m, MOSS, 4, rng)
        cv.rect(13, 16, 14, 22, k[0])
        cv.fill(m & (cv.Y >= 26) & (cv.X < 15), MOSS[1])
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
        cv, rng, m = plain_boulder(0)
        cover(cv, m, MOSS, 6, rng)
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # cattail clump
        a, b = P['leaf']
        for (x0, x1, h) in ((10, 7, 14), (13, 12, 21), (17, 18, 23), (20, 24, 16), (15, 15, 12), (22, 21, 10)):
            cv.line([(x0, 28), (x1, 28 - h)], a)
            cv.line([(x0 + 1, 28), (x1 + 1, 28 - h)], MOSS[1])
        for (x, y) in ((12, 5), (18, 3), (24, 10)):
            cv.rect(x, y, x + 1, y + 5, '#4a2e26')
            cv.vl(x, y, y + 4, '#74502c')
        cv.rect(8, 27, 24, 28, MOSS[0])
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # stump with mushrooms
        w = ('#1c121c', '#33242a', '#4e382e', '#6e5238')
        m, t = cyl(cv, w, 16, 28, 8, 10, top=('#4e382e', '#7a6444', '#988458'))
        for x in (10, 13, 19, 22):
            cv.vl(x, 22, 27, w[0])
        cover(cv, t, MOSS, 2, rng)
        for (x, y) in ((6, 23), (22, 20)):
            cv.grid(x, y, ".rrr.\nrRrrr\n..s..\n..s..", dict(r=RED[2], R=PAPER[2], s=PAPER[1]))
        out.append(fin(cv, P))

    elif name == 'yashiki':
        cv, rng = new(0)                                     # tansu chest
        box(cv, k, 6, 8, 26, 28, top=4)
        for y in (17, 22):
            cv.hl(7, 23, y, k[0])
        for (x, y) in ((14, 14), (14, 19), (14, 24)):
            cv.rect(x, y, x + 3, y + 1, IRON[2])
            cv.hl(x, x + 3, y + 1, IRON[0])
        cv.vl(15, 23, 27, k[0])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # unlit andon lamp
        pa = ('#2a2636', '#4a4456', '#6a6276', '#8a8290')
        cv.rect(10, 9, 22, 25, pa[1])
        cv.rect(10, 9, 14, 25, pa[2])
        cv.rect(19, 9, 22, 25, pa[0])
        for x in (10, 16, 22):
            cv.vl(x, 8, 28, k[1] if x < 22 else k[0])
        for y in (8, 14, 20, 25):
            cv.hl(10, 22, y, k[1])
        cv.hl(10, 22, 8, k[2])
        cv.fill(cv.PG([(17, 10), (21, 13), (18, 13), (20, 19)]), K)   # torn paper
        cv.rect(9, 26, 23, 26, k[2])
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # byobu folding screen
        g = ('#2a2230', '#4a3c3a', '#6a5a44', '#8a7a54')
        for i, (x0, x1, ya, yb) in enumerate(((4, 11, 9, 6), (11, 18, 6, 9), (18, 25, 9, 6))):
            m = cv.PG([(x0, ya), (x1, yb), (x1, yb + 19), (x0, ya + 19)])
            cv.fill(m, g[2] if i % 2 == 0 else g[1])
            cv.line([(x0, ya), (x1, yb)], k[1])
            cv.line([(x0, ya + 19), (x1, yb + 19)], k[0])
            cv.vl(x0, min(ya, yb), ya + 19, k[0])
        cv.vl(25, 6, 25, k[0])
        cv.line([(6, 20), (9, 15), (12, 19), (15, 14), (20, 21), (23, 17)], g[0])   # ink mountains
        cv.fill(cv.E(20, 12, 1.6, 1.6), RED[1])
        out.append(fin(cv, P))

    elif name == 'oeyama':
        cv, rng, m = plain_boulder(0)
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # komodaru sake barrel
        m, t = cyl(cv, STRAW, 16, 28, 9, 15, top=(STRAW[1], STRAW[2], STRAW[3]))
        side = m & ~t
        for y in (18, 25):
            cv.fill(side & (cv.Y == y), STRAW[0])
        for x in (9, 23):
            cv.fill(side & (cv.X == x), STRAW[0])
        cv.rect(13, 19, 18, 24, PAPER[2])
        cv.rect(14, 20, 17, 23, RED[2])
        cv.rect(15, 21, 16, 22, PAPER[2])
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # skulls on stakes
        w = ('#1c121c', '#3a2428', '#58382c')
        for (x, top) in ((10, 12), (21, 8)):
            cv.rect(x, top, x + 1, 28, w[1])
            cv.vl(x + 1, top, 28, w[0])
        skull(cv, 10.5, 11, BONE, r=3.8)
        skull(cv, 21.5, 7, BONE, r=3.8)
        cv.line([(6, 28), (14, 25)], w[2])
        cv.line([(17, 26), (26, 28)], w[2])
        out.append(fin(cv, P))

    elif name == 'shinkai':
        cv, rng = new(0)                                     # brain coral
        m = cv.E(16, 21, 10.4, 8.4) & (cv.Y <= 28)
        cv.form(m, (k[0], k[1], k[2]), 4, 1)
        for pts in ([(8, 20), (11, 17), (14, 19), (17, 16), (20, 18)], [(9, 24), (13, 22), (16, 24), (20, 22), (23, 24)],
                    [(12, 14), (15, 13), (18, 14)]):
            cv.line(pts, k[0])
            cv.line([(x, y + 1) for x, y in pts], k[3] if pts[0][1] < 21 else k[2])
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # glowing tube sponges
        for (x, h, r) in ((9, 12, 3), (22, 15, 3.2), (15.5, 21, 3.6)):
            m, t = cyl(cv, k, x, 28, r, h, top=(GLOW[0], GLOW[1], GLOW[2]))
            cv.fill(cv.E(x, 28 - h, r - 1.4, 1), K)
        out.append(fin(cv, P))
        cv, rng = new(2)                                     # giant spiral shell
        s = (P['shell'][0], P['shell'][1], P['shell'][2], '#6a8a98')
        m = cv.E(15, 19, 10.4, 9) & (cv.Y <= 28)
        cv.form(m, (s[0], s[1], s[2]), 4, 1)
        for (rx, ry) in ((7, 6), (4, 3.4)):
            ring = (cv.E(14, 18, rx, ry) & ~cv.E(14.6, 18.6, rx - 1, ry - 1)) & m
            cv.fill(ring, s[0])
        cv.fill(cv.E(13.5, 18, 1.4, 1.2), s[3])
        cv.fill(cv.PG([(22, 22), (27, 24), (27, 28), (20, 28)]), s[1])
        cv.fill(cv.PG([(23, 24), (26, 25), (26, 27), (22, 27)]), K)
        out.append(fin(cv, P))

    elif name == 'enma_cho':
        cv, rng = new(0)                                     # stone brazier
        box(cv, k, 10, 24, 22, 28, top=2)
        cv.rect(13, 17, 19, 23, k[1])
        cv.vl(13, 17, 23, k[2])
        cv.rect(18, 17, 19, 23, k[0])
        bowl = cv.E(16, 14, 9.4, 5) & (cv.Y >= 13)
        cv.form(bowl, (k[0], k[1], k[2]), 3, 1)
        cv.hl(7, 25, 13, GOLD[1])
        cv.fill(cv.E(16, 12, 6, 1.6), LAVA[1])
        flame(cv, 10, 7)
        flame(cv, 16, 6)
        out.append(fin(cv, P))
        cv, rng = new(1)                                     # judgment stele with gold script
        box(cv, k, 8, 24, 24, 28, top=2)
        m = cv.PG([(11, 23), (11, 7), (16, 4), (21, 7), (21, 23)])
        cv.form(m, (k[0], k[1], k[2]), 3, 1)
        for (x, ys) in ((14, (9, 12, 16, 19)), (17, (8, 11, 14, 18))):
            for y in ys:
                cv.rect(x, y, x + 1, y + 1, GOLD[1])
                cv.px(x + 1, y + 1, GOLD[0])
        out.append(fin(cv, P))
        out.append(fin(pillar(2, k, bands=GOLD), P))

    elif name == 'tsukiyomi':
        cv, rng, m = plain_boulder(0)                        # moon rock with craters
        for (cx, cy, rx, ry) in ((13, 17, 3, 2), (20, 22, 2.4, 1.6), (11, 24, 1.8, 1.2)):
            c = cv.E(cx, cy, rx, ry) & m
            cv.fill(c, k[0])
            cv.fill(c & sh(c, -1, -1), k[1])
            cv.fill(sh(c, 1, 1) & ~c & m & (cv.Y > cy), k[3])
        out.append(fin(cv, P))
        out.append(fin(pillar(1, SILVER, bands=WHITE), P))
        cv, rng = new(2)                                     # usu mortar with mochi and mallet
        w = ('#1e1a2c', '#3a3448', '#585268', '#7a7488')
        m, t = cyl(cv, w, 14, 28, 8, 12, top=(w[0], w[1], w[2]))
        cv.fill(cv.E(14, 15.5, 5, 2.2), WHITE[2])
        cv.fill(cv.E(13, 15, 3, 1.2), WHITE[3])
        cv.line([(21, 27), (27, 9)], w[2])
        cv.line([(22, 27), (28, 9)], w[1])
        hm = capsule(cv, 23, 7, 2.6, 30, 10, 2.6)
        cv.fill(dil(hm), K)
        cv.form(hm, (w[1], w[2], w[3]), 1, 1)
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
    return [a, b]
