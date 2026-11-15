"""Generiertes Bild -> sauberes Pixel-Sprite (wie SpriteCooks Nachbearbeitung):
Hintergrund entfernen, auf Zielgröße verkleinern, Palette begrenzen, Einzelpixel
entfernen, dunklen Umriss setzen."""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def remove_bg(img, tol=38):
    a = np.array(img.convert('RGB')).astype(int)
    h, w, _ = a.shape
    corners = np.array([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]])
    bgc = np.median(corners, axis=0)
    diff = np.abs(a - bgc).sum(-1)
    mx, mn = a.max(-1), a.min(-1)
    cand = (diff < tol) | ((mn > 205) & (mx - mn < 30))
    lab, n = ndimage.label(cand)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    # Schatten unter der Figur (grau, flach) auch entfernen
    fg = ~bg
    fg = ndimage.binary_opening(fg, iterations=1)
    lab2, n2 = ndimage.label(fg)
    if n2:
        sizes = ndimage.sum(fg, lab2, range(1, n2 + 1))
        fg = lab2 == (np.argmax(sizes) + 1)
        fg = ndimage.binary_fill_holes(fg)
        fg = ndimage.binary_erosion(fg, iterations=3)
    rgba = np.dstack([a, (fg * 255)]).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')


def pixelize(img, target_h=72, colors=24, outline=(14, 10, 18), palette=None):
    img = remove_bg(img)
    bb = img.getbbox()
    img = img.crop(bb)
    w, h = img.size
    th = target_h
    tw = max(1, round(w * th / h))
    from PIL import ImageEnhance
    hi = ImageEnhance.Color(ImageEnhance.Contrast(img.convert('RGB')).enhance(1.12)).enhance(1.2)
    hi = hi.filter(ImageFilter.MedianFilter(3))
    if palette is not None:
        hq = hi.quantize(palette=palette, dither=Image.Dither.NONE)
    else:
        hq = hi.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal_img = hq
    # k-Zentroid/Modus-Verkleinerung: pro Zielpixel die häufigste Palettenfarbe im Block -> klare Cluster
    idx = np.array(hq)
    ys = np.linspace(0, idx.shape[0], th + 1).astype(int)
    xs = np.linspace(0, idx.shape[1], tw + 1).astype(int)
    small = np.zeros((th, tw), np.uint8)
    for yy in range(th):
        for xx in range(tw):
            blk = idx[ys[yy]:ys[yy + 1], xs[xx]:xs[xx + 1]].ravel()
            small[yy, xx] = np.bincount(blk).argmax() if blk.size else 0
    q = Image.fromarray(small, 'P'); q.putpalette(hq.getpalette())
    rgb = q.convert('RGB')
    al = img.split()[3].resize((tw, th), Image.BOX)
    al = al.point(lambda v: 255 if v > 140 else 0)
    # kontrastreicher wie 16-Bit
    out = rgb.convert('RGBA')
    out.putalpha(al)
    a = np.array(out)
    m = a[..., 3] > 0
    # Einzelpixel-Rauschen glätten: Pixel ohne gleichfarbigen Nachbarn -> häufigste Nachbarfarbe
    rgbq = a[..., :3].copy()
    H, W = m.shape
    for y in range(H):
        for x in range(W):
            if not m[y, x]:
                continue
            c = tuple(rgbq[y, x])
            nb = []
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < H and 0 <= xx < W and m[yy, xx]:
                    nb.append(tuple(rgbq[yy, xx]))
            if nb and c not in nb:
                a[y, x, :3] = max(set(nb), key=nb.count)
    # Außenumriss: dunkelste Farbe der Figur
    ring = ndimage.binary_dilation(m, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])) & ~m
    pad = np.zeros((H + 2, W + 2, 4), np.uint8)
    pad[1:-1, 1:-1] = a
    mm = np.zeros((H + 2, W + 2), bool); mm[1:-1, 1:-1] = m
    ring = ndimage.binary_dilation(mm, structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])) & ~mm
    pad[ring, :3] = outline
    pad[ring, 3] = 255
    return Image.fromarray(pad, 'RGBA')


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    th = int(sys.argv[3]) if len(sys.argv) > 3 else 72
    im = pixelize(Image.open(src), th)
    im.save(dst)
    bg = Image.new('RGBA', im.size, (22, 40, 92, 255)); bg.alpha_composite(im)
    bg.resize((im.width * 6, im.height * 6), Image.NEAREST).save(dst.replace('.png', '_x6.png'))
