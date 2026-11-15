"""Tiny hand-pixel engine: indexed canvases, cel-shaded 'forms', text grids, part stamping."""
import numpy as np
from PIL import Image, ImageDraw

PAL = [(0, 0, 0, 0)]
IDX = {}


def col(name, hx):
    hx = hx.lstrip('#')
    rgba = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 255)
    if name in IDX:
        PAL[IDX[name]] = rgba
    else:
        IDX[name] = len(PAL)
        PAL.append(rgba)
    return IDX[name]


def I(c):
    if c is None:
        return 0
    return IDX[c] if isinstance(c, str) else c


W = H = 0
X = Y = None


def setsize(w, h):
    global W, H, X, Y
    W, H = w, h
    Y, X = np.mgrid[0:h, 0:w]


def E(cx, cy, rx, ry):
    return ((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2 <= 1.0


def L(x0, y0, r0, x1, y1, r1):
    """tapered capsule"""
    dx, dy = x1 - x0, y1 - y0
    d2 = dx * dx + dy * dy
    if d2 == 0:
        return E(x0, y0, r0, r0)
    t = np.clip(((X - x0) * dx + (Y - y0) * dy) / d2, 0, 1)
    px, py = x0 + t * dx, y0 + t * dy
    r = r0 + (r1 - r0) * t
    return (X - px) ** 2 + (Y - py) ** 2 <= r * r


def PG(pts):
    im = Image.new('1', (W, H), 0)
    ImageDraw.Draw(im).polygon([(int(round(x)), int(round(y))) for x, y in pts], fill=1, outline=1)
    return np.array(im, dtype=bool)


def LN(pts):
    im = Image.new('1', (W, H), 0)
    ImageDraw.Draw(im).line([(int(round(x)), int(round(y))) for x, y in pts], fill=1, width=1)
    return np.array(im, dtype=bool)


def R(x0, y0, x1, y1):
    return (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)


def sh(m, dx, dy):
    """move mask content by dx,dy"""
    o = np.zeros_like(m)
    h, w = m.shape
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    o[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = m[ys0:ys1, xs0:xs1]
    return o


def dil(m):
    return m | sh(m, 1, 0) | sh(m, -1, 0) | sh(m, 0, 1) | sh(m, 0, -1)


class C:
    def __init__(s):
        s.a = np.zeros((H, W), np.uint8)
        s.ln = np.zeros((H, W), bool)   # outline pixels (candidates for black on silhouette)

    @property
    def m(s):
        return s.a > 0

    def fill(s, m, c, only=None):
        if only is not None:
            m = m & only
        s.a[m] = I(c)
        s.ln[m] = False
        return m

    def form(s, m, ramp, sd=2, hl=1, only=None, sdir=(1, 1), hdir=(1, 1)):
        """cel-shaded form: mid fill, shadow crescent bottom-right, light top-left."""
        if only is not None:
            m = m & only
        s.a[m] = I(ramp[1])
        s.ln[m] = False
        if sd:
            shad = m & ~sh(m, -sd * sdir[0], -sd * sdir[1])
            s.a[shad] = I(ramp[0])
        else:
            shad = np.zeros_like(m)
        if hl:
            lit = m & ~sh(m, hl * hdir[0], hl * hdir[1]) & ~shad
            s.a[lit] = I(ramp[2])
        return m

    def line(s, pts, c, only=None):
        m = LN(pts)
        if only is not None:
            m = m & only
        s.a[m] = I(c)
        return m

    def px(s, x, y, c):
        if 0 <= x < W and 0 <= y < H:
            s.a[int(y), int(x)] = I(c)

    def pxs(s, pts, c):
        for x, y in pts:
            s.px(x, y, c)

    def grid(s, x0, y0, text, legend, flip=False):
        rows = [r for r in text.strip('\n').split('\n')]
        for j, row in enumerate(rows):
            if flip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch in '. ':
                    continue
                s.px(x0 + i, y0 + j, legend[ch])

    def stamp(s, p, ln='K', ring=True, dx=0, dy=0, skip=()):
        pm = sh(p.m, dx, dy)
        pa = np.roll(np.roll(p.a, dy, 0), dx, 1)
        pl = sh(p.ln, dx, dy)
        if ring:
            r = dil(pm) & ~pm
            for k_ in skip:
                r &= s.a != I(k_)
            s.a[r] = I(ln)
            s.ln[r] = True
        s.a[pm] = pa[pm]
        s.ln[pm] = pl[pm]

    def blacken(s, k='K', rim=True):
        """outline px touching transparency -> near black"""
        m = s.m
        edge = m & ~(sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1))
        s.a[edge & s.ln] = I(k)
        if rim:
            s.rim()

    def rim(s):
        """cold moonlight: first fill pixel under the outline on TOP-facing and upper-LEFT silhouette edges."""
        m = s.m
        kk = s.a == I('K')
        top = sh(~m, 0, 2) & sh(kk, 0, 1)                    # outline above, void above that
        left = sh(~m, 2, 0) & sh(kk, 1, 0) & sh(~m, 2, 1)    # outline left, void beyond (upper part of left edges)
        cand = m & ~kk & ~s.ln & (top | left)
        for n_, rc in RIM.items():
            s.a[cand & (s.a == I(n_))] = I(rc)

    def img(s):
        lut = np.array(PAL, np.uint8)
        return Image.fromarray(lut[s.a], 'RGBA')

    def bbox(s):
        ys, xs = np.nonzero(s.m)
        return xs.min(), ys.min(), xs.max(), ys.max()


def crop_img(im, margin=1):
    a = np.array(im)[:, :, 3] > 0
    ys, xs = np.nonzero(a)
    return im.crop((max(0, xs.min() - margin), max(0, ys.min() - margin),
                    min(im.width, xs.max() + 1 + margin), min(im.height, ys.max() + 1 + margin)))


def preview(im, path, scale=6, bg=(0x16, 0x28, 0x5c, 255)):
    b = Image.new('RGBA', im.size, bg)
    b.alpha_composite(im)
    b = b.resize((im.width * scale, im.height * scale), Image.NEAREST)
    b.save(path)


def strip(frames, path):
    w, h = frames[0].size
    out = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        out.paste(f, (i * w, 0))
    out.save(path)
    return out


def orphans(im):
    """count pixels with no 4-neighbour of same colour"""
    a = np.array(im).astype(np.int32)
    v = a[:, :, 0] * 65536 + a[:, :, 1] * 256 + a[:, :, 2] + (a[:, :, 3] > 0) * (1 << 24)
    p = np.pad(v, 1, constant_values=-1)
    same = (p[1:-1, 1:-1] == p[:-2, 1:-1]) | (p[1:-1, 1:-1] == p[2:, 1:-1]) | \
           (p[1:-1, 1:-1] == p[1:-1, :-2]) | (p[1:-1, 1:-1] == p[1:-1, 2:])
    o = (~same) & (a[:, :, 3] > 0)
    ys, xs = np.nonzero(o)
    return list(zip(xs.tolist(), ys.tolist()))


# ---------------- shared palette (dark / moonlit) ----------------
# every ramp runs dark -> light; shadows drift to blue-violet, lights stay warm, last step = glint only
col('K', '#0a0814')                                                                       # outline
col('r0', '#2e0a2e'); col('r1', '#6a1230'); col('r2', '#a81f2a'); col('r3', '#d2452f'); col('r4', '#f58a58')   # oni red skin
col('h0', '#0f0c22'); col('h1', '#1f1d44'); col('h2', '#474c94')                          # dark hair / mane
col('b0', '#5f4250'); col('b1', '#a8866a'); col('b2', '#dccb9c'); col('b3', '#fff6d8')    # bone, horn, claw
col('y0', '#8a4a12'); col('y1', '#d8961a'); col('y2', '#ffe24a'); col('y3', '#fffbc0')    # gold / glowing eye
col('t0', '#6e3214'); col('t1', '#b86a16'); col('t2', '#e8a530')                          # tiger pelt
col('i0', '#16162e'); col('i1', '#2f3358'); col('i2', '#5a6490'); col('i3', '#aebbe0')    # iron
col('w0', '#33202a'); col('w1', '#653c2a'); col('w2', '#96663a')                          # wood
col('q', '#24061c')                                                                       # mouth interior
col('g0', '#0a2a34'); col('g1', '#14503c'); col('g2', '#2e8236'); col('g3', '#6cb840'); col('g4', '#c8ee78')   # reptile green
col('c0', '#6a5a3a'); col('c1', '#a89a52'); col('c2', '#d8cf8a')                          # pale belly
col('s0', '#261622'); col('s1', '#553224'); col('s2', '#86562a'); col('s3', '#b98a40')    # shell / leather
col('a0', '#1f48a8'); col('a1', '#3f8ae8'); col('a2', '#9fe0ff')                          # water
col('k0', '#8a4650'); col('k1', '#c9806c'); col('k2', '#f0bc98'); col('k3', '#ffe6cc')    # human skin
col('v0', '#3e4a8c'); col('v1', '#8a98c8'); col('v2', '#d4dcf4'); col('v3', '#ffffff')    # white cloth / paper
col('m0', '#3e0c30'); col('m1', '#801634'); col('m2', '#c02634'); col('m3', '#ee5a48')    # miko red cloth
col('e0', '#c81e2a'); col('e1', '#ff5a3c')                                                # red glowing eye
# cold moonlight rim colours (one per material family)
col('xr', '#f09ab0'); col('xh', '#6f7ed0'); col('xg', '#a4ecc0'); col('xs', '#cfa8a0'); col('xt', '#f6d898')
RIM = {}
for fam, rc in (('r1 r2 r3', 'xr'), ('m1 m2 m3', 'xr'), ('h0 h1', 'xh'), ('g0 g1 g2 g3', 'xg'), ('s0 s1 s2 s3 w0 w1 w2', 'xs'),
                ('t0 t1 t2 y0 y1', 'xt'), ('i0 i1 i2', 'i3'), ('v0 v1 v2', 'v3'), ('k0 k1 k2', 'k3'),
                ('c0 c1', 'c2'), ('b0 b1', 'b2')):
    for n_ in fam.split():
        RIM[n_] = rc


def add_rim(fam, rc):
    """register a rim colour for extra palette entries: add_rim('p0 p1 p2', 'xp')"""
    for n_ in fam.split():
        RIM[n_] = rc
