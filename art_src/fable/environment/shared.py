"""Gemeinsame Requisiten: Urne, Steinlaterne, Stacheln, Gruben (Wasser, Lava, Eis, Wolke, Leere)."""
import math
import os
import random
import numpy as np
from core import *
from props import cyl, box, fin, IRON, STRAW


OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_shared')
P = {'f0': '#1e1a24'}
CLAY = ('#2a1418', '#5a2a22', '#8a4a2e', '#c07a48')
STONE = ('#1a1a26', '#3a3a4c', '#5e5e74', '#9a9ab0')
GLOW = ('#8a4a12', '#d8961a', '#ffe24a', '#fffbc0')


def pot(broken=False):
    cv = Cv(32, 32)
    if not broken:
        body = cv.E(16, 19, 9, 9) | cv.R(12, 8, 20, 12)
        cv.form(body, (CLAY[0], CLAY[1], CLAY[2]), 3, 1)
        cv.form(cv.E(16, 9, 5, 2), (CLAY[1], CLAY[2], CLAY[3]), 1, 1)
        cv.hl(13, 19, 9, '#1a0c10')
        cv.hl(9, 23, 16, CLAY[0]); cv.hl(9, 23, 17, CLAY[3])
        cv.px(11, 14, CLAY[3]); cv.px(12, 13, CLAY[3])
    else:
        cv.form(cv.E(16, 24, 9, 4), (CLAY[0], CLAY[1], CLAY[2]), 2, 1)
        for x, y in ((8, 26), (22, 27), (19, 22), (11, 22)):
            cv.form(cv.PG([(x, y), (x + 4, y - 2), (x + 5, y + 1), (x + 1, y + 2)]), (CLAY[0], CLAY[1], CLAY[2]), 1, 1)
        cv.fill(cv.E(16, 23, 6, 2), '#120a0c')
    return fin(cv, P)


def lantern(lit=True):
    cv = Cv(32, 32)
    box(cv, STONE, 11, 25, 21, 29, 2)                     # Sockel
    cv.form(cv.R(14, 17, 18, 25), (STONE[0], STONE[1], STONE[2]), 1, 1)    # Schaft
    box(cv, STONE, 10, 11, 22, 17, 2)                     # Lichtkammer
    cv.rect(13, 13, 19, 16, GLOW[2] if lit else '#0c0a14')
    if lit:
        cv.rect(15, 14, 17, 15, GLOW[3]); cv.hl(13, 19, 16, GLOW[1])
    cv.vl(16, 13, 16, STONE[0])
    cv.fill(cv.PG([(7, 11), (16, 4), (25, 11)]), STONE[1])   # Dach
    cv.fill(cv.PG([(16, 4), (25, 11), (16, 11)]), STONE[0])
    cv.line([(7, 11), (16, 4)], STONE[2])
    cv.rect(15, 2, 17, 4, STONE[2])
    return fin(cv, P)


def spikes(out=True):
    cv = Cv(32, 32)
    cv.fill(cv.R(3, 6, 28, 27), '#14121c'); cv.outline('#0a0814')
    for j in range(3):
        for i in range(3):
            x, y = 6 + i * 9, 9 + j * 8
            cv.fill(cv.E(x + 1, y + 3, 2, 1), '#05040a')
            if out:
                m = cv.PG([(x - 1, y + 4), (x + 1, y - 3), (x + 3, y + 4)])
                cv.fill(m, IRON[2]); cv.line([(x + 1, y - 3), (x + 3, y + 4)], IRON[1]); cv.px(x + 1, y - 3, IRON[3])
    return cv


def pit(kind, f):
    cv = Cv(32, 32, wrap=True)
    rng = random.Random(7 + f)
    if kind == 'water':
        base, a, b = '#0e2240', '#1a3a66', '#4a7ab0'
    elif kind == 'lava':
        base, a, b = '#5a1208', '#c0360e', '#ffb040'
    elif kind == 'ice':
        base, a, b = '#2a4a78', '#4a76a8', '#b0d8f0'
    elif kind == 'cloud':
        base, a, b = '#4a4a78', '#7a7ab0', '#d0d0ec'
    else:
        base, a, b = '#05040a', '#0c0a16', '#1a1828'
    cv.a[:] = hx(base)
    for i in range(7):
        x, y = rng.randrange(32), rng.randrange(32)
        L = rng.randint(3, 7)
        if kind in ('water', 'lava'):
            xo = (x + f * 3) % 32
            cv.hl(xo, xo + L, y, a)
            if kind == 'lava' or i % 3 == 0:
                cv.hl(xo + 1, xo + L - 2, y - 1 if y else 31, b)
        elif kind == 'ice':
            cv.line([(x, y), (x + L, y + L // 2)], a); cv.px(x, y, b)
        elif kind == 'cloud':
            cv.fill(cv.E((x + f * 2) % 32, y, L, L * .6), a); cv.px((x + f * 2) % 32, y - 1, b)
        else:
            if (i + f) % 3 == 0:
                cv.px(x, y, b)
    return cv


def build():
    os.makedirs(OUT, exist_ok=True)
    strip([pot(False), pot(True)], os.path.join(OUT, 'pot.png'))
    strip([lantern(True), lantern(False)], os.path.join(OUT, 'lantern.png'))
    strip([spikes(False), spikes(True)], os.path.join(OUT, 'spikes.png'))
    for k in ('water', 'lava', 'ice', 'cloud', 'void'):
        strip([pit(k, 0), pit(k, 1)], os.path.join(OUT, f'pit_{k}.png'))


if __name__ == '__main__':
    build()
