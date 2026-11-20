# Yōkai no Michi – Projektleitfaden

Roguelike im Stil von *The Binding of Isaac* / *Enter the Gungeon* mit japanischer Folklore.
Windows-Desktop-Spiel, gebaut über GitHub Actions (`.github/workflows/build.yml`, PyInstaller).

Eingebunden ist das Framework **Claude Code Game Studios** (`.claude/`, MIT-Lizenz,
siehe `.claude/CCGS-LICENSE`). Dessen Skills (z. B. `/art-bible`, `/balance-check`,
`/playtest-report`, `/design-review`, `/team-polish`, `/asset-audit`) gelten hier mit
folgenden Abweichungen: Es ist **kein** Web-/Godot-/Unity-Projekt; die Skills zum
Prototyp im Browser (`/prototype`, `engines/web`) werden nicht benutzt.

## Technik

- **Engine**: pygame-ce (Python 3.11+), eigene Engine in `yokai/`
- **Interne Auflösung**: 480×320, Fenster skaliert ganzzahlig
- **Hi-Res-Ebene**: Figuren, Gegner, Bosse und Requisiten werden in doppelter
  Pixeldichte gezeichnet (`gfx.hi_blit`). Neue Grafik gehört auf diese Ebene.
- **Daten**: Items, Gegner, Bosse, Biome in `yokai/data.py`; Lexikon-Texte in `yokai/bestiary.py`
- **Grafik-Quellen**: `art_src/` (selbst erstellte Pixelart-Generatoren, keine fremden Assets)
- **Musik/SFX**: offline synthetisiert in `art_src/music/` → `yokai/assets/music|sfx`

## Verbindliche Regeln

- Sprites dürfen selbst gezeichnet (art_src/fable) oder mit SpriteCook erzeugt sein (art_src/spritecook: Bogen + Aufbereitungsskript, das Palette, Pixeldichte, Umriss und Zellen ans Spiel angleicht). Klänge sind selbst erzeugt – keine heruntergeladenen Assets.
- Stil: 16-Bit, dunkle Mondnacht, „halb-ernst“; siehe `design/art/art-bible.md`.
- Spieltexte auf Deutsch.
- Vor jedem Commit: `tools/`-Tests (Bot-Läufe, Boss-Test, UI-Durchlauf, `validate.py`).

## Design-Dokumente

- `design/game-concept.md` – Spielidee, Säulen, Kernschleife
- `design/art/art-bible.md` – visuelle Identität (nach `/art-bible`)
- `design/balance/` – Balance-Berichte (nach `/balance-check`)
- `design/ereignisse.md` – Ereignisräume (Fuchshochzeit, Versteckspiel, Ema-Wand, Nachtparade)
