# Erledigt (Runden 48–49)
- Runde 48: Omikuji-Schrein überarbeitet (`run.py` → `interact` Fälle `omikuji`/`musubi`, Aufbau in `populate`).
  Ein Los pro Schrein; Kichi setzt `self.blessing`, Kyō setzt `self.curse` (nur `dunkel`/`nebel`/`verirrt`, weil
  `labyrinth` beim Erzeugen der Ebene greift). Neues Requisit `props.musubi(n)`; das 吉/凶-Siegel schwebt über dem Kasten.
- Runde 49: Lexikon-Synergieseite → Enter springt zu den Items im Codex (`lex_item`, `codex_back` in `app.py`).

# Nächster Schritt: Gesten beim Laufstart
Die Figur macht im ersten Raum einmal ihre Geste aus der Charakterauswahl (Pose-Klänge `pose_*` gibt es schon).
`pose_fx` ist auf doppelte Podestgröße ausgelegt → Versätze halbieren. Warum: gibt jedem Lauf einen kleinen,
charaktereigenen Auftakt und nutzt fertige Grafik/Klänge.

# Weitere Ideen
- Omikuji als Eintrag auf der Lexikon-Seite „Ereignisse“ (`LEX_EVENTS`) plus Erfolg „Fluch gebunden“ (Musubi-Gestell)
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Totenpalast-Ambiente: eigene Partikel (Maden-Glühwürmchen, Izanamis acht Donnergötter als Blitze im Hintergrund)
- Requisiten Teil 4: Yashiki und Kawabe (noch einfache Grundformen) neu modellieren
- Das Musubi-Gestell auch in Schreinräumen (`shrine`) aufstellen, damit Flüche häufiger lösbar sind
