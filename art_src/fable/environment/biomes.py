"""Per-biome palettes + parameters. Ramps run dark -> light. Floors stay dark (value ~ #1e1a24..#2c2a36)."""
from core import mix

ORDER = ['chikurin', 'inari', 'obakedera', 'hakaba', 'kurama', 'yukiyama', 'ryugu', 'uminobe', 'yomi', 'jigoku',
         'takamagahara', 'kawabe', 'yashiki', 'oeyama', 'shinkai', 'enma_cho', 'tsukiyomi', 'yomi_oku']


def B(floor_pat, wall_pat, pit, dark, f, cap, w, k, **extra):
    """f: 4 floor colours (joint/dark, base, light, highlight); cap: (dark, mid, lip); w: wall face ramp x4;
    k: obstacle ramp x4"""
    d = dict(floor_pat=floor_pat, wall_pat=wall_pat, pit=pit, dark=dark,
             f0=f[0], f1=f[1], f2=f[2], f3=f[3], fb=mix(f[1], f[0], 0.45),
             cap0=cap[0], cap1=cap[1], lip=cap[2],
             w0=w[0], w1=w[1], w2=w[2], w3=w[3],
             k0=k[0], k1=k[1], k2=k[2], k3=k[3])
    d.update(extra)
    return d


# common accent ramps (dimmed versions of the character palette so the environment stays behind the sprites)
RED = ('#3a0e2a', '#6e1a2c', '#9a2a2a', '#c04a30')      # vermilion lacquer
GOLD = ('#5a3414', '#96661c', '#c89a30', '#ecd070')
BONE = ('#33283a', '#5a4a52', '#8a786a', '#b8a888')
MOSS = ('#12302c', '#1c4a34', '#2e6a3a', '#4e8a44')
WOOD = ('#1c121c', '#33202a', '#50302a', '#6e4630')
PAPER = ('#3a3a5c', '#6a6c8c', '#a0a4b8', '#d0d0d8')
LAVA = ('#4a0e1c', '#8a1c1a', '#c8481c', '#f0a030')
ICE = ('#1c2c58', '#2e4c80', '#5080b0', '#98cce8')
GLOW = ('#0e3a4a', '#1a6a78', '#3aa8a8', '#90e8d0')     # deep-sea bioluminescence
STONE = ('#191a28', '#2a2c40', '#40445c', '#5c627e')
SILVER = ('#2a3050', '#4a5478', '#7a86a8', '#b4c0d8')
VIOLET = ('#1a0c24', '#2e1638', '#48244e', '#6a3a64')     # Izanamis morscher Schwarzlack
ONIBI = ('#2a1a5a', '#5a3aa8', '#9a7ae0', '#d8c8ff')      # kaltes Totenfeuer

BIOMES = {
    'chikurin': B('grass', 'bamboo', 'void', 0,
                  ('#111c20', '#17272a', '#1f3530', '#2b4a38'), ('#0c161a', '#14282a', '#3a6a44'),
                  ('#102420', '#1a4030', '#2a6238', '#4a8a48'), ('#141c24', '#263a38', '#3c5a48', '#5c7c58'),
                  leaf=('#2a5a34', '#4a7a40')),
    'inari': B('gravel', 'torii', 'void', 0,
               ('#181622', '#23212d', '#2e2c3a', '#3b3948'), ('#110e18', '#1c1824', '#b03a2c'),
               RED, STONE, leaf=('#7a2224', '#a84028')),
    'obakedera': B('tatami', 'wood', 'void', 40,
                   ('#14121a', '#24251f', '#2c2e25', '#36392b'), ('#0e0c14', '#1a1620', '#5a4038'),
                   WOOD, ('#1a1622', '#3a2a2c', '#5a4034', '#7a5c40')),
    'hakaba': B('stone', 'stone', 'void', 60,
                ('#12121a', '#1f2129', '#272b33', '#30363e'), ('#0e0e16', '#1a1c26', '#4a5066'),
                ('#16161f', '#262834', '#383c4a', '#4e5466'), ('#16161f', '#2c2e3c', '#444a5a', '#646c80')),
    'kurama': B('gravel', 'rock', 'void', 0,
                ('#19151d', '#252129', '#312c33', '#3e383e'), ('#100e16', '#1c1a26', '#505672'),
                ('#18182a', '#282a42', '#3c405a', '#565c78'), ('#18182a', '#2e3048', '#464a64', '#666c88')),
    'yukiyama': B('snow', 'ice', 'ice', 0,
                  ('#222a46', '#2d3555', '#384264', '#47537a'), ('#28304e', '#3a4468', '#8a9cc8'),
                  ICE, ('#1c2c58', '#34507e', '#5a86b4', '#a0d0ec'),
                  snow=('#3a4468', '#5c6a94', '#8a9cc8')),
    'ryugu': B('coral', 'coral', 'water', 20,
               ('#0f1e2a', '#172a36', '#1f3842', '#2a4a4e'), ('#200a1e', '#3a1026', '#c89a30'),
               RED, ('#3a1230', '#74243a', '#a8403e', '#d06c50'),
               shell=('#5a3848', '#8a5a5e', '#b88a7a')),
    'uminobe': B('sand', 'planks', 'water', 50,
                 ('#1a1824', '#27242c', '#322e34', '#3e383a'), ('#100e18', '#1e1a24', '#5a5058'),
                 ('#18141e', '#2c252e', '#443a3e', '#5c5048'), ('#18141e', '#342a30', '#50443e', '#6e6050'),
                 shell=('#3a3440', '#5a5258', '#7a7068')),
    'yomi': B('stone', 'bone', 'void', 60,
              ('#0e0c16', '#1a1724', '#231f2e', '#2c2838'), ('#0a0812', '#15121e', '#5a4a52'),
              BONE, BONE),
    'jigoku': B('lava', 'rock', 'lava', 30,
                ('#120c12', '#1d151b', '#281d23', '#33242a'), ('#0e080e', '#1c1016', '#6a2a2a'),
                ('#180c14', '#2c141a', '#44201e', '#603226'), ('#180c14', '#30181c', '#4c2620', '#6c3c28')),
    'takamagahara': B('cloud', 'cloud', 'cloud', 0,
                      ('#242646', '#303358', '#3c4068', '#50507a'), ('#2a2c50', '#3a3c64', '#c89a30'),
                      ('#34365e', '#4c4f80', '#6c70a2', '#9498c4'), ('#30325a', '#50548a', '#787cae', '#a8acd0')),
    'kawabe': B('grass', 'rock', 'water', 10,
                ('#0f1c24', '#16282c', '#1c3632', '#28483a'), ('#0c141a', '#142428', '#3e6a50'),
                ('#141c26', '#22303a', '#34484c', '#4c6460'), ('#141c26', '#283840', '#3e5454', '#5c7468'),
                leaf=('#2a5a44', '#5a8a50')),
    'yashiki': B('wood', 'wood', 'void', 80,
                 ('#110d16', '#20171f', '#2a1f25', '#35282b'), ('#0c0a12', '#18121c', '#5a4034'),
                 WOOD, ('#1a121c', '#38242a', '#56342c', '#744a32')),
    'oeyama': B('gravel', 'rock', 'void', 20,
                ('#191117', '#261b21', '#322429', '#402e30'), ('#120a10', '#20141a', '#6e4a3c'),
                ('#1e121c', '#342026', '#4c2e2c', '#684234'), ('#1e121c', '#3a242a', '#56362e', '#765038')),
    'shinkai': B('sand', 'coral', 'water', 90,
                 ('#0b1120', '#11192c', '#18243c', '#20314e'), ('#080c18', '#0f1626', '#2a6a78'),
                 ('#0c1222', '#162034', '#22304a', '#324660'), ('#0e1426', '#1c2a44', '#2c405e', '#44607c'),
                 shell=('#1a2a48', '#2a4460', '#3e6278')),
    'enma_cho': B('stone', 'stone', 'lava', 40,
                  ('#11090f', '#20131a', '#2a1920', '#362027'), ('#0e080e', '#1e0e16', '#96661c'),
                  ('#1a0a14', '#30121c', '#4a1c22', '#682c28'), ('#1a0a14', '#36161e', '#562424', '#783a2c')),
    'tsukiyomi': B('cloud', 'cloud', 'cloud', 50,
                   ('#1f2338', '#2a2e46', '#353b55', '#464e6c'), ('#22263e', '#30354e', '#9aa6c8'),
                   SILVER, ('#262c48', '#465070', '#7682a4', '#b0bcd4')),
    'yomi_oku': B('stone', 'stone', 'void', 80,
                  ('#100a14', '#1c1220', '#26182a', '#322036'), ('#0c0610', '#180c1c', '#6a3a64'),
                  VIOLET, ('#160c1c', '#2c1a30', '#463048', '#64506a')),
}
