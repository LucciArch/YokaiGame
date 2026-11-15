"""Epilog nach dem Sieg: Morgendämmerung, der Zug der Yōkai verblasst, Abschlusstext je Figur, Abspann."""
import math
import random
import pygame
from .settings import W, H
from . import gfx, sheets
from .data import CHARS, ENEMIES, BOSSES

# (normaler Sieg, wahrer Sieg)
ENDINGS = {
    'hana': ('Hana läutet die Schreinglocke, bis die letzte Laterne erlischt. Der Schrein ihrer Großmutter steht wieder unter dem Schutz der Kami.',
             'Amaterasu selbst legt Hana einen Sonnenstrahl in die Hände. Seitdem verlöscht das Licht des kleinen Schreins nie wieder.'),
    'kenji': ('Kenji wischt die Klinge ab und steckt sie fort. Zum ersten Mal seit Jahren kämpft er nicht für einen Herrn, sondern für ein Dorf, das ihm dankt.',
              'Auf dem Himmelspfad findet Kenji seinen alten Meister wieder. Der nickt nur einmal. Mehr braucht der Rōnin nicht.'),
    'kuzunoha': ('Kuzunoha kehrt in den Wald von Shinoda zurück. Ihr Sohn wartet dort, und diesmal muss sie ihn nicht verlassen.',
                 'Die Göttin Inari schenkt Kuzunoha einen zehnten Schweif. Halb Mensch, halb Fuchs – und endlich ganz sie selbst.'),
    'ponpoko': ('Ponpoko trommelt auf seinem Bauch, bis das ganze Tal tanzt. Die Münzen aus Laub behält er trotzdem.',
                'Im Himmel verkauft Ponpoko den Göttern einen Teekessel, der von selbst wandert. Niemand dort hat ihn je wieder erwischt.'),
    'benkei': ('Benkei stellt sich ein letztes Mal auf die Gojō-Brücke. Diesmal muss er niemanden besiegen – er wacht nur, bis die Sonne aufgeht.',
               'Benkei sammelt die tausend Klingen der Unterwelt und schmiedet daraus eine Glocke. Ihr Klang vertreibt die Oni für hundert Jahre.'),
    'okiku': ('Okiku zählt die Teller ein letztes Mal: neun … zehn. Der zehnte ist wieder da. Der Brunnen bleibt still, und sie kann ruhen.',
              'Izanami selbst gibt Okiku ihren Namen zurück. Sie steigt nicht mehr aus dem Brunnen, sondern zum Himmel.'),
    'kotaro': ('Kotarō landet auf dem Kurama und legt Sōjōbō die Feder zu Füßen. Aus dem Tengu-Kind ist ein Tengu geworden.',
               'Über den Wolken fliegt Kotarō höher als jeder Tengu vor ihm. Die Krähen erzählen noch heute davon.'),
    'seimei': ('Seimei schreibt den letzten Bannspruch und verbrennt die Feder. Der Hof in Kyō wird nie erfahren, wie knapp es war.',
               'Seimei versiegelt den bösen Stern in einem Spiegel. Er hängt bis heute in einem Schrein, den niemand finden kann.'),
    'akago': ('Akago wirft die Keule fort und lacht. Ein Oni, der Menschen beschützt – im Dorf erzählt man sich lieber diese Geschichte.',
              'Shuten-dōji hätte es nie für möglich gehalten: Ein Oni-Kind sitzt an der Tafel der Himmelsgötter und darf bleiben.'),
    'susanoo': ('Susanoo legt Kusanagi auf den Altar seiner Schwester. Der Sturmgott hat einmal nichts zerstört, sondern etwas gerettet.',
                'Amaterasu tritt aus ihrer Höhle, um ihren Bruder zu begrüßen. Zum ersten Mal seit Äonen lachen Sonne und Sturm gemeinsam.'),
}

STORY_NORMAL = ['Die Nacht der hundert Dämonen ist vorüber.',
                'Einer nach dem anderen kehren die Yōkai in ihre Brunnen, Wälder und Ruinen zurück.']
STORY_TRUE = ['Der böse Stern ist gefallen, und die Himmelsgefilde sind frei.',
              'Die Yōkai ziehen heim – nicht vertrieben, sondern versöhnt.']

T_STORY = 4.2        # Sekunden pro Textblock
T_CREDITS = 15.0


class Epilogue:
    def __init__(self, game, run):
        self.g, self.run = game, run
        self.t = 0.0
        self.true = run.depth >= 6
        self.char = run.char
        story = STORY_TRUE if self.true else STORY_NORMAL
        end = ENDINGS.get(self.char, ('', ''))[1 if self.true else 0]
        self.blocks = story + [end]
        seen = [e for e in game.save.data.get('enemies_seen', []) if e in ENEMIES and sheets.has(ENEMIES[e]['sprite'])
                and sheets.is_hi(ENEMIES[e]['sprite'])]
        if len(seen) < 6:
            seen += [e for e in ('kappa', 'kasa_obake', 'chochin', 'bakeneko', 'oni', 'kodama', 'nopperabo', 'gaki') if e not in seen]
        rng = random.Random(run.seed)
        rng.shuffle(seen)
        self.parade = seen[:14]
        self.t_story_end = 1.5 + T_STORY * len(self.blocks)
        self.duration = self.t_story_end + T_CREDITS
        p = run.player
        beaten = getattr(run, 'bosses_beaten', []) or []
        self.credits = [
            ('Yōkai no Michi', 18, (255, 230, 170)),
            ('', 6, None),
            ('%s – %s' % (CHARS[self.char]['name'], CHARS[self.char]['title']), 10, (240, 225, 200)),
            ('Ebene %d  •  %d:%02d  •  %d Yōkai besiegt  •  %d Items' % (run.depth, run.time // 60, run.time % 60, run.kills, len(p.items)), 7, (210, 200, 185)),
            ('Bosse: ' + (', '.join(BOSSES[b]['name'] for b in beaten) if beaten else '–'), 7, (210, 200, 185)),
            ('', 10, None),
            ('Spielidee und Leitung', 7, (190, 170, 150)),
            ('LucciArch', 11, (250, 240, 220)),
            ('', 6, None),
            ('Programmierung, Pixelgrafik und Musik', 7, (190, 170, 150)),
            ('LucciArch mit Claude', 11, (250, 240, 220)),
            ('', 6, None),
            ('Alle Grafiken und Klänge wurden selbst erzeugt.', 7, (200, 190, 175)),
            ('Die Yōkai stammen aus der japanischen Überlieferung –', 7, (200, 190, 175)),
            ('nachzulesen im Yōkai-Lexikon im Hauptmenü.', 7, (200, 190, 175)),
            ('', 12, None),
            ('Danke fürs Spielen.', 12, (255, 220, 160)),
        ]
        self.petals = [[rng.uniform(0, W), rng.uniform(-H, 0), rng.uniform(8, 20), rng.uniform(0, 6)] for _ in range(40)]
        self._sky_cache = {}

    # ---------------------------------------------------------------- helpers
    def dawn(self):
        return max(0.0, min(1.0, (self.t - 1.0) / (self.t_story_end - 1.0)))

    def sky(self, s, d):
        key = int(d * 40)
        img = self._sky_cache.get(key)
        if img is None:
            img = pygame.Surface((W, 240))
            dd = key / 40
            top_n, bot_n = (14, 10, 36), (44, 24, 66)
            top_d, bot_d = (70, 92, 150), (250, 170, 120)
            for y in range(240):
                f = y / 240
                n = [top_n[i] + (bot_n[i] - top_n[i]) * f for i in range(3)]
                dcol = [top_d[i] + (bot_d[i] - top_d[i]) * f ** 1.4 for i in range(3)]
                c = [int(n[i] + (dcol[i] - n[i]) * dd) for i in range(3)]
                pygame.draw.line(img, c, (0, y), (W, y))
            self._sky_cache[key] = img
        s.blit(img, (0, 0))

    # ---------------------------------------------------------------- frame
    def frame(self, s, dt, nav):
        self.t += dt
        d = self.dawn()
        gfx.HI.clear()
        self.sky(s, d)
        # Sterne verblassen
        rng = random.Random(5)
        for i in range(90):
            x, y = rng.randrange(W), rng.randrange(150)
            if rng.random() > d * 1.2:
                s.set_at((x, y), (220, 220, 255))
        # Mond sinkt, Sonne steigt
        my = 52 + d * 120
        if my < 200:
            pygame.draw.circle(s, (250, 240, 215), (90, int(my)), 16)
        sy = 230 - d * 120
        gfx.draw_glow(s, 380, int(sy), 70, (255, 200, 130), int(40 + 120 * d))
        pygame.draw.circle(s, (255, 236, 170), (380, int(sy)), int(18 + 4 * d))
        pygame.draw.circle(s, (255, 250, 220), (380, int(sy)), int(12 + 3 * d))
        # Berge in zwei Schichten
        for layer, (base, col_n, col_d, amp) in enumerate(((180, (30, 22, 52), (120, 90, 120), 30), (215, (20, 14, 32), (70, 48, 70), 18))):
            col = [int(col_n[i] + (col_d[i] - col_n[i]) * d) for i in range(3)]
            pts = [(0, H)]
            for x in range(0, W + 20, 16):
                pts.append((x, base - amp * math.sin(x * 0.011 + layer * 2) - amp * 0.4 * math.sin(x * 0.037 + layer)))
            pts.append((W, H))
            pygame.draw.polygon(s, col, pts)
        ground = [int(16 + 34 * d), int(12 + 22 * d), int(22 + 22 * d)]
        pygame.draw.rect(s, ground, (0, 250, W, H - 250))
        # Torii auf dem Hügel
        if not hasattr(self.g, '_title_torii'):
            self.g.draw_night(pygame.Surface((W, H)))
        ti = self.g._title_torii
        s.blit(ti, (300 - ti.get_width() // 2, 252 - ti.get_height()))
        # Zug der Yōkai zieht nach links davon und verblasst im Morgenlicht
        a = int(255 * max(0.0, 1 - d * 1.4))
        if a > 0:
            for i, eid in enumerate(self.parade):
                x = W + 30 + i * 46 - self.t * 34
                if -40 < x < W + 40:
                    spr = ENEMIES[eid]['sprite']
                    fr = sheets.frame(spr, sheets.LEFT, int(self.t * 6 + i) % 4, 1)
                    bob = abs(math.sin(self.t * 5 + i)) * 2
                    gfx.hi_blit(fr, x, 250 - bob, a)
        # Spielfigur blickt in den Sonnenaufgang
        if sheets.has(self.char) and sheets.is_hi(self.char):
            fr = sheets.frame(self.char, sheets.RIGHT, 0)
            ct = max(0.0, self.t - self.t_story_end)
            gfx.hi_blit(fr, 250, 252, int(255 - min(165, ct * 130)))
        # Kirschblüten
        for p in self.petals:
            p[1] += p[2] * dt
            p[0] += math.sin(self.t + p[3]) * 10 * dt - 6 * dt
            if p[1] > H:
                p[1] -= H + 10
            if d > 0.2:
                s.fill((240, 170, 200) if p[3] > 3 else (255, 214, 230), (int(p[0]) % W, int(p[1]), 2, 2))
        T = gfx.TEXT
        if self.t < self.t_story_end:
            i = int((self.t - 1.5) // T_STORY)
            if 0 <= i < len(self.blocks):
                lt = (self.t - 1.5) - i * T_STORY
                al = int(255 * max(0, min(1, lt * 2, (T_STORY - lt) * 2)))
                ov = pygame.Surface((W, 54), pygame.SRCALPHA)
                ov.fill((8, 4, 14, int(al * 0.55)))
                s.blit(ov, (0, 264))
                self.g._wrap_c(self.blocks[i], W // 2, 272, W - 80, 9 if i < len(self.blocks) - 1 else 8,
                               (250, 240, 220) if i < len(self.blocks) - 1 else (255, 225, 170), al)
        else:
            ct = self.t - self.t_story_end
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((6, 4, 10, int(min(150, ct * 120))))
            s.blit(ov, (0, 0))
            y = H + 10 - ct * 26
            for txt, size, col in self.credits:
                if col and -20 < y < H + 10:
                    al = int(255 * max(0, min(1, (y - 10) / 30, (H - y) / 30)))
                    T.add(txt, W // 2, y, size, col, 'c', alpha=al)
                y += size * 1.9
        if self.t > 1.0:
            T.add('Enter – weiter', W - 10, H - 12, 6, (170, 160, 150), 'r', alpha=120)
        done = self.t >= self.duration
        for n in nav:
            if n in ('ok', 'back') or isinstance(n, tuple):
                if self.t > 1.0:
                    if self.t < self.t_story_end:
                        self.t = self.t_story_end           # Text überspringen → Abspann
                    else:
                        done = True
        return done
