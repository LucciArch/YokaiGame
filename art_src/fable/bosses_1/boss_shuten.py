"""Shuten-dōji – König der Oni vom Ōeyama. Eigene Figur (Runde 111) statt Umfärbung des Oni:
größer gebaut (Riese, gleiche Pixeldichte), lange weiße Mähne, über den Schultern ein offener Haori in Rot-Gold
mit Wappen und weiten Ärmeln, Gürtel mit Strick; in der fernen Hand die riesige Sake-Kalebasse als Keule,
in der nahen Hand die rote Sake-Schale. Angriff: schwingt die Kalebasse."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shuten_body as SB
from shuten_body import *
import shuten_body as SB
from bl import export, tri

# Haut: tiefes Sake-Rot, Mähne weiß
for k_, v in zip(('r0', 'r1', 'r2', 'r3', 'r4'), ('#2a0818', '#62102a', '#a0202e', '#d24a34', '#f6905c')):
    col(k_, v)
col('h0', '#3e3e5c'); col('h1', '#9a9cb8'); col('h2', '#eceef8')
col('o0', '#6e4a22'); col('o1', '#a8843a'); col('o2', '#d6b85c'); col('o3', '#f4e49a'); add_rim('o0 o1 o2', 'o3')
col('sh0', '#120c24'); col('sh1', '#28224a'); col('sh2', '#463c78'); col('sh3', '#7468a8')
add_rim('sh0 sh1 sh2', 'xh')
HAORI = ('sh1', 'sh2', 'sh3')
HAORIF = ('sh0', 'sh1', 'sh2')
GOLD = ('y0', 'y1', 'y2')


def head(c, HX, HY, S):
    HX, HY = HX + 3, HY + 6                                          # Hals sitzt beim größeren Körper tiefer
    p = C()
    p.grid(HX, HY, SB.HEAD, SB.LEG)
    c.stamp(p, 'K', skip=('h0', 'h1', 'h2'))
    hm = p.m & (c.a == I('h1'))
    for a_, b_ in [((15, 6), (22, 7)), ((17, 10), (25, 13)), ((18, 15), (24, 18))]:
        c.line([(HX + a_[0], HY + a_[1]), (HX + b_[0], HY + b_[1])], 'h2', only=hm)
    # rote Trinkerwangen
    p = C()
    p.pxs([(HX + 3, HY + 17), (HX + 4, HY + 17), (HX + 10, HY + 17)], 'r4')
    c.stamp(p, ring=False)


def gourd(c, hand, ang, ln=40, back=9):
    """Riesige Sake-Kalebasse, am Hals gepackt; der Bauch zeigt in Schlagrichtung."""
    dx, dy = -math.cos(ang), -math.sin(ang)
    hx, hy = hand
    p = C()
    neck0 = (hx - dx * 6, hy - dy * 6)
    b1 = (hx + dx * 13, hy + dy * 13)
    b2 = (hx + dx * 30, hy + dy * 30)
    body = L(*neck0, 3.0, hx + dx * 5, hy + dy * 5, 3.4) | E(*b1, 7.4, 7.4) | E(*b2, 11, 11)
    p.form(body, ('o0', 'o1', 'o2'), sd=4, hl=2)
    waist = L(hx + dx * 19, hy + dy * 19, 4.4, hx + dx * 21, hy + dy * 21, 4.4) & body
    p.fill(waist, 'm1')                                               # rotes Band in der Taille
    p.pxs([(int(hx + dx * 20), int(hy + dy * 20))], 'm3')
    p.form(E(neck0[0] - dx * 2, neck0[1] - dy * 2, 3.2, 3.2), ('m0', 'm1', 'm2'), sd=1, hl=1)   # Stöpsel
    c.stamp(p, 'K')
    p = C()                                                           # Kordel mit Quaste
    t1 = (b1[0] + 2, b1[1] + 9)
    p.line([(hx + dx * 18, hy + dy * 18), t1], 'm2')
    p.form(E(t1[0], t1[1] + 2, 1.6, 2.6), ('m1', 'm2', 'm3'), sd=0, hl=1)
    c.stamp(p, 'K')


def behind(c, B, S):
    """Haori-Rückenteil hinter dem Körper."""
    p = C()
    back = PG([B((48, 46)), B((76, 44)), B((84, 62)), B((86, 88)), B((74, 94)), B((60, 92)), B((46, 94)), B((42, 70))])
    p.form(back, HAORIF, sd=4, hl=1)
    for x in (54, 64, 74):
        p.line([B((x, 60)), B((x + 2, 92))], 'sh0', only=back)
    c.stamp(p, 'K')


def over_torso(c, B, S):
    """Haori-Vorderkante (Kragen) über der Brust: schwarzer Kragen mit Goldmuster, Wappen auf der Schulter."""
    p = C()
    lap = PG([B((60, 46)), B((66, 46)), B((70, 70)), B((72, 92)), B((66, 92)), B((62, 70))])
    p.form(lap, HAORI, sd=2, hl=1)
    coll = L(*B((61, 47)), 1.8, *B((66, 80)), 1.8)
    p.form(coll & lap, ('h0', 'hb', 'h2'), sd=0, hl=1)
    c.stamp(p, 'K')
    p = C()
    mon = E(*B((76, 54)), 3.2, 3.2)                                   # Wappen: goldener Kreis mit Blüte
    p.fill(mon, 'y1'); p.fill(E(*B((76, 54)), 1.6, 1.6), 'sh1'); p.pxs([B((76, 54))], 'y2')
    c.stamp(p, ring=False)


def sleeve(c, sh_, el, S):
    """weiter Haori-Ärmel: hängt als Stoffbahn unter dem nahen Oberarm."""
    p = C()
    drop = 13
    sl = PG([(sh_[0] + 6, sh_[1] - 2), (el[0] + 5, el[1] - 1), (el[0] + 3, el[1] + drop), (sh_[0] + 8, sh_[1] + drop + 2)])
    p.form(sl, HAORI, sd=2, hl=1)
    p.line([(el[0] + 3, el[1] + drop - 1), (sh_[0] + 8, sh_[1] + drop + 1)], 'm2', only=sl)   # rotes Futter am Saum
    c.stamp(p, 'K')


def cup(c, wr, S):
    """rote Sake-Schale (Sakazuki) in der nahen Hand."""
    x, y = wr[0] - 4, wr[1] - 7
    p = C()
    dish = E(x, y, 8.0, 2.8)
    p.form(dish, ('m1', 'm2', 'm3'), sd=1, hl=1)
    p.fill(E(x, y - 0.8, 5.4, 1.2), 'y1')                            # Sake mit Goldglanz
    p.pxs([(int(x) - 2, int(y) - 1)], 'y3')
    p.fill(R(x - 1, y + 2, x + 2, y + 3), 'm0')                       # Fuß
    c.stamp(p, 'K')


SB.CFG.update(head=head, weapon=gourd, mane=True, cloth=('h0', 'h1', 'h2'), behind=behind, over_torso=over_torso,
             after_near=cup)
SB.CFG['sleeve'] = sleeve

if __name__ == '__main__':
    px.setsize(SB.CW, SB.CH)
    export('boss_shuten_doji', SB.oni, SB.WALK, SB.ATTACK)
