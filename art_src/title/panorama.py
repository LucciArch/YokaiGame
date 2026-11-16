"""Titelbild-Panorama in Ebenen: Mondnacht über einem See mit Torii im Wasser.
Grundebene (480x320), harte Farbstufen, Licht vom Mond oben rechts.
Ebenen: sky (Himmel, Mond, Wolken, Wasser), far (Fuji-Kette + Spiegelung), mid (Zedernkamm,
Pagode + Spiegelung), fog (Nebelbänder), near (Torii im See, Ufer, Schilf, Tōrō, Kirschzweig).
usage: python3 panorama.py"""
import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, '..', '..', 'yokai', 'assets', 'env', '_title')
W, H = 480, 320
HZ = 214                     # Horizont / Seeufer hinten
MX, MY, MR = 388, 64, 21     # Mond
PAR = {'far': 8, 'mid': 16, 'fog': 24, 'near': 32}   # Parallaxe: Überbreite je Seite


def hx(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))


K = hx('#0a0814')
SKY = [hx(c) for c in ('#07061a', '#0b0a22', '#100e2c', '#151236', '#1b1640', '#221a4a', '#2b2052', '#36265a', '#432c5e')]


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.zeros((h, w, 4), np.uint8)

    def poly(self, pts, c, alpha=255):
        m = Image.new('1', (self.w, self.h), 0)
        ImageDraw.Draw(m).polygon([(round(x), round(y)) for x, y in pts], fill=1, outline=1)
        self.mask(np.array(m, bool), c, alpha)

    def mask(self, m, c, alpha=255):
        self.a[m] = (*c, alpha)

    def px(self, x, y, c, alpha=255):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[int(y), int(x)] = (*c, alpha)

    def rect(self, x0, y0, x1, y1, c, alpha=255):
        x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(self.w - 1, int(x1)), min(self.h - 1, int(y1))
        if x1 >= x0 and y1 >= y0:
            self.a[y0:y1 + 1, x0:x1 + 1] = (*c, alpha)

    def outline(self, c=K):
        """1-px-Umriss um alle deckenden Pixel (nur nach außen)."""
        op = self.a[..., 3] > 0
        d = op.copy()
        d[1:] |= op[:-1]; d[:-1] |= op[1:]; d[:, 1:] |= op[:, :-1]; d[:, :-1] |= op[:, 1:]
        self.a[d & ~op] = (*c, 255)

    def save(self, name):
        os.makedirs(DST, exist_ok=True)
        Image.fromarray(self.a, 'RGBA').save(os.path.join(DST, name + '.png'))


def ridge(w, base, amp, rough, seed, peaks=()):
    """Kammlinie: Höhe je x, aus Sinuswellen + Zufallsstufen; peaks = (x, höhe, breite)."""
    rr = random.Random(seed)
    ph = [rr.uniform(0, 6.3) for _ in range(4)]
    ys = []
    for x in range(w):
        y = base - amp * (0.55 * math.sin(x * 0.011 + ph[0]) + 0.3 * math.sin(x * 0.029 + ph[1]) + 0.15 * math.sin(x * 0.07 + ph[2]))
        for px_, ph_, pw in peaks:
            d = abs(x - px_) / pw
            if d < 1:
                y -= ph_ * (1 - d) ** 2.1          # konkave Flanken wie beim Fuji
        ys.append(y)
    out, y = [], ys[0]
    for x in range(w):           # in 1–3-px-Stufen gehen: kantiger Pixelkamm statt glatter Kurve
        if x % rr.choice((2, 3, 4)) == 0:
            y = ys[x] + rr.uniform(-rough, rough)
        out.append(int(round(y)))
    return out


def mirror(cv, y0, dark, step=2):
    """Spiegelung unter y0: Zeilen gespiegelt, abgedunkelt, horizontal zerwellt; jede zweite Zeile Lücke."""
    rr = random.Random(7)
    src = cv.a.copy()
    for k in range(1, cv.h - y0):
        sy = y0 - k
        if sy < 0:
            break
        dy = y0 + k
        if dy >= cv.h:
            break
        if k % step == 0 and k > 6:
            continue                  # Wellenspalt
        row = src[sy].copy()
        sh = int(round(math.sin(k * 0.9) * (1 + k / 22)))
        row = np.roll(row, sh, axis=0)
        f = dark * max(0.35, 1 - k / 90)
        row[:, :3] = (row[:, :3] * f).astype(np.uint8)
        keep = row[:, 3] > 0
        cv.a[dy][keep] = row[keep]


# ------------------------------------------------------------------ Himmel + Wasser
def sky():
    cv = Canvas(W, H)
    rr = random.Random(3)
    for y in range(HZ):
        f = y / HZ
        i = min(len(SKY) - 1, int(f ** 0.9 * len(SKY)))
        cv.rect(0, y, W - 1, y, SKY[i])
    # Mondhof: konzentrische Stufen, nach außen dunkler
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - MX, (yy - MY) * 1.08)
    sky_m = yy < HZ
    for r, add in ((70, 5), (50, 10), (34, 18)):
        m = sky_m & (d < r)
        cv.a[m, :3] = np.minimum(255, cv.a[m, :3].astype(int) + np.array([add, add - 2, add + 6])).astype(np.uint8)
    # Sterne: meist einzeln, ein paar Kreuzsterne; nicht im Mondhof
    for _ in range(140):
        x, y = rr.randrange(W), rr.randrange(int(HZ * 0.75))
        if math.hypot(x - MX, y - MY) < 50:
            continue
        b = rr.choice((120, 150, 190, 230))
        cv.px(x, y, (b - 20, b - 10, b + 20 if b < 230 else 255))
    for _ in range(9):
        x, y = rr.randrange(20, W - 20), rr.randrange(8, 110)
        if math.hypot(x - MX, y - MY) < 60:
            continue
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            cv.px(x + dx, y + dy, (200, 210, 255) if dx or dy else (255, 255, 255))
    # Mond: Scheibe mit Licht oben rechts, Mare, Terminator unten links
    md = np.hypot(xx - MX, yy - MY)
    disc = md <= MR
    cv.mask(disc, hx('#dccb9c'))
    cv.mask(disc & (np.hypot(xx - MX - 5, yy - MY + 5) <= MR - 4), hx('#f2e6c0'))
    cv.mask(disc & (np.hypot(xx - MX - 8, yy - MY + 8) <= MR - 11), hx('#fff6d8'))
    cv.mask(disc & (np.hypot(xx - MX + 26, yy - MY - 20) <= MR + 9), hx('#b8a684'))   # Schattenrand unten links
    for cx, cy, rx, ry in ((-7, -4, 6, 4), (3, 6, 5, 3), (-2, 10, 3, 2), (8, -9, 3, 2), (-11, 6, 3, 3)):
        m = disc & (((xx - MX - cx) / rx) ** 2 + ((yy - MY - cy) / ry) ** 2 <= 1)
        cv.a[m, :3] = (cv.a[m, :3] * 0.84).astype(np.uint8)
    # Wolkenstreifen: dunkel mit mondbeschienener Oberkante, einer quert den Mond
    for cy, x0, x1, th in ((70, 300, 470, 3), (84, 330, 452, 2), (40, 30, 170, 2), (122, 120, 300, 3), (136, 360, 480, 2), (150, 0, 120, 2)):
        for x in range(x0, x1):
            e = min(x - x0, x1 - x) / 14
            t = int(min(th, e * th + 0.5 + math.sin(x * 0.21) * 0.6))
            if t <= 0:
                continue
            near_moon = math.hypot(x - MX, cy - MY) < 60
            cv.rect(x, cy - t, x, cy, hx('#2a2452') if not near_moon else hx('#3a3266'))
            cv.px(x, cy - t, hx('#6a6aa8') if near_moon else hx('#3e3a70'))
    # Wasser: dunkle Stufen, Glanzlinien
    WAT = [hx(c) for c in ('#1a1640', '#141234', '#100e2a', '#0c0a22', '#09081a')]
    for y in range(HZ, H):
        f = (y - HZ) / (H - HZ)
        cv.rect(0, y, W - 1, y, WAT[min(4, int(f * 5))])
    for _ in range(70):
        y = rr.randrange(HZ + 3, H - 4)
        x, ln = rr.randrange(W), rr.randrange(4, 16)
        cv.rect(x, y, x + ln, y, hx('#2a2458'))
    cv.save('sky')


# ------------------------------------------------------------------ Ferne Bergkette mit Fuji
def far():
    w = W + 2 * PAR['far']
    cv = Canvas(w, H)
    fx = 250 + PAR['far']
    top = ridge(w, HZ - 14, 14, 1.2, 11, peaks=((fx, 112, 190), (fx - 190, 22, 80), (fx + 170, 26, 90)))
    crest = min(top) + 6                         # abgeflachter Kraterrand
    top = [max(t, crest) for t in top]
    body, lit, snow, snow_sh = hx('#211c46'), hx('#3c3a74'), hx('#c8d0ee'), hx('#7a84b8')
    fr = random.Random(4)
    fing, cur = [], 0
    for x in range(w):                           # Schneefinger: in 2–4-px-Streifen wechselnd lang
        if x % fr.choice((2, 3, 4)) == 0:
            cur = fr.choice((0, 2, 5, 9, 14, 18)) * max(0.2, 1 - abs(x - fx) / 90)
        fing.append(int(cur))
    for x in range(w):
        cv.rect(x, top[x], x, HZ, body)
        # Mondlicht von rechts: Flanken, die nach rechts abfallen, hell
        if x + 1 < w and top[x + 1] > top[x]:
            cv.rect(x, top[x], x, top[x] + 2, lit)
        # Schneekappe am Fuji: oberhalb einer gezackten Linie
        sl = crest + 18 + fing[x]
        if abs(x - fx) < 80 and top[x] < sl:
            cv.rect(x, top[x], x, sl, snow if x >= fx - 2 else snow_sh)
            if x >= fx - 2 and fing[x] >= 9:
                cv.rect(x, sl - fing[x] // 2, x, sl, hx('#9aa4d0'))           # Rinnen werfen Schatten in den Schnee
    mirror(cv, HZ, 0.55)
    cv.save('far')


# ------------------------------------------------------------------ Zedernkamm mit Pagode
def mid():
    w = W + 2 * PAR['mid']
    cv = Canvas(w, H)
    rr = random.Random(21)
    top = ridge(w, HZ - 6, 8, 0.6, 5, peaks=((70, 22, 90), (w - 60, 16, 90)))
    body, lit = hx('#15122c'), hx('#24204a')
    for x in range(w):
        cv.rect(x, top[x], x, HZ + 1, body)
    # Zedern: gezackte Spitzkegel entlang des Kamms
    x = 0
    while x < w:
        th = rr.randint(10, 24)
        bw = th // 3 + 2
        by = top[min(w - 1, x)] + 2
        for k in range(th):
            half = int(bw * k / th) + (1 if k % 3 == 2 else 0)
            cv.rect(x - half, by - th + k, x + half, by - th + k, body)
            cv.px(x + half, by - th + k, lit)                     # Mondkante rechts
        x += rr.randint(5, 11)
    # Pagode (Gojū-no-tō) links auf der Kuppe
    px_ = w - 60
    base = top[px_] - 2
    roof, roof_l, wall = hx('#0e0b1e'), hx('#3a3670'), hx('#1c1834')
    y = base
    for i in range(5):
        hw = 15 - i * 2
        cv.rect(px_ - hw + 4, y - 6, px_ + hw - 4, y, wall)
        if i < 4:
            cv.rect(px_ - 1, y - 4, px_ + 1, y - 2, hx('#d8961a'))   # warmes Fenster
            cv.px(px_, y - 3, hx('#ffe24a'))
        y -= 6
        cv.rect(px_ - hw, y - 1, px_ + hw, y, roof)
        cv.px(px_ - hw - 1, y - 2, roof); cv.px(px_ + hw + 1, y - 2, roof)   # aufgebogene Traufenden
        cv.rect(px_ + 1, y - 1, px_ + hw, y - 1, roof_l)                  # Mondlicht auf der rechten Dachhälfte
        y -= 1
    cv.rect(px_, y - 12, px_, y, hx('#3a3670'))                          # Sōrin-Spitze
    for k in range(0, 10, 3):
        cv.rect(px_ - 1, y - 2 - k, px_ + 1, y - 2 - k, hx('#3a3670'))
    mirror(cv, HZ + 1, 0.6)
    cv.save('mid')


# ------------------------------------------------------------------ Nebelbänder
def fog():
    w = W + 2 * PAR['fog']
    cv = Canvas(w, H)
    rr = random.Random(9)
    for cy, amp, a in ((HZ - 4, 5, 44), (HZ + 6, 3, 30), (HZ - 22, 3, 22)):
        for x in range(w):
            t = amp + 2 * math.sin(x * 0.05 + cy) + 1.5 * math.sin(x * 0.013 + cy * 0.3)
            if t < 1:
                continue
            for y in range(int(cy - t), int(cy + t * 0.6)):
                inner = abs(y - cy) < t * 0.4
                cv.px(x, y, (150, 150, 196), a + (26 if inner else 0))
    cv.save('fog')


# ------------------------------------------------------------------ Vordergrund: Torii im See, Ufer, Tōrō, Kirschzweig
def torii(cv, cx, by):
    """Großes Ō-Torii (Ryōbu-Stil vereinfacht): Kasagi mit Schwung, Nuki, zwei Hauptsäulen."""
    V, Vd, Vl, Vk = hx('#c02634'), hx('#801634'), hx('#ee5a48'), hx('#3e0c30')
    Blk, Blk_l = hx('#16101e'), hx('#3a3254')
    ph, half = 92, 34
    top = by - ph
    for sx in (-half, half):                      # Säulen, leicht nach innen geneigt
        for y in range(top, by + 1):
            lean = int((by - y) * 0.05) * (1 if sx < 0 else -1)
            x0 = cx + sx + lean - 3
            cv.rect(x0, y, x0 + 6, y, Vd)
            cv.rect(x0 + 2, y, x0 + 5, y, V)
            cv.px(x0 + 5, y, Vl)                  # Mondlicht von rechts
        cv.rect(cx + sx - 5, by - 4, cx + sx + 5, by, Blk)       # Kamaki-Fuß
    # Nuki (unterer Balken), ragt seitlich heraus
    ny = top + 22
    cv.rect(cx - half - 12, ny, cx + half + 12, ny + 4, Vd)
    cv.rect(cx - half - 12, ny, cx + half + 12, ny + 1, V)
    # Gakuzuka (Mittelstütze mit Tafel)
    cv.rect(cx - 3, top + 6, cx + 3, ny, Vd)
    cv.rect(cx - 5, top + 9, cx + 5, top + 18, Vk)
    cv.rect(cx - 4, top + 10, cx + 4, top + 17, hx('#8a4a12'))
    cv.rect(cx - 3, top + 11, cx + 3, top + 16, hx('#d8961a'))
    # Shimaki + Kasagi: geschwungen nach oben an den Enden
    for x in range(cx - half - 22, cx + half + 23):
        d = abs(x - cx) / (half + 22)
        lift = int(round(9 * d ** 2.6))
        y = top - lift
        cv.rect(x, y + 1, x, y + 4, V if x > cx else Vd)                    # Shimaki rot
        cv.rect(x, y - 4, x, y, Blk)                                         # Kasagi schwarz
        cv.px(x, y - 4, Blk_l)
    cv.outline()


def tooro(cv, cx, by):
    """Steinlaterne (Kasuga-dōrō) mit warm leuchtendem Feuerfach."""
    S0, S1, S2 = hx('#1c1a2e'), hx('#3a3852'), hx('#5c5a7a')
    cv.rect(cx - 9, by - 4, cx + 9, by, S1)            # Kiso
    cv.rect(cx - 2, by - 22, cx + 2, by - 4, S1)       # Sao
    cv.rect(cx + 1, by - 22, cx + 2, by - 4, S2)
    cv.rect(cx - 8, by - 26, cx + 8, by - 22, S1)      # Chūdai
    cv.rect(cx - 6, by - 38, cx + 6, by - 26, S0)      # Hibukuro
    cv.rect(cx - 3, by - 35, cx + 3, by - 29, hx('#d8961a'))
    cv.rect(cx - 2, by - 34, cx + 2, by - 30, hx('#ffe24a'))
    cv.px(cx, by - 32, hx('#fffbc0'))
    for k in range(7):                                  # Kasa: geschwungenes Dach
        hw = 3 + k * 2
        cv.rect(cx - hw, by - 46 + k, cx + hw, by - 46 + k, S1)
        cv.px(cx + hw, by - 46 + k, S2)
    cv.px(cx - 15, by - 41, S1); cv.px(cx + 15, by - 41, S2)
    cv.rect(cx - 1, by - 50, cx + 1, by - 46, S1)       # Hōju
    cv.rect(cx - 2, by - 49, cx + 2, by - 48, S1)


def near():
    w = W + 2 * PAR['near']
    cv = Canvas(w, H)
    rr = random.Random(33)
    o = PAR['near']
    # Torii im Wasser + Spiegelung
    tcv = Canvas(w, H)
    torii(tcv, 84 + o, 266)
    mirror(tcv, 262, 0.45, step=2)
    cv.a = tcv.a
    # Ufer unten: dunkle Uferlinie mit Steinen
    shore = ridge(w, 302, 4, 0.8, 41)
    for x in range(w):
        cv.rect(x, shore[x], x, H - 1, hx('#0c0a18'))
        cv.px(x, shore[x], hx('#262444'))
    for _ in range(20):
        x = rr.randrange(w)
        y = shore[x] + rr.randrange(2, 10)
        r = rr.randint(2, 5)
        cv.rect(x - r, y - r // 2, x + r, y + r // 2, hx('#1a1830'))
        cv.rect(x - r + 1, y - r // 2, x + r - 1, y - r // 2, hx('#34324e'))
    # Schilf: Halme mit Mondspitzen, am dichtesten an den Rändern
    for _ in range(170):
        x = int(rr.triangular(0, w, rr.choice((0, w))))
        h = rr.randint(8, 30) + (10 if x < 60 or x > w - 70 else 0)
        y0 = shore[min(w - 1, x)] + 2
        lean = rr.uniform(-0.25, 0.35)
        for k in range(h):
            cv.px(x + int(k * lean * k / h), y0 - k, hx('#07060f') if k < h - 3 else hx('#2a2a4e'))
        if rr.random() < 0.25:                              # Rohrkolben
            tx = x + int(h * lean)
            cv.rect(tx - 1, y0 - h - 4, tx + 1, y0 - h + 1, hx('#2e1e24'))
            cv.px(tx + 1, y0 - h - 3, hx('#5a3e3a'))
    # Tōrō rechts am Ufer + Spiegelglut
    tooro(cv, w - 70, shore[w - 70] + 4)
    cv.outline()
    # Kirschzweig oben links, aus dem Bildrand hängend
    bcv = Canvas(w, H)
    bark, bark_l = hx('#2a1a24'), hx('#5a3a40')
    tips = []

    def branch(x, y, ang, ln, th, depth):
        steps = int(ln)
        for k in range(steps):
            x += math.cos(ang); y += math.sin(ang)
            ang += rr.uniform(-0.06, 0.06)
            for t in range(-int(th // 2), int(th // 2) + 1):
                bcv.px(int(x), int(y + t), bark)
            bcv.px(int(x), int(y - th // 2), bark_l)
        if depth == 0:
            tips.append((x, y))
            return
        for da in (-0.55, 0.35):
            branch(x, y, ang + da + rr.uniform(-0.2, 0.2), ln * 0.66, max(1, th * 0.6), depth - 1)

    branch(-2, 18, 0.32, 70, 5, 3)
    branch(-2, 4, 0.12, 50, 3, 2)
    P = [hx(c) for c in ('#6a2848', '#a8406a', '#e07ea4', '#ffc0d8')]
    for tx, ty in tips:
        for _ in range(55):
            a = rr.uniform(0, math.tau)
            d = rr.uniform(0, 1) ** 0.6 * 10
            x, y = int(tx + math.cos(a) * d), int(ty + math.sin(a) * d * 0.8 + 3)
            lvl = 3 if (x - tx) > 1 and (y - ty) < 0 else 2 if (x - tx) > -3 else 1   # Mond von rechts oben
            if y - ty > 6:
                lvl = 0
            bcv.rect(x, y, x + 1, y + 1, P[lvl])
            if rr.random() < 0.2:
                bcv.px(x, y, P[min(3, lvl + 1)])
    bcv.outline()
    m = bcv.a[..., 3] > 0
    cv.a[m] = bcv.a[m]
    cv.save('near')


def build():
    sky(); far(); mid(); fog(); near()
    # Vorschau
    im = Image.open(os.path.join(DST, 'sky.png')).convert('RGBA')
    for n in ('far', 'mid', 'fog', 'near'):
        l = Image.open(os.path.join(DST, n + '.png'))
        im.alpha_composite(l.crop((PAR[n], 0, PAR[n] + W, H)))
    im.resize((W * 2, H * 2), Image.NEAREST).save(os.path.join(HERE, 'preview_panorama.png'))


if __name__ == '__main__':
    build()
    print('ok')
