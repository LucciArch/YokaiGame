# Balance-Check 89 – Drachenkönig und Sanshu no Jingi

Werkzeug: `python tools/synbalance.py shuten_doji 5 jingi,drachenkoenig --leben` (Hana, Ebene 5, Seeds 11–22).

| | vorher | ohne Synergie-fx | nur `pierce` | nur Fähigkeit | nachher |
|---|---|---|---|---|---|
| Drachenkönig | 50,9 % | 6,2 % | 19,1 % | 8,2 % | **26,6 %** |
| Sanshu no Jingi | 81,4 % | 38,9 % | – | 67,7 % (ohne dmgm) | **76,5 %** |

## Drachenkönig
`pierce` + doppelter Seidenfaden: Der durchbohrende Talisman gleitet durch den großen Boss und legt alle 0,07 s ein
Faden-Feld, jedes doppelt stark. Die Wirkung ist nicht linear (Faktor 2: 50,9 %, 1,75: 26,6 %, 1,5: 20,7 %,
1,3: 24,8 % – Streuung der 12 Seeds), Kampfzeit bei 1,75: ×0,52 statt ×0,38. Gewählt: 1,75, Text „fast doppelt so tief“.

## Jingi
Drei-Item-Krönung, bewusst die stärkste Synergie. `dmgm` 1,4 → 1,2. Der Hauptanteil kommt von den Insignien-Blitzen
alle 5 s (38,9 → 67,7 %) – noch offen, ob `run.lightning` Folge-Sigs auslöst, die am Boss mehrfach zählen.
