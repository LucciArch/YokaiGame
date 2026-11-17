# Balance-Check 131/132 – Meister-Startitem und Kapitel IV–V

Messung: Gott-Modus-Bot ohne Zusatzschaden (`bot.play(..., dmg=1)`), 8 Läufe je Variante (Seeds 1–8, Figuren
reihum), Bosszeit = Sekunden im Bossraum mit lebenden Gegnern, Mittel je Ebene.

| Ebene | ohne (vorher) | Meister (vorher) | ohne (nachher) | Meister (nachher) |
|---|---|---|---|---|
| 1–2 | 25,9 / 20,7 | 24,9 / 21,0 | 25,7 / 19,6 | 27,6 / 22,3 |
| 3–4 | 33,1 / 20,5 | 29,1 / 16,4 | 36,8 / 26,2 | 20,3 / 17,1 |
| 5–6 | 32,8 / 21,4 | 14,3 / 15,5 | 23,1 / 21,5 | 17,8 / 18,0 |
| 7–8 | 12,3 / 11,3 | 9,7 / 9,5 | 13,6 / 11,2 | 13,4 / 11,9 |
| 9–10 | 7,6 / 6,9 | 9,0 / 6,9 | 10,7 / 9,0 | 13,8 / 13,4 |
| 11 | 15,2 | 15,2 | 15,1 | 18,1 |

## Befund
- Das Meister-Startitem kürzte Bosskämpfe auf Ebene 4–6 um ~25–50 %, Ebene 1–2 kaum.
- Unabhängig davon lagen Kapitel IV–V (Ebene 7–10) in beiden Varianten bei 7–12 s, Ziel ≥ ~15 s.

## Änderungen
- Runde 131: Meister-Läufe `Run.boss_mult = 1.15` (Boss-HP), im Lauf-Spielstand gesichert.
- Runde 132: Kapitel IV–V Boss-HP × `1 + 0,25 · (tier − 3)` (×1,25 … ×1,63). Kapitel VI bleibt darüber
  (Mikaboshi 1500 · 4,25 ≈ 6400 gegen Orochi 880 · 3,77 · 1,63 ≈ 5400).

## Offen
- Streuung ist groß (Seeds ziehen verschiedene Items). Ebene 9–10 ohne Meister noch ~10 s; der Bot weicht nicht
  aus, echte Kämpfe dauern länger. Nach Lucas nächstem Spieltest entscheiden, ob weiter angehoben wird.
