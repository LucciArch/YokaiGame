# Test-Werkzeuge

Vor jedem Commit laufen lassen (aus diesem Ordner):

| Skript | Prüft |
|---|---|
| `python validate.py` | Daten: Items, Pools, Symbole, Synergien, Raumvorlagen, Sprites, Erfolge |
| `python uiflow2.py` | Alle Menüs und Bildschirme einmal durchklicken |
| `python bot.py [n]` | n automatische Läufe (Standard 3) mit Unverwundbarkeit – findet Abstürze |
| `python bosstest.py` | Jeder Boss wird einmal besiegt, mit Zeit und Trefferzahl |

Jeder vierte Bot-Lauf ist ein Endlos-Lauf und endet deshalb ohne Ergebnis („None“) – das ist gewollt.
