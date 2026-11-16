# Nächster Schritt

**Ausweich-Rolle animieren (Wunsch von Luca, hat Vorrang)** – Die Rolle mit der Leertaste ist heute nur
eine halbtransparente Figur, die nach vorn gleitet, plus graue Punkte (`Player.update`/`Player.draw` in
`yokai/entities.py`, `dash_t` = 0,24 s). Sie soll für alle Figuren richtig aussehen:

1. Echte Rolle: Die Figur dreht sich in Rollrichtung um sich selbst (Hi-Res-Sprite in 4–6 Schritten drehen,
   bei Bewegung nach oben/unten eher stauchen/strecken), kurz geduckt beim Absprung und beim Aufkommen
   (Squash & Stretch), Schatten bleibt flach am Boden.
2. Nachbilder: 2–3 verblassende Silhouetten in Figurenfarbe statt grauer Punkte, dazu Staubwölkchen beim
   Absprung und Aufkommen (Gras/Schnee/Wasser je nach Gebiet eingefärbt).
3. Rollen-Synergien (Tengu-Flug, Hara-tsuzumi, Sommerwind, Feuerkind usw.) behalten ihre Effekte;
   Kostüme (`costume.draw`) müssen mitdrehen oder während der Rolle ausgeblendet werden.
4. Mit einem Screenshot-Streifen (mehrere Bilder der Rolle) prüfen, für mindestens zwei Figuren.

Warum: Die Rolle drückt man ständig – eine gute Animation verbessert das Spielgefühl in jedem Raum.

## Danach

**Ausweichender Mess-Bot für Dash- und Nahkampf-Synergien** – Runde 20 hat `tools/synbalance.py --raum`
(drei Gegnerwellen) gebracht und Tsukuyomis Sichelbögen repariert (Mondschein-Teich lief ins Zeitlimit),
Runde 21 eigene Grafik für Ratten und Knochensplitter. Im Raum-Bericht
(`design/balance/balance-check-20-raum.md`) sind die langsamsten Kampf-Synergien alle rollen- oder
schwertabhängig: Herrenlose Katze ×1.49 (Rōnin-Schwert = Nahkampf), Tengu-Flug ×1.60 (Windwirbel bei der
Rolle), Schreinwächter ×1.68, Hara-tsuzumi, Tsukumogami. Der Mess-Bot rollt aber nur alle 2 s ziellos und
hält Abstand – das misst diese Synergien unfair.

1. In `synbalance.py` einen Bot-Modus ergänzen, der zum nächsten Feind hin rollt und mit Nahkampfwaffe
   (`p.f['w_sword']`) nah herangeht, Geschossen grob ausweicht.
2. Raum- und `--tod`-Messung damit wiederholen; echte Ausreißer angleichen, Bericht ergänzen.

Warum: Erst dann lässt sich entscheiden, ob Herrenlose Katze/Tengu-Flug wirklich schwach sind.

## Weitere Ideen
- Eigenes Geschoss-Sprite für Fūjins Windklingen und Blätter (jetzt runde Kugeln) und für Windsicheln
- Synergien mit drei Items (z. B. die drei Kaiserinsignien als „große“ Kombination mit Fanfare)
- Weitere Ereignisräume (z. B. Tanuki-Bauchtrommel-Wettstreit)
- Kanabō allein ist im Raum langsamer als gar kein Item (weniger Schüsse, mehr Fehlschüsse) – prüfen,
  ob der Feuerraten-Malus (-0,4) zu hart ist
- Raum-Messung auch in Tiefe 4 (mit mehr Items), damit späte Gegner abgedeckt sind
