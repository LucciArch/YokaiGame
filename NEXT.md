# Erledigt (Runden 55–57)
- Runde 55 (parallele Sitzung): Ama-no-Iwato Teil 1 – Biom `iwato` (Kacheln, Wände, Requisiten) und Biom-Daten in
  `yokai/data.py`; noch **ohne** Pforte, Boss und Einbindung in `Run.oku`.
- Runde 56: Requisiten Ōeyama (Kanabō im Fels, Komodaru mit Oni-Mon, Knochenhaufen mit Oni-Maske) und Shinkai
  (Hamaguri mit Perle und Shinkirō-Dunst, Sango-Koralle mit Leuchtfischen, versunkene Tōrō) in
  `art_src/fable/environment/props.py`. Neu bauen: `build.py <biom>`, `hi.py`, `rock.png` nach `yokai/assets/env/<biom>/`
  kopieren, floor/wall-PNGs per `git checkout` zurücksetzen.
- Runde 57: Lexikon-Ereignisseite Omikuji zeigt die gezogenen Lose (`App.KUJI`, `kuji_seen`); uiflow2 zeichnet sie.

# Ama-no-Iwato: in Arbeit in einer anderen Sitzung (NICHT anfassen)
- Runde 58 (andere Sitzung): Iwato-Pforte, `Run.oku`, Endbossin Amaterasu (`bosses.Amaterasu`, Sprite
  `art_src/fable/bosses_3/boss_amaterasu.py`), Sieg-/Epilogtext, Lexikon. Teil 3 (Erfolg, Item-Belohnung) folgt dort.

# Nächster Schritt: Requisiten Teil 6 – Enma-chō, Tsukiyomi und Yomi no Oku
Gleiches Vorgehen wie Runde 56. Warum: letzte Biome mit Grundformen-Requisiten.

# Weitere Ideen
- Requisiten Teil 6: Enma-chō, Tsukiyomi und Yomi no Oku noch in Grundformen – gleiches Vorgehen wie Runde 56
- Wanddekos Yashiki/Kawabe/Ōeyama/Shinkai ebenfalls in Hi-Res überarbeiten (`wall_decos`)
- Totenpalast-Ambiente: eigene Partikel (Maden-Glühwürmchen, Izanamis acht Donnergötter als Blitze im Hintergrund)
- Kawabe-/Shinkai-Ambiente: Glühwürmchen über Wasser, aufsteigende Leuchtpartikel in der Tiefsee
- Shinkirō als Ereignis: eine Hamaguri spiegelt einen Trugladen vor, dessen Items nach dem Kauf verschwinden können
