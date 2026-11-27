# Geometry

All maths runs inside the `use_figma` script. Return the computed widths/heights so you can
verify the numbers before looking at a render.

## 1. Straight-on cylinder (the default)

Cards sit on a cylinder rotating about a **vertical** axis; the camera sits on the band's
centreline. Every card's two vertical edges stay centred on one horizontal line, so the top arc
is the exact mirror of the bottom arc.

```
W, H      card size in flat design space (e.g. 311 × 391)
Rc        carousel radius
D         camera distance to the nearest point of the cylinder
f         focal length — set f = D so the centre card renders 1:1
STEP      degrees between adjacent cards
CX, MIDY  where the band's centre lands on canvas
```

For a card at yaw `th` (radians) and a horizontal offset `u` along the card (`u = ±W/2` gives the
two vertical edges):

```js
x3 = Rc * Math.sin(th) + u * Math.cos(th)
z3 = Rc * Math.cos(th) - u * Math.sin(th)
s  = f / ((Rc + D) - z3)            // perspective scale at that edge
edgeX      = CX + x3 * s
edgeHalfH  = (H / 2) * s            // edge spans MIDY ± edgeHalfH
```

The card's bounding box: `x` from `edgeX(-W/2)` to `edgeX(+W/2)`, height `2 * max(hhL, hhR)`,
positioned at `y = MIDY - max(hhL, hhR)`.

### Choosing Rc so cards sit edge-to-edge

```js
Rc = (W + gap) / (STEP * Math.PI / 180)
```

Arc length per step equals card width plus the gap you want. Note the *projected* gaps come out
slightly uneven — perspective compresses the outer ones. That reads as correct, not as a bug.

### Tuning

| Knob | Down | Up |
|---|---|---|
| `D` (and `f` with it) | stronger perspective, faster size falloff, narrower outer cards | flatter, closer to a plain row |
| `STEP` | cards overlap | bigger gaps, wider band, more foreshortening |
| `Rc` | more yaw per card, more taper, narrower outer cards | gentler, flatter |

Sanity check every time: outer card width must clear whatever content it has to hold.

## 2. Adding tilt / shear (breaks top-bottom symmetry)

Move the camera off the centreline with `camY` (negative = camera above the band):

```js
screenY = CY0 + ((y3 - camY) * f) / Zc
```

Then build each card from three projected corners (TL, TR, BL) and feed Figma an affine:

```js
t1 = TR - TL;  t2 = BL - TL
w0 = |t1|;     h0 = |t2|
node.resize(w0, h0)
node.relativeTransform = [[t1.x/w0, t2.x/h0, TL.x],
                          [t1.y/w0, t2.y/h0, TL.y]]
```

Figma normalises the 2×2 columns to unit length (stripping scale) but **preserves the shear**, so
`resize` + normalised matrix together express a full affine. This is the level-1/level-2 hybrid:
real lean, but parallelogram cards — no taper.

## 3. Homography (level 3)

Maps flat design space `[0,W] × [0,H]` onto the card's projected quad. Lines map to lines, so
panels, rules and dividers computed through it land exactly on the taper.

Corners in card-local coordinates, with `cy = cardHeight / 2`:

```
TL = (0, cy - hhL)   TR = (w, cy - hhR)
BR = (w, cy + hhR)   BL = (0, cy + hhL)
```

Heckbert's unit-square-to-quad solution:

```js
function homography(q, W, H) {
  const [x0,y0, x1,y1, x2,y2, x3,y3] = q;              // TL, TR, BR, BL
  const dx1 = x1-x2, dy1 = y1-y2, dx2 = x3-x2, dy2 = y3-y2;
  const sx = x0-x1+x2-x3, sy = y0-y1+y2-y3;
  const det = dx1*dy2 - dx2*dy1;
  let a,b,c,d,e,ff,g,h;
  if (Math.abs(sx) < 1e-9 && Math.abs(sy) < 1e-9) {     // affine (the centre card)
    g = 0; h = 0;
    a = x1-x0; b = x2-x1; c = x0;
    d = y1-y0; e = y2-y1; ff = y0;
  } else {
    g = (sx*dy2 - dx2*sy) / det;
    h = (dx1*sy - sx*dy1) / det;
    a = x1-x0 + g*x1;  b = x3-x0 + h*x3;  c = x0;
    d = y1-y0 + g*y1;  e = y3-y0 + h*y3;  ff = y0;
  }
  return (fx, fy) => {
    const u = fx / W, v = fy / H, den = g*u + h*v + 1;
    return { x: (a*u + b*v + c) / den, y: (d*u + e*v + ff) / den };
  };
}
```

### Why this is the good way to build level 3

Lay every card out **once** in flat 311×391 space with identical type sizes and padding, then let
each card's homography do all the scaling. You get consistent design across the band for free,
and the size ramp is physically correct rather than hand-tuned.

## 4. Trapezoid paths

Card mask (rounded by `cornerRadius` on the vector):

```
M 0 (cy-hhL) L w (cy-hhR) L w (cy+hhR) L 0 (cy+hhL) Z
```

Inner panel occupying the bottom fraction `p` of the card — compute through the homography so it
tapers with the card, and let the card's mask round its bottom corners:

```js
const c0 = Hm(0, H*(1-p)), c1 = Hm(W, H*(1-p)), c2 = Hm(W, H), c3 = Hm(0, H);
`M ${c0.x} ${c0.y} L ${c1.x} ${c1.y} L ${c2.x} ${c2.y} L ${c3.x} ${c3.y} Z`
```
