"""Yōkai-Gegner – eigene Pixel-Art, gebaut mit pixelstudio (MIT).

Jeder Gegner ist eine Zeichenfunktion f(s, k) für Bild k (0/1). Alle Figuren schauen
nach links (das Spiel spiegelt für rechts). Licht oben links, Rampen mit
Farbverschiebung, gemeinsamer dunkler Außenumriss.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools'))
from pixelstudio import Sprite, ramp, mix  # noqa: E402

OUT = '#1c1422'
INK = '#22182a'
WHITE = '#f6f2ff'
FRAMES = 2

# ---------------------------------------------------------------- Rampen
def R(c, n=4, hs=16, dark=0.45, light=0.6):
    return ramp(c, n, hue_shift=hs, dark=dark, light=light)


GREEN = R('#4f9a4a')
BLUE = R('#5a7ec8')
RED = R('#c8463c')
PINK = R('#e88aa0')
PURPLE = R('#8a5ab8')
BROWN = R('#8a5a3a')
TAN = R('#c89a64')
GRAY = R('#8a8a9a')
BONE = R('#e6dcc4', hs=10, dark=0.3, light=0.5)
CLOTH = R('#eef0f6', hs=12, dark=0.25, light=0.5)
FIRE = R('#f08a2a', hs=22, dark=0.35, light=0.75)
SOUL = R('#7ac8ff', hs=20, dark=0.4, light=0.8)
DARK = R('#3a3448', hs=16, dark=0.4, light=0.45)
SKIN = R('#f0c8a4', 3, hs=12, dark=0.25, light=0.5)


# ---------------------------------------------------------------- Helfer
def blob(s, x0, y0, x1, y1, r, hi=True):
    """Gerundete Form mit Licht von oben links (shifted-shape-Rezept)."""
    s.ellipse(x0, y0, x1, y1, r[0])
    s.ellipse(x0, y0, x1 - max(1, (x1 - x0) // 6), y1 - max(1, (y1 - y0) // 6), r[1], only=r[0])
    if hi and len(r) > 2:
        w, h = x1 - x0, y1 - y0
        s.ellipse(x0 + max(1, w // 6), y0 + max(1, h // 7), x0 + int(w * 0.5), y0 + int(h * 0.42), r[2], only=r[1])
        if len(r) > 3 and w >= 8:
            s.px(x0 + max(2, w // 4), y0 + max(2, h // 5), r[3])


def eye(s, x, y, col=INK, glint=True, big=False):
    if big:
        s.rect(x, y, x + 1, y + 1, col)
        if glint:
            s.px(x, y, WHITE)
    else:
        s.px(x, y, col)


def glow_eye(s, x, y, col='#ffd84a'):
    s.px(x, y, col)
    s.px(x - 1, y, mix(col, '#b04020', 0.5))


def flame(s, cx, base, w, h, r, k, lean=-1):
    """Flamme: Tropfenform, Spitze flackert je Bild."""
    tip = (cx + lean * (1 + k), base - h)
    s.polygon([(cx - w, base - h // 3), tip, (cx + w, base - h // 3), (cx + w - 1, base), (cx - w + 1, base)], r[1])
    s.ellipse(cx - w, base - h // 2, cx + w, base + 1, r[1])
    s.polygon([(cx - w + 2, base - h // 3), (tip[0] + (1 if lean < 0 else -1), tip[1] + 3), (cx + w - 2, base - h // 3)], r[2])
    s.ellipse(cx - w + 2, base - h // 2 + 1, cx + w - 2, base - 1, r[2])
    s.ellipse(cx - w // 2, base - h // 3, cx + w // 2 - 1, base - 2, r[3])


def legs2(s, xs, y, k, col, h=2):
    for i, x in enumerate(xs):
        d = (1 if (i + k) % 2 else 0)
        s.rect(x, y - d, x + 1, y + h - 1 - d, col)


# ---------------------------------------------------------------- Gegner
def hitodama(s, k):
    # Seelenflamme mit Schweif
    flame(s, 8, 18, 5, 15, SOUL, k, lean=1)
    eye(s, 6, 13); eye(s, 9, 13)
    s.px(7, 15, SOUL[0])


def kodama(s, k):
    # Baumgeist: weißer Kopf, drei dunkle Löcher, kleiner Körper
    b = k
    s.rect(6, 15 - b, 10, 19, BONE[1]); s.line(10, 15 - b, 10, 19, BONE[0])
    s.px(5, 16 - b, BONE[1]); s.px(11, 16 - b, BONE[0])
    blob(s, 2, 2 - b, 14, 15 - b, BONE)
    s.rect(4, 7 - b, 5, 9 - b, INK); s.rect(10, 7 - b, 11, 9 - b, INK); s.rect(7, 11 - b, 8, 13 - b, INK)
    s.px(5, 3 - b, '#9ad86a'); s.px(6, 2 - b, '#5fae4a')


def kappa(s, k, sz=1):
    # Kappa: grüner Froschkörper, Panzer, gelber Schnabel, Wasserteller auf dem Kopf
    legs2(s, (7, 12), 21, k, GREEN[0])
    s.rect(6, 22, 9, 22, GREEN[0]); s.rect(11, 22, 14, 22, GREEN[0])
    blob(s, 12, 9, 21, 21, BROWN)                                # Panzer
    s.line(14, 12, 19, 18, BROWN[0]); s.line(19, 12, 14, 18, BROWN[0])
    blob(s, 4, 10, 16, 21, GREEN)                                # Körper
    s.ellipse(6, 14, 12, 20, mix(GREEN[2], '#e8e0a0', 0.5), only=GREEN[1])   # Bauch
    s.rect(2, 13 + k, 4, 15 + k, GREEN[1]); s.px(1, 15 + k, GREEN[0]); s.px(3, 16 + k, GREEN[0])  # Arm/Schwimmhaut
    blob(s, 3, 2, 16, 12, GREEN)                                 # Kopf
    s.polygon([(2, 8), (5, 7), (5, 10), (2, 9)], '#e8b030'); s.line(2, 9, 5, 9, '#a87018')  # kurzer Schnabel
    s.rect(5, 4, 7, 6, WHITE); s.rect(6, 5, 7, 6, INK); s.px(10, 5, INK)
    s.line(6, 11, 9, 10, GREEN[0])
    # Haarkranz + Teller
    s.polygon([(4, 3), (6, 0), (8, 2), (10, -1 + 1), (12, 2), (14, 0), (16, 4)], '#2a4a3a')
    s.ellipse(6, 0, 14, 3, '#9fd8f0'); s.line(8, 1, 11, 1, WHITE)


def kasa_obake(s, k):
    # Schirmgeist: Papierschirm, ein Auge, Zunge, ein Bein mit Geta
    hop = 2 if k else 0
    s.line(10, 17 - hop, 10, 21 - hop, '#c8a070')
    s.rect(7, 22 - hop, 13, 23 - hop, '#6a4a32'); s.px(8, 23 - hop + 0, '#4a3020')
    s.polygon([(10, 0 - hop), (19, 14 - hop), (1, 14 - hop)], PURPLE[1])
    s.polygon([(10, 0 - hop), (19, 14 - hop), (13, 14 - hop)], PURPLE[0])
    s.polygon([(10, 0 - hop), (4, 11 - hop), (7, 11 - hop)], PURPLE[2])
    for x in (4, 10, 16):
        s.line(10, 1 - hop, x, 14 - hop, PURPLE[0])
    s.rect(1, 14 - hop, 19, 15 - hop, PURPLE[0])
    s.px(10, -1 - hop, '#c8a070')
    s.ellipse(7, 6 - hop, 12, 10 - hop, WHITE); s.rect(8, 7 - hop, 9, 9 - hop, INK)
    s.polygon([(6, 12 - hop), (9, 12 - hop), (7, 18 - hop + k), (5, 17 - hop)], '#e0506a')


def bakezori(s, k):
    # Strohsandale mit Auge, Ärmchen und Beinchen
    legs2(s, (5, 12), 14, k, '#6a4a32')
    s.polygon([(2, 3), (15, 1), (17, 11), (4, 13)], TAN[1])
    s.polygon([(10, 2), (15, 1), (17, 11), (12, 12)], TAN[0])
    for y in (4, 7, 10):
        s.line(3, y, 15, y - 1, TAN[0])
    s.line(3, 3, 8, 2, TAN[2])
    s.line(9, 2, 9, 7, '#c83a3a'); s.line(9, 7, 6, 10, '#c83a3a')     # Riemen
    s.ellipse(4, 4, 9, 8, WHITE); s.rect(5, 5, 6, 6, INK)
    s.line(1, 8 + k, 0, 6 + k, TAN[0]); s.line(17, 8 - k, 18, 6 - k, TAN[0])


def tsuchinoko(s, k):
    # Dicke Schlange
    s.ellipse(2, 3 + k, 22, 13 - k, BROWN[0])
    s.ellipse(2, 3 + k, 21, 12 - k, BROWN[1], only=BROWN[0])
    s.ellipse(4, 4 + k, 14, 7, BROWN[2], only=BROWN[1])
    for x in (9, 14, 18):
        s.polygon([(x, 5 + k), (x + 2, 7), (x, 9 - k + 1), (x - 2, 7)], '#d8b45a')
    s.polygon([(21, 7), (24, 6), (24, 9)], BROWN[0])
    s.rect(4, 6 + k, 5, 7 + k, INK); s.px(4, 6 + k, '#ffd84a')
    s.line(0, 9, 2, 9, '#d84a4a'); s.px(0, 8, '#d84a4a')


def kitsunebi_e(s, k):
    # Fuchsfeuer mit Fuchsgesicht
    flame(s, 8, 18, 6, 16, R('#f070a0', hs=24, dark=0.35, light=0.75), k, lean=1)
    s.polygon([(3, 8), (4, 3), (7, 7)], '#ffe0f0'); s.polygon([(10, 7), (12, 3), (13, 8)], '#ffe0f0')
    s.line(5, 12, 6, 11, INK); s.line(10, 11, 11, 12, INK)
    s.px(8, 14, INK)


def chochin(s, k):
    # Papierlaterne mit Riss-Maul und Zunge
    s.rect(5, 0, 11, 1, '#3a2a2a'); s.rect(5, 22, 11, 23, '#3a2a2a')
    blob(s, 2, 2, 14, 22, R('#f0a040', hs=22, dark=0.3, light=0.7))
    for y in (6, 10, 14, 18):
        s.line(3, y, 13, y, '#c86a20')
    s.ellipse(3, 5, 8, 10, WHITE); s.rect(4, 7, 5, 8, INK)
    s.polygon([(3, 13), (13, 12), (12, 17), (4, 16)], '#4a1a1a')
    s.polygon([(5, 15), (9, 15), (7, 21 + k), (5, 20)], '#e0506a')
    s.px(11, 13, WHITE); s.px(9, 13, WHITE)


def nopperabo(s, k):
    # Gesichtsloser Mensch im Kimono
    legs2(s, (6, 11), 22, k, '#3a2a2e')
    s.polygon([(4, 11), (15, 11), (16, 22), (3, 22)], BLUE[1])
    s.polygon([(11, 11), (15, 11), (16, 22), (12, 22)], BLUE[0])
    s.line(9, 11, 6, 18, CLOTH[2]); s.line(5, 16, 14, 16, '#c8a24a')
    s.rect(2, 12, 4, 17 + k, BLUE[1])
    blob(s, 4, 1, 15, 12, SKIN)                     # glattes Gesicht ohne Züge
    s.ellipse(4, 0, 15, 5, '#2a2230'); s.rect(13, 2, 15, 9, '#2a2230')
    s.line(6, 1, 9, 1, '#4a4058')


def gaki(s, k, small=False):
    # Hungergeist: dürre Glieder, Blähbauch, hohle Augen
    G = R('#9aa87a', hs=18)
    legs2(s, (6, 12), 20, k, G[0])
    s.ellipse(4, 10, 17, 20, G[0]); s.ellipse(4, 10, 16, 19, G[1], only=G[0]); s.ellipse(6, 12, 11, 16, G[2], only=G[1])
    s.px(10, 15, G[0])
    s.line(4, 11, 1, 16 + k, G[0]); s.line(1, 16 + k, 0, 18 + k, G[0])
    blob(s, 3, 1, 14, 11, G)
    s.rect(5, 4, 6, 6, INK); s.rect(10, 4, 11, 6, INK); s.px(5, 5, '#e8e070'); s.px(10, 5, '#e8e070')
    s.line(6, 8, 10, 9, INK); s.px(7, 9, WHITE)
    s.line(4, 1, 7, 0, '#3a3a2a'); s.line(10, 0, 13, 2, '#3a3a2a')


def gaki_small(s, k):
    G = R('#9aa87a', hs=18)
    s.rect(4, 11 - k, 5, 12, G[0]); s.rect(8, 11 + k - 1, 9, 12, G[0])
    s.ellipse(2, 6, 11, 12, G[0]); s.ellipse(2, 6, 10, 11, G[1], only=G[0])
    blob(s, 2, 0, 10, 7, G)
    s.px(4, 3, INK); s.px(7, 3, INK); s.line(4, 5, 7, 5, INK)


def ittan_momen(s, k):
    # Fliegendes Stoffband mit Augen
    w = [0, 1][k]
    pts = [(0, 6), (6, 3), (12, 5 + w), (18, 8 - w), (24, 6), (28, 9 + w), (27, 12 + w), (22, 10), (17, 13 - w), (11, 10 + w), (6, 9), (1, 10)]
    s.polygon(pts, CLOTH[1])
    s.polygon([(12, 9 + w), (17, 12 - w), (22, 10), (27, 12 + w), (28, 9 + w), (24, 7), (18, 9 - w)], CLOTH[0])
    s.line(1, 6, 6, 4, CLOTH[3]); s.line(7, 4, 11, 5, CLOTH[2])
    s.rect(3, 7, 4, 8, INK); s.rect(7, 7, 8, 8, INK); s.px(3, 7, '#d8e8ff'); s.px(7, 7, '#d8e8ff')


def bakeneko(s, k):
    # Spukkatze im Sprung, glühende Augen, gespaltener Schwanz-Ansatz
    C = R('#e0b070', hs=16)
    run_ = [(4, 14, 7, 15), (5, 13, 6, 15)][k]
    s.polygon([(16, 8), (22, 2 - k), (21, 6), (18, 10)], C[0])                # Schwanz
    s.ellipse(5, 6, 19, 15, C[0]); s.ellipse(5, 6, 18, 14, C[1], only=C[0]); s.ellipse(7, 7, 14, 10, C[2], only=C[1])
    for x in (12, 15):
        s.line(x, 8, x + 1, 13, mix(C[0], '#6a3a1a', 0.5))
    s.rect(run_[0], run_[1], run_[2] - 1, 17, C[0]); s.rect(15 - k, 13, 16 - k, 17, C[0])
    blob(s, 0, 2, 9, 11, C)
    s.polygon([(0, 4), (1, -1 + 1), (3, 3)], C[1]); s.polygon([(5, 3), (7, 0), (8, 4)], C[0])
    s.px(2, 6, '#ffe84a'); s.px(5, 6, '#ffe84a'); s.px(2, 7, INK); s.px(5, 7, INK)
    s.px(3, 9, '#d06070'); s.line(0, 8, -1 + 1, 8, '#ffffff')


def onibi(s, k):
    # Dämonenfeuer: blauviolette Flamme mit Totenkopfgesicht
    flame(s, 8, 18, 6, 16, R('#7a6af0', hs=24, dark=0.4, light=0.75), k, lean=-1)
    s.rect(5, 10, 6, 11, INK); s.rect(10, 10, 11, 11, INK)
    s.line(6, 14, 10, 14, INK); s.px(7, 15, INK); s.px(9, 15, INK)


def karasu_tengu(s, k):
    # Krähen-Tengu mit Flügeln, Schnabel, rotem Gewand, Tokin
    Wg = R('#2c2a40', hs=18, dark=0.3, light=0.5)
    fl = [0, -3][k]
    s.polygon([(12, 9), (23, 2 + fl), (22, 12), (17, 17)], Wg[0])
    s.line(13, 10, 22, 4 + fl, Wg[2]); s.line(15, 13, 21, 9 + fl, Wg[1])
    legs2(s, (8, 12), 20, k, '#2a2228')
    s.polygon([(6, 10), (15, 10), (16, 20), (5, 20)], RED[1]); s.polygon([(11, 10), (15, 10), (16, 20), (12, 20)], RED[0])
    s.line(6, 11, 6, 19, RED[2]); s.line(5, 16, 15, 16, '#e8d070')
    s.polygon([(2, 9), (8, 3 + fl), (9, 12)], Wg[1])                       # vorderer Flügel
    blob(s, 5, 1, 15, 11, Wg)
    s.polygon([(5, 5), (0, 7), (5, 9)], '#e8a838'); s.px(2, 7, '#ffd36a')
    s.px(7, 5, '#ffd84a'); s.rect(8, -1 + 1, 11, 1, '#1c1a24')


def yuki_warashi(s, k):
    # Schneekind im Strohmantel mit Schneehut
    legs2(s, (6, 10), 18, k, '#3a3446')
    s.polygon([(3, 9), (14, 9), (16, 19), (1, 19)], R('#c8b070')[1])
    for x in range(2, 16, 2):
        s.line(x, 12, x - 1 + (x % 4) // 2, 19, R('#c8b070')[0])
    s.ellipse(4, 3, 13, 11, R('#f6e4dc', 3, hs=10)[1])
    s.ellipse(11, 5, 13, 11, R('#f6e4dc', 3, hs=10)[0], only=R('#f6e4dc', 3, hs=10)[1])
    s.px(6, 7, INK); s.px(9, 7, INK); s.px(5, 9, '#f08aa0'); s.px(10, 9, '#f08aa0')
    s.ellipse(1, 0, 16, 5, CLOTH[1]); s.ellipse(1, 2, 16, 5, CLOTH[0], only=CLOTH[1]); s.line(4, 0, 9, 0, WHITE)


def kamaitachi(s, k):
    # Sichelwiesel
    C = R('#c8a070', hs=16)
    s.polygon([(14, 8), (22, 4 - k), (21, 8), (16, 11)], C[0])
    s.ellipse(4, 6, 17, 13, C[0]); s.ellipse(4, 6, 16, 12, C[1], only=C[0]); s.ellipse(6, 7, 12, 9, C[2], only=C[1])
    legs2(s, (7, 13), 13, k, C[0])
    blob(s, 0, 3, 8, 10, C)
    s.px(1, 3, C[1]); s.px(5, 2, C[0])
    s.px(2, 6, INK); s.px(0, 7, INK)
    s.polygon([(5, 10), (1, 13 + k), (0, 11 + k), (3, 9)], '#dfe6f2'); s.line(1, 12 + k, 4, 10, '#9aa6c0')
    s.polygon([(10, 11), (6, 15), (5, 13), (8, 10)], '#c8d0e0')


def yamabiko(s, k):
    # Echo-Wesen: zottelig, großes Maul
    F = R('#9a8a7a', hs=14)
    legs2(s, (5, 11), 18, k, F[0])
    blob(s, 2, 4, 16, 19, F)
    for x in range(3, 16, 3):
        s.line(x, 16, x - 1, 19, F[0])
    s.polygon([(4, 4), (5, 0), (8, 3)], F[1]); s.polygon([(11, 3), (14, 0), (15, 5)], F[0])
    s.px(6, 8, INK); s.px(11, 8, INK); s.px(6, 7, '#ffe070'); s.px(11, 7, '#ffe070')
    s.ellipse(6, 10, 12, 14 + k, '#4a1a1a'); s.px(7, 10, WHITE); s.px(11, 10, WHITE)
    s.line(1, 10, 0, 13 + k, F[0]); s.line(17, 10, 18, 13 - k, F[0])


def heikegani(s, k):
    # Krabbe mit Samuraigesicht auf dem Panzer
    for i, x in enumerate((3, 6, 15, 18)):
        d = (k + i) % 2
        s.line(x, 11, x - (2 if x < 10 else -2), 15 - d, RED[0])
    s.polygon([(0, 5 - k), (3, 2), (5, 7), (2, 8)], RED[1]); s.line(0, 5 - k, 2, 4, RED[0])
    s.polygon([(21, 5 + k - 1), (18, 2), (16, 7), (19, 8)], RED[0])
    blob(s, 3, 4, 19, 14, RED)
    s.line(6, 7, 9, 8, INK); s.line(16, 7, 13, 8, INK)          # zornige Brauen
    s.px(8, 9, INK); s.px(14, 9, INK)
    s.line(8, 12, 14, 12, INK); s.px(11, 11, RED[0])
    s.px(5, 2, INK); s.px(16, 2, INK); s.line(6, 3, 6, 5, RED[0]); s.line(15, 3, 15, 5, RED[0])


def funayurei(s, k):
    # Ertrunkener Geist mit Schöpfkelle, ohne Beine
    P = R('#cfe0ee', hs=14, dark=0.3, light=0.5)
    sw = [0, 1][k]
    s.polygon([(4, 10), (14, 10), (16, 20), (12 + sw, 24), (9 + sw, 21), (6 + sw, 24), (3, 19)], P[1])
    s.polygon([(10, 10), (14, 10), (16, 20), (12 + sw, 24), (10, 21)], P[0])
    s.line(5, 11, 4, 18, P[2])
    s.line(2, 12, 0, 6, '#8a6a4a'); s.ellipse(-1 + 1, 3, 3, 6, '#6a4a32')     # Kelle
    s.rect(2, 12, 4, 14, P[1])
    blob(s, 4, 1, 14, 11, R('#b8d0e0', 3, hs=12))
    s.rect(3, 0, 15, 3, '#1e2030'); s.rect(3, 3, 5, 13, '#1e2030'); s.rect(12, 3, 15, 14, '#1e2030')
    s.px(7, 6, '#1a3a5a'); s.px(10, 6, '#1a3a5a'); s.line(7, 9, 10, 9, '#5a7a9a')
    s.polygon([(7, 3), (11, 3), (9, 5)], WHITE)


def ningyo(s, k):
    # Meerjungfisch mit Menschengesicht
    F = R('#e890a8', hs=20)
    t = [0, 2][k]
    s.polygon([(14, 10), (21, 6 - t), (19, 11), (21, 16 + t)], F[0])
    s.ellipse(5, 6, 18, 15, F[0]); s.ellipse(5, 6, 17, 14, F[1], only=F[0]); s.ellipse(7, 7, 13, 9, F[2], only=F[1])
    for x in (9, 12, 15):
        s.line(x, 8, x - 1, 13, F[0])
    s.polygon([(10, 6), (13, 2), (15, 7)], F[0])
    blob(s, 0, 3, 9, 12, SKIN)
    s.rect(1, 1, 9, 4, '#3a2a4a'); s.rect(6, 4, 9, 13, '#3a2a4a')
    s.px(2, 7, INK); s.px(5, 7, INK); s.px(3, 10, '#c04a5a')


def isonade(s, k):
    # Meeresungeheuer mit Hakenflosse
    S = R('#4a6a8a', hs=18)
    s.ellipse(2, 7, 22, 16, S[0]); s.ellipse(2, 7, 21, 15, S[1], only=S[0]); s.ellipse(4, 8, 14, 10, S[2], only=S[1])
    s.ellipse(4, 12, 18, 16, '#d8dce8', only=S[1])
    s.polygon([(9, 7), (13, 0), (15, 7)], S[0]); s.line(12, 2, 13, 6, S[2])
    s.polygon([(20, 11), (24, 5 + k), (25, 8 + k), (23, 12), (25, 17 - k), (21, 14)], S[0])
    s.polygon([(23, 6 + k), (21, 4 + k), (23, 5 + k)], '#e8e4d0')
    s.px(5, 10, '#ffd84a'); s.px(5, 11, INK)
    for x in range(3, 9, 2):
        s.px(x, 14, WHITE)
    s.line(2, 13, 9, 13, INK)


def oni(s, k):
    # Roter Oni mit Hörnern, Tigerfell und Kanabō
    Rk = R('#d0483c', hs=16)
    legs2(s, (9, 18), 30, k, Rk[0], h=3)
    s.rect(7, 31, 12, 31, Rk[0]); s.rect(16, 31, 21, 31, Rk[0])
    s.rect(8, 21, 22, 28, '#e8c040')                                  # Tigerfell
    for x in (10, 14, 18):
        s.line(x, 21, x + 1, 27, '#3a2a1a')
    blob(s, 6, 9, 24, 24, Rk)                                         # Oberkörper
    s.line(12, 15, 14, 18, Rk[0]); s.line(18, 15, 16, 18, Rk[0])
    s.rect(23, 11, 26, 20, Rk[0])                                      # hinterer Arm
    # Keule (Kanabō) im vorderen Arm
    s.polygon([(0, 2 + k), (5, 1 + k), (8, 16), (5, 17)], '#5a5468')
    s.line(1, 3 + k, 5, 16, '#8a86a0')
    for y in (5, 9, 13):
        s.px(1 + y // 5, y + k, '#c8c4d8'); s.px(5 + y // 6, y - 1 + k, '#c8c4d8')
    s.rect(4, 13, 9, 18, Rk[1]); s.px(5, 14, Rk[2])
    blob(s, 8, 1, 22, 14, Rk)                                          # Kopf
    s.polygon([(10, 2), (14, 0), (20, 2), (21, 5), (9, 5)], '#2a1e24')
    s.polygon([(8, 4), (6, -2), (11, 2)], '#f2e6c4'); s.polygon([(19, 2), (24, -2), (22, 4)], '#e0d0a8')
    s.px(7, -1, '#fffaf0')
    s.line(10, 6, 13, 7, INK); s.line(19, 6, 16, 7, INK)
    s.rect(11, 7, 12, 8, '#ffe070'); s.rect(17, 7, 18, 8, '#ffe070'); s.px(12, 8, INK); s.px(17, 8, INK)
    s.rect(11, 10, 19, 12, '#4a1a1a'); s.px(12, 10, WHITE); s.px(18, 10, WHITE); s.px(12, 9, WHITE); s.px(18, 9, WHITE)


def shikome(s, k):
    # Hexe aus Yomi: wildes weißes Haar, violette Haut, Krallen
    Sk = R('#9a7ab0', 3, hs=14)
    legs2(s, (6, 11), 22, k, '#2a2230')
    s.polygon([(3, 11), (15, 11), (17, 22), (2, 22)], DARK[1]); s.polygon([(11, 11), (15, 11), (17, 22), (12, 22)], DARK[0])
    s.line(3, 13, 0, 9 + k, Sk[0]); s.line(0, 9 + k, -1 + 1, 7 + k, WHITE); s.line(1, 9 + k, 1, 7 + k, WHITE)
    s.polygon([(1, 4), (9, -1 + 1), (18, 3), (19, 13), (14, 9), (4, 12)], '#e8e4f0')
    blob(s, 4, 2, 14, 12, Sk)
    s.polygon([(3, 2), (9, 0), (16, 2), (15, 5), (10, 3), (4, 5)], '#f2eef8')
    s.px(6, 6, '#ff3a3a'); s.px(11, 6, '#ff3a3a'); s.line(6, 9, 11, 9, INK); s.px(7, 10, WHITE); s.px(10, 10, WHITE)


def tsuchigumo(s, k):
    # Erdspinne: großer Körper, Tigerzeichnung, acht Beine
    B = R('#7a5a3a', hs=16)
    for i, (x, dx) in enumerate(((5, -5), (8, -4), (19, 5), (22, 5))):
        d = (i + k) % 2
        s.line(x, 12, x + dx, 8 - d, B[0]); s.line(x + dx, 8 - d, x + dx - (1 if dx < 0 else -1), 20, B[0])
    blob(s, 10, 4, 28, 20, B)                                         # Hinterleib
    for x in (15, 19, 23):
        s.line(x, 6, x - 1, 18, '#e8c040')
    blob(s, 2, 8, 14, 18, B)                                          # Kopfbrust
    for x, y in ((4, 11), (6, 10), (8, 11), (5, 13)):
        s.px(x, y, '#ff4a3a')
    s.line(3, 16, 1, 19, '#e8e0c8'); s.line(7, 16, 8, 19, '#e8e0c8')


def kumo(s, k):
    B = R('#4a3a5a', hs=16)
    for i, x in enumerate((2, 4, 7, 9)):
        d = (i + k) % 2
        s.line(x, 5, x + (-2 if x < 5 else 2), 9 - d, B[0])
    blob(s, 2, 1, 10, 8, B)
    s.px(3, 4, '#ff4a3a'); s.px(5, 4, '#ff4a3a')


def shinigami(s, k):
    # Todesgott: Kapuzenrobe, Schädelgesicht, Sense
    D = R('#2a2638', hs=18, dark=0.35, light=0.5)
    sw = [0, 1][k]
    s.polygon([(4, 9), (18, 9), (21, 26), (16 + sw, 28), (12, 25), (8 + sw, 28), (2, 25)], D[1])
    s.polygon([(13, 9), (18, 9), (21, 26), (16 + sw, 28), (14, 24)], D[0])
    s.line(5, 11, 4, 22, D[2])
    s.line(0, 1, 3, 27, '#7a5a3a')                                    # Stiel
    s.polygon([(0, 1), (11, -1 + 1), (16, 3), (8, 2), (1, 4)], '#d8dce8'); s.line(1, 2, 10, 1, WHITE)
    s.rect(2, 13, 5, 16, BONE[1])
    s.ellipse(4, 1, 18, 14, D[1]); s.ellipse(12, 2, 18, 14, D[0], only=D[1])
    blob(s, 6, 4, 14, 12, BONE)
    s.rect(7, 7, 8, 8, INK); s.rect(11, 7, 12, 8, INK); s.px(8, 7, '#ff5a5a'); s.px(11, 7, '#ff5a5a')
    s.line(8, 11, 12, 11, INK)


def tesso(s, k):
    # Eiserne Ratte
    M = R('#8a8aa0', hs=16)
    s.line(9, 7, 12, 4 - k, '#c89090')
    s.ellipse(2, 3, 11, 10, M[0]); s.ellipse(2, 3, 10, 9, M[1], only=M[0]); s.ellipse(3, 4, 6, 5, M[3], only=M[1])
    s.circle(4, 3, 1, M[2], fill=True)
    s.px(2, 5, '#ff4a3a'); s.px(0, 7, '#f0a0a0')
    s.px(4, 10, M[0]); s.px(8, 10 - k, M[0])


def abura_akago(s, k):
    # Ölbaby mit Flämmchen über dem Kopf
    Sk = R('#f0a888', 3, hs=12)
    flame(s, 8, 6, 3, 7, FIRE, k)
    s.ellipse(3, 11, 13, 18, Sk[0]); s.ellipse(3, 11, 12, 17, Sk[1], only=Sk[0])
    blob(s, 3, 4, 13, 13, Sk)
    s.px(6, 8, INK); s.px(10, 8, INK); s.ellipse(7, 10, 9, 12, '#a03a3a'); s.px(8, 12, '#e0607a')
    s.px(5, 18, Sk[0]); s.px(11, 18, Sk[0])


def nurikabe(s, k):
    # Wandgeist: Mauer mit Augen und Stummelbeinen
    W_ = R('#a09a8a', hs=12)
    legs2(s, (8, 26), 33, k, W_[0], h=3)
    s.rect(2, 2, 34, 32, W_[0]); s.rect(2, 2, 32, 30, W_[1])
    for y in range(2, 32, 6):
        s.line(2, y, 33, y, W_[0])
        off = 0 if (y // 6) % 2 else 5
        for x in range(2 + off, 34, 10):
            s.line(x, y, x, y + 5, W_[0])
    s.line(3, 3, 31, 3, W_[2]); s.line(3, 3, 3, 28, W_[2])
    s.noise(4, 4, 30, 30, W_[0], density=0.025, seed=7)
    s.ellipse(8, 10, 14, 15, WHITE); s.ellipse(21, 10, 27, 15, WHITE)
    s.rect(9, 12, 11, 14, INK); s.rect(22, 12, 24, 14, INK)
    s.line(13, 22, 23, 22, INK); s.line(12, 21, 13, 22, INK)


def mokumokuren(s, k):
    # Shōji-Schiebewand voller Augen
    s.rect(0, 0, 21, 21, '#6a4a32'); s.rect(1, 1, 20, 20, '#f4ecd8')
    for x in (7, 14):
        s.line(x, 1, x, 20, '#8a6a4a')
    for y in (7, 14):
        s.line(1, y, 20, y, '#8a6a4a')
    s.line(1, 1, 20, 1, WHITE)
    for i, (x, y) in enumerate(((3, 3), (10, 4), (16, 2), (2, 10), (9, 10), (16, 9), (4, 16), (11, 17), (17, 16))):
        if (i + k) % 4 == 0:
            s.line(x, y + 1, x + 2, y + 1, INK)
        else:
            s.ellipse(x, y, x + 3, y + 2, WHITE); s.rect(x + 1, y + 1, x + 2, y + 1, '#c83a3a'); s.px(x + 1, y + 1, INK)


def jinmenju(s, k):
    # Baum mit Menschengesicht-Früchten
    T = R('#6a4a32', hs=14)
    L_ = R('#3f8a4a', hs=18)
    s.rect(9, 14, 15, 27, T[1]); s.rect(13, 14, 15, 27, T[0]); s.line(10, 15, 10, 26, T[2])
    s.polygon([(9, 27), (5, 27), (9, 24)], T[0]); s.polygon([(15, 27), (19, 27), (15, 24)], T[0])
    blob(s, 0, 1, 24, 18, L_)
    s.noise(1, 2, 23, 17, L_[0], density=0.06, seed=3)
    for x, y in ((3, 7), (14, 4), (9, 11), (18, 11)):
        s.ellipse(x, y + k, x + 4, y + 4 + k, '#f2d8a8'); s.px(x + 1, y + 2 + k, INK); s.px(x + 3, y + 2 + k, INK); s.px(x + 2, y + 3 + k, '#c04a4a')
    s.rect(10, 18, 14, 20, '#2a1a12'); s.px(11, 17, '#ffd84a'); s.px(13, 17, '#ffd84a')


def yosuzume(s, k):
    # Nachtsperling
    B = R('#5a4a6a', hs=16)
    fl = [0, -2][k]
    s.polygon([(5, 4), (10, 0 + fl), (9, 5)], B[0])
    blob(s, 2, 2, 10, 9, B)
    s.polygon([(2, 5), (0, 6), (2, 7)], '#e8a838'); s.px(3, 4, '#ffd84a')
    s.polygon([(9, 6), (12, 5), (11, 8)], B[0])


def enenra(s, k):
    # Rauchwesen mit Gesicht
    S = R('#8a8a9a', hs=12, dark=0.35, light=0.7)
    for i, (x, y, r) in enumerate(((4, 14, 4), (10, 17, 4), (16, 12, 5), (8, 7, 5), (15, 5, 4), (19, 18, 3))):
        yy = y + (k if i % 2 else -k)
        s.ellipse(x - r, yy - r, x + r, yy + r, S[0])
        s.ellipse(x - r, yy - r, x + r - 1, yy + r - 1, S[1], only=S[0])
        s.ellipse(x - r + 1, yy - r + 1, x, yy - 1, S[2], only=S[1])
    s.rect(6, 7, 7, 8, INK); s.rect(11, 7, 12, 8, INK); s.px(6, 7, '#ffe07a'); s.px(11, 7, '#ffe07a')
    s.ellipse(7, 10, 11, 12, '#3a3040')


def gyuki(s, k):
    # Ushi-oni: Stierkopf auf Spinnenkörper
    B = R('#4a3a4a', hs=16)
    for i, (x, dx) in enumerate(((7, -6), (11, -5), (19, 5), (24, 6))):
        d = (i + k) % 2
        s.line(x, 14, x + dx, 10 - d, B[0]); s.line(x + dx, 10 - d, x + dx + (1 if dx < 0 else -1), 25, B[0])
        s.px(x + dx, 10 - d, B[2])
    blob(s, 8, 6, 29, 22, B)
    s.line(12, 9, 26, 9, B[2])
    blob(s, 0, 4, 12, 16, R('#7a3a3a', hs=14))
    s.polygon([(2, 5), (-1 + 1, 0), (4, 3)], '#f2e6c4'); s.polygon([(9, 4), (12, -1 + 1), (11, 5)], '#e0d0a8')
    s.px(3, 8, '#ff4a3a'); s.px(8, 8, '#ff4a3a')
    s.ellipse(2, 11, 8, 15, '#c87a6a'); s.px(4, 13, INK); s.px(6, 13, INK)


def kamikiri(s, k):
    # Haarschneider: Vogelschnabel, Scherenhände
    B = R('#3a3a4a', hs=16)
    legs2(s, (6, 11), 18, k, B[0])
    blob(s, 4, 6, 15, 19, B)
    s.polygon([(1, 9), (-1 + 1, 3 + k), (4, 8)], '#c8d0e0'); s.polygon([(2, 10), (0, 15 - k), (5, 11)], '#c8d0e0')
    s.line(4, 9, 2, 9, B[0])
    blob(s, 5, 0, 15, 9, B)
    s.polygon([(5, 4), (0, 6), (5, 7)], '#e0a03a')
    s.px(8, 3, '#ff4a3a'); s.px(9, 3, INK)


def kerakera_onna(s, k):
    # Riesige lachende Frau im Kimono
    Sk = R('#f2d8c8', 3, hs=10)
    K_ = R('#c84a6a', hs=18)
    s.polygon([(4, 16), (24, 16), (27, 31), (1, 31)], K_[1]); s.polygon([(16, 16), (24, 16), (27, 31), (18, 31)], K_[0])
    s.line(14, 16, 8, 31, '#f2e0a0'); s.rect(4, 22, 24, 24, '#3a2a4a')
    for x, y in ((7, 18), (20, 27), (12, 28)):
        s.px(x, y, '#ffd0e0')
    blob(s, 5, 2, 23, 18, Sk)
    s.ellipse(3, -1 + 1, 25, 8, '#1e1a26'); s.rect(3, 4, 6, 18, '#1e1a26'); s.rect(22, 4, 25, 18, '#1e1a26')
    s.rect(11, -1 + 1, 17, 1, '#1e1a26')
    s.line(9, 8, 12, 9, INK); s.line(16, 9, 19, 8, INK)                  # lachende Augen
    s.ellipse(10, 11, 18, 17 + k, '#5a1a2a'); s.ellipse(11, 11, 17, 12, WHITE); s.ellipse(11, 15 + k, 17, 17 + k, '#e05a6a')
    s.px(8, 12, '#f08aa0'); s.px(20, 12, '#f08aa0')


def sazae_oni(s, k):
    # Turbanschnecken-Oni: Schneckenhaus mit Fratze
    Sh = R('#c88a6a', hs=18)
    s.ellipse(1, 12 - k, 18, 17, R('#d8b0a0')[1])
    blob(s, 4, 1, 19, 15, Sh)
    for y, x in ((3, 8), (6, 6), (9, 5)):
        s.line(x, y, x + 9, y + 1, Sh[0])
    for x, y in ((6, 1), (11, 0), (16, 2), (19, 7)):
        s.polygon([(x - 1, y + 2), (x, y - 2), (x + 1, y + 2)], Sh[2])
    s.ellipse(0, 6, 8, 15, R('#9a6aa0', 3)[1])
    s.px(2, 9, '#ffe070'); s.px(5, 9, '#ffe070'); s.line(2, 12, 6, 12, INK); s.px(3, 13, WHITE); s.px(5, 13, WHITE)
    s.polygon([(1, 7), (0, 4), (3, 6)], '#f2e6c4')


def hyosube(s, k):
    # Hyōsube: glatzköpfig, haarig, breites Grinsen
    F = R('#8a6a4a', hs=14)
    legs2(s, (5, 10), 19, k, F[0])
    blob(s, 2, 8, 15, 19, F)
    for x in range(3, 15, 2):
        s.px(x, 18 - (x % 3), F[2])
    s.line(2, 11, 0, 15 + k, F[0]); s.line(15, 11, 16, 15 - k, F[0])
    blob(s, 3, 0, 14, 10, R('#d8b090', 3, hs=12))
    s.px(5, 4, INK); s.px(10, 4, INK)
    s.line(4, 7, 11, 7, INK); s.line(5, 8, 10, 8, WHITE)


def tenome(s, k):
    # Blinder Alter mit Augen in den Handflächen
    legs2(s, (6, 11), 22, k, '#3a3040')
    s.polygon([(4, 10), (14, 10), (16, 22), (2, 22)], GRAY[1]); s.polygon([(10, 10), (14, 10), (16, 22), (11, 22)], GRAY[0])
    s.line(4, 11, 3, 20, GRAY[2])
    blob(s, 4, 1, 14, 11, SKIN)
    s.line(5, 5, 7, 5, INK); s.line(10, 5, 12, 5, INK)            # geschlossene Augen
    s.line(7, 9, 10, 9, SKIN[0]); s.ellipse(4, 0, 14, 3, '#d8d8e0')
    up = [0, -1][k]
    for hx in (0, 16):
        s.line(hx + 2, 12, hx + 1, 6 + up, SKIN[0])
        s.ellipse(hx - 1, 2 + up, hx + 3, 6 + up, SKIN[1]); s.ellipse(hx, 3 + up, hx + 2, 5 + up, WHITE); s.px(hx + 1, 4 + up, '#c83a3a')


def nekomata(s, k):
    # Zweischwänzige Katze, violett mit Geisterflämmchen
    C = R('#7a5aa8', hs=18)
    for dx, tt in ((0, 0), (3, 1)):
        s.line(16 + dx, 9, 20 + dx, 2 + (k if tt else -k) + 1, C[0]); s.line(17 + dx, 9, 21 + dx, 3 + (k if tt else -k) + 1, C[1])
        s.px(20 + dx, 1 + (k if tt else -k) + 1, '#c8b0ff')
    s.ellipse(5, 6, 19, 15, C[0]); s.ellipse(5, 6, 18, 14, C[1], only=C[0]); s.ellipse(7, 7, 13, 9, C[2], only=C[1])
    legs2(s, (6, 9, 13, 16), 15, k, C[0])
    blob(s, 0, 2, 9, 11, C)
    s.polygon([(0, 4), (1, 0), (3, 3)], C[1]); s.polygon([(5, 3), (7, 0), (8, 4)], C[0])
    s.px(2, 6, '#7aff9a'); s.px(5, 6, '#7aff9a'); s.px(3, 9, '#e07a9a')


def kasha(s, k):
    # Feuerkatze, umhüllt von Flammen
    C = R('#3a2a2a', hs=14)
    for x, h in ((5, 10), (11, 12), (17, 9), (21, 7)):
        flame(s, x, 14, 3, h + (k if x % 2 else -k), FIRE, k)
    s.ellipse(4, 9, 20, 17, C[0]); s.ellipse(4, 9, 19, 16, C[1], only=C[0])
    legs2(s, (6, 10, 14, 18), 17, k, C[0])
    blob(s, 0, 5, 9, 14, C)
    s.polygon([(0, 7), (1, 3), (3, 6)], C[1]); s.polygon([(5, 6), (7, 3), (8, 7)], C[0])
    s.px(2, 9, '#ffd84a'); s.px(5, 9, '#ffd84a'); s.line(1, 12, 4, 12, '#ff6a3a')


def tsurube_otoshi(s, k):
    # Riesenkopf, der aus dem Baum fällt – wirres Haar, Riesenmaul
    Sk = R('#d8b8a0', 3, hs=12)
    s.line(13, 0, 13, 4, '#6a4a32')
    s.ellipse(1, 2, 25, 25, '#1e1a22')
    for x in range(2, 25, 3):
        s.line(x, 20, x - 1 + (x % 2) * 2, 26, '#1e1a22')
    blob(s, 4, 6, 22, 24, Sk)
    s.polygon([(4, 6), (13, 3), (22, 6), (20, 10), (13, 7), (6, 10)], '#1e1a22')
    s.line(7, 11, 11, 12, INK); s.line(19, 11, 15, 12, INK)
    s.rect(8, 12, 10, 14, '#ffe070'); s.rect(16, 12, 18, 14, '#ffe070'); s.px(9, 13, INK); s.px(17, 13, INK)
    s.ellipse(8, 16, 18, 22 + k, '#4a1a1a')
    for x in range(9, 18, 2):
        s.px(x, 16, WHITE); s.px(x, 21 + k, WHITE)


def wheel(s, k, face_skin, hair, fire, bald=False):
    cx, cy = 13, 14
    for i in range(8):
        import math
        a = i / 8 * math.tau + k * 0.4
        x, y = cx + math.cos(a) * 11, cy + math.sin(a) * 11
        s.ellipse(int(x) - 3, int(y) - 3, int(x) + 3, int(y) + 3, fire[1])
        s.ellipse(int(x) - 2, int(y) - 2, int(x) + 1, int(y) + 1, fire[2])
    s.circle(cx, cy, 10, '#5a4030', fill=True)
    s.circle(cx, cy, 10, '#3a2a1e')
    for i in range(6):
        import math
        a = i / 6 * math.tau + k * 0.5
        s.line(cx, cy, cx + int(math.cos(a) * 9), cy + int(math.sin(a) * 9), '#3a2a1e')
    blob(s, cx - 6, cy - 6, cx + 6, cy + 7, face_skin)
    if not bald:
        s.ellipse(cx - 7, cy - 7, cx + 7, cy - 2, hair); s.rect(cx - 7, cy - 3, cx - 5, cy + 6, hair); s.rect(cx + 5, cy - 3, cx + 7, cy + 6, hair)


def wanyudo(s, k):
    # Flammenrad mit Mönchskopf
    wheel(s, k, R('#d8a080', 3, hs=12), None, FIRE, bald=True)
    s.line(9, 12, 12, 13, INK); s.line(17, 12, 14, 13, INK)
    s.px(10, 14, '#ffe070'); s.px(16, 14, '#ffe070')
    s.ellipse(10, 17, 16, 20, '#5a1a1a'); s.px(11, 17, WHITE); s.px(15, 17, WHITE)


def katawaguruma(s, k):
    # Einrädriger Karren in rosa Flammen mit Frauengesicht
    wheel(s, k, R('#f2d8c8', 3, hs=10), '#1e1a26', R('#f06a9a', hs=22, dark=0.35, light=0.7))
    s.px(10, 14, INK); s.px(16, 14, INK); s.line(11, 18, 15, 18, '#c84a5a')


def azukiarai(s, k):
    # Bohnenwäscher: kleiner Alter mit Sieb
    legs2(s, (5, 9), 19, k, '#5a4a3a')
    s.polygon([(3, 10), (13, 10), (14, 19), (2, 19)], R('#6a8a6a')[1]); s.polygon([(9, 10), (13, 10), (14, 19), (10, 19)], R('#6a8a6a')[0])
    blob(s, 3, 1, 13, 11, SKIN)
    s.ellipse(3, 0, 13, 3, '#e8e8f0'); s.px(5, 5, INK); s.px(10, 5, INK); s.line(6, 8, 9, 8, INK)
    s.line(4, 9, 5, 11, '#e8e8f0'); s.line(11, 9, 10, 11, '#e8e8f0')
    s.ellipse(-1 + 1, 12, 9, 17, '#c8a064'); s.ellipse(1, 12, 8, 14, '#8a6a3a')
    for x in (2, 4, 6):
        s.px(x, 13 - k, '#a83a3a')


def bake_danuki(s, k):
    # Verwandlungs-Tanuki mit Blatt und Sake-Flasche
    F = R('#8a6a4a', hs=14)
    legs2(s, (5, 12), 20, k, F[0])
    blob(s, 2, 8, 17, 21, F)
    s.ellipse(5, 12, 14, 20, '#f0dcc0', only=F[1])
    s.ellipse(14, 12, 20, 19, F[0])
    blob(s, 3, 1, 15, 11, F)
    s.circle(4, 2, 2, F[1], fill=True); s.circle(14, 2, 2, F[0], fill=True)
    s.rect(4, 5, 7, 7, '#3a2a1e'); s.rect(10, 5, 13, 7, '#3a2a1e'); s.px(5, 5, WHITE); s.px(11, 5, WHITE)
    s.px(8, 8, INK); s.px(9, 8, INK)
    s.polygon([(7, 0), (11, -2 + 2), (12, 2), (8, 3)], '#5fae4a')
    s.rect(0, 12, 3, 18, '#e8dcc0'); s.rect(1, 10, 2, 11, '#e8dcc0'); s.line(0, 14, 3, 14, '#c83a3a')


def nuppeppo(s, k):
    # Fleischklumpen mit Hautfalten
    F = R('#e0a0a0', hs=14, dark=0.4, light=0.55)
    s.ellipse(1, 4 + k, 21, 21, F[0]); s.ellipse(1, 4 + k, 20, 20, F[1], only=F[0]); s.ellipse(3, 5 + k, 12, 11, F[2], only=F[1])
    s.ellipse(4, 1 + k, 16, 10 + k, F[1]); s.ellipse(6, 2 + k, 11, 5 + k, F[2], only=F[1])
    for y in (12, 15, 18):
        s.line(4, y, 17, y + 1, F[0])
    s.px(7, 6 + k, INK); s.px(12, 6 + k, INK); s.line(8, 8 + k, 11, 8 + k, F[0])
    s.rect(4, 21, 6, 21, F[0]); s.rect(15, 21, 17, 21, F[0])
    s.line(1, 12, -1 + 1, 15 - k, F[0]); s.line(21, 12, 21, 15 + k, F[0])


def kappa_small(s, k):
    G = GREEN
    legs2(s, (5, 9), 14, k, G[0])
    blob(s, 7, 6, 14, 14, BROWN)
    blob(s, 2, 6, 12, 15, G)
    blob(s, 2, 0, 12, 8, G)
    s.polygon([(1, 5), (3, 4), (3, 7)], '#e8b030')
    s.rect(4, 3, 5, 4, INK); s.px(4, 3, WHITE)
    s.ellipse(4, -1 + 1, 10, 2, '#9fd8f0')


def karasu(s, k):
    # Krähe
    B = R('#2e2c40', hs=18, dark=0.3, light=0.55)
    fl = [0, -4][k]
    s.polygon([(7, 5), (13, 0 + fl), (12, 6)], B[0])
    s.polygon([(11, 6), (15, 5), (14, 9)], B[0])
    blob(s, 3, 3, 13, 10, B)
    blob(s, 1, 1, 7, 7, B)
    s.polygon([(1, 4), (-1 + 1, 5), (1, 6)], '#c8c0b0')
    s.px(3, 3, '#ff4a3a')
    s.polygon([(5, 6), (9, -1 + 2 - fl // 2), (10, 6)], B[1])


# ================================================================ Aufbau
# Name: (Breite, Höhe, Zeichenfunktion) – 1 px Rand für den Umriss kommt automatisch dazu
SIZES = {
    'hitodama': (16, 20, hitodama), 'kodama': (16, 20, kodama), 'kappa': (22, 23, kappa),
    'kasa_obake': (20, 24, kasa_obake), 'bakezori': (19, 17, bakezori), 'tsuchinoko': (25, 14, tsuchinoko),
    'kitsunebi_e': (16, 19, kitsunebi_e), 'chochin': (16, 24, chochin), 'nopperabo': (18, 24, nopperabo),
    'gaki': (18, 22, gaki), 'gaki_small': (12, 13, gaki_small), 'ittan_momen': (29, 15, ittan_momen),
    'bakeneko': (23, 18, bakeneko), 'onibi': (16, 19, onibi), 'karasu_tengu': (24, 22, karasu_tengu),
    'yuki_warashi': (17, 20, yuki_warashi), 'kamaitachi': (23, 16, kamaitachi), 'yamabiko': (19, 20, yamabiko),
    'heikegani': (22, 16, heikegani), 'funayurei': (17, 25, funayurei), 'ningyo': (22, 16, ningyo),
    'isonade': (26, 18, isonade), 'oni': (28, 32, oni), 'shikome': (20, 23, shikome),
    'tsuchigumo': (29, 21, tsuchigumo), 'kumo': (12, 10, kumo), 'shinigami': (22, 29, shinigami),
    'tesso': (13, 11, tesso), 'abura_akago': (16, 19, abura_akago), 'nurikabe': (36, 36, nurikabe),
    'mokumokuren': (22, 22, mokumokuren), 'jinmenju': (25, 28, jinmenju), 'yosuzume': (13, 10, yosuzume),
    'enenra': (23, 23, enenra), 'gyuki': (30, 26, gyuki), 'kamikiri': (16, 20, kamikiri),
    'kerakera_onna': (28, 32, kerakera_onna), 'sazae_oni': (20, 18, sazae_oni), 'hyosube': (17, 21, hyosube),
    'tenome': (20, 24, tenome), 'nekomata': (24, 18, nekomata), 'kasha': (24, 19, kasha),
    'tsurube_otoshi': (26, 27, tsurube_otoshi), 'wanyudo': (27, 28, wanyudo), 'katawaguruma': (27, 28, katawaguruma),
    'azukiarai': (15, 21, azukiarai), 'bake_danuki': (21, 22, bake_danuki), 'nuppeppo': (22, 22, nuppeppo),
    'kappa_small': (15, 16, kappa_small), 'karasu': (16, 11, karasu),
}


def render(name, k):
    w, h, fn = SIZES[name]
    return render_with(w, h, fn, k)


def render_with(w, h, fn, k, pad=2, top=0):
    s = Sprite(w + pad * 2, h + pad * 2 + top, snap=False)
    ox, oy = pad, pad + top

    class Off:
        """Zeichen-Proxy mit Rand-Versatz."""
        def __getattr__(self, a):
            m = getattr(s, a)
            if a == 'px':
                return lambda x, y, c, only=None: s.px(x + ox, y + oy, c, only)
            if a == 'line':
                return lambda x0, y0, x1, y1, c, only=None: s.line(x0 + ox, y0 + oy, x1 + ox, y1 + oy, c, only)
            if a in ('rect', 'ellipse'):
                return lambda x0, y0, x1, y1, c, fill=True, only=None: m(x0 + ox, y0 + oy, x1 + ox, y1 + oy, c, fill=fill, only=only)
            if a == 'circle':
                return lambda cx, cy, r, c, fill=False, only=None: s.circle(cx + ox, cy + oy, r, c, fill=fill, only=only)
            if a == 'polygon':
                return lambda pts, c, fill=True, only=None: s.polygon([(x + ox, y + oy) for x, y in pts], c, fill=fill, only=only)
            if a == 'noise':
                return lambda x0, y0, x1, y1, c, density=0.1, seed=0: s.noise(x0 + ox, y0 + oy, x1 + ox, y1 + oy, c, density=density, seed=seed)
            return m
    fn(Off(), k)
    s.outline(OUT, where='outside')
    return s.composite(1)


def build_all(out_dir):
    from PIL import Image
    meta = {}
    for name in SIZES:
        frames = [render(name, k) for k in range(FRAMES)]
        w, h = frames[0].size
        strip = Image.new('RGBA', (w * FRAMES, h), (0, 0, 0, 0))
        for i, im in enumerate(frames):
            strip.paste(im, (i * w, 0))
        strip.save(os.path.join(out_dir, name + '.png'))
        meta[name] = {'kind': 'strip', 'w': w, 'h': h, 'n': FRAMES}
    return meta


def contact(path, names=None, scale=4):
    from PIL import Image
    names = names or list(SIZES)
    ims = [[render(n, k) for k in range(FRAMES)] for n in names]
    cw = max(sum(i.width for i in fr) + 6 for fr in ims)
    ch = max(fr[0].height for fr in ims) + 4
    cols = 5
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new('RGBA', (cw * cols, ch * rows), (66, 84, 76, 255))
    for i, fr in enumerate(ims):
        x, y = (i % cols) * cw, (i // cols) * ch
        for im in fr:
            sheet.alpha_composite(im, (x, y + ch - 2 - im.height))
            x += im.width + 2
    sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST).save(path)


if __name__ == '__main__':
    contact(sys.argv[1] if len(sys.argv) > 1 else '/tmp/prev/monsters.png', sys.argv[2:] or None)
