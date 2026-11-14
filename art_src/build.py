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
    with open(os.path.join(OUT, 'sprites.json'), 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, indent=1, sort_keys=True)
    print(len(meta), 'Sprites gebaut')


if __name__ == '__main__':
    main()
