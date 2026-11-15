"""Prozedural erzeugte Soundeffekte und Musik im japanischen Stil (Koto, Taiko, Shakuhachi)."""
import math
import random
import pygame

try:
    import numpy as np
except ImportError:  # ohne numpy: stumm
    np = None

SR = 44100
import os
MUSIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'music')


def _set_sr(v):
    global SR
    SR = v


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
        self._kscache = {}
        try:
            if np is None:
                raise RuntimeError('numpy fehlt')
            if not pygame.mixer.get_init():
                pygame.mixer.init(SR, -16, 2, 512)
            pygame.mixer.set_num_channels(24)
            _set_sr(pygame.mixer.get_init()[0])      # Effekte in der echten Mixer-Rate erzeugen
            self.channels = pygame.mixer.get_init()[2]
            self._build_sfx()
            self._variants()
            self._load_sfx_files()
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
        S = lambda w, v: self._snd(self._lowpass(w, 4800), v * 0.85)
        self.sfx = {
            'shoot': S(T(560, 0.07, 360, 'sine', 35) + np.concatenate([N(0.03, 80, 0.25), np.zeros(int(SR * 0.07) - int(SR * 0.03))]) * 0.4, 0.16),
            'ehit': S(T(300, 0.08, 150, 'square', 30), 0.25),
            'hit': S(N(0.08, 40, 0.4) + T(220, 0.08, 120, 'sine', 30), 0.35),
            'kill': S(N(0.25, 14, 0.25) + T(180, 0.25, 50, 'sine', 12), 0.45),
            'hurt': S(T(420, 0.25, 90, 'square', 10) + N(0.25, 12, 0.3), 0.45),
            'coin': S(cat([T(1320, 0.06, None, 'sine', 20), T(1760, 0.18, None, 'sine', 14)]), 0.35),
            'pickup': S(cat([P(660, 0.08), P(880, 0.25)]), 0.7),
            'heal': S(cat([P(523, 0.08), P(659, 0.08), P(784, 0.3)]), 0.7),
            'key': S(cat([T(1000, 0.05, None, 'tri', 25), T(1500, 0.12, None, 'tri', 18)]), 0.35),
            'item': S(cat([P(f, 0.11) for f in (392, 440, 523, 587, 659)] + [P(784, 0.8)]), 0.8),
            'synergy': S(cat([P(f, 0.09) for f in (523, 659, 784, 1046)] + [P(1318, 0.9) + P(659, 0.9)]), 0.8),
            'door': S(N(0.3, 9, 0.12) + T(90, 0.3, 60, 'sine', 8), 0.5),
            'dash': S(N(0.18, 12, 0.6) * np.linspace(0.3, 1, int(SR * 0.18)), 0.3),
            'boss': S(self._taiko(0.9, 50) + N(0.9, 3, 0.15) * 0.6 + T(55, 0.9, 40, 'buzz', 3) * 0.5, 0.7),
            'blank': S(T(200, 0.6, 1200, 'sine', 4) + N(0.6, 5, 0.7) * 0.5, 0.45),
            'explode': S(N(0.5, 7, 0.08) * 1.6 + T(80, 0.5, 30, 'sine', 6), 0.6),
            'thunder': S(N(0.7, 4, 0.1) * 1.8, 0.5),
            'unlock': S(cat([P(f, 0.12) for f in (659, 784, 988, 1318)] + [P(1568, 1.0)]), 0.8),
            'select': S(P(880, 0.12, 0.6), 0.6),
            'move': S(P(660, 0.06, 0.4), 0.4),
            'buy': S(cat([T(1200, 0.05, None, 'sine', 20), T(1600, 0.05, None, 'sine', 20), T(2000, 0.2, None, 'sine', 12)]), 0.35),
            'lock': S(T(150, 0.15, 100, 'square', 18), 0.3),
            'roar': S(N(1.0, 3, 0.05) * 1.4 + T(70, 1.0, 45, 'buzz', 2.5) * 0.6, 0.6),
            'bell': S(T(1046, 1.2, None, 'sine', 3) + T(2093, 1.2, None, 'sine', 5) * 0.3 + T(1568, 1.2, None, 'sine', 4) * 0.2, 0.45),
            'splash': S(N(0.3, 10, 0.5), 0.3),
            'stairs': S(cat([P(f, 0.14) for f in (784, 659, 523, 392, 330)]), 0.7),
            # Biom-Eigenheiten
            'drum': S(self._taiko(0.6, 58) * 1.3 + cat([np.zeros(int(SR * 0.12)), self._taiko(0.48, 64)]) * 0.8, 0.5),
            'gust': S(N(0.9, 2.5, 0.04) * np.sin(np.linspace(0, np.pi, int(SR * 0.9))) * 1.6, 0.4),
            'wave': S(N(1.2, 1.6, 0.07) * np.sin(np.linspace(0, np.pi, int(SR * 1.2))) ** 2 * 1.4
                      + N(1.2, 3, 0.5) * np.linspace(0, 1, int(SR * 1.2)) ** 3 * 0.35, 0.4),
            'bamboo': S(cat([T(420, 0.05, 300, 'tri', 40), T(520, 0.12, 380, 'tri', 25)]) + N(0.17, 30, 0.3) * 0.3, 0.45),
            'grab': S(T(140, 0.45, 70, 'buzz', 6) * 0.6 + N(0.45, 6, 0.06) * 0.6, 0.4),
            'wisp': S(T(1200, 0.5, 1800, 'sine', 5) * 0.5 + T(1800, 0.5, 2400, 'sine', 7) * 0.25, 0.3),
        }

    def _load_sfx_files(self):
        """Vorgerenderte Effekte aus assets/sfx (art_src/music/sfx.py) ersetzen die Sofort-Synthese."""
        d = os.path.join(os.path.dirname(MUSIC_DIR), 'sfx')
        if not os.path.isdir(d):
            return
        groups = {}
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.ogg') and '_' in fn:
                nm = fn.rsplit('_', 1)[0]
                try:
                    groups.setdefault(nm, []).append(pygame.mixer.Sound(os.path.join(d, fn)))
                except Exception:
                    pass
        for nm, snds in groups.items():
            self.sfx[nm] = snds[0]
            if len(snds) > 1:
                self.var[nm] = snds
            else:
                self.var.pop(nm, None)

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

    # ------------------------------------------------------------ Neue Musik-Engine
    def _ks(self, f, dur, decay=0.9965, bright=0.55):
        """Karplus-Strong-Saite (Koto/Shamisen) – vektorisiert blockweise, mit Bruchteil-Verzögerung."""
        key = (round(f, 1), round(dur, 2), decay, bright)
        c = self._kscache.get(key)
        if c is not None:
            return c
        n = int(SR * dur)
        period = SR / f - 0.5
        N = max(2, int(period))
        r = period - N
        y = np.zeros(n + N + 2)
        exc = np.random.uniform(-1, 1, N)
        k = max(1, int(1 + (1 - bright) * 6))
        exc = np.convolve(exc, np.ones(k) / k, mode='same')
        y[2:N + 2] = exc
        i = N + 2
        while i < len(y):
            j = min(len(y), i + N)
            L = j - i
            a = y[i - N:i - N + L]
            b = y[i - N - 1:i - N - 1 + L]
            c2 = y[i - N - 2:i - N - 2 + L]
            y[i:j] = decay * ((1 - r) * 0.5 * (a + b) + r * 0.5 * (b + c2))
            i = j
        out = y[2:n + 2]
        att = np.minimum(1, np.arange(n) / (SR * 0.002))
        out = out * att
        self._kscache[key] = out
        return out

    def _sho(self, freqs, dur):
        """Sanftes Shō-Klangbett (Mundorgel): weiche Sinus-Akkorde mit langsamem Ein- und Ausblenden."""
        t = self._t(dur)
        w = np.zeros_like(t)
        for i, f in enumerate(freqs):
            vib = 1 + 0.002 * np.sin(2 * np.pi * (0.3 + i * 0.07) * t)
            ph = np.cumsum(2 * np.pi * f * vib / SR)
            w += np.sin(ph) * 0.6 + np.sin(2 * ph) * 0.12
        env = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5).clip(0, 1)
        return w * env / len(freqs)

    def _shaku(self, f, dur):
        """Shakuhachi: Hauchton mit Tonhöhen-Gleiten am Anfang und langsamem Vibrato."""
        t = self._t(dur)
        bend = 1 - 0.03 * np.exp(-t * 6)
        vib = 1 + 0.006 * np.sin(2 * np.pi * 4.8 * t) * np.minimum(1, t / 0.6)
        ph = np.cumsum(2 * np.pi * f * bend * vib / SR)
        tone = np.sin(ph) + 0.08 * np.sin(2 * ph)
        breath = np.convolve(np.random.uniform(-1, 1, len(t)), np.ones(12) / 12, mode='same') * 0.35
        env = np.minimum(1, t / 0.25) ** 1.5 * np.minimum(1, (dur - t) / 0.5).clip(0, 1)
        return (tone * 0.8 + breath * (0.3 + 0.5 * np.exp(-t * 3))) * env

    def _drum(self, f=62, dur=0.6, soft=True):
        """Weiche Taiko: tiefer Sinus mit Tonhöhen-Abfall, nur ein Hauch Fell-Geräusch."""
        t = self._t(dur)
        ft = f * (1 + 0.6 * np.exp(-t * 30))
        ph = np.cumsum(2 * np.pi * ft / SR)
        w = np.sin(ph) * np.exp(-t * 6)
        noise = np.convolve(np.random.uniform(-1, 1, len(t)), np.ones(30) / 30, mode='same') * np.exp(-t * 40)
        return (w + noise * (0.3 if soft else 0.6)) * np.minimum(1, t / 0.003)

    def _wood(self, dur=0.08):
        t = self._t(dur)
        return np.sin(2 * np.pi * 1200 * t) * np.exp(-t * 60) * 0.5 + np.sin(2 * np.pi * 760 * t) * np.exp(-t * 45) * 0.5

    @staticmethod
    def _reverb(x, seconds=1.6, wet=0.28):
        n = int(SR * seconds)
        ir = np.random.uniform(-1, 1, n) * np.exp(-np.arange(n) / (SR * seconds / 5))
        ir = np.convolve(ir, np.ones(8) / 8, mode='same')
        ir /= np.sqrt(np.sum(ir ** 2)) + 1e-9
        L = len(x) + n
        size = 1 << (L - 1).bit_length()
        X = np.fft.rfft(x, size)
        Y = np.fft.irfft(X * np.fft.rfft(ir, size), size)[:len(x)]
        # Hallfahne an den Anfang falten -> nahtloser Loop
        tail = np.fft.irfft(X * np.fft.rfft(ir, size), size)[len(x):L]
        Y[:len(tail)] += tail
        return x * (1 - wet) + Y * wet * 0.6

    @staticmethod
    def _lowpass(x, cutoff=5200):
        X = np.fft.rfft(x)
        fr = np.fft.rfftfreq(len(x), 1 / SR)
        X *= 1 / (1 + (fr / cutoff) ** 4)
        return np.fft.irfft(X, len(x))

    def _make_music(self, key):
        scale_name, root, bpm, mood, seed = key
        rng = random.Random(seed)
        np.random.seed(seed % (2 ** 31))
        sc = self.SCALES[scale_name]
        if mood in ('calm', 'mystic'):
            bpm = int(bpm * 0.85)
        beat = 60 / bpm
        bars = 16
        total = bars * 4 * beat
        n = int(SR * total)
        out = np.zeros(n + SR * 4)

        def put(w, t0, v=1.0):
            i = int(t0 * SR) % n
            j = i + len(w)
            out[i:j] += w * v

        def note(deg, octave=0):
            o, d = divmod(deg, len(sc))
            return root * 2 ** ((sc[d] + 12 * (o + octave)) / 12)

        # --- Melodie: Phrasen A A' B A'' mit überwiegend Schrittbewegung
        rhythms = [[2, 1, 1, 2, 2], [1, 1, 2, 4], [2, 2, 1, 1, 2], [3, 1, 2, 2], [4, 2, 2], [1, 1, 1, 1, 4]]

        def phrase(start_deg, length_bars=4):
            notes = []
            deg = start_deg
            t8 = 0
            while t8 < length_bars * 8:
                rh = rng.choice(rhythms)
                for r_ in rh:
                    if t8 >= length_bars * 8:
                        break
                    if rng.random() < 0.18:
                        notes.append((t8, None, r_))
                    else:
                        step = rng.choice([-1, -1, 1, 1, 0, 2, -2])
                        deg = max(-2, min(9, deg + step))
                        notes.append((t8, deg, r_))
                    t8 += r_
            # Phrase auf Grundton oder Quinte enden lassen
            for i in range(len(notes) - 1, -1, -1):
                if notes[i][1] is not None:
                    notes[i] = (notes[i][0], rng.choice([0, 5, 3]), max(notes[i][2], 4))
                    break
            return notes

        A = phrase(rng.choice([2, 4, 5]))
        B = phrase(rng.choice([5, 7]))
        A2 = [(t_, (d + rng.choice([0, 0, 1, -1]) if d is not None and rng.random() < 0.3 else d), r_) for t_, d, r_ in A]
        form = [A, A2, B, A]
        e8 = beat / 2
        for pi, ph in enumerate(form):
            base = pi * 4 * 4 * beat
            for t8, deg, r_ in ph:
                if deg is None:
                    continue
                f = note(deg, 1)
                dur = min(2.4, r_ * e8 * 3 + 0.6)
                put(self._ks(f, dur, 0.9968, 0.5), base + t8 * e8, 0.42)
                # Koto-Verzierung: gelegentlicher Vorschlag
                if r_ >= 2 and rng.random() < 0.2:
                    put(self._ks(note(deg + 1, 1), 0.3, 0.99, 0.4), base + t8 * e8 - 0.06, 0.12)
        # --- Begleitung: tiefe Koto-Arpeggien (Grundton, Quinte, Oktave)
        prog = [0, 0, 3, 2, 0, 0, 4, 3, 0, 0, 3, 2, 5, 4, 3, 0] if mood != 'dark' else [0, 0, 1, 0, 0, 1, 2, 1] * 2
        for b in range(bars):
            d = prog[b % len(prog)]
            t0 = b * 4 * beat
            for k, (dd, oc) in enumerate(((d, -1), (d + 3, -1), (d, 0), (d + 3, -1))):
                put(self._ks(note(dd, oc), 1.6, 0.997, 0.35), t0 + k * beat, 0.2)
        # --- Shō-Klangbett
        for b in range(0, bars, 4):
            d = prog[b % len(prog)]
            put(self._sho([note(d, 0), note(d + 3, 0), note(d + 5, 0)], 4 * 4 * beat + 1.0), b * 4 * beat, 0.11)
        # --- Shakuhachi
        if mood in ('calm', 'mystic', 'dark'):
            t = beat * 8
            while t < total - beat * 6:
                d = rng.choice([4, 5, 7, 3])
                dur = rng.choice([4, 6, 8]) * beat
                put(self._shaku(note(d, 0), dur), t, 0.13)
                t += dur + rng.choice([6, 8, 12]) * beat
        # --- Rhythmus
        if mood in ('battle', 'boss', 'dark'):
            pat = {'battle': [1, 0, 0, 0, 1, 0, 1, 0], 'dark': [1, 0, 0, 0, 0, 0, 1, 0],
                   'boss': [1, 0, 1, 0, 1, 0, 1, 1]}[mood]
            for i in range(bars * 8):
                tt = i * e8
                if pat[i % 8]:
                    put(self._drum(58 if i % 8 == 0 else 72), tt, 0.5 if mood == 'boss' else 0.38)
                if mood != 'dark' and i % 2 == 1:
                    put(self._wood(), tt, 0.05)
        elif mood == 'mystic':
            for b in range(bars):
                put(self._wood(0.2), b * 4 * beat + 3 * beat, 0.04)
        # Loop schließen (Ausklang an den Anfang)
        tail = out[n:]
        out = out[:n].copy()
        out[:len(tail)] += tail
        out = self._lowpass(out, 5000)
        out = self._reverb(out)
        out = np.tanh(out / (np.abs(out).max() + 1e-9) * 1.4) * 0.55
        return self._snd(out)

    def prepare(self, key):
        nm = self.track_for(key)
        if nm and os.path.exists(os.path.join(MUSIC_DIR, nm + '.ogg')):
            return
        if self.ok and key and key not in self.music_cache:
            self.music_cache[key] = self._make_music(key)

    @staticmethod
    def track_for(key):
        """Ordnet einen Musik-Schlüssel einem komponierten Stück in assets/music zu."""
        if key is None:
            return None
        seed, mood = key[4], key[3]
        if seed == 99:
            return 'title'
        if seed == 77:
            return 'gameover'
        if seed == 78:
            return 'victory'
        if mood == 'boss':
            return 'boss_final' if (seed - 100) // 10 >= 5 else 'boss'
        return {1: 'forest', 2: 'temple', 3: 'mountain', 4: 'sea', 5: 'underworld', 6: 'heaven'}.get(seed // 10)

    def music(self, key):
        """key = (skala, grundton, bpm, stimmung, seed)"""
        if not self.ok:
            return
        name = self.track_for(key)
        path = os.path.join(MUSIC_DIR, name + '.ogg') if name else None
        ident = name if path and os.path.exists(path) else key
        if self.cur_music == ident:
            return
        self.cur_music = ident
        if key is None:
            self.music_ch.fadeout(400)
            pygame.mixer.music.fadeout(400)
            return
        if path and os.path.exists(path):
            try:
                self.music_ch.fadeout(300)
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(self.vol_music)
                pygame.mixer.music.play(loops=-1, fade_ms=900)
                return
            except Exception as e:  # pragma: no cover
                print('Musik konnte nicht geladen werden:', e)
        pygame.mixer.music.fadeout(300)
        if key not in self.music_cache:
            self.music_cache[key] = self._make_music(key)
        self.music_ch.set_volume(self.vol_music)
        self.music_ch.play(self.music_cache[key], loops=-1, fade_ms=600)

    def set_volumes(self, sfx, music):
        self.vol_sfx = sfx
        self.vol_music = music
        if self.ok and self.music_ch:
            self.music_ch.set_volume(music)
            pygame.mixer.music.set_volume(music)


AUDIO = None


def get():
    global AUDIO
    if AUDIO is None:
        AUDIO = Audio()
    return AUDIO


def play(name, vol=1.0):
    if AUDIO:
        AUDIO.play(name, vol)
