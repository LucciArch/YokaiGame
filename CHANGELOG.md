# Changelog

## 1.5.0 – „Matsuri-Update“

- Neues Ereignis **Kitsune no Yomeiri**: Eine Fuchshochzeit zieht durch einen Raum – wer sie nicht stört, bekommt ein Geschenk der Braut
- Neues Ereignis **Kakurenbo**: Zashiki-warashi versteckt sich in einer von vier Urnen – zwei Versuche
- Neues Ereignis **Hyakki Yagyō**: Die Nachtparade zieht in drei Reihen durch den Raum – ausweichen lohnt sich
- Neues Ereignis **Ema-Wand**: Drei Votivtafeln, nur ein Wunsch geht in Erfüllung
- 2 neue Items nur aus Ereignisräumen: **Schleier der Fuchsbraut** und **Temari-Ball**, dazu 2 Synergien (Fuchshochzeit, Glückliches Haus)
- Controller vibrieren bei Treffern und Explosionen (an „Bildschirmwackeln“ gekoppelt)
- Neues Musikstück **„Yomise“** (Nachtmarkt) für Laden, Teehaus, Spielhalle und Ereignisräume
- Endbildschirm und „Letzte Läufe“ zeigen, wer dich bezwungen hat
- Raum-Requisiten, Torii, Steinlaternen und Todesanimation in doppelter Pixeldichte
- Lexikon-Seite **Ereignisse**, Statistik „Ereignisse erlebt“, Erfolg „Festtagsgast“
- Hinweis unten links bei neuen Lexikon-Einträgen; Minikarte mit Rahmen und pulsierendem aktuellem Raum
- Lesbarkeit: Titelkarte mit dunklem Band, Hinweise, Tooltips und Erfolgsmeldungen liegen über den Figuren
- 19 Gegner komplett neu gezeichnet (u. a. Gozu und Mezu, Gyūki, Tsuchigumo, Nurikabe, Ningyo, Tennin, Bakeneko, Kawauso, Yamauba)
- Klänge überarbeitet: weicherer Ofuda-Wurf, kräftigere Treffer, eigene Klänge für vergehende Geister, schwere Gegner, zerbrechende Krüge und Felsen, Truhen, Geisterherzen, Salz, Anhänger, Bosssieg und den eigenen Tod
- Alle Klänge auf einheitliche Lautheit gebracht; Gegnerklänge kommen von links oder rechts, je nachdem wo der Gegner steht

## 1.4.0 – „Hyakki-Update“ (enthält 1.3 „Kapitel-Update“)

- **11 statt 6 Ebenen:** Kapitel I–V haben je zwei Ebenen, die zweite mit anderer Gegend und anderem Boss
- Schwierigkeit steigt jetzt pro Ebene statt pro Kapitel (Gegner- und Boss-HP, Feuerrate, Geschosstempo)
- Anzeige „Ebene 7 · Kapitel IV“ im HUD, auf der Titelkarte und im Boss-Intro
- Fairer: Tsurube-otoshi blitzt nach der Landung kurz auf, bevor er feuert; Nopperabō schießt nicht mehr sofort nach dem Auftauchen
- Späte Gegner gefährlicher: Shikome schneller, Onibi legen in tiefen Kapiteln Feuerspuren, Funayūrei feuern Fächer
- Balance-Berichte 2 bis 4 unter `design/balance/`
- Fortschrittspfad auf der Titelkarte jeder Ebene und im Pausenmenü
- Tiefere Ebenen liefern wertvollere Items
- Spielgefühl: kurzer Halt mit Lichtwelle beim Säubern eines Raums, schwere Gegner fallen mit Gewicht
- Kleine Schrift wird kräftiger gezeichnet, damit sie auch in kleinen Fenstern lesbar bleibt
- Prüfungen bleiben kurz (eine Ebene pro Kapitel)
- Läufe speichern und fortsetzen („Speichern & Hauptmenü“, im Titel „Fortsetzen“)
- Neue Spielweise „Entspannt“ in den Optionen: +1 Herz, nur halbe Herzen Schaden, langsamere Geschosse
- Türen, Item-Altäre, Felsen, Urnen und Laternen in doppelter Pixeldichte; Gruben mit Abbruchkante
- 4 neue Items (Glocke des Komainu, Feder der Tennin, Fels von Yomotsu, Sternenstaub) und 3 neue Synergien
- Waffen-, Figuren- und Boss-Balance gemessen und angeglichen (Berichte unter `design/balance/`)
- Kapitelnamen, eigener Seed (E in der Figurenauswahl), Codex mit Silhouetten, Menüs mit Nachthimmel
- Neue Herausforderung **„Der lange Weg“** (alle zehn Ebenen), Option **Blitzeffekte reduziert**, Erzählzeilen zu Kapitelbeginn
- Neue Gegner: **Kawauso** (Kapitel I), **Zashiki-warashi** (Kapitel II), **Yamauba** (Kapitel III), **Nure-onna** (Kapitel IV), **Gozu** und **Mezu** (Kapitel V), **Komainu** und **Tennin** (Kapitel VI)
- Wände in doppelter Pixeldichte; nach dem zweiten Boss eines Kapitels immer ein Schrein
- Statistik „Letzte Läufe“, Infos zum gespeicherten Lauf im Titelmenü
- Segen: Manche Ebenen sind gesegnet (Vollmond: Karte aufgedeckt, Füchse: Rabatt, Reichtum: doppelt Mon, Kami: Heilung)
- Item-Tooltips zeigen „Neu!“, vervollständigte Synergien und Transformations-Fortschritt
- Boss-Lebensbalken mit Schadensspur und Wut-Markierung; Steinlaternen werfen Licht
- Absturzschutz mit `fehler.log`
- 16 neue Raumvorlagen für tiefere Kapitel, 4 neue Erfolge, Lauf-Pfad auf dem Endbildschirm

## 1.2.0 – „Morgengrauen-Update“

### Neu
- **Yōkai-Lexikon** im Hauptmenü: 48 Yōkai und 23 Bosse mit Folklore, Verhalten im Spiel und Fundorten;
  Einträge schalten sich bei der ersten Begegnung frei
- **Epilog nach dem Sieg**: Morgendämmerung, der Zug der Yōkai verblasst, eigenes Ende für jede Figur
  (normaler und wahrer Sieg), Abspann
- Waffenarten: Schwert, Speer, Keule, Bogen, Fächer, Sense und Laser für Figuren und Items

### Grafik
- Eigene Schrift „Yōkai Fude“: lateinische Buchstaben im Stil eines japanischen Pinsels (selbst erzeugt, `art_src/font/fude.py`)
- Felsen, Urnen und Steinlaternen in doppelter Pixeldichte, nach Tiefe mit den Figuren sortiert
- Art Bible als verbindliche Stilvorgabe (`design/art/art-bible.md`)

### Balance
- Jedes Item gehört genau einer Raumart (Schatzraum, Laden, Boss, Kami- oder Oni-Schrein)
- Tiefer = stärker: mehr Gegner-HP und schnellere Geschosse pro Ebene, Tiefe 6 zusätzlich härter
- Weniger Drops, ab Tiefe 4 ganze Herzen Schaden
- Stärkerer Laden, mehr Gegnervielfalt in Tiefe 4

### Entwicklung
- Claude Code Game Studios eingebunden (`.claude/`), Spielkonzept und Balance-Bericht unter `design/`

## 1.1.0 – „Mondlicht-Update“

### Grafik
- Komplett neue, selbst gezeichnete Pixel-Art im düsteren 16-Bit-Stil mit doppelter Pixeldichte:
  alle 51 Yokai, 10 Heldinnen und Helden, 23 Bosse (inkl. mehrteiliger wie Ōmukade, Ryūjin, Rokurokubi)
- Jede Figur mit Lauf- und Angriffsanimation, passend zur Angriffsart aus der Folklore
- Neue Umgebungs-Tiles für alle 17 Biome, neue Item-Symbole, Pickups, Herzen und HUD-Symbole
- Neue Türen (Shōji, Schloss, Boss-Tür mit Shimenawa), Item-Sockel, Geschosse und Schreinobjekte
  (Saisen, Omikuji, Onsen, Torii, Hokora, Teebank, Tanuki-Automat)
- Titelbildschirm mit Pixel-Torii, Stein-Laternen und Kirschbaum; Charakterwahl mit Silhouetten
- Beschwörungskreis beim Erscheinen von Gegnern, Druckwelle und Lichtblitz beim Tod eines Bosses
- Figuren gleiten beim Raumwechsel mit, bleiben im Pause-Menü gedimmt sichtbar

### Spiel
- **Biom-Eigenheiten**: jedes Biom hat eine eigene kleine Mechanik (13 Stück, siehe README) mit eigenen Sounds
- Tanuki-Händler im Laden
- Einmalige Kontext-Tipps (in den Optionen abschaltbar)
- 12 neue Synergien (jetzt 81), 3 neue Erfolge (jetzt 47)
- Statistik zeigt besuchte Biome mit ihrer Eigenheit
- Balance: Susanoo abgeschwächt (6 Herzen, kein Schadensbonus)

### Fehlerbehebungen
- Ebenenfehler bei Spinnenbeinen und Flügeln einzelner Sprites
- Menüs (Herausforderungen, Item-Liste, Game Over) zeigen Sprites in richtiger Größe
- Steuerungshinweise im Startraum überlappen nicht mehr mit dem Ebenen-Titel

## 1.0.0
- Erste Veröffentlichung
