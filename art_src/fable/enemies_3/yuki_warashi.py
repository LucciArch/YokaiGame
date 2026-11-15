"""Yuki-warashi: pale snow child in a straw mino cloak and a snow-laden hat; throws snowballs."""
from kit import *
import px

NAME = 'yuki_warashi'
CW, CH = 92, 76
OX, OY = 40, 14            # local baseline y=58
STRAW = ('s2', 's3', 'c2')
STRAWD = ('s1', 's2', 's3')

LEG = dict(zip('hHK123Aaq0', ['h0', 'h2', 'K', 'u1', 'u2', 'u3', 'a2', 'a1', 'a0', 'u0']))
FACE = """
.hhhhhhhhhhhh.
hhHhhhHhhhhhhh
h3h33h33h2hhhh
h3333332222hhh
KKKK3KKKKK21hh
3KAK32KAAK21hh
3KKK32KKKK21hh
333332222211hh
.33qq3222111h.
..3322221110..
...22221110...
"""

DEF = dict(bob=0, lean=0, ffoot=14, nfoot=23, flift=0, nlift=0, sway=0,
           sh=(13, 33), hand=(5, 39), ball=(2, 38), ballr=3.2, trail=0, breath=0)


def P(x, y):
    return (x + OX, y + OY)


def tier(p, xl, xr, y0, y1, ramp, ph=0, sway=0):
    """one layer of straw: flat top, ragged fringe at the bottom"""
    pts = [(xl + 3, y0), (xr - 3, y0), (xr, y0 + 3)]
    x = xr + sway
    k = ph
    while x > xl + sway:
        pts.append((x, y1 + (2 if k % 2 else -1)))
        x -= 2.5
        k += 1
    pts.append((xl + sway, y1))
    pts.append((xl, y0 + 3))
    m = PG(pts)
    p.form(m, ramp, sd=3, hl=1)
    for i, xx in enumerate(range(int(xl) + 2, int(xr), 3)):
        p.line([(xx, y0 + 2), (xx + sway * 0.6 - (1 if i % 2 else 0), y1 - 1)], ramp[0] if xx > (xl + xr) / 2 else 's2', only=erode(m))
    return m


def warashi(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(x, y):
        return P(x + lean, y + bob)

    # ---- legs: pale shins in straw snow boots
    for fx, lift, ramp, bramp in ((S['ffoot'], S['flift'], ('u0', 'u1', 'u2'), STRAWD), (S['nfoot'], S['nlift'], PALE, STRAW)):
        p = C()
        x0, y0 = P(fx, 58 - lift)
        p.form(L(x0 + 4, y0 - 12, 2.4, x0 + 4, y0 - 5, 2.2), ramp, sd=1, hl=0)
        boot = PG([(x0 + 1, y0 - 7), (x0 + 7, y0 - 7), (x0 + 7, y0), (x0 - 2, y0), (x0 - 3, y0 - 2), (x0 + 1, y0 - 4)])
        p.form(boot, bramp, sd=2, hl=1)
        p.line([(x0 + 1, y0 - 5), (x0 + 7, y0 - 5)], 's1', only=boot)
        p.line([(x0 - 1, y0 - 2), (x0 + 6, y0 - 2)], 's1', only=boot)
        c.stamp(p, 'K')

    # ---- mino: three ragged tiers of straw, lowest first
    sw = S['sway']
    p = C(); tier(p, B(5, 0)[0], B(35, 0)[0], B(0, 40)[1], B(0, 51)[1], STRAWD, 0, sw); c.stamp(p, 'K')
    p = C(); tier(p, B(7, 0)[0], B(33, 0)[0], B(0, 33)[1], B(0, 43)[1], STRAW, 1, sw * 0.5); c.stamp(p, 's0')
    p = C(); m = tier(p, B(10, 0)[0], B(30, 0)[0], B(0, 27)[1], B(0, 36)[1], STRAW, 0, 0)
    # snow resting on the shoulders
    sn = m & ~sh(m, 0, 2) & (px.X > B(19, 0)[0])
    p.fill(sn, 'v3'); p.fill(sn & ~sh(sn, 0, 1) & sh(sn, 0, -1), 'v2')
    c.stamp(p, 's0')

    # ---- head
    hx, hy = B(8, 16)
    p = C()
    p.form(E(hx + 8, hy + 5, 7.6, 6.4), HAIR, sd=2, hl=0)      # bob of black hair behind the face
    p.grid(hx, hy, FACE, LEG)
    c.stamp(p, 'K')

    # ---- snow hat: straw cone under a heavy cap of snow
    p = C()
    ap, bl, br = B(19, 2), B(1, 16), B(37, 17)
    under = PG([bl, br, (br[0] - 6, br[1] + 1), (bl[0] + 6, bl[1] + 1)])
    p.fill(under, 's1')
    cone = PG([ap, (ap[0] - 9, ap[1] + 6), bl, (bl[0] + 8, bl[1] + 1), (br[0] - 8, br[1]), br, (ap[0] + 9, ap[1] + 6)])
    p.form(cone, STRAW, sd=3, hl=0)
    snow = PG([(ap[0], ap[1] - 2), (ap[0] - 6, ap[1] + 1), (ap[0] - 12, ap[1] + 6), (bl[0] + 1, bl[1] - 4), (bl[0] + 4, bl[1] - 1), (bl[0] + 9, bl[1] - 3),
               (bl[0] + 13, bl[1] - 1), (ap[0] + 2, ap[1] + 11), (ap[0] + 6, ap[1] + 9), (ap[0] + 10, ap[1] + 12), (br[0] - 3, br[1] - 4),
               (ap[0] + 10, ap[1] + 4), (ap[0] + 5, ap[1])])
    p.form(snow, WH, sd=3, hl=1)
    for xx in range(bl[0] + 3, br[0] - 2, 4):
        p.line([(xx, bl[1] - 1), (xx + (ap[0] - xx) * 0.25, bl[1] - 5)], 's2', only=cone & ~snow)
    c.stamp(p, 'K')

    # ---- near arm + snowball
    shd, hd = B(*S['sh']), B(*S['hand'])
    if S['ballr'] and not S['trail']:
        p = C()
        bx, by_ = B(*S['ball'])
        p.form(E(bx, by_, S['ballr'], S['ballr']), WH, sd=2, hl=1)
        c.stamp(p, 'K')
    p = C()
    el = ik(shd, hd, 5.5, 5.5, side=1)
    p.form(chain([shd, el, hd], 2.3, 1.9), PALE, sd=1, hl=0)
    p.form(E(hd[0], hd[1], 2.5, 2.3), PALE, sd=1, hl=1)
    c.stamp(p, 'u0')
    c.blacken()

    # ---- thrown snowball / frost (own cold outline)
    if S['trail']:
        bx, by_ = P(*S['ball'])
        p = C()
        p.fill(chain([(bx + 4, by_ - 1), (bx + 16, by_ - 3)], 2.0, 0.6), 'a1')
        p.fill(chain([(bx + 4, by_ + 2), (bx + 12, by_ + 3)], 1.4, 0.6), 'a0')
        p.fill(chain([(bx + 3, by_), (bx + 10, by_ - 1)], 1.2, 0.6), 'a2')
        c.stamp(p, ring=False)
        p = C()
        p.form(E(bx, by_, S['ballr'], S['ballr']), WH, sd=2, hl=1)
        c.stamp(p, 'K')
        for q in ((-6, -5), (7, 6), (-5, 5)):
            c.pxs([(bx + q[0], by_ + q[1]), (bx + q[0] + 1, by_ + q[1]), (bx + q[0], by_ + q[1] + 1), (bx + q[0] - 1, by_ + q[1]), (bx + q[0], by_ + q[1] - 1)], 'a2')
    if S['breath']:
        mx, my = B(6, 25)
        p = C()
        for q, r in (((-4, 0), 2.2), ((-8, -1), 1.8), ((-12, 1), 1.4)):
            p.fill(E(mx + q[0], my + q[1], r, r * 0.8), 'a2')
        c.stamp(p, ring=False)
    return c


WALK = [
    dict(bob=0, ffoot=10, nfoot=26, sway=1, hand=(5, 38), ball=(2, 37)),
    dict(bob=-1, ffoot=15, nfoot=21, nlift=0, flift=2, sway=0),
    dict(bob=0, ffoot=25, nfoot=11, sway=-1, hand=(6, 36), ball=(3, 35)),
    dict(bob=-1, ffoot=21, nfoot=15, nlift=2, sway=0),
]
ATTACK = [
    dict(lean=2, sh=(22, 28), hand=(31, 21), ball=(33, 18), ballr=3.6, ffoot=12, nfoot=25),
    dict(lean=-3, bob=1, sh=(11, 30), hand=(1, 28), ball=(-24, 26), ballr=3.6, trail=1, breath=1, ffoot=8, nfoot=24, sway=2),
    dict(lean=-1, sh=(12, 31), hand=(4, 35), ballr=0, breath=1, ffoot=11, nfoot=24, sway=1),
]

if __name__ == '__main__':
    export(NAME, warashi, WALK, ATTACK)
