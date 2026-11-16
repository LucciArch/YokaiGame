# Erledigt (Runden 50–51)
- Runde 50: Gesten beim Laufstart. Code aus `app.py` nach `yokai/pose.py` verschoben; `pose_fx(..., k=0.5, fade)`
  skaliert Versätze/Bilder um die Fußlinie. `Player.pose_t` (Run setzt 0 bei neuem Lauf), endet nach `POSE_T` = 2.4 s
  oder bei Laufen/Rolle/Wurf. Hinweis: Das Startblinken (iframes) verdeckt die Geste teilweise.
- Runde 51: Omikuji in `LEX_EVENTS` (+ `event_done('omikuji')`), Erfolg `musubi`, Musubi-Gestell im Kami-Schrein.
  „Festtagsgast“ zählt weiter nur `Run.EVENT_KINDS`.

# Nächster Schritt: Requisiten Teil 4 – Yashiki und Kawabe
Die Requisiten dieser Biome sind noch einfache Grundformen; in `props.py` neu als Hi-Res-Pixelart (dicke Umrisse,
satte Nachtfarben) zeichnen, wie bei Totenpalast (Runde 46) und Hakaba (Runde 47). Warum: Diese beiden Biome sieht
man in fast jedem Lauf früh – dort fällt der Stilbruch am meisten auf.

# Weitere Ideen
- Startblinken zu Laufbeginn weglassen, solange die Geste läuft (iframes ohne Blinken), damit sie ganz zu sehen ist
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Totenpalast-Ambiente: eigene Partikel (Maden-Glühwürmchen, Izanamis acht Donnergötter als Blitze im Hintergrund)
- Erfolg „Alle Lose“: Daikichi, Kichi, Chūkichi, Shōkichi und Kyō je einmal gezogen
