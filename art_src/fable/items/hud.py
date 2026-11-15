"""HUD icons, 32x32 static."""
from common import *
from icons_1 import mon
import pickups as P
import px


def heart_half():
    c = G(P.HEART)
    c.remap(P.EMPTY, only=px.X >= 16)
    return c


def build():
    save('hud', 'heart_full', P.heart(0))
    save('hud', 'heart_half', heart_half())
    save('hud', 'heart_empty', G(P.HEART, tr=P.EMPTY))
    save('hud', 'heart_soul', P.heart(0, tr=P.SOUL))
    save('hud', 'coin', mon(10.6))
    save('hud', 'key', P.key(0))
    save('hud', 'salt', P.salt(0))


if __name__ == '__main__':
    build()
