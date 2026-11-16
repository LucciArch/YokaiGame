# Erledigt (Runden 24–25)
- Runde 24: **Göttlicher Schutz** – Bosse ab Kapitel VI (`Boss.divine`, `run.depth >= 6`) nehmen höchstens 2 % Max-HP
  pro Treffer und 8 % pro Sekunde (Property `Boss.hp` in `yokai/bosses.py`, gilt auch für Brand/Gift/Ketten).
  HUD-Schriftzug über dem Lebensbalken, Boss-Test prüft die Grenze. Normale Builds sind weit unter der Grenze
  (Bosstest unverändert), sie fängt nur übermächtige Builds ab.
- Runde 25: **Kapitel VII Yomi no Kuni** – nach dem ersten Wahren Sieg (`stats.true_wins`) erscheint nach dem
  Kapitel-VI-Boss eine Yomi-Pforte (`Obj('yomi')`). Biom `yomi_oku` (Totenpalast, Tiefe 7) nutzt vorerst die
  Kacheln von `yomi` (`_id`-Shortcut in `data.py`), Boss-Pool 7 = Izanami (aus Pool 6 entfernt). Endlos-Modus
  läuft weiter in die Schleife. Boss-Test prüft die Pforte.

# Nächster Schritt

**Izanami als echte Endbossin (Endkapitel Teil 2)** – heute ist sie in Kapitel VII noch der normale Kapitel-VI-Boss
(Bosstest: 49,6 s, schneller als in VI, weil der Spieler mehr Items hat).
1. Eigene Endboss-Variante, wenn `run.depth == 7`: deutlich mehr HP (~×1,8), **drei Phasen** mit Schriftzug
   (z. B. „Izanami zeigt ihr wahres Gesicht“ bei 66 %, „Die acht Donnergötter erwachen“ bei 33 %), Arena-Wechsel
   (Licht geht aus / Arena wird enger), in Phase 3 die acht Ikazuchi-no-Kami als Blitz-Angriffe aus ihrem
   verwesten Körper, Shikome-Beschwörung.
2. Größere Hi-Res-Figur „Izanami, die Verweste“ (handgesetzte Pixel, `art_src/`), nicht nur die Kapitel-VI-Figur.
3. Belohnung beim ersten Sieg: Erfolg „Rückkehr aus Yomi“, ein neues Item freischalten (z. B. „Pfirsich von
   Yomotsu Hirasaka“ – Izanagi warf Pfirsiche gegen die Verfolger), eigener Abspann-Text im Epilog.
4. Bosstest: Izanami (Tiefe 7) soll mit Test-Build > 90 s brauchen.

Warum: Die Pforte steht, aber das Ziel dahinter fühlt sich noch nicht wie ein Endboss an.

## Danach (Endkapitel Teil 3+)
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) oder Susanoo als Endboss
- Eigene Kacheln/Requisiten für `yomi_oku` in `art_src/fable/environment` (Shortcut in `data.py` entfernen)
- Geheime Ebene (z. B. alle drei Kaiserinsignien) mit verborgenem letztem Gegner

## Ebenfalls offen

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
