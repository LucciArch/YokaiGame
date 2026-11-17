# Balance-Check 106 – Schwierigkeitskurve über den Lauf

Anlass: Luca – „viel zu viele Items, nach ein paar Items gibt es keine Schwierigkeit mehr“.

## Messung (Gott-Modus-Bot ohne Zusatzschaden, 6 Läufe, je Ebene nach dem Boss)

| Ebene | Items vorher | Bosszeit vorher | Items nachher | Bosszeit nachher |
|---|---|---|---|---|
| 1 | 0,7 | 31,7 s | 1,0 | 27,6 s |
| 4 | 8,8 | 17,4 s | 8,8 | 23,0 s |
| 6 | 13,8 | 7,8 s | 14,8 | 15,1 s |
| 8 | 19,3 | 6,5 s | 20,6 | 9,2 s |
| 10 | 25,5 | 4,6 s | 28,8 | 7,9 s |

Vorher wuchs die Spieler-DPS bis Ebene 10 um ~14×, die Boss-HP nur um ~2×. Ursache: Schadens-Multiplikatoren
(11 Items + 7 Synergien) stapelten sich voll multiplikativ, flacher Schaden linear; Boss-HP skalierten schwächer
als normale Gegner. Item-Herkunft (4 Läufe): 153 → 124 Items (−19 %), Endschaden im Mittel ~30 → ~15.

## Änderungen
- Flacher Schaden mit abnehmendem Ertrag: `3,5 · √(1 + 0,55 · Bonus)` (`entities.flat_dmg`).
- Schadens-Multiplikatoren: der stärkste wirkt voll, jeder weitere mit 40 % seines Bonus (`entities.stack_dmgm`).
- Gegner-HP `1 + 0,35(t−1) + 0,07(t−1)²` (vorher 0,3/0,05), Boss-HP `1 + 0,3(t−1) + 0,07(t−1)²` (vorher 0,15/0,02).
- Treffer kosten ab Kapitel III ein ganzes Herz (vorher IV), Boss-Kontakt ebenso.
- Mehr Gegner ab Kapitel II/IV/VI, Champions etwas häufiger.
- Weniger Items: Laden 2 statt 3 Items (teurer: 12 + 5·q), Schrein auf Zwischenebenen 12 % (+20 % ohne Treffer)
  statt 28 % (+30 %), Truhe 5 % statt 10 %, Mini-Boss 15 % statt 30 %, Dōjō 20 % statt 35 %, Geheimraum 35 %
  statt 45 %, zweite Schatzkammer 30 % statt 50 %.

## Offen
- Bosszeit fällt ab Ebene 8 weiter (≈ 8 s). Der Bot weicht nicht aus, echte Kämpfe dauern länger – nach Lucas
  nächstem Spieltest ggf. Boss-HP ab Kapitel V weiter anheben.
- Feuerrate wächst nur ~1,5× – kein Eingriff nötig.
