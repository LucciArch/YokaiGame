"""forge – erzeugt ein konsistentes, animiertes Yōkai-Sprite.

Ablauf pro Yōkai:
 1. Basisbild: eigene Posenzeichnung -> sd-turbo img2img (Stärke ~0.5) -> 512 px Bild
 2. Zurück aufs echte Pixelraster (Blockgröße wird erkannt, meist 8) -> natives Sprite
 3. Angriffsbilder: eigene Angriffspose -> gleiche Generierung; danach wird der Kopf
    des Basisbildes eingesetzt (Template-Matching), damit das Gesicht in jedem Bild gleich bleibt
 4. Laufbilder: aus dem Basisbild per Puppen-Animation (Beine versetzen, Körper wippen) –
    dadurch 100 % identisches Aussehen
 5. Alle Bilder auf die Palette des Basisbildes gesperrt.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
from pixelstudio import block_downscale, estimate_scale  # noqa: E402

_pipe = None


def pipe():
    global _pipe
    if _pipe is None:
        import torch
        from diffusers import AutoPipelineForImage2Image
        torch.set_num_threads(2)
        _pipe = AutoPipelineForImage2Image.from_pretrained('/home/claude/models/sd-turbo', dtype=torch.bfloat16, variant='fp16')
        _pipe.vae.enable_tiling()
        _pipe.enable_attention_slicing()
    return _pipe


def prep(src, fill=0.86):
    im = src.convert('RGBA')
    s = 512 / max(im.size) * fill
    im = im.resize((int(im.width * s), int(im.height * s)), Image.NEAREST)
    bg = Image.new('RGB', (512, 512), (255, 255, 255))
    bg.paste(im, ((512 - im.width) // 2, 512 - im.height - 24), im)
    return bg.filter(ImageFilter.GaussianBlur(2))


def generate(src, prompt, seed=2, strength=0.5, steps=4, fill=0.86):
    import torch
    init = prep(src, fill)
    return pipe()(prompt=prompt, image=init, num_inference_steps=steps, strength=strength, guidance_scale=0.0,
                  generator=torch.Generator().manual_seed(seed)).images[0]


def cutout(img):
    """Hintergrund (fast weiß, vom Rand her zusammenhängend) entfernen; Weiß IN der Figur bleibt."""
    a = np.array(img.convert('RGB')).astype(int)
    mx, mn = a.max(-1), a.min(-1)
    cand = (mn > 228) & (mx - mn < 22)
    lab, n = ndimage.label(cand)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    # leicht grauer Saum direkt am Hintergrund (Kompressions-/Weichzeichnungsreste)
    for _ in range(3):
        near = ndimage.binary_dilation(bg) & ~bg
        bg |= near & (mn > 200) & (mx - mn < 30)
    fg = ~bg
    fg = ndimage.binary_opening(fg, iterations=1)
    lab2, n2 = ndimage.label(fg)
    if n2:
        sizes = ndimage.sum(fg, lab2, range(1, n2 + 1))
        keep = [i + 1 for i, sz in enumerate(sizes) if sz > sizes.max() * 0.04]
        fg = np.isin(lab2, keep)
    return Image.fromarray(np.dstack([a, fg * 255]).astype(np.uint8), 'RGBA')


def to_native(img, grid=None):
    rgba = cutout(img)
    g = grid or estimate_scale(img.convert('RGBA'))
    g = max(4, min(10, g))
    return mode_downscale(rgba, g), g


def mode_downscale(rgba, g):
    """Blockweise häufigste Farbe (5 Bit je Kanal), Durchschnitt innerhalb der Gewinnerfarbe;
    Block ist sichtbar, wenn > 45 % deckend."""
    a = np.array(rgba).astype(int)
    H, W = a.shape[:2]
    th, tw = H // g, W // g
    out = np.zeros((th, tw, 4), np.uint8)
    key = (a[..., 0] >> 3) * 1024 + (a[..., 1] >> 3) * 32 + (a[..., 2] >> 3)
    for y in range(th):
        for x in range(tw):
            blk = a[y * g:(y + 1) * g, x * g:(x + 1) * g].reshape(-1, 4)
            k = key[y * g:(y + 1) * g, x * g:(x + 1) * g].ravel()
            op = blk[:, 3] > 0
            if op.sum() < g * g * 0.45:
                continue
            kk = k[op]
            vals, cnt = np.unique(kk, return_counts=True)
            win = vals[cnt.argmax()]
            sel = blk[op][kk == win]
            out[y, x, :3] = sel[:, :3].mean(0)
            out[y, x, 3] = 255
    return Image.fromarray(out, 'RGBA')


def lock_palette(frames, n=28):
    base = frames[0]
    rgb = base.convert('RGB')
    m = np.array(base)[..., 3] > 0
    pal = rgb.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    out = []
    for f in frames:
        q = f.convert('RGB').quantize(palette=pal, dither=Image.Dither.NONE).convert('RGBA')
        q.putalpha(f.split()[3])
        out.append(q)
    return out


def despeckle(img):
    a = np.array(img)
    src = a.copy()
    m = a[..., 3] > 0
    H, W = m.shape
    for y in range(H):
        for x in range(W):
            if not m[y, x]:
                continue
            c = tuple(src[y, x, :3])
            nb = [tuple(src[yy, xx, :3]) for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1), (y - 1, x - 1), (y + 1, x + 1), (y - 1, x + 1), (y + 1, x - 1))
                  if 0 <= yy < H and 0 <= xx < W and m[yy, xx]]
            if len(nb) >= 3 and c not in nb:
                a[y, x, :3] = max(set(nb), key=nb.count)
    return Image.fromarray(a, 'RGBA')


def outline(img, col=(14, 10, 18)):
    a = np.array(img)
    H, W = a.shape[:2]
    pad = np.zeros((H + 2, W + 2, 4), np.uint8)
    pad[1:-1, 1:-1] = a
    m = pad[..., 3] > 0
    ring = ndimage.binary_dilation(m, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])) & ~m
    pad[ring, :3] = col
    pad[ring, 3] = 255
    return Image.fromarray(pad, 'RGBA')


def match(big, tpl, cx, cy, r=8):
    """Sucht tpl (RGBA) in big um (cx, cy); gibt beste obere linke Ecke zurück."""
    B = np.array(big).astype(int)
    T = np.array(tpl).astype(int)
    th, tw = T.shape[:2]
    tm = T[..., 3] > 0
    best, bp = 1e18, (cx, cy)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            x, y = cx + dx, cy + dy
            if x < 0 or y < 0 or y + th > B.shape[0] or x + tw > B.shape[1]:
                continue
            reg = B[y:y + th, x:x + tw]
            d = np.abs(reg[..., :3] - T[..., :3]).sum(-1)
            d = np.where(tm & (reg[..., 3] > 0), d, 255 * 2)
            sc = d[tm].mean()
            if sc < best:
                best, bp = sc, (x, y)
    return bp


def canvas(img, W, H, x, y):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c.alpha_composite(img, (x, y))
    return c


def walk_frames(base, hip_frac=0.68, stride=2):
    """Puppen-Laufzyklus aus einem Bild: Kontakt/Passieren, Beine abwechselnd, Körper wippt."""
    a = np.array(base)
    H, W = a.shape[:2]
    ys, xs = np.nonzero(a[..., 3])
    top, bot = ys.min(), ys.max()
    hip = int(top + (bot - top) * hip_frac)
    cx = int(np.median(xs[ys > hip])) if (ys > hip).any() else W // 2
    frames = []
    for i in range(4):
        out = np.zeros((H + 2, W, 4), np.uint8)
        bob = 1 if i in (1, 3) else 0
        upper = a[:hip]
        out[1 - bob:1 - bob + hip] = upper
        lower = a[hip:]
        for side, sign in ((slice(0, cx), 1), (slice(cx, W), -1)):
            lift = 0
            if i == 1:
                lift = stride * sign if sign > 0 else 0
            if i == 3:
                lift = stride if sign < 0 else 0
            seg = lower[:, side]
            y0 = 1 + hip - lift
            dst = out[y0:y0 + seg.shape[0], side]
            msk = seg[..., 3] > 0
            h = min(dst.shape[0], seg.shape[0])
            d = dst[:h]
            d[msk[:h]] = seg[:h][msk[:h]]
        frames.append(Image.fromarray(out, 'RGBA'))
    return frames


def build(name, srcs, prompt, seed=2, strength=0.5, head_box=(0.15, 0.0, 0.85, 0.42), hip=0.68, show=None, grid=6, cache=None, fill=0.86):
    """srcs: dict pose->PIL (eigene Zeichnungen): 'base', 'wind', 'strike'."""
    gens = {}
    for k in ('base', 'wind', 'strike'):
        cp = cache and os.path.join(cache, f'{name}_{k}_512.png')
        if cp and os.path.exists(cp):
            gens[k] = Image.open(cp).convert('RGB')
            continue
        img = generate(srcs[k], prompt, seed=seed, strength=strength, fill=fill)
        if cp:
            img.save(cp)
        gens[k] = img
        if show:
            img.save(os.path.join(show, f'{name}_{k}_512.png'))
    nat = {}
    g = grid
    for k in ('base', 'wind', 'strike'):
        n, g = to_native(gens[k], g)
        nat[k] = n.crop(n.getbbox())
    base = nat['base']
    bw, bh = base.size
    # Kopf des Basisbildes
    hx0, hy0, hx1, hy1 = int(bw * head_box[0]), int(bh * head_box[1]), int(bw * head_box[2]), int(bh * head_box[3])
    head = base.crop((hx0, hy0, hx1, hy1))
    # gemeinsame Leinwand, Füße unten ausgerichtet
    W = max(n.width for n in nat.values()) + 16
    H = max(n.height for n in nat.values()) + 8
    frames = {}
    for k, n in nat.items():
        x = (W - n.width) // 2 if k == 'base' else None
        if k != 'base':
            # unten ausrichten, horizontal über Beine/Körperunterteil anpassen
            ref = canvas(base, W, H, (W - bw) // 2, H - bh - 2)
            low = base.crop((0, int(bh * 0.7), bw, bh))
            cand = canvas(n, W, H, (W - n.width) // 2, H - n.height - 2)
            lx, ly = match(cand, low, (W - bw) // 2, H - bh - 2 + int(bh * 0.7), r=10)
            dx = lx - (W - bw) // 2
            img = canvas(n, W, H, (W - n.width) // 2 - dx, H - n.height - 2)
            # Gesicht konstant halten
            px, py = match(img, head, (W - bw) // 2 + hx0, H - bh - 2 + hy0, r=12)
            img.alpha_composite(head, (px, py))
            frames[k] = img
        else:
            frames[k] = canvas(n, W, H, x, H - n.height - 2)
    walk = walk_frames(frames['base'], hip)
    walk = [w.crop((0, 1, W, H + 1)) for w in walk]
    recover = frames['wind']
    seq = walk + [frames['wind'], frames['strike'], recover]
    seq = lock_palette(seq)
    seq = [outline(despeckle(f)) for f in seq]
    return seq, g


# ---------------------------------------------------------------- Puppen-Angriffe
def _xform(img, dx=0, dy=0, sx=1.0, sy=1.0, rot=0.0):
    """Verschiebt/skaliert/dreht ein Bild um den Fußpunkt (unten Mitte), nächster Nachbar."""
    W, H = img.size
    bb = img.getbbox()
    if not bb:
        return img
    cx, by = (bb[0] + bb[2]) / 2, bb[3]
    out = img
    if sx != 1.0 or sy != 1.0:
        nw, nh = max(1, round(W * sx)), max(1, round(H * sy))
        sc = img.resize((nw, nh), Image.NEAREST)
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        c.alpha_composite(sc, (round(cx - cx * sx), round(by - by * sy)) if False else (0, 0)) if False else None
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ox, oy = round(cx - cx * sx), round(by - by * sy)
        c.paste(sc, (ox, oy), sc)
        out = c
    if rot:
        out = out.rotate(rot, resample=Image.NEAREST, center=(cx, by))
    if dx or dy:
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        c.paste(out, (dx, dy), out)
        out = c
    return out


def _fx(img, kind, color):
    """Angriffseffekt vor der Figur (Blick nach links)."""
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    bb = img.getbbox()
    if not bb:
        return img
    x0, y0, x1, y1 = bb
    h = y1 - y0
    if kind == 'slash':
        for i in range(3):
            d.arc([x0 - 14 + i, y0 + h * 0.15 + i, x0 + 16 - i, y0 + h * 0.85 - i], 110, 250, fill=(240, 248, 255, 255) if i == 0 else (170, 200, 235, 255))
    elif kind == 'spit':
        cy = y0 + h * 0.35
        for r, c in ((5, color), (3, (255, 250, 220))):
            d.ellipse([x0 - 4 - r, cy - r, x0 - 4 + r, cy + r], fill=c + (255,))
    return img


def attack_frames(base, kind, fx_color=(255, 170, 80)):
    W, H = base.size
    pad = 10
    b = Image.new('RGBA', (W + pad * 2, H + pad), (0, 0, 0, 0))
    b.paste(base, (pad, pad), base)
    if kind == 'lunge':
        wind = _xform(b, dx=2, sx=0.96, sy=0.94)
        strike = _xform(b, dx=-5, sx=1.08, sy=1.02)
        rec = _xform(b, dx=-2)
    elif kind == 'slash':
        wind = _xform(b, dx=2, rot=-8)
        strike = _fx(_xform(b, dx=-5, rot=10), 'slash', fx_color)
        rec = _xform(b, dx=-2, rot=4)
    elif kind == 'spit':
        wind = _xform(b, dx=1, sy=0.95, rot=-6)
        strike = _fx(_xform(b, dx=-2, sy=1.03, rot=5), 'spit', fx_color)
        rec = _xform(b, dx=-1)
    elif kind == 'rise':
        wind = _xform(b, sx=1.08, sy=0.88)
        strike = _xform(b, dy=-3, sx=0.94, sy=1.1)
        rec = _xform(b, dy=-1)
    elif kind == 'spin':
        wind = _xform(b, rot=30)
        strike = _xform(b, rot=60, dx=-3)
        rec = _xform(b, rot=90)
    else:  # swing
        wind = _xform(b, dx=2, rot=-10)
        strike = _xform(b, dx=-4, rot=12)
        rec = _xform(b, dx=-1, rot=4)
    return b, [wind, strike, rec]


def bob_frames(base, amp=2):
    out = []
    W, H = base.size
    for dy in (0, -amp // 2, -amp, -amp // 2):
        c = Image.new('RGBA', (W, H + amp), (0, 0, 0, 0))
        c.paste(base, (0, amp + dy), base)
        out.append(c)
    return out


def finalize(img512, kind, fly=False, grid=6, legs=True):
    """512er-Bild -> 7 Bilder (4 Lauf/Schwebe + 3 Angriff), alle aus EINEM Basisbild."""
    nat, _ = to_native(img512, grid)
    nat = nat.crop(nat.getbbox())
    nat = despeckle(nat)
    padded, atk = attack_frames(nat, kind)
    if fly or not legs:
        walk = bob_frames(padded)
    else:
        walk = walk_frames(padded)
    frames = walk + atk
    W = max(f.width for f in frames)
    H = max(f.height for f in frames)
    out = []
    for f in frames:
        c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        c.paste(f, ((W - f.width) // 2, H - f.height), f)
        out.append(c)
    out = lock_palette(out)
    return [outline(f) for f in out]
