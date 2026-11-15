## Balance Check: Gegner, Bosse, Item-Pools (v1.1 → v1.2)

*Nach dem CCGS-Ablauf `/balance-check`.*

### Data Sources Analyzed
`yokai/data.py` (ENEMIES, BOSSES, BOSS_POOL, BIOMES, DEPTH_BIOMES, ITEMS), `yokai/entities.py`
(HP-Multiplikator), Bot-Läufe `tools/bot.py`, Boss-Test `tools/bosstest.py`.
Es gibt kein GDD mit Zielbereichen; Zielwerte stammen aus `design/game-concept.md` (Säule 3).

### Health Summary: CONCERNS

### Gegner je Tiefe (vorher)

| Tiefe | Arten | ⌀ Basis-HP | ⌀ effektive HP | max |
|---|---|---|---|---|
| 1 | 12 | 8,7 | 8,7 | 12 |
| 2 | 16 | 14,2 | 18,4 | 28 |
| 3 | 14 | 18,1 | 28,9 | 34 |
| 4 | **8** | 18,0 | 34,2 | 34 |
| 5 | 12 | 26,2 | 57,6 | 70 |
| 6 | 8 | 23,6 | **59,1** | 70 |

### Outliers Detected
1. **Tiefe 4 hat die kleinste Vielfalt** (8 Arten, Biome je 5–6) – genau in der Spielmitte.
2. **Tiefe 6 ist kaum härter als Tiefe 5** (⌀ 59 gegen 58 effektive HP), obwohl es die letzte Ebene ist.
3. **Laden-Pool zu schwach:** 20 von 30 Laden-Items hatten die niedrigste Qualität. Münzen
   sind seit den gesenkten Drop-Raten knapper, ein schwacher Laden entwertet sie zusätzlich.

### Degenerate Strategies Found
Keine gefunden. Endlose Aufheb-Schleifen (Anhänger, aktive Items) wurden in v1.1 behoben.

### Progression Analysis
HP-Kurve steigt gleichmäßig bis Tiefe 5, dann flach. Boss-HP steigen in Stufen
(≈230 → 330 → 420 → 550 → 840 → 1450); der Sprung zu Tiefe 6 ist gewollt (Endbosse).

### Recommendations (umgesetzt in v1.2)
- Tiefe 6: zusätzlicher HP-Multiplikator +0,3 (gesamt ×2,8 statt ×2,5).
- Tiefe 4: Kappa-Brut und Onibi in Drachenpalast/Tiefsee, Kappa-Brut und Yosuzume an der Geisterküste.
- Laden: jedes fünfte Schatzraum-Item der Qualität 2 wandert in den Laden (Laden 41, Schatz 55).

### Values That Need Attention
- Münz-Einnahmen gegen Ladenpreise: nicht bewertet (keine Zielwerte festgelegt).
- Bot-Läufe sind zu schwach als Schwierigkeitsmaß (Bot gewinnt mit Unverwundbarkeitshilfen);
  ein echter Playtest-Bericht (`/playtest-report`) steht aus.
