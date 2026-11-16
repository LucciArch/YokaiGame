# Nächster Schritt

**Sichtbare Effekte für Synergie-Fähigkeiten** – Runde 7 hat Synergien im Lexikon und Pausebildschirm
nachlesbar gemacht, Runde 8 die Kettenreaktion aus Folgeschaden behoben. Im Kampf sehen viele der 86
Synergie-Fähigkeiten aber noch gleich aus (Standard-Ring `_ring`, weiße/graue Geschosse). Darum:

1. Die 10–15 stärksten/häufigsten Synergien (siehe `design/balance/balance-check-8-synergien.md`, oben in der Liste:
   Onmyōdō, Feuerwerk, Oni-Rausch, Blitz & Klaue, Abe no Seimei, Hannya-Zorn, Sanshu no Jingi, Kyūdō …)
   bekommen eigene Partikel/Farben in `yokai/sigs.py` (Papierdiener als kleine Shikigami-Form, Funken in Hanabi-Farben usw.).
2. Kurzer Schriftzug beim ersten Auslösen pro Raum (wie „Tigerhieb!“), damit der Spieler die Synergie erkennt.

Warum: Eine Synergie, die man im Kampf nicht wahrnimmt, fühlt sich nicht nach Belohnung an – das Lesen allein reicht nicht.

## Weitere Ideen
- Onmyōdō und Feuerwerk beobachten (~26 s gegen Shuten-dōji, stärkste Angriffs-Synergien); ggf. Papierdiener-Schaden 0,7 → 0,5
- `tools/synbalance.py` um Schutz-Synergien erweitern (Messung „Treffer bis Tod“ statt Kampfzeit)
- Neuer Boss für Kapitel V/VI mit eigener Hi-Res-Figur
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Neue Synergien für Items, die noch an keiner beteiligt sind
