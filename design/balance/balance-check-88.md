# Balance-Check 88 – Feuerwerk über Edo und Fūjin-Raijin-zu

Werkzeug: `python tools/synbalance.py shuten_doji 5 feuerwerk,fujin_raijin --leben` (Hana, Ebene 5, Seeds 11–22).
Anlass: nach Check 87 die neue Spitze. Median aller 98 Synergien weiter 13,4 %.

| | vorher | Items ohne Synergie-Fähigkeit | nachher |
|---|---|---|---|
| Feuerwerk über Edo | 60,7 % | 38,2 % | **44,2 %** |
| Fūjin-Raijin-zu | 57,4 % | 13,8 % | **33,4 %** |

## Ursachen
- **Feuerwerk:** Jeder explodierende Talisman zerplatzt in fünf Funken (je 0,4 × Schaden). Am großen Boss trafen
  alle fünf – derselbe Fehlertyp wie Hannya-Ring (Check 82) und Mehrfach-Hiebe (Check 79).
- **Fūjin-Raijin:** Windsack alle 1 s statt 4 s (4× so oft) *und* zusätzlich ein Blitz (2,5 × Schaden + 4) in jeden
  getroffenen Feind.

## Änderungen
- Funken teilen sich eine Trefferliste (`nb.hit = seen`), dafür 0,8 statt 0,4 × Schaden. Gegen Gruppen etwa gleich,
  am Boss ein Funke. Getestet: 0,4 (32,8 %), 0,8 (44,2 %), 1,0 (39,8 % – Streuung). Test in `tools/sigtest.py`.
- Windsack mit Fūjin-Raijin alle 1,5 s. Getestet: 2,0 s (29,8 %), 1,5 s (33,4 %).

## Neue Spitze
Sanshu no Jingi 81,4 % (3 Items, ×4,8), Drachenkönig 50,9 %, Orochi-Kusanagi 50,4 %, Izanagis Flucht 47,7 %.
