"""Projectiles: 2-frame strips 32x16 (frames 16x16), flying LEFT."""
from common import *
import px

OFUDA = (r"""
.WWWWWWWWWWWw
WWRRWRWRRRWwv
WWRWWRWRWRWwv
WWRRWRRRWRWwv
WWWWWWWWWWwwv
.wwwwwwwwwwvv
""", r"""
.WWWWWW......
WWRRWRWWWWWw.
WWRWWRWRRRWwv
WWRRWRRRWRWwv
WWWWWWWRWRWwv
.wwwwwWWWWwwv
......wwwwwvv
""")

FIRE = (r"""
....RRRRR.....
..RRMMMMRRR..R
.RMMyyyyMMRRR.
RMMyYYYYyMMMRR
RMyYYWWYYyMMRr
RMMyYYYYyMMRR.
.RMMyyyyMMRR.r
..RRMMMMRRr...
....RRRRr.....
""", r"""
....RRRRR...R.
..RRMMMMRR....
.RMMyyyyMMRRr.
RMyYYYYYyMMMRR
RMyYWWWYYyMRRr
RMyYYYYYyMMRRr
.RMMyyyyMMRR..
..RRMMMMRR..r.
....RRRRr.....
""")


def orb(ramp, f):
    c = Cv(16, 16)
    d0, d1, d2, d3 = ramp
    c.fill(E(7.5, 7.5, 6.2, 6.2), d0)
    c.fill(E(7.5, 7.5, 5.0 + 0.5 * f, 5.0 + 0.5 * f), d1)
    c.fill(E(7.0, 7.0, 3.4 + 0.7 * f, 3.4 + 0.7 * f), d2)
    c.fill(E(6.5, 6.5, 1.6 + 0.6 * f, 1.6 + 0.6 * f), d3)
    return c


def build():
    save('projectiles', 'ofuda', [G(t, 16, 16) for t in OFUDA])
    save('projectiles', 'orb_red', [orb('rRMY', f) for f in (0, 1)])
    save('projectiles', 'orb_purple', [orb('xpPX', f) for f in (0, 1)])
    save('projectiles', 'orb_blue', [orb('zaAW', f) for f in (0, 1)])
    save('projectiles', 'fireball', [G(t, 16, 16) for t in FIRE])


if __name__ == '__main__':
    build()
