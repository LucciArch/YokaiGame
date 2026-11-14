"""Prozedural erzeugte Soundeffekte und Musik im japanischen Stil (Koto, Taiko, Shakuhachi)."""
import math
import random
import pygame

try:
    import numpy as np
except ImportError:  # ohne numpy: stumm
    np = None

SR = 22050


class Audio:
    def __init__(self):
        self.ok = False
        self.sfx = {}
        self.music_cache = {}
        self.music_ch = None
        self.cur_music = None
        self.vol_sfx = 0.8
        self.vol_music = 0.55
        self.last_play = {}
        try:
            if np is None:
                raise RuntimeError('numpy fehlt')
            if not pygame.mixer.get_init():
                pygame.mixer.init(SR, -16, 2, 512)
            pygame.mixer.set_num_channels(24)
            self.channels = pygame.mixer.get_init()[2]
            self._build_sfx()
            self._variants()
            self.music_ch = pygame.mixer.Channel(23)
            pygame.mixer.set_reserved(1)
            self.ok = True
        except Exception as e:  # pragma: no cover
            print('Audio deaktiviert:', e)

    # ------------------------------------------------------------ Synth-Bausteine
    def _snd(self, wave, vol=1.0):
        w = np.clip(wave * vol, -1, 1)
        a = (w * 32000).astype(np.int16)
        if self.channels == 2:
            a = np.column_stack((a, a))
        return pygame.sndarray.make_sound(np.ascontiguousarray(a))

    @staticmethod
    def _t(dur):
        return np.arange(int(SR * dur)) / SR

    def _tone(self, f0, dur, f1=None, kind='sine', decay=8.0, attack=0.004):
        t = self._t(dur)
        f = np.full_like(t, f0) if f1 is None else np.linspace(f0, f1, len(t))
        ph = np.cumsum(2 * np.pi * f / SR)
        if kind == 'sine':
            w = np.sin(ph)
        elif kind == 'square':
            w = np.sign(np.sin(ph)) * 0.6
        elif kind == 'tri':
            w = 2 / np.pi * np.arcsin(np.sin(ph))
        else:
            w = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)
        env = np.exp(-t * decay) * np.minimum(1, t / attack)
        return w * env

    def _noise(self, dur, decay=10.0, lp=0.5):
        t = self._t(dur)
        n = np.random.uniform(-1, 1, len(t))
        if lp < 1:  # einfacher Tiefpass
            out = np.empty_like(n)
            acc = 0.0
            a = lp
            # vektorisierte Annäherung: gleitender Mittelwert
            k = max(1, int(1 / a))
            out = np.convolve(n, np.ones(k) / k, mode='same')
            n = out * min(3, k ** 0.5)
        return n * np.exp(-t * decay)

    def _pluck(self, f, dur, bright=1.0):
        """Koto-artiger Zupfton."""
        t = self._t(dur)
        w = np.zeros_like(t)
        for h, amp in ((1, 1.0), (2, 0.55 * bright), (3, 0.3 * bright), (4, 0.18 * bright), (5, 0.1 * bright)):
            w += amp * np.sin(2 * np.pi * f * h * t * (1 + 0.0008 * h)) * np.exp(-t * (3.2 + h * 1.6))
        bend = np.exp(-t * 30) * 0.0
        att = np.minimum(1, t / 0.003)
        return w * att * 0.5

    def _taiko(self, dur=0.5, f=70):
        t = self._t(dur)
        f_t = f * (1 + 1.2 * np.exp(-t * 25))
        ph = np.cumsum(2 * np.pi * f_t / SR)
        w = np.sin(ph) * np.exp(-t * 7)
        w += self._noise(dur, 40, 0.3)[:len(t)] * 0.35
        return w

    def _flute(self, f, dur):
        t = self._t(dur)
        vib = 1 + 0.008 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 0.4)
        ph = np.cumsum(2 * np.pi * f * vib / SR)
        w = np.sin(ph) + 0.15 * np.sin(2 * ph)
        env = np.minimum(1, t / 0.12) * np.minimum(1, (dur - t) / 0.25).clip(0, 1)
        breath = np.random.uniform(-1, 1, len(t)) * 0.06
        return (w * 0.5 + breath) * env

    def _build_sfx(self):
        T, N, P = self._tone, self._noise, self._pluck
        cat = np.concatenate
        self.sfx = {
            'shoot': self._snd(T(900, 0.07, 500, 'tri', 30) * 0.5, 0.22),
            'ehit': self._snd(T(300, 0.08, 150, 'square', 30), 0.25),
            'hit': self._snd(N(0.08, 40, 0.4) + T(220, 0.08, 120, 'sine', 30), 0.35),
            'kill': self._snd(N(0.25, 14, 0.25) + T(180, 0.25, 50, 'sine', 12), 0.45),
            'hurt': self._snd(T(420, 0.25, 90, 'square', 10) + N(0.25, 12, 0.3), 0.45),
            'coin': self._snd(cat([T(1320, 0.06, None, 'sine', 20), T(1760, 0.18, None, 'sine', 14)]), 0.35),
            'pickup': self._snd(cat([P(660, 0.08), P(880, 0.25)]), 0.7),
            'heal': self._snd(cat([P(523, 0.08), P(659, 0.08), P(784, 0.3)]), 0.7),
            'key': self._snd(cat([T(1000, 0.05, None, 'tri', 25), T(1500, 0.12, None, 'tri', 18)]), 0.35),
            'item': self._snd(cat([P(f, 0.11) for f in (392, 440, 523, 587, 659)] + [P(784, 0.8)]), 0.8),
            'synergy': self._snd(cat([P(f, 0.09) for f in (523, 659, 784, 1046)] + [P(1318, 0.9) + P(659, 0.9)]), 0.8),
            'door': self._snd(N(0.3, 9, 0.12) + T(90, 0.3, 60, 'sine', 8), 0.5),
            'dash': self._snd(N(0.18, 12, 0.6) * np.linspace(0.3, 1, int(SR * 0.18)), 0.3),
            'boss': self._snd(self._taiko(0.9, 50) + N(0.9, 3, 0.15) * 0.6 + T(55, 0.9, 40, 'buzz', 3) * 0.5, 0.7),
            'blank': self._snd(T(200, 0.6, 1200, 'sine', 4) + N(0.6, 5, 0.7) * 0.5, 0.45),
            'explode': self._snd(N(0.5, 7, 0.08) * 1.6 + T(80, 0.5, 30, 'sine', 6), 0.6),
            'thunder': self._snd(N(0.7, 4, 0.1) * 1.8, 0.5),
            'unlock': self._snd(cat([P(f, 0.12) for f in (659, 784, 988, 1318)] + [P(1568, 1.0)]), 0.8),
            'select': self._snd(P(880, 0.12, 0.6), 0.6),
            'move': self._snd(P(660, 0.06, 0.4), 0.4),
            'buy': self._snd(cat([T(1200, 0.05, None, 'sine', 20), T(1600, 0.05, None, 'sine', 20), T(2000, 0.2, None, 'sine', 12)]), 0.35),
            'lock': self._snd(T(150, 0.15, 100, 'square', 18), 0.3),
            'roar': self._snd(N(1.0, 3, 0.05) * 1.4 + T(70, 1.0, 45, 'buzz', 2.5) * 0.6, 0.6),
            'bell': self._snd(T(1046, 1.2, None, 'sine', 3) + T(2093, 1.2, None, 'sine', 5) * 0.3 + T(1568, 1.2, None, 'sine', 4) * 0.2, 0.45),
            'splash': self._snd(N(0.3, 10, 0.5), 0.3),
            'stairs': self._snd(cat([P(f, 0.14) for f in (784, 659, 523, 392, 330)]), 0.7),
        }

    def _variants(self):
        """Tonhöhen-Varianten, damit sich häufige Klänge nicht wiederholen."""
        self.var = {}
        for name in ('shoot', 'hit', 'kill', 'coin', 'ehit'):
            snd = self.sfx[name]
            arr = pygame.sndarray.array(snd).astype(np.float32)
            out = []
            for f in (0.9, 1.0, 1.1):
                n = int(len(arr) / f)
                idx = np.clip((np.arange(n) * f).astype(np.int64), 0, len(arr) - 1)
                out.append(pygame.sndarray.make_sound(np.ascontiguousarray(arr[idx].astype(np.int16))))
            self.var[name] = out

    def play(self, name, vol=1.0):
        if not self.ok or name not in self.sfx:
            return
        if name in getattr(self, 'var', {}) and random.random() < 0.8:
            s = random.choice(self.var[name])
            now = pygame.time.get_ticks()
            if now - self.last_play.get(name, -999) < 35:
                return
            self.last_play[name] = now
            ch = pygame.mixer.find_channel(False)
            if ch:
                ch.set_volume(self.vol_sfx * vol)
                ch.play(s)
            return
        now = pygame.time.get_ticks()
        if now - self.last_play.get(name, -999) < 35:
            return
        self.last_play[name] = now
        s = self.sfx[name]
        ch = pygame.mixer.find_channel(False)
        if ch:
            ch.set_volume(self.vol_sfx * vol)
            ch.play(s)

    # ------------------------------------------------------------ Musik
    SCALES = {
        'in': [0, 1, 5, 7, 8],        # Miyako-bushi
        'yo': [0, 2, 5, 7, 9],        # Yo-Skala (hell, himmlisch)
        'iwato': [0, 1, 5, 6, 10],    # düster
        'ryukyu': [0, 4, 5, 7, 11],   # Okinawa
    }

    def _make_music(self, key):
        scale_name, root, bpm, mood, seed = key
        rng = random.Random(seed)
        sc = self.SCALES[scale_name]
        beat = 60 / bpm
        bars = 8
        total = bars * 4 * beat
        n = int(SR * total) + SR
        out = np.zeros(n)

        def put(w, t0, v=1.0):
            i = int(t0 * SR)
            j = min(n, i + len(w))
            out[i:j] += w[:j - i] * v

        def note(deg, octave=0):
            o, d = divmod(deg, len(sc))
            return root * 2 ** ((sc[d] + 12 * (o + octave)) / 12)

        # Melodie (Koto) – Motiv + Variation
        motif = [rng.choice([0, 1, 2, 3, 4, 5, 6, 7]) for _ in range(8)]
        rhythm = rng.choice([[1, 1, 0.5, 0.5, 1], [0.5, 0.5, 1, 1, 1], [1.5, 0.5, 1, 1], [1, 0.5, 0.5, 2]])
        t = 0.0
        bar_i = 0
        while t < total - 0.01:
            for r in rhythm:
                if t >= total - 0.01:
                    break
                if rng.random() < (0.78 if mood != 'calm' else 0.6):
                    deg = motif[bar_i % len(motif)] + (rng.choice([0, 0, 1, -1, 2]) if bar_i > 8 else 0)
                    f = note(deg, 1)
                    put(self._pluck(f, min(1.6, r * beat * 2.5), 0.9), t, 0.32)
                    if rng.random() < 0.25:
                        put(self._pluck(f * 2, 0.4, 0.5), t + beat * 0.25, 0.1)
                bar_i += 1
                t += r * beat
        # Bass-Drone
        for b in range(bars):
            deg = [0, 0, 3, 2, 0, 4, 3, 0][b % 8] if mood != 'dark' else [0, 0, 1, 0, 0, 1, 2, 0][b % 8]
            put(self._pluck(note(deg, -1), 4 * beat, 0.4), b * 4 * beat, 0.35)
            put(self._pluck(note(deg, -1) * 1.5, 4 * beat, 0.3), b * 4 * beat + 2 * beat, 0.12)
        # Shakuhachi
        if mood in ('calm', 'dark', 'mystic'):
            t = beat * 4
            while t < total - beat * 4:
                d = rng.choice([2, 3, 4]) * beat
                put(self._flute(note(rng.choice([0, 2, 3, 4, 5]), 1), d), t, 0.16)
                t += d + rng.choice([2, 4, 6]) * beat
        # Taiko
        if mood in ('battle', 'boss', 'dark'):
            pattern = [1, 0, 0, 1, 0, 0, 1, 0] if mood != 'boss' else [1, 0, 1, 1, 0, 1, 1, 1]
            for b in range(bars * 8):
                tt = b * beat / 2
                if pattern[b % 8]:
                    put(self._taiko(0.4, 75 if b % 4 else 60), tt, 0.5 if mood == 'boss' else 0.35)
                if mood == 'boss' and b % 2 == 1:
                    put(self._noise(0.05, 50, 0.9), tt, 0.08)
        # Loop-Übergang weich
        out = out[:int(SR * total)]
        fade = int(SR * 0.02)
        out[:fade] *= np.linspace(0, 1, fade)
        out[-fade:] *= np.linspace(1, 0, fade)
        peak = max(0.5, np.abs(out).max())
        return self._snd(out / peak * 0.7)

    def music(self, key):
        """key = (skala, grundton, bpm, stimmung, seed)"""
        if not self.ok:
            return
        if self.cur_music == key:
            return
        self.cur_music = key
        if key is None:
            self.music_ch.fadeout(400)
            return
        if key not in self.music_cache:
            self.music_cache[key] = self._make_music(key)
        self.music_ch.set_volume(self.vol_music)
        self.music_ch.play(self.music_cache[key], loops=-1, fade_ms=600)

    def set_volumes(self, sfx, music):
        self.vol_sfx = sfx
        self.vol_music = music
        if self.ok and self.music_ch:
            self.music_ch.set_volume(music)


AUDIO = None


def get():
    global AUDIO
    if AUDIO is None:
        AUDIO = Audio()
    return AUDIO


def play(name, vol=1.0):
    if AUDIO:
        AUDIO.play(name, vol)
