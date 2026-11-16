# Erledigt (Runden 46–47)
- Runde 46: `yomi_oku` (Kapitel VII) hat eigene Kacheln – neues Biom in `art_src/fable/environment/biomes.py`
  (Paletten `VIOLET`, `ONIBI`), Boden-Deko in `floors.py`, Lackband in `walls.py`, Requisiten + Wanddeko in `props.py`.
  Der Shortcut `BIOMES['yomi_oku']['_id'] = 'yomi'` in `yokai/data.py` ist entfernt.
  Achtung: `build.py <biom>` schreibt nach `art_src/fable/environment/<biom>/` → von Hand nach `yokai/assets/env/` kopieren;
  `hi.py` schreibt `rock_hi.png` direkt. PNGs, deren Pixel gleich bleiben, mit `git checkout` zurücksetzen (nur Kodierung anders).
- Runde 47: Hakaba-Familiengrab mit Inschrift 家之墓 (`GLYPHS` in props.py, Hi-Res per `hpx`), Vasen, Kōro, Opfergaben.

# Nächster Schritt: Omikuji-Ereignisraum
Ein Schreinmädchen (oder Losschrein-Kasten) lässt dich ein Los ziehen: 大吉 / 吉 / 小吉 / 凶 / 大凶 mit Segen oder Fluch
für die aktuelle Ebene (z. B. +Glück, Bonusherz – oder Fluch: mehr Gegner, dafür mehr Mon). Ein 凶-Los kann man an
einen Baum knoten, um den Fluch gegen ein Opfer (Mon) abzulegen. Siegel `seal_kichi`/`seal_kyo` aus
`art_src/title/charsel.py` wiederverwenden; Muster: Ereignisse in `design/ereignisse.md` und `run.py`.
Warum: Ereignisräume bringen viel Wiederspielwert, und das Omikuji passt zur Folklore und den neuen Siegeln.

# Weitere Ideen
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Gesten beim Laufstart: Figur macht ihre Geste im ersten Raum (`pose_fx` auf doppelte Podestgröße ausgelegt → Versätze halbieren)
- Lexikon-Synergieseite: von der Synergie zurück zu den beteiligten Items im Codex springen
- Totenpalast-Ambiente: eigene Wetter-/Partikel-Eigenheit (Maden-Glühwürmchen? Izanamis acht Donnergötter als Blitze im Hintergrund)
- Requisiten Teil 4: Yashiki und Kawabe (noch einfache Grundformen) neu modellieren
