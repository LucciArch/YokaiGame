"""Yamabiko - shaggy grey-brown ape-dog of the mountains, drooping ears, huge roaring mouth that throws the echo back."""
from kit import *

NAME = 'yamabiko'
CW, CH = 128, 84
OX, OY = 40, 9            # local baseline y=70
FUR = ('f1', 'f2', 'f3')
FAR = ('f0', 'f1', 'f2')

LEG = dict(zip('abcdKqxmMYZrst', ['f0', 'f1', 'f2', 'f3', 'K', 'q', 'b3', 'm1', 'm2', 'y2', 'y3', 'n0', 'n1', 'n2']))
HEAD = """
.........bb..bb.............
.......bbccbbccbb..b........
.....bbccddccccccbbcb.......
....bccddddcccccccccbb......
...bccdddddccccccccccbb.....
..bccddssssssscccccccbbb....
..bcdsstttssssssccccccbbb...
.bccKKKKKsssssKKKKKccccbbb..
.bcKKKKKKKKssKKKKKKKKcccbbb.
.bcsKYZYKKssssKKYZYKsccbbba.
.bccssKKssrKKrssKKssccbbbba.
..bcsssssrKrrKrsssscccbbbaa.
..bcssKKKKKKKKKKKKsscbbbbaa.
...csKxqxqqxqqxqxqKscbbbaa..
...bsKqqqqqqqqqqqqKsbbbbaa..
...bsKqqqqqqqqqqqqKrbbbaa...
...bsKqqqmmmmmmqqqKrbbbaa...
...bsKqqmMMMMMMmqqKrbbaa....
...brKKqxmmmmmqxqKKrbbaa....
....brrKKKKKKKKKKrrbbaa.....
....bbbrssssrrrrrbbbaa......
...bbcbbccbbbbbbabbaa.......
...b.bb.cb.bb.ab.a..........
"""

DEF = dict(
    bob=0, lean=0, head=(0, 0), wave=None,
    fsh=(43, 41), felb=(33, 48), fwr=(27, 58), fang=120,
    nsh=(55, 41), nelb=(49, 53), nwr=(41, 62), nang=125,
    fhip=(47, 58), fank=(45, 65), ftoe=36,
    nhip=(56, 58), nank=(57, 65), ntoe=47,
)


def P(x, y):
    return (x + OX, y + OY)


def leg(c, hip, ank, toe, ramp):
    p = C()
    th = shag(curve([hip, lerp(hip, ank, 0.5), ank], 3), 5.4, 3.4, tuft=1.8, every=2)
    p.form(th, ramp, sd=2, hl=1)
    ax, ay = ank
    by = ay + 5
    foot = PG([(ax + 3, ay - 1), (ax + 4, by), (toe + 1, by), (toe, by - 1), (toe + 4, by - 4), (ax - 2, ay - 2)])
    p.form(foot, ramp, sd=2, hl=1)
    c.stamp(p, 'f0')
    for i in range(3):
        c.pxs([(toe - 1 + i * 3, by), (toe + i * 3, by)], 'b2')


def arm(c, sh_, el, wr, ang, ramp):
    claw_hand(c, wr, ang, ramp, 'f0', spread=36, ln=6.0, n=3, cl=2.6, r=1.6, palm=3.0)
    p = C()
    m = tube([el, wr], 3.2, 2.6)
    mid = lerp(el, wr, 0.5)
    m = tufts(m, [(el[0] + 1, el[1] + 1, el[0] + 5, el[1] + 7, 2.2), (mid[0] + 1, mid[1] + 1, mid[0] + 5, mid[1] + 6, 2.0),
                  (wr[0] + 1, wr[1] - 2, wr[0] + 5, wr[1] + 2, 1.8)])
    p.form(m, ramp, sd=2, hl=1)
    c.stamp(p, 'f0')
    p = C()
    m = tube([sh_, el], 4.2, 3.4) | E(sh_[0], sh_[1], 5.6, 5.2)
    mid = lerp(sh_, el, 0.5)
    m = tufts(m, [(mid[0] + 2, mid[1] + 1, mid[0] + 7, mid[1] + 7, 2.4), (sh_[0] + 3, sh_[1] + 2, sh_[0] + 9, sh_[1] + 7, 2.4)])
    p.form(m, ramp, sd=2, hl=1)
    zig(p, m, mid[1] - 2, ramp[0], period=4, amp=2, on=(ramp[1],))
    c.stamp(p, 'f0')


def creature(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    arm(c, B(S['fsh']), B(S['felb']), B(S['fwr']), S['fang'], FAR)
    leg(c, P(*S['fhip']), P(*S['fank']), S['ftoe'] + OX, FAR)

    # shaggy hunched body: long hanging tufts on the back and under the belly, zig-zag fringes inside
    p = C()
    bx, by = B((52, 47), 0.6)
    body = E(bx, by, 12.0, 12.6) | E(bx + 3, by - 6, 10, 8)
    body = tufts(body, [(bx + 10, by - 9, bx + 15, by - 4, 2.6), (bx + 11, by - 3, bx + 16, by + 3, 2.8), (bx + 10, by + 4, bx + 14, by + 10, 2.8),
                        (bx + 6, by + 9, bx + 9, by + 15, 2.6), (bx, by + 11, bx + 2, by + 17, 2.4), (bx - 6, by + 9, bx - 7, by + 15, 2.4)])
    p.form(body, FUR, sd=5, hl=1)
    for k, yy in enumerate((-6, -1, 4, 9)):
        zig(p, body, by + yy, 'f1', period=6, amp=3, slope=0.12, on=('f2',), x0=bx - 12 + (k % 2) * 3)
    p.fill(R(bx - 7, by - 9, bx - 4, by - 9), 'f3', only=body)
    c.stamp(p, 'f0')

    leg(c, P(*S['nhip']), P(*S['nank']), S['ntoe'] + OX, FUR)

    # head: swept-back mane and long drooping ears behind, face grid on top
    hx, hy = B((22 + S['head'][0], 13 + S['head'][1]))
    p = C()
    mane = E(hx + 16, hy + 11, 10.5, 10.5)
    mane = tufts(mane, [(hx + 21, hy + 4, hx + 27, hy + 7, 3.0), (hx + 24, hy + 9, hx + 30, hy + 11, 2.8), (hx + 23, hy + 15, hx + 28, hy + 21, 2.8)])
    p.form(mane, FAR, sd=3, hl=1)
    c.stamp(p, 'f0')
    p = C()
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'f0')
    # long floppy ear hanging beside the face
    p = C()
    ear = tube(curve([(hx + 21, hy + 4), (hx + 25, hy + 7), (hx + 26, hy + 14), (hx + 24, hy + 20)]), 3.0, 2.0)
    p.form(ear, FUR, sd=1, hl=1)
    p.line([(hx + 24, hy + 8), (hx + 25, hy + 13), (hx + 24, hy + 18)], 'n0', only=erode(ear, 1))
    p.line([(hx + 25, hy + 9), (hx + 26, hy + 13)], 'n1', only=erode(ear, 1))
    c.stamp(p, 'K')

    arm(c, B(S['nsh']), B(S['nelb']), B(S['nwr']), S['nang'], FUR)
    c.blacken()

    # echo shockwave rings (drawn after the outline pass: pure light, no outline)
    if S['wave']:
        mx, my = hx + 6, hy + 16
        for r_, span in S['wave']:
            c.fill(arc(mx + 6, my, r_, 180 - span, 180 + span, 2.0, ry=r_ * 1.15) & ~c.m, 'v1')
            c.fill(arc(mx + 5, my, r_, 180 - span, 180 + span, 1.2, ry=r_ * 1.15) & ~(c.m & (c.a != I('v1'))), 'v3')
    return c


WALK = [
    dict(bob=1, fank=(41, 65), ftoe=31, nank=(60, 65), ntoe=50, nelb=(51, 53), nwr=(47, 63), nang=110, felb=(32, 47), fwr=(24, 55), fang=130),
    dict(bob=0, fank=(47, 65), ftoe=38, nank=(57, 63), ntoe=47),
    dict(bob=1, fank=(53, 65), ftoe=44, nank=(51, 65), ntoe=41, nelb=(47, 52), nwr=(37, 60), nang=135, felb=(35, 50), fwr=(31, 60), fang=112),
    dict(bob=0, fank=(46, 63), ftoe=37, nank=(56, 65), ntoe=46),
]
ATTACK = [
    dict(lean=3, bob=-1, head=(2, -2), nelb=(60, 50), nwr=(62, 60), nang=80, felb=(40, 52), fwr=(40, 61), fang=95),
    dict(lean=-4, bob=1, head=(-4, 1), nelb=(51, 52), nwr=(44, 62), nang=140, felb=(31, 47), fwr=(22, 53), fang=150,
         wave=[(9, 62), (15, 52), (21, 42)]),
    dict(lean=-2, bob=0, head=(-2, 0), nelb=(50, 53), nwr=(42, 62), nang=130, felb=(32, 48), fwr=(25, 56), fang=130,
         wave=[(22, 48), (28, 36)]),
]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
