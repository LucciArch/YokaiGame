# Art Bible – Yōkai no Michi

*Erstellt nach dem CCGS-Ablauf `/art-bible` (9 Abschnitte). Gilt für alle neuen Grafiken.
Technische Detailregeln für Sprites stehen in `art_src/fable/STYLE_GUIDE.md`.*

## 1. Visuelle Identität

**Leitsatz:** *Ein warmes Licht in einer kalten Mondnacht.*

- **Lesbarkeit vor Pracht** – Figuren, Gegner und Geschosse sind die hellsten, schärfsten
  Dinge auf dem Bildschirm; Boden und Wände bleiben dunkel und ruhig.
  *Test:* Wenn ein Detail im Kampf mit einem Geschoss verwechselt werden kann, kommt es weg.
- **Folklore statt Fantasy** – Formen kommen aus der Edo-Bildwelt (Toriyama Sekien,
  Ukiyo-e): Tōrō-Laternen, Shimenawa-Seile, Ofuda-Siegel, Torii. Keine westlichen Burgen,
  keine generischen Kristalle.
- **Eine Pixeldichte** – alles, was im Spielfeld steht oder sich bewegt, wird auf der
  Hi-Res-Ebene gezeichnet (doppelte Dichte, 1-px-Umriss). Nur Boden, Wände und Gruben
  liegen auf der Grundebene.

## 2. Stimmung je Spielzustand

| Zustand | Gefühl | Licht | Träger der Stimmung |
|---|---|---|---|
| Erkunden | gespannte Stille | kühles Mondlicht von oben links, warme Laternen | Regen, Glühwürmchen, Blätter |
| Kampf | Druck, Tempo | Geschosse und Augen leuchten, Rest bleibt dunkel | Bildschirmwackeln, Treffer-Blitz |
| Boss | Ehrfurcht | Biom-Farbe gesättigt, rote Rahmenlinien beim Intro | Porträt-Intro, Taiko-Musik |
| Schrein (Kami/Oni) | Versuchung | Gold-Weiß bzw. Blutrot | Wechsel der Bodenfarbe |
| Sieg/Epilog | Erlösung | Morgendämmerung, warme Töne | aufgehende Sonne, Kirschblüten |
| Tod | stille Trauer | entsättigt, dunkel | Porträt, Gong |

## 3. Formensprache

- **Spielfigur:** aufrechte, kompakte Silhouette; Kopf groß genug, um Kostümteile zu tragen.
- **Gegner:** jede Art hat ihre eigene Silhouette (Schirm = Dreieck auf einem Bein,
  Nurikabe = Rechteck, Ittan-momen = langes Band). Keine Gegnerart ist ein umgefärbter Klon.
- **Bosse:** übergroß, oft gegliedert (Schlangenleiber als Röhren, Knochenarme), damit
  Trefferzonen lesbar sind.
- **Umgebung:** gerade, schwere Formen (Stein, Holz); Kurven nur bei Natur (Bambus, Wolken).
- **Oberfläche (HUD):** schlichte Rahmen mit Doppellinie, erinnert an lackierte Holztafeln.

## 4. Farbsystem

| Farbe | Bedeutung |
|---|---|
| Gold/Gelb `#ffe24a` | Belohnung, Licht, Items, Münzen |
| Rot `#c02634` / `#ff5a3c` | Gefahr, Gegneraugen, Oni, Schaden |
| Blau `#3f8ae8` / `#9fe0ff` | Geist, Wasser, Seelenherzen |
| Weiß/Papier `#d4dcf4` | Ofuda, Heiliges, Kami |
| Violett `#474c94` | Schatten, Nacht, Unterwelt |

- Schatten wandern ins Blau-Violette, Lichter ins Warme.
- Jedes Biom hat eine eigene Grundtemperatur (Bambuswald grün-kalt, Höllenfeuer rot-warm,
  Himmelsgefilde hell-gold). Die Biom-Farbe färbt nur Boden und Wände.
- **Farbschwäche:** Gegnergeschosse unterscheiden sich von eigenen auch in der Form
  (eigene = Ofuda/Klinge, gegnerische = runde Kugeln mit dunklem Kern).

## 5. Figuren

- Seitenansicht/¾, Blick nach links im Quellbild, wird gespiegelt.
- 3–4 Farbstufen pro Material, Licht oben links, Mondlicht-Kante oben/links.
- Kostüme aus Items werden **auf die Figur gezeichnet** (Kopf-Ankerpunkte je Figur), nie schwebend.
- Größenklassen: kleine Yōkai ≈ 20–28, Figuren ≈ 24–28, große Gegner bis 55 Weltpixel hoch.

## 6. Umgebung

- Boden: dunkel, wenig Kontrast, kleine Muster – er ist Bühne, nicht Darsteller.
- Stehende Requisiten (Felsen, Urnen, Tōrō-Laternen, Statuen) sind Hi-Res, werfen einen
  Bodenschatten nach unten rechts und werden mit den Figuren nach Tiefe sortiert.
- Jede Requisite erzählt etwas über das Biom: Kitsune-Statuen am Inari-Pfad,
  Grabsteine am Friedhof, Kessel im Höllenfeuer.

## 7. HUD und Menüs

- Kunst: Holztafel-Rahmen, warme Schrift auf dunklem Grund, Symbole als kleine Pixelbilder.
- UX: Text nie kleiner als Stufe 6; Kampf-HUD nur am Rand; Tooltips über Items mit Name,
  Satz und Werten. Kein Element überdeckt die Spielfigur.

## 8. Asset-Standards

- PNG, harte Alpha (0/255), keine Kantenglättung.
- Sprites als Streifen, Blick nach links; Hi-Res-Requisiten 64×64 pro Feld (`*_hi.png`).
- Alles wird per Skript in `art_src/` erzeugt – nie ein exportiertes PNG von Hand ändern.
- Musik OGG (Vorbis), SFX OGG mit 2–3 Varianten.

## 9. Bezugspunkte

| Quelle | Übernehmen | Vermeiden |
|---|---|---|
| Toriyama Sekiens Yōkai-Bücher | Silhouetten und Merkmale der Yōkai | Holzschnitt-Linien als Stil |
| *Enter the Gungeon* | Lesbarkeit von Geschossen, Raumgrößen | Waffen-Humor, Figurendesign |
| *The Binding of Isaac* | Item-Kostüme sichtbar am Körper | Ekel-Ästhetik |
| *Muramasa* (Vanillaware) | warme Lichtakzente in dunkler Nacht | gemalte Hi-Fi-Grafik |
