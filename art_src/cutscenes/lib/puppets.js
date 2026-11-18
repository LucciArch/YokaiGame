// puppets.js – Schattenspielfiguren für „Yōkai no Michi“. Jede Figur: fn(p, g, o, rods), p = Silhouetten-Ebene,
// g = Gelfolien-Ebene. Gezeichnet nach rechts blickend; o.dir = -1 dreht die Figur um (wie ein gewendeter Scherenschnitt).
function pose(p, g, o) {
  both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.tilt || 0); c.scale((o.dir || 1) * o.s, o.s); });
  p.fillStyle = INK; p.strokeStyle = INK;
}
const unpose = (p, g) => both([p, g], (c) => c.restore());

// ---------- Oni mit Kanabō (Füße bei 0, ~340 hoch) ----------
// o: step (Gangphase), arm (Schulterwinkel), head
function oni(p, g, o, rods) {
  pose(p, g, o);
  const st = o.step || 0;
  for (const [hx, ph] of [[-26, Math.PI], [26, 0]]) {
    const a = Math.sin(st + ph) * 0.38;
    both([p, g], (c) => { c.save(); c.translate(hx, -118); c.rotate(a); });
    p.beginPath(); p.moveTo(-21, 0); p.quadraticCurveTo(-28, 60, -15, 102); p.lineTo(15, 102); p.quadraticCurveTo(24, 50, 21, 0); p.closePath(); p.fill();
    p.beginPath(); p.ellipse(10, 110, 27, 11, 0, 0, TAU); p.fill();
    [0, 1, 2].forEach((k) => tear(p, 30, 110 - k * 4, 16, 6, 0.25 - k * 0.3));
    cut(p, () => { for (let k = 0; k < 4; k++) tear(p, -6 + (k % 2) * 8, 26 + k * 18, 12, 4, Math.PI / 2 + 0.3); });
    pin(p, 0, 0, 8);
    both([p, g], (c) => c.restore());
  }
  // Rumpf mit Buckel und Bauch
  p.beginPath(); p.moveTo(-62, -118); p.bezierCurveTo(-86, -200, -74, -262, -32, -284); p.lineTo(42, -286); p.bezierCurveTo(88, -264, 88, -190, 62, -118); p.closePath(); p.fill();
  p.beginPath(); p.ellipse(6, -170, 66, 58, 0, 0, TAU); p.fill();
  cut(p, () => {
    p.lineWidth = 3; p.beginPath(); p.arc(-18, -244, 24, 0.3, 2.6); p.stroke(); p.beginPath(); p.arc(34, -244, 24, 0.5, 2.8); p.stroke();
    dot(p, 6, -158, 4.5);
    for (let k = 0; k < 6; k++) tear(p, -40 + k * 17, -206, 12, 5, Math.PI / 2);
    for (let k = 0; k < 14; k++) { const a = Math.PI * (0.15 + 0.7 * k / 13); dot(p, 6 + Math.cos(a) * 52, -170 + Math.sin(a) * 40, 2.2); }
  });
  // Tigerfell-Lendenschurz (gelbe Gelfolie in den Streifen)
  p.beginPath(); p.moveTo(-68, -140); p.lineTo(72, -140); p.lineTo(64, -96); p.lineTo(32, -82); p.lineTo(6, -100); p.lineTo(-22, -80); p.lineTo(-62, -96); p.closePath(); p.fill();
  cut(p, () => { for (let k = 0; k < 6; k++) { const x = -54 + k * 22; p.beginPath(); p.moveTo(x, -134); p.lineTo(x + 13, -134); p.lineTo(x + 4, -100); p.closePath(); p.fill(); } });
  g.fillStyle = 'rgb(244,176,52)'; g.beginPath(); g.moveTo(-66, -138); g.lineTo(70, -138); g.lineTo(62, -98); g.lineTo(-60, -98); g.closePath(); g.fill();
  // Kopf
  both([p, g], (c) => { c.save(); c.translate(12, -284); c.rotate(o.head || 0); });
  p.beginPath(); p.ellipse(8, -40, 46, 44, 0, 0, TAU); p.fill();
  p.beginPath(); p.moveTo(18, -30); p.lineTo(64, -26); p.lineTo(54, -2); p.lineTo(8, -6); p.closePath(); p.fill();
  tear(p, -4, -74, 50, 22, -1.95); tear(p, 28, -76, 56, 24, -1.18);
  for (let k = 0; k < 10; k++) tear(p, -28, -66 + k * 8, 40 + ((k * 7) % 5) * 5, 12, Math.PI - 1.0 + k * 0.17);
  const eye = () => { p.beginPath(); p.moveTo(22, -54); p.lineTo(46, -46); p.lineTo(26, -38); p.closePath(); };
  const mouth = () => { p.beginPath(); p.moveTo(24, -20); p.lineTo(60, -18); p.lineTo(54, -8); p.lineTo(48, -15); p.lineTo(42, -7); p.lineTo(36, -15); p.lineTo(30, -8); p.closePath(); };
  cut(p, () => { eye(); p.fill(); mouth(); p.fill(); for (let k = 0; k < 6; k++) dot(p, -14 + k * 8, -78 + Math.abs(k - 2.5) * 2, 2); });
  g.fillStyle = 'rgb(255,214,70)'; g.beginPath(); g.ellipse(34, -46, 16, 10, 0.2, 0, TAU); g.fill();
  g.fillStyle = 'rgb(222,40,30)'; g.fillRect(22, -22, 40, 16);
  pin(p, 0, 0, 7);
  both([p, g], (c) => c.restore());
  // Arm mit Kanabō, an der Schulter gestiftet
  both([p, g], (c) => { c.save(); c.translate(52, -252); c.rotate(o.arm == null ? -0.5 : o.arm); });
  p.beginPath(); p.moveTo(-16, -10); p.quadraticCurveTo(40, -2, 70, 40); p.lineTo(98, 84); p.lineTo(78, 98); p.lineTo(50, 60); p.quadraticCurveTo(20, 32, -14, 20); p.closePath(); p.fill();
  dot(p, 90, 94, 19);
  both([p, g], (c) => { c.save(); c.translate(90, 94); c.rotate(-1.75); });
  p.beginPath(); p.moveTo(-30, -8); p.lineTo(210, -19); p.quadraticCurveTo(222, 0, 210, 19); p.lineTo(-30, 8); p.closePath(); p.fill();
  for (let k = 0; k < 8; k++) { const x = 50 + k * 22, h = 12 + x * 0.045; for (const sd of [-1, 1]) { p.beginPath(); p.moveTo(x - 5, sd * h); p.lineTo(x, sd * (h + 11)); p.lineTo(x + 5, sd * h); p.fill(); } }
  cut(p, () => { for (let k = 0; k < 8; k++) dot(p, 52 + k * 22, 0, 3); p.lineWidth = 2; p.beginPath(); p.moveTo(-20, 0); p.lineTo(30, 0); p.stroke(); });
  both([p, g], (c) => c.restore());
  pin(p, 0, 0, 9);
  if (rods && !o.noRods) rods.push([...wpt(p, 90, 94), 3.4]);
  both([p, g], (c) => c.restore());
  if (rods && !o.noRods) rods.push([...wpt(p, 0, -150), 3.6]);
  unpose(p, g);
}

// ---------- Kasa-obake: Schirm auf einem Bein, ein Auge, lange Zunge (Füße bei 0, ~350 hoch) ----------
function kasa(p, g, o, rods) {
  pose(p, g, o);
  p.fillRect(-6, -156, 12, 136);
  p.beginPath(); p.roundRect(-36, -26, 72, 12, 4); p.fill(); p.fillRect(-28, -14, 9, 14); p.fillRect(19, -14, 9, 14);
  cut(p, () => { p.lineWidth = 2; for (let y = -140; y < -40; y += 14) { p.beginPath(); p.moveTo(-3, y); p.lineTo(3, y + 6); p.stroke(); } });
  p.beginPath(); p.moveTo(0, -336); p.lineTo(124, -154);
  for (let k = 0; k < 8; k++) { const x0 = 124 - k * 31; p.quadraticCurveTo(x0 - 15.5, -130, x0 - 31, -154); }
  p.closePath(); p.fill();
  dot(p, 0, -338, 9); p.fillRect(-3, -362, 6, 26);
  cut(p, () => {
    p.lineWidth = 3.2; for (let k = -3; k <= 3; k++) { if (!k) continue; p.beginPath(); p.moveTo(k * 4, -314); p.lineTo(k * 36, -164); p.stroke(); }
    for (let k = -3; k < 3; k++) for (let j = 2; j < 6; j++) { const u = j / 6; if (Math.abs((k * 36 + 18) * u - 8) < 40 && Math.abs(-336 + 180 * u + 236) < 40) continue; dot(p, (k * 36 + 18) * u, -336 + 182 * u, 2.4); }
    dot(p, 8, -236, 27);
    p.beginPath(); p.ellipse(14, -188, 30, 8, 0.05, 0, TAU); p.fill();
  });
  g.fillStyle = 'rgb(250,226,120)'; dot(g, 8, -236, 29);
  g.fillStyle = 'rgb(222,40,40)'; g.beginPath(); g.ellipse(14, -188, 32, 10, 0, 0, TAU); g.fill();
  const lk = o.look || [0, 0];
  p.fillStyle = INK; dot(p, 8 + lk[0] * 9, -236 + lk[1] * 9, 11);
  cut(p, () => dot(p, 12 + lk[0] * 9, -240 + lk[1] * 9, 3.4));
  if (o.blink) { p.save(); p.beginPath(); p.arc(8, -236, 28, 0, TAU); p.clip(); p.fillRect(-22, -266, 60, 60 * o.blink); p.restore(); }
  tear(p, 30, -186, 96, 26, 1.25 + Math.sin(o.wag || 0) * 0.12);
  cut(p, () => { p.lineWidth = 2; p.beginPath(); p.moveTo(34, -176); p.lineTo(34 + Math.cos(1.25) * 70, -186 + Math.sin(1.25) * 70); p.stroke(); });
  if (rods && !o.noRods) rods.push([...wpt(p, 0, -60), 3.2]);
  unpose(p, g);
}

// ---------- Chōchin-obake: aufgerissene Papierlaterne an einer Stange ----------
function chochin(p, g, o, rods) {
  pose(p, g, o);
  const cy = -170;
  p.lineWidth = 7; p.lineCap = 'round'; p.beginPath(); p.moveTo(-120, -306); p.lineTo(130, -318); p.stroke();
  p.lineWidth = 3; p.beginPath(); p.moveTo(0, -312); p.lineTo(0, -280); p.stroke(); dot(p, 0, -312, 6);
  p.beginPath(); p.roundRect(-48, -282, 96, 22, 6); p.fill();
  p.beginPath(); p.roundRect(-48, -72, 96, 22, 6); p.fill();
  p.beginPath(); p.ellipse(0, cy, 84, 104, 0, 0, TAU); p.fill();
  const mouth = () => { p.beginPath(); p.moveTo(-74, cy + 4); p.lineTo(-40, cy - 10); p.lineTo(-20, cy + 2); p.lineTo(6, cy - 14); p.lineTo(30, cy); p.lineTo(52, cy - 16); p.lineTo(80, cy - 4); p.lineTo(70, cy + 22); p.lineTo(44, cy + 30); p.lineTo(18, cy + 18); p.lineTo(-10, cy + 30); p.lineTo(-40, cy + 22); p.closePath(); };
  cut(p, () => {
    for (let k = -4; k <= 4; k++) {
      const y = cy + k * 21, hw = 84 * Math.sqrt(Math.max(0, 1 - Math.pow((k * 21) / 104, 2))) - 12;
      if (Math.abs(k) <= 1) continue;
      p.fillRect(-hw, y - 2.5, hw * 2, 5);
    }
    mouth(); p.fill();
    p.beginPath(); p.ellipse(28, cy - 52, 20, 15, 0.1, 0, TAU); p.fill();
  });
  g.fillStyle = 'rgb(255,186,84)'; g.beginPath(); g.ellipse(0, cy, 84, 104, 0, 0, TAU); g.fill();
  g.fillStyle = 'rgb(230,50,36)'; g.save(); g.beginPath(); g.ellipse(0, cy + 8, 80, 26, 0, 0, TAU); g.fill(); g.restore();
  p.fillStyle = INK; const lk = o.look || [0, 0]; dot(p, 28 + lk[0] * 8, cy - 52 + lk[1] * 6, 8);
  tear(p, -6, cy + 22, 120, 30, 1.85 + Math.sin(o.wag || 0) * 0.15);
  cut(p, () => { p.lineWidth = 2; p.beginPath(); p.moveTo(-8, cy + 34); p.lineTo(-8 + Math.cos(1.85) * 90, cy + 22 + Math.sin(1.85) * 90); p.stroke(); });
  if (rods && !o.noRods) rods.push([...wpt(p, 110, -317), 3.2]);
  unpose(p, g);
}

// ---------- Rokurokubi: Frau im Kimono, deren Hals sich weit herauswindet ----------
function rokuro(p, g, o, rods) {
  pose(p, g, o);
  const nk = o.neck || 0;
  p.beginPath(); p.moveTo(-72, 0); p.lineTo(76, 0); p.lineTo(50, -182); p.quadraticCurveTo(10, -208, -30, -184); p.closePath(); p.fill();
  p.beginPath(); p.moveTo(-26, -172); p.lineTo(-90, -150); p.lineTo(-96, -54); p.lineTo(-40, -64); p.closePath(); p.fill();
  p.fillRect(-58, -122, 118, 32);
  cut(p, () => {
    for (const [x, y] of [[-34, -36], [22, -58], [44, -20], [-4, -150], [-64, -110]]) { for (let k = 0; k < 8; k++) tear(p, x, y, 13, 5, k * TAU / 8); }
    for (let x = -48; x < 54; x += 16) { p.save(); p.translate(x, -106); p.rotate(Math.PI / 4); p.fillRect(-4.5, -4.5, 9, 9); p.restore(); }
  });
  g.fillStyle = 'rgb(160,110,210)'; g.beginPath(); g.moveTo(-70, -2); g.lineTo(74, -2); g.lineTo(48, -180); g.lineTo(-28, -182); g.closePath(); g.fill();
  g.beginPath(); g.moveTo(-28, -170); g.lineTo(-88, -148); g.lineTo(-94, -56); g.lineTo(-40, -66); g.closePath(); g.fill();
  g.fillStyle = 'rgb(244,192,80)'; g.fillRect(-58, -122, 118, 32);
  const P = [[10, -198], [90 + 40 * nk, -280 - 120 * nk], [-40 - 90 * nk, -330 - 200 * nk], [lerp(36, 170, nk), lerp(-250, -430, nk)]];
  p.lineCap = 'round'; p.lineWidth = 18; p.beginPath();
  for (let i = 0; i <= 40; i++) { const q = bz(P, i / 40); if (i) p.lineTo(q[0], q[1]); else p.moveTo(q[0], q[1]); }
  p.stroke();
  cut(p, () => { for (let i = 3; i < 38; i += 3) { const q = bz(P, i / 40); dot(p, q[0], q[1], 2.2); } });
  const [hx, hy] = P[3];
  p.fillStyle = INK;
  p.beginPath(); p.ellipse(hx + 4, hy, 26, 30, 0, 0, TAU); p.fill();
  p.beginPath(); p.ellipse(hx - 10, hy - 32, 32, 20, 0, 0, TAU); p.fill();
  p.beginPath(); p.ellipse(hx - 30, hy - 8, 18, 26, 0, 0, TAU); p.fill();
  p.lineWidth = 3; for (const a of [-2.4, -1.9, -0.9]) { p.beginPath(); p.moveTo(hx - 10, hy - 34); p.lineTo(hx - 10 + Math.cos(a) * 52, hy - 34 + Math.sin(a) * 40); p.stroke(); dot(p, hx - 10 + Math.cos(a) * 52, hy - 34 + Math.sin(a) * 40, 4); }
  cut(p, () => { p.lineWidth = 2.6; p.beginPath(); p.arc(hx + 16, hy - 6, 7, 0.2, 2.9); p.stroke(); p.beginPath(); p.arc(hx + 16, hy + 14, 6, 0.4, 2.7); p.stroke(); dot(p, hx - 10, hy - 32, 4); });
  if (rods && !o.noRods) { rods.push([...wpt(p, 0, -80), 3.4]); rods.push([...wpt(p, hx, hy + 20), 2.4, 0.8]); }
  unpose(p, g);
}

// ---------- kleine Yōkai für den fernen Zug (ohne Gelfolie, für Unschärfe) ----------
function smallYokai(p, kind) {
  p.fillStyle = INK; p.strokeStyle = INK;
  if (kind === 0) { // Teekessel auf Beinen (Tsukumogami)
    p.beginPath(); p.ellipse(0, -60, 50, 38, 0, 0, TAU); p.fill(); p.fillRect(-14, -110, 28, 16);
    p.lineWidth = 6; p.beginPath(); p.arc(0, -96, 34, Math.PI, 0); p.stroke();
    p.beginPath(); p.moveTo(44, -64); p.lineTo(84, -88); p.lineTo(86, -78); p.lineTo(48, -48); p.fill();
    p.lineWidth = 7; p.beginPath(); p.moveTo(-20, -26); p.lineTo(-30, 0); p.moveTo(20, -26); p.lineTo(28, 0); p.stroke();
    cut(p, () => dot(p, 18, -66, 6));
  } else if (kind === 1) { // kleiner Oni
    p.beginPath(); p.ellipse(0, -60, 30, 44, 0, 0, TAU); p.fill(); dot(p, 6, -116, 24);
    tear(p, -4, -134, 22, 10, -1.9); tear(p, 14, -134, 24, 10, -1.2);
    p.lineWidth = 9; p.beginPath(); p.moveTo(-10, -20); p.lineTo(-18, 0); p.moveTo(12, -20); p.lineTo(18, 0); p.stroke();
    p.lineWidth = 7; p.beginPath(); p.moveTo(20, -80); p.lineTo(70, -140); p.stroke();
    cut(p, () => dot(p, 16, -118, 4));
  } else if (kind === 2) { // Kasa
    p.beginPath(); p.moveTo(0, -150); p.lineTo(60, -60); p.lineTo(-60, -60); p.closePath(); p.fill(); p.fillRect(-4, -64, 8, 60);
    p.fillRect(-18, -8, 36, 8); cut(p, () => dot(p, 4, -98, 9));
  } else { // Biwa-Laute auf Beinen
    p.beginPath(); p.ellipse(0, -62, 36, 48, 0.3, 0, TAU); p.fill();
    p.lineWidth = 9; p.beginPath(); p.moveTo(12, -100); p.lineTo(40, -160); p.stroke(); dot(p, 44, -166, 10);
    p.lineWidth = 6; p.beginPath(); p.moveTo(-10, -18); p.lineTo(-18, 0); p.moveTo(14, -18); p.lineTo(20, 0); p.stroke();
    cut(p, () => { p.beginPath(); p.arc(-4, -58, 9, 0.5, 2.6); p.fill(); });
  }
}

// ---------- Hitodama: Seelenflamme mit Schweif ----------
function hitodama(p, g, x, y, r, a, gel) {
  p.fillStyle = INK; tear(p, x, y, r * 4.2, r * 2, a);
  cut(p, () => { dot(p, x, y, r * 0.62); tear(p, x, y, r * 2.4, r * 0.7, a); });
  g.fillStyle = gel; dot(g, x, y, r * 0.7); tear(g, x, y, r * 2.6, r * 0.9, a);
}

// ---------- Dorf mit Strohdächern, Feuerturm, Kiefer (Grundlinie y) ----------
const HOUSES = [[300, 150, 96, 92], [478, 120, 84, 80], [640, 170, 104, 100], [860, 130, 90, 86], [1040, 160, 96, 96], [1210, 130, 80, 84]];
function village(p, g, o) {
  const y0 = o.y, fl = o.flicker || 1;
  p.fillStyle = INK; p.strokeStyle = INK;
  HOUSES.forEach(([x, w, h, rh], i) => {
    if (o.only && !o.only.includes(i)) return;
    p.fillRect(x, y0 - h, w, h);
    p.beginPath(); p.moveTo(x - 18, y0 - h + 6); p.lineTo(x + w + 18, y0 - h + 6); p.lineTo(x + w * 0.74, y0 - h - rh); p.lineTo(x + w * 0.26, y0 - h - rh); p.closePath(); p.fill();
    p.fillRect(x + w * 0.2, y0 - h - rh - 12, w * 0.6, 14);
    const wx = x + w * 0.3, wy = y0 - h * 0.78, ww = w * 0.3, wh = h * 0.42;
    cut(p, () => {
      p.fillRect(wx, wy, ww, wh);
      for (let k = 0; k < 5; k++) { p.save(); p.translate(x + w * (0.25 + k * 0.125), y0 - h - rh - 5); p.rotate(Math.PI / 4); p.fillRect(-3, -3, 6, 6); p.restore(); }
      p.lineWidth = 1.6; for (let k = 1; k < 6; k++) { p.beginPath(); p.moveTo(x - 10 + k * (w + 20) / 6, y0 - h + 2); p.lineTo(x + w * 0.26 + k * w * 0.48 / 6, y0 - h - rh + 4); p.stroke(); }
    });
    p.fillStyle = INK; for (let k = 1; k < 3; k++) p.fillRect(wx + ww * k / 3 - 1.5, wy, 3, wh);
    p.fillRect(wx, wy + wh / 2 - 1.5, ww, 3);
    const lit = i % 3 !== 1;
    g.fillStyle = lit ? H.rgba([255, 196 * fl, 90 * fl]) : 'rgb(120,110,140)'; g.fillRect(wx - 2, wy - 2, ww + 4, wh + 4);
  });
  // Feuerturm (Hinomi-yagura) mit Glocke
  if (!o.only) {
    const tx = 1150, th = 250;
    p.lineWidth = 7; p.beginPath(); p.moveTo(tx - 30, y0); p.lineTo(tx - 16, y0 - th); p.moveTo(tx + 30, y0); p.lineTo(tx + 16, y0 - th); p.stroke();
    p.lineWidth = 3; for (let k = 1; k < 7; k++) { const y = y0 - k * th / 7; p.beginPath(); p.moveTo(tx - 30 + k * 2, y); p.lineTo(tx + 30 - k * 2, y); p.stroke(); }
    p.beginPath(); p.moveTo(tx - 40, y0 - th); p.lineTo(tx + 40, y0 - th); p.lineTo(tx, y0 - th - 40); p.closePath(); p.fill();
    p.beginPath(); p.ellipse(tx, y0 - th + 22, 10, 14, 0, 0, TAU); p.fill();
  }
}

// ---------- Kiefer aus Tropfen-Nadelbüscheln ----------
function pine(p, x, y, h, lean) {
  p.fillStyle = INK; p.strokeStyle = INK; p.lineCap = 'round';
  const P = [[x, y], [x + lean * 0.3, y - h * 0.4], [x - lean * 0.2, y - h * 0.7], [x + lean, y - h]];
  for (let i = 0; i < 30; i++) { const a = bz(P, i / 30), b = bz(P, (i + 1) / 30); p.lineWidth = lerp(h * 0.07, h * 0.02, i / 30); p.beginPath(); p.moveTo(a[0], a[1]); p.lineTo(b[0], b[1]); p.stroke(); }
  [[0.45, -1], [0.62, 1], [0.8, -1], [1, 1]].forEach(([u, sd]) => {
    const q = bz(P, u), cx = q[0] + sd * h * 0.16, cy = q[1] - h * 0.04;
    p.lineWidth = h * 0.02; p.beginPath(); p.moveTo(q[0], q[1]); p.lineTo(cx, cy); p.stroke();
    for (let k = 0; k < 9; k++) tear(p, cx - h * 0.14 + k * h * 0.035, cy + h * 0.02, h * 0.07, h * 0.035, -Math.PI / 2 + (k - 4) * 0.12);
    p.beginPath(); p.ellipse(cx, cy + h * 0.01, h * 0.15, h * 0.03, 0, 0, TAU); p.fill();
  });
}

// ---------- Torii (Füße bei 0, ~300 hoch), Stanzmuster mit Zinnober-Gel ----------
function torii(p, g, o) {
  pose(p, g, o);
  for (const sd of [-1, 1]) {
    const x = sd * 112;
    p.beginPath(); p.moveTo(x - 15, 0); p.lineTo(x - 11, -300); p.lineTo(x + 11, -300); p.lineTo(x + 15, 0); p.closePath(); p.fill();
    p.fillRect(x - 20, -22, 40, 22);
    cut(p, () => { p.fillRect(x - 3.5, -270, 7, 230); for (let y = -280; y < -40; y += 26) dot(p, x, y, 2); });
    g.fillStyle = 'rgb(236,72,40)'; g.fillRect(x - 6, -280, 12, 250);
  }
  p.fillRect(-160, -236, 320, 18);
  p.fillRect(-7, -286, 14, 52);
  p.beginPath(); p.roundRect(-26, -282, 52, 40, 4); p.fill();
  p.beginPath(); p.moveTo(-206, -324); p.quadraticCurveTo(0, -296, 206, -324); p.lineTo(200, -304); p.quadraticCurveTo(0, -280, -200, -304); p.closePath(); p.fill();
  p.fillRect(-178, -300, 356, 14);
  cut(p, () => {
    for (let x = -180; x <= 180; x += 15) dot(p, x, -306 + Math.pow(x / 200, 2) * -14 + 2, 2.2);
    for (let x = -146; x <= 146; x += 22) { p.save(); p.translate(x, -227); p.rotate(Math.PI / 4); p.fillRect(-3.5, -3.5, 7, 7); p.restore(); }
    p.lineWidth = 2; p.beginPath(); p.roundRect(-20, -276, 40, 28, 3); p.stroke();
  });
  g.fillStyle = 'rgb(236,72,40)'; g.beginPath(); g.moveTo(-200, -320); g.quadraticCurveTo(0, -294, 200, -320); g.lineTo(196, -306); g.lineTo(176, -288); g.lineTo(-176, -288); g.lineTo(-196, -306); g.closePath(); g.fill(); g.fillRect(-158, -234, 316, 14);
  unpose(p, g);
}

// ---------- Schrein (Hokora) mit Shimenawa und Shide; gibt den Haken der Traufe zurück ----------
function shrine(p, g, o) {
  pose(p, g, o);
  p.fillRect(-130, -42, 260, 42);
  cut(p, () => { p.lineWidth = 2; for (let x = -110; x < 130; x += 40) { p.beginPath(); p.moveTo(x, -40); p.lineTo(x, -2); p.stroke(); } p.beginPath(); p.moveTo(-128, -22); p.lineTo(128, -22); p.stroke(); });
  p.fillRect(-96, -206, 192, 166);
  cut(p, () => p.fillRect(-76, -186, 152, 124));
  p.fillStyle = INK; for (let x = -76; x <= 76; x += 15) p.fillRect(x - 1.5, -186, 3, 124); for (let y = -186; y <= -62; y += 22) p.fillRect(-76, y - 1.5, 152, 3);
  g.fillStyle = 'rgb(255,170,80)'; g.fillRect(-78, -188, 156, 128);
  p.beginPath(); p.moveTo(-170, -196); p.quadraticCurveTo(-110, -210, -66, -262); p.lineTo(66, -262); p.quadraticCurveTo(110, -210, 170, -196); p.lineTo(162, -184); p.quadraticCurveTo(0, -204, -162, -184); p.closePath(); p.fill();
  p.lineWidth = 7; p.beginPath(); p.moveTo(-80, -246); p.lineTo(-46, -300); p.moveTo(-52, -246); p.lineTo(-86, -300); p.moveTo(80, -246); p.lineTo(46, -300); p.moveTo(52, -246); p.lineTo(86, -300); p.stroke();
  for (let k = -2; k <= 2; k++) { p.beginPath(); p.roundRect(k * 26 - 9, -276, 18, 14, 6); p.fill(); }
  cut(p, () => { for (let x = -150; x <= 150; x += 14) dot(p, x, -192 - Math.pow(x / 160, 2) * 6, 2); });
  // Shimenawa mit Shide
  const rope = [[-104, -214], [-40, -196], [40, -196], [104, -214]];
  p.lineWidth = 13; p.beginPath(); for (let i = 0; i <= 30; i++) { const q = bz(rope, i / 30); if (i) p.lineTo(q[0], q[1]); else p.moveTo(q[0], q[1]); } p.stroke();
  cut(p, () => { p.lineWidth = 2; for (let i = 1; i < 30; i++) { const q = bz(rope, i / 30); p.beginPath(); p.moveTo(q[0] - 4, q[1] - 5); p.lineTo(q[0] + 4, q[1] + 5); p.stroke(); } });
  for (const u of [0.22, 0.5, 0.78]) {
    const q = bz(rope, u), sw = Math.sin((o.t || 0) * 2 + u * 9) * 3;
    p.beginPath(); p.moveTo(q[0] - 7, q[1]); p.lineTo(q[0] + 7, q[1]); p.lineTo(q[0] + 7 + sw, q[1] + 16); p.lineTo(q[0] - 3 + sw, q[1] + 16); p.lineTo(q[0] + 7 + sw, q[1] + 32); p.lineTo(q[0] - 3 + sw, q[1] + 32); p.lineTo(q[0] + 5 + sw, q[1] + 48); p.lineTo(q[0] - 7 + sw, q[1] + 48); p.closePath(); p.fill();
    cut(p, () => { p.fillRect(q[0] - 3 + sw, q[1] + 4, 6, 8); p.fillRect(q[0] - 1 + sw, q[1] + 20, 6, 8); p.fillRect(q[0] - 1 + sw, q[1] + 36, 6, 8); });
  }
  g.fillStyle = 'rgb(255,248,226)'; for (const u of [0.22, 0.5, 0.78]) { const q = bz(rope, u), sw = Math.sin((o.t || 0) * 2 + u * 9) * 3; g.fillRect(q[0] - 4 + sw, q[1] + 3, 10, 42); }
  // Haken an der rechten Traufe
  p.lineWidth = 3; p.beginPath(); p.moveTo(150, -194); p.lineTo(150, -176); p.arc(144, -176, 6, 0, Math.PI * 0.9); p.stroke();
  const hook = wpt(p, 150, -170);
  unpose(p, g);
  return hook;
}

// ---------- Suzu: Schreinglocke mit drei Schellen und bunten Bändern ----------
// (x, y) = oberes Ende des Griffs; ang = Neigung; sh = Schütteln
function suzu(p, g, x, y, s, ang, sh) {
  both([p, g], (c) => { c.save(); c.translate(x, y); c.rotate(ang + Math.sin(sh * 40) * 0.25 * Math.min(1, sh * 4) * Math.exp(-sh * 3)); c.scale(s, s); });
  p.fillStyle = INK; p.strokeStyle = INK;
  p.lineWidth = 7; p.lineCap = 'round'; p.beginPath(); p.moveTo(0, 0); p.lineTo(0, 74); p.stroke();
  for (const [bx, by] of [[0, -14], [-15, 8], [15, 8], [0, 26]]) { dot(p, bx, by, 13); cut(p, () => { p.fillRect(bx - 8, by + 3, 16, 3); dot(p, bx, by - 3, 2.5); }); }
  g.fillStyle = 'rgb(255,214,96)'; for (const [bx, by] of [[0, -14], [-15, 8], [15, 8], [0, 26]]) dot(g, bx, by, 9);
  const cols = ['rgb(232,52,36)', 'rgb(80,190,110)', 'rgb(90,140,240)', 'rgb(255,230,120)', 'rgb(160,90,210)'];
  cols.forEach((c, k) => {
    const pts = []; for (let i = 0; i <= 12; i++) { const u = i / 12; pts.push([-16 + k * 8 + Math.sin(u * 5 + k + sh * 30) * 8 * u, 76 + u * 120]); }
    const path = (c2, w) => { c2.lineWidth = w; c2.lineCap = 'round'; c2.beginPath(); pts.forEach(([a, b], i) => (i ? c2.lineTo(a, b) : c2.moveTo(a, b))); c2.stroke(); };
    p.strokeStyle = INK; path(p, 9);
    cut(p, () => path(p, 4.5));
    g.strokeStyle = c; path(g, 7);
  });
  both([p, g], (c) => c.restore());
}

// ---------- Hana: junge Miko, weißes Kosode (Gel), rotes Hakama (Gel), langes Haar mit Papierband ----------
// o: step, arm (0 = hängt), bell (Glocke in der Hand), sh (Schütteln), bow
function hana(p, g, o, rods) {
  pose(p, g, o);
  const st = o.step || 0, sw = Math.sin(st) * 7;
  p.beginPath(); p.ellipse(-22 + sw, -4, 18, 6, 0, 0, TAU); p.fill(); p.beginPath(); p.ellipse(24 - sw, -4, 18, 6, 0, 0, TAU); p.fill();
  const hak = () => { p.beginPath(); p.moveTo(-36, -152); p.lineTo(40, -152); p.lineTo(68 - sw * 0.4, -8); p.lineTo(-60 + sw * 0.4, -8); p.closePath(); };
  hak(); p.fill();
  cut(p, () => {
    for (let k = 0; k < 6; k++) { const x0 = -26 + k * 12, x1 = -46 + k * 21; p.beginPath(); p.moveTo(x0, -138); p.lineTo(x0 + 4, -138); p.lineTo(x1 + 5, -22); p.lineTo(x1, -22); p.closePath(); p.fill(); }
    for (let x = -50; x <= 56; x += 13) { p.save(); p.translate(x, -14); p.rotate(Math.PI / 4); p.fillRect(-3, -3, 6, 6); p.restore(); }
  });
  g.fillStyle = 'rgb(232,46,30)'; g.beginPath(); g.moveTo(-34, -150); g.lineTo(38, -150); g.lineTo(65 - sw * 0.4, -10); g.lineTo(-57 + sw * 0.4, -10); g.closePath(); g.fill();
  tear(p, 30, -150, 26, 10, 0.5); tear(p, 30, -150, 22, 10, 1.4);
  // Oberkörper und hinterer Ärmel (weiß)
  p.beginPath(); p.moveTo(-32, -150); p.lineTo(36, -150); p.lineTo(30, -240); p.lineTo(-24, -242); p.closePath(); p.fill();
  p.beginPath(); p.moveTo(-22, -234); p.lineTo(-72, -206); p.lineTo(-70, -126); p.quadraticCurveTo(-46, -118, -26, -146); p.closePath(); p.fill();
  cut(p, () => {
    p.beginPath(); p.moveTo(-22, -232); p.lineTo(26, -232); p.lineTo(24, -160); p.lineTo(-24, -160); p.closePath(); p.fill();
    p.beginPath(); p.moveTo(-28, -222); p.lineTo(-62, -200); p.lineTo(-60, -136); p.lineTo(-30, -150); p.closePath(); p.fill();
  });
  p.fillStyle = INK; p.lineWidth = 4; p.beginPath(); p.moveTo(-6, -240); p.lineTo(8, -190); p.lineTo(22, -240); p.stroke();
  p.lineWidth = 2.4; for (let k = 0; k < 3; k++) { p.beginPath(); p.moveTo(-58 + k * 2, -196 + k * 22); p.quadraticCurveTo(-44, -186 + k * 22, -30, -194 + k * 22); p.stroke(); }
  for (const [x, y] of [[0, -214], [14, -176], [-48, -170]]) { for (let k = 0; k < 6; k++) tear(p, x, y, 7, 3, k * TAU / 6); }
  g.fillStyle = 'rgb(255,246,226)'; g.beginPath(); g.moveTo(-30, -150); g.lineTo(34, -150); g.lineTo(28, -238); g.lineTo(-22, -240); g.closePath(); g.fill();
  g.beginPath(); g.moveTo(-24, -230); g.lineTo(-68, -204); g.lineTo(-66, -130); g.lineTo(-28, -148); g.closePath(); g.fill();
  // Kopf, Haar, Papierband
  p.beginPath(); p.arc(8, -268, 25, 0, TAU); p.fill();
  p.beginPath(); p.moveTo(30, -272); p.lineTo(38, -262); p.lineTo(30, -258); p.fill();
  p.beginPath(); p.moveTo(-14, -292); p.quadraticCurveTo(8, -304, 24, -290); p.lineTo(-8, -258); p.lineTo(-30, -150); p.lineTo(-46, -156); p.lineTo(-34, -262); p.closePath(); p.fill();
  cut(p, () => { p.fillRect(-36, -232, 16, 12); p.lineWidth = 2.4; p.beginPath(); p.moveTo(18, -270); p.quadraticCurveTo(23, -268, 26, -271); p.stroke(); });
  g.fillStyle = 'rgb(255,250,236)'; g.fillRect(-38, -234, 20, 16);
  // Arm (an der Schulter gestiftet), mit Glocke
  both([p, g], (c) => { c.save(); c.translate(6, -228); c.rotate(o.arm || 0); });
  p.beginPath(); p.moveTo(-14, -4); p.lineTo(16, -4); p.lineTo(26, 62); p.lineTo(-22, 70); p.closePath(); p.fill();
  cut(p, () => { p.beginPath(); p.moveTo(-8, 4); p.lineTo(12, 4); p.lineTo(18, 56); p.lineTo(-14, 60); p.closePath(); p.fill(); });
  g.fillStyle = 'rgb(255,246,226)'; g.beginPath(); g.moveTo(-12, -2); g.lineTo(14, -2); g.lineTo(24, 60); g.lineTo(-20, 66); g.closePath(); g.fill();
  p.lineWidth = 9; p.lineCap = 'round'; p.beginPath(); p.moveTo(2, 60); p.lineTo(4, 92); p.stroke(); dot(p, 4, 96, 8);
  if (o.bell) suzu(p, g, 4, 92, 0.62, Math.PI - (o.arm || 0) * 0.3, o.sh || 0);
  pin(p, 0, 0, 6);
  if (rods && !o.noRods) rods.push([...wpt(p, 4, 96), 2.8]);
  both([p, g], (c) => c.restore());
  if (rods && !o.noRods) rods.push([...wpt(p, 0, -110), 3.4]);
  unpose(p, g);
}

// ---------- Sonne mit Strahlenkranz ----------
function sun(p, g, x, y, r, rot) {
  p.fillStyle = INK;
  for (let k = 0; k < 18; k++) { const a = rot + k * TAU / 18; tear(p, x + Math.cos(a) * (r + 8), y + Math.sin(a) * (r + 8), k % 2 ? 26 : 40, 14, a); }
  dot(p, x, y, r + 10);
  cut(p, () => { dot(p, x, y, r); });
  g.fillStyle = 'rgb(255,150,40)'; dot(g, x, y, r + 1);
  p.fillStyle = INK; for (let k = 0; k < 12; k++) { const a = rot * 0.5 + k * TAU / 12; tear(p, x + Math.cos(a) * r * 0.3, y + Math.sin(a) * r * 0.3, r * 0.6, 7, a); }
  dot(p, x, y, r * 0.3);
  cut(p, () => dot(p, x, y, r * 0.14));
}
