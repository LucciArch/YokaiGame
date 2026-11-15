"""Übernimmt die handgesetzten Sprites (Quellen: art_src/fable/**) ins Spiel.

Je Figur: <name>_walk.png (4 Bilder) + <name>_attack.png (3 Bilder), gleiche Zellgröße.
Ergebnis: yokai/assets/sprites/<name>.png als 7-Bilder-Streifen (Hi-Res, halbe Weltgröße).
"""
import glob
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'fable')
OUT = os.path.join(HERE, '..', 'yokai', 'assets', 'sprites')


def frames(path, n):
    im = Image.open(path).convert('RGBA')
    w = im.width // n
    return [im.crop((i * w, 0, (i + 1) * w, im.height)) for i in range(n)]


def main():
    meta_p = os.path.join(OUT, 'sprites.json')
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
    done = []
    for walk in sorted(glob.glob(os.path.join(SRC, '**', '*_walk.png'), recursive=True)):
        name = os.path.basename(walk)[:-9]
        atk = walk.replace('_walk.png', '_attack.png')
        if not os.path.exists(atk):
            continue
        fr = frames(walk, 4) + frames(atk, 3)
        W = max(f.width for f in fr)
        H = max(f.height for f in fr)
        cells = []
        for f in fr:
            c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            c.paste(f, ((W - f.width) // 2, H - f.height))
            cells.append(c)
        box = None
        for c in cells:
            b = c.getbbox()
            if b:
                box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        # Fuß-Mitte des ersten Bildes als horizontale Mitte, damit Ausholen nicht verschiebt
        b0 = cells[0].getbbox()
        cx = (b0[0] + b0[2]) // 2
        half = max(cx - box[0], box[2] - cx)
        x0, x1 = cx - half, cx + half
        cells = [c.crop((x0, box[1], x1, box[3])) for c in cells]
        w, h = cells[0].size
        st = Image.new('RGBA', (w * 7, h), (0, 0, 0, 0))
        for i, c in enumerate(cells):
            st.paste(c, (i * w, 0))
        st.save(os.path.join(OUT, name + '.png'))
        meta[name] = {'kind': 'strip', 'w': w, 'h': h, 'n': 7, 'walk': 4, 'atk': 4, 'hi': True}
        done.append(name)
    json.dump(meta, open(meta_p, 'w'), indent=1, sort_keys=True)
    print(len(done), 'übernommen:', ' '.join(done))


if __name__ == '__main__':
    main()
