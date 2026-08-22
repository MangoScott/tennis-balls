# @scottplaystennis — marks

Three directions, all built from the same drawn element: one sinusoidal seam,
the line you actually see on a ball at three-quarters.

| File | What it is |
| --- | --- |
| `avatar-ball.svg` | **A — avatar cut.** Ball bleeds to the edge, so a circle crop loses nothing. Use this one for profile pictures. |
| `mark-ball.svg` | A, padded, for placing on a page next to other things. |
| `mark-ball-flat.svg` | A in two flat colours — embroidery, stickers, one-colour print. |
| `mark-can.svg` | B — three balls behind a tin, on court blue. |
| `mark-badge.svg` | C — club crest with the handle set around the ring. |
| `lockup.svg` | Mark + handle, dark type for light grounds. |
| `lockup-dark.svg` | Mark + handle, reversed for dark grounds. |
| `banner.svg` | Header, 1500×500. |
| `favicon.svg` | Tab icon — seam scaled up so it survives 16px. |
| `png/` | Rendered PNGs. |

## Palette

| | Hex | Role |
| --- | --- | --- |
| Optic | `#CFE04A` | Felt. The only saturated colour in the system. |
| Court | `#0E4F7A` | Hard-court blue. Plates, banners. |
| Baseline | `#10301F` | Deep court green. Badge ground. |
| Chalk | `#FFFFFF` | Seams and reversed type. |
| Ink | `#1D1D1F` | Wordmark on light ground. |

Optic is the same green as the mark already in the `index.html` header, so the
tier list and the accounts stay one family.

## Type

The wordmark is Inter SemiBold at −2% tracking, with a
`-apple-system / SF Pro` fallback — close enough that the site header and the
wordmark read as one thing. The SVGs reference the font by name rather than
carrying outlines; if you need files with no font dependency, convert the text
to paths in Figma or Illustrator (Type → Create Outlines).

## Regenerating the PNGs

The SVGs are the masters — render at whatever size you need. With Chrome:

```sh
chrome --headless --screenshot=out.png --window-size=1024,1024 \
       --default-background-color=00000000 avatar-ball.svg
```

Chrome adds blank rows below the artwork when the window is taller than the
image, so render into a page that sizes the `<img>` exactly, or crop after.
