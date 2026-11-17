# Balance-Check 128 – Siegel-, Prüfungs- und Quest-Items

## Methode
- Passive: `tools/synbalance.py shuten_doji 5 <ids> --items --leben` (neu: `--items`): jedes Item + ein Zufalls-Item
  gegen zwei Zufalls-Items, 12 Seeds, Boss-Schaden in % bis zum Tod.
- Aktive: Messskript (nicht im Repo) – Boss vor der Spielerin, Aktiv auslösen, 4 s ohne Schießen, Boss-HP in % pro Ladung
  (Tiefe 3 und 5, je 6 Seeds). Yatagarasu-Feder/Oni-Trommel mit Schießen gegen dieselbe Zeit ohne Aktiv.

## Ergebnis Passive (Faktor gegen Zufall, 1,00 = 6,5 %)
| Item | vorher | nachher |
|---|---|---|
| habakiri | ×3,04 | ×1,42 (Bosse 1 % statt 4 % Max-HP) |
| hi_ogi | ×1,53 | – |
| masakari, setsubun_mame | ×1,35 / ×1,32 | – |
| übrige 56 | ×0,80 … ×1,24 | – |

×0,80 sind Nutz-Items ohne Bosswirkung (Geld, Schlüssel, Laden, Schutz) – gewollt.

## Ergebnis Aktive (Boss-% pro Ladung, Tiefe 3 / 5)
| Aktiv | T3 | T5 |
|---|---|---|
| ofuda_sturm | 5,6 | 6,0 |
| shikigami_ruf | 5,0 | 2,2 |
| matsuri_uchiwa | 2,5 | 1,3 |
| mondkine | 2,0 | 1,2 |
| totsuka | 1,7 | 0,9 |
| raijin_taiko | 1,5 | 0,8 |
| onryo_kerze | 1,3 | 0,8 |
| shiomitsu_tama | 0,8 | 0,5 |
| Oni-Trommel | +4,2 je Ladung über Basis | |
| Yatagarasu-Feder | ±0 gegen Boss (Nutzen in Räumen) | |

Quest-Aktive liegen im Rahmen; Totsuka ist pro Ladung etwas stärker als Raijin-Taiko (trifft auch alle Feinde) – passt
als schwerste Quest-Belohnung. Kein Eingriff nötig.
