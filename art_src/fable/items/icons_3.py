"""Item icons M-W: mirror moon omamori rice scroll shell skull staff star sword tail thread wave"""
from common import *
import px, math
import numpy as np


def mirror():
    c = Cv()
    m = E(15.5, 15.5, 10.2, 10.2)
    for k in range(8):
        a = math.radians(45 * k)
        m = m | E(15.5 + 9.0 * math.cos(a), 15.5 + 9.0 * math.sin(a), 3.3, 3.3)
    c.form(m, 'ogy', 2, 1)
    c.fill(E(15.5, 15.5, 8.2, 8.2), 'o')
    face = E(15.5, 15.5, 7.0, 7.0)
    c.form(face, 'aAW', 3, 0)
    c.line([(10, 16), (16, 10)], 'W', only=face); c.line([(10, 17), (17, 10)], 'W', only=face)
    c.line([(13, 20), (20, 13)], 'W', only=face)
    c.g(7, 7, ".Y\nY.")
    return c


def moon():
    c = Cv()
    m = E(14.5, 16, 11.4, 11.4) & ~E(20.5, 13, 9.8, 9.8)
    c.form(m, 'gyY', 2, 1)
    c.fill(m & ~sh(m, -1, -1) & (px.Y > 18), 'o')
    c.g(22, 6, "..Y..\n.YYY.\nYYWYY\n.YYY.\n..Y..")
    return c


def omamori():
    return G(r"""
......wWWw......
.....wW..Wv.....
.....wW..wv.....
......wWwv......
....pPPWvPPp....
...pPPPwvPPPpx..
..pPXPPPPPPPPpx.
..PXPwWWWWwPPpx.
..PPPWWWWWvPPpx.
..PPyWRRRWvyPpx.
..PPPWWRWWvPPpx.
..PPPWRRRWvPPpx.
..PyPWWWRWvPypx.
..PPPWRRRWvPPpx.
..PPPWWRWWvPPpx.
..PPyWRRRWvyPpx.
..PPPWWWWWvPPpx.
..PPPwvvvvvPppx.
..PyPPPPPPPPypx.
..pPPPPPPPPpppx.
..pppppppppppxx.
...xxxxxxxxxxx..
""")


def rice():
    c = Cv()
    m = L(16, 8, 4.6, 8, 22, 5) | L(8, 22, 5, 24, 22, 5) | L(24, 22, 5, 16, 8, 4.6) | PG([(16, 8), (8, 22), (24, 22)])
    c.form(m, 'vwW', 3, 1)
    c.fill(m & ~sh(m, 1, 1) & ~sh(m, 2, 2), 'W')
    c.g(13, 7, "WW.\nW..")
    c.g(8, 11, """
.........vv.....
................
......vv........
..............v.
...vv.........v.
................
.v..............
.v..............
""")
    nori = R(11, 17, 21, 27) & m
    c.fill(nori, 'h'); c.fill(nori & (px.X <= 12), 'H'); c.fill(nori & (px.Y <= 17), 'H')
    c.fill(nori & ((px.X >= 20) | (px.Y >= 26)), 'k')
    return c


def scroll():
    c = Cv()
    for x0 in (2, 26):
        c.fill(R(x0, 12, x0 + 3, 19), 'D'); c.fill(R(x0, 12, x0 + 3, 13), 't'); c.fill(R(x0, 18, x0 + 3, 19), 'd')
    c.fill(R(2, 11, 3, 20), 'g'); c.fill(R(2, 11, 3, 13), 'y'); c.fill(R(2, 19, 3, 20), 'o')
    c.fill(R(28, 11, 29, 20), 'g'); c.fill(R(28, 11, 29, 13), 'y'); c.fill(R(28, 19, 29, 20), 'o')
    body = R(6, 9, 25, 22)
    c.form(body, 'cCs', 3, 2, sdir=(0, 1), hdir=(0, 1), ring='K')
    c.fill(R(6, 9, 25, 9), 'C')
    for x0 in (6, 23):
        b = R(x0, 9, x0 + 2, 22)
        c.fill(b, 'p'); c.fill(b & (px.Y <= 12), 'P'); c.fill(b & (px.Y >= 20), 'x')
    cord = R(14, 9, 17, 22)
    c.fill(cord, 'R'); c.fill(cord & (px.Y <= 12), 'e'); c.fill(cord & (px.Y >= 20), 'r')
    c.g(12, 14, """
ee....RR
eRR..RRr
.RRyyRr.
eRRyoRRr
RR....rr
""")
    c.g(14, 23, "WWWw\nWRRw\nWWRw\nWRRw\nwwwv")
    return c


def shell():
    c = Cv()
    cx, cy = 15.5, 27.0
    ang = np.degrees(np.arctan2(cy - px.Y, px.X - cx))
    rr = np.hypot(px.X - cx, px.Y - cy)
    m = (E(15.5, 14.5, 12.6, 10.8) & (ang >= 36) & (ang <= 144)) | R(11, 24, 20, 27)
    c.form(m, 'bBi', 3, 1)
    c.fill(m & (rr >= 9.5) & (rr <= 12.5) & (px.Y < 24), 'T')
    c.fill(m & (rr >= 12.5) & (rr <= 14.5) & (px.Y < 24), 'S')
    for a in (54, 68, 82, 98, 112, 126):
        x, y = cx + 24 * math.cos(math.radians(a)), cy - 24 * math.sin(math.radians(a))
        c.line([(cx, cy - 3), (x, y)], 'b' if a < 90 else 'u', only=m & (px.Y < 24))
    c.fill(m & ~sh(m, -2, -2) & (px.Y < 24), 'b')
    c.fill(m & ~sh(m, -1, -1), 'u')
    c.fill(R(11, 24, 20, 24) & m, 'b'); c.fill(R(11, 25, 13, 25), 'i')
    return c


def skull():
    return G(r"""
.....iiiiiiiii......
...iiiBBBBBBBBBb....
..iiBBBBBBBBBBBBbb..
.iiBBBBBBBBBBBBBBbb.
.iBBBBBBBBBBBBBBBbbu
iiBBBBBBBBBBBBBBBbbu
iBBBBBBBBBBBBBBBBbbu
iBBKKKKKBBBKKKKKBbbu
iBKKKKKKBBBKKKKKKbbu
iBKKMMKKBBBKKMMKKbbu
iBKKMYKKBBBKKMYKKbuu
.BBKKKKBBKBBKKKKbbu.
.iBBBBBBKKKBBBBbbuu.
..bBBBBBKKKBBBbbbu..
...BBBBBBBBBBBbbu...
...BiBBiBBiBBibbu...
...BiKBiKBiKBibu....
...uBKuBKuBKubuu....
....bbbbbbbbbuu.....
""")


def staff():
    c = Cv()
    c.fill(STROKE([(12, 12), (28, 29)], 2), 'D'); c.line([(12, 12), (28, 29)], 't')
    c.fill(STROKE([(26, 27), (29, 30)], 2), 'g')
    for (x, y) in ((3.5, 14.5), (14.5, 3.5), (2.5, 9.5), (9.5, 2.5)):
        rg = E(x, y, 2.6, 2.6) & ~E(x, y, 1.0, 1.0)
        c.form(rg, 'ogy', 1, 0)
    ring = E(8.5, 8.5, 6.4, 6.4) & ~E(8.5, 8.5, 3.6, 3.6)
    c.form(ring, 'ogy', 2, 1, ring='K')
    c.g(4, 4, ".YY\nYY.\nY..")
    c.fill(R(8, 8, 9, 9), 'y'); c.fill(R(8, 5, 9, 12), 'g'); c.fill(R(8, 5, 8, 12), 'y')
    c.fill(STROKE([(11, 11), (14, 14)], 3), 'g'); c.line([(11, 11), (14, 14)], 'y')
    return c


def star():
    c = Cv()
    cx, cy, Ro, Ri = 15.5, 16.5, 12.6, 5.4
    tips = [(cx + Ro * math.cos(math.radians(-90 + 72 * k)), cy + Ro * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
    inn = [(cx + Ri * math.cos(math.radians(-54 + 72 * k)), cy + Ri * math.sin(math.radians(-54 + 72 * k))) for k in range(5)]
    for k in range(5):
        for v, sgn in ((inn[k], 1), (inn[k - 1], -1)):
            gx, gy = (cx + tips[k][0] + v[0]) / 3, (cy + tips[k][1] + v[1]) / 3
            mx, my = (cx + tips[k][0]) / 2, (cy + tips[k][1]) / 2
            d = -((gx - mx) + (gy - my))
            ch = 'y' if d > 0.4 else ('g' if d > -0.9 else 'o')
            c.fill(PG([(cx, cy), tips[k], v]), ch)
    c.g(13, 6, ".Y\nYY\nY.")
    c.g(6, 12, "YYY")
    return c


def sword():
    c = Cv()
    blade = PG([(2, 2), (6, 3), (21, 18), (18, 21), (3, 6)])
    d = px.X - px.Y
    c.fill(blade, '2')
    c.fill(blade & (d >= 1), '3'); c.fill(blade & (d == 0), 'W'); c.fill(blade & (d <= -2), '1')
    c.fill(blade & (d >= 3), 'W')
    hd = STROKE([(22, 22), (28, 28)], 3)
    c.fill(hd, 'h'); c.fill(hd & (px.X - px.Y >= 1), 'H'); c.fill(hd & (px.X - px.Y <= -1), 'k')
    c.g(23, 23, "R.....\n.R....\n..R...\n...R..\n....R.")
    c.fill(R(28, 28, 30, 30), 'g'); c.fill(R(28, 28, 29, 28), 'y'); c.fill(R(30, 29, 30, 30), 'o')
    guard = REL(20.5, 20.5, 5.4, 2.1, -45)
    c.form(guard, 'ogy', 1, 1, ring='K')
    return c


def tail():
    c = Cv()
    pts = [(25, 28, 2.0), (22, 25, 3.6), (19, 21, 5.2), (16, 16.5, 6.2), (13.5, 11.5, 5.6), (12.5, 7.5, 4.2), (13.5, 4, 2.6), (15.5, 2, 1.2)]
    m = np.zeros((32, 32), bool)
    for (x0, y0, r0), (x1, y1, r1) in zip(pts, pts[1:]):
        m |= L(x0, y0, r0, x1, y1, r1)
    c.form(m, '789', 3, 1)
    c.g(13, 14, "9......\n99.....\n.9.....\n...7...\n...77..\n....7..\n.......\n......7\n......7")
    tip = m & (px.Y < 9 + ((px.X % 4) < 2) * 2)
    c.remap({'7': 'v', '8': 'w', '9': 'W'}, only=tip)
    c.fill(tip & ~sh(m, 1, 1), 'W')
    return c


def thread():
    c = Cv()
    c.fill(STROKE([(21, 19), (25, 21), (27, 25), (25, 29), (22, 30)], 2), 'R')
    c.line([(21, 19), (25, 21), (27, 25)], 'e')
    body = R(10, 8, 21, 23)
    c.form(body, 'rRe', 3, 2, sdir=(1, 0), hdir=(1, 0))
    for y in (10, 13, 16, 19, 22):
        c.remap({'R': 'r', 'e': 'R', 'r': 'q'}, only=(px.Y == y) & body)
    for y in (9, 12, 15, 18, 21):
        c.fill(R(12, y, 13, y), 'E')
    for y0 in (4, 24):
        fl = R(7, y0, 24, y0 + 3)
        c.form(fl, 'dDt', 2, 1, ring='K')
    c.fill(R(13, 4, 18, 4), 'j'); c.fill(R(14, 5, 17, 5), 'j')
    return c


def wave():
    return G(r"""
........wWWWWw............
......wWWWWWWWWw..........
....wWWWAAAAAWWWWw........
...wWWAAaaaaaAAWWWw.......
..wWWAaazzzzzaaAAWWw......
..WWAaz.....zzaaAAWWw.....
.wWAaz........zaaAAWw.....
.WWAz..........zaAAWWw....
.WWaz.WW.......zaaAAWw....
.wWz..WWw.......zaAAWWw...
..w....w........zaaAAWw...
................zaaAAAWw..
...............zzaaAAAWWw.
..............zzaaaAAAAWWw
............zzzaaaaAAAAAWW
.........zzzzaaaaaaAAAAAAW
.....zzzzzaaaaaaaaaAAAAAAA
.zzzzzzaaaaaaaaaaaaaaAAAAA
zzzzzzzzzzzaaaaaaaaaaaaaaa
""")


ICONS = dict(mirror=mirror, moon=moon, omamori=omamori, rice=rice, scroll=scroll, shell=shell, skull=skull,
             staff=staff, star=star, sword=sword, tail=tail, thread=thread, wave=wave)


def build():
    for n, f in ICONS.items():
        save('icons', n, f())


if __name__ == '__main__':
    build()
