"""Render the YouTube cover (1280x720 + 2x) for Scott vs Kevin.

  python3 prep_assets.py                       # once, builds assets/
  python3 make_cover.py                        # -> cover-scott-vs-kevin.png
  python3 make_cover.py "FULL MATCH" alt-name  # custom sub-headline / filename

Composites assets/ into an HTML page (fonts and images inlined as data URIs)
and screenshots it with headless Chromium at 2x, then downsamples for crispness.

Requires: pillow, a Chromium/Chrome binary, and the two display fonts:
  npm install @fontsource/anton @fontsource/barlow-condensed
(without them it falls back to whatever bold sans is installed)
"""
import base64
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
BUILD = HERE / "build"
BUILD.mkdir(exist_ok=True)

SUB = sys.argv[1] if len(sys.argv) > 1 else "WHO WINS?"
NAME = sys.argv[2] if len(sys.argv) > 2 else "cover-scott-vs-kevin"

FONTS = {
    "__ANTON__": "node_modules/@fontsource/anton/files/anton-latin-400-normal.woff2",
    "__BARLOW__": "node_modules/@fontsource/barlow-condensed/files/"
                  "barlow-condensed-latin-700-normal.woff2",
}
CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("no Chromium/Chrome found - set CHROME=/path/to/chrome")


HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Anton;src:url(data:font/woff2;base64,__ANTON__) format('woff2');}
@font-face{font-family:BarlowC;font-weight:700;src:url(data:font/woff2;base64,__BARLOW__) format('woff2');}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#05140c}
.stage{position:relative;width:1280px;height:720px;overflow:hidden;
  font-family:BarlowC,'Liberation Sans',Arial,sans-serif}

/* ---------- background: their actual court, blurred + darkened ---------- */
.bg{position:absolute;inset:-4%;background:url(data:image/jpeg;base64,__BG__) center/cover}
.bg-tint{position:absolute;inset:0;
  background:radial-gradient(110% 85% at 50% 58%, rgba(4,30,16,.55) 0%, rgba(2,14,9,.90) 68%, #010c07 100%)}

/* ---------- player panels, split by one diagonal ---------- */
.panel{position:absolute;top:0;height:720px;overflow:hidden;z-index:2}
.left{left:0;width:702px;clip-path:polygon(0 0, 100% 0, calc(100% - 116px) 100%, 0 100%)}
.right{right:0;width:702px;clip-path:polygon(116px 0, 100% 0, 100% 100%, 0 100%)}

.left .photo{position:absolute;left:-30px;top:0;width:760px;height:720px;
  background:url(data:image/jpeg;base64,__SCOTT__) 46% 4%/cover;
  filter:saturate(1.08) contrast(1.05) brightness(1.05)}
.left .grade{position:absolute;inset:0;
  background:radial-gradient(52% 46% at 42% 31%, rgba(0,0,0,0) 32%, rgba(3,20,44,.60) 74%, rgba(2,12,30,.90) 100%),
             linear-gradient(100deg, rgba(10,58,120,.16) 0%, rgba(4,22,52,.24) 50%, rgba(1,12,8,.92) 100%),
             linear-gradient(0deg, rgba(1,10,6,.88) 0%, rgba(0,0,0,0) 40%)}
.right .fill{position:absolute;inset:0;
  background:linear-gradient(260deg, rgba(26,116,58,.30) 0%, rgba(9,58,32,.34) 52%, rgba(1,12,8,.94) 100%),
             linear-gradient(0deg, rgba(1,10,6,.85) 0%, rgba(0,0,0,0) 38%)}

/* the bright seam on the diagonal */
.seam{position:absolute;left:637px;top:-60px;width:10px;height:840px;z-index:4;
  background:linear-gradient(180deg,#f2ff6a,#b6e544 50%,#2f9a4d);
  transform:rotate(9.15deg);box-shadow:0 0 30px 8px rgba(226,255,90,.40)}
.seam.glowonly{width:34px;left:625px;opacity:.20;filter:blur(14px)}

/* ---------- players ---------- */
.kev{position:absolute;right:20px;bottom:-4px;height:726px;z-index:3;
  filter:drop-shadow(-18px 12px 26px rgba(0,0,0,.72)) saturate(1.08) contrast(1.04)}

.halo{position:absolute;width:430px;height:430px;border-radius:50%;z-index:2;filter:blur(2px)}
.hl{left:70px;top:30px;background:radial-gradient(circle,rgba(120,205,255,.20) 0%,rgba(90,190,255,0) 66%)}
.hr{right:34px;top:24px;background:radial-gradient(circle,rgba(200,255,90,.26) 0%,rgba(200,255,90,0) 66%)}
.vignette{position:absolute;inset:0;z-index:5;
  background:radial-gradient(118% 82% at 50% 44%, rgba(0,0,0,0) 42%, rgba(0,0,0,.58) 100%)}

/* ---------- top ribbon ---------- */
.ribbon{position:absolute;top:20px;left:50%;transform:translateX(-50%);z-index:9;
  display:flex;align-items:center;gap:11px;padding:9px 22px 8px;
  background:linear-gradient(180deg,#153a23,#06180e);border:2px solid rgba(233,255,77,.8);
  border-radius:999px;box-shadow:0 10px 26px rgba(0,0,0,.6)}
.ribbon span{font-weight:700;font-size:24px;letter-spacing:4.5px;color:#eefff4}
.ribbon b{font-family:Anton;font-size:25px;letter-spacing:2px;color:#e9ff4d}

/* ---------- center VS ---------- */
.vs-wrap{position:absolute;left:50%;top:318px;transform:translate(-50%,-50%);z-index:8;text-align:center}
.disc{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);
  width:250px;height:250px;border-radius:50%;
  background:radial-gradient(circle at 50% 45%, rgba(4,26,14,.90) 0%, rgba(3,18,10,.55) 58%, rgba(0,0,0,0) 72%)}
.vs{position:relative;font-family:Anton;font-size:158px;line-height:.8;color:#f4ff54;letter-spacing:-3px;
  -webkit-text-stroke:10px #06150c;paint-order:stroke fill;
  text-shadow:0 0 46px rgba(226,255,70,.60)}
.sub{position:relative;margin-top:4px;font-weight:700;font-size:25px;letter-spacing:7px;color:#eafff0;
  text-shadow:0 3px 10px #000,0 0 3px #000}

/* ---------- name plates ---------- */
.plate{position:absolute;bottom:34px;z-index:9;text-align:center}
.plate.l{left:52px}
.plate.r{right:44px}
.name{font-family:Anton;font-size:74px;line-height:.9;color:#fff;letter-spacing:1px;
  -webkit-text-stroke:8px #06150c;paint-order:stroke fill;text-shadow:0 12px 24px rgba(0,0,0,.75)}
.tag{display:inline-block;margin-top:10px;padding:5px 18px 4px;border-radius:7px;
  font-family:Anton;font-size:30px;letter-spacing:2.5px;box-shadow:0 7px 18px rgba(0,0,0,.55)}
.tag.blue{background:linear-gradient(180deg,#8fdcff,#2ca6ea);color:#03202f}
.tag.green{background:linear-gradient(180deg,#eaff56,#98d635);color:#06170e}

/* ---------- bottom framing ---------- */
.band{position:absolute;left:0;right:0;bottom:0;height:150px;z-index:6;
  background:linear-gradient(0deg, rgba(1,10,6,.94) 0%, rgba(1,10,6,.80) 45%, rgba(0,0,0,0) 100%)}
.strip{position:absolute;left:0;right:0;bottom:0;height:11px;z-index:10;
  background:linear-gradient(90deg,#2ca6ea 0%,#2ca6ea 45%,#e9ff4d 45%,#e9ff4d 55%,#4cc25e 55%,#4cc25e 100%)}

/* ---------- tiny self-deprecating tag ---------- */
.sloppy{position:absolute;left:50%;bottom:24px;transform:translateX(-50%);z-index:9;
  padding:4px 14px 3px;border-radius:999px;white-space:nowrap;
  background:rgba(4,18,10,.72);border:1px solid rgba(233,255,77,.35);
  font-weight:700;font-size:15px;letter-spacing:5px;color:rgba(233,255,77,.75)}
</style></head><body>
<div class="stage">
  <div class="bg"></div><div class="bg-tint"></div>

  <div class="halo hl"></div>
  <div class="panel left"><div class="photo"></div><div class="grade"></div></div>
  <div class="panel right"><div class="fill"></div></div>
  <div class="seam glowonly"></div><div class="seam"></div>

  <div class="halo hr"></div>
  <img class="kev" src="data:image/png;base64,__KEVIN__">

  <div class="vignette"></div><div class="band"></div>

  <div class="ribbon"><span>USTA</span><b>4.5</b><span>SINGLES</span></div>

  <div class="vs-wrap"><div class="disc"></div><div class="vs">VS</div><div class="sub">__SUB__</div></div>

  <div class="plate l"><div class="name">SCOTT</div><div class="tag blue">4.5</div></div>
  <div class="plate r"><div class="name">KEVIN</div><div class="tag green">4.5</div></div>

  <div class="sloppy">SLOPPY MATCH</div>

  <div class="strip"></div>
</div></body></html>"""

html = HTML
for token, rel in FONTS.items():
    path = HERE / rel
    html = html.replace(token, b64(path) if path.exists() else "")
html = (html.replace("__BG__", b64(ASSETS / "bg.jpg"))
            .replace("__SCOTT__", b64(ASSETS / "scott.jpg"))
            .replace("__KEVIN__", b64(ASSETS / "kevin_top.png"))
            .replace("__SUB__", SUB))
page = BUILD / f"{NAME}.html"
page.write_text(html)

raw = BUILD / f"raw-{NAME}.png"
raw.unlink(missing_ok=True)
subprocess.run([find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                "--hide-scrollbars", "--force-device-scale-factor=2",
                "--window-size=1400,900", f"--screenshot={raw}", f"file://{page}"],
               check=True, capture_output=True)

# chromium pads the shot to the window; keep just the 1280x720 stage (at 2x)
img = Image.open(raw).crop((0, 0, 2560, 1440))
img.save(HERE / f"{NAME}@2x.png")
small = img.resize((1280, 720), Image.LANCZOS)
small.save(HERE / f"{NAME}.png")
small.convert("RGB").save(HERE / f"{NAME}.jpg", quality=92)
print(f"wrote {NAME}.png, {NAME}@2x.png, {NAME}.jpg")
