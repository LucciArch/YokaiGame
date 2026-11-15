"""Kleine Notations-Hilfen zum Komponieren.

Melodie-Notation (Tokens durch Leerzeichen, '|' wird ignoriert):
    5        Skalenstufe 5, Standardlänge
    5'  5,   eine Oktave höher / tiefer (mehrfach möglich)
    5/3      Länge 3 Achtel (auch 5/0.5 für Sechzehntel)
    5^       Koto-Oshide: Ton nach dem Anschlag einen Ganzton hochdrücken
    5~       Koto: Halbton hochdrücken
    5!       Akzent
    r/4      Pause
    5-7      Bindung (für Bläser: gleitet von 5 nach 7 innerhalb der Länge)
Schlagwerk-Muster: ein Zeichen pro Raster-Schritt
    O ōdaiko laut  o ōdaiko leise  S shime laut  s shime leise  k Rand (ka)  h hyōshigi  . nichts
"""
import random
import synth as Y

SCALES = {
    'hira': [0, 2, 3, 7, 8],       # Hirajōshi (klassische Koto-Stimmung)
    'in': [0, 1, 5, 7, 8],         # Miyako-bushi
    'yo': [0, 2, 5, 7, 9],
    'iwato': [0, 1, 5, 6, 10],
    'kumoi': [0, 2, 3, 7, 9],
    'ryukyu': [0, 4, 5, 7, 11],
}


class Song:
    def __init__(self, bpm, root_midi, scale, bars, beats=4, tail=6.0, seed=1):
        Y.seed(seed)
        self.rng = random.Random(seed)
        self.bpm = bpm
        self.beat = 60.0 / bpm
        self.e8 = self.beat / 2
        self.root = root_midi
        self.scale = SCALES[scale] if isinstance(scale, str) else scale
        self.beats = beats
        self.bar = beats * self.beat
        self.bars = bars
        self.dur = bars * self.bar
        self.mix = Y.Mix(self.dur, tail)

    # -------------------------------------------------------------- Tonhöhen
    def midi(self, deg, octv=0):
        o, d = divmod(deg, len(self.scale))
        return self.root + 12 * (o + octv) + self.scale[d]

    def f(self, deg, octv=0):
        return Y.mtof(self.midi(deg, octv))

    def t(self, bar, e8=0.0):
        return bar * self.bar + e8 * self.e8

    # -------------------------------------------------------------- Parser
    def parse(self, seq, dflt=2):
        out = []
        pos = 0.0
        for tok in seq.replace('|', ' ').split():
            ln = dflt
            if '/' in tok:
                tok, l_ = tok.split('/')
                ln = float(l_)
            if tok.startswith('r'):
                pos += ln
                continue
            acc = '!' in tok
            bend = 2 if '^' in tok else (1 if '~' in tok else 0)
            tok = tok.replace('!', '').replace('^', '').replace('~', '')
            to = None
            if '-' in tok[1:]:
                a, b = tok[0] + tok[1:].split('-', 1)[0], tok[1:].split('-', 1)[1]
                tok, to = a, b
            octs = tok.count("'") - tok.count(',')
            deg = int(tok.replace("'", '').replace(',', ''))
            deg_to = None
            if to is not None:
                o2 = to.count("'") - to.count(',')
                deg_to = int(to.replace("'", '').replace(',', '')) + o2 * len(self.scale)
            out.append(dict(pos=pos, len=ln, deg=deg + octs * len(self.scale), acc=acc, bend=bend, to=deg_to))
            pos += ln
        return out, pos

    # -------------------------------------------------------------- Instrumente
    def koto(self, seq, bar, octv=0, vel=0.75, pan=-0.2, rev=0.3, ring=2.5, dflt=2):
        notes, ln = self.parse(seq, dflt)
        for nt in notes:
            f = self.f(nt['deg'], octv)
            dur = min(ring, max(0.6, nt['len'] * self.e8 * 2.5))
            bend = None
            if nt['bend']:
                bend = (min(0.25, nt['len'] * self.e8 * 0.4), nt['bend'], 0.12)
            v = vel * (1.15 if nt['acc'] else 1.0) * self.rng.uniform(0.9, 1.05)
            x = Y.koto(f, dur, min(1, v), bend)
            self.mix.add(x, self.t(bar, nt['pos']) + self.rng.uniform(-0.006, 0.006), 0.5, pan, rev)
        return ln

    def shamisen(self, seq, bar, octv=0, vel=0.7, pan=0.25, rev=0.18, dflt=1):
        notes, ln = self.parse(seq, dflt)
        for nt in notes:
            x = Y.shamisen(self.f(nt['deg'], octv), max(0.35, nt['len'] * self.e8 * 2), vel * (1.2 if nt['acc'] else 1))
            self.mix.add(x, self.t(bar, nt['pos']), 0.42, pan, rev)
        return ln

    def wind(self, seq, bar, kind='shaku', octv=0, vel=0.7, pan=0.15, rev=0.42, dflt=2):
        notes, ln = self.parse(seq, dflt)
        ph = []
        for nt in notes:
            s = self.t(bar, nt['pos'])
            d = nt['len'] * self.e8
            if nt['to'] is not None:
                ph.append((s, d * 0.55, self.f(nt['deg'], octv), 1.0 if nt['acc'] else 0.3))
                ph.append((s + d * 0.55, d * 0.45, self.f(nt['to'], octv), 0.0))
            else:
                ph.append((s, d, self.f(nt['deg'], octv), 1.0 if nt['acc'] else 0.3))
        # Phrasen an Pausen trennen
        groups, cur = [], []
        for nt in ph:
            if cur and nt[0] - (cur[-1][0] + cur[-1][1]) > 0.05:
                groups.append(cur); cur = []
            cur.append(nt)
        if cur:
            groups.append(cur)
        for g in groups:
            x, t0 = Y.wind_phrase(g, kind, vel)
            self.mix.add(x, t0, 0.55 if kind == 'shaku' else 0.38, pan, rev)
        return ln

    def sho(self, degs, bar, bars_len, octv=0, vel=0.45, pan=0.0, rev=0.5):
        fr = [self.f(d, octv) for d in degs]
        x = Y.sho(fr, bars_len * self.bar + 1.5, vel)
        self.mix.add(x, self.t(bar) - 0.5, 0.6, pan, rev)

    def drone(self, deg, bar, bars_len, octv=-2, vel=0.4, cutoff=500, pan=0.0, rev=0.35):
        x = Y.drone(self.f(deg, octv), bars_len * self.bar + 2.0, vel, cutoff)
        self.mix.add(x, self.t(bar) - 0.8, 0.7, pan, rev)

    def drums(self, pattern, bar, steps_per_beat=2, vel=1.0, rev=0.2, swing=0.0, humanize=0.006):
        step = self.beat / steps_per_beat
        pat = pattern.replace('|', '').replace(' ', '')
        for i, ch in enumerate(pat):
            if ch == '.':
                continue
            tt = self.t(bar) + i * step + (swing * step if i % 2 else 0) + self.rng.uniform(-humanize, humanize)
            if ch == 'O':
                self.mix.add(Y.odaiko(50, 1.0 * vel), tt, 0.55, -0.05, rev)
            elif ch == 'o':
                self.mix.add(Y.odaiko(56, 0.6 * vel), tt, 0.5, 0.05, rev)
            elif ch == 'S':
                self.mix.add(Y.shime(330, 0.9 * vel), tt, 0.32, 0.35, rev)
            elif ch == 's':
                self.mix.add(Y.shime(350, 0.5 * vel), tt, 0.28, 0.35, rev)
            elif ch == 'k':
                self.mix.add(Y.ka(0.6 * vel), tt, 0.25, -0.35, rev)
            elif ch == 'h':
                self.mix.add(Y.hyoshigi(0.6 * vel), tt, 0.25, 0.5, rev + 0.2)
        return len(pat) / steps_per_beat / self.beats

    def bell(self, deg, bar, e8=0, octv=1, vel=0.5, pan=0.3, rev=0.6):
        self.mix.add(Y.kane(self.f(deg, octv), vel), self.t(bar, e8), 0.5, pan, rev)

    def bonsho(self, bar, e8=0, vel=0.8, f=None):
        self.mix.add(Y.bonsho(f or Y.mtof(self.root - 24), vel), self.t(bar, e8), 0.8, 0.0, 0.55)

    def windfx(self, bar, bars_len, vel=0.25, center=500):
        x = Y.wind(bars_len * self.bar + 3, vel, center)
        self.mix.add(x, self.t(bar) - 1.0, 0.6, self.rng.uniform(-0.4, 0.4), 0.3)

    # -------------------------------------------------------------- Begleitmuster
    def arp(self, chords, bar, pattern=(0, 2, 4, 2), octv=-1, vel=0.5, pan=-0.35, per_bar=8, rev=0.3):
        """chords: Liste von Grundstufen pro Takt; pattern: Stufen-Offsets, über den Takt verteilt."""
        for b, c in enumerate(chords):
            if c is None:
                continue
            for i in range(per_bar):
                d = c + pattern[i % len(pattern)]
                self.mix.add(Y.koto(self.f(d, octv), 1.6, vel * (1.1 if i == 0 else 0.85)), self.t(bar + b, i * 8 / per_bar), 0.42, pan, rev)

    def render(self, path, room=3.0, damp=3500):
        st = self.mix.render(room, damp=damp)
        Y.write_ogg(path, st)
        return st
