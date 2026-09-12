#!/bin/bash
# Renders each option-*.html to a 1280x720 PNG and JPG in ./out
cd "$(dirname "$0")"
BIN=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
mkdir -p out
for f in option-*.html; do
  n=${f%.html}
  "$BIN" --headless=new --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size=1280,720 --screenshot="out/$n@2x.png" "file://$PWD/$f" >/dev/null 2>&1
done
python3 - <<'PY'
from PIL import Image; import glob,os
for f in glob.glob('out/*@2x.png'):
    im=Image.open(f).convert('RGB').resize((1280,720),Image.LANCZOS)
    base=f.replace('@2x.png','')
    im.save(base+'.png',optimize=True); im.save(base+'.jpg',quality=92)
    print(os.path.basename(base), os.path.getsize(base+'.png')//1024,'KB png', os.path.getsize(base+'.jpg')//1024,'KB jpg')
PY
