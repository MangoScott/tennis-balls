#!/usr/bin/env python3
"""Generate YouTube thumbnail candidates (1280x720) from the court photos.

Usage:  python3 make_thumbnails.py            # writes out/*.png + out/contact-sheet.png
Requires: pillow  (pip install pillow)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

HERE = Path(__file__).parent
SRC, FONTS, OUT = HERE / "src", HERE / "fonts", HERE / "out"
W, H = 1280, 720

YELLOW = (223, 255, 79)      # tennis-ball optic yellow
WHITE = (255, 255, 255)
NAVY = (12, 22, 48)
RED = (227, 24, 55)
BLACK = (0, 0, 0)


def load(name):
    img = Image.open(SRC / name)
    if name == "forehand.jpg":  # trim the iPhone video scrub bar off the bottom
        img = img.crop((0, 0, img.width, img.height - 90))
    return img


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def cover(img, w, h, fx=0.5, fy=0.5):
    """Scale-and-crop img to exactly w x h, keeping the focal point (fx, fy)."""
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = int((img.width - w) * fx)
    y = int((img.height - h) * fy)
    return img.crop((x, y, x + w, y + h))


def gradient(w, h, color, start=0.0, end=1.0, direction="down", max_alpha=230):
    """Linear alpha gradient of `color`, transparent at `start` and max_alpha at `end`."""
    layer = Image.new("RGBA", (w, h), color + (0,))
    px = layer.load()
    n = h if direction in ("down", "up") else w
    for i in range(n):
        t = i / max(n - 1, 1)
        if direction in ("up", "left"):
            t = 1 - t
        a = 0 if t < start else (max_alpha if t > end else int(max_alpha * (t - start) / (end - start)))
        if direction in ("down", "up"):
            for x in range(w):
                px[x, i] = color + (a,)
        else:
            for y in range(h):
                px[i, y] = color + (a,)
    return layer


def text_block(draw, xy, text, fnt, fill, stroke=0, stroke_fill=BLACK, shadow=True):
    x, y = xy
    if shadow:
        draw.text((x + 6, y + 8), text, font=fnt, fill=(0, 0, 0, 160), stroke_width=stroke, stroke_fill=(0, 0, 0, 160))
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def pill(draw, xy, text, fnt, bg, fg, pad=(28, 12), radius=999):
    x, y = xy
    l, t, r, b = draw.textbbox((0, 0), text, font=fnt)
    tw, th = r - l, b - t
    box = (x, y, x + tw + pad[0] * 2, y + th + pad[1] * 2)
    draw.rounded_rectangle(box, radius=radius, fill=bg)
    draw.text((x + pad[0] - l, y + pad[1] - t), text, font=fnt, fill=fg)
    return box


def tennis_ball(size):
    """A simple flat tennis-ball glyph as an RGBA image."""
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, s - 1, s - 1), fill=YELLOW)
    # seam: two arcs from circles centred outside the ball, clipped to the ball
    lw = s // 13
    seam = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sd = ImageDraw.Draw(seam)
    sd.arc((-s * 1.0, -s * 0.15, s * 0.3, s * 1.15), 300, 60, fill=WHITE, width=lw)
    sd.arc((s * 0.7, -s * 0.15, s * 2.0, s * 1.15), 120, 240, fill=WHITE, width=lw)
    clip = Image.new("L", (s, s), 0)
    ImageDraw.Draw(clip).ellipse((lw, lw, s - 1 - lw, s - 1 - lw), fill=255)
    im.paste(seam, (0, 0), Image.composite(seam.split()[3], Image.new("L", (s, s), 0), clip))
    # shading
    shade = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(shade).ellipse((s * 0.15, s * 0.15, s * 1.1, s * 1.1), fill=(0, 0, 0, 70))
    shade = shade.filter(ImageFilter.GaussianBlur(s // 12))
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
    im = Image.alpha_composite(im, Image.composite(shade, Image.new("RGBA", (s, s), (0, 0, 0, 0)), mask))
    return im.resize((size, size), Image.LANCZOS)


def rounded_photo(img, w, h, radius, border=8, border_color=WHITE, fx=0.5, fy=0.5):
    ph = cover(img, w, h, fx, fy).convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    out = Image.new("RGBA", (w + border * 2, h + border * 2), (0, 0, 0, 0))
    ImageDraw.Draw(out).rounded_rectangle((0, 0, out.width - 1, out.height - 1), radius=radius + border, fill=border_color)
    out.paste(ph, (border, border), mask)
    return out


def add_shadow(canvas, layer, pos, blur=18, offset=(0, 14), alpha=150):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, alpha), (0, 0), layer.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (pos[0] + offset[0], pos[1] + offset[1]))
    canvas.alpha_composite(layer, pos)


def punch(img, contrast=1.15, color=1.2, sharp=1.2):
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(color)
    return ImageEnhance.Sharpness(img).enhance(sharp)


# ---------------------------------------------------------------- concepts

def concept_a_action():
    """Full-bleed forehand shot, huge '7+ SHOT RALLIES' bottom-left, team selfie inset."""
    bg = punch(cover(load("forehand.jpg"), W, H, 0.5, 0.55)).convert("RGBA")
    bg.alpha_composite(gradient(W, H, NAVY, 0.35, 1.0, "down", 235))
    bg.alpha_composite(gradient(W, H, NAVY, 0.0, 0.55, "left", 120))
    d = ImageDraw.Draw(bg)

    pill(d, (56, 54), "RAW COMMENTARY", font("BebasNeue.ttf", 40), RED, WHITE)

    big = font("Anton.ttf", 180)
    text_block(d, (48, 262), "7+ SHOT", big, YELLOW, stroke=6)
    text_block(d, (48, 422), "RALLIES", big, WHITE, stroke=6)
    pill(d, (56, 640), "TEAM SINGLES  •  CINCY OPEN COURTS", font("BebasNeue.ttf", 38), YELLOW, NAVY, pad=(22, 8))

    inset = rounded_photo(load("team-selfie.jpg"), 400, 300, 26, fx=0.55, fy=0.35)
    inset = inset.rotate(4, resample=Image.BICUBIC, expand=True)
    add_shadow(bg, inset, (W - inset.width - 30, 50))
    bg.alpha_composite(tennis_ball(96), (W - 120, 400))
    return bg.convert("RGB")


def concept_b_squad():
    """Team selfie is the hero (faces sell clicks); title stacked in the dusk sky."""
    bg = punch(cover(load("team-selfie.jpg"), W, H, 0.5, 0.0), 1.1, 1.15).convert("RGBA")
    bg.alpha_composite(gradient(W, H, BLACK, 0.45, 1.0, "down", 215))
    d = ImageDraw.Draw(bg)

    box = pill(d, (48, 40), "RAW COMMENTARY", font("BebasNeue.ttf", 44), RED, WHITE)
    pill(d, (box[2] + 16, 40), "CINCY OPEN COURTS", font("BebasNeue.ttf", 44), YELLOW, NAVY)

    big = font("Anton.ttf", 150)
    text_block(d, (48, 430), "7+ SHOT RALLIES", big, YELLOW, stroke=8)
    text_block(d, (52, 590), "TEAM SINGLES", font("Anton.ttf", 92), WHITE, stroke=6)
    return bg.convert("RGB")


def concept_c_split():
    """Left: dusk stadium column. Right: forehand action. Giant '7+' as the hook."""
    canvas = Image.new("RGBA", (W, H), NAVY + (255,))
    left_w = 470
    left = punch(cover(load("stadium-dusk.jpg"), left_w, H, 0.5, 0.38)).convert("RGBA")
    right = punch(cover(load("forehand.jpg"), W - left_w + 40, H, 0.62, 0.6)).convert("RGBA")
    canvas.alpha_composite(right, (left_w - 40, 0))
    # diagonal divider: mask the left photo with a slanted edge
    mask = Image.new("L", (left_w, H), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (left_w, 0), (left_w - 70, H), (0, H)], fill=255)
    canvas.paste(left, (0, 0), mask)
    d = ImageDraw.Draw(canvas)
    d.line([(left_w + 4, -4), (left_w - 66, H + 4)], fill=YELLOW, width=14)

    canvas.alpha_composite(gradient(W, H, BLACK, 0.5, 1.0, "down", 210))
    d = ImageDraw.Draw(canvas)

    text_block(d, (30, 30), "7+", font("Anton.ttf", 300), YELLOW, stroke=8)
    text_block(d, (44, 335), "SHOT", font("Anton.ttf", 120), WHITE, stroke=6)
    text_block(d, (44, 455), "RALLIES", font("Anton.ttf", 120), WHITE, stroke=6)

    box = pill(d, (560, 44), "RAW COMMENTARY", font("BebasNeue.ttf", 40), RED, WHITE)
    pill(d, (box[2] + 16, 44), "CINCY OPEN COURTS", font("BebasNeue.ttf", 40), YELLOW, NAVY)
    d.text((48, 606), "TEAM SINGLES", font=font("BebasNeue.ttf", 54), fill=WHITE, stroke_width=4, stroke_fill=BLACK)
    canvas.alpha_composite(tennis_ball(110), (W - 150, 300))
    return canvas.convert("RGB")


def contact_sheet(paths):
    thumbs = [Image.open(p).resize((640, 360), Image.LANCZOS) for p in paths]
    sheet = Image.new("RGB", (640 * 2 + 60, 360 * 2 + 60), (30, 30, 30))
    for i, t in enumerate(thumbs):
        sheet.paste(t, (20 + (i % 2) * 660, 20 + (i // 2) * 380))
    return sheet


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    made = []
    for name, fn in [("A-action", concept_a_action), ("B-squad", concept_b_squad), ("C-split", concept_c_split)]:
        p = OUT / f"{name}.png"
        img = fn()
        img.save(p, optimize=True)
        img.save(p.with_suffix(".jpg"), quality=90, optimize=True)
        made.append(p)
        print("wrote", p, "and", p.with_suffix(".jpg"))
    contact_sheet(made).save(OUT / "contact-sheet.png")
    print("wrote", OUT / "contact-sheet.png")
