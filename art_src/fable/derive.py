"""Ableitungen per Paletten-Tausch aus vorhandenen handgesetzten Figuren (gleiches Gerüst, neue Materialien)."""
import importlib, os, sys
BASE = '/home/claude/fable_art'
JOBS = {
    # neuer Name: (Ordner, Modul, Zeichenfunktion, Farb-Überschreibungen)
    # 'boss_shuten_doji' hat jetzt eine eigene Figur (bosses_1/boss_shuten.py)
    'hyosube': ('', 'kappa', 'kappa', {'g0': '#160a0c', 'g1': '#3a2016', 'g2': '#64402a', 'g3': '#946a44', 'g4': '#c49c6c',
                                         'a0': '#3a2016', 'a1': '#64402a', 'a2': '#946a44', 'xg': '#d8b890'}),
    'bake_danuki': ('heroes', 'ponpoko', 'ponpoko', {'s0': '#120c16', 's1': '#2e2228', 's2': '#54423e', 's3': '#86705a',
                                                   'c0': '#3a1420', 'c1': '#6a2430', 'c2': '#a84a3a'}),
    # 'gyuki' hat jetzt eine eigene Datei (enemies_3/gyuki.py, Ochsenkopf)
    '_gyuki_alt': ('enemies_3', 'tsuchigumo', 'spider', {'s0': '#0a0610', 's1': '#1e1420', 's2': '#3a2632', 's3': '#5e4048',
                                                     't0': '#3a0c12', 't1': '#7a1a1e', 't2': '#b83a2a'}),
    'boss_raiju': ('enemies_4', 'kasha', 'draw', {'h0': '#0e1a4a', 'h1': '#2a54b0', 'h2': '#8ac8ff',
                                                  'f0': '#1a3ab0', 'f1': '#7ac8ff', 'f2': '#fff6a0'}),
    'boss_mikaboshi': ('heroes', 'seimei', 'seimei', {'v0': '#0a0820', 'v1': '#1e1a48', 'v2': '#3a3478', 'v3': '#ffe24a'}),
    'boss_oonyudo': ('heroes', 'benkei', 'benkei', {}),
}


def run(name):
    folder, mod, fn, cols = JOBS[name]
    repo = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
    d = repo if folder and os.path.isdir(repo) else (os.path.join(BASE, folder) if folder else BASE)   # Repo-Quellen zuerst
    os.chdir(d)
    sys.path.insert(0, d)
    m = importlib.import_module(mod)
    import px
    for k, v in cols.items():
        px.col(k, v)
    f = getattr(m, fn)
    if hasattr(m, 'export'):
        m.export(name, f, m.WALK, m.ATTACK)
    else:
        # Meisterfiguren (oni/kappa): eigene Ausgabe
        from px import crop_img, strip
        crop_img(f().img()).save(os.path.join(d, name + '.png'))
        strip([f(**k).img() for k in m.WALK], os.path.join(d, name + '_walk.png'))
        strip([f(**k).img() for k in m.ATTACK], os.path.join(d, name + '_attack.png'))
    print('ok', name)


if __name__ == '__main__':
    run(sys.argv[1])
