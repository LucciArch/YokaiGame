"""Eigene Effekte der Items („Signaturen“).

Jedes Item kann neben seinen Werten eine Signatur tragen: einen Schlüssel ``sig_<name>`` in seinen fx.
So fühlt sich jedes Item anders an, statt dass viele denselben Flag (z. B. homing) teilen.
Die Spiel-Logik ruft an festen Stellen die Haken unten auf; ohne passende Signatur kosten sie nichts.
"""
import math
import random

# Name → (Kurztext für Tooltip/Banner)
TEXT = {
    'spiegel': 'Jedes 3. Geschoss, das dich trifft, wird zurückgeworfen',
    'ewigkeit': 'Alle 5 gesäuberten Räume: +½ Herz',
    'sichel': 'Talismane fliegen in Mondsichel-Bögen',
    'rueckenwind': 'Im Laufen: schnellere, stärkere Talismane',
    'treffsicher': 'Jeder Treffer: +2 % Volltreffer-Chance (bis 20 %, weg bei Schaden)',
    'vergaenglich': 'In den ersten 10 s jedes Raums bis +40 % Schaden',
    'daemonenbrecher': '+50 % Schaden gegen Bosse und Champions',
    'bannkreis': 'Ein heiliger Kreis hält kleine Yokai auf Abstand',
    'klingen': 'Jeder 8. Wurf läutet: Feinde in der Nähe erstarren kurz',
    'fuchsglueck': 'Münzen sind manchmal fünf wert',
    'neun': 'Jeder 9. Wurf: ein Fächer aus neun Talismanen',
    'sternkugel': 'Eine Sternkugel schießt kleine Sterne auf Feinde',
    'opfergabe': 'Gesäuberte Räume lassen manchmal einen Schlüssel fallen',
    'statik': 'Laufen lädt auf – der nächste Wurf ruft einen Blitz',
    'donnerbiest': 'Drei Treffer auf denselben Feind rufen einen Blitz',
    'windstoss': 'Talismane wehen feindliche Geschosse weg',
    'hochmut': 'Mehr Schaden auf große Entfernung (bis +50 %)',
    'schnitt': 'Treffer schneiden: Feinde bluten (stapelt bis 3)',
    'pentagramm': 'Jeder 5. Treffer auf einen Feind: Siegel-Explosion',
    'buendel': 'Jeder 4. Wurf: drei kleine Talismane zusätzlich',
    'kuji': 'Treffer bannen Feinde manchmal (Starre)',
    'kraniche': 'Jeder Raum faltet einen Kranich – zehn retten dich vor dem Tod',
    'kranichflug': 'Ein Papierkranich greift regelmäßig an',
    'rache': 'Wer dich trifft, ist verflucht: doppelter Schaden',
    'zwischenwelt': 'Nach einem Treffer länger unverwundbar',
    'irrlicht': 'Besiegte Feinde werden zu Irrlichtern, die weiterbrennen',
    'knochenbruch': 'Feinde unter 15 % Leben zerbrechen sofort',
    'rausch': 'Talismane torkeln, treffen aber härter (+30 %)',
    'tigerfell': 'Der erste Treffer in jedem Raum: dreifacher Schaden',
    'ewige_flamme': 'Feuer erlischt nie und springt beim Tod über',
    'kammzinken': 'Talismane teilen sich im Flug wie Kammzinken',
    'schuppenpanzer': '25 % Chance, ein Geschoss abzuwehren',
    'kappa_freund': 'Kappa greifen dich nicht mehr an',
    'anmut': 'Raum ohne Treffer gesäubert: +0,15 Feuerrate (Ebene)',
    'starrt': 'Feinde in deiner Blickrichtung werden langsamer',
    'seidenfaden': 'Talismane ziehen einen schneidenden Faden',
    'stromauf': 'Talismane werden im Flug schneller und stärker',
    'tanuki_bauch': 'Alle 25 Mon: +½ Herz',
    'tarnung': 'Nach der Rolle sehen dich Feinde kurz nicht',
    'kenko': 'Einmal pro Ebene: bei ½ Herz heilst du ein Herz',
    'kinun': 'Truhen geben mehr her',
    'gokaku': 'Raum in unter 10 s gesäubert: +10 % Schaden (Ebene, bis 5×)',
    'proviant': 'Die nächsten drei Räume heilen je ½ Herz',
    'satt': 'Bei vollen Herzen +20 % Schaden',
    'klebrig': 'Wer dich berührt, bleibt kurz kleben',
    'drei_baellchen': 'Jeder 3. Wurf: drei Talismane',
    'wach': 'Dauerfeuer steigert die Feuerrate (bis +60 %)',
    'nasebrennt': 'Nach einer Pause: doppelt starker Wurf',
    'wurfstern': 'Talismane prallen zu einem zweiten Feind ab',
    'ehre': 'Ohne Treffer auf dieser Ebene: +25 % Schaden',
    'lange_reise': '+5 % Schaden pro Ebene',
    'klingeling': 'Geschosse in deiner Nähe werden langsamer',
    'aufstehen': 'Nach einem Treffer: Rückstoß-Welle und längere Schonzeit',
    'parade': 'Jeder Kill: +3 % Schaden im Raum (bis +45 %)',
    'maskenwechsel': 'Raum für Raum wechselnd: +35 % Schaden oder Feuerrate',
    'a_gyo': 'Beim Betreten brüllt der Wächter Feinde zurück',
    'sternschnuppe': 'Gesäuberte Räume: manchmal fällt ein Geschenk vom Himmel',
    'springfeuer': 'Treffer entzünden manchmal den Boden',
    'goldfaecher': 'Im Stehen +25 % Schaden',
    'spinnennetz': 'Treffer spinnen Netze, die Feinde bremsen',
    'giftspur': 'Gift spritzt auf benachbarte Feinde',
    'schlangenschweif': 'Ein Schlangenkopf beißt Feinde hinter dir',
    'reinigung': 'Reinigungssalz heilt auch ½ Herz',
    'iaido': 'Der erste Treffer nach einer Rolle ist kritisch',
    'neujahr': 'Jede neue Ebene heilt ein Herz',
    'ema': 'Jeder Boss erfüllt einen Wunsch (zufälliger Wert)',
    'falkenblick': 'Würfe lenken sich auf das nächste Ziel in Blickrichtung',
    'verzaubern': 'Treffer verwirren Feinde manchmal',
    'oni_koenig': 'Wer dich berührt, nimmt schweren Schaden',
    'boeser_stern': 'Jeder 3. Wurf ruft einen Sternenfall herab',
    'oel': 'Treffer tränken in Öl: langsamer, Feuer und Explosionen ×1,6',
    'hundert_augen': 'Getroffene Feinde sind markiert: +15 % Schaden',
    'flatter': 'Die Rolle wirft vier Federn',
    'rauch': 'Die Rolle hinterlässt Rauch, der Geschosse schluckt',
    'lachen': 'Kills jagen nahe Feinde in die Flucht',
    'panzer': 'Im Stehen zieht man sich ins Haus zurück: 50 % Abwehr',
    'drei_wiesel': 'Treffer: stolpern, schneiden – und manchmal heilen',
    'tinte': 'Treffer blenden Feinde, sie schießen daneben',
    'johari': 'Wer dich trifft, büßt mit achtfachem Schaden',
    'kichern': 'Feinde in der Nähe erschrecken manchmal',
    'augenhand': 'Das Handauge schießt auf Feinde in deiner Nähe',
    'zweischwanz': 'Manche Würfe kommen doppelt',
    'gross': 'Talismane wachsen im Flug',
    'reichtum': 'Ab 50 Mon: +15 % Feuerrate',
    'schlagfolge': 'Treffer in Folge auf dasselbe Ziel: bis +48 % Schaden',
    'sonnenkraehe': 'Die dreibeinige Krähe stößt auf Feinde herab',
    'schweiss': 'Nach einer Rolle: der nächste Wurf +40 %',
    'schweben': 'Talismane bleiben am Ende ihrer Bahn schweben',
    'windsack': 'Alle 4 s öffnet sich der Windsack: ein Sturm in Wurfrichtung fegt Geschosse fort und schneidet Feinde',
    'hara_tsuzumi': 'Bauchtrommel: die Rolle schlägt eine Schockwelle, die Tarnung hält doppelt so lang',
    'gelaechter': 'Das Lachen hallt weit: Kills verscheuchen Feinde im doppelten Umkreis, Verängstigte nehmen +30 % Schaden',
    'enenra': 'Der Rauch glimmt: Feinde im Rauch brennen, explodierende Feinde hinterlassen Rauch',
    'gashadokuro': 'Feinde unter 25 % Leben zerbrechen in vier Knochensplitter, die weiterfliegen',
    'tsukumogami': 'Die Rolle wirft Geschosse als zielsuchende Papierpuppen zurück, +1 Papierschild',
    'shinsen': 'Gesäuberte Räume geben dreimal so oft Schlüssel, Reinigungssalz heilt ein ganzes Herz',
    'nanakorobi': 'Schlagfolge bis +80 %, Erfolg zählt Räume unter 15 s und stapelt bis 8×',
    'jinmenju': 'Jeder Boss erfüllt zwei Wünsche und heilt dich ganz',
    'mokumokuren': 'Talismane wachsen weiter; sind sie groß, öffnet sich ein Auge: sie suchen ihr Ziel und treffen 40 % stärker',
    'fujin_raijin': 'Der Windsack öffnet sich alle 1,5 Sekunden, und Raijin schlägt in jeden getroffenen Feind ein',
    'erstes_feuer': 'Brennende Feinde explodieren beim Tod',
    'fuchsregen': 'Ein Sonnenregen fällt auf deine Feinde',
    'hausglueck': 'Der erste Krug in jedem Raum gibt immer etwas her',
    'felsblock': 'Unbeweglich: nichts bremst dich, Feinde prallen ab',
    'wandbruch': 'Bricht der Schild, stößt er alle Feinde weg',
    'glockenschlag': 'Wirst du getroffen, erstarren alle Feinde',
    'momo': 'Wirst du getroffen, wirfst du drei Pfirsiche (300 %), nahe Feinde fliehen 3 s',
    # ---- Synergie-Fähigkeiten (verstärken die Fähigkeiten der beteiligten Items)
    'sonnenregen': 'Der Fuchsregen fällt öfter und lässt Münzen fallen',
    'sternenstaub': 'Schwebende Talismane zerstieben in vier Sternsplitter',
    'jingi': 'Alle 5 s richten die Insignien die drei stärksten Feinde',
    'gewittersturm': 'Weggewehte Geschosse rufen manchmal einen Blitz',
    'neun_flammen': 'Der Neunerfächer besteht aus suchendem Fuchsfeuer',
    'kranichschwarm': 'Zwei Kraniche fliegen, für je drei gefaltete einer mehr',
    'himmelsbote': 'Im Laufen stößt die Krähe doppelt so oft herab',
    'kyudo': 'Weit geflogene Talismane treffen 60 % stärker',
    'tengu_sturm': 'Jeder 6. Wurf entfesselt einen Sturmring um dich',
    'allsehend': 'Markierte Feinde nehmen +30 % Schaden, der Blick lenkt weiter',
    'augen_ueberall': 'Das Handauge trifft markierte Feinde auf jede Entfernung',
    'mondteich': 'Mondsichel-Talismane lassen Feinde erstarren und treffen Gebremste 40 % stärker',
    'leben_tod': 'Kills schenken manchmal ½ Geisterherz',
    'suzu': 'Nach der Rolle läuten die Glöckchen (alle 4 s): feindliche Geschosse in der Nähe verlöschen, nahe Feinde fliehen lachend 2 s',
    'iwato': 'Verlöschte Geschosse kehren als Sonnenstrahlen (120 %) zu den Feinden zurück, die Glöckchen läuten schon nach 2,5 s',
    'izanagis_flucht': 'Auch die Rolle wirft Pfirsiche (150 %, alle 3 s), Feinde fliehen doppelt so weit und lang',
    'onmyo_spiegel': 'Der Spiegel wirft jedes 2. Geschoss als Siegel-Explosion zurück',
    'seimei': 'Siegel-Explosion schon nach 3 Treffern, Bann öfter',
    'koi_drache': 'Beschleunigte Talismane werden zu durchbohrenden Drachen',
    'drachenkoenig': 'Der Seidenfaden schneidet fast doppelt so tief',
    'verfluchte_sterne': 'Sternenfall verwirrt getroffene Feinde',
    'katzenreich': 'Doppelte Würfe kommen jedes zweite Mal',
    'ninja': 'Wurfsterne prallen bis zu dreimal ab',
    'ninja_flug': 'Im Laufen fliegt jeder 3. Wurf auch nach hinten',
    'tintenpanzer': 'Im Schneckenhaus blendet Tinte Feinde in der Nähe',
    'tiefsee_blick': 'Der starre Blick verletzt Feinde',
    'brandung': 'Talismane teilen sich beim Abprallen',
    'a_un': 'Wirst du getroffen, brüllt der Wächter alle zurück',
    'sonne_mond': 'Würfe wechseln: Sonne (Feuer) und Mond (Frost)',
    'taifun': 'Talismane wehen Geschosse in weitem Umkreis weg und schicken sie als Windklinge zurück',
    'fuchsstern': 'Die Sternkugel schießt drei Sterne',
    'giftnetz': 'Spinnennetze vergiften',
    'papiersturm': 'Jeder 2. Wurf bringt drei Talismane mehr',
    'mondschnitt': 'Mondsichel-Talismane schneiden tief: Bluten stapelt bis 6, dann reißt der nächste Bogen alles auf (300 %)',
    'rattenschwarm': 'Durchbohrende Talismane lassen Ratten auf Feinde los',
    'sonnenspiegel': 'Der Spiegel wirft Geschosse als drei Sonnenstrahlen zurück',
    'goetter_arsenal': 'Jeder Speerstoß schießt auch einen Pfeil Hachimans; Treffsicher wächst doppelt so schnell, bis 35 %',
    'geisterlicht': 'Zwei Irrlichter pro Kill, sie fliegen durch Wände',
    'faehrmann': 'Jeder 12. Kill: der Fährmann zahlt ½ Geisterherz',
    'ewiger_winter': 'Erstarrte Feinde nehmen +50 % Schaden, Gebremste erstarren öfter',
    'tengu_flug': 'Die Rolle entfesselt einen schneidenden Windwirbel',
    'oni_rausch': 'Torkelnde Talismane treffen +45 % statt +30 %',
    'oni_krieger': 'Tigerhieb: die ersten drei Treffer jedes Raums und der erste Treffer auf jeden unverletzten Feind',
    'gluecksgoetter': 'Goldene Treffer lassen manchmal Mon fallen',
    'onmyodo': 'Siegel-Explosionen entlassen drei Papierdiener',
    'hanami': 'Die Blüte hält länger: 15 s lang bis +60 % Schaden',
    'teezeremonie': 'Im Stehen +50 % Schaden, die Wachheit bleibt',
    'sushi': 'Doppelt starke Würfe vergiften und explodieren',
    'omamori_set': 'Kenkō rettet zweimal pro Ebene, Truhen geben doppelt mehr',
    'tempelmusik': 'Jeder vierte Schlag hallt als Klangwelle um dich',
    'bushi': 'Ehre wiegt schwerer: +45 % statt +25 %',
    'feuerwerk': 'Explodierende Talismane zerplatzen in fünf brennende Funken',
    'oelfeuer': 'Geölte Feinde gehen beim Tod in einer Feuerexplosion auf',
    'feuerkind': 'Die Rolle schleudert brennendes Öl auf Feinde in der Nähe',
    'feuerwagen': 'Die Rolle lässt zwei Feuerräder in Rollrichtung losrollen',
    'gericht': 'Zurückgeworfene Geschosse verfluchen: doppelter Schaden',
    'sturmfaecher': 'Jeder dritte Schlag ruft einen Blitz; Blitze entfesseln Böen, die Feinde wegschleudern',
    'sturmgott': 'Statik lädt doppelt so schnell, ihr Blitz springt auf drei Feinde',
    'blitzschlag': 'Das Donnerbiest erwacht schon nach 2 Treffern und springt weiter',
    'orochi': 'Das Grasmäher-Schwert trifft Vergiftete 20 % härter',
    'hannya_zorn': 'Wirst du getroffen, lodert die Hannya: 6 s lang +50 % Schaden und Feuer',
    'oni_tanz': 'Jeder große Schlag schleudert einen Ring aus acht Talismanen',
    'oeyama_bande': 'Wer dich berührt, nimmt doppelten Oni-König-Schaden und taumelt',
    'maskenzug': 'Die Parade zieht weiter: Kills stapeln über die ganze Ebene, bis +60 %',
    'unterweltgift': 'Der Schlangenkopf verflucht seine Opfer: doppelter Schaden',
    'wirbelklingen': 'Blutende Feinde zerfallen beim Tod in drei Windsicheln',
    'strassenkatze': 'Der Iai-Hieb nach der Rolle trifft dreifach',
    'yamabushi': 'Der Stab läutet jeden 4. Wurf und stößt Feinde weg',
    'tempelfest': 'Große Schläge lassen die Glocke dröhnen: 3 s doppelte Aura',
    'schreinwaechter': 'Der Bannkreis wird doppelt so groß, der Wächter brüllt alle 8 s',
    'unbeweglich': 'Die Wand baut sich 8 s nach dem Bruch wieder auf',
    'drachenschuppen': '35 % Abwehr, abgewehrte Geschosse kehren als Drachenperle zurück',
    'daruma_geist': 'Die Welle nach einem Treffer sprengt acht goldene Splitter ab',
    'yomotsu': 'Abgeprallte Feinde sind versiegelt: starr und verflucht',
    'riesenmoench': 'Die Gebetsperlen kreisen weiter und treffen doppelt',
    'totenfaehre': 'Nach 40 Kills liegt wieder eine Münze für den Fährmann bereit',
    'hyakki_herr': 'Dein Gefolge wirft doppelt so oft und zielt selbst',
    'gluecksheim': 'Die ersten zwei Krüge jedes Raums geben immer etwas her',
    'winkekatze': 'Das Glöckchen bremst Geschosse im doppelten Umkreis',
    'fuchsgeld': 'Münzen sind doppelt so oft fünf wert',
    'wunsch': 'Nach gesäuberten Räumen fallen dreimal so oft Sternschnuppen',
    'tennyo': 'Jeder Kill lässt die Blüte 2 s länger blühen',
    'kappa_fest': 'Abprallende Talismane spritzen Wasser und bremsen Feinde, danach treffen sie 50 % stärker',
    'hanami_picknick': 'Bei vollen Herzen +40 % statt +20 %',
    'shogatsu': 'Klebende Feinde sind verflucht: doppelter Schaden',
    'pilger': '+10 % Schaden pro Ebene statt +5 %',
    'sommerwind': 'Die Rolle wirft acht Federn, die weiter fliegen',
    'fest_der_laternen': 'Treffer entzünden doppelt so oft den Boden, die Flammen brennen länger',
    'kaufmann': 'Der Hammer zählt jede Münze doppelt, Reichtum schon ab 25 Mon (+25 %)',
}

BULLET_SIGS = ('sichel', 'kammzinken', 'seidenfaden', 'stromauf', 'gross', 'schweben', 'windstoss', 'koi_drache')


def has(p, name):
    return p.f.get('sig_' + name, 0) > 0


def active(p):
    return {k[4:] for k, v in p.f.items() if k.startswith('sig_') and v > 0}


def st(p):
    if not hasattr(p, 'sg') or p.sg is None:
        p.sg = {}
    return p.sg


def _nearest(run, x, y, maxd=9999, cond=None):
    best, bd = None, maxd
    for e in run.enemies:
        if e.active() and (cond is None or cond(e)):
            d = math.hypot(e.x - x, e.y - y)
            if d < bd:
                best, bd = e, d
    return best


def _ring(run, x, y, col, r=40):
    from .entities import Particle
    run.particles.append(Particle(x, y, 0, 0, 0.3, col, r, kind='ring'))


def _chain_strikes(run, src, n, dmg):
    """Blitz springt von src auf bis zu n weitere nahe Feinde."""
    done = {id(src)}
    for _ in range(n):
        nxt = _nearest(run, src.x, src.y, 110, lambda o: id(o) not in done)
        if not nxt:
            return
        done.add(id(nxt))
        run.zap(src.x, src.y, nxt.x, nxt.y)
        run.lightning(nxt.x, nxt.y, dmg)
        src = nxt


def _float(run, e, txt, col):
    run.floats.append([e.x, e.y - 16, txt, col, 0.6])


_SYN_NAME = {}


def _syn(run, key, x, y, col):
    """Erstes Auslösen einer Synergie im Raum: Name als Schriftzug und farbige Welle."""
    g = st(run.player)
    seen = g.setdefault('syn_seen', [])   # Liste statt Menge: p.sg wird als JSON gespeichert
    if key in seen:
        return
    seen.append(key)
    if not _SYN_NAME:
        from .data import SYNERGIES
        _SYN_NAME.update({k[4:]: s['name'] for s in SYNERGIES for k in s['fx'] if k.startswith('sig_')})
    from .entities import Particle
    run.floats.append([x, y - 22, _SYN_NAME.get(key, key) + '!', col, 1.1])
    run.particles.append(Particle(x, y, 0, 0, 0.45, col, 38, kind='wave'))


def _sparks(run, x, y, cols, n=10, spd=110):
    from .entities import Particle
    for _ in range(n):
        a = random.uniform(0, math.tau)
        v = random.uniform(0.5, 1) * spd
        run.particles.append(Particle(x, y, math.cos(a) * v, math.sin(a) * v, random.uniform(0.25, 0.5),
                                      random.choice(cols), 2, 60, kind='spark'))


# ====================================================================== Haken
def on_fire(p, run, bullets):
    S = p.sgs
    if not S:
        return
    g = st(p)
    g['shots'] = g.get('shots', 0) + 1
    n = g['shots']
    base = math.atan2(p.facing[1], p.facing[0])
    dmg = p.damage()
    spd = p.s['shotspd']
    life = p.s['range'] / spd
    size = p.s['size']
    tags = tuple(s for s in BULLET_SIGS if s in S)
    for b in bullets:
        if tags:
            b.fl = dict(b.fl); b.fl['sg'] = tags
    if 'sichel' in S:
        g['sichel'] = -g.get('sichel', 1)
        tgt = run.nearest_enemy(p.x, p.y)
        for b in bullets:
            b.curve = 1.7 * g['sichel']
            # schräg ansetzen, damit der Bogen die Ziellinie beim nächsten Feind wieder kreuzt
            th = b.curve * min(b.life, math.hypot(tgt.x - p.x, tgt.y - p.y) / max(1, math.hypot(b.vx, b.vy)) if tgt else b.life) / 2
            c, s_ = math.cos(-th), math.sin(-th)
            b.vx, b.vy = b.vx * c - b.vy * s_, b.vx * s_ + b.vy * c
            if 'mondteich' in S:
                _syn(run, 'mondteich', p.x, p.y, (170, 230, 255))
                b.fl = dict(b.fl); b.fl['slow'] = 1; b.fl['_frost'] = 1
    if 'goetter_arsenal' in S:
        from . import weapons
        if weapons.weapon_of(p) == 'w_spear':   # Hachimans Bogen geht sonst im Speer unter
            fl = dict(weapons.shot_flags(p), pierce=1)
            a = run.fire_player_bullet(p.x, p.y - 4, base, dmg * 1.6, spd * 1.7, max(2, size * 0.8), life * 1.4 / 1.7, fl)
            a.arrow = True
            _syn(run, 'goetter_arsenal', p.x, p.y, (255, 220, 150))
    if 'sturmfaecher' in S and n % 3 == 0:
        tgt = run.nearest_enemy(p.x, p.y, 130)
        if tgt:
            run.lightning(tgt.x, tgt.y, dmg * 1.5 + 3)
    if 'sonne_mond' in S:
        sun = n % 2 == 0
        for b in bullets:
            b.fl = dict(b.fl); b.fl['burn' if sun else '_frost'] = 1
            b.col = (255, 190, 90) if sun else (180, 220, 255)
        _syn(run, 'sonne_mond', p.x, p.y, (255, 210, 140))
    if 'rueckenwind' in S and p.moving:
        for b in bullets:
            b.vx *= 1.3; b.vy *= 1.3; b.dmg *= 1.15
    if 'rausch' in S:
        for b in bullets:
            a = math.atan2(b.vy, b.vx) + random.uniform(-0.28, 0.28)
            sp = math.hypot(b.vx, b.vy)
            b.vx, b.vy = math.cos(a) * sp, math.sin(a) * sp
            b.dmg *= 1.45 if 'oni_rausch' in S else 1.3
            if 'oni_rausch' in S:
                b.col = (255, 150, 130)
        if 'oni_rausch' in S:
            _syn(run, 'oni_rausch', p.x, p.y, (255, 110, 90))
    if g.get('hannya', 0) > 0:
        for b in bullets:
            b.fl = dict(b.fl); b.fl['burn'] = 1
    if 'goldfaecher' in S and not p.moving:
        for b in bullets:
            b.dmg *= 1.5 if 'teezeremonie' in S else 1.25
        if 'teezeremonie' in S:
            _syn(run, 'teezeremonie', p.x, p.y, (170, 210, 140))
    if 'nasebrennt' in S:
        if run.time - g.get('last_fire', -9) > 1.0:
            for b in bullets:
                b.dmg *= 2; b.col = (170, 255, 120)
                if 'sushi' in S:
                    b.fl = dict(b.fl); b.fl['poison'] = 1; b.fl['explode'] = 1
                    _syn(run, 'sushi', p.x, p.y, (170, 255, 120))
    if 'schweiss' in S and g.get('schweiss', 0) > 0:
        g['schweiss'] = 0
        for b in bullets:
            b.dmg *= 1.4
    if 'falkenblick' in S:
        for b in bullets:
            a = math.atan2(b.vy, b.vx)
            best, bd = None, (0.9 if 'allsehend' in S else 0.45)
            for e in run.enemies:
                if e.active():
                    w = math.atan2(e.y - b.y, e.x - b.x)
                    d = abs((w - a + math.pi) % math.tau - math.pi)
                    if d < bd:
                        best, bd = w, d
            if best is not None:
                sp = math.hypot(b.vx, b.vy)
                b.vx, b.vy = math.cos(best) * sp, math.sin(best) * sp
    if 'wach' in S:
        if run.time - g.get('last_fire', -9) < 0.7:
            g['wach'] = min(0.6, g.get('wach', 0) + 0.04)
        elif 'teezeremonie' in S and not p.moving:
            pass
        else:
            g['wach'] = 0
    g['last_fire'] = run.time
    extra = []
    xfl = {'homing': 1, 'burn': 1} if 'neun_flammen' in S else {}
    if 'neun' in S and n % 9 == 0:
        extra += [(base + (i - 4) * 0.13, 0.7, 1.0) for i in range(9)]
        if xfl:
            _syn(run, 'neun_flammen', p.x, p.y, (120, 200, 255))
    if 'buendel' in S and n % (2 if 'papiersturm' in S else 4) == 0:
        extra += [(base + random.uniform(-0.35, 0.35), 0.5, 0.7) for _ in range(3)]
        if 'papiersturm' in S:
            _syn(run, 'papiersturm', p.x, p.y, (240, 235, 210))
    if 'drei_baellchen' in S and n % 3 == 0:
        extra += [(base - 0.12, 0.8, 0.9), (base + 0.12, 0.8, 0.9)]
    if 'ninja_flug' in S and p.moving and n % 3 == 0:
        extra.append((base + math.pi, 0.8, 1.0))
        _syn(run, 'ninja_flug', p.x, p.y, (150, 150, 190))
    for a, dm, sz in extra:
        run.fire_player_bullet(p.x, p.y - 3, a, dmg * dm, spd, size * sz, life, dict(xfl))
    if any(b.big for b in bullets):
        if 'tempelfest' in S:
            g['glocke'] = 3.0
        if 'oni_tanz' in S:
            _syn(run, 'oni_tanz', p.x, p.y, (255, 140, 100))
            for i in range(8):
                run.fire_player_bullet(p.x, p.y - 3, i / 8 * math.tau, dmg * 0.9, spd, size, 0.8, {'pierce': 1})
    if 'tempelmusik' in S and any(b.big for b in bullets):
        _syn(run, 'tempelmusik', p.x, p.y, (230, 200, 140))
        _ring(run, p.x, p.y, (230, 200, 140), 60)
        for e in run.enemies:
            if e.active() and math.hypot(e.x - p.x, e.y - p.y) < 60 + e.r:
                run.damage_enemy(e, dmg * 0.8, None)
    if 'tengu_sturm' in S and n % 6 == 0:
        _syn(run, 'tengu_sturm', p.x, p.y, (220, 240, 255))
        _ring(run, p.x, p.y, (220, 240, 255), 70)
        for eb in run.ebullets:
            if (eb.x - p.x) ** 2 + (eb.y - p.y) ** 2 < 70 ** 2:
                eb.dead = True
        for e in run.enemies:
            d = math.hypot(e.x - p.x, e.y - p.y)
            if e.active() and d < 80 and not e.is_boss:
                e.kx += (e.x - p.x) / max(d, 1) * 400; e.ky += (e.y - p.y) / max(d, 1) * 400
    if 'zweischwanz' in S and random.random() < (0.5 if 'katzenreich' in S else 0.25):
        run.fire_player_bullet(p.x, p.y - 3, base, dmg * 0.8, spd, size, life, {}, delay=0.08)
        if 'katzenreich' in S:
            _syn(run, 'katzenreich', p.x, p.y, (200, 160, 230))
    if 'statik' in S and g.get('statik', 0) >= 3.0:
        g['statik'] = 0
        tgt = run.nearest_enemy(p.x, p.y, 400)
        if tgt:
            run.lightning(tgt.x, tgt.y, dmg * 2 + 4)
            if 'sturmgott' in S:
                _syn(run, 'sturmgott', tgt.x, tgt.y, (200, 220, 255))
                _chain_strikes(run, tgt, 3, dmg * 1.5 + 3)
    if 'klingen' in S and n % (4 if 'yamabushi' in S else 8) == 0:
        from . import audio
        audio.play('bell', 0.4)
        _ring(run, p.x, p.y, (255, 230, 150), 60)
        for e in run.enemies:
            if e.active() and math.hypot(e.x - p.x, e.y - p.y) < 64:
                e.frozen = max(e.frozen, 0.25 if e.is_boss else 0.7)
                if 'yamabushi' in S and not e.is_boss:
                    _syn(run, 'yamabushi', p.x, p.y, (255, 230, 150))
                    d = math.hypot(e.x - p.x, e.y - p.y) or 1
                    e.kx += (e.x - p.x) / d * 320; e.ky += (e.y - p.y) / d * 320
    if 'boeser_stern' in S and n % 3 == 0:
        from .entities import Hazard
        tx, ty = p.x + math.cos(base) * 90, p.y + math.sin(base) * 90
        tgt = _nearest(run, tx, ty, 80)
        if tgt:
            tx, ty = tgt.x, tgt.y
        h = Hazard(tx, ty, 16, 0.45, 0.12, dmg * 2.2, 'p', 'meteor')
        h.sg_conf = 'verfluchte_sterne' in S
        run.hazards.append(h)
    if 'windsack' in S and run.time - g.get('windsack', -9) >= (1.5 if 'fujin_raijin' in S else 4.0):
        g['windsack'] = run.time
        from .entities import Particle
        from . import audio
        audio.play('dash', 0.6)
        for i in range(14):                                   # sichtbare Windstreifen im Kegel
            a = base + random.uniform(-0.5, 0.5)
            v = random.uniform(160, 260)
            run.particles.append(Particle(p.x, p.y, math.cos(a) * v, math.sin(a) * v, 0.45, (200, 240, 225), 2))
        for eb in run.ebullets:
            dx, dy = eb.x - p.x, eb.y - p.y
            if dx * dx + dy * dy < 130 ** 2 and abs((math.atan2(dy, dx) - base + math.pi) % math.tau - math.pi) < 0.6:
                eb.dead = True
        for e in run.enemies:
            dx, dy = e.x - p.x, e.y - p.y
            d = math.hypot(dx, dy)
            if e.active() and d < 130 + e.r and abs((math.atan2(dy, dx) - base + math.pi) % math.tau - math.pi) < 0.6:
                run.damage_enemy(e, dmg * 1.5, None)
                if 'fujin_raijin' in S:
                    _syn(run, 'fujin_raijin', e.x, e.y, (200, 240, 160))
                    run.lightning(e.x, e.y, dmg * 2.5 + 4)
                if not e.is_boss:
                    e.kx += dx / max(d, 1) * 380; e.ky += dy / max(d, 1) * 380


def bullet_tick(b, run, dt):
    """Nur für Spieler-Talismane mit Bahn-Signatur. False = Talisman verschwindet."""
    tags = b.fl.get('sg')
    if not tags:
        return True
    if 'stromauf' in tags:
        f = 1 + 1.3 * dt
        b.vx *= f; b.vy *= f
        b.dmg *= 1 + 0.6 * dt
    if 'gross' in tags:
        moku = 'mokumokuren' in run.player.sgs
        b.r = min(b.r * (1 + 1.2 * dt), 16 if moku else 12)
        if moku and b.r > 4.5 and not b.fl.get('homing'):
            _syn(run, 'mokumokuren', b.x, b.y, (245, 240, 225))
            b.fl = dict(b.fl); b.fl['homing'] = 1
            b.dmg *= 1.4   # das Auge im Papier öffnet sich
    if 'kammzinken' in tags and b.t > 0.2 and not b.fl.get('_kz'):
        b.fl = dict(b.fl); b.fl['_kz'] = 1
        a = math.atan2(b.vy, b.vx)
        sp = math.hypot(b.vx, b.vy)
        for da in (-0.32, 0.32):
            run.fire_player_bullet(b.x, b.y, a + da, b.dmg * 0.6, sp, max(1.5, b.r * 0.7), b.life, {'_kz': 1})
    if 'schweben' in tags and not b.fl.get('_sw') and b.life < b.maxlife * 0.35:
        b.fl = dict(b.fl); b.fl['_sw'] = 1
        b.vx *= 0.06; b.vy *= 0.06
        b.curve = 0
        b.life += 1.4
    if 'seidenfaden' in tags:
        b.fl['_sf'] = b.fl.get('_sf', 0) + dt
        if b.fl['_sf'] > 0.07:
            b.fl['_sf'] = 0
            from .entities import Hazard
            k = 1.75 if 'drachenkoenig' in run.player.sgs else 1
            if k > 1:
                _syn(run, 'drachenkoenig', b.x, b.y, (140, 220, 200))
            run.hazards.append(Hazard(b.x, b.y, 4, 0.0, 0.5, max(0.5, b.dmg * 0.18 * k), 'p', 'silk'))
    if 'koi_drache' in tags and b.t > 0.35 and not b.fl.get('pierce'):
        _syn(run, 'koi_drache', b.x, b.y, (255, 150, 90))
        b.fl = dict(b.fl); b.fl['pierce'] = 1
        b.r *= 1.5; b.col = (255, 150, 90)
    if 'windstoss' in tags:
        S = run.player.sgs
        rr = (b.r + (14 if 'taifun' in S else 5)) ** 2
        for eb in run.ebullets:
            if not eb.dead and (eb.x - b.x) ** 2 + (eb.y - b.y) ** 2 < rr:
                eb.dead = True
                if 'taifun' in S:
                    _syn(run, 'taifun', b.x, b.y, (210, 240, 230))
                    tgt = None if b.fl.get('_tf') else run.nearest_enemy(eb.x, eb.y, 220)
                    if tgt:   # ein Gegenwind pro Geschoss, sonst zerlegt der Fächer jeden Kugelhagel in Windklingen
                        b.fl = dict(b.fl, _tf=1)
                        w = run.fire_player_bullet(eb.x, eb.y, math.atan2(tgt.y - eb.y, tgt.x - eb.x), run.player.damage() * 1.5, 230, 3, 1.2, {'pierce': 1, 'knock': 1})
                        w.wind = True; w.col = (210, 240, 230)
                if 'gewittersturm' in S and random.random() < 0.08:
                    tgt = run.nearest_enemy(b.x, b.y, 200)
                    if tgt:
                        run.lightning(tgt.x, tgt.y, run.player.damage() * 1.5 + 3)
                        _syn(run, 'gewittersturm', tgt.x, tgt.y, (200, 220, 255))
    return True


def bullet_end(run, b):
    """Ein Spieler-Talisman verschwindet (Treffer, Wand oder Reichweite)."""
    if b.fl.get('explode') and not b.fl.get('_split') and 'feuerwerk' in run.player.sgs:
        hanabi = ((255, 120, 160), (255, 220, 120), (140, 220, 255))
        _syn(run, 'feuerwerk', b.x, b.y, (255, 150, 190))
        _sparks(run, b.x, b.y, hanabi, 14, 130)
        seen = set()   # die fünf Funken teilen sich eine Trefferliste: jeder Feind höchstens einmal
        for i in range(5):
            nb = run.fire_player_bullet(b.x, b.y, i / 5 * math.tau + random.uniform(0, 1.2), b.dmg * 0.8, 170, 2, 0.4, {'burn': 1})
            nb.hit = seen
            nb.col = random.choice(((255, 120, 160), (255, 220, 120), (140, 220, 255)))
    if b.fl.get('_sw') and 'sternenstaub' in run.player.sgs:
        _syn(run, 'sternenstaub', b.x, b.y, (255, 240, 170))
        for i in range(4):
            a = i / 4 * math.tau + 0.4
            nb = run.fire_player_bullet(b.x, b.y, a, b.dmg * 0.5, 200, 2, 0.35, {})
            nb.col = (255, 240, 170)


def bullet_bounce(run, b):
    if 'kappa_fest' in run.player.sgs:
        _syn(run, 'kappa_fest', b.x, b.y, (120, 200, 240))
        _ring(run, b.x, b.y, (120, 200, 240), 26)
        for e in run.enemies:
            if e.active() and math.hypot(e.x - b.x, e.y - b.y) < 26 + e.r:
                e.slowed = max(e.slowed, 2.0)
        if not b.fl.get('_kf'):   # Tellerwasser: der abgeprallte Talisman trifft schwerer und bremst
            b.fl = dict(b.fl, _kf=1, slow=1)
            b.dmg *= 1.5; b.col = (120, 200, 240)
    if 'brandung' in run.player.sgs and not b.fl.get('_br'):
        _syn(run, 'brandung', b.x, b.y, (110, 190, 255))
        b.fl = dict(b.fl); b.fl['_br'] = 1
        a = math.atan2(b.vy, b.vx)
        for da in (-0.35, 0.35):
            run.fire_player_bullet(b.x, b.y, a + da, b.dmg * 0.6, math.hypot(b.vx, b.vy), max(1.5, b.r * 0.8), 0.5, {'_br': 1})


def hit_pre(run, e, b, dmg):
    p = run.player
    S = p.sgs
    if not S:
        return dmg
    g = st(p)
    if 'treffsicher' in S and random.random() < g.get('ts', 0):
        dmg *= 2
        _float(run, e, 'Kritisch!', (255, 220, 90))
    if 'iaido' in S and g.get('iaido', 0) > 0:
        g['iaido'] = 0
        dmg *= 3 if 'strassenkatze' in S else 2
        if 'strassenkatze' in S:
            _syn(run, 'strassenkatze', e.x, e.y, (230, 220, 200))
        _float(run, e, 'Iai!', (230, 230, 255))
    if 'daemonenbrecher' in S and (e.is_boss or e.champ):
        dmg *= 1.5
    if 'hochmut' in S:
        dmg *= 1 + min(0.5, math.hypot(e.x - p.x, e.y - p.y) / 300)
    fresh = 'oni_krieger' in S and not e.is_boss and e.hp >= e.maxhp   # Oni-Krieger: jeder unverletzte Feind
    if 'tigerfell' in S and (fresh or g.get('tiger', 0) < (3 if 'oni_krieger' in S else 1)):
        g['tiger'] = g.get('tiger', 0) + 1
        dmg *= 3
        _float(run, e, 'Tigerhieb!', (255, 190, 80))
        if g['tiger'] == 2:
            _syn(run, 'oni_krieger', p.x, p.y, (255, 170, 60))
    if getattr(e, 'sg_curse', 0) > 0:
        dmg *= 2
    if 'hundert_augen' in S and getattr(e, 'sg_mark', False):
        dmg *= 1.3 if 'allsehend' in S else 1.15
        if 'allsehend' in S:
            _syn(run, 'allsehend', e.x, e.y, (255, 120, 160))
    if 'ewiger_winter' in S and e.frozen > 0:
        dmg *= 1.5
    if 'mondteich' in S and b is not None and b.curve and (e.frozen > 0 or e.slowed > 0):
        dmg *= 1.4   # Mondlicht auf stillem Wasser
    if 'mondschnitt' in S and b is not None and b.curve and getattr(e, 'sg_bleed', 0) >= 6:
        e.sg_bleed = 0   # die tiefen Schnitte reißen auf einmal auf
        dmg *= 3
        _float(run, e, 'Mondschnitt!', (230, 90, 110))
    if 'gelaechter' in S and getattr(e, 'sg_fear', 0) > 0:
        dmg *= 1.3
    if 'orochi' in S and e.poison > 0:
        _syn(run, 'orochi', e.x, e.y, (150, 235, 110))
        dmg *= 1.2
    if 'kyudo' in S and b is not None and b.t > 0.45:
        dmg *= 1.6
        _syn(run, 'kyudo', e.x, e.y, (200, 230, 160))
    if getattr(e, 'sg_oil', 0) > 0 and (b is None or b.fl.get('burn') or b.fl.get('explode')):
        dmg *= 1.6
    if 'schlagfolge' in S:
        if g.get('last_tgt') == id(e):
            g['chain'] = min(10 if 'nanakorobi' in S else 6, g.get('chain', 0) + 1)
            if g['chain'] == 7:
                _syn(run, 'nanakorobi', e.x, e.y, (230, 90, 70))
        else:
            g['chain'] = 0
        g['last_tgt'] = id(e)
        dmg *= 1 + 0.08 * g['chain']
    return dmg


def hit_post(run, e, b, dmg):
    p = run.player
    S = p.sgs
    if not S:
        return
    g = st(p)
    echo = getattr(run, '_echo', False)   # Schaden von Bodenfeuer, Blitz oder Explosion
    if 'treffsicher' in S:
        hi = 'goetter_arsenal' in S
        g['ts'] = min(0.35 if hi else 0.2, g.get('ts', 0) + (0.04 if hi else 0.02))
        if hi and g['ts'] > 0.2:
            _syn(run, 'goetter_arsenal', e.x, e.y, (255, 220, 150))
    if 'hundert_augen' in S:
        e.sg_mark = True
    if 'gluecksgoetter' in S and b is not None and b.gold and random.random() < 0.15:
        run.spawn_pickup('coin', e.x, e.y)
        _syn(run, 'gluecksgoetter', e.x, e.y, (255, 220, 110))
    if 'donnerbiest' in S and not echo:
        e.sg_thunder = getattr(e, 'sg_thunder', 0) + 1
        if e.sg_thunder >= (2 if 'blitzschlag' in S else 3):
            e.sg_thunder = 0
            run.lightning(e.x, e.y, p.damage() * 1.6 + 3)
            if 'blitzschlag' in S:
                _syn(run, 'blitzschlag', e.x, e.y, (255, 240, 120))
                _chain_strikes(run, e, 1, p.damage() * 1.6 + 3)
    if b is not None and b.fl.get('_urteil'):
        e.sg_curse = 6.0
    if 'pentagramm' in S and not echo and not (b is not None and b.fl.get('_shiki')):   # Papierdiener laden das Siegel nicht nach
        e.sg_pent = getattr(e, 'sg_pent', 0) + 1
        if e.sg_pent >= (3 if 'seimei' in S else 5):
            e.sg_pent = 0
            _ring(run, e.x, e.y, (255, 230, 120), 34)
            run.explode(e.x, e.y, 28, p.damage() * 2.4, 'p')
            if 'seimei' in S:
                _syn(run, 'seimei', e.x, e.y, (255, 230, 120))
            if 'onmyodo' in S:
                _syn(run, 'onmyodo', e.x, e.y, (240, 240, 240))
                for i in range(3):
                    a = i / 3 * math.tau
                    ox, oy = math.cos(a) * (e.r + 8), math.sin(a) * (e.r + 8)   # außerhalb starten, damit man sie fliegen sieht
                    sb = run.fire_player_bullet(e.x + ox, e.y + oy, a, p.damage() * 0.7, 160, 2.5, 1.4, {'homing': 1, '_shiki': 1})
                    sb.col = (240, 240, 240)
                    sb.kind = 'shiki'
    if 'schnitt' in S or 'drei_wiesel' in S:
        deep = 'mondschnitt' in S and b is not None and b.curve
        if deep:
            _syn(run, 'mondschnitt', e.x, e.y, (220, 80, 90))
        e.sg_bleed = min(6 if deep else 3, getattr(e, 'sg_bleed', 0) + (2 if deep else 1))
        e.sg_bleed_t = 3.0
    if 'drei_wiesel' in S:
        if not e.is_boss:
            e.frozen = max(e.frozen, 0.25)
        if random.random() < 0.04 and p.heal(1):
            from . import audio
            audio.play('heal', 0.4)
    if 'ewiger_winter' in S and e.slowed > 0 and random.random() < 0.15:
        e.frozen = max(e.frozen, 0.3 if e.is_boss else 1.0)
        _syn(run, 'ewiger_winter', e.x, e.y, (180, 230, 255))
    if 'rattenschwarm' in S and b is not None and b.fl.get('pierce') and not b.fl.get('_rat') and random.random() < 0.3:
        _syn(run, 'rattenschwarm', e.x, e.y, (160, 170, 190))
        tgt = _nearest(run, e.x, e.y, 160, lambda o: o is not e)
        a = math.atan2(tgt.y - e.y, tgt.x - e.x) if tgt else random.uniform(0, math.tau)
        rb = run.fire_player_bullet(e.x, e.y, a, dmg * 0.5, 190, 2, 0.8, {'homing': 1, '_rat': 1})
        rb.col = (160, 170, 190)
        rb.kind = 'rat'
    if b is not None and b.fl.get('_frost') and random.random() < 0.2:
        e.frozen = max(e.frozen, 0.3 if e.is_boss else 1.2)
    if 'kuji' in S and random.random() < (1 / 5 if 'seimei' in S else 1 / 9):
        e.frozen = max(e.frozen, 0.4 if e.is_boss else 1.5)
        _float(run, e, 'Gebannt', (220, 200, 255))
    if 'knochenbruch' in S and not e.is_boss and 0 < e.hp < e.maxhp * (0.25 if 'gashadokuro' in S else 0.15):
        e.hp = 0
        _float(run, e, 'Zerbrochen!', (240, 230, 210))
        if 'gashadokuro' in S and not echo:
            _syn(run, 'gashadokuro', e.x, e.y, (240, 230, 210))
            a0 = random.uniform(0, math.tau)
            for i in range(4):
                nb = run.fire_player_bullet(e.x, e.y, a0 + i * math.tau / 4, p.damage() * 0.6, 220, 3, 0.6, {'pierce': 1})
                nb.col = (235, 228, 205)
                nb.kind = 'bone'
    if 'springfeuer' in S and not echo and random.random() < (0.4 if 'fest_der_laternen' in S else 0.2):
        from .entities import Hazard
        run.hazards.append(Hazard(e.x, e.y + 4, 10, 0.0, 3.5 if 'fest_der_laternen' in S else 2.0, max(0.6, p.damage() * 0.3), 'p', 'fire'))
        if 'fest_der_laternen' in S:
            _syn(run, 'fest_der_laternen', e.x, e.y, (255, 170, 90))
    if 'spinnennetz' in S and random.random() < 0.3:
        webs = g.setdefault('webs', [])
        if len(webs) < 6:
            webs.append([e.x, e.y, 4.0])
    if 'giftspur' in S:
        for o in run.enemies:
            if o is not e and o.active() and math.hypot(o.x - e.x, o.y - e.y) < 34:
                o.poison = max(o.poison, 3.0)
                o.poison_dps = max(o.poison_dps, max(1.0, dmg * 0.3))
    if 'oel' in S:
        e.sg_oil = 3.0
    if 'verzaubern' in S and not e.is_boss and random.random() < 0.08:
        e.sg_conf = 3.0
        _float(run, e, 'Verwirrt', (255, 170, 230))
    if 'tinte' in S:
        e.sg_blind = 3.0
    if 'wurfstern' in S and b is not None and b.fl.get('_ric', 0) < (3 if 'ninja' in S else 1):
        tgt = _nearest(run, e.x, e.y, 130, lambda o: o is not e and id(o) not in b.hit)
        if tgt:
            a = math.atan2(tgt.y - e.y, tgt.x - e.x)
            nb = run.fire_player_bullet(e.x, e.y, a, dmg * 0.7, p.s['shotspd'], max(1.5, b.r * 0.8), 0.6, {'_ric': b.fl.get('_ric', 0) + 1})
            nb.hit |= b.hit | {id(e)}
            if b.fl.get('_ric', 0) == 1 and 'ninja' in S:
                _syn(run, 'ninja', e.x, e.y, (200, 200, 220))


def on_kill(run, e):
    p = run.player
    S = p.sgs
    if not S:
        return
    g = st(p)
    if 'irrlicht' in S:
        tgt = _nearest(run, e.x, e.y, 200, lambda o: o is not e)
        a = math.atan2(tgt.y - e.y, tgt.x - e.x) if tgt else random.uniform(0, math.tau)
        two = 'geisterlicht' in S
        if two:
            _syn(run, 'geisterlicht', e.x, e.y, (120, 190, 255))
        for da in ((-0.5, 0.5) if two else (0,)):
            b = run.fire_player_bullet(e.x, e.y, a + da, p.damage() * 0.8, 150, 3, 1.6,
                                       {'homing': 1, 'burn': 1, 'spectral': 1} if two else {'homing': 1, 'burn': 1})
            b.col = (120, 190, 255)
    if 'faehrmann' in S:
        g['souls'] = g.get('souls', 0) + 1
        if g['souls'] >= 12:
            g['souls'] = 0
            p.add_spirit(1)
            _float(run, e, 'Fährgeld', (190, 190, 220))
            _syn(run, 'faehrmann', e.x, e.y + 10, (190, 190, 220))
    if 'ewige_flamme' in S and e.burn > 0:
        tgt = _nearest(run, e.x, e.y, 60, lambda o: o is not e)
        if tgt:
            tgt.burn = max(tgt.burn, 3.0)
            tgt.burn_dps = max(tgt.burn_dps, e.burn_dps)
            run.zap(e.x, e.y, tgt.x, tgt.y)
    if 'oelfeuer' in S and getattr(e, 'sg_oil', 0) > 0:
        _syn(run, 'oelfeuer', e.x, e.y, (255, 150, 60))
        from .entities import Hazard
        run.explode(e.x, e.y, 30, p.damage() * 1.6, 'p')
        run.hazards.append(Hazard(e.x, e.y + 4, 14, 0.0, 2.5, max(0.8, p.damage() * 0.4), 'p', 'fire'))
    if 'erstes_feuer' in S and e.burn > 0:
        run.explode(e.x, e.y, 26, p.damage() * 1.4, 'p')
        if 'enenra' in S:
            clouds = g.setdefault('clouds', [])
            clouds.append([e.x, e.y, 2.5])
            del clouds[:-6]
    if 'tennyo' in S:
        g['bluete'] = min(g.get('bluete', 0) + 2, run.time - getattr(run, 'room_enter_time', run.time))
    if 'totenfaehre' in S and p.revives == 0:
        g['faehre'] = g.get('faehre', 0) + 1
        if g['faehre'] >= 40:
            g['faehre'] = 0
            p.revives = 1
            _float(run, p, 'Münze für den Fährmann', (190, 220, 230))
            _syn(run, 'totenfaehre', p.x, p.y + 10, (190, 220, 230))
    if 'parade' in S:
        g['parade'] = min(20 if 'maskenzug' in S else 15, g.get('parade', 0) + 1)
    if 'wirbelklingen' in S and getattr(e, 'sg_bleed', 0) > 0:
        _syn(run, 'wirbelklingen', e.x, e.y, (230, 230, 240))
        for i in range(3):
            b = run.fire_player_bullet(e.x, e.y, i / 3 * math.tau + random.uniform(0, 2), p.damage() * 0.7, 180, 2.5, 0.7, {'pierce': 1})
            b.curve = 2.0
            b.col = (230, 230, 240)
    if 'leben_tod' in S and random.random() < 0.05:
        p.add_spirit(1)
        _syn(run, 'leben_tod', e.x, e.y, (200, 160, 230))
    if 'lachen' in S:
        far = 'gelaechter' in S
        for o in run.enemies:
            if o is not e and o.active() and not o.is_boss and math.hypot(o.x - e.x, o.y - e.y) < (150 if far else 75):
                o.sg_fear = 3.0 if far else 2.0
                if far:
                    _syn(run, 'gelaechter', e.x, e.y, (255, 170, 230))
    if 'ema' in S and e.is_boss:
        from .texts import FX_NAMES
        wishes = []
        for _ in range(2 if 'jinmenju' in S else 1):
            k = random.choice(('dmg', 'rate', 'spd', 'range', 'luck'))
            v = {'dmg': 0.5, 'rate': 0.4, 'spd': 6, 'range': 30, 'luck': 1}[k]
            bonus = g.setdefault('ema', {})
            bonus[k] = bonus.get(k, 0) + v
            wishes.append('%s +%g' % (FX_NAMES[k][0], v))
        if 'jinmenju' in S:
            p.heal(p.maxhp)
            _syn(run, 'jinmenju', e.x, e.y, (240, 190, 140))
        p.recalc()
        run.banner('Ema: Wunsch erfüllt', ', '.join(wishes), (255, 220, 140))


def on_hurt(p, run):
    """Nach echtem Schaden, vor der Todesprüfung."""
    S = p.sgs
    if not S:
        return
    g = st(p)
    g['room_hit'] = True
    g['ts'] = 0
    if 'hannya_zorn' in S:
        g['hannya'] = 6.0
        _syn(run, 'hannya_zorn', p.x, p.y, (255, 90, 60))
    if 'zwischenwelt' in S:
        p.iframes += 0.8
    if 'aufstehen' in S:
        p.iframes += 0.6
        _ring(run, p.x, p.y, (255, 120, 100), 50)
        for e in run.enemies:
            d = math.hypot(e.x - p.x, e.y - p.y)
            if e.active() and d < 60 and not e.is_boss:
                e.kx += (e.x - p.x) / max(d, 1) * 420
                e.ky += (e.y - p.y) / max(d, 1) * 420
        if 'daruma_geist' in S:
            _syn(run, 'daruma_geist', p.x, p.y, (255, 210, 90))
            seen = set()                       # Splitter treffen jeden Feind nur einmal
            for i in range(8):
                b = run.fire_player_bullet(p.x, p.y - 3, i / 8 * math.tau, p.damage() * 1.5, 220, 3, 0.8, {'pierce': 1})
                b.col = (255, 210, 90); b.hit = seen
    if 'momo' in S:
        _momo(p, run)
    if 'a_un' in S:
        g['agyo'] = 0.01
        _syn(run, 'a_un', p.x, p.y, (220, 220, 200))
    if 'glockenschlag' in S:
        _ring(run, p.x, p.y, (255, 230, 150), 90)
        for e in run.enemies:
            if e.active():
                e.frozen = max(e.frozen, 0.3 if e.is_boss else 1.0)
    if 'rache' in S or 'johari' in S:
        e = _nearest(run, p.x, p.y, 160)
        if e:
            if 'rache' in S:
                e.sg_curse = 8.0
                _float(run, e, 'Verflucht', (200, 120, 255))
            if 'johari' in S:
                run.zap(p.x, p.y, e.x, e.y)
                run.damage_enemy(e, p.damage() * 8, None)
    if 'kenko' in S and g.get('kenko_used', 0) < (2 if 'omamori_set' in S else 1) and p.total_hp() == 1:
        g['kenko_used'] = g.get('kenko_used', 0) + 1
        p.heal(2)
        if g['kenko_used'] == 2:
            _syn(run, 'omamori_set', p.x, p.y, (255, 200, 210))
    if 'kraniche' in S and p.total_hp() <= 0 and g.get('cranes', 0) >= 10:
        g['cranes'] = 0
        p.hp = max(p.hp, 1) if not p.spirit_only else p.hp
        if p.spirit_only:
            p.spirit = max(p.spirit, 1)
        p.iframes = 2.0
        run.banner('Tausend Kraniche', 'Dein Wunsch hat dich gerettet', (250, 240, 230))


def block(p, run, b):
    """Feindliches Geschoss trifft gleich – True, wenn es abgewehrt wird."""
    S = p.sgs
    if 'tsukumogami' in S and p.dash_t > 0:
        _syn(run, 'tsukumogami', p.x, p.y, (220, 80, 60))
        nb = run.fire_player_bullet(b.x, b.y, math.atan2(-b.vy, -b.vx), p.damage() * 1.2, 240, 3.5, 1.2, {'homing': 1})
        nb.col = (180, 200, 250)
        return True
    if not S or p.iframes > 0:
        return False
    g = st(p)
    if 'rauch' in S:
        for c in g.get('clouds', ()):
            if (b.x - c[0]) ** 2 + (b.y - c[1]) ** 2 < 20 ** 2:
                return True
    if 'spiegel' in S:
        g['mirror'] = g.get('mirror', 0) + 1
        if g['mirror'] % (2 if 'onmyo_spiegel' in S else 3) == 0:
            if 'onmyo_spiegel' in S:
                _syn(run, 'onmyo_spiegel', p.x, p.y, (255, 230, 150))
            a = math.atan2(-b.vy, -b.vx)
            nb = run.fire_player_bullet(b.x, b.y, a, p.damage() * 1.5, 260, 3.5, 1.0,
                                        {'homing': 1, 'explode': 1} if 'onmyo_spiegel' in S else {'homing': 1})
            nb.col = (255, 230, 150)
            if 'gericht' in S:
                _syn(run, 'gericht', p.x, p.y, (200, 120, 255))
                nb.fl['_urteil'] = 1
            if 'sonnenspiegel' in S:
                _syn(run, 'sonnenspiegel', p.x, p.y, (255, 190, 90))
                nb.fl['burn'] = 1
                for da in (-0.3, 0.3):
                    sb = run.fire_player_bullet(b.x, b.y, a + da, p.damage() * 1.2, 260, 3, 1.0,
                                                {'homing': 1, 'burn': 1, '_urteil': 1} if 'gericht' in S else {'homing': 1, 'burn': 1})
                    sb.col = (255, 190, 90)
            return True
    if 'schuppenpanzer' in S and random.random() < (0.35 if 'drachenschuppen' in S else 0.25):
        if 'drachenschuppen' in S:
            _syn(run, 'drachenschuppen', p.x, p.y, (120, 200, 255))
            nb = run.fire_player_bullet(b.x, b.y, math.atan2(b.y - p.y, b.x - p.x), p.damage() * 1.3, 200, 3.5, 1.2, {'homing': 1})
            nb.col = (120, 200, 255)
        return True
    if 'panzer' in S and g.get('still', 0) > 1.0 and random.random() < 0.5:
        return True
    return False


def shield_break(p, run):
    if 'unbeweglich' in p.sgs:
        _syn(run, 'unbeweglich', p.x, p.y, (200, 200, 220))
        st(p)['wand'] = 8.0
    if has(p, 'wandbruch'):
        _ring(run, p.x, p.y, (200, 200, 220), 80)
        for e in run.enemies:
            d = math.hypot(e.x - p.x, e.y - p.y)
            if e.active() and d < 110 and not e.is_boss:
                e.kx += (e.x - p.x) / max(d, 1) * 520
                e.ky += (e.y - p.y) / max(d, 1) * 520


def ebullet_dt(p, b, dt):
    if 'klingeling' in p.sgs and (b.x - p.x) ** 2 + (b.y - p.y) ** 2 < (80 if 'winkekatze' in p.sgs else 40) ** 2:
        return dt * 0.55
    return dt


def _momo(p, run, mult=3):
    """Izanagis Pfirsiche: drei Würfe auf die nächsten Feinde, nahe Yokai fliehen."""
    flucht = 'izanagis_flucht' in p.sgs
    st(p)['momo'] = run.time
    foes = sorted((e for e in run.enemies if e.active()), key=lambda e: math.hypot(e.x - p.x, e.y - p.y))
    for k in range(3):
        a = math.atan2(foes[k % len(foes)].y - p.y, foes[k % len(foes)].x - p.x) if foes else k * math.tau / 3
        b = run.fire_player_bullet(p.x, p.y - 3, a + (k - 1) * 0.12, p.damage() * mult, 170, 4, 1.4, {'pierce': 1})
        b.col = (255, 170, 140)
    reach = 140 if flucht else 90
    for e in foes:
        if not e.is_boss and math.hypot(e.x - p.x, e.y - p.y) < reach:
            e.sg_fear = max(getattr(e, 'sg_fear', 0), 6.0 if flucht else 3.0)
    _ring(run, p.x, p.y, (255, 170, 140), reach * 0.6)


def on_dash(p, run):
    S = p.sgs
    if not S:
        return
    g = st(p)
    if 'suzu' in S and run.time - g.get('suzu', -9) >= (2.5 if 'iwato' in S else 4.0):
        _suzu(p, run)
    if 'izanagis_flucht' in S and run.time - g.get('momo', -9) >= 3.0:
        _syn(run, 'izanagis_flucht', p.x, p.y, (255, 170, 140))
        _momo(p, run, 1.5)
    if 'tarnung' in S:
        g['invis'] = 2.6 if 'hara_tsuzumi' in S else 1.3
    if 'hara_tsuzumi' in S:
        _syn(run, 'hara_tsuzumi', p.x, p.y, (200, 150, 90))
        _ring(run, p.x, p.y, (200, 150, 90), 60)
        from . import audio
        audio.play('roar', 0.25)
        for e in run.enemies:
            d = math.hypot(e.x - p.x, e.y - p.y)
            if e.active() and d < 60 + e.r:
                run.damage_enemy(e, p.damage() * 1.2, None)
                if not e.is_boss:
                    e.kx += (e.x - p.x) / max(d, 1) * 450
                    e.ky += (e.y - p.y) / max(d, 1) * 450
    if 'iaido' in S:
        g['iaido'] = 1.2
    if 'schweiss' in S:
        g['schweiss'] = 1
    if 'rauch' in S:
        clouds = g.setdefault('clouds', [])
        clouds.append([p.x, p.y, 1.6])
        del clouds[:-4]
    if 'tengu_flug' in S:
        _syn(run, 'tengu_flug', p.x, p.y, (200, 230, 210))
        _ring(run, p.x, p.y, (200, 230, 210), 55)
        for e in run.enemies:
            d = math.hypot(e.x - p.x, e.y - p.y)
            if e.active() and d < 55 + e.r:
                run.damage_enemy(e, p.damage() * 1.2, None)
                if not e.is_boss:
                    e.kx += (e.x - p.x) / max(d, 1) * 360
                    e.ky += (e.y - p.y) / max(d, 1) * 360
    if 'feuerkind' in S:
        _syn(run, 'feuerkind', p.x, p.y, (240, 170, 60))
        _ring(run, p.x, p.y, (240, 170, 60), 60)
        for e in run.enemies:
            if e.active() and math.hypot(e.x - p.x, e.y - p.y) < 60 + e.r:
                e.sg_oil = 3.0
                e.burn = 3.0
                e.burn_dps = max(e.burn_dps, max(1.0, p.damage() * 0.4))
    if 'feuerwagen' in S:
        _syn(run, 'feuerwagen', p.x, p.y, (255, 110, 40))
        a = math.atan2(p.dash_dir[1], p.dash_dir[0])
        for da in (-0.25, 0.25):
            b = run.fire_player_bullet(p.x, p.y, a + da, p.damage() * 1.1, 150, 5, 1.2, {'pierce': 1, 'burn': 1})
            b.col = (255, 110, 40)
    if 'flatter' in S:
        n = 8 if 'sommerwind' in S else 4
        if 'sommerwind' in S:
            _syn(run, 'sommerwind', p.x, p.y, (200, 240, 220))
        for i in range(n):
            a = i / n * math.tau + math.pi / 4
            run.fire_player_bullet(p.x, p.y - 3, a, p.damage() * 0.7, p.s['shotspd'], 2.5, 1.1 if 'sommerwind' in S else 0.7, {})


def _suzu(p, run):
    """Uzumes Kagura-Suzu: der Klang löscht nahe Geschosse, die Yokai lachen und fliehen."""
    from . import audio
    st(p)['suzu'] = run.time
    near = [b for b in run.ebullets if math.hypot(b.x - p.x, b.y - p.y) < 55]
    run.ebullets = [b for b in run.ebullets if math.hypot(b.x - p.x, b.y - p.y) >= 55]
    for e in run.enemies:
        if e.active() and not e.is_boss and math.hypot(e.x - p.x, e.y - p.y) < 70 + e.r:
            e.sg_fear = max(getattr(e, 'sg_fear', 0), 2.0)
    _ring(run, p.x, p.y, (255, 214, 90), 55)
    audio.play('bell', 0.5)
    if 'iwato' in p.sgs and near:
        _syn(run, 'iwato', p.x, p.y, (255, 230, 140))
        for k, b in enumerate(near[:8]):
            e = _nearest(run, b.x, b.y)
            a = math.atan2(e.y - b.y, e.x - b.x) if e else k * math.tau / 8
            sb = run.fire_player_bullet(b.x, b.y, a, p.damage() * 1.2, 240, 3, 1.0, {'pierce': 1})
            sb.col = (255, 230, 140)


def on_coin(p, run, v):
    """Gibt zusätzliche Mon zurück."""
    S = p.sgs
    if not S:
        return 0
    g = st(p)
    extra = 0
    if 'fuchsglueck' in S and v == 1 and random.random() < (0.4 if 'fuchsgeld' in S else 0.2):
        extra = 4
        if 'fuchsgeld' in S:
            _syn(run, 'fuchsgeld', p.x, p.y, (255, 170, 90))
    if 'tanuki_bauch' in S:
        g['bauch'] = g.get('bauch', 0) + v + extra
        while g['bauch'] >= 25:
            g['bauch'] -= 25
            p.heal(1)
    return extra


def on_room_enter(run):
    p = run.player
    S = p.sgs
    if not S:
        return
    g = st(p)
    g['tiger'] = 0
    g['syn_seen'] = []
    if 'maskenzug' not in S:
        g['parade'] = 0
    g['room_hit'] = False
    g['bluete'] = 0
    g['webs'] = []
    g['clouds'] = []
    g['rooms'] = g.get('rooms', 0) + 1
    if 'proviant' in S and g.get('proviant', 0) > 0 and not run.room.cleared:
        g['proviant'] -= 1
        p.heal(1)
    if 'a_gyo' in S and not run.room.cleared:
        g['agyo'] = 0.75
    g['pot'] = 0


def on_room_clear(run):
    p = run.player
    S = p.sgs
    if not S:
        return
    g = st(p)
    luck = p.s['luck']
    if 'ewigkeit' in S:
        g['ewig'] = g.get('ewig', 0) + 1
        if g['ewig'] >= 5:
            g['ewig'] = 0
            p.heal(1)
    if 'opfergabe' in S and random.random() < (0.1 + 0.01 * luck) * (3 if 'shinsen' in S else 1):
        run.spawn_pickup('key', p.x, p.y - 20)
        if 'shinsen' in S:
            _syn(run, 'shinsen', p.x, p.y, (240, 240, 245))
    if 'sternschnuppe' in S and random.random() < (0.08 + 0.006 * luck) * (3 if 'wunsch' in S else 1):
        run.random_drop(p.x + random.uniform(-30, 30), p.y - 24)
        if 'wunsch' in S:
            _syn(run, 'wunsch', p.x, p.y, (255, 240, 170))
    if 'kraniche' in S and g.get('cranes', 0) < 10:
        g['cranes'] = g.get('cranes', 0) + 1
        if g['cranes'] == 10:
            run.banner('Tausend Kraniche', 'Der Wunsch ist gefaltet', (250, 240, 230))
    if 'anmut' in S and not g.get('room_hit'):
        g['anmut'] = min(1.0, g.get('anmut', 0) + 0.15)
        p.recalc()
    if 'gokaku' in S and run.time - getattr(run, 'room_enter_time', run.time) < (15 if 'nanakorobi' in S else 10):
        g['gokaku'] = min(8 if 'nanakorobi' in S else 5, g.get('gokaku', 0) + 1)


def on_floor(run):
    p = run.player
    S = p.sgs
    if not S:
        return
    g = st(p)
    g['kenko_used'] = 0
    g['parade'] = 0
    g['anmut'] = 0
    g['gokaku'] = 0
    if 'neujahr' in S:
        p.heal(2)
    p.recalc()


def on_gain(p, iid):
    if iid == 'onigiri':
        st(p)['proviant'] = st(p).get('proviant', 0) + 3


def on_chest(run, pk):
    if 'kinun' in run.player.sgs:
        for _ in range(2 if 'omamori_set' in run.player.sgs else 1):
            run.random_drop(pk.x, pk.y)
        if 'omamori_set' in run.player.sgs:
            _syn(run, 'omamori_set', pk.x, pk.y, (255, 200, 210))


def on_salt(p, run):
    if 'reinigung' in p.sgs:
        p.heal(2 if 'shinsen' in p.sgs else 1)
        if 'shinsen' in p.sgs:
            _syn(run, 'shinsen', p.x, p.y, (240, 240, 245))


def on_pot(run, x, y):
    """True: dieser Krug lässt sicher etwas fallen."""
    p = run.player
    if 'hausglueck' in p.sgs and st(p).get('pot', 0) < (2 if 'gluecksheim' in p.sgs else 1):
        st(p)['pot'] = st(p).get('pot', 0) + 1
        if st(p)['pot'] == 2:
            _syn(run, 'gluecksheim', x, y, (255, 190, 200))
        return True
    return False


def contact(p, run, e):
    """Ein Feind berührt dich. True = Schaden an dir ausbleiben lassen."""
    S = p.sgs
    if not S:
        return False
    g = st(p)
    if 'kappa_freund' in S and e.id.startswith('kappa'):
        return True
    cd = getattr(e, 'sg_touch', 0)
    if cd <= 0:
        if 'klebrig' in S and not e.is_boss:
            e.frozen = max(e.frozen, 1.0)
            if 'shogatsu' in S:
                _syn(run, 'shogatsu', e.x, e.y, (255, 220, 200))
                e.sg_curse = max(getattr(e, 'sg_curse', 0), 3.0)
            e.sg_touch = 1.5
        if 'oni_koenig' in S:
            run.damage_enemy(e, p.damage() * (3.0 if 'oeyama_bande' in S else 1.5), None)
            e.sg_touch = 0.5
            if 'oeyama_bande' in S and not e.is_boss:
                _syn(run, 'oeyama_bande', e.x, e.y, (255, 110, 90))
                e.sg_conf = max(getattr(e, 'sg_conf', 0), 1.0)
        if 'felsblock' in S and not e.is_boss:
            d = math.hypot(e.x - p.x, e.y - p.y) or 1
            e.kx += (e.x - p.x) / d * 380
            e.ky += (e.y - p.y) / d * 380
            e.sg_touch = 0.4
            if 'yomotsu' in S:
                _syn(run, 'yomotsu', e.x, e.y, (200, 180, 255))
                e.frozen = max(e.frozen, 1.5)
                e.sg_curse = 3.0
    return False


def enemy_tick(e, dt):
    """Statuseffekte der Signaturen am Feind. True = KI diesen Frame übernehmen (keine eigene Bewegung)."""
    run = e.run
    if getattr(e, 'sg_bleed_t', 0) > 0:
        e.sg_bleed_t -= dt
        e.hp -= e.sg_bleed * 1.0 * dt
        if random.random() < 0.15:
            from .entities import Particle
            run.particles.append(Particle(e.x + random.uniform(-3, 3), e.y, 0, 20, 0.3, (200, 30, 40), 1))
        if e.sg_bleed_t <= 0:
            e.sg_bleed = 0
    for k in ('sg_curse', 'sg_oil', 'sg_blind', 'sg_touch'):
        v = getattr(e, k, 0)
        if v > 0:
            setattr(e, k, v - dt)
    if getattr(e, 'sg_oil', 0) > 0:
        e.slowed = max(e.slowed, 0.05)
    if 'ewige_flamme' in run.player.sgs and e.burn > 0:
        e.burn = max(e.burn, 0.5)
    conf = getattr(e, 'sg_conf', 0)
    fear = getattr(e, 'sg_fear', 0)
    if conf > 0 or fear > 0:
        e.sg_conf = max(0, conf - dt)
        e.sg_fear = max(0, fear - dt)
        from .entities import move_body
        p = run.player
        if fear > 0:
            dx, dy = e.x - p.x, e.y - p.y
        else:
            a = e.t * 2.3 + id(e) % 7
            dx, dy = math.cos(a), math.sin(a)
        d = math.hypot(dx, dy) or 1
        sp = e.speed * 0.8 + 20
        e.x, e.y, _, _ = move_body(run.room, e.x, e.y, e.r, dx / d * sp * dt, dy / d * sp * dt, e.fly)
        return True
    return False


def no_attack(e):
    """True = dieser Feind greift gerade nicht an."""
    run = e.run
    p = run.player
    if getattr(e, 'sg_conf', 0) > 0 or getattr(e, 'sg_fear', 0) > 0:
        return True
    if st(p).get('invis', 0) > 0:
        return True
    if getattr(e, 'sg_blind', 0) > 0 and random.random() < 0.7:
        return True
    if 'kappa_freund' in p.sgs and e.id.startswith('kappa'):
        return True
    return False


def tick(p, run, dt):
    S = p.sgs
    if not S:
        return
    g = st(p)
    for k in ('invis', 'iaido', 'hannya', 'glocke'):
        if g.get(k, 0) > 0:
            g[k] -= dt
    if p.moving:
        g['still'] = 0
    else:
        g['still'] = g.get('still', 0) + dt
    if 'statik' in S and p.moving:
        before = g.get('statik', 0)
        g['statik'] = min(3.0, before + dt * (2 if 'sturmgott' in S else 1))
        if g['statik'] >= 3.0 and random.random() < 0.3:
            from .entities import Particle
            run.particles.append(Particle(p.x + random.uniform(-6, 6), p.y - 6, 0, 0, 0.15, (255, 250, 160), 1))
    fighting = any(e.active() for e in run.enemies)
    for key, period in (('sternkugel', 1.4), ('kranichflug', 2.0), ('augenhand', 0.9),
                        ('sonnenkraehe', 1.5 if ('himmelsbote' in S and p.moving) else 3.0),
                        ('fuchsregen', 2.0 if 'sonnenregen' in S else 3.5), ('schlangenschweif', 0.5), ('kichern', 1.0),
                        ('jingi', 5.0), ('tintenpanzer', 1.0), ('tiefsee_blick', 0.5)):
        if key not in S:
            continue
        tk = 't_' + key
        g[tk] = g.get(tk, 0) - dt
        if g[tk] > 0 or not fighting:
            continue
        g[tk] = period
        dmg = p.damage()
        if key == 'sternkugel':
            a = run.time * 2.2
            ox, oy = p.x + math.cos(a) * 24, p.y - 3 + math.sin(a) * 24
            tgt = _nearest(run, ox, oy, 220)
            if tgt:
                a0 = math.atan2(tgt.y - oy, tgt.x - ox)
                if 'fuchsstern' in S:
                    _syn(run, 'fuchsstern', ox, oy, (255, 240, 160))
                for da in ((-0.3, 0, 0.3) if 'fuchsstern' in S else (0,)):
                    b = run.fire_player_bullet(ox, oy, a0 + da, dmg * 0.6, 240, 2.2, 1.0, {'homing': 1})
                    b.col = (255, 240, 160)
        elif key == 'kranichflug':
            tgt = _nearest(run, p.x, p.y, 260)
            if tgt:
                k = 2 + min(3, g.get('cranes', 0) // 3) if 'kranichschwarm' in S else 1
                if k > 1:
                    _syn(run, 'kranichschwarm', p.x, p.y, (250, 250, 255))
                for i in range(k):
                    a = math.atan2(tgt.y - p.y, tgt.x - p.x) + (i - (k - 1) / 2) * 0.5
                    b = run.fire_player_bullet(p.x, p.y - 8, a, dmg * 0.9, 170, 3.0, 1.6, {'homing': 1, 'pierce': 1})
                    b.col = (250, 250, 255)
        elif key == 'augenhand':
            tgt = _nearest(run, p.x, p.y, 75)
            if tgt is None and 'augen_ueberall' in S:
                tgt = _nearest(run, p.x, p.y, 999, lambda o: getattr(o, 'sg_mark', False))
                if tgt:
                    _syn(run, 'augen_ueberall', tgt.x, tgt.y, (255, 120, 160))
            if tgt:
                b = run.fire_player_bullet(p.x, p.y - 3, math.atan2(tgt.y - p.y, tgt.x - p.x), dmg * 0.7, 260, 2.5, 0.5, {})
                b.col = (255, 140, 140)
        elif key == 'sonnenkraehe':
            tgt = _nearest(run, p.x, p.y, 300)
            if tgt:
                from .entities import Hazard
                run.hazards.append(Hazard(tgt.x, tgt.y, 12, 0.35, 0.12, dmg * 2.0, 'p', 'slam', (255, 200, 90)))
                if 'himmelsbote' in S and p.moving:
                    _syn(run, 'himmelsbote', tgt.x, tgt.y, (255, 200, 90))
        elif key == 'fuchsregen':
            cand = [e for e in run.enemies if e.active()]
            if cand:
                e = random.choice(cand)
                from .entities import Hazard
                run.hazards.append(Hazard(e.x, e.y, 14, 0.3, 0.15, dmg * 1.5, 'p', 'water'))
                if 'sonnenregen' in S and random.random() < 0.15:
                    run.spawn_pickup('coin', e.x, e.y)
                    _syn(run, 'sonnenregen', e.x, e.y, (255, 200, 120))
        elif key == 'schlangenschweif':
            bx, by = p.x - p.facing[0] * 16, p.y - p.facing[1] * 16
            for e in run.enemies:
                if e.active() and math.hypot(e.x - bx, e.y - by) < 22 + e.r:
                    run.damage_enemy(e, dmg * 0.8, None)
                    e.poison = max(e.poison, 2.5)
                    e.poison_dps = max(e.poison_dps, 1.0)
                    if 'unterweltgift' in S:
                        _syn(run, 'unterweltgift', e.x, e.y, (170, 110, 220))
                        e.sg_curse = 4.0
                    run.zap(bx, by, e.x, e.y)
                    break
        elif key == 'jingi':
            for e in sorted((e for e in run.enemies if e.active()), key=lambda e: -e.hp)[:3]:
                _syn(run, 'jingi', p.x, p.y, (255, 220, 120))
                run.lightning(e.x, e.y, dmg * 2.5 + 4)
        elif key == 'tintenpanzer':
            if g.get('still', 0) > 1.0:
                for e in run.enemies:
                    if e.active() and math.hypot(e.x - p.x, e.y - p.y) < 65:
                        e.sg_blind = 2.0
                        _syn(run, 'tintenpanzer', p.x, p.y, (110, 110, 170))
        elif key == 'tiefsee_blick':
            fx, fy = p.facing
            for e in run.enemies:
                dx, dy = e.x - p.x, e.y - p.y
                d = math.hypot(dx, dy) or 1
                if e.active() and d < 170 and (dx * fx + dy * fy) / d > 0.85:
                    run.damage_enemy(e, max(0.5, dmg * 0.25), None)
                    _syn(run, 'tiefsee_blick', e.x, e.y, (90, 170, 220))
        elif key == 'kichern':
            for e in run.enemies:
                if e.active() and not e.is_boss and math.hypot(e.x - p.x, e.y - p.y) < 85 and random.random() < 0.2:
                    e.frozen = max(e.frozen, 0.45)
                    if 'gelaechter' in S:
                        e.sg_fear = max(getattr(e, 'sg_fear', 0), 1.5)
    if 'bannkreis' in S:
        for e in run.enemies:
            if e.active() and not e.is_boss:
                d = math.hypot(e.x - p.x, e.y - p.y)
                if d < (56 if 'schreinwaechter' in S else 28) + e.r:
                    e.kx += (e.x - p.x) / max(d, 1) * 160 * dt * 10
                    e.ky += (e.y - p.y) / max(d, 1) * 160 * dt * 10
    if 'starrt' in S:
        fx, fy = p.facing
        for e in run.enemies:
            if e.active():
                dx, dy = e.x - p.x, e.y - p.y
                d = math.hypot(dx, dy) or 1
                if d < 170 and (dx * fx + dy * fy) / d > 0.85:
                    e.slowed = max(e.slowed, 0.05)
    if 'schreinwaechter' in S and fighting:
        g['schrein'] = g.get('schrein', 0) + dt
        if g['schrein'] >= 8:
            g['schrein'] = 0
            g['agyo'] = 0.01
            _syn(run, 'schreinwaechter', p.x, p.y, (255, 200, 120))
    if g.get('wand', 0) > 0:
        g['wand'] -= dt
        if g['wand'] <= 0 and 'unbeweglich' in S and p.f['shield']:
            p.shield_ready = True
            _ring(run, p.x, p.y, (140, 200, 255), 30)
    if g.get('agyo', 0) > 0:
        g['agyo'] -= dt
        if g['agyo'] <= 0:
            from . import audio
            audio.play('roar', 0.35)
            _ring(run, p.x, p.y, (220, 220, 200), 90)
            for e in run.enemies:
                d = math.hypot(e.x - p.x, e.y - p.y)
                if not e.is_boss and d < 110:
                    e.kx += (e.x - p.x) / max(d, 1) * 480
                    e.ky += (e.y - p.y) / max(d, 1) * 480
    webs = g.get('webs')
    if webs:
        for w in webs:
            w[2] -= dt
            for e in run.enemies:
                if e.active() and (e.x - w[0]) ** 2 + (e.y - w[1]) ** 2 < 18 ** 2:
                    e.slowed = max(e.slowed, 0.1)
                    if 'giftnetz' in S:
                        e.poison = max(e.poison, 2.0); e.poison_dps = max(e.poison_dps, 1.0)
                        _syn(run, 'giftnetz', e.x, e.y, (150, 235, 110))
            if random.random() < 0.08:
                from .entities import Particle
                run.particles.append(Particle(w[0] + random.uniform(-10, 10), w[1] + random.uniform(-6, 6), 0, 0, 0.4, (230, 230, 240), 1))
        g['webs'] = [w for w in webs if w[2] > 0]
    clouds = g.get('clouds')
    if clouds:
        from .entities import Particle
        hot = 'enenra' in S
        for c in clouds:
            c[2] -= dt
            if random.random() < 0.5:
                run.particles.append(Particle(c[0] + random.uniform(-14, 14), c[1] + random.uniform(-10, 10), 0, -6, 0.5,
                                              (190, 110, 70) if hot and random.random() < 0.4 else (150, 150, 160), 4))
            if hot:
                for e in run.enemies:
                    if e.active() and (e.x - c[0]) ** 2 + (e.y - c[1]) ** 2 < (20 + e.r) ** 2:
                        if e.burn <= 0:
                            _syn(run, 'enenra', e.x, e.y, (255, 140, 70))
                        e.burn = max(e.burn, 2.0)
                        e.burn_dps = max(e.burn_dps, max(0.8, p.damage() * 0.35))
        g['clouds'] = [c for c in clouds if c[2] > 0]


def dmg_mult(p):
    S = p.sgs
    if not S:
        return 1.0
    g = st(p)
    run = p.run
    m = 1.0
    if 'vergaenglich' in S:
        t = run.time - getattr(run, 'room_enter_time', run.time) - g.get('bluete', 0)
        dur, top = (15, 0.6) if 'hanami' in S else (10, 0.4)
        if t < dur and not run.room.cleared:
            m *= 1 + top * (1 - t / dur)
    if 'satt' in S and p.hp >= p.maxhp and p.maxhp > 0:
        m *= 1.4 if 'hanami_picknick' in S else 1.2
    if 'ehre' in S and not getattr(p, 'hit_this_floor', False):
        m *= 1.45 if 'bushi' in S else 1.25
    if 'lange_reise' in S:
        m *= 1 + (0.1 if 'pilger' in S else 0.05) * max(0, run.depth - 1)
    if 'parade' in S:
        m *= 1 + 0.03 * g.get('parade', 0)
    if g.get('hannya', 0) > 0:
        m *= 1.5
    if 'gokaku' in S:
        m *= 1 + 0.1 * g.get('gokaku', 0)
    if 'maskenwechsel' in S and g.get('rooms', 0) % 2 == 0:
        m *= 1.35
    return m


def rate_mult(p):
    S = p.sgs
    if not S:
        return 1.0
    g = st(p)
    m = 1.0
    if 'wach' in S:
        m *= 1 + g.get('wach', 0)
    if 'maskenwechsel' in S and g.get('rooms', 0) % 2 == 1:
        m *= 1.35
    if 'reichtum' in S and p.coins >= (25 if 'kaufmann' in S else 50):
        m *= 1.25 if 'kaufmann' in S else 1.15
    return m


def stat_bonus(p, f):
    """Dauerhafte, gesammelte Boni (Ema, Anmut) in die Werte-Summe einrechnen."""
    if not getattr(p, 'sg', None):
        return
    for k, v in p.sg.get('ema', {}).items():
        f[k] += v
    if f.get('sig_anmut'):
        f['rate'] += p.sg.get('anmut', 0)


def on_lightning(run, x, y):
    if 'sturmfaecher' in run.player.sgs:
        _syn(run, 'sturmfaecher', x, y, (200, 240, 220))
        _ring(run, x, y, (200, 240, 220), 45)
        for e in run.enemies:
            d = math.hypot(e.x - x, e.y - y)
            if e.active() and d < 45 + e.r and not e.is_boss:
                e.kx += (e.x - x) / max(d, 1) * 380
                e.ky += (e.y - y) / max(d, 1) * 380
