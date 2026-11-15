"""Shared helpers for enemy batch 2 (export, flames, small utilities). Engine = ../px.py (unmodified)."""
import sys, math
sys.path.insert(0, '/home/claude/fable_art')
import numpy as np
from PIL import Image
from px import *
import px

D = '/home/claude/fable_art/enemies_2/'
BG = (0x16, 0x28, 0x5c, 255)

# ---- extra materials for this batch (dark -> light; shadows drift blue/violet) ----
col('f0', '#6a1050'); col('f1', '#c8306e'); col('f2', '#ff6a5a'); col('f3', '#ffb040')      # fox-fire pink -> orange
col('xf', '#ffb8d8'); add_rim('f0 f1', 'xf')
col('u0', '#18243a'); col('u1', '#34504e'); col('u2', '#5f8266'); col('u3', '#9cb88a')      # gaki grey-green
col('xu', '#c4e4cc'); add_rim('u0 u1 u2', 'xu')
col('p0', '#1c0f3c'); col('p1', '#43266e'); col('p2', '#70429c'); col('p3', '#a276c8')      # yomi purple skin
col('xp', '#cdb4f0'); add_rim('p0 p1 p2', 'xp')
col('n0', '#110d22'); col('n1', '#251d3c'); col('n2', '#3d3260'); col('n3', '#5d5088')      # dark tattered cloth
col('xn', '#8478c0'); add_rim('n0 n1 n2', 'xn')
col('z0', '#4a1c44'); col('z1', '#96486a'); col('z2', '#d08488'); col('z3', '#f4baa4')      # saggy pink flesh
col('xz', '#ffd8dc'); add_rim('z0 z1 z2', 'xz')
col('d0', '#101a30'); col('d1', '#213a56'); col('d2', '#3c6280'); col('d3', '#7aa4b4')      # kamikiri dusk-teal hide
col('xd', '#b0dcec'); add_rim('d0 d1 d2', 'xd')
col('j0', '#1e1c34'); col('j1', '#3c3c5a'); col('j2', '#66688a'); col('j3', '#9a9eb8')      # grey monk robe
col('xj', '#c4cce8'); add_rim('j0 j1 j2', 'xj')
col('l0', '#2a2440'); col('l1', '#6e5a62'); col('l2', '#a89080'); col('l3', '#d8c8a8')      # corpse-pale old skin
col('xl', '#f0e8d8'); add_rim('l0 l1 l2', 'xl')
add_rim('e0', 'xr')


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


def pol(c, r, deg):
    """point at radius r, angle deg (0 = left, 90 = up, screen coords)"""
    a = math.radians(deg)
    return (c[0] - math.cos(a) * r, c[1] - math.sin(a) * r)


def flame(p, mask, ramp, steps=(1, 2, 2), drift=(0, 1)):
    """emissive flame: nested bands from the dark outer colour to the hot core (core sinks toward the base)."""
    p.fill(mask, ramp[0])
    m = mask
    for i, n in enumerate(steps):
        if i + 1 >= len(ramp):
            break
        m = sh(erode(m, n), drift[0], drift[1]) & mask
        p.fill(m, ramp[i + 1])
    return mask


def tongue(base, tip, w, bend=0.0):
    """flame tongue polygon: base centre, tip, base half-width, sideways bend of the middle"""
    bx, by = base; tx, ty = tip
    dx, dy = tx - bx, ty - by
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    mx, my = bx + dx * 0.55 + nx * bend, by + dy * 0.55 + ny * bend
    return PG([(bx + nx * w, by + ny * w), (mx + nx * w * 0.55, my + ny * w * 0.55), (tx, ty),
               (mx - nx * w * 0.45, my - ny * w * 0.45), (bx - nx * w, by - ny * w)]) | E(bx, by, w, w)


def export(name, fn, WALK, ATTACK, verbose=True):
    base_c = fn()
    CW, CH = px.W, px.H
    base = crop_img(base_c.img())
    base.save(D + name + '.png')
    rows = []
    allf = [base_c]
    strips = {}
    for tag, frames in (('walk', WALK), ('attack', ATTACK)):
        cs = [fn(**f) for f in frames]
        for i, c_ in enumerate(cs):
            x0, y0, x1, y1 = c_.bbox()
            assert x0 >= 1 and y0 >= 1 and x1 <= CW - 2 and y1 <= CH - 2, (name, tag, i, (x0, y0, x1, y1), (CW, CH))
        ims = [c_.img() for c_ in cs]
        st = strip(ims, D + f'{name}_{tag}.png')
        preview(st, D + f'{name}_{tag}_preview.png', 6)
        strips[tag] = ims
    # combined preview: row 1 = static + 4 walk frames, row 2 = 3 attack frames
    sc = 6
    o = Image.new('RGBA', (CW * 5, CH * 2), BG)
    o.alpha_composite(base_c.img(), (0, 0))
    for i, im in enumerate(strips['walk']):
        o.alpha_composite(im, (CW * (i + 1), 0))
    for i, im in enumerate(strips['attack']):
        o.alpha_composite(im, (CW * i, CH))
    o.resize((o.width * sc, o.height * sc), Image.NEAREST).save(D + name + '_preview.png')
    a = np.array(base)
    semi = int(((a[:, :, 3] > 0) & (a[:, :, 3] < 255)).sum())
    if verbose:
        print(name, 'static', base.size, 'cell', (CW, CH), 'orphans', len(orphans(base)), 'semi', semi)
    return base


def zoom(name, scale=8, floor=False, out=None):
    """review helper: static sprite at big zoom on the style bg (left) and a dungeon floor colour (right)"""
    im = Image.open(D + name + '.png')
    o = Image.new('RGBA', (im.width * 2 + 2, im.height), BG)
    fl = Image.new('RGBA', im.size, (0x24, 0x20, 0x2c, 255))
    o.paste(fl, (im.width + 2, 0))
    o.alpha_composite(im, (0, 0)); o.alpha_composite(im, (im.width + 2, 0))
    o = o.resize((o.width * scale, o.height * scale), Image.NEAREST)
    o.save(out or ('/tmp/z_' + name + '.png'))


def wisp(pts, r0, r1=0.7):
    """curved tapering flame/hair lick: chain of capsules along pts, radius r0 -> r1"""
    m = np.zeros((px.H, px.W), bool)
    n = len(pts) - 1
    for i in range(n):
        ra = r0 + (r1 - r0) * i / n
        rb = r0 + (r1 - r0) * (i + 1) / n
        m |= L(pts[i][0], pts[i][1], ra, pts[i + 1][0], pts[i + 1][1], rb)
    return m
