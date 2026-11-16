# Erledigt (Runden 32–34): Titelbildschirm komplett neu
- Runde 32: Panorama in fünf Ebenen (`art_src/title/panorama.py` → `yokai/assets/env/_title/`): Himmel mit Mondhof,
  Fuji-Kette, Zedernkamm mit Pagode, Nebel, Vordergrund (Torii im See, Schilf, Tōrō, Kirschzweig). Spiegelungen im
  Wasser sind mitgebacken. `app.draw_night` legt die Ebenen mit Parallaxe übereinander (auch Hintergrund aller Menüs).
- Runde 33: Logo (`art_src/title/logo.py`): Schriftzug aus YokaiFude, Goldstufen, Hanko-Siegel 妖怪の道 (Kanji als
  Strich-Skelette im 16er-Raster). Hi-Res-Ebene.
- Runde 34: Einblendung (Nacht → Logo → Menü), Pinselstrich-Auswahl (`brush.png`), Menüschleier, Glühwürmchen, Hitodama.

# Nächster Schritt: Kapitel-Kartenbildschirm / Charakterauswahl im selben Stil
Die Charakterauswahl (`st_chars`) und die Untermenüs (`menu_bg`) nutzen jetzt zwar das Panorama, aber ihre Tafeln
(`gfx.panel`) wirken neben dem neuen Titel altmodisch. Charakterauswahl neu: Figur groß auf einem Steinpodest am
Seeufer, Name als Pinselschrift-Banner, Werte als Tuschebalken, gesperrte Figuren als Schattenriss mit Siegel.
Pinselstrich-Auswahl (`brush.png`) auch in Pause-, Options- und Untermenüs verwenden.
Warum: Der erste Eindruck endet nicht beim Titel – der Sprung in die alten Tafeln fällt jetzt auf.

# Weitere Ideen
- Titel: Tageszeit/Jahreszeit je nach Fortschritt (z. B. nach dem Wahren Sieg roter Herbstmond, nach Yomi violette Nacht)
- Requisiten Teil 3: eigene Requisiten für `yomi_oku`, Grabsteine Hakaba mit Inschrift/Opfergaben
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Eigenes Geschoss-Sprite für Pfirsiche, Fūjins Windklingen und Windsicheln
- Synergien mit drei Items (die drei Kaiserinsignien als „große“ Kombination mit Fanfare)
