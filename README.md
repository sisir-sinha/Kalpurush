# Kalpurush: SemiBold, Bold and Italic styles

Files
- `ttf/`    Regular (your original, unchanged) + SemiBold, Bold, Italic, SemiBoldItalic, BoldItalic
- `woff2/`  web versions of all six
- `kalpurush.scss` / `kalpurush.css`  ready-made @font-face for the whole family
- `specimen.html`  open in a browser to check the fonts and the conjunct stress test
- `source/build_kalpurush.py`  the script that generated them (re-runnable, tweakable)

Install (Windows): select all `ttf/*.ttf` → right-click → Install for all users.
After installing, "Kalpurush" shows Regular / Italic / Bold / Bold Italic as one family;
the two SemiBold styles appear as the family "Kalpurush SemiBold" in apps that don't
read weight-based families (Word), and as weight 600 of "Kalpurush" in browsers/CSS.

CSS: `font-weight: 600` = SemiBold, `700` = Bold, `font-style: italic` = Italic.

How they were made (these are synthetic styles, not hand-drawn)
- Bold/SemiBold: outlines are offset outward. Bengali is thickened by 14/28 units and
  Latin by 17/34 units (per 1000 em), more horizontally than vertically.
- Italic: 12° oblique slant; GPOS mark anchors are slanted with the outlines.
- GSUB/GPOS/cmap are untouched, so reph, conjuncts and matra placement are identical to Regular.
- Hinting tables were removed from the new files (they no longer match the outlines).
- 20 glyphs that were all named ".notdef" in the original were given unique names.
- Tweak the amounts at the top of `build_kalpurush.py` (STYLES, ITALIC_ANGLE, VERT_RATIO), then:
  `pip install fonttools skia-pathops` and `python build_kalpurush.py Kalpurush.ttf out`

License
Kalpurush is under the SIL Open Font License 1.0 (text kept verbatim inside every font).
These are modified versions. The embedded license says nothing about a Reserved Font Name,
but check the copy you downloaded; if it declares one, change FAMILY in the script.
