"""Shared helpers for enemy batch 4 (extra ramps, limb helpers, export)."""
import sys, math, os
sys.path.insert(0, '/home/claude/fable_art')
from px import *
import px
import numpy as np
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(D + '_review', exist_ok=True)

# ---- extra materials (dark -> light), each with a moonlight rim
col('n0', '#111640'); col('n1', '#1f3484'); col('n2', '#3558b8'); col('n3', '#6f94e4')   # indigo kimono
col('p0', '#5a1648'); col('p1', '#a8325e'); col('p2', '#e06c88'); col('p3', '#ffb4b0')   # pink fish
col('u0', '#170c2c'); col('u1', '#341a58'); col('u2', '#5e3490'); col('u3', '#9a6cc8')   # spider purple
col('z0', '#20203a'); col('z1', '#40465e'); col('z2', '#6e778c'); col('z3', '#a4acb8')   # stone / smoke grey
col('f0', '#a82414'); col('f1', '#f0641c'); col('f2', '#ffac28')                          # flame
col('o0', '#6e4a22'); col('o1', '#a8843a'); col('o2', '#d6b85c'); col('o3', '#f4e49a')   # straw
col('xu', '#b49cf0'); col('xn', '#8fc0ff'); col('xp', '#ffd0d8'); col('xz', '#d0dcf0'); col('xf', '#ffe08a')
add_rim('n0 n1 n2', 'xn'); add_rim('p0 p1 p2', 'xp'); add_rim('u0 u1 u2', 'xu'); add_rim('z0 z1 z2', 'xz'); add_rim('o0 o1 o2', 'o3')

DARK = {}
for ramp in ('r0 r1 r2 r3 r4', 'h0 h1 h2', 'b0 b1 b2 b3', 'y0 y1 y2 y3', 't0 t1 t2', 'i0 i1 i2 i3', 'w0 w1 w2',
             'g0 g1 g2 g3 g4', 'c0 c1 c2', 's0 s1 s2 s3', 'a0 a1 a2', 'k0 k1 k2 k3', 'v0 v1 v2 v3', 'm0 m1 m2 m3',
             'n0 n1 n2 n3', 'p0 p1 p2 p3', 'u0 u1 u2 u3', 'z0 z1 z2 z3', 'f0 f1 f2', 'o0 o1 o2 o3'):
    r = ramp.split()
    for a_, b_ in zip(r[1:], r[:-1]):
        DARK[a_] = b_
DARK['o0'] = 's1'


def darken(c, m, steps=1):
    """shift every pixel under mask one ramp step darker"""
    for _ in range(steps):
        a = c.a.copy()
        for hi, lo in DARK.items():
            c.a[m & (a == I(hi))] = I(lo)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def pol(o, ang, ln):
    """point at angle (deg, screen coords: 0=right, 90=down, 180=left, 270=up)"""
    a = math.radians(ang)
    return (o[0] + math.cos(a) * ln, o[1] + math.sin(a) * ln)


def seg(c, a, ra, b, rb, ramp, sd=1, hl=1, ln=None):
    """one limb segment as its own stamped part"""
    p = C()
    p.form(L(a[0], a[1], ra, b[0], b[1], rb), ramp, sd=sd, hl=hl)
    c.stamp(p, ln or ramp[0])


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


def flame(c, base, tips, ramp=('f0', 'f1', 'f2'), core='y3', w=3.0, ln='f0'):
    """tongues of fire: each tip = (x, y); a tapered capsule from base point(s) with inner lighter cores"""
    p = C()
    outer = np.zeros((px.H, px.W), bool); mid = outer.copy(); inn = outer.copy()
    for (b, t, ww) in [(bt[0], bt[1], bt[2] if len(bt) > 2 else w) for bt in tips]:
        outer |= L(b[0], b[1], ww, t[0], t[1], 0.6)
        q = lerp(b, t, 0.62)
        mid |= L(b[0], b[1], ww - 1.2, q[0], q[1], 0.5)
        q = lerp(b, t, 0.3)
        if ww > 2.6:
            inn |= L(b[0], b[1], ww - 2.4, q[0], q[1], 0.5)
    p.fill(outer, ramp[1]); p.fill(mid, ramp[2]); p.fill(inn, core)
    c.stamp(p, ln)
    return outer


def export(name, fn, walk, attack, static=None):
    base = crop_img(fn(**(static or {})).img())
    base.save(D + name + '.png')
    rows = []
    for tag, frames in (('walk', walk), ('attack', attack)):
        cs = [fn(**f) for f in frames]
        for i, c_ in enumerate(cs):
            x0, y0, x1, y1 = c_.bbox()
            assert x0 >= 1 and y0 >= 1 and x1 <= px.W - 2 and y1 <= px.H - 2, (name, tag, i, c_.bbox(), (px.W, px.H))
        st = strip([c_.img() for c_ in cs], D + f'{name}_{tag}.png')
        preview(st, D + f'{name}_{tag}_preview.png', 6)
        rows.append(st)
    # all-frames preview: static | walk x4  /  attack x3
    cw, ch = px.W, px.H
    Wd = max(base.width + 4 + rows[0].width, rows[1].width)
    o = Image.new('RGBA', (Wd, ch * 2), (0, 0, 0, 0))
    o.alpha_composite(base, (2, ch - base.height))
    o.alpha_composite(rows[0], (base.width + 4, 0))
    o.alpha_composite(rows[1], (0, ch))
    preview(o, D + name + '_preview.png', 6)
    # small review montage (static 6x + everything 3x) for critique passes
    bg = (0x16, 0x28, 0x5c, 255)
    s6 = Image.new('RGBA', base.size, (0x24, 0x20, 0x2c, 255)); s6.alpha_composite(base)
    s6 = s6.resize((base.width * 6, base.height * 6), Image.NEAREST)
    al = Image.new('RGBA', (cw * 4, ch * 2), bg)
    al.alpha_composite(rows[0], (0, 0)); al.alpha_composite(rows[1], (0, ch))
    al = al.resize((al.width * 3, al.height * 3), Image.NEAREST)
    rv = Image.new('RGBA', (s6.width + 8 + al.width, max(s6.height, al.height)), (40, 40, 40, 255))
    rv.paste(s6, (0, 0)); rv.paste(al, (s6.width + 8, 0))
    rv.save(D + '_review/' + name + '.png')
    a = np.array(base)
    semi = int(((a[:, :, 3] > 0) & (a[:, :, 3] < 255)).sum())
    print(name, 'static', base.size, 'cell', (cw, ch), 'orphans', len(orphans(base)), 'semi', semi)
