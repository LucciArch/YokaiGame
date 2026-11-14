import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sculpt import Canvas, ramp, preview, mix

M = {
 'skin': ramp('#5e8a4e', 6, hue_shift=20),
 'belly': ramp('#a8a86a', 5, hue_shift=16),
 'shell': ramp('#6a5038', 6, hue_shift=16),
 'shellrim': ramp('#a08050', 5),
 'beak': ramp('#b89040', 5, hue_shift=20),
 'hair': ramp('#2a3a30', 4, hue_shift=12, dark=0.5, light=0.35),
 'water': ramp('#5aa0b8', 5, hue_shift=14),
}

def kappa(k):
    c = Canvas(46, 48, M, ox=3, oy=4)
    st = [0, 1, 0, -1][k]
    # hinteres Bein / Arm
    c.limb([(26, 30), (30, 36), (27, 40)], 6, 5, 'skin')
    c.limb([(14, 18), (8, 24), (6, 30)], 5, 4, 'skin')
    # Panzer (hinten)
    c.ellipse(16, 10, 40, 36, 'shell', bulge=1.3)
    c.limb([(18, 12), (36, 14), (40, 26), (34, 36)], 3, 3, 'shellrim', bulge=0.5)
    # Körper gebückt
    c.ellipse(9, 14, 30, 36, 'skin')
    c.ellipse(11, 20, 22, 35, 'belly', bulge=0.7)
    # vorderes Bein
    c.limb([(18, 32), (14 + st, 38), (12 + st, 41)], 7, 5, 'skin')
    c.poly([(7 + st, 40), (16 + st, 40), (17 + st, 42), (6 + st, 42)], 'skin', bulge=0.4)
    c.limb([(26, 31), (29 - st, 37), (30 - st, 41)], 6, 5, 'skin')
    # Kopf
    c.ellipse(4, 2, 22, 19, 'skin')
    # Schnabel
    c.poly([(0, 11), (7, 9), (10, 13), (8, 16), (1, 14)], 'beak', bulge=0.6)
    # Haarkranz + Teller
    c.poly([(5, 5), (8, 1), (12, 0), (18, 1), (22, 4), (23, 9), (20, 7), (16, 6), (10, 6), (6, 8)], 'hair', bulge=0.4)
    c.ellipse(8, -1, 20, 4, 'water', bulge=0.4)
    # vorderer Arm mit Klauen
    c.limb([(14, 18), (8, 24), (4, 30)], 5, 4, 'skin')
    for dx in (-2, 0, 2):
        c.line(4 + dx // 2, 30, 2 + dx, 33, '#2a3a24')
    # Details
    c.line(1, 13, 8, 12, '#5a3a14')               # Mundspalte
    c.px(3, 14, '#e8e0c8'); c.px(6, 14, '#e8e0c8')  # Zähne
    c.px(10, 7, '#e8d050'); c.px(11, 7, '#e8d050'); c.px(11, 8, '#1a1008'); c.px(10, 8, '#c8a030')   # Auge
    c.line(9, 6, 13, 5, '#1e2a18')                # Braue
    c.line(10, 0, 13, 0, '#c8f0ff')
    for x, y in ((24, 22), (28, 18), (32, 26), (23, 29)):
        c.px(x, y, '#3a2a1a')
    return c.render()

preview([('kappa', [kappa(i) for i in range(4)])], '/tmp/prev/v2kappa.png', scale=5, cols=1)
