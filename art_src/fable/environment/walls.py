"""Wall kit: cap textures + face patterns per wall_pat, assembled into wall_h / wall_h_bottom / wall_v / corner.
Layout (top wall, 32x16): rows 0-3 cap (top of the wall seen from above), row 4 moonlit lip, rows 5-14 face,
row 15 contact shadow."""
import random
import numpy as np
from core import *
from biomes import *
from floors import place, put

FY = 5      # first face row
FH = 10     # face rows (5..14)


def tri(draw, w, h):
    """draw(cv, xoff) on a 3x wide canvas at three offsets -> horizontally periodic image"""
    cv = Cv(w * 3, h)
    draw(cv)
    out = Cv(w, h)
    out.a = cv.a[:, w:2 * w].copy()
    return out


# ------------------------------------------------------------------ caps
def cap_tex(name, P, w, h, seed=0):
    """cap texture of any size; all motifs stay inside so it tiles along both axes"""
    pat = P['wall_pat']
    rng = random.Random('%s-cap-%d-%d-%d' % (name, w, h, seed))
    c0, c1 = P['cap0'], P['cap1']
    c2 = mix(c1, P['lip'], .25)
    cv = Cv(w, h, bg=c0)
    occ = np.zeros((h, w), bool)

    def scat(sprites, legend, n, pad=1):
        for _ in range(n):
            t = rng.choice(sprites)
            rows = t.split('\n')
            sw, shh = max(len(r) for r in rows), len(rows)
            if sw > w or shh > h:
                continue
            for _ in range(40):
                x, y = rng.randint(0, w - sw), rng.randint(0, h - shh)
                if not occ[max(0, y - pad):y + shh + pad, max(0, x - pad):x + sw + pad].any():
                    occ[y:y + shh, x:x + sw] = True
                    cv.grid(x, y, t, legend)
                    break
    area = w * h
    if pat == 'bamboo':
        scat(["aa.\n.aa", ".aa\naa.", "aaa", "bb.\n.bb", ".bb\nbb."], dict(a=c1, b=c2), area // 16)
    elif pat in ('torii', 'wood'):
        # kawara roof tiles: 8x4 bricks, alternate rows offset
        cv.rect(0, 0, w - 1, h - 1, c1)
        for y in range(0, h, 4):
            cv.hl(0, w - 1, y + 3, c0)
            off = 0 if (y // 4) % 2 == 0 else 4
            for x in range(off, w, 8):
                cv.vl(x, y, y + 2, c0)
    elif pat == 'stone':
        cv.rect(0, 0, w - 1, h - 1, c1)
        if w >= h:
            for x in range(15, w, 16):
                cv.vl(x, 0, h - 1, c0)
            if h > 8:
                cv.hl(0, w - 1, 7, c0)
        else:
            for y in range(15, h, 16):
                cv.hl(0, w - 1, y, c0)
            cv.vl(6, 0, h - 1, c0)
        if name == 'hakaba':
            scat(["mm.\nmmm", "mmm\n.mm", "mm"], dict(m=MOSS[0]), area // 60)
        if name == 'enma_cho':
            scat(["gg"], dict(g=GOLD[0]), area // 90, pad=3)
    elif pat in ('rock', 'bone') or name == 'shinkai':
        for _ in range(area // 30):
            rx, ry = rng.uniform(2, 4), rng.uniform(1.4, 2.4)
            x, y = rng.uniform(rx, w - rx - 1), rng.uniform(ry, h - ry - 1)
            cv.form(cv.E(x, y, rx, ry), (c0, c1, c2), 1, 1)
        if pat == 'bone':
            scat([".bb.\nbccb\nbkkb"], dict(b=BONE[0], c=BONE[1], k=c0), area // 150, pad=2)
        if name == 'shinkai':
            scat(["gg", "g\ng"], dict(g=GLOW[0]), area // 70, pad=2)
        if name == 'kawabe':
            scat(["mm.\nmmm", "mmm\n.mm"], dict(m=MOSS[0]), area // 50)
        if name == 'jigoku':
            scat(["ee", "e\ne"], dict(e=LAVA[0]), area // 80, pad=2)
    elif pat == 'ice':
        scat([".aaaa.\naaaaaa", "aaa\n.aa", ".aaa\naaaa"], dict(a=c1), area // 34)
    elif pat == 'coral':      # ryugu lacquer beam with gold studs
        cv.rect(0, 0, w - 1, h - 1, c1)
        if w >= h:
            cv.hl(0, w - 1, h - 1, c0)
            for x in range(3, w, 8):
                cv.rect(x, max(0, h // 2 - 1), x + 1, max(0, h // 2 - 1) + 1, GOLD[1] if h > 2 else c1)
        else:
            cv.vl(w - 1, 0, h - 1, c0)
            for y in range(3, h, 8):
                cv.rect(w // 2 - 1, y, w // 2, y + 1, GOLD[1])
    elif pat == 'planks':
        cv.rect(0, 0, w - 1, h - 1, c1)
        if w >= h:
            for x in range(7, w, 8):
                cv.vl(x, 0, h - 1, c0)
        else:
            for y in range(7, h, 8):
                cv.hl(0, w - 1, y, c0)
    elif pat == 'cloud':
        for _ in range(area // 40):
            rx, ry = rng.uniform(2.5, 4.5), rng.uniform(1.4, 2.4)
            x, y = rng.uniform(rx, w - rx - 1), rng.uniform(ry, h - ry - 1)
            m = cv.E(x, y, rx, ry)
            cv.fill(m, c1)
            cv.fill(m & ~sh(m, 0, 1), c2)
    return cv


# ------------------------------------------------------------------ faces (drawn into rows 5..15 of a 32x16 canvas)
def bulges(P, rng, ramp, n=9, big=False):
    """craggy / puffy face made of overlapping shaded lumps, periodic over 32 px"""
    specs = []
    xs = [2, 9, 17, 25] if not big else [3, 13, 23]
    for row, yc in enumerate((2.2, 7.4)):
        for i, x in enumerate(xs):
            xx = x + (4 if row else 0) + rng.uniform(-1, 1)
            specs.append((xx, yc + rng.uniform(-.8, .8), rng.uniform(4.2, 5.6) + (1.2 if big else 0),
                          rng.uniform(3.0, 3.8) + (.6 if big else 0)))

    def draw(cv):
        cv.a[:] = hx(ramp[0])
        for (x, y, rx, ry) in specs:
            for k in range(3):
                m = cv.E(x + k * 32, y, rx, ry)
                cv.fill(dil(m), ramp[0])
                cv.form(m, (mix(ramp[0], ramp[1], .5), ramp[1], ramp[2]), 2, 1)
    return tri(draw, 32, FH)


def face(name, P, seed=0):
    pat = P['wall_pat']
    rng = random.Random('%s-face-%d' % (name, seed))
    w0, w1, w2, w3 = P['w0'], P['w1'], P['w2'], P['w3']
    cv = Cv(32, 16)
    f = Cv(32, FH, bg=w0)
    base = mix(w0, K, .5)

    if pat == 'bamboo':
        for x in (4, 11, 17, 23, 30):                       # far culms in the gaps
            f.vl(x, 0, FH - 1, mix(w0, w1, .6))
        for (x, wd, ny) in ((0, 4, 3), (6, 5, 6), (13, 4, 2), (18, 5, 7), (25, 5, 4)):
            f.rect(x, 0, x + wd - 1, FH - 1, w2)
            f.vl(x, 0, FH - 1, w3)
            f.vl(x + wd - 1, 0, FH - 1, w1)
            f.hl(x, x + wd - 1, ny, w1)                     # node ring
            f.hl(x, x + wd - 2, ny + 1, w3)
    elif pat == 'torii':
        f.a[:] = hx(mix(w0, K, .6))
        f.rect(0, 0, 31, 1, w2)                             # top rail
        f.hl(0, 31, 0, w3)
        f.hl(0, 31, 2, w0)
        for x in range(2, 32, 8):
            f.rect(x, 2, x + 3, 7, w2)
            f.vl(x, 2, 7, w3)
            f.vl(x + 3, 2, 7, w1)
            f.rect(x, 7, x + 3, 7, '#16121e')               # black footing
        f.rect(0, 5, 31, 5, w1)                             # lower rail behind the posts
        for x in range(2, 32, 8):
            f.rect(x, 5, x + 2, 5, w2)
            f.px(x, 5, w3)
        f.hl(0, 31, 8, STONE[2])                            # stone sill
        f.hl(0, 31, 9, STONE[1])
        for x in (9, 25):
            f.px(x, 9, STONE[0])
    elif pat == 'wood' and name == 'yashiki':
        pa0, pa1, pa2 = '#2a2636', '#4a4456', '#5e5666'     # shoji paper by moonlight
        f.rect(0, 0, 31, 1, w2)
        f.hl(0, 31, 1, w1)
        f.rect(0, 2, 31, 6, pa1)
        for x in range(3, 32, 5):                           # kumiko lattice
            f.vl(x + 4 if x + 4 < 32 else 31, 2, 6, w1)
        f.hl(0, 31, 4, w1)
        f.rect(8, 2, 11, 3, pa2)                            # faint lit cells
        f.rect(23, 5, 26, 6, pa2)
        f.rect(18, 2, 21, 3, pa0)
        f.rect(0, 7, 31, 9, w1)                             # wooden skirt
        f.hl(0, 31, 7, w2)
        for x in (10, 21):
            f.vl(x, 8, 9, w0)
        f.rect(0, 0, 2, 9, w2)                              # post
        f.vl(0, 0, 9, w3)
        f.vl(2, 0, 9, w1)
    elif pat == 'wood':
        f.a[:] = hx(w1)
        for x in range(7, 32, 8):
            f.vl(x, 2, 7, w0)
        for (x, y, ln, c) in ((5, 3, 3, w0), (13, 4, 3, w2), (18, 2, 4, w0), (27, 4, 3, w2), (10, 5, 2, w0)):
            f.vl(x, y, y + ln - 1, c)
        f.rect(0, 0, 31, 1, w2)                             # nageshi beam
        f.hl(0, 31, 0, w3)
        f.hl(0, 31, 2, w0)
        f.rect(0, 8, 31, 9, w2)                             # sill
        f.hl(0, 31, 9, w1)
        f.rect(0, 0, 3, 9, w2)                              # post
        f.vl(0, 0, 9, w3)
        f.vl(3, 0, 9, w1)
        f.rect(1, 4, 2, 5, w0)                              # iron nail cover
    elif pat == 'stone':
        for row, (y0, off) in enumerate(((0, 0), (5, 8))):
            for x0 in range(off - 16, 32, 16):
                dark = rng.random() < .3
                f.rect(x0, y0, x0 + 15, y0 + 4, mix(w1, w0, .35) if dark else w1)
                f.hl(x0, x0 + 14, y0, w2)
                f.vl(x0, y0, y0 + 3, w2)
                f.hl(x0, x0 + 15, y0 + 4, w0)
                f.vl(x0 + 15, y0, y0 + 4, w0)
        if name == 'hakaba':
            f.grid(3, 0, "mmmm.\n.mmn.\n..m..", dict(m=MOSS[0], n=MOSS[1]))
            f.grid(20, 0, "mmm\nmn.\nm..", dict(m=MOSS[0], n=MOSS[1]))
            f.line([(27, 5), (25, 7), (26, 9)], w0)
        if name == 'enma_cho':
            f.rect(0, 0, 31, 1, RED[1])
            f.hl(0, 31, 0, RED[2])
            f.hl(0, 31, 2, w0)
            for x in range(3, 32, 8):
                f.rect(x, 0, x + 1, 1, GOLD[1])
                f.px(x + 1, 1, GOLD[0])
    elif pat == 'rock':
        f = bulges(P, rng, (w0, w1, w2))
        if name == 'kawabe':
            top = Cv(32, FH)
            top.a = f.a.copy()
            m = np.all(top.a == np.array(hx(w2), np.uint8), axis=2) & (top.Y < 4)
            f.fill(m, MOSS[1])
            f.grid(6, 3, "m.m\nmmm", dict(m=MOSS[0]))
            f.grid(22, 2, "mm.\n.mm", dict(m=MOSS[0]))
        if name == 'jigoku':
            f.line([(11, 0), (13, 3), (11, 6), (13, 9)], LAVA[0])
            f.line([(13, 3), (11, 6)], LAVA[1])
            f.line([(27, 4), (25, 7), (27, 9)], LAVA[0])
    elif pat == 'ice':
        x = 0
        for i, wd in enumerate((6, 5, 7, 4, 6, 4)):
            top = (1, 0, 2, 0, 1, 2)[i]
            f.rect(x, top, x + wd - 1, FH - 1, w1)
            f.vl(x, top, FH - 1, w2)
            if wd > 4:
                f.vl(x + 1, top + 1, FH - 3, w2)
            f.vl(x + wd - 1, top, FH - 1, w0)
            f.px(x, top, w3)
            if i in (0, 2, 4):
                f.line([(x + 3, top + 2), (x + 2, top + 4)], w3)
            x += wd
    elif pat == 'coral' and name == 'ryugu':
        f.a[:] = hx(w1)
        f.hl(0, 31, 0, GOLD[1])                             # gold rail
        f.hl(0, 31, 1, GOLD[0])
        f.rect(7, 3, 29, 7, w0)                             # inset panel with seigaiha waves
        f.rect(8, 3, 29, 6, mix(w0, w1, .5))
        for cx in (11, 17, 23, 29):
            m = (f.E(cx, 7, 3.2, 3.2) & ~f.E(cx, 7, 2.2, 2.2)) & f.R(8, 3, 29, 6)
            f.fill(m, w2)
        f.hl(0, 31, 9, w0)
        f.rect(0, 0, 4, 9, w2)                              # round pillar
        f.vl(0, 0, 9, w1)
        f.vl(1, 0, 9, w3)
        f.vl(4, 0, 9, w1)
        f.hl(0, 4, 1, GOLD[1])
        f.hl(0, 4, 8, GOLD[1])
        f.px(4, 1, GOLD[0])
        f.px(4, 8, GOLD[0])
    elif pat == 'coral':                                    # shinkai: dark reef rock with glowing polyps
        f = bulges(P, rng, (w0, w1, w2))
        k1, k2 = P['k1'], P['k2']
        f.grid(4, 4, "c.c.c\nccccc\n.ccc.\n..c..\n..c..", dict(c=k1))
        f.grid(20, 5, "c..c\ncc.c\n.ccc\n..c.", dict(c=k1))
        for (x, y) in ((12, 2), (27, 3), (15, 7)):
            f.rect(x, y, x + 1, y + 1, GLOW[1])
            f.px(x, y, GLOW[2])
    elif pat == 'planks':
        x = 0
        for i, wd in enumerate((5, 5, 6, 5, 6, 5)):
            top = (1, 0, 2, 0, 1, 0)[i]
            c = (w1, mix(w1, w2, .5), w1, mix(w1, w0, .3), mix(w1, w2, .5), w1)[i]
            f.rect(x, top, x + wd - 2, FH - 1, c)
            f.vl(x, top, FH - 1, w2)
            f.vl(x + wd - 1, 0, FH - 1, mix(w0, K, .5))
            gy = rng.randint(3, 6)
            f.vl(x + 2, gy, gy + 2, w0)
            x += wd
        ra, rb = '#6a5e50', '#3e3438'                       # rope lashed across
        for xx in range(32):
            f.px(xx, 3, ra if xx % 4 < 2 else rb)
            f.px(xx, 4, rb if xx % 4 < 2 else w0)
    elif pat == 'bone':
        f.a[:] = hx(mix(w0, K, .55))
        b, c, k = w1, mix(w1, w2, .55), mix(w0, K, .6)
        skull = ".bcccb.\nbcccccb\nbkkckkb\nbkkckkb\n.bckcb.\n.b.b.b."
        for x in (1, 17):
            f.grid(x, 0, skull, dict(b=b, c=c, k=k))
        for x in (9, 12, 25, 28):                           # upright long bones between the skulls
            f.vl(x, 1, 5, b)
            f.vl(x + 1, 0, 5, c)
            f.px(x, 0, c)
        for (x, y) in ((0, 7), (16, 7), (8, 8), (24, 8)):   # stacked femurs
            f.hl(x + 1, x + 13, y, c)
            f.hl(x + 1, x + 13, y + 1, b)
            f.px(x, y, b)
            f.px(x + 14, y + 1, b)
    elif pat == 'cloud':
        f = bulges(P, rng, (w0, w1, w2), big=True)
        m = np.all(f.a == np.array(hx(w2), np.uint8), axis=2) & (f.Y < 3)
        f.fill(m, w3)
    cv.a[FY:FY + FH] = f.a
    cv.hl(0, 31, 15, base)
    return cv


# ------------------------------------------------------------------ assembly
def wall_set(name):
    P = BIOMES[name]
    lip = P['lip']
    lipd = mix(P['lip'], P['cap0'], .55)
    shade = mix(P['w0'], K, .6)
    # top wall
    h = face(name, P)
    h.a[0:4] = cap_tex(name, P, 32, 4).a
    h.hl(0, 31, 4, lip)
    # bottom wall: far lip catches the moon, rest is cap
    b = Cv(32, 16)
    b.a[2:16] = cap_tex(name, P, 32, 14).a
    b.hl(0, 31, 0, shade)
    b.hl(0, 31, 1, lip)
    # left wall: cap, dim lip, sliver of shadowed inner face
    v = Cv(16, 32)
    v.a[:, 0:13] = cap_tex(name, P, 13, 32).a
    v.vl(13, 0, 31, lipd)
    v.rect(14, 0, 15, 31, shade)
    # top-left corner: capstone
    c = Cv(16, 16, bg=P['cap0'])
    c.a[:, :] = cap_tex(name, P, 16, 16, 1).a
    c.rect(14, 5, 15, 15, shade)
    c.vl(13, 4, 15, lipd)
    c.hl(13, 15, 4, lip)
    c0, c1 = P['cap0'], P['cap1']
    c.rect(2, 2, 10, 10, c0)                                # post top
    c.rect(2, 2, 9, 9, mix(c1, lip, .2))
    c.hl(2, 9, 2, mix(c1, lip, .55))
    c.vl(2, 2, 9, mix(c1, lip, .55))
    c.rect(5, 5, 6, 6, c0)
    return dict(h=h, bottom=b, v=v, corner=c)
