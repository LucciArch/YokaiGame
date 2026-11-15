"""Gyūki (牛鬼): Ochsenkopf auf Spinnenleib – Gerüst von Tsuchigumo, eigener Kopf, dunkelrote Farben."""
import functools
import tsuchigumo as T
from kit import export
import px

for k, v in {'s0': '#0a0610', 's1': '#1e1420', 's2': '#3a2632', 's3': '#5e4048',
             't0': '#3a0c12', 't1': '#7a1a1e', 't2': '#b83a2a'}.items():
    px.col(k, v)

if __name__ == '__main__':
    export('gyuki', functools.partial(T.spider, ox=True), T.WALK, T.ATTACK, review=3)
