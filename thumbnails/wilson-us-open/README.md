# Wilson US Open review – YouTube thumbnails

Thumbnails for the Wilson US Open ball review video (1280x720).

**Final pick: `final-thumbnail.png`** (same as `out/option-d-best-ball.png`) – tier row with a glowing S tile,
"BEST BALL EVER?" headline, ball and cut-open half, court footage behind Scott.

Earlier options kept for reference:

- `out/option-a-worth-it.png` – Scott left, "WILSON US OPEN / WORTH IT?", ball and cut-open half.
- `out/option-b-rank.png` – court background, S–F tier row with a "?" tile, "WHERE DOES IT RANK?".
- `out/option-c-cut-open.png` – yellow diagonal band, "WE CUT IT OPEN", ball and half.
- `out/option-d-best-ball.png` – the final pick described above.

JPG versions sit next to each PNG (all under YouTube's 2 MB limit).

Each option is a plain HTML file styled by `base.css`. Edit the text or positions,
then run `./render.sh` (needs the Playwright Chromium headless shell and Python Pillow) to regenerate `out/`.
Assets in `assets/` are cut out from `tennis ball pics/me.jpg` and frames of the video.
Fonts (Anton, Archivo Black, Barlow Condensed) are from Google Fonts under the Open Font License.
