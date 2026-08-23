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
| `png/avatar-photo-ring-800.png` | **Use this as the profile picture.** The portrait, treated. |
| `mark-avatar.svg` | The block as an avatar, for later. Inset so a circle crop takes nothing off the line ends. |
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

The face stays in the circle; the logo does not go there. YouTube prints the
channel name in text beside the avatar everywhere it appears, so a wordmark in
that slot is the same words twice in 48 pixels — and the channel is a person
doing a thing.

`png/avatar-photo-*.png` is `tennis ball pics/me.jpg`, treated to match:
a 480px crop of the 1080px source at `(350, 60)`, greyscale, contrast `1.9`,
brightness `1.05`, and everything outside the inscribed circle painted white
(the circle crop removes it anyway, and it keeps the square clean). The `-ring`
files add a black ring so the white ground still has an edge on a light UI —
that's the one to upload.

Kruger's work is black-and-white photography with Futura on top. A hard mono
portrait isn't a compromise with this identity; it's the other half of it.

Switch to `mark-avatar.svg` only when guests' names start out-pulling yours in
your own video titles.

## Scale

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
