"""Raumvorlagen und prozedurale Ebenen-Generierung."""
import random
from collections import deque
from .settings import *

# 13x7 Vorlagen.  . Boden  R Fels  P Grube  S Stacheln  O Topf  L Steinlaterne
#                 e Bodengegner  f Flieger  x beliebiger Gegner
TEMPLATES = [
    ["............."
     , "..e.......e.."
     , "............."
     , "......x......"
     , "............."
     , "..e.......e.."
     , "............."],
    ["............."
     , ".RR.......RR."
     , ".R..e...e..R."
     , "......f......"
     , ".R..e...e..R."
     , ".RR.......RR."
     , "............."],
    ["............."
     , "...R.....R..."
     , "..e.......e.."
     , ".....RRR....."
     , "..e.......e.."
     , "...R.....R..."
     , "............."],
    ["............."
     , ".PPPP...PPPP."
     , ".P..e...e..P."
     , "......f......"
     , ".P..e...e..P."
     , ".PPPP...PPPP."
     , "............."],
    ["............."
     , "..O.......O.."
     , "....e...e...."
     , "...L.....L..."
     , "....e...e...."
     , "..O.......O.."
     , "............."],
    ["............."
     , "....RRRRR...."
     , "..e.......e.."
     , "..R..x.x..R.."
     , "..e.......e.."
     , "....RRRRR...."
     , "............."],
    ["............."
     , ".SS..e.e..SS."
     , ".S.........S."
     , "......x......"
     , ".S.........S."
     , ".SS..e.e..SS."
     , "............."],
    ["............."
     , "..PPP...PPP.."
     , "..PeP...PeP.."
     , "..P.P.f.P.P.."
     , "..PeP...PeP.."
     , "..PPP...PPP.."
     , "............."],
    ["............."
     , ".e.R.....R.e."
     , "...R..f..R..."
     , "...R.....R..."
     , "...R..f..R..."
     , ".e.R.....R.e."
     , "............."],
    ["............."
     , "..f.......f.."
     , "....RR.RR...."
     , "....R...R...."
     , "....RR.RR...."
     , "..f.......f.."
     , "............."],
    ["............."
     , ".OO.......OO."
     , ".O..e.e.e..O."
     , "............."
     , ".O..e.e.e..O."
     , ".OO.......OO."
     , "............."],
    ["............."
     , ".....PPP....."
     , "..e..PPP..e.."
     , "..f..PPP..f.."
     , "..e..PPP..e.."
     , ".....PPP....."
     , "............."],
    ["............."
     , ".RRRR...RRRR."
     , "......e......"
     , "..e..LLL..e.."
     , "......e......"
     , ".RRRR...RRRR."
     , "............."],
    ["............."
     , ".x.........x."
     , "..SSS...SSS.."
     , "..S.......S.."
     , "..SSS...SSS.."
     , ".x.........x."
     , "............."],
    ["............."
     , "..R.R.R.R.R.."
     , ".e.........e."
     , "..R.R.R.R.R.."
     , ".e.........e."
     , "..R.R.R.R.R.."
     , "............."],
    ["............."
     , "......P......"
     , "..e..PPP..e.."
     , ".....PfP....."
     , "..e..PPP..e.."
     , "......P......"
     , "............."],
    ["............."
     , ".f.........f."
     , "............."
     , "...O.O.O.O..."
     , "............."
     , ".f.........f."
     , "............."],
    ["............."
     , ".R.R.....R.R."
     , "...e.....e..."
     , ".R.R..x..R.R."
     , "...e.....e..."
     , ".R.R.....R.R."
     , "............."],
    ["............."
     , "..PPPPPPPPP.."
     , "..P.......P.."
     , "....e.f.e...."
     , "..P.......P.."
     , "..PPPPPPPPP.."
     , "............."],
    ["............."
     , ".L....e....L."
     , "............."
     , "..e..x.x..e.."
     , "............."
     , ".L....e....L."
     , "............."],
    ["............."
     , "..RRR...RRR.."
     , "..R.......R.."
     , "..R.e.x.e.R.."
     , "..R.......R.."
     , "..RRR...RRR.."
     , "............."],
    ["............."
     , "...S.....S..."
     , ".e.S..f..S.e."
     , "...S.....S..."
     , ".e.S..f..S.e."
     , "...S.....S..."
     , "............."],
    ["............."
     , ".PP.......PP."
     , ".PP..e.e..PP."
     , "......x......"
     , ".PP..e.e..PP."
     , ".PP.......PP."
     , "............."],
    ["............."
     , "....O...O...."
     , "..R...e...R.."
     , ".....f.f....."
     , "..R...e...R.."
     , "....O...O...."
     , "............."],
    ["............."
     , ".e...RRR...e."
     , ".....R.R....."
     , "..f.......f.."
     , ".....R.R....."
     , ".e...RRR...e."
     , "............."],
    ["............."
     , "..x.......x.."
     , "...PP...PP..."
     , "....P...P...."
     , "...PP...PP..."
     , "..x.......x.."
     , "............."],
    ["............."
     , ".R.........R."
     , "..R..e.e..R.."
     , "...R.....R..."
     , "..R..e.e..R.."
     , ".R.........R."
     , "............."],
    ["............."
     , ".SSS.....SSS."
     , "....e...e...."
     , "....R...R...."
     , "....e...e...."
     , ".SSS.....SSS."
     , "............."],
    ["............."
     , "..L.......L.."
     , "....f...f...."
     , "............."
     , "....f...f...."
     , "..L.......L.."
     , "............."],
    ["............."
     , ".OOO.....OOO."
     , ".O..x...x..O."
     , "............."
     , ".O..x...x..O."
     , ".OOO.....OOO."
     , "............."],
    ["............."
     , "..R...R...R.."
     , "....e...e...."
     , "..R...R...R.."
     , "....e...e...."
     , "..R...R...R.."
     , "............."],
    ["............."
     , "...PPPPPPP..."
     , ".e.P.....P.e."
     , "...P..x..P..."
     , ".e.P.....P.e."
     , "...PPP.PPP..."
     , "............."],
    ["............."
     , "............."
     , "..RR..e..RR.."
     , "..RR.x.x.RR.."
     , "..RR..e..RR.."
     , "............."
     , "............."],
    ["............."
     , ".e.S.S.S.S.e."
     , "............."
     , "...f.....f..."
     , "............."
     , ".e.S.S.S.S.e."
     , "............."],
    ["............."
     , "..O.R...R.O.."
     , "...e.....e..."
     , ".R....L....R."
     , "...e.....e..."
     , "..O.R...R.O.."
     , "............."],
    ["............."
     , ".PPP.....PPP."
     , ".PPP..e..PPP."
     , "....e...e...."
     , ".PPP..e..PPP."
     , ".PPP.....PPP."
     , "............."],
    ["............."
     , "..f..RRR..f.."
     , ".....R.R....."
     , ".e...R.R...e."
     , ".....R.R....."
     , "..f..RRR..f.."
     , "............."],
    ["............."
     , "...e.....e..."
     , ".RRRR...RRRR."
     , "............."
     , ".RRRR...RRRR."
     , "...e.....e..."
     , "............."],
    ["............."
     , ".x....P....x."
     , "......P......"
     , "..PPPPPPPPP.."
     , "......P......"
     , ".x....P....x."
     , "............."],
    ["............."
     , "..SSSSSSSSS.."
     , "..S..e.e..S.."
     , "......x......"
     , "..S..e.e..S.."
     , "..SSSSSSSSS.."
     , "............."],
    ["............."
     , ".R..O...O..R."
     , "....e...e...."
     , ".O....f....O."
     , "....e...e...."
     , ".R..O...O..R."
     , "............."],
    ["............."
     , "..L.e...e.L.."
     , "............."
     , "....L.x.L...."
     , "............."
     , "..L.e...e.L.."
     , "............."],
    ["............."
     , ".PP..RRR..PP."
     , ".P..e...e..P."
     , "......f......"
     , ".P..e...e..P."
     , ".PP..RRR..PP."
     , "............."],
    ["............."
     , "....e.e.e...."
     , "..R.......R.."
     , "..R.......R.."
     , "..R.......R.."
     , "....e.e.e...."
     , "............."],
    ["............."
     , ".e.........e."
     , "..R..PPP..R.."
     , "..R..PPP..R.."
     , "..R..PPP..R.."
     , ".e.........e."
     , "............."],
    ["............."
     , ".......O....."
     , "..x.R...R.x.."
     , ".O...SSS...O."
     , "..x.R...R.x.."
     , ".....O......."
     , "............."],
    ['.............' , '.RRR.....RRR.' , '.R.........R.' , '...e.x.x.e...' , '.R.........R.' , '.RRR.....RRR.' , '.............'],
    ['.............' , '..P.P.P.P.P..' , '.e.........e.' , '......f......' , '.e.........e.' , '..P.P.P.P.P..' , '.............'],
    ['.............' , '.O.O.O.O.O.O.' , '.............' , '..e..LLL..e..' , '.............' , '.O.O.O.O.O.O.' , '.............'],
    ['.............' , '...RRR.RRR...' , '..R.e...e.R..' , '..R...f...R..' , '..R.e...e.R..' , '...RRR.RRR...' , '.............'],
    ['.............' , '.SSSSS.SSSSS.' , '.....e.e.....' , '..f.......f..' , '.....e.e.....' , '.SSSSS.SSSSS.' , '.............'],
    ['.............' , '.PPPPP.PPPPP.' , '.PPPPP.PPPPP.' , '..f.......f..' , '.PPPPP.PPPPP.' , '.PPPPP.PPPPP.' , '.............'],
    ['.............' , '..x.R...R.x..' , '....R...R....' , '..RRR...RRR..' , '....R...R....' , '..x.R...R.x..' , '.............'],
    ['.............' , '.L.e.....e.L.' , '...RR...RR...' , '......x......' , '...RR...RR...' , '.L.e.....e.L.' , '.............'],
    ['.............' , '..e...O...e..' , '.OOO.....OOO.' , '......f......' , '.OOO.....OOO.' , '..e...O...e..' , '.............'],
    ['.............' , '.e..P...P..e.' , '...PPP.PPP...' , '....P...P....' , '...PPP.PPP...' , '.e..P...P..e.' , '.............'],
    ['.............' , '..R.......R..' , '.RxR.....RxR.' , '..R.......R..' , '.RxR.....RxR.' , '..R.......R..' , '.............'],
    ['.............' , '.f.S.....S.f.' , '...S..e..S...' , '..SS.....SS..' , '...S..e..S...' , '.f.S.....S.f.' , '.............'],
    ['.............' , '....e...e....' , '.RR.......RR.' , '.RR..LLL..RR.' , '.RR.......RR.' , '....e...e....' , '.............'],
    ['.............' , '..PPP...PPP..' , '..PxP...PxP..' , '..P.......P..' , '..PxP...PxP..' , '..PPP...PPP..' , '.............'],
    ['.............' , '.e.O.O.O.O.e.' , '.............' , '....RR.RR....' , '.............' , '.e.O.O.O.O.e.' , '.............'],
    ['.............' , '..f.......f..' , '.....RRR.....' , '..e.R...R.e..' , '.....RRR.....' , '..f.......f..' , '.............'],
    ['.............' , '.SS.SS.SS.SS.' , '..x.......x..' , '.............' , '..x.......x..' , '.SS.SS.SS.SS.' , '.............'],
    ['.............' , '.R.R.R.R.R.R.' , '..e.......e..' , '.R.R..f..R.R.' , '..e.......e..' , '.R.R.R.R.R.R.' , '.............'],
    ['.............' , '....PPPPP....' , '..e.P...P.e..' , '....P.x.P....' , '..e.P...P.e..' , '....PP.PP....' , '.............'],
    ['.............' , '.x....L....x.' , '..RR.....RR..' , '.............' , '..RR.....RR..' , '.x....L....x.' , '.............'],
    ['.............' , '.x.R.x.x.R.x.' , '...R.....R...' , '.PPP..f..PPP.' , '...R.....R...' , '.x.R.x.x.R.x.' , '.............'],
    ['.............' , '..xSSSSSSSx..' , '..S.......S..' , '.....fxf.....' , '..S.......S..' , '..xSSSSSSSx..' , '.............'],
    ['.............' , '.RRx.....xRR.' , '.R..PPPPP..R.' , '....P.x.P....' , '.R..PPPPP..R.' , '.RRx.....xRR.' , '.............'],
    ['.............' , '..e.x.e.x.e..' , '.OOOO...OOOO.' , '......f......' , '.OOOO...OOOO.' , '..e.x.e.x.e..' , '.............'],
    ['.............' , '.f.f.....f.f.' , '..LL.....LL..' , '....x.x.x....' , '..LL.....LL..' , '.f.f.....f.f.' , '.............'],
    ['.............' , '.PxP.PxP.PxP.' , '.P.P.P.P.P.P.' , '.............' , '.P.P.P.P.P.P.' , '.PxP.PxP.PxP.' , '.............'],
    ['.............' , '...RRR.RRR...' , '.x.R.x.x.R.x.' , '...R..f..R...' , '.x.R.x.x.R.x.' , '...RRR.RRR...' , '.............'],
    ['.............' , '.SxS.....SxS.' , '.SSS.RRR.SSS.' , '......x......' , '.SSS.RRR.SSS.' , '.SxS.....SxS.' , '.............'],
    ['.............' , 'x...........x' , '..PPPP.PPPP..' , '..P..fxf..P..' , '..PPPP.PPPP..' , 'x...........x' , '.............'],
    ['.............' , '.e.e.e.e.e.e.' , '.............' , '..R.R.R.R.R..' , '.............' , '.e.e.e.e.e.e.' , '.............'],
    # --- v1.3: Räume für tiefere Kapitel
    ["......P......"
     , ".e....P....e."
     , "PPPP..P..PPPP"
     , "......x......"
     , "PPPP..P..PPPP"
     , ".e....P....e."
     , "......P......"],
    ["............."
     , ".L.SSS.SSS.L."
     , "..e.......e.."
     , ".S...f.f...S."
     , "..e.......e.."
     , ".L.SSS.SSS.L."
     , "............."],
    ["............."
     , ".RRR.RRR.RRR."
     , ".e.R..e..R.e."
     , ".R.....x...R."
     , ".e.R..e..R.e."
     , ".RRR.RRR.RRR."
     , "............."],
    ["PP.........PP"
     , "P..PP...PP..P"
     , "..eP.....Pe.."
     , "......f......"
     , "..eP.....Pe.."
     , "P..PP...PP..P"
     , "PP.........PP"],
    ["............."
     , ".OO..e.e..OO."
     , ".O.........O."
     , "....RRxRR...."
     , ".O.........O."
     , ".OO..e.e..OO."
     , "............."],
    ["......P......"
     , "..e...P...e.."
     , "..RRR.P.RRR.."
     , "PPP.f.x.f.PPP"
     , "..RRR.P.RRR.."
     , "..e...P...e.."
     , "......P......"],
    ["............."
     , "...SSSSSSS..."
     , "..S..e.e..S.."
     , "..S...x...S.."
     , "..S..e.e..S.."
     , "...SSSSSSS..."
     , "............."],
    ["R...........R"
     , ".R..e....e.R."
     , "..R.......R.."
     , "....f.x.f...."
     , "..R.......R.."
     , ".R..e....e.R."
     , "R...........R"],
    ["............."
     , ".L.R.R.R.R.L."
     , "..e.......e.."
     , "....f...f...."
     , "..e.......e.."
     , ".L.R.R.R.R.L."
     , "............."],
    ["RRRRR...RRRRR"
     , "R...e...e...R"
     , "R..PPP.PPP..R"
     , "......x......"
     , "R..PPP.PPP..R"
     , "R...e...e...R"
     , "RRRRR...RRRRR"],
    [".....R.R....."
     , ".e...R.R...e."
     , ".....R.R....."
     , "..f..x.x..f.."
     , ".....R.R....."
     , ".e...R.R...e."
     , ".....R.R....."],
    ["............."
     , "..e.......e.."
     , "....PPPPP...."
     , "..f.PPPPP.f.."
     , "....PPPPP...."
     , "..e.......e.."
     , "............."],
    ["............."
     , ".SSSSS.SSSSS."
     , "..e...f...e.."
     , "......x......"
     , "..e...f...e.."
     , ".SSSSS.SSSSS."
     , "............."],
    ["............."
     , ".R.R.R.R.R.R."
     , "..e..x..e...."
     , "............."
     , "....e..x..e.."
     , ".R.R.R.R.R.R."
     , "............."],
    [".....RRR....."
     , "..e..f.f..e.."
     , ".R.........R."
     , ".R.e.xxx.e.R."
     , ".R.........R."
     , "..e..f.f..e.."
     , ".....RRR....."],
    [".L....L....L."
     , "...e.....e..."
     , ".L....f....L."
     , "...e..x..e..."
     , ".L....f....L."
     , "...e.....e..."
     , ".L....L....L."],
]

# Spezialraum-Layouts (ohne Gegner)
SPECIAL_LAYOUTS = {
    'treasure': ["............."
                 , "..L.......L.."
                 , "............."
                 , "............."
                 , "............."
                 , "..L.......L.."
                 , "............."],
    'shop': ["............."
             , ".L.........L."
             , "............."
             , "............."
             , "............."
             , ".L.........L."
             , "............."],
    'boss': ["............."
             , "............."
             , "............."
             , "............."
             , "............."
             , "............."
             , "............."],
    'start': ["............."
              , ".L.........L."
              , "............."
              , "............."
              , "............."
              , ".L.........L."
              , "............."],
}

CH = {'.': T_FLOOR, 'R': T_ROCK, 'P': T_PIT, 'S': T_SPIKE, 'O': T_POT, 'L': T_LANTERN,
      'e': T_FLOOR, 'f': T_FLOOR, 'x': T_FLOOR}

CLEAR_CELLS = [(6, 0), (6, 1), (6, 6), (6, 5), (0, 3), (1, 3), (12, 3), (11, 3), (6, 3)]


def parse(tpl, rng, mirror=True):
    rows = [list(r) for r in tpl]
    if mirror and rng.random() < 0.5:
        rows = [r[::-1] for r in rows]
    if mirror and rng.random() < 0.5:
        rows = rows[::-1]
    tiles = [[CH.get(c, 0) for c in r] for r in rows]
    spawns = []
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c in 'efx':
                spawns.append((x, y, c))
    for x, y in CLEAR_CELLS:
        if tiles[y][x] != T_FLOOR:
            tiles[y][x] = T_FLOOR
    _ensure_connected(tiles)
    return tiles, spawns


def _ensure_connected(tiles):
    """Sorgt dafür, dass alle Türen zueinander erreichbar sind (Gruben/Felsen ggf. entfernen)."""
    def walk(t):
        return t in (T_FLOOR, T_SPIKE)
    start = (6, 3)
    for door in [(6, 0), (6, 6), (0, 3), (12, 3)]:
        seen = {start}
        q = deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in seen and walk(tiles[ny][nx]):
                    seen.add((nx, ny)); q.append((nx, ny))
        if door not in seen:
            # Gerade Linie freiräumen
            x, y = start
            while (x, y) != door:
                if x != door[0]:
                    x += 1 if door[0] > x else -1
                elif y != door[1]:
                    y += 1 if door[1] > y else -1
                if not walk(tiles[y][x]):
                    tiles[y][x] = T_FLOOR


def random_layout(rng):
    """Prozeduraler symmetrischer Raum für noch mehr Abwechslung."""
    rows = [['.'] * 13 for _ in range(7)]
    kinds = rng.choice(['R', 'P', 'O', 'S', 'R', 'L'])
    kind2 = rng.choice(['R', 'P', 'O', '.', '.'])
    for _ in range(rng.randint(3, 8)):
        x, y = rng.randint(1, 5), rng.randint(1, 2)
        c = kinds if rng.random() < 0.7 else kind2
        for mx, my in ((x, y), (12 - x, y), (x, 6 - y), (12 - x, 6 - y)):
            rows[my][mx] = c
    for _ in range(rng.randint(2, 4)):
        x, y = rng.randint(1, 5), rng.randint(1, 2)
        sym = rng.choice('efx')
        rows[y][x] = sym
        rows[6 - y][12 - x] = sym
    return [''.join(r) for r in rows]


class Room:
    def __init__(self, pos, kind):
        self.pos = pos
        self.kind = kind          # start normal boss treasure shop challenge curse omikuji onsen
        self.doors = {}            # dir -> Nachbarraum-pos
        self.tiles = None
        self.spawns = []
        self.cleared = kind not in ('normal', 'boss', 'challenge', 'dojo')
        self.visited = False
        self.seen = False
        self.objects = []          # persistente Pickups/Sockel etc. (gespeichert beim Verlassen)
        self.locked = False
        self.layout_seed = 0
        self.populated = False
        self.boss_id = None
        self.extra = {}
        self.revealed = kind != 'secret'


def generate_floor(rng, depth, labyrinth=False, hard=False):
    """Isaac-artige Ebenen: Räume auf einem 9x9 Raster."""
    target = min(22, 7 + depth * 2 + rng.randint(0, 2) + (5 if labyrinth else 0))
    for attempt in range(200):
        grid = {}
        start = (4, 4)
        grid[start] = True
        q = deque([start])
        while q and len(grid) < target:
            cx, cy = q.popleft()
            dirs = list(DIRS.values())
            rng.shuffle(dirs)
            for dx, dy in dirs:
                n = (cx + dx, cy + dy)
                if len(grid) >= target:
                    break
                if not (0 <= n[0] < 9 and 0 <= n[1] < 9) or n in grid:
                    continue
                if rng.random() < 0.5:
                    continue
                neigh = sum(1 for ddx, ddy in DIRS.values() if (n[0] + ddx, n[1] + ddy) in grid)
                if neigh > 1:
                    continue
                grid[n] = True
                q.append(n)
            if not q and len(grid) < target:
                q.append(rng.choice(list(grid.keys())))
        if len(grid) < target:
            continue
        def neighbours(p):
            return [(p[0] + dx, p[1] + dy) for dx, dy in DIRS.values() if (p[0] + dx, p[1] + dy) in grid]
        dead = [p for p in grid if p != start and len(neighbours(p)) == 1]
        if len(dead) < 4:
            continue
        # Distanzen
        dist = {start: 0}
        q = deque([start])
        while q:
            p = q.popleft()
            for n in neighbours(p):
                if n not in dist:
                    dist[n] = dist[p] + 1
                    q.append(n)
        dead.sort(key=lambda p: -dist[p])
        boss = dead[0]
        if dist[boss] < 3:
            continue
        rest = dead[1:]
        rng.shuffle(rest)
        rooms = {}
        for p in grid:
            rooms[p] = Room(p, 'normal')
        rooms[start] = Room(start, 'start')
        rooms[boss] = Room(boss, 'boss')
        rooms[rest[0]].kind = 'treasure'
        rooms[rest[1]].kind = 'shop'
        extras = ['challenge', 'curse', 'omikuji', 'onsen', 'treasure2', 'library', 'dojo', 'teahouse', 'slots']
        rng.shuffle(extras)
        for p, k in zip(rest[2:], extras):
            if k == 'treasure2':
                if depth >= 2 and rng.random() < 0.5:
                    rooms[p].kind = 'treasure'
            elif k == 'library' and depth < 2:
                continue
            else:
                rooms[p].kind = k
        for r in rooms.values():
            r.cleared = r.kind not in ('normal', 'boss', 'challenge', 'dojo')
            r.layout_seed = rng.randrange(1 << 30)
            r.depth = depth
            for d, (dx, dy) in DIRS.items():
                n = (r.pos[0] + dx, r.pos[1] + dy)
                if n in rooms:
                    r.doors[d] = n
            if r.kind == 'treasure' and depth >= 2:
                r.locked = True
        # Geheimraum: leere Zelle neben mindestens zwei Räumen (nicht neben Boss)
        cands = []
        for x in range(9):
            for y in range(9):
                if (x, y) in rooms:
                    continue
                ns = [(x + dx, y + dy) for dx, dy in DIRS.values() if (x + dx, y + dy) in rooms]
                if not ns or any(rooms[n].kind in ('boss',) for n in ns):
                    continue
                cands.append((len(ns), rng.random(), (x, y)))
        if cands:
            cands.sort(reverse=True)
            pos = cands[0][2]
            sr = Room(pos, 'secret')
            sr.layout_seed = rng.randrange(1 << 30)
            rooms[pos] = sr
            for d, (dx, dy) in DIRS.items():
                n = (pos[0] + dx, pos[1] + dy)
                if n in rooms and n != pos:
                    sr.doors[d] = n
                    rooms[n].doors[OPP[d]] = pos
        return rooms, start, boss
    raise RuntimeError('Ebenen-Generierung fehlgeschlagen')


def build_room_tiles(room, rng):
    if room.kind in ('normal', 'challenge', 'dojo'):
        if rng.random() < 0.22:
            tpl = random_layout(rng)
        else:
            pool = TEMPLATES if getattr(room, 'depth', 3) >= 3 else TEMPLATES[:66] if getattr(room, 'depth', 3) < 2 else TEMPLATES[:76]
            tpl = rng.choice(pool)
        room.tiles, room.spawns = parse(tpl, rng)
    elif room.kind == 'secret':
        tpl = ["............."
               , ".O.........O."
               , "............."
               , "............."
               , "............."
               , ".O.........O."
               , "............."]
        room.tiles, room.spawns = parse(tpl, rng, mirror=False)
    elif room.kind == 'curse':
        tpl = ["............."
               , ".SSS.....SSS."
               , ".S.........S."
               , "............."
               , ".S.........S."
               , ".SSS.....SSS."
               , "............."]
        room.tiles, room.spawns = parse(tpl, rng, mirror=False)
    else:
        tpl = SPECIAL_LAYOUTS.get(room.kind, SPECIAL_LAYOUTS['treasure'])
        room.tiles, room.spawns = parse(tpl, rng, mirror=False)
