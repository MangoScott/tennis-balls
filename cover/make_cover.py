#!/usr/bin/env python3
"""Build the YouTube cover image for the Doubles Highlights video.

Reads the four player photos out of "tennis ball pics", removes their
backgrounds, and lays them out as a row of cards under the title.

    pip install pillow rembg[cpu]
    python3 cover/make_cover.py

Writes cover/youtube-cover.png (1280x720) plus the cached cutouts in
cover/cutouts/ so a re-run does not need the segmentation model again.
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICS = os.path.join(ROOT, "tennis ball pics")
OUT_DIR = os.path.join(ROOT, "cover")
CUT_DIR = os.path.join(OUT_DIR, "cutouts")

W, H = 1280, 720          # YouTube thumbnail size
SS = 2                    # supersample, downscaled at the end

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TITLE = "DOUBLES HIGHLIGHTS"
SUBTITLE = "& SOME SINGLES"

# Colour schemes. Pick one with `python3 cover/make_cover.py <name>`; the
# layout is identical in every case, only the palette moves.
THEMES = {
    # Deep grass green, tennis-ball lime accents.
    "grass": dict(deep=(7, 30, 21), night=(5, 18, 30), glow=(92, 176, 74),
                  vignette=(2, 10, 8), card_lo=(17, 52, 38), card_hi=(26, 74, 52),
                  fade=(9, 30, 21), accent=(214, 242, 75), ink=(10, 26, 18),
                  stroke=(6, 22, 14)),
    # Hard court: US Open blue under the same lime.
    "hard": dict(deep=(10, 30, 66), night=(5, 14, 34), glow=(46, 108, 220),
                 vignette=(3, 8, 22), card_lo=(19, 43, 90), card_hi=(30, 62, 124),
                 fade=(8, 20, 48), accent=(214, 242, 75), ink=(9, 20, 44),
                 stroke=(7, 18, 42)),
    # Neutral graphite, lets the lime and the shirts do all the talking.
    "slate": dict(deep=(30, 32, 35), night=(14, 15, 17), glow=(84, 90, 97),
                  vignette=(6, 6, 7), card_lo=(40, 43, 47), card_hi=(57, 61, 66),
                  fade=(18, 19, 21), accent=(214, 242, 75), ink=(18, 20, 14),
                  stroke=(12, 13, 14)),
    # Clay court: terracotta with chalk-line cream.
    "clay": dict(deep=(84, 38, 24), night=(42, 19, 12), glow=(206, 98, 52),
                 vignette=(22, 9, 6), card_lo=(97, 46, 31), card_hi=(128, 63, 42),
                 fade=(44, 19, 12), accent=(246, 238, 224), ink=(58, 26, 16),
                 stroke=(40, 17, 11)),
}
DEFAULT_THEME = "hard"
THEME = THEMES[DEFAULT_THEME]

# Per player: source file, name, and the head measurements (hair top, chin,
# face centre x) taken off the original photo. Head height is what keeps every
# face the same size on the finished card no matter how the photo was framed.
PLAYERS = [
    # Scott is framed off-centre on purpose so the racket over his shoulder
    # stays in the card rather than being clipped by the edge.
    {"file": "me.jpg",     "name": "SCOTT",  "hair": 95, "chin": 455, "cx": 505},
    {"file": "kevin.png",  "name": "KEVIN",  "hair": 25, "chin": 250, "cx": 610},
    {"file": "jimmy.jpg",  "name": "JAMES",  "hair": 65, "chin": 235, "cx": 505},
    {"file": "elijah.png", "name": "ELIJAH", "hair": 90, "chin": 330, "cx": 325},
]

# Card geometry, in final (non-supersampled) pixels.
CARD_W, CARD_GAP = 287, 24
CARD_X0 = (W - (4 * CARD_W + 3 * CARD_GAP)) // 2
CARD_TOP, CARD_BOT = 182, 696
PLATE_H = 62                                  # name plate at the foot of a card
PHOTO_H = (CARD_BOT - CARD_TOP) - PLATE_H
HEAD_MIN, HEAD_MAX, TOP_PAD = 182, 182, 34    # face sizing rules


def s(v):
    """Scale a final-size coordinate into supersampled space."""
    return int(round(v * SS))


def cutouts():
    """Background-free RGBA versions of the four photos, cached on disk."""
    os.makedirs(CUT_DIR, exist_ok=True)
    out = {}
    session = None
    for p in PLAYERS:
        dst = os.path.join(CUT_DIR, p["name"].lower() + ".png")
        if not os.path.exists(dst):
            from rembg import new_session, remove
            if session is None:
                session = new_session("isnet-general-use")
            src = Image.open(os.path.join(PICS, p["file"])).convert("RGBA")
            remove(
                src,
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=250,
                alpha_matting_background_threshold=15,
                alpha_matting_erode_size=8,
            ).save(dst)
        out[p["name"]] = Image.open(dst).convert("RGBA")
    return out


def fit_font(text, target_w, cap=400):
    """Largest font size whether the text still fits inside target_w."""
    lo, hi = 8, cap
    while lo < hi:
        mid = (lo + hi + 1) // 2
        f = ImageFont.truetype(FONT, mid)
        if f.getbbox(text)[2] - f.getbbox(text)[0] <= target_w:
            lo = mid
        else:
            hi = mid - 1
    return ImageFont.truetype(FONT, lo)


def background():
    """Dark court gradient with a lime glow behind the row of players."""
    bg = Image.new("RGB", (s(W), s(H)), THEME["deep"])
    grad = Image.new("L", (1, s(H)))
    for y in range(s(H)):
        grad.putpixel((0, y), int(255 * (y / s(H)) ** 0.85))
    bg = Image.composite(
        Image.new("RGB", bg.size, THEME["night"]), bg, grad.resize(bg.size)
    )

    # Soft lime pool of light sitting behind the cards.
    glow = Image.new("L", (s(W), s(H)), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([s(60), s(190), s(W - 60), s(H + 240)], fill=150)
    gd.ellipse([s(330), s(-260), s(W - 330), s(250)], fill=90)
    glow = glow.filter(ImageFilter.GaussianBlur(s(80)))
    bg = Image.composite(Image.new("RGB", bg.size, THEME["glow"]), bg, glow)

    d = ImageDraw.Draw(bg, "RGBA")

    # Oversized tennis-ball seams, barely there, top corners.
    for cx, cy, r in ((s(-40), s(-60), s(300)), (s(W + 60), s(30), s(340))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 16),
                  width=s(3))
        d.arc([cx - r * 2, cy - r, cx, cy + r], 300, 60,
              fill=(255, 255, 255, 14), width=s(3))

    # Court lines running off toward the horizon.
    d.line([(s(-140), s(760)), (s(452), s(196))], fill=(255, 255, 255, 34), width=s(4))
    d.line([(s(W + 140), s(760)), (s(828), s(196))], fill=(255, 255, 255, 34), width=s(4))
    d.line([(s(300), s(760)), (s(556), s(196))], fill=(255, 255, 255, 18), width=s(3))
    d.line([(s(W - 300), s(760)), (s(724), s(196))], fill=(255, 255, 255, 18), width=s(3))
    d.line([(s(120), s(470)), (s(W - 120), s(470))], fill=(255, 255, 255, 22), width=s(4))
    d.line([(s(250), s(300)), (s(W - 250), s(300))], fill=(255, 255, 255, 14), width=s(3))

    # Vignette to keep the eye on the middle of the frame.
    vig = Image.new("L", (s(W), s(H)), 255)
    ImageDraw.Draw(vig).ellipse([s(-330), s(-250), s(W + 330), s(H + 250)], fill=0)
    vig = vig.filter(ImageFilter.GaussianBlur(s(120)))
    bg = Image.composite(Image.new("RGB", bg.size, THEME["vignette"]), bg, vig)
    return bg.convert("RGBA")


def draw_title(canvas):
    """Headline plus the lime subtitle pill. Returns nothing."""
    title_font = fit_font(TITLE, s(1136))
    d = ImageDraw.Draw(canvas)
    tb = title_font.getbbox(TITLE)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    tx, ty = (s(W) - tw) // 2 - tb[0], s(26) - tb[1]

    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((tx, ty + s(7)), TITLE, font=title_font,
                                fill=(0, 0, 0, 190))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(s(9))))
    d.text((tx, ty), TITLE, font=title_font, fill=(255, 255, 255, 255),
           stroke_width=s(3), stroke_fill=THEME["stroke"] + (255,))

    # Subtitle pill.
    sub_font = ImageFont.truetype(FONT, s(38))
    sb = sub_font.getbbox(SUBTITLE)
    sw, sh = sb[2] - sb[0], sb[3] - sb[1]
    pad_x, pad_y = s(30), s(15)
    pw, ph = sw + pad_x * 2, sh + pad_y * 2
    px, py = (s(W) - pw) // 2, s(26) + th + s(20)
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=ph // 2, fill=THEME["accent"])
    d.text((px + pad_x - sb[0], py + pad_y - sb[1]), SUBTITLE, font=sub_font,
           fill=THEME["ink"])


def player_card(img, p):
    """One rounded card: gradient, cut-out player scaled by head height, name."""
    cw, ch = s(CARD_W), s(CARD_BOT - CARD_TOP)
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))

    # Card backdrop, a touch lighter than the page so faces separate from it.
    back = Image.new("RGBA", (cw, ch), THEME["card_lo"] + (255,))
    top = Image.new("RGBA", (cw, ch), THEME["card_hi"] + (255,))
    ramp = Image.new("L", (1, ch))
    for y in range(ch):
        ramp.putpixel((0, y), int(255 * (y / ch) ** 1.3))
    card.alpha_composite(Image.composite(back, top, ramp.resize((cw, ch))))

    # Scale the player so every face lands at the same size.
    head = p["chin"] - p["hair"]
    reach = (img.height - p["hair"]) / head           # head-heights below the hair
    span = s(PHOTO_H - TOP_PAD)
    head_px = min(max(span / reach, s(HEAD_MIN)), s(HEAD_MAX))
    pad = max(s(TOP_PAD), s(PHOTO_H) - reach * head_px)
    scale = head_px / head

    person = img.resize(
        (max(1, int(img.width * scale)), max(1, int(img.height * scale))),
        Image.LANCZOS,
    )
    # Hair top sits `pad` down the card, face centred left to right.
    ox = int(cw / 2 - p["cx"] * scale)
    oy = int(pad - p["hair"] * scale)

    layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    layer.paste(person, (ox, oy), person)

    # Grounding shadow so the player is not pasted flat onto the card.
    shadow = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 150), (ox + s(6), oy + s(10)), person)
    card.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(s(10))))
    card.alpha_composite(layer)

    # Name plate.
    d = ImageDraw.Draw(card)
    plate_top = ch - s(PLATE_H)
    fade = Image.new("RGBA", (cw, s(70)), (0, 0, 0, 0))
    for y in range(s(70)):
        ImageDraw.Draw(fade).line([(0, y), (cw, y)],
                                  fill=THEME["fade"] + (int(215 * y / s(70)),))
    card.alpha_composite(fade, (0, plate_top - s(70)))
    d.rectangle([0, plate_top, cw, ch], fill=THEME["accent"])

    name_font = fit_font(p["name"], cw - s(36), cap=s(40))
    nb = name_font.getbbox(p["name"])
    d.text(((cw - (nb[2] - nb[0])) // 2 - nb[0],
            plate_top + (s(PLATE_H) - (nb[3] - nb[1])) // 2 - nb[1]),
           p["name"], font=name_font, fill=THEME["ink"])

    # Round the corners and add a hairline edge.
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=s(22),
                                           fill=255)
    card.putalpha(Image.composite(card.getchannel("A"), Image.new("L", (cw, ch), 0),
                                  mask))
    ImageDraw.Draw(card, "RGBA").rounded_rectangle(
        [0, 0, cw - 1, ch - 1], radius=s(22), outline=THEME["accent"] + (70,),
        width=s(2))
    return card


def render(imgs):
    """Compose the whole cover at the current THEME and return it at 1280x720."""
    canvas = background()
    draw_title(canvas)

    for i, p in enumerate(PLAYERS):
        card = player_card(imgs[p["name"]], p)
        x, y = s(CARD_X0 + i * (CARD_W + CARD_GAP)), s(CARD_TOP)

        drop = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        drop.paste((0, 0, 0, 170), (x, y + s(14)), card.getchannel("A"))
        canvas.alpha_composite(drop.filter(ImageFilter.GaussianBlur(s(14))))
        canvas.alpha_composite(card, (x, y))

    return canvas.convert("RGB").resize((W, H), Image.LANCZOS)


def main(argv):
    global THEME
    names = argv[1:] or [DEFAULT_THEME]
    if names == ["all"]:
        names = list(THEMES)

    imgs = cutouts()
    for name in names:
        THEME = THEMES[name]
        out = render(imgs)
        stem = "youtube-cover" if name == DEFAULT_THEME else "youtube-cover-" + name
        path = os.path.join(OUT_DIR, stem + ".png")
        out.save(path, optimize=True)
        out.save(os.path.join(OUT_DIR, stem + ".jpg"), quality=92, subsampling=0)
        print("wrote", path, out.size)


if __name__ == "__main__":
    import sys
    main(sys.argv)
