"""Item icons D-M: drum eye fan fang feather fish flame flower gourd hammer hat lantern leaf magatama mask"""
from common import *
import px, math
import numpy as np


def drum():
    c = Cv()
    rim = E(15.5, 15.5, 11.4, 11.4)
    c.form(rim, 'dDt', 2, 1)
    head = E(15.5, 15.5, 8.6, 8.6)
    c.form(head, 'bBi', 2, 0, ring='j')
    c.fill(head & ~sh(head, 1, 1), 'b')
    # mitsudomoe
    for k in range(3):
        a0 = math.radians(-90 + 120 * k)
        c.fill(E(15.5 + 3.4 * math.cos(a0), 15.5 + 3.4 * math.sin(a0), 2.3, 2.3), 'R')
        for j in range(1, 9):
            a = a0 - math.radians(j * 11)
            rr = 2.0 - j * 0.2
            c.fill(E(15.5 + (3.6 + j * 0.28) * math.cos(a), 15.5 + (3.6 + j * 0.28) * math.sin(a), rr, rr), 'R')
    for k in range(8):                                   # gold studs
        a = math.radians(22.5 + 45 * k)
        x, y = int(15.5 + 10 * math.cos(a)), int(15.5 + 10 * math.sin(a))
        c.fill(R(x, y, x + 1, y + 1), 'y' if k in (3, 4, 5, 6) else 'g')
    return c


def eye():
    c = Cv()
    ball = E(15.5, 15.5, 10.6, 10.6)
    c.form(ball, 'vwW', 3, 1)
    c.line([(26, 12), (22, 13), (20, 12)], 'R', only=ball)
    c.line([(26, 19), (23, 18), (21, 20)], 'R', only=ball)
    c.line([(19, 25), (19, 22)], 'R', only=ball)
    c.fill(E(12.5, 15.5, 6.2, 6.6), 'o')
    c.fill(E(12.5, 15.5, 5.2, 5.6), 'g')
    c.fill(E(12.0, 15.0, 4.0, 4.4), 'y')
    c.fill(E(12.5, 15.5, 1.5, 4.6), 'K')
    c.g(9, 11, "WW\nWW")
    return c


def fan():
    c = Cv()
    cx, cy = 15.5, 27.0
    ang = np.degrees(np.arctan2(cy - px.Y, px.X - cx))
    rr = np.hypot(px.X - cx, px.Y - cy)
    sect = (ang >= 30) & (ang <= 150)
    paper = sect & (rr <= 16.4) & (rr >= 7.0)
    seg = ((150 - ang) // 15).astype(int)
    c.fill(paper, 'W')
    c.fill(paper & (seg % 2 == 1), 'w')
    c.fill(paper & (seg >= 6), 'w'); c.fill(paper & (seg >= 7), 'v')
    sun = E(15.5, 14.5, 4.2, 4.2) & paper
    c.fill(sun, 'R'); c.fill(sun & (seg % 2 == 1), 'r'); c.fill(sun & ~sh(sun, 1, 1), 'e')
    c.fill(paper & (rr >= 15.2), 'y'); c.fill(paper & (rr >= 15.2) & (seg % 2 == 1), 'g')
    c.fill(paper & (rr >= 15.2) & (seg >= 6), 'o')
    sticks = sect & (rr < 7.0)
    c.fill(sticks, 'D'); c.fill(sticks & (seg % 2 == 1), 'd'); c.fill(sticks & (seg == 0), 't')
    c.fill(E(15.5, 27, 1.5, 1.5), 'y')
    return c


def fang():
    return G(r"""
..qrRRRRRRRRRRrq..
.rReeeRRRRRRRRRrq.
.rRRRRRRRRRRRRrrq.
..rriBBBBBBbbrrq..
...iiBBBBBBbbbu...
...iiBBBBBBbbbu...
...iBBBBBBBbbbu...
....iBBBBBBbbuu...
....iBBBBBbbbu....
....iBBBBBbbbu....
.....iBBBBbbuu....
.....iBBBBbbu.....
.....iBBBbbbu.....
......iBBbbuu.....
......iBBbbu......
......iBBbbu......
.......iBbbu......
.......iBbu.......
.......iBbu.......
........Bu........
........eR........
.......eRRr.......
.......RRRr.......
........Rr........
""")


def feather():
    c = Cv()
    vane = REL(17.5, 13.5, 13.5, 5.6, -45) | REL(21, 10, 8, 5.2, -45)
    vane &= ~PG([(17, 24), (20, 19), (22, 21)]) & ~PG([(6, 13), (11, 12), (10, 10)])
    c.form(vane, 'khH', 3, 2)
    for k in range(6):                                   # barbs
        x, y = 9 + k * 3, 21 - k * 3
        c.line([(x, y), (x + 3, y + 3)], 'k', only=vane)
        c.line([(x, y), (x - 3, y - 2)], 'h', only=vane)
    c.line([(3, 28), (26, 5)], 'B')
    c.line([(3, 28), (8, 23)], 'i'); c.fill(R(2, 28, 3, 29), 'B')
    c.g(20, 4, "..pP\n.pP.\npP..")
    return c


def fish():
    c = Cv()
    tail = PG([(21, 16), (29, 7), (27, 16), (29, 25)])
    c.form(tail, 'qrR', 1, 1)
    c.line([(23, 16), (28, 9)], 'e'); c.line([(23, 17), (28, 23)], 'q')
    dors = PG([(8, 10), (13, 5), (20, 7), (21, 11)])
    c.form(dors, 'qrR', 1, 1)
    vent = PG([(13, 21), (17, 26), (19, 21)])
    c.form(vent, 'qrR', 1, 0)
    body = E(13, 16, 10.4, 7.2)
    c.form(body, 'rRe', 2, 1, ring='q')
    belly = body & (px.Y >= 19)
    c.fill(belly, 'S'); c.fill(body & (px.Y >= 21), 'm'); c.fill(belly & (px.Y == 19) & (px.X < 17), 'T')
    c.line([(11, 12), (10, 15), (11, 19)], 'r', only=body)
    c.g(13, 15, "ree\n.rr")                             # pectoral fin
    c.g(15, 12, "E.E.E\n.E.E.")
    c.fill(E(7, 14.5, 2.2, 2.2), 'y'); c.fill(R(6, 14, 7, 15), 'K')
    c.g(3, 17, "qq")
    return c


def flame():
    return G(r"""
..............za....
.............zaa....
............zaAa....
...........zaAa.....
...........zaAAa....
..........zaAAAa....
.........zaAAAAaz...
........zaAAAAAaz...
.......zaAAAWAAAaz..
......zaAAAWWWAAaz..
.....zaAAAWWWWAAAaz.
....zaAAAWWWWWWAAaz.
....zaAAWWWWWWWAAaz.
...zaAAAWWWWWWWWAAaz
...zaAAWWWWWWWWWAAaz
...zaAAWWWWWWWWWAAaz
...zaAAAWWWWWWWAAaaz
....zaAAAWWWWWAAAaz.
....zzaAAAAAAAAAaaz.
.....zzaaAAAAAaazz..
.......zzaaaaazz....
""")


def flower():
    c = Cv()
    for k in (2, 3, 1, 4, 0):
        a = math.radians(-90 + 72 * k)
        pm = REL(15.5 + 7.2 * math.cos(a), 15.5 + 7.2 * math.sin(a), 5.6, 4.4, math.degrees(a))
        c.form(pm, 'mST', 1, 1, ring='m')
        tx, ty = 15.5 + 12.6 * math.cos(a), 15.5 + 12.6 * math.sin(a)
        c.fill(E(tx, ty, 1.1, 1.1), '.')                 # petal notch
    c.fill(E(15.5, 15.5, 2.6, 2.6), 'R')
    c.fill(E(15.5, 15.5, 1.2, 1.2), 'y')
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        x, y = 15.5 + 5.0 * math.cos(a), 15.5 + 5.0 * math.sin(a)
        c.line([(15.5 + 3 * math.cos(a), 15.5 + 3 * math.sin(a)), (x, y)], 'R')
    return c


def gourd():
    c = Cv()
    c.fill(R(15, 2, 17, 6), 'd'); c.fill(R(15, 2, 15, 5), 'D'); c.fill(R(14, 2, 18, 3), 'j'); c.fill(R(14, 2, 16, 2), 'd')
    m = E(16, 21, 8.6, 7.8) | E(16, 10.5, 5.8, 5.4) | R(14, 13, 18, 17)
    c.form(m, 'Dts', 3, 1, ring='j')
    c.fill(m & ~sh(m, -1, -1), 'd')
    c.g(11, 7, ".ii\nii.\ni..")
    c.g(9, 17, ".ii\nii.\ni..\ni..")
    c.fill(R(12, 14, 20, 16) & m, 'R'); c.fill(R(12, 14, 17, 14) & m, 'e'); c.fill(R(18, 16, 20, 16) & m, 'r')
    c.g(19, 15, """
RRr.
.yy.
.RRr
.eRr
eRRr
eRrr
""")
    return c


def hammer():
    c = Cv()
    hd = R(6, 5, 25, 17) | E(6, 11, 2.6, 6.4) | E(25, 11, 2.6, 6.4)
    handle = R(14, 17, 17, 27)
    c.form(handle, 'dDt', 1, 1)
    c.fill(R(13, 27, 18, 29), 'g'); c.fill(R(13, 27, 15, 27), 'y'); c.fill(R(17, 28, 18, 29), 'o')
    c.form(hd, 'dDt', 3, 1, ring='j')
    c.fill(R(6, 5, 25, 6) & hd, 't')
    for x0 in (6, 22):
        b = R(x0, 4, x0 + 3, 18) & hd
        c.fill(b, 'g'); c.fill(b & (px.Y <= 8), 'y'); c.fill(b & (px.Y >= 15), 'o'); c.fill(b & (px.Y <= 5), 'Y')
    c.fill(E(15.5, 11, 3.6, 3.6), 'o'); c.fill(E(15.5, 11, 2.6, 2.6), 'y')
    c.fill(R(15, 10, 16, 12), 'R'); c.g(14, 9, "Y")
    return c


def hat():
    c = Cv()
    # chin cord first (behind)
    c.fill(STROKE([(8, 22), (12, 27), (16, 29), (20, 27), (24, 22)], 2), 'R')
    c.line([(8, 22), (12, 27), (16, 28)], 'e')
    cone = PG([(16, 5), (2, 20), (30, 20)]) | E(16, 20.5, 14.2, 3.4)
    c.form(cone, 'cCs', 3, 1, ring='K')
    c.fill(cone & (px.Y >= 22), 'c')
    c.fill(cone & (px.Y >= 23), 'd')
    for xb in (5, 10, 21, 26):
        c.line([(16, 6), (xb, 21)], 'c', only=cone)
    c.line([(16, 6), (15, 21)], 'c', only=cone)
    c.fill(R(15, 4, 17, 6), 'D'); c.fill(R(15, 4, 15, 5), 't')
    return c


def lantern():
    c = Cv()
    c.fill(E(16, 5, 4.6, 4.4) & ~E(16, 5, 3.4, 3.2) & (px.Y <= 5), 'g')
    body = E(15.5, 16.5, 9.4, 9.8)
    c.form(body, 'rRe', 3, 1)
    c.fill(E(14.5, 16, 5.2, 6.2), 'M')
    c.fill(E(14.5, 16, 3.2, 4.4), 'y')
    c.fill(E(14.5, 16, 1.5, 2.6), 'Y')
    for y in (10, 13, 16, 19, 22):
        c.remap({'R': 'r', 'e': 'R', 'M': 'N', 'y': 'g', 'Y': 'y', 'r': 'q'}, only=(px.Y == y) & body)
    for y0 in (5, 26):
        c.fill(R(11, y0, 20, y0 + 2), 'h'); c.fill(R(11, y0, 17, y0), 'H'); c.fill(R(18, y0 + 2, 20, y0 + 2), 'k')
        c.fill(R(19, y0, 20, y0 + 1), 'k')
    c.fill(R(15, 29, 16, 30), 'y')
    return c


def leaf():
    c = Cv()
    c.fill(STROKE([(7, 25), (3, 29)], 2), 'D'); c.line([(6, 25), (2, 29)], 't')
    m = E(24, 23.5, 17.8, 17.8) & E(8, 7.5, 17.8, 17.8)
    c.form(m, 'fGl', 3, 1)
    c.line([(6, 26), (26, 5)], 'L', only=m)
    for k in range(4):
        x, y = 10 + k * 4, 21 - k * 4
        c.line([(x, y), (x + 1, y - 6)], 'l', only=m)
        c.line([(x + 1, y), (x + 7, y + 1)], 'f', only=m)
    return c


def magatama():
    c = Cv()
    pts = [(13, 11, 7.6), (18.5, 15, 6.2), (21, 20, 4.8), (19.5, 25, 3.4), (16, 28, 2.2), (12.5, 28.5, 1.2)]
    m = np.zeros((32, 32), bool)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        m |= L(x0, y0, r0, x1, y1, r1)
    m &= ~E(11.5, 21.5, 5.0, 5.2)
    c.form(m, 'fGl', 3, 1)
    c.fill(m & ~sh(m, -1, -1), 'F')
    c.fill(E(12.5, 10.5, 2.3, 2.3), 'K')
    c.g(10, 8, "f..\n...")
    c.g(7, 6, "..LL\n.LL.\nLL..\nL...")
    c.g(22, 17, "l\nl\nl")
    return c


def mask():
    return G(r"""
.WW................ww.
WWWw..............wWWv
WRRWw............wWRRv
WRRRWw..........wWRRRv
WWRRWWwwwwwwwwwwWWRRWv
.WWWWWWWWWRRWWWWWWWWv.
.WWWWWWWWWRRWWWWWWWwv.
.WWWWWWWWWRRWWWWWWwvv.
.WWKKKWWWWWWWWWWKKKvv.
.WWRKKKKWWWWWWKKKKRvn.
.WWRRyYKKWWWWKKyYRRvn.
..WWRRRKWWWWWWKRRRvv..
..WWWWWWWWWWWWWWwwvn..
..WRRWWWWWWWWWWwRRvn..
...WWRRWWWWWWWwRRvn...
...WWWWWWWWWWwwwvvn...
....WWWWWWWWwwwvvn....
....WWWWWKKKKwwvn.....
.....WWWWKKKKwvvn.....
.....WWRRRKKRRRvn.....
......WWRRRRRRvn......
.......WWwwwvvn.......
........wwvvnn........
""")


ICONS = dict(drum=drum, eye=eye, fan=fan, fang=fang, feather=feather, fish=fish, flame=flame, flower=flower,
             gourd=gourd, hammer=hammer, hat=hat, lantern=lantern, leaf=leaf, magatama=magatama, mask=mask)


def build():
    for n, f in ICONS.items():
        save('icons', n, f())


if __name__ == '__main__':
    build()
