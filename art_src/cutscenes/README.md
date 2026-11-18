# Zwischensequenzen (Schattenspiel)

Story-Videos im Stil „Shadow Puppet Theatre“ (Scherenschnitt vor einer beleuchteten Leinwand). Alles wird im Browser
aus Code berechnet, jedes Bild ist eine reine Funktion der Zeit; die Töne sind synthetisiert (keine fremden Dateien).

- `lib/harness.js`, `lib/sound.js` – Hilfsbibliothek und Klang-Kit (unverändert aus der Stilvorlage)
- `lib/kage.js` – Bühne: Lampe, Tuchgewebe, Gelfolien, Körnung, Schilder, Ranken, Vorhänge
- `lib/puppets.js` – Figuren (Oni, Kasa-obake, Chōchin-obake, Rokurokubi, Hana, Torii, Schrein, Suzu …)
- `<kapitel>.js` – Drehbuch: `explainer(ctx, W, H, t)`, `scoreSound(k)`, `DURATION`
- `player.html` – Abspielseite (Vorlage)

Bauen und rendern (Chromium/Playwright + ffmpeg):

    python3 build.py prolog "Die Nacht ohne Morgen"     # -> out/prolog.html
    node shots.js out/prolog.html 2,8,15 /tmp/probe     # Standbilder zur Kontrolle
    node render.js out/prolog.html out/prolog.mp4 30    # -> MP4 mit Ton
