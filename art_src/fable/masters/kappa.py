import sys, math
sys.path.insert(0, '/home/claude/fable_art')
from px import *
import px

CW, CH = 96, 80
OX, OY = 14, 7          # local baseline y=70
G = ('g1', 'g2', 'g3')
GF = ('g0', 'g1', 'g2')
SH = ('s0', 's1', 's2')
BL = ('c0', 'c1', 'c2')

LEG = dict(zip('abcdemnouvwxYWKsrR123',
               ['g0', 'g1', 'g2', 'g3', 'g4', 'h0', 'h1', 'h2', 'y0', 'y1', 'y2', 'y3', 'y2', 'v3', 'K',
                'c0', 'c1', 'c2', 'a0', 'a1', 'a2']))

HEAD = """
...........sRRRRRRRs
.........sR2233W2222Rs
........mrR2222222111Rrm
.......mnrrRRRRRRRRRRrrnm
......mnonmrrrrrrrrrrmnnnm
......mnomnmmnommnmonmnonm
.....mnmdnmddmoddmnccmnnom
.....mnddmdeddmddcmcccmnnm
.....mcdeedddKKKKcmnccbmnom
.....cdddKKKKKKaccmncbbmnnm
...vwwvKKKYKYYaccccmcbba
.vwxxwwvaWYKYYacccccbbba
vwwwuuwvaaYYaabccccbbbba
vwvvvvvuucaacddcccccbbba
uvKKKKKKKKcddcccccbbbaa
uu.vvvvuubcccccccbbbaa
....uuuuuabccccccbbbaa
.........aabcccccbbbaa
...........aabbccbbbaa
.............aabbbbaa
"""


def erode(m, n=1):
    for _ in range(n):
        m = m & sh(m, 1, 0) & sh(m, -1, 0) & sh(m, 0, 1) & sh(m, 0, -1)
    return m


def P(x, y):
    return (x + OX, y + OY)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def hand(c, wr, ang, ramp, spread=30, ln=6.0):
    """webbed 3-claw hand; ang in degrees: 180=left, 90=down (screen coords)"""
    p = C()
    tips = []
    for da in (-spread, 0, spread):
        a = math.radians(ang + da)
        tips.append((wr[0] + math.cos(a) * ln, wr[1] + math.sin(a) * ln))
    web = PG([wr] + [lerp(wr, t, 0.75) for t in tips])
    p.fill(web | E(wr[0], wr[1], 2.4, 2.4), ramp[0])
    for t in tips:
        p.fill(L(wr[0], wr[1], 1.3, t[0], t[1], 0.8), ramp[1])
    p.fill(E(wr[0] - 0.5, wr[1] - 0.5, 1.6, 1.6), ramp[2])
    for t, da in zip(tips, (-spread, 0, spread)):
        a = math.radians(ang + da)
        e = (t[0] + math.cos(a) * 1.6, t[1] + math.sin(a) * 1.6)
        p.fill(LN([t, e]), 'b2')
    c.stamp(p, 'g0')


def arm(c, sh_, el, wr, ang, ramp, spread=30):
    hand(c, wr, ang, ramp, spread)
    p = C()
    p.form(L(el[0], el[1], 2.3, wr[0], wr[1], 1.7), ramp, sd=1, hl=1)
    c.stamp(p, 'g0')
    p = C()
    p.form(L(sh_[0], sh_[1], 2.8, el[0], el[1], 2.2), ramp, sd=1, hl=1)
    p.form(E(sh_[0], sh_[1], 3.6, 3.4), ramp, sd=1, hl=1)
    c.stamp(p, 'g0')


def leg(c, hip, knee, ank, toe, ramp, lift=0):
    p = C()
    p.form(L(hip[0], hip[1], 4.8, knee[0], knee[1], 3.2), ramp, sd=3, hl=1)
    p.form(L(knee[0], knee[1], 2.8, ank[0], ank[1], 2.1), ramp, sd=2, hl=1)
    mx, my = int((hip[0] + knee[0]) / 2), int((hip[1] + knee[1]) / 2)
    for (qx, qy) in [(mx + 1, my - 1), (mx - 2, my + 1)]:
        if p.a[qy, qx] == I(ramp[1]) and p.a[qy, qx + 1] == I(ramp[1]):
            p.pxs([(qx, qy), (qx + 1, qy)], ramp[0])
    ax, ay = ank
    by = ay + 4
    foot = PG([(ax + 2, ay - 1), (ax + 3, by), (toe + 1, by), (toe, by - 1), (toe + 4, by - 3), (ax - 2, ay - 2)])
    p.form(foot, ramp, sd=2, hl=1)
    # web lines
    p.line([(toe + 4, by - 2), (toe + 7, by)], ramp[0], only=foot)
    c.stamp(p, 'g0')
    for i in range(3):
        c.pxs([(toe - 1 + i * 4, by), (toe + i * 4, by)], 'b3')


DEF = dict(
    bob=0, lean=0,
    fsh=(41, 41), felb=(31, 46), fwr=(21, 43), fang=172, fspread=32,
    nsh=(46, 41), nelb=(40, 52), nwr=(29, 53), nang=168, nspread=30,
    fhip=(47, 56), fknee=(38, 60), fank=(39, 65), ftoe=28,
    nhip=(52, 56), nknee=(50, 62), nank=(55, 65), ntoe=45,
    near_behind=False,
)


def kappa(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    # far arm
    arm(c, B(S['fsh']), B(S['felb']), B(S['fwr']), S['fang'], GF, S['fspread'])
    # far leg
    leg(c, P(*S['fhip']), P(*S['fknee']), P(*S['fank']), S['ftoe'] + OX, GF)

    # shell: voronoi scutes (each plate its own little form), dark seams, big core shadow bottom-right
    p = C()
    shell = L(*B((53, 32)), 8, *B((58, 50)), 9.5)
    seeds = [(55, 34), (57, 42), (59, 51), (62, 28), (65, 35), (67, 43), (67, 51), (63, 58), (50, 27), (57, 24),
             (49, 37), (51, 47), (54, 58)]
    d = np.stack([(px.X - B(q)[0]) ** 2 + (px.Y - B(q)[1]) ** 2 for q in seeds])
    cid = d.argmin(0)
    p.fill(shell, 's0')
    seam = (cid != np.roll(cid, -1, 1)) | (cid != np.roll(cid, -1, 0))
    for k in range(len(seeds)):
        cell = shell & (cid == k) & ~seam
        p.form(cell, ('s1', 's2', 's3'), sd=1, hl=1 if k < 3 else 0)
    core = shell & ~sh(shell, -5, -5)
    for hi_, lo_ in (('s1', 's0'), ('s2', 's1'), ('s3', 's2')):
        p.a[core & (p.a == I(hi_))] = I(lo_)
    c.stamp(p, 'K')

    # torso
    p = C()
    torso = L(*B((45, 42)), 6.8, *P(50, 55), 6.5)
    p.form(torso, G, sd=4, hl=1)
    belly = torso & ~L(*B((55, 36)), 6, *P(59, 58), 6)
    belly &= sh(torso, 1, 0) & (px.Y > B((0, 39))[1])
    p.form(belly, BL, sd=2, hl=0)
    for y in (45, 49, 53, 57):
        p.line([P(35 + lean, y + bob), P(50 + lean, y + bob + 2)], 'c0', only=belly)
    for (qx, qy) in [(49, 44), (51, 48), (48, 50)]:
        q = B((qx, qy))
        if p.a[q[1], q[0]] == I('g2') and p.a[q[1], q[0] + 1] == I('g2'):
            p.pxs([q, (q[0] + 1, q[1])], 'g1')
    c.stamp(p, 'g0')

    if S['near_behind']:
        arm(c, B(S['nsh']), B(S['nelb']), B(S['nwr']), S['nang'], G, S['nspread'])

    # near leg
    leg(c, P(*S['nhip']), P(*S['nknee']), P(*S['nank']), S['ntoe'] + OX, G)

    # head: wet strands first (they hang behind the skull), then the face grid
    p = C()
    hx, hy = B((17, 16))
    for pts, hi in [([(23, 6), (24, 10), (24, 15)], 9), ([(25, 5), (27, 10), (27, 17)], 12), ([(27, 5), (29, 9), (30, 13)], 8),
                    ([(22, 7), (22, 12)], 0)]:
        q = [(hx + a_, hy + b_) for a_, b_ in pts]
        p.line(q, 'h1')
        p.line([(a_ + 1, b_) for a_, b_ in q[:2]], 'h1')
        if hi:
            p.pxs([(hx + pts[1][0], hy + hi), (hx + pts[1][0], hy + hi + 1)], 'h2')
    p.grid(hx, hy, HEAD, LEG)
    c.stamp(p, 'K')

    if not S['near_behind']:
        arm(c, B(S['nsh']), B(S['nelb']), B(S['nwr']), S['nang'], G, S['nspread'])

    c.blacken()
    return c


WALK = [
    dict(bob=1, fknee=(37, 61), fank=(38, 65), ftoe=26, nknee=(50, 62), nank=(57, 65), ntoe=46,
         nelb=(44, 52), nwr=(40, 60), nang=110, felb=(31, 49), fwr=(23, 53)),
    dict(bob=0, fknee=(41, 60), fank=(45, 65), ftoe=33, nknee=(47, 59), nank=(53, 62), ntoe=41,
         nelb=(42, 52), nwr=(36, 59)),
    dict(bob=1, fknee=(45, 61), fank=(51, 65), ftoe=40, nknee=(43, 61), nank=(45, 65), ntoe=33,
         nelb=(40, 51), nwr=(32, 57), nang=135, felb=(33, 49), fwr=(27, 54), fang=150),
    dict(bob=0, fknee=(39, 58), fank=(43, 62), ftoe=31, nknee=(47, 61), nank=(53, 65), ntoe=41,
         nelb=(42, 52), nwr=(36, 59)),
]
ATTACK = [
    dict(lean=2, bob=0, nelb=(52, 36), nwr=(50, 25), nang=250, nspread=36,
         felb=(34, 50), fwr=(28, 55), fang=140),
    dict(lean=-4, bob=2, nelb=(34, 43), nwr=(22, 44), nang=185, nspread=40,
         felb=(34, 52), fwr=(30, 59), fang=120, fknee=(36, 61), fank=(37, 65), ftoe=25),
    dict(lean=-2, bob=1, nelb=(38, 49), nwr=(29, 54), nang=150,
         felb=(33, 50), fwr=(26, 55), fang=150, fknee=(38, 61), fank=(41, 65), ftoe=29),
]


def sheet(frames, path, scale=4):
    st = strip(frames, path)
    preview(st, path.replace('.png', '_preview.png'), scale)


if __name__ == '__main__':
    D = '/home/claude/fable_art/'
    c = kappa()
    cr = crop_img(c.img())
    cr.save(D + 'kappa.png')
    preview(cr, D + 'kappa_preview.png', 8)
    print(cr.size)
    sheet([kappa(**f).img() for f in WALK], D + 'kappa_walk.png')
    sheet([kappa(**f).img() for f in ATTACK], D + 'kappa_attack.png')
