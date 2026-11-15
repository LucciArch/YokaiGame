"""Hi-Res-Requisiten (doppelte Pixeldichte, passend zu Figuren): rock_hi.png je Biom, *_hi.png geteilt.
usage: python3 hi.py"""
import os, sys
import core
core.SS = 2
from core import *
from biomes import ORDER
from props import rocks
import shared
import shared_hi

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, '..', '..', '..', 'yokai', 'assets', 'env')


def build():
    for n in ORDER:
        strip(rocks(n), os.path.join(DST, n, 'rock_hi.png'))
    shared_hi.build(os.path.join(DST, '_shared'))
    strip([shared.spikes(False), shared.spikes(True)], os.path.join(DST, '_shared', 'spikes_hi.png'))


if __name__ == '__main__':
    build()
    print('ok')
