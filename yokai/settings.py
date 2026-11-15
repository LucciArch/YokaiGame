"""Grundeinstellungen und Konstanten."""
import os

TITLE = "Yōkai no Michi – Hyakki Yagyō"
VERSION = "1.1.0"

W, H = 480, 320          # interne Auflösung (Pixel-Art), wird hochskaliert
TILE = 32
COLS, ROWS = 13, 7
RX, RY = 32, 44          # linke obere Ecke des Raum-Inneren
RW, RH = COLS * TILE, ROWS * TILE   # 416 x 224
FPS = 60

DIRS = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0)}
OPP = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}
DOOR_TILE = {'n': (6, 0), 's': (6, 6), 'w': (0, 3), 'e': (12, 3)}
DOOR_POS = {
    'n': (RX + 6 * TILE + 16, RY),
    's': (RX + 6 * TILE + 16, RY + RH),
    'w': (RX, RY + 3 * TILE + 16),
    'e': (RX + RW, RY + 3 * TILE + 16),
}

# Kachel-Typen
T_FLOOR, T_ROCK, T_PIT, T_SPIKE, T_POT, T_LANTERN = 0, 1, 2, 3, 4, 5
SOLID_TILES = (T_ROCK, T_POT, T_LANTERN)


def save_dir():
    base = os.getenv('APPDATA') or os.path.join(os.path.expanduser('~'), '.local', 'share')
    d = os.path.join(base, 'YokaiNoMichi')
    try:
        os.makedirs(d, exist_ok=True)
    except OSError:
        d = os.path.abspath('.')
    return d
