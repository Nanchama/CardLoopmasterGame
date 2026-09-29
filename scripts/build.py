from pathlib import Path
import base64, io, re, shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"

def join_parts(pattern):
    parts = sorted(ROOT.glob(pattern))
    if not parts:
        raise RuntimeError(f"No parts found: {pattern}")
    return "".join(p.read_text(encoding="utf-8") for p in parts)

def convert_embedded_pngs_to_webp(html):
    pattern = re.compile(r"data:image/png;base64,([A-Za-z0-9+/=]+)")
    converted = 0
    def repl(m):
        nonlocal converted
        raw = base64.b64decode(m.group(1))
        im = Image.open(io.BytesIO(raw)).convert("RGBA")
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=84, method=6)
        converted += 1
        return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    return pattern.sub(repl, html), converted

def build_icons():
    b64 = join_parts("assets/icon-512.b64.part*.txt").strip()
    raw = base64.b64decode(b64)
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    img.save(DIST / "icon-512.png", "PNG")
    img.resize((192,192), Image.Resampling.LANCZOS).save(DIST / "icon-192.png", "PNG")

def main():
    DIST.mkdir(exist_ok=True)
    html = join_parts("src/index.part*.txt")
    html, converted = convert_embedded_pngs_to_webp(html)
    (DIST / "index.html").write_text(html, encoding="utf-8")
    build_icons()
    for name in ("manifest.webmanifest","service-worker.js","robots.txt"):
        shutil.copy2(ROOT / name, DIST / name)
    print(f"Built index.html: {len(html.encode('utf-8'))/1024/1024:.2f} MB")
    print(f"Embedded PNG -> WebP conversions: {converted}")

if __name__ == "__main__":
    main()
