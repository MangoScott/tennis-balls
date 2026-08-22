# scottplaystennis

One circle. One cut.

A tennis ball is two identical pieces. The mark is that fact and nothing
else: a disc divided by a single curve into two congruent panels, each one
the other turned a half turn. The curve is not drawn on the disc — it is
missing from it, so there is no white line, no outline, no gradient and no
shadow, and whatever sits behind the mark shows through.

## Construction

Two circular arcs of one radius, meeting at the centre of the disc with a
shared tangent, so the curve passes through without a corner.

| | |
| --- | --- |
| Rise | `0.340 R` |
| Arc radius | `0.5377 R` — follows from the rise, `(0.25 + rise²) / (2 · rise)` |
| Arc centres | `(±R/2, ∓0.1977 R)` |
| Cut | `5.1%` of the diameter (`8.6%` in the tight cut) |
| Rotation | 180°, exact |

Nothing here was nudged by eye. Change the rise and everything else follows.

## Colour

| | Hex | |
| --- | --- | --- |
| Optic | `#D2F034` | The mark. The only saturated colour in the system. |
| Ink | `#0B0B0C` | Type, reversed grounds. |
| Paper | `#FAFAF8` | Light grounds, reversed mark. |

One colour at a time — the mark is never two-tone.

## Files

| File | What it is |
| --- | --- |
| `mark.svg` | **Primary.** Optic disc, cut transparent. This is the avatar. |
| `mark-ink.svg` | Ink disc, for light grounds where the optic is too loud. |
| `mark-paper.svg` | Reversed, for ink grounds. |
| `mark-tight.svg` | Cut widened to 8.6%, for 32px and below. |
| `mark-square.svg` | Optic on ink, square, for platforms that don't crop to a circle. |
| `favicon.svg` | Tab icon. |
| `wordmark.svg` | `scottplaystennis`, two weights, ink. |
| `wordmark-paper.svg` | Reversed. |
| `wordmark-at.svg` | With a dimmed `@`, where the handle needs to read as a handle. |
| `lockup.svg` | Mark and wordmark, ink type. |
| `lockup-paper.svg` | Mark and wordmark, reversed. |
| `banner.svg` | Header, 1500×500. |
| `png/` | Rendered PNGs at the sizes the platforms ask for. |

## Wordmark

Seventeen characters and no room for a space, so weight does the work a
space would: **scott** at 600, `playstennis` at 400, tracked −2.2%. Set in
Instrument Sans, called by name rather than converted to outlines — if you
need files with no font dependency, open them in Figma or Illustrator and
run Type → Create Outlines.

## Regenerating

The SVGs are the masters; render at any size. `scratchpad/export.sh` in the
session used headless Chrome, which appends blank rows when the window is
taller than the image — render into a page that sizes the `<img>` exactly,
then trim.
