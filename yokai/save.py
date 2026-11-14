"""Dauerhafter Spielstand: Freischaltungen, Statistiken, Einstellungen."""
import json
import os
from .settings import save_dir

DEFAULT = {
    'version': 1,
    'chars': ['hana'],
    'items': [],            # freigeschaltete (gesperrte) Items
    'achievements': [],
    'seen': [],             # im Codex entdeckte Items
    'bosses': [],           # besiegte Bosse
    'stats': {
        'runs': 0, 'wins': 0, 'deaths': 0, 'kills': 0, 'coins': 0, 'items': 0,
        'oni_deals': 0, 'kami_deals': 0, 'rooms': 0, 'best_floor': 0, 'daikichi': 0,
        'onsen': 0, 'transforms': 0, 'synergies': 0, 'wins_hard': 0, 'true_wins': 0,
        'challenges': 0, 'donations': 0, 'nohit_bosses': 0, 'playtime': 0.0,
    },
    'char_wins': {},
    'transforms_seen': [],
    'synergies_seen': [],
    'hard_unlocked': False,
    'heaven_unlocked': False,
    'daily': {},
    'settings': {'music': 0.55, 'sfx': 0.8, 'fullscreen': False, 'shake': True, 'dmgnums': True},
}


class Save:
    def __init__(self):
        self.path = os.path.join(save_dir(), 'spielstand.json')
        self.data = json.loads(json.dumps(DEFAULT))
        self.load()

    def load(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                d = json.load(f)
            for k, v in d.items():
                if isinstance(v, dict) and isinstance(self.data.get(k), dict):
                    self.data[k].update(v)
                else:
                    self.data[k] = v
        except (OSError, ValueError):
            pass

    def write(self):
        try:
            tmp = self.path + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=1)
            os.replace(tmp, self.path)
        except OSError as e:
            print('Speichern fehlgeschlagen:', e)

    def __getitem__(self, k):
        return self.data[k]

    def __setitem__(self, k, v):
        self.data[k] = v

    def stat(self, k, add=1):
        self.data['stats'][k] = self.data['stats'].get(k, 0) + add

    def add_to(self, k, v):
        if v not in self.data[k]:
            self.data[k].append(v)
            return True
        return False
