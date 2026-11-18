// Prolog „Die Nacht ohne Morgen“ als Schattenspiel.
// A (0–6,1): Blutmond über dem Dorf, Hitodama steigen auf, ein Oni tritt in die Lampe.
// B (6,1–13,2): Hyakki Yagyō zieht vorbei, Zähler bis 100; die Sonne versucht aufzugehen und sinkt zurück.
// C (13,2–18,4): Hana nimmt am Schrein die Glocke ihrer Großmutter und wendet sich dem Zug zu.
// D (18,4–22): Vorhang; Merksatz.
const DURATION = 22;
const T = {
  title: 0.15, titleLand: 0.8, hoist: 2.0, moonRed: 2.6, blood: 3.05,
  wisp0: 3.5, wispPlaque: 4.45, oniIn: 4.85, lamp0: 5.75, lamp1: 6.45, sceneB: 6.1,
  hyakki: 6.6, board: 6.9, count0: 7.3, count1: 10.6, sun0: 11.0, sunTag: 11.3, sunX: 11.95, sunSink: 12.1,
  dim0: 12.9, sceneC: 13.2, hanaIn: 13.5, hanaStop: 14.6, hanaPlaque: 14.75, reach: 15.0, grab: 15.55, bellPlaque: 15.75,
  ring2: 16.3, turn: 16.4, vine0: 16.9, vine1: 17.5, zugPlaque: 17.35, cur0: 18.0, cur1: 18.3, part0: 18.45, part1: 18.8,
  card: 18.5, cardLand: 18.85,
};
const WISPS = [[420, 0.0], [700, 0.35], [560, 0.7], [960, 0.95], [1100, 1.3], [820, 1.55], [330, 1.8]];
const ONI_STEPS = [];
for (let t = T.oniIn + 0.2; t < T.lamp0; t += 0.4) ONI_STEPS.push(t);
const count = (t) => Math.round(100 * EO(sm(T.count0, T.count1, t)));
const PAR = [
  { kind: 'oni', t0: 6.3, v: 150, s: 0.92 }, { kind: 'kasa', t0: 7.45, v: 150, s: 0.76 },
  { kind: 'chochin', t0: 8.5, v: 150, s: 0.78 }, { kind: 'rokuro', t0: 9.5, v: 150, s: 0.84 },
];
const parX = (c, t) => 1460 - c.v * (t - c.t0);
const RINGS = [15.55, 16.3, 17.05, 19.9, 20.9];
const ringSh = (t) => { let l = -99; RINGS.forEach((r) => { if (r <= t) l = r; }); return t - l; };
const HANA_X = (t) => lerp(1420, 490, EIO(sm(T.hanaIn, T.hanaStop, t)));
const VZ = [[560, 420], [700, 250], [900, 230], [1080, 470]];

function header(st, t) {
  const hp = EIO(sm(T.hoist, T.hoist + 0.5, t));
  const dropY = lerp(-260, 300, EO(sm(T.title, T.title + 0.65, t)));
  pup(st, {}, (p, g) => titleCard(p, g, {
    x: lerp(640, 238, hp), y: lerp(dropY, 86, hp), w: 820, h: 220, s: lerp(1, 0.5, hp),
    rot: swing(t, T.titleLand - 0.1, 0.08, 2.2, 7) + swing(t, T.hoist + 0.45, 0.05, 2.5, 8),
    lines: [{ text: 'Prolog', size: 58, y: -22, italic: true }, { text: 'Die Nacht ohne Morgen', size: 70, y: 56 }],
  }));
}

function sceneA(st, t) {
  const red = EIO(sm(T.moonRed, T.moonRed + 0.5, t));
  pup(st, {}, (p, g) => {
    const sw = Math.sin(t * 1.1) * 0.03;
    p.save(); p.translate(980, 0); p.rotate(sw); p.lineWidth = 2; p.beginPath(); p.moveTo(0, 0); p.lineTo(0, 118); p.stroke(); p.restore();
    moon(p, g, { x: 980 - Math.sin(sw) * 210, y: 220, r: 88, fill: 1, burst: 0, gel: H.rgba(H.mix([255, 246, 214], [236, 40, 30], red)) });
    [[840, 90, 13, 1.3], [1200, 120, 11, 0.9], [760, 200, 9, 1.7]].forEach(([x, y, r, f]) => {
      const a = Math.sin(t * f + x) * 0.06; p.save(); p.translate(x, 0); p.rotate(a); p.lineWidth = 1.6; p.beginPath(); p.moveTo(0, 0); p.lineTo(0, y - r); p.stroke(); star(p, 0, y, r); cut(p, () => dot(p, 0, y, r * 0.22)); p.restore();
    });
    if (t > T.blood) plaque(p, { x: 720, y: lerp(-60, 260, EO(sm(T.blood, T.blood + 0.25, t))), text: 'Blutmond', size: 40, rot: swing(t, T.blood + 0.25, 0.07, 3, 9), hang: 230 });
  });
  // Hitodama steigen aus den Dächern
  pup(st, {}, (p, g) => {
    WISPS.forEach(([x, d], i) => {
      const u = t - T.wisp0 - d; if (u <= 0) return;
      const y = 560 - 260 * EO(cl(u / 2.2)) - 12 * Math.sin(u * 3 + i), xx = x + 26 * Math.sin(u * 1.7 + i);
      hitodama(p, g, xx, y, 17 * Math.min(1, u * 3), -Math.PI / 2 - 0.5 * Math.sin(u * 2.4 + i) + (i % 2 ? 0.3 : -0.3), i % 3 ? 'rgb(110,196,255)' : 'rgb(120,240,170)');
    });
    if (t > T.wispPlaque) plaque(p, { x: 470, y: lerp(-60, 300, EO(sm(T.wispPlaque, T.wispPlaque + 0.25, t))), text: 'Hitodama', size: 40, rot: swing(t, T.wispPlaque + 0.25, 0.07, 3, 9), hang: 280 });
  });
  pup(st, {}, (p, g) => { village(p, g, { y: 620, flicker: 0.85 + 0.15 * NZ.n2(t * 5, 1) }); pine(p, 200, 620, 260, 30); });
  // Ein Oni stapft herein (dann hebt ihn der Spieler zur Lampe)
  if (t > T.oniIn && t < T.lamp0) {
    const u = sm(T.oniIn, T.lamp0, t);
    pup(st, {}, (p, g, rods) => oni(p, g, { x: lerp(1480, 1010, EO(u)), y: 664 - Math.abs(Math.sin((t - T.oniIn) * Math.PI / 0.4)) * 8, s: 0.9, dir: -1, step: (t - T.oniIn) * Math.PI / 0.4, arm: -0.5 + 0.12 * Math.sin(t * 4) }, rods));
  }
}
function oniToLamp(st, t) {
  const q = sm(T.lamp0, T.lamp1, t), s = lerp(0.9, 7.4, Math.pow(q, 1.2));
  const cx = lerp(1010, 640, EIO(sm(0, 0.5, q))) + 700 * sm(0.5, 1, q) * sm(0.5, 1, q), cy = lerp(664, 1000, EIO(sm(0, 0.5, q))) + 900 * sm(0.55, 1, q);
  toLamp(st, q, (p, g) => oni(p, g, { x: cx, y: cy, s, dir: -1, step: t * 9, arm: -1.2, noRods: true }));
}

function sceneB(st, t) {
  pup(st, {}, (p, g) => {
    moon(p, g, { x: 1130, y: 150, r: 54, fill: 1, burst: 0, gel: 'rgb(236,40,30)' });
    if (t > T.hyakki) {
      plaque(p, { x: 1000, y: lerp(-80, 150, EO(sm(T.hyakki, T.hyakki + 0.3, t))), text: 'Hyakki Yagyō', size: 48, rot: swing(t, T.hyakki + 0.3, 0.06, 3, 8), hang: 120 });
      if (t > T.hyakki + 0.35) plaque(p, { x: 1000, y: lerp(-80, 232, EO(sm(T.hyakki + 0.35, T.hyakki + 0.6, t))), text: 'Zug der hundert Dämonen', size: 30, rot: swing(t, T.hyakki + 0.6, 0.05, 3, 9), hang: 26 });
    }
  });
  // Zähler-Tafel
  if (t > T.board) {
    const dy = lerp(-300, 0, EO(sm(T.board, T.board + 0.35, t))), v = count(t), hit = t > T.count1 ? Math.exp(-(t - T.count1) * 6) : 0;
    pup(st, {}, (p) => {
      p.save(); p.translate(660, 214 + dy); p.rotate(swing(t, T.board + 0.35, 0.04, 2.5, 7));
      p.lineWidth = 2; p.beginPath(); p.moveTo(-170, 34); p.lineTo(-170, -260); p.moveTo(170, 34); p.lineTo(170, -260); p.stroke();
      p.fillRect(-176, 22, 352, 7); dot(p, -176, 25, 8); dot(p, 176, 25, 8);
      p.save(); p.translate(0, -12); p.scale(1 + hit * 0.22, 1 + hit * 0.22); p.font = `400 118px ${NF}`; p.textAlign = 'center'; p.textBaseline = 'alphabetic'; p.fillText(String(v), 0, 0); p.restore();
      p.restore();
      plaque(p, { x: 660, y: 262 + dy, text: 'Dämonen', size: 38 });
    });
  }
  // ferner Zug: kleine Yōkai, weiter vom Tuch weg (unscharf)
  if (t > 7.6) pup(st, { blur: 2.2, alpha: 0.9 }, (p) => {
    for (let j = 0; j < 22; j++) {
      const x = 1380 - 150 * (t - 7.6 - j * 0.32); if (x < -120 || x > 1400) continue;
      p.save(); p.translate(x, 600 - Math.abs(Math.sin((t + j) * 5)) * 6); p.scale(-0.42, 0.42); smallYokai(p, j % 4); p.restore();
    }
  });
  // Sonne versucht aufzugehen (links) und sinkt zurück
  if (t > T.sun0) {
    const up = EO(sm(T.sun0, T.sun0 + 0.8, t)) * (1 - EIO(sm(T.sunSink, T.sunSink + 0.7, t)));
    pup(st, {}, (p, g) => sun(p, g, 220, lerp(790, 600, up), 64, t * 0.6));
    if (t > T.sunTag) pup(st, {}, (p, g) => tag(p, g, {
      x: 250, y: 190, rot: swing(t, T.sunTag + 0.2, 0.12, 2.5, 8) + (t > T.sunX && t < T.sunX + 0.5 ? Math.sin((t - T.sunX) * 60) * 0.06 * (1 - (t - T.sunX) / 0.5) : 0),
      w: 260 * EO(sm(T.sunTag, T.sunTag + 0.2, t)), h: 80 * EO(sm(T.sunTag, T.sunTag + 0.2, t)), text: 'Morgen?', size: 48 * EO(sm(T.sunTag, T.sunTag + 0.2, t)), tx: -30,
      badge: t > T.sunX ? 'x' : null, badgeS: EO(sm(T.sunX, T.sunX + 0.14, t)) * 0.92,
    }));
  }
  // die vier großen Figuren des Zugs
  pup(st, {}, (p, g, rods) => {
    PAR.forEach((c) => {
      if (t < c.t0) return;
      const x = parX(c, t), ph = (t - c.t0) * Math.PI / 0.42;
      if (x < -300) return;
      if (c.kind === 'oni') oni(p, g, { x, y: 664 - Math.abs(Math.sin(ph)) * 8, s: c.s, dir: -1, step: ph, arm: -0.5 + 0.15 * Math.sin(t * 3) }, rods);
      else if (c.kind === 'kasa') kasa(p, g, { x, y: 664 - Math.abs(Math.sin(ph * 0.8)) * 36, s: c.s, dir: -1, look: [1, 0.2], wag: t * 5, blink: blinkAt(t, [9.2, 11.6]) }, rods);
      else if (c.kind === 'chochin') chochin(p, g, { x, y: 600 + Math.sin(t * 2.2) * 10, s: c.s, dir: -1, tilt: Math.sin(t * 1.8) * 0.05, look: [1, 0], wag: t * 4 }, rods);
      else rokuro(p, g, { x, y: 664 - Math.abs(Math.sin(ph)) * 4, s: c.s, dir: -1, neck: EIO(sm(10.4, 11.4, t)) * (1 - 0.1 * Math.sin(t * 2)) }, rods);
    });
  });
}

function sceneC(st, t) {
  let hook = [0, 0];
  pup(st, {}, (p, g) => { hook = shrine(p, g, { x: 230, y: 650, s: 1, t }); });
  pup(st, {}, (p, g) => torii(p, g, { x: 980, y: 652, s: 0.92 }));
  // ferner Zug hinter dem Torii (unscharf)
  pup(st, { blur: 2.6, alpha: 0.85 }, (p) => {
    for (let j = 0; j < 9; j++) {
      const x = 1360 - 70 * (t - T.sceneC - j * 0.9); if (x < 760 || x > 1400) continue;
      p.save(); p.translate(x, 588 - Math.abs(Math.sin((t + j) * 5)) * 4); p.scale(-0.3, 0.3); smallYokai(p, (j + 1) % 4); p.restore();
    }
  });
  const grabbed = t > T.grab;
  const turnU = sm(T.turn, T.turn + 0.4, t), dir = turnU < 0.5 ? -1 : 1, flip = Math.max(0.06, Math.abs(Math.cos(turnU * Math.PI)));
  const arm = t < T.grab ? -1.96 * EIO(sm(T.reach, T.grab, t)) : lerp(-1.96, -0.9, EIO(sm(T.grab + 0.3, T.grab + 0.65, t)));
  const walking = t < T.hanaStop, x = HANA_X(t);
  // Glocke hängt am Haken, bis Hana sie nimmt
  if (!grabbed) pup(st, {}, (p, g) => { p.lineWidth = 2; p.beginPath(); p.moveTo(hook[0], hook[1]); p.lineTo(hook[0], hook[1] + 12); p.stroke(); suzu(p, g, hook[0], hook[1] + 12, 0.62, Math.sin(t * 1.3) * 0.05, 0); });
  pup(st, {}, (p, g, rods) => hana(p, g, {
    x, y: 652 - (walking ? Math.abs(Math.sin((t - T.hanaIn) * 7)) * 6 : 0), s: 1.06 * flip, dir, step: walking ? (t - T.hanaIn) * 7 : 0,
    arm: dir < 0 ? arm : -0.9 + 0.08 * Math.sin(t * 3), bell: grabbed, sh: grabbed ? ringSh(t) : 9,
  }, rods));
  pup(st, {}, (p) => {
    if (t > T.hanaPlaque) plaque(p, { x: 620, y: lerp(-60, 240, EO(sm(T.hanaPlaque, T.hanaPlaque + 0.25, t))), text: 'Hana', size: 46, rot: swing(t, T.hanaPlaque + 0.25, 0.07, 3, 9), hang: 250 });
    if (t > T.bellPlaque) plaque(p, { x: 300, y: lerp(-60, 190, EO(sm(T.bellPlaque, T.bellPlaque + 0.25, t))), text: 'Großmutters Glocke', size: 36, rot: swing(t, T.bellPlaque + 0.25, 0.06, 3, 9), hang: 40 });
    vine(p, VZ, EIO(sm(T.vine0, T.vine1, t)), 7);
    if (t > T.zugPlaque) plaque(p, { x: 820, y: lerp(-60, 160, EO(sm(T.zugPlaque, T.zugPlaque + 0.25, t))), text: 'dem Zug entgegen', size: 38, rot: swing(t, T.zugPlaque + 0.25, 0.06, 3, 9), hang: 170 });
  });
}

function sceneD(st, t) {
  pup(st, { blur: 2.4, alpha: 0.85 }, (p) => {
    for (let j = 0; j < 12; j++) {
      const x = 1400 - 90 * (t - T.card - j * 0.7); if (x < -100 || x > 1400) continue;
      p.save(); p.translate(x, 606 - Math.abs(Math.sin((t + j) * 5)) * 4); p.scale(-0.34, 0.34); smallYokai(p, j % 4); p.restore();
    }
  });
  pup(st, {}, (p, g, rods) => {
    const ph = (t - T.card) * 6;
    hana(p, g, { x: lerp(120, 420, sm(T.card, DURATION, t)), y: 652 - Math.abs(Math.sin(ph)) * 5, s: 0.62, dir: 1, step: ph, arm: -1.1 + 0.1 * Math.sin(t * 4), bell: true, sh: ringSh(t) }, rods);
  });
  pup(st, {}, (p, g) => titleCard(p, g, {
    x: 640, y: lerp(-220, 300, EO(sm(T.card, T.cardLand, t))), w: 1000, h: 260, s: 1, rot: swing(t, T.cardLand, 0.05, 2.2, 6),
    lines: [{ text: 'Jemand musste', size: 72, y: -14 }, { text: 'dem Zug entgegengehen.', size: 72, y: 76, italic: true }],
  }));
}

function explainer(ctx, W, Hh, t) {
  const st = begin(W, Hh);
  let b = sm(0, 0.55, t) * (1 - 0.35 * Math.max(0, NZ.n2(t * 23, 3.3)) * (1 - sm(0.35, 0.7, t)));
  b *= 1 - 0.93 * Math.sin(Math.PI * cl((t - T.dim0) / 0.6));                    // Lampe herunter- und wieder hochgedreht
  b *= 1 - 0.18 * sm(T.sunSink, T.sunSink + 0.6, t) * (1 - sm(T.dim0, T.dim0 + 0.3, t));
  const flare = t > T.count1 && t < T.sun0 ? Math.exp(-(t - T.count1) * 3) * 0.3 : 0;
  lamp(ctx, W, Hh, t, b + flare * 0.3, flare);
  // Blutmond: rote Gelfolie vor der Lampe in Szene A/B
  const redGel = 0.35 * sm(T.moonRed, T.moonRed + 0.6, t) * (1 - sm(T.dim0, T.dim0 + 0.3, t));
  if (redGel > 0) { ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = `rgba(255,90,70,${redGel})`; ctx.fillRect(0, 0, W, Hh); ctx.restore(); }
  if (t < T.sceneB) sceneA(st, t); else if (t < T.sceneC) sceneB(st, t); else if (t < T.card - 0.15) sceneC(st, t); else sceneD(st, t);
  if (t > T.lamp0 && t < T.lamp1 + 0.1) oniToLamp(st, t);
  stage(st, t);
  if (t < T.sceneB) nearFern(st, t, -1, 0.82 * sm(0.3, 0.9, t)); else if (t < T.card) nearFern(st, t, 1, 0.82);
  if (t > T.titleLand - 0.7) header(st, t);
  const cover = EIO(sm(T.cur0, T.cur1, t)) * (1 - EIO(sm(T.part0, T.part1, t)));
  if (cover > 0.001) pup(st, {}, (p) => curtains(p, W, Hh, cover, t));
  end(ctx, st, t);
}

function scoreSound(k) {
  const D = DURATION;
  const gam = (t, n, g = 1, pan = 0, minor = false) => {
    const f = k.hz(n);
    k.tone(t, { f, dur: 1.9, gain: 0.13 * g, a: 0.002, pan, verb: 0.3, minor });
    k.tone(t, { f: f * 1.007, dur: 1.6, gain: 0.07 * g, a: 0.002, pan, verb: 0.3, minor });
    k.tone(t, { f: f * 2.01, dur: 0.55, gain: 0.04 * g, a: 0.002, pan, minor });
    if (f * 2.95 < 2500) k.tone(t, { f: f * 2.95, dur: 0.22, gain: 0.018 * g, a: 0.002, pan, minor });
    k.noise(t, { dur: 0.02, filter: 'bandpass', f: Math.min(2200, f * 1.6), q: 2, gain: 0.08 * g, pan, minor });
  };
  const gong = (t, g = 1) => {
    k.play('thud', t, { f: 90, gain: 0.7 * g });
    k.tone(t, { f: [[0, 98], [3.6, 95]], dur: 3.6, gain: 0.36 * g, a: 0.012, verb: 0.45 });
    k.tone(t, { f: [[0, 99.2], [3.2, 96]], dur: 3.2, gain: 0.16 * g, a: 0.02 });
    k.tone(t, { f: 202, dur: 2.2, gain: 0.1 * g, a: 0.01, verb: 0.4 });
    k.noise(t, { dur: 0.3, color: 'brown', filter: 'lowpass', f: 450, gain: 0.3 * g });
  };
  const tap = (t, f = 640, g = 0.55, pan = 0, minor = true) => { k.play('tock', t, { f, gain: g, pan, minor }); k.noise(t, { dur: 0.014, filter: 'bandpass', f: 1700, q: 2.5, gain: 0.32 * g, a: 0.001, pan, minor }); };
  const hyoshigi = (t, g = 1) => { tap(t, 1500, 1.1 * g, -0.1, false); k.noise(t, { dur: 0.03, filter: 'bandpass', f: 2600, q: 3, gain: 0.4 * g, a: 0.001 }); };
  const taiko = (t, g = 1, pan = 0) => { k.play('thud', t, { f: 78, gain: 0.55 * g, pan }); k.noise(t, { dur: 0.08, filter: 'bandpass', f: 420, q: 1.2, gain: 0.18 * g, pan }); };
  const hide = (t, dur, g = 0.5, pan = 0, minor = true) => k.play('paper', t, { dur, gain: g, pan, minor });
  const slide = (t, dur, g = 0.12, minor = true) => k.noise(t, { dur, color: 'brown', filter: 'lowpass', f: [[0, 260], [dur * 0.5, 520], [dur, 240]], gain: g, a: dur * 0.4, minor });
  const suzuJ = (t, g = 1, pan = 0) => { const r = ['E6', 'G6', 'B6', 'D7', 'E7']; for (let i = 0; i < 6; i++) { const f = k.hz(r[(i * 3) % 5]); k.tone(t + i * 0.035, { f, dur: 0.5, gain: 0.05 * g, a: 0.002, verb: 0.35, pan }); k.tone(t + i * 0.035, { f: f * 2.4, dur: 0.15, gain: 0.015 * g, a: 0.001, pan }); } k.noise(t, { dur: 0.25, filter: 'highpass', f: 6000, gain: 0.05 * g, a: 0.01, pan }); };
  const wisp = (t, n, pan) => k.tone(t, { f: [[0, k.hz(n) * 0.98], [0.9, k.hz(n) * 1.03]], dur: 1.1, gain: 0.05, a: 0.3, verb: 0.5, pan, minor: true });

  k.bed('hum', 0.2, D, { gain: 0.5 });
  k.bed('room', 0, D, { gain: 0.7 });
  k.noise(0.3, { dur: 12, color: 'pink', filter: 'bandpass', f: 380, q: 0.6, gain: 0.03, a: 2, hold: 8, bus: 'amb' });   // Nachtwind
  // Hyōshigi: das Klappern, mit dem das Spiel beginnt
  hyoshigi(0.05); hyoshigi(0.3, 0.9);
  k.noise(0.06, { dur: 0.45, color: 'brown', filter: 'lowpass', f: [[0, 200], [0.12, 700], [0.45, 180]], gain: 0.35, a: 0.05 });
  [0.2, 0.36, 0.5].forEach((t, i) => k.noise(t, { dur: 0.012, filter: 'bandpass', f: 1300 + i * 300, q: 1.5, gain: 0.12, minor: true }));
  // Titel fällt an seinen Schnüren
  hide(T.title + 0.05, 0.3, 0.7); tap(T.titleLand - 0.02, 520, 0.7, 0, false); gam(T.titleLand, 'D4', 1.0);
  slide(T.hoist, 0.55, 0.14); tap(T.hoist + 0.48, 700, 0.45, -0.5);
  // Blutmond
  k.tone(T.moonRed, { f: 'D2', dur: 2.2, gain: 0.14, a: 0.6, verb: 0.4 }); k.tone(T.moonRed, { f: 'Eb2', dur: 2.0, gain: 0.07, a: 0.7 });
  k.noise(T.moonRed, { dur: 0.25, filter: 'highpass', f: 1200, gain: 0.07, a: 0.08 });
  tap(T.blood + 0.24, 820, 0.6, 0.2); gam(T.blood + 0.28, 'Eb4', 0.55, 0.2, true);
  WISPS.forEach(([x, d], i) => wisp(T.wisp0 + d, ['A5', 'D6', 'F5', 'C6', 'A5', 'E6', 'G5'][i], (x - 640) / 700));
  tap(T.wispPlaque + 0.24, 780, 0.55, -0.3);
  // Oni stapft herein
  hide(T.oniIn, 0.4, 0.5, 0.8);
  ONI_STEPS.forEach((t, i) => taiko(t, 0.7 + i * 0.05, 0.6));
  // Szenenwechsel: der Oni wird zur Lampe gehoben, sein Schatten füllt die Leinwand
  k.noise(T.lamp0 + 0.05, { dur: 0.75, color: 'pink', filter: 'bandpass', f: [[0, 180], [0.35, 800], [0.75, 160]], q: 0.8, gain: 0.42, a: 0.3, verb: 0.2 });
  taiko(6.05, 1.2); k.play('thud', 6.08, { f: 60, gain: 0.4 });
  // Hyakki Yagyō
  tap(T.hyakki + 0.28, 840, 0.6, 0.5); tap(T.hyakki + 0.58, 900, 0.45, 0.5);
  hide(T.board, 0.3, 0.35, -0.1); tap(T.board + 0.33, 760, 0.45, -0.1);
  for (let t = 6.3 + 0.21; t < T.sceneC; t += 0.42) taiko(t, 0.5, 0.2 - (t - 6.3) * 0.08);     // Schritte des Oni
  for (let t = 7.45; t < T.sceneC; t += 0.525) tap(t, 460, 0.35, 0.6 - (t - 7) * 0.12);             // Geta des Schirms
  k.noise(8.5, { dur: 4.4, color: 'pink', filter: 'bandpass', f: 1100, q: 3, gain: 0.02, a: 1, hold: 3, bus: 'amb', pan: 0.3 });  // Knarren der Laterne
  k.tone(10.4, { f: [[0, 'C5'], [1.0, 'G5']], type: 'triangle', dur: 1.0, gain: 0.03, a: 0.5, verb: 0.3, minor: true });          // der Hals streckt sich
  { let last = -1, prev = count(T.count0); for (let t = T.count0; t < T.count1 - 0.02; t += 0.002) { const v = count(t); if (v !== prev && t - last >= 0.09) { tap(t, 1150, 0.34, -0.15); last = t; } prev = v; } }
  gong(T.count1, 1.0); taiko(T.count1, 1.3);
  // die Sonne versucht es
  k.tone(T.sun0, { f: [[0, 'D4'], [0.8, 'A4']], type: 'triangle', dur: 0.9, gain: 0.06, a: 0.4, verb: 0.3 });
  hide(T.sunTag, 0.2, 0.4, -0.5); tap(T.sunTag + 0.2, 600, 0.55, -0.5, false);
  gam(T.sunX, 'Eb4', 0.8, -0.4); gam(T.sunX, 'E4', 0.7, -0.4); gam(T.sunX, 'A2', 0.9, 0);
  k.tone(T.sunSink, { f: [[0, 'A4'], [0.7, 'D3']], type: 'triangle', dur: 0.8, gain: 0.06, a: 0.05 });
  // Lampe herunter- und hochgedreht
  k.noise(T.dim0, { dur: 0.6, color: 'brown', filter: 'lowpass', f: [[0, 600], [0.3, 140], [0.6, 600]], gain: 0.35, a: 0.05, hold: 0.35 });
  // Hana
  for (let t = T.hanaIn + 0.05; t < T.hanaStop; t += Math.PI / 7) tap(t, 980, 0.3, 0.5 - (t - T.hanaIn) * 0.8);
  hide(T.hanaIn, 0.4, 0.45, 0.8);
  tap(T.hanaPlaque + 0.24, 820, 0.6, 0); gam(T.hanaPlaque + 0.26, 'A4', 0.5, 0, true);
  hide(T.reach, 0.45, 0.35, -0.2);
  suzuJ(RINGS[0], 1.2, -0.3); suzuJ(RINGS[1], 0.8, -0.2); suzuJ(RINGS[2], 0.7, 0);
  tap(T.bellPlaque + 0.24, 760, 0.55, -0.5);
  hide(T.turn, 0.35, 0.6, 0);
  k.play('stroke', T.vine0, { material: 'brush', dur: T.vine1 - T.vine0, gain: 0.9, minor: true });
  tap(T.zugPlaque + 0.24, 860, 0.6, 0.3);
  // Vorhang schließt und öffnet sich
  for (const pan of [-0.7, 0.7]) k.noise(T.cur0, { dur: 0.32, color: 'pink', filter: 'bandpass', f: [[0, 500], [0.2, 1500], [0.32, 700]], q: 0.7, gain: 0.25, a: 0.12, pan });
  k.play('thud', T.cur1, { f: 110, gain: 0.3 });
  for (const pan of [-0.7, 0.7]) k.noise(T.part0, { dur: 0.36, color: 'pink', filter: 'bandpass', f: [[0, 700], [0.2, 1500], [0.36, 500]], q: 0.7, gain: 0.22, a: 0.12, pan });
  // Merksatz: auflösende Bronze-Phrase, dazu die Glocke der Wanderin
  tap(T.cardLand, 520, 1.0, 0, false);
  gam(T.cardLand + 0.12, 'D4', 0.9, -0.2); gam(T.cardLand + 0.26, 'A4', 0.85, 0); gam(T.cardLand + 0.4, 'D5', 0.8, 0.2);
  k.tone(T.cardLand + 0.12, { f: 'D3', dur: 2.4, gain: 0.12, a: 0.01, verb: 0.4 });
  [RINGS[3], RINGS[4]].forEach((t) => suzuJ(t, 0.55, -0.4));
  hyoshigi(21.45, 0.8); hyoshigi(21.62, 0.7);
}
