# Balance-Check 8 – Synergie-Fähigkeiten

Werkzeug: `python tools/synbalance.py [boss] [tiefe] [ids]` (Standard: Shuten-dōji, Ebene 5, Hana; `ids` z. B. `onmyodo,feuerwerk` misst nur diese).
Jede Synergie bekommt nur ihre eigenen Items und kämpft dreimal (Seeds 11–13) gegen denselben Boss;
Vergleich mit gleich vielen Zufalls-Items. Zeitlimit 180 s, „Treffer“ = erlittene Treffer.

## Befund vor der Korrektur

| Synergie | Kampfzeit |
|---|---|
| Obon-Fest (Hōzuki + Chōchin-Feuer) | **4,7 s** |
| Feuerwerk über Edo | 9,1 s |
| Onmyōdō | 14,5 s |
| Ölfeuer | 15,8 s |
| Blitz & Klaue | 28,8 s |
| Chōchin-Feuer allein | 30,9 s |

Ursache: Schaden von Bodenfeuer, Blitzen und Explosionen löste selbst wieder Springfeuer, Donnerbiest
und Pentagramm aus. Jede Flamme erzeugte im Schnitt 1,4 neue (mit Obon-Fest 4,8) – eine Kettenreaktion.

## Korrektur

Folgeschaden (Hazard-Ticks, `run.explode`) setzt `run._echo`; Springfeuer, Donnerbiest und Pentagramm
zählen nur noch echte Treffer (Talismane und Nahkampf).

## Ergebnis danach (gekürzt)

```
Zufall 2 Items: 179.9 s, 53.3 Treffer
Zufall 3 Items: 115.2 s, 35.0 Treffer
onmyodo          Zeit ×0.14 ( 26.0 s)  Treffer -48.0
feuerwerk        Zeit ×0.15 ( 27.3 s)  Treffer -48.0
oni_rausch       Zeit ×0.23 ( 40.6 s)  Treffer -46.7
blitzschlag      Zeit ×0.30 ( 54.0 s)  Treffer -42.0
seimei_meister   Zeit ×0.34 ( 61.8 s)  Treffer -41.0
hannya_zorn      Zeit ×0.35 ( 62.4 s)  Treffer -41.7
jingi            Zeit ×0.35 ( 40.7 s)  Treffer -27.7
kyudo            Zeit ×0.38 ( 67.6 s)  Treffer -36.0
oni_tanz         Zeit ×0.39 ( 69.7 s)  Treffer -36.3
sonne_mond       Zeit ×0.39 ( 70.4 s)  Treffer -34.0
drachenkoenig    Zeit ×0.41 ( 73.4 s)  Treffer -39.7
sturmgott        Zeit ×0.42 ( 74.7 s)  Treffer -41.3
...
gluecksgoetter   Zeit ×1.00 (180.0 s)  Treffer +13.0
sushi            Zeit ×1.00 (180.0 s)  Treffer +14.7
omamori_set      Zeit ×1.56 (180.0 s)  Treffer +26.3
hanami_picknick  Zeit ×1.56 (180.0 s)  Treffer +27.7
```

Obon-Fest 4,7 s → 118 s, Ölfeuer 15,8 s → 76,6 s, Blitz & Klaue 28,8 s → 54 s.
Onmyōdō und Feuerwerk bleiben die stärksten Angriffs-Synergien (~26 s) – stark, aber ohne Rückkopplung; beobachten.
Synergien mit „×1,00 (180 s)“ sind Schutz-, Glücks- oder Raum-Fähigkeiten, die gegen einen einzelnen Boss
nicht wirken; sie sind hier nicht bewertbar. Omamori-Sammler und Hanami-Picknick erhöhen die erlittenen Treffer
nur, weil sie mehr Leben geben und der Test so länger läuft.

## Nachtrag Runde 9–11

Seit Runde 9 starten die Onmyōdō-Papierdiener am Rand des explodierenden Gegners (statt in seiner Mitte)
und fliegen als Hitogata sichtbar zurück. Sie trafen vorher sofort und unsichtbar.

```
python synbalance.py shuten_doji 5 onmyodo,feuerwerk,oni_rausch
feuerwerk        Zeit ×0.18 ( 32.5 s)  Treffer -45.7
oni_rausch       Zeit ×0.23 ( 40.6 s)  Treffer -46.7
onmyodo          Zeit ×0.26 ( 46.3 s)  Treffer -43.7
```

Onmyōdō 26,0 s → 46,3 s – die hier angeregte Abschwächung (Schaden 0,7 → 0,5) ist damit unnötig.
Feuerwerk 27,3 s → 32,5 s (Streuung durch geänderte Zufallsfolge, Wirkung unverändert). Beide liegen jetzt
im oberen Mittelfeld neben Oni-Rausch, keine Synergie sticht mehr allein heraus.
