"""Spielfiguren – eigene Pixel-Art (24x24, Chibi), gebaut mit pixelstudio (MIT).

Methode (pixel-art-studio-Skill): Silhouette → Farbflächen → Licht oben links
(Rampen mit Farbverschiebung) → Umriss → Details. Jede Figur hat 4 Blickrichtungen
(unten, oben, links, rechts) × 4 Laufbilder (Kontakt, Passieren, Kontakt, Passieren).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'tools'))
from pixelstudio import Sprite as _Sprite, ramp, mix  # noqa: E402


class Sprite(_Sprite):
    """Sprite mit festem Zeichen-Versatz (OX, OY)."""
    def px(self, x, y, c, only=None):
        return super().px(x + OX, y + OY, c, only)

    def line(self, x0, y0, x1, y1, c, only=None):
        return super().line(x0 + OX, y0 + OY, x1 + OX, y1 + OY, c, only)

    def rect(self, x0, y0, x1, y1, c, fill=True, only=None):
        return super().rect(x0 + OX, y0 + OY, x1 + OX, y1 + OY, c, fill, only)

    def circle(self, cx, cy, r, c, fill=False, only=None):
        return super().circle(cx + OX, cy + OY, r, c, fill, only)

    def ellipse(self, x0, y0, x1, y1, c, fill=True, only=None):
        return super().ellipse(x0 + OX, y0 + OY, x1 + OX, y1 + OY, c, fill, only)

    def polygon(self, pts, c, fill=True, only=None):
        return super().polygon([(x + OX, y + OY) for x, y in pts], c, fill, only)

OUT = '#1c1422'          # gemeinsame Umrissfarbe (warmes Dunkelviolett)
EYE = '#2a1e34'
W = H = 32
OX, OY = 4, 6       # Zeichenkoordinaten (24er-Raster) -> Zelle 32x32 mit Rand für Ohren/Waffen
DOWN, UP, LEFT, RIGHT = 0, 1, 2, 3
BOB = [0, -1, 0, -1]     # Kontakt unten, Passieren oben


class Look:
    def __init__(self, hair, skin='#f2c9a8', top='#f2efe6', bottom='#c23a3a', hair_style='long', feet='#3a2a2e',
                 sleeves='wide', extras=None, eye='#2a1e34', no_legs=False, belt=None):
        self.H = ramp(hair, 4, hue_shift=14)
        self.SK = ramp(skin, 3, hue_shift=12, dark=0.22, light=0.5)
        self.T = ramp(top, 3, hue_shift=16, dark=0.3, light=0.5)
        self.B = ramp(bottom, 3, hue_shift=18, dark=0.35, light=0.45)
        self.style = hair_style
        self.feet = feet
        self.sleeves = sleeves
        self.extras = extras or []
        self.eye = eye
        self.no_legs = no_legs
        self.belt = belt


# ------------------------------------------------------------------ Körper
def legs(s, L, d, f, oy):
    if L.no_legs:
        # Geisterschweif
        sway = [0, 1, 0, -1][f]
        s.polygon([(7, 17 + oy), (16, 17 + oy), (14 + sway, 21), (12 + sway, 23), (9 + sway, 21)], L.B[1])
        s.line(14 + sway, 21, 12 + sway, 23, L.B[0])
        return
    if d in (DOWN, UP):
        # Kontakt: ein Fuß vorn (tiefer), Passieren: beide zusammen
        lf, rf = [(0, -1), (0, 0), (-1, 0), (0, 0)][f]
        s.rect(8, 21 + oy + lf, 10, 22 + oy + lf, L.feet)
        s.rect(13, 21 + oy + rf, 15, 22 + oy + rf, L.feet)
    else:
        stride = [2, 0, -2, 0][f]
        s.rect(10 - stride, 21 + oy, 12 - stride, 22 + oy, L.feet)
        s.rect(11 + stride, 21 + oy, 13 + stride, 22 + oy, mix(L.feet, '#000000', 0.25))


def lower_body(s, L, d, f, oy):
    B = L.B
    if d in (DOWN, UP):
        s.polygon([(7, 16 + oy), (16, 16 + oy), (17, 21 + oy), (6, 21 + oy)], B[1])
        s.polygon([(13, 16 + oy), (16, 16 + oy), (17, 21 + oy), (14, 21 + oy)], B[0])     # Schatten rechts
        s.line(7, 17 + oy, 7, 20 + oy, B[2])                                              # Licht links
        s.line(11, 17 + oy, 11, 21 + oy, B[0])                                            # Falte
    else:
        sw = [1, 0, -1, 0][f]
        s.polygon([(8, 16 + oy), (15, 16 + oy), (16 + sw, 21 + oy), (7 - sw, 21 + oy)], B[1])
        s.polygon([(12, 16 + oy), (15, 16 + oy), (16 + sw, 21 + oy), (12, 21 + oy)], B[0])
        s.line(8, 17 + oy, 8, 20 + oy, B[2])


def upper_body(s, L, d, f, oy):
    T, SK = L.T, L.SK
    swing = [1, 0, -1, 0][f]
    if d in (DOWN, UP):
        s.rect(8, 12 + oy, 15, 16 + oy, T[1])
        s.rect(14, 12 + oy, 15, 16 + oy, T[0])
        s.line(8, 12 + oy, 8, 16 + oy, T[2])
        if L.sleeves == 'wide':
            s.rect(5, 12 + oy, 7, 16 + oy + swing, T[1]); s.line(5, 12 + oy, 5, 16 + oy + swing, T[2])
            s.rect(16, 12 + oy, 18, 16 - swing + oy, T[0])
            s.px(6, 17 + oy + swing, SK[1]); s.px(17, 17 + oy - swing, SK[0])
        else:
            s.rect(6, 12 + oy, 7, 15 + oy + swing, T[1])
            s.rect(16, 12 + oy, 17, 15 + oy - swing, T[0])
            s.px(6, 16 + oy + swing, SK[1]); s.px(17, 16 + oy - swing, SK[0])
        if L.belt:
            s.line(8, 16 + oy, 15, 16 + oy, L.belt)
    else:
        s.rect(9, 12 + oy, 14, 16 + oy, T[1])
        s.line(14, 12 + oy, 14, 16 + oy, T[0])
        s.line(9, 12 + oy, 9, 16 + oy, T[2])
        # Arm vorn, schwingt
        if L.sleeves == 'wide':
            s.rect(10 + swing, 12 + oy, 13 + swing, 16 + oy, T[2] if swing <= 0 else T[1])
            s.px(10 + swing, 17 + oy, SK[1])
        else:
            s.rect(11 + swing, 12 + oy, 12 + swing, 15 + oy, T[2])
            s.px(11 + swing, 16 + oy, SK[1])
        if L.belt:
            s.line(9, 16 + oy, 14, 16 + oy, L.belt)


# ------------------------------------------------------------------ Kopf
def back_hair(s, L, d, f, oy):
    """Lange Haare hinter dem Körper (unten/seitlich) bzw. über dem Rücken (oben)."""
    Hh = L.H
    if L.style not in ('long', 'ghost', 'ponytail'):
        return
    if d == DOWN:
        s.rect(6, 6 + oy, 17, 15 + oy, Hh[0])
    elif d == LEFT:
        s.polygon([(12, 5 + oy), (18, 5 + oy), (18, 16 + oy), (13, 16 + oy)], Hh[0])
        s.line(17, 6 + oy, 17, 15 + oy, mix(Hh[0], '#000000', 0.3))
    else:  # UP: Haarvorhang über dem Rücken
        s.polygon([(6, 7 + oy), (17, 7 + oy), (17, 16 + oy), (12, 17 + oy), (6, 16 + oy)], Hh[1])
        s.rect(15, 8 + oy, 17, 16 + oy, Hh[0])
        s.line(9, 9 + oy, 9, 15 + oy, Hh[2])
        s.line(12, 9 + oy, 12, 16 + oy, Hh[0])


def head(s, L, d, f, oy):
    Hh, SK = L.H, L.SK
    st = L.style
    hy = oy
    if d == UP:
        if st == 'bald':
            s.ellipse(6, 1 + hy, 17, 12 + hy, SK[1]); s.ellipse(12, 3 + hy, 17, 12 + hy, SK[0], only=SK[1])
            return
        s.ellipse(5, 0 + hy, 18, 12 + hy, Hh[1])
        s.ellipse(13, 3 + hy, 18, 12 + hy, Hh[0], only=Hh[1])
        s.line(7, 3 + hy, 9, 1 + hy, Hh[2]); s.line(7, 4 + hy, 8, 3 + hy, Hh[2])
        s.line(11, 5 + hy, 11, 11 + hy, Hh[0])
        return
    if d == DOWN:
        if st != 'bald':
            s.ellipse(5, 0 + hy, 18, 12 + hy, Hh[1])                  # Haarkappe
            s.ellipse(14, 3 + hy, 18, 12 + hy, Hh[0], only=Hh[1])
        s.ellipse(7, 4 + hy, 16, 12 + hy, SK[1])                     # Gesicht
        s.ellipse(14, 6 + hy, 16, 12 + hy, SK[0], only=SK[1])
        if st != 'bald':
            s.rect(7, 3 + hy, 16, 5 + hy, Hh[1])                      # Pony
            for x in (7, 9, 12, 15):
                s.px(x, 6 + hy, Hh[1])
            s.px(16, 6 + hy, Hh[0])
            s.line(8, 1 + hy, 11, 1 + hy, Hh[2]); s.px(7, 2 + hy, Hh[2]); s.px(9, 3 + hy, Hh[2])
            if st in ('long', 'ghost', 'ponytail'):
                s.rect(5, 6 + hy, 6, 13 + hy, Hh[1]); s.rect(17, 6 + hy, 18, 13 + hy, Hh[0])
        else:
            s.ellipse(6, 1 + hy, 17, 12 + hy, SK[1]); s.ellipse(14, 3 + hy, 17, 12 + hy, SK[0], only=SK[1])
            s.px(8, 3 + hy, SK[2]); s.px(9, 2 + hy, SK[2])
        for ex in (8, 14):
            s.rect(ex, 8 + hy, ex + 1, 9 + hy, L.eye)
            s.px(ex, 8 + hy, '#f6f2ff')
        s.px(8, 10 + hy, mix(SK[1], '#e06070', 0.45)); s.px(15, 10 + hy, mix(SK[0], '#e06070', 0.45))
        s.px(11, 11 + hy, '#a4434a'); s.px(12, 11 + hy, '#a4434a')
    else:   # Seite, Blick nach links (rechts = gespiegelt)
        if st != 'bald':
            s.ellipse(6, 0 + hy, 18, 12 + hy, Hh[1])
            s.ellipse(14, 3 + hy, 18, 12 + hy, Hh[0], only=Hh[1])
        s.ellipse(4, 4 + hy, 12, 12 + hy, SK[1])                      # Gesicht vorn
        s.px(3, 9 + hy, SK[1])                                         # Nase
        s.px(11, 9 + hy, SK[0]); s.px(11, 10 + hy, SK[0])              # Ohrschatten
        if st != 'bald':
            s.rect(5, 2 + hy, 13, 4 + hy, Hh[1])                       # Pony
            s.px(5, 5 + hy, Hh[1]); s.px(7, 5 + hy, Hh[1]); s.px(4, 4 + hy, Hh[1])
            s.rect(11, 5 + hy, 13, 9 + hy, Hh[1])                      # Schläfe/Ohr bedeckt
            s.line(8, 1 + hy, 12, 1 + hy, Hh[2]); s.px(7, 2 + hy, Hh[2])
        else:
            s.ellipse(5, 1 + hy, 16, 12 + hy, SK[1], only=None) if False else None
        s.rect(6, 7 + hy, 7, 8 + hy, L.eye); s.px(6, 7 + hy, '#f6f2ff')
        s.px(7, 10 + hy, mix(SK[1], '#e06070', 0.45))
        s.px(4, 11 + hy, '#a4434a')


def build_figure(L, extra_fn=None):
    """Erzeugt ein 4x4-Sheet (Spalten = Richtung, Zeilen = Laufbild) als PIL-Image."""
    from PIL import Image
    sheet = Image.new('RGBA', (W * 4, H * 4), (0, 0, 0, 0))
    for d in (DOWN, UP, LEFT):
        for f in range(4):
            s = Sprite(W, H, snap=False)
            oy = BOB[f]
            if d != UP:
                back_hair(s, L, d, f, oy)
            legs(s, L, d, f, oy)
            lower_body(s, L, d, f, oy)
            upper_body(s, L, d, f, oy)
            if d == UP:
                back_hair(s, L, d, f, oy)
            head(s, L, d, f, oy)
            if extra_fn:
                extra_fn(s, L, d, f, oy)
            s.outline(OUT, where='outside')
            im = s.composite(1)
            sheet.paste(im, (d * W, f * H))
            if d == LEFT:
                sheet.paste(im.transpose(Image.FLIP_LEFT_RIGHT), (RIGHT * W, f * H))
    return sheet


# ------------------------------------------------------------------ Figuren
def hana_extra(s, L, d, f, oy):
    # rote Haarschleife (Mizuhiki) und roter Kragen
    if d == DOWN:
        s.polygon([(15, 0 + oy), (19, -1 + oy), (19, 3 + oy), (16, 2 + oy)], '#d4343c')
        s.px(16, 1 + oy, '#f06a5c')
        s.px(10, 12 + oy, '#c23a3a'); s.px(13, 12 + oy, '#c23a3a'); s.px(11, 13 + oy, '#c23a3a'); s.px(12, 13 + oy, '#c23a3a')
    elif d == LEFT:
        s.polygon([(15, 3 + oy), (19, 2 + oy), (19, 6 + oy), (16, 5 + oy)], '#d4343c')
        s.px(10, 12 + oy, '#c23a3a'); s.px(10, 13 + oy, '#c23a3a')
    else:
        s.polygon([(4, 0 + oy), (8, -1 + oy), (8, 3 + oy), (5, 2 + oy)], '#d4343c')


def kenji_extra(s, L, d, f, oy):
    # Samurai: Haarknoten (Chonmage), Katana an der Hüfte, Stirnband
    if d == DOWN:
        s.rect(10, -1 + oy, 13, 1 + oy, L.H[1]); s.px(11, -1 + oy, L.H[2])
        s.line(7, 5 + oy, 16, 5 + oy, '#e8e2d0')
        s.line(17, 13 + oy, 20, 19 + oy, '#3a3046'); s.px(17, 13 + oy, '#c8a24a')
    elif d == UP:
        s.rect(10, -1 + oy, 13, 1 + oy, L.H[1]); s.line(10, 2 + oy, 13, 2 + oy, '#e8e2d0')
        s.line(6, 13 + oy, 3, 19 + oy, '#3a3046')
    else:
        s.rect(12, -1 + oy, 15, 1 + oy, L.H[1]); s.px(13, -1 + oy, L.H[2])
        s.line(5, 4 + oy, 13, 4 + oy, '#e8e2d0'); s.px(18, 5 + oy, '#e8e2d0'); s.px(19, 6 + oy, '#e8e2d0')
        s.line(15, 15 + oy, 21, 13 + oy, '#3a3046'); s.line(8, 16 + oy, 14, 15 + oy, '#c8ccd8'); s.px(15, 15 + oy, '#c8a24a')


def fox_extra(s, L, d, f, oy):
    # Kitsune: spitze Ohren, buschiger Schweif mit weißer Spitze
    E, EI = L.H[1], '#f2b0a0'
    sw = [0, 1, 0, -1][f]
    if d in (DOWN, UP):
        for ex, m in ((6, 1), (15, -1)):
            s.polygon([(ex, 2 + oy), (ex + 2 * m, -3 + oy), (ex + 3 * m, 2 + oy)], E)
            if d == DOWN:
                s.px(ex + 2 * m, 0 + oy, EI); s.px(ex + 2 * m, 1 + oy, EI)
        if d == UP:
            s.ellipse(15 + sw, 13 + oy, 22 + sw, 19 + oy, L.H[1]); s.ellipse(19 + sw, 12 + oy, 22 + sw, 15 + oy, '#fbf3e6')
        else:
            s.ellipse(16 + sw, 14 + oy, 21 + sw, 19 + oy, L.H[0])
    else:
        s.polygon([(13, 2 + oy), (15, -3 + oy), (17, 2 + oy)], E); s.px(15, 0 + oy, EI)
        s.polygon([(9, 2 + oy), (10, -2 + oy), (12, 2 + oy)], L.H[0])
        s.ellipse(15, 12 + oy + sw, 22, 17 + oy + sw, L.H[1]); s.ellipse(15, 15 + oy + sw, 22, 17 + oy + sw, L.H[0], only=L.H[1])
        s.ellipse(19, 11 + oy + sw, 23, 15 + oy + sw, '#fbf3e6')


def tanuki_extra(s, L, d, f, oy):
    # Tanuki: runde Ohren, Augenmaske, dicker Ringelschwanz, Blatt auf dem Kopf
    sw = [0, 1, 0, -1][f]
    if d in (DOWN, UP):
        s.circle(7, 2 + oy, 2, L.H[1], fill=True); s.circle(16, 2 + oy, 2, L.H[1], fill=True)
        s.polygon([(10, -1 + oy), (13, -3 + oy), (14, 0 + oy), (11, 1 + oy)], '#5fae4a'); s.px(12, -1 + oy, '#9ad86a')
        if d == DOWN:
            s.rect(7, 8 + oy, 9, 10 + oy, '#4a3428'); s.rect(13, 8 + oy, 15, 10 + oy, '#4a3428')
            s.px(8, 8 + oy, '#f6f2ff'); s.px(14, 8 + oy, '#f6f2ff')
            s.ellipse(9, 13 + oy, 14, 17 + oy, '#f0dcc0')
        else:
            s.ellipse(9 + sw, 15 + oy, 15 + sw, 21 + oy, L.H[1])
            s.line(10 + sw, 17 + oy, 14 + sw, 17 + oy, L.H[0]); s.line(10 + sw, 19 + oy, 14 + sw, 19 + oy, L.H[0])
    else:
        s.circle(14, 2 + oy, 2, L.H[1], fill=True)
        s.polygon([(9, -1 + oy), (12, -3 + oy), (13, 0 + oy), (10, 1 + oy)], '#5fae4a')
        s.rect(5, 7 + oy, 8, 9 + oy, '#4a3428'); s.px(6, 7 + oy, '#f6f2ff')
        s.ellipse(15, 14 + oy + sw, 21, 19 + oy + sw, L.H[1])
        s.line(17, 14 + oy + sw, 17, 19 + oy + sw, L.H[0]); s.line(19, 14 + oy + sw, 19, 19 + oy + sw, L.H[0])


def benkei_extra(s, L, d, f, oy):
    # Sōhei: weiße Kapuze (Katō), Naginata, Gebetskette
    C = ramp('#e9e4d8', 3, hue_shift=10, dark=0.25, light=0.4)
    if d == DOWN:
        s.ellipse(5, -1 + oy, 18, 8 + oy, C[1], only='empty')
        s.ellipse(5, -1 + oy, 18, 6 + oy, C[1])
        s.rect(5, 3 + oy, 7, 14 + oy, C[1]); s.rect(16, 3 + oy, 18, 14 + oy, C[0])
        s.line(7, 0 + oy, 11, -1 + oy, C[2]); s.line(6, 1 + oy, 6, 3 + oy, C[2])
        s.line(8, 6 + oy, 15, 6 + oy, C[0])
        s.line(20, -2 + oy, 20, 21 + oy, '#6a4a32'); s.polygon([(19, -2 + oy), (20, -6 + oy), (22, -3 + oy), (21, -1 + oy)], '#d6dbe6')
        for i, x in enumerate(range(8, 16)):
            s.px(x, 13 + oy + (1 if 9 < x < 14 else 0), '#7a3b2e' if i % 2 else '#a45a3c')
    elif d == UP:
        s.ellipse(5, 0 + oy, 18, 12 + oy, C[1]); s.polygon([(6, 8 + oy), (17, 8 + oy), (16, 15 + oy), (7, 15 + oy)], C[1])
        s.rect(15, 2 + oy, 18, 14 + oy, C[0]); s.line(7, 2 + oy, 10, 1 + oy, C[2])
        s.line(3, -2 + oy, 3, 21 + oy, '#6a4a32'); s.polygon([(2, -2 + oy), (3, -6 + oy), (5, -3 + oy), (4, -1 + oy)], '#d6dbe6')
    else:
        s.ellipse(6, -1 + oy, 18, 6 + oy, C[1])
        s.polygon([(12, 3 + oy), (18, 3 + oy), (18, 15 + oy), (13, 15 + oy)], C[1])
        s.rect(16, 3 + oy, 18, 15 + oy, C[0]); s.line(8, 0 + oy, 12, -1 + oy, C[2])
        s.line(5, 6 + oy, 11, 6 + oy, C[0])
        s.line(2, 10 + oy, 14, 20 + oy, '#6a4a32'); s.polygon([(2, 10 + oy), (-1, 5 + oy), (0, 4 + oy), (4, 9 + oy)], '#d6dbe6')


def okiku_extra(s, L, d, f, oy):
    # Geist: weißes Dreieckstuch (Hitaikakushi) auf der Stirn, Teller
    if d == DOWN:
        s.polygon([(9, 3 + oy), (14, 3 + oy), (11, 6 + oy)], '#f4f4fa'); s.px(11, 4 + oy, '#c8c8d8')
        s.ellipse(15, 14 + oy, 20, 17 + oy, '#e8eef6'); s.ellipse(16, 15 + oy, 19, 16 + oy, '#5a8ac8')
    elif d == LEFT:
        s.polygon([(4, 3 + oy), (8, 3 + oy), (5, 6 + oy)], '#f4f4fa')
        s.ellipse(2, 14 + oy, 7, 17 + oy, '#e8eef6'); s.ellipse(3, 15 + oy, 6, 16 + oy, '#5a8ac8')


def kotaro_extra(s, L, d, f, oy):
    # Karasu-Tengu: Schnabel, Tokin-Kappe, schwarze Flügel (flattern)
    fl = [0, -2, 0, -1][f]
    Wg = ramp('#2c2a40', 3, hue_shift=18, dark=0.3, light=0.5)
    if d in (DOWN, UP):
        for side in (-1, 1):
            x0 = 5 if side < 0 else 18
            pts = [(x0, 11 + oy), (x0 + 6 * side, 6 + oy + fl), (x0 + 5 * side, 14 + oy), (x0 + 2 * side, 16 + oy)]
            s.polygon(pts, Wg[1] if side < 0 else Wg[0])
            s.line(x0 + side, 12 + oy, x0 + 5 * side, 8 + oy + fl, Wg[2])
        if d == DOWN:
            s.polygon([(10, 9 + oy), (13, 9 + oy), (12, 13 + oy), (11, 13 + oy)], '#e8a838'); s.px(11, 9 + oy, '#ffd36a')
        s.rect(10, -1 + oy, 13, 1 + oy, '#1c1a24')
    else:
        s.polygon([(13, 10 + oy), (21, 6 + oy + fl), (20, 15 + oy), (15, 17 + oy)], Wg[1])
        s.line(14, 11 + oy, 20, 7 + oy + fl, Wg[2])
        s.polygon([(4, 8 + oy), (0, 10 + oy), (4, 11 + oy)], '#e8a838'); s.px(3, 9 + oy, '#ffd36a')
        s.rect(9, -1 + oy, 12, 1 + oy, '#1c1a24')


def seimei_extra(s, L, d, f, oy):
    # Onmyōji: hohe schwarze Eboshi-Mütze, Ofuda-Talisman, Fünfstern auf der Brust
    if d in (DOWN, UP, LEFT):
        x = 8 if d != LEFT else 9
        s.polygon([(x, 2 + oy), (x + 7, 2 + oy), (x + 6, -5 + oy), (x + 2, -6 + oy)], '#22202c')
        s.line(x + 2, -5 + oy, x + 2, 1 + oy, '#3c3a4c')
    if d == DOWN:
        s.px(11, 14 + oy, '#d84848'); s.px(12, 14 + oy, '#d84848'); s.px(11, 13 + oy, '#d84848'); s.px(12, 15 + oy, '#d84848')
        s.rect(18, 15 + oy, 20, 20 + oy, '#f2e6c4'); s.line(19, 16 + oy, 19, 19 + oy, '#c43a3a')
    elif d == LEFT:
        s.rect(4, 14 + oy, 6, 19 + oy, '#f2e6c4'); s.line(5, 15 + oy, 5, 18 + oy, '#c43a3a')


def akago_extra(s, L, d, f, oy):
    # Akago: rotes Baby mit kleinem Horn und Lätzchen
    if d == DOWN:
        s.polygon([(11, 1 + oy), (12, -2 + oy), (13, 1 + oy)], '#f2e6c4')
        s.ellipse(8, 12 + oy, 15, 16 + oy, '#f2efe6'); s.line(9, 12 + oy, 14, 12 + oy, '#c43a3a')
    elif d == LEFT:
        s.polygon([(8, 1 + oy), (9, -2 + oy), (10, 1 + oy)], '#f2e6c4')
        s.ellipse(7, 12 + oy, 11, 16 + oy, '#f2efe6')
    else:
        s.polygon([(11, 1 + oy), (12, -2 + oy), (13, 1 + oy)], '#f2e6c4')


def susanoo_extra(s, L, d, f, oy):
    # Sturmgott: Kopfband, wilder Haarschopf, Kusanagi-Schwert, Magatama-Kette, Blitzfunken
    if d == DOWN:
        s.polygon([(6, 1 + oy), (8, -3 + oy), (10, 0 + oy), (12, -4 + oy), (14, 0 + oy), (16, -3 + oy), (17, 1 + oy)], L.H[1])
        s.line(6, 4 + oy, 17, 4 + oy, '#d6b04a')
        for x, c in ((9, '#3fbf8a'), (11, '#e04848'), (13, '#3fbf8a')):
            s.px(x, 13 + oy, c)
        s.line(19, 3 + oy, 19, 16 + oy, '#dfe6f2'); s.line(20, 4 + oy, 20, 15 + oy, '#9aa6c0'); s.rect(18, 16 + oy, 21, 16 + oy, '#d6b04a')
        if f in (1, 3):
            s.px(21, 2 + oy, '#9fe8ff'); s.px(22, 1 + oy, '#ffffff')
    elif d == UP:
        s.polygon([(6, 1 + oy), (8, -3 + oy), (10, 0 + oy), (12, -4 + oy), (14, 0 + oy), (16, -3 + oy), (17, 1 + oy)], L.H[1])
        s.line(4, 3 + oy, 4, 16 + oy, '#dfe6f2')
    else:
        s.polygon([(8, 1 + oy), (11, -4 + oy), (13, 0 + oy), (16, -3 + oy), (18, 2 + oy)], L.H[1])
        s.line(5, 4 + oy, 13, 4 + oy, '#d6b04a')
        s.line(2, 8 + oy, 10, 16 + oy, '#dfe6f2'); s.line(3, 8 + oy, 10, 15 + oy, '#9aa6c0'); s.px(11, 17 + oy, '#d6b04a')
        if f in (1, 3):
            s.px(1, 7 + oy, '#9fe8ff')


FIGURES = {
    'hana': (Look('#2b2236', top='#f2efe6', bottom='#c8323c', hair_style='long'), hana_extra),
    'kenji': (Look('#1e1c26', top='#3c5a9a', bottom='#2c3046', hair_style='short', sleeves='wide', belt='#c8a24a'), kenji_extra),
    'kuzunoha': (Look('#e8902e', top='#f4ece0', bottom='#7a4ab0', hair_style='long', eye='#7a2a1a'), fox_extra),
    'ponpoko': (Look('#8a5a34', skin='#c99666', top='#7a5a3e', bottom='#5a4030', hair_style='short', belt='#e0c050'), tanuki_extra),
    'benkei': (Look('#2a2228', skin='#d9a27e', top='#3a3448', bottom='#2a2636', hair_style='bald', feet='#5a4632'), benkei_extra),
    'okiku': (Look('#16141e', skin='#dce6f0', top='#eef2fa', bottom='#d8e2f0', hair_style='ghost', no_legs=True, eye='#3a4a7a'), okiku_extra),
    'kotaro': (Look('#1e1c2a', skin='#e2b48c', top='#3a5a4a', bottom='#2a3a34', hair_style='short', feet='#2a2228'), kotaro_extra),
    'seimei': (Look('#1a1a24', top='#f6f4fa', bottom='#5a4aa0', hair_style='short', sleeves='wide'), seimei_extra),
    'akago': (Look('#3a1a1a', skin='#e06a5a', top='#e06a5a', bottom='#d05a4c', hair_style='bald', feet='#b04a40', sleeves='narrow'), akago_extra),
    'susanoo': (Look('#2a2a3a', skin='#e8c09a', top='#e8eef6', bottom='#3a4a7a', hair_style='long', belt='#d6b04a'), susanoo_extra),
}


def build_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for name, (L, fn) in FIGURES.items():
        build_figure(L, fn).save(os.path.join(out_dir, name + '.png'))
    return list(FIGURES)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'yokai', 'assets', 'sprites')
    print(build_all(out))
