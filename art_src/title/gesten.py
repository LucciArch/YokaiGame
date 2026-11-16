"""Kleine Effekt-Bilder für die Gesten in der Charakterauswahl (Hi-Res-Ebene), Pixel für Pixel gesetzt:
fx_spark   – goldener Funke (Hanas Kagura-Glöckchen)
fx_fire_b  – blaues Kitsunebi (Kuzunoha), fx_fire_r – rote Oni-Glut (Akago)
fx_feather – schwarze Tengu-Feder (Kotarō)
fx_ofuda   – Papiertalisman mit Zinnober-Zeichen (Seimei)
fx_dust    – Staubwolke (Benkei), fx_smoke – weiße Verwandlungswolke (Ponpoko)
fx_leaf    – Verwandlungsblatt des Tanuki (Ponpoko)
fx_drop    – Brunnenwasser (Okiku)
fx_glint   – Glanz auf der gezogenen Klinge (Kenji)
fx_bolt    – Blitz (Susanoo)
usage: python3 gesten.py"""
import os
import numpy as np
from PIL import Image
from panorama import DST, K, hx

SPARK = """
....k....
...kak...
...kbk...
.kkbcbkk.
kabcwcbak
.kkbcbkk.
...kbk...
...kak...
....k....
"""
FIRE = """
....k....
...kak...
...kak...
..kabak..
..kabbak.
.kabcbak.
.kabccbak
kabccwcbk
kabcwwcbk
kabcwwcbk
.kbccccbk
..kbbbbk.
...kkkk..
"""
FEATHER = """
...k...
..kbk..
..kbck.
.kabck.
.kabck.
.kabck.
kaabcck
kaabeck
kaabeck
.kabek.
.kaaek.
..kaek.
...ke..
...ke..
...k...
"""
OFUDA = """
kkkkkkkkk
kpppppppk
kprrrrrpk
kpppppppk
kpprrrppk
kpppppqpk
kppprppqk
kpprrrpqk
kppprppqk
kpprprpqk
kppprppqk
kpppppqqk
kprpprpqk
kppprppqk
kppppppqk
kqqqqqqqk
kkkkkkkkk
"""
DUST = """
....kkk......
..kkeffk.kk..
.kdeffffkefk.
kddeeffeeeffk
kdddeeeeeeefk
.kkdddddddkk.
...kkkkkkk...
"""
LEAF = """
......kk.
....kkbk.
..kkbbck.
.kabbcbk.
.kabcbbk.
kabcbbk..
kacbak...
kkkkk....
k........
"""
DROP = """
...k...
..kak..
..kak..
.kabak.
.kabak.
kabbcak
kabwcak
kabccak
.kaaak.
..kkk..
"""
GLINT = """
..........w..........
.........cwc.........
.....bbccwwwccbb.....
bbccccwwwwwwwwwccccbb
.....bbccwwwccbb.....
.........cwc.........
..........w..........
"""
BOLT = """
.....kkk.
....kwyk.
...kwyk..
...kwyk..
..kwyk...
..kwykkk.
.kwwwwyk.
.kkkkwyk.
....kwyk.
...kwyk..
...kwyk..
..kwyk...
..kwykkk.
.kwwwwyk.
.kkkkwyk.
....kwyk.
...kwyk..
...kyk...
..kyk....
..kzk....
.kzk.....
.kk......
"""


def P(**cols):
    """Palette: Buchstabe -> '#rrggbb' oder ('#rrggbb', alpha); k ist immer der Umriss."""
    out = {'k': (*K, 255)}
    for ch, c in cols.items():
        c, a = (c, 255) if isinstance(c, str) else c
        out[ch] = (*hx(c), a)
    return out


GOLD = P(a='#b8742c', b='#f0c040', c='#fff0a0', w='#ffffff')
BLUE = P(a='#1c3c8c', b='#3c7ce0', c='#90d0ff', w='#f0fcff')
RED = P(a='#7c1414', b='#d0401c', c='#ffa040', w='#fff0b0')
SPRITES = {
    'fx_spark': (SPARK, GOLD),
    'fx_fire_b': (FIRE, BLUE),
    'fx_fire_r': (FIRE, RED),
    'fx_feather': (FEATHER, P(a='#141020', b='#2e2848', c='#5c5484', e='#c8b890')),
    'fx_ofuda': (OFUDA, P(p='#f0e6c8', q='#c0ac88', r='#b8281e')),
    'fx_dust': (DUST, P(d='#4c4458', e='#7a7086', f='#a89eb0')),
    'fx_smoke': (DUST, P(d='#8c88a4', e='#c4c0d4', f='#f0eef8')),
    'fx_leaf': (LEAF, P(a='#1e4a24', b='#3e7a30', c='#7cb450')),
    'fx_drop': (DROP, P(a='#2c5a7c', b='#5ea0c8', c='#a8dcf0', w='#ffffff')),
    'fx_glint': (GLINT, P(b=('#5070c0', 120), c=('#b0d0ff', 210), w='#ffffff')),
    'fx_bolt': (BOLT, P(y='#fff4a0', w='#ffffff', z='#d8a830')),
}


def build(art, pal):
    rows = art.strip('\n').split('\n')
    w = max(len(r) for r in rows)
    a = np.zeros((len(rows), w, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.':
                a[y, x] = pal[ch]
    return np.kron(a, np.ones((2, 2, 1), np.uint8))   # gleiche Pixelgröße wie die doppelt große Figur auf dem Podest


if __name__ == '__main__':
    os.makedirs(DST, exist_ok=True)
    for name, (art, pal) in SPRITES.items():
        Image.fromarray(build(art, pal), 'RGBA').save(os.path.join(DST, name + '.png'))
    print(len(SPRITES), 'Gesten-Bilder')
