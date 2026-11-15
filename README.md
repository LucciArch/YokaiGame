# Yōkai no Michi – Hyakki Yagyō

Ein Roguelike-Twin-Stick-Shooter im Stil von *The Binding of Isaac* und *Enter the Gungeon*, angesiedelt in der japanischen Folklore.
Du kämpfst dich als Schreinmaid, Rōnin, Fuchsgeist oder Tengu-Kind durch die **Nacht der hundert Dämonen** – vom Bambuswald bis hinab nach Yomi, die Unterwelt, und wieder hinauf in die Himmelsgefilde Takamagahara.

## Herunterladen & spielen (Windows)

1. Rechts auf **Releases** klicken
2. `YokaiNoMichi.exe` herunterladen
3. Doppelklicken – fertig. (Falls Windows SmartScreen warnt: *Weitere Informationen → Trotzdem ausführen*.)

Jeder Push auf `main` baut über GitHub Actions automatisch eine neue `.exe`.

## Steuerung

| Aktion | Tastatur/Maus | Controller |
|---|---|---|
| Bewegen | WASD | Linker Stick |
| Ofuda werfen (schießen) | Pfeiltasten oder linke Maustaste (zielt zur Maus) | Rechter Stick / Steuerkreuz |
| Ausweichrolle (unverwundbar) | Leertaste / Shift / rechte Maustaste | A / RB |
| Aktives Item | E | Y / LB |
| Reinigungssalz (löscht alle Geschosse) | Q | X |
| Items & Werte | Tab (halten) | – |
| Pause | Esc / P | Start |
| Vollbild | F11 | – |

## Inhalt

- **6 Kapitel mit 11 Ebenen, 17 Biome** (Kapitel I–V je zwei Ebenen mit anderer Gegend und anderem Boss): Bambuswald, Inari-Torii-Pfad, Kappa-Flussufer, Geistertempel, Alter Friedhof, Spukvilla, Kurama-Berg, Schneeberg, Ōe-Berg, Drachenpalast, Geisterküste, Tiefsee, Yomi, Höllenfeuer, Hof des Enma, Takamagahara und Mondpalast
- **23 Bosse** mit je eigenen Angriffsmustern und zweiter Phase: Ōmukade, Kappa-Ō, Jorōgumo, Gashadokuro, Rokurokubi, Nue, Sōjōbō, Raijū, Yuki-onna, Umibōzu, Ryūjin, Bake-kujira, Yamata no Orochi, Shuten-dōji, Tamamo-no-Mae Ōnyūdō, Nurarihyon, die drei Kamaitachi, Akkorokamui, Enma-Daiō sowie in Takamagahara Amatsu-Mikaboshi, Izanami und Kagutsuchi
- **53 Yokai-Gegnertypen** (neu in Kapitel VI: Komainu und Tennin) plus 8 Champion-Varianten (rot, blau, gold, violett, grün, weiß, geisterhaft, teilend)
- **146 passive Items** und **15 aktive Items**, **14 Omamori-Anhänger** (ein tauschbarer Slot), Itempools für Schatzraum, Laden, Boss, Kami-Schrein und Oni-Schrein
- **81 Synergien** (z. B. die drei Throninsignien *Kusanagi + Yata no Kagami + Yasakani no Magatama*)
- **9 Transformationen**: 3 Items eines Themas verwandeln dich (Kitsune, Donnergott, Oni, Onmyōji, Yūrei, Tengu, Drache, Kami, Tanuki)
- **10 Charaktere** zum Freischalten, jeweils mit eigener Fähigkeit, eigenen Werten und Startitems
- **51 Erfolge**, die Charaktere, Items, den Oni-Modus und Takamagahara freischalten
- Prozedurale Ebenen mit 92 Raumvorlagen + zufällig generierten Räumen (gespiegelt → hunderte Varianten)
- Spezialräume: Schatzraum (verschlossen ab Kapitel II), Laden, Fluchraum, Kampfraum, Geheimräume (mit Reinigungssalz an rissigen Wänden aufdecken), Omikuji-Schrein, heiße Quelle (Onsen), Schriftrollenarchiv (1 von 3 Items), Dōjō (Champion-Kampf), Teehaus (dauerhafte Werte-Upgrades), Tanuki-Spielautomat, Kami- und Oni-Schreine nach Bossen
- Flüche (Dunkelheit, Nebel, Labyrinth, Verirrte), Oni-Modus (schwer), **Endlose Nacht** (endlose Schleifen mit steigender Schwierigkeit), tägliche Prüfung mit festem Seed, **8 Herausforderungen** mit Sonderregeln (Glaskanone, Boss-Ansturm, Wettlauf gegen den Morgen, Papiermeister …)
- **Biom-Eigenheiten**: jedes Biom hat eine eigene Mechanik – Eisboden, Tengu-Windböen, speiende Lavagruben, Irrlichter, Meeresströmung, Poltergeist-Töpfe, Sternschnuppen, Bambus-Fallen, Fuchsfeuer, greifende Hände, Kappa-Dank, Oni-Kriegstrommeln, Brandung
- Tanuki-Händler im Laden, einmalige Kontext-Tipps (abschaltbar)
- Mini-Bosse in normalen Räumen, Wutphase der Bosse bei 25 % Leben, Wetter (Regen, Schneesturm, Asche)
- **Yōkai-Lexikon** mit Folklore, Verhalten, Fundorten und Zähler, **Codex** aller Items, Erfolge, Statistik (Biome, letzte Läufe)
- **Läufe speichern und fortsetzen**, eigener Seed (Figurenauswahl: E), Spielweise **Entspannt**, Segen und Flüche pro Ebene
- **Epilog** mit eigenem Ende für jede Figur und Abspann; eigene Pinsel-Schrift „Yōkai Fude“
- Düstere 16-Bit-Pixel-Art in doppelter Pixeldichte (selbst gezeichnet, siehe unten); Musik und Sounds werden im Code erzeugt (Koto, Taiko, Shakuhachi in japanischen Tonleitern)

Der Spielstand liegt unter `%APPDATA%\YokaiNoMichi\spielstand.json`, ein laufender Lauf unter `lauf.json`, Fehlerberichte unter `fehler.log`.

## Aus dem Quellcode starten

```bash
pip install -r requirements.txt
python main.py
```

## Projektstruktur

```
main.py              Startpunkt
yokai/app.py         Fenster, Eingabe, Menüs, Codex, Pause, Spielende
yokai/run.py         Ein Lauf: Ebenen, Räume, Kampf, Belohnungen, HUD
yokai/entities.py    Spielfigur, Geschosse, Yokai-KI, Pickups
yokai/bosses.py      Die 23 Bosse (Angriffe als Koroutinen)
yokai/data.py        Items, Synergien, Transformationen, Charaktere, Gegner, Erfolge
yokai/rooms.py       Raumvorlagen und Ebenen-Generator
yokai/gfx.py         Sprites, Icons, Kacheln, Hi-Res-Ebene, Text
yokai/props.py       Türen, Sockel, Schreinobjekte, Geschosse (Pixel-Art im Code)
yokai/sheets.py      Lädt die Sprite-Streifen aus yokai/assets/sprites
yokai/audio.py       Prozedurale Musik und Soundeffekte
```


## Grafik
Alle Sprites sind selbst gezeichnet – als Python-Quellcode in `art_src/fable/` (Figuren, Yōkai, Bosse,
Umgebung, Items) im Stil von `art_src/fable/STYLE_GUIDE.md`: 16-Bit, mondbeschienen-düster, mit
Lauf- (4 Bilder) und Angriffsanimation (3 Bilder) pro Figur. `python3 art_src/import_fable.py`
erzeugt daraus die Sprite-Streifen in `yokai/assets/sprites/`. Umgebungs-Tiles liegen in
`yokai/assets/env/`, Item-Symbole in `yokai/assets/items/`.

Siehe auch [CHANGELOG.md](CHANGELOG.md).
