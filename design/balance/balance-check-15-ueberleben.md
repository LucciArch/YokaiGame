# Balance-Check 15 – Überleben mit Synergien („Treffer bis Tod“)

Werkzeug: `python tools/synbalance.py shuten_doji 5 --tod` – Hana, Ebene 5, ohne Gott-Modus.
Shuten-dōji wird in Phase 2 festgehalten (30–45 % HP), gemessen wird die Zeit bis zum Tod.
12 Seeds pro Synergie, Vergleich mit gleich vielen Zufalls-Items (Faktor > 1 = zäher als Zufall).

## Ergebnis

- Schutz-Synergien wirken messbar: Omamori-Sammler ×1,61, Yomotsu Hirasaka ×1,61, Schreinwächter ×1,33,
  A und Un ×1,28, Unbeweglich ×1,26, Drachenpanzer ×1,15. Kein Ausreißer über ×2.
- Sanshu no Jingi (×1,88) und Leben und Tod / Todesbote (×1,69) überleben am längsten – Jingi durch
  Blitze, die den Boss unterbrechen, die beiden anderen durch Geisterherzen ihrer Items. Legendär bzw.
  selten und an Kills gebunden, daher bleiben sie so.
- Reine Angriffs- und Glücks-Synergien liegen zwischen ×0,77 und ×1,1 – Streuung des Zufallsvergleichs
  (Zufall 2 Items 19,1 s vs. 3 Items 16,9 s zeigt etwa ±15 %).
- Doppeltes Katzenglück (×0,96): Der Bot weicht nicht gezielt aus, gebremste Geschosse bleiben dadurch
  länger bei ihm. Stärkeres Bremsen (versucht: 40 % Tempo) machte den Wert schlechter (×0,91) und wurde
  zurückgenommen – das Glöckchen hilft echten Spielerinnen beim Ausweichen, das misst der Bot nicht.

Keine Änderungen an Werten nötig.

## Rohdaten

```
pygame-ce 2.5.8 (SDL 2.32.10, Python 3.11.18)
Zufall 2 Items: 19.1 s, 3.7 Treffer
Zufall 3 Items: 16.9 s, 3.7 Treffer
jingi            Zeit ×1.88 ( 31.7 s)  Treffer  +0.8
leben_tod        Zeit ×1.69 ( 32.3 s)  Treffer  +3.9
todesbote        Zeit ×1.69 ( 32.3 s)  Treffer  +0.9
omamori_set      Zeit ×1.61 ( 27.3 s)  Treffer  +1.9
yomotsu          Zeit ×1.61 ( 30.9 s)  Treffer  +3.7
shogatsu         Zeit ×1.52 ( 29.2 s)  Treffer  +2.9
hanami_picknick  Zeit ×1.43 ( 24.1 s)  Treffer  +2.8
schreinwaechter  Zeit ×1.33 ( 25.5 s)  Treffer  +1.9
ewiger_winter    Zeit ×1.29 ( 24.7 s)  Treffer  -0.5
daruma_geist     Zeit ×1.28 ( 24.4 s)  Treffer  +1.6
a_un             Zeit ×1.28 ( 24.4 s)  Treffer  +1.9
tennyo           Zeit ×1.28 ( 24.4 s)  Treffer  +2.8
unbeweglich      Zeit ×1.26 ( 24.1 s)  Treffer  +2.8
ninja_flug       Zeit ×1.22 ( 23.4 s)  Treffer  -0.3
spinnennetz      Zeit ×1.20 ( 22.9 s)  Treffer  -0.3
pilger           Zeit ×1.19 ( 22.7 s)  Treffer  +0.6
mondschein_teich Zeit ×1.16 ( 22.3 s)  Treffer  -0.2
oeyama_bande     Zeit ×1.16 ( 22.2 s)  Treffer  +1.9
orochi_kusanagi  Zeit ×1.16 ( 22.1 s)  Treffer  -0.2
drachenschuppen  Zeit ×1.15 ( 22.0 s)  Treffer  +1.6
totenfaehre      Zeit ×1.13 ( 21.7 s)  Treffer  +0.8
tiefsee          Zeit ×1.13 ( 21.6 s)  Treffer  +1.8
tengu_flug       Zeit ×1.13 ( 21.6 s)  Treffer  -0.4
seimei_meister   Zeit ×1.12 ( 21.5 s)  Treffer  -0.4
feuerwerk        Zeit ×1.12 ( 21.4 s)  Treffer  -0.3
kappa_fest       Zeit ×1.10 ( 21.0 s)  Treffer  +1.4
strassenkatze    Zeit ×1.07 ( 20.5 s)  Treffer  -0.5
oni_krieger      Zeit ×1.07 ( 20.4 s)  Treffer  +0.7
riesenmoench     Zeit ×1.06 ( 20.2 s)  Treffer  -0.1
fujin_raijin     Zeit ×1.06 ( 20.2 s)  Treffer  -0.5
sturmfaecher     Zeit ×1.01 ( 19.4 s)  Treffer  -0.4
bushi            Zeit ×0.99 ( 19.0 s)  Treffer  -0.2
sturmgott        Zeit ×0.99 ( 19.0 s)  Treffer  -0.2
koi_drache       Zeit ×0.98 ( 18.9 s)  Treffer  -0.3
wirbelklingen    Zeit ×0.98 ( 18.8 s)  Treffer  +0.5
feuerkind        Zeit ×0.98 ( 18.7 s)  Treffer  -0.4
geisterlicht     Zeit ×0.98 ( 18.7 s)  Treffer  -0.2
sommerwind       Zeit ×0.98 ( 18.7 s)  Treffer  -0.2
hanami           Zeit ×0.98 ( 18.7 s)  Treffer  -0.4
drachenkoenig    Zeit ×0.97 ( 18.6 s)  Treffer  -0.3
augen_ueberall   Zeit ×0.97 ( 18.6 s)  Treffer  -0.4
onmyodo          Zeit ×0.96 ( 18.5 s)  Treffer  -0.3
winkekatze       Zeit ×0.96 ( 18.4 s)  Treffer  -0.3
maskenzug        Zeit ×0.95 ( 18.2 s)  Treffer  -0.2
hannya_zorn      Zeit ×0.94 ( 18.1 s)  Treffer  -0.2
sternenfall      Zeit ×0.94 ( 17.9 s)  Treffer  -0.7
mondklinge       Zeit ×0.93 ( 17.8 s)  Treffer  -0.6
hyakki_herr      Zeit ×0.93 ( 17.8 s)  Treffer  -0.2
tiefsee_herr     Zeit ×0.93 ( 17.7 s)  Treffer  -0.4
gericht          Zeit ×0.92 ( 17.7 s)  Treffer  -0.3
feuerwagen       Zeit ×0.92 ( 17.6 s)  Treffer  -0.5
tempelfest       Zeit ×0.91 ( 17.5 s)  Treffer  -0.3
kranichschwarm   Zeit ×0.91 ( 17.5 s)  Treffer  -0.5
sturmgoetter     Zeit ×0.91 ( 17.5 s)  Treffer  -0.4
fest_der_laternen Zeit ×0.91 ( 17.4 s)  Treffer  -0.4
teezeremonie     Zeit ×0.90 ( 17.2 s)  Treffer  -0.2
sonnenspiegel    Zeit ×0.90 ( 17.2 s)  Treffer  -0.4
hundert_augen    Zeit ×0.89 ( 17.1 s)  Treffer  -0.2
fuchstanz        Zeit ×0.89 ( 17.1 s)  Treffer  -0.2
oelfeuer         Zeit ×0.89 ( 17.1 s)  Treffer  -0.4
goetter_arsenal  Zeit ×0.89 ( 17.1 s)  Treffer  -0.6
oni_rausch       Zeit ×0.89 ( 17.0 s)  Treffer  -0.5
ninja            Zeit ×0.88 ( 16.8 s)  Treffer  -0.4
verfluchte_sterne Zeit ×0.88 ( 16.8 s)  Treffer  -0.2
fuchshochzeit    Zeit ×0.88 ( 16.8 s)  Treffer  -0.4
oni_tanz         Zeit ×0.87 ( 16.7 s)  Treffer  -0.4
tengu_koenig     Zeit ×0.87 ( 16.7 s)  Treffer  -0.5
papiersturm      Zeit ×0.87 ( 16.7 s)  Treffer  -0.3
kaufmann         Zeit ×0.87 ( 16.7 s)  Treffer  -0.4
katzenreich      Zeit ×0.87 ( 16.6 s)  Treffer  -0.2
fuchsstern       Zeit ×0.87 ( 16.6 s)  Treffer  -0.2
unterweltgift    Zeit ×0.85 ( 16.4 s)  Treffer  -0.2
rattenschwarm    Zeit ×0.84 ( 16.1 s)  Treffer  -0.3
onmyo_spiegel    Zeit ×0.84 ( 16.0 s)  Treffer  -0.7
blitzschlag      Zeit ×0.84 ( 16.0 s)  Treffer  -0.3
grosser_wind     Zeit ×0.83 ( 15.9 s)  Treffer  -0.4
sonne_mond       Zeit ×0.83 ( 15.9 s)  Treffer  -0.5
himmelsbote      Zeit ×0.83 ( 15.9 s)  Treffer  -0.6
kyudo            Zeit ×0.83 ( 15.8 s)  Treffer  -0.3
wunsch           Zeit ×0.82 ( 15.8 s)  Treffer  -0.2
gluecksheim      Zeit ×0.82 ( 15.8 s)  Treffer  -0.2
fuchsgeld        Zeit ×0.82 ( 15.8 s)  Treffer  -0.2
grosse_welle     Zeit ×0.82 ( 15.7 s)  Treffer  -0.4
gluecksgoetter   Zeit ×0.82 ( 15.6 s)  Treffer  -0.7
yamabushi        Zeit ×0.80 ( 15.3 s)  Treffer  -0.5
sushi            Zeit ×0.79 ( 15.1 s)  Treffer  -0.4
tempelmusik      Zeit ×0.77 ( 14.7 s)  Treffer  -0.6
```
