"""Ausweich-Rolle der Spielfiguren, im selben Pixel-System wie Lauf/Angriff (px.py, Licht oben links).
Je Figur 5 Zellen (Rig-Größe der Figur, Blick nach links): [geduckt (Absprung/Landung), Ball 0..3].
Die Ball-Bilder sind eigens gezeichnet: Rücken, angezogene Beine, Füße und der Kopf (aus dem HEAD-Raster der
Figur) wandern um den Ball – die Licht-/Schattenseite bleibt dabei oben links, wie bei gezeichneten Bildern.
Ergebnis: yokai/assets/sprites/<name>_roll.png. Ball-Mitte = Zellmitte."""
import importlib, math, os, sys
DIR = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [DIR, os.path.join(DIR, '..'), os.path.join(DIR, '..', 'masters')]
from herolib import *
import numpy as np

OUT = os.path.join(DIR, '..', '..', '..', 'yokai', 'assets', 'sprites')
CW, CH, CX, CY, RB = 104, 88, 52, 44, 17

# Figuren mit KI-Bogen (art_src/spritecook, z. B. Hana, Kenji, Kuzunoha, Ponpoko, Benkei, Okiku) bringen ihre Rolle selbst mit und fehlen hier.
# Figur: Kopfraster/Legende im Modul, Rücken, Beine, Füße, Extra (Schweif, Flügel, Haar, Lätzchen)
SPEC = {
    'kotaro':   dict(head='L_', back=('g1', 'g2', 'g3'), legs=('g0', 'g1', 'g2'), feet=SKN, extra=('wing', ('h0', 'h1', 'h2'))),
    'seimei':   dict(head='L_', back=WH, legs=PUR, feet=WH, extra=None),
    'akago':    dict(head='A_', back=('r1', 'r2', 'r3'), legs=('r0', 'r1', 'r2'), feet=('r1', 'r2', 'r3'), extra=('bib', WH)),
    'susanoo':  dict(head='L_', back=WH, legs=WH, feet=SKN, extra=('band', RD)),
}
ANG = (135, 225, 315, 45)          # Kopfrichtung je Bild (180 = links, 90 = oben); Rolle nach links = gegen den Uhrzeiger


def rot_grid(text, k):
    rows = text.strip('\n').split('\n')
    w = max(len(r) for r in rows)
    a = np.array([list(r.ljust(w, '.')) for r in rows])
    a = np.rot90(a, k)                               # k = 1: 90° gegen den Uhrzeiger
    return '\n'.join(''.join(r) for r in a)


def P(a, r):
    dx, dy = vec(a)
    return CX + dx * r, CY + dy * r


def ball(mod, sp, k):
    setsize(CW, CH)
    c = C()
    a = ANG[k]
    ex = sp['extra']
    # Schweif / Flügel / Haar hinter dem Körper (gegenüber vom Kopf, etwas nachgezogen)
    if ex and ex[0] in ('tail', 'tanuki', 'wing', 'hair'):
        p = C()
        b = a + 200
        r0, r1 = (RB - 3, RB + (9 if ex[0] == 'tail' else 7 if ex[0] != 'hair' else 5))
        x0, y0 = P(b - 25, r0); x1, y1 = P(b, r1); x2, y2 = P(b + 30, r0 - 1)
        m = L(x0, y0, 3.2, x1, y1, 2.2) | L(x1, y1, 2.2, x2, y2, 3.0) | PG([(x0, y0), (x1, y1), (x2, y2), (CX, CY)])
        p.form(m, ex[1], sd=2, hl=1)
        if ex[0] == 'tail':
            p.fill(E(*P(b, r1 - 1), 3, 3), 'c2', only=m)
        if ex[0] == 'tanuki':
            for t in (0.35, 0.7):
                q = lerp((x0, y0), (x1, y1), t)
                p.fill(E(q[0], q[1], 1.2, 1.2), 's0', only=m)
        if ex[0] == 'wing':
            for t in (-14, 0, 14):
                p.line([P(b + t, RB - 2), P(b + t, RB + 6)], 'K', only=m)
        c.stamp(p, 'K')
    # Rücken: die große Rundung
    p = C()
    body = E(CX, CY, RB, RB - 0.5)
    p.form(body, sp['back'], sd=3, hl=2)
    p.line([P(a + 70 + i * 12, RB - 3) for i in range(9)], sp['back'][0], only=body)    # Gewandfalte entlang des Rückens
    if sp.get('belly'):
        p.form(E(*P(a + 180, RB * 0.25), 7, 7), sp['belly'], sd=1, hl=1, only=body)
    c.stamp(p, 'K')
    # angezogene Beine (Knie zur Brust), auf der Bauchseite
    p = C()
    kx, ky = P(a - 70, RB * 0.35)
    hx, hy = P(a - 150, RB * 0.45)
    legs = L(hx, hy, 5.0, kx, ky, 4.4)
    p.form(legs, sp['legs'], sd=2, hl=1)
    p.line([P(a - 145, RB * 0.2), P(a - 75, RB * 0.15)], sp['legs'][0], only=legs)
    c.stamp(p, 'K')
    if sp['feet']:
        p = C()
        fx, fy = P(a - 100, RB - 1)
        p.form(E(fx, fy, 3.2, 2.6), sp['feet'], sd=1, hl=1)
        c.stamp(p, 'K')
    if ex and ex[0] == 'band':                       # Stirnband-/Gürtelenden flattern nach hinten
        p = C()
        x0, y0 = P(a + 25, RB - 2); x1, y1 = P(a + 60, RB + 6)
        p.form(L(x0, y0, 1.4, x1, y1, 0.9), ex[1], sd=1, hl=0)
        c.stamp(p, 'K')
    if ex and ex[0] == 'beads':
        p = C()
        for i in range(6):
            q = P(a + 40 + i * 14, RB - 4)
            p.form(E(q[0], q[1], 1.4, 1.4), ex[1], sd=1, hl=0)
        c.stamp(p, 'K', ring=False)
    if ex and ex[0] == 'bib':
        p = C()
        p.form(E(*P(a - 30, RB * 0.3), 4.5, 4.5), ex[1], sd=1, hl=1)
        p.fill(E(*P(a - 30, RB * 0.3), 1.2, 1.2), 'm2')
        c.stamp(p, 'K')
    # Kopf: eingezogen vorn am Ball, Raster in 90°-Schritten mitgedreht
    txt = rot_grid(mod.HEAD, k)
    rows = txt.split('\n')
    hw, hh = len(rows[0]), len(rows)
    hx, hy = P(a, RB * 0.62)
    p = C()
    p.grid(int(round(hx - hw / 2)), int(round(hy - hh / 2)), txt, getattr(mod, sp['head']))
    c.stamp(p, 'K')
    c.blacken()
    return c.img()


def crouch(mod, name):
    D = mod.DEF
    kw = {k: v for k, v in dict(bob=7, lean=-3, ffoot=D['ffoot'] - 4, nfoot=D['nfoot'] + 4).items() if k in D}
    for k, (dx, dy) in (('nelb', (2, 3)), ('nwr', (3, 5))):
        if k in D:
            kw[k] = (D[k][0] + dx, D[k][1] + dy)
    return getattr(mod, name)(**kw).img()


def build(name):
    global CW, CH, CX, CY
    mod = importlib.import_module(name)
    cr = crouch(mod, name)
    CW, CH = cr.size
    CX, CY = CW // 2, CH // 2
    ims = [cr] + [ball(mod, SPEC[name], k) for k in range(4)]
    st = Image.new('RGBA', (CW * len(ims), CH), (0, 0, 0, 0))
    for i, im in enumerate(ims):
        assert im.size == (CW, CH), (name, im.size)
        st.paste(im, (i * CW, 0))
    st.save(os.path.join(OUT, name + '_roll.png'))
    return st


if __name__ == '__main__':
    strips = [build(n) for n in SPEC]
    if len(sys.argv) > 1:                            # Vorschau: python3 roll.py vorschau.png
        o = Image.new('RGBA', (max(s.width for s in strips), sum(s.height for s in strips)), (40, 36, 50, 255))
        y = 0
        for s in strips:
            o.alpha_composite(s, (0, y)); y += s.height
        o.resize((o.width * 2, o.height * 2), Image.NEAREST).save(sys.argv[1])
    print(len(strips), 'Figuren')
