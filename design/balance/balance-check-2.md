## Balance Check 2: Progression über 11 Ebenen (v1.3)

*Nach dem CCGS-Ablauf `/balance-check`, Schwerpunkt Progression.*

### Änderung
Kapitel I–V haben jetzt je **zwei Ebenen** (andere Gegend und anderer Boss als in der ersten),
Kapitel VI (Himmelsgefilde) bleibt eine Ebene. Ein Lauf hat damit 10 Ebenen bis zum Sieg,
11 bis zum wahren Sieg (vorher 5 bzw. 6).

### Schwierigkeitsstufe
`tier = Kapitel + 0,5 · (zweite Ebene)` ersetzt die Kapitelnummer in allen Skalierungen:

| Wert | Formel |
|---|---|
| Gegner-HP | × (1 + 0,3·(tier−1) + 0,05·(tier−1)² [+0,3 in Kapitel VI]) |
| Boss-HP | × (1 + 0,15·(tier−1) + 0,02·(tier−1)²) |
| Gegner-Feuerpause | × max(0,7; 1 − 0,06·(tier−1)) |
| Geschosstempo | + 4,5 % je tier |

Der quadratische Anteil gleicht aus, dass Spielerinnen und Spieler über doppelt so viele
Ebenen auch etwa doppelt so viele Items sammeln (Bot-Läufe: 30–40 statt 16–31).

### Messung (Bot mit Unverwundbarkeit, Seeds 11–13)
Spieler-DPS wächst von ≈ 9 auf 25–140 (je nach Synergien); Gegner-HP pro Raum von ≈ 40 auf 350–600.
Sekunden pro Raum bleiben über den ganzen Lauf bei 4–13 s – keine Ebene kippt in reines Durchlaufen.

### Offen
- Stark synergierende Builds (DPS > 100) bleiben in Kapitel V/VI überlegen. Gewollt (Isaac-Gefühl),
  aber beobachten.
- Echte Gefahr (Treffer pro Raum) misst der Bot nicht → `/playtest-report` mit Menschen nötig.
