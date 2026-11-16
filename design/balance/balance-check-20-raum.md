# Balance-Check 20 – Synergien im Gegnerraum

Werkzeug: `python tools/synbalance.py --raum shuten_doji 2` – drei Wellen zu je 8 Normalgegnern aus dem
Gebiet der Tiefe 2, je 6 Seeds, Bot schießt auf den nächsten Feind. Faktor = Zeit / Zeit mit gleich vielen
Zufalls-Items (2 Items: 68 s, 3 Items: 46 s). Die nächste Welle kommt, sobald nur noch ein Feind lebt,
damit sich die Türen nicht öffnen (sonst lief der Bot in den Nachbarraum).

## Befunde und Änderungen

| Synergie | vorher | nachher | Ursache / Änderung |
|---|---|---|---|
| Mondschein-Teich | 180 s (Zeitlimit) | 72 s | Tsukuyomis Sichel-Talismane kurvten mit fester Drehrate vom Ziel weg und verfehlten jeden entfernten Feind. Jetzt setzt der Bogen schräg an und kreuzt die Ziellinie beim nächsten Feind. |
| Mondsichel-Klinge | 107 s | 47 s | dieselbe Ursache |
| Tsukuyomis Mondsichel (allein) | 149 s | 78 s | dieselbe Ursache |
| Oni-Krieger | 134 s | 89 s | Tigerhieb jetzt zusätzlich beim ersten Treffer auf jeden unverletzten Normalgegner (Bosse unverändert) |

Befürchtete Ausreißer nach oben gibt es nicht: Gashadokuro ×0.71, Enenra ×0.67, Mokumokuren ×1.28.

## Schnellste (Raum)
Sturmgott, Feuerwerk, Sonne & Mond, Sanshu no Jingi, Fūjin-Raijin-zu (×0.33–0.34) – alle Flächen- oder
Kettenschaden, im Raum erwartbar stark; gegen Bosse liegen sie im Mittelfeld.

## Langsamste Kampf-Synergien (offen)
Herrenlose Katze ×1.49, Tengu-Flug ×1.60, Schreinwächter ×1.68, Großer Wind ×1.32, Mokumokuren ×1.28.
Glücks- und Schutz-Synergien (Fuchsgeld, Wunsch, Omamori-Sammler, Hanami-Picknick) sind hier erwartbar
langsam – sie geben keinen Schaden.

Hinweis: Die Streuung je Seed ist groß (z. B. Kanabō 96–167 s), Unterschiede unter ±15 % sind Rauschen.
