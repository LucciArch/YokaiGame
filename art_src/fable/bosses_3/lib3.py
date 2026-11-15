"""Shared helpers for boss batch 3 (engine px.py imported untouched)."""
import sys, math, os
sys.path.insert(0, '/home/claude/fable_art')
import numpy as np
from PIL import Image
import px
from px import *

D = os.path.dirname(os.path.abspath(__file__)) + '/'
REV = '/tmp/rev3/'
BG = (0x16, 0x28, 0x5c, 255)
FLOOR = (0x24, 0x20, 0x2c, 255)

# ---- extra materials (dark -> light, shadows drift blue/violet) ----
col('hb', '#1a1738'); px.add_rim('hb', 'xh')
col('p0', '#1c1040'); col('p1', '#3c1f6c'); col('p2', '#6a3c9c'); col('p3', '#a878d0')    # purple cloth / miasma
col('xp', '#c4b8f4'); px.add_rim('p0 p1 p2', 'xp')
col('n0', '#4a2c3c'); col('n1', '#8c6450'); col('n2', '#c09a6c'); col('n3', '#e6cc98')    # sallow old skin
px.add_rim('n0 n1 n2', 'n3')
col('z0', '#2a2a4c'); col('z1', '#57628a'); col('z2', '#96a8b4'); col('z3', '#d2e2d4')    # corpse pale skin / smoke
px.add_rim('z0 z1 z2', 'z3')
col('d0', '#0c0c26'); col('d1', '#181c4c'); col('d2', '#2c3888'); col('d3', '#5c70cc')    # night-sky robe
col('xd', '#8ea4f0'); px.add_rim('d0 d1 d2', 'xd')
col('o0', '#7a2a48'); col('o1', '#c8627a'); col('o2', '#f2a4a0')                          # octopus underside
px.add_rim('o0 o1', 'o2')
px.add_rim('a0 a1', 'a2'); px.add_rim('e0', 'e1'); px.add_rim('y2', 'y3'); px.add_rim('e1', 'y2')
px.add_rim('r0', 'r2')


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def pol(o, ang, r):
    """angle in degrees, screen coords: 0=right, 90=down, 180=left, 270=up"""
    a = math.radians(ang)
    return (o[0] + math.cos(a) * r, o[1] + math.sin(a) * r)


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


def grow(m, n=1):
    for _ in range(n):
        m = dil(m)
    return m


def curve(pts, n=8):
    if len(pts) < 3:
        return list(pts)
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


def tube(pts, r0, r1, pw=1.0):
    """union of tapered capsules along a polyline"""
    m = np.zeros((px.H, px.W), bool)
    n = len(pts) - 1
    for i in range(n):
        ta, tb = (i / n) ** pw, ((i + 1) / n) ** pw
        m |= L(pts[i][0], pts[i][1], r0 + (r1 - r0) * ta, pts[i + 1][0], pts[i + 1][1], r0 + (r1 - r0) * tb)
    return m


def offset(pts, d0, d1):
    """polyline shifted along its normal by d0..d1"""
    out = []
    n = len(pts)
    for i in range(n):
        a = pts[max(0, i - 1)]; b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        d = d0 + (d1 - d0) * i / (n - 1)
        out.append((pts[i][0] - dy / l * d, pts[i][1] + dx / l * d))
    return out


def limb(c, a, ra, b, rb, ramp, sd=2, hl=1, only=None):
    return c.form(L(a[0], a[1], ra, b[0], b[1], rb), ramp, sd=sd, hl=hl, only=only)


def tongue(base, tip, w, bend=0.0, tr=0.5):
    """flame tongue / wisp: tapered curved tube from base to tip"""
    mx, my = (base[0] + tip[0]) / 2, (base[1] + tip[1]) / 2
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    l = math.hypot(dx, dy) or 1
    mid = (mx - dy / l * bend, my + dx / l * bend)
    return tube(curve([base, mid, tip], 6), w, tr)


def star(cx, cy, r, r2=None, n=4, rot=0):
    """n-pointed star mask"""
    r2 = r2 if r2 is not None else r * 0.3
    pts = []
    for i in range(n * 2):
        a = rot + 360.0 * i / (n * 2) - 90
        pts.append(pol((cx, cy), a, r if i % 2 == 0 else r2))
    return PG(pts)


def _bgim(im, bg, sc):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im)
    return b.resize((im.width * sc, im.height * sc), Image.NEAREST)


def export(name, fn, walk, attack):
    base_c = fn()
    base = crop_img(base_c.img())
    base.save(D + name + '.png')
    rows = []
    for tag, frames in (('walk', walk), ('attack', attack)):
        cs = [fn(**f) for f in frames]
        for i, c_ in enumerate(cs):
            x0, y0, x1, y1 = c_.bbox()
            ok = x0 >= 1 and y0 >= 1 and x1 <= px.W - 2 and y1 <= px.H - 2
            assert ok, ('EDGE', name, tag, i, (x0, y0, x1, y1), (px.W, px.H))
        rows.append(strip([c_.img() for c_ in cs], D + f'{name}_{tag}.png'))
    cw, ch = px.W, px.H
    sheet = Image.new('RGBA', (cw * 4, ch * 2), (0, 0, 0, 0))
    sheet.paste(rows[0], (0, 0))
    sheet.paste(base_c.img(), (0, ch))
    sheet.paste(rows[1], (cw, ch))
    _bgim(sheet, BG, 4).save(D + name + '_preview.png')
    os.makedirs(REV, exist_ok=True)
    _bgim(base, FLOOR, 6).save(REV + f'{name}_s.png')
    _bgim(sheet, BG, 2).save(REV + f'{name}_all.png')
    a = np.array(base)
    ncol = len({tuple(q) for q in a.reshape(-1, 4) if q[3] > 0})
    print(name, 'static', base.size, 'cell', (cw, ch), 'orphans', len(orphans(base)), 'colours', ncol)
    return base
