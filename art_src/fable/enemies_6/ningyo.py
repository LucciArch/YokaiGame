"""Ningyo (人魚) – kein Meermädchen, sondern der Fisch mit Menschengesicht aus den Edo-Berichten.
Komplett neu (Runde 106): kräftiger Karpfenleib mit großen Schuppen (heller Bauch, dunkler Rücken),
stachelige Rückenflosse, Brust- und Bauchflossen, gegabelte Schwanzflosse mit Strahlen, Seitenlinie.
Vorn ein fahles, unheimlich menschliches Gesicht (eingesunkene Augen, schmale Lippen mit kleinen Zähnen),
nasses schwarzes Haar, das über den Rücken fließt, und zwei dürre Arme mit Schwimmhäuten.
Bewegung: schlängelnd. Angriff: reißt den Mund auf und spuckt einen Wasserstrahl."""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 104, 64
OX, OY = 6, 8
col('hb', '#1a1738')
FISH = ('p1', 'p2', 'p3')
FISHF = ('p0', 'p1', 'p2')
FACE = ('l1', 'l2', 'l3')
col('l0', '#2a2440'); col('l1', '#7a6c78'); col('l2', '#b4a6a8'); col('l3', '#e2d8cc')
add_rim('l0 l1 l2', 'l3')
HAIR = ('h0', 'hb', 'h1')
LEG = dict(zip('abcdKqWe', ['l0', 'l1', 'l2', 'l3', 'K', 'q', 'b3', 'e1']))
FACEG = """
.....dddcc.......
...dddddcccbb....
..ddddccccccbb...
.dddcccccccbbbb..
.ddccccccccbbbbb.
.dcbaaccbaacbbbbb
.dcKKKcdcKKKbbbbb
.dcWeKcdcWeKbbbbb
.dccbacdccbabbbbb
ddcccdddccccbbbbb
dddccdcdcccbbbbba
.cccccccccbbbbbba
.ccbbbbbbbbbbbbaa
..cqWqWqWqWbbbba.
..cbqqqqqqqbbbaa.
...cbbbbbbbbbaa..
....bbbbbbbaaa...
......aaaaaa.....
"""


def P(x, y):
    return (x + OX, y + OY)


def draw(ph=0.0, mouth=0, arm=0, bob=0):
    setsize(CW, CH)
    c = C()

    def spine(t):                                        # t: 0 Kopf → 1 Schwanzstiel
        x = 22 + t * 52
        y = 30 + bob + math.sin(t * 3.0 + ph) * (1 + t * 3)
        return (x, y)

    def thick(t):
        T = [0, 0.15, 0.35, 0.6, 0.85, 1.0]; V = [11, 13.5, 14, 10.5, 5.4, 2.6]
        for i in range(5):
            if t <= T[i + 1]:
                f = (t - T[i]) / (T[i + 1] - T[i])
                return V[i] + (V[i + 1] - V[i]) * f
        return V[-1]

    # ---- Schwanzflosse (gegabelt, mit Strahlen)
    tp = spine(1.0)
    p = C()
    up = (tp[0] + 14, tp[1] - 13 + math.sin(ph) * 2)
    dn = (tp[0] + 14, tp[1] + 11 + math.sin(ph) * 2)
    fin = PG([P(*tp), P(*up), P(tp[0] + 9, tp[1] - 1), P(*dn)])
    p.form(fin, FISHF, sd=2, hl=1)
    for k in range(5):
        q = lerp(up, dn, k / 4)
        p.line([P(*tp), P(q[0] - 1, q[1])], 'p0', only=erode(fin, 1))
    c.stamp(p, 'K')
    # ---- ferne Brustflosse + Rückenflosse
    p = C()
    for k in range(6):                                   # Stachelstrahlen
        t = 0.3 + k * 0.07
        b_ = spine(t)
        th = thick(t)
        p.form(L(*P(b_[0], b_[1] - th + 1), 1.4, *P(b_[0] + 3, b_[1] - th - 7 + abs(k - 2) * 0.8), 0.5), FISHF, sd=0, hl=1)
    memb = PG([P(*(lambda b: (b[0], b[1] - thick(0.3) + 1))(spine(0.3))),
               P(spine(0.32)[0] + 3, spine(0.32)[1] - thick(0.32) - 6),
               P(spine(0.65)[0] + 3, spine(0.65)[1] - thick(0.65) - 3),
               P(*(lambda b: (b[0], b[1] - thick(0.66) + 1))(spine(0.66)))])
    p.fill(memb & ~p.a.astype(bool), 'p1')
    c.stamp(p, 'K')
    # ---- Leib
    p = C()
    body = None
    for i in range(24):
        t0, t1 = i / 24, (i + 1) / 24
        s_ = L(*P(*spine(t0)), thick(t0), *P(*spine(t1)), thick(t1))
        body = s_ if body is None else body | s_
    p.form(body, FISH, sd=4, hl=1)
    # heller Bauch
    belly = body & ~sh(body, 0, -4)
    p.fill(belly, 'l3')
    p.fill(belly & ~sh(body, 0, -2), 'l2')
    # Schuppen: versetzte Bögen
    for row in range(-2, 3):
        for k in range(8):
            t = 0.14 + k * 0.095 + (row % 2) * 0.045
            if t > 0.95:
                continue
            b_ = spine(t)
            th = thick(t)
            cy = b_[1] + row * th * 0.34
            if abs(row) * th * 0.34 > th - 3:
                continue
            q = P(b_[0], cy)
            p.line([(q[0] - 1, q[1] - 1.5), (q[0] + 1, q[1]), (q[0] - 1, q[1] + 1.5)], 'p1', only=erode(body, 1) & ~belly)
    p.line([P(*spine(t / 10)) for t in range(1, 10)], 'p0', only=erode(body, 1))   # Seitenlinie
    c.stamp(p, 'K')
    # ---- Bauchflosse + nahe Brustflosse
    for (t, ln, dyf) in ((0.55, 7, 1), (0.22, 9, 0)):
        b_ = spine(t)
        th = thick(t)
        p = C()
        root = (b_[0] - 1, b_[1] + th * 0.5 - dyf * 2)
        tip = (b_[0] + ln * 0.8, b_[1] + th * 0.5 + ln * 0.7 + math.sin(ph + t * 5) * 1.5)
        f_ = PG([P(*root), P(root[0] + 4, root[1] - 1), P(*tip), P(tip[0] - 4, tip[1] - 1)])
        p.form(f_, FISHF, sd=1, hl=1)
        p.line([P(*root), P(*tip)], 'p0', only=f_)
        c.stamp(p, 'K')
    # ---- Gesicht vorn am Kopf
    hx, hy = spine(0.0)
    p = C()
    p.grid(int(P(hx - 16, hy - 9)[0]), int(P(hx - 16, hy - 9)[1]), FACEG, LEG)
    if mouth:
        p.fill(E(*P(hx - 10, hy + 5), 3.6, 1.0 + mouth * 0.7), 'q')
    c.stamp(p, 'K')
    # ---- nasses Haar über Kopf und Rücken
    rg = random.Random(4)
    for i in range(7):
        t = i / 6
        p = C()
        root = P(hx - 12 + t * 10, hy - 9 + t * 2)
        Q = [root]
        for f in (0.35, 0.7, 1.0):
            sx = root[0] + (18 + t * 10) * f
            sy = root[1] - 2 * f + math.sin(f * 4 + ph + i) * 2 + f * (3 + t * 3)
            Q.append((sx, sy))
        r_ = 2.6 - (i % 2) * 0.4
        lock = L(*Q[0], r_, *Q[1], r_ * 0.9) | L(*Q[1], r_ * 0.9, *Q[2], r_ * 0.6) | L(*Q[2], r_ * 0.6, *Q[3], 0.6)
        p.form(lock, HAIR, sd=1, hl=1)
        p.line([Q[0], Q[1], Q[2]], 'h2' if i % 2 else 'h0', only=erode(lock, 1))
        c.stamp(p, 'K')
    # ---- dürre Arme mit Schwimmhäuten
    for (sx, far) in ((6, True), (2, False)):
        p = C()
        s0 = P(hx + sx - 2, hy + 10)
        el = (s0[0] - 3 - arm, s0[1] + 5)
        hd = (el[0] - 5 - arm * 2, el[1] - arm)
        ramp = ('l0', 'l1', 'l2') if far else FACE
        p.form(L(*s0, 1.6, *el, 1.3) | L(*el, 1.3, *hd, 1.1), ramp, sd=1, hl=1)
        web = PG([hd, (hd[0] - 3, hd[1] - 2), (hd[0] - 3.5, hd[1] + 1), (hd[0] - 2, hd[1] + 3)])
        p.fill(web, 'p2' if not far else 'p1')
        for (dx, dy) in ((-3, -2), (-3.5, 1), (-2, 3)):
            p.line([hd, (hd[0] + dx, hd[1] + dy)], ramp[1])
        c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(ph=0), dict(ph=1.6, bob=-1), dict(ph=3.2), dict(ph=4.8, bob=-1)]
ATTACK = [dict(ph=0.5, arm=1), dict(ph=1.0, mouth=2, arm=2), dict(ph=1.6, mouth=1)]

if __name__ == '__main__':
    export('ningyo', draw, WALK, ATTACK)
