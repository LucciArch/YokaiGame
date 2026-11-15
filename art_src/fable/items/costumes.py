"""Verwandlungs-Kostüme für die Spielfigur (Hi-Res, Stil der Item-Symbole).
Erzeugt yokai/assets/costume/<name>.png als Bildstreifen + costume.json mit Ankerpunkten.

'back'-Teile: Leinwand 96x84, Anker (48, 46) = Körpermitte der Figur, liegen HINTER der Figur.
'head'-Teile: Leinwand 64x48, Anker (32, 34) = Kopfoberkante, liegen VOR der Figur.
Alle Teile sind für eine nach LINKS blickende Figur gezeichnet (Rücken = rechts)."""
import json
import os
from ihelp import *

OUT = os.path.join(HERE, '..', '..', '..', 'yokai', 'assets', 'costume')
BACK = (96, 84, 48, 46)
HEAD = (64, 48, 32, 34)
META = {}


def outline_img(c):
    a = c.idx()
    m = a > 0
    o = dil(m) & ~m
    a[o] = IDX['K']
    lut = np.array(PAL, np.uint8)
    return Image.fromarray(lut[a], 'RGBA')


def strip(name, frames, kind, layer):
    ims = [outline_img(f) for f in frames]
    w, h = ims[0].size
    st = Image.new('RGBA', (w * len(ims), h), (0, 0, 0, 0))
    for i, im in enumerate(ims):
        st.paste(im, (i * w, 0))
    os.makedirs(OUT, exist_ok=True)
    st.save(os.path.join(OUT, name + '.png'))
    cw, ch, ax, ay = BACK if kind == 'back' else HEAD
    META[name] = dict(n=len(ims), w=w, h=h, ax=ax, ay=ay, layer=layer)


# ------------------------------------------------------------------ Rücken-Teile
def fox_tails(ph, n=3, fam='orange', tip='white'):
    c = Cv(*BACK[:2])
    for k in range(n):
        base = (52, 56)
        ang = math.radians(-112 + k * 40 + math.sin(ph * math.tau + k) * 5)
        pts = []
        for j in range(9):
            t = j / 8
            r = 4 + t * 34
            curl = math.sin(ph * math.tau + k * 1.3 + t * 2.4) * 4 * t
            x = base[0] + math.cos(ang) * r + 10 * t * t + curl
            y = base[1] + math.sin(ang) * r
            pts.append((x, y, 2.2 + 5.2 * (t ** 0.6) * (1 - 0.3 * t)))
        m = tube(pts, fam, c, 2, 1)
        tipm = m & E(pts[-1][0], pts[-1][1], 9.5, 9.5)
        c.form(tipm, 'vwW', 1, 1)
        for j in (3, 5):                                              # Fellsträhnen
            x, y, r_ = pts[j]
            c.line([(x - r_ * 0.4, y), (x + r_ * 0.3, y - r_ * 0.6)], '9')
    return c


def wings(ph, fam='black', fam2='indigo'):
    c = Cv(*BACK[:2])
    lift = math.sin(ph * math.tau) * 6
    for side in (1, -1):
        sh_ = (48 + side * 5, 42)
        el = (48 + side * 20, 27 - lift)
        tp = (48 + side * 40, 17 - lift * 1.6)
        # Schwungfedern hängen von Arm und Hand nach unten-außen
        for j in range(9):
            t = j / 8
            if t < 0.4:
                f = t / 0.4
                bx, by = sh_[0] + (el[0] - sh_[0]) * f, sh_[1] + (el[1] - sh_[1]) * f
            else:
                f = (t - 0.4) / 0.6
                bx, by = el[0] + (tp[0] - el[0]) * f, el[1] + (tp[1] - el[1]) * f
            ln = 12 + 12 * t
            ang = math.radians(100 - 55 * t) if side > 0 else math.radians(80 + 55 * t)
            ex, ey = bx + math.cos(ang) * ln, by + math.sin(ang) * ln
            c.form(L(bx, by, 3.2, ex, ey, 1.2), RAMP3[fam], 1, 1)
        arm = L(sh_[0], sh_[1], 4.2, el[0], el[1], 3.4) | L(el[0], el[1], 3.4, tp[0], tp[1], 1.4)
        c.form(arm, RAMP3[fam2], 1, 1)
        cov = L(sh_[0], sh_[1] + 4, 5, el[0], el[1] + 5, 4)
        c.form(cov, RAMP3[fam2], 2, 1)
    return c


def halo(ph):
    c = Cv(*HEAD[:2])
    cx, cy = 32, 34 + 2
    for k in range(16):
        a = k * math.tau / 16 + ph * math.tau / 16
        r1 = 19 if k % 2 == 0 else 16
        c.form(L(cx + math.cos(a) * 12, cy + math.sin(a) * 12, 1.4, cx + math.cos(a) * r1, cy + math.sin(a) * r1, 0.4), 'gyY', 0, 1)
    ring = E(cx, cy, 13, 13) & ~E(cx, cy, 10.6, 10.6)
    c.form(ring, 'gyY', 1, 1)
    return c


def drum_ring(ph):
    c = Cv(*BACK[:2])
    cx, cy = 48, 34
    hoop = E(cx, cy, 30, 24) & ~E(cx, cy, 28, 22)
    c.fill(hoop, 'd')
    for k in range(8):
        a = k * math.tau / 8 + 0.2
        x, y = cx + math.cos(a) * 29, cy + math.sin(a) * 23
        if y > cy + 12:
            continue                                                 # untere Trommeln verdeckt die Figur
        c.form(E(x, y, 6, 6), 'qrR', 1, 1, ring='K')
        c.form(E(x, y, 3.6, 3.6), 'bBi', 0, 1)
        c.fill(E(x, y, 1.4, 1.4) & ~E(x, y, 0.5, 0.5), 'q')
    if ph % 2:
        c.line([(cx - 4, cy - 30), (cx - 8, cy - 22), (cx - 2, cy - 22), (cx - 6, cy - 14)], 'Y', 2)
    return c


def seal(ph):
    c = Cv(*BACK[:2])
    cx, cy = 48, 46
    ring = E(cx, cy, 34, 12) & ~E(cx, cy, 31, 10)
    c.fill(ring, 'P')
    pts = []
    for k in range(6):
        a = -math.pi / 2 + k * 2 * math.tau / 5 + ph * math.tau / 20
        pts.append((cx + math.cos(a) * 31, cy + math.sin(a) * 10))
    c.line(pts, 'X', 1)
    for k in range(5):
        a = -math.pi / 2 + k * math.tau / 5 + ph * math.tau / 20
        c.form(E(cx + math.cos(a) * 33, cy + math.sin(a) * 11, 2, 2), 'nvW', 0, 1)
    return c


def flame_aura(ph, fam='crimson'):
    c = Cv(*BACK[:2])
    for k in range(7):
        x = 22 + k * 8.5
        h = 22 + 10 * math.sin(ph * math.tau + k * 1.7) + (8 if 2 <= k <= 4 else 0)
        base = 70
        c.form(PG([(x - 6, base), (x - 3, base - h * 0.6), (x, base - h), (x + 3, base - h * 0.55), (x + 6, base)]), RAMP3[fam], 1, 1)
    return c


def wisps(ph):
    c = Cv(*BACK[:2])
    for k in range(3):
        a = ph * math.tau + k * math.tau / 3
        x, y = 48 + math.cos(a) * 34, 38 + math.sin(a) * 14
        c.form(PG([(x, y - 9), (x + 4, y), (x, y + 4), (x - 4, y)]), 'zaA', 1, 1)
        c.fill(E(x, y, 1.6, 2), 'W')
    return c


def scale_tail(ph):
    c = Cv(*BACK[:2])
    pts = []
    for j in range(9):
        t = j / 8
        x = 56 + t * 30 + math.sin(ph * math.tau + t * 4) * 3
        y = 58 - t * 30 + math.sin(t * 5 + ph * math.tau) * 6
        pts.append((x, y, 5.5 - t * 4))
    m = tube(pts, 'jade', c, 2, 1)
    for j in range(0, 8):
        x, y, r = pts[j]
        c.fill(E(x, y - r * 0.4, max(1, r * 0.5), 1) & m, '6')
    c.form(PG([(pts[-1][0], pts[-1][1] - 4), (pts[-1][0] + 8, pts[-1][1] - 9), (pts[-1][0] + 4, pts[-1][1] + 2)]), 'gyY', 1, 1)
    return c


def tanuki_tail(ph):
    c = Cv(*BACK[:2])
    sway = math.sin(ph * math.tau) * 3
    pts = [(54, 60, 4), (64, 58, 7), (74, 52 + sway, 8), (80, 44 + sway, 7), (82, 37 + sway, 4)]
    m = tube(pts, 'wood', c, 2, 1)
    for x in (66, 74):
        c.fill(m & (abs(px.X - x) <= 1.5), 'j')
    c.form(m & (px.Y < 40 + sway), 'khH', 1, 1)
    return c


# ------------------------------------------------------------------ Kopf-Teile
def fox_ears():
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        x = 32 + sx * 9
        c.form(PG([(x - 6, 38), (x + sx * 4, 18), (x + 6, 38)]), '789', 1, 1)
        c.form(PG([(x - 3, 36), (x + sx * 3, 24), (x + 3, 36)]), 'vwW', 0, 0)
        c.form(PG([(x + sx * 2, 22), (x + sx * 4, 18), (x + sx * 5, 23)]), 'khH', 0, 0)
    return c


def oni_horns():
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        x = 32 + sx * 7
        tube([(x, 38, 3.4), (x + sx * 3, 30, 2.6), (x + sx * 7, 23, 1.6), (x + sx * 8, 18, 0.6)], 'bone', c, 1, 1)
        c.fill(R(x - 3, 36, x + 3, 38), 'U')
    return c


def tengu_cap():
    c = Cv(*HEAD[:2])
    c.form(PG([(23, 38), (32, 20), (41, 38)]), 'khH', 1, 1)       # Tokin
    c.form(E(32, 37, 10, 3), 'khH', 0, 1)
    c.fill(E(32, 29, 2.2, 2.2), 'R')
    for x in (27, 37):
        c.form(E(x, 40, 1.6, 1.6), 'nvW', 0, 1)
    return c


def yurei_band():
    c = Cv(*HEAD[:2])
    c.form(PG([(27, 44), (37, 44), (32, 36)]), 'nvW', 1, 1)
    c.line([(22, 45), (42, 45)], 'w')
    return c


def ryu_antlers():
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        x = 32 + sx * 7
        tube([(x, 38, 2.4), (x + sx * 4, 28, 1.8), (x + sx * 9, 20, 1.0)], 'jade', c, 1, 1)
        tube([(x + sx * 4, 29, 1.4), (x + sx * 10, 27, 0.8)], 'jade', c, 0, 1)
        tube([(x + sx * 6, 24, 1.2), (x + sx * 3, 17, 0.6)], 'jade', c, 0, 1)
    return c


def tanuki_ears():
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        c.form(E(32 + sx * 10, 32, 6, 6), 'jdD', 1, 1)
        c.form(E(32 + sx * 10, 33, 3, 3), 'khH', 0, 0)
    c.form(REL(31, 25, 8, 3, -20), 'FfG', 1, 1)                       # Verwandlungsblatt auf dem Kopf
    c.line([(25, 27), (37, 23)], 'F')
    return c


def eboshi():
    c = Cv(*HEAD[:2])
    c.form(PG([(25, 39), (24, 26), (30, 15), (38, 16), (40, 30), (39, 39)]), 'khH', 2, 1)
    c.line([(24, 37), (40, 37)], 'H')
    c.line([(25, 40), (39, 40)], 'n')
    return c


def build():
    phases = [i / 4 for i in range(4)]
    strip('kitsune_back', [fox_tails(p) for p in phases], 'back', 'back')
    strip('kitsune_head', [fox_ears()], 'head', 'front')
    strip('tengu_back', [wings(p) for p in phases], 'back', 'back')
    strip('tengu_head', [tengu_cap()], 'head', 'front')
    c = [wings(p, 'white', 'white') for p in phases]
    strip('fly_back', c, 'back', 'back')
    strip('kami_head', [halo(p) for p in phases], 'head', 'back')
    strip('raijin_back', [drum_ring(i) for i in range(4)], 'back', 'back')
    strip('shikigami_back', [seal(i) for i in range(4)], 'back', 'back')
    strip('shikigami_head', [eboshi()], 'head', 'front')
    strip('oni_back', [flame_aura(p) for p in phases], 'back', 'back')
    strip('oni_head', [oni_horns()], 'head', 'front')
    strip('yurei_back', [wisps(p) for p in phases], 'back', 'front')
    strip('yurei_head', [yurei_band()], 'head', 'front')
    strip('ryu_back', [scale_tail(p) for p in phases], 'back', 'back')
    strip('ryu_head', [ryu_antlers()], 'head', 'front')
    strip('tanuki_back', [tanuki_tail(p) for p in phases], 'back', 'back')
    strip('tanuki_head', [tanuki_ears()], 'head', 'front')
    json.dump(META, open(os.path.join(OUT, 'costume.json'), 'w'), indent=1, sort_keys=True)
    print('Kostüme:', len(META))


if __name__ == '__main__':
    build()
