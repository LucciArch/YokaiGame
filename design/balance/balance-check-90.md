# Balance-Check 90 – Orochi-Kusanagi, Izanagis Flucht, Jingi-Blitze

Werkzeug: `python tools/synbalance.py shuten_doji 5 orochi_kusanagi,izanagis_flucht --leben` (Hana, Ebene 5, Seeds 11–22).

| | vorher | ohne Synergie-fx | nur Fähigkeit | nachher |
|---|---|---|---|---|
| Aus dem Schwanz der Orochi | 50,4 % | 32,5 % | 51,0 % (ohne dmgm) | **40,4 %** |
| Izanagis Flucht | 47,7 % | 25,1 % | 32,3 % (ohne spd) | **37,8 %** |

## Orochi-Kusanagi
Gift von Yamata-Zahn liegt dank dreifachem Wurf praktisch dauerhaft auf dem Boss, der Bonus wirkt also fast immer.
Vergiftete 1,4× → 1,2×, `dmgm` 1,1 entfällt (1,25 ohne dmgm: 47 % – stark nichtlinear).

## Izanagis Flucht
Die Rollen-Pfirsiche (3 × 300 %, durchbohrend) wirkten zusammen mit +10 Tempo (mehr Rollen, mehr Ausweichen) fast doppelt.
Rollen-Pfirsiche jetzt 150 % (200 %: 44 %); Pfirsiche bei Treffern bleiben 300 %. Abklingzeit 4,5 s statt weniger
Schaden hätte 43 % ergeben.

## Jingi-Blitze
`run.lightning` legt ein einmal treffendes Feld (`Hazard.done`, `_echo` verhindert Folge-Feuer/Blitze);
`sigs.on_lightning` kennt nur `sturmfaecher` (stößt keine Bosse). Keine Mehrfachauslösung – der Blitz alle 5 s ist
einfach stark (2,5× + 4). Jingi bleibt bewusst die Drei-Item-Krönung.

## Gegencheck Schwert (`--waffe=w_sword`)
Izanagi 16,8 %, Orochi 16,6 % (Zufall 3 Items 11,1 %), Jingi 28,3 %, übrige vier aus 87–89 zwischen 4,6 und 9,2 %.
Kein Ausreißer.

## Neue Spitze (Talisman)
Jingi 76,5 · Feuerwerk 44,2 · Oni-Rausch 43,5 · Hannya-Zorn 43,3 · Orochi 40,4 · Izanagi 37,8 · Blitzschlag 37,7.
Untere Enden: goetter_arsenal 5,7 %, kranichschwarm 6,2 %, bushi 6,7 % (Faktor ~0,6) – Kandidaten zum Aufwerten.
