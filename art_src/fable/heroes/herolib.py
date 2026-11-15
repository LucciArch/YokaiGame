"""Shared kit for the hero sprites: extra ramps, a small rig (feet, hakama, sleeve arm, hands), FX and export.
Engine + base palette come from ../px.py (unchanged)."""
import sys, math
sys.path.insert(0, '/home/claude/fable_art')
from px import *
import px
import numpy as np
from PIL import Image

HERE = '/home/claude/fable_art/heroes/'
BG = (0x16, 0x28, 0x5c, 255)
FLOOR = (0x24, 0x20, 0x2c, 255)

col('hb', '#1a1738'); px.add_rim('hb', 'xh')                                              # black human hair (as hana)
col('p0', '#24103e'); col('p1', '#46216e'); col('p2', '#7440a0'); col('p3', '#a874cc')    # purple cloth
col('xp', '#c9b4f2'); px.add_rim('p0 p1 p2', 'xp')
col('u0', '#131a44'); col('u1', '#213c78'); col('u2', '#3966a8'); col('u3', '#6c9cd6')    # indigo cloth
col('xu', '#a6d2f6'); px.add_rim('u0 u1 u2', 'xu')

WH = ('v1', 'v2', 'v3')
WHD = ('v0', 'v1', 'v2')
RD = ('m1', 'm2', 'm3')
HAIR = ('h0', 'hb', 'h2')
SKN = ('k1', 'k2', 'k3')
IRON = ('i1', 'i2', 'i3')
DARK = ('i0', 'i1', 'i2')
WOOD = ('w0', 'w1', 'w2')
GOLD = ('y0', 'y1', 'y2')
PUR = ('p1', 'p2', 'p3')
BLU = ('u1', 'u2', 'u3')

# base legend for text grids (same letters as hana.py, plus extras)
LEG = dict(zip('abcdmnoKeWrRsvwV',
               ['k0', 'k1', 'k2', 'k3', 'h0', 'hb', 'h2', 'K', 'w1', 'v3', 'm2', 'm3', 'm1', 'v1', 'v2', 'v0']))

HAND = """
.ccc
cdcb
cacb
cccb
.bb
"""
# open hand, palm forward (casting / throwing), fingers to the left
PALM = """
.cc..
cdccb
cdccb
cdcb.
.cb..
"""


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def vec(ang):
    """unit vector, ang in degrees: 180 = left, 90 = up"""
    a = math.radians(ang)
    return math.cos(a), -math.sin(a)


def arc(cx, cy, r0, r1, a0, a1, taper=True):
    """crescent between radius r0..r1 and angles a0..a1 (degrees, 180=left, 90=up); thins toward a1 end if taper."""
    dx, dy = px.X - cx, cy - px.Y
    rr = np.sqrt(dx * dx + dy * dy)
    ang = np.degrees(np.arctan2(dy, dx)) % 360
    lo, hi = a0 % 360, a1 % 360
    if lo <= hi:
        t = (ang - lo) / max(1e-6, hi - lo)
        ins = (ang >= lo) & (ang <= hi)
    else:
        aa = (ang - lo) % 360
        span = (hi - lo) % 360
        t = aa / span
        ins = aa <= span
    if taper:
        w = (r1 - r0) * np.sin(np.clip(t, 0, 1) * math.pi) ** 0.7
        return ins & (rr <= r1) & (rr >= r1 - w)
    return ins & (rr >= r0) & (rr <= r1)


class Rig:
    def __init__(s, S, cw=104, ch=88, ox=26, oy=14):
        s.S = S; s.ox = ox; s.oy = oy
        setsize(cw, ch)
        s.c = C()
        s.bob = S.get('bob', 0); s.lean = S.get('lean', 0)

    def P(s, x, y):
        return (x + s.ox, y + s.oy)

    def B(s, pt):
        return (pt[0] + s.lean + s.ox, pt[1] + s.bob + s.oy)

    # ---------- feet: local foot x (heel side = x+7), ground row = y 69
    def feet(s, kind='tabi', strap='m2', which='fn'):
        S = s.S
        for w_ in which:
            fx, lift = S[w_ + 'foot'], S.get(w_ + 'lift', 0)
            p = C()
            x0, y0 = s.P(fx, 66 - lift)
            if kind == 'tabi':
                foot = PG([(x0, y0 + 2), (x0 + 2, y0), (x0 + 7, y0), (x0 + 7, y0 + 3), (x0, y0 + 3)])
                p.form(foot, WH, sd=1, hl=0)
                p.fill(R(x0, y0 + 3, x0 + 7, y0 + 3), 'w1')
                p.fill(R(x0 + 3, y0 + 1, x0 + 4, y0 + 1), strap)
            elif kind == 'dark':
                foot = PG([(x0, y0 + 2), (x0 + 2, y0), (x0 + 7, y0), (x0 + 7, y0 + 3), (x0, y0 + 3)])
                p.form(foot, DARK, sd=1, hl=0)
                p.fill(R(x0, y0 + 3, x0 + 7, y0 + 3), 'c1')
                p.fill(R(x0 + 3, y0 + 1, x0 + 4, y0 + 1), strap)
            elif kind == 'waraji':
                foot = PG([(x0, y0 + 2), (x0 + 2, y0), (x0 + 7, y0), (x0 + 7, y0 + 3), (x0, y0 + 3)])
                p.form(foot, SKN, sd=1, hl=0)
                p.fill(R(x0, y0 + 3, x0 + 7, y0 + 3), 'c1')
                p.fill(R(x0 + 3, y0, x0 + 3, y0 + 2), 'c1')
                p.fill(R(x0 + 6, y0, x0 + 7, y0), 'c1')
            elif kind == 'geta':
                foot = PG([(x0, y0), (x0 + 2, y0 - 2), (x0 + 7, y0 - 2), (x0 + 7, y0), (x0, y0)])
                p.form(foot, strap if isinstance(strap, tuple) else SKN, sd=1, hl=0)
                p.fill(R(x0 - 1, y0 + 1, x0 + 8, y0 + 1), 'w2')
                p.fill(R(x0 + 1, y0 + 2, x0 + 2, y0 + 3), 'w1')
                p.fill(R(x0 + 5, y0 + 2, x0 + 6, y0 + 3), 'w1')
                p.fill(R(x0 + 3, y0 - 1, x0 + 3, y0), 'm2')
            s.c.stamp(p, 'K')

    # ---------- hakama / long skirt (same construction as hana)
    def hakama(s, ramp, deep, waist=(35, 46), wy=38, tie=None, slit=None, split=True, flare=(32, 49), stamp=True, hem=66):
        S, B, P = s.S, s.B, s.P
        p = C()
        f, n = S['ffoot'], S['nfoot']
        lo_, hi_ = (f, n) if f <= n else (n, f)
        ll, hl_ = (S.get('flift', 0), S.get('nlift', 0)) if f <= n else (S.get('nlift', 0), S.get('flift', 0))
        ny_ = hem - min(6, max(0, (hi_ - lo_ - 8) * 0.5)) if split else hem - max(ll, hl_) * 0.5
        mid = ((lo_ + hi_) / 2 + 4, ny_)
        w0, w1 = waist
        hk = PG([B((w0, wy)), B((w1, wy)), P(flare[1], 50), P(hi_ + 9, hem - hl_), P(hi_ - 1, hem - hl_), P(*mid),
                 P(lo_ + 8, hem - ll), P(lo_ - 1, hem - ll), P(flare[0], 50)])
        p.form(hk, ramp, sd=3, hl=1)
        for (a_, b_, col_) in [((w0 + 3, wy + 2), (lo_ + 3, hem - 1), ramp[0]), ((w0 + 6, wy + 2), (mid[0], mid[1] - 1), deep),
                               ((w1 - 2, wy + 2), (hi_ + 5, hem - 1), ramp[0]),
                               ((w0 + 1.5, wy + 3), (lo_ + 0.5, hem - 4), ramp[2]), ((w0 + 7.5, wy + 3), (hi_ + 2, hem - 2), ramp[2])]:
            p.line([B(a_), P(*b_)], col_, only=hk)
        if slit:
            p.fill(PG([B((w1 - 1, wy + 2)), B((w1 + 1, wy + 2)), B((w1 + 1, wy + 7))]), slit, only=hk)
            p.line([B((w1 - 1, wy + 2)), B((w1 + 1, wy + 8))], deep, only=hk)
        if tie:
            p.form(R(*B((w0, wy - 1)), *B((w1, wy + 1))), tie, sd=1, hl=1)
            p.form(E(*B((w0 + 2, wy + 2)), 2, 2), tie, sd=1, hl=1)
        if stamp:
            s.c.stamp(p, 'K')
        return p, hk

    # ---------- sleeved arm: upper arm + hanging sleeve bag + hand
    def arm(s, sh_, el, wr, ramp=WH, sv=0, bag=12, trim=None, hand=HAND, hleg=LEG, deep=None, upr=(3.6, 3.8), cuff=None):
        c = s.c
        deep = deep or ramp[0]
        if bag:
            p = C()
            bg = PG([(el[0] + 3, el[1] - 3), (wr[0] + 2, wr[1] - 3), (wr[0], wr[1] + 3), (wr[0] + 1 + sv, wr[1] + bag),
                     (wr[0] + 3 + sv, wr[1] + bag + 2), (el[0] + 1 + sv, el[1] + bag - 2), (el[0] + 4, el[1] + 2)])
            p.form(bg, ramp, sd=2, hl=1)
            p.line([(el[0] - 1, el[1]), (el[0] - 2 + sv, el[1] + bag - 3)], ramp[0], only=bg)
            p.line([(wr[0] + 5, wr[1] + 1), (wr[0] + 5 + sv, wr[1] + bag - 3)], ramp[0], only=bg)
            if trim:
                for k in range(bag // 3):
                    p.fill(R(wr[0] + 2 + (k * sv) // 3, wr[1] + 2 + k * 3, wr[0] + 2 + (k * sv) // 3, wr[1] + 3 + k * 3), trim, only=bg)
            if cuff:
                p.line([(wr[0] + 1 + sv, wr[1] + bag - 1), (el[0] + 1 + sv, el[1] + bag - 3)], cuff, only=bg)
                p.line([(wr[0] + 2 + sv, wr[1] + bag), (el[0] + 1 + sv, el[1] + bag - 2)], cuff, only=bg)
            c.stamp(p, 'K')
        else:
            p = C()
            fa = L(el[0], el[1], 2.9, wr[0] + 1, wr[1], 2.4)
            p.form(fa, ramp, sd=1, hl=1)
            if cuff:
                p.fill(L(wr[0] + 2, wr[1], 2.6, wr[0] + 4, wr[1] + (el[1] - wr[1]) * 0.25, 2.8), cuff, only=fa)
            c.stamp(p, 'K')
        p = C()
        up = L(sh_[0], sh_[1], upr[0], el[0] + 1, el[1] - 1, upr[1])
        p.form(up, ramp, sd=2, hl=1)
        p.line([(sh_[0] - 2, sh_[1] + 1), (el[0], el[1] - 3)], ramp[0], only=up)
        c.stamp(p, 'K')
        if hand:
            p = C()
            p.grid(int(wr[0]) - 3, int(wr[1]) - 2, hand, hleg)
            c.stamp(p, 'K')

    def head(s, text, leg, at, skip=('h0', 'hb', 'h2'), ln='K'):
        p = C()
        p.grid(*s.B(at), text, leg)
        s.c.stamp(p, ln, skip=skip)

    def done(s):
        s.c.blacken()
        return s.c


def build(name, fn, WALK, ATTACK, D=HERE, quiet=False):
    """exports <name>.png, _walk.png, _attack.png, _preview.png (6x, static+attack / walk) and a 4x review on floor colour."""
    c0 = fn()
    cw, ch = px.W, px.H
    base = c0.img()
    cr = crop_img(base)
    cr.save(D + name + '.png')
    out = {}
    for tag, frames in (('walk', WALK), ('attack', ATTACK)):
        cs = [fn(**f) for f in frames]
        for i, c_ in enumerate(cs):
            assert (px.W, px.H) == (cw, ch)
            x0, y0, x1, y1 = c_.bbox()
            assert x0 >= 1 and y0 >= 1 and x1 <= cw - 2 and y1 <= ch - 2, (name, tag, i, c_.bbox(), (cw, ch))
        out[tag] = [c_.img() for c_ in cs]
        strip(out[tag], D + f'{name}_{tag}.png')
    rows = [[base] + out['attack'], out['walk']]
    sheet = Image.new('RGBA', (cw * 4, ch * 2), (0, 0, 0, 0))
    for j, r in enumerate(rows):
        for i, im in enumerate(r):
            sheet.paste(im, (i * cw, j * ch))
    preview(sheet, D + name + '_preview.png', 6)
    preview(sheet, D + '_review/' + name + '.png', 4, bg=FLOOR)
    z = Image.new('RGBA', cr.size, BG); z.alpha_composite(cr)
    z.resize((cr.width * 10, cr.height * 10), Image.NEAREST).save(D + '_review/' + name + '_zoom.png')
    a = np.array(cr)
    semi = int(((a[:, :, 3] > 0) & (a[:, :, 3] < 255)).sum())
    ncol = len({tuple(q) for q in a.reshape(-1, 4) if q[3] > 0})
    if not quiet:
        print(name, 'static', cr.size, 'cell', (cw, ch), 'colours', ncol, 'semi', semi, 'orphans', len(orphans(cr)))
    return cr
