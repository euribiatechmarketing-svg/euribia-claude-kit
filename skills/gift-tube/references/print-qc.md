# Print QC + fixing an exported PDF (sizes, bleed, image resolution)

After exporting the frames to PDF, verify they're genuinely print-ready. Two things fail silently:
wrong size, and low-resolution placed images. Both are checkable with pymupdf, fixable with
pikepdf/PIL — no need to round-trip through Figma for the fixes below.

## 1. Measure size + min image DPI
```python
import fitz, glob, os
mm=lambda p: round(p/72*25.4,1)
for f in glob.glob('*.pdf'):
    d=fitz.open(f); pg=d[0]; r=pg.rect; dpis=[]
    for img in pg.get_images(full=True):
        xref,pw,ph=img[0],img[2],img[3]
        for rc in pg.get_image_rects(xref):
            if rc.width>3 and rc.height>3: dpis.append(min(pw/(rc.width/72), ph/(rc.height/72)))
    print(os.path.basename(f), mm(r.width),'x',mm(r.height),'mm  min', round(min(dpis)),'dpi')
```
Targets: tube label **201×156mm**, voucher **136×306mm** (130×300 + 3mm bleed). Print wants
**≥300 dpi** on photos; ~150 dpi is tolerable only on soft backgrounds, not on logos/photos/text.

**Figma quirk:** layers with effects (blur, some blend modes, masks) rasterize on PDF export at
**2× = 144 dpi**. So a design full of effects shows a 144 dpi floor even though the text/vectors stay
sharp. To lift that floor you must re-export from Figma at a higher scale or reduce the effects —
it can't be fixed in the PDF. Genuinely low-res **source** images (e.g. a 1000px photo placed
full-bleed → 59 dpi) are the real defect, and those you fix below.

## 2. Upscale a low-res placed image in-place (no regen, keeps everything else vector)
Swap the image XObject's bytes for an upscaled version; the placement matrix is untouched, so it
just renders sharper. Identify the base image vs its alpha by `/SMask` (the base has one, the mask
doesn't). Upscale both by the same factor.
```python
import pikepdf, fitz; from pikepdf import Name; from PIL import Image, ImageFilter
# extract: fitz extract_image(xref) -> bytes; find the low-dpi one from step 1 by its W×H
rgb=Image.open(src).convert('RGB'); f=4
up=rgb.resize((rgb.width*f,rgb.height*f),Image.LANCZOS).filter(ImageFilter.UnsharpMask(3,90,2))
up.save('up.jpg',quality=92)                      # + upscale the /SMask to grayscale jpg the same way
RGB=open('up.jpg','rb').read(); GRAY=open('mask.jpg','rb').read(); NW,NH=rgb.width*f,rgb.height*f
pdf=pikepdf.open(infile)
for o in pdf.objects:
    if o.get('/Subtype')==Name('/Image') and int(o.get('/Width',0))==W0 and int(o.get('/Height',0))==H0:
        if '/DecodeParms' in o: del o['/DecodeParms']
        if '/SMask' in o.keys(): o.write(RGB,filter=Name('/DCTDecode')); o.Width=NW;o.Height=NH;o.BitsPerComponent=8
        else: o.write(GRAY,filter=Name('/DCTDecode')); o.Width=NW;o.Height=NH;o.ColorSpace=Name('/DeviceGray');o.BitsPerComponent=8
pdf.save(outfile)
```
Lanczos+unsharp removes pixelation but adds no real detail; for a hero photo prefer a true upscaler
(`upscale_image` MCP / Topaz). For a busy food/texture background, Lanczos ×4 is fine.

## 2b. Defringe a cut-out photo (white/light halo around the edge)
A cut-out on a coloured background often shows a light rim — the edge RGB still holds the photo's
original (white) background, and a soft/JPEG-compressed alpha lets it bleed through. Fix = colour
**decontamination** (push the subject's colour out under the edge) + a **lossless, slightly choked**
mask. Never store an alpha mask as JPEG — DCT ringing *is* a halo. Identify base vs mask by `/SMask`
(base has it) and follow the ref so any mask resolution works.
```python
import numpy as np, zlib, io; from scipy import ndimage; from PIL import Image, ImageFilter
rgb=np.asarray(rgb_img,np.uint8); m=np.asarray(mask_img.resize(rgb_img.size),np.uint8)
op=m>140
idx=ndimage.distance_transform_edt(~op, return_distances=False, return_indices=True)
clean=rgb[tuple(idx)]; clean[op]=rgb[op]                         # nearest-subject-colour under edge
a=ndimage.grey_erosion(m,size=5).astype('f4')                    # choke ~2px
a=np.asarray(Image.fromarray(a.astype('u1')).filter(ImageFilter.GaussianBlur(0.8)),'f4')
alpha=np.clip((a-115)/(205-115),0,1)*255                          # steepen edge
buf=io.BytesIO(); Image.fromarray(clean,'RGB').save(buf,'JPEG',quality=95)
# embed: base.write(buf.getvalue(), DCTDecode); base.SMask.write(zlib.compress(alpha.astype('u1').tobytes()), FlateDecode)
```
Worked example: the Cizi crackers (also upscaled ×4) and the McVitie's embossed biscuit both had a
light rim on the blue/teal — this removed it cleanly without touching the soft glow/shadow graphics.

## 3. Declare bleed + trim (the "print padding")
Even when the canvas already includes 3mm bleed, the PDF should carry **BleedBox** (= the full
canvas) and **TrimBox** (= the final cut) so the printer knows where to cut.
```python
import pikepdf; from pikepdf import Array
PT=lambda mm: mm*72/25.4
for page in pdf.pages:
    mb=[float(x) for x in page.MediaBox]; W,H=mb[2]-mb[0],mb[3]-mb[1]
    page.obj.BleedBox=Array(mb); page.obj.CropBox=Array(mb)
    if W>H: i=PT(3); page.obj.TrimBox=Array([mb[0]+i,mb[1]+i,mb[2]-i,mb[3]-i])   # tube: 3mm inset
    else:   tx=(W-PT(130))/2; ty=(H-PT(300))/2                                    # voucher: exact 130×300
            page.obj.TrimBox=Array([mb[0]+tx,mb[1]+ty,mb[2]-tx,mb[3]-ty])
```
Verify by re-reading (keep the Pdf referenced — `pdf=pikepdf.open(f); p=pdf.pages[0]`, never
`pikepdf.open(f).pages[0]`, which GC-destroys the page mid-read).
