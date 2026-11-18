"""Setzt eine Zwischensequenz zu einer eigenständigen HTML-Datei zusammen: python3 build.py prolog "Die Nacht ohne Morgen"
Ergebnis: out/<name>.html (Artifact/Browser) – daraus rendert render.js das MP4."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
name, title = sys.argv[1], sys.argv[2]
libs = '\n'.join(open(os.path.join(HERE, 'lib', f), encoding='utf-8').read() for f in ('harness.js', 'sound.js', 'kage.js', 'puppets.js'))
scene = open(os.path.join(HERE, name + '.js'), encoding='utf-8').read()
html = open(os.path.join(HERE, 'player.html'), encoding='utf-8').read()
html = html.replace('{{TITLE}}', title).replace('{{LIBS}}', libs).replace('{{SCENE}}', scene)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
open(os.path.join(HERE, 'out', name + '.html'), 'w', encoding='utf-8').write(html)
print('out/%s.html' % name, len(html))
