# Ereignisräume

Ereignisräume sind Sonderräume ohne Kampf, die eine kleine Geschichte aus der Folklore
erzählen und eine Entscheidung verlangen. Sie stehen auf der Minikarte mit eigenem Symbol
und spielen die Nachtmarkt-Musik „Yomise“.

| Raum | Kapitel | Häufigkeit | Entscheidung | Belohnung / Strafe |
|---|---|---|---|---|
| Kitsune no Yomeiri (Fuchshochzeit) | alle | ca. jede 7. Ebene | Nicht auf den Zug schießen | Schleier der Fuchsbraut, danach meist Fuchs-Items / Fuchsfeuer greifen an |
| Kakurenbo (Versteckspiel) | ab II | ca. jede 7. Ebene | Die richtige von vier Urnen zerschlagen, zwei Versuche | Glück +1 und Temari-Ball (danach Mon) / nichts |

Code: `yokai/yomeiri.py`, Raumverteilung in `yokai/rooms.py` (`extras`).

## Regeln für neue Ereignisse

- Ein Satz Erklärung reicht (Banner beim Betreten und Raum-Hinweis).
- Die Entscheidung muss sichtbar sein, bevor sie fällt (kein Zufall ohne Vorwarnung).
- Eigene Figuren werden selbst gezeichnet (`art_src/fable/events_1/`).
- Belohnung klein halten: Ereignisse sollen Abwechslung bringen, keine Pflicht sein.
