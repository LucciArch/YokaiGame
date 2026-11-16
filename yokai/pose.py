"""Gesten der Figuren: auf dem Podest der Charakterauswahl und einmal zu Beginn jedes Laufs."""
import math
import random
import pygame
from . import gfx


# ---------------------------------------------------------------- Gesten der Charakterauswahl
POSE_ATK = ('hana', 'kenji', 'kuzunoha', 'kotaro', 'seimei', 'susanoo')    # zeigen ihr Wurf-/Hiebbild
POSE_HOP = {'ponpoko': 6, 'benkei': 11, 'akago': 7}                        # springen und landen


def pose_motion(cid, t):
    """(Bildnummer oder None, Versatz nach oben) der Geste kurz nach dem Wechsel auf eine Figur."""
    if cid in POSE_ATK and t < 0.3:
        return 4 + int(t / 0.1), 0
    if cid in POSE_HOP and t < 0.32:
        return 0, -int(POSE_HOP[cid] * math.sin(math.pi * t / 0.32))
    if cid == 'okiku':                                   # schwebt aus dem Brunnen höher und bleibt dort
        return None, -int(10 * (1 - math.exp(-t * 4)) + 2 * math.sin(t * 2.2))
    return None, 0


_G = (1, 1.0, 0, 0)                                      # Maßstab, Ausblenden, Ankerpunkt der laufenden Geste
_small = {}


def _fx(name, x, y, alpha=255):
    k, fade, ax, ay = _G
    im = gfx.env_img('_title', name)[0]
    if k != 1:                                           # Versätze sind für die Podestgröße geschrieben
        x, y = ax + (x - ax) * k, ay + (y - ay) * k
        im = _small.get(name) or _small.setdefault(name, pygame.transform.scale_by(im, k))
    alpha *= fade
    if alpha > 0:
        gfx.hi_blit(im, x, y + im.get_height() / 4, max(0, min(255, int(alpha))))


def _burst(name, n, t, ox, oy, a0, a1, v0, v1, grav, dur, seed):
    """n Teilchen fliegen aus (ox, oy) in Winkeln a0..a1, fallen mit grav und verblassen bis dur."""
    if not 0 < t < dur:
        return
    rng = random.Random(seed)
    for _ in range(n):
        a, v = rng.uniform(a0, a1), rng.uniform(v0, v1)
        _fx(name, ox + math.cos(a) * v * t, oy + math.sin(a) * v * t + grav * t * t / 2, 255 * min(1, 3 * (1 - t / dur)))


def pose_fx(s, cid, t, px, fb, k=1, fade=1.0):
    """Effekte der Geste vor der Figur; fb = Fußlinie der Figur auf dem Podest.
    k = 0.5 im Spiel (Figur halb so groß wie auf dem Podest): Versätze und Bilder schrumpfen mit."""
    global _G
    _G = (k, fade, px, fb)
    P = math.pi
    if cid == 'hana':                                    # Kagura-Glöckchen streuen kreisende Goldfunken
        for k in range(6):
            a = t * 3 + k * P / 3
            _fx('fx_spark', px + math.cos(a) * 30, fb - 36 + math.sin(a) * 10 - t * 14, 255 * min(1, 2 * (1.4 - t)))
    elif cid == 'kenji':                                 # Glanz wandert über die gezogene Klinge
        if 0.15 < t < 0.7:
            _fx('fx_glint', px + 14 + (t - 0.15) * 40, fb - 46, 255 * min(1, 3 * (0.7 - t)))
    elif cid == 'kuzunoha':                              # drei Fuchsfeuer umkreisen sie, solange sie gewählt ist
        for k in range(3):
            a = t * 1.6 + k * 2 * P / 3
            _fx('fx_fire_b', px + math.cos(a) * 34, fb - 30 + math.sin(a) * 9 + 2 * math.sin(t * 7 + k), 230 * min(1, t * 2))
    elif cid == 'ponpoko':                               # Verwandlungsrauch, ein Blatt schaukelt herab
        _burst('fx_smoke', 7, t - 0.2, px, fb - 26, 0, 2 * P, 25, 45, -10, 0.7, 7)
        if t < 2.2:
            _fx('fx_leaf', px + 12 * math.sin(t * 4), fb - 86 + t * 34, 255 * min(1, 3 * (2.2 - t)))
    elif cid == 'benkei':                                # Landung wirbelt Staub zu beiden Seiten auf
        _burst('fx_dust', 3, t - 0.32, px - 16, fb - 4, P - 0.35, P + 0.1, 40, 70, 30, 0.6, 3)
        _burst('fx_dust', 3, t - 0.32, px + 16, fb - 4, -0.1, 0.35, 40, 70, 30, 0.6, 4)
    elif cid == 'okiku':                                 # Brunnenwasser tropft vom Saum
        for k in range(3):
            u = (t * 0.8 + k / 3) % 1
            _fx('fx_drop', px - 12 + k * 12, fb - 12 + u * 22, 255 * (1 - u) * min(1, t * 2))
    elif cid == 'kotaro':                                # Flügelschlag wirbelt Federn hoch
        _burst('fx_feather', 7, t - 0.05, px, fb - 34, -P, 0, 40, 85, 70, 1.5, 11)
    elif cid == 'seimei':                                # fünf Ofuda fächern sich über ihm auf
        r = 40 * min(1, t / 0.35) ** 0.5
        for k in range(5):
            a = -P / 2 + (k - 2) * 0.5
            _fx('fx_ofuda', px + math.cos(a) * r, fb - 34 + math.sin(a) * r, 255 * min(1, 2 * (1.6 - t)))
    elif cid == 'akago':                                 # rote Glut steigt nach der Landung auf
        _burst('fx_fire_r', 6, t - 0.3, px, fb - 10, -P / 2 - 0.7, -P / 2 + 0.7, 25, 45, -30, 1.1, 5)
    elif cid == 'susanoo':                               # Doppelblitz schlägt neben ihm ein, Himmel zuckt auf
        if t < 0.3 and int(t * 20) % 2 == 0:
            s.fill((40, 40, 60), special_flags=pygame.BLEND_RGB_ADD)
            _fx('fx_bolt', px - 42, fb - 22)
            _fx('fx_bolt', px + 46, fb - 26)
