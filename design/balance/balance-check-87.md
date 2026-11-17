# Balance-Check 87 – Oni-Rausch und Onmyōdō

Werkzeug: `python tools/synbalance.py shuten_doji 5 oni_rausch,onmyodo --leben` (Hana, Ebene 5, Seeds 11–22).
Anlass: Check 82 zeigte beide weit über dem Median von 13,4 %.

| | vorher | Items ohne Synergie-Fähigkeit | nachher |
|---|---|---|---|
| Oni-Rausch | 72,5 % | 35,3 % | **43,5 %** |
| Onmyōdō | 70,7 % | 23,0 % | **25,8 %** |

## Ursachen
- **Onmyōdō:** Die drei zielsuchenden Papierdiener aus jeder Siegel-Explosion zählten selbst für das Pentagramm
  (5 Treffer, mit Seimei 3). Jede Explosion lud die nächste zu 60 % auf – eine Kettenreaktion am Boss.
- **Oni-Rausch:** +60 % statt +30 % Schaden pro torkelndem Talisman und zusätzlich `dmgm=1.1`. Shutens Kalebasse
  lässt jeden Talisman mit `b.dmg × 1,3` explodieren, der Bonus wirkt also doppelt.

## Änderungen
- Papierdiener tragen `_shiki`; `sigs.hit_post` zählt sie nicht fürs Pentagramm. Test in `tools/sigtest.py`
  (schlägt auf altem Code mit `sg_pent = 3` fehl).
- Oni-Rausch: +45 % statt +60 %, `dmgm=1.1` entfernt. Getestet: 1,3 (= ohne Fähigkeit, 43,5 % nur durch dmgm),
  1,4 (41,2 %), 1,45 (43,5 %), ohne dmgm bei 1,6 (60,0 %).

## Neue Spitze (Median weiter 13,4 %)
Feuerwerk über Edo 60,7 %, Fūjin und Raijin 57,4 %, Drachenkönig 50,9 %, Orochi-Kusanagi 50,4 %,
Sanshu no Jingi 81,4 % (3 Items, ×4,8 gegen Zufall mit 3 Items).
