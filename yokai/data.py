"""Spielinhalte: Biome, Items, Synergien, Transformationen, aktive Items, Charaktere, Yokai, Erfolge."""

# =====================================================================  BIOME
BIOMES = {
    'chikurin': dict(name='Bambuswald', jp='Chikurin', depth=1, floor=(62, 92, 52), floor_pat='grass',
                     wall=(120, 166, 74), wall_pat='bamboo', rock=(118, 116, 104), moss=True, ambient='leaves',
                     enemies=['hitodama', 'kodama', 'kappa', 'kasa_obake', 'bakezori', 'tsuchinoko', 'hyosube', 'azukiarai', 'bake_danuki'],
                     music=('in', 220, 92, 'calm', 11), dark=0),
    'inari': dict(name='Inari-Torii-Pfad', jp='Fushimi', depth=1, floor=(150, 112, 82), floor_pat='gravel',
                  wall=(196, 58, 44), wall_pat='torii', rock=(150, 140, 130), moss=False, ambient='petals',
                  enemies=['hitodama', 'kitsunebi_e', 'kasa_obake', 'bakezori', 'kodama', 'tsuchinoko', 'bake_danuki'],
                  music=('yo', 233, 96, 'calm', 12), dark=0),
    'obakedera': dict(name='Geistertempel', jp='Obake-dera', depth=2, floor=(176, 164, 104), floor_pat='tatami',
                      wall=(88, 56, 44), wall_pat='wood', rock=(120, 110, 100), moss=False, ambient='fireflies',
                      enemies=['chochin', 'nopperabo', 'gaki', 'ittan_momen', 'bakeneko', 'onibi', 'hitodama', 'tsurube_otoshi', 'nuppeppo'],
                      music=('in', 196, 84, 'mystic', 21), dark=40),
    'hakaba': dict(name='Alter Friedhof', jp='Hakaba', depth=2, floor=(84, 84, 96), floor_pat='stone',
                   wall=(104, 104, 116), wall_pat='stone', rock=(130, 130, 140), moss=True, ambient='fog',
                   enemies=['gaki', 'onibi', 'nopperabo', 'ittan_momen', 'chochin', 'kasa_obake', 'tenome', 'nuppeppo'],
                   music=('iwato', 185, 80, 'dark', 22), weather='rain', dark=60),
    'kurama': dict(name='Kurama-Berg', jp='Kurama-yama', depth=3, floor=(116, 86, 64), floor_pat='gravel',
                   wall=(92, 72, 60), wall_pat='rock', rock=(110, 100, 92), moss=True, ambient='leaves',
                   enemies=['karasu_tengu', 'kamaitachi', 'yamabiko', 'bakeneko', 'yuki_warashi', 'nekomata', 'tsurube_otoshi'],
                   music=('in', 247, 110, 'battle', 31), dark=0),
    'yukiyama': dict(name='Schneeberg', jp='Yuki-yama', depth=3, floor=(208, 218, 234), floor_pat='snow',
                     wall=(140, 162, 194), wall_pat='ice', rock=(170, 186, 210), moss=False, ambient='snow',
                     enemies=['yuki_warashi', 'kamaitachi', 'yamabiko', 'karasu_tengu', 'onibi'],
                     music=('yo', 262, 100, 'mystic', 32), weather='blizzard', dark=0),
    'ryugu': dict(name='Drachenpalast', jp='Ryūgū-jō', depth=4, floor=(54, 118, 128), floor_pat='coral',
                  wall=(206, 96, 96), wall_pat='coral', rock=(210, 150, 150), moss=False, ambient='bubbles',
                  enemies=['heikegani', 'funayurei', 'ningyo', 'isonade', 'kappa'],
                  music=('ryukyu', 233, 104, 'battle', 41), dark=20),
    'uminobe': dict(name='Geisterküste', jp='Umi-no-be', depth=4, floor=(74, 74, 84), floor_pat='sand',
                    wall=(76, 56, 44), wall_pat='planks', rock=(96, 90, 86), moss=False, ambient='fog',
                    enemies=['funayurei', 'heikegani', 'isonade', 'ningyo', 'onibi', 'nekomata'],
                    music=('iwato', 208, 92, 'dark', 42), weather='rain', dark=50),
    'yomi': dict(name='Unterwelt', jp='Yomi no Kuni', depth=5, floor=(62, 26, 36), floor_pat='stone',
                 wall=(44, 12, 22), wall_pat='bone', rock=(90, 50, 60), moss=False, ambient='embers',
                 enemies=['oni', 'shikome', 'tsuchigumo', 'shinigami', 'gaki', 'onibi', 'kasha'],
                 music=('iwato', 175, 116, 'battle', 51), weather='ash', dark=60),
    'jigoku': dict(name='Höllenfeuer', jp='Jigoku', depth=5, floor=(82, 32, 22), floor_pat='lava',
                   wall=(52, 22, 16), wall_pat='rock', rock=(70, 40, 30), moss=False, ambient='embers',
                   enemies=['oni', 'shikome', 'shinigami', 'onibi', 'tsuchigumo', 'bakeneko', 'kasha', 'wanyudo'],
                   music=('in', 165, 124, 'battle', 52), weather='ash', dark=30),
    'takamagahara': dict(name='Himmelsgefilde', jp='Takamagahara', depth=6, floor=(226, 206, 150), floor_pat='cloud',
                         wall=(240, 240, 250), wall_pat='cloud', rock=(220, 200, 140), moss=False, ambient='sparkle',
                         enemies=['shinigami', 'oni', 'karasu_tengu', 'ningyo', 'yamabiko', 'kamaitachi', 'shikome', 'katawaguruma'],
                         music=('yo', 294, 112, 'battle', 61), dark=0),
}
BIOMES.update({
    'kawabe': dict(name='Kappa-Flussufer', jp='Kawabe', depth=1, floor=(70, 104, 70), floor_pat='grass',
                   wall=(96, 120, 86), wall_pat='rock', rock=(120, 124, 116), moss=True, ambient='fireflies',
                   enemies=['kappa', 'tesso', 'hitodama', 'kasa_obake', 'yosuzume', 'tsuchinoko', 'hyosube', 'azukiarai'],
                   music=('ryukyu', 220, 98, 'calm', 13), weather='rain', dark=10, pit='water', decor='reeds'),
    'yashiki': dict(name='Spukvilla', jp='Bake-yashiki', depth=2, floor=(118, 82, 56), floor_pat='wood',
                    wall=(70, 44, 36), wall_pat='wood', rock=(110, 90, 80), moss=False, ambient='fog',
                    enemies=['mokumokuren', 'chochin', 'tesso', 'enenra', 'kerakera_onna', 'nopperabo', 'tenome', 'katawaguruma', 'nuppeppo'],
                    music=('iwato', 196, 78, 'mystic', 23), dark=80, decor='cracks'),
    'oeyama': dict(name='Ōe-Berg', jp='Ōe-yama', depth=3, floor=(96, 70, 58), floor_pat='gravel',
                   wall=(70, 50, 44), wall_pat='rock', rock=(100, 84, 76), moss=False, ambient='embers',
                   enemies=['kamikiri', 'jinmenju', 'abura_akago', 'karasu_tengu', 'bakeneko', 'gyuki', 'tenome', 'wanyudo'],
                   music=('in', 233, 116, 'battle', 33), dark=20, decor='bones'),
    'shinkai': dict(name='Tiefsee', jp='Shinkai', depth=4, floor=(24, 46, 78), floor_pat='sand',
                    wall=(30, 60, 100), wall_pat='coral', rock=(60, 90, 130), moss=False, ambient='bubbles',
                    enemies=['sazae_oni', 'gyuki', 'isonade', 'ningyo', 'funayurei'],
                    music=('iwato', 196, 96, 'mystic', 43), weather='rain_dark', dark=90, pit='water', decor='shells'),
    'enma_cho': dict(name='Hof des Enma', jp='Enma-chō', depth=5, floor=(110, 30, 30), floor_pat='stone',
                     wall=(60, 16, 16), wall_pat='stone', rock=(140, 110, 60), moss=False, ambient='embers',
                     enemies=['oni', 'nurikabe', 'kerakera_onna', 'shinigami', 'abura_akago', 'shikome', 'katawaguruma', 'wanyudo'],
                     music=('in', 175, 120, 'battle', 53), dark=40, pit='lava', decor='cracks'),
})
BIOMES['tsukiyomi'] = dict(name='Mondpalast', jp='Tsuki no Miya', depth=6, floor=(150, 160, 200), floor_pat='cloud',
                          wall=(210, 215, 235), wall_pat='cloud', rock=(170, 180, 210), moss=False, ambient='sparkle',
                          enemies=['shinigami', 'yamabiko', 'kamaitachi', 'ningyo', 'katawaguruma', 'karasu_tengu', 'nurikabe'],
                          music=('yo', 247, 100, 'mystic', 62), dark=50, pit='cloud', decor='clouds')
DEPTH_BIOMES = {1: ['chikurin', 'inari', 'kawabe'], 2: ['obakedera', 'hakaba', 'yashiki'], 3: ['kurama', 'yukiyama', 'oeyama'],
                4: ['ryugu', 'uminobe', 'shinkai'], 5: ['yomi', 'jigoku', 'enma_cho'], 6: ['takamagahara', 'tsukiyomi']}
for _b, _pit, _dec in (('chikurin', 'void', 'grass'), ('inari', 'void', 'petals'), ('obakedera', 'void', 'cracks'),
                       ('hakaba', 'void', 'graves'), ('kurama', 'void', 'leaves'), ('yukiyama', 'ice', 'snow'),
                       ('ryugu', 'water', 'shells'), ('uminobe', 'water', 'planks'), ('yomi', 'void', 'bones'),
                       ('jigoku', 'lava', 'cracks'), ('takamagahara', 'cloud', 'clouds')):
    BIOMES[_b].setdefault('pit', _pit)
    BIOMES[_b].setdefault('decor', _dec)
BOSS_POOL = {1: ['omukade', 'kappa_ou', 'jorogumo', 'oonyudo'], 2: ['gashadokuro', 'rokurokubi', 'nue', 'nurarihyon'],
             3: ['sojobo', 'raiju', 'yuki_onna', 'kamaitachi_trio'], 4: ['umibozu', 'ryujin', 'bake_kujira', 'akkorokamui'],
             5: ['orochi', 'shuten_doji', 'tamamo', 'enma'], 6: ['mikaboshi', 'izanami', 'kagutsuchi', 'fujin']}

# =====================================================================  ITEMS
ITEMS = {}
ORDER = []


def I(iid, name, desc, icon, col, pools, tags, q, locked=False, **fx):
    ITEMS[iid] = dict(id=iid, name=name, desc=desc, icon=icon, col=col, pools=pools, tags=tags, q=q,
                      locked=locked, fx=fx)
    ORDER.append(iid)


GOLD = (236, 196, 80)
# ---- Die drei Throninsignien & Götter (Kami-Pool)
I('kusanagi', 'Kusanagi no Tsurugi', 'Das Grasmäher-Schwert', 'sword', (200, 230, 255), 'K', ['kami'], 4, True, dmg=1.5, dmgm=1.2, pierce=1)
I('yata_kagami', 'Yata no Kagami', 'Der Spiegel der Sonnengöttin', 'mirror', GOLD, 'K', ['kami'], 4, True, rate=0.5, sig_spiegel=1)
I('yasakani', 'Yasakani no Magatama', 'Juwel der Ewigkeit', 'magatama', (110, 220, 140), 'K', ['kami'], 4, True, hp=1, luck=1, sig_ewigkeit=1)
I('amaterasu', 'Amaterasus Strahl', 'Die Sonne brennt', 'star', (255, 210, 80), 'K', ['kami'], 3, burn=1, dmg=1, size=1)
I('tsukuyomi', 'Tsukuyomis Mondsichel', 'Das Licht der Nacht', 'moon', (200, 210, 255), 'K', ['kami'], 3, ratem=1.2, sig_sichel=1)
I('susanoo_zorn', 'Susanoos Zorn', 'Der Sturm folgt dir', 'cloud', (150, 160, 200), 'KB', ['kami', 'raijin'], 3, chain=1, dmg=0.5)
I('ame_nuboko', 'Ame-no-Nuboko', 'Der Speer, der die Inseln schuf', 'sword', GOLD, 'K', ['kami'], 3, pierce=1, range=80, dmg=1)
I('kamikaze', 'Göttlicher Wind', 'Kamikaze trägt dich', 'cloud', (250, 250, 255), 'K', ['kami', 'tengu'], 3, spd=15, sig_rueckenwind=1)
I('hachiman_bogen', 'Hachimans Bogen', 'Gott der Bogenschützen', 'bow', GOLD, 'K', ['kami'], 3, w_bow=1, sig_treffsicher=1)
I('sakura_zweig', 'Sakura-Zweig', 'Vergänglich und schön', 'flower', (250, 170, 200), 'TK', ['kami'], 2, luck=1, sig_vergaenglich=1)
I('hamaya', 'Hamaya', 'Der Dämonen-brechende Pfeil', 'bow', (230, 60, 60), 'TK', ['kami'], 2, dmg=0.5, sig_daemonenbrecher=1)
I('juzu', 'Juzu-Gebetskette', 'Gebete durchdringen alles', 'beads', (160, 110, 70), 'TK', ['kami'], 2, spectral=1, dmg=0.4, rate=0.2)
I('teru_teru', 'Teru-teru-bōzu', 'Verscheucht Regen und Flüche', 'doll', (200, 200, 220), 'TK', ['kami'], 2, luck=2, curse_immune=1)
I('shimenawa', 'Shimenawa-Seil', 'Heiliges Seil, heilige Grenze', 'thread', (230, 210, 150), 'TS', ['kami', 'shikigami'], 2, sig_bannkreis=1, hp=1)
I('shakujo', 'Shakujō-Stab', 'Das Klingen vertreibt Böses', 'staff', GOLD, 'TK', ['kami', 'tengu'], 2, sig_klingen=1, dmg=0.3)
# ---- Kitsune
I('inari_maske', 'Inari-Maske', 'Glück der Füchse', 'mask', (250, 250, 250), 'T', ['kitsune'], 1, luck=1, coins=5, sig_fuchsglueck=1)
I('kitsunebi', 'Kitsune-bi', 'Fuchsfeuer sucht seinen Weg', 'flame', (110, 170, 255), 'T', ['kitsune'], 3, homing=1, burn=1)
I('kyubi_schweif', 'Neunter Schweif', 'Mehr Schwänze, mehr Macht', 'tail', (240, 150, 60), 'T', ['kitsune'], 2, sig_neun=1)
I('hoshi_no_tama', 'Hoshi no Tama', 'Die Sternenkugel des Fuchses', 'beads', (250, 250, 220), 'T', ['kitsune'], 2, rate=0.3, sig_sternkugel=1)
I('fuchsschrein', 'Kleiner Fuchsschrein', 'Opfergaben zahlen sich aus', 'box', (220, 70, 50), 'TS', ['kitsune'], 1, luck=1, keys=1, sig_opfergabe=1)
# ---- Raijin / Donner
I('raijin_trommel', 'Raijins Trommelstock', 'Donner bei jedem Schlag', 'drum', (250, 220, 90), 'T', ['raijin'], 3, raijin_chance=0.1)
I('inazuma', 'Inazuma-Splitter', 'Ein Stück eines Blitzes', 'crystal', (255, 240, 120), 'T', ['raijin'], 2, chain=1, shotspd=30)
I('raijin_magatama', 'Donner-Magatama', 'Es knistert leise', 'magatama', (250, 230, 80), 'T', ['raijin'], 2, luck=1, sig_statik=1)
I('raiju_klaue', 'Raijū-Klaue', 'Die Kralle des Donnerbiests', 'claw', (255, 230, 90), 'B', ['raijin'], 3, rate=0.4, sig_donnerbiest=1)
# ---- Fūjin / Tengu
I('fujin_sack', 'Fūjins Windsack', 'Der Wind ist mit dir', 'bag', (140, 210, 150), 'T', ['tengu'], 2, shotspd=60, range=60, sig_windstoss=1)
I('tengu_faecher', 'Tengu-Fächer', 'Ein Hauch wird zum Sturm', 'fan', (60, 140, 60), 'T', ['tengu'], 2, knock=1, shotspd=40, spd=15)
I('karasu_feder', 'Krähenfeder', 'Leicht wie die Nacht', 'feather', (60, 60, 80), 'T', ['tengu'], 2, spd=20, fly=1)
I('tengu_geta', 'Ippon-Geta', 'Tengu-Sandalen mit einem Zahn', 'hat', (150, 100, 60), 'T', ['tengu'], 2, spd=25, dash_dmg=1)
I('tengu_maske', 'Tengu-Maske', 'Stolz und Langnasig', 'mask', (220, 50, 40), 'T', ['tengu'], 2, range=50, sig_hochmut=1)
I('kamaitachi_sichel', 'Kamaitachi-Sichel', 'Schnitte im Wind', 'claw', (200, 200, 210), 'T', ['tengu'], 2, rate=0.7, dmgm=0.85, sig_schnitt=1)
I('furin', 'Fūrin', 'Die Windglocke ruft Salz herbei', 'bell', (150, 220, 240), 'TS', ['tengu'], 1, salts_regen=0.25, salts=1)
I('sojobo_feder', 'Sōjōbōs Federfächer', 'Der König der Tengu fächert', 'feather', (230, 230, 230), 'B', ['tengu'], 3, multishot=2, dmgm=0.8)
# ---- Shikigami / Onmyōdō
I('shikigami_papier', 'Shikigami-Papier', 'Ein Diener aus Papier', 'doll', (230, 70, 70), 'T', ['shikigami'], 2, familiar=1)
I('seimei_stern', 'Seimeis Pentagramm', 'Das Siegel des großen Onmyōji', 'star', (170, 110, 230), 'TB', ['shikigami'], 3, dmg=0.5, sig_pentagramm=1)
I('hitogata', 'Hitogata', 'Ein Papierschild umkreist dich', 'doll', (110, 150, 240), 'T', ['shikigami'], 2, orbital=1)
I('ofuda_buendel', 'Ofuda-Bündel', 'Mehr Talismane!', 'scroll', (230, 60, 60), 'T', ['shikigami'], 2, ratem=1.1, sig_buendel=1)
I('kuji_in', 'Kuji-in-Siegel', 'Neun Handsiegel der Macht', 'scroll', (130, 90, 200), 'T', ['shikigami'], 2, dmg=0.4, sig_kuji=1)
I('senbazuru', 'Senbazuru', 'Tausend Kraniche für einen Wunsch', 'crane', (240, 120, 160), 'T', ['shikigami'], 3, True, luck=1, sig_kraniche=1)
I('origami_kranich', 'Origami-Kranich', 'Er fliegt für dich', 'crane', (120, 200, 240), 'T', ['shikigami'], 2, sig_kranichflug=1)
# ---- Yūrei / Tod
I('yurei_laterne', 'Yūrei-Laterne', 'Ihr Licht geht durch Wände', 'lantern', (150, 220, 230), 'T', ['yurei'], 2, spectral=1, range=40)
I('shinigami_sense', 'Sense des Shinigami', 'Der Tod schneidet tief', 'sword', (90, 90, 110), 'O', ['yurei'], 3, dmgm=1.4, pierce=1)
I('onryo_haar', 'Haar der Onryō', 'Rache, die langsam vergiftet', 'thread', (40, 30, 50), 'OT', ['yurei'], 2, dmg=0.3, sig_rache=1)
I('sanzu_muenze', 'Münze vom Sanzu-Fluss', 'Bezahle den Fährmann – einmal', 'coin', (190, 190, 200), 'TS', ['yurei'], 3, True, revive=1)
I('shiro_kimono', 'Weißes Totengewand', 'Halb hier, halb dort', 'cloth', (240, 240, 250), 'T', ['yurei'], 2, spirit=2, sig_zwischenwelt=1)
I('yuki_traene', 'Yuki-onnas Träne', 'Eiskalt', 'crystal', (190, 240, 255), 'T', ['yurei'], 2, freeze=0.15)
I('onibi_ring', 'Onibi-Ring', 'Geisterfeuer kreist um dich', 'flame', (180, 110, 240), 'T', ['yurei'], 2, sig_irrlicht=1)
I('gashadokuro_knochen', 'Riesenknochen', 'Von einem Skelett aus Hunger', 'skull', (230, 226, 210), 'B', ['yurei'], 3, dmg=1, size=1, sig_knochenbruch=1)
# ---- Oni
I('kanabo', 'Kanabō', 'Wie einem Oni ein Eisenknüppel', 'hammer', (70, 70, 80), 'O', ['oni'], 3, dmg=2, rate=-0.4, knock=1, size=1)
I('oni_horn', 'Oni-Horn', 'Wut wird zu Stärke', 'fang', (240, 220, 160), 'O', ['oni'], 3, dmgm=1.3, rage=1)
I('oni_sake', 'Oni-Sake', 'Ein Schluck zu viel', 'cup', (230, 80, 80), 'TO', ['oni'], 2, dmg=1, sig_rausch=1)
I('shuten_kalebasse', 'Shutens Kalebasse', 'Explosiver Rausch', 'gourd', (220, 60, 50), 'OB', ['oni'], 3, explode=1, rate=-0.3, dmg=1)
I('tigerfell', 'Tigerfell', 'Was echte Oni tragen', 'cloth', (250, 200, 60), 'T', ['oni'], 2, hp=1, sig_tigerfell=1)
I('hannya', 'Hannya-Maske', 'Eifersucht wird Feuer', 'mask', (210, 230, 200), 'O', ['oni', 'yurei'], 3, hurt_ring=1, dmg=1)
I('yomi_feuer', 'Feuer von Yomi', 'Es brennt ewig', 'flame', (200, 30, 40), 'O', ['oni', 'yurei'], 3, burn=1, dmgm=1.15, sig_ewige_flamme=1)
I('izanami_kamm', 'Izanamis Kamm', 'Aus dem Reich der Toten', 'fan', (60, 30, 60), 'O', ['yurei'], 3, spirit=2, sig_kammzinken=1)
# ---- Ryū / Wasser
I('ryu_perle', 'Drachenperle', 'Nyoi-hōju erfüllt Wünsche', 'beads', (120, 200, 255), 'T', ['ryu'], 3, homing=1, shotspd=30, size=0.5)
I('ryu_schuppe', 'Drachenschuppe', 'Hart wie Jade', 'crystal', (60, 200, 170), 'T', ['ryu'], 2, hp=1, sig_schuppenpanzer=1)
I('kappa_teller', 'Kappa-Teller', 'Wasser auf dem Kopf', 'coin', (200, 230, 240), 'T', ['ryu'], 2, bounce=1, range=40)
I('kappa_gurke', 'Kappas Gurke', 'Ein Kappa würde töten dafür', 'leaf', (90, 180, 70), 'TS', ['ryu'], 1, hp=1, fullheal=1, sig_kappa_freund=1)
I('otohime_kamm', 'Otohimes Haarkamm', 'Von der Prinzessin des Meeres', 'fan', (250, 160, 200), 'T', ['ryu'], 2, luck=1, sig_anmut=1)
I('kanagawa', 'Welle von Kanagawa', 'Die große Welle', 'wave', (60, 110, 200), 'T', ['ryu'], 3, wave=1, pierce=1, dmg=0.3)
I('suijin_schale', 'Suijins Wasserschale', 'Der Wassergott ist gnädig', 'cup', (100, 160, 240), 'T', ['ryu'], 2, slow=1, size=1)
I('umibozu_auge', 'Auge des Umibōzu', 'Es starrt aus der Tiefe', 'eye', (40, 60, 90), 'B', ['ryu'], 3, size=1, dmg=1, sig_starrt=1)
I('ryujin_bart', 'Barthaar des Ryūjin', 'Fein wie Seide, stark wie Stahl', 'thread', (120, 200, 230), 'B', ['ryu'], 3, range=60, sig_seidenfaden=1)
I('koinobori', 'Koinobori', 'Der Karpfen schwimmt stromauf', 'fish', (230, 70, 70), 'T', ['ryu'], 2, spd=15, sig_stromauf=1)
# ---- Tanuki / Glück
I('ebisu_angel', 'Ebisus Angelrute', 'Der Glücksgott fischt Gold', 'staff', (120, 180, 220), 'TS', ['tanuki'], 2, gold_shots=0.15, luck=1)
I('daikoku_hammer', 'Daikokus Glückshammer', 'Reichtum wird Macht', 'hammer', GOLD, 'T', ['tanuki'], 3, money_dmg=1, coins=10)
I('maneki_neko', 'Maneki-neko', 'Die Winkekatze lockt Münzen', 'daruma', (250, 250, 240), 'S', ['tanuki'], 2, magnet=1, discount=1, luck=1)
I('tanuki_beutel', 'Tanuki-Beutel', 'Prall gefüllt', 'bag', (160, 110, 70), 'S', ['tanuki'], 1, coins=15, hp=1, sig_tanuki_bauch=1)
I('tanuki_blatt_p', 'Verwandlungsblatt', 'Ein Tanuki ist nie, was er scheint', 'leaf', (90, 170, 80), 'T', ['tanuki'], 2, luck=2, spd=10, sig_tarnung=1)
# ---- Omamori (Shop)
I('omamori_kenko', 'Omamori: Gesundheit', 'Kenkō – möge dein Herz stark sein', 'omamori', (220, 60, 60), 'S', [], 1, hp=1, sig_kenko=1)
I('omamori_kinun', 'Omamori: Glück', 'Kin-un – möge das Gold fließen', 'omamori', (240, 200, 60), 'S', [], 1, luck=1, sig_kinun=1)
I('omamori_yakuyoke', 'Omamori: Schutz', 'Yakuyoke – Unheil prallt ab', 'omamori', (80, 120, 230), 'S', [], 2, shield=1)
I('omamori_gokaku', 'Omamori: Erfolg', 'Gōkaku – du schaffst das', 'omamori', (80, 190, 100), 'S', [], 1, rate=0.4, sig_gokaku=1)
# ---- Essen
I('onigiri', 'Onigiri', 'Reisbällchen mit Umeboshi', 'rice', (240, 240, 240), 'SB', [], 1, hp=1, sig_proviant=1)
I('bento', 'Bentō', 'Mamas Mittagessen', 'box', (200, 60, 60), 'S', [], 1, hp=1, heal=4, sig_satt=1)
I('mochi', 'Mochi', 'Klebrig und süß', 'beads', (250, 245, 240), 'TS', [], 1, hp=1, spd=-3, sig_klebrig=1)
I('dango', 'Dango', 'Drei Bällchen am Spieß', 'dango', (240, 160, 190), 'TS', [], 1, spd=10, sig_drei_baellchen=1)
I('matcha', 'Matcha-Tee', 'Bitter und wach', 'cup', (110, 180, 90), 'S', [], 1, spd=5, sig_wach=1)
I('fugu', 'Fugu', 'Ein falscher Schnitt...', 'fish', (240, 210, 90), 'T', [], 2, kill_explode=0.2)
I('wasabi', 'Wasabi', 'Scharf bis in die Nase', 'leaf', (130, 200, 90), 'T', [], 2, dmg=0.5, sig_nasebrennt=1)
I('umeboshi', 'Umeboshi', 'Saure Pflaume, gesunder Körper', 'beads', (200, 50, 70), 'TS', [], 1, clear_heal=0.2, luck=1)
I('natto', 'Nattō', 'Fäden ziehen sich überall hin', 'beads', (170, 130, 60), 'T', [], 2, split=1, size=-0.5)
# ---- Waffen & Krieger
I('tamahagane', 'Tamahagane-Klinge', 'Gefaltet tausendmal', 'sword', (220, 220, 230), 'T', [], 2, dmg=1, w_sword=1)
I('shuriken', 'Shuriken', 'Schnell und leise', 'star', (160, 160, 170), 'T', [], 2, rate=0.6, shotspd=50, sig_wurfstern=1)
I('kunai', 'Kunai-Gürtel', 'Messer zu allen Seiten', 'sword', (90, 90, 100), 'T', [], 2, side=1, rate=0.3)
I('yumi', 'Yumi-Bogen', 'Lang, asymmetrisch, tödlich', 'bow', (160, 110, 60), 'T', [], 2, range=80, shotspd=80, dmg=0.5, pierce=1)
I('bushido', 'Bushidō-Rolle', 'Der Weg des Kriegers', 'scroll', (200, 40, 40), 'T', [], 2, dmg=0.4, rate=0.3, sig_ehre=1)
I('strohhut', 'Strohhut', 'Für die lange Reise', 'hat', (220, 190, 110), 'T', [], 1, spd=15, hp=1, sig_lange_reise=1)
I('bakeneko_kralle', 'Bakeneko-Kralle', 'Katzen treffen immer kritisch', 'claw', (160, 90, 210), 'T', [], 2, crit=0.15, dmg=0.5)
I('neko_gloeckchen', 'Katzenglöckchen', 'Klingeling', 'bell', (250, 220, 90), 'TS', [], 1, luck=1, spd=10, sig_klingeling=1)
# ---- Tempel & Kultur
I('mokugyo', 'Mokugyo', 'Jeder vierte Schlag ist mächtig', 'drum', (170, 100, 50), 'T', [], 2, big_every=4)
I('bonsho', 'Tempelglocke', 'Ihr Klang schmerzt Yokai', 'bell', (180, 130, 70), 'TB', [], 2, aura=1)
I('daruma', 'Daruma', 'Siebenmal fallen, achtmal aufstehen', 'daruma', (220, 40, 40), 'T', [], 2, hp=1, sig_aufstehen=1)
I('kintsugi', 'Kintsugi-Schale', 'Gebrochen und doch schöner', 'cup', GOLD, 'T', [], 2, hurt_dmg=1, rate=0.3)
I('hyakki_rolle', 'Rolle des Hyakki Yagyō', 'Die Nacht der 100 Dämonen', 'scroll', (120, 70, 160), 'TB', [], 3, dmg=0.5, sig_parade=1)
I('noh_maske', 'Nō-Maske', 'Das Gesicht verändert sich mit dem Licht', 'mask', (245, 235, 220), 'T', [], 2, sig_maskenwechsel=1)
I('shamisen', 'Shamisen', 'Drei Saiten, eine Welle', 'bow', (120, 70, 40), 'T', [], 2, wave=1, rate=0.4)
I('komainu', 'Komainu-Statue', 'Ein Wächter an deiner Seite', 'daruma', (170, 170, 150), 'TS', [], 3, True, hp=1, sig_a_gyo=1)
I('tanabata', 'Tanabata-Wunschzettel', 'Wünsch dir was', 'scroll', (120, 200, 240), 'T', [], 2, luck=2, sig_sternschnuppe=1)
I('hanabi', 'Hanabi', 'Feuerwerk!', 'star', (250, 120, 160), 'T', [], 3, explode=1, split=1)
I('horagai', 'Horagai', 'Das Muschelhorn der Yamabushi', 'shell', (240, 210, 190), 'T', ['tengu'], 2, knock=1, shotspd=40, dmg=0.3)
I('chochin_feuer', 'Chōchin-Feuer', 'Das Laternenfeuer springt über', 'lantern', (230, 70, 50), 'T', [], 2, dmg=0.5, sig_springfeuer=1)
I('hozuki', 'Hōzuki-Laterne', 'Lichter der Ahnen weisen den Weg', 'lantern', (250, 140, 50), 'TS', [], 2, map=1, luck=1)
I('sensu', 'Sensu', 'Ein goldener Faltfächer', 'fan', GOLD, 'S', [], 1, rate=0.3, sig_goldfaecher=1)
I('karakasa', 'Karakasa', 'Ein Schirm, der Kugeln abwehrt', 'hat', (220, 80, 60), 'T', [], 2, dash_reflect=1, spd=10)
I('jorogumo_seide', 'Jorōgumo-Seide', 'Klebrig und überall', 'thread', (240, 240, 240), 'TB', [], 2, slow=1, sig_spinnennetz=1)
I('omukade_gift', 'Ōmukade-Gift', 'Hundert Beine, ein Biss', 'fang', (170, 80, 200), 'B', [], 3, poison=1, sig_giftspur=1)
I('nue_schweif', 'Schweif der Nue', 'Eine Schlange als Schwanz', 'tail', (90, 160, 80), 'TB', [], 2, sig_schlangenschweif=1)
I('kiyome_sack', 'Sack mit Reinigungssalz', 'Kiyome – Reinigung', 'bag', (240, 240, 245), 'S', [], 1, salts=3, sig_reinigung=1)
I('ronin_schwur', 'Schwur des Rōnin', 'Ohne Herrn, ohne Furcht', 'sword', (120, 120, 140), 'T', [], 3, True, dmg=1, w_sword=1, sig_iaido=1)
I('kagami_mochi', 'Kagami-Mochi', 'Neujahrsglück', 'beads', (250, 250, 240), 'S', [], 2, hp=1, sig_neujahr=1)
I('ema', 'Ema-Holztafel', 'Ein Wunsch an die Götter', 'box', (210, 170, 110), 'TS', [], 1, luck=1, sig_ema=1)
I('tengu_auge', 'Allsehendes Tengu-Auge', 'Nichts bleibt verborgen', 'eye', (220, 60, 60), 'T', ['tengu'], 2, True, sig_falkenblick=1)
I('yamata_zahn', 'Zahn der Orochi', 'Acht Köpfe, acht Zähne', 'fang', (110, 200, 110), 'B', [], 4, True, multishot=3, poison=1, dmgm=0.85)
I('kyubi_juwel', 'Tamamos Juwel', 'Das Herz der Neunschwänzigen', 'crystal', (250, 180, 80), 'B', ['kitsune'], 4, True, crit=0.1, sig_verzaubern=1)
I('shuten_schale', 'Shutens Sakeschale', 'Der König der Oni trinkt', 'cup', (180, 40, 40), 'B', ['oni'], 4, True, dmgm=1.3, hp=1, sig_oni_koenig=1)
I('hoshi_splitter', 'Splitter des bösen Sterns', 'Mikaboshis Licht', 'star', (180, 120, 255), 'B', ['kami'], 4, True, rate=0.3, sig_boeser_stern=1)

# ---- Neue Items (Runde 1)
I('tesso_zahn', 'Zahn des Tesso', 'Die Eisenratte nagt alles durch', 'fang', (160, 170, 190), 'T', [], 2, pierce=1, rate=0.3)
I('abura_schale', 'Ölschale', 'Das Feuerkind leckt daran', 'cup', (240, 170, 60), 'T', [], 2, range=30, sig_oel=1)
I('nurikabe_stein', 'Nurikabe-Stein', 'Eine unsichtbare Wand schützt dich', 'crystal', (160, 160, 150), 'TS', [], 3, shield=1, hp=1, sig_wandbruch=1)
I('mokumoku_auge', 'Hundert Augen', 'Aus den Shōji starrt es zurück', 'eye', (230, 230, 210), 'T', ['yurei'], 2, sig_hundert_augen=1)
I('jinmen_frucht', 'Gesichterfrucht', 'Sie lacht, wenn man sie isst', 'daruma', (240, 190, 140), 'TS', [], 1, fullheal=1, luck=1)
I('suzume_feder', 'Spatzenfeder', 'Der Nachtspatz singt', 'feather', (150, 100, 60), 'T', ['tengu'], 1, rate=0.2, spd=10, sig_flatter=1)
I('enenra_pfeife', 'Rauchpfeife', 'Du wirst zu Rauch, wenn du rollst', 'staff', (140, 140, 150), 'T', ['yurei'], 2, sig_rauch=1)
I('gyuki_horn', 'Gyūki-Horn', 'Vom Ochsenkopf-Spinnendämon', 'fang', (60, 60, 70), 'TO', ['oni'], 2, dmg=1.2, knock=1)
I('kerakera_faecher', 'Fächer der Kerakera-onna', 'Ihr Lachen hallt wider', 'fan', (190, 80, 160), 'T', [], 2, sig_lachen=1)
I('sazae_muschel', 'Sazae-Muschel', 'Eine Turbanschnecke mit Geheimnissen', 'shell', (230, 150, 170), 'T', ['ryu'], 2, hp=1, sig_panzer=1)
I('onyudo_kette', 'Ōnyūdōs Gebetskette', 'Riesige Perlen eines riesigen Mönchs', 'beads', (190, 140, 90), 'B', ['kami'], 4, True, orbital=3, dmg=0.5)
I('nurarihyon_pfeife', 'Nurarihyons Kiseru', 'Der Herr der Yokai befiehlt', 'staff', (180, 150, 90), 'B', ['shikigami'], 4, True, familiar=2, luck=2)
I('kamaitachi_klingen', 'Klingen der drei Wiesel', 'Stolpern, Schneiden, Heilen', 'claw', (230, 230, 240), 'B', ['tengu'], 4, True, rate=0.5, sig_drei_wiesel=1)
I('akkoro_tinte', 'Akkorokamuis Tinte', 'Rot wie das Meer bei Sonnenuntergang', 'gourd', (200, 40, 60), 'B', ['ryu'], 4, True, sig_tinte=1, dmg=0.5)
I('enma_spiegel', 'Jōhari-Spiegel', 'Er zeigt alle Sünden', 'mirror', (220, 60, 50), 'B', ['kami'], 4, True, dmgm=1.3, sig_johari=1)
I('hyosube_haar', 'Hyōsubes Haarbüschel', 'Es kichert leise', 'thread', (150, 110, 70), 'T', [], 1, dmg=0.6, sig_kichern=1)
I('tenome_handschuh', 'Augenhandschuh', 'Sieh mit den Händen', 'eye', (240, 200, 160), 'T', [], 2, range=40, sig_augenhand=1)
I('nekomata_schweif', 'Zweiter Katzenschweif', 'Mit zwanzig Jahren wächst er', 'tail', (250, 240, 230), 'T', [], 2, sig_zweischwanz=1)
I('kasha_rad', 'Feuerrad des Kasha', 'Es raubt die Seelen der Bösen', 'flame', (255, 110, 40), 'TO', ['oni'], 3, dash_fire=1)
I('shoji_papier', 'Shōji-Papier', 'Größere Talismane, mehr Salz', 'scroll', (245, 240, 225), 'S', [], 1, salts=1, sig_gross=1)
I('koban', 'Koban', 'Ein ovales Goldstück aus der Edo-Zeit', 'coin', GOLD, 'TS', ['tanuki'], 1, coins=25, sig_reichtum=1)
I('daruma_otoshi', 'Daruma-otoshi', 'Schlag schnell, aber genau', 'hammer', (90, 160, 220), 'T', [], 2, rate=0.6, dmgm=0.92, sig_schlagfolge=1)
I('yatagarasu', 'Yatagarasu', 'Die dreibeinige Krähe weist den Weg', 'feather', (40, 40, 50), 'K', ['kami', 'tengu'], 3, map=1, sig_sonnenkraehe=1)
I('tenugui', 'Tenugui', 'Ein Handtuch für alle Fälle', 'cloth', (90, 130, 200), 'TS', [], 1, spd=12, sig_schweiss=1)
I('hagoromo', 'Hagoromo', 'Das Federgewand einer Himmelsjungfrau', 'cloth', (230, 240, 255), 'K', ['kami'], 3, fly=1, spirit=4)
I('izanami_schleier', 'Izanamis Schleier', 'Leben und Tod in einem Gewand', 'cloth', (120, 60, 120), 'B', ['yurei', 'kami'], 4, True, revive=1, spirit=4)
I('kaze_bukuro', 'Kaze-bukuro', 'Fūjins Windsack', 'cloud', (150, 220, 180), 'B', ['kami', 'tengu'], 4, True, spd=10, rate=0.3, sig_windsack=1)
I('yomi_momo', 'Pfirsich von Yomotsu Hirasaka', 'Izanagis Wurf gegen die Verfolger aus Yomi', 'yomi_momo', (255, 170, 140), 'B', ['kami'], 4, True, hp=1, sig_momo=1)
I('uzume_suzu', 'Uzumes Kagura-Suzu', 'Ihr Tanz lockte die Sonne aus der Höhle', 'uzume_suzu', (255, 214, 90), 'B', ['kami'], 4, True, spd=5, sig_suzu=1)
I('kagutsuchi_glut', 'Glut des Kagutsuchi', 'Das erste Feuer der Welt', 'flame', (255, 90, 30), 'B', ['kami', 'oni'], 4, True, burn=1, dmgm=1.2, sig_erstes_feuer=1)
I('geheimkarte', 'Karte des Diebes', 'Wo sind die verborgenen Räume?', 'scroll', (190, 160, 110), 'TS', [], 2, True, map=1, salts=2)

# ---- v1.3: Fundstücke aus den Himmelsgefilden und aus Yomi
I('komainu_glocke', 'Glocke des Komainu', 'Wird ihr Träger getroffen, läutet sie für alle', 'komainu_glocke', (236, 190, 70), ['K'], ['kami'], 3, hurt_ring=1, hp=1, sig_glockenschlag=1)
I('tennin_feder', 'Feder der Tennin', 'Leicht wie ein Himmelsgewand', 'tennin_feder', (236, 236, 255), ['T'], ['kami'], 3, shotspd=40, spd=8, sig_schweben=1)
I('yomi_stein', 'Fels von Yomotsu', 'Der Stein, der die Unterwelt verschließt', 'yomi_stein', (120, 128, 160), ['O'], ['oni'], 3, hp=2, spd=-10, dmg=0.6, sig_felsblock=1)
I('mikaboshi_staub', 'Sternenstaub', 'Ein Säckchen aus dem Gewand des bösen Sterns', 'mikaboshi_staub', (120, 150, 255),
  ['B'], ['raijin'], 4, crit=0.12, rate=0.35, luck=1)
# ---- v1.4: Geschenke aus Ereignisräumen (nur dort zu finden, Pool 'Y')
I('brautschleier', 'Schleier der Fuchsbraut', 'Ein Dank für den ungestörten Hochzeitszug', 'brautschleier', (240, 240, 250), ['Y'], ['kitsune'], 3, luck=2, spd=8, sig_fuchsregen=1)
I('zashiki_temari', 'Temari-Ball', 'Zashiki-warashis Spielball bringt Glück ins Haus', 'zashiki_temari', (220, 60, 70), ['Y'], [], 2, luck=1, coins=6, sig_hausglueck=1)

# ---- Figuren-Siegel: jede Figur schaltet mit jedem Siegel ein eigenes Item frei (gesperrt bis dahin)
I('haraegushi', 'Haraegushi', 'Der Reinigungsstab der Schreinmaid fegt das Unreine fort', 'haraegushi', (245, 245, 235), 'T', ['kami'], 3, True, salts=1, sig_harae=1)
I('zanshin_tsuba', 'Tsuba des alten Meisters', 'Zanshin – der Geist bleibt nach dem Schnitt wach', 'zanshin_tsuba', (200, 170, 90), 'T', [], 3, True, dmg=0.3, sig_zanshin=1)
I('kuzu_blatt', 'Kuzu-Blatt', 'Das Abschiedsgedicht der Fuchsfrau aus dem Shinoda-Wald', 'kuzu_blatt', (150, 200, 110), 'T', ['kitsune'], 3, True, luck=1, sig_fuchszauber=1)
I('bunbuku_kessel', 'Bunbuku-Chagama', 'Der Teekessel, der eigentlich ein Tanuki war', 'bunbuku_kessel', (150, 120, 90), 'T', ['tanuki'], 3, True, hp=1, sig_chagama=1)
I('tausendstes_schwert', 'Das tausendste Schwert', 'Benkei nahm 999 Kriegern die Klinge ab – eine fehlte ihm', 'tausendstes_schwert', (200, 210, 230), 'T', [], 3, True, dmg=0.3, sig_schwertjagd=1)
I('neunter_teller', 'Der neunte Teller', 'Ichi-mai … ni-mai … – im Brunnen fehlt immer einer', 'neunter_teller', (230, 240, 255), 'T', ['yurei'], 3, True, spirit=2, sig_sarayashiki=1)
I('tengu_tsubute', 'Tengu-Tsubute', 'Steine, die aus heiterem Himmel fallen', 'tengu_tsubute', (150, 140, 130), 'T', ['tengu'], 3, True, shotspd=20, sig_tsubute=1)
I('taizan_fukun', 'Taizan-Fukun-Ritual', 'Seimei tauschte vor dem Herrn des Berges ein Leben gegen ein anderes', 'taizan_fukun', (200, 60, 60), 'T', ['shikigami'], 3, True, sig_taizan=1)
I('ibaraki_arm', 'Ibaraki-dōjis Arm', 'Watanabe no Tsuna schlug ihn ab – der Oni kam zurück, ihn zu holen', 'ibaraki_arm', (200, 80, 70), 'T', ['oni'], 3, True, dmg=0.3, sig_ibaraki=1)
I('yashiori_sake', 'Yashiori no Sake', 'Achtmal gebraut – genug, um die Orochi zu berauschen', 'yashiori_sake', (230, 220, 180), 'T', ['raijin'], 3, True, hp=1, sig_yashiori=1)
I('hi_ogi', 'Hi-ōgi der Miko', 'Der Zypressenfächer des Kagura-Tanzes', 'hi_ogi', (240, 90, 80), 'T', ['kami'], 3, True, rate=0.2, sig_kagura_mai=1)
I('muramasa', 'Muramasa-Klinge', 'Ein verfluchtes Schwert, das nach Blut dürstet', 'muramasa', (200, 60, 70), 'T', ['oni'], 3, True, dmg=0.4, sig_blutdurst=1)
I('fuchs_trugbild', 'Kuzunohas Spiegelbild', 'Was du siehst, ist nur ein Schatten der Füchsin', 'fuchs_trugbild', (255, 170, 90), 'T', ['kitsune'], 3, True, spd=8, sig_doppelgaenger=1)
I('shigaraki_tanuki', 'Shigaraki-Tanuki', 'Die Tonfigur mit Sakeflasche und Schuldbuch bringt Kaufleuten Glück', 'shigaraki_tanuki', (190, 140, 90), 'T', ['tanuki'], 3, True, luck=1, coins=5, sig_gluecksstraehne=1)
I('tachi_ojo', 'Tachi-ōjō', 'Benkei starb aufrecht, von tausend Pfeilen durchbohrt', 'tachi_ojo', (210, 200, 180), 'T', [], 3, True, hp=1, sig_tachi_ojo=1)
I('tsurube', 'Brunneneimer von Banchō', 'Kaltes Wasser aus Okikus Brunnen', 'tsurube', (120, 170, 220), 'T', ['yurei'], 3, True, spirit=2, sig_tsurube=1)
I('kakuremino', 'Kakuremino', 'Der Strohmantel der Tengu macht unsichtbar', 'kakuremino', (200, 180, 110), 'T', ['tengu'], 3, True, spd=6, sig_kakuremino=1)
I('hoki_naiden', 'Hoki Naiden', 'Seimeis geheimes Buch der Yin-Yang-Kunst', 'hoki_naiden', (110, 130, 200), 'T', ['shikigami'], 3, True, shotspd=20, sig_hoki=1)
I('masakari', 'Kintarōs Masakari', 'Die Axt des Bergkindes, das mit Bären rang', 'masakari', (220, 120, 60), 'T', ['oni'], 3, True, dmg=0.3, sig_masakari=1)
I('habakiri', 'Ame-no-Habakiri', 'Das Zehn-Faust-Schwert, das die Orochi zerschnitt', 'habakiri', (190, 220, 255), 'T', ['raijin'], 3, True, dmg=0.4, sig_habakiri=1)
I('tamagushi', 'Tamagushi', 'Ein Sakaki-Zweig mit Shide, den Göttern dargebracht', 'tamagushi', (110, 180, 90), 'T', ['kami'], 3, True, luck=1, sig_tamagushi=1)
I('kesagiri', 'Kesa-giri-Rolle', 'Der Schnitt von der Schulter bis zur Hüfte', 'kesagiri', (220, 220, 235), 'T', [], 3, True, dmg=0.3, sig_kesagiri=1)
I('hoshi_tama', 'Hoshi no Tama', 'Das Sternjuwel, in dem ein Fuchs seine Seele verwahrt', 'hoshi_tama', (255, 210, 150), 'T', ['kitsune'], 3, True, luck=1, sig_hoshi_tama=1)
I('tanuki_bayashi', 'Tanuki-bayashi', 'Im Garten des Shōjō-ji trommeln die Tanuki im Mondlicht', 'tanuki_bayashi', (170, 120, 80), 'T', ['tanuki'], 3, True, hp=1, sig_bayashi=1)
I('gojo_giboshi', 'Giboshi der Gojō-Brücke', 'Hier stellte Benkei sich Ushiwakamaru in den Weg', 'gojo_giboshi', (200, 170, 90), 'T', [], 3, True, hp=1, sig_gojo=1)
I('ido_kagami', 'Brunnenspiegel', 'Im Wasser des Brunnens zählt jemand Teller', 'ido_kagami', (150, 190, 230), 'T', ['yurei'], 3, True, spirit=1, sig_ido_kagami=1)
I('sojobo_hane', 'Sōjōbōs Feder', 'Eine Feder des Tengu-Königs vom Kurama', 'sojobo_hane', (90, 90, 110), 'T', ['tengu'], 3, True, spd=6, sig_tengu_wirbel=1)
I('juni_shinsho', 'Jūni-Shinshō', 'Die zwölf Himmelsgeneräle dienten Seimei als Shikigami', 'juni_shinsho', (230, 200, 120), 'T', ['shikigami'], 3, True, rate=0.1, sig_juni=1)
I('setsubun_mame', 'Setsubun-Bohnen', '„Oni wa soto, fuku wa uchi!“', 'setsubun_mame', (210, 170, 110), 'T', ['oni'], 3, True, luck=1, sig_mame=1)
I('murakumo', 'Ame-no-Murakumo', 'Die Wolke, die stets über der Orochi hing', 'murakumo', (150, 160, 190), 'T', ['raijin'], 3, True, dmg=0.2, sig_murakumo=1)
I('kotodama', 'Kotodama-Norito', 'Im gesprochenen Gebet wohnt ein Gott', 'kotodama', (240, 230, 200), 'T', ['kami'], 3, True, spirit=1, sig_kotodama=1)
I('tsubame_gaeshi', 'Tsubame-gaeshi', 'Der Schnitt, schnell wie eine wendende Schwalbe', 'tsubame_gaeshi', (90, 110, 160), 'T', [], 3, True, rate=0.2, sig_tsubame=1)
I('shinoda_blatt', 'Blatt aus dem Shinoda-Wald', '„Wenn du mich vermisst, komm in den Wald von Shinoda“', 'shinoda_blatt', (200, 150, 70), 'T', ['kitsune'], 3, True, luck=1, sig_shinoda=1)
I('tanuki_tokkuri', 'Tokkuri des Tanuki', 'Die Sakeflasche, die nie leer wird', 'tanuki_tokkuri', (200, 180, 140), 'T', ['tanuki'], 3, True, coins=5, sig_tokkuri=1)
I('nanatsu_dogu', 'Benkeis sieben Waffen', 'Er trug sie alle auf dem Rücken', 'nanatsu_dogu', (170, 170, 190), 'T', ['oni'], 3, True, dmg=0.3, sig_nanatsu=1)
I('zehnter_teller', 'Der zehnte Teller', 'Okiku zählte bis neun – doch einmal fand sich der zehnte', 'zehnter_teller', (220, 230, 255), 'T', ['yurei'], 3, True, spirit=2, sig_zehnter=1)
I('hanadaka_men', 'Hanadaka-Maske', 'Das lange Nasengesicht des Tengu', 'hanadaka_men', (210, 60, 50), 'T', ['tengu'], 3, True, spd=6, sig_hanadaka=1)
I('kikyo_mon', 'Kikyō-Mon', 'Der Glockenblumen-Stern, Seimeis Wappen', 'kikyo_mon', (140, 120, 220), 'T', ['shikigami'], 3, True, dmg=0.2, sig_kikyo=1)
I('oni_tsuno', 'Abgebrochenes Oni-Horn', 'Wer es trägt, spürt den Zorn des Oni', 'oni_tsuno', (230, 210, 170), 'T', ['oni'], 3, True, dmg=0.3, sig_oni_tsuno=1)
I('kushinada_kushi', 'Kushinadas Kamm', 'Susanoo verwandelte die Braut in einen Kamm und trug sie im Haar', 'kushinada_kushi', (230, 120, 140), 'T', ['raijin'], 3, True, hp=1, sig_kushinada=1)
I('onusa', 'Ōnusa', 'Der große Reinigungsstab der Shintō-Priester', 'onusa', (245, 245, 235), 'T', ['kami'], 3, True, spirit=1, sig_onusa=1)
I('ichi_no_tachi', 'Ichi-no-tachi', 'Der erste Hieb entscheidet den Kampf', 'ichi_no_tachi', (200, 200, 215), 'T', [], 3, True, dmg=0.2, sig_ichi=1)
I('kitsune_chochin', 'Kitsune-Chōchin', 'Die Laterne der Fuchshochzeit', 'kitsune_chochin', (255, 170, 90), 'T', ['kitsune'], 3, True, luck=1, sig_chochin=1)
I('tanuki_kesa', 'Tanuki-Kesa', 'In der Mönchsrobe wird der Tanuki zum steinernen Jizō', 'tanuki_kesa', (190, 150, 90), 'T', ['tanuki'], 3, True, hp=1, sig_jizo=1)
I('kanjincho', 'Kanjinchō', 'Die leere Spendenliste, die Benkei am Ataka-Tor vorlas', 'kanjincho', (230, 220, 190), 'T', [], 3, True, coins=8, sig_kanjin=1)
I('okiku_ido', 'Brunnen von Banchō Sarayashiki', 'Aus der Tiefe zählt eine Stimme Teller', 'okiku_ido', (120, 170, 220), 'T', ['yurei'], 3, True, spirit=1, sig_reikon=1)
I('ushiwaka_fue', 'Ushiwakas Flöte', 'Auf der Gojō-Brücke spielte der junge Yoshitsune', 'ushiwaka_fue', (110, 150, 90), 'T', ['tengu'], 3, True, spd=6, sig_fue=1)
I('seimei_ido', 'Seimei-Brunnen', 'Die Quelle, die Seimei mit dem Glockenblumen-Stern öffnete', 'seimei_ido', (140, 120, 220), 'T', ['shikigami'], 3, True, luck=1, sig_seimei_ido=1)
I('kodomo_kanabo', 'Kinder-Kanabō', 'Klein, aber aus echtem Oni-Eisen', 'kodomo_kanabo', (90, 90, 105), 'T', ['oni'], 3, True, dmg=0.3, sig_kodomo_kanabo=1)
I('ohabari', 'Ama-no-Ōhabari', 'Das Götterschwert, mit dem Izanagi den Feuergott erschlug', 'ohabari', (255, 240, 150), 'T', ['raijin'], 3, True, dmg=0.2, sig_ohabari=1)
# Prüfungs-Belohnungen (je Herausforderung ein Item)
I('fuurin', 'Biidoro-Fūrin', 'Ein gläsernes Windspiel – schön, solange es nicht zerspringt', 'fuurin', (150, 220, 240), 'T', [], 3, True, dmg=0.3, sig_fuurin=1)
I('abura_age', 'Abura-age', 'Frittierter Tofu – die Lieblingsspeise der Inari-Füchse', 'abura_age', (230, 170, 80), 'T', ['kitsune'], 3, True, luck=1, sig_abura_age=1)
I('tsukikage', 'Tsukikage', 'Eine Klinge, die nur im Mondschatten zu sehen ist', 'tsukikage', (150, 160, 220), 'T', [], 3, True, dmg=0.2, sig_tsukikage=1)
I('hayate_waraji', 'Hayate-Waraji', 'Strohsandalen, schnell wie der Sturmwind', 'hayate_waraji', (210, 190, 120), 'T', ['tengu'], 3, True, spd=8, sig_hayate=1)
I('senryo_bako', 'Senryō-bako', 'Eine Truhe für tausend Goldstücke', 'senryo_bako', (220, 180, 80), 'T', ['tanuki'], 3, True, coins=10, sig_senryo=1)
I('keppan', 'Keppan', 'Ein Pakt, mit dem eigenen Blut gesiegelt', 'keppan', (200, 50, 50), 'T', ['oni'], 3, True, dmg=0.2, sig_keppan=1)
I('miidera_kane', 'Glocke von Mii-dera', 'Benkei schleppte sie allein den Berg Hiei hinauf', 'miidera_kane', (120, 150, 110), 'T', [], 3, True, hp=1, sig_miidera=1)
I('nademono', 'Nademono', 'Eine Papierpuppe, die das Unheil an deiner Stelle trägt', 'nademono', (240, 240, 230), 'T', ['shikigami'], 3, True, spirit=1, sig_nademono=1)
I('aokusa_mino', 'Aokusa-Mino', 'Im Grasmantel wanderte der verbannte Susanoo durch den Regen', 'aokusa_mino', (110, 150, 80), 'T', ['raijin'], 3, True, spirit=2, sig_mino=1)
I('kongozue', 'Kongō-zue', 'Der Stab des Pilgers – Dōgyō ninin, nie allein unterwegs', 'kongozue', (200, 170, 120), 'T', [], 3, True, hp=1, sig_kongozue=1)

ITEM_IDS = ORDER

# ---- Omamori-Anhänger (ein Slot, tauschbar)
TRINKETS = {
    'am_kitsune': dict(name='Fuchs-Anhänger', desc='Glück +2', icon='mask', col=(250, 240, 230), fx=dict(luck=2)),
    'am_tora': dict(name='Tiger-Anhänger', desc='Schaden +0.7', icon='claw', col=(250, 200, 60), fx=dict(dmg=0.7)),
    'am_usagi': dict(name='Hasen-Anhänger', desc='Tempo +18', icon='leaf', col=(250, 250, 250), fx=dict(spd=18)),
    'am_kame': dict(name='Schildkröten-Anhänger', desc='Schild pro Raum', icon='shell', col=(90, 160, 90), fx=dict(shield=1)),
    'am_tsuru': dict(name='Kranich-Anhänger', desc='Feuerrate +0.5', icon='crane', col=(240, 240, 250), fx=dict(rate=0.5)),
    'am_koi': dict(name='Koi-Anhänger', desc='Reichweite +60', icon='fish', col=(240, 120, 60), fx=dict(range=60)),
    'am_hebi': dict(name='Schlangen-Anhänger', desc='Giftige Talismane', icon='tail', col=(110, 200, 90), fx=dict(poison=1)),
    'am_kumo': dict(name='Wolken-Anhänger', desc='Zielsuchend', icon='cloud', col=(220, 230, 250), fx=dict(homing=1)),
    'am_hi': dict(name='Feuer-Anhänger', desc='Brennende Talismane', icon='flame', col=(255, 140, 40), fx=dict(burn=1)),
    'am_tama': dict(name='Perlen-Anhänger', desc='Ein Schild-Orbital', icon='beads', col=(200, 220, 255), fx=dict(orbital=1)),
    'am_kane': dict(name='Münz-Anhänger', desc='Goldene Talismane, Magnet', icon='coin', col=GOLD, fx=dict(gold_shots=0.12, magnet=1)),
    'am_tsuki': dict(name='Mond-Anhänger', desc='Salz bei Raumende', icon='moon', col=(200, 210, 255), fx=dict(salts_regen=0.2)),
    'am_ken': dict(name='Schwert-Anhänger', desc='Krit-Chance +12 %', icon='sword', col=(210, 210, 230), fx=dict(crit=0.12)),
    'am_yama': dict(name='Berg-Anhänger', desc='Rückstoß, größere Talismane', icon='hat', col=(140, 120, 100), fx=dict(knock=1, size=0.7)),
}

# =====================================================================  SYNERGIEN
SYNERGIES = [
    dict(id='fuchshochzeit', name='Fuchshochzeit', desc='Die Braut trägt die Maske ihres Gottes', items=['brautschleier', 'inari_maske'], fx=dict(luck=2, sig_sonnenregen=1)),
    dict(id='gluecksheim', name='Glückliches Haus', desc='Wo Zashiki-warashi spielt, wohnt das Glück', items=['zashiki_temari', 'maneki_neko'], fx=dict(luck=3, sig_gluecksheim=1)),
    dict(id='a_un', name='A und Un', desc='Zwei Wächter: Anfang und Ende', items=['komainu', 'komainu_glocke'], fx=dict(dmg=0.8, sig_a_un=1)),
    dict(id='sternenfall', name='Sternenfall', desc='Federn aus Licht, Staub aus Sternen', items=['tennin_feder', 'mikaboshi_staub'], fx=dict(crit=0.08, sig_sternenstaub=1)),
    dict(id='yomotsu', name='Yomotsu Hirasaka', desc='Der Pass zwischen den Welten ist versiegelt', items=['yomi_stein', 'shimenawa'], fx=dict(hp=1, sig_yomotsu=1)),
    dict(id='jingi', name='Sanshu no Jingi', desc='Die drei Throninsignien vereint!', items=['kusanagi', 'yata_kagami', 'yasakani'], fx=dict(dmgm=1.2, sig_jingi=1)),
    dict(id='sonne_mond', name='Sonne & Mond', desc='Tag und Nacht in deiner Hand', items=['amaterasu', 'tsukuyomi'], fx=dict(dmgm=1.3, sig_sonne_mond=1)),
    dict(id='sturmgoetter', name='Sturmgötter', desc='Raijin und Fūjin kämpfen mit dir', items=['raijin_trommel', 'fujin_sack'], fx=dict(raijin_chance=0.15, sig_gewittersturm=1)),
    dict(id='fuchstanz', name='Fuchsfeuer-Tanz', desc='Neun Flammen tanzen', items=['kitsunebi', 'kyubi_schweif'], fx=dict(dmg=0.5, sig_neun_flammen=1)),
    dict(id='fuchsstern', name='Kitsune no Yomeiri', desc='Sonnenregen – die Fuchshochzeit', items=['inari_maske', 'hoshi_no_tama'], fx=dict(luck=2, sig_fuchsstern=1)),
    dict(id='gluecksgoetter', name='Glücksgötter', desc='Ebisu und Daikoku lachen', items=['ebisu_angel', 'daikoku_hammer'], fx=dict(gold_shots=0.1, coins=20, luck=2, sig_gluecksgoetter=1)),
    dict(id='onmyodo', name='Onmyōdō', desc='Der Weg von Yin und Yang', items=['shikigami_papier', 'seimei_stern'], fx=dict(familiar=1, sig_onmyodo=1)),
    dict(id='papiersturm', name='Papiersturm', desc='Talismane überall', items=['ofuda_buendel', 'kuji_in'], fx=dict(ratem=1.2, sig_papiersturm=1)),
    dict(id='kranichschwarm', name='Kranichschwarm', desc='Tausend Flügel', items=['senbazuru', 'origami_kranich'], fx=dict(luck=1, sig_kranichschwarm=1)),
    dict(id='geisterlicht', name='Geisterlicht', desc='Laternen der Verstorbenen', items=['yurei_laterne', 'onibi_ring'], fx=dict(burn=1, sig_geisterlicht=1)),
    dict(id='todesbote', name='Todesbote', desc='Der Fährmann arbeitet für dich', items=['shinigami_sense', 'sanzu_muenze'], fx=dict(dmgm=1.2, sig_faehrmann=1)),
    dict(id='ewiger_winter', name='Ewiger Winter', desc='Alles erstarrt', items=['yuki_traene', 'suijin_schale'], fx=dict(freeze=0.1, sig_ewiger_winter=1)),
    dict(id='tengu_flug', name='Tengu-Flug', desc='Spring über Berge', items=['karasu_feder', 'tengu_geta'], fx=dict(spd=20, sig_tengu_flug=1)),
    dict(id='grosser_wind', name='Großer Wind', desc='Ein Taifun bricht los', items=['tengu_faecher', 'fujin_sack'], fx=dict(knock=1, shotspd=60, sig_taifun=1)),
    dict(id='oni_rausch', name='Oni-Rausch', desc='Sake macht Oni unbesiegbar', items=['oni_sake', 'shuten_kalebasse'], fx=dict(sig_oni_rausch=1)),
    dict(id='oni_krieger', name='Oni-Krieger', desc='Knüppel und Tigerfell', items=['kanabo', 'tigerfell'], fx=dict(dmg=1, knock=1, sig_oni_krieger=1)),
    dict(id='drachenkoenig', name='Drachenkönig', desc='Perle und Bart des Ryūjin', items=['ryu_perle', 'ryujin_bart'], fx=dict(pierce=1, sig_drachenkoenig=1)),
    dict(id='grosse_welle', name='Tsunami', desc='Die Welle prallt zurück', items=['kanagawa', 'kappa_teller'], fx=dict(bounce=1, sig_brandung=1)),
    dict(id='kappa_fest', name='Kappa-Festmahl', desc='Gurken für alle!', items=['kappa_gurke', 'kappa_teller'], fx=dict(hp=1, fullheal=1, sig_kappa_fest=1)),
    dict(id='blitzschlag', name='Blitz & Klaue', desc='Das Donnerbiest erwacht', items=['inazuma', 'raiju_klaue'], fx=dict(rate=0.3, sig_blitzschlag=1)),
    dict(id='hanami', name='Hanami', desc='Kirschblüten und Dango', items=['sakura_zweig', 'dango'], fx=dict(clear_heal=0.25, sig_hanami=1)),
    dict(id='teezeremonie', name='Teezeremonie', desc='Ruhe vor dem Sturm', items=['matcha', 'sensu'], fx=dict(rate=0.4, sig_teezeremonie=1)),
    dict(id='sushi', name='Sushi-Platte', desc='Fugu mit Wasabi – riskant!', items=['wasabi', 'fugu'], fx=dict(dmg=0.5, sig_sushi=1)),
    dict(id='omamori_set', name='Omamori-Sammler', desc='Die Götter beschützen dich doppelt', items=['omamori_kenko', 'omamori_kinun', 'omamori_yakuyoke'], fx=dict(revive=1, sig_omamori_set=1)),
    dict(id='tempelmusik', name='Tempelmusik', desc='Shamisen und Holzfisch', items=['shamisen', 'mokugyo'], fx=dict(rate=0.3, sig_tempelmusik=1)),
    dict(id='tempelfest', name='Tempelfest', desc='Die Glocke schlägt zurück', items=['bonsho', 'mokugyo'], fx=dict(aura=1, sig_tempelfest=1)),
    dict(id='bushi', name='Bushi-Seele', desc='Klinge und Ehre', items=['tamahagane', 'bushido'], fx=dict(crit=0.15, sig_bushi=1)),
    dict(id='ninja', name='Shinobi', desc='Shuriken und Kunai', items=['shuriken', 'kunai'], fx=dict(side=1, rate=0.5, sig_ninja=1)),
    dict(id='kyudo', name='Kyūdō', desc='Der Weg des Bogens', items=['yumi', 'hamaya'], fx=dict(crit=0.1, sig_kyudo=1)),
    dict(id='daruma_geist', name='Unbeugsam', desc='Gebrochen, gekittet, gestärkt', items=['daruma', 'kintsugi'], fx=dict(hp=1, sig_daruma_geist=1)),
    dict(id='wunsch', name='Wunsch erfüllt', desc='Die Sterne hören dich', items=['tanabata', 'teru_teru'], fx=dict(luck=3, sig_wunsch=1)),
    dict(id='unterweltgift', name='Unterweltgift', desc='Haar und Schweif', items=['onryo_haar', 'nue_schweif'], fx=dict(poison=1, sig_unterweltgift=1)),
    dict(id='hannya_zorn', name='Hannya-Zorn', desc='Wut ohne Grenzen', items=['hannya', 'oni_horn'], fx=dict(dmg=0.5, sig_hannya_zorn=1)),
    dict(id='spinnennetz', name='Netz der Spinne', desc='Gift und Seide', items=['jorogumo_seide', 'omukade_gift'], fx=dict(slow=1, sig_giftnetz=1)),
    dict(id='mondklinge', name='Mondsichel-Klinge', desc='Schnitte kehren zurück', items=['tsukuyomi', 'kamaitachi_sichel'], fx=dict(boomerang=1, sig_mondschnitt=1)),
    dict(id='feuerwerk', name='Feuerwerk über Edo', desc='Hanabi am Sommerfest', items=['hanabi', 'chochin_feuer'], fx=dict(burn=1, sig_feuerwerk=1)),
    dict(id='koi_drache', name='Koi wird zum Drachen', desc='Der Karpfen erklimmt den Wasserfall', items=['koinobori', 'ryu_perle'], fx=dict(dmg=1, sig_koi_drache=1)),
    dict(id='winkekatze', name='Doppeltes Katzenglück', desc='Zwei Katzen, doppeltes Glück', items=['maneki_neko', 'neko_gloeckchen'], fx=dict(luck=2, sig_winkekatze=1)),
    dict(id='schreinwaechter', name='Schreinwächter', desc='Komainu bewacht das Seil', items=['komainu', 'shimenawa'], fx=dict(shield=1, sig_schreinwaechter=1)),
    dict(id='seimei_meister', name='Abe no Seimei', desc='Der legendäre Onmyōji', items=['seimei_stern', 'kuji_in'], fx=dict(familiar=1, sig_seimei=1)),
    dict(id='tengu_koenig', name='Tengu-König', desc='Maske und Fächer des Sōjōbō', items=['tengu_maske', 'sojobo_feder'], fx=dict(dmgm=1.2, sig_tengu_sturm=1)),
    dict(id='hundert_augen', name='Hundert Augen sehen alles', desc='Kein Yokai entkommt deinem Blick', items=['mokumoku_auge', 'tengu_auge'], fx=dict(sig_allsehend=1)),
    dict(id='rattenschwarm', name='Tessos Schwarm', desc='Tausend kleine Zähne', items=['tesso_zahn', 'natto'], fx=dict(rate=0.3, sig_rattenschwarm=1)),
    dict(id='oelfeuer', name='Ölfeuer', desc='Laternenöl brennt am besten', items=['abura_schale', 'chochin_feuer'], fx=dict(burn=1, sig_oelfeuer=1)),
    dict(id='gericht', name='Göttliches Gericht', desc='Zwei Spiegel – Himmel und Hölle', items=['enma_spiegel', 'yata_kagami'], fx=dict(dmgm=1.15, sig_gericht=1)),
    dict(id='hyakki_herr', name='Herr der Nachtparade', desc='Alle Yokai folgen dir', items=['nurarihyon_pfeife', 'shikigami_papier'], fx=dict(familiar=1, sig_hyakki_herr=1)),
    dict(id='wirbelklingen', name='Wirbelwind-Klingen', desc='Die Wiesel kehren immer zurück', items=['kamaitachi_klingen', 'kamaitachi_sichel'], fx=dict(rate=0.3, sig_wirbelklingen=1)),
    dict(id='tiefsee', name='Aus der Tiefsee', desc='Tinte und Muschel', items=['akkoro_tinte', 'sazae_muschel'], fx=dict(hp=1, sig_tintenpanzer=1)),
    dict(id='unbeweglich', name='Unbeweglich', desc='Wand und Wächter', items=['nurikabe_stein', 'komainu'], fx=dict(shield=1, hp=1, sig_unbeweglich=1)),
    dict(id='riesenmoench', name='Gebet des Riesen', desc='Perlen kreisen um dich', items=['onyudo_kette', 'juzu'], fx=dict(orbital=1, sig_riesenmoench=1)),
    dict(id='katzenreich', name='Katzenreich', desc='Nekomata und Bakeneko verbünden sich', items=['nekomata_schweif', 'bakeneko_kralle'], fx=dict(crit=0.15, sig_katzenreich=1)),
    dict(id='feuerwagen', name='Feuerwagen', desc='Der Kasha fährt aus der Hölle', items=['kasha_rad', 'yomi_feuer'], fx=dict(dmg=0.5, sig_feuerwagen=1)),
    dict(id='himmelsbote', name='Himmelsbote', desc='Die Krähe reitet den göttlichen Wind', items=['yatagarasu', 'kamikaze'], fx=dict(dmgm=1.2, sig_himmelsbote=1)),
    dict(id='tennyo', name='Himmlische Jungfrau', desc='Federgewand und Kirschblüten', items=['hagoromo', 'sakura_zweig'], fx=dict(spirit=2, sig_tennyo=1)),
    dict(id='kaufmann', name='Reich wie ein Kaufmann', desc='Gold regiert die Welt', items=['koban', 'daikoku_hammer'], fx=dict(coins=30, sig_kaufmann=1)),
    dict(id='augen_ueberall', name='Augen überall', desc='Hände und Wände sehen dich', items=['tenome_handschuh', 'mokumoku_auge'], fx=dict(sig_augen_ueberall=1)),
    dict(id='sturmfaecher', name='Sturmfächer', desc='Fūjin und Raijin im selben Fächer', items=['tengu_faecher', 'raijin_trommel'], fx=dict(raijin_chance=0.05, sig_sturmfaecher=1)),
    dict(id='sonnenspiegel', name='Sonnenspiegel', desc='Amaterasus Licht im Spiegel', items=['amaterasu', 'yata_kagami'], fx=dict(dmg=0.5, sig_sonnenspiegel=1)),
    dict(id='mondschein_teich', name='Mondschein-Teich', desc='Tsukuyomi spiegelt sich im Wasser', items=['tsukuyomi', 'suijin_schale'], fx=dict(freeze=0.1, sig_mondteich=1)),
    dict(id='fuchsgeld', name='Fuchsgeld', desc='Inari liebt Opfergaben', items=['inari_maske', 'koban'], fx=dict(luck=2, sig_fuchsgeld=1)),
    dict(id='totenfaehre', name='Totenfähre', desc='Laterne und Münze für den Sanzu-Fluss', items=['yurei_laterne', 'sanzu_muenze'], fx=dict(kill_heal=0.05, sig_totenfaehre=1)),
    dict(id='oni_tanz', name='Oni-Tanz', desc='Trommeln und Masken', items=['hannya', 'mokugyo'], fx=dict(rage=1, sig_oni_tanz=1)),
    dict(id='drachenschuppen', name='Drachenpanzer', desc='Schuppe und Perle', items=['ryu_schuppe', 'ryu_perle'], fx=dict(hp=1, sig_drachenschuppen=1)),
    dict(id='ninja_flug', name='Ninja-Flug', desc='Krähenfeder und Shuriken', items=['karasu_feder', 'shuriken'], fx=dict(spd=15, sig_ninja_flug=1)),
    dict(id='fest_der_laternen', name='Obon-Fest', desc='Laternen für die Ahnen', items=['hozuki', 'chochin_feuer'], fx=dict(map=1, luck=2, sig_fest_der_laternen=1)),
    dict(id='onmyo_spiegel', name='Onmyō-Spiegel', desc='Pentagramm im Spiegel', items=['seimei_stern', 'yata_kagami'], fx=dict(familiar=1, sig_onmyo_spiegel=1)),
    dict(id='feuerkind', name='Kind des Feuers', desc='Ölschale und Feuerrad', items=['abura_schale', 'kasha_rad'], fx=dict(spd=10, sig_feuerkind=1)),
    dict(id='strassenkatze', name='Herrenlose Katze', desc='Ein Rōnin und eine Katze', items=['ronin_schwur', 'neko_gloeckchen'], fx=dict(dash_dmg=1, sig_strassenkatze=1)),
    dict(id='orochi_kusanagi', name='Aus dem Schwanz der Orochi', desc='Susanoo fand das Schwert in der Schlange', items=['kusanagi', 'yamata_zahn'], fx=dict(sig_orochi=1)),
    dict(id='leben_tod', name='Leben und Tod', desc='Izanamis Erbe vereint', items=['izanami_kamm', 'izanami_schleier'], fx=dict(dmgm=1.2, sig_leben_tod=1)),
    dict(id='goetter_arsenal', name='Göttliches Arsenal', desc='Speer und Bogen der Kami', items=['ame_nuboko', 'hachiman_bogen'], fx=dict(crit=0.1, sig_goetter_arsenal=1)),
    dict(id='hanami_picknick', name='Hanami-Picknick', desc='Unter Kirschblüten schmeckt alles besser', items=['onigiri', 'bento', 'umeboshi'], fx=dict(hp=1, clear_heal=0.2, sig_hanami_picknick=1)),
    dict(id='shogatsu', name='Shōgatsu', desc='Ein gutes neues Jahr!', items=['mochi', 'kagami_mochi'], fx=dict(hp=1, sig_shogatsu=1)),
    dict(id='pilger', name='Reisender Pilger', desc='Der Weg ist das Ziel', items=['strohhut', 'tenugui'], fx=dict(spd=10, sig_pilger=1)),
    dict(id='yamabushi', name='Bergasket', desc='Stab und Muschelhorn der Yamabushi', items=['shakujo', 'horagai'], fx=dict(dmg=0.5, sig_yamabushi=1)),
    dict(id='tiefsee_herr', name='Herr der Tiefe', desc='Das Meer gehorcht dir', items=['otohime_kamm', 'umibozu_auge'], fx=dict(rate=0.5, sig_tiefsee_blick=1)),
    dict(id='sturmgott', name='Zorn des Sturmgottes', desc='Susanoo schleudert Blitze', items=['susanoo_zorn', 'raijin_magatama'], fx=dict(dmg=0.5, sig_sturmgott=1)),
    dict(id='oeyama_bande', name='Ōeyama-Bande', desc='Trinkfest und hart wie Horn', items=['shuten_schale', 'gyuki_horn'], fx=dict(hp=1, sig_oeyama_bande=1)),
    dict(id='maskenzug', name='Maskenzug', desc='Die Parade der hundert Gesichter', items=['hyakki_rolle', 'noh_maske'], fx=dict(crit=0.05, sig_maskenzug=1)),
    dict(id='fujin_raijin', name='Fūjin-Raijin-zu', desc='Wind und Donner wie auf dem Wandschirm', items=['kaze_bukuro', 'raijin_trommel'], fx=dict(sig_fujin_raijin=1)),
    dict(id='izanagis_flucht', name='Izanagis Flucht', desc='Kamm und Pfirsich hielten die Verfolger auf', items=['yomi_momo', 'izanami_kamm'], fx=dict(spd=10, sig_izanagis_flucht=1)),
    dict(id='ama_no_iwato', name='Ama-no-Iwato', desc='Spiegel und Tanz lockten die Sonne hervor', items=['uzume_suzu', 'yata_kagami'], fx=dict(dmg=0.5, sig_iwato=1)),
    dict(id='verfluchte_sterne', name='Verfluchte Sterne', desc='Fuchs und Stern leuchten gemeinsam', items=['hoshi_splitter', 'kyubi_juwel'], fx=dict(crit=0.1, sig_verfluchte_sterne=1)),
    dict(id='hara_tsuzumi', name='Hara-tsuzumi', desc='Der Tanuki trommelt auf seinen Bauch', items=['tanuki_beutel', 'tanuki_blatt_p'], fx=dict(sig_hara_tsuzumi=1)),
    dict(id='gelaechter', name='Gelächter der Nacht', desc='Kerakera-onna und Hyōsube lachen im Chor', items=['kerakera_faecher', 'hyosube_haar'], fx=dict(sig_gelaechter=1)),
    dict(id='enenra', name='Enenra', desc='Der Rauch des ersten Feuers lebt', items=['enenra_pfeife', 'kagutsuchi_glut'], fx=dict(sig_enenra=1)),
    dict(id='gashadokuro', name='Gashadokuro', desc='Die Knochen der Ungeborgenen stehen auf', items=['gashadokuro_knochen', 'shiro_kimono'], fx=dict(sig_gashadokuro=1)),
    dict(id='tsukumogami', name='Tsukumogami', desc='Schirm und Papierpuppe erwachen', items=['karakasa', 'hitogata'], fx=dict(orbital=1, sig_tsukumogami=1)),
    dict(id='shinsen', name='Shinsen', desc='Reine Gaben für den Fuchsgott', items=['kiyome_sack', 'fuchsschrein'], fx=dict(sig_shinsen=1)),
    dict(id='nanakorobi', name='Nanakorobi Yaoki', desc='Siebenmal fallen, achtmal aufstehen', items=['daruma_otoshi', 'omamori_gokaku'], fx=dict(sig_nanakorobi=1)),
    dict(id='jinmenju', name='Jinmenju', desc='Der Gesichterbaum lacht über erfüllte Wünsche', items=['ema', 'jinmen_frucht'], fx=dict(sig_jinmenju=1)),
    dict(id='mokumokuren', name='Mokumokuren', desc='Augen im zerrissenen Papier', items=['shoji_papier', 'geheimkarte'], fx=dict(sig_mokumokuren=1)),
    dict(id='sommerwind', name='Sommerwind', desc='Windglocke und Spatzenfeder', items=['furin', 'suzume_feder'], fx=dict(salts_regen=0.15, sig_sommerwind=1)),
    dict(id='misogi', name='Misogi', desc='Reinigung im kalten Wasser – Stab und Salz tilgen jede Unreinheit', items=['onusa', 'kiyome_sack'], fx=dict(salts=1, sig_misogi=1)),
    dict(id='kagura', name='Kagura', desc='Fächer und Glöckchen – der Tanz für die Götter', items=['hi_ogi', 'uzume_suzu'], fx=dict(spd=3, sig_kagura=1)),
    dict(id='sarayashiki', name='Banchō Sarayashiki', desc='Ichi-mai … kyū-mai … – und doch fehlt einer', items=['neunter_teller', 'zehnter_teller'], fx=dict(spirit=1, sig_okiku=1)),
    dict(id='gojo_ohashi', name='Gojō-Ōhashi', desc='Flötenspieler und Naginata-Mönch – aus Feinden werden Gefährten', items=['gojo_giboshi', 'ushiwaka_fue'], fx=dict(hp=1, sig_gojo_bashi=1)),
    dict(id='orochi_taiji', name='Orochi-Taiji', desc='Erst der Sake, dann das Schwert – so fiel die achtköpfige Schlange', items=['habakiri', 'yashiori_sake'], fx=dict(sig_yamata_giri=1)),
    dict(id='seimei_jinja', name='Seimei-Jinja', desc='Glockenblumen-Stern und Brunnen – der Schrein in Kyōto', items=['kikyo_mon', 'seimei_ido'], fx=dict(luck=1, sig_kikyo_ido=1)),
    dict(id='ido_no_yurei', name='Ido no Yūrei', desc='Eimer und Brunnen – aus dem kalten Wasser steigt Okiku', items=['okiku_ido', 'tsurube'], fx=dict(spirit=1, sig_ido_reikon=1)),
    dict(id='shikigami_tsukai', name='Shikigami-Tsukai', desc='Das geheime Buch und die zwölf Generäle – Seimeis Papiervögel', items=['hoki_naiden', 'juni_shinsho'], fx=dict(sig_juni_tori=1)),
    dict(id='yakumo_tatsu', name='Yakumo Tatsu', desc='Achtfach steigen die Wolken über Izumo – Susanoos Lied für Kushinada', items=['murakumo', 'kushinada_kushi'], fx=dict(sig_yakumo=1)),
    dict(id='koishikuba', name='Koishikuba', desc='„Wenn du mich vermisst …“ – Kuzunohas Abschied liegt als Nebel über jedem Raum', items=['kuzu_blatt', 'shinoda_blatt'], fx=dict(sig_koishikuba=1)),
    dict(id='yoto_muramasa', name='Yōtō Muramasa', desc='Die verfluchte Klinge lernt den Kesa-Schnitt – und kann nicht mehr aufhören', items=['muramasa', 'kesagiri'], fx=dict(sig_yoto=1)),
    dict(id='ganryujima', name='Ganryūjima', desc='Die wendende Schwalbe gegen den ersten Hieb – Kojirō und Musashi auf der Insel', items=['tsubame_gaeshi', 'ichi_no_tachi'], fx=dict(sig_ganryu=1)),
    dict(id='senbon_gari', name='Senbon-gari', desc='Sieben Waffen auf dem Rücken, die tausendste Klinge vor Augen – Benkeis Jagd an der Gojō-Brücke', items=['tausendstes_schwert', 'nanatsu_dogu'], fx=dict(sig_senbon=1)),
    dict(id='tamagushi_hoten', name='Tamagushi-hōten', desc='Der Sakaki-Zweig wird dargebracht, das Norito gesprochen – und die Kami antworten', items=['tamagushi', 'kotodama'], fx=dict(sig_hoten=1)),
    dict(id='ataka_no_seki', name='Ataka no Seki', desc='Die leere Liste laut vorgelesen, aufrecht vor dem Tor – kein Wächter wagt sich vor', items=['tachi_ojo', 'kanjincho'], fx=dict(sig_ataka=1)),
    dict(id='shojoji_utage', name='Shōjō-ji no Utage', desc='Shō, shō, Shōjō-ji – im Mondlicht trommeln die Tanuki, und der Sake geht nie aus', items=['tanuki_bayashi', 'tanuki_tokkuri'], fx=dict(sig_utage=1)),
    dict(id='kintaro', name='Kintarō', desc='Das Bergkind mit Axt und Keule – es rang mit Bären und wurde Raikōs Gefolgsmann', items=['masakari', 'kodomo_kanabo'], fx=dict(sig_kintaro=1)),
    dict(id='kurama_lehre', name='Kurama-Lehre', desc='Nachts auf dem Kurama lehrte der Tengu-König den jungen Ushiwaka die Kunst des Windes', items=['sojobo_hane', 'hanadaka_men'], fx=dict(sig_kurama=1)),
    dict(id='rashomon', name='Rashōmon', desc='Watanabe no Tsuna schlug den Arm ab – im Zorn kehrt Ibaraki-dōji zurück, ihn zu holen', items=['ibaraki_arm', 'oni_tsuno'], fx=dict(sig_rashomon=1)),
    dict(id='henro', name='Henro', desc='Dōgyō ninin – Pilgerstab und Kraniche wandern mit dir', items=['kongozue', 'senbazuru'], fx=dict(luck=1, sig_henro=1)),
]

# =====================================================================  TRANSFORMATIONEN
TRANSFORMS = {
    'kitsune': dict(name='Kitsune-Avatar', desc='Du wirst zum Fuchsgeist', fx=dict(multishot=1, homing=1, spd=15), col=(250, 160, 60)),
    'raijin': dict(name='Donnergott', desc='Blitze gehorchen dir', fx=dict(chain=1, raijin_chance=0.2), col=(255, 230, 90)),
    'oni': dict(name='Oni-Gestalt', desc='Hörner wachsen dir', fx=dict(dmgm=1.4, size=1, hp=1), col=(230, 60, 50)),
    'shikigami': dict(name='Onmyōji-Meister', desc='Papier gehorcht dir', fx=dict(familiar=2, orbital=1), col=(240, 240, 240)),
    'yurei': dict(name='Yūrei-Gestalt', desc='Du bist zwischen den Welten', fx=dict(fly=1, spectral=1, spirit=4), col=(190, 220, 255)),
    'tengu': dict(name='Tengu-Herr', desc='Dir wachsen Flügel', fx=dict(fly=1, spd=20, multishot=1), col=(60, 60, 70)),
    'ryu': dict(name='Drachenblut', desc='Das Blut des Ryūjin', fx=dict(hp=2, pierce=1, homing=1, size=0.5), col=(80, 200, 220)),
    'kami': dict(name='Kami-Erleuchtung', desc='Göttliches Licht umgibt dich', fx=dict(shield=1, dmgm=1.3, aura=1), col=(255, 230, 140)),
    'tanuki': dict(name='Bake-Danuki', desc='Meister der Verwandlung und des Geldes', fx=dict(coins=30, luck=3, gold_shots=0.25, discount=1), col=(160, 110, 70)),
}

# =====================================================================  AKTIVE ITEMS
ACTIVES = {
    'ofuda_sturm': dict(name='Ofuda-Sturm', desc='Ein Ring aus Talismanen', icon='scroll', col=(230, 60, 60), charge=3),
    'kagura_suzu': dict(name='Kagura-Suzu', desc='Göttlicher Tanz: unverwundbar', icon='bell', col=GOLD, charge=4),
    'tanuki_blatt': dict(name='Tanuki-Blatt', desc='Verwandelt Items im Raum', icon='leaf', col=(90, 170, 80), charge=6),
    'uchide_kozuchi': dict(name='Uchide no Kozuchi', desc='Der Glückshammer klopft Münzen', icon='hammer', col=(220, 170, 60), charge=4),
    'tamatebako': dict(name='Tamatebako', desc='Was ist wohl in der Kiste?', icon='box', col=(200, 50, 90), charge=2),
    'raijin_taiko': dict(name='Raijin-Taiko', desc='Blitze treffen alle Feinde', icon='drum', col=(250, 220, 80), charge=4),
    'tsukuyomi_spiegel': dict(name='Mondspiegel', desc='Die Zeit steht still', icon='mirror', col=(200, 210, 255), charge=4),
    'sake_kalebasse': dict(name='Sake-Kalebasse', desc='Heilt und macht mutig', icon='gourd', col=(220, 220, 200), charge=3),
    'shikigami_ruf': dict(name='Shikigami-Ruf', desc='Papierkrieger stürzen sich auf Feinde', icon='doll', col=(240, 240, 240), charge=3),
    'onryo_kerze': dict(name='Kerze der Onryō', desc='Fluch auf alle Feinde', icon='flame', col=(170, 90, 230), charge=3),
    'hyotan_sauger': dict(name='Saugkalebasse', desc='Saugt Geschosse ein und schießt zurück', icon='gourd', col=(200, 120, 60), charge=2),
    'oni_trommel': dict(name='Oni-Kriegstrommel', desc='Sechs Sekunden Oni-Wut: fast doppelter Schaden', icon='drum', col=(220, 60, 50), charge=3),
    'kitsune_laterne': dict(name='Kitsune-Laterne', desc='Vier Fuchsfeuer umkreisen dich', icon='lantern', col=(120, 180, 255), charge=3),
    'horagai': dict(name='Horagai', desc='Der Muschelhornruf lähmt alle Yokai', icon='shell', col=(240, 210, 190), charge=3),
    'tengu_uchiwa': dict(name='Tengu-Uchiwa', desc='Ein Windstoß fegt alles fort', icon='fan', col=(60, 140, 60), charge=2),
    # Quest-Belohnungen (gesperrt bis zum Erfolg, siehe ACHIEVEMENTS 'q_*')
    'mondkine': dict(name='Kine des Mondhasen', desc='Ein Mörserschlag betäubt alles in der Nähe', icon='mondkine', col=(235, 235, 255), charge=3, locked=True),
    'shiomitsu_tama': dict(name='Shiomitsu-Tama', desc='Ryūjins Flutjuwel spült alle Geschosse fort', icon='shiomitsu_tama', col=(90, 170, 255), charge=4, locked=True),
    'matsuri_uchiwa': dict(name='Matsuri-Uchiwa', desc='Hanabi! Feuerwerk zerplatzt über den Feinden', icon='matsuri_uchiwa', col=(255, 140, 90), charge=3, locked=True),
    'totsuka': dict(name='Totsuka no Tsurugi', desc='Die Klinge, die Orochi zerteilte, trifft jeden Feind', icon='totsuka', col=(220, 230, 250), charge=5, locked=True),
    'mayoiga_wan': dict(name='Mayoiga-Wan', desc='Die Schale aus dem verborgenen Haus zeigt den Weg und füllt sich', icon='mayoiga_wan', col=(200, 70, 60), charge=4, locked=True),
    'nusa': dict(name='Nusa des Ōharae', desc='Die Große Reinigung tilgt Fluch und Geschosse und schützt kurz', icon='nusa', col=(245, 245, 235), charge=3, locked=True),
    'yatagarasu_feder': dict(name='Yatagarasu-Feder', desc='Die dreibeinige Krähe weist deinen Würfen den Weg', icon='yatagarasu_feder', col=(60, 60, 110), charge=3, locked=True),
}

# =====================================================================  CHARAKTERE
CHARS = {
    'hana': dict(name='Hana', title='Die Schreinmaid', desc='Ausgeglichen. Findet öfter Reinigungssalz.',
                 hp=6, spirit=0, fx=dict(salts_regen=0.15), items=[], active='ofuda_sturm', coins=0, keys=0, salts=2,
                 unlock='Von Beginn an verfügbar'),
    'kenji': dict(name='Kenji', title='Der Rōnin', desc='Kämpft mit dem Katana: Schwerthiebe zerschlagen auch Geschosse. Die Ausweichrolle schneidet.',
                  hp=6, spirit=0, fx=dict(dmgm=1.0, knock=1, dash_dmg=1), items=[], active=None,
                  coins=0, keys=0, salts=2, unlock='Besiege einen Boss in Kapitel II'),
    'kuzunoha': dict(name='Kuzunoha', title='Die Fuchsfrau', desc='Schnell und zerbrechlich. Ihre Rolle löscht Geschosse.',
                     hp=4, spirit=0, fx=dict(spd=20, dmgm=0.85, dash_reflect=1), items=['kitsunebi'], active=None,
                     coins=0, keys=0, salts=2, unlock='Werde zum Kitsune-Avatar'),
    'ponpoko': dict(name='Ponpoko', title='Der Tanuki', desc='Goldene Talismane und Münzmagnet. Viel Leben, viel Glück.',
                    hp=8, spirit=0, fx=dict(spd=-12, luck=2, gold_shots=0.1, magnet=1), items=[], active='tanuki_blatt',
                    coins=25, keys=1, salts=1, unlock='Sammle insgesamt 300 Mon'),
    'benkei': dict(name='Benkei', title='Der Kriegermönch', desc='Stößt mit der Naginata weit voraus und blockt in jedem Raum einen Treffer.',
                   hp=10, spirit=0, fx=dict(spd=-8, dmgm=1.25, rate=-0.6, size=1.5, knock=1, shield=1), items=[],
                   active='kagura_suzu', coins=0, keys=0, salts=2, unlock='Besiege insgesamt 500 Yokai'),
    'okiku': dict(name='Okiku', title='Der Brunnengeist', desc='Nur Geisterherzen. Fliegt, Schüsse durch Wände.',
                  hp=0, spirit=6, fx=dict(fly=1, spectral=1, dmgm=0.95), items=[], active='onryo_kerze',
                  coins=0, keys=0, salts=2, unlock='Stirb 10-mal', spirit_only=True),
    'kotaro': dict(name='Kotarō', title='Das Tengu-Kind', desc='Fliegt von Anfang an und fächert Windstöße, die Feinde zurückwerfen.',
                   hp=6, spirit=0, fx=dict(fly=1, shotspd=40, spd=10), items=['karasu_feder'], active='tengu_uchiwa',
                   coins=0, keys=0, salts=2, unlock='Besiege Sōjōbō, den Tengu-König'),
    'seimei': dict(name='Seimei', title='Der Onmyōji', desc='Schwacher Schuss, aber Shikigami-Diener.',
                   hp=6, spirit=0, fx=dict(dmgm=0.85), items=['shikigami_papier', 'hitogata'], active='shikigami_ruf',
                   coins=0, keys=0, salts=2, unlock='Gewinne einen Lauf'),
    'akago': dict(name='Akago', title='Das Oni-Kind', desc='Schlägt mit der Keule zu und wird stärker, je verletzter es ist.',
                  hp=8, spirit=0, fx=dict(rage=1, dmgm=1.1), items=['oni_sake'], active=None,
                  coins=0, keys=0, salts=1, unlock='Schließe 3 Oni-Pakte'),
    'susanoo': dict(name='Susanoo', title='Der Sturmgott', desc='Ein Gott unter Sterblichen. Sein Schwert sendet Wellen, Blitze folgen ihm.',
                    hp=6, spirit=0, fx=dict(dmgm=1.0, rate=0.15, raijin_chance=0.08), items=['kusanagi'], active='raijin_taiko',
                    coins=0, keys=0, salts=3, unlock='Besiege einen Boss in Takamagahara'),
}
CHAR_ORDER = ['hana', 'kenji', 'kuzunoha', 'ponpoko', 'benkei', 'okiku', 'kotaro', 'seimei', 'akago', 'susanoo']

# =====================================================================  YOKAI (Gegner)
def A(kind, **kw):
    d = dict(kind=kind, n=1, spread=0.0, speed=110, cd=2.0, col=(240, 80, 120), eff=None, r=3)
    d.update(kw)
    return d


ENEMIES = {
    'hitodama': dict(name='Hitodama', sprite='hitodama', hp=6, speed=36, r=6, move='float', attack=None, fly=True, glow=(120, 220, 255)),
    'kodama': dict(name='Kodama', sprite='kodama', hp=10, speed=0, r=7, move='static', attack=A('ring', n=6, speed=70, cd=2.6, col=(200, 255, 200))),
    'kappa': dict(name='Kappa', sprite='kappa', hp=11, speed=34, r=7, move='wander', attack=A('aimed', speed=120, cd=2.2, col=(100, 190, 255))),
    'kasa_obake': dict(name='Kasa-obake', sprite='kasa_obake', hp=9, speed=95, r=7, move='hop', attack=None),
    'bakezori': dict(name='Bake-zōri', sprite='bakezori', hp=7, speed=62, r=6, move='chase', attack=None, erratic=True),
    'tsuchinoko': dict(name='Tsuchinoko', sprite='tsuchinoko', hp=10, speed=40, r=7, move='charge', attack=None),
    'kitsunebi_e': dict(name='Kitsune-bi', sprite='kitsunebi_e', hp=10, speed=55, r=6, move='circle', attack=A('aimed', speed=110, cd=2.4, col=(120, 180, 255)), glow=(120, 180, 255)),
    'chochin': dict(name='Chōchin-obake', sprite='chochin', hp=13, speed=26, r=7, move='float', attack=A('cross', speed=95, cd=2.4, col=(255, 160, 60)), fly=True, glow=(255, 180, 90)),
    'nopperabo': dict(name='Nopperabō', sprite='nopperabo', hp=15, speed=0, r=7, move='teleport', attack=A('aimed', n=3, spread=0.35, speed=115, cd=2.2, col=(230, 220, 200))),
    'gaki': dict(name='Gaki', sprite='gaki', hp=13, speed=46, r=7, move='chase', attack=None, death=('split', 'gaki_small', 2)),
    'gaki_small': dict(name='Kleiner Gaki', sprite='gaki_small', hp=4, speed=66, r=4, move='chase', attack=None),
    'ittan_momen': dict(name='Ittan-momen', sprite='ittan_momen', hp=11, speed=72, r=7, move='bounce', attack=None, fly=True),
    'bakeneko': dict(name='Bakeneko', sprite='bakeneko', hp=15, speed=50, r=7, move='charge', attack=None),
    'onibi': dict(name='Onibi', sprite='onibi', hp=7, speed=44, r=6, move='float', attack=None, fly=True, death=('explode', 8), glow=(190, 120, 255)),
    'karasu_tengu': dict(name='Karasu-Tengu', sprite='karasu_tengu', hp=16, speed=70, r=7, move='circle', attack=A('aimed', n=3, spread=0.3, speed=125, cd=2.0, col=(90, 90, 110)), fly=True),
    'yuki_warashi': dict(name='Yuki-warashi', sprite='yuki_warashi', hp=14, speed=34, r=7, move='wander', attack=A('aimed', n=2, spread=0.2, speed=105, cd=2.0, col=(190, 240, 255), eff='slow')),
    'kamaitachi': dict(name='Kamaitachi', sprite='kamaitachi', hp=12, speed=55, r=6, move='charge', attack=None, fast_charge=True),
    'yamabiko': dict(name='Yamabiko', sprite='yamabiko', hp=18, speed=0, r=7, move='static', attack=A('mirror', speed=120, cd=0.5, col=(150, 160, 210))),
    'heikegani': dict(name='Heikegani', sprite='heikegani', hp=20, speed=40, r=7, move='side', attack=A('ring', n=8, speed=80, cd=2.8, col=(150, 220, 255))),
    'funayurei': dict(name='Funayūrei', sprite='funayurei', hp=13, speed=40, r=7, move='float', attack=A('aimed', speed=100, cd=2.6, col=(150, 230, 230)), fly=True, glow=(150, 230, 230)),
    'ningyo': dict(name='Ningyo', sprite='ningyo', hp=15, speed=0, r=7, move='teleport', attack=A('aimed', speed=190, cd=1.6, col=(120, 240, 220))),
    'isonade': dict(name='Isonade', sprite='isonade', hp=20, speed=60, r=7, move='burrow', attack=A('ring', n=10, speed=90, cd=99, col=(140, 160, 200))),
    'oni': dict(name='Oni', sprite='oni', hp=46, speed=32, r=10, move='chase', attack=A('aimed', n=3, spread=0.4, speed=100, cd=3.0, col=(255, 90, 60)), big=True),
    'shikome': dict(name='Shikome', sprite='shikome', hp=16, speed=78, r=7, move='chase', attack=None, erratic=True),
    'tsuchigumo': dict(name='Tsuchigumo', sprite='tsuchigumo', hp=28, speed=26, r=9, move='wander', attack=A('spawn', what='kumo', cd=3.2, max=4)),
    'kumo': dict(name='Kumo', sprite='kumo', hp=3, speed=82, r=4, move='chase', attack=None),
    'shinigami': dict(name='Shinigami', sprite='shinigami', hp=32, speed=22, r=9, move='float', attack=A('spiral', n=3, speed=85, cd=3.4, col=(170, 100, 230)), fly=True),
    'tesso': dict(name='Tesso', sprite='tesso', hp=4, speed=88, r=4, move='chase', attack=None, group=3, erratic=True),
    'abura_akago': dict(name='Abura-akago', sprite='abura_akago', hp=12, speed=38, r=6, move='float', attack=A('trail', cd=0.45), fly=True, glow=(255, 160, 60)),
    'nurikabe': dict(name='Nurikabe', sprite='nurikabe', hp=70, speed=17, r=12, move='chase', attack=None, heavy=True, big=True),
    'mokumokuren': dict(name='Mokumokuren', sprite='mokumokuren', hp=16, speed=0, r=7, move='static', attack=A('aimed', speed=200, cd=1.5, col=(255, 250, 220))),
    'jinmenju': dict(name='Jinmenju', sprite='jinmenju', hp=32, speed=0, r=8, move='static', attack=A('spiral', n=2, speed=70, cd=4.0, col=(250, 200, 150))),
    'yosuzume': dict(name='Yosuzume', sprite='yosuzume', hp=3, speed=95, r=4, move='circle', attack=None, fly=True, group=4),
    'enenra': dict(name='Enenra', sprite='enenra', hp=14, speed=30, r=7, move='float', attack=A('trail', cd=0.6, smoke=True), fly=True),
    'gyuki': dict(name='Gyūki', sprite='gyuki', hp=34, speed=42, r=9, move='charge', attack=None, charge_ring=10),
    'kamikiri': dict(name='Kamikiri', sprite='kamikiri', hp=11, speed=60, r=6, move='charge', attack=None, fast_charge=True),
    'kerakera_onna': dict(name='Kerakera-onna', sprite='kerakera_onna', hp=28, speed=26, r=8, move='wander', attack=A('ring', n=16, speed=75, cd=3.2, col=(240, 120, 200), double=True)),
    'sazae_oni': dict(name='Sazae-oni', sprite='sazae_oni', hp=24, speed=38, r=7, move='side', attack=A('aimed', n=5, spread=0.22, speed=105, cd=2.6, col=(250, 170, 190))),
    'hyosube': dict(name='Hyōsube', sprite='hyosube', hp=12, speed=55, r=6, move='chase', attack=A('ring', n=6, speed=80, cd=2.6, col=(200, 160, 110)), erratic=True),
    'tenome': dict(name='Tenome', sprite='tenome', hp=18, speed=24, r=7, move='wander', attack=A('aimed', n=2, spread=0.15, speed=140, cd=1.8, col=(255, 240, 160))),
    'nekomata': dict(name='Nekomata', sprite='nekomata', hp=20, speed=55, r=7, move='charge', attack=A('aimed', n=2, spread=0.2, speed=120, cd=2.8, col=(250, 170, 90)), fast_charge=True),
    'kasha': dict(name='Kasha', sprite='kasha', hp=22, speed=50, r=7, move='float', attack=A('trail', cd=0.35), fly=True, glow=(255, 120, 40)),
    'tsurube_otoshi': dict(name='Tsurube-otoshi', sprite='tsurube_otoshi', hp=20, speed=0, r=8, move='drop', attack=A('ring', n=10, speed=85, cd=99, col=(220, 200, 160))),
    'wanyudo': dict(name='Wanyūdō', sprite='wanyudo', hp=24, speed=95, r=8, move='bounce', attack=A('trail', cd=0.3), fly=True, glow=(255, 120, 40)),
    'katawaguruma': dict(name='Katawaguruma', sprite='katawaguruma', hp=16, speed=60, r=7, move='zigzag', attack=A('aimed', n=3, spread=0.3, speed=110, cd=2.4, col=(255, 160, 80)), glow=(255, 150, 60)),
    'azukiarai': dict(name='Azukiarai', sprite='azukiarai', hp=10, speed=0, r=6, move='static', attack=A('aimed', n=3, spread=0.3, speed=75, cd=2.8, col=(170, 60, 60), r=2)),
    'bake_danuki': dict(name='Bake-danuki', sprite='bake_danuki', hp=12, speed=0, r=7, move='teleport', attack=A('ring', n=8, speed=80, cd=2.2, col=(110, 180, 80))),
    'nuppeppo': dict(name='Nuppeppō', sprite='nuppeppo', hp=22, speed=24, r=8, move='chase', attack=None, death=('split', 'nuppeppo_klein', 2)),
    'nuppeppo_klein': dict(name='Kleiner Nuppeppō', sprite='gaki_small', hp=6, speed=44, r=4, move='chase', attack=None),
    'kappa_small': dict(name='Kappa', sprite='kappa_small', hp=6, speed=50, r=5, move='chase', attack=None),
    'karasu': dict(name='Krähe', sprite='karasu', hp=5, speed=80, r=5, move='float', attack=None, fly=True),
}

CHAMPIONS = {
    'rot': dict(name='Roter', col=(255, 120, 120), hp=2.0),
    'blau': dict(name='Blauer', col=(120, 160, 255), hp=1.3, fire=1.6),
    'gold': dict(name='Goldener', col=(255, 220, 90), hp=1.4, coins=3),
    'lila': dict(name='Violetter', col=(200, 120, 255), hp=1.3, explode=True),
    'gruen': dict(name='Grüner', col=(130, 240, 140), hp=1.3, regen=True),
    'weiss': dict(name='Weißer', col=(255, 255, 255), hp=1.5, speed=1.4),
    'geist': dict(name='Geisterhafter', col=(170, 220, 255), hp=1.3, ghost=True),
    'teiler': dict(name='Teilender', col=(255, 170, 120), hp=1.2, splitter=True),
}

# =====================================================================  BOSSE (Infos; Logik in bosses.py)
BOSSES = {
    'omukade': dict(name='Ōmukade', title='Der Riesentausendfüßler', hp=230),
    'kappa_ou': dict(name='Kappa-Ō', title='König der Flussgeister', hp=220),
    'jorogumo': dict(name='Jorōgumo', title='Die Spinnenfrau', hp=225),
    'gashadokuro': dict(name='Gashadokuro', title='Das hungrige Riesenskelett', hp=340),
    'rokurokubi': dict(name='Rokurokubi', title='Die mit dem langen Hals', hp=310),
    'nue': dict(name='Nue', title='Die Chimäre der Nacht', hp=320),
    'sojobo': dict(name='Sōjōbō', title='König der Tengu', hp=430),
    'raiju': dict(name='Raijū', title='Das Donnerbiest', hp=410),
    'yuki_onna': dict(name='Yuki-onna', title='Die Schneefrau', hp=400),
    'umibozu': dict(name='Umibōzu', title='Der Meeresmönch', hp=540),
    'ryujin': dict(name='Ryūjin', title='Der Drachenkönig', hp=560),
    'bake_kujira': dict(name='Bake-kujira', title='Der Geisterwal', hp=530),
    'orochi': dict(name='Yamata no Orochi', title='Die achtköpfige Schlange', hp=880),
    'shuten_doji': dict(name='Shuten-dōji', title='König der Oni', hp=820),
    'tamamo': dict(name='Tamamo-no-Mae', title='Die neunschwänzige Füchsin', hp=800),
    'oonyudo': dict(name='Ōnyūdō', title='Der riesige Mönch', hp=240),
    'nurarihyon': dict(name='Nurarihyon', title='Oberhaupt aller Yokai', hp=330),
    'kamaitachi_trio': dict(name='Die drei Kamaitachi', title='Stolpern, Schneiden, Heilen', hp=420),
    'akkorokamui': dict(name='Akkorokamui', title='Der rote Riesenkrake', hp=560),
    'enma': dict(name='Enma-Daiō', title='Richter der Unterwelt', hp=860),
    'izanami': dict(name='Izanami', title='Die Göttin, die in Yomi blieb', hp=1450),
    'amaterasu': dict(name='Amaterasu', title='Die Sonne, die sich verbarg', hp=2400),
    'kagutsuchi': dict(name='Kagutsuchi', title='Der Gott des Feuers', hp=1450),
    'mikaboshi': dict(name='Amatsu-Mikaboshi', title='Der böse Stern des Himmels', hp=1500),
    'fujin': dict(name='Fūjin', title='Der Gott des Windes', hp=1600),
}
BOSS_REWARD = {  # Freischaltung beim ersten Sieg
    'omukade': 'senbazuru', 'kappa_ou': 'komainu', 'jorogumo': 'ronin_schwur', 'gashadokuro': 'sanzu_muenze',
    'rokurokubi': 'tengu_auge', 'nue': 'yata_kagami', 'sojobo': None, 'raiju': 'kusanagi',
    'yuki_onna': 'yasakani', 'umibozu': None, 'ryujin': None, 'bake_kujira': None,
    'oonyudo': 'onyudo_kette', 'nurarihyon': 'nurarihyon_pfeife', 'kamaitachi_trio': 'kamaitachi_klingen',
    'akkorokamui': 'akkoro_tinte', 'enma': 'enma_spiegel', 'izanami': 'izanami_schleier', 'amaterasu': None, 'kagutsuchi': 'kagutsuchi_glut',
    'fujin': 'kaze_bukuro', 'orochi': 'yamata_zahn', 'shuten_doji': 'shuten_schale', 'tamamo': 'kyubi_juwel', 'mikaboshi': 'hoshi_splitter',
}

# =====================================================================  PRÜFUNGEN (Herausforderungen)
CHALLENGES = [
    dict(id='glaskanone', name='Glaskanone', char='hana', desc='Nur ein Herz – aber doppelter Schaden.', goal=5),
    dict(id='fuchspfad', name='Der Pfad des Fuchses', char='kuzunoha', desc='Startet mit Fuchs-Items. Keine Läden.', goal=5),
    dict(id='dunkle_nacht', name='Die dunkelste Nacht', char='kenji', desc='Jede Ebene ist verflucht und finster.', goal=5),
    dict(id='zeitlauf', name='Wettlauf gegen den Morgen', char='kotaro', desc='Besiege Kapitel V in 15 Minuten.', goal=5),
    dict(id='kaufmann', name='Der reiche Kaufmann', char='ponpoko', desc='99 Mon zu Beginn, aber Schatzräume werden zu Läden.', goal=5),
    dict(id='oni_pakt', name='Pakt mit dem Teufel', char='akago', desc='Drei Oni-Items, aber nur ein Herzcontainer.', goal=5),
    dict(id='bossrush', name='Boss-Ansturm', char='benkei', desc='Nur Bosskämpfe – nach jedem Boss ein Item.', goal=6),
    dict(id='papiermeister', name='Papiermeister', char='seimei', desc='Du schießt nicht – nur deine Shikigami kämpfen.', goal=5),
    dict(id='verbannung', name='Verbannt aus Takamagahara', char='susanoo', desc='Nur Geisterherzen – keine Heilung, kein Herzcontainer.', goal=5),
    dict(id='langer_weg', name='Der lange Weg', char='okiku', desc='Alle zehn Ebenen bis Kapitel V – ohne Läden, Oni-Pakte kosten doppelt.', goal=5),
]

# =====================================================================  ERFOLGE
# (id, Name, Beschreibung, Belohnung)  – geprüft in run.py über check_achievements
ACHIEVEMENTS = [
    ('first_blood', 'Erster Yokai', 'Besiege deinen ersten Yokai', None),
    ('first_boss', 'Dämonenjäger', 'Besiege deinen ersten Boss', None),
    ('chapter2', 'Zwei Gesichter', 'Besiege beide Bosse eines Kapitels in einem Lauf', None),
    ('floor8', 'Tief in der Nacht', 'Erreiche Ebene 8', None),
    ('floor11', 'Über den Wolken', 'Erreiche Ebene 11', None),
    ('items40', 'Schatzkammer', 'Trage 40 Items in einem Lauf', None),
    ('yomeiri', 'Hochzeitsgast', 'Lass eine Fuchshochzeit ungestört vorbeiziehen', None),
    ('kakurenbo', 'Gefunden!', 'Finde Zashiki-warashi beim Versteckspiel', None),
    ('ema_wunsch', 'Ein Wunsch', 'Hänge eine Ema-Tafel auf', None),
    ('feste', 'Festtagsgast', 'Erlebe alle Ereignisräume: Fuchshochzeit, Versteckspiel, Ema-Wand, Nachtparade, Shinkirō und Mochitsuki', None),
    ('mochitsuki', 'Aitori', 'Wende beim Mochitsuki des Mondhasen jeden Teig, ohne getroffen zu werden', None),
    ('hyakki', 'Unbemerkt', 'Lass die Nachtparade vorbeiziehen, ohne getroffen zu werden', None),
    ('musubi', 'Fluch gebunden', 'Binde ein Unglückslos an das Musubi-Gestell', None),
    ('lexikon_half', 'Yōkai-Kundige', 'Begegne der Hälfte aller Yōkai', None),
    ('lexikon_all', 'Hyakki Yagyō', 'Begegne allen Yōkai des Lexikons', None),
    ('kenji', 'Herrenlos', 'Besiege einen Boss in Kapitel II', ('char', 'kenji')),
    ('kuzunoha', 'Neun Schwänze', 'Werde zum Kitsune-Avatar', ('char', 'kuzunoha')),
    ('ponpoko', 'Reicher Tanuki', 'Sammle insgesamt 300 Mon', ('char', 'ponpoko')),
    ('benkei', 'Tausend Schwerter', 'Besiege insgesamt 500 Yokai', ('char', 'benkei')),
    ('okiku', 'Zehnmal gestorben', 'Stirb 10-mal', ('char', 'okiku')),
    ('kotaro', 'Tengu-Bezwinger', 'Besiege Sōjōbō', ('char', 'kotaro')),
    ('seimei', 'Die Nacht überlebt', 'Gewinne einen Lauf', ('char', 'seimei')),
    ('akago', 'Pakt mit den Oni', 'Schließe insgesamt 3 Oni-Pakte', ('char', 'akago')),
    ('susanoo', 'Der Himmel ist frei', 'Besiege einen Boss in Takamagahara', ('char', 'susanoo')),
    ('hard', 'Oni-Modus', 'Gewinne einen Lauf (schaltet den Oni-Modus frei)', ('mode', 'hard')),
    ('heaven', 'Der Weg nach oben', 'Gewinne einen Lauf (öffnet Takamagahara)', ('mode', 'heaven')),
    ('synergy1', 'Harmonie', 'Entdecke eine Synergie', ('item', 'tanabata')),
    ('synergy10', 'Meister der Harmonie', 'Entdecke 10 verschiedene Synergien', None),
    ('transform', 'Verwandlung', 'Erlebe eine Transformation', None),
    ('daikichi', 'Großes Glück', 'Ziehe ein Daikichi-Omikuji', None),
    ('alle_lose', 'Alle Lose', 'Ziehe Daikichi, Kichi, Chūkichi, Shōkichi und Kyō je einmal', None),
    ('onsen', 'Entspannung', 'Bade in einer heißen Quelle', None),
    ('rich', 'Wie Daikoku', 'Habe 99 Mon gleichzeitig', None),
    ('nohit', 'Unberührt', 'Besiege einen Boss ohne Treffer', None),
    ('items10', 'Sammler', 'Sammle 10 Items in einem Lauf', None),
    ('kami', 'Gesegnet', 'Erhalte einen Kami-Segen', None),
    ('challenge', 'Herausforderung angenommen', 'Schließe einen Kampfraum ab', None),
    ('donor', 'Großzügig', 'Spende 30 Mon in Saisen-Kästen', ('item', 'ema')),
    ('floor5', 'Die Tore von Yomi', 'Erreiche die Unterwelt (Kapitel V)', None),
    ('win_hard', 'Oni unter Oni', 'Gewinne im Oni-Modus', None),
    ('all_chars', 'Hyakki Yagyō', 'Schalte alle Charaktere frei', None),
    ('secret', 'Verborgene Pfade', 'Finde einen Geheimraum (Reinigungssalz an Wänden!)', ('item', 'geheimkarte')),
    ('secret10', 'Schatzjäger', 'Finde 10 Geheimräume', None),
    ('yomi', 'Rückkehr aus Yomi', 'Besiege Izanami in ihrem Totenpalast', ('item', 'yomi_momo')),
    ('iwato', 'Die Sonne kehrt zurück', 'Besiege Amaterasu in Ama-no-Iwato', ('item', 'uzume_suzu')),
    ('all_bosses', 'Bezwinger der Nachtparade', 'Besiege alle 24 Bosse', None),
    ('teahouse', 'Teezeremonie', 'Trinke im Teehaus', None),
    ('slots', 'Glücksspieler', 'Spiele am Tanuki-Automaten', None),
    ('endless', 'Die Nacht endet nie', 'Besiege einen Boss in Takamagahara (schaltet die Endlose Nacht frei)', ('mode', 'endless')),
    ('loop1', 'Noch eine Runde', 'Erreiche Schleife 2 in der Endlosen Nacht', None),
    ('library', 'Bücherwurm', 'Besuche ein Schriftrollenarchiv', None),
    ('dojo', 'Meister des Dōjō', 'Besiege die Champions im Dōjō', None),
    ('ch_glaskanone', 'Prüfung: Glaskanone', 'Bestehe die Prüfung „Glaskanone“', ('item', 'fuurin')),
    ('ch_fuchspfad', 'Prüfung: Der Pfad des Fuchses', 'Bestehe die Prüfung „Der Pfad des Fuchses“', ('item', 'abura_age')),
    ('ch_dunkle_nacht', 'Prüfung: Die dunkelste Nacht', 'Bestehe die Prüfung „Die dunkelste Nacht“', ('item', 'tsukikage')),
    ('ch_zeitlauf', 'Prüfung: Wettlauf gegen den Morgen', 'Bestehe die Prüfung „Wettlauf gegen den Morgen“', ('item', 'hayate_waraji')),
    ('ch_kaufmann', 'Prüfung: Der reiche Kaufmann', 'Bestehe die Prüfung „Der reiche Kaufmann“', ('item', 'senryo_bako')),
    ('ch_oni_pakt', 'Prüfung: Pakt mit dem Teufel', 'Bestehe die Prüfung „Pakt mit dem Teufel“', ('item', 'keppan')),
    ('ch_bossrush', 'Prüfung: Boss-Ansturm', 'Bestehe die Prüfung „Boss-Ansturm“', ('item', 'miidera_kane')),
    ('ch_papiermeister', 'Prüfung: Papiermeister', 'Bestehe die Prüfung „Papiermeister“', ('item', 'nademono')),
    ('ch_langer_weg', 'Prüfung: Der lange Weg', 'Bestehe die Prüfung „Der lange Weg“', ('item', 'kongozue')),
    ('ch_verbannung', 'Prüfung: Verbannt aus Takamagahara', 'Bestehe die Prüfung „Verbannt aus Takamagahara“', ('item', 'aokusa_mino')),
    ('foxfire', 'Kitsunebi-Fänger', 'Fange ein Fuchsfeuer im Inari-Schrein', None),
    ('quirks_all', 'Wanderer der Welten', 'Erlebe die Eigenheiten aller Biome', None),
    ('synergy25', 'Meister der Harmonie', 'Entdecke 25 verschiedene Synergien', None),
    ('q_mochi', 'Gehilfe des Mondhasen', 'Gelinge dreimal beim Mochitsuki (mindestens 5 Teige gewendet)', ('active', 'mondkine')),
    ('q_nohit5', 'Unberührbar', 'Besiege insgesamt 5 Bosse ohne Treffer', ('active', 'shiomitsu_tama')),
    ('q_feste4', 'Festnacht', 'Erlebe vier verschiedene Ereignisräume in einem Lauf', ('active', 'matsuri_uchiwa')),
    ('q_pruefungen', 'Alle Prüfungen', 'Bestehe alle zehn Prüfungen', ('active', 'totsuka')),
    ('q_geheim3', 'Mayoiga', 'Entdecke drei Geheimräume in einem Lauf', ('active', 'mayoiga_wan')),
    ('q_kami50', 'Ōharae', 'Nimm insgesamt 50 Kami-Gaben an', ('active', 'nusa')),
    ('q_loop3', 'Ewige Nacht', 'Erreiche Schleife 3 in der Endlosen Nacht', ('active', 'yatagarasu_feder')),
]


# Figuren-Siegel (wie die Abschlussmarken in Isaac): Siegel → Item je Figur
MARKS = [('boss3', 'Kapitel III', 'Besiege einen Boss in Kapitel III'),
         ('sieg', 'Sieg', 'Gewinne einen Lauf'),
         ('himmel', 'Takamagahara', 'Besiege einen Boss in Takamagahara'),
         ('oku', 'Yomi / Iwato', 'Besiege Izanami oder Amaterasu'),
         ('oni', 'Oni-Modus', 'Gewinne im Oni-Modus')]
CHAR_UNLOCKS = {
    'hana': {'boss3': 'haraegushi', 'sieg': 'hi_ogi', 'himmel': 'tamagushi', 'oku': 'kotodama', 'oni': 'onusa'}, 'kenji': {'boss3': 'zanshin_tsuba', 'sieg': 'muramasa', 'himmel': 'kesagiri', 'oku': 'tsubame_gaeshi', 'oni': 'ichi_no_tachi'}, 'kuzunoha': {'boss3': 'kuzu_blatt', 'sieg': 'fuchs_trugbild', 'himmel': 'hoshi_tama', 'oku': 'shinoda_blatt', 'oni': 'kitsune_chochin'},
    'ponpoko': {'boss3': 'bunbuku_kessel', 'sieg': 'shigaraki_tanuki', 'himmel': 'tanuki_bayashi', 'oku': 'tanuki_tokkuri', 'oni': 'tanuki_kesa'}, 'benkei': {'boss3': 'tausendstes_schwert', 'sieg': 'tachi_ojo', 'himmel': 'gojo_giboshi', 'oku': 'nanatsu_dogu', 'oni': 'kanjincho'}, 'okiku': {'boss3': 'neunter_teller', 'sieg': 'tsurube', 'himmel': 'ido_kagami', 'oku': 'zehnter_teller', 'oni': 'okiku_ido'},
    'kotaro': {'boss3': 'tengu_tsubute', 'sieg': 'kakuremino', 'himmel': 'sojobo_hane', 'oku': 'hanadaka_men', 'oni': 'ushiwaka_fue'}, 'seimei': {'boss3': 'taizan_fukun', 'sieg': 'hoki_naiden', 'himmel': 'juni_shinsho', 'oku': 'kikyo_mon', 'oni': 'seimei_ido'}, 'akago': {'boss3': 'ibaraki_arm', 'sieg': 'masakari', 'himmel': 'setsubun_mame', 'oku': 'oni_tsuno', 'oni': 'kodomo_kanabo'},
    'susanoo': {'boss3': 'yashiori_sake', 'sieg': 'habakiri', 'himmel': 'murakumo', 'oku': 'kushinada_kushi', 'oni': 'ohabari'},
}
for _c, _ms in CHAR_UNLOCKS.items():
    for _m, _n, _d in MARKS:
        if _m in _ms:
            ACHIEVEMENTS.append(('m_%s_%s' % (_c, _m), '%s: %s' % (CHARS[_c]['name'], _n), '%s mit %s' % (_d, CHARS[_c]['name']), ('item', _ms[_m])))
    ACHIEVEMENTS.append(('meister_' + _c, 'Meister: ' + CHARS[_c]['name'], 'Alle Siegel mit %s – jeder Lauf beginnt mit einem ihrer Siegel-Items' % CHARS[_c]['name'], None))

# Kapitel VII (geheim, nach dem ersten Wahren Sieg): Izanamis Totenpalast tief in Yomi no Kuni
BIOMES['yomi_oku'] = dict(name='Totenpalast', jp='Yomi no Oku', depth=7, floor=(40, 26, 44), floor_pat='stone',
                          wall=(30, 14, 30), wall_pat='bone', rock=(80, 60, 80), moss=False, ambient='embers',
                          enemies=['shikome', 'gaki', 'shinigami', 'mezu', 'gozu', 'kasha', 'onibi', 'oni'],
                          music=('iwato', 165, 108, 'mystic', 54), weather='ash', dark=80,
                          grade=(70, 20, 90), pit='void', decor='bones')
DEPTH_BIOMES[7] = ['yomi_oku']
# Kapitel VII, zweiter Weg (nach dem ersten Wahren Sieg): Ama-no-Iwato, die Felsenhöhle der verborgenen Sonne.
# Nicht in DEPTH_BIOMES – nur die Iwato-Pforte führt hierher (Run.oku).
BIOMES['iwato'] = dict(name='Felsenhöhle der Sonne', jp='Ama-no-Iwato', depth=7, floor=(42, 28, 30), floor_pat='stone',
                       wall=(46, 28, 28), wall_pat='rock', rock=(110, 80, 60), moss=False, ambient='embers',
                       enemies=['komainu', 'tennin', 'karasu_tengu', 'kitsunebi_e', 'yamabiko', 'katawaguruma', 'kamaitachi', 'nurikabe'],
                       music=('iwato', 220, 100, 'mystic', 57), dark=95, grade=(110, 60, 10), pit='void', decor='cracks',
                       boss='amaterasu')
BOSS_POOL[6].remove('izanami')    # Izanami wartet jetzt in ihrem eigenen Reich
BOSS_POOL[7] = ['izanami']

for _k, _b in BIOMES.items():
    _b['_id'] = _k


# Jedes Item bekommt sein eigenes Symbol (assets/items/icons/<id>.png), falls vorhanden
def _own_icons():
    import os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'items', 'icons')
    for table in (ITEMS, ACTIVES, TRINKETS):
        for k, v in table.items():
            if os.path.exists(os.path.join(d, k + '.png')):
                v['icon'] = k


_own_icons()


# Waffen: Items und Figuren mit eigener Angriffsart (siehe weapons.py)
for _iid, _w in (('tamahagane', 'w_sword'), ('ronin_schwur', 'w_sword'), ('kusanagi', 'w_sword'), ('ame_nuboko', 'w_spear'),
                 ('shinigami_sense', 'w_scythe'), ('amaterasu', 'w_laser'), ('hachiman_bogen', 'w_bow'), ('yumi', 'w_bow'),
                 ('hamaya', 'w_bow'), ('kanabo', 'w_club'), ('tengu_faecher', 'w_fan')):
    ITEMS[_iid]['fx'][_w] = 1
ITEMS['kusanagi']['fx']['sword_wave'] = 1
for _c, _w in (('kenji', 'w_sword'), ('benkei', 'w_spear'), ('kotaro', 'w_fan'), ('susanoo', 'w_sword'), ('akago', 'w_club')):
    CHARS[_c]['fx'][_w] = 1
CHARS['susanoo']['fx']['sword_wave'] = 1


# Gegner thematisch zu den Biomen (keine Katzen an der Küste/in der Hölle, himmlische Wächter im Himmel)
BIOMES['uminobe']['enemies'] = ['funayurei', 'heikegani', 'isonade', 'ningyo', 'onibi', 'sazae_oni']
BIOMES['jigoku']['enemies'] = ['oni', 'shikome', 'shinigami', 'onibi', 'tsuchigumo', 'kasha', 'wanyudo', 'gaki']
BIOMES['takamagahara']['enemies'] = ['karasu_tengu', 'yamabiko', 'kamaitachi', 'katawaguruma', 'nurikabe', 'kitsunebi_e', 'ningyo', 'shinigami']


# Exklusive Item-Pools: jedes Item gehört genau einer Raumart (Schatzraum T, Laden S, Boss B, Kami-Schrein K, Oni-Schrein O, Ereignis Y)
def _exclusive_pools():
    for k, it in ITEMS.items():
        ps = [p for p in it['pools'] if p in 'TSBKOY']
        if len(ps) > 1:
            for pref in 'OKBS':
                if pref in ps:
                    ps = [pref]
                    break
        it['pools'] = ps or ['T']


_exclusive_pools()


# Balance-Check 1.2 (design/balance/balance-check-1.md)
def _balance_12():
    # Laden war fast nur Qualität 1: jedes fünfte Schatzraum-Item der Qualität 2 wandert in den Laden
    t2 = [k for k, it in ITEMS.items() if it['pools'] == ['T'] and it['q'] == 1 + 1]
    for k in t2[::5]:
        ITEMS[k]['pools'] = ['S']
    # Tiefe 4 hatte die kleinste Gegnervielfalt
    for b, extra in (('ryugu', ['kappa_small', 'onibi']), ('shinkai', ['kappa_small', 'onibi']), ('uminobe', ['kappa_small', 'yosuzume'])):
        for e in extra:
            if e not in BIOMES[b]['enemies']:
                BIOMES[b]['enemies'].append(e)


_balance_12()


# Balance-Check 3 (design/balance/balance-check-3.md): späte Gegner gefährlicher
def _balance_13():
    ENEMIES['shikome']['speed'] = 92
    ENEMIES['onibi']['attack'] = {'kind': 'trail', 'n': 1, 'spread': 0.0, 'speed': 110, 'cd': 0.7, 'col': (110, 160, 255), 'eff': None, 'r': 3}
    fa = ENEMIES['funayurei']['attack']
    fa['n'], fa['spread'] = 3, 0.25
    ENEMIES['kappa_small']['speed'] = 62
    ya = ENEMIES['yamabiko']['attack']               # Echo traf zu oft (Balance-Check 5)
    ya['cd'], ya['speed'] = 0.85, 105
    na = ENEMIES['nopperabo']['attack']               # Balance-Check 8: weiterhin Spitzenreiter
    na['n'], na['speed'] = 2, 105


_balance_13()


# Balance-Check 7: Figuren (design/balance/balance-check-7-figuren.md)
CHARS['susanoo']['fx']['dmgm'] = 0.65
CHARS['akago']['fx']['dmgm'] = 0.95
CHARS['kuzunoha']['fx']['dmgm'] = 1.0
BOSSES['izanami']['hp'] = 1250        # Boss-Test: brauchte fast doppelt so lange wie die anderen Endbosse
BOSSES['shuten_doji']['hp'] = 740


# Neue Gegner der Himmelsgefilde (v1.3)
ENEMIES['komainu'] = {'name': 'Komainu', 'sprite': 'komainu', 'hp': 36, 'speed': 64, 'r': 10, 'move': 'charge', 'attack': None,
                      'charge_ring': 8}
ENEMIES['tennin'] = {'name': 'Tennin', 'sprite': 'tennin', 'hp': 24, 'speed': 30, 'r': 9, 'move': 'float', 'fly': True,
                     'attack': {'kind': 'aimed', 'n': 5, 'spread': 0.17, 'speed': 112, 'cd': 2.5, 'col': (255, 226, 120),
                                'eff': None, 'r': 3}}
ENEMIES['zashiki'] = {'name': 'Zashiki-warashi', 'sprite': 'zashiki', 'hp': 12, 'speed': 42, 'r': 7, 'move': 'wander',
                      'attack': {'kind': 'aimed', 'n': 1, 'spread': 0.0, 'speed': 95, 'cd': 2.0, 'col': (110, 140, 255),
                                 'eff': None, 'r': 4}}
for _b in ('yashiki', 'obakedera'):
    BIOMES[_b]['enemies'].append('zashiki')
ENEMIES['kawauso'] = {'name': 'Kawauso', 'sprite': 'kawauso', 'hp': 9, 'speed': 44, 'r': 7, 'move': 'wander',
                      'attack': {'kind': 'aimed', 'n': 2, 'spread': 0.25, 'speed': 100, 'cd': 2.4, 'col': (150, 160, 180),
                                 'eff': None, 'r': 3}}
for _b in ('kawabe', 'chikurin'):
    BIOMES[_b]['enemies'].append('kawauso')
ENEMIES['nureonna'] = {'name': 'Nure-onna', 'sprite': 'nureonna', 'hp': 26, 'speed': 46, 'r': 9, 'move': 'zigzag',
                       'attack': {'kind': 'aimed', 'n': 3, 'spread': 0.28, 'speed': 108, 'cd': 2.5, 'col': (110, 210, 220),
                                  'eff': None, 'r': 3}}
for _b in ('uminobe', 'shinkai', 'ryugu'):
    BIOMES[_b]['enemies'].append('nureonna')
ENEMIES['gozu'] = {'name': 'Gozu', 'sprite': 'gozu', 'hp': 52, 'speed': 30, 'r': 11, 'move': 'chase',
                   'attack': {'kind': 'ring', 'n': 10, 'spread': 0.0, 'speed': 80, 'cd': 3.2, 'col': (230, 120, 70),
                              'eff': None, 'r': 3}}
for _b in ('enma_cho', 'jigoku'):
    BIOMES[_b]['enemies'].append('gozu')
ENEMIES['mezu'] = {'name': 'Mezu', 'sprite': 'mezu', 'hp': 44, 'speed': 62, 'r': 11, 'move': 'charge', 'attack': None,
                   'charge_ring': 8}
for _b in ('enma_cho', 'yomi'):
    BIOMES[_b]['enemies'].append('mezu')
ENEMIES['yamauba'] = {'name': 'Yamauba', 'sprite': 'yamauba', 'hp': 22, 'speed': 40, 'r': 8, 'move': 'chase',
                      'attack': {'kind': 'aimed', 'n': 3, 'spread': 0.22, 'speed': 125, 'cd': 2.3, 'col': (200, 210, 230),
                                 'eff': None, 'r': 3}}
for _b in ('kurama', 'yukiyama', 'oeyama'):
    BIOMES[_b]['enemies'].append('yamauba')
for _b in ('takamagahara', 'tsukiyomi'):
    BIOMES[_b]['enemies'] += ['komainu', 'tennin']
BIOMES['takamagahara']['enemies'] = [e for e in BIOMES['takamagahara']['enemies'] if e != 'ningyo']

