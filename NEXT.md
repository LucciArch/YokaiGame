# Nächster Schritt

**Synergie-Fähigkeiten sichtbar machen** – seit Runde 6 haben alle 86 Synergien eine eigene Fähigkeit
(`sig_*` in `yokai/data.py`, Text in `yokai/sigs.py` → `TEXT`). Der Spieler sieht sie aber nur einmal im
Banner beim Aufheben. Darum:

1. Pausebildschirm (`app.py`, Synergie-Zeile in der Item-Übersicht): beim Überfahren/Auswählen einer
   Synergie ihren Fähigkeitstext zeigen (wie bei Items per Maus-Hover).
2. Lexikon: eigene Seite „Synergien“ (entdeckte mit Namen, Items und Fähigkeitstext, unentdeckte als ???).

Warum: Synergien sind der Kern des Wiederspielwerts – wer nicht nachlesen kann, was eine Kombination tut,
plant keine Builds. Danach Balance (siehe unten), weil viele neue Fähigkeiten sich stapeln.

## Weitere Ideen
- Balance-Check der Synergie-Fähigkeiten: Bot-Läufe mit erzwungenen Synergien (z. B. Feuerwerk + Ölfeuer + Obon-Fest,
  Unbeweglich-Schild, Totenfähre-Münzen) und `/balance-check`
- Sichtbare Effekte für Synergie-Fähigkeiten (eigene Partikel/Farben statt Standard-Ring)
- Neuer Boss für Kapitel V/VI mit eigener Hi-Res-Figur
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Neue Synergien für Items, die noch an keiner beteiligt sind
