"""Nekomata: violetter Geisterkater mit zwei Schwänzen und grün glühenden Augen (Ableitung vom Bakeneko-Gerüst).
Angriff: Sprung mit gespreizten Krallen, Schwänze lodern."""
from common import *
import cat as catlib
import cat_bakeneko_alt as bk  # Gerüst der alten Bakeneko (die neue liegt in enemies_6)

NAME = 'nekomata'
CELL = bk.CELL
ORG = bk.ORG
NEAR = ('u1', 'u2', 'u3')
FAR = ('u0', 'u1', 'u2')
LEG = dict(zip('KmnopYZqWrR', ['K', 'u1', 'u2', 'u3', 'p1', 'g3', 'g4', 'q', 'b3', 'm2', 'm3']))


def second_tail(c, S, B, layer):
    if layer != 'back':
        return
    tail = S['tail']
    pts = [B((x + 5 + i * 2, y + 3 + i)) for i, (x, y) in enumerate(tail)]
    catlib.chain(c, pts, [2.6, 3.2, 2.8, 1.4][:len(pts)], FAR, 'u0')
    # Geisterflämmchen an den Schwanzspitzen
    for (x, y) in (pts[-1], B(tail[-1])):
        flame(c, None, [((x, y), (x - 1, y - 7), 2.2), ((x, y), (x + 2, y - 5), 1.8)], ramp=('u2', 'xu', 'g4'), core='g4', ln='u0')


def draw(**kw):
    S = dict(bk.DEF); S.update(kw)
    return catlib.cat(S, NEAR, FAR, 'u0', LEG, CELL, ORG, fire=second_tail)


if __name__ == '__main__':
    export(NAME, draw, bk.WALK, bk.ATTACK)
