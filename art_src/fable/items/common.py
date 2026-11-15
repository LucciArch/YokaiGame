"""Shared engine for item icons / pickups / projectiles / HUD.
Icons are authored as character maps (one char = one pixel, see LEG) on a small char canvas `Cv`.
Big clean masses (discs, cones) come from px.py masks + cel `form`, details are text grids.
Rendering adds the 1 px near-black silhouette outline and centres the sprite in its cell."""
import os, sys, math
sys.path.insert(0, '/home/claude/fable_art')
import numpy as np
from PIL import Image
import px
from px import col, PAL, IDX, E, L, PG, R, LN, sh, dil

HERE = os.path.dirname(os.path.abspath(__file__))

# extra material: spirit purple (shadow -> blue-violet, light -> warm pink-white)
col('p0', '#3a1470'); col('p1', '#7a34c8'); col('p2', '#b678f4'); col('p3', '#ecd0ff')

LEG = {
    'K': 'K',
    'q': 'm0', 'r': 'm1', 'R': 'm2', 'e': 'm3', 'E': 'r4',       # red
    'N': 'e0', 'M': 'e1',                                        # ember red
    'o': 'y0', 'g': 'y1', 'y': 'y2', 'Y': 'y3',                  # gold
    'n': 'v0', 'v': 'v1', 'w': 'v2', 'W': 'v3',                  # white / paper
    '0': 'i0', '1': 'i1', '2': 'i2', '3': 'i3',                  # iron
    'j': 's0', 'd': 's1', 'D': 's2', 't': 's3',                  # wood / leather
    'u': 'b0', 'b': 'b1', 'B': 'b2', 'i': 'b3',                  # bone
    'z': 'a0', 'a': 'a1', 'A': 'a2',                             # spirit blue
    'F': 'g0', 'f': 'g1', 'G': 'g2', 'l': 'g3', 'L': 'g4',       # green
    'x': 'p0', 'p': 'p1', 'P': 'p2', 'X': 'p3',                  # purple
    'k': 'h0', 'h': 'h1', 'H': 'h2',                             # black lacquer / dark hair
    'c': 'c0', 'C': 'c1', 's': 'c2',                             # straw / parchment
    'm': 'k0', 'S': 'xr', 'T': 'k3',                             # sakura pink
    '7': 't0', '8': 't1', '9': 't2',                             # orange fur
}


def REL(cx, cy, a, b, deg):
    """rotated ellipse mask; deg=-45 puts the long axis toward the upper right"""
    t = math.radians(deg)
    dx, dy = px.X - cx, px.Y - cy
    u = dx * math.cos(t) + dy * math.sin(t)
    v = -dx * math.sin(t) + dy * math.cos(t)
    return (u / a) ** 2 + (v / b) ** 2 <= 1.0


def STROKE(pts, w=2):
    from PIL import ImageDraw
    im = Image.new('1', (px.W, px.H), 0)
    ImageDraw.Draw(im).line([(int(round(x)), int(round(y))) for x, y in pts], fill=1, width=w)
    return np.array(im, dtype=bool)


class Cv:
    def __init__(s, w=32, h=32):
        px.setsize(w, h)
        s.w, s.h = w, h
        s.a = np.full((h, w), '.', dtype='<U1')

    @property
    def m(s):
        return s.a != '.'

    def fill(s, m, ch, only=None):
        if only is not None:
            m = m & only
        s.a[m] = ch
        return m

    def form(s, m, ramp, sd=2, hl=1, sdir=(1, 1), hdir=(1, 1), ring=None, only=None):
        if only is not None:
            m = m & only
        if ring:
            r = dil(m) & ~m & s.m
            s.a[r] = ring
        s.a[m] = ramp[1]
        shad = np.zeros_like(m)
        if sd:
            shad = m & ~sh(m, -sd * sdir[0], -sd * sdir[1])
            s.a[shad] = ramp[0]
        if hl:
            s.a[m & ~sh(m, hl * hdir[0], hl * hdir[1]) & ~shad] = ramp[2]
        return m

    def g(s, x0, y0, text, tr=None):
        """stamp a text grid; '.'/' ' = keep, '_' = erase"""
        rows = text.strip('\n').split('\n')
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in '. ':
                    continue
                if tr:
                    ch = tr.get(ch, ch)
                x, y = x0 + i, y0 + j
                if 0 <= x < s.w and 0 <= y < s.h:
                    s.a[y, x] = '.' if ch == '_' else ch
        return s

    def line(s, pts, ch, w=1, only=None):
        m = STROKE(pts, w)
        if only is not None:
            m = m & only
        s.a[m] = ch
        return m

    def remap(s, tr, only=None):
        b = s.a.copy()
        for k, v in tr.items():
            m = b == k
            if only is not None:
                m = m & only
            s.a[m] = v
        return s

    def idx(s):
        out = np.zeros((s.h, s.w), np.uint8)
        for ch in np.unique(s.a):
            if ch == '.':
                continue
            out[s.a == ch] = IDX[LEG[ch]]
        return out


def G(text, w=32, h=32, tr=None):
    """pure text-grid icon"""
    rows = text.strip('\n').split('\n')
    gw = max(len(r) for r in rows)
    c = Cv(w, h)
    c.g(max(1, (w - gw) // 2), max(1, (h - len(rows)) // 2), text, tr)
    return c


WARN = []


def render(frames, name=''):
    """list of Cv (same size) -> list of RGBA images, outlined, centred with one shared offset"""
    if isinstance(frames, Cv):
        frames = [frames]
    w, h = frames[0].w, frames[0].h
    arrs = []
    for c in frames:
        a = c.idx()
        m = a > 0
        o = dil(m) & ~m
        a[o] = IDX['K']
        arrs.append(a)
    un = np.zeros((h, w), bool)
    for a in arrs:
        un |= a > 0
    ys, xs = np.nonzero(un)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if x0 == 0 or y0 == 0 or x1 == w - 1 or y1 == h - 1:
        # may be clipped: check that the fill itself does not touch the border
        for c in frames:
            mm = c.m
            if mm[0].any() or mm[-1].any() or mm[:, 0].any() or mm[:, -1].any():
                WARN.append('%s: fill touches cell edge' % name)
    dx = (w - (x1 - x0 + 1)) // 2 - x0
    dy = (h - (y1 - y0 + 1)) // 2 - y0
    lut = np.array(PAL, np.uint8)
    out = []
    for a in arrs:
        b = np.zeros_like(a)
        b[y0 + dy:y1 + 1 + dy, x0 + dx:x1 + 1 + dx] = a[y0:y1 + 1, x0:x1 + 1]
        out.append(Image.fromarray(lut[b], 'RGBA'))
    return out


REG = {}   # group -> list of (name, strip image, frame width)


def save(group, name, frames):
    ims = render(frames, group + '/' + name)
    d = os.path.join(HERE, group)
    os.makedirs(d, exist_ok=True)
    w, h = ims[0].size
    st = Image.new('RGBA', (w * len(ims), h), (0, 0, 0, 0))
    for i, im in enumerate(ims):
        st.paste(im, (i * w, 0))
    st.save(os.path.join(d, name + '.png'))
    REG.setdefault(group, []).append((name, st, w))
    return st
