"""Tsuchigumo: giant earth spider, hairy brown legs, tiger-striped abdomen, a cluster of red eyes."""
from kit import *
import px

NAME = 'tsuchigumo'
CW, CH = 168, 116
OX, OY = 40, 26            # local baseline y=80
TIG = ('t0', 't1', 't2')

LEG = dict(zip('abcdKRrZvwxq', ['s0', 's0', 's1', 's2', 'K', 'e1', 'e0', 'y3', 'b1', 'b2', 'b3', 'q']))
HEAD = """
.....bbccccbb....
...bccddddcccbb..
..bcdddccccccccb.
.bcdKKKccKKKccccb
.bcKRRZKKRRZKcccb
bccKRRRKKRRRKcccb
bcccKKKccKKKKKccb
bcKKKcKKKcKRZKccb
bcKRZKKRZKcKKKcbb
bccKKccKKccccbbba
.bbccccccccbbbbaa
.abKKKKKKKbbbaaa.
..bcqqqqcbaaa....
.bccb..bccb......
.bcba..bcba......
.abwx..abwx......
..awx...awx......
...wx....wx......
...w.....w.......
"""

HIPS = [(-3, 3), (1, 5), (6, 5), (10, 3)]
KN = [(-30, -34), (-9, -30), (15, -31), (36, -40)]          # near knees, relative to the cephalothorax
KF = [(-20, -25), (-3, -25), (23, -25), (41, -31)]          # far knees
NEAR0 = [(0, 80), (45, 80), (73, 80), (110, 80)]
FAR0 = [(13, 80), (53, 80), (85, 80), (101, 80)]
DEF = dict(cth=(50, 53), abd=(83, 46), tilt=0, near=NEAR0, far=FAR0, nk=[0, 0, 0, 0], fk=[0, 0, 0, 0])


def P(x, y):
    return (x + OX, y + OY)


def leg(c, hip, foot, ramp, knee):
    dx, dy = foot[0] - knee[0], foot[1] - knee[1]
    ln = math.hypot(dx, dy)
    ank = (knee[0] + dx * 0.72, knee[1] + dy * 0.72)
    # tibia + tarsus (in front of nothing: drawn first), then femur over the knee
    p = C()
    tb = L(knee[0], knee[1], 2.3, ank[0], ank[1], 1.7)
    ts = L(ank[0], ank[1], 1.5, foot[0], foot[1] - 1, 1.0)
    p.form(tb | ts, ramp, sd=1, hl=1)
    # dark bands on the shin
    for t in (0.3, 0.55):
        q = (knee[0] + dx * t, knee[1] + dy * t)
        p.fill(L(q[0], q[1], 2.8, q[0] + dx / ln * 1.5, q[1] + dy / ln * 1.5, 2.8) & (tb | ts), ramp[0])
    # bristles on the outer side
    ox_ = -1 if foot[0] < hip[0] else 1
    for t in (0.3, 0.7):
        q = (knee[0] + dx * t, knee[1] + dy * t)
        p.line([q, (q[0] + ox_ * 3.4, q[1] - 1.5)], ramp[0])
    p.fill(L(foot[0], foot[1] - 2, 1.0, foot[0] + (-1 if ox_ < 0 else 1), foot[1], 0.7), 'b2')   # claw
    c.stamp(p, 'K')
    p = C()
    fm = L(hip[0], hip[1], 3.3, knee[0], knee[1], 2.5)
    p.form(fm, ramp, sd=1, hl=1)
    fx, fy = knee[0] - hip[0], knee[1] - hip[1]
    for t in (0.55,):
        q = (hip[0] + fx * t, hip[1] + fy * t)
        p.line([q, (q[0] + ox_ * 3.6, q[1] - 2.0)], ramp[0])
    p.form(E(knee[0], knee[1], 3.2, 3.0), ramp, sd=1, hl=1)       # knee joint
    c.stamp(p, 'K')


def knee_of(S, which, i, cx, cy):
    ex = (S['nk'] if which == 'near' else S['fk'])[i]
    if ex:
        return P(*ex)
    base = (KN if which == 'near' else KF)[i]
    d0 = (NEAR0 if which == 'near' else FAR0)[i]
    f = S[which][i]
    return (cx + base[0] + (f[0] - d0[0]) * 0.45, cy + base[1] - (d0[1] - f[1]) * 0.6)


def spider(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx, cy = P(*S['cth'])
    ax, ay = P(*S['abd'])
    # ---- far legs
    for i in (3, 0, 2, 1):
        h = HIPS[i]
        leg(c, (cx + h[0] + 3, cy + h[1] - 3), P(*S['far'][i]), BRNF, knee_of(S, 'far', i, cx, cy))

    # ---- hintere nahe Beine HINTER den Hinterleib (sonst verdecken sie ihn)
    for i in (3, 2):
        h = HIPS[i]
        leg(c, (cx + h[0], cy + h[1]), P(*S['near'][i]), BRN, knee_of(S, 'near', i, cx, cy))
    # ---- abdomen: tiger pelt
    p = C()
    ab = E(ax, ay, 24.4, 19.4) | E(ax + 12, ay + 3, 15, 14)
    p.form(ab, TIG, sd=6, hl=2)
    for k, sx in enumerate(range(-18, 26, 7)):
        top_y = ay - 19
        st = PG([(ax + sx, top_y), (ax + sx + 4, top_y), (ax + sx + 3 + (k % 2) * 2, ay - 2 + (k % 3) * 3), (ax + sx + 1, ay + 3 + (k % 2) * 4)])
        p.fill(st, 'K', only=ab)
        st2 = PG([(ax + sx + 3, ay + 20), (ax + sx + 6, ay + 20), (ax + sx + 5, ay + 8 - (k % 2) * 3)])
        p.fill(st2, 'K', only=ab)
    # pale belly fur underneath
    und = ab & ~sh(ab, 0, -3) & (px.Y > ay + 6)
    p.a[und & (p.a != I('K'))] = I('t0')
    # spinneret
    p.form(E(ax + 25, ay + 8, 3.2, 2.6), BRN, sd=1, hl=1)
    c.stamp(p, 'K')
    # waist
    p = C()
    p.form(L(cx + 10, cy - 1, 5, ax - 18, ay + 3, 6), BRNF, sd=2, hl=0)
    c.stamp(p, 'K')

    # ---- cephalothorax: hairy brown carapace with a spiky mane
    p = C()
    ct = E(cx, cy, 15.4, 11.4)
    spikes = np.zeros_like(ct)
    for sx, hgt in ((-9, 4), (-4, 6), (1, 7), (6, 6), (11, 5), (15, 3)):
        spikes |= PG([(cx + sx - 2, cy - 7), (cx + sx + 2, cy - 12 - hgt + abs(sx) * 0.3), (cx + sx + 3, cy - 6)])
    p.form(ct | spikes, BRN, sd=4, hl=1)
    for q in ((2, -3), (8, 1), (-1, 3), (6, 6), (11, -4)):
        p.fill(R(cx + q[0], cy + q[1], cx + q[0] + 1, cy + q[1]), 's1')
    c.stamp(p, 'K')

    # ---- head
    p = C()
    p.grid(cx - 28, cy - 5 + S['tilt'], HEAD, LEG)
    c.stamp(p, 'K')
    for i in (1, 0):
        h = HIPS[i]
        leg(c, (cx + h[0], cy + h[1]), P(*S['near'][i]), BRN, knee_of(S, 'near', i, cx, cy))
    c.blacken()
    return c


def step(a, b, la=0, lb=0, bob=0):
    """set A = near 0,2 + far 1,3 ; set B = near 1,3 + far 0,2. a/b = x shift, la/lb = lift"""
    near = [(x + (a if i % 2 == 0 else b), y - (la if i % 2 == 0 else lb)) for i, (x, y) in enumerate(NEAR0)]
    far = [(x + (b if i % 2 == 0 else a), y - (lb if i % 2 == 0 else la)) for i, (x, y) in enumerate(FAR0)]
    return dict(near=near, far=far, cth=(50, 53 + bob), abd=(83, 46 + bob))


WALK = [step(-5, 5), step(0, 0, 0, 5, 1), step(5, -5), step(0, 0, 5, 0, 1)]
ATTACK = [
    # rear up: front pairs lifted high, fangs bared
    dict(cth=(56, 42), abd=(88, 50), tilt=-2, near=[(18, -4), (14, 22), (76, 80), (112, 80)], far=[(34, -10), (26, 12), (88, 80), (103, 80)],
         nk=[(38, 6), (32, 28), 0, 0], fk=[(50, 2), (44, 22), 0, 0]),
    # strike: body slams forward, front legs stab down
    dict(cth=(40, 57), abd=(74, 47), tilt=1, near=[(-26, 80), (36, 80), (68, 80), (104, 80)], far=[(-18, 72), (-8, 80), (80, 80), (95, 80)],
         nk=[(2, 36), (30, 28), 0, 0], fk=[(8, 40), (16, 38), 0, 0]),
    dict(cth=(47, 54), abd=(80, 46), near=[(-6, 80), (42, 80), (71, 80), (108, 80)], far=[(6, 78), (50, 80), (83, 80), (99, 80)]),
]

if __name__ == '__main__':
    export(NAME, spider, WALK, ATTACK, review=3)
