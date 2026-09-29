from pathlib import Path
import base64, io, math, re, shutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
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

def make_icon(size):
    # Adopted Chronoloop motif: deep purple field, gold compass ring,
    # ruby side accents and a large gold infinity symbol.
    scale = size / 512.0
    img = Image.new("RGBA", (size, size), (20, 8, 25, 255))
    d = ImageDraw.Draw(img)

    def S(v):
        return int(round(v * scale))

    # background / rounded gold frame
    d.rounded_rectangle(
        [S(8), S(8), size-S(8), size-S(8)],
        radius=S(72),
        fill=(35, 13, 45, 255),
        outline=(241, 190, 72, 255),
        width=max(2, S(8))
    )
    # subtle inner purple field
    d.ellipse([S(55), S(55), S(457), S(457)], fill=(61, 18, 66, 255))
    d.ellipse([S(86), S(86), S(426), S(426)], outline=(93, 45, 99, 255), width=max(1, S(3)))

    # compass rings
    for inset, width, color in [
        (105, 18, (91, 48, 8, 255)),
        (112, 12, (188, 111, 18, 255)),
        (119, 5, (255, 218, 108, 255)),
    ]:
        d.ellipse([S(inset), S(inset), size-S(inset), size-S(inset)],
                  outline=color, width=max(1, S(width)))

    # compass points
    cx = cy = size // 2
    gold = (232, 160, 38, 255)
    bright = (255, 220, 112, 255)
    dark = (93, 47, 10, 255)
    points = [
        [(cx, S(18)), (cx-S(17), S(110)), (cx, S(92)), (cx+S(17), S(110))],
        [(cx, size-S(18)), (cx-S(17), size-S(110)), (cx, size-S(92)), (cx+S(17), size-S(110))],
        [(S(18), cy), (S(110), cy-S(17)), (S(92), cy), (S(110), cy+S(17))],
        [(size-S(18), cy), (size-S(110), cy-S(17)), (size-S(92), cy), (size-S(110), cy+S(17))],
    ]
    for poly in points:
        d.polygon(poly, fill=gold, outline=dark)
    # ruby side gems
    for x in (S(95), size-S(95)):
        r = S(15)
        d.polygon([(x, cy-r), (x+r, cy), (x, cy+r), (x-r, cy)],
                  fill=(151, 8, 78, 255), outline=bright)

    # small stars
    for x, y in [(165,105),(350,105),(145,390),(370,390),(255,145),(255,370)]:
        x, y = S(x), S(y)
        r1, r2 = S(10), S(3)
        d.polygon([(x,y-r1),(x+r2,y-r2),(x+r1,y),(x+r2,y+r2),
                   (x,y+r1),(x-r2,y+r2),(x-r1,y),(x-r2,y-r2)],
                  fill=(255, 210, 76, 255))

    # infinity symbol using a Gerono lemniscate sampled into a smooth path.
    pts = []
    for i in range(361):
        t = 2 * math.pi * i / 360
        x = 256 + 142 * math.sin(t)
        y = 256 + 78 * math.sin(t) * math.cos(t)
        pts.append((S(x), S(y)))

    # layered strokes create a metallic gold look.
    d.line(pts, fill=(46, 19, 7, 255), width=max(2, S(45)), joint="curve")
    d.line(pts, fill=(145, 77, 8, 255), width=max(2, S(37)), joint="curve")
    d.line(pts, fill=(240, 166, 34, 255), width=max(2, S(30)), joint="curve")
    d.line(pts, fill=(255, 225, 124, 255), width=max(1, S(9)), joint="curve")

    return img

def build_icons():
    make_icon(512).save(DIST / "icon-512.png", "PNG")
    make_icon(192).save(DIST / "icon-192.png", "PNG")

def main():
    DIST.mkdir(exist_ok=True)

    html = join_parts("src/index.part*.txt")
    html, converted = convert_embedded_pngs_to_webp(html)
    (DIST / "index.html").write_text(html, encoding="utf-8")

    build_icons()

    for name in ("manifest.webmanifest", "service-worker.js", "robots.txt"):
        shutil.copy2(ROOT / name, DIST / name)

    print(f"Built index.html: {len(html.encode('utf-8'))/1024/1024:.2f} MB")
    print(f"Embedded PNG -> WebP conversions: {converted}")
    print("Generated Chronoloop app icons: 192px / 512px")

if __name__ == "__main__":
    main()
