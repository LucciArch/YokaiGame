"""Synthesizer für den Soundtrack von Yōkai no Michi.

Alles wird hier aus Formeln erzeugt – keine fremden Samples.
Instrumente: Koto, Shamisen, Shakuhachi, Shinobue, Shō, Taiko (Ōdaiko, Shime, Ka), Kane/Rin-Glocken,
Bonshō (Tempelglocke), Hyōshigi, dunkle Drones und Wind.
"""
import math
import subprocess
import wave

import numpy as np
from scipy import signal

SR = 44100
RNG = np.random.default_rng(1)


def seed(s):
    global RNG
    RNG = np.random.default_rng(s)


def t_axis(dur):
    return np.arange(int(SR * dur)) / SR


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# ------------------------------------------------------------------ Filter
def biquad(x, kind, f, q=0.7, gain_db=0.0):
    f = min(f, SR * 0.45)
    w0 = 2 * math.pi * f / SR
    al = math.sin(w0) / (2 * q)
    cw = math.cos(w0)
    A = 10 ** (gain_db / 40)
    if kind == 'lp':
        b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]; a = [1 + al, -2 * cw, 1 - al]
    elif kind == 'hp':
        b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]; a = [1 + al, -2 * cw, 1 - al]
    elif kind == 'bp':
        b = [al, 0, -al]; a = [1 + al, -2 * cw, 1 - al]
    elif kind == 'peak':
        b = [1 + al * A, -2 * cw, 1 - al * A]; a = [1 + al / A, -2 * cw, 1 - al / A]
    else:
        raise ValueError(kind)
    return signal.lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


def onepole_lp(x, f):
    a = math.exp(-2 * math.pi * f / SR)
    return signal.lfilter([1 - a], [1, -a], x)


def noise(n):
    return RNG.uniform(-1, 1, n)


def env_adsr(n, a=0.01, d=0.1, s=0.7, r=0.2):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.where(t < a, t / max(a, 1e-4), 1.0)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s) * (t - a) / max(d, 1e-4), e)
    e = np.where(t >= a + d, s, e)
    rel = np.clip((dur - t) / max(r, 1e-4), 0, 1)
    return e * rel


def pitch_warp(x, ratio):
    """Tonhöhe zeitabhängig verändern (ratio pro Sample, 1 = unverändert)."""
    pos = np.cumsum(ratio) - ratio[0]
    pos = pos[pos < len(x) - 1]
    return np.interp(pos, np.arange(len(x)), x)


# ------------------------------------------------------------------ Saiten (Karplus-Strong)
_ks_cache = {}


def ks(f, dur, decay=0.996, bright=0.5, pick=0.5):
    key = (round(f, 2), round(dur, 3), decay, bright, pick)
    if key in _ks_cache:
        return _ks_cache[key].copy()
    n = int(SR * dur)
    period = SR / f
    N = max(2, int(period - 0.5))
    frac = period - 0.5 - N
    y = np.zeros(n + N + 2)
    exc = noise(N)
    k = max(1, int(1 + (1 - bright) * 10))
    exc = np.convolve(exc, np.ones(k) / k, mode='same')
    # Anschlagposition: Kammfilter im Erreger
    p = max(1, int(N * pick * 0.5))
    exc = exc - np.roll(exc, p) * 0.6
    exc -= exc.mean()
    y[2:N + 2] = exc
    i = N + 2
    g = decay ** (1.0 / max(1.0, f / 220.0) ** 0.15)
    while i < len(y):
        j = min(len(y), i + N)
        L = j - i
        a = y[i - N:i - N + L]
        b = y[i - N - 1:i - N - 1 + L]
        c = y[i - N - 2:i - N - 2 + L]
        y[i:j] = g * ((1 - frac) * 0.5 * (a + b) + frac * 0.5 * (b + c))
        i = j
    out = y[2:n + 2].copy()
    out *= np.minimum(1, np.arange(n) / (SR * 0.0015))
    out /= (np.abs(out).max() + 1e-9)
    _ks_cache[key] = out
    return out.copy()


def koto(f, dur, vel=0.8, bend=None, bright=None):
    """Koto: KS-Saite mit Holzkörper-Resonanz. bend: (verzögerung s, Halbtöne, Gleitzeit) für Oshide."""
    br = 0.35 + 0.35 * vel if bright is None else bright
    x = ks(f, dur + 0.05, decay=0.9978, bright=br, pick=0.3)
    click = noise(int(SR * 0.012)) * np.exp(-np.arange(int(SR * 0.012)) / (SR * 0.002))
    click = biquad(click, 'hp', 2500)
    x[:len(click)] += click * 0.25 * vel
    x = biquad(x, 'peak', 220, 1.2, 4) + 0.0
    x = biquad(x, 'peak', 520, 1.5, 3)
    x = biquad(x, 'lp', 3500 + 3500 * vel, 0.6)
    if bend:
        delay, semis, glide = bend
        n = len(x)
        t = np.arange(n) / SR
        r = np.ones(n)
        target = 2 ** (semis / 12)
        m = t > delay
        r[m] = 1 + (target - 1) * np.clip((t[m] - delay) / glide, 0, 1)
        x = pitch_warp(x, r)
    e = np.ones(len(x))
    e[-int(SR * 0.05):] = np.linspace(1, 0, int(SR * 0.05))
    return x * e * vel


def shamisen(f, dur, vel=0.8):
    """Shamisen: helle Saite mit Sawari-Schnarren und Bachi-Anschlag."""
    x = ks(f, dur + 0.05, decay=0.986, bright=0.85, pick=0.12)
    tt = np.arange(len(x)) / SR
    x = x * np.exp(-tt * 2.5)
    # Sawari: nichtlineares Schnarren, das mit der Saite abklingt
    buzz = np.tanh(x * 4) - x * 0.9
    buzz = biquad(buzz, 'bp', 2400, 0.8)
    x = x + buzz * 0.35
    n = int(SR * 0.02)
    bachi = noise(n) * np.exp(-np.arange(n) / (SR * 0.003))
    x[:n] += biquad(bachi, 'bp', 1800, 1.0) * 0.9 * vel
    thump = np.sin(2 * np.pi * 140 * np.arange(n) / SR) * np.exp(-np.arange(n) / (SR * 0.006))
    x[:n] += thump * 0.5 * vel
    x = biquad(x, 'peak', 900, 1.0, 5)       # Fellkorpus (Katzen-/Hundefell)
    x = biquad(x, 'lp', 6000, 0.7)
    e = np.ones(len(x)); e[-int(SR * 0.04):] = np.linspace(1, 0, int(SR * 0.04))
    return x * e * vel


# ------------------------------------------------------------------ Blasinstrumente (Phrasen-Renderer)
def wind_phrase(notes, kind='shaku', vel=0.8):
    """notes: Liste (start_s, dur_s, freq, accent). Rendert eine zusammenhängende Phrase mit Legato,
    Portamento, verzögertem Vibrato (Yuri) und Atemgeräusch (Muraiki)."""
    if not notes:
        return np.zeros(1), 0.0
    t0 = notes[0][0]
    end = max(s + d for s, d, f, a in notes)
    n = int(SR * (end - t0 + 0.6))
    fcur = np.zeros(n)
    amp = np.zeros(n)
    vib = np.zeros(n)
    acc = np.zeros(n)
    glide = 0.06 if kind == 'shaku' else 0.035
    for idx, (s, d, f, a) in enumerate(notes):
        i0 = int((s - t0) * SR)
        i1 = min(n, int((s - t0 + d) * SR))
        fcur[i0:i1] = f
        L = i1 - i0
        tt = np.arange(L) / SR
        att = 0.09 if kind == 'shaku' else 0.03
        rel = min(0.18, d * 0.3)
        legato = idx + 1 < len(notes) and notes[idx + 1][0] - (s + d) < 0.02
        tied = idx > 0 and s - (notes[idx - 1][0] + notes[idx - 1][1]) < 0.02
        e = np.minimum(1, tt / att) ** (1.6 if kind == 'shaku' else 1.0)
        if tied:
            dip = 0.75 if a > 0.5 else 0.92          # Atari: kleiner Akzent statt neuem Einsatz
            e = 1 - (1 - dip) * np.exp(-tt / 0.04) * np.minimum(1, tt / 0.01 + 0.2)
        if not legato:
            e *= np.clip((d - tt) / rel, 0, 1)
        swell = 1 + 0.12 * np.sin(np.pi * np.clip(tt / max(d, 0.1), 0, 1))
        amp[i0:i1] = np.maximum(amp[i0:i1], e * swell * (0.75 + 0.25 * a))
        vd = 0.006 if kind == 'shaku' else 0.004
        vib[i0:i1] = np.clip((tt - 0.35) / 0.5, 0, 1) * vd * (1 if d > 0.5 else 0.3)
        acc[i0:i0 + int(SR * 0.08)] += a * np.exp(-np.arange(min(int(SR * 0.08), n - i0)) / (SR * 0.025))
    # Portamento in Log-Frequenz
    held = fcur.copy()
    nz = held > 0
    idx = np.where(nz, np.arange(n), 0)
    np.maximum.accumulate(idx, out=idx)
    held = held[idx]
    held[held == 0] = notes[0][2]
    lf = np.log(held)
    lf = onepole_lp(lf - lf[0], 1 / (2 * math.pi * glide)) + lf[0]
    t = np.arange(n) / SR
    rate = 5.0 if kind == 'shaku' else 6.2
    fm = np.exp(lf) * (1 + vib * np.sin(2 * np.pi * rate * t + 0.3 * np.sin(2 * np.pi * 0.7 * t)))
    # Anfangs-Gleiten von unten (Meri -> Kari) bei Akzenten
    ph = np.cumsum(2 * np.pi * fm / SR)
    if kind == 'shaku':
        harm = [(1, 1.0), (2, 0.28), (3, 0.12), (4, 0.05), (5, 0.03)]
        breath_amt = 0.22
    else:
        harm = [(1, 1.0), (2, 0.45), (3, 0.2), (4, 0.08), (5, 0.04), (6, 0.02)]
        breath_amt = 0.16
    tone = sum(h_a * np.sin(h * ph) for h, h_a in harm)
    nb = noise(n)
    breath_tonal = biquad(nb, 'bp', 1500 if kind == 'shaku' else 3000, 0.5) * (1 + np.sin(ph)) * 0.5
    breath_air = biquad(nb, 'hp', 2500) * 0.5
    breath = (breath_tonal * 1.0 + breath_air * 0.12) * breath_amt * (amp * 0.7 + acc * 1.6)
    out = tone * amp * 0.6 + breath
    out = biquad(out, 'lp', 5200 if kind == 'shaku' else 8000, 0.6)
    return out * vel, t0


# ------------------------------------------------------------------ Shō (Mundorgel)
def sho(freqs, dur, vel=0.5):
    n = int(SR * dur)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for i, f in enumerate(freqs):
        det = 1 + (i - len(freqs) / 2) * 0.0007
        ph = 2 * np.pi * f * det * t + RNG.uniform(0, 6.28)
        for h, a in ((1, 1.0), (2, 0.35), (3, 0.25), (4, 0.1), (5, 0.08), (7, 0.03)):
            out += np.sin(h * ph) * a
    breathe = 0.85 + 0.15 * np.sin(2 * np.pi * t / max(4.0, dur / 2) - 1.5)
    e = np.minimum(1, t / 1.8) * np.clip((dur - t) / 1.8, 0, 1)
    out = biquad(out, 'lp', 2600, 0.6)
    return out * e * breathe * vel / (len(freqs) * 1.6)


# ------------------------------------------------------------------ Schlagwerk
def odaiko(f=52, vel=1.0, dur=1.6):
    n = int(SR * dur)
    t = np.arange(n) / SR
    modes = [(1.0, 1.0, 3.5), (1.59, 0.45, 6), (2.14, 0.25, 9), (2.65, 0.12, 12)]
    out = np.zeros(n)
    for r, a, dcy in modes:
        fr = f * r * (1 + 0.5 * np.exp(-t * 25))
        out += a * np.sin(np.cumsum(2 * np.pi * fr / SR)) * np.exp(-t * dcy)
    hit = biquad(noise(n), 'lp', 900) * np.exp(-t * 35)
    out += hit * 0.6
    return np.tanh(out * 1.3) * vel


def shime(f=330, vel=0.8):
    n = int(SR * 0.35)
    t = np.arange(n) / SR
    fr = f * (1 + 0.15 * np.exp(-t * 60))
    out = np.sin(np.cumsum(2 * np.pi * fr / SR)) * np.exp(-t * 22)
    out += np.sin(np.cumsum(2 * np.pi * fr * 1.6 / SR)) * np.exp(-t * 30) * 0.4
    crack = biquad(noise(n), 'bp', 3200, 0.9) * np.exp(-t * 90)
    return (out * 0.8 + crack * 1.4) * vel


def ka(vel=0.6):
    """Schlag auf den Taiko-Rand."""
    n = int(SR * 0.08)
    t = np.arange(n) / SR
    out = np.sin(2 * np.pi * 1850 * t) * np.exp(-t * 80) + np.sin(2 * np.pi * 980 * t) * np.exp(-t * 60) * 0.6
    out += biquad(noise(n), 'bp', 4000, 1.2) * np.exp(-t * 150) * 0.6
    return out * vel


def hyoshigi(vel=0.7):
    n = int(SR * 0.25)
    t = np.arange(n) / SR
    out = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in ((2210, 1, 30), (3470, 0.5, 45), (5900, 0.25, 70)))
    out += biquad(noise(n), 'hp', 3000) * np.exp(-t * 200) * 0.5
    return out * vel


def kane(f=880, vel=0.6, dur=4.0):
    """Kleine Tempelglocke / Rin-Schale: inharmonische Teiltöne mit Schwebung."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for r, a, d in ((1.0, 1.0, 0.9), (2.71, 0.55, 1.6), (5.15, 0.25, 3.0), (8.4, 0.1, 5.0)):
        out += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) * (1 + 0.25 * np.sin(2 * np.pi * (0.7 + r * 0.3) * t))
    out *= np.minimum(1, t / 0.002)
    return out * vel * 0.5


def bonsho(f=62, vel=0.8, dur=9.0):
    """Große Tempelglocke (Bonshō): tief, lange schwebend."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for r, a, d in ((0.5, 0.8, 0.35), (1.0, 1.0, 0.45), (1.19, 0.5, 0.6), (2.0, 0.45, 0.8), (2.53, 0.3, 1.1), (3.4, 0.15, 1.6)):
        beat = 1 + 0.4 * np.sin(2 * np.pi * (0.4 + r * 0.15) * t)
        out += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * d) * beat
    strike = biquad(noise(int(SR * 0.1)), 'lp', 600) * np.exp(-np.arange(int(SR * 0.1)) / (SR * 0.02))
    out[:len(strike)] += strike * 0.8
    return out * vel * 0.45


# ------------------------------------------------------------------ Flächen
def drone(f, dur, vel=0.4, cutoff=600, detune=0.004):
    """Dunkle Saiten-Fläche: verstimmte Sägezähne durch wanderndes Tiefpassfilter."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    out = np.zeros(n)
    nh = max(1, int(cutoff * 2.5 / f))
    for d in (-detune, 0, detune):
        p0 = RNG.uniform(0, 6.28)
        for h in range(1, nh + 1):
            out += np.sin(2 * np.pi * f * (1 + d) * h * t + p0 * h) / h
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * t / 7.0)
    seg = 2048
    y = np.zeros(n)
    zi = None
    for i in range(0, n, seg):
        fc = cutoff * (0.6 + 0.8 * lfo[i])
        b, a = signal.butter(2, min(fc, SR * 0.45) / (SR / 2))
        if zi is None:
            zi = signal.lfilter_zi(b, a) * 0
        y[i:i + seg], zi = signal.lfilter(b, a, out[i:i + seg], zi=zi)
    e = np.minimum(1, t / 2.5) * np.clip((dur - t) / 2.5, 0, 1)
    return y * e * vel / 3


def wind(dur, vel=0.3, center=500):
    n = int(SR * dur)
    t = np.arange(n) / SR
    x = noise(n)
    seg = 4096
    y = np.zeros(n)
    for i in range(0, n, seg):
        fc = center * (0.6 + 0.8 * (0.5 + 0.5 * math.sin(2 * math.pi * i / SR / 9.0)))
        y[i:i + seg] = biquad(x[i:i + seg], 'bp', fc, 2.0)
    y = onepole_lp(y, 2000)
    e = np.minimum(1, t / 3) * np.clip((dur - t) / 3, 0, 1) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 5.3))
    return y * e * vel * 3


# ------------------------------------------------------------------ Mischpult
class Mix:
    def __init__(self, dur, tail=6.0):
        self.n = int(SR * dur)
        self.len = self.n + int(SR * tail)
        self.dry = np.zeros((2, self.len))
        self.wet = np.zeros((2, self.len))

    def add(self, x, t, gain=1.0, pan=0.0, rev=0.25):
        i = int(t * SR)
        if i < 0:
            x = x[-i:]; i = 0
        j = min(self.len, i + len(x))
        if j <= i:
            return
        x = x[:j - i] * gain
        l = math.cos((pan + 1) * math.pi / 4)
        r = math.sin((pan + 1) * math.pi / 4)
        self.dry[0, i:j] += x * l * (1 - rev * 0.5)
        self.dry[1, i:j] += x * r * (1 - rev * 0.5)
        self.wet[0, i:j] += x * l * rev
        self.wet[1, i:j] += x * r * rev

    def render(self, room=3.2, loop=True, damp=3500):
        out = self.dry.copy()
        for ch in range(2):
            out[ch] += reverb(self.wet[ch], room, seed_=11 + ch * 7, damp=damp)
        out[0] = biquad(out[0], 'hp', 32, 0.7)
        out[1] = biquad(out[1], 'hp', 32, 0.7)
        if loop:
            tail = out[:, self.n:]
            out = out[:, :self.n].copy()
            m = min(tail.shape[1], self.n)
            out[:, :m] += tail[:, :m]
        pk = np.abs(out).max() + 1e-9
        out = out / pk
        out = np.tanh(out * 1.25) / math.tanh(1.25)
        rms = np.sqrt((out ** 2).mean())
        target = 0.16
        out = out * min(0.95 / (np.abs(out).max() + 1e-9), target / (rms + 1e-9))
        return out


def reverb(x, seconds=3.0, seed_=1, damp=3500):
    rng = np.random.default_rng(seed_)
    n = int(SR * seconds)
    t = np.arange(n) / SR
    ir = rng.uniform(-1, 1, n) * np.exp(-t * 6.9 / seconds)
    # frequenzabhängige Dämpfung: späte Anteile dunkler
    dark = onepole_lp(ir, damp * 0.35)
    mixw = np.clip(t / seconds * 2, 0, 1)
    ir = ir * (1 - mixw) + dark * mixw * 1.8
    pre = int(SR * 0.025)
    ir = np.concatenate([np.zeros(pre), ir])
    for d, g in ((0.011, 0.5), (0.019, 0.35), (0.027, 0.3), (0.041, 0.25)):
        k = int(d * SR)
        if k < len(ir):
            ir[k] += g * (1 if rng.random() > 0.5 else -1)
    ir = onepole_lp(ir, damp)
    ir /= np.sqrt((ir ** 2).sum()) + 1e-9
    L = len(x) + len(ir)
    size = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[:len(x)]
    return y * 0.9


def write_ogg(path, stereo, q=4):
    pcm = (np.clip(stereo.T, -1, 1) * 32000).astype(np.int16)
    wav = path.rsplit('.', 1)[0] + '.wav'
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'libvorbis', '-q:a', str(q), path], check=True)
    return wav
