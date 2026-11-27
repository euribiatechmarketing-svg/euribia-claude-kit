# OFFICIAL-EURIBIA design system (single source of truth)

Used by every `contento-*` agent. Do not invent new colors, fonts, or chrome — reuse exactly what is below.

## Canvas
- Slide frame: **1920 × 1080**, white background `#ffffff`, `clipsContent = true`.
- Left/right safe margin: **80px**. Content column width: **1760px** (x80 → x1840).
- Build slides on the **currently open page** in the user's Figma desktop app (`figma.currentPage`). Edits persist only on the open page. `createPage` also persists. A thrown error rolls back the ENTIRE `use_figma` call — wrap risky work in try/catch and never touch removed nodes.

## Working file
- File key: `gl9Dh2EjmUHuUfIp3qsFGo` (Euribia deck). Page "Euribidigital" `0:1`.
- Brand wordmark to clone: node **`183:4`** ("Group 613", black `euribia digital` lockup). Clone + `rescale(150 / SRC.width)`; place at x80 y58. To make it white (on gradient slides): after clone, `for (const n of lg.findAll(x => "fills" in x)) { try { n.fills = [solid("#ffffff")]; } catch(e){} }`.
- `createImageAsync(url)` inside plugin code is NOT available → recreate vector content natively and clone the logo node.
- **Real photos CAN be placed** via the `upload_assets` MCP tool (not plugin code): build a placeholder node, then `upload_assets` with its `nodeId` sets the photo as a fill. Library lives in `~/.claude/contento/assets/` (see its `manifest.md`). PNG/JPG/GIF/WebP, ≤10MB. _(To be verified end-to-end in testing.)_

## Color tokens
| Token | Hex |
|---|---|
| Purple (primary) | `#bf40ff` |
| Purple deep (gradient end) | `#7c09b5` |
| Near-black (text) | `#0a0a0a` |
| Gray (secondary text) | `#6b6b6b` |
| Card bg | `#fbfbfb` |
| Border / hairline | `#e8e6e0` |
| Pill bg (lilac) | `#f5e6ff` |
| Muted tag bg | `#f0f0f0` |
| Muted bar (wrong/before) | `#c9c9c9` |
| White | `#ffffff` |

## Type (only these two families)
- **Mulish** — headlines & body. Styles in use: Black, ExtraBold, Bold, SemiBold, Medium, Regular.
- **Azeret Mono** — eyebrows, labels, page tags, footer. Styles: Medium, Regular.
- Always `loadFontAsync` each style before use.

Type scale:
- Cover/closing hero line: Mulish Black 120–150, tracking -4 to -5.
- Section title (divider): Mulish Black 86–96, tracking -3.
- Slide headline: Mulish Black 54–72, tracking -1.5 to -2, lineHeight ~104–108%.
- Card title: Mulish ExtraBold / Black 26–34.
- Body: Mulish Regular/Medium 17–28, lineHeight 150–160%.
- Eyebrow / pill / page tag: Azeret Mono Medium 12–15, UPPERCASE, letterSpacing 1.5–2.
- Footer: Azeret Mono Regular 14, gray.

## Chrome (every standard slide)
- Logo top-left: clone `183:4`, rescale to 150px wide, x80 y58.
- Page tag top-right: Azeret Mono Medium 14, gray, UPPERCASE, ls 1.5, right-aligned ending at x1840, y64. Format: `СЕКЦИЯ · NN` (e.g. `СТЪЛБ 1 · 02`, `ОТВАРЯНЕ · 04`, `ДЕМО · 03`, `ФИНАЛ · 05`).
- Hairline at y140 and y994: x80 w1760 h1, color `#e8e6e0`.
- Footer trio at y1020: left `euribiadigital.com`; center (w600, x660) `Content engine · Masterclass 2026` (swap per deck); right (ending x1840) `© 2026 Euribia Digital`. All Azeret Mono Regular 14 gray.
- Gradient bar: y1074, full width 1920, h6, linear `#bf40ff → #7c09b5`.

## Gradients
```js
const gradBar = [{type:"GRADIENT_LINEAR",gradientTransform:[[1,0,0],[0,1,0]],
  gradientStops:[{position:0,color:{...hx("#bf40ff"),a:1}},{position:1,color:{...hx("#7c09b5"),a:1}}]}];
// Hero / full-bleed dramatic panels (diagonal):
const gradHero = [{type:"GRADIENT_LINEAR",gradientTransform:[[0.85,0.5,0],[-0.3,0.85,0.1]],
  gradientStops:[{position:0,color:{...hx("#bf40ff"),a:1}},{position:1,color:{...hx("#7c09b5"),a:1}}]}];
```

## Helper code (paste at the top of every use_figma call)
```js
const page = figma.currentPage;
const hx = h => ({r:parseInt(h.slice(1,3),16)/255, g:parseInt(h.slice(3,5),16)/255, b:parseInt(h.slice(5,7),16)/255});
const solid = (h,a=1) => ({type:"SOLID", color:hx(h), opacity:a});
const FONTS=[["Mulish","Black"],["Mulish","ExtraBold"],["Mulish","Bold"],["Mulish","SemiBold"],["Mulish","Medium"],["Mulish","Regular"],["Azeret Mono","Medium"],["Azeret Mono","Regular"]];
for (const f of FONTS) { await figma.loadFontAsync({family:f[0], style:f[1]}); }
function txt(p,o){const t=figma.createText();t.fontName={family:o.f||"Mulish",style:o.s||"Regular"};t.fontSize=o.size;t.characters=o.ch;t.fills=[solid(o.color||"#0a0a0a")];if(o.w){t.resize(o.w,t.height);t.textAutoResize="HEIGHT";}else t.textAutoResize="WIDTH_AND_HEIGHT";if(o.align)t.textAlignHorizontal=o.align;if(o.lh)t.lineHeight={unit:"PERCENT",value:o.lh};if(o.ls!=null)t.letterSpacing={unit:"PIXELS",value:o.ls};if(o.uc)t.textCase="UPPER";if(o.op!=null)t.opacity=o.op;t.x=o.x;t.y=o.y;p.appendChild(t);return t;}
function rect(p,o){const r=figma.createRectangle();r.resize(o.w,o.h);r.x=o.x;r.y=o.y;r.fills=o.fill!==undefined?o.fill:[solid(o.color||"#ffffff")];if(o.radius)r.cornerRadius=o.radius;if(o.tl!=null){r.topLeftRadius=o.tl;r.topRightRadius=o.tr;r.bottomRightRadius=o.br;r.bottomLeftRadius=o.bl;}if(o.stroke){r.strokes=[solid(o.stroke)];r.strokeWeight=o.sw||1;}p.appendChild(r);return r;}
const SRC = figma.getNodeById("183:4");
function frame(name,x,y,bg){const F=figma.createFrame();F.name=name;F.resize(1920,1080);F.x=x;F.y=y;F.fills=bg||[solid("#ffffff")];F.clipsContent=true;page.appendChild(F);return F;}
function chrome(F,tag,footerCenter){
  const lg=SRC.clone();lg.rescale(150/SRC.width);lg.x=80;lg.y=58;F.appendChild(lg);
  txt(F,{ch:tag,f:"Azeret Mono",s:"Medium",size:14,color:"#6b6b6b",uc:true,ls:1.5,w:500,align:"RIGHT",x:1340,y:64});
  rect(F,{x:80,y:140,w:1760,h:1,color:"#e8e6e0"});
  rect(F,{x:80,y:994,w:1760,h:1,color:"#e8e6e0"});
  txt(F,{ch:"euribiadigital.com",f:"Azeret Mono",s:"Regular",size:14,color:"#6b6b6b",x:80,y:1020});
  txt(F,{ch:footerCenter||"Content engine · Masterclass 2026",f:"Azeret Mono",s:"Regular",size:14,color:"#6b6b6b",align:"CENTER",w:600,x:660,y:1020});
  txt(F,{ch:"© 2026 Euribia Digital",f:"Azeret Mono",s:"Regular",size:14,color:"#6b6b6b",align:"RIGHT",w:500,x:1340,y:1020});
  rect(F,{x:0,y:1074,w:1920,h:6,fill:gradBar});
}
function pill(F,x,y,label){const w=label.length*9.2+44;rect(F,{x:x,y:y,w:w,h:36,color:"#f5e6ff",radius:18});txt(F,{ch:label,f:"Azeret Mono",s:"Medium",size:13,color:"#bf40ff",uc:true,ls:1.5,align:"CENTER",w:w,x:x,y:y+11});return w;}
```
Note: text node IDs returned per call; capture them so you can re-screenshot / edit later.

## Layout pattern catalog (pick the one that fits the idea)
1. **Section divider** — pill `СТЪЛБ N-ТИ`, 2-line Black title (line 2 in purple), supporting idea in gray; giant faint `0N` (Mulish Black 560, `#f5e6ff`) bottom-right, OR a faint glyph (★ / →) for non-numbered sections.
2. **Big-number / statement** — one huge figure or phrase; minimal support text. Good for shock facts.
3. **Two-card contrast** — left muted card (gray top bar, `#f0f0f0` tag) = wrong/before; right purple-top card (`#f5e6ff` tag) = right/after. Bottom one-line takeaway. (wrong-question, myth/reality, before/after, обикновен-AI/агент.)
4. **Stack rows** — full-width `#fbfbfb` rows (h~96, radius14, purple left bar w6); left bold label + small gray sublabel, right Mulish Black purple value, optional `→` mid. (tool stack, posoka→format mapping.)
5. **3-card row** — three `#fbfbfb` cards (w~560 at x80/680/1280, purple top bar); number eyebrow + ExtraBold title + gray body. Last card may be solid purple for emphasis. (levers, human layer, recap, steps.)
6. **Flow / pipeline** — horizontal boxes joined by purple `→`; final box solid purple. (Глас→Агент→Резултат, backstage pipeline, ядро→посоки→формати→отпечатък.)
7. **Architecture tree** — gradient orchestrator box centered on top, thin purple connector rects, 3 child agent cards below. (оркестратор + агенти.)
8. **Ratio bar** — single split bar: ~80% gradient + ~20% black, big % labels inside; takeaway below. (80/20.)
9. **Gradient hero** — full-width `gradHero` panel (x80 y210 w1760 h680, radius24) with white eyebrow + 2-line Black white headline + white sub. Use for the 3–4 most dramatic beats only. For a full-bleed closing, set the whole frame fill to `gradHero` and recolor the logo white.
10. **Equation / banner** — full-width gradient bar (h100–110, radius16) with one centered white Black line. (`Инструмент + връзки + инструкции = агент`.)
11. **QR takeaway** — left text column, right `#fbfbfb` rounded card containing a faux-QR (loop of small black rounded rects + 3 corner finder blocks) + mono caption. Replace with a real QR image later.

## Hard rules
- **Bulgarian copy EXACTLY as given** (the "Булети" / script). Never paraphrase, never translate, never add em-dashes the source doesn't have.
- **One idea per slide.** Dense but not crowded.
- **Only** Mulish + Azeret Mono. **Only** the palette above.
- Reuse the real logo (clone 183:4). Never fake the wordmark with text.
- Keep chrome identical across every slide of a deck; only the page tag and footer-center change.
- Verify EVERY built slide by screenshot before claiming done; fix overflow/clipping.

## Build workflow
1. Get the script/content (e.g. extract a .docx: unzip, parse `word/document.xml` `<w:t>` runs; each "Момент" = one slide, its "Булети" = the verbatim slide content).
2. Map each moment to the best layout from the catalog. Add a divider per section.
3. Lay frames out in a horizontal row per section at a fixed `y` (e.g. opening y=28000, pillar1 y=30000, …), x stepping by 2120 (1920 + 200 gap). Keep a manifest of {name → nodeId, x, y}.
4. Build in batches of 3–4 frames per `use_figma` call (smaller calls = safer rollback). Always `return` the created node IDs.
5. Screenshot each frame (`get_screenshot`), download via curl, Read to inspect. Fix issues.
6. Present screenshots to the user; wait for approval before the next section.
