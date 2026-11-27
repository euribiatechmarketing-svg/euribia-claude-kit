# Figma Plugin API traps in this workflow

Every one of these was hit live. Read before writing the script, not after the render looks wrong.

## Vectors

**`figma.createVector()` ships with a default black stroke.** Every shape you create gets a
hairline outline until you clear it. Set `strokes = []` on masks, panels and flattened text.

**`GLASS` does not render on a VECTOR.** Assigning the effect succeeds and `node.effects` reads
back `["GLASS"]`, but the shape renders as an outline only. Glass must sit on a `RECTANGLE`.

**Working glass-in-a-trapezoid card** — keeps the node a FRAME, so it still holds content:

```
Card (FRAME, clipsContent)
├── child[0]  VECTOR trapezoid, isMask = true, cornerRadius set
├── child[1]  RECTANGLE, the fill + GLASS effect, full bbox
└── child[2…] content — also clipped by the mask
```

`isMask` on `children[0]` masks every sibling above it. Corner rounding on the mask handles the
card's corners, so inner panels can be plain square quads.

## Text → curves

**`textNode.outlineText()` does not exist.** Use `figma.flatten([textNode], parent)`, which
returns a `VectorNode` and removes the original.

**Order of operations for warping — this is the one that silently breaks:**

```js
const v = figma.flatten([t], card);
const net = v.vectorNetwork, ox = v.x, oy = v.y;   // 1. read the origin
// 2. build warped coords in CARD space: Hm(ox + px, oy + py)
v.x = 0; v.y = 0;                                  // 3. zero the origin BEFORE writing
await v.setVectorNetworkAsync({ vertices, segments, regions });
v.strokes = []; v.fills = fills;                   // 4. NEVER touch x/y after this
```

Figma re-normalises the network on write and compensates via `x`/`y`. Setting `x`/`y` *after*
`setVectorNetworkAsync` destroys that compensation and collapses everything into the top-left
corner.

**Cubic segments** must have their control points mapped, not just their vertices:

```js
const P0 = M(A.x, A.y), P3 = M(B.x, B.y);
const P1 = M(A.x + tangentStart.x, A.y + tangentStart.y);
const P2 = M(B.x + tangentEnd.x,   B.y + tangentEnd.y);
tangentStart = { x: P1.x - P0.x, y: P1.y - P0.y };
tangentEnd   = { x: P2.x - P3.x, y: P2.y - P3.y };
```

A projective map of a cubic is not exactly a cubic, but mapping control points is the standard
approximation and is invisible at these angles.

Preserve the other vertex properties with `Object.assign({}, vt, { x, y })` — vertices carry
`strokeCap`, `strokeJoin`, `cornerRadius`, `handleMirroring`. Pass `regions` through untouched.

Cost: a 50-character line of body copy outlines to ~1300 vertices per card. Fine to write, but
the text is no longer editable.

## Transforms

**`relativeTransform` accepts an arbitrary 2×2.** Figma normalises each column to unit length
(stripping scale) but keeps the shear. Combined with `resize(w, h)` that expresses a full affine —
rotation, non-uniform scale and skew — on a real frame.

Reset a previously sheared node with `relativeTransform = [[1,0,tx],[0,1,ty]]`; setting
`rotation = 0` does not clear shear.

## Screenshots of a region

`node.screenshot()` only frames a node. To capture a *section* of a page, make a temporary slice:

```js
const slice = figma.createSlice();
parent.appendChild(slice);
slice.x = 0; slice.y = 1060; slice.resize(1512, 660);
await slice.screenshot({ scale: 0.9 });
slice.remove();
```

## Misc

- A `GROUP` does not break the GLASS effect — grouping the finished band is safe.
- `figma.ungroup(group)` before re-laying out members, then regroup; child `relativeTransform`
  inside a group is not worth reasoning about.
- **A literal U+2028 / U+2029 in the script source kills the MCP transport** with
  `SyntaxError: unexpected line terminator in regexp`. Figma layer names contain them. Build such
  regexes from escapes: `new RegExp('[\\u2028\\u2029]', 'g')`, and sanitise every name you return.
