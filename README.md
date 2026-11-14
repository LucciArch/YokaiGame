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

- **6 Ebenen, 11 Biome**: Bambuswald, Inari-Torii-Pfad, Geistertempel, Alter Friedhof, Kurama-Berg, Schneeberg, Drachenpalast Ryūgū-jō, Geisterküste, Yomi, Höllenfeuer und Takamagahara
- **16 Bosse** mit je eigenen Angriffsmustern und zweiter Phase: Ōmukade, Kappa-Ō, Jorōgumo, Gashadokuro, Rokurokubi, Nue, Sōjōbō, Raijū, Yuki-onna, Umibōzu, Ryūjin, Bake-kujira, Yamata no Orochi, Shuten-dōji, Tamamo-no-Mae und Amatsu-Mikaboshi
- **29 Yokai-Gegnertypen** plus 6 Champion-Varianten (rot, blau, gold, violett, grün, weiß)
- **118 passive Items** und **12 aktive Items**, Itempools für Schatzraum, Laden, Boss, Kami-Schrein und Oni-Schrein
- **42 Synergien** (z. B. die drei Throninsignien *Kusanagi + Yata no Kagami + Yasakani no Magatama*)
- **9 Transformationen**: 3 Items eines Themas verwandeln dich (Kitsune, Donnergott, Oni, Onmyōji, Yūrei, Tengu, Drache, Kami, Tanuki)
- **10 Charaktere** zum Freischalten, jeweils mit eigenen Werten und Startitems
- **27 Erfolge**, die Charaktere, Items, den Oni-Modus und Takamagahara freischalten
- Prozedurale Ebenen mit 46 Raumvorlagen + zufällig generierten Räumen (gespiegelt → hunderte Varianten)
- Spezialräume: Schatzraum (verschlossen ab Ebene 2), Laden, Fluchraum, Kampfraum, Omikuji-Schrein, heiße Quelle (Onsen), Kami- und Oni-Schreine nach Bossen
- Flüche (Dunkelheit, Nebel, Labyrinth, Verirrte), Oni-Modus (schwer), tägliche Prüfung mit festem Seed
- Codex aller Items, Erfolge, Statistik
- Pixel-Art und Musik werden komplett im Code erzeugt (Koto, Taiko, Shakuhachi in japanischen Tonleitern)

Der Spielstand liegt unter `%APPDATA%\YokaiNoMichi\spielstand.json`.

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
yokai/bosses.py      Die 16 Bosse (Angriffe als Koroutinen)
yokai/data.py        Items, Synergien, Transformationen, Charaktere, Gegner, Erfolge
yokai/rooms.py       Raumvorlagen und Ebenen-Generator
yokai/gfx.py         Pixel-Art-Sprites, Icons, Kacheln, Text
yokai/audio.py       Prozedurale Musik und Soundeffekte
```
