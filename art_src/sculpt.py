"""sculpt – eigenes Werkzeug für volumetrische Pixel-Art.

Idee: Figuren werden aus Körperteilen (Formen) mit Material aufgebaut. Jedes Teil
bekommt automatisch eine Wölbung (Höhenfeld aus der Distanztransformation), daraus
werden Normale und Licht (oben links) berechnet und auf die hue-verschobene Rampe
des Materials quantisiert. Teilgrenzen bekommen eine dunkle Innenlinie (selout),
der Außenrand eine Umrisslinie. Danach kommen handgesetzte Details (Augen, Falten,
Glanzlichter) als einzelne Pixel obendrauf.

Ergebnis: ruhige, ernst wirkende, „gemalte“ Pixel-Art mit sauberem Licht – ohne
Weichzeichnen, ohne Halbtransparenz, mit begrenzter Palette.
"""
import colorsys
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


def hexrgb(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def rgbhex(t):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in t)


def mix(a, b, t):
    a, b = hexrgb(a), hexrgb(b)
    return rgbhex([a[i] + (b[i] - a[i]) * t for i in range(3)])


def ramp(base, n=6, hue_shift=18.0, dark=0.62, light=0.55, sat_drop=0.35):
    """Hue-verschobene Rampe dunkel->hell (Schatten kühl/blau, Licht warm/gelb)."""
    r, g, b = [v / 255 for v in hexrgb(base)]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    out = []
    for i in range(n):
        t = i / (n - 1)
        hd = h * 360
        if t < 0.5:
            target, amt = 240.0, (0.5 - t) * 2 * hue_shift
        else:
            target, amt = 60.0, (t - 0.5) * 2 * hue_shift
        diff = ((target - hd + 180) % 360) - 180
        hd = (hd + max(-amt, min(amt, diff))) % 360
        vv = v * (1 - dark * (1 - t * 2)) if t < 0.5 else v + (1 - v) * light * (t - 0.5) * 2
        ss = s * (1 + 0.2 * (0.5 - t)) if t < 0.5 else s * (1 - sat_drop * (t - 0.5) * 2)
        rr, gg, bb = colorsys.hsv_to_rgb(hd / 360, max(0, min(1, ss)), max(0, min(1, vv)))
        out.append(rgbhex((rr * 255, gg * 255, bb * 255)))
    return out


LIGHT = np.array([-0.55, -0.65, 0.52])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


class Part:
    __slots__ = ('mask', 'mat', 'bulge', 'z', 'flat', 'rim')

    def __init__(self, mask, mat, bulge, z, flat, rim):
        self.mask, self.mat, self.bulge, self.z, self.flat, self.rim = mask, mat, bulge, z, flat, rim


class Canvas:
    """Zeichenfläche. Materialien: name -> Rampe (Liste von Hex-Farben, dunkel->hell)."""

    def __init__(self, w, h, mats, outline='#140d18', ox=0, oy=0):
        self.w, self.h = w, h
        self.mats = dict(mats)
        self.outline_col = outline
        self.parts = []
        self.details = []
        self.ox, self.oy = ox, oy
        self._z = 0

    # ---------------------------------------------------------- Formen
    def _new(self):
        im = Image.new('L', (self.w, self.h), 0)
        return im, ImageDraw.Draw(im)

    def _t(self, pts):
        return [(x + self.ox, y + self.oy) for x, y in pts]

    def _add(self, im, mat, bulge, flat, rim, cut=None):
        m = np.array(im) > 0
        if cut is not None:
            m &= ~cut
        self._z += 1
        self.parts.append(Part(m, mat, bulge, self._z, flat, rim))
        return m

    def ellipse(self, x0, y0, x1, y1, mat, bulge=1.0, flat=False, rim=True):
        im, d = self._new()
        (a, b), (c, e) = self._t([(x0, y0), (x1, y1)])
        d.ellipse([a, b, c, e], fill=255)
        return self._add(im, mat, bulge, flat, rim)

    def circle(self, cx, cy, r, mat, **kw):
        return self.ellipse(cx - r, cy - r, cx + r, cy + r, mat, **kw)

    def poly(self, pts, mat, bulge=1.0, flat=False, rim=True):
        im, d = self._new()
        d.polygon(self._t(pts), fill=255)
        return self._add(im, mat, bulge, flat, rim)

    def rect(self, x0, y0, x1, y1, mat, **kw):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], mat, **kw)

    def limb(self, pts, w0, w1, mat, bulge=1.0, flat=False, rim=True):
        """Gliedmaße / Schlauch entlang eines Pfades, Breite w0 -> w1."""
        im, d = self._new()
        P = self._t(pts)
        n = len(P) - 1
        for i in range(n):
            (xa, ya), (xb, yb) = P[i], P[i + 1]
            steps = max(1, int(math.hypot(xb - xa, yb - ya) * 2))
            for k in range(steps + 1):
                f = k / steps
                t = (i + f) / n
                rr = (w0 + (w1 - w0) * t) / 2
                x, y = xa + (xb - xa) * f, ya + (yb - ya) * f
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
        return self._add(im, mat, bulge, flat, rim)

    def erase(self, pts=None, ellipse=None):
        """Schneidet aus allen bisherigen Teilen aus."""
        im, d = self._new()
        if pts:
            d.polygon(self._t(pts), fill=255)
        if ellipse:
            (a, b), (c, e) = self._t([ellipse[:2], ellipse[2:]])
            d.ellipse([a, b, c, e], fill=255)
        m = np.array(im) > 0
        for p in self.parts:
            p.mask &= ~m

    # ---------------------------------------------------------- Details (flach)
    def px(self, x, y, col):
        self.details.append(('px', (x + self.ox, y + self.oy), col))

    def line(self, x0, y0, x1, y1, col):
        self.details.append(('line', self._t([(x0, y0), (x1, y1)]), col))

    def dpoly(self, pts, col):
        self.details.append(('poly', self._t(pts), col))

    def dellipse(self, x0, y0, x1, y1, col):
        self.details.append(('ell', self._t([(x0, y0), (x1, y1)]), col))

    # ---------------------------------------------------------- Rendern
    def render(self, outline=True, inner=True):
        H, W = self.h, self.w
        top = np.full((H, W), -1, int)
        for i, p in enumerate(self.parts):
            top[p.mask] = i
        out = np.zeros((H, W, 4), np.uint8)
        for i, p in enumerate(self.parts):
            vis = top == i
            if not vis.any():
                continue
            ramp_ = self.mats[p.mat]
            n = len(ramp_)
            if p.flat:
                idx = np.full((H, W), n // 2, int)
            else:
                dist = ndimage.distance_transform_edt(p.mask)
                rmax = max(1.0, dist.max())
                hgt = np.sqrt(np.clip(dist / rmax, 0, 1)) * rmax * p.bulge
                hgt = ndimage.gaussian_filter(hgt, 0.8)
                gy, gx = np.gradient(hgt)
                nz = np.ones_like(hgt)
                nrm = np.sqrt(gx * gx + gy * gy + nz)
                shade = (-gx * LIGHT[0] * -1 * -1 + 0) if False else None
                dot = (-gx / nrm) * LIGHT[0] + (-gy / nrm) * LIGHT[1] + (nz / nrm) * LIGHT[2]
                # Hauptlicht + leichtes Umgebungslicht, Kontrast leicht gestreckt
                val = np.clip(0.18 + 0.95 * dot, 0, 1)
                val = val ** 1.15
                idx = np.clip((val * (n - 0.01)).astype(int), 0, n - 1)
            cols = np.array([hexrgb(c) for c in ramp_], np.uint8)
            out[vis, :3] = cols[idx[vis]]
            out[vis, 3] = 255
            if inner and p.rim:
                # Teilgrenze: dunkle Innenlinie dort, wo das Teil an ein tieferes Teil grenzt
                er = ndimage.binary_erosion(vis, iterations=1, border_value=0)
                edge = vis & ~er
                below = np.zeros_like(vis)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    sh = np.roll(np.roll(top, dy, 0), dx, 1)
                    below |= (sh >= 0) & (sh < i)
                e2 = edge & below
                # Lichtseite (oben/links) nur eine Stufe dunkler, Schattenseite die dunkelste
                yy, xx = np.mgrid[0:H, 0:W]
                darkest = cols[0]
                mid = cols[max(0, min(n - 1, 1))]
                out[e2, :3] = darkest
                lit = e2 & (np.roll(top, 1, 0) != i) & (np.roll(top, -1, 0) == i)
                out[lit, :3] = mid
        alpha = out[..., 3] > 0
        if outline:
            dil = ndimage.binary_dilation(alpha, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
            ring = dil & ~alpha
            out[ring, :3] = hexrgb(self.outline_col)
            out[ring, 3] = 255
        im = Image.fromarray(out, 'RGBA')
        d = ImageDraw.Draw(im)
        for kind, data, col in self.details:
            c = hexrgb(col) + (255,)
            if kind == 'px':
                x, y = data
                if 0 <= x < W and 0 <= y < H:
                    im.putpixel((int(x), int(y)), c)
            elif kind == 'line':
                d.line([tuple(map(int, data[0])), tuple(map(int, data[1]))], fill=c)
            elif kind == 'poly':
                d.polygon([tuple(map(int, p)) for p in data], fill=c)
            elif kind == 'ell':
                d.ellipse([tuple(map(int, data[0])), tuple(map(int, data[1]))], fill=c)
        return im


def strip(frames):
    w = max(f.width for f in frames)
    h = max(f.height for f in frames)
    s = Image.new('RGBA', (w * len(frames), h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        s.paste(f, (i * w, h - f.height))
    return s


def preview(frames_list, path, scale=3, bg=(48, 52, 58), cols=4, gap=6):
    """frames_list: [(name, [PIL frames])] -> Kontaktbogen zum Anschauen."""
    rows = []
    for name, frs in frames_list:
        rows.append(frs)
    cw = max(sum(f.width for f in fr) + gap * len(fr) for fr in rows) + gap
    ch = max(max(f.height for f in fr) for fr in rows) + gap * 2
    nrow = (len(rows) + cols - 1) // cols
    sheet = Image.new('RGBA', (cw * cols, ch * nrow), bg + (255,))
    for i, fr in enumerate(rows):
        x, y = (i % cols) * cw + gap, (i // cols) * ch
        for f in fr:
            sheet.alpha_composite(f, (x, y + ch - gap - f.height))
            x += f.width + gap
    sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST).save(path)
