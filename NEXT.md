# Erledigt (Runden 30–31)
- Runde 30: **Grundfläche je Fels-Variante.** `gfx.rock_foot(x, y, biome)` misst x-Mitte und halbe Breite aus dem
  Alpha des Sprite-Rumpfs (Hi-Res-Zeilen 32–52, ohne Bodenschatten), begrenzt auf 5–12 px und die Kachel.
  `entities.solid_hit` nutzt sie für `T_ROCK`; das Biom setzt `Run.new_floor` in `entities.FOOT_BIOME`.
  Höhe bleibt `FOOT[T_ROCK]`. Test: `tools/kolltest.py` (schmale Ryūgū-Variante).
- Runde 31: Takamagahara: Kumo-Wolkenfels mit Spiralen, Magatama auf Wolkenkissen. Yukiyama: facettierter
  Eisbrocken (Risse, Blasen, Schneekappe), Eiszapfen in Schneewehe. Bau: `cd art_src/fable/environment && python3 hi.py`.

# Nächster Schritt (Wunsch von Luca): Titelbildschirm komplett neu
Den Startbildschirm/das Hauptmenü komplett überarbeiten – **nicht** einfach Sprites herumlaufen lassen,
sondern ein schöner, stimmiger Titelbildschirm wie bei richtig guten Spielen: z. B. großes gemaltes
Mondnacht-Panorama in Ebenen (Torii, Berge, Nebel, Parallaxe), handgesetztes Logo „Yōkai no Michi“
mit Kanji, edles Menü mit Pinselstrich-Auswahl, dezente Partikel (Glühwürmchen, Hitodama), Einblendung.
Alles selbst gepixelt (Hi-Res-Ebene), Stil laut `design/art/art-bible.md`. Auf mehrere Runden verteilen
(1: Panorama-Ebenen als Generator in `art_src/`, 2: Logo, 3: Menü + Partikel + Einblendung).
Warum: ausdrücklicher Wunsch von Luca, der erste Eindruck des Spiels.

# Weitere Ideen
- Requisiten Teil 3: eigene Requisiten für `yomi_oku` (nutzt noch Yomi), Grabsteine Hakaba mit Inschrift/Opfergaben
- Größere Hi-Res-Figur „Izanami, die Verweste“ für Phase 3 (`art_src/fable/bosses_3/`)
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Eigenes Geschoss-Sprite für Pfirsiche, Fūjins Windklingen und Windsicheln
- Synergien mit drei Items (die drei Kaiserinsignien als „große“ Kombination mit Fanfare)
