# Yokai roguelike — sprite style guide

Visual reference: `masters_preview.png` (oni, kappa, hana at 6x) and `masters_floor_preview.png`
(same on a dark dungeon floor). Source of the masters: `oni.py`, `kappa.py`, `hana.py`.
Engine + palette: `px.py`. Starter script: `template_creature.py`. Rebuild masters: `python3 build_all.py`.

Look at the masters before drawing. Match them; do not copy characters from existing games.

## 1. Mood

16-bit console era (SNES / Mega Drive), semi-serious and sinister. Not cute, not chibi.
Night scene lit by a warm key light from the TOP-LEFT plus a cold moonlight rim on upper-left edges.
Bodies are dark and slightly desaturated; only eyes, teeth, claws, metal glints and paper are bright.

## 2. Hard rules

- Native 1x resolution, transparent background, alpha is 0 or 255 only. No anti-aliasing to transparency.
- No gradients, no dithering, no noise. Clean clusters: avoid single stray pixels (allowed: eye pupils,
  2–3 px glints, claw tips).
- Sprites face LEFT (side or 3/4 view). The game mirrors them.
- Light from the top-left: shadow crescents sit on the bottom-right of every form, lights on the top-left.
  Never darken all edges equally (pillow shading).
- 3–4 steps per material. Use the ramps below; do not add near-duplicate colours.
- Every drawing is produced by a script. Never hand-edit an exported PNG.

## 3. Palette (all in `px.py`, referenced by name)

Ramps run dark → light. Typical cel ramp passed to `form()` is `(shadow, mid, light)`.
The last step of a 5-step ramp is for glints only (a few pixels).

| Material | Names | Hex | Typical form ramp |
|---|---|---|---|
| Outline | K | #0a0814 | silhouette outline |
| Demon red skin | r0 r1 r2 r3 r4 | #2e0a2e #6a1230 #a81f2a #d2452f #f58a58 | (r1,r2,r3); far limbs (r0,r1,r2); lines r0; glint r4 |
| Dark hair / mane | h0 h1 h2 | #0f0c22 #1f1d44 #474c94 | (h0,h1,h2); h2 only as streaks |
| Black human hair | hb (defined in hana.py) | #1a1738 | (h0,hb,h2) |
| Bone, horn, claw, teeth | b0 b1 b2 b3 | #5f4250 #a8866a #dccb9c #fff6d8 | claws b2/b3 |
| Gold / yellow glow | y0 y1 y2 y3 | #8a4a12 #d8961a #ffe24a #fffbc0 | (y0,y1,y2); eyes y2 with y3 core |
| Red glow (eyes, embers) | e0 e1 | #c81e2a #ff5a3c | eyes e1 with y3 core |
| Tiger pelt / orange fur | t0 t1 t2 | #6e3214 #b86a16 #e8a530 | (t0,t1,t2); stripes K |
| Iron / steel | i0 i1 i2 i3 | #16162e #2f3358 #5a6490 #aebbe0 | (i1,i2,i3); lines i0; spec stripe i3 |
| Wood | w0 w1 w2 | #33202a #653c2a #96663a | (w0,w1,w2) |
| Mouth interior | q | #24061c | flat |
| Reptile / amphibian green | g0 g1 g2 g3 g4 | #0a2a34 #14503c #2e8236 #6cb840 #c8ee78 | (g1,g2,g3); far limbs (g0,g1,g2) |
| Pale belly / parchment | c0 c1 c2 | #6a5a3a #a89a52 #d8cf8a | (c0,c1,c2) |
| Shell / leather / brown fur | s0 s1 s2 s3 | #261622 #553224 #86562a #b98a40 | (s1,s2,s3); seams s0 |
| Water / spirit blue | a0 a1 a2 | #1f48a8 #3f8ae8 #9fe0ff | (a0,a1,a2) |
| Human skin | k0 k1 k2 k3 | #8a4650 #c9806c #f0bc98 #ffe6cc | (k1,k2,k3) |
| White cloth / paper | v0 v1 v2 v3 | #3e4a8c #8a98c8 #d4dcf4 #ffffff | (v1,v2,v3); deep folds v0 |
| Red cloth | m0 m1 m2 m3 | #3e0c30 #801634 #c02634 #ee5a48 | (m1,m2,m3); deep folds m0 |
| Moonlight rim | xr xh xg xs xt | #f09ab0 #6f7ed0 #a4ecc0 #cfa8a0 #f6d898 | applied automatically, see 5 |

New material (e.g. purple ghost, grey stone): add 3–4 steps with `col('p0', '#...')` in your own script.
Shadows must shift toward blue/violet and get darker; lights shift warm. Keep the mid slightly desaturated.
Register its rim colour with `px.add_rim('p0 p1 p2', 'xp')` (a pale, cold tint of the material).

## 4. Outlines

- Silhouette: 1 px near-black `K`. `C.blacken()` does this for you.
- Between overlapping parts inside the figure: 1 px in the darkest step of the material on top
  (`c.stamp(part, 'r0')` for red skin, `'g0'` green, `'K'` for cloth, hair, metal, paper).
- Muscle, fold and seam lines: darkest or second-darkest step, 1 px, drawn with `line()` clipped by `only=`.

## 5. Light and shading

- `form(mask, (shadow, mid, light), sd, hl)` fills the mid, puts a shadow crescent `sd` px wide on the
  bottom-right and a `hl` px light edge on the top-left. Big forms: `sd` 3–5. Small forms: `sd` 1–2. `hl` 0–1 (2 only on the largest form).
- Build anatomy from overlapping forms (deltoid over upper arm, pecs over ribcage, kneecap over leg);
  each form's shadow crescent becomes the muscle line.
- Far-side limbs use the next darker ramp so they separate from near limbs.
- Glints: 2–4 px dashes of the brightest step on the most lit forms only. Few of them.
- Rim light: `blacken()` recolours the first fill pixel under the outline on top-facing and upper-left
  silhouette edges with the cold rim colour. This is what keeps sprites readable on dark floors
  (#1e1a24–#2c2a36). Always check your sprite on such a background, not only on #16285c.
- Eyes glow: y2 or e1 with a y3 core pixel, set in a dark socket (darkest skin step or K) under a heavy,
  slanted K brow (inner end lower). Enemies look menacing; the heroine looks determined, never cute.

## 6. Proportions and size classes

Height = body from top of head/horns to baseline, weapons excluded.

| Class | Height | Examples |
|---|---|---|
| Small yokai | 32–40 px | wisps, imps, umbrella or lantern spirits |
| Normal | 48–60 px | kappa (54), heroine (61), tengu, fox spirits |
| Large | 70–90 px | oni (80) |
| Boss | 100–128 px | |

Humanoids: head about 1/4–1/5 of body height. Creatures may have bigger heads but keep limbs with
visible joints, fingers/claws and feet. Silhouette must read as the creature when filled flat black.
Give every sprite one strong secondary shape (weapon, shell, mane, sleeve, tail).

## 7. Files and animation format

For a creature called `<name>` (lowercase, no spaces):

| File | Content |
|---|---|
| `<name>.png` | static pose, cropped with 1 px transparent margin |
| `<name>_walk.png` | horizontal strip, 4 frames (walk: contact, passing, contact, passing; flyers: 4-frame float) |
| `<name>_attack.png` | horizontal strip, 3 frames: wind-up, strike, recover |
| `<name>_preview.png` (also `_walk_preview`, `_attack_preview`) | 6x nearest-neighbour on #16285c |

- All frames of one creature use the same cell size in both strips. No frame may touch the cell edge.
- Feet (or lowest rest point) on the same baseline in every frame; body bob at most 1–2 px.
- The face/head is the same pixel grid in every frame; it only translates.
- Never rotate or scale bitmaps. Re-pose by changing joint coordinates and redrawing the forms.
- Attack: the strike frame should extend clearly forward (left); size the cell for it.

## 8. Using px.py

```python
import sys; sys.path.insert(0, '/home/claude/fable_art')
from px import *
```

| Call | Purpose |
|---|---|
| `setsize(w, h)` | set the cell size; call first in every frame function |
| `C()` | new empty canvas (the final image, or one body part) |
| `E(cx,cy,rx,ry)`, `L(x0,y0,r0,x1,y1,r1)`, `PG(points)`, `R(x0,y0,x1,y1)`, `LN(points)` | masks: ellipse, tapered limb capsule, polygon, rectangle, polyline. Combine with `|`, `&`, `~` |
| `c.form(mask, ramp, sd, hl, only=)` | cel-shaded form |
| `c.fill(mask, colour, only=)`, `c.line(points, colour, only=)`, `c.pxs(points, colour)` | flat fill, 1 px line, single pixels |
| `c.grid(x, y, text, legend, flip=)` | stamp a text grid: one character per pixel, `.` = transparent |
| `dst.stamp(part, line_colour, ring=True, skip=())` | composite a part with a 1 px outline ring; `skip` = colours the ring must not overwrite (use for hair on hair) |
| `c.blacken()` | final step: silhouette outline to K + moonlight rim |
| `c.img()`, `crop_img(im)`, `preview(im, path, 6)`, `strip(frames, path)`, `orphans(im)` | export and checks |

Workflow per creature (see `template_creature.py`, which runs as-is):

1. Choose size class, cell size, baseline, and a `DEF` dict of joint coordinates.
2. Draw back-to-front: far limbs, body, near limbs, head, front arm/weapon. One `C()` per part, then `stamp`.
3. Author the head/face, hands and other key details as text grids. Use shapes for big masses.
4. `blacken()`, export, then LOOK at the 6x preview and a zoom of the head. Critique silhouette,
   anatomy, face, clusters, light. Fix and repeat at least 4 times.
5. Pose `WALK` (4 dicts) and `ATTACK` (3 dicts) by overriding joint coordinates only.

Tips: use radii like 9.4 instead of 9 for ellipses (integer radii leave 1 px nubs). Keep limb radii ≥ 1.7.
Ellipse/polygon coordinates are in cell pixels; keep a local origin plus `OX, OY` offset so the cell can grow.
