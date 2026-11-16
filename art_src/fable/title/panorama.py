"""Titelbildschirm-Panorama in Ebenen (Hi-Res, 960x640 = doppelte Pixeldichte von 480x320).
Mondnacht über einem Bergschrein: Himmel mit Mond, ferne Berge, Zedernkamm mit Pagode, Nebel,
Vordergrund mit Torii, Tōrō-Laternen und Kirschbaum. Licht oben links (Mond), harte Alpha.
usage: python3 panorama.py   ->  yokai/assets/env/title/*.png"""
import math, os, random
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, '..', '..', '..', 'yokai', 'assets', 'env', 'title')
W, H = 960, 640
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
MOON = (250, 150, 64)                                     # Mittelpunkt und Radius des Mondes


def canvas(w, h=H):
    return np.zeros((h, w, 4), np.uint8)


def grid(w, h=H):
    return np.mgrid[0:h, 0:w]


def put(c, mask, rgb):
    c[mask] = (*rgb, 255)


def dither(f, w, h=H):
    """Bayer-Schwelle: True, wo der Anteil f (0..1, Array oder Zahl) den Rasterwert übersteigt."""
    yy, xx = grid(w, h)
    return np.broadcast_to(f, (h, w)) > BAYER[yy % 4, xx % 4]


def outline(c, rgb=(10, 6, 18)):
    """1-px-Umriss um alles Deckende (dicke Umrisse laut Art Bible)."""
    a = c[..., 3] > 0
    n = np.zeros_like(a)
    n[1:] |= a[:-1]; n[:-1] |= a[1:]; n[:, 1:] |= a[:, :-1]; n[:, :-1] |= a[:, 1:]
    put(c, n & ~a, rgb)


def save(c, name):
    os.makedirs(DST, exist_ok=True)
    Image.fromarray(c, 'RGBA').save(os.path.join(DST, name + '.png'))


# ------------------------------------------------------------------  Himmel
def sky():
    c = canvas(W)
    yy, xx = grid(W)
    bands = [(10, 8, 30), (16, 12, 42), (22, 16, 54), (30, 20, 64), (40, 26, 74), (54, 32, 82), (72, 40, 88), (94, 52, 92)]
    f = (yy / H) ** 1.3 * (len(bands) - 1)
    lo = np.floor(f).astype(int)
    up = dither(f - lo, W)                                # Bänder mit 4x4-Raster verzahnt (16-Bit-Verlauf)
    idx = np.clip(lo + up, 0, len(bands) - 1)
    c[..., :3] = np.array(bands, np.uint8)[idx]
    c[..., 3] = 255
    mx, my, mr = MOON
    d = np.hypot(xx - mx, yy - my)
    for r0, r1, col, k in ((mr + 6, mr + 60, (70, 60, 110), 0.55), (mr + 4, mr + 26, (120, 104, 150), 0.5)):
        f = np.clip(1 - (d - r0) / (r1 - r0), 0, 1) * k   # Hof: zwei geraffelte Lichtringe
        m = (d > mr) & dither(f, W)
        put(c, m, col)
    rng = random.Random(7)
    # Milchstraße: schräges Band aus feinem Sternenstaub
    band = np.abs((yy - 40) - (xx - 300) * 0.32) < 70 + 30 * np.sin(xx * 0.01)
    dust = band & (np.random.default_rng(3).random((H, W)) < 0.035) & (yy < 380) & (d > mr + 30)
    put(c, dust, (86, 76, 128))
    for _ in range(420):
        x, y = rng.randrange(W), int(rng.random() ** 1.6 * 420)
        if math.hypot(x - mx, y - my) < mr + 34:
            continue
        b = rng.random()
        col = rng.choice([(230, 230, 255), (255, 236, 200), (200, 214, 255)])
        if b > 0.97:                                     # helle Sterne als kleines Kreuz
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                c[y + dy, (x + dx) % W] = (*col, 255)
            c[y, x] = (255, 255, 255, 255)
        elif b > 0.8:
            c[y:y + 2, x:x + 2] = (*[v * 3 // 4 for v in col], 255)
            c[y, x] = (*col, 255)
        else:
            c[y, x] = (*[int(v * (0.45 + b * 0.5)) for v in col], 255)
    # Mondscheibe: Licht oben links, Schattensichel unten rechts, Maria
    m = d <= mr
    lx, ly = (xx - mx) / mr, (yy - my) / mr
    lit = -(lx * 0.55 + ly * 0.65) + np.sqrt(np.clip(1 - lx * lx - ly * ly, 0, 1)) * 0.6
    tones = [(150, 140, 160), (196, 186, 190), (232, 222, 206), (250, 244, 226), (255, 252, 240)]
    t = np.clip((lit + 0.55) * 2.6, 0, 4)
    ti = np.floor(t).astype(int)
    ti = np.clip(ti + dither(t - ti, W), 0, 4)
    for i, col in enumerate(tones):
        put(c, m & (ti == i), col)
    noise = np.zeros((H, W))
    for cx, cy, r in ((-0.3, -0.2, 0.32), (0.15, -0.35, 0.22), (0.25, 0.15, 0.3), (-0.2, 0.35, 0.2), (0.45, -0.05, 0.15)):
        noise += np.clip(1 - np.hypot(lx - cx, ly - cy) / r, 0, 1)
    mare = m & (noise > 0.25)
    sub = np.clip(ti - 1, 0, 4)
    for i, col in enumerate(tones):
        put(c, mare & (sub == i), col)
    for cx, cy, r in ((-0.5, 0.1, 0.07), (0.05, 0.55, 0.06), (0.6, 0.3, 0.05), (-0.1, -0.6, 0.05)):
        k = np.hypot(lx - cx, ly - cy)
        put(c, m & (k < r), tones[1])
        put(c, m & (k < r) & (k > r * 0.6) & (lx - cx + ly - cy > 0), tones[3])   # Kraterrand lichtseitig unten rechts
    rim = m & (d > mr - 2) & (lx + ly < -0.2)
    put(c, rim, (255, 255, 248))
    # Wolkenschleier vor dem Mond: lange Bänder mit beleuchteter Oberkante
    for (y0, x0, x1, th) in ((my + 26, mx - 190, mx + 150, 9), (my + 44, mx - 80, mx + 260, 7), (my - 30, mx + 70, mx + 330, 6),
                             (238, 520, 900, 8), (262, 610, 960, 6), (210, 20, 260, 6)):
        xs = np.arange(max(0, x0), min(W, x1))
        for x in xs:
            u = (x - x0) / (x1 - x0)
            h = th * math.sin(u * math.pi) ** 0.6 * (0.8 + 0.2 * math.sin(x * 0.07))
            yt, yb = int(y0 - h * 0.6), int(y0 + h * 0.4)
            near = math.hypot(x - mx, y0 - my) < mr + 40
            base, top = ((96, 82, 128), (200, 186, 210)) if near else ((44, 32, 78), (92, 74, 128))
            c[yt:yb, x] = (*base, 255)
            c[yt:yt + 2, x] = (*top, 255)
            c[yb - 1:yb, x] = (30, 22, 56, 255)
    return c


# ------------------------------------------------------------------  Berge
def ridge(w, base, amps, seed):
    rng = random.Random(seed)
    ph = [rng.random() * 6.28 for _ in amps]
    x = np.arange(w)
    y = np.full(w, float(base))
    for (a, f), p in zip(amps, ph):
        y -= a * np.sin(x * f + p)
    return y


def shade_rim(c, top, w, body, rim, rim2=None, k=2):
    """Bergkörper unter der Kammlinie top[x]; lichtseitige Kante (Hang nach links oben) heller."""
    yy, xx = grid(w)
    m = yy >= top[None, :]
    put(c, m, body)
    slope = np.gradient(top)
    lit = (slope > 0.15)[None, :] & m & (yy < top[None, :] + k + 2 * np.clip(slope, 0, 3)[None, :])
    put(c, lit, rim)
    if rim2:
        put(c, m & (yy < top[None, :] + 1) & (slope > 0.4)[None, :], rim2)


def far():
    w = 1000
    c = canvas(w)
    yy, xx = grid(w)
    top = ridge(w, 400, [(22, 0.006), (12, 0.017), (5, 0.05)], 2)
    # Heiliger Berg (Fuji-Kegel) rechts der Mitte, abgeflachter Gipfel
    cx, peak, base_hw = 690, 238, 330
    cone = peak + (np.abs(np.arange(w) - cx) - 26).clip(0) ** 1.12 * 0.62
    cone = np.where(np.abs(np.arange(w) - cx) < 26, peak + np.abs(np.arange(w) - cx) * 0.06, cone)
    top = np.minimum(top, cone)
    shade_rim(c, top, w, (34, 30, 70), (66, 62, 116), (98, 94, 150), k=3)
    # Schneekappe mit gezackter Unterkante, Lichtseite links
    snow_y = peak + 64 + 10 * np.sin(np.arange(w) * 0.21) + 6 * np.sin(np.arange(w) * 0.53)
    snow = (yy >= top[None, :]) & (yy < snow_y[None, :]) & (np.abs(xx - cx) < 140)
    put(c, snow & (xx < cx + 6), (178, 182, 222))
    put(c, snow & (xx >= cx + 6), (110, 112, 168))
    put(c, snow & (xx < cx - 10) & (yy < top[None, :] + 3), (226, 228, 250))
    # Schneerinnen nach unten
    for i, dx in enumerate((-70, -38, -12, 30, 64)):
        r = (np.abs(xx - (cx + dx) - (yy - peak) * dx / 90) < 2) & (yy >= top[None, :]) & (yy < snow_y[None, :] + 26 - i * 3)
        put(c, r, (178, 182, 222) if dx < 6 else (96, 98, 150))
    put(c, yy > 470, (34, 30, 70))
    return c


def mid():
    w = 1020
    c = canvas(w)
    yy, xx = grid(w)
    top = ridge(w, 452, [(30, 0.004), (14, 0.012), (4, 0.06)], 9)
    shade_rim(c, top, w, (22, 18, 46), (44, 40, 86))
    rng = random.Random(4)
    body, lit, dark = (16, 13, 36), (40, 40, 84), (10, 8, 24)
    # Zedern (Sugi) auf dem Kamm: gestufte Kegel
    for x in list(range(10, w, 23)):
        if 605 < x < 695:
            continue                                      # Platz für die Pagode
        x += rng.randint(-6, 6)
        h = rng.randint(46, 92)
        by = int(top[min(w - 1, x)]) + 8
        for k in range(5):
            ty = by - h + k * h // 6
            hw = 4 + k * (h // 16 + 2)
            tri = (yy >= ty) & (yy < ty + h // 3) & (np.abs(xx - x) <= (yy - ty) * hw / (h / 3) + 1)
            put(c, tri, body)
            put(c, tri & (xx < x) & (xx >= x - (yy - ty) * hw / (h / 3) - 1) & (xx < x - (yy - ty) * hw / (h / 3) + 2), lit)
        put(c, (np.abs(xx - x) <= 1) & (yy >= by - 10) & (yy < by + 4), dark)
    # Fünfstöckige Pagode auf dem Kamm
    px = 650
    gy = int(top[px]) + 6
    for k in range(5):
        fy = gy - 18 - k * 26
        hw = 46 - k * 6
        bw = hw - 14
        put(c, (yy >= fy) & (yy < fy + 18) & (np.abs(xx - px) <= bw), (20, 16, 40))
        put(c, (yy >= fy + 4) & (yy < fy + 14) & (np.abs(xx - px) <= bw - 3) & ((xx - px) % 8 < 3), (12, 10, 26))
        if k in (1, 3):                                   # warm erleuchtete Fenster
            put(c, (yy >= fy + 6) & (yy < fy + 12) & (np.abs(xx - px) <= bw - 6) & ((xx - px + 2) % 10 < 4), (255, 176, 84))
        ry = fy - 2
        curve = (np.abs(xx - px) / hw) ** 3 * 9
        roof = (yy >= ry - 6 + 0 * xx) & (yy <= ry + 2 - curve * 0) & (np.abs(xx - px) <= hw) & (yy >= ry - 6 - curve + 6 * (np.abs(xx - px) / hw))
        put(c, roof, (26, 22, 54))
        put(c, roof & (yy < ry - 3 - curve + 6 * (np.abs(xx - px) / hw) + 2) & (xx < px), (74, 72, 130))
    # Sōrin: Spitze mit Ringen
    sy = gy - 18 - 4 * 26 - 8
    put(c, (np.abs(xx - px) <= 1) & (yy >= sy - 40) & (yy < sy), (30, 26, 60))
    for k in range(6):
        put(c, (np.abs(xx - px) <= 4) & (yy == sy - 8 - k * 5), (74, 72, 130))
    put(c, (np.hypot(xx - px, yy - (sy - 44)) < 3), (120, 116, 170))
    outline(c, (8, 6, 18))
    return c


def mist():
    """Nebelband (nahtlos kachelbar, 2x Breite für Scrollen): geraffeltes Lavendel mit harter Alpha."""
    w = W * 2
    c = canvas(w)
    yy, xx = grid(w)
    for cy, amp, th, dens, col in ((458, 10, 22, 0.38, (80, 76, 132)), (480, 7, 14, 0.22, (128, 122, 176)), (505, 12, 26, 0.16, (66, 62, 116))):
        u = xx / w * math.tau
        cen = cy + amp * np.sin(u * 3) + amp * 0.6 * np.sin(u * 7 + 1)
        f = np.clip(1 - np.abs(yy - cen) / th, 0, 1) * dens * (0.7 + 0.3 * np.sin(u * 5 + 2))
        put(c, dither(f, w), col)
    return c


# ------------------------------------------------------------------  Vordergrund
def torii(c, x0, gy, sc=1.0):
    yy, xx = grid(c.shape[1])
    R0, R1, R2, R3 = (196, 64, 52), (146, 36, 40), (98, 24, 38), (62, 14, 32)
    BLK = (22, 16, 26)
    h = int(300 * sc)
    span = int(150 * sc)
    pw = int(13 * sc)
    for side in (-1, 1):                                 # Pfeiler, leicht nach innen geneigt
        px = x0 + side * span
        lean = side * -0.035
        m = (yy <= gy) & (yy >= gy - h) & (np.abs(xx - (px + (gy - yy) * lean)) <= pw + (yy - (gy - h)) * 0.012)
        put(c, m, R1)
        put(c, m & (xx - (px + (gy - yy) * lean) < -pw * 0.35), R0)
        put(c, m & (xx - (px + (gy - yy) * lean) > pw * 0.45), R2)
        base = (yy <= gy) & (yy > gy - int(22 * sc)) & (np.abs(xx - px) <= pw + 4)    # schwarzer Kamebara-Sockel
        put(c, base, BLK)
        put(c, base & (xx < px - pw), (52, 44, 58))
    ny = gy - int(220 * sc)                              # Nuki (unterer Balken)
    m = (yy >= ny) & (yy < ny + int(16 * sc)) & (np.abs(xx - x0) <= span + int(34 * sc))
    put(c, m, R1); put(c, m & (yy < ny + 4), R0); put(c, m & (yy >= ny + int(12 * sc)), R2)
    gx = (yy >= gy - h + int(40 * sc)) & (yy < ny) & (np.abs(xx - x0) <= int(18 * sc))   # Gakuzuka mit Tafel
    put(c, gx, R2)
    tab = (yy >= gy - h + int(46 * sc)) & (yy < ny - 8) & (np.abs(xx - x0) <= int(14 * sc))
    put(c, tab, BLK)
    put(c, tab & (np.abs(xx - x0) <= int(10 * sc)) & (yy >= gy - h + int(50 * sc)) & (yy < ny - 12), (40, 30, 34))
    for k in range(3):                                   # goldene Schriftzeichen-Andeutung
        ky = gy - h + int(58 * sc) + k * int(14 * sc)
        put(c, (np.abs(xx - x0) <= 5) & (yy >= ky) & (yy < ky + 3), (206, 164, 74))
        put(c, (np.abs(xx - x0) <= 1) & (yy >= ky - 3) & (yy < ky + 8), (206, 164, 74))
    ky = gy - h                                          # Shimaki + Kasagi mit aufgeschwungenen Enden
    rel = np.abs(xx - x0) / (span + 60 * sc)
    lift = rel ** 2.4 * 26 * sc
    shim = (yy >= ky + 14 * sc - lift) & (yy < ky + 30 * sc - lift) & (rel <= 1)
    put(c, shim, R1); put(c, shim & (yy < ky + 18 * sc - lift), R0); put(c, shim & (yy >= ky + 26 * sc - lift), R3)
    kas = (yy >= ky - lift) & (yy < ky + 14 * sc - lift) & (rel <= 1.06)
    put(c, kas, BLK)
    put(c, kas & (yy < ky + 3 - lift), (70, 62, 84))
    outline(c)


def toro(c, x, gy, s=1.0):
    """Stein-Tōrō mit warm leuchtendem Lichtfenster."""
    yy, xx = grid(c.shape[1])
    S0, S1, S2 = (120, 116, 134), (78, 74, 96), (44, 40, 60)
    parts = [(0, 10, 26), (10, 46, 7), (46, 56, 22), (56, 82, 15), (82, 90, 26), (90, 100, 13), (100, 106, 5)]
    for (a, b, hw) in parts:
        hw = int(hw * s)
        m = (yy <= gy - a * s) & (yy > gy - b * s) & (np.abs(xx - x) <= hw)
        if b == 90:                                       # Dach: nach außen geschwungen
            m = (yy <= gy - a * s) & (yy > gy - b * s) & (np.abs(xx - x) <= hw - (gy - a * s - yy) * 1.2)
        put(c, m, S1)
        put(c, m & (xx < x - hw * 0.4), S0)
        put(c, m & (xx > x + hw * 0.5), S2)
    win = (yy <= gy - 61 * s) & (yy > gy - 77 * s) & (np.abs(xx - x) <= 8 * s)
    put(c, win, (255, 196, 96))
    put(c, win & (np.abs(xx - x) <= 3 * s) & (yy > gy - 74 * s) & (yy < gy - 64 * s), (255, 244, 200))
    put(c, (np.abs(xx - x) <= 1) & win, S2)
    outline(c)


def sakura(c, x0, gy):
    rng = random.Random(21)
    from PIL import ImageDraw
    im = Image.new('L', (c.shape[1], H), 0)
    D = ImageDraw.Draw(im)
    tips = []

    def branch(x, y, ang, ln, w, depth):
        x2, y2 = x + math.cos(ang) * ln, y + math.sin(ang) * ln
        D.line([(x, y), (x2, y2)], fill=1 if w > 3 else 2, width=max(2, int(w)))
        if depth <= 2:                                   # Blüten auch entlang der oberen Äste, nicht nur an den Spitzen
            tips.append(((x + x2) / 2, (y + y2) / 2))
        if depth == 0:
            tips.append((x2, y2))
            return
        for da in ((-0.55, 0.42) if depth > 2 else (-0.65, 0.0, 0.5)):
            branch(x2, y2, ang + da + rng.uniform(-0.2, 0.2), ln * rng.uniform(0.6, 0.78), w * 0.62, depth - 1)

    branch(x0, gy, -1.78, 120, 24, 5)
    a = np.array(im)
    yy, xx = grid(c.shape[1])
    put(c, a > 0, (46, 28, 40))
    put(c, (a > 0) & np.roll(a == 0, 3, axis=1), (96, 64, 76))        # Rinde: Lichtkante links
    pal = [(110, 50, 86), (170, 82, 124), (222, 132, 170), (250, 192, 216), (255, 232, 240)]
    cl = np.zeros((H, c.shape[1]), np.int8) - 1
    for (tx, ty) in tips:
        for _ in range(7):
            cx, cy = tx + rng.uniform(-18, 18), ty + rng.uniform(-16, 6)
            r = rng.uniform(7, 14)
            d = np.hypot(xx - cx, (yy - cy) * 1.25)
            m = d < r
            lv = np.clip(((cx - xx) + (cy - yy)) / r * 1.6 + 2.2, 0, 4).astype(np.int8)   # oben links hell
            cl = np.where(m, np.maximum(cl, lv), cl)
    grain = np.random.default_rng(5).random(cl.shape) < 0.18
    cl = np.where(grain & (cl > 0), cl - 1, cl)
    for i, col in enumerate(pal):
        put(c, cl == i, col)
    outline(c)


def near():
    w = 1040
    c = canvas(w)
    yy, xx = grid(w)
    gy = 600
    # Boden: dunkler Hang, Kiesweg, Gras-Silhouetten
    top = ridge(w, 560, [(10, 0.008), (4, 0.03)], 13)
    put(c, yy >= top[None, :], (14, 10, 24))
    put(c, (yy >= top[None, :]) & (yy < top[None, :] + 2), (40, 36, 72))
    path = (yy >= 566) & (np.abs(xx - 520) < 60 + (yy - 566) * 2.4)
    put(c, path, (30, 26, 44))
    put(c, path & dither(np.clip((yy - 566) / 160, 0, 1) * 0.35, w) & ((xx + yy) % 5 == 0), (58, 54, 78))
    rng = random.Random(30)
    for _ in range(220):
        x = rng.randrange(w)
        if abs(x - 520) < 90:
            continue
        y = int(top[x]) + rng.randint(-2, 30)
        hgt = rng.randint(6, 18)
        lean = rng.uniform(-0.4, 0.4)
        for k in range(hgt):
            xi = int(x + lean * k)
            if 0 <= xi < w:
                c[y - k, xi] = (20, 16, 34, 255) if k < hgt - 3 else (44, 46, 76, 255)
    torii(c, 250, gy, 0.9)
    toro(c, 420, 584, 0.9)
    toro(c, 640, 584, 0.9)
    sakura(c, 1010, 620)
    return c


def build():
    for name, fn in (('sky', sky), ('far', far), ('mid', mid), ('mist', mist), ('near', near)):
        save(fn(), name)
    # Vorschau des Gesamtbilds
    out = Image.new('RGBA', (W, H))
    for n, w in (('sky', W), ('far', 1000), ('mid', 1020), ('mist', W * 2), ('near', 1040)):
        im = Image.open(os.path.join(DST, n + '.png')).crop(((w - W) // 2, 0, (w - W) // 2 + W, H))
        out.alpha_composite(im)
    out.save(os.path.join(HERE, 'preview.png'))


if __name__ == '__main__':
    build()
    print('ok')
