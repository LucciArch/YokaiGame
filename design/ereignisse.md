# Ereignisräume

Ereignisräume sind Sonderräume ohne Kampf, die eine kleine Geschichte aus der Folklore
erzählen und eine Entscheidung verlangen. Sie stehen auf der Minikarte mit eigenem Symbol
und spielen die Nachtmarkt-Musik „Yomise“.

| Raum | Kapitel | Häufigkeit | Entscheidung | Belohnung / Strafe |
|---|---|---|---|---|
| Kitsune no Yomeiri (Fuchshochzeit) | alle | ca. jede 7. Ebene | Nicht auf den Zug schießen | Schleier der Fuchsbraut, danach meist Fuchs-Items / Fuchsfeuer greifen an |
| Kakurenbo (Versteckspiel) | ab II | ca. jede 7. Ebene | Die richtige von vier Urnen zerschlagen (rosa Funken verraten sie), zwei Versuche | Glück +1 und Temari-Ball (danach Mon) / nichts |
| Ema-Wand | alle | ca. jede 6. Ebene | Einen von drei Wünschen wählen | Schaden, Herz, Mon, Karte+Schlüssel, Seelenherzen oder Feuerrate |
| Omikuji-Schrein | alle | Sonderraum | Ein Los ziehen (5 Mon), Unglückslos am Musubi-Gestell anbinden (3 Mon) | Item, Ebenen-Segen, Schaden oder Drops / Ebenen-Fluch, bei Daikyō −1 Herz |
| Hyakki Yagyō (Nachtparade) | ab II | ca. jede 9. Ebene | Den drei Reihen der Parade ausweichen | Eine Truhe, ohne Treffer zwei; Treffer kosten Herzen |
| Shinkirō (Trugbild der Hamaguri) | alle | ca. jede 3. Ebene | Das echte von drei Items nehmen – nur es wirft einen Schatten; 15 s Zeit; ab Tiefe 4 zu 35 % zwei echte, das zweite kostet ein Herz | Ein Item / Trugbild zerfließt, nichts |

Code: `yokai/yomeiri.py`, Raumverteilung in `yokai/rooms.py` (`extras`).

## Regeln für neue Ereignisse

- Ein Satz Erklärung reicht (Banner beim Betreten und Raum-Hinweis).
- Die Entscheidung muss sichtbar sein, bevor sie fällt (kein Zufall ohne Vorwarnung).
- Eigene Figuren werden selbst gezeichnet (`art_src/fable/events_1/`).
- Belohnung klein halten: Ereignisse sollen Abwechslung bringen, keine Pflicht sein.
