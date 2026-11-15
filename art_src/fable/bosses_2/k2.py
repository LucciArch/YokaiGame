"""Shared helpers for boss batch 2 (engine px.py imported untouched)."""
import sys, math, os
sys.path.insert(0, '/home/claude/fable_art')
import numpy as np
from PIL import Image
import px
from px import *

D = os.path.dirname(os.path.abspath(__file__)) + '/'
BG = (0x16, 0x28, 0x5c, 255)
FLOOR = (0x24, 0x20, 0x2c, 255)

# ---- extra materials (dark -> light; shadows drift blue/violet) ----
col('hb', '#1a1738'); px.add_rim('hb', 'xh')                                             # black human hair mid
col('u0', '#5a4a8a'); col('u1', '#a896cc'); col('u2', '#ddd0ec'); col('u3', '#f8f0ff')   # corpse-pale skin (yuki-onna)
col('n0', '#0e0e24'); col('n1', '#191c40'); col('n2', '#2c3670'); col('n3', '#5a70b8')   # umibozu wet black
col('j0', '#0a2242'); col('j1', '#0f5560'); col('j2', '#1f9a84'); col('j3', '#66d8a8'); col('j4', '#d4ffe0')  # jade scales
col('z0', '#1c1a34'); col('z1', '#37385c'); col('z2', '#5f6488'); col('z3', '#989fbe')   # grey monk robe
col('o0', '#3a2440'); col('o1', '#78505c'); col('o2', '#ac8274'); col('o3', '#d8b698'); col('o4', '#f4dcc0')  # ashen giant skin
col('d0', '#120e30'); col('d1', '#1c1a56'); col('d2', '#2c3486')                         # ghost flesh (bake-kujira)
col('p0', '#1c1040'); col('p1', '#3c1f6c'); col('p2', '#6a3c9c'); col('p3', '#a878d0')   # purple cloth
col('f0', '#7a2408'); col('f1', '#d8501a'); col('f2', '#ffa63a'); col('f3', '#fff2a8')   # fox-fire orange (unused if blue)
col('xu', '#ffffff'); col('xn', '#7f94dc'); col('xj', '#b4f4d8'); col('xz', '#c4cae4'); col('xo', '#f6e2cc')
col('xd', '#5a66c8'); col('xp', '#c4b0f0')
px.add_rim('u0 u1 u2', 'xu'); px.add_rim('n0 n1 n2', 'xn'); px.add_rim('j0 j1 j2', 'xj')
px.add_rim('z0 z1 z2', 'xz'); px.add_rim('o0 o1 o2', 'xo'); px.add_rim('d0 d1', 'xd'); px.add_rim('p0 p1 p2', 'xp')
px.add_rim('a0 a1', 'a2'); px.add_rim('e0', 'e1')


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def pol(o, ang, r):
    """angle deg, screen coords: 0=right, 90=down, 180=left, 270=up"""
    a = math.radians(ang)
    return (o[0] + math.cos(a) * r, o[1] + math.sin(a) * r)


def limb(c, a, ra, b, rb, ramp, sd=2, hl=1, only=None):
    return c.form(L(a[0], a[1], ra, b[0], b[1], rb), ramp, sd=sd, hl=hl, only=only)


def tri(o, ang, ln, w):
    t = pol(o, ang, ln)
    return PG([pol(o, ang + 90, w / 2), t, pol(o, ang - 90, w / 2)])


def band(a, b, t0, t1, r):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((px.X - a[0]) * dx + (px.Y - a[1]) * dy) / (dx * dx + dy * dy)
    return (t >= t0) & (t <= t1) & L(a[0], a[1], r, b[0], b[1], r)


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


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


def tube(pts, radii):
    """union of capsules along polyline; radii = list of (t, r) keys (t 0..1) or a list per point"""
    m = np.zeros((px.H, px.W), bool)
    n = len(pts)
    if radii and isinstance(radii[0], tuple):
        ts = [k[0] for k in radii]; rs = [k[1] for k in radii]
        rr = [float(np.interp(i / (n - 1), ts, rs)) for i in range(n)]
    else:
        rr = radii
    for i in range(n - 1):
        m |= L(pts[i][0], pts[i][1], rr[i], pts[i + 1][0], pts[i + 1][1], rr[i + 1])
    return m


def at(pts, t):
    """point + unit tangent at fraction t of a polyline (by index)"""
    f = t * (len(pts) - 1)
    i = min(int(f), len(pts) - 2)
    p = lerp(pts[i], pts[i + 1], f - i)
    dx, dy = pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]
    d = math.hypot(dx, dy) or 1
    return p, (dx / d, dy / d)


def darken_core(p, m, n, pairs, d=(1, 1)):
    core = m & ~sh(m, -n * d[0], -n * d[1])
    for hi_, lo_ in pairs:
        p.a[core & (p.a == I(hi_))] = I(lo_)


def flame(c, o, h, w, ramp, lean=0, ln=None, core=None):
    """teardrop spirit flame, base centre o, height h, width w; tip bends by lean"""
    x, y = o
    tip = (x + lean, y - h)
    m = E(x, y - w * 0.45, w / 2, w / 2) | PG([(x - w / 2 + 0.6, y - w * 0.5), (x + w / 2 - 0.6, y - w * 0.5), tip])
    m |= L(x + lean * 0.4, y - h * 0.55, max(w * 0.22, 0.8), tip[0], tip[1], 0.5)
    p = C()
    p.fill(m, ramp[0])
    inner = erode(m, 1) | sh(erode(m, 1), 0, 1) & m
    p.fill(inner, ramp[1])
    p.fill(E(x, y - w * 0.4, max(w / 2 - 2, 0.9), max(w / 2 - 2, 0.9)) & m, ramp[2])
    if core:
        p.fill(E(x, y - w * 0.35, max(w / 2 - 3.4, 0.6), max(w / 2 - 3.4, 0.6)) & m, core)
    c.stamp(p, ln or ramp[0])


def _bgim(im, bg, sc):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im)
    return b.resize((im.width * sc, im.height * sc), Image.NEAREST)


def export(name, fn, walk, attack, check=True):
    base_c = fn()
    base = crop_img(base_c.img())
    base.save(D + name + '.png')
    # review helpers (not deliverables)
    _bgim(base, BG, 6 if base.width < 90 else 5).save(D + '_review/' + name + '_bg.png')
    _bgim(base, FLOOR, 4).save(D + '_review/' + name + '_floor.png')
    sil = Image.new('RGBA', base.size, (200, 200, 210, 255))
    sil.paste(Image.new('RGBA', base.size, (0, 0, 0, 255)), (0, 0), base.split()[3])
    sil.save(D + '_review/' + name + '_sil.png')
    strips = {}
    for tag, frames in (('walk', walk), ('attack', attack)):
        cs = [fn(**f) for f in frames]
        if check:
            for i, c_ in enumerate(cs):
                x0, y0, x1, y1 = c_.bbox()
                assert x0 >= 1 and y0 >= 1 and x1 <= px.W - 2 and y1 <= px.H - 2, \
                    f'{name} {tag}[{i}] touches the cell edge: bbox {x0},{y0},{x1},{y1} cell {px.W}x{px.H}'
        strips[tag] = strip([c_.img() for c_ in cs], D + f'{name}_{tag}.png')
    cw, ch = px.W, px.H
    # preview: row 1 = walk x4, row 2 = static (centred in a cell) + attack x3
    sheet = Image.new('RGBA', (cw * 4, ch * 2), (0, 0, 0, 0))
    sheet.paste(strips['walk'], (0, 0))
    sheet.paste(base, ((cw - base.width) // 2, ch + (ch - base.height) // 2))
    sheet.paste(strips['attack'], (cw, ch))
    _bgim(sheet, BG, 4).save(D + name + '_preview.png')
    for tag in ('walk', 'attack'):
        _bgim(strips[tag], BG, 2 if cw > 150 else 3).save(D + f'_review/{name}_{tag}.png')
    al = np.array(base)[:, :, 3]
    assert set(np.unique(al)) <= {0, 255}
    print(name, 'static', base.size, 'cell', (cw, ch), 'orphans', len(orphans(base)))
    return base


def zoom(name, box, sc=8, out=None, src=None):
    im = Image.open(src or (D + name + '.png')).convert('RGBA').crop(box)
    _bgim(im, BG, sc).save(out or (D + '_review/' + name + '_zoom.png'))


def rot(pt, about, deg):
    a = math.radians(deg)
    x, y = pt[0] - about[0], pt[1] - about[1]
    return (about[0] + x * math.cos(a) - y * math.sin(a), about[1] + x * math.sin(a) + y * math.cos(a))


def scales(p, m, dark, on, sx=4, sy=3, light=None, lon=None, x0=0, y0=0):
    """brick pattern of small 'v' scale marks (3 px each) where the form currently shows a colour in `on`"""
    ok = np.zeros_like(m)
    for c_ in on:
        ok |= p.a == I(c_)
    ok &= m
    okl = np.zeros_like(m)
    for c_ in (lon or ()):
        okl |= p.a == I(c_)
    okl &= m
    H_, W_ = m.shape
    for j in range(-2, H_ // sy + 2):
        for i in range(-2, W_ // sx + 2):
            x = x0 + i * sx + (j % 2) * (sx // 2); y = y0 + j * sy
            pts = [(x, y), (x + 1, y), (x + 1, y - 1)] if sx < 6 else [(x, y), (x + 1, y), (x + 2, y), (x + 2, y - 1)]
            if all(0 <= a < W_ and 0 <= b < H_ and ok[b, a] for a, b in pts):
                for a, b in pts:
                    p.a[b, a] = I(dark)
            elif light and all(0 <= a < W_ and 0 <= b < H_ and okl[b, a] for a, b in pts):
                for a, b in pts:
                    p.a[b, a] = I(light)


def lock(base, ang, ln, w, bend=20):
    """curved, tapering lock of hair / flame tongue: mask. bend = degrees the tip curls (+ = clockwise on screen)"""
    a = pol(base, ang - bend * 0.5, ln * 0.4)
    b = pol(base, ang, ln * 0.75)
    t = pol(base, ang + bend * 0.6, ln)
    cv = curve([base, a, b, t], 6)
    return tube(cv, [(0, w / 2), (0.45, w / 2 * 0.85), (0.8, w / 2 * 0.45), (1, 0.5)])
