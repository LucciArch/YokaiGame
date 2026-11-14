"""Version 2: ernste, folkloretreue Yōkai mit volumetrischer Schattierung (sculpt).

Jede Kreatur: fn(pose) -> PIL-Bild. pose = ('walk', i) mit i in 0..3 oder
('atk', i) mit i in 0..2 (Ausholen, Zuschlagen, Zurückziehen). Blick nach links.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sculpt import Canvas, ramp, mix  # noqa: E402

INK = '#140d18'
BONEW = '#e8e0c8'


def M(**kw):
    return kw


# Gemeinsame Materialien (gedeckte, ernste Farbwelt)
SKIN_K = ramp('#56785a', 6, hue_shift=22)
BELLY_K = ramp('#9a9a6a', 5, hue_shift=16)
SHELL = ramp('#5a4632', 6, hue_shift=16)
SHELLRIM = ramp('#8a7048', 5)
BEAK = ramp('#5e5a30', 5, hue_shift=18)
HAIR_D = ramp('#262a2e', 4, hue_shift=12, dark=0.5, light=0.35)
WATER = ramp('#4a8ea8', 5, hue_shift=14)
ONI_R = ramp('#a8382c', 6, hue_shift=20)
TIGER = ramp('#c8902a', 5, hue_shift=16)
IRON = ramp('#55505e', 6, hue_shift=14, light=0.5)
HAIR_W = ramp('#3a2a2a', 4, hue_shift=10, dark=0.5)
HORN = ramp('#d8c8a0', 5, hue_shift=12)
GAKI_S = ramp('#8a8a72', 6, hue_shift=18)
CLOTH_R = ramp('#5a4a46', 5, hue_shift=14)
WEASEL = ramp('#a07a52', 6, hue_shift=18)
BLADE = ramp('#9aa2b4', 5, hue_shift=10, light=0.75)
WIND = '#c8d8e8'


def pose_vals(pose):
    kind, i = pose
    walk = [0, 1, 0, -1][i % 4] if kind == 'walk' else 0
    bob = [0, -1, 0, -1][i % 4] if kind == 'walk' else 0
    atk = i if kind == 'atk' else -1
    return walk, bob, atk


# ------------------------------------------------------------------ Kappa
def kappa(pose):
    w, bob, atk = pose_vals(pose)
    c = Canvas(48, 46, M(skin=SKIN_K, belly=BELLY_K, shell=SHELL, rim=SHELLRIM, beak=BEAK, hair=HAIR_D, water=WATER), ox=6, oy=5)
    lean = {-1: 0, 0: -2, 1: 3, 2: 1}[atk]           # Ausholen: zurücklehnen, Zuschlagen: vorschnellen
    y0 = bob
    # hinterer Arm, hinteres Bein
    c.limb([(26 + lean, 17 + y0), (31 + lean, 25 + y0), (30 + lean, 31 + y0)], 4, 3, 'skin')
    c.limb([(27, 28 + y0), (30 - w, 34), (31 - w, 38)], 6, 4, 'skin')
    c.poly([(28 - w, 37), (35 - w, 37), (35 - w, 39), (27 - w, 39)], 'skin', bulge=0.3)
    # Panzer
    c.ellipse(17 + lean, 9 + y0, 39 + lean, 33 + y0, 'shell', bulge=1.4)
    c.limb([(19 + lean, 10 + y0), (32 + lean, 10 + y0), (39 + lean, 20 + y0), (35 + lean, 32 + y0)], 3, 2, 'rim', bulge=0.4)
    for (a, b, d, e) in ((24, 13, 34, 16), (23, 20, 36, 22), (25, 27, 35, 29)):
        c.line(a + lean, b + y0, d + lean, e + y0, '#2e2218')
    # gebückter Körper
    c.ellipse(11 + lean, 13 + y0, 30 + lean, 33 + y0, 'skin')
    c.ellipse(13 + lean, 19 + y0, 23 + lean, 32 + y0, 'belly', bulge=0.6)
    for yy in (22, 25, 28):
        c.line(14 + lean, yy + y0, 21 + lean, yy + y0, mix(BELLY_K[1], BELLY_K[0], 0.5))
    # vorderes Bein
    c.limb([(18, 29 + y0), (15 + w, 35), (13 + w, 38)], 7, 5, 'skin')
    c.poly([(8 + w, 37), (16 + w, 37), (17 + w, 39), (7 + w, 39)], 'skin', bulge=0.3)
    c.line(8 + w, 39, 7 + w, 40, INK); c.line(11 + w, 39, 11 + w, 40, INK)
    # Kopf – weit vorgeschoben, Haar als Topfschnitt bis zum Kiefer
    hx = 4 + lean * 2
    hy = 4 + y0 + (1 if atk == 0 else 0)
    c.ellipse(hx, hy, hx + 17, hy + 16, 'skin')
    for i in range(7):
        x = hx + 2 + i * 2.4
        c.limb([(x + 1, hy), (x + (i - 3) * 0.6, hy + 4 + (i % 2) * 2 + (3 if i > 4 else 0))], 2.6, 1.2, 'hair', bulge=0.3, rim=False)
    c.ellipse(hx + 3, hy - 3, hx + 15, hy + 2, 'rim', bulge=0.3)
    c.ellipse(hx + 5, hy - 2, hx + 13, hy + 1, 'water', bulge=0.3)
    # gekrümmter Schnabel, bei Angriff geöffnet
    if atk == 1:
        c.poly([(hx - 5, hy + 7), (hx + 3, hy + 6), (hx + 4, hy + 9), (hx - 4, hy + 9)], 'beak', bulge=0.5)
        c.poly([(hx - 3, hy + 12), (hx + 4, hy + 11), (hx + 4, hy + 14), (hx - 1, hy + 14)], 'beak', bulge=0.5)
        c.dpoly([(hx - 3, hy + 10), (hx + 4, hy + 10), (hx + 4, hy + 11), (hx - 2, hy + 11)], '#3a1414')
    else:
        c.poly([(hx - 4, hy + 8), (hx + 3, hy + 6), (hx + 5, hy + 10), (hx + 3, hy + 13), (hx - 2, hy + 12), (hx - 4, hy + 10)], 'beak', bulge=0.5)
        c.line(hx - 3, hy + 10, hx + 4, hy + 10, '#2a2008')
        c.px(hx - 4, hy + 11, '#2a2008')
    # Auge: tief, gelb, geschlitzt, mit Braue
    c.line(hx + 4, hy + 5, hx + 9, hy + 6, '#16200e')
    c.px(hx + 6, hy + 7, '#e8c040'); c.px(hx + 7, hy + 7, '#e8c040'); c.px(hx + 7, hy + 8, '#e8c040'); c.px(hx + 6, hy + 8, '#120a04')
    c.line(hx + 7, hy - 3, hx + 10, hy - 3, '#c8f0ff')
    # vorderer Arm: lang, Schwimmhaut-Klauen, greift beim Angriff weit nach vorn
    if atk == 0:
        arm = [(16 + lean, 18 + y0), (20 + lean, 24 + y0), (17 + lean, 29 + y0)]
    elif atk == 1:
        arm = [(14 + lean, 18 + y0), (6 + lean, 20 + y0), (-4 + lean, 21 + y0)]
    else:
        arm = [(15 + lean, 18 + y0), (9 + lean, 24 + y0), (6 + lean, 30 + y0)]
    c.limb(arm, 5, 4, 'skin')
    hxe, hye = arm[-1]
    c.poly([(hxe - 3, hye - 1), (hxe + 2, hye - 2), (hxe + 2, hye + 3), (hxe - 3, hye + 3)], 'skin', bulge=0.3)
    for d in (-2, 0, 2):
        if atk == 1:
            c.line(hxe - 3, hye + d, hxe - 5, hye + d, '#1e2a16')
        else:
            c.line(hxe + d // 2, hye + 3, hxe + d, hye + 5, '#1e2a16')
    # Flecken
    for x, y in ((20, 16), (27, 22), (14, 27)):
        c.px(x + lean, y + y0, SKIN_K[1])
    return c.render()


# ------------------------------------------------------------------ Oni
def oni(pose):
    w, bob, atk = pose_vals(pose)
    c = Canvas(64, 64, M(skin=ONI_R, tiger=TIGER, iron=IRON, hair=HAIR_W, horn=HORN), ox=14, oy=10)
    y0 = bob
    # Keule je nach Angriffsphase
    if atk == 0:
        club = [(28, 14 + y0), (36, -6 + y0)]          # hoch über die Schulter
    elif atk == 1:
        club = [(6, 26 + y0), (-12, 40 + y0)]          # nach vorn unten geschmettert
    else:
        club = [(10, 24 + y0), (2, 6 + y0)]
    # hinteres Bein / Arm
    c.limb([(26, 34 + y0), (29 - w, 44), (29 - w, 51)], 9, 7, 'skin')
    c.poly([(24 - w, 50), (33 - w, 50), (34 - w, 53), (23 - w, 53)], 'skin', bulge=0.3)
    c.limb([(30, 16 + y0), (35, 25 + y0), (33, 33 + y0)], 7, 6, 'skin')
    # Rumpf, muskulös
    c.ellipse(8, 10 + y0, 34, 38 + y0, 'skin', bulge=1.2)
    c.line(20, 17 + y0, 21, 32 + y0, ONI_R[1]); c.line(13, 22 + y0, 19, 23 + y0, ONI_R[1]); c.line(22, 23 + y0, 29, 22 + y0, ONI_R[1])
    # Tigerfell-Lendenschurz
    c.poly([(7, 31 + y0), (34, 31 + y0), (36, 42 + y0), (30, 40 + y0), (25, 43 + y0), (19, 40 + y0), (13, 43 + y0), (6, 40 + y0)], 'tiger', bulge=0.7)
    for x in (10, 16, 22, 28):
        c.line(x, 32 + y0, x + 2, 39 + y0, '#20160e')
    # vorderes Bein
    c.limb([(14, 38 + y0), (12 + w, 45), (11 + w, 51)], 10, 8, 'skin')
    c.poly([(5 + w, 50), (15 + w, 50), (16 + w, 53), (4 + w, 53)], 'skin', bulge=0.3)
    # Keule
    c.limb(club, 6, 9, 'iron', bulge=0.8)
    (ax, ay), (bx, by) = club
    for f in (0.35, 0.55, 0.75, 0.95):
        x, y = ax + (bx - ax) * f, ay + (by - ay) * f
        c.px(int(x) - 2, int(y), '#c8c4d0'); c.px(int(x) + 2, int(y) + 1, '#8a86a0')
    # vorderer Arm hält Keule
    c.limb([(12, 14 + y0), (8, 20 + y0), (ax, ay)], 8, 7, 'skin')
    c.circle(ax, ay, 4, 'skin', bulge=0.6)
    # Kopf: zackige Mähne, Hörner, Fratze
    mane = [(2, 14), (0, 6), (5, 7), (4, -1), (10, 3), (14, -4), (18, 2), (24, -3), (27, 4), (34, 1), (32, 9), (37, 12), (32, 16), (35, 22), (29, 21), (28, 25), (8, 24), (6, 20), (1, 21), (4, 16)]
    c.poly([(x, y + y0) for x, y in mane], 'hair', bulge=0.5)
    c.ellipse(8, 1 + y0, 29, 22 + y0, 'skin', bulge=1.1)
    c.limb([(11, 4 + y0), (8, -2 + y0), (7, -9 + y0)], 4, 1.5, 'horn', bulge=0.6)
    c.limb([(25, 3 + y0), (29, -3 + y0), (31, -10 + y0)], 4, 1.5, 'horn', bulge=0.6)
    c.line(10, 8 + y0, 16, 10 + y0, '#1a0a0a'); c.line(10, 7 + y0, 15, 8 + y0, '#1a0a0a')
    c.line(27, 8 + y0, 21, 10 + y0, '#1a0a0a'); c.line(27, 7 + y0, 22, 8 + y0, '#1a0a0a')
    c.dpoly([(11, 11 + y0), (16, 11 + y0), (15, 12 + y0), (12, 12 + y0)], '#f0d040'); c.px(14, 11 + y0, '#140806')
    c.dpoly([(21, 11 + y0), (26, 11 + y0), (25, 12 + y0), (22, 12 + y0)], '#f0d040'); c.px(23, 11 + y0, '#140806')
    c.line(18, 12 + y0, 17, 15 + y0, ONI_R[1]); c.line(16, 15 + y0, 19, 15 + y0, ONI_R[0])
    mo = 2 if atk == 1 else 0
    c.dpoly([(12, 17 + y0), (25, 17 + y0), (23, 20 + y0 + mo), (14, 20 + y0 + mo)], '#2a0808')
    for x in range(14, 24, 2):
        c.px(x, 17 + y0, BONEW)
    c.line(13, 19 + y0 + mo, 13, 15 + y0, BONEW); c.line(24, 19 + y0 + mo, 24, 15 + y0, BONEW)
    return c.render()


# ------------------------------------------------------------------ Gaki
def gaki(pose):
    w, bob, atk = pose_vals(pose)
    c = Canvas(40, 46, M(skin=GAKI_S, cloth=CLOTH_R, hair=HAIR_D), ox=6, oy=4)
    y0 = bob
    reach = {-1: 0, 0: -2, 1: 5, 2: 2}[atk]
    # hintere dürre Glieder
    c.limb([(20, 27 + y0), (23 - w, 33), (22 - w, 39)], 3, 3, 'skin')
    c.limb([(20, 14 + y0), (24, 21 + y0), (23, 28 + y0)], 3, 2, 'skin')
    # Lumpen um die Hüfte
    c.poly([(9, 27 + y0), (23, 27 + y0), (24, 34 + y0), (20, 32 + y0), (16, 35 + y0), (12, 32 + y0), (8, 34 + y0)], 'cloth', bulge=0.5)
    # aufgeblähter Bauch, eingefallene Brust mit Rippen
    c.ellipse(7, 12 + y0, 23, 30 + y0, 'skin', bulge=1.3)
    for yy in (14, 17, 20):
        c.line(10, yy + y0, 17, yy + 1 + y0, GAKI_S[1])
    c.px(12, 25 + y0, GAKI_S[0])
    c.limb([(13, 31 + y0), (11 + w, 36), (10 + w, 40)], 3, 3, 'skin')
    c.line(8 + w, 40, 12 + w, 40, GAKI_S[0])
    # Kopf: Schädelhaft, wirres dünnes Haar, eingefallene Augen
    hx = 5 + (reach // 2)
    c.ellipse(hx, 1 + y0, hx + 13, 15 + y0, 'skin')
    for i, (dx, L) in enumerate(((6, 8), (9, 11), (12, 13), (14, 9))):
        c.limb([(hx + dx, 1 + y0), (hx + dx + 3, 1 + L + y0 + (1 if (i + max(0, pose[1])) % 2 else 0))], 1.6, 1, 'hair', bulge=0.2, rim=False)
    c.dellipse(hx + 2, 5 + y0, hx + 5, 8 + y0, '#1a1414'); c.px(hx + 3, 6 + y0, '#d8d070')
    c.dellipse(hx + 7, 5 + y0, hx + 9, 8 + y0, '#1a1414')
    c.line(hx + 4, 9 + y0, hx + 5, 10 + y0, GAKI_S[1])
    mo = 3 if atk == 1 else 1
    c.dpoly([(hx + 1, 11 + y0), (hx + 7, 11 + y0), (hx + 6, 12 + y0 + mo), (hx + 2, 12 + y0 + mo)], '#2a0c10')
    c.px(hx + 2, 11 + y0, BONEW); c.px(hx + 5, 11 + y0, BONEW)
    # vorderer Arm, krallend
    if atk == 1:
        arm = [(10, 15 + y0), (3, 16 + y0), (-5, 17 + y0)]
    elif atk == 0:
        arm = [(10, 15 + y0), (12, 20 + y0), (10, 24 + y0)]
    else:
        arm = [(10, 15 + y0), (6, 21 + y0), (4, 27 + y0)]
    c.limb(arm, 3, 2, 'skin')
    ex, ey = arm[-1]
    for d in (-1, 1, 3):
        c.line(ex, ey, ex - 2, ey + d, '#2a2a20')
    return c.render()


# ------------------------------------------------------------------ Kamaitachi
def kamaitachi(pose):
    w, bob, atk = pose_vals(pose)
    c = Canvas(52, 34, M(fur=WEASEL, blade=BLADE), ox=4, oy=6)
    stretch = {-1: 0, 0: -3, 1: 4, 2: 1}[atk]
    # Wirbelwind-Spuren
    for i, (x, y) in enumerate(((30, 6), (36, 20), (26, 24))):
        ph = (i + max(0, pose[1])) % 3
        c.line(x + ph, y, x + 10 + ph, y - 3, WIND); c.line(x + 4 + ph, y + 1, x + 13 + ph, y - 1, '#8aa0b8')
    if atk == 1:
        for k in range(4):
            c.line(-2 + k * 3, 4 + k, 10 + k * 4, -2 + k * 2, '#e8f4ff')
    # Schwanz
    c.limb([(30, 14), (38, 10 - w), (44, 6 - w)], 6, 3, 'fur', bulge=0.7)
    # langer Körper im Sprung
    c.ellipse(9 - stretch, 8, 34 + stretch // 2, 20, 'fur', bulge=1.1)
    c.ellipse(12 - stretch, 14, 28, 20, 'fur', bulge=0.4)
    # Hinterbeine
    c.limb([(28, 17), (32 + w, 22), (35 + w, 24)], 4, 3, 'fur')
    # Kopf
    c.ellipse(0 - stretch, 5, 12 - stretch, 15, 'fur')
    c.poly([(-3 - stretch, 10), (2 - stretch, 8), (3 - stretch, 13), (-2 - stretch, 12)], 'fur', bulge=0.4)
    c.ellipse(4 - stretch, 3, 8 - stretch, 7, 'fur', bulge=0.4)
    c.px(-3 - stretch, 10, INK)
    c.px(2 - stretch, 9, '#f0e070'); c.px(3 - stretch, 9, '#f0e070'); c.px(3 - stretch, 10, INK)
    c.line(-1 - stretch, 13, 3 - stretch, 13, '#2a1a10')
    # Sichel-Vorderbeine
    up = {-1: 0, 0: -4, 1: 2, 2: 0}[atk]
    c.limb([(10 - stretch, 15), (6 - stretch, 18 + up // 2)], 4, 3, 'fur')
    c.poly([(6 - stretch, 18 + up // 2), (-6 - stretch, 22 + up), (-9 - stretch, 18 + up), (-2 - stretch, 18 + up)], 'blade', bulge=0.4)
    c.line(-8 - stretch, 19 + up, 4 - stretch, 18 + up // 2, '#f0f6ff')
    c.limb([(18, 17), (16 + w, 22)], 4, 3, 'fur')
    c.poly([(16 + w, 22), (8 + w, 26), (6 + w, 24), (12 + w, 21)], 'blade', bulge=0.4)
    return c.render()


ALL = {'kappa': kappa, 'oni': oni, 'gaki': gaki, 'kamaitachi': kamaitachi}


def frames(fn):
    return [fn(('walk', i)) for i in range(4)] + [fn(('atk', i)) for i in range(3)]


if __name__ == '__main__':
    from sculpt import preview
    preview([(n, frames(f)) for n, f in ALL.items()], '/tmp/prev/v2.png', scale=3, cols=1)
