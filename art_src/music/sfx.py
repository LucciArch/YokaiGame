"""Soundeffekte für Yōkai no Michi – mit derselben Synth-Engine wie der Soundtrack.
Erzeugt yokai/assets/sfx/<name>_<n>.ogg (mehrere Varianten je Effekt). Aufruf: python3 sfx.py"""
import os
import subprocess
import wave

import numpy as np

import synth as Y
from synth import SR, biquad, noise, onepole_lp

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'yokai', 'assets', 'sfx')


def T(d):
    return np.arange(int(SR * d)) / SR


def sweep_noise(d, f0, f1, q=1.5, curve=1.0):
    """Rauschen durch ein Bandpass, dessen Frequenz von f0 nach f1 wandert."""
    n = int(SR * d)
    x = noise(n)
    out = np.zeros(n)
    seg = 256
    for i in range(0, n, seg):
        k = (i / n) ** curve
        f = f0 * (f1 / f0) ** k
        out[i:i + seg] = biquad(x[max(0, i - 64):i + seg], 'bp', f, q)[-len(x[i:i + seg]):]
    return out


def tone(f0, f1, d, kind='sine', decay=10.0):
    t = T(d)
    f = f0 * (f1 / f0) ** (t / d)
    ph = np.cumsum(2 * np.pi * f / SR)
    w = np.sin(ph) if kind == 'sine' else (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph))
    return w * np.exp(-t * decay) * np.minimum(1, t / 0.002)


def env(d, a, dec):
    t = T(d)
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) * dec)


def room(x, sec=0.6, wet=0.18):
    y = Y.reverb(np.concatenate([x, np.zeros(int(SR * sec))]), sec, 5, 4000)
    xx = np.concatenate([x, np.zeros(int(SR * sec))])
    return xx * (1 - wet) + y * wet


def cat(*xs):
    return np.concatenate(xs)


def at(base_len, *parts):
    """parts: (zeit_s, signal, gain)"""
    n = int(SR * base_len)
    out = np.zeros(n)
    for t0, x, g in parts:
        i = int(t0 * SR)
        j = min(n, i + len(x))
        out[i:j] += x[:j - i] * g
    return out


def trim(x, thresh=1e-4):
    nz = np.where(np.abs(x) > thresh)[0]
    if len(nz):
        x = x[:nz[-1] + 1]
    fade = min(len(x), int(SR * 0.01))
    x[-fade:] *= np.linspace(1, 0, fade)
    return x


# ------------------------------------------------------------------ Effekte
def s_ehit(v):
    """Geschoss prallt ab / Gegnertreffer: dumpfer Holz-Plock."""
    p = 1 + (v - 1.5) * 0.08
    knock = tone(520 * p, 380 * p, 0.07, 'rich', 50)
    thud = tone(150 * p, 90 * p, 0.1, 'sine', 30)
    n = biquad(noise(int(SR * 0.03)), 'lp', 1800) * env(0.03, 0.001, 120)
    return at(0.12, (0, knock, 0.5), (0, thud, 0.8), (0, n, 0.6))


def s_kill(v):
    """Yokai löst sich auf: Geisterhauch, fallendes Pfeifen, Glöckchen."""
    p = 1 + (v - 1.5) * 0.07
    puff = sweep_noise(0.45, 900 * p, 300 * p, 1.0, 0.8) * env(0.45, 0.02, 7)
    whistle = tone(1400 * p, 500 * p, 0.35, 'sine', 8) * 0.25
    ting = Y.kane(2200 * p, 0.6, 0.6) * 0.3
    thump = tone(110, 55, 0.25, 'sine', 14) * 0.8
    return room(at(0.6, (0, thump, 1.0), (0.005, puff, 1.0), (0.03, whistle, 1.0), (0.06, ting, 1.0)), 0.7, 0.25)


def s_hurt(v):
    """Spieler getroffen: harter Schlag + schnarrende Shamisen-Dissonanz."""
    hit = tone(180, 70, 0.25, 'sine', 12)
    s1 = Y.shamisen(196, 0.4, 0.9)
    s2 = Y.shamisen(207.7, 0.4, 0.8)
    n = biquad(noise(int(SR * 0.08)), 'bp', 1200, 0.7) * env(0.08, 0.001, 40)
    return room(at(0.45, (0, hit, 1.0), (0, n, 0.7), (0.01, s1, 0.45), (0.012, s2, 0.4)), 0.5, 0.15)


def s_coin(v):
    """Mon-Münze: zwei Metall-Klinge."""
    p = 1 + (v - 1.5) * 0.05
    a = Y.kane(1850 * p, 0.8, 0.5)
    b = Y.kane(2480 * p, 0.7, 0.6)
    return at(0.55, (0, a, 0.7), (0.06, b, 0.8))


def s_pickup(v):
    return room(at(0.6, (0, Y.koto(659, 0.4, 0.8), 0.8), (0.07, Y.koto(880, 0.5, 0.85), 0.8)), 0.6, 0.2)


def s_heal(v):
    parts = [(i * 0.06, Y.koto(f, 0.6, 0.7), 0.6) for i, f in enumerate((523, 659, 784, 1047))]
    sh = Y.sho([523, 784, 1047], 0.9, 0.5)
    return room(at(1.0, *parts, (0.05, sh, 1.0)), 0.8, 0.3)


def s_key(v):
    return at(0.5, (0, Y.kane(2900, 0.6, 0.35), 0.7), (0.05, Y.kane(3500, 0.6, 0.35), 0.6), (0.1, Y.kane(2600, 0.5, 0.3), 0.5))


def s_item(v):
    run = [(i * 0.07, Y.koto(f, 0.7, 0.75), 0.55) for i, f in enumerate((392, 440, 523, 587, 659, 784))]
    return room(at(1.6, *run, (0.42, Y.kane(1568, 0.7, 1.2), 0.6), (0.42, Y.sho([523, 659, 784], 1.1, 0.5), 1.0)), 1.0, 0.3)


def s_synergy(v):
    run = [(i * 0.06, Y.koto(f, 0.8, 0.8), 0.55) for i, f in enumerate((523, 659, 784, 1047, 1319))]
    return room(at(2.0, *run, (0.3, Y.sho([523, 659, 784, 1047], 1.6, 0.7), 1.2), (0.3, Y.kane(2093, 0.6, 1.5), 0.5)), 1.2, 0.35)


def s_door(v):
    """Shōji gleitet: Holzreibung + Anschlag."""
    slide = biquad(noise(int(SR * 0.28)), 'bp', 700, 0.8) * np.sin(np.linspace(0, np.pi, int(SR * 0.28))) ** 0.7
    knock = tone(320, 240, 0.08, 'rich', 40)
    return at(0.42, (0, slide, 0.7), (0.27, knock, 0.6))


def s_dash(v):
    n = int(SR * 0.24)
    w = sweep_noise(0.24, 600, 3200, 1.0, 1.0) * np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return w


def s_boss(v):
    return room(at(2.5, (0, Y.odaiko(46, 1.0, 1.8), 1.0), (0.02, Y.bonsho(55, 0.9, 2.4), 0.7), (0.35, Y.odaiko(52, 0.8, 1.5), 0.7)), 1.5, 0.3)


def s_blank(v):
    """Reinigungssalz: aufsteigendes Glitzern + Glocke."""
    rise = sweep_noise(0.6, 400, 6000, 1.5, 1.2) * np.sin(np.linspace(0, np.pi, int(SR * 0.6)))
    return room(at(1.2, (0, rise, 0.8), (0.3, Y.kane(1760, 0.8, 0.9), 0.6), (0.33, Y.kane(2637, 0.6, 0.8), 0.4)), 0.9, 0.3)


def s_explode(v):
    boom = tone(90, 30, 0.7, 'sine', 5)
    rumble = onepole_lp(noise(int(SR * 0.8)), 400) * env(0.8, 0.005, 5) * 3
    crackle = biquad(noise(int(SR * 0.3)), 'hp', 2000) * env(0.3, 0.001, 18) * (np.random.rand(int(SR * 0.3)) > 0.85)
    return room(at(0.9, (0, boom, 1.0), (0, rumble, 0.8), (0.01, crackle, 0.6)), 0.8, 0.25)


def s_thunder(v):
    crack = biquad(noise(int(SR * 0.15)), 'hp', 1500) * env(0.15, 0.001, 25)
    rumble = onepole_lp(noise(int(SR * 1.4)), 250) * env(1.4, 0.05, 2.5) * 4
    return room(at(1.5, (0, crack, 1.0), (0.05, rumble, 0.9)), 1.2, 0.3)


def s_unlock(v):
    run = [(i * 0.09, Y.koto(f, 0.8, 0.8), 0.55) for i, f in enumerate((659, 784, 988, 1319))]
    return room(at(1.6, *run, (0.36, Y.kane(1568, 0.8, 1.2), 0.7)), 1.0, 0.3)


def s_select(v):
    return Y.koto(880, 0.35, 0.7)[:int(SR * 0.35)] * 0.8


def s_move(v):
    return Y.hyoshigi(0.5)[:int(SR * 0.08)] * 0.6


def s_buy(v):
    return at(0.8, (0, s_coin(1.5), 0.8), (0.12, Y.kane(1318, 0.6, 0.6), 0.6))


def s_lock(v):
    return at(0.2, (0, tone(240, 180, 0.12, 'rich', 30), 0.7), (0, biquad(noise(int(SR * 0.04)), 'lp', 1200) * env(0.04, 0.001, 80), 0.6))


def s_roar(v):
    """Brüllen eines Yokai: tiefes Knurren mit Formant."""
    d = 1.1
    t = T(d)
    f = 70 * (1 + 0.25 * np.sin(2 * np.pi * 9 * t) * 0.3) * (1 + 0.15 * np.sin(np.pi * t / d))
    ph = np.cumsum(2 * np.pi * f / SR)
    saw = sum(np.sin(h * ph) / h for h in range(1, 30))
    growl = biquad(saw, 'bp', 450, 1.2) + biquad(saw, 'bp', 1100, 2.0) * 0.6
    breath = biquad(noise(len(t)), 'bp', 900, 0.6) * 0.5
    e = np.minimum(1, t / 0.12) * np.clip((d - t) / 0.4, 0, 1)
    return room((growl + breath) * e * (1 + 0.3 * np.sin(2 * np.pi * 23 * t)), 0.8, 0.2)


def s_bell(v):
    return Y.kane(1046, 0.8, 1.6)


def s_splash(v):
    return at(0.36, (0, sweep_noise(0.35, 2500, 500, 1.0, 0.7) * env(0.35, 0.005, 9), 1.0), (0, tone(600, 300, 0.1, 'sine', 30), 0.3))


def s_stairs(v):
    run = [(i * 0.09, Y.koto(f, 0.7, 0.75), 0.55) for i, f in enumerate((784, 659, 523, 440, 392, 330))]
    return room(at(1.3, *run), 0.9, 0.3)


def s_drum(v):
    return room(at(0.9, (0, Y.odaiko(55, 1.0, 0.8), 1.0), (0.13, Y.odaiko(62, 0.8, 0.7), 0.8)), 0.6, 0.2)


def s_gust(v):
    n = int(SR * 0.9)
    return sweep_noise(0.9, 300, 1400, 2.0, 1.0) * np.sin(np.linspace(0, np.pi, n)) * 1.6


def s_wave(v):
    n = int(SR * 1.3)
    return (sweep_noise(1.3, 300, 900, 0.7, 1.0) * np.sin(np.linspace(0, np.pi, n)) ** 2 * 1.5
            + biquad(noise(n), 'hp', 3000) * np.linspace(0, 1, n) ** 3 * np.exp(-np.linspace(0, 1, n) * 0) * 0.3)


def s_bamboo(v):
    return at(0.3, (0, tone(420, 300, 0.06, 'rich', 40), 0.7), (0.06, tone(520, 380, 0.1, 'rich', 30), 0.8),
              (0.06, biquad(noise(int(SR * 0.05)), 'bp', 1800, 1) * env(0.05, 0.001, 80), 0.6))


def s_grab(v):
    return room(tone(140, 70, 0.5, 'rich', 6) * 0.6 + biquad(noise(int(SR * 0.5)), 'lp', 500) * env(0.5, 0.05, 6) * 1.5, 0.6, 0.3)


def s_wisp(v):
    return room(tone(1200, 1800, 0.5, 'sine', 5) * 0.5 + tone(1800, 2400, 0.5, 'sine', 7) * 0.25, 0.8, 0.4)


def s_eshot(v):
    """Yokai feuert: dunkles Geister-Fauchen."""
    p = 1 + (v - 1) * 0.08
    w = sweep_noise(0.2, 300 * p, 1100 * p, 1.6, 0.8) * np.sin(np.linspace(0, np.pi, int(SR * 0.2))) ** 0.8
    t_ = tone(200 * p, 300 * p, 0.18, 'rich', 12) * 0.35
    return at(0.22, (0, w, 1.0), (0, t_, 1.0))


def s_slash(v):
    """Schwerthieb: scharfes Zischen mit metallischem Nachklang."""
    p = 1 + (v - 1) * 0.06
    w = sweep_noise(0.16, 2500 * p, 6500 * p, 1.4, 0.7) * np.sin(np.linspace(0, np.pi, int(SR * 0.16))) ** 0.6
    ring = Y.kane(3100 * p, 0.4, 0.25) * 0.25
    return at(0.3, (0, w, 1.0), (0.04, ring, 1.0))


def s_laser(v):
    t = T(0.25)
    f = 900 + 600 * np.exp(-t * 12)
    ph = np.cumsum(2 * np.pi * f / SR)
    w = (np.sin(ph) + 0.4 * np.sin(2.01 * ph) + 0.2 * np.sin(3.02 * ph)) * np.exp(-t * 7)
    return w * 0.6 + biquad(noise(len(t)), 'hp', 4000) * np.exp(-t * 20) * 0.3


def s_bow(v):
    tw = tone(180, 140, 0.12, 'rich', 25) * 0.6
    sw = sweep_noise(0.12, 3000, 1200, 1.2, 0.8) * env(0.12, 0.004, 25)
    return at(0.15, (0, tw, 1.0), (0.01, sw, 0.7))



# ------------------------------------------------------------------ neu in Runde 110
def s_shoot(v):
    """Ofuda wird geworfen: weicher Papier-Fwip mit kurzem Körper, ohne schrille Spitze (wird ständig gehört)."""
    p = 1 + (v - 1.5) * 0.05
    fw = sweep_noise(0.08, 3600 * p, 1100 * p, 1.1, 0.6) * env(0.08, 0.003, 45)
    body = tone(420 * p, 260 * p, 0.06, 'sine', 50) * 0.5
    tick = biquad(noise(int(SR * 0.006)), 'bp', 2400 * p, 1.2) * 0.6
    return biquad(at(0.1, (0, tick, 1.0), (0.001, fw, 0.9), (0.002, body, 1.0)), 'lp', 6500)


def s_hit(v):
    """Ofuda trifft: Klatsch mit Tiefe, Papier reißt, kurzes Knistern."""
    p = 1 + (v - 1.5) * 0.07
    click = biquad(noise(int(SR * 0.004)), 'bp', 3000 * p, 1.0)
    slap = biquad(noise(int(SR * 0.05)), 'bp', 1700 * p, 0.8) * env(0.05, 0.001, 75)
    body = tone(190 * p, 95 * p, 0.1, 'sine', 32)
    tear = sweep_noise(0.05, 4200 * p, 2200 * p, 2.0, 0.8) * env(0.05, 0.004, 55)
    return biquad(at(0.13, (0, click, 0.9), (0, slap, 1.0), (0, body, 0.9), (0.01, tear, 0.35)), 'lp', 7000)


def s_kill_ghost(v):
    """Geist/Irrlicht vergeht: luftiges Ausatmen nach unten, schimmerndes Glöckchen, kein Aufprall."""
    p = 1 + (v - 1) * 0.06
    sigh = sweep_noise(0.55, 2400 * p, 500 * p, 2.2, 0.7) * env(0.55, 0.03, 5)
    shimmer = (tone(1760 * p, 1320 * p, 0.6, 'sine', 5) + tone(2637 * p, 1980 * p, 0.6, 'sine', 7) * 0.5) * 0.25
    ting = Y.kane(2350 * p, 0.5, 0.8) * 0.35
    return room(at(0.8, (0, sigh, 1.0), (0.02, shimmer, 1.0), (0.05, ting, 1.0)), 0.9, 0.35)


def s_kill_big(v):
    """Schwerer Yokai fällt: dumpfer Aufschlag, Bröckeln, tiefes Ausklingen."""
    p = 1 + (v - 1) * 0.06
    thud = tone(85 * p, 40 * p, 0.45, 'sine', 7) * 1.2
    knock = tone(220 * p, 120 * p, 0.12, 'rich', 30) * 0.5
    grit = biquad(noise(int(SR * 0.5)), 'bp', 900, 0.8) * env(0.5, 0.01, 8) * (np.random.rand(int(SR * 0.5)) > 0.7)
    growl = biquad(tone(70 * p, 50 * p, 0.6, 'rich', 4), 'lp', 500) * 0.4
    return room(at(0.9, (0, thud, 1.0), (0, knock, 1.0), (0.03, grit, 0.7), (0.02, growl, 1.0)), 0.7, 0.22)


def s_pot(v):
    """Tonkrug zerbricht: hohler Schlag, dann mehrere Scherben-Klicks."""
    p = 1 + (v - 1) * 0.08
    knock = tone(380 * p, 260 * p, 0.07, 'rich', 45)
    parts = [(0, knock, 0.8), (0, biquad(noise(int(SR * 0.03)), 'bp', 1500 * p, 1.0) * env(0.03, 0.001, 90), 0.8)]
    rng = np.random.RandomState(int(v * 7 + 3))
    for k in range(7):
        t0 = 0.02 + rng.uniform(0, 0.22) * (k / 7) ** 0.6
        f = rng.uniform(2200, 5200) * p
        sh_ = biquad(noise(int(SR * 0.018)), 'bp', f, 3.0) * env(0.018, 0.0005, 220)
        parts.append((t0, sh_, rng.uniform(0.3, 0.7)))
    return at(0.32, *parts)


def s_rock(v):
    """Felsen zerbröckelt."""
    rumble = onepole_lp(noise(int(SR * 0.35)), 600) * env(0.35, 0.004, 12) * 3
    parts = [(0, rumble, 1.0), (0, tone(120, 70, 0.15, 'sine', 18), 0.8)]
    rng = np.random.RandomState(11)
    for k in range(6):
        parts.append((rng.uniform(0.01, 0.25), biquad(noise(int(SR * 0.03)), 'bp', rng.uniform(700, 1800), 1.5) * env(0.03, 0.001, 100), 0.5))
    return at(0.4, *parts)


def s_chest(v):
    """Truhe: Holzdeckel knarrt, Riegel schnappt, Münzen klingen."""
    n = int(SR * 0.22)
    creak = biquad(tone(240, 300, 0.22, 'rich', 2) * (1 + 0.6 * np.sign(np.sin(2 * np.pi * 38 * T(0.22)))), 'bp', 900, 1.5) * np.sin(np.linspace(0, np.pi, n))
    latch = at(0.04, (0, tone(900, 600, 0.04, 'rich', 70), 1.0), (0, biquad(noise(int(SR * 0.02)), 'hp', 3000) * env(0.02, 0.0005, 150), 1.0))
    return room(at(0.9, (0, creak, 0.6), (0.2, latch, 0.7), (0.3, Y.kane(1850, 0.6, 0.4), 0.5), (0.36, Y.kane(2480, 0.6, 0.45), 0.5),
                   (0.43, Y.kane(2100, 0.5, 0.4), 0.4)), 0.6, 0.2)


def s_spirit(v):
    """Geisterherz: kühler Sho-Akkord mit aufsteigendem Hauch."""
    sh = Y.sho([587, 880, 1175], 0.8, 0.5)
    rise = tone(700, 1400, 0.5, 'sine', 4) * 0.3
    return room(at(1.0, (0, sh, 1.0), (0.02, rise, 1.0), (0.1, Y.kane(1760, 0.4, 0.8), 0.4)), 0.9, 0.35)


def s_salt(v):
    """Reinigungssalz aufgehoben: kristallines Rieseln."""
    parts = []
    rng = np.random.RandomState(5)
    for k in range(10):
        f = rng.uniform(3500, 7000)
        parts.append((k * 0.022 + rng.uniform(0, 0.01), tone(f, f * 0.98, 0.05, 'sine', 60), 0.25))
    return room(at(0.45, *parts, (0.02, Y.kane(1568, 0.5, 0.5), 0.4)), 0.5, 0.3)


def s_trinket(v):
    """Anhänger: zwei kleine Glöckchen am Band."""
    return room(at(0.9, (0, Y.kane(1975, 0.6, 0.7), 0.6), (0.09, Y.kane(2637, 0.5, 0.7), 0.5), (0.18, Y.kane(1975, 0.4, 0.6), 0.35)), 0.7, 0.3)


def s_death(v):
    """Tod der Spielfigur: harter Taiko-Schlag, fallende Flöte, Tempelglocke klingt aus."""
    hit = Y.odaiko(50, 1.0, 1.2)
    t = T(1.4)
    f = 740 * (0.5 ** (t / 1.4)) * (1 + 0.01 * np.sin(2 * np.pi * 5 * t))
    ph = np.cumsum(2 * np.pi * f / SR)
    flute = (np.sin(ph) + 0.2 * np.sin(2 * ph)) * np.minimum(1, t / 0.05) * np.exp(-t * 1.6) * 0.35
    flute = flute + biquad(noise(len(t)), 'bp', 1500, 1.0) * np.exp(-t * 2.5) * 0.06
    return room(at(3.0, (0, hit, 1.0), (0.08, flute, 1.0), (0.25, Y.bonsho(65, 0.7, 2.6), 0.8)), 1.6, 0.35)


def s_bossdie(v):
    """Boss besiegt: Trommelwirbel, großer Glockenschlag, aufsteigender Sho-Akkord."""
    roll = [(i * 0.07, Y.odaiko(55 + i * 2, 0.5 + i * 0.06, 0.7), 1.0) for i in range(7)]
    return room(at(3.4, *roll, (0.5, Y.odaiko(46, 1.0, 1.8), 1.2), (0.52, Y.bonsho(58, 0.9, 2.8), 0.9),
                   (0.9, Y.sho([392, 523, 659, 784], 2.2, 0.6), 1.0)), 1.8, 0.35)


SFX = {k[2:]: f for k, f in globals().items() if k.startswith('s_')}
VARIANTS = {'slash': 3, 'eshot': 3, 'shoot': 4, 'hit': 4, 'ehit': 4, 'kill': 4, 'coin': 3, 'kill_ghost': 3, 'kill_big': 2, 'pot': 3}
PEAK = {'slash': 0.5, 'laser': 0.4, 'bow': 0.45, 'eshot': 0.3, 'shoot': 0.35, 'hit': 0.55, 'ehit': 0.45, 'kill': 0.6, 'hurt': 0.8, 'coin': 0.45, 'move': 0.35, 'select': 0.5,
        'boss': 0.9, 'explode': 0.85, 'roar': 0.75, 'thunder': 0.8, 'kill_ghost': 0.5, 'kill_big': 0.75, 'pot': 0.5, 'rock': 0.6,
        'chest': 0.6, 'spirit': 0.55, 'salt': 0.45, 'trinket': 0.5, 'death': 0.9, 'bossdie': 0.95}

# Ziel-Lautheit (lautestes 50-ms-Fenster, dBFS): häufige Kleinklänge leise, wichtige Rückmeldungen deutlich
LOUD = dict(shoot=-24, move=-22, select=-19, hit=-18, ehit=-20, eshot=-21, coin=-18, pot=-18, slash=-17, bow=-17, laser=-18,
            kill=-15, kill_ghost=-16, kill_big=-12, pickup=-16, heal=-15, spirit=-15, salt=-17, key=-16, trinket=-16, chest=-15,
            item=-14, synergy=-13, unlock=-14, hurt=-11, bell=-15, explode=-11, drum=-13, gust=-17, wave=-17, wisp=-16,
            grab=-14, lock=-16, roar=-11, thunder=-13, blank=-13, buy=-15, door=-16, stairs=-14, splash=-16, rock=-16,
            dash=-17, bamboo=-16, death=-9, boss=-8, bossdie=-7)


def loudness(x):
    w = int(SR * 0.05)
    r = max(np.sqrt(np.mean(x[i:i + w] ** 2)) for i in range(0, max(1, len(x) - w), w // 2))
    return 20 * np.log10(r + 1e-9)


def level(x, name):
    x = x / (np.abs(x).max() + 1e-9) * 0.5
    x = x * 10 ** ((LOUD.get(name, -15) - loudness(x)) / 20)
    pk = np.abs(x).max()
    if pk > 0.9:                                     # weiche Begrenzung statt Übersteuern
        x = np.tanh(x / 0.9 * 1.2) * 0.9 / np.tanh(1.2)
    return x


def write(path, x):
    pcm = (np.clip(x, -1, 1) * 32000).astype(np.int16)
    st = np.column_stack([pcm, pcm])
    wav = path[:-4] + '.wav'
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(st.tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', '5', path], check=True)
    os.remove(wav)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, fn in sorted(SFX.items()):
        for v in range(VARIANTS.get(name, 1)):
            Y.seed(hash((name, v)) % 10000)
            x = fn(v)
            x = biquad(x, 'hp', 40)
            x = trim(x)
            x = level(x, name)
            write(os.path.join(OUT, '%s_%d.ogg' % (name, v)), x)
        print(name, VARIANTS.get(name, 1), round(len(x) / SR, 2), 's')
