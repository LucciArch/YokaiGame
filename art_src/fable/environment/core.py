"""Tiny RGBA pixel engine for environment tiles (hard alpha, no AA, clean clusters)."""
import numpy as np
from PIL import Image

K = '#0a0814'


def hx(s):
    if isinstance(s, tuple):
        return s
    s = s.lstrip('#')
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)


def mix(a, b, t):
    a, b = hx(a), hx(b)
    return '#%02x%02x%02x' % tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def sh(m, dx, dy):
    o = np.zeros_like(m)
    h, w = m.shape
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    o[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = m[ys0:ys1, xs0:xs1]
    return o


def dil(m):
    return m | sh(m, 1, 0) | sh(m, -1, 0) | sh(m, 0, 1) | sh(m, 0, -1)


SS = 1   # Supersampling: 2 = Hi-Res-Ebene (doppelte Pixeldichte, Koordinaten bleiben logisch)


class Cv:
    def __init__(s, w, h, bg=None, wrap=False, ss=None):
        s.ss = SS if ss is None else ss
        s.w, s.h, s.wrap = w, h, wrap
        q = s.ss
        s.a = np.zeros((h * q, w * q, 4), np.uint8)
        Y, X = np.mgrid[0:h * q, 0:w * q]
        if q == 1:
            s.Y, s.X = Y, X
        else:
            s.Y, s.X = (Y - (q - 1) / 2) / q, (X - (q - 1) / 2) / q
        if bg:
            s.a[:] = hx(bg)

    def nz(s, m):
        """Koordinaten gesetzter Pixel in logischen Einheiten"""
        ys, xs = np.nonzero(m)
        return (ys / s.ss).round().astype(int), (xs / s.ss).round().astype(int)

    @property
    def m(s):
        return s.a[:, :, 3] > 0

    def copy(s):
        o = Cv(s.w, s.h, wrap=s.wrap, ss=s.ss)
        o.a = s.a.copy()
        return o

    # ---- pixels
    def px(s, x, y, c):
        x, y = int(x), int(y)
        if s.wrap:
            x %= s.w
            y %= s.h
        if 0 <= x < s.w and 0 <= y < s.h:
            q = s.ss
            s.a[y * q:(y + 1) * q, x * q:(x + 1) * q] = hx(c)

    def hpx(s, x, y, c):
        """ein einzelnes Hi-Res-Pixel (halbe logische Koordinaten erlaubt)"""
        q = s.ss
        X, Y = int(round(x * q)), int(round(y * q))
        if 0 <= X < s.w * q and 0 <= Y < s.h * q:
            s.a[Y, X] = hx(c)

    def get(s, x, y):
        q = s.ss
        return tuple(s.a[(int(y) % s.h) * q, (int(x) % s.w) * q])

    def rect(s, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            for x in range(int(x0), int(x1) + 1):
                s.px(x, y, c)

    def hl(s, x0, x1, y, c):
        s.rect(x0, y, x1, y, c)

    def vl(s, x, y0, y1, c):
        s.rect(x, y0, x, y1, c)

    def line(s, pts, c):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
            dx, dy = abs(x1 - x0), -abs(y1 - y0)
            sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
            err = dx + dy
            while True:
                s.px(x0, y0, c)
                if x0 == x1 and y0 == y1:
                    break
                e2 = 2 * err
                if e2 >= dy:
                    err += dy
                    x0 += sx
                if e2 <= dx:
                    err += dx
                    y0 += sy

    def grid(s, x0, y0, text, legend, flip=False):
        rows = text.strip('\n').split('\n')
        for j, row in enumerate(rows):
            if flip:
                row = row[::-1]
            for i, ch in enumerate(row):
                if ch in '. ':
                    continue
                s.px(x0 + i, y0 + j, legend[ch])

    # ---- masks
    def E(s, cx, cy, rx, ry):
        return ((s.X - cx) / rx) ** 2 + ((s.Y - cy) / ry) ** 2 <= 1.0

    def R(s, x0, y0, x1, y1):
        e = 0.5 - 0.5 / s.ss
        return (s.X >= x0 - e) & (s.X <= x1 + e) & (s.Y >= y0 - e) & (s.Y <= y1 + e)

    def PG(s, pts):
        from PIL import ImageDraw
        q = s.ss
        im = Image.new('1', (s.w * q, s.h * q), 0)
        o = (q - 1) / 2
        ImageDraw.Draw(im).polygon([(int(round(x * q + o)), int(round(y * q + o))) for x, y in pts], fill=1, outline=1)
        return np.array(im, dtype=bool)

    def hline(s, pts, c):
        """dünne Linie in Hi-Res-Pixeln (logische Koordinaten)"""
        q = s.ss
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * q * 1.5) + 1
            for i in range(n + 1):
                t = i / n
                s.hpx(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)

    def fill(s, m, c, only=None):
        if only is not None:
            m = m & only
        s.a[m] = hx(c)
        return m

    def form(s, m, ramp, sd=2, hl=1, only=None, sdir=(1, 1)):
        """cel form: mid fill, shadow crescent bottom-right, light edge top-left"""
        if only is not None:
            m = m & only
        s.a[m] = hx(ramp[1])
        shad = np.zeros_like(m)
        if sd:
            k = int(round(sd * s.ss))
            shad = m & ~sh(m, -k * sdir[0], -k * sdir[1])
            s.a[shad] = hx(ramp[0])
        if hl:
            lit = m & ~sh(m, hl, hl) & ~shad
            s.a[lit] = hx(ramp[2])
        return m

    def outline(s, c=K, m=None):
        mm = s.m if m is None else m
        r = dil(mm) & ~mm
        s.a[r] = hx(c)

    def recolor(s, a, b):
        m = np.all(s.a == np.array(hx(a), np.uint8), axis=2)
        s.a[m] = hx(b)

    def blit(s, o, x, y, flipx=False, flipy=False):
        src = o.a if isinstance(o, Cv) else np.array(o.convert('RGBA'))
        x, y = x * s.ss, y * s.ss
        if flipx:
            src = src[:, ::-1]
        if flipy:
            src = src[::-1]
        h, w = src.shape[:2]
        for j in range(h):
            for i in range(w):
                if src[j, i, 3]:
                    yy, xx = y + j, x + i
                    if 0 <= yy < s.a.shape[0] and 0 <= xx < s.a.shape[1]:
                        s.a[yy, xx] = src[j, i]

    def img(s):
        return Image.fromarray(s.a, 'RGBA')


def strip(cvs, path=None):
    w, h = cvs[0].w, cvs[0].h
    q = cvs[0].ss
    out = Cv(w * len(cvs), h, ss=q)
    w *= q
    for i, c in enumerate(cvs):
        out.a[:, i * w:(i + 1) * w] = c.a
    if path:
        out.img().save(path)
    return out


def orphans(a):
    """count opaque pixels with no 4-neighbour of the same colour"""
    v = a[:, :, 0].astype(np.int64) * 65536 + a[:, :, 1] * 256 + a[:, :, 2] + (a[:, :, 3] > 0) * (1 << 24)
    p = np.pad(v, 1, constant_values=-1)
    same = (p[1:-1, 1:-1] == p[:-2, 1:-1]) | (p[1:-1, 1:-1] == p[2:, 1:-1]) | \
           (p[1:-1, 1:-1] == p[1:-1, :-2]) | (p[1:-1, 1:-1] == p[1:-1, 2:])
    return int(((~same) & (a[:, :, 3] > 0)).sum())
