# Erledigt (Runden 22–23)
Ausweich-Rolle animiert: Runde 22 drehte/stauchte das Sprite (Luca fand das „blöd“), Runde 23 ersetzt das durch
eigene gepixelte Roll-Bilder für alle 10 Figuren (`art_src/fable/heroes/roll.py` → `yokai/assets/sprites/<name>_roll.png`:
geduckt + 4 Ball-Bilder), Nachbilder als Ball-Silhouette, Staub in Bodenfarbe. Offen dabei: Ball-Bilder ggf. pro Figur
nachschärfen, wenn Luca Feedback gibt (z. B. Waffe sichtbar halten, größere Schweife); neue Figuren brauchen einen
SPEC-Eintrag in `roll.py`.

# Nächster Schritt

**Geheime Endkapitel mit echten Endbossen (Wunsch von Luca)** – mit Teil 1 beginnen: Schadensobergrenze + Pforten-Wahl nach Kapitel VI
Heute endet der Lauf nach Kapitel VI (Takamagahara/Tsukiyomi) mit einem Boss aus einem Pool von vier
(Mikaboshi, Izanami, Kagutsuchi, Fūjin). Diese Bosse fühlen sich nicht wie Endbosse an und lassen sich mit starken
Builds sehr schnell besiegen. Geplant, über mehrere Runden verteilt:

1. **Weg wählen:** Nach dem Boss von Kapitel VI öffnen sich (wenn freigeschaltet) zwei Pforten, eine zu
   **Yomi no Kuni** (Unterwelt: Endboss Izanami in ihrer verwesten Gestalt mit den acht Donnergöttern) und eine zu
   **Takamagahara no Oku** (Endboss Amaterasu, die sich aus der Felsenhöhle Ama-no-Iwato erhebt, oder Susanoo).
   Jeder Weg hat 2–3 Ebenen mit eigener Gegend, Musik und eigenen späten Gegnern.
2. **Geheime Ebene:** Sie wird durch etwas Besonderes ausgelöst, z. B. alle drei Kaiserinsignien tragen, oder
   Reinigungssalz an einer Wand auf Ebene 11 ohne einen Treffer im Kapitel. Dahinter wartet ein verborgener
   letzter Gegner, etwa Ame-no-Minakanushi oder der „Nue der Leere“.
3. **Endboss-Regeln:**
   - **Schadensobergrenze:** höchstens ~2 % der Max-HP pro Treffer und ~8 % pro Sekunde, damit niemand den Boss
     mit einem Treffer erledigt. Das HUD zeigt dann z. B. „Göttlicher Schutz“.
   - Drei Phasen mit Zwischensequenz/Schriftzug, Arena-Veränderung (z. B. die Arena wird kleiner, Licht geht aus)
     und eigene Hi-Res-Figur, deutlich größer als normale Bosse.
   - Kein Itemdrop vor dem Kampf, dafür eigene Belohnungen: Erfolg, neue Figur oder neues Item freischalten,
     ein eigener Abspann.
4. **Testen:** Ein Boss-Test für jeden Endboss (`tools/bosstest.py`), dazu prüfen, dass die Schadensobergrenze greift
   (z. B. Obon-Fest/Onmyōdō-Build braucht > 60 s).

Warum: Der Abschluss eines Laufs soll ein Höhepunkt sein, und geheime Wege erhöhen den Wiederspielwert.

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
