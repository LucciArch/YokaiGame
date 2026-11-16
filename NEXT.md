# Nächster Schritt

**Synergien Teil 3** – noch ~37 Synergien geben nur Werte oder alte Flags (orbital, familiar, aura, explode …).
Nach dem Muster in `yokai/sigs.py` (Abschnitt Synergie-Fähigkeiten, `TEXT` + Haken) je eine eigene
Fähigkeit, die die Signaturen ihrer Items verstärkt. Als Nächstes (je Runde ~9):

1. feuerwerk, oelfeuer, feuerkind, feuerwagen, gericht, sturmfaecher, sturmgott, blitzschlag, orochi_kusanagi
2. hannya_zorn, oni_tanz, oeyama_bande, maskenzug, unterweltgift, wirbelklingen, strassenkatze, yamabushi, tempelfest
3. schreinwaechter, unbeweglich, drachenschuppen, daruma_geist, yomotsu, riesenmoench, totenfaehre, hyakki_herr, kaufmann
4. Rest: gluecksheim, winkekatze, fuchsgeld, wunsch, tennyo, kappa_fest, hanami_picknick, shogatsu, pilger, sommerwind, fest_der_laternen

Warum: Synergien sind der Kern des Wiederspielwerts; reine Werte-Synergien fühlen sich nach dem
Item-Umbau (eigene Signaturen) blass an. `tools/sigtest.py` testet neue `sig_*` automatisch.

## Weitere Ideen
- Balance-Check der neuen Synergie-Fähigkeiten (`/balance-check`, Bot-Läufe mit erzwungenen Synergien)
- Sichtbare Effekte für Synergie-Fähigkeiten (eigene Partikel/Farben statt Standard-Ring)
- Neuer Boss für Kapitel V/VI mit eigener Hi-Res-Figur
- Lexikon-Seite „Synergien“ mit Fähigkeitstext (TEXT aus sigs.py) statt nur Namen
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
