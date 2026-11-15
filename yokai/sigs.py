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
    'erstes_feuer': 'Brennende Feinde explodieren beim Tod',
    'fuchsregen': 'Ein Sonnenregen fällt auf deine Feinde',
    'hausglueck': 'Der erste Krug in jedem Raum gibt immer etwas her',
    'felsblock': 'Unbeweglich: nichts bremst dich, Feinde prallen ab',
    'wandbruch': 'Bricht der Schild, stößt er alle Feinde weg',
    'glockenschlag': 'Wirst du getroffen, erstarren alle Feinde',
}

BULLET_SIGS = ('sichel', 'kammzinken', 'seidenfaden', 'stromauf', 'gross', 'schweben', 'windstoss')


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


def _float(run, e, txt, col):
    run.floats.append([e.x, e.y - 16, txt, col, 0.6])


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
        for b in bullets:
            b.curve = 1.7 * g['sichel']
    if 'rueckenwind' in S and p.moving:
        for b in bullets:
            b.vx *= 1.3; b.vy *= 1.3; b.dmg *= 1.15
    if 'rausch' in S:
        for b in bullets:
            a = math.atan2(b.vy, b.vx) + random.uniform(-0.28, 0.28)
            sp = math.hypot(b.vx, b.vy)
            b.vx, b.vy = math.cos(a) * sp, math.sin(a) * sp
            b.dmg *= 1.3
    if 'goldfaecher' in S and not p.moving:
        for b in bullets:
            b.dmg *= 1.25
    if 'nasebrennt' in S:
        if run.time - g.get('last_fire', -9) > 1.0:
            for b in bullets:
                b.dmg *= 2; b.col = (170, 255, 120)
    if 'schweiss' in S and g.get('schweiss', 0) > 0:
        g['schweiss'] = 0
        for b in bullets:
            b.dmg *= 1.4
    if 'falkenblick' in S:
        for b in bullets:
            a = math.atan2(b.vy, b.vx)
            best, bd = None, 0.45
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
        else:
            g['wach'] = 0
    g['last_fire'] = run.time
    extra = []
    if 'neun' in S and n % 9 == 0:
        extra += [(base + (i - 4) * 0.13, 0.7, 1.0) for i in range(9)]
    if 'buendel' in S and n % 4 == 0:
        extra += [(base + random.uniform(-0.35, 0.35), 0.5, 0.7) for _ in range(3)]
    if 'drei_baellchen' in S and n % 3 == 0:
        extra += [(base - 0.12, 0.8, 0.9), (base + 0.12, 0.8, 0.9)]
    for a, dm, sz in extra:
        run.fire_player_bullet(p.x, p.y - 3, a, dmg * dm, spd, size * sz, life, {})
    if 'zweischwanz' in S and random.random() < 0.25:
        run.fire_player_bullet(p.x, p.y - 3, base, dmg * 0.8, spd, size, life, {}, delay=0.08)
    if 'statik' in S and g.get('statik', 0) >= 3.0:
        g['statik'] = 0
        tgt = run.nearest_enemy(p.x, p.y, 400)
        if tgt:
            run.lightning(tgt.x, tgt.y, dmg * 2 + 4)
    if 'klingen' in S and n % 8 == 0:
        from . import audio
        audio.play('bell', 0.4)
        _ring(run, p.x, p.y, (255, 230, 150), 60)
        for e in run.enemies:
            if e.active() and math.hypot(e.x - p.x, e.y - p.y) < 64:
                e.frozen = max(e.frozen, 0.25 if e.is_boss else 0.7)
    if 'boeser_stern' in S and n % 3 == 0:
        from .entities import Hazard
        tx, ty = p.x + math.cos(base) * 90, p.y + math.sin(base) * 90
        tgt = _nearest(run, tx, ty, 80)
        if tgt:
            tx, ty = tgt.x, tgt.y
        run.hazards.append(Hazard(tx, ty, 16, 0.45, 0.12, dmg * 2.2, 'p', 'meteor'))


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
        b.r = min(b.r * (1 + 1.2 * dt), 12)
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
            run.hazards.append(Hazard(b.x, b.y, 4, 0.0, 0.5, max(0.5, b.dmg * 0.18), 'p', 'silk'))
    if 'windstoss' in tags:
        rr = (b.r + 5) ** 2
        for eb in run.ebullets:
            if not eb.dead and (eb.x - b.x) ** 2 + (eb.y - b.y) ** 2 < rr:
                eb.dead = True
    return True


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
        dmg *= 2
        _float(run, e, 'Iai!', (230, 230, 255))
    if 'daemonenbrecher' in S and (e.is_boss or e.champ):
        dmg *= 1.5
    if 'hochmut' in S:
        dmg *= 1 + min(0.5, math.hypot(e.x - p.x, e.y - p.y) / 300)
    if 'tigerfell' in S and not g.get('tiger'):
        g['tiger'] = 1
        dmg *= 3
        _float(run, e, 'Tigerhieb!', (255, 190, 80))
    if getattr(e, 'sg_curse', 0) > 0:
        dmg *= 2
    if 'hundert_augen' in S and getattr(e, 'sg_mark', False):
        dmg *= 1.15
    if getattr(e, 'sg_oil', 0) > 0 and (b is None or b.fl.get('burn') or b.fl.get('explode')):
        dmg *= 1.6
    if 'schlagfolge' in S:
        if g.get('last_tgt') == id(e):
            g['chain'] = min(6, g.get('chain', 0) + 1)
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
    if 'treffsicher' in S:
        g['ts'] = min(0.2, g.get('ts', 0) + 0.02)
    if 'hundert_augen' in S:
        e.sg_mark = True
    if 'donnerbiest' in S:
        e.sg_thunder = getattr(e, 'sg_thunder', 0) + 1
        if e.sg_thunder >= 3:
            e.sg_thunder = 0
            run.lightning(e.x, e.y, p.damage() * 1.6 + 3)
    if 'pentagramm' in S:
        e.sg_pent = getattr(e, 'sg_pent', 0) + 1
        if e.sg_pent >= 5:
            e.sg_pent = 0
            _ring(run, e.x, e.y, (255, 230, 120), 34)
            run.explode(e.x, e.y, 28, p.damage() * 2.4, 'p')
    if 'schnitt' in S or 'drei_wiesel' in S:
        e.sg_bleed = min(3, getattr(e, 'sg_bleed', 0) + 1)
        e.sg_bleed_t = 3.0
    if 'drei_wiesel' in S:
        if not e.is_boss:
            e.frozen = max(e.frozen, 0.25)
        if random.random() < 0.04 and p.heal(1):
            from . import audio
            audio.play('heal', 0.4)
    if 'kuji' in S and random.random() < 1 / 9:
        e.frozen = max(e.frozen, 0.4 if e.is_boss else 1.5)
        _float(run, e, 'Gebannt', (220, 200, 255))
    if 'knochenbruch' in S and not e.is_boss and 0 < e.hp < e.maxhp * 0.15:
        e.hp = 0
        _float(run, e, 'Zerbrochen!', (240, 230, 210))
    if 'springfeuer' in S and random.random() < 0.2:
        from .entities import Hazard
        run.hazards.append(Hazard(e.x, e.y + 4, 10, 0.0, 2.0, max(0.6, p.damage() * 0.3), 'p', 'fire'))
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
    if 'wurfstern' in S and b is not None and not b.fl.get('_ric'):
        tgt = _nearest(run, e.x, e.y, 130, lambda o: o is not e)
        if tgt:
            a = math.atan2(tgt.y - e.y, tgt.x - e.x)
            nb = run.fire_player_bullet(e.x, e.y, a, dmg * 0.7, p.s['shotspd'], max(1.5, b.r * 0.8), 0.6, {'_ric': 1})
            nb.hit.add(id(e))


def on_kill(run, e):
    p = run.player
    S = p.sgs
    if not S:
        return
    g = st(p)
    if 'irrlicht' in S:
        tgt = _nearest(run, e.x, e.y, 200, lambda o: o is not e)
        a = math.atan2(tgt.y - e.y, tgt.x - e.x) if tgt else random.uniform(0, math.tau)
        b = run.fire_player_bullet(e.x, e.y, a, p.damage() * 0.8, 150, 3, 1.6, {'homing': 1, 'burn': 1})
        b.col = (120, 190, 255)
    if 'ewige_flamme' in S and e.burn > 0:
        tgt = _nearest(run, e.x, e.y, 60, lambda o: o is not e)
        if tgt:
            tgt.burn = max(tgt.burn, 3.0)
            tgt.burn_dps = max(tgt.burn_dps, e.burn_dps)
            run.zap(e.x, e.y, tgt.x, tgt.y)
    if 'erstes_feuer' in S and e.burn > 0:
        run.explode(e.x, e.y, 26, p.damage() * 1.4, 'p')
    if 'parade' in S:
        g['parade'] = min(15, g.get('parade', 0) + 1)
    if 'lachen' in S:
        for o in run.enemies:
            if o is not e and o.active() and not o.is_boss and math.hypot(o.x - e.x, o.y - e.y) < 75:
                o.sg_fear = 2.0
    if 'ema' in S and e.is_boss:
        k = random.choice(('dmg', 'rate', 'spd', 'range', 'luck'))
        v = {'dmg': 0.5, 'rate': 0.4, 'spd': 6, 'range': 30, 'luck': 1}[k]
        bonus = g.setdefault('ema', {})
        bonus[k] = bonus.get(k, 0) + v
        p.recalc()
        from .texts import FX_NAMES
        run.banner('Ema: Wunsch erfüllt', '%s +%g' % (FX_NAMES[k][0], v), (255, 220, 140))


def on_hurt(p, run):
    """Nach echtem Schaden, vor der Todesprüfung."""
    S = p.sgs
    if not S:
        return
    g = st(p)
    g['room_hit'] = True
    g['ts'] = 0
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
    if 'kenko' in S and not g.get('kenko_used') and p.total_hp() == 1:
        g['kenko_used'] = True
        p.heal(2)
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
    if not S or p.iframes > 0:
        return False
    g = st(p)
    if 'rauch' in S:
        for c in g.get('clouds', ()):
            if (b.x - c[0]) ** 2 + (b.y - c[1]) ** 2 < 20 ** 2:
                return True
    if 'spiegel' in S:
        g['mirror'] = g.get('mirror', 0) + 1
        if g['mirror'] % 3 == 0:
            a = math.atan2(-b.vy, -b.vx)
            nb = run.fire_player_bullet(b.x, b.y, a, p.damage() * 1.5, 260, 3.5, 1.0, {'homing': 1})
            nb.col = (255, 230, 150)
            return True
    if 'schuppenpanzer' in S and random.random() < 0.25:
        return True
    if 'panzer' in S and g.get('still', 0) > 1.0 and random.random() < 0.5:
        return True
    return False


def shield_break(p, run):
    if has(p, 'wandbruch'):
        _ring(run, p.x, p.y, (200, 200, 220), 80)
        for e in run.enemies:
            d = math.hypot(e.x - p.x, e.y - p.y)
            if e.active() and d < 110 and not e.is_boss:
                e.kx += (e.x - p.x) / max(d, 1) * 520
                e.ky += (e.y - p.y) / max(d, 1) * 520


def ebullet_dt(p, b, dt):
    if 'klingeling' in p.sgs and (b.x - p.x) ** 2 + (b.y - p.y) ** 2 < 40 ** 2:
        return dt * 0.55
    return dt


def on_dash(p, run):
    S = p.sgs
    if not S:
        return
    g = st(p)
    if 'tarnung' in S:
        g['invis'] = 1.3
    if 'iaido' in S:
        g['iaido'] = 1.2
    if 'schweiss' in S:
        g['schweiss'] = 1
    if 'rauch' in S:
        clouds = g.setdefault('clouds', [])
        clouds.append([p.x, p.y, 1.6])
        del clouds[:-4]
    if 'flatter' in S:
        for i in range(4):
            a = i / 4 * math.tau + math.pi / 4
            run.fire_player_bullet(p.x, p.y - 3, a, p.damage() * 0.7, p.s['shotspd'], 2.5, 0.7, {})


def on_coin(p, run, v):
    """Gibt zusätzliche Mon zurück."""
    S = p.sgs
    if not S:
        return 0
    g = st(p)
    extra = 0
    if 'fuchsglueck' in S and v == 1 and random.random() < 0.2:
        extra = 4
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
    g['parade'] = 0
    g['room_hit'] = False
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
    if 'opfergabe' in S and random.random() < 0.1 + 0.01 * luck:
        run.spawn_pickup('key', p.x, p.y - 20)
    if 'sternschnuppe' in S and random.random() < 0.08 + 0.006 * luck:
        run.random_drop(p.x + random.uniform(-30, 30), p.y - 24)
    if 'kraniche' in S and g.get('cranes', 0) < 10:
        g['cranes'] = g.get('cranes', 0) + 1
        if g['cranes'] == 10:
            run.banner('Tausend Kraniche', 'Der Wunsch ist gefaltet', (250, 240, 230))
    if 'anmut' in S and not g.get('room_hit'):
        g['anmut'] = min(1.0, g.get('anmut', 0) + 0.15)
        p.recalc()
    if 'gokaku' in S and run.time - getattr(run, 'room_enter_time', run.time) < 10:
        g['gokaku'] = min(5, g.get('gokaku', 0) + 1)


def on_floor(run):
    p = run.player
    S = p.sgs
    if not S:
        return
    g = st(p)
    g['kenko_used'] = False
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
        run.random_drop(pk.x, pk.y)


def on_salt(p, run):
    if 'reinigung' in p.sgs:
        p.heal(1)


def on_pot(run, x, y):
    """True: dieser Krug lässt sicher etwas fallen."""
    p = run.player
    if 'hausglueck' in p.sgs and not st(p).get('pot'):
        st(p)['pot'] = 1
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
            e.sg_touch = 1.5
        if 'oni_koenig' in S:
            run.damage_enemy(e, p.damage() * 1.5, None)
            e.sg_touch = 0.5
        if 'felsblock' in S and not e.is_boss:
            d = math.hypot(e.x - p.x, e.y - p.y) or 1
            e.kx += (e.x - p.x) / d * 380
            e.ky += (e.y - p.y) / d * 380
            e.sg_touch = 0.4
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
    for k in ('invis', 'iaido'):
        if g.get(k, 0) > 0:
            g[k] -= dt
    if p.moving:
        g['still'] = 0
    else:
        g['still'] = g.get('still', 0) + dt
    if 'statik' in S and p.moving:
        before = g.get('statik', 0)
        g['statik'] = min(3.0, before + dt)
        if g['statik'] >= 3.0 and random.random() < 0.3:
            from .entities import Particle
            run.particles.append(Particle(p.x + random.uniform(-6, 6), p.y - 6, 0, 0, 0.15, (255, 250, 160), 1))
    fighting = any(e.active() for e in run.enemies)
    for key, period in (('sternkugel', 1.4), ('kranichflug', 2.0), ('augenhand', 0.9), ('sonnenkraehe', 3.0),
                        ('fuchsregen', 3.5), ('schlangenschweif', 0.5), ('kichern', 1.0)):
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
                b = run.fire_player_bullet(ox, oy, math.atan2(tgt.y - oy, tgt.x - ox), dmg * 0.6, 240, 2.2, 1.0, {'homing': 1})
                b.col = (255, 240, 160)
        elif key == 'kranichflug':
            tgt = _nearest(run, p.x, p.y, 260)
            if tgt:
                b = run.fire_player_bullet(p.x, p.y - 8, math.atan2(tgt.y - p.y, tgt.x - p.x), dmg * 0.9, 170, 3.0, 1.6, {'homing': 1, 'pierce': 1})
                b.col = (250, 250, 255)
        elif key == 'augenhand':
            tgt = _nearest(run, p.x, p.y, 75)
            if tgt:
                b = run.fire_player_bullet(p.x, p.y - 3, math.atan2(tgt.y - p.y, tgt.x - p.x), dmg * 0.7, 260, 2.5, 0.5, {})
                b.col = (255, 140, 140)
        elif key == 'sonnenkraehe':
            tgt = _nearest(run, p.x, p.y, 300)
            if tgt:
                from .entities import Hazard
                run.hazards.append(Hazard(tgt.x, tgt.y, 12, 0.35, 0.12, dmg * 2.0, 'p', 'slam', (255, 200, 90)))
        elif key == 'fuchsregen':
            cand = [e for e in run.enemies if e.active()]
            if cand:
                e = random.choice(cand)
                from .entities import Hazard
                run.hazards.append(Hazard(e.x, e.y, 14, 0.3, 0.15, dmg * 1.5, 'p', 'water'))
        elif key == 'schlangenschweif':
            bx, by = p.x - p.facing[0] * 16, p.y - p.facing[1] * 16
            for e in run.enemies:
                if e.active() and math.hypot(e.x - bx, e.y - by) < 22 + e.r:
                    run.damage_enemy(e, dmg * 0.8, None)
                    e.poison = max(e.poison, 2.5)
                    e.poison_dps = max(e.poison_dps, 1.0)
                    run.zap(bx, by, e.x, e.y)
                    break
        elif key == 'kichern':
            for e in run.enemies:
                if e.active() and not e.is_boss and math.hypot(e.x - p.x, e.y - p.y) < 85 and random.random() < 0.2:
                    e.frozen = max(e.frozen, 0.45)
    if 'bannkreis' in S:
        for e in run.enemies:
            if e.active() and not e.is_boss:
                d = math.hypot(e.x - p.x, e.y - p.y)
                if d < 28 + e.r:
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
            if random.random() < 0.08:
                from .entities import Particle
                run.particles.append(Particle(w[0] + random.uniform(-10, 10), w[1] + random.uniform(-6, 6), 0, 0, 0.4, (230, 230, 240), 1))
        g['webs'] = [w for w in webs if w[2] > 0]
    clouds = g.get('clouds')
    if clouds:
        from .entities import Particle
        for c in clouds:
            c[2] -= dt
            if random.random() < 0.5:
                run.particles.append(Particle(c[0] + random.uniform(-14, 14), c[1] + random.uniform(-10, 10), 0, -6, 0.5, (150, 150, 160), 4))
        g['clouds'] = [c for c in clouds if c[2] > 0]


def dmg_mult(p):
    S = p.sgs
    if not S:
        return 1.0
    g = st(p)
    run = p.run
    m = 1.0
    if 'vergaenglich' in S:
        t = run.time - getattr(run, 'room_enter_time', run.time)
        if t < 10 and not run.room.cleared:
            m *= 1 + 0.4 * (1 - t / 10)
    if 'satt' in S and p.hp >= p.maxhp and p.maxhp > 0:
        m *= 1.2
    if 'ehre' in S and not getattr(p, 'hit_this_floor', False):
        m *= 1.25
    if 'lange_reise' in S:
        m *= 1 + 0.05 * max(0, run.depth - 1)
    if 'parade' in S:
        m *= 1 + 0.03 * g.get('parade', 0)
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
    if 'reichtum' in S and p.coins >= 50:
        m *= 1.15
    return m


def stat_bonus(p, f):
    """Dauerhafte, gesammelte Boni (Ema, Anmut) in die Werte-Summe einrechnen."""
    if not getattr(p, 'sg', None):
        return
    for k, v in p.sg.get('ema', {}).items():
        f[k] += v
    if f.get('sig_anmut'):
        f['rate'] += p.sg.get('anmut', 0)
