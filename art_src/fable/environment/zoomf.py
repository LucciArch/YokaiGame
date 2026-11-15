import sys, random
from floors import *
names = sys.argv[2:]
out = sys.argv[1]
sheet = Image.new('RGBA', (2 * 584, ((len(names) + 1) // 2) * 392), (0, 0, 0, 255))
for n, name in enumerate(names):
    tl = floor_tiles(name)
    rng = random.Random(name + 'z')
    room = Cv(6 * T, 4 * T)
    k = 0
    for j in range(4):
        for i in range(6):
            t = tl[rng.randint(0, 3)]
            if (i, j) in ((1, 1), (4, 2)):
                t = tl[4 + k]; k += 1
            room.a[j * T:(j + 1) * T, i * T:(i + 1) * T] = t.a
    im = room.img().resize((576, 384), Image.NEAREST)
    sheet.paste(im, ((n % 2) * 584, (n // 2) * 392))
sheet.save(out)
