"""Lesbare Texte für Item-Effekte."""
import math
import pygame

FX_NAMES = {
    'dmg': ('Schaden', '+'), 'dmgm': ('Schaden', '×'), 'rate': ('Feuerrate', '+'), 'ratem': ('Feuerrate', '×'),
    'spd': ('Lauftempo', '+'), 'shotspd': ('Schussgeschwindigkeit', '+'), 'range': ('Reichweite', '+'), 'luck': ('Glück', '+'),
    'w_sword': ('Angriff: Schwerthieb', ''), 'w_spear': ('Angriff: Speerstoß', ''), 'w_scythe': ('Angriff: Sensenwirbel', ''),
    'w_laser': ('Angriff: Lichtstrahl', ''), 'w_bow': ('Angriff: Pfeile', ''), 'w_club': ('Angriff: Keulenschlag', ''),
    'w_fan': ('Angriff: Windfächer', ''), 'sword_wave': ('Hiebe senden eine Schwertwelle', ''),
    'size': ('Talismangröße', '+'), 'hp': ('Herzcontainer', '+'), 'heal': ('Heilt ½ Herzen', 'n'),
    'spirit': ('Geisterherzen (½)', '+'), 'coins': ('Mon', '+'), 'keys': ('Schlüssel', '+'), 'salts': ('Reinigungssalz', '+'),
    'fullheal': ('Heilt alle Herzen', ''), 'homing': ('Talismane suchen ihr Ziel', ''),
    'pierce': ('Talismane durchbohren Feinde', ''), 'bounce': ('Talismane prallen von Wänden ab', ''),
    'spectral': ('Talismane fliegen durch Hindernisse', ''), 'explode': ('Talismane explodieren', ''),
    'burn': ('Talismane setzen Feinde in Brand', ''), 'slow': ('Talismane verlangsamen Feinde', ''),
    'poison': ('Talismane vergiften Feinde', ''), 'chain': ('Treffer springen als Blitz weiter', ''),
    'split': ('Talismane teilen sich beim Treffer', ''), 'boomerang': ('Talismane kehren zurück', ''),
    'wave': ('Talismane fliegen in Wellen', ''), 'knock': ('Stärkerer Rückstoß', ''), 'crit': ('Chance auf doppelten Schaden', '%'),
    'freeze': ('Chance, Feinde einzufrieren', '%'), 'multishot': ('Zusätzliche Talismane pro Wurf', '+'),
    'back': ('Talisman nach hinten', '+'), 'side': ('Talismane zu beiden Seiten', '+'),
    'orbital': ('Kreisende Schilde, die Geschosse blocken', '+'), 'familiar': ('Shikigami-Begleiter, die mitschießen', '+'),
    'aura': ('Schadensaura um dich herum', '+'), 'fly': ('Du fliegst über Gruben und Stacheln', ''),
    'dash_fire': ('Die Rolle hinterlässt Feuer', ''), 'dash_dmg': ('Die Rolle verletzt Feinde', ''),
    'dash_reflect': ('Die Rolle löscht Geschosse', ''), 'hurt_ring': ('Bei Treffer: Talismanring', ''),
    'hurt_dmg': ('Nach einem Treffer kurz mehr Schaden', ''), 'kill_heal': ('Chance auf Heilung pro Kill', '%'),
    'kill_explode': ('Chance, dass Feinde explodieren', '%'), 'clear_heal': ('Chance auf Heilung pro Raum', '%'),
    'money_dmg': ('Mehr Schaden, je mehr Mon du hast', ''), 'shield': ('Blockt den ersten Treffer pro Raum', ''),
    'revive': ('Extra-Leben', '+'), 'map': ('Zeigt die ganze Karte', ''), 'magnet': ('Zieht Münzen und Schlüssel an', ''),
    'discount': ('Laden-Rabatt', ''), 'gold_shots': ('Chance auf goldene Talismane (Münzen)', '%'),
    'big_every': ('Jeder N. Schuss ist mächtig', ''), 'rage': ('Mehr Schaden bei wenig Leben', ''),
    'salts_regen': ('Chance auf Salz pro Raum', '%'), 'curse_immune': ('Immun gegen Flüche', ''),
    'raijin_chance': ('Chance, dass ein Blitz einschlägt', '%'),
}
from .sigs import TEXT as _SIG
for _k, _v in _SIG.items():
    FX_NAMES['sig_' + _k] = (_v, '')
TAG_NAMES = {'kitsune': 'Kitsune', 'raijin': 'Donner', 'oni': 'Oni', 'shikigami': 'Shikigami', 'yurei': 'Yūrei',
             'tengu': 'Tengu', 'ryu': 'Drache', 'kami': 'Kami', 'tanuki': 'Tanuki'}


def star(s, x, y, col):
    pts = []
    for i in range(10):
        a = i / 10 * math.tau - math.pi / 2
        r = 3.5 if i % 2 == 0 else 1.5
        pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
    pygame.draw.polygon(s, col, pts)


def fx_lines(fx):
    out = []
    for k, v in fx.items():
        if k not in FX_NAMES:
            continue
        n, m = FX_NAMES[k]
        if m == '+':
            out.append('%s %s%g' % (n, '+' if v > 0 else '', v) if k not in ('hp', 'revive') else '%s%g %s' % ('+' if v > 0 else '', v, n))
        elif m == '×':
            out.append('%s ×%g' % (n, v))
        elif m == 'n':
            out.append(n.replace('½', '%g' % (v / 2)))
        elif m == '%':
            out.append('%s: %d %%' % (n, round(v * 100)))
        else:
            out.append(n if k != 'big_every' else 'Jeder %d. Talisman ist dreifach stark' % v)
    return out
