import sys, math
sys.path.insert(0, '/home/claude/fable_art')
from px import *
import px

CW, CH = 104, 88
OX, OY = 26, 14          # local baseline y=70
WH = ('v1', 'v2', 'v3')
RD = ('m1', 'm2', 'm3')
col('hb', '#1a1738'); px.add_rim('hb', 'xh')
HAIR = ('h0', 'hb', 'h2')
SKN = ('k1', 'k2', 'k3')

LEG = dict(zip('abcdmnoKeWrRsvw',
               ['k0', 'k1', 'k2', 'k3', 'h0', 'hb', 'h2', 'K', 'w1', 'v3', 'm2', 'm3', 'm1', 'v1', 'v2']))

HEAD = """
......mmmmmm
....mmnnnnnnmm
...mnoooonnnnnm
..mnoonnnnnnnnnm
..mnnnnnnnnnnnnm
.mnnnnnnnnnnnnnnm
.mnmnnmnnnmnnnnnm
.mcmccmccmnmnnnnm
.cmmcccmmmcmnnnnm
.cKKccKKKKcmnnnnm
.cKWccKeWbcmnnnnm
..ccbcccccbmnnnnm
..cccccccbbmmnnnm
...caaccbbmm.mnnm
...bcccbb.m..mnm
....bbba.....mm
"""

HAND = """
.ccc
cdcb
cacb
cccb
.bb
"""

SHIDE = """
..WWW
..WWW
..WWW
WWWWv
WWW
WWW
WWWWW
vvWWW
..WWW
..WWW
WWWWW
WWWvv
WWW
WWv
"""


def P(x, y):
    return (x + OX, y + OY)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


DEF = dict(
    bob=0, lean=0,
    nsh=(44, 29), nelb=(38, 37), nwr=(29, 32), wang=110,      # wand angle deg: 180=left, 90=up
    ffoot=30, nfoot=45, flift=0, nlift=0,
    hair=0, trail=(0, 0), sleeve=0, arm_back=False,
)


def hana(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    bob, lean = S['bob'], S['lean']

    def B(pt):
        return P(pt[0] + lean, pt[1] + bob)

    hs = S['hair']
    # ---- back hair (long tail, tied at the nape)
    p = C()
    tail = PG([B((43, 18)), B((48, 22)), B((52 + hs, 32)), B((54 + hs * 2, 42)), B((52 + hs * 2, 51)),
               B((50 + hs * 2, 46)), B((48 + hs * 2, 50)), B((46 + hs, 40)), B((43, 30))])
    p.form(tail, HAIR, sd=2, hl=0)
    p.line([B((47, 25)), B((50 + hs, 34)), B((51 + hs * 2, 45))], 'h2', only=tail)
    p.line([B((45, 28)), B((47 + hs, 38)), B((48 + hs * 2, 46))], 'h0', only=tail)
    c.stamp(p, 'K')

    # ---- far sleeve peeking behind the torso
    p = C()
    fs = PG([B((36, 28)), B((33, 33)), B((31, 42)), B((38, 44)), B((40, 30))])
    p.form(fs, ('v0', 'v1', 'v2'), sd=2, hl=1)
    c.stamp(p, 'K')

    # ---- feet (tabi + zori)
    for fx, lift in ((S['ffoot'], S['flift']), (S['nfoot'], S['nlift'])):
        p = C()
        x0, y0 = P(fx, 66 - lift)
        foot = PG([(x0, y0 + 2), (x0 + 2, y0), (x0 + 7, y0), (x0 + 7, y0 + 3), (x0, y0 + 3)])
        p.form(foot, WH, sd=1, hl=0)
        p.fill(R(x0, y0 + 3, x0 + 7, y0 + 3), 'w1')
        p.fill(R(x0 + 3, y0 + 1, x0 + 4, y0 + 1), 'm2')
        c.stamp(p, 'K')

    # ---- hakama
    p = C()
    f, n = S['ffoot'], S['nfoot']
    lo_, hi_ = (f, n) if f <= n else (n, f)
    ll, hl_ = (S['flift'], S['nlift']) if f <= n else (S['nlift'], S['flift'])
    ny_ = 66 - min(6, max(0, (hi_ - lo_ - 8) * 0.5))
    mid = ((lo_ + hi_) / 2 + 4, ny_)
    hk = PG([B((35, 38)), B((46, 38)), P(49, 50), P(hi_ + 9, 66 - hl_), P(hi_ - 1, 66 - hl_), P(*mid),
             P(lo_ + 8, 66 - ll), P(lo_ - 1, 66 - ll), P(32, 50)])
    p.form(hk, RD, sd=3, hl=1)
    for (a_, b_, col_) in [((38, 40), (lo_ + 3, 65), 'm1'), ((41, 40), (mid[0], mid[1] - 1), 'm0'), ((44, 40), (hi_ + 5, 65), 'm1'),
                           ((36.5, 41), (lo_ + 0.5, 62), 'm3'), ((42.5, 41), (hi_ + 2, 64), 'm3')]:
        p.line([B(a_), P(*b_)], col_, only=hk)
    p.fill(PG([B((45, 40)), B((47, 40)), B((47, 45))]), 'v2', only=hk)
    p.line([B((45, 40)), B((47, 46))], 'm0', only=hk)
    # waist tie
    p.form(R(*B((35, 37)), *B((46, 39))), RD, sd=1, hl=1)
    p.form(E(*B((37, 40)), 2, 2), RD, sd=1, hl=1)
    c.stamp(p, 'K')

    # ---- torso
    p = C()
    torso = L(*B((40, 30)), 5.6, *B((41, 36)), 5.2)
    p.form(torso, WH, sd=2, hl=1)
    p.line([B((36, 26)), B((40, 33))], 'm2', only=torso)
    p.line([B((37, 26)), B((41, 33))], 'v3', only=torso)
    p.line([B((44, 26)), B((40, 34)), B((40, 37))], 'v0', only=torso)
    c.stamp(p, 'K')
    # neck
    p = C()
    p.form(R(*B((38, 24)), *B((41, 26))), ('k0', 'k1', 'k2'), sd=1, hl=0)
    c.stamp(p, 'K', ring=False)

    # ---- gohei wand
    sh_, el, wr = B(S['nsh']), B(S['nelb']), B(S['nwr'])
    a = math.radians(S['wang'])
    dx, dy = math.cos(a), -math.sin(a)
    tip = (wr[0] + dx * 24, wr[1] + dy * 24)
    butt = (wr[0] - dx * 6, wr[1] - dy * 6)
    tx, ty = S['trail']
    def shide():
        p = C()
        p.form(L(*butt, 0.9, *tip, 0.9), ('w0', 'w1', 'w2'), sd=0, hl=1)
        c.stamp(p, 'K')
        # two separate paper strips: rear one (shaded, hangs lower) then the front one
        for k, (ox_, flip) in ((1, (-2, True)), (0, (-9, False))):
            p = C()
            lg = dict(LEG, W='v2', v='v1') if k else dict(LEG, W='v3', v='v1')
            p.grid(int(round(tip[0])) + ox_ + tx * (2 - k), int(round(tip[1])) + 1 + 3 * k + ty, SHIDE, lg, flip=flip)
            c.stamp(p, 'K')
        p = C()
        p.fill(E(tip[0], tip[1], 1.6, 1.6), 'v3')
        c.stamp(p, 'K')

    def near_arm():
        sv = S['sleeve']
        p = C()
        bag = PG([(el[0] + 3, el[1] - 3), (wr[0] + 2, wr[1] - 3), (wr[0], wr[1] + 3), (wr[0] + 1 + sv, wr[1] + 12),
                  (wr[0] + 3 + sv, wr[1] + 14), (el[0] + 1 + sv, el[1] + 10), (el[0] + 4, el[1] + 2)])
        p.form(bag, WH, sd=2, hl=1)
        p.line([(el[0] - 1, el[1]), (el[0] - 2 + sv, el[1] + 9)], 'v1', only=bag)
        p.line([(wr[0] + 5, wr[1] + 1), (wr[0] + 5 + sv, wr[1] + 9)], 'v1', only=bag)
        for k in range(4):
            p.fill(R(wr[0] + 2 + (k * sv) // 3, wr[1] + 2 + k * 3, wr[0] + 2 + (k * sv) // 3, wr[1] + 3 + k * 3), 'm2', only=bag)
        p.line([(wr[0] + 1, wr[1] - 2), (wr[0], wr[1] + 2)], 'v0', only=bag)
        c.stamp(p, 'K')
        p = C()
        up = L(sh_[0], sh_[1], 3.6, el[0] + 1, el[1] - 1, 3.8)
        p.form(up, WH, sd=2, hl=1)
        p.line([(sh_[0] - 2, sh_[1] + 1), (el[0], el[1] - 3)], 'v1', only=up)
        c.stamp(p, 'K')
        p = C()
        p.grid(int(wr[0]) - 3, int(wr[1]) - 2, HAND, LEG)
        c.stamp(p, 'K')

    # ---- head
    if S['arm_back']:
        shide()
        near_arm()
    p = C()
    p.grid(*B((30, 9)), HEAD, LEG)
    c.stamp(p, 'K', skip=('h0', 'hb', 'h2'))

    # ---- ribbon bow at the back of the head
    bx, by = B((45, 19))
    for pts in ([(bx, by), (bx + 6 + hs, by - 6), (bx + 8 + hs, by + 1)], [(bx, by + 1), (bx + 7 + hs, by + 3), (bx + 5 + hs, by + 9)]):
        p = C()
        p.form(PG(pts), RD, sd=1, hl=1)
        c.stamp(p, 'K')
    p = C()
    p.form(R(bx - 1, by - 1, bx + 1, by + 1), ('m0', 'm1', 'm2'), sd=1, hl=0)
    c.stamp(p, 'K')

    if not S['arm_back']:
        shide()
        near_arm()
    c.blacken()
    return c


WALK = [
    dict(bob=0, ffoot=26, nfoot=49, hair=1, sleeve=1),
    dict(bob=-1, ffoot=33, nfoot=42, nlift=2, hair=0),
    dict(bob=0, ffoot=40, nfoot=34, hair=1, sleeve=-1),
    dict(bob=-1, ffoot=33, flift=2, nfoot=41, hair=0),
]
ATTACK = [
    dict(lean=1, nelb=(50, 32), nwr=(53, 24), wang=62, hair=-1, ffoot=31, nfoot=45),
    dict(lean=-2, bob=1, nelb=(36, 32), nwr=(27, 35), wang=195, trail=(1, 0), ffoot=26, nfoot=47, hair=2, sleeve=2),
    dict(lean=-1, nelb=(38, 35), nwr=(30, 36), wang=150, ffoot=28, nfoot=46, hair=1),
]


def sheet(frames, path, scale=4):
    st = strip(frames, path)
    preview(st, path.replace('.png', '_preview.png'), scale)


if __name__ == '__main__':
    D = '/home/claude/fable_art/'
    c = hana()
    cr = crop_img(c.img())
    cr.save(D + 'hana.png')
    preview(cr, D + 'hana_preview.png', 8)
    print(cr.size)
    sheet([hana(**f).img() for f in WALK], D + 'hana_walk.png')
    sheet([hana(**f).img() for f in ATTACK], D + 'hana_attack.png')
