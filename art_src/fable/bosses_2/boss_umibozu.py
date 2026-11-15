"""Umibozu (~128 px): giant black sea monk rising from dark waves. Face (eyes) is one fixed grid-like stamp; the body only translates.
Local baseline (water line) y=150."""
from k2 import *

NAME = 'boss_umibozu'
CW, CH = 328, 192
OX, OY = 106, 30
N = ('n0', 'n1', 'n2')
NF = ('K', 'n0', 'n1')
WV = ('d1', 'a0', 'a1')
WVB = ('d0', 'd1', 'a0')

DEF = dict(bob=0, lean=0, ph=0.0,
           fsh=(46, 116), felb=(16, 122), fwr=(4, 96), fhand=252,     # far (front-left) arm; fhand = finger direction deg
           nsh=(154, 118), nelb=(184, 108), nwr=(186, 76), nhand=222,
           splash=0, drip=0, spread=26)


def P(x, y):
    return (x + OX, y + OY)


def hand(c, wr, ang, ramp, spread=26, ln=21, lnc='K'):
    """huge 4-fingered hand, fingers fanning around ang"""
    p = C()
    palm = pol(wr, ang, 6)
    m = E(palm[0], palm[1], 9.4, 9.4)
    p.form(m, ramp, sd=3, hl=1)
    c.stamp(p, lnc)
    for i, da in enumerate((-1.5, -0.5, 0.5, 1.5)):
        a = ang + da * spread
        base = pol(palm, a, 5)
        k = pol(palm, a, 5 + ln * 0.55)
        tip = pol(k, a + 14, ln * 0.5)
        p = C()
        fm = L(base[0], base[1], 3.4, k[0], k[1], 2.8) | L(k[0], k[1], 2.8, tip[0], tip[1], 1.2)
        p.form(fm, ramp, sd=1, hl=1)
        c.stamp(p, lnc)
    # thumb
    a = ang + 2.6 * spread
    base = pol(palm, a, 5); tip = pol(palm, a - 10, 15)
    p = C()
    p.form(L(base[0], base[1], 3.2, tip[0], tip[1], 1.7), ramp, sd=1, hl=1)
    c.stamp(p, lnc)
    p = C()
    p.form(E(palm[0], palm[1], 8, 8), ramp, sd=2, hl=0)
    c.stamp(p, ring=False)


def arm(c, sh_, el, wr, ang, ramp, spread, drip=0):
    p = C()
    m = L(sh_[0], sh_[1], 15, el[0], el[1], 11.5)
    p.form(m, ramp, sd=5, hl=1)
    c.stamp(p, 'K')
    p = C()
    m = L(el[0], el[1], 11.5, wr[0], wr[1], 8.5)
    p.form(m, ramp, sd=4, hl=1)
    c.stamp(p, 'K')
    hand(c, wr, ang, ramp, spread)
    # water running off the elbow
    if drip is not None:
        x, y = int(el[0]) + 2, int(el[1]) + 10
        c.fill(R(x, y + drip, x + 1, y + 4 + drip), 'a2')
        c.fill(R(x - 5, y + 3 + drip * 2, x - 4, y + 5 + drip * 2), 'a1')


def waves(c, x0, x1, base, amp, wl, ph, ramp, foam=True, bottom=None):
    """row of pointed crests; base = trough y (cell coords)"""
    p = C()
    xs = np.arange(px.W)
    top = base - amp * (1 - np.abs(np.sin((xs + ph) * math.pi / wl))) ** 1.4
    # taper to nothing at both ends
    edge = np.clip(np.minimum(xs - x0, x1 - xs) / 10.0, 0, 1)
    bot = (bottom if bottom is not None else base + 9)
    top = bot - (bot - top) * edge
    m = (px.Y >= np.round(top)[None, :]) & (px.Y <= bot) & (px.X >= x0) & (px.X <= x1)
    m &= ~((px.Y > bot - 3) & ((px.X < x0 + 4) | (px.X > x1 - 4)))
    p.fill(m, ramp[1])
    p.fill(m & ~sh(m, 0, 2), ramp[2])                       # lit crest lip
    p.fill(m & sh(m, 0, 5) & ~sh(m, 0, 7), ramp[0])        # dark band under the crest
    p.fill(m & ~sh(m, 0, -2), ramp[0])
    if foam:
        cap = m & ~sh(m, 0, 1) & (px.Y < base - amp * 0.45)
        p.fill(cap | (sh(cap, 0, 1) & m), 'a2')
        p.fill(cap & sh(cap, 1, 0) & sh(cap, -1, 0), 'v3')
    c.stamp(p, 'K')


def splash(c, x, base, h, w):
    """crown of water thrown up by the slam (attack)"""
    lobes = [(-0.9, 205, 0.55, 0.5, -30), (-0.55, 238, 0.95, 0.62, -26), (0.0, 262, 1.15, 0.7, -18), (0.5, 288, 0.9, 0.6, 22), (0.9, 318, 0.6, 0.5, 30)]
    for i in (0, 4, 1, 3, 2):
        dx, a, hl_, wl, bend = lobes[i]
        p = C()
        m = lock((x + w * dx * 0.6, base + 4), a, h * hl_, w * wl, bend) & (px.Y <= base + 8)
        p.form(m, WV if i in (1, 2, 3) else WVB, sd=3, hl=1)
        tipzone = m & ~sh(m, 0, 4) & (px.Y < base - h * hl_ * 0.45)
        p.fill(tipzone, 'a2')
        p.fill(m & ~sh(m, 0, 1) & (px.Y < base - h * hl_ * 0.45), 'v3')
        c.stamp(p, 'K')
    for (dx, dy, r) in [(-1.25, -0.8, 2.4), (-0.8, -1.2, 1.9), (-0.3, -1.3, 2.6), (0.35, -1.18, 1.8), (0.85, -0.85, 2.2), (-1.45, -0.4, 1.7), (1.2, -0.45, 1.6)]:
        p = C()
        p.fill(E(x + w * dx, base + h * dy, r, r), 'a2')
        p.fill(E(x + w * dx - 0.5, base + h * dy - 0.5, max(r - 1.3, 0.6), max(r - 1.3, 0.6)), 'v3')
        c.stamp(p, 'K')


def eye(p, cx, cy, rx, ry, inner):
    """huge lamp eye; inner = -1 if the nose is to the left of this eye, +1 if to the right. Lid slants down toward the nose."""
    p.fill(E(cx, cy, rx + 3.2, ry + 3.2), 'n0')
    p.fill(E(cx, cy, rx + 2, ry + 2), 'K')
    p.fill(E(cx, cy, rx + 1, ry + 1), 'y0')
    p.fill(E(cx, cy, rx, ry), 'y1')
    p.fill(E(cx - 0.6, cy - 0.4, rx - 1.6, ry - 1.6), 'y2')
    p.fill(E(cx - rx * 0.28, cy + ry * 0.3, rx * 0.46, ry * 0.4), 'y3')
    # slit pupil, staring down-left at the player
    p.fill(E(cx - rx * 0.3, cy + ry * 0.28, max(rx * 0.13, 1.2), ry * 0.36), 'K')
    # heavy lid
    xi, xo = cx + inner * (rx + 4), cx - inner * (rx + 4)
    lid = PG([(xi, cy + ry * 0.12), (xo, cy - ry * 0.62), (xo, cy - ry - 5), (xi, cy - ry - 5)]) & E(cx, cy, rx + 2, ry + 2)
    p.fill(lid, 'K')
    low = PG([(xi, cy + ry * 0.12), (xo, cy - ry * 0.62), (xo, cy - ry * 0.62 + 1.6), (xi, cy + ry * 0.12 + 1.6)]) & E(cx, cy, rx, ry)
    p.fill(low, 'y0')


def umi(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    b = S['bob']; ln = S['lean']; ph = S['ph']
    base = OY + 150

    def B(pt, k=1.0):
        return P(pt[0] + ln * k, pt[1] + b)

    # back waves
    waves(c, OX - 16, OX + 208, base - 7, 8, 22, ph * 0.6 + 9, WVB, foam=False, bottom=base + 2)
    # far arm
    arm(c, B(S['fsh']), B(S['felb'], 1.2), B(S['fwr'], 1.4), S['fhand'], NF, S['spread'], S['drip'])
    # ---- body: sloped mountain of shoulders + dome head, one smooth mass
    p = C()
    torso = E(*B((102, 152), 0.5), 70, 58) & (px.Y < base + 8)
    head = E(*B((94, 62)), 33.4, 35.4)
    neck = L(*B((95, 66)), 31, *B((100, 118), 0.7), 50)
    body = (torso | head | neck) & (px.Y < base + 8)
    p.form(body, N, sd=12, hl=2)
    inner = erode(body, 4)
    # wet sheen: broad light plane on the upper-left of the dome + shoulder
    sheen = E(*B((80, 44)), 21, 15) & inner & ~E(*B((87, 53)), 22, 16)
    p.fill(sheen, 'n2')
    p.fill(E(*B((73, 38)), 7, 3) & inner, 'n3')
    p.fill(R(*B((86, 31)), *B((92, 32))), 'n3', only=erode(body, 3))
    shl = E(*B((56, 108), 0.6), 17, 8) & inner & ~E(*B((61, 114), 0.6), 19, 9)
    p.fill(shl, 'n2')
    p.fill(R(*B((46, 106), 0.6), *B((52, 106), 0.6)), 'n3', only=inner)
    # brow overhang: deep shadow band the eyes sit in
    band_ = E(*B((84, 64)), 31, 13) & body & ~E(*B((84, 50)), 36, 10)
    p.fill(band_, 'n0')
    # water streaks running down
    for (x, y0, y1) in [(50, 114, 136), (66, 120, 142), (84, 112, 132), (122, 112, 140), (140, 106, 130), (104, 124, 144)]:
        d = S['drip']
        p.line([B((x, y0 + d * 2), 0.6), B((x + 1, y1 + d * 2), 0.6)], 'n2', only=inner)
    c.stamp(p, 'K')
    # eyes
    hx, hy = B((0, 0))
    hx, hy = int(round(hx)), int(round(hy))
    p = C()
    eye(p, hx + 96, hy + 66, 11.4, 11.4, -1)
    eye(p, hx + 67, hy + 66, 7.4, 10.4, +1)
    c.stamp(p, ring=False)
    # near arm
    arm(c, B(S['nsh']), B(S['nelb'], 1.2), B(S['nwr'], 1.4), S['nhand'], N, S['spread'], S['drip'])
    # front waves + foam where the body breaks the surface
    if S['splash']:
        sx, sh_, sw = S['splash']
        splash(c, OX + sx, base, sh_, sw)
    # foam where the body breaks the surface (two patches at the flanks)
    p = C()
    for i, x in enumerate((36, 47, 158, 169)):
        yy = base - 8 + ((i + int(ph // 6)) % 2) * 2
        p.fill(E(OX + x + ln * 0.4, yy, 6.2, 2.8), 'a2')
        p.fill(R(OX + x + ln * 0.4 - 3, yy - 1, OX + x + ln * 0.4 + 1, yy - 1), 'v3')
    c.stamp(p, 'a0')
    waves(c, OX - 26, OX + 216, base, 9, 26, ph, WV)
    c.blacken()
    return c


WALK = [dict(bob=0, ph=0, drip=0), dict(bob=-2, ph=6.5, drip=1, fwr=(3, 94), nwr=(187, 74)),
        dict(bob=-3, ph=13, drip=2, fwr=(2, 93), nwr=(188, 73)), dict(bob=-1, ph=19.5, drip=3, fwr=(3, 95), nwr=(187, 75))]
ATTACK = [
    dict(bob=-8, lean=4, ph=4, fsh=(48, 108), felb=(24, 74), fwr=(40, 40), fhand=268, nsh=(152, 108), nelb=(176, 74), nwr=(160, 40), nhand=256, spread=16),
    dict(bob=4, lean=-12, ph=11, fsh=(44, 118), felb=(12, 126), fwr=(-22, 138), fhand=178, nsh=(140, 120), nelb=(112, 134), nwr=(76, 142), nhand=184,
         spread=20, splash=(-34, 78, 40)),
    dict(bob=1, lean=-6, ph=18, fsh=(46, 118), felb=(18, 128), fwr=(-6, 132), fhand=205, nsh=(148, 120), nelb=(150, 136), nwr=(118, 142), nhand=192,
         splash=(-40, 34, 34)),
]

if __name__ == '__main__':
    export(NAME, umi, WALK, ATTACK)
