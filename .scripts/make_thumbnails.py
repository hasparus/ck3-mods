from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MODS = [
    ("the-crimson-bath", "The Crimson\nBath", "#3a0a0a", "#d4a373"),
    ("eclectic-traditions", "Eclectic\nTraditions", "#1f3a3d", "#e6c79c"),
    ("vigil-at-the-holy-site", "Vigil at the\nHoly Site", "#2a2440", "#d8c98f"),
]

def font(size):
    for name in ("georgia.ttf", "Georgia.ttf", "times.ttf", "DejaVuSerif.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()

def render(folder, label, bg, fg):
    img = Image.new("RGB", (512, 512), bg)
    draw = ImageDraw.Draw(img)
    f = font(64)
    bbox = draw.multiline_textbbox((0, 0), label, font=f, align="center", spacing=8)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (512 - w) // 2 - bbox[0]
    y = (512 - h) // 2 - bbox[1]
    draw.multiline_text((x, y), label, font=f, fill=fg, align="center", spacing=8)
    out = ROOT / folder / "thumbnail.png"
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")

for f, l, bg, fg in MODS:
    render(f, l, bg, fg)
