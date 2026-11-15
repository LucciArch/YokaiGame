"""Handgezeichnete Hi-Res-Requisiten (64x64, direkt in Hi-Res-Pixeln): Steinlaterne (Tōrō) und Siegel-Urne.
Licht von oben links, Umriss K, Schatten nach unten rechts – wie die Figuren."""
import os
import numpy as np
from core import *

STONE = ('#151521', '#2a2a3c', '#45465c', '#6c6e88', '#a3a6be')
MOSS = ('#14301e', '#285a2c', '#4c8a38')
GLOW = ('#8a4a12', '#d8961a', '#ffe24a', '#fffbc0')
DARKWIN = ('#0b0912', '#141020')
CLAY = ('#25121a', '#4e2422', '#7c3e2a', '#ad6838', '#d89a5c')
GLAZE = ('#121a2c', '#1d2e4a', '#30507a', '#5f88b4', '#a6c8e4')
ROPE = ('#3a2a1e', '#7a5c34', '#b8955a', '#e2c88c')
PAPER = ('#8a8070', '#d8d0b8', '#f6f0dc')
RED = ('#5a1020', '#a81f2a', '#e0503a')
SHADOW = '#0d0b14'


def ground_shadow(cv, cx, by, rx, ry=4):
    m = cv.E(cx + 3, by, rx, ry) & ~cv.m
    cv.fill(m, SHADOW)


def finish(cv, cx, by, rx):
    cv.outline(K)
    ground_shadow(cv, cx, by, rx)
    return cv


def toro(lit=True):
    cv = Cv(64, 64, ss=1)
    cx = 31.5
    S = STONE
    # Sockel (kiso) – zweistufig
    cv.form(cv.R(18, 56, 45, 60), (S[0], S[1], S[2]), 2, 1)
    cv.form(cv.R(21, 52, 42, 55), (S[1], S[2], S[3]), 2, 1)
    # Schaft (sao) – leicht gerundet, mit Ringen
    sao = cv.R(27, 37, 36, 51)
    cv.form(sao, (S[0], S[1], S[2]), 3, 1)
    for y in (40, 48):
        cv.hl(27, 36, y, S[0]); cv.hl(27, 35, y + 1, S[3])
    # Plattform (chūdai)
    cv.form(cv.PG([(19, 36), (44, 36), (40, 31), (23, 31)]), (S[1], S[2], S[3]), 2, 1)
    cv.hl(23, 40, 31, S[4])
    # Feuerkammer (hibukuro), sechseckig angedeutet
    box = cv.R(22, 19, 41, 30)
    cv.form(box, (S[0], S[1], S[2]), 3, 1)
    cv.vl(26, 19, 30, S[0]); cv.vl(37, 19, 30, S[0])
    win = cv.R(28, 21, 35, 28)
    if lit:
        cv.fill(win, GLOW[1])
        cv.fill(cv.R(29, 22, 34, 27), GLOW[2])
        cv.fill(cv.E(31.5, 24.5, 1.6, 2.2), GLOW[3])
        cv.hl(28, 35, 28, GLOW[0])
    else:
        cv.fill(win, DARKWIN[0]); cv.fill(cv.R(29, 22, 34, 24), DARKWIN[1])
    cv.vl(31, 21, 28, S[0])                       # Gitterstab
    # seitliche Fensterchen
    cv.fill(cv.R(23, 22, 25, 27), GLOW[0] if lit else DARKWIN[0])
    cv.fill(cv.R(38, 22, 40, 27), GLOW[0] if lit else DARKWIN[0])
    # Dach (kasa) mit hochgezogenen Ecken (warabite)
    roof = cv.PG([(13, 18), (17, 16), (25, 10), (38, 10), (46, 16), (50, 18), (48, 20), (15, 20)])
    cv.form(roof, (S[1], S[2], S[3]), 3, 1)
    cv.fill(cv.R(15, 19, 48, 20), S[0])
    cv.form(cv.PG([(12, 15), (15, 17), (13, 19), (11, 17)]), (S[1], S[3], S[4]), 1, 1)   # Ecke links
    cv.form(cv.PG([(51, 15), (52, 17), (50, 19), (48, 17)]), (S[0], S[2], S[3]), 1, 1)   # Ecke rechts
    cv.line([(18, 16), (26, 11)], S[4])                                                  # Mondlicht-Kante
    cv.line([(31, 11), (31, 18)], S[1])
    # Knauf (hōju) – Lotusknospe
    cv.form(cv.R(29, 7, 34, 9), (S[0], S[2], S[3]), 1, 1)
    cv.form(cv.E(31.5, 4.5, 3.2, 3.6) | cv.PG([(31.5, -1), (34, 3), (29, 3)]), (S[1], S[3], S[4]), 2, 1)
    # Moos
    for (x, y, r) in ((20, 19, 2.5), (44, 19, 1.8), (24, 31, 1.8), (19, 55, 2.2), (42, 52, 1.5)):
        m = cv.E(x, y, r * 1.4, r * .8) & cv.m
        cv.fill(m, MOSS[1]); cv.fill(m & ~sh(m, 1, 1), MOSS[2])
    finish(cv, cx, 60, 15)
    if lit:   # warmer Schein auf dem Dachrand unten
        cv.hl(24, 39, 20, GLOW[0])
    return cv


def tsubo(broken=False):
    cv = Cv(64, 64, ss=1)
    cx = 31.5
    if not broken:
        body = cv.E(cx, 41, 16, 15) | cv.E(cx, 33, 13, 10)
        cv.form(body, (GLAZE[0], GLAZE[1], GLAZE[2]), 5, 2)
        # Glanzlicht der Glasur
        cv.fill(cv.E(23, 34, 2.4, 4.2) & body, GLAZE[3])
        cv.fill(cv.E(22.5, 32.5, 1, 1.6) & body, GLAZE[4])
        # tropfende Glasurkante: unten Ton sichtbar
        foot = body & (cv.Y > 49 + np.sin(cv.X * .55) * 1.6)
        cv.form(foot, (CLAY[1], CLAY[2], CLAY[3]), 2, 0)
        # Hals und Rand
        cv.form(cv.R(24, 19, 39, 24), (GLAZE[0], GLAZE[1], GLAZE[2]), 2, 1)
        cv.form(cv.E(cx, 19, 9, 3), (GLAZE[1], GLAZE[2], GLAZE[3]), 1, 1)
        cv.fill(cv.E(cx, 19, 6, 1.6), '#06050a')
        # Deckel aus Papier mit Kordel
        cv.form(cv.E(cx, 17.5, 9.5, 3.5) & (cv.Y < 19), (PAPER[0], PAPER[1], PAPER[2]), 1, 1)
        rope = cv.R(23, 22, 40, 23)
        cv.fill(rope, ROPE[1]); cv.fill(rope & (cv.X % 3 == 0), ROPE[3]); cv.hl(23, 40, 23, ROPE[0])
        # Siegel-Ofuda
        tag = cv.R(28, 30, 35, 44)
        cv.form(tag, (PAPER[0], PAPER[1], PAPER[2]), 1, 1)
        cv.fill(cv.E(31.5, 33, 2.3, 2.3), RED[1]); cv.px(31, 32, RED[2])
        for y in (37, 39, 41):
            cv.hl(30, 33, y, '#3a2a2a')
        cv.hl(30, 31, 43, RED[1])
        # Kordelenden
        cv.line([(24, 23), (21, 29)], ROPE[1]); cv.px(21, 30, ROPE[2])
        finish(cv, cx, 56, 16)
    else:
        for (x, y, w, h, r) in ((14, 50, 11, 6, 0), (34, 52, 12, 5, 1), (26, 46, 9, 5, 1), (41, 46, 7, 5, 0)):
            pts = [(x, y + h), (x + w * .2, y), (x + w, y + h * .3), (x + w * .8, y + h)]
            m = cv.PG(pts)
            cv.form(m, (GLAZE[0], GLAZE[1], GLAZE[2]) if r else (CLAY[1], CLAY[2], CLAY[3]), 2, 1)
        cv.fill(cv.E(cx, 54, 8, 2.2) & ~cv.m, '#07060c')
        cv.form(cv.R(30, 50, 35, 54), (PAPER[0], PAPER[1], PAPER[2]), 1, 1)
        cv.px(32, 51, RED[1])
        finish(cv, cx, 56, 15)
    return cv


def build(dst):
    strip([tsubo(False), tsubo(True)], os.path.join(dst, 'pot_hi.png'))
    strip([toro(True), toro(False)], os.path.join(dst, 'lantern_hi.png'))
