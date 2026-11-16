# Erledigt (Runden 37–38): Untermenüs im Titelstil, wandelnde Titelnacht
- Runde 37: `App.veil(s, rect, a)` (weicher Nachtschleier statt `gfx.panel`) und `App.page_head(title, seal, sub)`
  (Überschrift mit Hanko-Siegel) in Herausforderungen, Codex, Lexikon, Erfolge, Statistik, Steuerung. Siegel aus
  `art_src/title/charsel.py` (`SEALS`: 力 玉 妖 功 史 手). `brush_sel` hat jetzt einen Strich je Auswahlreihe (`key[0]`).
- Runde 38: `draw_night` liest den Fortschritt: `true_wins` → Herbst (`aki`: Himmel/Nebel getönt, Ahorn per Palettentausch
  `_maple`), Erfolg `yomi` → violette Totennacht mit 6 Hitodama. Helfer `gfx.tinted_mult`.

# Nächster Schritt: Charakterauswahl lebendiger
Jede Figur bekommt beim Wechsel eine kurze eigene Geste auf dem Podest (Kenji zieht das Schwert, Okiku schwebt höher,
Seimei hebt ein Ofuda, Benkei stampft – mit Staub/Funken) und einen eigenen kurzen Klang (Schwertziehen, Glocke,
Windstoß …, offline in `art_src/music/` synthetisieren). Warum: Titel und Menüs sind jetzt aus einem Guss; die
Figurenwahl ist der letzte Schritt vor jedem Lauf und soll die Figuren unterscheidbar und begehrenswert machen.

# Weitere Ideen
- Requisiten Teil 3: eigene Requisiten für `yomi_oku` (Kapitel VII), Grabsteine in Hakaba mit Inschrift/Opfergaben
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Synergie-Fanfare: beim Wecken einer Synergie kurze Einblendung mit den Item-Symbolen und eigenem Klang
- Titel: Jahreszeit auch für weitere Meilensteine (Schnee nach dem Oni-Modus-Sieg)
- Codex: Filter nach Thema/Fundort und Sprung zu den Synergien eines Items im Lexikon
