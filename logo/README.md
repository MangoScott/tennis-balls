# SCOTT PLAYS TENNIS

The name is the logo. No symbol, no ball, no container.

SCOTT, PLAYS, TENNIS — five, five and six characters. Stacked and forced to a
single measure they close into a solid rectangle, and that rectangle is the
mark. Read it as a shape first and a name second.

Black and white only. The green appears once, as the X, and never inside the
mark.

## Specification

| | |
| --- | --- |
| Lines | 3 |
| Characters | 5 / 5 / 6 |
| Measure | identical, forced (`textLength` + `lengthAdjust="spacingAndGlyphs"`) |
| Leading | `1.02 ×` cap height, set solid |
| Condensed to | ~58% of the natural width |
| Type | Jost 700 (a Futura revival), cap height `0.7031 em` |
| Ink | `#000000` |
| Paper | `#FFFFFF` |
| Green | `#2FD95B` — the X only |

## Files

| File | What it is |
| --- | --- |
| `png/avatar-ring-800.png` | **Use this as the profile picture.** The block, with a keyline. |
| `mark-avatar-ring.svg` | The avatar. Keyline so it holds an edge in light and dark mode. |
| `mark-avatar.svg` | The same block, no keyline. |
| `watermark.svg` | White block on nothing — video watermark, thumbnails. |
| `png/avatar-photo-800.png` | The portrait, reframed. About page, thumbnails, press. |
| `mark-avatar-invert.svg` | The same, reversed. |
| `mark.svg` | Primary, edge to edge. White on black. |
| `mark-invert.svg` | Black on white. |
| `mark-compact.svg` | `SCOTT.` — one line, one period, for 32px and below. |
| `favicon.svg` | Tab icon. |
| `wordmark.svg` | One justified line, for anywhere with width and no height. |
| `wordmark-invert.svg` | Reversed. |
| `x.svg` | The green X. |
| `banner*.svg` | X / Twitter header, 1500×500. |
| `youtube*.svg` | YouTube channel art, 2560×1440. |
| `png/` | Rendered PNGs. |

## Headers

The block never changes. Only the right-hand column does, and it can be empty:

| Suffix | Line |
| --- | --- |
| *(none)* | EVERY PLAYER. EVERY LEVEL. EVERY COURT. I MEAN EVERYONE. |
| `-you` | YOU PLAY. I PLAY YOU. I MEAN YOU. |
| `-gear` | RACQUETS. STRINGS. SHOES. GRIPS. BALLS. COURTS. I MEAN ALL OF IT. |
| `-plain` | *nothing — block and X only* |

Each exists at both sizes: `banner-gear.svg` / `youtube-gear.svg`, and so on.

### YouTube crops hard

Upload **2560×1440**. Televisions show all of it; desktop shows a 2560×423
band; phones show only a centred **1546×423** box. Every element in
`youtube*.svg` sits inside that box, so nothing is lost on a phone.
`youtube-safe-areas.svg` draws the guides — it is a reference, not an asset.
The exported PNGs are under 130 KB, well inside YouTube's 6 MB limit.

## The avatar

The block goes in the circle. The channel name does sit beside the avatar as
text, but it's small grey type people skim; a mark is a shape they learn
without reading, and it compounds every scroll.

It holds small because the block is distinctive as a **silhouette** — three
stacked bars, flush on both edges. At 40px nobody reads the words, they
recognise the shape, which is the job. `mark-compact.svg` takes over at
favicon sizes.

**The keyline is structural, not decorative.** A black disc disappears into
YouTube's dark mode and a white one disappears into light mode, and you only
get to upload one file. A white ring just inside the crop (r=247, 10px) gives
the mark an edge either way. Block inset to 330px of the 512px box so the ring
has room; without the ring, `mark-avatar.svg` runs the block at 348.

`png/avatar-photo-800.png` stays in the repo: `me.jpg` reframed to a 560px
window at `(285, 40)`, slight saturation and contrast lift, colour kept. It
belongs on the about page, in thumbnails, and anywhere with room for a person.

## Scale## Scale

The three-line block holds down to about 48px. Below that the lines merge into
three bars, so `mark-compact.svg` takes over — same type, one word.

## The X

One green mark in an otherwise binary system, taken from the struck-through
words on the wall. It has a job: the stamp for a can that doesn't make the cut.
Use it on a can, on a tier, on a word. Never on the logo.

## Type

Set in Jost, called by name rather than converted to outlines. For files with
no font dependency, open them in Figma or Illustrator and run
Type → Create Outlines.

## Regenerating

The SVGs are the masters. Line positions come from the measured cap height
(`0.7031 em`), not from `line-height` — every line is placed on an explicit
baseline and stretched to the measure, so the block stays solid at any size.

If you re-render the PNGs with headless Chrome, note that it paints only
`window_height − 88` rows and pads the rest of the screenshot with unpainted
pixels. Render into a window at least 88px taller than the image and crop back
down, or the last rows of every export come out transparent.
