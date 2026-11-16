# Erledigt (Runden 35–36): Charakterauswahl und Menüs im Titelstil
- Runde 35: `st_chars` neu – Figur groß (Faktor 2) auf Steinpodest im Mondlicht, Name auf Pinselstrich, Werte als
  Goldtusche-Balken (Leben/Kraft/Tempo/Wurfrate aus `CHARS`), Figurenleiste unten, gesperrte als Schattenriss mit
  Siegel 封. Grafik: `art_src/title/charsel.py` → `pedestal.png`, `lock.png`, `ink.png` (in `assets/env/_title/`).
- Runde 36: `Game.brush_sel(key, cx, y, w, dt)` – Pinselstrich-Auswahl in Titel, Pause und Optionen.

# Nächster Schritt: Restliche Untermenüs im Titelstil
Herausforderungen (`st_challenges`), Codex, Lexikon, Erfolge und Statistik nutzen noch die alten Kasten-Tafeln
(`gfx.panel`) mit goldenem Rand für die Auswahl. Auswahl auf `brush_sel` umstellen, Tafeln durch einen weichen
Schleier wie im Titel (`_scrim`) ersetzen, Überschriften in größerer Schrift mit kleinem Siegel daneben.
Warum: Titel, Charakterwahl und Pause sind jetzt aus einem Guss – die Lexikon-/Codex-Seiten fallen dagegen ab.

# Weitere Ideen
- Titel: Tageszeit/Jahreszeit je nach Fortschritt (nach dem Wahren Sieg roter Herbstmond, nach Yomi violette Nacht)
- Charakterauswahl: kurze Idle-Pose je Figur (Kenji zieht das Schwert, Okiku schwebt) und eigener Klang beim Wechsel
- Requisiten Teil 3: eigene Requisiten für `yomi_oku`, Grabsteine Hakaba mit Inschrift/Opfergaben
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Synergien mit drei Items (die drei Kaiserinsignien als „große“ Kombination mit Fanfare)
