"""Gaki - hungry ghost: emaciated grey-green body, rib cage, bloated belly, stick limbs with claws, sunken eyes, rag loincloth."""
from kit import *

NAME = 'gaki'
CW, CH = 104, 84
OX, OY = 20, 8            # local baseline y=70
SK = ('z1', 'z2', 'z3')
FAR = ('z0', 'z1', 'z2')
RAG = ('m0', 'm1', 'm2')

LEG = dict(zip('abcdKqxwYZmn', ['z0', 'z1', 'z2', 'z3', 'K', 'q', 'b3', 'b2', 'e1', 'y3', 'h0', 'h1']))
HEAD = """
.......bbbbbb.......
.....bbcccccbbb.....
...bbcddccccccbbb...
..bcdddddcccccccbb..
..cddddccccccccbbba.
.bcddcccccccccbbbba.
.bKKKccccccccKKKbba.
.cKKKKKcbbcKKKKKbba.
.cKYZKKcbbcKKYZKbaa.
.bcKKKKcabcKKKKbbaa.
..bccccaKcbbbbbbaa..
..bacccbabbbaabaa...
...bKKKKKKKKKaaa....
...KxqxqqxqxKaa.....
...KqqqqqqqqKa......
...KqqqqqqqqKa......
...KqqqqqqqqKa......
...KwqqwqqwqKa......
....bKKKKKKKaa......
.....bccbbba........
"""

DEF = dict(
    bob=0, lean=0, head=(0, 0),
    fsh=(46, 37), felb=(36, 35), fwr=(25, 33), fang=184,
    nsh=(51, 37), nelb=(42, 41), nwr=(30, 39), nang=180,
    fhip=(48, 57), fknee=(41, 61), fank=(43, 66), ftoe=33,
    nhip=(53, 57), nknee=(51, 62), nank=(56, 66), ntoe=46,
)


def P(x, y):
    return (x + OX, y + OY)


def leg(c, hip, knee, ank, toe, ramp):
    p = C()
    p.form(L(hip[0], hip[1], 2.5, knee[0], knee[1], 1.8), ramp, sd=1, hl=1)
    p.form(L(knee[0], knee[1], 1.7, ank[0], ank[1], 1.5), ramp, sd=1, hl=1)
    p.form(E(knee[0], knee[1], 2.5, 2.5), ramp, sd=1, hl=1)          # knobby knee
    ax, ay = ank
    by = ay + 4
    foot = PG([(ax + 2, ay), (ax + 2, by), (toe + 1, by), (toe, by - 1), (toe + 5, by - 2), (ax - 1, ay - 1)])
    p.form(foot, ramp, sd=1, hl=1)
    c.stamp(p, 'z0')
    for i in range(3):
        c.pxs([(toe - 1 + i * 3, by), (toe + i * 3, by)], 'b2')


def arm(c, sh_, el, wr, ang, ramp, spread=30):
    claw_hand(c, wr, ang, ramp, 'z0', spread=spread, ln=6.5, n=4, cl=2.4, r=1.1, palm=2.3)
    thin_limb(c, el, wr, 1.7, 1.3, ramp, 'z0', knob=2.3)
    thin_limb(c, sh_, el, 1.8, 1.6, ramp, 'z0', knob=2.9)


def creature(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt, k=1.0):
        return P(pt[0] + lean * k, pt[1] + bob)

    arm(c, B(S['fsh']), B(S['felb']), B(S['fwr']), S['fang'], FAR)
    leg(c, P(*S['fhip']), P(*S['fknee']), P(*S['fank']), S['ftoe'] + OX, FAR)

    # neck (stringy)
    p = C()
    p.form(L(*B((51, 35)), 2.4, *B((42 + S['head'][0], 29 + S['head'][1])), 1.8), FAR, sd=1, hl=0)
    c.stamp(p, 'z0')

    # rib cage: hunched and narrow, vertebrae knobs down the back, every rib its own lit ridge
    p = C()
    chest = L(*B((53, 38)), 7.0, *B((53, 47), 0.6), 6.0)
    for i in range(4):
        chest |= E(*B((60.4 - i * 0.3, 35 + i * 3.6), 1 - i * 0.1), 1.6, 1.5)
    p.form(chest, SK, sd=3, hl=1)
    for i in range(4):
        y = 37 + i * 3
        a_, m_, b_ = B((46, y + 2)), B((52, y + 2.4)), B((59, y))
        p.line([a_, m_, b_], 'z0', only=chest)
        p.line([(a_[0], a_[1] - 1), (m_[0] + 3, m_[1] - 1)], 'z3', only=chest & (p.a == I('z2')))
    p.line([B((46, 33)), B((52, 34)), B((58, 33))], 'z0', only=chest)
    c.stamp(p, 'z0')

    # rag loincloth
    p = C()
    rag = PG([P(42, 55), P(58, 54), P(60, 61), P(57, 65), P(55, 60), P(52, 67), P(49, 61), P(46, 66), P(44, 61), P(41, 63)])
    p.form(rag, RAG, sd=3, hl=1)
    p.line([P(50, 58), P(51, 62)], 'm0', only=rag)
    p.line([P(55, 57), P(56, 61)], 'm0', only=rag)
    c.stamp(p, 'K')

    # bloated belly, hanging forward over the rag
    p = C()
    bx, by = B((42, 50), 0.5)
    belly = E(bx, by, 11.2, 8.8) | E(bx + 6, by - 3, 7, 7)
    p.form(belly, SK, sd=4, hl=1)
    p.fill(R(bx - 7, by - 6, bx - 4, by - 6), 'z3', only=belly)          # taut-skin glint
    p.pxs([(bx - 8, by + 3), (bx - 8, by + 4)], 'z0')                    # navel
    p.line([(bx - 1, by - 8), (bx + 4, by - 5), (bx + 7, by)], 'z1', only=erode(belly, 3))
    p.line([(bx - 6, by + 7), (bx, by + 8), (bx + 5, by + 6)], 'z0', only=erode(belly, 1))   # sag crease
    c.stamp(p, 'z0')

    leg(c, P(*S['nhip']), P(*S['nknee']), P(*S['nank']), S['ntoe'] + OX, SK)

    # head
    p = C()
    hx, hy = B((25 + S['head'][0], 12 + S['head'][1]))
    # lank hair strands hanging off the back of the skull
    for pts in ([(16, 3), (19, 7), (19, 12)], [(8, 0), (6, -2)], [(11, 0), (12, -2)], [(14, 1), (17, -1)]):
        q = [(hx + a_, hy + b_) for a_, b_ in pts]
        p.line(q, 'h1')
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'K')

    arm(c, B(S['nsh']), B(S['nelb']), B(S['nwr']), S['nang'], SK)
    c.blacken()
    return c


WALK = [
    dict(bob=1, fknee=(39, 62), fank=(38, 66), ftoe=28, nknee=(54, 62), nank=(60, 66), ntoe=50,
         nelb=(43, 42), nwr=(32, 42), nang=172, felb=(36, 34), fwr=(25, 31)),
    dict(bob=0, fknee=(44, 60), fank=(48, 66), ftoe=38, nknee=(50, 60), nank=(55, 63), ntoe=45),
    dict(bob=1, fknee=(48, 62), fank=(55, 66), ftoe=45, nknee=(45, 62), nank=(46, 66), ntoe=36,
         nelb=(41, 40), nwr=(29, 37), nang=186, felb=(37, 36), fwr=(27, 36), fang=176),
    dict(bob=0, fknee=(43, 59), fank=(45, 63), ftoe=35, nknee=(50, 61), nank=(54, 66), ntoe=44),
]
ATTACK = [
    dict(lean=4, bob=-1, head=(2, -1), nelb=(60, 29), nwr=(56, 18), nang=240, felb=(50, 27), fwr=(44, 17), fang=232),
    dict(lean=-7, bob=2, head=(-4, 2), nelb=(37, 37), nwr=(22, 36), nang=178, felb=(31, 34), fwr=(17, 30), fang=186,
         fknee=(39, 62), fank=(37, 66), ftoe=27, nknee=(55, 62), nank=(61, 66), ntoe=51),
    dict(lean=-3, bob=1, head=(-1, 1), nelb=(42, 43), nwr=(31, 45), nang=160, felb=(35, 38), fwr=(25, 38), fang=168,
         fknee=(40, 61), fank=(40, 66), ftoe=30),
]

if __name__ == '__main__':
    export(NAME, creature, WALK, ATTACK)
