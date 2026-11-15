# Changelog

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
