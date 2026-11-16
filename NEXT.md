# Erledigt (Runden 28–29)
- Runde 28: **Ehrliche Hitboxen.** `entities.solid_hit()` prüft Kreis gegen die gezeichnete Grundfläche
  (`FOOT`: Fels, Krug, Laterne) statt gegen die volle Kachel; zu festen Nachbarn hin bleibt sie dicht.
  Gilt für Spieler, Gegner (`blocked`), Geschosse und Strahlen (`weapons.beam`). Spieler mit `fly` überfliegt
  Felsen und Krüge (`LOW_TILES`), Laternen bleiben fest; fliegend wird er über Requisiten gezeichnet.
  Wer über einem Fels den Flug verliert, kann herauslaufen. Test: `tools/kolltest.py`.
- Runde 29: Felsbrocken (`props.boulder`, neun Biome) mit Facetten, Rissen, Körnung, Kieseln; Bambusstümpfe
  im Bambuswald neu (schräger Schnitt, hohl, Knoten). Bau: `cd art_src/fable/environment && python3 hi.py`
  (deterministisch; braucht pip-Pillow, nicht das System-PIL).

# Nächster Schritt
**Requisiten Teil 2: Grundfläche je Sprite-Variante + weitere Biom-Requisiten neu pixeln**
- `FOOT` ist je Kachelart fest; schmale Varianten (Takenoko, Totenpfähle, Pfeiler) blocken noch zu breit.
  Idee: Grundfläche beim Laden aus dem Alpha der unteren Sprite-Zeilen von `rock_hi` ableiten
  (Variante wie in `gfx.hi_tile`: `(x*7 + y*13)//32 % 3`) und in `solid_hit` nutzen.
- Neu pixeln, was noch flach wirkt: Takenoko (Scheiden mit Flecken), Wolkenfelsen Takamagahara,
  Eiswürfel Yukiyama, Holzstapel/Fass Kawabe, Grabsteine Hakaba; eigene Requisiten für `yomi_oku`.
Warum: Luca wünscht besser modellierte, zur Umgebung passende Objekte mit passender Hitbox.

# Danach (Wunsch von Luca): Titelbildschirm komplett neu
Den Startbildschirm/das Hauptmenü komplett überarbeiten – **nicht** einfach Sprites herumlaufen lassen,
sondern ein schöner, stimmiger Titelbildschirm wie bei richtig guten Spielen: z. B. großes gemaltes
Mondnacht-Panorama in Ebenen (Torii, Berge, Nebel, Parallaxe), handgesetztes Logo „Yōkai no Michi“
mit Kanji, edles Menü mit Pinselstrich-Auswahl, dezente Partikel (Glühwürmchen, Hitodama), Einblendung.
Alles selbst gepixelt (Hi-Res-Ebene), Stil laut `design/art/art-bible.md`.

# Weitere Ideen
- Größere Hi-Res-Figur „Izanami, die Verweste“ für Phase 3 (`art_src/fable/bosses_3/`)
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Eigenes Geschoss-Sprite für Pfirsiche, Fūjins Windklingen und Windsicheln
- Synergien mit drei Items (die drei Kaiserinsignien als „große“ Kombination mit Fanfare)
- Ausweichender Mess-Bot für Dash-/Nahkampf-Synergien in `tools/synbalance.py`
