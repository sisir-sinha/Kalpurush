# Kalpurush — কালপুরুষ

> A free, open-source **Bengali display typeface** with six styles —
> **Regular, SemiBold, Bold** and their **Italics** — generated from
> [Kalpurush Regular v0.258](https://github.com/sisir-sinha/Kalpurush) by
> **Tanbin Islam Siyam** (Avro Font Development Project).
> Licensed under the **SIL Open Font License 1.0** — free for personal and commercial use.

[![Open-source](https://img.shields.io/badge/license-SIL_OFL_1.0-49b07a)](https://scripts.sil.org/OFL)
[![Fonts](https://img.shields.io/badge/styles-6-d8a64a)](specimen.html)
[![Web-ready](https://img.shields.io/badge/web-woff2+ttf+CDN-6ea8e8)](kalpurush.cdn.css)

---

## Documentation

- **Interactive specimen & documentation — [`specimen.html`](specimen.html)**
  Open it in a browser: all six styles, the conjunct/matra stress test, a **free WYSIWYG
  editor** (type and format text in-place — weight, italic, size, line height, tracking,
  color — and export the result as ready-to-use HTML), the full character set, metrics,
  and install guides. Fonts load from the **CDN** (`kalpurush.cdn.css`), so it works on any host.
- **Homepage — [`index.html`](index.html)**
  Landing page for the Jekyll/GitHub Pages site. It links straight to the specimen.
- **CDN stylesheet — [`kalpurush.cdn.css`](kalpurush.cdn.css)**
  One `<link>` loads all six styles from jsDelivr (mirrors this repo). Use this in any
  website or documentation.
- **Local stylesheets — [`kalpurush.css`](kalpurush.css) / [`kalpurush.scss`](kalpurush.scss)**
  Same @font-face rules with relative paths, for self-hosted fonts.

> GitHub Pages (Jekyll): push this repo to GitHub and the workflow in
> [`.github/workflows/jekyll-gh-pages.yml`](.github/workflows/jekyll-gh-pages.yml) builds and
> deploys the site — the homepage (`index.html`) links to the full specimen.

---

## The family — six styles

| Style | File (`ttf/` · `woff2/`) | CSS weight | Italic |
|---|---|---|---|
| Regular | `Kalpurush-Regular` | 400 | — |
| SemiBold | `Kalpurush-SemiBold` | 600 | — |
| Bold | `Kalpurush-Bold` | 700 | — |
| Italic | `Kalpurush-Italic` | 400 | ✓ |
| SemiBold Italic | `Kalpurush-SemiBoldItalic` | 600 | ✓ |
| Bold Italic | `Kalpurush-BoldItalic` | 700 | ✓ |

All six share the **identical outlines, metrics and OpenType layout tables** as the original
Regular — only weight and slant change. Bengali shaping (reph, conjuncts, matras) is preserved
exactly.

## Quick start — web (CDN)

```html
<link rel="stylesheet" href="kalpurush.cdn.css">
<style>
  body { font-family: "Kalpurush", serif; font-weight: 600; }
</style>
```

That's it — no font files to host. `kalpurush.cdn.css` references jsDelivr, which serves the
woff2/ttf files directly from this repository.

## Quick start — install locally

1. **Windows:** select all `ttf/*.ttf` → right-click → **Install for all users**
2. **macOS:** open `ttf/*.ttf` in Font Book → **Install Font**
3. **Linux:** copy to `~/.local/share/fonts` → `fc-cache -f`

After installing, “Kalpurush” appears as **one family** — Regular / Italic / Bold / Bold Italic.
The two SemiBold styles show up as a separate family **“Kalpurush SemiBold”** in apps that don’t
read weight-based families (e.g. Word), and as weight `600` of “Kalpurush” in browsers/CSS.

```css
font-weight: 600;            /* SemiBold */
font-weight: 700;            /* Bold */
font-style: italic;          /* Italic */
```

## Character coverage

Measured from the font binaries — identical for all six styles:

- **586 glyphs**, 210 codepoints in the Unicode map
- **91 Bengali characters** (U+0980–U+09FF): all vowels + vowel signs, conjunct marks,
  Bengali digits **০–৯**, ৰ ৱ ৲ and the Bengali rupee sign **৳**
- **95 printable Latin characters** (U+0020–U+007E)
- Punctuation: en/em dash, quotes, ellipsis, minus sign, ZWJ/ZWNJ, combining dotted circle

## How the styles were made

SemiBold, Bold and Italic are **synthetic styles** (outline-level, not hand-drawn), produced by
[`source/build_kalpurush.py`](source/build_kalpurush.py):

- **Bold / SemiBold** — every outline is offset outward (skia-pathops stroke + union).
  Bengali is thickened by 14/28 units and Latin by 17/34 units per 1000 em (more horizontally
  than vertically), because Bengali stems are thinner than the Latin stems.
- **Italic** — a 12° oblique skew about the baseline; GPOS mark anchors are skewed with the
  outlines so matra placement stays correct.
- **GSUB / GPOS / GDEF / cmap are untouched** — shaping is identical to Regular.
- Hinting tables are removed (they no longer match the outlines); grayscale rendering only.
- 20 glyphs that were all named `.notdef` in the original were given unique names.

Tweak `STYLES`, `ITALIC_ANGLE` or `VERT_RATIO` at the top of the script, then:

```bash
pip install fonttools skia-pathops brotli
python source/build_kalpurush.py Kalpurush.ttf out
```

## Repo layout

```
Kalpurush/
├── index.html          ← Jekyll homepage (links to the specimen)
├── specimen.html       ← interactive specimen, sandbox & documentation
├── kalpurush.cdn.css   ← @font-face via jsDelivr CDN
├── kalpurush.css       ← @font-face with local paths
├── kalpurush.scss      ← Sass source (configurable font path)
├── preview.png         ← preview image
├── ttf/                ← 6 TrueType files
├── woff2/              ← 6 web-optimized files
├── source/
│   └── build_kalpurush.py   ← re-runnable style generator
└── .github/workflows/jekyll-gh-pages.yml   ← GitHub Pages deploy
```

## License

Kalpurush is under the **SIL Open Font License 1.0** (the license text is embedded verbatim in
every font). These are modified versions of the original.

- The fonts declare **no Reserved Font Name** — derivatives may keep using the name “Kalpurush”.
  (If you download a copy from elsewhere, check the embedded license; if it declares an RFN,
  change `FAMILY` in `source/build_kalpurush.py`.)
- Free to use, study, modify and redistribute — including commercial work — under OFL 1.0.

## Credits

- **Kalpurush Regular v0.258** — Tanbin Islam Siyam, Avro Font Development Project
  (<http://www.omicronlab.com>)
- SemiBold / Bold / Italic variants — synthetic styles generated with
  fonttools + skia-pathops
- OFL FAQ: <http://scripts.sil.org/OFL>
