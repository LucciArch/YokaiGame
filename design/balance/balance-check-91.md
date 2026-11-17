# Balance-Check 91 – Unteres Ende: Göttliches Arsenal, Kranichschwarm, Bushi

Werkzeug: `python tools/synbalance.py shuten_doji 5 --leben` (Hana, Ebene 5, Seeds 11–22).

## Messfehler behoben
`synbalance.py` ließ den Bot nur mit `--waffe=` an Nahkampfwaffen heranlaufen. Items wie Ame-no-Nuboko (`w_spear`),
Tamahagane (`w_sword`) oder der Tengu-Fächer (`w_fan`) schlugen deshalb aus der Ferne ins Leere. Jetzt entscheidet
`weapons.weapon_of(p)` nach den Items. Nahkampf bleibt im `--leben`-Maß benachteiligt (mehr Treffer kassiert):
Vergleichsbasis dafür ist `--waffe=w_sword` (Zufall 2 Items 4,5 %, 3 Items 11,1 %).

| | vorher | nachher |
|---|---|---|
| Göttliches Arsenal | 5,7 % (×0,55) | **10,5 % (×1,01)** |
| Kranichschwarm | 6,2 % (×0,60) | **12,7 % (×1,22)** |
| Bushi-Seele | 6,7 % (Schwert aus der Ferne) | 7,3 % mit Nahkampf = ×1,6 der Schwert-Basis, unverändert |

## Göttliches Arsenal
Ame-no-Nuboko macht den Speer zur Waffe – Hachimans Bogen ging darin unter, die Synergie war eine Falle.
Jetzt schießt jeder Speerstoß zusätzlich einen durchbohrenden Pfeil (Pfeilwerte wie `w_bow`, erbt die Wurf-Flags).
sigtest prüft den Pfeil.

## Kranichschwarm
Kraniche falten sich erst beim Räumen von Räumen; im Bosskampf zu Laufbeginn gab die Synergie nichts. Jetzt fliegen
immer mindestens zwei Kraniche, je drei gefaltete einer mehr (bis 5).

## Offen
Fächer-Synergien Sturmfächer (3,2 %) und Großer Wind (2,2 %) liegen jetzt als Nahkampf am Ende – mit
`--waffe=w_fan` gegen die Fächer-Basis nachmessen.
