"""Build the image assets used by make_cover.py.

  python3 prep_assets.py

Reads the photos in "../tennis ball pics" and writes into assets/:
  kevin_cut.png  Kevin with his white studio background flood-filled away
  kevin_top.png  the head-to-thumbs-up crop actually used on the cover
  bg.jpg         the match court photo, cropped 16:9, blurred and darkened
  scott.jpg      Scott's photo, cropped and graded to match Kevin

Requires: pillow
"""
from collections import deque
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = Path(__file__).parent
SRC = HERE.parent / "tennis ball pics"
OUT = HERE / "assets"
OUT.mkdir(exist_ok=True)

WHITE = 238  # anything this bright on a border-connected run is backdrop


def cut_white_background(img):
    """Alpha mask from the white studio backdrop, flood-filled in from the
    borders so Kevin's white shorts survive."""
    w, h = img.size
    px = img.load()
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()

    def is_bg(p):
        return p[0] >= WHITE and p[1] >= WHITE and p[2] >= WHITE

    seen = bytearray(w * h)
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not seen[y * w + x] and is_bg(px[x, y]):
                seen[y * w + x] = 1
                dq.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not seen[y * w + x] and is_bg(px[x, y]):
                seen[y * w + x] = 1
                dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        ap[x, y] = 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and is_bg(px[nx, ny]):
                seen[ny * w + nx] = 1
                dq.append((nx, ny))
    # erode a pixel then feather, so no white fringe survives the composite
    return alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))


# ---- Kevin ----------------------------------------------------------------
kev = Image.open(SRC / "kevin.png").convert("RGB")
alpha = cut_white_background(kev)
kev = kev.convert("RGBA")
kev.putalpha(alpha)
kev = kev.crop(alpha.getbbox())
kev.save(OUT / "kevin_cut.png")
# head through the thumbs-up: keeps his face as big as Scott's
kev.crop((0, 0, kev.width, 740)).save(OUT / "kevin_top.png")

# ---- background: their actual court --------------------------------------
bg = Image.open(SRC / "IMG_8524.jpg").convert("RGB")
bg = ImageOps.fit(bg, (1280, 720), method=Image.LANCZOS, centering=(0.5, 0.42))
bg = bg.filter(ImageFilter.GaussianBlur(7))
bg = ImageEnhance.Color(bg).enhance(1.25)
bg = ImageEnhance.Brightness(bg).enhance(0.55)
bg.save(OUT / "bg.jpg", quality=95)

# ---- Scott ---------------------------------------------------------------
scott = Image.open(SRC / "me.jpg").convert("RGB").crop((60, 0, 1080, 1040))
scott = ImageEnhance.Color(scott).enhance(1.15)
scott = ImageEnhance.Contrast(scott).enhance(1.12)
scott = ImageEnhance.Brightness(scott).enhance(1.06)
scott = scott.filter(ImageFilter.UnsharpMask(radius=2.4, percent=95, threshold=3))
scott.save(OUT / "scott.jpg", quality=95)

print("wrote", ", ".join(sorted(p.name for p in OUT.iterdir())))
