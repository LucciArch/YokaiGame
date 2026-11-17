"""Hi-Res-Requisiten (doppelte Pixeldichte, passend zu Figuren): rock_hi.png und wall_deco_hi.png je Biom, *_hi.png geteilt.
usage: python3 hi.py"""
import os, sys
import core
core.SS = 2
from core import *
from biomes import ORDER
from props import rocks
import shared
import shared_hi
import objects_hi
import walls
import walldeco_hi

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, '..', '..', '..', 'yokai', 'assets', 'env')


def build():
    for n in ORDER:
        strip(rocks(n), os.path.join(DST, n, 'rock_hi.png'))
        core.SS = 1                                      # Wände selbst gibt es nur in einfacher Dichte
        base = walls.wall_set(n)['h']
        core.SS = 2
        strip(walldeco_hi.wall_decos_hi(n, base), os.path.join(DST, n, 'wall_deco_hi.png'))
    shared_hi.build(os.path.join(DST, '_shared'))
    objects_hi.build(os.path.join(DST, '_shared'))


if __name__ == '__main__':
    build()
    print('ok')
