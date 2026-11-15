"""Item icons A-D: bag beads bell bow box claw cloth cloud coin crane crystal cup dango daruma doll"""
from common import *
import px


def bag():
    return G(r"""
........dDDd..DDd.....
.......dDttDddDtDd....
.......dDDtDDDDDDd....
........dDDDDDDDd.....
........oyyyyyygo.....
.......ogyYyyyggo.....
.......dDDDDDDDdd.....
.....dDDttDDDDDDddj...
....dDttttDDDDDDDddj..
...dDtttDDDDDDDDDDdj..
...dDttDDDDDDDDDDDddj.
..dDDtDDDDRRRDDDDDddj.
..dDDDDDDReeRRDDDDddj.
..dDDDDDDReRRRDDDDddj.
..dDDDDDDRRRRrDDDDddj.
..dDDDDDDDRrrDDDDdddj.
..ddDDDDDDDDDDDDDddjj.
...dDDDDDDDDDDDDdddj..
...ddDDDDDDDDDDddddj..
....dddDDDDDDdddddj...
.....jdddddddddddj....
.......jjjjjjjjj......
""")


def beads():
    c = Cv()
    import math
    n = 12
    for k in range(n):
        if k == 3:
            continue           # bottom: big gold bead
        a = math.radians(k * 360 / n)
        x = int(round(16 + 9.5 * math.cos(a) - 1.5))
        y = int(round(12 + 9.5 * math.sin(a) - 1.5))
        c.g(x, y, ".tD.\ntDDd\nDDdd\n.dj.")
    c.g(13, 19, """
.gyyg.
gyYyyg
gyyygo
gyyggo
.ggoo.
..RR..
.eRRr.
.eRRr.
eRRRrr
eRRrrq
eRrRrq
""")
    return c


def bell():
    c = Cv()
    body = E(16, 17.5, 10.4, 10.4)
    c.form(body, 'ogy', 3, 1)
    c.fill(R(0, 19, 31, 19) & body, 'o')
    c.fill(R(0, 18, 20, 18) & body, 'Y')
    c.fill(R(21, 18, 31, 18) & body, 'g')
    c.fill(R(15, 22, 16, 28) & body, 'K')
    c.fill(E(15.5, 22.5, 2.2, 2.2), 'K')
    c.g(9, 10, "..YY\n.YY.\nYY..\nY...")
    c.fill(R(13, 6, 18, 7), 'g'); c.fill(R(13, 6, 15, 6), 'y'); c.fill(R(17, 7, 18, 7), 'o')
    ring = E(15.5, 3.5, 3.4, 3.0) & ~R(15, 3, 16, 4)
    c.form(ring, 'rRe', 1, 1)
    return c


def bow():
    c = Cv()
    pts = [(21, 2), (17, 4), (13, 8), (10, 13), (9, 18), (10, 22), (13, 26), (18, 29)]
    c.line([(21, 2), (18, 29)], 'v')                         # string
    c.fill(STROKE(pts, 2), 'D')
    c.line(pts[:5], 't')
    c.line([(10, 19), (11, 23), (14, 27), (18, 29)], 'd')
    c.fill(R(20, 1, 22, 2), 'y'); c.fill(R(18, 29, 19, 30), 'g')
    c.fill(R(8, 14, 10, 20), 'R'); c.fill(R(8, 14, 8, 20), 'e'); c.fill(R(10, 15, 10, 20), 'r')
    # arrow
    c.fill(R(4, 17, 27, 17), 't'); c.fill(R(4, 18, 27, 18), 'd')
    c.g(1, 15, "..3\n.33\n332\n221\n.21\n..1")
    c.g(24, 14, ".eRR\neRRr\n....\n....\nRRrr\n.Rrr")
    return c


def box():
    return G(r"""
....HHHHHHHHHHHHHHHHH...
...HHHHHHHHHHHHHHHHHHh..
..HHWWHHHHHHHHHHHHHHhhh.
.HHHHHHHHHHHHHHHHHHhhhhh
yyyyyyyyyyyyyyyyyyyyggoo
hHhhhhhhhhhhhhhhhhhhhkkk
hHhhhhhhhhhhhhhhhhhhkkkk
eeeeeeeRRRRRRRRRRRRRrrrq
RRRRRRRRRRRRRRRRRRrrrrqq
hHhhhhhhhhhhhhhhhhhhhkkk
hHhhhhhhhgyyyghhhhhhhkkk
hHhhhhhhgyYyyyghhhhhhkkk
hHhhhhhhgyyKKyohhhhhhkkk
hhhhhhhhgyyKKoohhhhhkkkk
hhhhhhhhhgyyoohhhhhhkkkk
hhhhhhhhhhhhhhhhhhhkkkkk
yyyyyyyyyyyyyyyyyyggoooo
kkkkkkkkkkkkkkkkkkkkkkkk
""")


def claw():
    c = Cv()
    claws = [
        (L(19, 7, 2.8, 10, 7, 2.2) | L(10, 7, 2.2, 3, 12, 0.6)),
        (L(20, 10, 3.0, 11, 14, 2.4) | L(11, 14, 2.4, 5, 23, 0.6)),
        (L(22, 13, 3.0, 17, 20, 2.4) | L(17, 20, 2.4, 14, 29, 0.6)),
    ]
    for m in claws:
        c.form(m, 'bBi', 1, 1, ring='u')
    base = E(23, 8.5, 5.6, 5.6) | E(26, 12, 3.4, 3.6) | E(20.5, 4.5, 3, 2.6)
    c.form(base, 'khH', 2, 1, ring='K')
    c.g(19, 5, "..HH...\n.H..H..\n.....H.\n....H..")
    return c


def cloth():
    return G(r"""
....eeeeeeeeeyyyeeeeeeeee.
...eeRRRRRRRRyyyRRRRRRRRRr
..eeRRRyRRRRRyygRRRRyRRRRr
.eeRRRyyyRRRRyygRRRyyyRRRr
eeRRRRRyRRRRRyygRRRRyRRRrr
eRRRRRRRRRRRRyggRRRRRRRRrr
rrrrrrrrrrrrrgoorrrrrrrrrq
wWWWWWWWWWWWWyggwwwwwwwwvq
rrrrrrrrrrrrrgoorrrrrrrrqq
RRRRRRRRRRRRRyggRRRRRRRrrq
rrrrrrrrrrrrrgoorrrrrrrrqq
wWWWWWWWWWWWWyggwwwwwwwvvq
qqqqqqqqqqqqqgooqqqqqqqqq.
""")


def cloud():
    c = Cv()
    m = (E(9.5, 17, 6.4, 5.4) | E(16.5, 12.5, 7.4, 7.4) | E(24, 17.5, 5.4, 5.0) | R(5, 17, 27, 22)) & (px.Y <= 22)
    m |= R(2, 21, 9, 22) | R(22, 21, 30, 22)
    c.form(m, 'vwW', 2, 2)
    c.fill(m & (px.Y >= 22), 'v')
    c.g(12, 10, """
..vvvv...
.v....v..
v..vv..v.
v.v..v.v.
v.v.vv.v.
v..v...v.
.v...vv..
..vvv....
""")
    c.g(4, 19, "vvvv"); c.g(21, 18, "vvvvv")
    return c


def mon(r=10.6, ramp='ogyY', f=0):
    """coin with a square hole"""
    c = Cv()
    o, g, y, Yy = ramp
    d = E(15.5, 15.5, r, r)
    c.form(d, o + y + Yy, 2, 1)
    c.fill(d & ~sh(d, 1, 1) & (px.X + px.Y > 30), y)
    inner = E(15.5, 15.5, r - 2.4, r - 2.4)
    c.fill(inner, g)
    c.fill(inner & ~sh(inner, 1, 1), o)                   # rim casts shadow into the field
    hr = 3 if r > 9 else 2
    c.fill(R(15 - hr, 15 - hr, 16 + hr, 16 + hr), y)
    c.fill(R(15 - hr + 1, 16 + hr, 16 + hr, 16 + hr), o); c.fill(R(16 + hr, 15 - hr + 1, 16 + hr, 16 + hr), o)
    c.fill(R(16 - hr, 16 - hr, 15 + hr, 15 + hr), '.')
    if r > 9:                                             # four cast characters
        c.fill(R(15, 8, 16, 9), o); c.fill(R(15, 22, 16, 23), o)
        c.fill(R(8, 15, 9, 16), o); c.fill(R(22, 15, 23, 16), o)
    gx = int(15.5 - r * 0.62)
    if f == 0:
        c.g(gx, gx, ".%s%s\n%s%s.\n%s.." % (Yy, Yy, Yy, Yy, Yy))
    else:
        bx = int(15.5 + r * 0.45)
        c.g(bx - 1, bx - 1, ".W.\nWWW\n.W.")
    return c


def coin():
    return mon()


def crane():
    return G(r"""
..............WW..........
.............WWWw.........
............WWWWwv........
...........WWWWwwv....w...
..WW......WWWWWwwv...Wwv..
.WWWW....WWWWWwwvv..WWwv..
WWRWWw..WWWWWWwwvv.WWwvv..
.w.WWWw.WWWWWwwwvvWWwvv...
....WWWwWWWWwwwwvWWwvvn...
.....WWWWWWwwwwvvWwvvn....
.....wWWWWwwwwvvvvvvn.....
......wWWWwwwvvvvvnn......
.......wwwwwvvvvnnn.......
........wvvvvvnnn.........
.........vvvnnn...........
..........nnn.............
""")


def crystal():
    return G(r"""
..........WA..........
.........WWAa.........
........WWAAaa........
.......WWAAAaaz.......
......WWAAAAaazz......
......WAAAAAaazz......
......WAAAAAaazz......
......WAAAAAaazz.Aa...
..WA..WAAAAAaazzAAaz..
.WWAa.WAAAAAaazAAAazz.
.WAAa.AAAAAAaazAAAazz.
.WAAazAAAAAAaazAAaazz.
.AAAazAAAAAAaazAAaazz.
.AAaazAAAAAaaazAaaazz.
.Aaaazaaaaaaazzaaazzz.
..aazzzaaaaazzzzazzz..
...zzzzzzzzzzzzzzzz...
""")


def cup():
    c = Cv()
    bowl = E(16, 13, 12.4, 10.6) & (px.Y >= 13)
    c.form(bowl, 'rRe', 3, 0)
    c.fill(bowl & (px.X <= 7) & (px.Y <= 18), 'e')
    foot = PG([(12, 23), (20, 23), (21, 26), (11, 26)])
    c.form(foot, 'qrR', 1, 0, ring='q')
    c.fill(E(16, 13, 12.4, 4.2), 'e')
    c.fill(E(16, 13.2, 11.0, 3.2), 'o')
    c.fill(E(16, 13.8, 9.6, 2.5), 'g')
    c.fill(E(16, 14.3, 8.0, 1.8), 'a')
    c.g(10, 14, "AAWWA")
    c.fill(E(16, 13, 12.4, 4.2) & ~E(16, 13.6, 12.0, 3.8) & (px.X < 18), 'E')
    c.g(14, 18, ".y.\nyYy\n.y.")
    return c


def dango():
    c = Cv()
    c.fill(STROKE([(3, 3), (29, 29)], 2), 'D')
    c.line([(3, 3), (29, 29)], 't')
    for (cx, cy, rp, gl) in ((8.5, 8.5, 'mST', 'W'), (15.5, 15.5, 'vwW', 'W'), (22.5, 22.5, 'fGl', 'L')):
        c.form(E(cx, cy, 5.2, 5.2), rp, 2, 1, ring='K')
        c.g(int(cx - 3), int(cy - 3), ".%s%s\n%s%s." % (gl, gl, gl, gl))
    return c


def daruma():
    c = Cv()
    body = E(16, 16.5, 11.4, 12.2) | E(16, 22, 11.8, 6.5)
    c.form(body, 'rRe', 3, 1)
    c.g(8, 6, "..EE\n.EE.\nEE..")
    face = E(15.5, 13, 8.2, 6.6)
    c.form(face, 'bBi', 2, 0, ring='q')
    c.g(9, 8, """
..KKKK...KKKK.
.KKKKKK.KKKKKK
..WWWW...WWWW.
.WWKKW...WWWWb
.WWKKW...WWWWb
..WWW.mm..WWb.
......mm......
..KKKB..BKKK..
...KKK..KKK...
""")
    c.g(11, 21, """
.y.yyyy.y.
yy..yy..yy
y...yy...y
....yy....
...gyyg...
""")
    return c


def doll():
    c = G(r"""
.........CssC.........
........CsssCc........
........CssCCc........
........CsCCCc........
.........RRRr.........
.C.......sCCc.......C.
CsCCCCCCCssCCCCCCCCCcc
ssCCCCCCCsCCCCCCCCCCcc
.cccccccCsCCccccccccc.
........CsCCc.........
........eRRRr.........
........CsCCc.........
.......CssCCCc........
.......CsCCCCc........
......CsCCcCCCc.......
......CsCc..CCc.......
.....CsCCc..CCCc......
.....CsCc....CCc......
.....eRRr....RRr......
.....Cscc....CCc......
....CsCcc...CcCcc.....
""")
    # iron nail through the chest
    c.g(13, 9, "33.....\n.322...\n..K22..\n...K21.\n.....11")
    return c


ICONS = dict(bag=bag, beads=beads, bell=bell, bow=bow, box=box, claw=claw, cloth=cloth, cloud=cloud, coin=coin,
             crane=crane, crystal=crystal, cup=cup, dango=dango, daruma=daruma, doll=doll)


def build():
    for n, f in ICONS.items():
        save('icons', n, f())


if __name__ == '__main__':
    build()
