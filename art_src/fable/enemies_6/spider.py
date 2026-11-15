"""Gemeinsames Spinnengerüst für Gyūki und Tsuchigumo (Runde 104).
Anatomie: Kopfbruststück (Prosoma) mit Kopf vorn, Hinterleib (Opisthosoma) über einem schmalen Stiel,
acht Beine je vier pro Seite, jedes aus Hüfte → Schenkel steil nach oben → Knie hoch über dem Körper →
Schiene schräg nach unten → Fußglied mit Klaue. Gelenkringe hell, ferne Beine dunkel und zuerst gezeichnet."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'enemies_4'))
from common import *
import common
common.D = os.path.dirname(os.path.abspath(__file__)) + '/'

CW, CH = 136, 102
OX, OY = 14, 16                     # lokale Grundlinie y = 78
GY = 78
# Fußpunkte (lokal) der vier Beine einer Seite, von vorn nach hinten, und Hüftpunkte am Prosoma
FEET_N = [(6, GY), (28, GY), (76, GY), (106, GY)]
FEET_F = [(14, GY - 3), (40, GY - 3), (80, GY - 3), (112, GY - 3)]
HIPS_N = [(40, 50), (46, 52), (52, 52), (57, 50)]
HIPS_F = [(42, 46), (48, 47), (54, 47), (58, 45)]
KNEE_H = [22, 20, 26, 30]          # Kniehöhe über dem Boden-Ursprung


def P(x, y):
    return (x + OX, y + OY)


def leg(c, hip, foot, kh, ramp, joint, stripe=None, lift=0, reach=0):
    foot = (foot[0] + reach, foot[1] - lift)
    knee = (hip[0] + (foot[0] - hip[0]) * 0.42, kh - lift * 0.5)
    ank = (foot[0] + (knee[0] - foot[0]) * 0.18, foot[1] - 9 - lift * 0.3)
    p = C()
    fem = L(*P(*hip), 2.6, *P(*knee), 2.0)
    tib = L(*P(*knee), 2.0, *P(*ank), 1.4)
    tar = L(*P(*ank), 1.3, *P(*foot), 0.6)
    p.form(fem, ramp, sd=1, hl=1)
    p.form(tib | tar, ramp, sd=1, hl=1)
    if stripe:
        for seg, n in ((fem, 3), (tib, 3)):
            pass
        for (a_, b_, n) in ((hip, knee, 3), (knee, ank, 3)):
            for k in range(1, n + 1):
                q = lerp(a_, b_, k / (n + 1))
                d = (b_[0] - a_[0], b_[1] - a_[1]); l_ = math.hypot(*d) or 1
                nx, ny = -d[1] / l_ * 3, d[0] / l_ * 3
                p.line([P(q[0] - nx, q[1] - ny), P(q[0] + nx, q[1] + ny)], stripe, only=fem | tib)
    for j in (knee, ank):                                            # Gelenkringe
        p.fill(E(*P(*j), 2.0, 2.0) & (fem | tib | tar), joint)
        p.pxs([P(j[0] - 1, j[1] - 1)], ramp[2])
    p.pxs([P(foot[0] - 1, foot[1])], 'b2')                            # Klaue
    c.stamp(p, 'K')
    # Borsten am Schenkel
    p = C()
    for k in (0.3, 0.6):
        q = lerp(hip, knee, k)
        p.pxs([P(q[0] + 2, q[1] - 2)], ramp[0])
    c.stamp(p, 'K')


def body(c, S, ramps, head_fn, abd_fn):
    """S: dict mit bob, rear (Aufbäumen), gait (0..3), reach (Vorderbeine), mouth"""
    bob, rear, gait = S.get('bob', 0), S.get('rear', 0), S.get('gait', 0)
    LEGR, LEGF, JNT, STR = ramps['leg'], ramps['legf'], ramps['joint'], ramps.get('stripe')
    lifts = [[0, 3, 0, 3], [3, 0, 3, 0]][gait % 2]
    sw = [-2, 2][gait % 2]
    # ---- ferne Beine
    for i in range(4):
        lift = lifts[(i + 1) % 4] if not rear or i > 1 else 8 + i * 2
        reach = (sw if i % 2 else -sw) - (rear * 0.6 if i < 2 else 0)
        hip = (HIPS_F[i][0], HIPS_F[i][1] + bob - (rear if i < 2 else 0))
        leg(c, hip, FEET_F[i], KNEE_H[i] + bob - rear * (2 if i < 2 else 0), LEGF, LEGF[0], STR and LEGF[0], lift, reach)
    # ---- Hinterleib + Stiel
    abd_fn(c, P(84, 36 + bob + rear * 0.3), S)
    # ---- Prosoma
    p = C()
    pro = E(*P(50, 44 + bob - rear * 0.7), 13, 9)
    p.form(pro, ramps['body'], sd=3, hl=1)
    p.line([P(44, 38 + bob - rear * 0.7), P(56, 38 + bob - rear * 0.7)], ramps['body'][0], only=erode(pro, 1))
    c.stamp(p, 'K')
    # ---- nahe Beine
    for i in range(4):
        lift = lifts[i] if not rear or i > 1 else 10 + i * 3
        reach = (-sw if i % 2 else sw) - (rear * 0.8 if i < 2 else 0)
        hip = (HIPS_N[i][0], HIPS_N[i][1] + bob - (rear if i < 2 else 0))
        leg(c, hip, FEET_N[i], KNEE_H[i] + bob - rear * (2 if i < 2 else 0), LEGR, JNT, STR, lift, reach)
    # ---- Kopf
    head_fn(c, P(32, 40 + bob - rear * 1.2), S)
    c.blacken()
    return c
