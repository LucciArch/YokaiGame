"""Build every item/pickup/projectile/HUD sprite + overview.png (3x on #24202c) + review sheets."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import common, icons_1, icons_2, icons_3, pickups, projectiles, hud
import px

BG = (0x24, 0x20, 0x2c, 255)


def cells():
    out = []
    for grp in ('icons', 'pickups', 'projectiles', 'hud'):
        row = []
        for name, st, fw in common.REG[grp]:
            for i in range(st.width // fw):
                row.append(st.crop((i * fw, 0, (i + 1) * fw, st.height)))
        out.append((grp, row))
    return out


def sheet(groups, scale, per_row, path, gap=4, bg=BG):
    rows = []
    for grp, ims in groups:
        for i in range(0, len(ims), per_row):
            rows.append(ims[i:i + per_row])
    cw = 32 * scale + gap
    Wd = per_row * cw + gap
    Hd = sum(max(im.height for im in r) * scale + gap for r in rows) + gap
    sh = Image.new('RGBA', (Wd, Hd), bg)
    y = gap
    for r in rows:
        h = max(im.height for im in r)
        for i, im in enumerate(r):
            big = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
            sh.alpha_composite(big, (gap + i * cw + (32 - im.width) * scale // 2, y))
        y += h * scale + gap
    sh.save(path)


def main():
    common.REG.clear()
    for mod in (icons_1, icons_2, icons_3, pickups, projectiles, hud):
        mod.build()
    common.REG['icons'].sort(key=lambda t: t[0])
    cs = cells()
    here = common.HERE
    sheet(cs, 3, 11, os.path.join(here, 'overview.png'), gap=6)
    rv = os.path.join(here, '_review'); os.makedirs(rv, exist_ok=True)
    ic = dict(cs)['icons']
    for i in range(0, len(ic), 15):
        sheet([('icons', ic[i:i + 15])], 7, 5, os.path.join(rv, 'icons_%d.png' % (i // 15)), gap=8)
    sheet([c for c in cs if c[0] != 'icons'], 6, 6, os.path.join(rv, 'rest.png'), gap=8)
    sheet(cs, 1, 22, os.path.join(rv, 'actual_1x.png'), gap=4)
    sheet(cs, 2, 22, os.path.join(rv, 'actual_2x.png'), gap=4)
    n = 0
    for grp, lst in common.REG.items():
        for name, st, fw in lst:
            n += 1
            o = px.orphans(st)
            if len(o) > 6:
                print('orphans %s/%s: %d' % (grp, name, len(o)))
    for w in common.WARN:
        print('WARN', w)
    print('built', n, 'sprites')


if __name__ == '__main__':
    main()
