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
    """Buschige Kitsune-Schwänze: setzen am unteren Rücken an, schwellen auf und schwingen gegeneinander."""
    c = Cv(*BACK[:2])
    base = (54, 58)
    for k in range(n):
        ang = math.radians(-100 + k * 38 + math.sin(ph * math.tau + k * 1.4) * 6)
        pts = []
        for j in range(11):
            t = j / 10
            r = 3 + t * 32
            bend = math.sin(ph * math.tau + k * 1.3 + t * 2.0) * 3 * t + 8 * t * t
            x = base[0] + math.cos(ang) * r + bend
            y = base[1] + math.sin(ang) * r
            rad = 1.8 + 4.6 * math.sin(math.pi * min(1, t * 1.05) ** 0.75)
            pts.append((x, y, max(1.6, rad)))
        m = np.zeros((c.h, c.w), bool)
        for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
            m |= L(x0, y0, r0, x1, y1, r1)
        for j in (3, 5, 7):                                          # Fellbüschel am Rand
            x, y, r_ = pts[j]
            nx, ny = math.cos(ang + 1.57), math.sin(ang + 1.57)
            m |= E(x + nx * r_ * 0.9, y + ny * r_ * 0.9, 2.2, 2.2)
            m |= E(x - nx * r_ * 0.9 + 1, y - ny * r_ * 0.9, 1.8, 1.8)
        c.form(m, RAMP3[fam], 2, 1, ring='K')
        tx, ty, tr = pts[-1]
        c.form(m & E(tx, ty, tr + 7, tr + 7), RAMP3[tip], 1, 1)
        for j in (2, 4, 6):                                          # Fellstriche
            x, y, r_ = pts[j]
            c.line([(x - r_ * 0.3, y + r_ * 0.3), (x + r_ * 0.3, y - r_ * 0.4)], '7', only=m)
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


def kanabo(ph):
    """Oni-Gestalt: eiserner Kanabō mit Nieten schräg über dem Rücken, Glutfunken steigen auf."""
    c = Cv(*BACK[:2])
    x0, y0, x1, y1 = 44, 70, 76, 20
    grip = L(x0, y0, 2.2, x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.3, 2.6)
    head = L(x0 + (x1 - x0) * 0.3, y0 + (y1 - y0) * 0.3, 3.0, x1, y1, 5.0)
    c.form(head, '123', 2, 1, ring='K')
    c.form(grip, 'qrR', 1, 1, ring='K')
    for j in range(5):                                               # Griffwicklung
        t = 0.05 + j * 0.05
        c.fill(E(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, 2.4, 0.8) & grip, 'q')
    for j in range(7):                                               # Nieten
        t = 0.38 + j * 0.09
        cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        for side in (-1, 1):
            r = 2.4 + 2.6 * t
            sx, sy = cx + side * r * 0.8, cy + side * r * 0.45
            c.fill(E(sx, sy, 1.0, 1.0), 'y')
    for k in range(4):                                               # Glutfunken
        q = (ph + k / 4) % 1
        x = 60 + 14 * math.sin(k * 2.1 + q * 3)
        y = 60 - q * 46
        if 0 < y < c.h - 2:
            c.fill(E(x, y, 1.1, 1.1), 'N' if q > 0.5 else 'e')
    return c


def wisps(ph):
    """Hitodama: drei blassblaue Seelenflammen kreisen hinter der Gestalt, die Flammenspitze weht nach oben."""
    c = Cv(*BACK[:2])
    for k in range(3):
        a = ph * math.tau + k * math.tau / 3
        x, y = 48 + math.cos(a) * 34, 40 + math.sin(a) * 13
        lean = math.sin(a + 1.0) * 3
        flame = E(x, y, 4.0, 3.8) | PG([(x - 4, y - 0.5), (x - 2 + lean * 0.5, y - 6), (x + lean, y - 11), (x + 2 + lean * 0.4, y - 5), (x + 4, y - 0.5)])
        c.form(flame, 'zaA', 1, 1, ring='K')
        c.fill(E(x - 0.5, y + 0.3, 2.2, 2.0), 'W')
        c.fill(E(x + lean * 0.5, y - 5, 1.0, 1.6), 'A')
    return c


def scale_tail(ph):
    """Ryūjin-Schwanz: geschuppter Schlangenleib mit hellem Bauchband, Rückenzacken und Flammenquaste."""
    c = Cv(*BACK[:2])
    pts = []
    for j in range(12):
        t = j / 11
        x = 54 + t * 28 + math.sin(ph * math.tau + t * 3.5) * 3
        y = 64 - t * 40 + math.sin(t * 4.5 + ph * math.tau) * 5
        pts.append((x, y, 7.0 - t * 4.2))
    for j in range(1, 11, 2):                                        # Rückenzacken (oben-links)
        x, y, r = pts[j]
        c.form(PG([(x - r * 0.9, y - r * 0.5), (x - r - 3.5, y - r - 2.5), (x - r * 0.1, y - r * 0.9)]), 'ogy', 0, 1, ring='K')
    m = np.zeros((c.h, c.w), bool)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        m |= L(x0, y0, r0, x1, y1, r1)
    c.form(m, RAMP3['jade'], 2, 1, ring='K')
    belly = np.zeros_like(m)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):                # Bauchband (unten-rechts)
        belly |= L(x0 + r0 * 0.55, y0 + r0 * 0.4, r0 * 0.38, x1 + r1 * 0.55, y1 + r1 * 0.4, r1 * 0.38)
    c.form(belly & m, 'uBi', 0, 1)
    for j in range(1, 11):                                           # Schuppenkanten
        x, y, r = pts[j]
        c.line([(x - r * 0.6, y - r * 0.2), (x, y + r * 0.2), (x + r * 0.3, y - r * 0.3)], '4', only=m & ~belly)
    tx, ty, _ = pts[-1]
    for k in range(3):                                               # Flammenquaste an der Spitze
        a = math.radians(-60 + k * 38) + math.sin(ph * math.tau + k) * 0.25
        c.form(PG([(tx - 2, ty + 1), (tx + math.cos(a) * 11, ty + math.sin(a) * 11), (tx + 2, ty - 1)]), 'aAW', 0, 1)
    return c


def tanuki_tail(ph):
    """Bake-Danuki: dicker, buschiger Schwanz mit dunklen Ringen."""
    c = Cv(*BACK[:2])
    sway = math.sin(ph * math.tau) * 3
    pts = [(52, 62, 3.5), (61, 61, 7), (71, 56 + sway * 0.5, 9), (79, 47 + sway, 9), (83, 38 + sway, 7), (84, 31 + sway, 4)]
    m = np.zeros((c.h, c.w), bool)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        m |= L(x0, y0, r0, x1, y1, r1)
    for x, y, r in pts[2:5]:                                         # Fellbüschel
        m |= E(x + r * 0.8, y - 1, 2.2, 2.2)
    c.form(m, RAMP3['wood'], 2, 1, ring='K')
    for y in (54, 45):                                               # Ringe
        c.form(m & (abs(px.Y - y - sway * 0.6 - (px.X - 74) * 0.5) <= 2.2), 'jjd', 0, 0)
    c.form(m & (px.Y < 37 + sway), 'khH', 1, 1)
    return c


def fox_ears():
    """Fuchsohren am Scheitel: rotgold außen, cremefarben innen, schwarze Spitzen."""
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        x = 32 + sx * 8
        outer = PG([(x - 4.5, 39), (x + sx * 4, 24), (x + 4.5, 39)])
        c.form(outer, '789', 1, 1, ring='K')
        c.form(PG([(x - 2, 37), (x + sx * 3, 28), (x + 2, 37)]), 'svW', 0, 0)
        c.form(outer & (px.Y < 27), 'khH', 0, 1)
    return c


def oni_horns():
    """Zwei gebogene Oni-Hörner aus dem Haaransatz, elfenbeinfarben mit Rillen und dunkler Spitze."""
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        x = 32 + sx * 6
        pts = [(x, 38, 2.8), (x + sx * 2.5, 32, 2.2), (x + sx * 5.5, 27, 1.4), (x + sx * 6, 23, 0.6)]
        m = tube(pts, 'bone', c, 1, 1)
        for y in (35, 32, 29):
            c.fill(m & (abs(px.Y - y) < 0.6), 'u')
        c.fill(m & (px.Y < 26), 'j')
    return c


def tengu_cap():
    """Tokin der Yamabushi: kleine schwarze Kappe auf der Stirn mit roter Bommel-Schnur."""
    c = Cv(*HEAD[:2])
    c.form(PG([(26, 38), (28, 31), (32, 27), (36, 31), (38, 38)]), 'khH', 1, 1, ring='K')
    c.line([(28, 34), (36, 34)], 'h')
    for x in (26, 38):
        c.form(E(x, 39, 1.6, 1.6), 'qrR', 0, 1)
    return c


def yurei_band():
    """Hitai-kakushi: kleines weißes Totendreieck an der Stirn, zwischen Haaransatz und Augen."""
    c = Cv(*HEAD[:2])
    c.line([(24, 40), (40, 40)], 'v')
    c.form(PG([(28.5, 40), (32, 35), (35.5, 40)]), 'nvW', 1, 1, ring='K')
    return c


def ryu_antlers():
    """Hirschartiges Drachengeweih, schlank und goldbeinern, mit je zwei Enden."""
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        x = 32 + sx * 6
        tube([(x, 38, 1.9), (x + sx * 3, 31, 1.5), (x + sx * 7, 24, 0.9)], 'bone', c, 1, 1)
        tube([(x + sx * 3, 31, 1.2), (x + sx * 8, 29, 0.7)], 'bone', c, 0, 1)
        tube([(x + sx * 5, 27, 1.0), (x + sx * 4, 22, 0.5)], 'bone', c, 0, 1)
    return c


def tanuki_ears():
    """Runde Tanuki-Ohren mit schwarzem Rand und das Verwandlungsblatt auf dem Scheitel."""
    c = Cv(*HEAD[:2])
    for sx in (-1, 1):
        x = 32 + sx * 9
        ear = E(x, 36, 4.2, 4.0) & (px.Y < 38)
        c.form(ear, 'khH', 0, 1, ring='K')
        c.form(E(x, 36.5, 2.2, 2.0) & (px.Y < 38), 'jdD', 0, 0)
    leaf = REL(32, 31, 6.5, 2.8, -25)
    c.form(leaf, 'FfG', 1, 1, ring='K')
    c.line([(27, 33), (37, 29)], 'F')
    c.line([(26, 35), (28, 33)], 'F')
    return c


def eboshi():
    """Onmyōji-Eboshi: schwarzer Lackhut, nach hinten geneigt, mit Faltkante – nicht höher als ein halber Kopf."""
    c = Cv(*HEAD[:2])
    c.form(PG([(25, 38), (25, 31), (29, 24), (37, 23), (40, 28), (39, 38)]), 'khH', 2, 1, ring='K')
    c.line([(29, 25), (35, 31)], 'h')
    c.line([(25, 37), (39, 37)], 'n')
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
    strip('oni_back', [kanabo(p) for p in phases], 'back', 'back')
    strip('oni_head', [oni_horns()], 'head', 'front')
    strip('yurei_back', [wisps(p) for p in phases], 'back', 'back')
    strip('yurei_head', [yurei_band()], 'head', 'front')
    strip('ryu_back', [scale_tail(p) for p in phases], 'back', 'back')
    strip('ryu_head', [ryu_antlers()], 'head', 'front')
    strip('tanuki_back', [tanuki_tail(p) for p in phases], 'back', 'back')
    strip('tanuki_head', [tanuki_ears()], 'head', 'front')
    json.dump(META, open(os.path.join(OUT, 'costume.json'), 'w'), indent=1, sort_keys=True)
    print('Kostüme:', len(META))


if __name__ == '__main__':
    build()
