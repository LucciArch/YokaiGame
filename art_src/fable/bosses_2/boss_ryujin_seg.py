"""Ryujin body segment (~36 px) for chaining behind boss_ryujin_head. Body centre = cell (CX, CY), radius ~15.
Chain segments 18-22 px apart; draw tail-to-head so each segment overlaps the one behind it."""
from k2 import *

NAME = 'boss_ryujin_seg'
CW, CH = 64, 64
CX, CY = 30, 36
J_ = ('j0', 'j1', 'j2')
BL = ('c0', 'c1', 'c2')
MN = ('v0', 'v1', 'v2')

DEF = dict(dy=0, fin=0, shift=0, flare=0, glow=False)


def seg(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    cx, cy = CX, CY + S['dy']
    f = S['fin']; fl = S['flare']
    # dorsal mane (behind the body)
    for (x, a, ln, w) in [(-9, 292, 13, 8), (0, 300, 15, 9), (9, 308, 13, 8)]:
        p = C()
        m = lock((cx + x, cy - 11), a + f, ln + fl, w + fl * 0.3, 30)
        p.form(m, MN, sd=2, hl=1)
        c.stamp(p, 'K', skip=('v0', 'v1', 'v2', 'v3'))
    # body
    p = C()
    body = L(cx - 3, cy, 14.6, cx + 3, cy, 14.6)
    p.form(body, J_, sd=6, hl=1, sdir=(0, 1), hdir=(0, 1))
    belly = body & (px.Y > cy + 7)
    p.form(belly, BL, sd=2, hl=0)
    for x in (-14, -8, -2, 4, 10, 16):
        p.line([(cx + x, cy + 7), (cx + x + 1, cy + 15)], 'c0', only=belly)
    p.line([(cx - 18, cy + 7), (cx + 18, cy + 7)], 'j0', only=body)
    scales(p, body & ~belly, 'j0', ('j1',), 6, 4, light='j3', lon=('j2',), x0=(cx + S['shift']) % 6, y0=cy % 4)
    # wet glint on the top-left
    p.fill(R(cx - 9, cy - 11, cx - 5, cy - 11), 'j4' if S['glow'] else 'j3', only=body)
    if S['glow']:
        p.fill(R(cx - 11, cy - 8, cx - 10, cy - 6), 'j4', only=body)
    c.stamp(p, 'K')
    c.blacken()
    return c


WALK = [dict(dy=0, fin=0, shift=0), dict(dy=-1, fin=6, shift=2), dict(dy=0, fin=0, shift=3), dict(dy=1, fin=-6, shift=5)]
ATTACK = [dict(dy=1, fin=10, flare=-2), dict(dy=-1, fin=-12, flare=5, glow=True), dict(dy=0, fin=-4, flare=2)]

if __name__ == '__main__':
    export(NAME, seg, WALK, ATTACK)
    # chain test (review only): head + 5 segments on a wave
    import boss_ryujin_head as hd
    hc = hd.head(); him = hc.img()
    T = Image.new('RGBA', (300, 130), BG)
    sim = seg().img()
    pts = [(120 + i * 20, 62 + round(9 * math.sin(i * 0.9))) for i in range(7)]
    for (x, y) in pts[::-1]:
        T.alpha_composite(sim, (x - CX, y - CY))
    T.alpha_composite(him, (112 - (hd.OX + 60), 62 - (hd.OY + 35)))
    T.resize((900, 390), Image.NEAREST).save(D + '_review/ryujin_chain.png')
