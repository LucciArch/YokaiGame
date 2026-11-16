# Erledigt (Runden 26–27)
- Runde 26: **Izanami als Endbossin** in Kapitel VII (`Izanami.final`, `run.depth >= 7`): doppeltes Leben,
  Phase 2 schon bei 66 % (`Boss.P2`), Phase 3 bei 33 % mit Schriftzügen, zusätzlicher Dunkelheit
  (`Boss.extra_dark` → `Run.dark_level()`), Händen der Toten am ganzen Arenarand (an den Boss gebundene
  `Hazard.boss`, verschwinden mit ihrem Tod) und dem Angriff `a_ikazuchi` (acht Blitzbahnen in zwei Fächern +
  gezielter Großer Donner). Bosstest: ~95 s, prüft Phase 3, Dunkelheit und Hände.
- Runde 27: Erfolg **„Rückkehr aus Yomi“** → Item `yomi_momo` (Pfirsich, `sig_momo` in `on_hurt`), Synergie
  `izanagis_flucht` (Pfirsich + Izanamis Kamm, Pfirsiche auch bei der Rolle), Epilog `STORY_YOMI`,
  Icon `art_src/fable/items/icons_v15.py`. Bosstest prüft Freischaltung, Epilog und Pfirsichwurf.

# Nächster Schritt (Wunsch von Luca)

**Umgebungsobjekte überarbeiten: neue Sprites, ehrliche Hitboxen, Überfliegen mit Flug-Items**
Luca: Steine, Bambussprossen usw. sollen besser modelliert sein und zur jeweiligen Umgebung passen; die Hitbox
fühlt sich oft größer an als das Objekt; mit Flügeln/Flug-Items soll man darüber fliegen können.

Befund aus dem Code:
- `entities.blocked()` prüft die vier Ecken des Begrenzungsquadrats gegen `SOLID_TILES` (Fels, Krug, Laterne)
  → jedes Hindernis blockt die volle 32×32-Kachel, auch wenn der Stein rund und kleiner gezeichnet ist.
- Fliegen (`p.f['fly']`, Gegner `fly`) überquert bisher nur Gruben (`T_PIT`), keine Felsen/Requisiten.

Plan:
1. Bestandsaufnahme: welche Hindernis-Requisiten pro Biom gezeichnet werden (Felsen, Bambus, Krüge, Laternen,
   Dekor in `art_src/fable/environment`), Screenshot jedes Bioms.
2. Hitbox je Hindernisart an die gezeichnete Form anpassen (Kreis/Ellipse statt voller Kachel, z. B. Fels Radius
   ~11 px, Krug ~9 px); `blocked()` auf Abstand zum Objektmittelpunkt umstellen, Geschosse gleich behandeln.
3. Fliegen: `fly` darf Felsen und niedrige Requisiten (Fels, Bambusstumpf, Krug) überqueren; Laternen/hohe
   Säulen bleiben fest. Beim Überfliegen Figur über dem Objekt zeichnen (Ebenen-Reihenfolge).
4. Sprites pro Biom neu pixeln (Hi-Res, Licht oben links, dicke Umrisse, Biom-Farben): Bambuswald-Stümpfe,
   Bergfelsen, Eisbrocken, Korallen, Lavagestein, Wolkenfelsen, Totenpalast-Grabsteine.
5. Tests: Bot-Läufe (bleibt niemand hängen?), uiflow, neuer Kurztest „fliegende Figur überquert Fels“.

Warum: Direkter Spielgefühl-Gewinn in jedem Raum – unfaire Kollisionen ärgern mehr als jede fehlende Inhalte.

## Danach (Endkapitel Teil 3+)
- Größere Hi-Res-Figur „Izanami, die Verweste“ für Phase 3 (`art_src/fable/bosses_3/`), heute nutzt sie die
  Kapitel-VI-Figur
- Eigene Kacheln/Requisiten für `yomi_oku` (Shortcut `_id = 'yomi'` in `data.py` entfernen) – passt gut zu Schritt 4 oben
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin

## Weitere Ideen
- Ausweichender Mess-Bot für Dash-/Nahkampf-Synergien in `tools/synbalance.py` (Herrenlose Katze, Tengu-Flug
  wirken im Raum-Bericht schwach, der Bot misst sie aber unfair)
- Eigenes Geschoss-Sprite für Pfirsiche, Fūjins Windklingen und Windsicheln (jetzt runde Kugeln)
- Synergien mit drei Items (z. B. die drei Kaiserinsignien als „große“ Kombination mit Fanfare)
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Kanabō: Feuerraten-Malus (-0,4) prüfen
