"""Shared helpers for enemy batch 1 (lives only in this folder; engine px.py is imported untouched)."""
import sys, math, os
sys.path.insert(0, '/home/claude/fable_art')
import numpy as np
from PIL import Image
import px
from px import *

D = os.path.dirname(os.path.abspath(__file__)) + '/'
BG = (0x16, 0x28, 0x5c, 255)
FLOOR = (0x24, 0x20, 0x2c, 255)

# ---- extra materials for this batch (dark -> light, shadows drift blue/violet) ----
col('p0', '#1e1260'); col('p1', '#4a2cb4'); col('p2', '#8468f0'); col('p3', '#cfc4ff')      # onibi violet fire
col('z0', '#182634'); col('z1', '#35504a'); col('z2', '#638462'); col('z3', '#9fb888')      # gaki corpse grey-green
col('f0', '#241c30'); col('f1', '#4c4044'); col('f2', '#7e6e5c'); col('f3', '#b4a284')      # yamabiko grey-brown fur
col('d0', '#0c1238'); col('d1', '#1a2a68'); col('d2', '#30509c'); col('d3', '#6a90d4')      # isonade deep-sea blue
col('u0', '#170f2c'); col('u1', '#35224a'); col('u2', '#5c3c66'); col('u3', '#946a88')      # gyuki spider chitin
col('n0', '#472834'); col('n1', '#875644'); col('n2', '#b8855c'); col('n3', '#e2b986')      # hyosube bald skin
col('xp', '#e4dcff'); col('xz', '#c4e4c0'); col('xf', '#d4cdb8'); col('xd', '#a4c4f4'); col('xu', '#c49ab8')
px.add_rim('p0 p1', 'p3'); px.add_rim('z0 z1 z2', 'xz'); px.add_rim('f0 f1 f2', 'xf')
px.add_rim('d0 d1 d2', 'xd'); px.add_rim('u0 u1 u2', 'xu'); px.add_rim('n0 n1 n2', 'n3')


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def curve(pts, n=8):
    """Catmull-Rom through pts -> dense polyline"""
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


def tube(pts, r0, r1, radii=None):
    """union of tapered capsules along a polyline; radii = optional list per point"""
    m = np.zeros((px.H, px.W), bool)
    n = len(pts) - 1
    for i in range(n):
        if radii is not None:
            ra, rb = radii[i], radii[i + 1]
        else:
            ra, rb = r0 + (r1 - r0) * i / n, r0 + (r1 - r0) * (i + 1) / n
        m |= L(pts[i][0], pts[i][1], ra, pts[i + 1][0], pts[i + 1][1], rb)
    return m


def arc(cx, cy, r, a0, a1, th=1.0, ry=None):
    """ring segment mask; angles in degrees, screen coords (0=right, 90=down, 180=left)"""
    ry = ry or r
    dx, dy = (px.X - cx) / r, (px.Y - cy) / ry
    d = np.sqrt(dx * dx + dy * dy)
    ang = np.degrees(np.arctan2(dy, dx)) % 360
    a0 %= 360; a1 %= 360
    inr = (ang >= a0) & (ang <= a1) if a0 <= a1 else (ang >= a0) | (ang <= a1)
    return (np.abs(d - 1) * r <= th / 2 + 0.01) & inr


def spiky(cx, cy, rx, ry, n, amp, ph=0.0, lean=0.0):
    """jagged tuft blob (fur, wild hair): polygon alternating outer/inner radius"""
    pts = []
    for i in range(n * 2):
        a = ph + math.pi * i / n
        k = 1 + (amp if i % 2 == 0 else -amp * 0.35)
        pts.append((cx + math.cos(a + (lean if i % 2 == 0 else 0)) * rx * k, cy + math.sin(a + (lean if i % 2 == 0 else 0)) * ry * k))
    return PG(pts)


def glowlayers(c, m, cols, steps):
    """concentric flat layers for fire: cols dark->light, steps = erosion depth per layer"""
    c.fill(m, cols[0])
    for cl, n in zip(cols[1:], steps):
        c.fill(erode(m, n), cl)


def export(name, fn, walk, attack, quiet=False):
    base_c = fn()
    cw, ch = px.W, px.H
    base = crop_img(base_c.img())
    base.save(D + name + '.png')
    rows = [[base_c.img()]]
    info = []
    for tag, frames in (('walk', walk), ('attack', attack)):
        cs = [fn(**f) for f in frames]
        for i, c_ in enumerate(cs):
            assert (px.W, px.H) == (cw, ch)
            x0, y0, x1, y1 = c_.bbox()
            assert x0 >= 1 and y0 >= 1 and x1 <= cw - 2 and y1 <= ch - 2, (name, tag, i, (x0, y0, x1, y1), (cw, ch))
            info.append((tag, i, int(y1)))
        ims = [c_.img() for c_ in cs]
        st = strip(ims, D + f'{name}_{tag}.png')
        preview(st, D + f'{name}_{tag}_preview.png', 6)
        rows.append(ims)
    # <name>_preview.png : every frame, 6x on #16285c (row 1 static, row 2 walk, row 3 attack)
    sheet = Image.new('RGBA', (cw * 4, ch * 3), (0, 0, 0, 0))
    for r, ims in enumerate(rows):
        for i, im in enumerate(ims):
            sheet.paste(im, (i * cw, r * ch))
    preview(sheet, D + name + '_preview.png', 6)
    # small review image for critique passes
    sc = max(2, min(8, 760 // max(base.width, base.height)))
    a_ = Image.new('RGBA', (base.width * 2 + 4, base.height + 2), BG)
    a_.paste(Image.new('RGBA', (base.width + 2, base.height + 2), FLOOR), (base.width + 2, 0))
    a_.alpha_composite(base, (1, 1)); a_.alpha_composite(base, (base.width + 3, 1))
    a_.resize((a_.width * sc, a_.height * sc), Image.NEAREST).save(D + f'_review/{name}_static.png')
    s2 = max(2, min(6, 1560 // (cw * 4)))
    b_ = Image.new('RGBA', (cw * 4, ch * 2), BG)
    b_.alpha_composite(sheet.crop((0, ch, cw * 4, ch * 3)))
    b_.resize((b_.width * s2, b_.height * s2), Image.NEAREST).save(D + f'_review/{name}_anim.png')
    arr = np.array(base)
    semi = int(((arr[:, :, 3] > 0) & (arr[:, :, 3] < 255)).sum())
    if not quiet:
        print(name, 'static', base.size, 'cell', (cw, ch), 'orphans', len(orphans(base)), 'semi', semi,
              'bottoms', [b for _, _, b in info], 'static bottom', int(base_c.bbox()[3]))
    return base


def claw_hand(c, wr, ang, ramp, ln_col, spread=28, ln=6.0, n=3, claw='b2', cl=2.0, r=1.2, palm=2.2):
    """bony clawed hand; ang in degrees (180=left, 90=down)."""
    p = C()
    tips = []
    offs = [(-spread + 2 * spread * i / (n - 1)) for i in range(n)]
    for da in offs:
        a = math.radians(ang + da)
        tips.append((wr[0] + math.cos(a) * ln, wr[1] + math.sin(a) * ln))
    p.fill(E(wr[0], wr[1], palm, palm), ramp[1])
    for t in tips:
        p.fill(L(wr[0], wr[1], r, t[0], t[1], 0.7), ramp[1])
    p.fill(E(wr[0] - 0.5, wr[1] - 0.5, palm - 0.9, palm - 0.9), ramp[2])
    p.fill((p.m & ~sh(p.m, -1, -1)) & E(wr[0], wr[1], palm, palm), ramp[0])
    for t, da in zip(tips, offs):
        a = math.radians(ang + da)
        e = (t[0] + math.cos(a) * cl, t[1] + math.sin(a) * cl)
        p.fill(LN([t, e]), claw)
    c.stamp(p, ln_col)


def thin_limb(c, a, b, ra, rb, ramp, ln_col, knob=None, sd=1, hl=1):
    p = C()
    p.form(L(a[0], a[1], ra, b[0], b[1], rb), ramp, sd=sd, hl=hl)
    if knob:
        p.form(E(a[0], a[1], knob, knob), ramp, sd=1, hl=1)
    c.stamp(p, ln_col)


def fur_ticks(p, mask, mid, dark, step=(5, 4), ph=0, d=(1, 1)):
    """short 2px diagonal fur strokes where the fill is flat mid tone"""
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return
    for y in range(ys.min(), ys.max(), step[1]):
        off = ((y // step[1]) % 2) * (step[0] // 2) + ph
        for x in range(xs.min() + off, xs.max(), step[0]):
            ok = True
            for (qx, qy) in ((x, y), (x + d[0], y + d[1]), (x - 1, y), (x + d[0] + 1, y + d[1]), (x, y - 1), (x + d[0], y + d[1] + 1)):
                if not (0 <= qx < px.W and 0 <= qy < px.H) or not mask[qy, qx] or p.a[qy, qx] != I(mid):
                    ok = False
            if ok:
                p.pxs([(x, y), (x + d[0], y + d[1])], dark)


def shag(pts, r0, r1, tuft=2.6, every=2, side=(0.5, 1.0), ph=0):
    """shaggy limb: tube + hanging fur spikes along it"""
    m = tube(pts, r0, r1)
    n = len(pts) - 1
    for i in range(ph, n + 1, every):
        r = r0 + (r1 - r0) * i / max(1, n)
        x, y = pts[i]
        m |= PG([(x - 1.6, y), (x + 1.6, y), (x + side[0] * (r + tuft), y + side[1] * (r + tuft))])
    return m


def zig(p, mask, y, colr, x0=None, x1=None, period=4, amp=2, slope=0.0, on=None):
    """zig-zag fur fringe line across a form (classic 16-bit shag shorthand)"""
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return
    x0 = xs.min() if x0 is None else x0
    x1 = xs.max() if x1 is None else x1
    pts = []
    k = 0
    x = x0
    while x <= x1:
        pts.append((x, y + slope * (x - x0) + (amp if k % 2 else 0)))
        x += period / 2
        k += 1
    m = LN(pts) & erode(mask, 1)
    if on is not None:
        ok = np.zeros_like(m)
        for o in on:
            ok |= p.a == I(o)
        m &= ok
    p.a[m] = I(colr)


def tufts(base, pts):
    """add triangular hanging tufts: pts = [(bx, by, tipx, tipy, halfwidth)]"""
    m = base.copy()
    for bx, by, tx, ty, hw in pts:
        dx, dy = tx - bx, ty - by
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d * hw, dx / d * hw
        m |= PG([(bx + nx, by + ny), (bx - nx, by - ny), (tx, ty)])
    return m
