"""Shared helpers for enemy batch 3 (palette additions, curve masks, IK, export)."""
import sys, math, os
sys.path.insert(0, '/home/claude/fable_art')
import numpy as np
from PIL import Image
from px import *
import px

D = os.path.dirname(os.path.abspath(__file__)) + '/'
BG = (0x16, 0x28, 0x5c, 255)
FLOOR = (0x24, 0x20, 0x2c, 255)

# ---- extra materials (dark -> light), each with a cold rim tint
col('p0', '#221048'); col('p1', '#47227a'); col('p2', '#7a3fa8'); col('p3', '#b27ad4'); col('xp', '#d8c0f6')   # purple paper / ghost fur
col('n0', '#4a1446'); col('n1', '#8e2a68'); col('n2', '#cc4f8a'); col('n3', '#f490b4'); col('xn', '#ffd0e0')   # pink cloth
col('f0', '#7a1478'); col('f1', '#d82e94'); col('f2', '#ff7cc0'); col('f3', '#ffe0f0')                          # pink ghost fire
col('u0', '#34486a'); col('u1', '#6f90a4'); col('u2', '#a8cac8'); col('u3', '#def2e6')                          # drowned / snow-pale skin
col('hb', '#1a1738')                                                                                           # black human hair mid
px.add_rim('p0 p1 p2', 'xp'); px.add_rim('n0 n1 n2', 'xn'); px.add_rim('u0 u1 u2', 'u3'); px.add_rim('hb', 'xh')
px.add_rim('f0 f1', 'f2')

PUR = ('p1', 'p2', 'p3'); PURF = ('p0', 'p1', 'p2')
PINK = ('n1', 'n2', 'n3'); PALE = ('u1', 'u2', 'u3')
HAIR = ('h0', 'hb', 'h2'); SKN = ('k1', 'k2', 'k3')
WH = ('v1', 'v2', 'v3'); RD = ('m1', 'm2', 'm3'); WOOD = ('w0', 'w1', 'w2')
BRN = ('s1', 's2', 's3'); BRNF = ('s0', 's1', 's2')
FIRE = ('e0', 'y1', 'y2'); PFIRE = ('f0', 'f1', 'f2')


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


def spline(pts, n=6):
    """Catmull-Rom through pts -> dense point list"""
    P_ = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = P_[i - 1], P_[i], P_[i + 1], P_[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(tuple(pts[-1]))
    return out


def chain(pts, r0, r1=None):
    """union of capsules along a polyline, radius r0 -> r1 by arc length"""
    if r1 is None:
        r1 = r0
    d = [0.0]
    for a, b in zip(pts, pts[1:]):
        d.append(d[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    T = d[-1] or 1.0
    m = np.zeros((px.H, px.W), bool)
    for i in range(len(pts) - 1):
        ra = r0 + (r1 - r0) * d[i] / T
        rb = r0 + (r1 - r0) * d[i + 1] / T
        m |= L(pts[i][0], pts[i][1], ra, pts[i + 1][0], pts[i + 1][1], rb)
    return m


def ik(a, b, l1, l2, side=1):
    """joint between a and b for bone lengths l1,l2; side=+1 bends to the left of a->b (screen coords)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = math.hypot(dx, dy) or 0.001
    d = min(d, l1 + l2 - 0.01)
    x = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - x * x))
    ux, uy = dx / math.hypot(dx, dy), dy / math.hypot(dx, dy)
    return (a[0] + ux * x + uy * h * side, a[1] + uy * x - ux * h * side)


def flame(p, base, tip, r, ramp, bend=0.0, core=True):
    """one flame tongue: tapered, slightly bent, 3 nested tones (ramp dark->light, + optional white-hot core)"""
    mid = lerp(base, tip, 0.5)
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    ln = math.hypot(dx, dy) or 1
    mid = (mid[0] - dy / ln * bend, mid[1] + dx / ln * bend)
    pts = spline([base, mid, tip], 5)
    p.fill(chain(pts, r, 0.6), ramp[0])
    if r > 2.2:
        k = max(2, int(len(pts) * 0.7))
        p.fill(chain(pts[:k], r - 1.5, 0.6), ramp[1])
    if r > 3.6 and core:
        k = max(2, int(len(pts) * 0.45))
        p.fill(chain(pts[:k], r - 3.0, 0.6), ramp[2])


def polar(c, ang, r, ry=None):
    a = math.radians(ang)
    return (c[0] + math.cos(a) * r, c[1] - math.sin(a) * (r if ry is None else ry))


def bg_img(im, scale, bg):
    b = Image.new('RGBA', im.size, bg)
    b.alpha_composite(im)
    return b.resize((im.width * scale, im.height * scale), Image.NEAREST)


def export(name, fn, WALK, ATTACK, review=4):
    """writes <name>.png, _walk.png, _attack.png, _preview.png (6x, all frames) + a review sheet."""
    c0 = fn()
    base = crop_img(c0.img())
    base.save(D + name + '.png')
    strips = {}
    for tag, frames in (('walk', WALK), ('attack', ATTACK)):
        cs = [fn(**f) for f in frames]
        for i, c_ in enumerate(cs):
            x0, y0, x1, y1 = c_.bbox()
            assert x0 >= 1 and y0 >= 1 and x1 <= px.W - 2 and y1 <= px.H - 2, (name, tag, i, c_.bbox(), (px.W, px.H))
        strips[tag] = [c_.img() for c_ in cs]
        strip(strips[tag], D + f'{name}_{tag}.png')
    cw, ch = strips['walk'][0].size
    full = c0.img()
    sheet = Image.new('RGBA', (cw * 4, ch * 2), (0, 0, 0, 0))
    sheet.paste(full, (0, 0))
    for i, f in enumerate(strips['attack']):
        sheet.paste(f, ((i + 1) * cw, 0))
    for i, f in enumerate(strips['walk']):
        sheet.paste(f, (i * cw, ch))
    bg_img(sheet, 6, BG).save(D + name + '_preview.png')
    # review: frames on style bg, static on dungeon floor
    rv = Image.new('RGBA', (cw * 4, ch * 2), BG)
    rv.paste(Image.new('RGBA', (cw, ch), FLOOR), (0, 0))
    rv.alpha_composite(sheet)
    rv.resize((rv.width * review, rv.height * review), Image.NEAREST).save(D + f'_review/{name}.png')
    a = np.array(base)
    semi = int(((a[:, :, 3] > 0) & (a[:, :, 3] < 255)).sum())
    ncol = len({tuple(q) for q in a.reshape(-1, 4) if q[3] > 0})
    print(name, 'static', base.size, 'cell', (cw, ch), 'colours', ncol, 'semi', semi, 'orphans', len(orphans(base)))
    return base


def zoom(name, box, scale=10, bg=BG, src=None):
    im = Image.open(src or (D + name + '.png')).convert('RGBA').crop(box)
    bg_img(im, scale, bg).save(D + f'_review/{name}_zoom.png')
