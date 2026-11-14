"""Baut alle selbst gezeichneten Sprites nach yokai/assets/sprites (+ sprites.json)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, '..', 'yokai', 'assets', 'sprites')


def main():
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    import chars
    for name in chars.build_all(OUT):
        meta[name] = {'kind': 'dir4', 'w': chars.W, 'h': chars.H, 'n': 4}
    try:
        import monsters
        meta.update(monsters.build_all(OUT))
    except ImportError:
        pass
    try:
        import bosses_art
        meta.update(bosses_art.build_all(OUT))
    except ImportError:
        pass
    # Version 2 (16-Bit-Stil, Lauf- + Angriffsbilder) ersetzt Version 1, wo vorhanden
    sys.path.insert(0, os.path.join(HERE, 'v2'))
    import creatures
    from PIL import Image
    for name, fn in creatures.ALL.items():
        frs = creatures.frames(fn)
        box = None
        for f in frs:
            b = f.getbbox()
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        frs = [f.crop(box) for f in frs]
        w, h = frs[0].size
        st = Image.new('RGBA', (w * len(frs), h), (0, 0, 0, 0))
        for i, f in enumerate(frs):
            st.paste(f, (i * w, 0))
        st.save(os.path.join(OUT, name + '.png'))
        meta[name] = {'kind': 'strip', 'w': w, 'h': h, 'n': len(frs), 'walk': 4, 'atk': 4}
    with open(os.path.join(OUT, 'sprites.json'), 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, indent=1, sort_keys=True)
    print(len(meta), 'Sprites gebaut')


if __name__ == '__main__':
    main()
