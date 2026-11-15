"""Spielfiguren als Posen-Vorlagen (Seitenansicht, Blick nach links) im Cel-Stil."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sculpt import Canvas, cel

SKIN = cel('#f2c8a0', 12)
HAIR = cel('#2a2236', 14)
WHITE = cel('#f4f2ee', 10)
RED = cel('#d0303a', 18)
GOLD = cel('#e8c050', 16)
WOOD = cel('#8a5a32', 14)


def hana(pose=('walk', 0)):
    """Miko (Schreinmaid): weißes Haori, rote Hakama, langes schwarzes Haar, Gohei-Stab."""
    c = Canvas(48, 70, dict(skin=SKIN, hair=HAIR, white=WHITE, red=RED, gold=GOLD, wood=WOOD), ox=10, oy=6)
    # Haar hinten (lang, bis zur Hüfte)
    c.poly([(14, 8), (26, 6), (30, 14), (30, 36), (26, 40), (20, 36), (18, 18)], 'hair', bulge=0.6)
    # Beine / Hakama (weit, rot, plissiert)
    c.poly([(8, 34), (26, 34), (30, 58), (22, 59), (17, 56), (12, 59), (5, 58)], 'red', bulge=0.8)
    c.line(13, 38, 11, 57, '#7a1018'); c.line(19, 38, 19, 57, '#7a1018'); c.line(24, 38, 26, 57, '#7a1018')
    c.poly([(9, 58), (15, 58), (15, 61), (8, 61)], 'white', bulge=0.4)
    c.poly([(19, 58), (25, 58), (25, 61), (18, 61)], 'white', bulge=0.4)
    # Oberkörper: weißes Haori mit weiten Ärmeln
    c.poly([(9, 18), (24, 18), (27, 36), (7, 36)], 'white', bulge=0.9)
    c.line(16, 18, 13, 34, '#a8a8b8'); c.rect(8, 33, 26, 35, 'red', bulge=0.3)
    # Ärmel vorn, hält Gohei
    c.poly([(9, 20), (2, 30), (4, 38), (12, 36), (14, 26)], 'white', bulge=0.8)
    c.line(4, 37, 11, 35, '#c8303a')
    c.circle(3, 33, 2, 'skin', bulge=0.5)
    c.limb([(3, 40), (2, 12)], 2, 2, 'wood', bulge=0.4)
    for i, y in enumerate((12, 15, 18, 21)):
        c.dpoly([(2, y), (-3 - (i % 2), y + 2), (2, y + 3)], '#ffffff')
        c.line(2, y, -3 - (i % 2), y + 2, '#b8b8c8')
    # Kopf (realistischere Proportionen, ca. 1/4 Körperhöhe)
    c.ellipse(9, 2, 23, 19, 'skin')
    c.poly([(8, 9), (10, 1), (17, -1), (25, 2), (27, 10), (26, 20), (22, 12), (17, 6), (12, 7)], 'hair', bulge=0.6)
    c.line(11, 3, 16, 1, HAIR[3])
    # rotes Haarband (Mizuhiki) hinten
    c.rect(24, 9, 27, 12, 'red', bulge=0.3); c.line(25, 12, 27, 16, '#f0f0f0')
    # Gesicht
    c.line(11, 10, 14, 10, '#2a1a20')
    c.px(12, 11, '#2a1a20'); c.px(13, 11, '#4a3a6a'); c.px(11, 11, '#ffffff')
    c.px(9, 13, SKIN[1]); c.px(11, 15, '#c0605a'); c.px(12, 15, '#c0605a')
    c.px(14, 13, '#f0a0a0')
    return c.render()
