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
| `mark-avatar.svg` | **Use this as the profile picture.** Block inset so a circle crop takes nothing off the line ends. |
| `mark-avatar-invert.svg` | The same, reversed. |
| `mark.svg` | Primary, edge to edge. White on black. |
| `mark-invert.svg` | Black on white. |
| `mark-compact.svg` | `SCOTT.` — one line, one period, for 32px and below. |
| `favicon.svg` | Tab icon. |
| `wordmark.svg` | One justified line, for anywhere with width and no height. |
| `wordmark-invert.svg` | Reversed. |
| `x.svg` | The green X. |
| `banner.svg` | Header, 1500×500. |
| `png/` | Rendered PNGs. |

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
