"""Kitsune-bi (enemy) - pink/orange fox-fire: a living flame with a fox mask, pointed ears and a curling tail."""
from common import *

NAME = 'kitsunebi_e'
CW, CH = 92, 64
OX, OY = 34, 12           # local: lowest hover point y = 44
FIRE = ('f1', 'f2', 'f3', 'y2', 'y3')

LEG = dict(zip('KZfqoy', ['K', 'y3', 'f0', 'q', 'f2', 'y2']))
# fox mask: slanted slit eyes (inner end lower), black nose at the snout tip, sly split mouth. Identical every frame.
FACE = """
.......KK.......KK
.....KKKK.....KKKK
....KZKK....KKZKK.
....KKK....KKKK...
...........KK.....
..................
KK................
KKK...............
.KfKKK............
...fqqKKK.........
.....fqqqK........
"""

DEF = dict(bob=0, fl=0, flare=0, ball=None, snout=0, ear=0, tail=0)


def P(x, y):
    return (x + OX, y + OY)


def kitsunebi(**kw):
    S = dict(DEF); S.update(kw)
    setsize(CW, CH)
    c = C()
    b, fl, fr = S['bob'], S['fl'], S['flare']

    def B(x, y):
        return P(x, y + b)

    # ---- tail: three flame tongues streaming back and curling up
    p = C()
    tail = wisp([B(27, 30), B(35, 31), B(42 + fr, 27), B(45 + fr, 20 - fl), B(42 + fr, 13 - fl * 2 - fr), B(37 + fl, 10 - fr * 2)], 6.2 + fr)
    tail |= wisp([B(29, 34), B(36, 37 + fl), B(42 + fr, 36 + fl), B(46 + fr * 2, 32 + fl * 2)], 4.0 + fr * 0.5)
    tail |= wisp([B(26, 33), B(29, 38), B(33 - fl, 42), B(38 - fl, 43 if not fr else 42)], 4.4)
    tail |= tongue(B(44 + fr, 24), B(51 + fr * 2, 17 - fl * 2), 2.6, -1.5)        # licks breaking off the curl
    tail |= tongue(B(40, 33), B(47 + fr, 41 + fl), 2.6, 1.5)
    flame(p, tail, FIRE, steps=(2, 2, 2), drift=(-1, 1))
    c.stamp(p, 'f0')

    # ---- head: skull of the flame + snout + two ear tongues
    p = C()
    skull = E(*B(20, 27), 10.4 + fr, 8.6 + fr)
    snout = PG([B(14, 22), B(3 - S['snout'], 30), B(4 - S['snout'], 32), B(14, 35), B(20, 30)])
    ear_n = tongue(B(25, 21), B(28 + fl, 5 - fr * 2 - S['ear']), 4.0, -1.5)
    ear_f = tongue(B(16, 20), B(14 - fl, 8 - fr * 2 - S['ear']), 3.2, 1.0)
    cheek = tongue(B(24, 33), B(31 + fr, 38 + fl), 3.4, 1)          # cheek-fur wisp
    head = skull | snout | ear_n | ear_f | cheek
    flame(p, head, FIRE, steps=(1, 2, 3, 3), drift=(0, 0))
    # dark inner ears, so the ears read as ears
    p.fill(erode(ear_n, 2) & (px.Y < B(0, 17)[1]), 'f0')
    # brow shadow: keeps the eyes in a darker socket band
    p.fill(E(*B(19, 24), 8.5, 3.2) & skull, 'f2')
    p.grid(*B(3 - S['snout'], 21), FACE, LEG) if S['snout'] == 0 else None
    if S['snout']:
        p.grid(*B(3, 21), FACE.replace('KK................', '..................').replace('KKK...............', '..................')
               .replace('.KfKKK', '...KKK'), LEG)
        p.grid(*B(3 - S['snout'], 27), "KK\nKKK\n.Kf", LEG)
    c.stamp(p, 'f0')
    c.fill(R(*B(15, 17), *B(17, 17)), 'y3')
    # loose embers drifting up behind the ears
    e1_ = B(33 + fl, 16 - fl * 2)
    c.fill(R(e1_[0], e1_[1], e1_[0] + 1, e1_[1] + 1), 'f3'); c.fill(R(e1_[0], e1_[1] + 2, e1_[0] + 1, e1_[1] + 2), 'f1')                         # hot glint on the brow

    # ---- thrown fox-fire
    if S['ball']:
        bx, by, r = S['ball']
        p = C()
        m = E(*P(bx, by), r, r) | tongue(P(bx + 1, by), P(bx + r * 2.6, by - r * 0.9), r * 0.8, -1) \
            | tongue(P(bx, by - 1), P(bx + r * 1.2, by - r * 2.0), r * 0.6, 1)
        flame(p, m, FIRE, steps=(1, 1, 1, 1))
        c.stamp(p, 'f0')

    c.blacken()
    return c


WALK = [dict(bob=0, fl=0), dict(bob=-1, fl=1), dict(bob=0, fl=0, ear=1), dict(bob=1, fl=-1)]
ATTACK = [
    dict(flare=1, fl=1, bob=-1, ball=(2, 14, 2.6)),            # gathers a spark above the snout
    dict(flare=2, fl=-1, bob=1, snout=2, ball=(-22, 30, 4.4)),   # spits it forward, whole flame flares
    dict(flare=0, fl=0, bob=0, ear=-1),
]

if __name__ == '__main__':
    export(NAME, kitsunebi, WALK, ATTACK)
    zoom(NAME)
