"""Shared helpers for boss batch 1 (uses the approved px.py engine unchanged)."""
import sys, math, os
sys.path.insert(0, '/home/claude/fable_art')
from px import *
import px
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__)) + '/'
BG = (0x16, 0x28, 0x5c, 255)
FLOOR = (0x24, 0x20, 0x2c, 255)

# extra materials (dark -> light), shadows drift blue/violet
col('hb', '#1a1738'); px.add_rim('hb', 'xh')                                              # black human hair mid
col('p0', '#1c1040'); col('p1', '#3c1f6c'); col('p2', '#6a3c9c'); col('p3', '#a878d0')    # purple cloth
col('xp', '#b8b0f0'); px.add_rim('p0 p1 p2', 'xp')
px.add_rim('a0 a1', 'a2')
px.add_rim('e0', 'e1')


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def pol(o, ang, r):
    """point at angle (deg, screen coords: 0=right, 90=down, 180=left, 270=up)"""
    a = math.radians(ang)
    return (o[0] + math.cos(a) * r, o[1] + math.sin(a) * r)


def limb(c, a, ra, b, rb, ramp, sd=2, hl=1, only=None):
    return c.form(L(a[0], a[1], ra, b[0], b[1], rb), ramp, sd=sd, hl=hl, only=only)


def tri(o, ang, ln, w):
    """spike / tuft: base centred on o (width w), tip at angle"""
    t = pol(o, ang, ln)
    return PG([pol(o, ang + 90, w / 2), t, pol(o, ang - 90, w / 2)])


def band(a, b, t0, t1, r):
    """slab perpendicular to a->b between t0..t1 (for cuffs, stripes)"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((px.X - a[0]) * dx + (px.Y - a[1]) * dy) / (dx * dx + dy * dy)
    return (t >= t0) & (t <= t1) & L(a[0], a[1], r, b[0], b[1], r)


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


def claw_hand(c, wr, ang, ramp, lncol, n=3, spread=30, ln=6.0, fr=1.3, tr=0.8, palm=2.4, claw='b2', clen=1.6, web=True):
    """n-fingered clawed hand fanning around ang"""
    p = C()
    das = [(-spread + 2 * spread * i / (n - 1)) for i in range(n)]
    tips = [pol(wr, ang + da, ln) for da in das]
    if web:
        p.fill(PG([wr] + [lerp(wr, t, 0.72) for t in tips]), ramp[0])
    p.fill(E(wr[0], wr[1], palm, palm), ramp[0])
    for t in tips:
        p.fill(L(wr[0], wr[1], fr, t[0], t[1], tr), ramp[1])
    p.form(E(wr[0] - 0.5, wr[1] - 0.5, palm - 0.8, palm - 0.8), ramp, sd=1, hl=1)
    for t, da in zip(tips, das):
        e = pol(t, ang + da, clen)
        p.fill(L(t[0], t[1], max(tr - 0.3, 0.5), e[0], e[1], 0.4), claw)
    c.stamp(p, lncol)


def darken_core(p, m, n, pairs):
    """big core shadow on an already detailed form: push bottom-right crescent one step darker"""
    core = m & ~sh(m, -n, -n)
    for hi_, lo_ in pairs:
        p.a[core & (p.a == I(hi_))] = I(lo_)


def _bgim(im, bg, sc):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im)
    return b.resize((im.width * sc, im.height * sc), Image.NEAREST)


def export(name, fn, walk, attack, check=True):
    base_c = fn()
    base = crop_img(base_c.img())
    base.save(D + name + '.png')
    rows = []
    for tag, frames in (('walk', walk), ('attack', attack)):
        cs = [fn(**f) for f in frames]
        for i, c_ in enumerate(cs):
            x0, y0, x1, y1 = c_.bbox()
            ok = x0 >= 1 and y0 >= 1 and x1 <= px.W - 2 and y1 <= px.H - 2
            if not ok:
                print('!! EDGE', name, tag, i, (x0, y0, x1, y1), (px.W, px.H))
            assert ok or not check
        rows.append(strip([c_.img() for c_ in cs], D + f'{name}_{tag}.png'))
    cw, ch = px.W, px.H
    # 4x preview with every frame: row 1 = walk (4), row 2 = static + attack (3)
    sheet = Image.new('RGBA', (cw * 4, ch * 2), (0, 0, 0, 0))
    sheet.paste(rows[0], (0, 0))
    sheet.paste(base_c.img(), (0, ch))
    sheet.paste(rows[1], (cw, ch))
    _bgim(sheet, BG, 4).save(D + name + '_preview.png')
    # review helpers (not deliverables)
    _bgim(base, FLOOR, 5).save(f'/tmp/rev/{name}_s.png')
    _bgim(sheet, BG, 2).save(f'/tmp/rev/{name}_all.png')
    a = np.array(base)
    semi = int(((a[:, :, 3] > 0) & (a[:, :, 3] < 255)).sum())
    ncol = len({tuple(q) for q in a.reshape(-1, 4) if q[3] > 0})
    print(name, 'static', base.size, 'cell', (cw, ch), 'orphans', len(orphans(base)), 'colours', ncol, 'semi', semi)
    return base
