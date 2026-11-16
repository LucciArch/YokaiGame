# Erledigt (Runden 52–54)
- Runde 52: Requisiten Kawabe (Flussfels mit Kappa-Gurke + Wellenringe, Rohrkolben im Seichtwasser mit Hotaru,
  Suijin-Stein mit 水神 `SUIJIN`-Glyphen) und Yashiki (Tansu mit Augen in offener Lade, Andon mit Onibi-Licht,
  goldener Byōbu mit Fingern) in `art_src/fable/environment/props.py`. Neu bauen: `build.py kawabe yashiki`, `hi.py`,
  dann `rock.png` nach `yokai/assets/env/<biom>/` kopieren; floor/wall-PNGs danach per `git checkout` zurücksetzen
  (nur Metadaten-Änderungen).
- Runde 53: Kein Startblinken während der Geste (`pose_t`), `hurt()` beendet die Geste.
- Runde 54: Erfolg `alle_lose`, Spielstand-Liste `kuji_seen`; Test am Ende von `tools/sigtest.py`.

# Nächster Schritt: Requisiten Teil 5 – Ōeyama und Shinkai
Gleiches Vorgehen wie Runde 52. Ōeyama (Kapitel nach dem Yashiki) und Shinkai haben noch Grundformen-Requisiten
(Felsen, Spitzen). Ideen: Ōeyama – Sake-Fass der Oni, Kanabō im Fels, Knochenhaufen mit Oni-Maske; Shinkai –
Riesenmuschel mit Perle, Korallen mit Leuchtfischen, versunkene Steinlaterne. Warum: Stilbruch fällt neben den
neuen Hi-Res-Figuren auf; die Biome davor sind jetzt fertig.

# Weitere Ideen
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Totenpalast-Ambiente: eigene Partikel (Maden-Glühwürmchen, Izanamis acht Donnergötter als Blitze im Hintergrund)
- Lexikon-Ereignisseite zeigt bei Omikuji, welche der fünf Lose schon gezogen sind (`kuji_seen`)
- Kawabe-Ambiente: Glühwürmchen-Partikel über Wasserflächen
- Wanddekos Yashiki/Kawabe ebenfalls in Hi-Res überarbeiten (`wall_decos`)
