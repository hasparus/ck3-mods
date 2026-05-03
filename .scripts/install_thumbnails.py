"""Crop the triptych-*.png set to square, resize to 512x512, and install
into each mod folder. Usage: python install_thumbnails.py [SRC_DIR]"""
import sys
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads"

PAIRS = [
    ("triptych-left.png",   "the-crimson-bath"),
    ("triptych-middle.png", "eclectic-traditions"),
    ("triptych-right.png",  "vigil-at-the-holy-site"),
]

def square(im):
    w, h = im.size
    s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))

for src_name, mod in PAIRS:
    src = SRC / src_name
    dst = ROOT / mod / "thumbnail.png"
    im = square(Image.open(src)).resize((512, 512), Image.LANCZOS)
    im.save(dst, "PNG", optimize=True)
    print(f"{src.name} -> {dst.relative_to(ROOT)}  ({dst.stat().st_size} bytes)")
