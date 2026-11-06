#!/usr/bin/env python3
"""
Build synthetic Kalpurush weight/style variants from Kalpurush.ttf.

  SemiBold, Bold, Italic, SemiBold Italic, Bold Italic

Method (outline-level, keeps all OpenType layout tables intact):
  * Embolden: offset every outline outwards (skia-pathops stroke + union).
    Horizontal growth is larger than vertical growth (VERT_RATIO) so glyph
    height / line density stays reasonable.  Bengali and Latin get different
    amounts because Bengali stems (~52u) are thinner than the Latin
    (Gentium) stems (~72u).
  * Italic: oblique skew of ITALIC_ANGLE degrees about the baseline.
    Mark-to-base anchors in GPOS are skewed with the outlines.
  * Bengali advances are NOT changed (the font joins letters by overlapping
    the headline; widening would open gaps).  Latin advances grow slightly.
  * GSUB / GPOS / GDEF / cmap are left untouched, so shaping is unchanged.

Requires: fonttools, skia-pathops   (pip install fonttools skia-pathops brotli)

Usage:  python build_kalpurush.py Kalpurush.ttf out_dir
"""
import math
import sys
import os

from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
import pathops
from pathops import Path, PathOp, LineCap, LineJoin

FAMILY = "Kalpurush"          # change here if you must rename the family
ITALIC_ANGLE = 12.0           # degrees
VERT_RATIO = 0.6              # vertical growth / horizontal growth
MITER_LIMIT = 3.0

# style key -> settings.  bn / lat = total stem thickening in font units.
STYLES = {
    #  key              display            wght  bn  lat  italic bold
    "SemiBold":       ("SemiBold",         600,  14, 17,  False, False),
    "Bold":           ("Bold",             700,  28, 34,  False, True),
    "Italic":         ("Italic",           400,   0,  0,  True,  False),
    "SemiBoldItalic": ("SemiBold Italic",  600,  14, 17,  True,  False),
    "BoldItalic":     ("Bold Italic",      700,  28, 34,  True,  True),
}


def is_bengali(name):
    return name.startswith(("u09", "bn", "uni25CC", "kalp.alt"))


def load_source(path):
    font = TTFont(path)
    # --- give the 20 duplicate ".notdef" glyphs unique names *before* any
    #     other table is decompiled, so GSUB/GPOS/cmap pick up the new names.
    order = font.getGlyphOrder()
    new, n = [], 0
    for i, g in enumerate(order):
        if i > 0 and g.startswith(".notdef"):
            n += 1
            g = "kalp.alt%02d" % n
        new.append(g)
    font.setGlyphOrder(new)
    return font


def record_outlines(font):
    """Decomposed, overlap-free outline of every glyph, from the ORIGINAL."""
    gs = font.getGlyphSet()
    out = {}
    for name in font.getGlyphOrder():
        p = Path()
        gs[name].draw(p.getPen(glyphSet=gs))
        if len(list(p.segments)):
            p.simplify(fix_winding=True, keep_starting_points=False)
        out[name] = p
    return out


def embolden(path, w):
    """Offset outline by w/2 horizontally (VERT_RATIO*w/2 vertically)."""
    if w <= 0 or not len(list(path.segments)):
        return path
    k = VERT_RATIO
    base = path.transform(1, 0, 0, 1.0 / k, 0, 0)
    ring = Path(base)
    ring.stroke(w, LineCap.BUTT_CAP, LineJoin.MITER_JOIN, MITER_LIMIT)
    merged = pathops.op(base, ring, PathOp.UNION, fix_winding=True,
                        keep_starting_points=False, clockwise=True)
    return merged.transform(1, 0, 0, k, 0, 0)


def to_ttglyph(path):
    path.convertConicsToQuads()
    pen = TTGlyphPen(None)
    path.draw(Cu2QuPen(pen, max_err=0.6, reverse_direction=False))
    return pen.glyph()


def skew_anchors(font, tan):
    gpos = font["GPOS"].table
    def fix(a):
        if a is None:
            return
        a.XCoordinate = int(round(a.XCoordinate + tan * a.YCoordinate))
        if a.Format != 1:           # drop contour-point / device refs
            a.Format = 1
            for attr in ("AnchorPoint", "XDeviceTable", "YDeviceTable"):
                if hasattr(a, attr):
                    delattr(a, attr)
    for lk in gpos.LookupList.Lookup:
        for st in lk.SubTable:
            if lk.LookupType == 9:
                st = st.ExtSubTable
            if hasattr(st, "MarkArray") and st.MarkArray:
                for mr in st.MarkArray.MarkRecord:
                    fix(mr.MarkAnchor)
            if hasattr(st, "BaseArray") and st.BaseArray:
                for br in st.BaseArray.BaseRecord:
                    for a in br.BaseAnchor:
                        fix(a)
            if hasattr(st, "Mark2Array") and st.Mark2Array:
                for r in st.Mark2Array.Mark2Record:
                    for a in r.Mark2Anchor:
                        fix(a)
            if hasattr(st, "LigatureArray") and st.LigatureArray:
                for la in st.LigatureArray.LigatureAttach:
                    for comp in la.ComponentRecord:
                        for a in comp.LigatureAnchor:
                            fix(a)


def set_names(font, family, style_display, ps_name, wght, italic, bold, version):
    name = font["name"]
    drop = {1, 2, 3, 4, 6, 16, 17, 21, 22, 25}
    name.names = [r for r in name.names if r.nameID not in drop]

    riibi = wght in (400, 700)           # fits the 4-style R/I/B/BI group
    if riibi:
        nid1 = family
        nid2 = ("Bold Italic" if bold and italic else "Bold" if bold
                else "Italic" if italic else "Regular")
    else:                                 # SemiBold(+Italic): legacy name
        nid1 = "%s %s" % (family, "SemiBold")
        nid2 = "Italic" if italic else "Regular"

    full = "%s %s" % (family, style_display)
    uid = "%s; %s; synthesized from %s Regular" % (full, version, family)
    recs = {1: nid1, 2: nid2, 3: uid, 4: full, 6: ps_name}
    if not riibi:
        recs[16] = family
        recs[17] = style_display
    for nid, s in recs.items():
        name.setName(s, nid, 3, 1, 0x409)   # Windows, Unicode BMP, en-US
        name.setName(s, nid, 1, 0, 0)       # Macintosh, Roman, English


def build(src_path, out_dir, key):
    style_display, wght, bn_w, lat_w, italic, bold = STYLES[key]
    font = load_source(src_path)
    upem = font["head"].unitsPerEm
    order = font.getGlyphOrder()
    version = font["name"].getDebugName(5) or "Version 1.000"

    outlines = record_outlines(font)          # from original
    tan = math.tan(math.radians(ITALIC_ANGLE)) if italic else 0.0

    glyf, hmtx = font["glyf"], font["hmtx"]
    new_glyphs = {}
    for name in order:
        path = outlines[name]
        if not len(list(path.segments)):
            new_glyphs[name] = TTGlyphPen(None).glyph()
            continue
        bengali = is_bengali(name)
        w = bn_w if bengali else lat_w
        p = embolden(path, w)
        adv, lsb = hmtx[name]
        if w and not bengali:                  # keep Latin side-bearings
            p = p.transform(1, 0, 0, 1, w / 2.0, 0)
            adv += int(round(w))
        if tan:
            p = p.transform(1, 0, tan, 1, 0, 0)
        new_glyphs[name] = to_ttglyph(p)
        hmtx[name] = (adv, lsb)

    for name in order:
        glyf[name] = new_glyphs[name]
    for name in order:
        g = glyf[name]
        g.recalcBounds(glyf)
        adv, _ = hmtx[name]
        hmtx[name] = (adv, g.xMin if g.numberOfContours else 0)

    if italic:
        skew_anchors(font, tan)

    # ---- drop hinting (no longer matches the new outlines) ---------------
    for t in ("fpgm", "prep", "cvt ", "VDMX", "hdmx", "LTSH"):
        if t in font:
            del font[t]
    font["gasp"].gaspRange = {0xFFFF: 0x000A}      # grayscale, no grid-fit
    font["maxp"].maxSizeOfInstructions = 0

    # ---- metrics / flags ---------------------------------------------------
    os2, head, hhea, post = font["OS/2"], font["head"], font["hhea"], font["post"]
    os2.usWeightClass = wght
    sel = os2.fsSelection & ~(0x01 | 0x20 | 0x40)
    if italic: sel |= 0x01
    if bold:   sel |= 0x20
    if not italic and not bold: sel |= 0x40
    os2.fsSelection = sel
    head.macStyle = (0x01 if bold else 0) | (0x02 if italic else 0)
    post.italicAngle = -ITALIC_ANGLE if italic else 0.0
    hhea.caretSlopeRise = upem if italic else 1
    hhea.caretSlopeRun = int(round(tan * upem)) if italic else 0
    os2.recalcAvgCharWidth(font)

    ps_name = "%s-%s" % (FAMILY, key)
    set_names(font, FAMILY, style_display, ps_name, wght, italic, bold, version)

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, ps_name + ".ttf")
    font.save(out)
    return out


if __name__ == "__main__":
    src, out_dir = sys.argv[1], sys.argv[2]
    only = sys.argv[3:] or list(STYLES)
    for k in only:
        print("built", build(src, out_dir, k))
