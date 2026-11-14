"""Version 2: ernste, folkloretreue Yōkai mit volumetrischer Schattierung (sculpt).

Jede Kreatur: fn(pose) -> PIL-Bild. pose = ('walk', i) mit i in 0..3 oder
('atk', i) mit i in 0..2 (Ausholen, Zuschlagen, Zurückziehen). Blick nach links.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sculpt import Canvas, ramp, mix, cel  # noqa: E402

INK = '#140d18'
BONEW = '#e8e0c8'


def M(**kw):
    return kw


# Gemeinsame Materialien – satt, kontrastreich, 16-Bit-Stil
SKIN_K = cel('#3fa04a')
BELLY_K = cel('#c8c870')
SHELL = cel('#7a5030')
SHELLRIM = cel('#c89a50')
BEAK = cel('#e8b020')
HAIR_D = cel('#2a3a5a', 16)
WATER = cel('#50b8e8')
ONI_R = cel('#e0302a', 18)
TIGER = cel('#f0b020')
IRON = cel('#5a6080', 14)
HAIR_W = cel('#3a2a3a', 12)
HORN = cel('#f0e0b0', 12)
GAKI_S = cel('#a0a888', 18)
CLOTH_R = cel('#7a4a8a', 16)
WEASEL = cel('#d89a50')
BLADE = cel('#b8c8e0', 10)
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
    """Roter Oni: muskulös, Mähne, zwei Hörner, Hauer, Tigerfell, eiserner Kanabō."""
    w, bob, atk = pose_vals(pose)
    c = Canvas(72, 74, M(skin=ONI_R, tiger=TIGER, iron=IRON, hair=HAIR_W, horn=HORN, nail=cel('#f0e8d0', 8)), ox=16, oy=12)
    y0 = bob
    L = '#5a0c10'                              # Muskel-/Faltenlinien (dunkelrot)
    if atk == 0:
        club = [(30, 16 + y0), (40, -8 + y0)]
    elif atk == 1:
        club = [(4, 30 + y0), (-15, 46 + y0)]
    else:
        club = [(9, 27 + y0), (1, 6 + y0)]
    # ---- hinteres Bein
    c.limb([(29, 40 + y0), (32 - w, 50), (31 - w, 57)], 11, 9, 'skin')
    c.poly([(25 - w, 56), (36 - w, 56), (37 - w, 60), (24 - w, 60)], 'skin', bulge=0.4)
    for x in (26, 29, 32, 35):
        c.px(x - w, 60, '#f0e8d0')
    # ---- hinterer Arm
    c.limb([(34, 18 + y0), (40, 27 + y0), (38, 36 + y0)], 9, 8, 'skin')
    c.circle(38, 37 + y0, 4, 'skin', bulge=0.6)
    c.line(36, 39 + y0, 37, 41 + y0, L); c.line(39, 39 + y0, 40, 41 + y0, L)
    # ---- Rumpf: Brust, Bauch
    c.ellipse(8, 12 + y0, 38, 44 + y0, 'skin', bulge=1.2)
    c.ellipse(10, 15 + y0, 23, 26 + y0, 'skin', bulge=0.8)              # Brustmuskel vorn
    c.ellipse(22, 15 + y0, 35, 26 + y0, 'skin', bulge=0.8)              # Brustmuskel hinten
    c.line(22, 17 + y0, 22, 40 + y0, L)
    for yy in (29, 33, 37):
        c.line(15, yy + y0, 21, yy + y0, L); c.line(23, yy + y0, 29, yy + y0, L)
    c.line(12, 25 + y0, 20, 27 + y0, L); c.line(24, 27 + y0, 33, 25 + y0, L)
    c.px(16, 22 + y0, L); c.px(29, 22 + y0, L)
    # ---- Tigerfell-Lendenschurz mit Gürtelstrick
    c.poly([(7, 38 + y0), (38, 38 + y0), (40, 50 + y0), (34, 47 + y0), (28, 51 + y0), (22, 47 + y0), (16, 51 + y0), (10, 47 + y0), (6, 50 + y0)], 'tiger', bulge=0.7)
    for x in (10, 16, 22, 28, 34):
        c.dpoly([(x, 39 + y0), (x + 2, 39 + y0), (x + 3, 46 + y0), (x + 1, 44 + y0)], '#1a1008')
    c.limb([(6, 38 + y0), (39, 38 + y0)], 3, 3, 'horn', bulge=0.3)
    # ---- vorderes Bein
    c.limb([(15, 45 + y0), (13 + w, 52), (12 + w, 57)], 12, 10, 'skin')
    c.poly([(5 + w, 56), (17 + w, 56), (18 + w, 60), (4 + w, 60)], 'skin', bulge=0.4)
    c.line(9 + w, 50, 15 + w, 51, L)
    for x in (5, 8, 11, 14):
        c.px(x + w, 60, '#f0e8d0')
    # ---- Kanabō mit Eisenbuckeln
    c.limb(club, 7, 11, 'iron', bulge=0.9)
    (ax, ay), (bx, by) = club
    for f in (0.3, 0.45, 0.6, 0.75, 0.9):
        x, y = ax + (bx - ax) * f, ay + (by - ay) * f
        c.circle(int(x - 3), int(y), 1, 'nail', bulge=0.3, rim=False)
        c.circle(int(x + 3), int(y + 1), 1, 'nail', bulge=0.3, rim=False)
    # ---- vorderer Arm mit Faust um die Keule
    c.limb([(12, 16 + y0), (7, 23 + y0), (ax + 2, ay)], 10, 8, 'skin')
    c.circle(ax, ay, 5, 'skin', bulge=0.7)
    for d in (-2, 0, 2):
        c.line(ax - 4, ay + d, ax - 1, ay + d, L)
    c.line(9, 20 + y0, 11, 25 + y0, L)
    # ---- Kopf: wilde Mähne, Hörner, Fratze
    mane = [(1, 16), (-2, 8), (4, 8), (1, -1), (9, 3), (11, -6), (17, 0), (22, -7), (26, 0), (33, -4), (33, 4), (40, 4), (36, 11), (41, 16), (35, 18), (38, 25), (31, 23), (30, 28), (9, 27), (7, 22), (1, 23), (5, 18)]
    c.poly([(x, y + y0) for x, y in mane], 'hair', bulge=0.6)
    for x0, y1 in ((4, 8), (11, -2), (22, -5), (33, 0), (38, 14)):
        c.line(x0 + 3, y1 + 6 + y0, x0, y1 + y0, mix(HAIR_W[2], HAIR_W[3], 0.5))
    c.ellipse(8, 2 + y0, 31, 25 + y0, 'skin', bulge=1.1)
    c.limb([(11, 6 + y0), (7, -1 + y0), (5, -10 + y0)], 5, 1.5, 'horn', bulge=0.7)
    c.limb([(27, 5 + y0), (31, -2 + y0), (34, -11 + y0)], 5, 1.5, 'horn', bulge=0.7)
    for k in range(3):
        c.line(7 - k // 2, 2 - k * 3 + y0, 10 - k // 2, 1 - k * 3 + y0, HORN[0])
    # Stirnfalten, buschige Brauen
    c.line(14, 6 + y0, 25, 6 + y0, L); c.line(16, 4 + y0, 23, 4 + y0, L)
    c.dpoly([(9, 9 + y0), (18, 11 + y0), (17, 13 + y0), (10, 11 + y0)], '#1a0a0a')
    c.dpoly([(30, 9 + y0), (21, 11 + y0), (22, 13 + y0), (29, 11 + y0)], '#1a0a0a')
    # Augen: gelb, glühend, kleine Pupille
    c.dpoly([(11, 13 + y0), (17, 13 + y0), (16, 15 + y0), (12, 15 + y0)], '#ffe040'); c.px(15, 14 + y0, '#140806'); c.px(12, 13 + y0, '#fff8c0')
    c.dpoly([(22, 13 + y0), (28, 13 + y0), (27, 15 + y0), (23, 15 + y0)], '#ffe040'); c.px(23, 14 + y0, '#140806'); c.px(27, 13 + y0, '#fff8c0')
    # Nase
    c.dpoly([(18, 15 + y0), (21, 15 + y0), (22, 18 + y0), (17, 18 + y0)], ONI_R[0]); c.px(18, 18 + y0, '#1a0a0a'); c.px(21, 18 + y0, '#1a0a0a')
    # Maul mit Zahnreihe und Hauern
    mo = 3 if atk == 1 else (1 if atk == 0 else 0)
    c.dpoly([(12, 20 + y0), (27, 20 + y0), (25, 23 + y0 + mo), (14, 23 + y0 + mo)], '#2a0608')
    if mo:
        c.dpoly([(15, 22 + y0 + mo), (24, 22 + y0 + mo), (23, 23 + y0 + mo), (16, 23 + y0 + mo)], '#c83a4a')
    for x in range(14, 26, 2):
        c.px(x, 20 + y0, BONEW); c.px(x + 1, 20 + y0, '#c8c0a8')
    c.dpoly([(12, 23 + y0 + mo), (14, 23 + y0 + mo), (13, 17 + y0)], BONEW)
    c.dpoly([(25, 23 + y0 + mo), (27, 23 + y0 + mo), (26, 17 + y0)], BONEW)
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
