# Nächster Schritt

**Ausrufe und Messung für Schutz-/Glücks-Synergien** – Runden 12–14 haben Kapitel VI auf vier Bosse gebracht
(neu: Fūjin, Gott des Windes, eigene Hi-Res-Figur in `art_src/fable/bosses_3/boss_fujin.py`), dazu sein
Belohnungs-Item Kaze-bukuro und die Synergie Fūjin-Raijin-zu. Jedes Kapitel hat jetzt vier Bosse.
Offen ist, dass Schutz-Synergien (Kenkō-Rettung, Omamori-Sammler, Drachenpanzer, Unbeweglich …) im Spiel kaum
wahrnehmbar sind und nicht gemessen werden:

1. `tools/synbalance.py` um einen Modus „Treffer bis Tod“ erweitern (Spielerin ohne Gott-Modus, Feuer aus).
2. Schutz-Synergien bekommen beim Auslösen `_syn(...)` (Schriftzug + Welle) wie die Kampf-Synergien.
3. Ausreißer angleichen, Bericht unter `design/balance/`.

Warum: Spielerinnen sollen auch defensive Kombinationen bemerken und ihnen vertrauen können.

## Weitere Ideen
- Fūjin-Lexikonbild ist das Spielsprite – ein eigenes, größeres Porträt wie bei den anderen Bossen zeichnen
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Eigene Grafik für Ratten (Tessos Schwarm) und Windsicheln statt eingefärbter Talismane
- Eigenes Geschoss-Sprite für Fūjins Windklingen und Blätter (jetzt runde Kugeln)
- Neue Synergien für Items, die noch an keiner beteiligt sind
