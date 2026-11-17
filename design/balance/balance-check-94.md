# Balance-Check 94 – Mokumokuren und Kappa-Festmahl

Werkzeug: `python tools/synbalance.py shuten_doji 5 mokumokuren,kappa_fest --leben` bzw. `--raum`.

| | Boss vorher | Boss nachher |
|---|---|---|
| Mokumokuren | 7,4 % (×0,72) | **10,0 % (×0,97)** |
| Kappa-Festmahl | 7,5 % (×0,72) | 7,5 % (×0,72) |

## Mokumokuren (Shōji-Papier + Karte des Diebes)
Die Talismane wurden erst ab Radius 7 „sehend“ – bei Größe 3 und 0,9 s Flugzeit erst nach ~150 px, im Bosskampf fast
nie. Jetzt öffnet sich das Auge ab Radius 4,5 (nach ~70 px): zielsuchend und +40 % Schaden.

## Kappa-Festmahl (Kappas Gurke + Kappa-Teller)
Abgeprallte Talismane treffen jetzt einmalig 50 % stärker und bremsen. Im Bosskampf prallt kaum ein Talisman ab,
deshalb bleibt der Wert dort gleich; die Synergie lebt von +1 Herz, voller Heilung und der Raum-Wirkung.

## Messhinweis Raum-Test
Mit 2 Zufalls-Items braucht der Bot im Raum schon 164 s (3 Items: 110 s). Zwei-Item-Synergien stoßen deshalb oft an
die 180-s-Grenze (Faktor ×1,10) – das ist kein hängender Gegner, sondern die Messgrenze.
