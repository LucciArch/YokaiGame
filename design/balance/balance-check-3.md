## Balance Check 3: Gefahr je Gegnerart (v1.3)

*Nach `/balance-check` + `/playtest-report` (automatisiert): sechs Bot-Läufe ohne Unverwundbarkeit,
jeder Treffer wird den Gegnern im Raum anteilig zugerechnet. *

### Befund vorher
Die Gefahr war **umgekehrt** zur Tiefe verteilt: frühe Gegner trafen am häufigsten
(Kodama 1,5, Tsurube-otoshi 1,3, Nopperabō 1,2 Treffer pro Raum), späte fast nie
(Shikome 0,12, Onibi 0,08, Funayūrei 0,05).

| Ursache | Fix |
|---|---|
| Tsurube-otoshi feuert seinen Ring im selben Moment, in dem er auf dir landet – kaum ausweichbar | 0,4 s Aufblitzen nach der Landung, dann erst der Ring |
| Nopperabō schießt 0,35 s nach dem Auftauchen | erst nach 0,6–0,8 s |
| Shikome ohne Angriff, zu langsam für Kapitel V | Tempo 78 → 92 |
| Onibi in Kapitel IV–V reines Füllmaterial | legt ab Stufe 4 Feuerspuren |
| Funayūrei ein einzelner langsamer Schuss | Fächer aus drei Schüssen |
| Kappa-Brut zu langsam | Tempo 50 → 62 |

### Befund nachher
Spitze 1,6 → Mittelfeld; späte Gegner treffen 2–3× so oft wie vorher (Shikome 0,22, Onibi 0,22,
Funayūrei 0,21), Tsurube-otoshi 1,31 → 0,87. Späte Bosse treffen deutlich öfter (Ryūjin 7 → 31,
Enma 3 → 25, Orochi 4 → 19), weil Boss-HP jetzt mit der Ebene quadratisch steigt.

### Offen
Kodama (1,6) bleibt oben, aber nur in 7 Räumen beobachtet – bei der nächsten Messung prüfen.
