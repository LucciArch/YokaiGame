"""Die Geschichte des Weges: Kapitel, die sich mit dem Spielfortschritt öffnen, gezeichnete Zwischensequenzen
und der Story-Baum im Hauptmenü."""
import math
import pygame
from .settings import W, H
from . import gfx
from .data import CHAR_ORDER


def _st(sv, k):
    return sv['stats'].get(k, 0)


# id, Titel, Bedingung (Spielstand), Hinweis solange gesperrt, Szene, Texttafeln
CHAPTERS = [
    ('prolog', 'Die Nacht ohne Morgen', lambda sv: True, '', 'mond', [
        'In der Nacht, in der der Mond rot wurde, öffneten sich die Brunnen, Wälder und Ruinen Japans.',
        'Hundert Dämonen zogen durch die Dörfer – die Hyakki Yagyō. Und der Morgen kam nicht.',
        'Im kleinen Schrein am Bambuswald nahm Hana die Glocke ihrer Großmutter vom Haken. Jemand musste dem Zug entgegengehen.']),
    ('morgen', 'Der falsche Morgen', lambda sv: _st(sv, 'wins') >= 1, 'Gewinne einen Lauf.', 'morgen', [
        'Der Zug ist zerschlagen, im Osten graut der Himmel. Doch die Sonne steigt nicht.',
        'Hoch über den Wolken hängt ein schwarzer Stern und trinkt ihr Licht: Amatsu-Mikaboshi, der sich den Göttern nie beugte.',
        'Die Schreinglocke klingt jetzt anders. Sie ruft hinauf – nach Takamagahara.']),
    ('stern', 'Der Fall des bösen Sterns', lambda sv: _st(sv, 'true_wins') >= 1,
     'Folge dem Ruf nach Takamagahara und gewinne dort.', 'stern', [
        'Der schwarze Stern zerbricht in tausend Splitter. Für einen Atemzug ist es still in den Himmelsgefilden.',
        'Dann reißt die Erde auf. Aus der Tiefe ruft eine Stimme den Namen ihres Mannes – Izanami ist erwacht.',
        'Und Amaterasu, gekränkt vom langen Dunkel, hat sich in der Felsenhöhle verschlossen. Zwei Wege führen weiter.']),
    ('yomi', 'Yomotsu Hirasaka', lambda sv: _st(sv, 'yomi_wins') >= 1, 'Steig hinab nach Yomi und stelle dich Izanami.', 'yomi', [
        'Im Palast der Toten fällt Izanamis Schleier. Darunter liegt kein Zorn, nur Trauer über ein gebrochenes Versprechen.',
        'Du rollst den Felsen vor den Pass zwischen den Welten. Diesmal schaut niemand zurück.',
        'Doch hinter dem Felsen bewegt sich noch etwas in der Dunkelheit – älter als der Tod selbst.']),
    ('iwato', 'Die Sonne kehrt zurück', lambda sv: _st(sv, 'iwato_wins') >= 1, 'Öffne Ama-no-Iwato und stelle dich Amaterasu.', 'sonne', [
        'Ame-no-Uzume tanzt auf dem umgedrehten Fass, die Götter lachen, und die Hähne des ewigen Tages krähen.',
        'Neugierig schaut Amaterasu hinaus – und erblickt im Yata-Spiegel ihr eigenes Licht.',
        'Die Sonne steht wieder am Himmel. Doch ihr Licht wirft einen Schatten, den es vorher nicht gab.']),
    ('gefaehrten', 'Gefährten am Feuer', lambda sv: len(sv['chars']) >= 5, 'Gewinne fünf Gefährten für den Weg.', 'feuer', [
        'Wer gegen die hundert Dämonen zieht, ist nicht allein: ein Rōnin, eine Füchsin, ein Tanuki, ein Mönch …',
        'Jeder trägt seine eigene Schuld in diese Nacht, und jeder muss seinen Weg bis zum Ende gehen.',
        'Erst wenn alle Siegel einer Seele gebrochen sind, sprechen die Kami von ihr als Meister.']),
    ('meister', 'Der erste Meister', lambda sv: any(a.startswith('meister_') for a in sv['achievements']),
     'Brich alle Siegel mit einer Figur.', 'siegel', [
        'Das dritte Kapitel, der Sieg, der Himmel, die Unterwelt und die Nacht der Oni – alle Siegel sind gebrochen.',
        'Die Kami schreiben einen Namen in das Buch des Weges. Wer so weit gegangen ist, trägt ein Siegel in jeden neuen Lauf.']),
    ('schatten', 'Der Schatten hinter dem Morgen',
     lambda sv: _st(sv, 'yomi_wins') >= 1 and _st(sv, 'iwato_wins') >= 1 and len(sv['chars']) >= 8,
     'Bezwinge Izanami und Amaterasu und versammle acht Gefährten.', 'schatten', [
        'Sonne und Unterwelt sind versöhnt. Doch die Schatten, die beide warfen, sind zusammengewachsen.',
        'Man erzählt von einem Wesen ohne Namen, geboren in der Nacht der hundert Dämonen – aus all der Angst der Menschen.',
        'Wenn es sich zeigt, wird kein Morgen es aufhalten. Die Geschichte ist noch nicht zu Ende …']),
    ('wahres_ende', 'Der Kaiser von Shiramine', lambda sv: _st(sv, 'sutoku_wins') >= 1,
     'Folge dem Schatten nach Shiramine und stelle dich, was dort wartet.', 'shiramine', [
        'Der Schatten hatte einen Namen: Sutoku-in, der Kaiser, den man in die Verbannung schickte und dessen Sutren man zurückwies.',
        'Achthundert Jahre wuchs sein Groll auf Shiramine, genährt von jeder Angst in der Nacht der hundert Dämonen.',
        'Hana legt die Schreinglocke auf sein Grab und betet für ihn. Diesmal nimmt jemand seine Sutren an.',
        'Über den Bergen von Sanuki geht die Sonne auf – ein Morgen ohne Schatten. Der Weg ist zu Ende.']),
]
BY_ID = {c[0]: c for c in CHAPTERS}
# Story-Baum: Lage der Knoten und Verbindungen
POS = {'prolog': (240, 40), 'morgen': (240, 76), 'stern': (240, 112), 'yomi': (140, 148), 'iwato': (340, 148),
       'schatten': (240, 184), 'wahres_ende': (240, 220), 'gefaehrten': (400, 76), 'meister': (400, 112)}
EDGES = [('prolog', 'morgen'), ('morgen', 'stern'), ('stern', 'yomi'), ('stern', 'iwato'), ('yomi', 'schatten'),
         ('iwato', 'schatten'), ('schatten', 'wahres_ende'), ('prolog', 'gefaehrten'), ('gefaehrten', 'meister')]
ORDER = ['prolog', 'morgen', 'stern', 'yomi', 'iwato', 'schatten', 'wahres_ende', 'gefaehrten', 'meister']


def unlocked(sv, cid):
    return cid in sv.data.get('story_seen', []) or BY_ID[cid][2](sv.data)


def pending(sv):
    """Kapitel, deren Bedingung erfüllt ist, die aber noch nie gezeigt wurden (ohne Prolog)."""
    seen = sv.data.get('story_seen', [])
    return [c[0] for c in CHAPTERS if c[0] != 'prolog' and c[0] not in seen and c[2](sv.data)]


def mark_seen(sv, cid):
    seen = sv.data.setdefault('story_seen', [])
    if cid not in seen:
        seen.append(cid)
        sv.write()


# ====================================================================== Szenen
_BG = {}


def draw_scene(s, kind, t, save=None):
    """Platzhalter, bis die Zwischensequenz-Videos da sind (je Szene ein Video unter assets/story/<kind>):
    ruhiger dunkler Grund mit sanftem Verlauf."""
    img = _BG.get('base')
    if img is None:
        img = _BG['base'] = pygame.Surface((W, H))
        for y in range(H):
            f = y / H
            pygame.draw.line(img, (int(10 + 14 * f), int(8 + 6 * f), int(18 + 10 * f)), (0, y), (W, y))
    s.blit(img, (0, 0))


# ====================================================================== Zwischensequenz
class Cutscene:
    """Spielt Kapitel nacheinander: Bild, Titel, Texttafeln mit Schreibmaschinen-Einblendung.
    Bestätigen = Tafel fertig zeigen bzw. weiter, Zurück = alle überspringen."""

    def __init__(self, game, ids):
        self.g, self.ids, self.i, self.k, self.t, self._full = game, list(ids), 0, 0, 0.0, -1

    def frame(self, s, dt, nav):
        cid, title, _, _, scene, texts = BY_ID[self.ids[self.i]]
        self.t += dt
        gfx.HI.clear()
        draw_scene(s, scene, self.t, self.g.save)
        lay = pygame.Surface((W, 64), pygame.SRCALPHA)
        lay.fill((6, 4, 12, 190))
        s.blit(lay, (0, H - 64))
        a = int(255 * min(1.0, self.t / 0.8))
        T = gfx.TEXT
        T.add('Kapitel %d' % (CHAPTERS.index(BY_ID[cid]) + 1) if cid != 'prolog' else 'Prolog', W // 2, 10, 7, (230, 180, 120), 'c', alpha=a)
        T.add(title, W // 2, 20, 14, (255, 236, 200), 'c', alpha=a)
        tt = self.t - 0.6
        txt = texts[self.k]
        n = len(txt) if self.k < self._full else max(0, int(tt * 45))
        self.g._wrap_c(txt[:n], W // 2, H - 52, W - 120, 8, (240, 230, 210))
        if n >= len(txt):
            T.add('weiter ▸' if self.k + 1 < len(texts) or self.i + 1 < len(self.ids) else 'Ende ▸', W - 16, H - 14, 6,
                  (190, 170, 140), 'r', alpha=int(160 + 90 * math.sin(self.t * 4)))
        if self.t < 0.5:
            ov = pygame.Surface((W, H)); ov.set_alpha(int(255 * (1 - self.t / 0.5)))
            s.blit(ov, (0, 0))
        for nv in nav:
            if nv == 'back':
                for c in self.ids:
                    mark_seen(self.g.save, c)
                return True
            if nv == 'ok':
                if n < len(txt):
                    self._full = self.k + 1
                elif self.k + 1 < len(texts):
                    self.k += 1
                    self.t = 0.6                         # neue Tafel: Bild läuft weiter, Text schreibt neu
                    self._full = -1
                else:
                    mark_seen(self.g.save, cid)
                    self.i += 1
                    if self.i >= len(self.ids):
                        return True
                    self.k, self.t, self._full = 0, 0.0, -1
        return False


# ====================================================================== Story-Baum
def draw_tree(game, s, sel):
    sv = game.save
    T = gfx.TEXT
    for a, b in EDGES:
        on = unlocked(sv, b)
        pygame.draw.line(s, (200, 160, 90) if on else (70, 64, 84), POS[a], POS[b], 2 if on else 1)
    for k, cid in enumerate(ORDER):
        x, y = POS[cid]
        on = unlocked(sv, cid)
        if k == sel:
            gfx.draw_glow(s, x, y, 26, (255, 210, 120), 90)
        col = (255, 214, 110) if on else (90, 86, 110)
        pygame.draw.circle(s, (20, 14, 26), (x, y), 11)
        pygame.draw.circle(s, col, (x, y), 11, 2)
        if on:
            pygame.draw.circle(s, col, (x, y), 5)
        T.add(BY_ID[cid][1] if on else '???', x, y + 13, 6, (240, 225, 200) if on else (140, 130, 150), 'c')
    cid = ORDER[sel]
    ch = BY_ID[cid]
    if unlocked(sv, cid):
        T.add(ch[1], W // 2, 262, 9, (255, 230, 170), 'c')
        T.add('Bestätigen – Zwischensequenz ansehen', W // 2, 276, 6, (200, 190, 170), 'c')
    else:
        T.add('Noch verborgen', W // 2, 262, 9, (190, 170, 170), 'c')
        T.add(ch[3], W // 2, 276, 7, (220, 200, 170), 'c')
    # Figuren und ihre Siegel
    from .data import MARKS, CHAR_UNLOCKS
    got = sv['achievements']
    nch = len(sv['chars'])
    nm = sum(1 for c in CHAR_ORDER if 'meister_' + c in got)
    ns = sum(1 for c in CHAR_ORDER for mk in MARKS if mk[0] in CHAR_UNLOCKS.get(c, {}) and 'm_%s_%s' % (c, mk[0]) in got)
    tot = sum(1 for c in CHAR_ORDER for mk in MARKS if mk[0] in CHAR_UNLOCKS.get(c, {}))
    T.add('Gefährten %d / %d   •   Siegel %d / %d   •   Meister %d' % (nch, len(CHAR_ORDER), ns, tot, nm), W // 2, 292, 6,
          (190, 180, 160), 'c')
