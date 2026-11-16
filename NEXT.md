# Nächster Schritt

**Raum-Synergien messbar machen und nachbalancieren** – Runden 18–19 haben die letzten 12 ungebundenen Items
in 6 neue Synergien gebracht (Gashadokuro, Tsukumogami, Shinsen, Nanakorobi Yaoki, Jinmenju, Mokumokuren);
jetzt gehört jedes Item zu mindestens einer Synergie (96 insgesamt).

1. `tools/synbalance.py` um einen Messmodus in einem normalen Gegnerraum (statt nur gegen Shuten-dōji)
   erweitern, damit Raum-Synergien vergleichbar werden (Gelächter der Nacht, Enenra, Hara-tsuzumi,
   Gashadokuro, Mokumokuren, Tsukumogami).
2. Ausreißer (deutlich schneller/langsamer als der Median) angleichen, Bericht unter `design/balance/`.

Warum: Die neuen Synergien wirken vor allem gegen viele Normalgegner – die Boss-Messung erreicht mit
2 Zufalls-Items das Zeitlimit und sagt über sie nichts aus. Besonders Gashadokuro (Zerbrechen unter 25 %
plus Splitter) und Mokumokuren (zielsuchende große Talismane) könnten zu stark sein.

## Weitere Ideen
- Bot mit Ausweichen für `synbalance.py --tod`, damit Doppeltes Katzenglück und Tsukumogami (Rolle) messbar werden
- Eigene Grafik für Ratten (Tessos Schwarm), Windsicheln und Gashadokuro-Knochensplitter statt eingefärbter Talismane
- Eigenes Geschoss-Sprite für Fūjins Windklingen und Blätter (jetzt runde Kugeln)
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Synergien mit drei Items (z. B. die drei Kaiserinsignien als „große“ Kombination mit Fanfare)
