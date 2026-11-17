# Balance-Check 82 – Treffer-Auslöser mit echter Lebensgrenze

Werkzeug: `python tools/synbalance.py shuten_doji 5 --leben [--waffe=w_sword]`. Neu: ohne Gott-Modus, gemessen wird
der Boss-Schaden in % bis zum Tod der Spielerin (Hana, Ebene 5, Seeds 11–22). Der Bot stirbt nach rund 5–9 s
(etwa 4 Treffer) – so wirken Effekte „wenn du getroffen wirst“ nur so oft, wie die Herzen reichen.

Anlass: Check 79 ließ offen, ob Hannya-Zorn, Göttliches Gericht, Oni-Tanz und Unbeugsam im Nahkampf nur im
Gott-Modus übermächtig wirken.

## Ergebnis vorher (Boss-Schaden bis zum Tod)

| | Median aller 98 | Hannya-Zorn | Oni-Tanz | Unbeugsam | Gericht |
|---|---|---|---|---|---|
| Talisman | 13,4 % | 68,0 % | – | – | – |
| Schwert | 6,0 % | **55,1 %** | 32,9 % | 25,9 % | 18,4 % |

Auch mit Lebensgrenze blieb Hannya-Zorn im Schwertkampf 9× über dem Median und fast doppelt so stark wie Platz 2.

## Ursache
Hannya-Maske (`hurt_ring`) und Darumas goldene Splitter (Unbeugsam) feuern 12 bzw. 8 durchbohrende Geschosse im
Kreis. Steht die Spielerin direkt an einem großen Boss, treffen ihn **alle** – ein Treffer wurde zu 12 × 1,2 Schaden.
Gleicher Fehlertyp wie die Mehrfach-Hiebe aus Check 79.

## Änderung
Ein Ring (und Darumas Splitter) teilt sich eine Trefferliste: jeder Feind höchstens einmal pro Ring. Dafür 1,5× statt
1,2× Schaden pro Geschoss, damit der Ring gegen Gruppen etwas stärker bleibt. Test in `tools/waffentest.py`
(schlägt auf altem Code mit 50,4 statt ≤ 1,5 × Schaden fehl).

## Ergebnis nachher

| | Hannya-Zorn | Oni-Tanz | Unbeugsam | Gericht |
|---|---|---|---|---|
| Talisman | 43,3 % (Platz 11) | 32,3 % | 24,9 % | 18,5 % |
| Schwert | 28,4 % (gleichauf mit Platz 2, Yomotsu 28,1 %) | 15,1 % | 19,0 % | 18,4 % |

Göttliches Gericht (Jōhari-Rache) bleibt mit 18 % im oberen Feld ohne Ausreißer – keine Änderung nötig.
