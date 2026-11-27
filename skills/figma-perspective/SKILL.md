---
name: figma-perspective
description: >-
  Build curved / perspective card bands in Figma — the "cards wrapped around a cylinder" look
  (Patta, Arc, Linear-style hero strips) — on REAL frames that keep their fills, GLASS effects
  and editable content. Use whenever the user asks to curve, fan, arc, tilt or add perspective
  to a row of cards, frames or images ("curve these cards", "like a circle", "перспектива",
  "трапецовидни", "cylinder", "carousel arc", "make it 3D", "fan them out", or points at a
  reference shot of a curved card strip). Also use to warp TEXT into a card's perspective by
  outlining it to curves. Covers the three build levels — rotated fan, true trapezoid mask,
  and homography-warped content — and picks the right one from the user's constraints.
---

Figma has no perspective tool. This skill fakes it correctly, at three escalating levels of
fidelity, using only the Plugin API through `use_figma`.

**Always load `figma-use` first** (the MCP prerequisite skill) before any `use_figma` call.

## 1. Pick the level BEFORE building

Read the user's constraints and jump straight to the right level. Building the wrong level and
retrofitting is the main way this task goes slow.

| The user says… | Level | What you build |
|---|---|---|
| "arc", "fan", "like a circle", cards splayed | **1 — Rotated fan** | frames rotated about a shared pivot on a circle |
| "perspective", "cylinder", "wrapped", "like Patta" | **2 — Trapezoid mask** | frame + vector trapezoid mask + inner content rect |
| "the text/elements must be in perspective too", "turn it into curves" | **3 — Homography warp** | level 2 + outlined text warped through the card's homography |

Escalate only as far as the ask requires. Level 3 destroys text editability.

### The constraint that decides everything

> **Strong curve ⟺ narrow outer cards.** There is no setting that gives both.

A card yawed 32° is foreshortened to ~45 % of its width. That is fine for photos (Patta crops
them off-screen) and fatal for body copy. **Ask which matters before choosing the radius**, or
state the trade-off explicitly with numbers when you deliver.

Two calibrated presets for a 311×391 card in a 1512-wide frame:

| Preset | Rc | D = f | step | Card widths | Use when |
|---|---|---|---|---|---|
| Dramatic | 1250 | 950 | 16° | 141 / 257 / **311** / 257 / 141 | images, decorative, Patta look |
| Readable | 1800 | 1050 | 11° | 198 / 278 / **311** / 278 / 198 | cards carrying real copy |

## 2. Mutually exclusive requirements — say so out loud

Three asks that users combine and cannot all hold at once:

- **"horizontal + symmetric + top and bottom equal"** → the camera must sit on the band's
  centreline (`camY = 0`). That kills all shear. Any tilt/skew makes a card's top edge and
  bottom edge diverge.
- **shear/tilt (the Patta lean)** → camera off the centreline. Top and bottom stop being equal.
- **affine on a frame** → parallelogram only. Parallel edges stay parallel, so you get a *sheared*
  card, never a *tapered* one.

A true trapezoid (level 2) resolves the first two: it restores top/bottom symmetry **and** gives
the taper, because both vertical edges stay centred on one line. When a user asks for symmetry
and curve at once, go to level 2 — do not try to satisfy it with a transform.

## 3. Pipeline

1. **Read the target.** `get_metadata` on the cards, then a read-only `use_figma` dumping
   `fills`, `strokes`, `effects`, `cornerRadius`, parent, and sibling z-order. Copy the existing
   card recipe — never invent a new one.
2. **Never restyle what the user made.** Their card look (fill opacity, GLASS, radius) is the
   spec. If legibility later fails, report it as their decision, don't silently add scrims or
   change fills.
3. **Compute geometry** from `references/geometry.md`. Return the resulting card widths and edge
   heights from the script so you can sanity-check before rendering.
4. **Build**, then screenshot. Use a temporary `SliceNode` over the section, `await
   slice.screenshot()`, then `slice.remove()` — this is the only way to frame a region rather
   than a node.
5. **Group** the cards last, and verify the GLASS effect survived grouping (it does).
6. **Report the trade-off** with real numbers: card widths, text column widths, line counts.

## 4. Hard limits — state these, don't discover them live

- Affine transforms cannot taper. Only a vector path can.
- `GLASS` does **not** render on a `VECTOR` — you get a hairline outline. Glass must live on a
  `RECTANGLE` inside a frame masked by the trapezoid.
- Warped text is curves. A copy change means rebuilding the card. Offer to keep an editable
  text layer off-canvas as the source.
- Corner radius: let the card's mask round the corners. Do not round the inner panel — the mask
  clips it for free.

## 5. References

- `references/geometry.md` — cylinder projection, the homography, parameter tuning
- `references/figma-api.md` — every API trap in this workflow, with the fix
- `scripts/perspective-lib.js` — paste-ready helpers (`cylinderEdges`, `homography`, `warpText`,
  `makeTrapezoidCard`)

Worked example: the Neuribia "5 THINGS YOU GAIN" band — file `MBuBwOXmQWO99NdtrZTF88`, page
Branding, group `Cards cylinder`. Glass cards, trapezoid masks, white tapered panels, and
homography-warped Exo 2 copy.
