# Balance-Check 97 – unteres Ende der Synergien

Messung: `python3 tools/synbalance.py shuten_doji 5 grosse_welle,tsukumogami,hundert_augen,tengu_flug --leben`
(Bosskampf bis zum Tod, Vergleich mit Zufalls-Build aus 2 Items).

| Synergie | vorher | nachher | Änderung |
|---|---|---|---|
| tsukumogami | ×0,89 | ×1,07 | jede Rolle wirft zwei zielsuchende Papierpuppen (100 %) |
| hundert_augen | ×0,89 | ×1,05 | Augen stapeln sich pro Treffer: +20 % + 6 % je Auge (max. 6 → +56 %) statt fest +30 % |
| grosse_welle | ×0,85 | ×0,99 | Rückflut: abgeprallter Talisman und Teilstücke (70 % statt 60 %) suchen ihr Ziel |
| tengu_flug | ×0,90 | ×1,09 | nach der Rolle fliegen vier Würfe als durchbohrende Krähenfedern (200 %) |

Hinweis: Tengu-Flug reagiert nicht linear (Federn ×1,6 → ×0,91, ×2 → ×1,09, ×2,4 → ×1,29, ×3 → ×1,72).
Der Bot rollt alle 2 s – echte Spielerinnen seltener, daher eher etwas großzügiger.
