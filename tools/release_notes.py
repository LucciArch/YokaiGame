"""Schreibt release_notes.md: Download-Hinweis + Changelog-Abschnitt der aktuellen Version."""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, ROOT)
from yokai.settings import VERSION  # noqa: E402

log = open(os.path.join(ROOT, 'CHANGELOG.md'), encoding='utf-8').read()
m = re.search(r'^## ' + re.escape(VERSION) + r'.*?$(.*?)(?=^## |\Z)', log, re.S | re.M)
section = m.group(1).strip() if m else ''
head = re.search(r'^## (' + re.escape(VERSION) + r'.*?)$', log, re.M)
out = ['**Herunterladen:** `YokaiNoMichi.exe` unten anklicken, speichern, doppelklicken – fertig.',
       'Windows SmartScreen kann beim ersten Start warnen („Unbekannter Herausgeber“): *Weitere Informationen → Trotzdem ausführen*.',
       '']
if section:
    out += ['### Neu in ' + (head.group(1) if head else VERSION), '', section]
open(os.path.join(ROOT, 'release_notes.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('release_notes.md:', len(section), 'Zeichen Changelog')
