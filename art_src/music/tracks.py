"""Die Stücke des Soundtracks. Aufruf: python3 tracks.py [name ...]  (ohne Namen: alle)

Leitmotiv (Hirajōshi): 3 4 3 | 2 1 | 0 1 2 | 3   – taucht in vielen Stücken verwandelt wieder auf.
"""
import os
import sys
import time

from score import Song, SCALES
import synth as Y

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'yokai', 'assets', 'music')

THEME = "3/4 4/2 3/2 | 2/6 1/2 | 0/3 1/1 2/4 | 3/8 | 5/4 4/2 3/2 | 4-3/4 2/4 | 1/2 2/2 1/2 0/2 | 0/8"


# ============================================================ Titel: Hyakki Yagyō no Yoru
def title():
    s = Song(72, 62, 'hira', 32, seed=101)
    s.bonsho(0, vel=0.9)
    s.windfx(0, 32, 0.18, 450)
    # Intro: einzelne Koto-Töne im Raum
    s.koto("5'/4 r/4 | 3/4 4^/4 | 2/8 | 1/2 0/6", 0, octv=0, vel=0.8, pan=-0.3, rev=0.5)
    s.bell(5, 2, 4, octv=1, vel=0.25)
    # A: Ostinato + Shakuhachi-Thema
    prog_a = [0, 0, 2, 1, 0, 0, 3, 2]
    s.arp(prog_a, 4, pattern=(0, 2, 4, 5, 4, 2), octv=-1, vel=0.42, per_bar=6)
    s.wind(THEME, 4, 'shaku', octv=0, vel=0.8)
    s.sho([0, 2, 4], 4, 8, octv=0, vel=0.25)
    # A': Koto übernimmt die Melodie eine Oktave höher, Shakuhachi hält Gegenstimme
    s.arp(prog_a, 12, pattern=(0, 2, 4, 5, 4, 2), octv=-1, vel=0.42, per_bar=6)
    s.koto("3'/4 4'/2 3'/2 | 2'^/6 1'/2 | 0'/3 1'/1 2'/4 | 3'/8 | 5'/4 4'/2 3'/2 | 4'~/4 2'/4 | 1'/2 2'/2 1'/2 0'/2 | 0'/8",
           12, vel=0.7, pan=0.1, rev=0.35)
    s.wind("0/16 | 2/8 1/8 | 3/16 | 2/8 0/8", 12, 'shaku', octv=0, vel=0.45, pan=0.35)
    s.sho([0, 2, 4, 5], 12, 4, vel=0.3)
    s.sho([1, 3, 5], 16, 4, vel=0.3)
    for b in range(12, 20):
        s.drums("s.......", b, vel=0.45)
    # B: dunkler, Drone, hoher Shakuhachi-Bogen
    prog_b = [3, 3, 1, 1, 2, 2, 4, 3]
    s.drone(0, 20, 8, octv=-2, vel=0.35, cutoff=420)
    s.arp(prog_b, 20, pattern=(0, 4, 2, 4), octv=-1, vel=0.4, per_bar=8)
    s.wind("7/6 6/2 | 5/8 | 6/4 5/2 4/2 | 3/8 | 4/3 5/1 6/4 | 7-6/4 5/4 | 4/2 3/2 2/2 1/2 | 3/8", 20, 'shaku', vel=0.85)
    for b in (20, 22, 24, 26):
        s.drums("o.......|........", b, vel=0.6)
    s.drums("o...o...|o.o.O...", 26, vel=0.7)
    s.bell(3, 24, 0, octv=1, vel=0.2); s.bell(5, 27, 4, octv=1, vel=0.2)
    # Ausklang: Themenfragment, führt zurück zum Anfang
    s.koto("3/4 4/2 3/2 | 2/8 | 1/4 0/4 | 0,/8", 28, vel=0.55, pan=-0.2, rev=0.5)
    s.sho([0, 2, 4], 28, 4, vel=0.25)
    return s


# ============================================================ Ebene 1: Kitsunebi no Michi (Bambuswald, Inari, Flussufer)
def forest():
    s = Song(84, 57, 'in', 32, seed=201)
    s.windfx(0, 32, 0.12, 700)
    ost = (0, 2, 3, 4, 3, 2, 1, 2)
    s.arp([0, 0, 0, 0], 0, pattern=ost, octv=0, vel=0.38, per_bar=8, pan=-0.3)
    s.drums("h.......", 0); s.drums("h.......", 2)
    mel = "4/3 3/1 2/2 3/2 | 4^/6 r/2 | 5/2 4/2 3/2 2/2 | 3/8 | 4/3 3/1 2/2 1/2 | 2~/4 0/4 | 1/2 2/2 3/2 2/2 | 0/8"
    prog = [0, 0, 2, 2, 0, 0, 1, 0]
    s.arp(prog, 4, pattern=ost, octv=0, vel=0.34, per_bar=8, pan=-0.35)
    s.koto(mel, 4, octv=1, vel=0.75, pan=0.15)
    for b in range(4, 12):
        s.drums("s...s.s.", b, vel=0.6)
    s.drums("o.......", 4); s.drums("o.......", 8)
    # A': Shakuhachi singt das Lied, Koto antwortet
    s.arp(prog, 12, pattern=ost, octv=0, vel=0.34, per_bar=8, pan=-0.35)
    s.wind(mel.replace('^', '').replace('~', ''), 12, 'shaku', octv=1, vel=0.75)
    s.koto("r/6 2/2 | r/8 | r/6 4/2 | 3/4 2/4 | r/6 1/2 | r/8 | r/6 3/2 | 4/8", 12, octv=1, vel=0.45, pan=-0.1)
    for b in range(12, 20):
        s.drums("s...s.s.", b, vel=0.6)
        if b % 2 == 0:
            s.drums("o...k...", b, vel=0.8)
    s.sho([0, 2, 4], 12, 8, octv=1, vel=0.18)
    # B: Fuchsfeuer – Shinobue darüber, volleres Schlagwerk
    progb = [2, 2, 3, 3, 0, 0, 1, 1]
    s.arp(progb, 20, pattern=(0, 2, 4, 2, 0, 2, 4, 5), octv=0, vel=0.36, per_bar=8)
    s.wind("7/2 8/2 7/2 5/2 | 6-5/4 4/4 | 5/2 4/2 3/2 4/2 | 5/8 | 7/2 8/2 9/4 | 8/2 7/2 5/4 | 6/2 5/2 4/2 3/2 | 2/8", 20, 'fue', octv=1, vel=0.7, pan=0.25)
    for b in range(20, 28):
        s.drums("O.s.S.s.|" if b % 2 == 0 else "o.s.S.ss", b, vel=0.75)
    s.drone(0, 20, 8, octv=-1, vel=0.22, cutoff=700)
    # Ausklang
    s.arp([0, 0, 0, 0], 28, pattern=ost, octv=0, vel=0.32, per_bar=8, pan=-0.3)
    s.koto("4/3 3/1 2/2 3/2 | 4^/8 | 2/4 1/4 | 0/8", 28, octv=1, vel=0.6, pan=0.15)
    s.bell(4, 30, 0, octv=1, vel=0.2)
    s.drums("h.......", 31, vel=0.8)
    return s


# ============================================================ Ebene 2: Bōrei no Tera (Geistertempel, Friedhof, Spukvilla)
def temple():
    s = Song(66, 52, 'iwato', 24, seed=301)
    s.drone(0, 0, 12, octv=-1, vel=0.32, cutoff=380)
    s.drone(0, 12, 12, octv=-1, vel=0.32, cutoff=380)
    s.drone(1, 12, 12, octv=-1, vel=0.12, cutoff=300)
    s.windfx(0, 24, 0.2, 380)
    s.bonsho(0, vel=0.7)
    for b, e, d in ((1, 2, 5), (3, 6, 6), (6, 0, 4), (9, 4, 7), (13, 2, 5), (17, 6, 6), (21, 0, 8)):
        s.bell(d, b, e, octv=1, vel=0.22, pan=s.rng.uniform(-0.6, 0.6))
    for b in range(0, 24, 2):
        s.drums("o..o............", b, steps_per_beat=2, vel=0.55)
    s.koto("0/4 1/4 | r/8 | 4/2 3/6 | r/8 | 2/4 1~/4 | r/8 | 0/2 1/2 0/4 | r/8", 2, octv=1, vel=0.6, pan=-0.3, rev=0.6)
    s.wind("r/8 | 3/8 | 4-3/8 | r/8 | 2/6 1/2 | 0/8 | r/8 | r/8", 4, 'shaku', octv=1, vel=0.6, pan=0.3, rev=0.6)
    # B: Spuk wird lauter
    s.arp([0, 1, 0, 1, 0, 1, 3, 2], 12, pattern=(0, 1, 0, 3), octv=0, vel=0.35, per_bar=4, pan=-0.4, rev=0.5)
    s.wind("5/6 4/2 | 3/8 | 4/4 3-2/4 | 1/8 | 2/6 3/2 | 4-5/8 | 3/4 1/4 | 0/8", 12, 'shaku', octv=1, vel=0.7, pan=0.2, rev=0.55)
    s.koto("r/4 5'/4 | r/8 | r/4 4'^/4 | r/8 | r/4 6'/4 | r/8 | r/4 5'/4 | r/8", 12, octv=0, vel=0.45, pan=0.5, rev=0.7)
    for b in (15, 19, 23):
        s.drums("h...............", b, vel=0.5)
    return s


# ============================================================ Ebene 3: Tengu no Mine (Kurama, Schneeberg, Ōe-Berg)
def mountain():
    s = Song(112, 55, 'in', 40, seed=401)
    riff = "0,/1 0/1 2/1 0/1 3/1 2/1 1/1 0/1"
    riff2 = "0,/1 0/1 3/1 0/1 4/1 3/1 2/1 1/1"
    groove = "O..kS.k.o.kkS.k."
    groove2 = "O.kkS.k.O..kS.kS"
    s.drums("O...O...O.O.OOOO", 0, steps_per_beat=4, vel=0.8)
    s.shamisen(riff, 1, vel=0.65); s.shamisen(riff2, 2, vel=0.65); s.shamisen(riff, 3, vel=0.7)
    for b in range(1, 4):
        s.drums(groove, b, steps_per_beat=4, vel=0.7)
    theme = THEME
    for sec in (4, 16):
        for b in range(sec, sec + 12):
            s.shamisen(riff if b % 2 == 0 else riff2, b, vel=0.6)
            s.drums(groove if b % 4 != 3 else groove2, b, steps_per_beat=4, vel=0.75)
        s.wind(theme, sec, 'fue', octv=1, vel=0.75, pan=0.2)
        s.koto("0/2 2/2 3/2 4/2 | 3/2 2/2 1/2 0/2 | 2/2 3/2 4/2 5/2 | 4/8", sec + 8, octv=1, vel=0.6, pan=-0.2)
        s.drone(0, sec, 12, octv=-1, vel=0.2, cutoff=600)
    # Breakdown: Taiko + Shakuhachi
    for b in range(28, 34):
        s.drums("O.......o.......|" if b < 32 else "O...o...O.o.OoOo", b, steps_per_beat=4, vel=0.85)
    s.wind("4/8 | 3-2/8 | 1/6 2/2 | 0/8 | 5/8 | 4/4 3/4", 28, 'shaku', octv=1, vel=0.8)
    s.windfx(28, 6, 0.3, 900)
    for b in range(34, 40):
        s.shamisen(riff if b % 2 == 0 else riff2, b, vel=0.7)
        s.drums(groove2, b, steps_per_beat=4, vel=0.85)
    s.wind("5/4 4/2 3/2 | 4-3/4 2/4 | 1/2 2/2 1/2 0/2 | 0/8 | 3/4 4/2 3/2 | 2/8", 34, 'fue', octv=1, vel=0.8)
    return s


# ============================================================ Ebene 4: Ryūgū no Yume (Drachenpalast, Geisterküste, Tiefsee)
def sea():
    s = Song(88, 53, 'ryukyu', 32, seed=501)
    s.windfx(0, 32, 0.22, 260)
    s.windfx(8, 24, 0.12, 900)
    wave = (0, 2, 4, 5, 7, 5, 4, 2, 4, 2, 1, 2)
    prog = [0, 0, 3, 3, 1, 1, 4, 3]
    for sec in (0, 8, 16, 24):
        s.arp(prog, sec, pattern=wave, octv=0, vel=0.32, per_bar=12, pan=-0.3, rev=0.45)
    s.bell(7, 0, 0, octv=1, vel=0.2)
    mel = "4/3 5/1 4/2 2/2 | 3/6 r/2 | 2/2 3/2 4/2 7/2 | 5/8 | 4/3 2/1 1/2 2/2 | 3/4 2/4 | 1/2 0/2 1/2 2/2 | 0/8"
    s.shamisen(mel.replace('/3', '/3'), 8, octv=1, vel=0.45, pan=0.25, rev=0.35, dflt=2)
    s.wind(mel, 16, 'shaku', octv=1, vel=0.7, pan=0.15, rev=0.5)
    s.sho([0, 2, 4], 16, 8, octv=1, vel=0.16)
    s.wind("7/4 8/4 | 9/8 | 8/2 7/2 5/4 | 4/8 | 5/4 7/4 | 8-7/8 | 5/2 4/2 2/4 | 0/8", 24, 'fue', octv=1, vel=0.6, pan=0.3)
    for b in range(8, 32):
        s.drums("o.....s.|" if b % 2 == 0 else "..s....s", b, vel=0.55)
    s.bonsho(24, vel=0.35, f=None)
    return s


# ============================================================ Ebene 5: Yomotsu Hirasaka (Yomi, Höllenfeuer, Hof des Enma)
def underworld():
    s = Song(104, 48, 'iwato', 32, seed=601)
    for sec in (0, 8, 16, 24):
        s.drone(0, sec, 8, octv=-1, vel=0.35, cutoff=420)
        s.bonsho(sec, vel=0.65)
    s.drone(1, 8, 8, octv=-1, vel=0.15, cutoff=300)
    s.drone(1, 24, 8, octv=-1, vel=0.15, cutoff=300)
    s.windfx(0, 32, 0.25, 300)
    heavy = "O...o.O.O.o.O..."
    heavy2 = "O.o.O..kO.o.OkOk"
    for b in range(4, 32):
        s.drums(heavy if b % 4 != 3 else heavy2, b, steps_per_beat=4, vel=0.8)
    trem = " ".join(["0,/0.5"] * 16)
    trem1 = " ".join(["1,/0.5"] * 16)
    for b in range(8, 32):
        s.shamisen(trem if (b // 2) % 2 == 0 else trem1, b, octv=0, vel=0.32, pan=-0.3, rev=0.25)
    s.wind("8-7/6 r/2 | 6/8 | 5-4/6 r/2 | 3/8 | 4/4 5/4 | 6-5/8 | 3/4 1/4 | 0/8", 8, 'shaku', octv=0, vel=0.85, pan=0.25)
    s.wind("5'/2 4'/2 3'/4 | 2'/8 | 1'/2 2'/2 1'/4 | 0'/8 | 3'/2 4'/2 5'/4 | 6'-5'/8 | 4'/4 3'/4 | 1'/8", 16, 'fue', octv=0, vel=0.65, pan=0.3)
    s.koto("0/2 1/2 0/2 4,/2 | 0/8 | 0/2 1/2 3/2 1/2 | 0/8", 24, octv=1, vel=0.75, pan=-0.2)
    s.koto("0/2 1/2 0/2 4,/2 | 0/8 | 3/2 4/2 3/2 1/2 | 0/8", 28, octv=1, vel=0.75, pan=-0.2)
    return s


# ============================================================ Ebene 6: Takamagahara (Himmelsgefilde, Mondpalast)
def heaven():
    s = Song(80, 62, 'yo', 32, seed=701)
    clusters = [[0, 2, 4, 5], [1, 3, 5, 6], [2, 4, 5, 7], [0, 3, 4, 6]]
    for i, sec in enumerate(range(0, 32, 4)):
        s.sho(clusters[i % 4], sec, 4, octv=0, vel=0.42)
    s.bell(5, 0, 0, octv=1, vel=0.25); s.bell(7, 8, 0, octv=1, vel=0.2); s.bell(4, 16, 0, octv=1, vel=0.2); s.bell(9, 24, 0, octv=1, vel=0.2)
    s.arp([0, 0, 3, 3, 1, 1, 4, 4] * 3, 8, pattern=(0, 2, 4, 7, 4, 2), octv=0, vel=0.32, per_bar=6, pan=-0.35, rev=0.5)
    theme_yo = THEME.replace('4-3', '4-3')
    s.wind(theme_yo, 8, 'fue', octv=1, vel=0.65, pan=0.2, rev=0.55)
    s.koto("3'/4 4'/2 3'/2 | 2'/6 1'/2 | 0'/3 1'/1 2'/4 | 3'/8 | 5'/4 4'/2 3'/2 | 4'~/4 2'/4 | 1'/2 2'/2 1'/2 0'/2 | 0'/8",
           16, octv=0, vel=0.62, pan=0.25)
    s.wind("7/8 | 9/8 | 8/4 7/4 | 5/8 | 7/4 8/4 | 9-8/8 | 7/4 5/4 | 4/8", 24, 'fue', octv=1, vel=0.6, pan=0.15)
    for b in range(8, 32, 2):
        s.drums("o.......s.s.....", b, vel=0.45)
    return s


# ============================================================ Boss: Oni no Ikari
def boss():
    s = Song(140, 52, 'in', 32, seed=801)
    riff = "0,/1 0,/1 3,/1 0,/1 1/1 0/1 3,/1 4,/1"
    riff2 = "0,/1 0,/1 3,/1 0,/1 2/1 1/1 0/1 1/1"
    g1 = "O.kOS.k.O.kOS.kk"
    g2 = "OkOkS.kSO.OkSSkS"
    s.drums("O...O...O...O.O.", 0, steps_per_beat=4, vel=0.9)
    s.drums("O.O.O.O.OOOOSSSS", 1, steps_per_beat=4, vel=0.95)
    for b in range(2, 16):
        s.drums(g1 if b % 4 != 3 else g2, b, steps_per_beat=4, vel=0.85)
        s.shamisen(riff if b % 2 == 0 else riff2, b, vel=0.7, pan=-0.25)
    s.drone(0, 2, 14, octv=-1, vel=0.3, cutoff=700)
    s.wind("5!/3 4/1 3/2 4/2 | 5/8 | 7!/2 5/2 4/2 3/2 | 4-3/8 | 5!/3 4/1 3/2 1/2 | 2/8 | 3/2 1/2 0/2 1/2 | 0/8", 2, 'fue', octv=1, vel=0.8, pan=0.25)
    s.wind("8!/4 7/4 | 5/8 | 7/2 8/2 9/4 | 8-7/8 | 5!/4 4/4 | 3/8", 10, 'fue', octv=1, vel=0.85, pan=0.25)
    # Zwischenspiel: nur Taiko, Spannung steigt
    for b in range(16, 20):
        s.drums("O.......O.......|" if b < 18 else "O...O...O.O.OOOO", b, steps_per_beat=4, vel=0.9)
    s.wind("4/16 | 3/8 5/8", 16, 'shaku', octv=1, vel=0.75)
    for b in range(20, 32):
        s.drums(g2 if b % 2 else g1, b, steps_per_beat=4, vel=0.9)
        s.shamisen(riff if b % 2 == 0 else riff2, b, vel=0.75, pan=-0.25)
        s.koto("0/1 2/1 3/1 4/1 3/1 2/1 1/1 2/1", b, octv=1, vel=0.4, pan=0.4)
    s.drone(0, 20, 12, octv=-1, vel=0.32, cutoff=800)
    s.wind(THEME.replace('3/4 4/2', '3!/4 4/2'), 20, 'fue', octv=1, vel=0.85, pan=0.2)
    s.wind("5/8 | 4-3/8 | 2/8 | 0/8", 28, 'fue', octv=1, vel=0.85, pan=0.2)
    return s


# ============================================================ Endboss: Kami-goroshi
def boss_final():
    s = Song(132, 50, 'iwato', 32, seed=901)
    s.bonsho(0, vel=1.0); s.bonsho(16, vel=0.9)
    s.sho([0, 1, 2], 0, 4, octv=0, vel=0.5)
    s.sho([0, 1, 3], 16, 4, octv=0, vel=0.45)
    g1 = "O.kOS.kOO.kOS.kk"
    g2 = "OOkOSSkOOkOkSSSS"
    riff = "0,/1 1,/1 0,/1 4,,/1 0,/1 1,/1 3,/1 2,/1"
    for b in range(4, 16):
        s.drums(g1 if b % 4 != 3 else g2, b, steps_per_beat=4, vel=0.9)
        s.shamisen(riff, b, vel=0.7, pan=-0.3)
    s.drone(0, 4, 12, octv=-1, vel=0.32, cutoff=600)
    s.drone(1, 8, 8, octv=-1, vel=0.16, cutoff=500)
    s.wind(THEME, 4, 'shaku', octv=1, vel=0.85, pan=0.15)
    s.wind("5!/2 6/2 7/4 | 8-7/8 | 6!/2 5/2 4/4 | 3/8", 12, 'fue', octv=1, vel=0.8, pan=0.3)
    for b in range(20, 32):
        s.drums(g2 if b % 2 else g1, b, steps_per_beat=4, vel=0.95)
        s.shamisen(riff, b, vel=0.75, pan=-0.3)
        s.koto("0/1 1/1 3/1 1/1 4/1 3/1 1/1 3/1", b, octv=1, vel=0.42, pan=0.4)
    s.drone(0, 20, 12, octv=-1, vel=0.35, cutoff=750)
    s.wind(THEME.replace('/', '/'), 20, 'fue', octv=2, vel=0.75, pan=0.25)
    s.wind("0/16 | 1/16 | 0/16", 20, 'shaku', octv=1, vel=0.6, pan=-0.1)
    s.sho([0, 1, 2, 4], 28, 4, octv=0, vel=0.45)
    for b in range(16, 20):
        s.drums("O...............", b, steps_per_beat=4, vel=1.0)
    s.wind("7/16 | 6-5/16", 16, 'shaku', octv=1, vel=0.8)
    return s


# ============================================================ Endbossin: Ama-no-Iwato (Kagura bis zum Morgen)
def _suzu(s, bar, e8=0.0, vel=0.35, n=5):
    """Kagura-Suzu: ein Bündel kleiner Glöckchen, kurz geschüttelt."""
    for i in range(n):
        f = s.rng.uniform(2300, 3400)
        s.mix.add(Y.kane(f, vel * s.rng.uniform(0.6, 1.0), 0.7), s.t(bar, e8) + i * 0.035 + s.rng.uniform(0, 0.012),
                  0.35, s.rng.uniform(0.1, 0.6), 0.45)


def amaterasu():
    s = Song(126, 50, 'in', 36, seed=1201)
    # Fels vor der Höhle: Dunkel, Glocke, Uzumes erste Glöckchen
    s.bonsho(0, vel=0.9)
    s.windfx(0, 4, 0.16, 380)
    s.sho([0, 1, 3], 0, 4, octv=0, vel=0.38)
    for b in range(0, 4):
        s.drums("h.......h...h...", b, steps_per_beat=4, vel=0.8)
        _suzu(s, b, 4, vel=0.22 + b * 0.05)
    # Kagura im Dunkeln: Taiko, Shamisen, Kagura-Bue
    g1 = "O.s.S.k.O.s.S.kk"
    g2 = "O.kOS.kSO.OkSSSS"
    riff = "0,/1 2,/1 1/1 2,/1 0,/1 4,,/1 1/1 0/1"
    for b in range(4, 16):
        s.drums(g1 if b % 4 != 3 else g2, b, steps_per_beat=4, vel=0.85)
        s.shamisen(riff, b, vel=0.62, pan=-0.3)
        _suzu(s, b, 0, vel=0.3); _suzu(s, b, 4, vel=0.22, n=3)
    s.drone(0, 4, 12, octv=-1, vel=0.3, cutoff=600)
    s.wind("4!/3 3/1 2/2 3/2 | 4/8 | 2!/2 3/2 4/2 5/2 | 4-3/8 | 1!/3 2/1 3/4 | 2/4 1/4 | 0/2 1/2 2/2 1/2 | 0/8", 4, 'fue', octv=1, vel=0.78, pan=0.2)
    s.wind("5!/4 4/4 | 3/8 | 4/2 3/2 2/4 | 1-0/8", 12, 'fue', octv=1, vel=0.8, pan=0.2)
    # Der Fels bewegt sich: Taiko-Wirbel, Glöckchen werden dichter
    for b in range(16, 20):
        s.drums("O.......O.......|" if b < 18 else "O...O...O.O.OOOO", b, steps_per_beat=4, vel=0.95)
        for k in range(0, 8, 2 if b < 18 else 1):
            _suzu(s, b, k, vel=0.18 + (b - 16) * 0.06, n=3)
    s.wind("3/16 | 4/8 5-6/8", 16, 'shaku', octv=1, vel=0.75)
    # Morgen: die Sonne tritt hervor – helle Yo-Skala, Shō, Koto und Glocken
    s.scale = SCALES['yo']
    s.bonsho(20, vel=0.8)
    s.sho([0, 2, 4, 6], 20, 8, octv=0, vel=0.42)
    s.sho([1, 3, 5, 7], 28, 8, octv=0, vel=0.4)
    riff2 = "0,/1 2,/1 4,/1 2,/1 3,/1 2,/1 1,/1 2,/1"
    for b in range(20, 36):
        s.drums(g2 if b % 2 else g1, b, steps_per_beat=4, vel=0.9)
        s.shamisen(riff2, b, vel=0.66, pan=-0.3)
        _suzu(s, b, 0, vel=0.32)
        if b % 2 == 0:
            s.bell(4, b, 0, octv=2, vel=0.22, pan=0.4)
    s.arp([0, 0, 3, 3, 1, 1, 0, 0] * 2, 20, pattern=(0, 2, 4, 7, 4, 2, 4, 2), octv=0, vel=0.32, per_bar=8, pan=0.35)
    s.drone(0, 20, 16, octv=-1, vel=0.3, cutoff=900)
    s.wind(THEME, 20, 'fue', octv=2, vel=0.78, pan=0.2)
    s.wind("7!/4 8/4 | 9/8 | 8/2 7/2 5/4 | 7/8 | 5!/4 4/4 | 3/4 4/4 | 2/2 3/2 2/2 1/2 | 0/8", 28, 'fue', octv=1, vel=0.8, pan=0.25)
    return s


# ============================================================ Geheimer Endboss: Sutoku-in (Shiramine no Onryō)
def sutoku():
    s = Song(138, 49, 'in', 36, seed=1301)
    # Grab im Nebel: Tempelglocke, Mokugyo-Takt der Sutren-Lesung, Shakuhachi-Klage des Verbannten
    s.bonsho(0, vel=1.0)
    s.windfx(0, 8, 0.2, 320)
    s.drone(0, 0, 8, octv=-2, vel=0.34, cutoff=420)
    for b in range(0, 8):
        s.drums("k...k...k...k.k.", b, steps_per_beat=4, vel=0.55 + b * 0.04)
    s.wind("0/6 1/2 | 0/8 | 4,/4 0/2 1/2 | 2-1/8 | 3/4 2/2 1/2 | 0/8 | 1/2 0/2 4,/4 | 4,/8", 0, 'shaku', octv=0, vel=0.8, pan=-0.1)
    s.sho([0, 1, 3], 4, 4, octv=0, vel=0.3)
    # Der Groll erwacht: Taiko, harte Shamisen, Tengu-Fue umkehrt das Thema (Umkehr-Fluch)
    s.bonsho(8, vel=0.9)
    g1 = "O.kOS.kOO.kSS.kk"
    g2 = "OOkSOOkSOkOkSSSS"
    riff = "0,/1 1,/1 0,/1 4,,/1 0,/1 1,/1 2,/1 1,/1"
    for b in range(8, 20):
        s.drums(g1 if b % 4 != 3 else g2, b, steps_per_beat=4, vel=0.92)
        s.shamisen(riff, b, vel=0.72, pan=-0.3)
    s.drone(0, 8, 12, octv=-1, vel=0.34, cutoff=650)
    s.wind("3/4 2/2 3/2 | 4/6 5/2 | 6/3 5/1 4/4 | 3/8 | 1/4 2/2 3/2 | 2~/4 4/4 | 5/2 4/2 5/2 6/2 | 6/8", 8, 'fue', octv=1, vel=0.82, pan=0.25)
    s.wind("0/16 | 1/8 0/8", 8, 'shaku', octv=0, vel=0.5, pan=-0.2)
    s.wind("7!/4 6/4 | 5-4/8 | 3!/2 4/2 5/4 | 6/8", 16, 'fue', octv=1, vel=0.85, pan=0.25)
    # Sanuki: alles bricht ab, nur Glocke, Krähen-Wind und Sutren-Takt
    s.bonsho(20, vel=0.9)
    s.windfx(20, 4, 0.28, 700)
    for b in range(20, 24):
        s.drums("k.k.k.k.k.k.kkkk" if b == 23 else "k...k...k...k...", b, steps_per_beat=4, vel=0.7)
    s.wind("4,/8 | 0/8 | 1/4 0/4 | 4,/8", 20, 'shaku', octv=0, vel=0.75)
    # Der König der Tengu: volles Ensemble, Leitmotiv in der Tiefe, Fue darüber
    for b in range(24, 36):
        s.drums(g2 if b % 2 else g1, b, steps_per_beat=4, vel=0.98)
        s.shamisen(riff, b, vel=0.78, pan=-0.3)
        s.koto("0/1 1/1 3/1 1/1 4/1 3/1 1/1 0/1", b, octv=1, vel=0.42, pan=0.4)
    s.drone(0, 24, 12, octv=-1, vel=0.36, cutoff=800)
    s.wind(THEME, 24, 'shaku', octv=0, vel=0.8, pan=-0.15)
    s.wind("7/8 | 6-5/8 | 6!/2 5/2 4/4 | 3/8 | 5!/4 6/4 | 7/8 | 6/2 5/2 4/2 3/2 | 0'/8", 24, 'fue', octv=1, vel=0.8, pan=0.3)
    s.sho([0, 1, 3, 4], 32, 4, octv=0, vel=0.42)
    return s


# ============================================================ Spielende: Shi no Kane
def gameover():
    s = Song(60, 57, 'hira', 10, seed=1001)
    s.bonsho(0, vel=0.9)
    s.windfx(0, 10, 0.18, 400)
    s.wind("r/4 3/4 | 4/2 3/2 2/4 | 1/6 0/2 | 0,/8 | r/8", 0, 'shaku', octv=0, vel=0.75, pan=0.1)
    s.koto("r/8 | r/8 | r/8 | r/4 4/2 3/2 | 2/2 1/2 0/4 | 0,/8", 0, octv=1, vel=0.5, pan=-0.3, rev=0.6)
    s.drone(0, 0, 10, octv=-1, vel=0.22, cutoff=350)
    s.bonsho(6, vel=0.5)
    return s


# ============================================================ Sieg: Akatsuki (Morgengrauen)
def victory():
    s = Song(96, 62, 'yo', 16, seed=1101)
    s.arp([0, 0, 2, 2, 3, 3, 1, 0] * 2, 0, pattern=(0, 2, 4, 7, 4, 2, 4, 2), octv=0, vel=0.38, per_bar=8, pan=-0.3)
    s.sho([0, 2, 4], 0, 8, octv=0, vel=0.3); s.sho([0, 2, 4, 6], 8, 8, octv=0, vel=0.3)
    s.wind(THEME, 0, 'fue', octv=1, vel=0.7, pan=0.2)
    s.koto("3'/4 4'/2 3'/2 | 2'/6 1'/2 | 0'/3 1'/1 2'/4 | 3'/8 | 5'/4 4'/2 3'/2 | 4'/4 2'/4 | 1'/2 2'/2 1'/2 0'/2 | 0'/8", 8, octv=0, vel=0.62, pan=0.2)
    for b in range(0, 16):
        s.drums("s.s.S.s.", b, vel=0.55)
        if b % 4 == 0:
            s.drums("o...h...", b, vel=0.8)
    s.bell(5, 0, 0, octv=1, vel=0.3); s.bell(7, 15, 4, octv=1, vel=0.3)
    return s


# ============================================================ Laden & Ereignisse: Yomise (Nachtmarkt)
def matsuri():
    s = Song(96, 60, 'yo', 16, seed=701)
    s.windfx(0, 16, 0.08, 900)
    prog = [0, 0, 3, 3, 1, 1, 0, 0]
    # Shamisen-Ostinato, leicht und federnd
    for b in range(0, 16):
        s.shamisen("0/1 2/1 4/1 2/1 | 3/1 2/1 0/1 2/1" if b % 2 == 0 else "1/1 2/1 4/1 5/1 | 4/1 2/1 1/1 0/1", b, octv=0, vel=0.42, pan=-0.25)
    mel = "4/2 5/2 4/2 2/2 | 3/4 2/4 | 0/2 2/2 3/2 4/2 | 2/8 | 4/2 5/2 7/2 5/2 | 4/4 3/2 2/2 | 3/2 2/2 0/2 1/2 | 0/8"
    s.wind(mel, 0, 'fue', octv=1, vel=0.55, pan=0.2, rev=0.35)
    s.wind(mel.replace('7/2', '5/2'), 8, 'fue', octv=1, vel=0.5, pan=0.2, rev=0.35)
    s.koto("r/4 4/4 | r/4 2/4 | r/4 3/4 | r/4 0/4 | r/4 4/4 | r/4 5/4 | r/4 2/4 | 0/8", 8, octv=1, vel=0.4, pan=-0.1)
    s.arp(prog, 0, pattern=(0, 2, 4, 2), octv=-1, vel=0.22, per_bar=4, pan=0.0)
    s.arp(prog, 8, pattern=(0, 2, 4, 2), octv=-1, vel=0.22, per_bar=4, pan=0.0)
    for b in range(0, 16):
        s.drums("k.s.s.ss" if b % 4 == 3 else "k...s.k.", b, vel=0.45, swing=0.12)
    for b in (0, 4, 8, 12):
        s.bell(4, b, 0, octv=1, vel=0.15)
    return s


TRACKS = {'title': title, 'forest': forest, 'temple': temple, 'mountain': mountain, 'sea': sea,
          'underworld': underworld, 'heaven': heaven, 'boss': boss, 'boss_final': boss_final, 'amaterasu': amaterasu, 'sutoku': sutoku,
          'gameover': gameover, 'victory': victory, 'matsuri': matsuri}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(TRACKS)
    for nm in names:
        t0 = time.time()
        song = TRACKS[nm]()
        path = os.path.join(OUT, nm + '.ogg')
        song.render(path)
        print(nm, '%.1fs Musik, %.1fs Rechenzeit' % (song.dur, time.time() - t0), os.path.getsize(path) // 1024, 'KB')
