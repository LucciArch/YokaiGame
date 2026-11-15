import sys, math
sys.path.insert(0, '/home/claude/fable_art')
from px import *
import px

CW, CH = 160, 120
OX, OY = 44, 15          # local -> cell offset ; local baseline y=100
SK = ('r1', 'r2', 'r3')
FAR = ('r0', 'r1', 'r2')
GOLD = ('i0', 'i1', 'i2')
HAIR = ('h0', 'h1', 'h2')

LEG = dict(zip('abcdemnouvwxyYKqZ',
               ['r0', 'r1', 'r2', 'r3', 'r4', 'h0', 'h1', 'h2', 'b0', 'b1', 'b2', 'b3', 'y1', 'y2', 'K', 'q', 'y3']))

HEAD = """
.........x..................
.........xw.................
..x.....xwwv................
..xw....xwvvu...mm..........
..wwv...wwvvu..mnnnn..mm....
...wvu..wwvvumnnonnnnnnm....
...wvvmmwvvuumnoonnnnnnnm...
..mwvumnmuuumnoonnnnnnnnn.m.
..mnmmnonmmmnnonnnnnnnnnnnm.
.mnnddnnoonnnnnnnnnnnnnnnnm.
.mnddeedddnnnnnnnnnnnnnnnnm.
.mcdeeeddddcbnnnnnnnnnnnnnnm
..cddedddcccbbnnnnnnnnnnnnnm
..KabbcbbbbaKKKbnnnnnnnnnnm.
..KKKacdaKKKKKabnnnnnnnnnnnm
..ZKKKbaKKZKYabbnnnnnnnnnnnm
..aYyabbaZYyaabbnnnnnnnnnnm.
.cdaaddccaaaccbbannnnnnnnnm.
.deeddcbcddcccbaannnnnnnnm..
.cddccbbcdccccbba.mnnnnnnm..
.bKcKbacccccxbba...mnnnnm...
..xaaaaaaaaaxwba....mnm.....
..xwqwwqwwqqwvba............
..wvqqqqqqqqwvba............
..bvqwqwwqwqvbb.............
...bccddcccbbba.............
...bcddccccbba..............
....bccccbbaa...............
.....aaaaaa.................
"""


FIST = """
..cdddcc..
.cdeedccb.
cdddddccbb
caaaadccbb
cdddaccbbb
caaaadcbba
cddddacbba
.caaaccbba
..bccbbba.
"""


def P(x, y):
    return (x + OX, y + OY)


def limb(c, a, ra, b, rb, ramp, sd=2, hl=1):
    return c.form(L(a[0], a[1], ra, b[0], b[1], rb), ramp, sd=sd, hl=hl)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def cuff(c, a, b, t0, t1, r, only):
    """gold band across a limb: slab perpendicular to a->b between t0..t1"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((px.X - a[0]) * dx + (px.Y - a[1]) * dy) / (dx * dx + dy * dy)
    m = (t >= t0) & (t <= t1) & L(a[0], a[1], r + 3, b[0], b[1], r + 3)
    if only is not None:
        m &= only
    else:
        m &= c.m
    c.form(m, GOLD, sd=1, hl=1)


def leg(c, hip, knee, ank, toe, ramp, far=False):
    """toe = x of toe tip (foot points left)"""
    p = C()
    th = limb(p, hip, 7.5, knee, 5.5, ramp, sd=4)
    # shin + calf
    shin = L(knee[0], knee[1], 5, ank[0], ank[1], 3.2)
    calf = E((knee[0] + ank[0]) / 2 + 2, (knee[1] + ank[1]) / 2 - 1, 4.5, 5)
    p.form(shin | calf, ramp, sd=3)
    # knee cap
    p.form(E(knee[0] - 1, knee[1], 3.5, 3.2), ramp, sd=1, hl=1)
    ax, ay = ank
    by = ay + 7  # ground contact handled by caller via ank y
    foot = PG([(ax + 4, ay), (ax + 4, by), (toe + 2, by), (toe, by - 2), (toe + 3, by - 4), (ax - 3, ay - 3)])
    p.form(foot, ramp, sd=2, hl=1)
    cuff(p, knee, ank, 0.62, 0.86, 3.6, shin)
    # claws
    for i in range(3):
        cx = toe + i * 3
        p.pxs([(cx, by), (cx, by - 1), (cx + 1, by)], 'b2')
    c.stamp(p, 'r0')


def club(c, hand, ang, ln=40, back=9):
    """iron studded kanabo through 'hand', ang = direction of tip (radians, 0=left, +=up)"""
    dx, dy = -math.cos(ang), -math.sin(ang)
    nx, ny = -dy, dx
    hx, hy = hand
    p = C()
    # handle
    e0 = (hx - dx * back, hy - dy * back)
    g1 = (hx + dx * 6, hy + dy * 6)
    p.form(L(e0[0], e0[1], 2.2, g1[0], g1[1], 2.2), ('w0', 'w1', 'w2'), sd=1, hl=1)
    p.form(E(e0[0], e0[1], 3, 3), ('i0', 'i1', 'i2'), sd=1, hl=1)
    # iron body
    b0 = (hx + dx * 7, hy + dy * 7)
    b1 = (hx + dx * ln, hy + dy * ln)
    body = L(b0[0], b0[1], 3.2, b1[0], b1[1], 5.6)
    # spikes on silhouette
    spikes = np.zeros_like(body)
    n = 5
    for i in range(n):
        t = 0.2 + 0.8 * i / (n - 1)
        q = lerp(b0, b1, t)
        r = 3.2 + (5.6 - 3.2) * t
        for s_ in (-1, 1):
            sx, sy = q[0] + nx * s_ * (r - 0.5), q[1] + ny * s_ * (r - 0.5)
            spikes |= L(sx, sy, 1.4, sx + nx * s_ * 3.2, sy + ny * s_ * 3.2, 0.5)
    spikes |= L(b1[0], b1[1], 1.5, b1[0] + dx * 8.4, b1[1] + dy * 8.4, 0.5)
    full = body | spikes
    p.form(full, ('i0', 'i1', 'i2'), sd=2, hl=0)
    p.form(body, ('i1', 'i2', 'i3'), sd=3, hl=0)
    # spec stripe on lit side (upper-left flank)
    sgn = -1 if (-nx - ny) > 0 else 1
    for (t0, t1) in ((0.12, 0.5), (0.58, 0.9)):
        q0, q1 = lerp(b0, b1, t0), lerp(b0, b1, t1)
        r0_, r1_ = 3.2 + 2.4 * t0 - 1.6, 3.2 + 2.4 * t1 - 1.6
        p.line([(q0[0] + nx * sgn * r0_, q0[1] + ny * sgn * r0_), (q1[0] + nx * sgn * r1_, q1[1] + ny * sgn * r1_)], 'i3', only=body)
    # studs: pyramid 2x2 light + L shadow
    for i in range(5):
        t = 0.14 + 0.8 * i / 4
        q = lerp(b0, b1, t)
        r = 3.2 + (5.6 - 3.2) * t
        off = -sgn * 0.35 * r
        sx, sy = int(round(q[0] + nx * off)), int(round(q[1] + ny * off))
        p.pxs([(sx + 1, sy - 1), (sx + 1, sy), (sx - 1, sy + 1), (sx, sy + 1), (sx + 1, sy + 1)], 'i0')
        p.pxs([(sx, sy), (sx - 1, sy), (sx, sy - 1), (sx - 1, sy - 1)], 'i3')
    # iron bands at the neck of the club
    for t in (0.0, 0.07):
        q = lerp(b0, b1, t)
        r = 3.4 + 2.4 * t
        bm = LN([(q[0] + nx * r, q[1] + ny * r), (q[0] - nx * r, q[1] - ny * r)])
        p.fill(bm, 'i0', only=body)
    c.stamp(p, 'K')


def fist(c, at, ramp, r=5.2, lines=True):
    x, y = at
    p = C()
    p.form(E(x, y, r, r - 0.4), ramp, sd=2, hl=1)
    c.stamp(p, 'r0')
    if lines:
        for i in (-2, 1):
            c.line([(x - 4, y + i), (x - 1, y + i)], ramp[0])


DEF = dict(
    bob=0, lean=0,
    fhip=(53, 75), fknee=(46, 85), fank=(48, 93), ftoe=37,
    nhip=(66, 75), nknee=(71, 85), nank=(69, 93), ntoe=57,
    fsh=(45, 54), felb=(37, 63), fhand=(29, 57), cang=math.radians(68),
    nsh=(72, 53), nelb=(80, 66), nwr=(71, 74),
    arm_behind_head=True, head=(0, 0), fore_behind=False,
)


CFG = dict(head=None, weapon=None, mane=True, cloth=('m0', 'm1', 'm2'))


def oni(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob = S['bob']; lean = S['lean']

    def B(pt, k=1.0):   # upper body point (bob + lean)
        return P(pt[0] + lean * k, pt[1] + bob - 2)

    hx, hy = S['head']
    HX, HY = P(34 + lean + hx, 20 + bob + hy)

    # ---- Mähne hinter dem Rücken (nur Mezu)
    if CFG['mane']:
        p = C()
        mp = [(54, 27), (62, 23), (70, 27), (77, 25), (73, 31), (82, 35), (76, 39), (84, 46), (77, 47), (81, 56),
              (74, 54), (74, 63), (68, 58), (63, 62), (56, 50)]
        mane = PG([B(q) for q in mp])
        p.form(mane, HAIR, sd=3, hl=0)
        for a_, b_ in [((64, 27), (75, 26)), ((67, 33), (80, 35.5)), ((69, 40), (81, 45)), ((70, 47), (79, 54)), ((69, 53), (73, 61))]:
            p.line([B(a_), B(b_)], 'h2', only=mane)
        c.stamp(p, 'K')

    def far_arm():
        sh_, el, ha = B(S['fsh']), B(S['felb']), B(S['fhand'])
        p = C()
        limb(p, sh_, 6.5, el, 5, FAR)
        c.stamp(p, 'r0')
        return sh_, el, ha

    def far_fore(el, ha):
        (CFG['weapon'] or club)(c, ha, S['cang'])
        p = C()
        fa = limb(p, el, 5, ha, 4, SK)
        cuff(p, el, ha, 0.5, 0.72, 4.4, fa)
        c.stamp(p, 'r0')
        p = C()
        p.grid(int(ha[0]) - 5, int(ha[1]) - 5, FIST, LEG)
        c.stamp(p, 'r0')

    if S['fore_behind']:
        sh_, el, ha = far_arm()
        far_fore(el, ha)
    elif S['arm_behind_head']:
        sh_, el, ha = far_arm()

    # ---- far leg
    leg(c, P(*S['fhip']), P(*S['fknee']), P(*S['fank']), S['ftoe'] + OX, FAR, far=True)

    # ---- torso
    p = C()
    chest = E(*B((58, 57)), 15.5, 11) | L(*B((57, 58)), 13, *P(59, 70), 10.5) | L(*B((50, 48)), 5, *B((66, 47)), 6)
    p.form(chest, SK, sd=5, hl=2)
    # abs: lines on the mid tone + small lights
    p.line([B((55, 62)), P(56, 68)], 'r0', only=chest)
    p.line([P(50, 63 + bob), P(55, 64 + bob), P(62, 63 + bob)], 'r1', only=chest)
    p.line([P(50, 66), P(55, 67), P(62, 66)], 'r1', only=chest)
    for (x, y) in [(51, 61.5), (58, 61.5)]:
        p.fill(R(*P(x, y + bob - 0.5), *P(x + 2, y + bob)), 'r3', only=chest)
    # pecs
    p.form(E(*B((61, 56)), 9.5, 6.5), SK, sd=2, hl=1, only=chest)
    p.form(E(*B((48.5, 57)), 5.5, 6), SK, sd=2, hl=1, only=chest)
    p.line([B((54, 52)), B((54, 61))], 'r0', only=chest)       # sternum
    p.line([B((53, 63)), B((57, 63)), B((66, 62)), B((70, 59))], 'r0', only=chest)  # under-pec line
    p.line([B((44, 62)), B((47, 63)), B((53, 63))], 'r0', only=chest)
    # serratus on shadow side
    for i in range(3):
        p.line([B((66 + i, 65 + i * 3)), B((69 + i * 0.5, 66 + i * 3))], 'r0', only=chest)
    # collar bone
    p.line([B((50, 50)), B((56, 51)), B((63, 50))], 'r1', only=chest)
    # specular on pecs
    p.fill(R(*B((56, 53)), *B((59, 53))), 'r4', only=chest)
    p.fill(R(*B((46, 54)), *B((48, 54))), 'r4', only=chest)
    c.stamp(p, 'r0')

    # ---- near leg
    leg(c, P(*S['nhip']), P(*S['nknee']), P(*S['nank']), S['ntoe'] + OX, SK)

    # ---- Lendentuch (grobes Tuch) mit Strickgürtel
    p = C()
    lo = PG([P(46, 69), P(72, 68), P(75, 77), P(72, 82), P(68, 78), P(64, 84), P(60, 79), P(56, 83), P(52, 78),
             P(48, 81), P(45, 75)])
    p.form(lo, CFG['cloth'], sd=3, hl=1)
    for (x0, y0, x1, y1) in [(52, 71, 51, 78), (60, 71, 60, 80), (67, 71, 68, 78)]:
        p.line([P(x0, y0), P(x1, y1)], CFG['cloth'][0], only=lo)
    belt = L(*P(46, 69), 1.8, *P(72, 68), 1.8)
    p.form(belt, ('o0', 'o1', 'o2'), sd=1, hl=1)
    for x in range(47, 72, 3):
        p.pxs([P(x, 69)], 'o0')
    knot = E(*P(49, 72), 2.2, 2.0) | L(*P(49, 72), 1.0, *P(47, 79), 0.8) | L(*P(50, 72), 1.0, *P(52, 80), 0.8)
    p.form(knot, ('o0', 'o1', 'o2'), sd=1, hl=1)
    c.stamp(p, 'K')

    # ---- head
    if not S['arm_behind_head']:
        pass
    CFG['head'](c, HX, HY, S)

    if S['fore_behind']:
        pass
    elif S['arm_behind_head']:
        far_fore(el, ha)
    else:
        sh_, el, ha = far_arm()
        far_fore(el, ha)

    # ---- near arm
    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    p = C()
    up = L(sh_[0], sh_[1] + 2, 6.5, el[0], el[1], 5.2)
    p.form(up, SK, sd=3, hl=1)
    mid = lerp(sh_, el, 0.55)
    p.form(E(mid[0] - 2.5, mid[1] + 0.5, 4.2, 5.2), SK, sd=2, hl=1, only=up | E(mid[0] - 2.5, mid[1] + 0.5, 4.2, 5.2))  # bicep
    p.form(E(sh_[0], sh_[1] - 1, 7.5, 7), SK, sd=2, hl=2)   # deltoid
    p.fill(R(sh_[0] - 4, sh_[1] - 5, sh_[0] - 1, sh_[1] - 5), 'r4')
    c.stamp(p, 'r0')
    p = C()
    fa = L(el[0], el[1], 5.2, wr[0], wr[1], 3.8)
    bulge = lerp(el, wr, 0.3)
    fa |= E(bulge[0], bulge[1] - 1, 5, 5)
    p.form(fa, SK, sd=3, hl=1)
    cuff(p, el, wr, 0.6, 0.8, 4.4, fa)
    c.stamp(p, 'r0')
    p = C()
    p.grid(int(wr[0]) - 7, int(wr[1]) - 5, FIST, LEG)
    c.stamp(p, 'r0')

    c.blacken()
    return c


R_ = math.radians
WALK = [
    dict(bob=1, fknee=(44, 85), fank=(42, 93), ftoe=31, nknee=(72, 85), nank=(75, 93), ntoe=63,
         nelb=(79, 66), nwr=(69, 73), fhand=(29, 58), cang=R_(66)),
    dict(bob=-1, fknee=(50, 85), fank=(51, 93), ftoe=40, nknee=(67, 84), nank=(69, 90), ntoe=57,
         nelb=(80, 66), nwr=(71, 74), fhand=(29, 56), cang=R_(69)),
    dict(bob=1, fknee=(55, 85), fank=(58, 93), ftoe=47, nknee=(64, 85), nank=(61, 93), ntoe=50,
         nelb=(81, 66), nwr=(74, 75), fhand=(30, 58), cang=R_(71)),
    dict(bob=-1, fknee=(48, 83), fank=(49, 90), ftoe=38, nknee=(70, 85), nank=(70, 93), ntoe=58,
         nelb=(80, 66), nwr=(72, 74), fhand=(29, 56), cang=R_(69)),
]
ATTACK = [
    dict(lean=2, bob=-1, fsh=(46, 52), felb=(35, 45), fhand=(31, 32), cang=R_(140), fore_behind=True,
         nelb=(79, 66), nwr=(68, 72), fknee=(47, 85), fank=(50, 93), ftoe=39, nknee=(72, 85), nank=(72, 93), ntoe=60),
    dict(lean=-4, bob=2, fsh=(45, 55), felb=(33, 60), fhand=(21, 62), cang=R_(-14), head=(0, 1),
         nelb=(82, 64), nwr=(79, 75), fknee=(42, 85), fank=(40, 93), ftoe=29, nknee=(72, 86), nank=(75, 93), ntoe=63),
    dict(lean=-2, bob=1, fsh=(45, 54), felb=(35, 62), fhand=(25, 60), cang=R_(24),
         nelb=(81, 65), nwr=(75, 75), fknee=(44, 85), fank=(44, 93), ftoe=33, nknee=(71, 85), nank=(72, 93), ntoe=60),
]


