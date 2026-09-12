# Wilson US Open review – YouTube thumbnails

Three 1280x720 thumbnail options for the Wilson US Open ball review video.

- `out/option-a-worth-it.png` – Scott left, "WILSON US OPEN / WORTH IT?", ball and cut-open half.
- `out/option-b-rank.png` – court background, S–F tier row with a "?" tile, "WHERE DOES IT RANK?".
- `out/option-c-cut-open.png` – yellow diagonal band, "WE CUT IT OPEN", ball and half.

JPG versions sit next to each PNG (all under YouTube's 2 MB limit).

Each option is a plain HTML file styled by `base.css`. Edit the text or positions,
then run `./render.sh` (needs Chromium and Python Pillow) to regenerate `out/`.
Assets in `assets/` are cut out from `tennis ball pics/me.jpg` and frames of the video.
Fonts (Anton, Archivo Black, Barlow Condensed) are from Google Fonts under the Open Font License.
