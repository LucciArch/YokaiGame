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

# Erledigt (Runden 79–80)
- Runde 79: `tools/synbalance.py --waffe=w_sword|w_laser|w_bow` (Nahkampf läuft heran). Bericht
  `design/balance/balance-check-79-waffen-builds.md`: Waffen ≈ 1,4–1,85× Talisman, kein pauschales Dämpfen nötig.
  Fehler behoben: Seiten-/Rückhiebe trafen große Feinde mehrfach pro Angriff (`weapons.melee(seen=…)`, waffentest).
  Offen: „Wenn du getroffen wirst“-Synergien (Hannya-Zorn, Gericht, Oni-Tanz, Unbeugsam) wirken im Gott-Modus-Bot
  mit Schwert übermächtig – Messartefakt, erst mit Lebensgrenze nachmessen.
- Runde 80: Titelbild-Stimmung `'iwato'` in `App.draw_night` (Morgenröte `_dawn`, Strahlenkranz, Vorrang vor 'yomi').

# Erledigt (Runden 81–82)
- Runde 81: Bossstück `amaterasu` („Iwato Kagura“, `art_src/music/tracks.py`, Suzu-Helfer `_suzu`, Skalenwechsel
  `s.scale = SCALES['yo']` zum Sonnenaufgang). `Audio.track_for` erkennt den Iwato-Boss am Seed 164 (57 + 100 + Tiefe 7);
  `validate.py` prüft für jedes Biom, dass die Bossmusik existiert und nur Iwato `amaterasu` spielt.
  Hinweis: `write_ogg` lässt eine `.wav` neben der `.ogg` liegen – nicht committen.
- Runde 82: `synbalance.py --leben` (Bossschaden in % bis zum Tod, ohne Gott-Modus). Hannya-Ring (`hurt_ring`) und
  Daruma-Splitter (`daruma_geist`) teilen sich eine Trefferliste (`b.hit = seen`), 1,5× statt 1,2× Schaden.
  Bericht `design/balance/balance-check-82-leben.md`. Treffer-Auslöser-Frage aus Check 79 damit geklärt.

# Erledigt (Runden 83–84)
- Runde 83: Wanddekos in Hi-Res. `art_src/fable/environment/walldeco_hi.py` (Hi-Raster-Helfer `hr/hp/he/hpoly/hln`,
  eigene Zeichnungen in `HI[biom]`, sonst `wall_decos` mit SS=2) → `wall_deco_hi.png` (je 64x32, nur Deko-Pixel),
  gebaut von `hi.py`. Laufzeit: `gfx.env_walls(..., decos)` merkt Platzierungen, `gfx.walls_hi` legt Scale2x der
  schlichten Wand + Hi-Deko auf `walls_hi`. Gleicher Index wie `wall_deco.png` (WALL_LIGHT gilt weiter); validate prüft das.
  Eigene Hi-Res: Yashiki (Mokumokuren, Schatten hinter Shōji), Kawabe (Rohrkolben, Rinnsal), Ōeyama (Schädel, Kanabō, Oni-Höhle).
- Runde 84: Eigene Hi-Res für Shinkai (Chōchin-anko, Anemonen, Qualle), Enma-chō (Jōhari-Spiegel, Kohlebecken),
  Tsukiyomi (Mondhase mit Mochi, Sichel + Suzu). Übrige Biome nutzen die SS=2-Fassung (glattere Rundungen).

# Erledigt (Runden 85–86)
- Runde 85: `Run.near_synergies()` – Pausenmenü „Items & Werte“ zeigt bis zu 4 Synergien, denen nur noch ein Item fehlt
  („Fast komplett: Name (+ Item)“, unentdeckte als „???“). uiflow2 prüft Logik und Anzeige.
  Hinweis: uiflow2 druckt „menu play“ (Speichern & Hauptmenü nach Retry) – war schon vorher so, ggf. ansehen.
- Runde 86: Eigene Hi-Res-Wanddekos für Jigoku (Lavafall, Ketten + Eisenegge), Iwato (Shimenawa, Kagaribi),
  Yomi no Oku (Misu mit Hand, Tōrō). Lichtpunkte aus `gfx.WALL_LIGHT` bleiben an derselben Stelle.
  Ohne eigene Zeichnung (SS=2-Fassung) bleiben noch: chikurin, inari, obakedera, hakaba, kurama, yukiyama, ryugu,
  uminobe, yomi, takamagahara.

# Erledigt (Runden 87–89): Balance der Synergie-Spitze
- Runde 87: Onmyōdō – Papierdiener (`_shiki`) laden das Pentagramm nicht nach (Kettenreaktion; 71 → 26 %).
  Oni-Rausch +45 % statt +60 %, ohne `dmgm` (73 → 44 %). Bericht `balance-check-87`.
- Runde 88: Feuerwerk – fünf Funken teilen eine Trefferliste, 0,8× Schaden (61 → 44 %). Fūjin-Raijin: Windsack alle
  1,5 s (57 → 33 %). Bericht `balance-check-88`. sigtest prüft Onmyōdō-Kette und Funken.
- Runde 89: Drachenkönig Seidenfaden 1,75× (51 → 27 %), Jingi `dmgm` 1,2 (81 → 77 %). Bericht `balance-check-89`.
- Muster bei allen Ausreißern: mehrere Teilgeschosse/Felder treffen denselben großen Boss. Bei neuen Sigs immer
  eine geteilte Trefferliste (`b.hit = seen`) oder ein Flag gegen Selbst-Aufladung vorsehen.
- Methode: `synbalance.py ... --leben`, Vergleich mit Synergie-fx entfernt (Items allein), dann Werte variieren.
  Achtung: 12 Seeds streuen stark (±5 Punkte), Effekte sind oft nicht linear.

# Erledigt (Runden 90–92): Balance Spitze und unteres Ende
- Runde 90: Orochi-Kusanagi Vergiftete 1,2× ohne dmgm (50 → 40 %), Izanagis Flucht Rollen-Pfirsiche 150 % (`_momo(mult)`;
  48 → 38 %). Jingi-Blitze: `run.lightning` trifft einmal, `_echo` blockt Folge-Sigs – keine Mehrfachauslösung.
- Runde 91: **Messfehler** – synbalance lief nur mit `--waffe=` an Nahkampf heran; jetzt nach `weapons.weapon_of(p)`.
  Nahkampf ist im `--leben`-Maß benachteiligt → Vergleich mit `--waffe=w_sword`/`w_fan`-Basis. Göttliches Arsenal:
  Speerstoß schießt Hachiman-Pfeil (Speer verdrängte den Bogen). Kranichschwarm: immer ≥ 2 Kraniche.
- Runde 92: Sturmfächer – jeder 3. Angriff ein Blitz; Großer Wind – weggewehte Geschosse als Windklinge zurück (`_tf`).
- Berichte `balance-check-90/91/92`. sigtest prüft Arsenal-Pfeil und Sturmfächer-Blitz.

# Erledigt (Runden 93–94): unteres Ende der Kampf-Synergien
- Waffen-Verdrängung geprüft: nur das Göttliche Arsenal kombiniert zwei Waffen-Items (seit 91 gelöst). Achtung bleibt bei
  Figuren mit Waffe (Kotaro-Fächer + Amaterasu-Laser → Laser verdrängt Fächer) – das ist allgemein, nicht synergiebezogen.
- Runde 93: Mondsichel-Klinge – bei 6 Blutungen reißt der nächste Bogen alles auf (300 %, ×0,87 → ×1,45);
  Mondschein-Teich – Bogen-Talismane +40 % gegen Gebremste (×0,73 → ×1,04). Bushi gegen Schwert-Basis ×1,63: ok.
- Runde 94: Mokumokuren – Auge ab Radius 4,5, +40 % (×0,72 → ×0,97); Kappa-Festmahl – Abpraller +50 % und bremsend
  (Boss unverändert ×0,72, weil kaum Abpraller; Sustain-Synergie).
- Messhinweis: Raum-Test mit 2 Zufalls-Items braucht schon 164 s → Zwei-Item-Synergien stoßen oft an die 180-s-Grenze.
  Ganzer `--raum`-Lauf dauert > 10 min, `--leben` nur 40 s.

# Erledigt (Runden 95–96)
- Runde 95: Figuren-Waffe hat Vorrang (`weapons._own`, `weapon_of`). Ein Waffen-Item wird per `weapons.bridge_of(p)` zum
  Zusatzangriff in `weapons.fire`: Laser → dünner Strahl 0,7×, Bogen → ein Pfeil 1,2×, Fächer → drei Windstöße 0,45×,
  Nahkampf-Item an Kotarōs Fächer → Klingenwelle 0,7×. Göttliches Arsenal schießt bei Benkei keinen zweiten Pfeil.
  waffentest prüft Kotarō+Amaterasu, Kenji+Yumi, Akago+Tengu-Fächer, Benkei+Arsenal. Balance der Brücken nicht gemessen.
- Fächer-Messung (`--leben`, Shuten-dōji): Talisman 10,4 %, Fächer 4,4 %, Schwert 4,5 % → der Fächer ist nicht
  eigens schwach, nur der allgemeine Nahkampf-Nachteil des Bots. Idee damit erledigt.
- Runde 96: Eigene Hi-Res-Wanddekos Chikurin (Taketori-Bambus mit Kaguya + neues Licht `('chikurin', 0)`, Ishidōrō),
  Inari (Torii vor Senbon-Torii-Gang, Steinfuchs mit Schlüssel), Obakedera (Ofuda, Yūrei-ga). Helfer `_niche`.
  Vorschau-Trick: Wand-Basis per `walls.wall_set(n)['h']` + `walldeco_hi.wall_decos_hi` mit PIL zusammensetzen.
  Ohne eigene Zeichnung bleiben: hakaba, kurama, yukiyama, ryugu, uminobe, yomi, takamagahara.

# Erledigt (Runden 97–98)
- Runde 97: unteres Ende aufgewertet (`--leben`, Shuten-dōji): Tsukumogami – jede Rolle wirft zwei Papierpuppen (in
  `sigs.on_dash`, ×0,89 → ×1,07); Hundert Augen – `e.sg_eyes` stapelt pro Treffer bis 6, +20 % + 6 %/Auge (×0,89 → ×1,05);
  Tsunami – Rückflut: Abpraller und Teilstücke (70 %) zielsuchend (×0,85 → ×0,99); Tengu-Flug – `g['tengu_f']` vier
  durchbohrende Federn 200 % nach der Rolle (×0,90 → ×1,09; reagiert stark nichtlinear). Bericht `balance-check-97`.
- Gesamtmessung danach: Spitze unverändert (Feuerwerk/Oni-Rausch/Hannya-Zorn ≈ 43–44 %, wie nach Runde 88). Unteres
  Ende sind nur Nutz-Synergien (Geld, Schlüssel, Sternschnuppen) und Nahkampf (gegen Schwert-Basis ok).
- Runde 98: Eigene Hi-Res-Wanddekos Hakaba (Sotoba + Higanbana, Jizō mit Kerze – Licht `('hakaba', 1)` jetzt (19, 8)),
  Kurama (Shimenawa, Hanadaka-Tengu-Maske), Yukiyama (Eiszapfen, Eishöhle mit Yuki-onna). Helfer `_higanbana`.
  Vorschau: Skript wie in Runde 96 (Wand-Basis + `wall_decos_hi`, ×6 vergrößert). Python braucht ggf.
  `pip install --ignore-installed pillow` (System-PIL ist kaputt).
  Ohne eigene Zeichnung bleiben: ryugu, uminobe, yomi, takamagahara.

# Nächster Schritt: Balance der Waffen-Brücken (Runde 95)
Warum: Seit Runde 95 wird ein Waffen-Item bei Figuren mit eigener Waffe zum Zusatzangriff – das betrifft jeden Lauf mit
Kenji, Benkei, Kotarō, Susanoo oder Akago, ist aber nie gemessen. `tools/synbalance.py` bekommt einen Schalter
`--figur=<id>` (statt fest 'hana'), dann je Figur mit/ohne Waffen-Item vergleichen (z. B. Kotarō + `w_laser`,
Kenji + `w_bow`). Ziel: das Item soll sich lohnen (≥ ×1,1 gegenüber zwei Zufalls-Items), aber nicht die Figur ersetzen.

# Weitere Ideen
- Hi-Res-Wanddekos Teil 4: ryugu (Korallentor, Otohime-Tamatebako), uminobe (Netz mit Glaskugeln, Funayūrei-Hände),
  yomi (Yomotsu-Steinblock, Ikazuchi), takamagahara (Wolkenpalast, Ame-no-Ukihashi)
- Nutz-Synergien (Fuchsgeld, Glückliches Haus, Wunsch, Shinsen) im Pausenmenü mit sichtbarem Zähler belohnen
- Shinkirō als Ereignis: eine Hamaguri spiegelt einen Trugladen vor
- Figurenbeschreibung im Auswahlmenü: Hinweis, dass Waffen-Items zum Zusatzangriff werden
- Spitze (Feuerwerk/Oni-Rausch/Hannya-Zorn ≈ ×4,2) mit `--raum` gegenprüfen, ob sie auch in Räumen dominieren
