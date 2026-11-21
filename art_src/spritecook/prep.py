"""Gemeinsame Aufbereitung von SpriteCook-/KI-Bögen fürs Spiel: verkleinern, Palette, Umriss, Zellen mit Fußmitte,
Ausgabe <name>_walk.png (4) + <name>_attack.png (3) für import_fable.py. Blick im Spiel: nach links."""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

SPRITES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'yokai', 'assets', 'sprites')


def build(name, im, fg, boxes, target_h, flip=True, colors=48, k=None, roll=None):
    """im: RGB-Array des Bogens, fg: Vordergrundmaske, boxes: 7 Rechtecke (x0, y0, x1, y1), erst 4 Lauf-, dann 3 Angriffsbilder.
    target_h: Höhe der Laufbilder in Hi-Res-Pixeln. roll: optional 3 Rechtecke (geduckt, Ball A, Ball B) einer Spielfigur."""
    walk_h = max(np.ptp(np.where(fg[y0:y1, x0:x1].any(1))[0]) + 1 for x0, y0, x1, y1 in boxes[:4])
    k = k or target_h / walk_h                        # k vorgeben, wenn der Bogen ein echtes Kunst-Pixelraster hat (k = 1/Rastergröße)
    cells = []
    for i, (x0, y0, x1, y1) in enumerate(list(boxes) + list(roll or [])):
        m = fg[y0:y1, x0:x1]
        ys = np.where(m.any(1))[0]
        bot = ys.max() + 1                           # Füße unten bündig, Platz oben bleibt gleich groß
        top = max(0, bot - int(round(walk_h * 1.25)))
        if ys.min() < top or i > len(boxes):         # Ballbilder der Rolle: knapp zugeschnitten
            top = ys.min()
        m = m[top:bot]
        rgb = im[y0 + top:y0 + bot, x0:x1]
        w, h = int(round((x1 - x0) * k)), int(round((bot - top) * k))
        # Farben nur aus dem Vordergrund mitteln (sonst färbt der Grund die Kanten ein), Deckung als Alpha
        pre = Image.fromarray(np.dstack([rgb * m[..., None], m * 255]).astype(np.uint8)).resize((w, h), Image.BOX)
        p = np.array(pre).astype(float)
        al = p[..., 3:4] / 255
        col = np.where(al > 0, p[..., :3] / np.maximum(al, 1e-6), 0)
        out = np.dstack([np.clip(col, 0, 255), (al[..., 0] > 0.5) * 255]).astype(np.uint8)
        pad = Image.new('RGBA', (w + 2, h + 2)); pad.paste(Image.fromarray(out), (1, 1))
        cells.append(pad.transpose(Image.FLIP_LEFT_RIGHT) if flip else pad)
    # gemeinsame Palette, harte Pixelkanten
    sheet = Image.new('RGBA', (sum(c.width for c in cells), max(c.height for c in cells)))
    x = 0
    for c in cells:
        sheet.paste(c, (x, 0)); x += c.width
    pal = sheet.convert('RGB').quantize(colors, method=Image.MEDIANCUT)
    cells = [tidy(Image.merge('RGBA', (*c.convert('RGB').quantize(palette=pal, dither=0).convert('RGB').split(), c.split()[3])))
             for c in cells]
    if roll:
        save_roll(name, cells[7:])
        cells = cells[:7]
    H = max(c.height for c in cells)
    half = max(max(foot_cx(c), c.width - foot_cx(c)) for c in cells) + 2
    W = half * 2
    out = []
    for c in cells:
        cell = Image.new('RGBA', (W, H))
        cell.paste(c, (half - foot_cx(c), H - c.height))
        out.append(cell)
    for suffix, fr in (('_walk.png', out[:4]), ('_attack.png', out[4:])):
        st = Image.new('RGBA', (W * len(fr), H))
        for i, f in enumerate(fr):
            st.paste(f, (i * W, 0))
        st.save(name + suffix)
    assert len(out) == 7 and all(f.getbbox() for f in out)
    print(name, 'Zelle', (W, H), 'Maßstab', round(k, 3))


def save_roll(name, cells):
    """Ausweich-Rolle wie art_src/fable/heroes/roll.py: 5 Zellen [geduckt, Ball 0..3], Blick nach links, Ball-Mitte = Zellmitte.
    Ball 2/3 sind Ball 0/1 um 180° gedreht (bei Pixelkunst verlustfrei). Unterkante des Balls 17 px unter der Mitte wie bisher."""
    cr, a, b = cells
    balls = [a, b, a.rotate(180), b.rotate(180)]
    D = max(max(c.size) for c in balls)
    CW = max(cr.width, D) + 2
    CH = max(88, 2 * (D - 17) + 2, 2 * cr.height)
    st = Image.new('RGBA', (CW * 5, CH))
    st.paste(cr, ((CW - cr.width) // 2, CH - cr.height))
    for i, c in enumerate(balls):
        st.paste(c, ((i + 1) * CW + (CW - c.width) // 2, CH // 2 + 17 - c.height))
    st.save(os.path.join(SPRITES, name + '_roll.png'))


def grid_boxes(fg, rows=2, cols=4):
    """Bildgrenzen je Zeile an Spaltenlücken statt starrem Raster – Waffen und Effekte ragen oft über die Rastergrenze.
    Fällt auf das starre Raster zurück, wenn die Lücken nicht genau cols Bilder ergeben."""
    H, W = fg.shape
    occ_y = ndimage.uniform_filter1d(fg.sum(1).astype(float), 61)   # geglättet: Grenze in die Mitte der leeren Bande, nicht an ihren Rand
    ys = [0] + [r * H // rows - H // 8 + int(np.argmin(occ_y[r * H // rows - H // 8: r * H // rows + H // 8])) for r in range(1, rows)] + [H]
    out = []                                           # Zeilengrenze an der leersten Bildzeile nahe der Rastermitte (hochgerissene Waffen)
    for r in range(rows):
        y0, y1 = ys[r], ys[r + 1]
        occ = fg[y0:y1].sum(0) > 0
        segs, s0 = [], None
        for x, v in enumerate(occ):
            if v and s0 is None:
                s0 = x
            if not v and s0 is not None:
                segs.append([s0, x]); s0 = None
        if s0 is not None:
            segs.append([s0, W])
        merged = []                                    # Splitter (Staub, Spitzen) zum Nachbarn mit kleinerem Abstand
        for g in segs:
            if merged and (g[1] - g[0] < W // 40 or g[0] - merged[-1][1] < 4):
                merged[-1][1] = g[1]
            else:
                merged.append(g)
        if len(merged) != cols:
            merged = [[c * W // cols, (c + 1) * W // cols] for c in range(cols)]
        out.append([(a, y0, b, y1) for a, b in merged])
    return out


def tidy(c):
    """Krümel weg (Teile unter 12 px), dann 1-px-Umriss wie bei den übrigen Spielfiguren."""
    a = np.array(c)
    op = a[..., 3] > 0
    nb = sum(np.roll(np.roll(op, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1)) - op
    op &= nb >= 2
    lab, n = ndimage.label(op)
    if n > 1:
        sizes = ndimage.sum(op, lab, range(1, n + 1))
        op = np.isin(lab, [i + 1 for i, v in enumerate(sizes) if v >= 12])
    a[..., 3] = op * 255
    ring = ~op & (sum(np.roll(np.roll(op, dy, 0), dx, 1) for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))) > 0)
    a[ring] = (18, 16, 26, 255)
    return Image.fromarray(a)


def foot_cx(c):
    """Fußmitte: Mitte der untersten Pixelzeilen – Bezugspunkt, damit Waffe/Strahl die Figur nicht verschieben."""
    a = np.array(c)[..., 3] > 0
    ys = np.where(a.any(1))[0]
    return int(np.where(a[ys.max() - 6:ys.max() + 1].any(0))[0].mean())
