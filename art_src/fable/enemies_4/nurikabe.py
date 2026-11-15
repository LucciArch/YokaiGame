"""Nurikabe: huge living stone wall with eyes, a mouth and stubby legs. Large (~80 px). Attack: topples forward, slamming."""
from common import *

NAME = 'nurikabe'
CW, CH = 136, 108
OX, BASE = 82, 102
ST = ('z1', 'z2', 'z3')
STD = ('z0', 'z1', 'z2')
HT = 76.0

LEG = dict(zip('KzZyYXqwWa', ['K', 'z0', 'z1', 'y1', 'y2', 'y3', 'q', 'b2', 'b3', 'z2']))
EYES = """
KK.................KK...
zKKKK...........KKKKz...
.zzKKKKK.....KKKKKzz....
.KKzzKKKK...KKKKzzKK....
.KyYYYXKK...KKyYYYXK....
.KKyYYYK.....KyYYYKK....
..zKKKKz.....zKKKKz.....
"""
MOUTH = """
K.........................K.
KK.......................KK.
.KKKKKKKKKKKKKKKKKKKKKKKKK..
.zKWqqWWqqqWWqqqWWqqqWWqKz..
..KqqqqqqqqqqqqqqqqqqqqqK...
..KqWWqqqWWqqqWWqqqWWqqqK...
..zKKKKKKKKKKKKKKKKKKKKKz...
"""


def stub_leg(c, hip, foot, ramp):
    p = C()
    m = L(hip[0], hip[1], 5.6, foot[0], foot[1] - 4, 5.0)
    ft = PG([(foot[0] + 6, foot[1] - 5), (foot[0] + 6, foot[1]), (foot[0] - 9, foot[1]), (foot[0] - 9, foot[1] - 3), (foot[0] - 4, foot[1] - 6)])
    p.form(m | ft, ramp, sd=3, hl=1)
    p.line([(foot[0] - 6, foot[1] - 3), (foot[0] - 6, foot[1])], ramp[0], only=ft)
    p.line([(foot[0] - 3, foot[1] - 4), (foot[0] - 3, foot[1])], ramp[0], only=ft)
    c.stamp(p, 'K')


def stub_arm(c, s, w, ramp, ang):
    p = C()
    p.form(L(s[0], s[1], 4.6, w[0], w[1], 4.0), ramp, sd=2, hl=1)
    for da in (-35, 0, 35):
        p.form(L(w[0], w[1], 2.0, *pol(w, ang + da, 5.5), 1.6), ramp, sd=1, hl=1)
    c.stamp(p, 'K')


DEF = dict(dx=0, bob=0, lean=0, squash=0,
           nft=(6, 0), fft=(-16, 0),
           nsh=(-6, -23), nwr=(-20, -17), nang=165,
           fsh=(-30, -36), fwr=(-40, -29), fang=160, dust=0)


def draw(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx = OX + S['dx']
    b = S['bob']
    ln_ = S['lean']
    top = -HT - 8 + S['squash']         # wall top (local y), bottom at -8

    def sx(y):                           # shear: how far a point at local height y leans
        return ln_ * (-(y + 8) / HT)

    def B(pt):
        return (cx + pt[0] + sx(pt[1]), BASE + pt[1] + b)

    U = px.X - cx - ln_ * (-(px.Y - BASE - b + 8) / HT)
    V = px.Y - BASE - b
    # legs
    stub_leg(c, (cx + S['fft'][0] + 2, BASE - 12 + b), (cx + S['fft'][0], BASE + S['fft'][1]), STD)
    # far arm
    stub_arm(c, B(S['fsh']), B(S['fwr']), STD, S['fang'])
    stub_leg(c, (cx + S['nft'][0] + 2, BASE - 12 + b), (cx + S['nft'][0], BASE + S['nft'][1]), ST)
    # side face (thickness, in shadow)
    p = C()
    side = (U > 14) & (U <= 26) & (V >= top + 2 + (U - 14) * 0.5) & (V <= -8 - (U - 14) * 0.4)
    p.fill(side, 'z1')
    p.fill(side & (((V - top) % 13 < 1)), 'z0')
    p.fill(side & (U > 22), 'z0')
    c.stamp(p, 'K')
    # front face: plastered masonry blocks
    p = C()
    front = (U >= -32) & (U <= 14) & (V >= top) & (V <= -8)
    p.fill(front, 'z0')
    rowh = 13
    row = np.floor((V - top) / rowh)
    offs = np.where(row % 2 == 0, 0, 9)
    colw = 18
    cu = (U + 32 + offs) % colw
    cv = (V - top) % rowh
    block = front & (cu >= 1) & (cv >= 1)
    p.fill(block, 'z2')
    p.fill(block & ((cu == 1) | (cv == 1)), 'z3')
    p.fill(block & ((cu >= colw - 2) | (cv >= rowh - 2)), 'z1')
    # big plaster patch around the face (smoother, lighter) so the face reads
    patch = front & (((U + 9) / 21.0) ** 2 + ((V - top - 33) / 24.0) ** 2 <= 1)
    p.fill(patch, 'z2')
    p.fill(patch & ~sh(patch, 2, 2), 'z3')
    p.fill(patch & ~sh(patch, -3, -3), 'z1')
    # overall shadow toward the right/bottom of the slab
    darken(p, front & ((U > 7) | (V > -14)) & (p.a != I('z0')))
    # cracks
    for pts in ([(-30, top + 8), (-24, top + 13), (-25, top + 20)], [(10, top + 4), (5, top + 12), (8, top + 18), (4, top + 24)],
                [(-6, -10), (-3, -17), (-8, -22)], [(-28, -30), (-22, -27)]):
        p.line([B((x, y)) for x, y in pts], 'z0', only=front)
    # moss on the top edge
    moss = front & (V <= top + 2 + ((U + 40) % 7 < 3))
    p.fill(moss, 'g1'); p.fill(moss & (V <= top + 1), 'g2')
    c.stamp(p, 'K')
    # coping stones on top
    p = C()
    cope = (U >= -34) & (U <= 16) & (V >= top - 4) & (V < top)
    p.form(cope, ST, sd=1, hl=1)
    p.fill(cope & ((U + 34) % 10 == 0), 'z0')
    cs = (U > 16) & (U <= 28) & (V >= top - 4 + (U - 16) * 0.5) & (V < top + 1 + (U - 16) * 0.5)
    p.fill(cs, 'z1')
    c.stamp(p, 'K')
    # face
    fo = B((-22, top + 22))
    p = C()
    p.grid(int(fo[0]), int(fo[1]), EYES, LEG)
    mo = B((-24, top + 38))
    p.grid(int(mo[0]), int(mo[1]), MOUTH, LEG)
    c.stamp(p, ring=False)
    # near arm
    stub_arm(c, B(S['nsh']), B(S['nwr']), ST, S['nang'])
    c.blacken()
    # dust kicked up by the slam
    if S['dust']:
        p = C()
        for (ox, oy, r) in [(-52, -4, 4.4), (-45, -7, 5.4), (-37, -4, 4.0), (-58, -9, 2.6), (20, -4, 3.6), (27, -6, 2.6)]:
            m = E(cx + ox, BASE + oy, r, r * 0.8)
            p.fill(m, 'z2'); p.fill(m & ~sh(m, 1, 1), 'z3')
        c.stamp(p, 'K')
    return c


WALK = [
    dict(bob=0, lean=-2, nft=(10, 0), fft=(-20, 0), nwr=(-18, -16), fwr=(-42, -30)),
    dict(bob=-1, lean=0, nft=(4, -3), fft=(-15, 0)),
    dict(bob=0, lean=2, nft=(-1, 0), fft=(-9, 0), nwr=(-22, -18), fwr=(-38, -28)),
    dict(bob=-1, lean=0, nft=(5, 0), fft=(-15, -3)),
]
ATTACK = [
    # rocks back on its heels, arms up
    dict(dx=4, lean=9, nft=(8, 0), fft=(-12, 0), nsh=(-6, -24), nwr=(-21, -30), nang=220, fsh=(-30, -40), fwr=(-39, -50), fang=250),
    # crashes forward
    dict(dx=-4, lean=-30, squash=10, bob=2, nft=(8, 0), fft=(-10, 0), nsh=(-6, -22), nwr=(-22, -17), nang=175,
         fsh=(-30, -36), fwr=(-43, -33), fang=175, dust=1),
    dict(dx=-2, lean=-10, squash=3, nft=(6, 0), fft=(-14, 0)),
]

if __name__ == '__main__':
    export(NAME, draw, WALK, ATTACK)
