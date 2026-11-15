"""Pickups: every file is a 2-frame shimmer strip (64x32, frames 32x32)."""
from common import *
from icons_1 import mon
import px
import numpy as np

HEART = r"""
...eeeee......RRRRR...
..eeeeeRR....RRRRRRr..
.eeWWeRRRR..RRRRRRRRr.
eeWWeRRRRRRRRRRRRRRRRr
eeWeRRRRRRRRRRRRRRRRrr
eeeRRRRRRRRRRRRRRRRRrr
eeRRRRRRRRRRRRRRRRRRrr
eRRRRRRRRRRRRRRRRRRrrr
eRRRRRRRRRRRRRRRRRRrrq
.RRRRRRRRRRRRRRRRRrrq.
.RRRRRRRRRRRRRRRRrrrq.
..RRRRRRRRRRRRRRrrrq..
...RRRRRRRRRRRRrrrq...
....RRRRRRRRRRrrrq....
.....RRRRRRRRrrrq.....
......RRRRRRrrrq......
.......RRRRrrrq.......
........RRrrrq........
.........rrqq.........
..........qq..........
"""
SOUL = {'q': 'z', 'r': 'z', 'R': 'a', 'e': 'A', 'W': 'W'}
EMPTY = {'q': 'k', 'r': 'k', 'R': 'h', 'e': 'H', 'W': 'H'}
SPARK = ".W.\nWWW\n.W."


def heart(f=0, tr=None, half=False):
    c = G(HEART, tr=tr)
    if half:
        c.a[:, 16:] = '.'
        edge = c.m & (px.X == 15)
        c.remap({'R': 'r', 'a': 'z'}, only=edge)
    if f:
        c.g(6, 8, "__\n_.", tr=None)
        c.a[8:10, 6:9][c.a[8:10, 6:9] == '.'] = (tr or {}).get('e', 'e')
        c.g(8 if half else 19, 9, SPARK)
    return c


def coin(f=0):
    return mon(8.6, 'ogyY', f)


def coin5(f=0):
    c = mon(11.6, '123W', f)
    return c


def key(f=0):
    c = Cv()
    # tassel (behind)
    c.line([(19, 8), (23, 9), (24, 12)], 'R')
    c.g(22, 12, """
.yy.
.gy.
eRRr
eRRr
eRRr
eRRrr
eRrRr
eRrRr
""")
    ring = E(15.5, 7.5, 6.2, 6.2) & ~E(15.5, 7.5, 2.6, 2.6)
    c.form(ring, '123', 2, 1, ring='K')
    shaft = R(14, 13, 17, 28)
    c.form(shaft, '123', 1, 1, ring='K')
    c.fill(R(13, 13, 18, 15), '2'); c.fill(R(13, 13, 15, 13), '3'); c.fill(R(17, 15, 18, 15), '1')
    for y0 in (20, 25):
        t = R(9, y0, 13, y0 + 3)
        c.form(t, '123', 1, 1)
    c.fill(R(11, 21, 11, 23), '.')
    if f == 0:
        c.g(11, 3, ".WW\nWW.\nW..")
    else:
        c.g(17, 9, SPARK)
    return c


def salt(f=0):
    c = Cv()
    paper = PG([(16, 18), (2, 24), (16, 30), (30, 24)])
    c.form(paper, 'cCs', 2, 1)
    c.line([(3, 24), (16, 19), (29, 24)], 's', only=paper)
    c.line([(6, 25), (16, 29), (26, 25)], 'R', only=paper)
    cone = PG([(16, 5), (7, 23), (25, 23)]) | E(16, 23, 9.0, 3.0) | E(16, 7, 2.2, 2.2)
    c.form(cone, 'vwW', 3, 2, ring='c')
    c.fill(cone & ~sh(cone, -1, -1), 'n')
    c.g(11, 12, "....v...\n........\n.v......\n.....vv.\n........\n..v.....")
    if f:
        c.g(18, 10, SPARK)
    else:
        c.g(13, 16, "W")
    return c


def battery(f=0):
    c = Cv()
    jar = R(9, 13, 22, 26) | E(15.5, 13, 7.0, 3.0) | E(15.5, 26, 7.0, 2.6)
    c.form(jar, 'kza', 2, 1)
    g = 0.8 * f
    c.fill(E(15.5, 20, 4.8 + g, 5.6 + g) & jar, 'a')
    c.fill(E(15.5, 20.5, 3.6 + g, 4.4 + g) & jar, 'A')
    c.fill(E(15.5, 21, 2.0 + g, 2.8 + g), 'W')
    c.fill(PG([(14, 16), (16 - f, 13), (17, 16)]) & jar, 'A')
    c.fill(R(10, 15, 10, 21), 'A'); c.fill(R(10, 15, 10, 16), 'W')
    c.fill(R(11, 9, 20, 11), 'z'); c.fill(R(11, 9, 12, 11), 'a'); c.fill(R(19, 9, 20, 11), 'k')
    lid = R(9, 6, 22, 8)
    c.form(lid, 'dDt', 1, 1, ring='K')
    c.g(14, 3, "WWWw\nWRRw\nWWRw\nWRRw\nWRWw\nWRRw\nWWWw\nwwwv")
    return c


def chest(f=0):
    c = Cv()
    body = R(3, 15, 28, 26)
    c.form(body, 'qrR', 2, 0)
    lid = (E(15.5, 15, 12.9, 8.6) & (px.Y <= 14)) | R(3, 12, 28, 14)
    c.form(lid, 'rRe', 2, 1)
    c.fill(R(3, 14, 28, 14), 'g'); c.fill(R(3, 14, 20, 14), 'y'); c.fill(R(3, 15, 28, 15), 'q')
    for x0 in (6, 23):
        b = R(x0, 0, x0 + 2, 26) & (lid | body)
        c.fill(b, 'g'); c.fill(b & (px.X == x0), 'y'); c.fill(b & (px.X == x0 + 2), 'o'); c.fill(b & (px.Y >= 23), 'o')
    c.fill(R(3, 25, 28, 26), 'k'); c.fill(R(3, 25, 20, 25), 'h')
    c.g(13, 12, """
gyyyyg
yYyyyg
yyKKgo
yyKKgo
ygKKoo
.gooo.
""")
    c.g(9, 8, "EEE") if f == 0 else c.g(17, 10, SPARK)
    return c


def trinket(f=0):
    c = Cv()
    loop = E(15.5, 6.5, 3.6, 4.6) & ~E(15.5, 6.5, 1.8, 2.8)
    c.form(loop, 'rRe', 1, 1)
    c.fill(R(14, 11, 17, 13), 'g'); c.fill(R(14, 11, 15, 11), 'y'); c.fill(R(16, 13, 17, 13), 'o')
    ring = E(15.5, 20, 7.0, 7.0) & ~E(15.5, 20, 2.8, 2.8)
    c.form(ring, 'fGl', 2, 1, ring='K')
    c.fill(ring & ~sh(ring, -1, -1), 'F')
    c.g(14, 27, "eRr\neRr\nRrr")
    if f == 0:
        c.g(10, 15, ".LL\nLL.\nL..")
    else:
        c.g(18, 21, SPARK.replace('W', 'L'))
    return c


def spirit(f=0):
    body = r"""
...zaAAAAAAAAAaz..
..zaAAWWWWWAAAAaz.
.zaAWWWWWWWWAAAaz.
.zAAWWWWWWWWWAAaz.
.zAWWKKWWWKKWWAaz.
.zAWWKKWWWKKWWAaz.
.zAAWWWWWWWWWAAaz.
.zaAAWWWWWWWAAaaz.
..zaAAAWWWAAAAaz..
...zzaAAAAAAaazz..
.....zzaaaaazz....
"""
    t0 = r"""
.............za...
............zaa...
...........zaAa...
..........zaAAz...
.....zaaaaaAAaz...
"""
    t1 = r"""
.........az.......
.........aaz......
.........aAaz.....
.........zAAaz....
.....zaaaaAAAaz...
"""
    c = Cv()
    c.g(7, 7 + f, t1 if f else t0)
    c.g(7, 12 + f, body)
    return c


PICK = dict(heart=heart, half=lambda f=0: heart(f, half=True), soul=lambda f=0: heart(f, tr=SOUL), coin=coin, coin5=coin5,
            key=key, salt=salt, battery=battery, chest=chest, trinket=trinket, spirit=spirit)


def build():
    for n, fn in PICK.items():
        save('pickups', n, [fn(0), fn(1)])


if __name__ == '__main__':
    build()
