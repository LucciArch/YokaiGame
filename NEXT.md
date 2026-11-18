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

# Erledigt (Runden 99–100)
- Runde 99: `tools/synbalance.py --figur=<id>` misst jedes Waffen-Item (+ Zufalls-Item) gegen zwei Zufalls-Items, mit
  Spalte „ohne“ (Brücke per `weapons.bridge_of = lambda p: None` abgeschaltet); dritter Positionsparameter filtert Items.
  Brücken bringen +0,1 … +1,1. Fächer-Brücke war zu schwach → 0,65× / 0,5 s. Bericht `balance-check-99-waffen-bruecken`.
  Kotarō bleibt insgesamt niedrig (Bot-Nachteil Nahkampf/Fächer). Messung dauert ~15 min pro Figur (5 parallel ok).
- Runde 100: Eigene Hi-Res-Wanddekos Ryūgū (Rundfenster mit Riemenfisch + neues Licht `('ryugu', 0)`, Tamatebako mit Rauch
  zwischen Edelkorallen) und Uminobe (Netz mit Ukidama, Funayūrei-Hände + Hishaku unter dem Totenlicht `('uminobe', 1)`).
  Vorschau-Skript wie Runde 96/98; `pip install --ignore-installed pillow` nötig.
  Ohne eigene Zeichnung bleiben: yomi, takamagahara.

# Erledigt (Runden 101–103)
- Runde 101: Eigene Hi-Res-Wanddekos Yomi (Chibiki-iwa mit Shimenawa/Shide und Shikome-Augen; Ikazuchi auf Izanamis
  Gebeinen, neues Licht `('yomi', 1)`) und Takamagahara (Wolkenpalast mit Chigi/Katsuogi, Tor-Licht bei (16, 8);
  Ame-no-Ukihashi mit Ame-no-Nuboko). **Jetzt haben alle Biome eigene Hi-Res-Wandbilder.**
- Runde 102: Ereignis `shinkiro` – Hamaguri (Bild `shinkai/rock_hi.png`[0]) haucht drei Items (Gruppe 'shinkiro') aus,
  nur das echte (`pd.mirage == False`) wirft einen Hi-Res-Schatten; 15 s (`room.extra['shinkiro_t']`). Trugbild-Items gehen
  zurück in `run.pool`. In `EVENT_KINDS`, `MATSURI_ROOMS`, Kartensymbol, Lexikon, `design/ereignisse.md`.
- Runde 103: Figurenwahl zeigt „Waffen-Items werden zum Zusatzangriff“; uiflow2 prüft Shinkirō und den Hinweis.
- Hinweis: Lokaler `main` im Container kann ein fremder alter Klon sein (keine gemeinsame Geschichte mit origin/main) –
  dann auf einem Zweig von `origin/main` arbeiten und mit `git push origin HEAD:main` pushen.

# Erledigt (Runden 104–105)
- Runde 104: `sigs._gain(p, key, n)` zählt in `st(p)['nutz']`, `sigs.nutz_lines(p)` liefert die Zeilen fürs Pausenmenü
  („Items & Werte“, unter „Fast komplett“): Fuchsgeld (Mon extra), Glückliches Haus (Krüge mehr), Wunsch erfüllt
  (Sternschnuppen), Shinsen (Schlüssel/Herzen), Kaufmann (aktueller Münz-Schaden), Totenfähre (x/40 Kills bzw. Münze bereit).
  uiflow2 prüft Text und Anzeige. Neue Nutz-Synergien dort eintragen.
- Runde 105: SFX `shinkiro` (Ausatmen) und `mirage` (Trugbild zerfließt / Muschel schließt) in `art_src/music/sfx.py`,
  gespielt in `run.py`. Neu bauen: `cd art_src/music && python3 sfx.py shinkiro mirage` (braucht scipy, ffmpeg).

# Erledigt (Runden 106–107, Wunsch von Luca: Spiel war zu leicht, Kostüme veraltet)
- Runde 106: `entities.flat_dmg` (Wurzel-Ertrag für flachen Schaden), `entities.stack_dmgm` (stärkster Multiplikator voll,
  weitere 40 %), steilere Gegner-/Boss-HP-Kurve, ganzes Herz ab Kapitel III, mehr Gegner/Champions, weniger Gratis-Items
  (Laden 2 Items, Schrein/Truhe/Mini-Boss/Dōjō/Geheimraum/2. Schatzkammer seltener). Bericht `balance-check-106-skalierung`.
  Messwerkzeug (nicht im Repo): Gott-Bot ohne Zusatzschaden, Bosskampfdauer je Ebene – Ziel: nicht unter ~15 s fallen.
  **Schwierigkeit bleibt Lucas Wunsch: neue Items/Synergien nicht stärker machen, ohne die Kurve nachzumessen.**
- Runde 107: Kostüme in `art_src/fable/items/costumes.py` neu (Kitsune, Ryū, Oni + Kanabō, Yūrei, Tanuki, Eboshi, Tokin).
  Bauen: `cd art_src/fable/items && PYTHONPATH=.. python3 costumes.py` (Pillow per `pip install --ignore-installed pillow`).
  Unveränderte PNGs danach zurücksetzen (Encoder schreibt neu). `costume.OWN` = Merkmale, die eine Figur schon trägt.

# Erledigt (Runden 108–109)
- Runde 108: `costumes.wings(ph, fam, fam2, tip)` – Krähenflügel aus Hand-/Arm-/Schirm- und zwei Reihen Deckfedern
  (Tengu), weiße Kranichflügel mit dunklen Schwungfeder-Spitzen (`fly_back`); `halo` ist jetzt ein Kaen-Kōhai
  (Goldreif mit Spiegelpunkten, züngelnde Flammen, unten offen). **Damit sind alle Kostümteile im neuen Stil.**
  Vorschau im Spiel: Skript mit `g.start_run(ch)`, `p.transforms[:] = [...]`, `g.window` ausschneiden.
- Runde 109: Shinkirō ab Tiefe 4 zu 35 % mit zwei echten Items (`pd.twin`); nach dem ersten bekommt das zweite
  `hearts = 1` (zählt nicht als Oni-Handel). uiflow2 prüft das.

# Erledigt (Runden 110–111)
- Runde 110: Endbildschirm (`App.st_over`) zeigt `sigs.nutz_lines(p)` in zwei Spalten unter der Statistik; uiflow2 prüft das.
- Runde 111: Ereignis `mochitsuki` (Tsukimi): Obj `usagi` (Hi-Res `objects_hi.usagi(f)`, 3 Bilder → `_shared/usagi_hi.png`,
  nur diese Datei schreiben), Logik `yomeiri.mochitsuki_start/update`, Wendezone `mochi_zone(o)` links vom Usu. Takt
  `per = 1,3 − 0,07·n`, Fenster 0,25–0,75, Schlag bei 1,0 trifft, wer noch am Usu steht. 5–6 gewendet: +1 Herz, 3–4: 1 Herz,
  2: ½ Herz. Erfolg `mochitsuki` („Aitori“), Lexikon, Minikarten-Symbol, `EVENT_KINDS` (Festtagsgast zählt jetzt alle).
  Achtung: `rooms.py` zieht eine Zufallszahl mehr → Karten zu festen Seeds haben sich verschoben.

# Erledigt (Runden 112–113, Wunsch von Luca: viele Unlockables wie in Isaac)
- Runde 112: **Figuren-Siegel** – `data.MARKS` (boss3, sieg, himmel, oku, oni) und `data.CHAR_UNLOCKS[figur][siegel] = item`
  erzeugen automatisch Erfolge `m_<figur>_<siegel>` mit Item-Belohnung. `Run.mark(m)` (nicht in Prüfungen) wird bei
  Bosssieg Tiefe 3/6 und beim Laufsieg (sieg, oku bei Tiefe 7, oni im Oni-Modus) aufgerufen. Charakterwahl zeigt
  „Siegel x / y“ mit Item-Namen (nur Siegel, die schon ein Item haben). Codex nennt bei gesperrten Items die Bedingung.
  Welle 1 (boss3): haraegushi, zanshin_tsuba, kuzu_blatt, bunbuku_kessel, tausendstes_schwert, neunter_teller,
  tengu_tsubute, taizan_fukun, ibaraki_arm, yashiori_sake.
- Runde 113: Welle 2 (sieg): hi_ogi, muramasa, fuchs_trugbild, shigaraki_tanuki, tachi_ojo, tsurube, kakuremino,
  hoki_naiden, masakari, habakiri. Wurf-Fähigkeiten in `sigs._siegel_fire`, Zeit-Fähigkeiten in `sigs._siegel_tick`.
- Symbole: `art_src/fable/items/icons_v16.py` (kopiert selbst nach `yokai/assets/items/icons`), Aufruf
  `cd art_src/fable/items && PYTHONPATH=.. python3 icons_v16.py vorschau.png`. sigtest prüft mehrere Siegel-Fähigkeiten.
- Fix: grabende Gegner (Isonade) steckten unter Felsen fest → Raum unlösbar (bot.py 2 hing auf Ebene 4).

# Erledigt (Runden 114–115): Figuren-Siegel Wellen 3–4
- Runde 114 (himmel): tamagushi, kesagiri, hoshi_tama, tanuki_bayashi, gojo_giboshi, ido_kagami, sojobo_hane,
  juni_shinsho, setsubun_mame, murakumo. Neuer Helfer `sigs._blast(run, x, y, rad, dmg, col, push)` für Rundumwellen.
- Runde 115 (oku): kotodama, tsubame_gaeshi, shinoda_blatt, tanuki_tokkuri, nanatsu_dogu, zehnter_teller, hanadaka_men,
  kikyo_mon, oni_tsuno, kushinada_kushi. Symbole in `icons_v16.py` (NAMES ergänzen), sigtest prüft je 5 pro Welle.
- Balance nicht gemessen (alle Werte bewusst moderat, Stufe 3). Item-Ideen hatten Namenskonflikte: `hara_tsuzumi` ist
  schon eine Synergie – vor neuen Sig-Namen `grep -n "'name'" yokai/sigs.py yokai/data.py`.

# Erledigt (Runden 116–118)
- Runde 116: Figuren-Siegel Welle 5 (Oni-Modus) – onusa, ichi_no_tachi, kitsune_chochin, tanuki_kesa (`sigs.jizo` in
  `Player.hurt`), kanjincho (Rabatt in `Run` Laden-Aufbau), okiku_ido, ushiwaka_fue, seimei_ido, kodomo_kanabo, ohabari.
  Jede Figur hat jetzt 5 Siegel-Items (50 insgesamt).
- Runde 117: Meister-Siegel – `Run.check_meister()` vergibt `meister_<figur>`; Läufe starten dann mit einem zufälligen
  eigenen Siegel-Item (nicht Prüfung/Tageslauf). Charakterwahl zeigt „Meister“.
- Runde 118: eigener Klang `kine` (art_src/music/sfx.py, 2 Varianten) für den Kine-Schlag beim Mochitsuki.

# Erledigt (Runden 119–120): Prüfungen mit Item-Belohnung
- Runde 119: Alle Prüfungen geben ein Item (`ACHIEVEMENTS` 'ch_<id>' → ('item', …)): fuurin, abura_age, tsukikage,
  hayate_waraji, senryo_bako, keppan (Zähler `sg['pakt']` in `Run` beim Oni-Handel), miidera_kane, nademono (in
  `sigs.block`), kongozue. Symbole `art_src/fable/items/icons_v17.py` (gleiches Muster wie v16). `Run.__init__` vergibt
  Item-Belohnungen schon erreichter Erfolge rückwirkend. Prüfungsmenü zeigt „Belohnung: …“ (uiflow2 prüft das).
- Runde 120: Prüfung `verbannung` (Susanoo, `spirit_only`, nur Geisterherzen) mit Belohnung `aokusa_mino` (sig `mino`).
  Jede Figur hat jetzt eine Prüfung (10). Menüzeilen 24 px statt 26 – für eine 11. Prüfung muss das Menü scrollen.
- Balance der neuen Items nicht gemessen (moderat gewählt, Stufe 3).

# Erledigt (Runden 121–122): Quests mit aktiven Items
- Neue Belohnungsart `('active', id)` in `ACHIEVEMENTS`; `ACTIVES[...]['locked']=True` hält ein aktives Item aus
  `Run.active_pool`, bis der Erfolg da ist (Freischaltung landet in `save['items']`). validate prüft das.
- q_mochi (3× Mochitsuki mit ≥5 Teigen, `stats['mochi_good']`) → `mondkine` (Schlag r 80 + Betäubung);
  q_nohit5 (`stats['nohit_bosses']` ≥ 5) → `shiomitsu_tama` (Geschosse weg, Treffer + Verlangsamung im ganzen Raum);
  q_feste4 (4 verschiedene Ereignisse in einem Lauf, `p.sg['feste_lauf']`) → `matsuri_uchiwa` (5 Hanabi mit Brand);
  q_pruefungen (alle Prüfungen, geprüft in `check_meister`, auch rückwirkend) → `totsuka` (Schnitt auf alle Feinde).
- Symbole: `art_src/fable/items/icons_v18.py` (Muster wie v17). sigtest prüft Sperre, Freischaltung und Wirkung.
- Balance nicht gemessen (Ladungen 3/4/3/5, moderat).

# Erledigt (Runden 123–125)
- Runde 123: Codex zeigt aktive Items hinten im Item-Raster (`ids = ITEM_IDS + ['active:'+a]`, Kupferrahmen, Ladung);
  gesperrte Quest-Aktive nennen ihren Erfolg. Aktive Items haben keine eigene Entdeckung (alle offen sichtbar).
- Runde 124: `bosstest.py` nutzt einen eigenen leeren Spielstand (tempfile) – Amaterasu-Assert besteht wieder.
- Runde 125: Quest `q_geheim3` (3 Geheimräume in einem Lauf, `p.sg['geheim_lauf']` in `Run.reveal_near`) →
  `mayoiga_wan` (Ebene aufdecken + 2 Gaben). Fix: Quest-Aktive hatten `icon='hammer'/'orb'/…` statt ihrer eigenen PNGs.
  **Neue aktive Items: `icon` = eigene ID, Symbol in `icons_v18.py` (NAMES ergänzen).**

# Erledigt (Runden 126–127)
- Runde 126: Quests `q_kami50` (Stat `kami_deals` ≥ 50, Prüfung im Kami-Schrein-Zweig von `Run.collect`) → `nusa`
  (Fluch bannen, Geschosse löschen, ½ Geisterherz, 3 s iframes) und `q_loop3` (`go_deeper`, `self.loop >= 2`) →
  `yatagarasu_feder` (`p.temp` 8 s homing+pierce). Symbole in `icons_v18.py`. sigtest prüft Auslöser und Wirkung.
- Runde 127: Synergie `henro` (kongozue + senbazuru): `on_floor` +2 Kraniche, Geisterherz jede 2. statt 3. Ebene,
  Zähler in `nutz_lines`.

# Erledigt (Runden 128–130)
- Runde 128: `synbalance.py <boss> <tiefe> <ids> --items --leben` misst Einzel-Items (Item + Zufalls-Item gegen zwei
  Zufalls-Items, 12 Seeds, ~80 s für 60 Items). Alle Siegel-/Prüfungs-Items gemessen: nur Habakiri war Ausreißer (×3,04,
  4 % Max-HP auch bei Bossen) → Bosse 1 % (×1,42). Quest-Aktive pro Ladung im Rahmen. Bericht `balance-check-128`.
- Runde 129: Synergie `misogi` (onusa + kiyome_sack): Salz macht alle Feindgeschosse im Raum zu Shide (bis 12, 60 %),
  Ōnusa-Rolle 90 px / bis 8. Helfer `sigs._shide(p, run, rad, n, mult)`.
- Runde 130: Yatagarasu-Feder-Symbol mit breiterer Fahne.

# Erledigt (Runden 131–132)
- Runde 131: Meister-Läufe `Run.boss_mult = 1.15` (Boss-HP, in `RUN_KEYS`). Messung: Startitem kürzte Bosskämpfe
  auf Ebene 4–6 um ~25–50 %.
- Runde 132: Kapitel IV–V Boss-HP × `1 + 0,25·(tier−3)` in `bosses.Boss.__init__`; Ebene 7–10 jetzt 9–14 s statt
  7–12 s. Bericht `design/balance/balance-check-131-meister.md`. Messskript: Bot mit `dmg=1`, `Run.update`
  umwickeln und Zeit im Bossraum mit lebenden Gegnern je `floor_no` summieren (~4 min für 8 Läufe).

# Erledigt (Runden 133–134): Synergien für Belohnungs-Items
- Runde 133: `kagura` (hi_ogi + uzume_suzu, sig `kagura`): Suzu alle 2,5 s, im Tanz (4 s ohne Treffer) 6 Sakaki-Blätter
  50 % aus `sigs._suzu` (×1,28). `sarayashiki` (neunter_teller + zehnter_teller, sig `okiku`): zehnter Teller jeden
  9. Kill und nach Okikus Klage um die Spielerin, Helfer `sigs._teller` (×1,38).
- Runde 134: `gojo_ohashi` (gojo_giboshi + ushiwaka_fue, sig `gojo_bashi`): Flötenton jeden 4. Wurf, Treffer → Naginata-
  `_blast` 80 % am Ziel, alle 1,5 s (in `hit_post`; erst ×2,06 mit 120 %/1 s, gedämpft auf ×1,55).
- Messung jeweils `synbalance.py shuten_doji 5 <id> --leben` (Iwato ×1,45 als Vergleich).

# Erledigt (Runden 135–137): Synergien für Belohnungs-Items Teil 2
- Runde 135: `orochi_taiji` (habakiri + yashiori_sake, sig `yamata_giri`): Habakiri gegen Berauschte schon beim 6. Treffer,
  Schnitt berauscht gewöhnliche Feinde (nur +25 %, ohne Bremse – mit Bremse ×3,2→ höher). ×3,2 gegen ×2,2 nur Items.
  Achtung: Der Habakiri-Schnitt ruft `damage_enemy` → `hit_post` erneut auf und zählt selbst als Treffer (alt).
- Runde 136: `seimei_jinja` (kikyo_mon + seimei_ido, sig `kikyo_ido`): Pentagramm-Schluss → `_blast` 60 % mit
  `run._echo = True` (sonst laden Nachbar-Pentagramme), Geisterherz-Chance 40 %. ×1,72 (Items ×1,67).
- Runde 137: `ido_no_yurei` (okiku_ido + tsurube, sig `ido_reikon`): Brunnenwasser trifft alle Feinde 25 % je Geisterherz,
  ½ Geisterherz jeden 2. Raum. ×1,42 (Raum-Synergie, Bossmaß wenig aussagekräftig).

# Erledigt (Runden 138–140): Synergien für Belohnungs-Items Teil 3
- Runde 138: `shikigami_tsukai` (hoki_naiden + juni_shinsho, sig `juni_tori`): Jūni-Shinshō jeden 8. statt 12. Wurf,
  als verfolgende Papiervögel (1,5× Flugzeit). ×1,40 gegen ×0,94 nur Items.
- Runde 139: `yakumo_tatsu` (murakumo + kushinada_kushi, sig `yakumo`): Wolke blitzt je Kamm-Stufe 10 % öfter, ab 4 Stufen
  `_chain_strikes` auf einen zweiten Feind (60 %). Bosstest hat keine Kamm-Stufen → gemessen mit `kushi` fest auf 8
  (vorübergehendes sed): ×1,75 gegen ×1,34.
- Runde 140: `koishikuba` (kuzu_blatt + shinoda_blatt, sig `koishikuba`): Fuchsnebel jeden Raum (auch nach Treffern),
  Nicht-Bosse brennen 3 s (30 %). `synbalance --raum` misst das nicht (Wellen kommen nach `on_room_enter`, beide 180 s).

# Erledigt (Runden 141–143): Synergien für Belohnungs-Items Teil 4
- Runde 141: `yoto_muramasa` (muramasa + kesagiri, sig `yoto`): im Blutdurst (`g['bd_t']`) Kesa-giri jeden 2. Wurf, rot, 150 %. ×1,18.
- Runde 142: `ganryujima` (tsubame_gaeshi + ichi_no_tachi, sig `ganryu`): `g['ichi']` lädt in `tick` nach 8 s neu
  (`g['ichi_t']`), danach zwei Schwalbenschnitte (100 %). ×1,09.
- Runde 143: `senbon_gari` (tausendstes_schwert + nanatsu_dogu, sig `senbon`): Waffe jeden 5. Wurf, Treffer mit `fl['senbon']`
  zählen über `sigs._jagd` für die Schwertjagd. ×0,99 im Bosstest (wächst über den Lauf, Bossmaß sieht das nicht).

# Erledigt (Runden 144–146): Synergien für Belohnungs-Items Teil 5
- Runde 144: `tamagushi_hoten` (tamagushi + kotodama, sig `hoten`): Norito jeden 12. Wurf, bis zu 8 vergehende
  Feindgeschosse → Sakaki-Blätter (60 %). ×1,37.
- Runde 145: `ataka_no_seki` (tachi_ojo + kanjincho, sig `ataka`): Tachi-ōjō bei ≤1 Herz, 4 s, Yokai erstarren 2 s
  (Bosse 0,5 s). ×1,21.
- Runde 146: `shojoji_utage` (tanuki_bayashi + tanuki_tokkuri, sig `utage`): Trommelschläge zählen 2 für den Tokkuri
  (Helfer `sigs._schluck`), im Sake-Rausch Trommel auch im Gehen, 200 %/70 px. ×1,02 – Bosstest-Bot steht nie still
  und sammelt keine Münzen, misst die Synergie also nicht.
- Testumgebung: `pip install pygame-ce numpy` (ohne numpy stürzen uiflow2/bot ab).

# Erledigt (Runden 147–149): Synergien für Belohnungs-Items Teil 6
- Runde 147: `kintaro` (masakari + kodomo_kanabo, sig `kintaro`): Axt-Geschosse tragen `fl['axt']`, Treffer zählen 4 für
  `g['kk']` (jetzt Zähler ≥ 8 + Reset statt `% 8`), Keulenschlag 55 px. ×1,46.
- Runde 148: `kurama_lehre` (sojobo_hane + hanadaka_men, sig `kurama`): Rollen-Wirbel 65 px, je verwehtem Feindgeschoss
  +1 Windklinge (`g['hd']`, max +3). ×1,36.
- Runde 149: `rashomon` (ibaraki_arm + oni_tsuno, sig `rashomon`): Oni-Arm alle 2 s, unter 2 Herzen jede Sekunde mit 250 %. ×1,40.

# Erledigt (Runden 150–152): Synergien für Belohnungs-Items Teil 7
- Runde 150: `mamemaki` (setsubun_mame + oni_tsuno, sig `mamemaki`): Bohnen jeden 2. Wurf, 4 statt 3, Flucht 2 s. ×1,22
  (erster Versuch mit 5 Bohnen ×1,77 – zu stark).
- Runde 151: `kitsunebi_gyoretsu` (hoshi_tama + kitsune_chochin, sig `gyoretsu`): Fuchsfeuer-Ring doppelt so oft,
  Flammen zielsuchend, Lebensdauer 1,5 s. Bosstest ×0,83 (keine Kills), `--raum` ×1,10.
- Runde 152: `morinji` (bunbuku_kessel + shigaraki_tanuki, sig `morinji`): Rolle → 3 s Glückssträhne (`g['gold_t']`),
  Kessel 1,2 s. ×1,12.
- Testumgebung: `python -m pip install pygame-ce numpy` (das nackte `pip` zeigt auf ein anderes Python).

# Erledigt (Runden 153–155): Synergien für Siegel-Items Teil 8
- Runde 153: `kotaro` (tengu_tsubute + kakuremino, sig `kotaro`): unsichtbar Steine alle 1,5 s mit 200 %.
  Neu: `synbalance --still` (Bot steht, wirft 2 s ja/2 s nein). Gegen Shuten-dōji schafft der stehende Bot nichts →
  `synbalance x 2 kotaro --still --raum`: ×0,69 gegen ×0,99 nur Items. `utage` dort ×0,41 (Trommel wirkt im Stand stark).
- Runde 154: `oharae` (haraegushi + onusa, sig `oharae`): Rolle schwingt alle 4 s den Haraegushi (8 %, Bosse 200 % Schaden
  statt Prozent – 2 % Bossleben war ×3,2). ×1,41 gegen ×1,18.
- Runde 155: `totsuka` (habakiri + ohabari, sig `totsuka`): Habakiri-Schnitt → Blitz aufs Ziel + Kette auf 3 (je 100 %).
  Boss (kappa_ou 2) ≈ neutral, `--raum` Tiefe 3 ×0,58.
- Hinweis: `synbalance --leben` ist bei Shuten-dōji Tiefe 5 sehr verrauscht (Bot stirbt nach 3 Treffern, ~4 % Schaden);
  für Treffer-Effekte besser `kappa_ou 2` ohne --leben gegenprüfen.

# Erledigt (Runden 156–158): Synergien für Siegel-Items Teil 9
- Runde 156: `ichigeki` (zanshin_tsuba + ichi_no_tachi, sig `ichigeki`): erster Hieb → Zanshin 3 Stufen, Fenster 3 s
  (`sigs._zs_win`). kappa_ou 2 ×0,64 gegen ×0,65 nur Items, --raum ×1,04 gegen ×1,07 (eher Würze als Kraft).
- Runde 157: `mizukagami` (ido_kagami + okiku_ido, sig `mizukagami`): Spiegel fängt bis 3 Geschosse, Umkreis 70, Rückwurf bremst.
  ×0,59 gegen ×0,69, --raum ×0,92 gegen ×1,07.
- Runde 158: `kage_kitsune` (fuchs_trugbild + kuzu_blatt, sig `kage_kitsune`): Trugbild 4,5 s, wirft brennend mit 70 %.
  Boss ≈ neutral (verrauscht), --raum ×0,62 gegen ×0,74.
- Messung „nur Items“: Wrapper, der vor `runpy` von synbalance die `fx` der Synergie leert (dann gleiche Seeds/Baseline).
  Achtung: shuten_doji Tiefe 5 läuft für Siegel-Paare oft bis 180 s → nutzlos, besser kappa_ou 2.

# Erledigt (Runden 159–161): Synergien für Siegel-Items Teil 10
- Runde 159: `hoshi_danuki` (tanuki_kesa + tanuki_tokkuri, sig `hoshi_danuki`): Jizō-Abpraller → Sake 4 s; der nächste
  Schluck macht den Jizō im Raum wieder bereit (`g['hd_jz']` 0→1→2, einmal pro Raum). Boss/--raum neutral (Gott-Modus-Bot).
- Runde 160: `shanao` (ushiwaka_fue + sojobo_hane, sig `shanao`): Rollen-Wirbel verwirrt Yokai 2 s, Flötenton jeder 4. Wurf.
  Boss neutral, --raum ×1,20 gegen ×1,13 (Kontrolle, kein Tempo).
- Runde 161: `taizan_sai` (taizan_fukun + kikyo_mon, sig `taizan_sai`): Pentagramm nach 4 Treffern; nach dem Ritual
  tilgen 12 Pentagramme Malus + `taizan_used`. kappa_ou 2 ×0,37 gegen ×0,50, --raum ×0,81 gegen ×0,94.
- Fix: Kikyō-Pentagramm-Schaden lief ohne `run._echo` und zählte selbst fürs nächste Pentagramm (effektiv jeder 4. statt 5.).
  Kikyō-Mon und Seimei-Jinja sind dadurch etwas schwächer – beim nächsten Messen beobachten.

# Erledigt (Runden 162–164): Synergien für Siegel-Items Teil 11 – alle Siegel-Items haben jetzt eine
- Runde 162: `sakaki_mai` (hi_ogi + tamagushi, sig `sakaki_mai`): Tanz-Blätter bremsen (`slow`), Tamagushi heilt jeden
  2. statt 3. Raum ohne Treffer. Bewusst Kontrolle/Komfort (Hi-ōgi schon ×1,53): kappa_ou 2 ×0,63 gegen ×0,59 nur Items.
- Runde 163: `koromogawa` (gojo_giboshi + tachi_ojo, sig `koromogawa`): Naginata 75 px; während Tachi-ōjō jede Sekunde
  150 % (`g['kg_t']`). kappa_ou 2 ×0,62 gegen ×0,63, --leben ×1,64 gegen ×1,64 (Boss stirbt so oder so – gesättigt).
- Runde 164: `ichigeki` verstärkt – Kill durch den ersten Hieb lädt ihn neu. --raum kappa_ou 3 ×1,04 gegen ×1,07
  (Messung zeigt kaum Wirkung; der Bot trifft mit dem ersten Hieb selten einen tödlichen Treffer).
- „Nur Items“-Wrapper liegt nicht im Repo: Skript, das `data.SYNERGIES[..]['fx'] = {}` für die IDs setzt und dann
  `runpy.run_path('tools/synbalance.py')` aufruft.

# Erledigt (Runden 165–166)
- Runde 165: `synbalance.py ... --nur-items` misst jede Synergie zusätzlich mit leerem `fx` (Spalte „nur Items ×…“) –
  ersetzt den Hand-Wrapper. Kikyō-Mon nach dem Fix: kappa_ou 2 `--items` ×0,63 (Masakari/Hi-ōgi ×0,59, Habakiri ×0,64,
  Hoki Naiden ×0,71) → kein Nachbessern.
- Runde 166: Jūni-Shinshō war mit ×0,87 das schwächste Siegel-Item (radialer Ring, kaum Treffer am Boss). Jetzt
  umzingeln die 12 Talismane den nächsten Feind (Radius 60, nach innen, je 50 %, gestaffelt `delay`) → ×0,69.
  Ohne Feind und bei Shikigami-Tsukai (`juni_tori`) bleibt der alte Ring.

- Messung aller 50 Siegel-Items (kappa_ou 2 `--items`, nach Runde 166): Kampf-Items ×0,59 (Masakari) bis ×0,85
  (Ido-Kagami). Bei ×1,03 liegen Schutz-/Raum-/Münz-Items (Tamagushi, Tachi-ōjō, Tsurube, Kesa …) – Bossmaß sieht sie nicht.
  Grenzfälle ×0,91–0,99 mit Kampfanteil: zanshin_tsuba, yashiori_sake, kakuremino, onusa, hoshi_tama, kuzu_blatt,
  ushiwaka_fue, oni_tsuno, tausendstes_schwert, bunbuku_kessel, ichi_no_tachi.

# Erledigt (Runden 167–168)
- Runde 167: `--raum`-Gegenmessung (kappa_ou 3) der elf Grenzfälle: onusa/zanshin/kuzu/bunbuku ×0,92–0,95 (im Feld);
  hoshi_tama ×0,99, ichi/tausendstes/yashiori/oni_tsuno/fue/kakuremino ×1,02–1,07. Gestärkt: Schwertjagd jeden 20.
  statt 30. Kill, Hoshi no Tama 15 % statt 10 % (→ ×0,98). Fue-Verwirrung 3 s getestet → ×1,09 (schlechter, Rauschen
  ±0,05; Verwirrung lässt Feinde wegtorkeln) → zurück auf 2 s. Kakuremino (Stillstand), Oni-Horn (<2 Herzen),
  Yashiori (Boss/Champion), Ichi-no-tachi (Raumwechsel) zeigt das Raummaß systembedingt nicht.
- Runde 168: Codex speichert aktive Items als `'active:<id>'` in `save['seen']` (Aufheben, Start-Item der Figur);
  unentdeckte zeigen „?“, Sockel zeigt „Neu!“, Zähler/Statistik zählen aktive Items mit. uiflow2 prüft beides.

# Erledigt (Runden 169–170)
- Runde 169: Ushiwakas Flötenton (jeder 6. Wurf) +50 % Schaden und `pierce` → kappa_ou 3 `--items` ×0,98 → ×0,87,
  `--raum` ×1,05 → ×0,92. sigtest (Gojō-Ōhashi) prüft pierce und dmg 1,5.
- Runde 170: `synbalance --raum` ruft je Welle `sigs.on_room_enter` (Welle = neuer Raum; ältere --raum-Zahlen sind
  damit nicht 1:1 vergleichbar). Ichi-no-tachi blieb so bei ×1,03 → neu: erster Treffer je Feind +50 % (`e.sg_ichi`)
  → `--raum` ×0,92, Boss ×0,85. sigtest-Schwelle auf 35.

# Erledigt (Runden 171–173)
- Runde 171: Tsukumogami Teil 1 – `biwa_bokuboku`, `chochin_obake`, `bake_zori`, `ittan_momen`, `kosode_te` (Pool T,
  nicht gesperrt, Symbole `art_src/fable/items/icons_v19.py`). kappa_ou 2 `--items`: Biwa ×0,65, Kosode ×0,75,
  Chōchin ×0,80, Ittan ×0,89, Bake-zōri ×0,97 (wirkt bei Kills – Bossmaß sieht das kaum; ggf. `--raum` messen).
  Achtung: Item-ID `karakasa` ist vergeben (alter Schirm), deshalb kein Kasa-obake-Item.
- Runde 172: Synergien `hoichi` (Biwa + Juzu), `furisode_kaji` (Kosode + Chōchin-obake), `dogu_yagyo` (Bake-zōri + Ittan).
- Runde 173 (Wunsch von Luca: Story-Progression wie Isaac): `yokai/story.py` – 8 Kapitel mit Bedingung auf dem
  Spielstand (`save['story_seen']`), prozedural gezeichnete Szenen (`draw_scene`), `Cutscene`, Story-Baum
  (`draw_tree`, Menü „Geschichte“, `App.st_storytree`/`st_scene`/`play_story`). Neue Kapitel spielen auf dem Titel,
  sobald `pending()` etwas meldet (nach Läufen); Prolog beim ersten „Neuer Lauf“. uiflow2 prüft alles.
  Bestehendes Gating (schon vorher da): erster Sieg nur bis Kapitel V, danach Himmel (VI), nach wahrem Sieg Yomi/Iwato (VII).

# Wartet auf Luca: KI-Videos für die Zwischensequenzen
In dieser Sitzung gab es kein Video-Werkzeug. Vorgeschlagen (Plugin-Verzeichnis, eigenes Konto/Guthaben nötig):
„Cinematic AI Video Maker“, „AI Video & Image Generator by Clipwave“, „AI Video Editor & Timeline“ (ManyMotions).
Sobald eines aktiv ist (`ListPlugins` prüfen): je Kapitel (Szenen-Schlüssel in `story.CHAPTERS`: mond, morgen, stern,
yomi, sonne, feuer, siegel, schatten, shiramine) ein Video erzeugen, als MP4 nach `yokai/assets/story/<szene>.mp4`, Wiedergabe
in `Cutscene.frame` (pygame kann kein MP4 → z. B. beim Build in JPG-Einzelbilder zerlegen oder `imageio`/`cv2`;
Größe im PyInstaller-Build beachten). Abweichung von „alles selbst erzeugt“ nur hierfür – Lucas ausdrücklicher Wunsch.
Ohne Video-Werkzeug NICHT wieder selbst Szenen malen.

# Erledigt (Runden 174–175): Story Teil 2 – geheimer Boss Sutoku-in, Kapitel VIII Shiramine
- Runde 174: `bosses.Sutoku` (3 Phasen: Blut-Sutren-Spalten rechts→links, Umkehr-Fluch, Tengu-Federn; Phase 2 Krähen-Tengu,
  Federsturm, Groll-Feuer; Phase 3 `extra_dark`, Sutren-Spirale). Sprite `art_src/fable/bosses_3/boss_sutoku.py`
  (`PYTHONPATH=.. python3 boss_sutoku.py`, dann `python3 ../../import_fable.py .` in bosses_3 – danach die anderen
  Boss-PNGs per `git checkout` zurücksetzen, sie werden nur neu kodiert). bosstest: ~41 Treffer (Amaterasu ~21, Izanami ~52).
- Runde 175: Biom `shiramine` (depth 8; Palette in `environment/biomes.py`, Requisiten in `props.rocks`, gebaut mit
  `build.py shiramine` + `hi.py`, Ordner nach `yokai/assets/env/shiramine` kopiert). Pforte `Obj('shiramine')` im Bossraum
  von Kapitel VII, nur wenn `story.unlocked(save, 'schatten')` und keine Prüfung. Sieg: `stats.sutoku_wins`, Erfolg `sutoku`
  (noch ohne Belohnung), `epilogue.STORY_SHIRAMINE`, Kapitel `wahres_ende` im Story-Baum (Szene `shiramine`, Platzhalter).
  bosstest prüft die Pforte („Shiramine-Pforte OK“).

# Erledigt (Runden 176–178): Belohnung + Feinschliff für Sutoku-in
- Runde 176: Item `sutoku_sutra` (Blut-Sutra, Pool B, sig `blutsutra`): jeder 7. Wurf bekommt Bahn-Tag `sutra` (in `fl['sg']`),
  `bullet_tick` kehrt ihn nach 0,6 s um (×1,5, `hit` geleert, durchbohrend). Belohnung über `BOSS_REWARD['sutoku']` und
  Erfolg `sutoku`. Symbol `art_src/fable/items/icons_v20.py`. sigtest + bosstest prüfen.
- Runde 177: Bossmusik `tracks.sutoku` (`python3 tracks.py sutoku` in art_src/music; .wav danach löschen), `audio.track_for`
  Seed 166; validate prüft die Zuordnung.
- Runde 178: Titelstimmung `sutoku` in `App.draw_night` (Blutmond, `BRANCH['sutoku']`, Krähenzug); uiflow2 zeichnet sie.

# Erledigt (Runden 179–180)
- Runde 179: Wanddekos Shiramine – Low-Res-Zweig in `props.wall_decos`, Hi-Res `walldeco_hi.shiramine_hi` (Blut-Sutren mit
  Krähen-Tengu / Gorintō mit Groll-Feuer), `WALL_LIGHT[('shiramine', 1)]`. Gebaut mit `build.py shiramine` (wall_deco.png
  nach yokai/assets kopieren) + `hi.py`. Damit haben alle Biome eigene Hi-Res-Wanddekos.
- Runde 180: Synergie `daitengu` (Blut-Sutra + Tengu-Maske, sig `daitengu`): beim Wenden in `bullet_tick` drei durchbohrende
  Federn (je 60 % des gewendeten Schadens). sigtest prüft. **synbalance ungemessen**: `synbalance.py shuten_doji 5 …` läuft
  bei allen Kämpfen in den 180-s-Deckel (auch Zufall) – andere Boss/Tiefe suchen, bei der die Baseline unter 180 s bleibt.

# Erledigt (Runde 181)
- Runde 181: `bosses.Masakado` (Sprite `art_src/fable/bosses_3/boss_masakado.py`, Onibi-Farbfamilie `u0–u3`; Import wie bei
  Sutoku, danach die anderen Boss-PNGs per `git checkout` zurücksetzen). Phase 1 Reiterpfeile/Yabusame/Sturmangriff,
  Phase 2 (65 %) fliegendes Haupt: Onibi-Bogen, Zähneknirschen-Kiefer; Phase 3 (30 %) `decoys`: sechs Kagemusha ohne Schatten
  und ohne Treffer-Aufblitzen (in `draw` nach `super().draw` geblittet), alle 4 s `shuffle()`. `hitboxes` nur am Haupt.
  `BOSSES['masakado']` hp 2600, `BOSS_REWARD['masakado'] = None`, Lexikon-Eintrag. bosstest: ~37 Treffer (Sutoku ~41).
  **Noch nicht erreichbar** – keine Pforte, kein Biom.

# Erledigt (Runden 182–184): Kapitel IX Kubizuka
- Runde 182: Biom `kubizuka` (depth 9; Palette `environment/biomes.py`, Requisiten in `props.rocks` – Onibi-Steinlaterne,
  Itabi-Grabstein, Steinfrösche; Wanddekos in `props.wall_decos` – Sotoba, Froschnische; Hi-Res nur hochskaliert über
  `walldeco_hi`-Fallback). Pforte `Obj('kubizuka')` im Shiramine-Bossraum, wenn `stats.sutoku_wins` ≥ 1. Sieg: `masakado_wins`,
  Erfolg `masakado`, `STORY_KUBIZUKA`, Story-Knoten `kubizuka` (rechts neben `wahres_ende`). bosstest „Kubizuka-Pforte OK“.
- Runde 183: Bossmusik `tracks.masakado`; Biom-Musikseed 50 (Boss-Seed 159; 168 war schon Tsukiyomi). validate prüft.
- Runde 184: Item `masakado_kage` (Kagemusha, Pool B, hp+1, sig `kagemusha` in `sigs.block`: jedes 7. treffende Geschoss →
  sieben suchende Onibi je 80 %). Symbol `art_src/fable/items/icons_v21.py`. sigtest + bosstest prüfen.

# Nächster Schritt: Feinschliff Kubizuka
Warum: Kapitel IX ist spielbar, aber noch nicht so eigen wie Shiramine.
1. Hi-Res-Wanddeko `walldeco_hi.kubizuka_hi` (Sotoba mit Bonji-Schrift, Froschnische mit Onibi) + `WALL_LIGHT` prüfen;
   gebaut mit `hi.py` (setzt alle Biome neu, ist deterministisch).
2. Titelstimmung `masakado` in `App.draw_night` (wie `sutoku` in Runde 178: bleicher Mond, Onibi, fliegendes Haupt am Himmel).
3. Synergie mit Kagemusha (z. B. `masakado_kage` + `sutoku_sutra` = „Drei große Onryō“ Teil 1, oder + Yabusame-/Bogen-Item).
4. Masakado-Balance beobachten (bosstest ~16 Treffer, 44 s – deutlich leichter als Sutoku mit ~74 Treffern).

# Danach (Story)
- Danach Sugawara no Michizane (Raijin-Onryō, Blitze, Pflaumenblüten) als dritter großer Onryō
- Je Figur ein eigenes Story-Kapitel (`ENDINGS` in `epilogue.py` als Knoten im Baum, Bedingung `char_wins`)
- Iwato erst nach Yomi öffnen (strengerer Pfad wie Isaac), oder Kapitel VII je nach gewähltem Weg

# Weitere Ideen
- Zwischensequenzen als Schattenspiel (`art_src/cutscenes`, parallele Sitzung, Probe für Luca) – auf Lucas Antwort warten
- Tsukumogami Teil 3: Ungaikyō, Kyōrinrin, Zorigami als Items
- `--raum`-Gegenmessung Oni-Horn ×1,03, Yashiori ×1,04, Kakuremino ×1,07 mit `--leben`/`--still`
- Hi-ōgi (×1,53) und Masakari (×1,35) beobachten
- Ereignisraum „Tsukumogami-Markt“ passend zur neuen Item-Welle
