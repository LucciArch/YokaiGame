# Balance-Check 79 – Waffen-Builds mit Synergien

Werkzeug: `python tools/synbalance.py shuten_doji 5 [ids] --waffe=w_laser|w_sword|w_bow`.
Wie Check 8 (Shuten-dōji, Ebene 5, Hana, Seeds 11–13, Gott-Modus, Limit 180 s), aber die Spielerin bekommt die
Angriffsart zusätzlich. Nahkampf läuft auf Hiebweite heran und umkreist das Ziel.

Anlass: Seit Runde 65 übernehmen Waffen fast alle Wurf-Fähigkeiten (Mehrfachwurf, Elemente, Sigs).

## Grundwerte (3 Zufalls-Items)

| Angriff | Kampfzeit | Faktor zu Talisman | Ziel (Check 6) |
|---|---|---|---|
| Talisman | 121,8 s | 1,0 | – |
| Lichtstrahl | 89,0 s | 1,37 | Fern 1,1–1,3 |
| Bogen | 74,2 s | 1,64 | Fern 1,1–1,3 |
| Schwert | 66,0 s | 1,85 | Nah 1,4–1,8 |

Median über alle 98 Synergien: Talisman 180 s (Limit), Strahl 93 s, Schwert 78 s, Bogen 103 s.
Die Waffen liegen im Mittel leicht über dem Zielband, aber ohne Ausreißer nach oben – kein Grund für eine pauschale Dämpfung.

## Ausreißer (< ½ Median der Angriffsart)

| Synergie | Talisman | Strahl | Schwert | Bogen | Ursache |
|---|---|---|---|---|---|
| Shinobi (Shuriken + Kunai) | 98,0 | 87,1 | **29,6 → 62,1** | 66,6 | **Fehler**, behoben |
| Hannya-Zorn | 54,8 | 33,3 | 10,9 | 28,1 | Treffer-Auslöser, s. u. |
| Göttliches Gericht | 122,3 | 69,1 | 27,0 | 63,0 | Treffer-Auslöser (Jōhari 8× Rache) |
| Oni-Tanz | 67,2 | 52,3 | 21,2 | 50,4 | Treffer-Auslöser (Hannya-Ring) |
| Unbeugsam | 150,4 | 86,4 | 34,8 | 83,6 | Treffer-Auslöser (goldene Splitter) |
| Feuerwagen | 71,0 | 51,2 | 27,6 | 54,5 | Rolle neben dem Boss |
| Orochi/Kusanagi, Rōnin-Katze | – | – | – | – | Synergie bringt selbst ein Schwert mit |

### Behoben: Seiten- und Rückhiebe trafen denselben Feind mehrfach
Seitenwurf (Kunai) und Rückwurf erzeugen beim Schwert, Speer, Keule zusätzliche Hiebe. Deren breite Bögen
(Schwert 130°) erfassten einen großen Boss direkt neben der Spielerin ein zweites und drittes Mal – ein Angriff
zählte doppelt oder dreifach. Jetzt trifft ein Angriff jeden Feind höchstens einmal (`weapons.melee(seen=…)`);
Test in `tools/waffentest.py` (schlägt auf altem Code mit 15,4 statt 7,7 Schaden fehl).

### Bewusst gelassen: Treffer-Auslöser im Nahkampf
Im Gott-Modus wird der Nahkampf-Bot rund 0,6-mal pro Sekunde getroffen und nie bestraft. Effekte „wenn du
getroffen wirst“ (Hannya-Ring, Hannya-Zorn, Jōhari, Daruma-Splitter) laufen so dauerhaft und treffen den Boss
aus nächster Nähe mit fast allen Ring-Geschossen. Im echten Spiel kostet jeder Auslöser ein halbes Herz –
das ist das gewollte Risiko-für-Schaden-Spiel des Nahkampfs. Erst nachmessen, wenn ein Messmodus mit echter
Lebensgrenze für Nahkampf existiert (Idee: `--tod` mit Schadenszählung).
