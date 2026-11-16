# Erledigt (Runden 41–42): Synergie-Fanfare
- Runde 41: `Run.banner(..., icons=[(icon, col), …])`; `Run.draw_fanfare` lässt die Item-Symbole über dem Banner
  zusammenfliegen (goldener Glow beim Treffen, „+“ dazwischen). Die Hi-Res-Symbole sammeln sich in `Run._fan_hi` und kommen
  erst **nach** der HUD-Ebene (`top`) in `gfx.HI`, sonst deckt der Banner-Schleier sie ab.
- Runde 42: `Run.slowmo` (Sekunden Echtzeit, dt × 0.3) – gesetzt in `Player.gain_item` beim Wecken einer Synergie.
  Klang `synergy` (Koto-Lauf + Shō + Kane) gab es schon.

# Nächster Schritt: Codex-Sprung zu Synergien
Im Codex (Item-Liste) bei einem Item die Synergien zeigen, an denen es beteiligt ist (bekannte mit Namen, unbekannte als ???),
und mit einer Taste direkt auf die Lexikon-Seite **Synergien** springen. Warum: Die Fanfare macht Synergien jetzt zum
Höhepunkt; als Nächstes soll man gezielt danach suchen können – das trägt den Wiederspielwert.

# Weitere Ideen
- Requisiten Teil 3: eigene Requisiten für `yomi_oku` (Kapitel VII), Grabsteine in Hakaba mit Inschrift/Opfergaben
- Zweiter Weg: Pforte nach **Takamagahara no Oku** mit Amaterasu (Ama-no-Iwato) als Endbossin
- Gesten auch beim Laufstart: die gewählte Figur macht ihre Geste im ersten Raum, bevor die Steuerung freigegeben wird
- Endbildschirm im Titelstil (Nachtschleier, Pinselstrich, Siegel) – letzter Bildschirm ohne neuen Stil
- Transformationen (3 Items gleichen Themas) bekommen dieselbe Fanfare mit den drei Symbolen
