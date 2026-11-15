"""Kappa – handgesetzt. Körper/Panzer/Beine mit sculpt (Volumen), Kopf, Gesicht,
Hände und Füße als von Hand gesetzte Pixelkarten (jeder Pixel bewusst platziert).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from PIL import Image  # noqa: E402
from sculpt import Canvas, cel, hexrgb  # noqa: E402

PAL = {
    'K': '#0c0812',                                        # Umriss
    'g': '#1d5a36', 'G': '#3a8c3c', 'L': '#6cc04a', 'H': '#b4e46c',   # Haut (grün)
    'y': '#8a8436', 'Y': '#c8c05a', 'Z': '#ece49a',          # Bauch
    'b': '#8a5a10', 'B': '#e0a020', 'C': '#f8dc68',          # Schnabel
    'w': '#2a6e9e', 'W': '#5ab8e4', 'X': '#d0f4ff',          # Wasser im Teller
    'r': '#c89a4a', 'R': '#8a6430',                          # Tellerrand
    'h': '#141c30', 'j': '#2e4266', 'J': '#4a6490',          # Haar
    'e': '#f8e040', 'E': '#fff8b0', 'p': '#0c0812',          # Auge
    'm': '#5a1018', 'n': '#f0e8d0', 'N': '#b8b098',          # Maul, Krallen
}

# Kopf (Blick nach links), 21 x 19 – jeder Buchstabe ein Pixel, '.' = durchsichtig
HEAD = """
........KKKKKKKKKK........
......KKRrrrrrrrrRKK......
.....KRrWWWXXXWWWWrRK.....
.....KRwWWXXXXWWWWwRK.....
....KjKRwwwwwwwwwwRKjK....
...KjJKKRRRRRRRRRRKKJjK...
...KjJjKLLLLLLGGGGKjJjK...
..KhjJhLLHHLLLLGGGGhJjhK..
..KhjKLLHLLLLLLLGGGGhjjhK.
..KjKLLLLLLLLLLLGGGGgjJhK.
..KKgggggLLLLLLGGGGgghjhK.
.KLKKKKKgLLLLLLGGGGgghjhK.
.KLKeeEKLLLLLLGGGGggghjK..
.KLKepeKLLLLLLGGGGgggjhK..
KBKKKKKLLLLLLGGGGGgggjK...
KCCBBKLLLLLLGGGGGgggghK...
KCCCCBBKLLLLLGGGGggghK....
KBCCBBBBKLLLGGGGGgggK.....
KKbbbbbbbKLLGGGGggggK.....
KbnbnbbbKGLGGGGggggK......
.KbbbbbbKGGGGGgggKK.......
..KKbbbKgGGGggggK.........
....KKKKKggggKKK..........
"""

HAIR = """
.KhjK.KjK
KhjJhKjJK
KhjjhKjhK
.KjhKKjhK
.KjhK.KhK
..KhK.KK.
..KK.....
"""

# Vordere Hand mit Schwimmhäuten und Krallen, 8 x 7
HAND = """
..KKKK..
.KLLGGK.
KLGGGgGK
KGGgGGgK
KgKGgKgK
KnK nKnK
.K...K.K
"""

FOOT = """
....KKKKK..
..KKLGGGGK.
.KLGGGGGgK.
KGGGGgGGGgK
KgnKgnKgnK.
.K..K..K...
"""


def stamp(img, art, x0, y0):
    rows = [r for r in art.strip('\n').split('\n')]
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in '. ':
                continue
            px, py = x0 + x, y0 + y
            if 0 <= px < img.width and 0 <= py < img.height:
                img.putpixel((px, py), hexrgb(PAL[ch]) + (255,))


SKIN = cel('#3fa04a')
BELLY = cel('#c8c060')
SHELL = cel('#7a4a24')
SCUTE = cel('#946032')
RIM = cel('#a87a3a')


def kappa(pose):
    kind, i = pose
    w = [0, 1, 0, -1][i] if kind == 'walk' else 0
    bob = [0, -1, 0, -1][i] if kind == 'walk' else 0
    atk = i if kind == 'atk' else -1
    lean = {-1: 0, 0: -2, 1: 3, 2: 1}[atk]
    c = Canvas(52, 54, dict(skin=SKIN, belly=BELLY, shell=SHELL, scute=SCUTE, rim=RIM), ox=8, oy=8)
    y0 = bob
    # hinteres Bein + Arm
    c.limb([(29, 30 + y0), (32 - w, 36), (32 - w, 41)], 7, 5, 'skin')
    c.limb([(29 + lean, 19 + y0), (34 + lean, 26 + y0), (33 + lean, 32 + y0)], 5, 4, 'skin')
    # Panzer mit einzelnen Schilden
    c.ellipse(18 + lean, 10 + y0, 41 + lean, 36 + y0, 'shell', bulge=1.4)
    for (a, b, d, e) in ((22, 13, 29, 20), (29, 12, 37, 20), (21, 20, 29, 28), (29, 20, 38, 28), (23, 28, 30, 34), (30, 28, 37, 34)):
        c.ellipse(a + lean, b + y0, d + lean, e + y0, 'scute', bulge=0.6)
    c.limb([(20 + lean, 11 + y0), (33 + lean, 10 + y0), (41 + lean, 20 + y0), (37 + lean, 35 + y0)], 3, 2, 'rim', bulge=0.4)
    # Körper und Bauchplatten
    c.ellipse(11 + lean, 14 + y0, 31 + lean, 35 + y0, 'skin', bulge=1.1)
    c.ellipse(12 + lean, 19 + y0, 25 + lean, 35 + y0, 'belly', bulge=0.8)
    for yy, x0, x1 in ((23, 14, 23), (27, 13, 24), (31, 14, 23)):
        c.line(x0 + lean, yy + y0, x1 + lean, yy + y0, '#8a8436')
    # vorderes Bein
    c.limb([(19, 30 + y0), (16 + w, 37), (14 + w, 41)], 8, 6, 'skin')
    # vorderer Arm
    if atk == 1:
        arm = [(16 + lean, 19 + y0), (8 + lean, 21 + y0), (0 + lean, 22 + y0)]
    elif atk == 0:
        arm = [(17 + lean, 19 + y0), (22 + lean, 25 + y0), (19 + lean, 30 + y0)]
    else:
        arm = [(16 + lean, 19 + y0), (10 + lean, 25 + y0), (7 + lean, 30 + y0)]
    c.limb(arm, 6, 4, 'skin')
    img = c.render()
    ox, oy = 8, 8
    # Füße (handgesetzt)
    stamp(img, FOOT, ox + 9 + w, oy + 40)
    stamp(img, FOOT, ox + 27 - w, oy + 40)
    # Hand
    hx, hy = arm[-1]
    stamp(img, HAND, ox + hx - 4, oy + hy - 1)
    # Kopf (handgesetzt), bei Angriff vorgeschoben und Maul weiter offen
    head_x = ox - 3 + lean * 2
    head_y = oy - 4 + y0 + (1 if atk == 0 else 0)
    stamp(img, HEAD, head_x, head_y)
    stamp(img, HAIR, head_x + 17, head_y + 9)
    if atk == 1:
        stamp(img, "KmmmmmmmK\nKmnmmnmK\n.KbbbbK", head_x, head_y + 18)
    return img


def frames():
    return [kappa(('walk', i)) for i in range(4)] + [kappa(('atk', i)) for i in range(3)]


if __name__ == '__main__':
    from sculpt import preview
    preview([('kappa', frames())], '/tmp/prev/kappa_hand.png', scale=5, cols=1, bg=(22, 40, 92))
