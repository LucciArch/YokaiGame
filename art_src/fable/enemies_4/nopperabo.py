"""Nopperabo: faceless woman in a blue kimono, smooth blank egg face. Normal (~58 px).
Walk: hides behind her sleeve as if weeping. Attack: lowers the sleeve, reveals the blank face, reaches out."""
from common import *

NAME = 'nopperabo'
CW, CH = 96, 76
OX, BASE = 54, 70
KIM = ('n0', 'n1', 'n2')
KIMF = ('n0', 'n0', 'n1')
HAIR = ('h0', 'h1', 'h2')
OBI = ('m1', 'm2', 'm3')

LEG = dict(zip('mnokKjJ', ['h0', 'h1', 'h2', 'k3', 'v3', 'k2', 'k1']))
HLEG = dict(zip('kKj', ['k2', 'k3', 'k1']))
HEAD = """
.....mmmmmmm...
...mmnnnnnnnmm.
..mnnoonnnnnnnm
.mnooonnnnnnnnm
.mnkkkkonnnnnnm
.mkKKKkkknnnnnm
mkKKKKKkkknnnnm
mkKKKKKkkkjnnnm
mkKKKKkkkkjnnnm
mkKKKkkkkkjnnnm
mkkKkkkkkjjnnnm
.kkkkkkkkjjnnnm
.kkkkkkkjjJnnnm
..kkkkkjjJnnnnm
...jjjjjJnnnnnm
.....JJJnnnnnm.
"""
HAND = """
kk.........
.kkkk......
...kkKkk...
KKkkKKKkkk.
...kKKKkkkj
kkkkkKkkkj.
...kkkkjj..
.kkk.kj....
"""


def sleeve(c, s, w, ramp, drop=13):
    """kimono sleeve: arm tube shoulder->wrist plus the hanging pocket below the wrist"""
    p = C()
    armm = L(s[0], s[1], 4.2, w[0], w[1], 3.6)
    pocket = PG([(w[0] - 2, w[1] - 3), (w[0] + 1, w[1] + drop), (w[0] + 8, w[1] + drop + 1),
                 lerp(w, s, 0.75)[0:2], (w[0] + 3, w[1] - 3)])
    m = armm | pocket
    p.form(m, ramp, sd=3, hl=1)
    # fold lines + pale lining at the opening
    p.line([(w[0] + 3, w[1] + 2), (w[0] + 5, w[1] + drop - 1)], ramp[0], only=erode(m, 1))
    p.line([(w[0] - 2, w[1] - 2), (w[0] - 1, w[1] + 4)], 'v1', only=m)
    c.stamp(p, 'K')


def hand(c, w, flip=False):
    p = C()
    p.grid(int(w[0]) - 9, int(w[1]) - 4, HAND, HLEG)
    c.stamp(p, 'k0')


DEF = dict(dx=0, bob=0, sway=0, hx=0, hy=0, step=0,
           nsh=(2, -42), nwr=(-9, -30), nhand=True,
           fsh=(-4, -43), fwr=(-13, -35), fhand=True, hair=0)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx = OX + S['dx']
    b = S['bob']
    sw = S['sway']

    def B(pt):
        return (cx + pt[0], BASE + pt[1] + b)

    # long hair down the back
    p = C()
    hair = PG([B((2 + S['hx'], -55)), B((10 + S['hx'], -52)), B((13 + S['hair'], -34)), B((11 + S['hair'], -22)),
               B((6 + S['hair'], -20)), B((5, -40))])
    p.form(hair, HAIR, sd=2, hl=0)
    p.line([B((9 + S['hx'], -50)), B((10 + S['hair'], -26))], 'h2', only=erode(hair, 1))
    c.stamp(p, 'K')
    # far arm
    sleeve(c, B(S['fsh']), B(S['fwr']), KIMF, 11)
    if S['fhand']:
        hand(c, B((S['fwr'][0] - 2, S['fwr'][1])))
    # feet: white tabi under the hem
    p = C()
    for fx in (-6 + S['step'], 3 - S['step']):
        p.form(PG([(cx + fx - 3, BASE - 1), (cx + fx - 2, BASE - 3), (cx + fx + 3, BASE - 3), (cx + fx + 3, BASE - 1)]), ('v0', 'v1', 'v2'), sd=1, hl=0)
        p.fill(R(cx + fx - 4, BASE, cx + fx + 4, BASE), 'w1')
    c.stamp(p, 'K')
    # kimono body
    p = C()
    body = PG([B((-5, -45)), B((6, -45)), B((8, -30)), (cx + 9 + sw, BASE - 12), (cx + 11 + sw, BASE - 3),
               (cx - 10 + sw, BASE - 3), (cx - 8, BASE - 14), B((-6, -30))])
    p.form(body, KIM, sd=5, hl=1)
    inner = erode(body, 1)
    # overlap seam, hem band, wave crests
    p.line([B((-2, -44)), B((-1, -28)), (cx - 3 + sw, BASE - 4)], 'n0', only=inner)
    hem = body & (px.Y >= BASE - 8)
    p.form(hem, ('n1', 'n2', 'n3'), sd=3, hl=0)
    for k in range(-8, 10, 5):
        p.line([(cx + k + sw, BASE - 10), (cx + k + 2 + sw, BASE - 12), (cx + k + 4 + sw, BASE - 10)], 'n3', only=inner)
    for (x0, y0, x1, y1) in [(4, -20, 6, -8), (-6, -18, -7, -9)]:
        p.line([B((x0, y0)), (cx + x1 + sw, BASE + y1)], 'n0', only=inner)
    # white collar V
    p.line([B((-4, -45)), B((0, -40)), B((3, -45))], 'v2', only=body)
    p.line([B((-3, -45)), B((0, -41)), B((2, -45))], 'v1', only=body)
    c.stamp(p, 'K')
    # obi with knot at the back
    p = C()
    obi = PG([B((-7, -33)), B((8, -33)), B((8, -26)), B((-7, -26))])
    p.form(obi & sh(body, 0, 0) | PG([B((7, -35)), B((12, -34)), B((12, -24)), B((7, -25))]), OBI, sd=2, hl=1)
    p.line([B((-7, -30)), B((12, -30))], 'y1')
    c.stamp(p, 'K')
    # head
    p = C()
    hx, hy = B((-9 + S['hx'], -62 + S['hy']))
    p.fill(L(*B((0, -47)), 2.6, *B((0, -44)), 2.8), 'k1')
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'K')
    # near arm
    if S['nhand']:
        hand(c, B((S['nwr'][0] - 2, S['nwr'][1])))
    sleeve(c, B(S['nsh']), B(S['nwr']), KIM)
    c.blacken()
    return c


HIDE = dict(nwr=(-7, -50), nhand=False, fwr=(-10, -47), fhand=False)
WALK = [
    dict(HIDE, bob=0, step=2, sway=1, hair=0),
    dict(HIDE, bob=-1, step=0, sway=0, hair=1),
    dict(HIDE, bob=0, step=-2, sway=-1, hair=0),
    dict(HIDE, bob=-1, step=0, sway=0, hair=-1),
]
ATTACK = [
    dict(dx=2, nwr=(-10, -43), nhand=False, fwr=(-12, -42), fhand=False, hair=1),
    dict(dx=-4, bob=1, hx=-2, hy=1, nwr=(-17, -37), fwr=(-22, -44), sway=3, hair=3, step=3),
    dict(dx=-2, hx=-1, nwr=(-12, -32), fwr=(-16, -38), sway=1, hair=1, step=1),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
