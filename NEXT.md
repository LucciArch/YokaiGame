# Erledigt (Runden 55–57)
- Runde 55 (parallele Sitzung): Ama-no-Iwato Teil 1 – Biom `iwato` (Kacheln, Wände, Requisiten) und Biom-Daten in
  `yokai/data.py`; noch **ohne** Pforte, Boss und Einbindung in `Run.oku`.
- Runde 56: Requisiten Ōeyama (Kanabō im Fels, Komodaru mit Oni-Mon, Knochenhaufen mit Oni-Maske) und Shinkai
  (Hamaguri mit Perle und Shinkirō-Dunst, Sango-Koralle mit Leuchtfischen, versunkene Tōrō) in
  `art_src/fable/environment/props.py`. Neu bauen: `build.py <biom>`, `hi.py`, `rock.png` nach `yokai/assets/env/<biom>/`
  kopieren, floor/wall-PNGs per `git checkout` zurücksetzen.
- Runde 57: Lexikon-Ereignisseite Omikuji zeigt die gezogenen Lose (`App.KUJI`, `kuji_seen`); uiflow2 zeichnet sie.

# Nächster Schritt: Ama-no-Iwato Teil 2 – Pforte und Endbossin Amaterasu
Biom `iwato` existiert, ist aber nicht erreichbar. Als Nächstes: Iwato-Pforte nach dem ersten Wahren Sieg
(analog zur Yomi-Pforte in `Run.oku`), Raumfolge in Kapitel VII, Endbossin **Amaterasu** (Hi-Res-Figur, Phasen:
verborgen im Fels → Spiegel-Lichtstrahlen → Sonnenscheibe), Lexikon-Eintrag, Erfolg und Epilog.
Warum: Der Inhalt ist halb fertig im Spiel und bringt den zweiten Weg mit echtem Endkampf.
Achtung: Eine zweite Sitzung arbeitet evtl. parallel daran – vorher `git log` prüfen.

# Weitere Ideen
- Requisiten Teil 6: Enma-chō, Tsukiyomi und Yomi no Oku noch in Grundformen – gleiches Vorgehen wie Runde 56
- Wanddekos Yashiki/Kawabe/Ōeyama/Shinkai ebenfalls in Hi-Res überarbeiten (`wall_decos`)
- Totenpalast-Ambiente: eigene Partikel (Maden-Glühwürmchen, Izanamis acht Donnergötter als Blitze im Hintergrund)
- Kawabe-/Shinkai-Ambiente: Glühwürmchen über Wasser, aufsteigende Leuchtpartikel in der Tiefsee
- Shinkirō als Ereignis: eine Hamaguri spiegelt einen Trugladen vor, dessen Items nach dem Kauf verschwinden können
