"""Tsurube-otoshi – riesiger Kopf, der aus den Baumkronen herabstürzt. Komplett neu (Runde 103): anatomischer
Schädel im Dreiviertelprofil nach links: schwerer Brauenwulst, tiefliegende blutunterlaufene Augen, Hakennase,
hohe Wangenknochen, Ohr, Kiefermuskel, breites Grinsen mit Zahnreihen und Zahnfleisch, Stirnfalten, Bartstoppeln.
Das schwarze Haar weht beim Fallen nach oben wie Äste. Angriff: reißt das Maul auf und stürzt herab."""
import sys, os, math, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 92, 100
OX, OY = 8, 6
col('hb', '#1a1738')
col('ts0', '#341a26'); col('ts1', '#744434'); col('ts2', '#b07e52'); col('ts3', '#dcb276'); col('ts4', '#f6dca2')
col('xts', '#f4e0b4'); add_rim('ts0 ts1 ts2', 'xts')
DARK.update(ts4='ts3', ts3='ts2', ts2='ts1', ts1='ts0')
SK = ('ts1', 'ts2', 'ts3')
SKD = ('ts0', 'ts1', 'ts2')
HAIR = ('h0', 'hb', 'h1')


def P(x, y):
    return (x + OX, y + OY)


def draw(bob=0, mouth=0, wave=0.0, drop=0, squint=0):
    setsize(CW, CH)
    c = C()

    def B(x, y):
        return P(x, y + bob + drop)

    # ---- Haar: lange Strähnen, die nach oben wehen (wie Äste)
    rg = random.Random(7)
    for i in range(13):
        t = i / 12
        root = B(22 + t * 34, 40 - math.sin(t * math.pi) * 14)
        ln = 18 + rg.uniform(0, 10) + math.sin(t * math.pi) * 8 + drop * 0.6
        ang = math.radians(-90 - (0.5 - t) * 110 + rg.uniform(-10, 10))
        wob = rg.choice((-1, 1)) * rg.uniform(3.0, 5.0)
        ph = rg.uniform(0, 6)
        Q = []
        for f in (0, 0.35, 0.7, 1):
            x = root[0] + math.cos(ang) * ln * f + math.sin(f * 5 + ph + wave) * wob * f
            y = root[1] + math.sin(ang) * ln * f
            Q.append((x, max(4, y)))
        q = C()
        r_ = 3.6 - (i % 3) * 0.5
        lock = L(*Q[0], r_, *Q[1], r_ * 0.9) | L(*Q[1], r_ * 0.9, *Q[2], r_ * 0.6) | L(*Q[2], r_ * 0.6, *Q[3], 0.7)
        q.form(lock, HAIR, sd=1, hl=1)
        q.line([lerp(Q[0], Q[1], 0.3), Q[1], lerp(Q[1], Q[2], 0.6)], 'h2' if i % 2 else 'h0', only=erode(lock, 1))
        c.stamp(q, 'K')
    # ---- Ohr (rechts, hinter dem Kiefer)
    p = C()
    ear = E(*B(60, 52), 4.4, 7.0)
    p.form(ear, SK, sd=2, hl=1)
    p.line([B(60, 48), B(58, 52), B(60, 56)], 'ts1', only=ear)
    c.stamp(p, 'ts0')
    # ---- Schädel + Unterkiefer
    p = C()
    cran = E(*B(42, 44), 21, 18)
    jaw = PG([B(18, 60), B(26, 72 + mouth), B(40, 78 + mouth), B(54, 72 + mouth * 0.6), B(60, 60), B(58, 52), B(22, 54)])
    head = cran | jaw
    p.form(head, SK, sd=5, hl=2)
    darken(p, head & ~sh(E(*B(30, 42), 26, 26), 0, 0) & (p.a > 0))                  # Schattenseite rechts
    darken(p, head & ~sh(E(*B(30, 42), 30, 30), 0, 0) & (p.a > 0))
    # Haaransatz: Haar liegt auf dem Oberkopf
    hcap = cran & ~E(*B(36, 56), 22, 22)
    p.form(hcap, HAIR, sd=1, hl=1)
    for x in range(24, 60, 4):
        p.line([B(x, 28), B(x - 1, 34)], 'h2', only=hcap)
    # Stirnfalten
    for k, y in enumerate((40,)):
        p.line([B(24 + k, y), B(30, y - 1), B(38, y)], 'ts1', only=head)
    # Wangenknochen + Kiefermuskel
    p.form(E(*B(36, 56), 6, 4) & head, SK, sd=1, hl=1)
    p.line([B(40, 59), B(46, 62)], 'ts1', only=head)
    p.line([B(52, 56), B(54, 66)], 'ts1', only=head)
    # Bartstoppeln am Kinn
    for (x, y) in ((44, 74), (48, 72), (40, 76), (51, 69), (36, 75)):
        p.pxs([B(x, y + mouth * 0.8)], 'ts1')
    c.stamp(p, 'K')
    # ---- Brauenwulst + Augen
    p = C()
    for (ex, ey, s_) in ((24, 48, 0.85), (38, 48, 1.1)):
        sock = E(*B(ex, ey), 4.6 * s_ + 0.6, 3.4 * s_)
        p.fill(sock, 'ts0')
        eye = E(*B(ex - 0.5, ey + 0.5), 3.4 * s_, 2.0 * s_ - squint * 0.6)
        p.form(eye, ('b1', 'b2', 'b3'), sd=1, hl=1)
        p.pxs([B(ex + 1.6 * s_, ey + 1)], 'e0')                                         # Äderchen
        p.fill(E(*B(ex - 1, ey + 0.5), 1.4, 1.4) & eye, 'e1')                            # Iris
        p.pxs([B(ex - 1, ey + 0.5)], 'K')
        p.pxs([B(ex - 2, ey - 0.5)], 'y3')
    brow = L(*B(19, 41), 1.8, *B(29, 44), 2.4) | L(*B(32, 44), 2.4, *B(44, 40), 2.2)
    p.form(brow, SK, sd=1, hl=1)
    p.line([B(20, 43), B(29, 46), B(32, 46), B(44, 42)], 'ts0', only=brow)
    c.stamp(p, 'K')
    # ---- Hakennase
    p = C()
    nose = PG([B(29, 44), B(25, 54), B(19, 59), B(23, 61), B(30, 61), B(33, 58)])
    p.form(nose, SK, sd=2, hl=1)
    p.pxs([B(24, 60), B(25, 60)], 'ts0')
    p.line([B(31, 50), B(33, 58)], 'ts1', only=nose)
    c.stamp(p, 'ts0')
    # ---- Maul: breites Grinsen mit Zahnreihen
    p = C()
    m = PG([B(18, 64), B(30, 63), B(46, 62), B(52, 61), B(48, 66 + mouth), B(34, 70 + mouth * 1.4), B(22, 68 + mouth)])
    p.fill(m, 'q')
    gum = m & ~sh(m, 0, -2)
    p.fill(m & sh(m, 0, 2) & ~sh(m, 0, -1) & (E(*B(34, 63), 20, 2.2)), 'm2')
    p.fill(R(*B(20, 64), *B(49, 65)) & m, 'b2')                                         # obere Zähne
    for x in range(22, 50, 4):
        p.pxs([B(x, 64), B(x, 65)], 'b0')
        p.pxs([B(x - 2, 64)], 'b3')
    lw = m & sh(m, 0, -2) & ~sh(m, 0, 2 + int(mouth))
    for x in range(24, 48, 4):                                                        # untere Zähne
        yb = 68 + mouth * 1.2 - abs(x - 34) * 0.12
        p.fill(R(*B(x, yb - 1), *B(x + 2, yb)) & m, 'b2')
    if mouth > 1:
        p.fill(E(*B(34, 68 + mouth), 6, 1.8) & m & ~lw, 'm1')                            # Zunge
    p.line([B(17, 63), B(22, 62), B(30, 62)], 'ts0')                                    # Oberlippe
    c.stamp(p, 'ts0')
    p = C()
    lip = (L(*B(22, 70 + mouth), 1.4, *B(34, 72 + mouth * 1.4), 1.6) | L(*B(34, 72 + mouth * 1.4), 1.6, *B(48, 68 + mouth), 1.2))
    p.form(lip & ~m, SK, sd=1, hl=1)
    c.stamp(p, 'ts0')
    c.blacken()
    return c


WALK = [dict(bob=0, wave=0), dict(bob=-1, wave=1.5), dict(bob=-2, wave=3), dict(bob=-1, wave=4.5)]
ATTACK = [dict(bob=-3, squint=1, wave=1, mouth=1), dict(drop=6, mouth=5, wave=2.5), dict(drop=4, mouth=3, wave=4)]

if __name__ == '__main__':
    export('tsurube_otoshi', draw, WALK, ATTACK)
