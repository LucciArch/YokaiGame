# Balance-Check 99 – Waffen-Brücken (Runde 95)

Methode: `python tools/synbalance.py --leben --figur=<id>` gegen Shuten-dōji, Tiefe 5, 12 Seeds.
Jedes Waffen-Item + ein Zufalls-Item gegen zwei Zufalls-Items (Faktor = Bossschaden in % bis zum Tod).
Spalte „ohne“: dasselbe Item-Paar mit abgeschalteter Brücke (`weapons.bridge_of` → None), also nur die Werte des Items.

| Figur (Basis) | Brücke bringt (mit − ohne) | schwächstes Item mit Brücke |
|---|---|---|
| Akago (Keule, 11,3 %) | +0,05 … +0,76 | Tengu-Fächer ×1,44 → **×1,69** |
| Benkei (Speer, 7,9 %) | +0,2 … +1,1 (Hamaya-Bogen) | Tengu-Fächer ×1,28 → **×1,64** |
| Kenji (Schwert, 6,2 %) | +0,1 … +0,8 | Tengu-Fächer ×0,96 → **×1,25** |
| Kotarō (Fächer, 5,0 %) | +0,1 … +0,4 | Tamahagane ×1,06, Yumi ×1,08 |
| Susanoo (Schwert, 9,4 %) | +0,1 … +0,6 | Tengu-Fächer ×0,90 → **×1,00** |

Ergebnis:
- Ziel „Item lohnt sich (≥ ×1,1)“ wird fast überall erreicht. Ausreißer nach unten war nur die Fächer-Brücke
  (drei Windstöße 0,45×, Flugzeit 0,42 s): jetzt 0,65× und 0,5 s. Susanoo bleibt grenzwertig, weil der Tengu-Fächer
  kaum Werte mitbringt.
- Kotarō liegt insgesamt niedrig – das ist der bekannte Nahkampf-/Fächer-Nachteil des Bots (Check 96), keine Brücken-Frage.
- Bogen-Brücke (Hamaya bei Benkei +1,1) ist die stärkste, ersetzt die Figur aber nicht (Speer bleibt Hauptangriff). Beobachten.
- Streuung: zwei Läufe derselben Messung weichen um ±0,1–0,2 ab.
