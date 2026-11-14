"""Erzeugt icon.png aus der Pixel-Art von Hana."""
import os, sys
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygame
pygame.init()
pygame.display.set_mode((1, 1))
from yokai import gfx
S = 256
img = pygame.Surface((S, S), pygame.SRCALPHA)
pygame.draw.circle(img, (30, 16, 40), (S // 2, S // 2), S // 2 - 4)
pygame.draw.circle(img, (200, 50, 50), (S // 2, S // 2), S // 2 - 4, 10)
pygame.draw.circle(img, (250, 236, 210), (S // 2 + 50, S // 2 - 50), 46)
spr = pygame.transform.scale(gfx.sprite('hana'), (12 * 13, 14 * 13))
img.blit(spr, (S // 2 - spr.get_width() // 2, S // 2 - spr.get_height() // 2 + 12))
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'icon.png')
pygame.image.save(img, out)
print('icon gespeichert:', out)
