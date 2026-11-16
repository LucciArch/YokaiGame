# Nächster Schritt

**Neuer Boss für Kapitel V oder VI mit eigener Hi-Res-Figur** – Runden 9–11 haben Synergien im Kampf
sichtbar gemacht (Schriftzug + Welle beim ersten Auslösen pro Raum für 41 Kampf-Synergien, Papierdiener als
Hitogata, Hanabi-Funken) und Onmyōdō nachgemessen (jetzt 46 s gegen Shuten-dōji, gleichauf mit Feuerwerk).
Das Synergie-System ist damit rund. Am meisten Wiederspielwert bringt jetzt neuer Inhalt am Ende eines Laufs:

1. In `yokai/data.py` (BOSSES) prüfen, welches späte Kapitel die wenigsten Bosse hat.
2. Folkloretreuen Yōkai wählen (z. B. Ōmukade – Riesentausendfüßler vom Mikami-Berg, Gegner von Tawara Tōda;
   oder Nue – Chimäre im schwarzen Gewitterwolkenkleid, von Minamoto no Yorimasa erlegt).
3. Hi-Res-Figur in `yokai/bosses.py` (wie die übrigen Bosse, `gfx.hi_blit`), zwei Phasen mit zur Sage passenden
   Angriffen, Lexikon-Eintrag in `yokai/bestiary.py`, `tools/bosstest.py` muss ihn besiegen.

Warum: Synergien und Items sind jetzt reichlich; Bosse sind das, was einen Lauf im Gedächtnis hält.

## Weitere Ideen
- Ausrufe für Schutz-/Glücks-Synergien (z. B. Kenkō-Rettung, Omamori-Sammler) – diese lösen im Bot selten aus
- `tools/synbalance.py` um Schutz-Synergien erweitern (Messung „Treffer bis Tod“ statt Kampfzeit)
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Neue Synergien für Items, die noch an keiner beteiligt sind
- Eigene Grafik für Ratten (Tessos Schwarm) und Windsicheln (Wirbelwind-Klingen) statt eingefärbter Talismane
