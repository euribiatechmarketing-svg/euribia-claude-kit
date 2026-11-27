// Paste-ready helpers for use_figma. Not a module — copy the functions you need
// into the script body. Code runs in Figma's async wrapper: top-level await is fine.

// ---------------------------------------------------------------- geometry ---

// Projected vertical edges of a card yawed `th` radians on a straight-on cylinder.
// Camera sits on the band centreline => top arc mirrors bottom arc exactly.
function makeCylinder({ W, H, Rc, D, f, CX, MIDY }) {
  const edge = (th, u) => {
    const x3 = Rc * Math.sin(th) + u * Math.cos(th);
    const z3 = Rc * Math.cos(th) - u * Math.sin(th);
    const s = f / ((Rc + D) - z3);
    return { x: CX + x3 * s, hh: (H / 2) * s };
  };
  return (deg) => {
    const th = deg * Math.PI / 180;
    const L = edge(th, -W / 2), R = edge(th, W / 2);
    const w = R.x - L.x, halfH = Math.max(L.hh, R.hh);
    return {
      th, w, h: 2 * halfH, cy: halfH,
      hhL: L.hh, hhR: R.hh,
      x: L.x, y: MIDY - halfH,
      scale: f / ((Rc + D) - Rc * Math.cos(th)),   // the card's own depth scale
    };
  };
}

// Radius that puts cards edge-to-edge with `gap` between them.
const radiusFor = (W, gap, stepDeg) => (W + gap) / (stepDeg * Math.PI / 180);

// Flat design space [0,W]x[0,H] -> the card's projected quad (TL, TR, BR, BL).
function homography(q, W, H) {
  const [x0, y0, x1, y1, x2, y2, x3, y3] = q;
  const dx1 = x1 - x2, dy1 = y1 - y2, dx2 = x3 - x2, dy2 = y3 - y2;
  const sx = x0 - x1 + x2 - x3, sy = y0 - y1 + y2 - y3;
  const det = dx1 * dy2 - dx2 * dy1;
  let a, b, c, d, e, ff, g, h;
  if (Math.abs(sx) < 1e-9 && Math.abs(sy) < 1e-9) {
    g = 0; h = 0;
    a = x1 - x0; b = x2 - x1; c = x0;
    d = y1 - y0; e = y2 - y1; ff = y0;
  } else {
    g = (sx * dy2 - dx2 * sy) / det;
    h = (dx1 * sy - sx * dy1) / det;
    a = x1 - x0 + g * x1; b = x3 - x0 + h * x3; c = x0;
    d = y1 - y0 + g * y1; e = y3 - y0 + h * y3; ff = y0;
  }
  return (fx, fy) => {
    const u = fx / W, v = fy / H, den = g * u + h * v + 1;
    return { x: (a * u + b * v + c) / den, y: (d * u + e * v + ff) / den };
  };
}

const quadOf = (g) => [0, g.cy - g.hhL, g.w, g.cy - g.hhR, g.w, g.cy + g.hhR, 0, g.cy + g.hhL];

// ------------------------------------------------------------------- build ---

// Turn an existing FRAME into a tapered glass card. Keeps it a frame, so it
// still accepts content. `fill` / `effects` should be copied off the user's own card.
function shapeCard(card, g, { W, H, radius, fill, effects }) {
  for (const c of [...card.children]) c.remove();
  card.relativeTransform = [[1, 0, g.x], [0, 1, g.y]];
  card.resize(g.w, g.h);
  card.fills = []; card.effects = []; card.clipsContent = true;

  const mask = figma.createVector();
  card.appendChild(mask);
  mask.name = 'Perspective mask';
  mask.x = 0; mask.y = 0;
  mask.vectorPaths = [{ windingRule: 'NONZERO', data:
    `M 0 ${g.cy - g.hhL} L ${g.w} ${g.cy - g.hhR} ` +
    `L ${g.w} ${g.cy + g.hhR} L 0 ${g.cy + g.hhL} Z` }];
  mask.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
  mask.strokes = [];                                   // createVector adds a black stroke
  mask.cornerRadius = radius * Math.sqrt((g.w / W) * (g.h / H));
  mask.isMask = true;

  const glass = figma.createRectangle();
  card.appendChild(glass);
  glass.name = 'Glass';
  glass.x = 0; glass.y = 0; glass.resize(g.w, g.h);
  glass.fills = fill; glass.effects = effects;         // GLASS renders here, NOT on a vector
  return { mask, glass };
}

// A tapered quad in flat coords -> vector inside the card. Mask rounds its corners.
function addQuad(card, Hm, name, flatQuad, fills, index) {
  const p = flatQuad.map(([fx, fy]) => Hm(fx, fy));
  const v = figma.createVector();
  if (index === undefined) card.appendChild(v); else card.insertChild(index, v);
  v.name = name; v.x = 0; v.y = 0;
  v.vectorPaths = [{ windingRule: 'NONZERO',
    data: 'M ' + p.map(q => `${q.x} ${q.y}`).join(' L ') + ' Z' }];
  v.fills = fills; v.strokes = [];
  return v;
}

// ------------------------------------------------------------- warped text ---

// Lay text out in FLAT design space, outline it, push every point through the
// card's homography. Result is curves — no longer editable.
// Load the font with figma.loadFontAsync BEFORE calling.
async function warpText(card, Hm, {
  text, family, style, size, lineHeight, letterSpacing = 0,
  fills, upper = false, colWidth, x, y, name,
}) {
  const t = figma.createText();
  t.fontName = { family, style };
  t.characters = text;
  t.fontSize = size;
  t.lineHeight = { unit: 'PIXELS', value: lineHeight };
  t.letterSpacing = { unit: 'PIXELS', value: letterSpacing };
  t.fills = fills;
  if (upper) t.textCase = 'UPPER';
  t.textAutoResize = 'HEIGHT';
  t.resize(colWidth, t.height);
  card.appendChild(t);
  t.x = x; t.y = y;

  const v = figma.flatten([t], card);            // outlineText() does not exist
  v.name = name;
  const net = v.vectorNetwork, ox = v.x, oy = v.y;
  const M = (px, py) => Hm(ox + px, oy + py);

  const vertices = net.vertices.map(vt => {
    const p = M(vt.x, vt.y);
    return Object.assign({}, vt, { x: p.x, y: p.y });   // keep strokeCap/cornerRadius/etc
  });
  const segments = net.segments.map(s => {
    const A = net.vertices[s.start], B = net.vertices[s.end];
    const ts = s.tangentStart || { x: 0, y: 0 }, te = s.tangentEnd || { x: 0, y: 0 };
    const P0 = M(A.x, A.y), P3 = M(B.x, B.y);
    const P1 = M(A.x + ts.x, A.y + ts.y), P2 = M(B.x + te.x, B.y + te.y);
    return { start: s.start, end: s.end,
             tangentStart: { x: P1.x - P0.x, y: P1.y - P0.y },
             tangentEnd:   { x: P2.x - P3.x, y: P2.y - P3.y } };
  });

  v.x = 0; v.y = 0;                              // MUST be before the write
  await v.setVectorNetworkAsync({ vertices, segments, regions: net.regions });
  v.strokes = []; v.fills = fills;               // and never touch x/y after
  return v;
}

// ------------------------------------------------------------------ verify ---

// Screenshot an arbitrary region of a page (node.screenshot only frames a node).
async function shotRegion(parent, x, y, w, h, scale = 0.9) {
  const slice = figma.createSlice();
  parent.appendChild(slice);
  slice.x = x; slice.y = y; slice.resize(w, h);
  await slice.screenshot({ scale });
  slice.remove();
}

// Layer names can contain U+2028, which kills the MCP transport if it reaches
// the script source or the return value. Build the regex from escapes.
const CLEAN = new RegExp('[\\u2028\\u2029]', 'g');
const clean = (s) => String(s).replace(CLEAN, ' ');
