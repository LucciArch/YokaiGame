# Erledigt (Runden 55–57)
- Runde 55 (parallele Sitzung): Ama-no-Iwato Teil 1 – Biom `iwato` (Kacheln, Wände, Requisiten) und Biom-Daten in
  `yokai/data.py`; noch **ohne** Pforte, Boss und Einbindung in `Run.oku`.
- Runde 56: Requisiten Ōeyama (Kanabō im Fels, Komodaru mit Oni-Mon, Knochenhaufen mit Oni-Maske) und Shinkai
  (Hamaguri mit Perle und Shinkirō-Dunst, Sango-Koralle mit Leuchtfischen, versunkene Tōrō) in
  `art_src/fable/environment/props.py`. Neu bauen: `build.py <biom>`, `hi.py`, `rock.png` nach `yokai/assets/env/<biom>/`
  kopieren, floor/wall-PNGs per `git checkout` zurücksetzen.
- Runde 57: Lexikon-Ereignisseite Omikuji zeigt die gezogenen Lose (`App.KUJI`, `kuji_seen`); uiflow2 zeichnet sie.

# Ama-no-Iwato: fertig (Runden 55, 58, 59)
- Biom `iwato`, Iwato-Pforte nach dem Wahren Sieg (`Run.oku`), Endbossin `bosses.Amaterasu` (3 Phasen, Sprite
  `art_src/fable/bosses_3/boss_amaterasu.py`, Import über `art_src/import_fable.py <ordner>`), Erfolg `iwato`,
  Item `uzume_suzu` (sig `suzu`), Synergie `ama_no_iwato` (sig `iwato`). bosstest/sigtest prüfen alles.
- Offen/Ideen: Titelbild-Stimmung nach Iwato-Sieg (wie 'yomi' in `app.py`), Amaterasu-Bossmusik, Boss-Balance
  (bosstest: ~80 Treffer gegen ~30 bei Izanami – etwas schwerer gewollt, beobachten).

# Erledigt (Runden 60–63, Wunsch von Luca)
- Runde 60: Lichtsystem – `Run.collect_lights()` sammelt alle Lichtquellen (Spielerin, Laternen, leuchtende
  Requisiten `gfx.PROP_LIGHT`, Wanddekos `gfx.WALL_LIGHT`, Gegner mit `glow`, Bosse, Sockel, Feuer/Blitz/Meteor-Hazards,
  helle Gegnergeschosse, brennende/Ketten-Ofuda, Explosions-/Seelen-Partikel). `draw_dark` stanzt Lichtkreise,
  `draw_light_tint` färbt sie, `hi_light` hellt Hi-Res-Figuren an jeder Lichtquelle auf.
  **Neue leuchtende Requisiten/Wanddekos/Gegner immer in PROP_LIGHT/WALL_LIGHT bzw. mit `glow=` eintragen.**
- Runde 61: Torii-Pforten (5 Varianten), Kami-/Oni-Schrein, Tanuki-Automat in Hi-Res
  (`art_src/fable/environment/objects_hi.py`, gebaut auch von `hi.py`).
- Runde 62: Ladentheke, Saisen, Omikuji, Musubi, Ema, Onsen, Teebank/-schale, Treppe in Hi-Res (gleiche Datei).
- Runde 63: Symbol für `kaze_bukuro` (`art_src/fable/items/icons_v15.py`, Aufruf mit `PYTHONPATH=..`).
- Durchsicht: Alle Gegner und Figuren sind Hi-Res, alle Items haben Symbole. Runde 64: Epilog-Torii nutzt `torii_hi.png`.
  Minikarten-Symbole sind bewusst klein.

# Wunsch von Luca (gilt ab jetzt dauerhaft): Item-Synergien
Nach den Grafiken immer weiter daran arbeiten, dass **alle Items miteinander funktionieren** (Beispiel: Laser + Mehrfachwurf
+ Zielsuche muss drei zielsuchende Laser ergeben). Runde 65: Waffen (`weapons.py`) übernehmen alle Wurf-Eigenschaften
(`weapons.shot_flags`, `shot_angles`, Träger-Geschoss `_carrier` für damage_enemy). Test: `tools/waffentest.py`.
Runde 66: Gefolge erbt `shot_flags`, Kreisschild/Aura nutzen `weapons.touch` + `elem_flags`.
Runde 67: `Run.fire_player_bullet` vererbt `INHERIT` (burn/poison/slow) an jedes Spielergeschoss.
Nächste Kandidaten: aktive Items (Geschoss-Salven) mit Mehrfachwurf/Elementen, Bodenfeuer/Explosionen mit Gift/Frost, Sigs prüfen, die nur
für Talismane greifen (z. B. `bullet_tick`) – sollen sie auch für Strahl/Hieb wirken?

# Erledigt: Requisiten Teil 6 (Runden 68–69)
- Enma-chō: Kohlebecken auf Krallenfüßen, Jōhari no Kagami, Nintōjō (Miru-me/Kagu-hana). Tsukiyomi: Tsuki no Katsura,
  Tsukimi-Sanbō mit Dango/Susuki, Usu und Kine. Yomi no Oku: Ōkamuzumi-Pfirsichbaum statt Lacksäule. Lichter in
  `gfx.PROP_LIGHT` angepasst. Damit hat kein Biom mehr Grundformen-Requisiten.
- Hinweis für parallele Läufe: Rundennummer erst direkt vor dem Push aus `origin/main` bestimmen (mehrere Sitzungen pushen gleichzeitig).

# Erledigt: Item-Synergien (Runden 70–72)
- Runde 70: Aktive Salven (Ofuda-Sturm, Shikigami-Ruf, Hyōtan-Sauger) erben `weapons.shot_flags` ohne chain/split/explode;
  Mehrfachwurf = mehr Wellen bzw. Shikigami.
- Runde 71: `damage_enemy` – Folgeschaden der Spielerin (`run._echo`: Explosion, Hazards 'p') trägt burn/poison/slow der Items.
- Runde 72: `weapons._path_sigs` – Bahn-Sigs (`gross`, `stromauf`, `seidenfaden`, `windstoss`, `kammzinken`) wirken für
  Strahl, `gross`/`seidenfaden` für Hiebe. `sichel`, `schweben`, `koi_drache` bleiben bewusst Talisman-only.
- Alle Fälle in `tools/waffentest.py`. Alle 98 Synergien haben schon eigene sig_-Fähigkeiten.

# Erledigt (Runden 73–74)
- Runde 73: `weapons.fire` ruft `sigs.on_fire` selbst auf. Hieb/Strahl: vorher auf ein Probe-Geschoss (`_carrier` mit
  `_big`/`_gold` im fl), dessen dmg/fl/Farbe dann der Angriff nutzt; Bogen/Fächer wie bisher danach auf die Pfeile.
  Goldwürfe (`gold_shots`) jetzt für alle Waffen. Tests in `tools/waffentest.py` (schlagen auf altem Code fehl).
- Runde 74: `Run.LAMP_ITEMS` – Laternen-/Feuer-Items vergrößern und färben das Spielerinnen-Licht.
  Achtung: `ITEMS[i]['icon']` ist meist die Item-ID (eigene Symbole), nicht 'lantern'/'flame'.

# Erledigt (Runden 75–76)
- Runde 75: `weapons._hit` gibt immer ein Träger-Geschoss (auch ohne Flags) mit `t` (Strahl: along/shotspd → Kyūdō) und
  `curve` (Hieb mit sig `sichel` → Mondsichel-Klinge). Wurfstern: höchstens ein Abpraller pro Hieb/Strahl (`_ric=9` nach dem
  ersten Treffer, gilt auch für Kammzinken-/Spiegel-Nebenstrahlen).
- Runde 76: `Run.LAMP_ACTIVES` (Kitsune-Laterne, Onryō-Kerze) und `LAMP_TRINKETS` (Feuer-Anhänger) zählen fürs Spielerinnen-Licht.

# Erledigt (Runden 77–78)
- Runde 77: `weapons.beam` – Strahltreffer tragen `pierce` (Tessos Schwarm, eine Ratte pro Strahl über `_rat`);
  Spiegelung ruft `sigs.bullet_bounce` mit Träger-Geschoss (Kappa-Festmahl, Brandung einmal pro Strahl über `_br`).
- Runde 78: `weapons._hit` ruft bei zerplatzenden Sprengsiegel-Treffern `sigs.bullet_end` (Feuerwerk über Edo).
  Bewusst offen: Strahl-Ende ohne Treffer löst keine Ende-Sigs aus (wäre Funken-Spam bei jedem Strahl).

# Nächster Schritt: Balance-Nachmessung Waffen-Builds
Warum: Seit Runde 65 übernehmen Waffen fast alle Wurf-Fähigkeiten – Strahl/Hieb könnten jetzt zu stark sein.
`tools/synbalance.py` um Waffen (w_laser, w_sword, w_bow) erweitern, Schaden pro Sekunde gegen Talisman-Builds
vergleichen, Ausreißer (> 2× Median) dämpfen; Bericht nach `design/balance/`.

# Weitere Ideen
- Amaterasu-Bossmusik (`art_src/music/`) und Titelbild-Stimmung nach dem Iwato-Sieg (wie 'yomi' in `app.py`)
- Wanddekos Yashiki/Kawabe/Ōeyama/Shinkai/Enma-chō/Tsukiyomi in Hi-Res überarbeiten (`wall_decos`)
- Mondpalast-Ambiente: fallende Katsura-Blätter, Mondhase als seltener Ereignis-NPC (Mochi-Tausch)
- Shinkirō als Ereignis: eine Hamaguri spiegelt einen Trugladen vor
- Tessos Schwarm auch für Hiebe in Gruppen (gedeckelt wie Wurfstern) – erst nach der Balance-Messung
