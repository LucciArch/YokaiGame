# Erledigt (Runden 39–40): Gesten in der Charakterauswahl, Winter im Titel
- Runde 39: `pose_motion` / `pose_fx` in `yokai/app.py` (vor `class Game`): Wurfbilder 4–6 bzw. Sprung, danach Effekte aus
  `art_src/title/gesten.py` (`fx_*`, handgesetzte Raster, 2× für die doppelt große Podestfigur). Klänge `s_pose_<figur>` in
  `art_src/music/sfx.py`; `python3 sfx.py pose_hana …` erzeugt nur die genannten Klänge neu (Seeds der übrigen bleiben unberührt).
- Runde 40: `draw_night`-Stimmung `yuki` bei `stats['wins_hard']` (Vorrang: yomi > yuki > aki); `_branch(near, mood)` tauscht
  die Blütenpalette des Zweigs (Ahorn oder Schnee).

# Nächster Schritt: Synergie-Fanfare
Wird eine Synergie zum ersten Mal vollständig, kurze Einblendung mitten im Raum: die Symbole der beteiligten Items fliegen
zusammen, verschmelzen mit einem Lichtblitz zum Synergie-Namen in Pinselschrift (wie Charakterauswahl), dazu ein eigener
Klang (Koto-Lauf + Kane). Spiel kurz verlangsamen (nicht anhalten). Warum: Item-Kombinationen sind der Kern des
Wiederspielwerts; das Finden einer Synergie soll sich wie ein Höhepunkt anfühlen statt nur als Textzeile.

# Weitere Ideen
- Requisiten Teil 3: eigene Requisiten für `yomi_oku` (Kapitel VII), Grabsteine in Hakaba mit Inschrift/Opfergaben
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Codex: Filter nach Thema/Fundort und Sprung zu den Synergien eines Items im Lexikon
- Gesten auch beim Laufstart: die gewählte Figur macht ihre Geste im ersten Raum, bevor die Steuerung freigegeben wird
- Endbildschirm im Titelstil (Nachtschleier, Pinselstrich, Siegel) – letzter Bildschirm ohne neuen Stil
