# Nächster Schritt

**Weitere Synergien für ungebundene Items** – Runden 15–17 haben alle auslösbaren Synergien sichtbar gemacht
(Schriftzug + Welle beim ersten Auslösen pro Raum), `tools/synbalance.py --tod` misst Überlebenszeit
(Bericht `design/balance/balance-check-15-ueberleben.md`) und drei neue Synergien gebracht
(Hara-tsuzumi, Gelächter der Nacht, Enenra). Noch 12 Items gehören zu keiner Synergie:
fuchsschrein, hitogata, shiro_kimono, gashadokuro_knochen, omamori_gokaku, karakasa, kiyome_sack, ema,
jinmen_frucht, shoji_papier, daruma_otoshi, geheimkarte.

1. 3–4 folkloretreue Paare bilden (z. B. Gashadokuro-Knochen + Weißes Totengewand, Karakasa + Hitogata,
   Kiyome-Salz + Kleiner Fuchsschrein, Daruma-otoshi + Omamori: Erfolg) und je eine eigene Fähigkeit
   geben, die die Signaturen der Items verstärkt, mit `_syn(...)`-Ausruf.
2. Mit `tools/synbalance.py` (Kampfzeit) und `--tod` (Überleben) messen.

Warum: Jedes Item soll mindestens eine Kombination haben – das erhöht den Wiederspielwert.

## Weitere Ideen
- Die Messung gegen Shuten-dōji erreicht mit 2 Zufalls-Items das Zeitlimit (180 s) – Messung zusätzlich
  in einem Raum mit normalen Gegnern, damit Raum-Synergien (Gelächter, Enenra, Hara-tsuzumi) vergleichbar werden
- Doppeltes Katzenglück ist im Bot-Test nicht messbar (Bot weicht nicht aus) – Bot mit Ausweichen für `--tod`
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Eigene Grafik für Ratten (Tessos Schwarm) und Windsicheln statt eingefärbter Talismane
- Eigenes Geschoss-Sprite für Fūjins Windklingen und Blätter (jetzt runde Kugeln)
