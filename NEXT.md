# Erledigt (Runden 43–45)
- Runde 43: Codex → Enter springt zur Synergie des Items auf der Lexikon-Seite **Synergien** (mehrfach drücken blättert,
  `Game.codex_syn`), Esc führt über `Game.lex_back` zurück in den Codex. Synergie-Zeile bricht per `_wrap` um.
  Behoben: KeyError 'Y' im Codex bei entdeckten Ereignis-Items. uiflow2 prüft den Sprung.
- Runde 44: Transformationen zeigen die Fanfare mit ihren drei Item-Symbolen. `Run.slowmo` wird jetzt beim **Anzeigen**
  eines Banners mit `icons` gesetzt (run.py, Banner-Warteschlange), nicht mehr beim Aufheben – sonst verpuffte die
  Zeitlupe während der vorherigen Item-Meldung.
- Runde 45: Endbildschirm mit `veil` statt `gfx.panel` und Omikuji-Siegel `seal_kichi` (吉) / `seal_kyo` (凶)
  aus `art_src/title/charsel.py` (SEALS).

# Nächster Schritt: Requisiten Teil 3
Eigene Requisiten für `yomi_oku` (Kapitel VII) und Grabsteine in Hakaba mit Inschrift und Opfergaben (Hi-Res, `art_src/`).
Warum: Die Menüs und Fanfaren sind jetzt einheitlich; die späten Biome sehen noch am meisten nach Baukasten aus.

# Weitere Ideen
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Gesten beim Laufstart: Figur macht ihre Geste im ersten Raum (ohne Steuerung zu sperren; `pose_fx` ist auf doppelte
  Podestgröße ausgelegt → Versätze halbieren)
- Omikuji als Ereignisraum: Los ziehen (大吉 … 凶) mit Segen oder Fluch für die Ebene – die neuen Siegel passen dazu
- Lexikon-Synergieseite: von der Synergie zurück zu den beteiligten Items im Codex springen
