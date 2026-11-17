# Balance-Check 92 – Fächer-Synergien Sturmfächer und Großer Wind

Werkzeug: `python tools/synbalance.py shuten_doji 5 sturmfaecher,grosser_wind --leben --waffe=w_fan` (Boss)
und `--raum` (drei Wellen Normalgegner). Fächer-Basis (Zufall, `--waffe=w_fan`): 2 Items 4,4 %, 3 Items 9,9 %.

| | Boss vorher | Boss nachher | Raum vorher | Raum nachher |
|---|---|---|---|---|
| Sturmfächer | 3,2 % (×0,73) | **5,0 % (×1,16)** | ×0,69, +29 Treffer | **×0,58, +15 Treffer** |
| Großer Wind | 2,2 % (×0,50) | **3,8 % (×0,87)** | ×0,82, +44 Treffer | **×0,49, −1 Treffer** |

## Sturmfächer (Tengu-Fächer + Raijins Trommelstock)
Die Böen stoßen nur Normalgegner – am Boss gab die Synergie nichts. Jetzt ruft jeder dritte Angriff einen Blitz
(1,5× + 3) auf den nächsten Feind in 130 px, der wie bisher eine Böe entfesselt. sigtest prüft den Blitz.

## Großer Wind (Tengu-Fächer + Fūjins Windsack)
Weggewehte Geschosse kommen als Windklinge (1,5×, durchbohrend) auf den nächsten Feind zurück – höchstens eine pro
Spielergeschoss (`_tf`), damit dichter Kugelhagel nicht explodiert. Im Bosskampf selten (11–26 Mal pro Kampf),
die Synergie bleibt eine Raum-Synergie; dort jetzt doppelt so schnell wie Zufall.
