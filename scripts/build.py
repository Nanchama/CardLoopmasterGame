from pathlib import Path
import base64, io, re, shutil
from PIL import Image

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

# These SHA-256 values correspond to the user-approved PNG artwork.
APPROVED_ICON_HASHES = {
    192: "6590aea2ab0cf10a76797d4cc651869cfdadf54f90eb50b0c62360b3e66e2c3f",
    512: "9c46b45412696c659fb60cad19745cbb21f322152259cf0e0c32ada3884c4c28",
}

def build_icons():
    # 192-pixel icon is a PNG Git blob. The larger original is stored as
    # Git-friendly base64 chunks, then restored byte-for-byte at build time.
    for size, expected in APPROVED_ICON_HASHES.items():
        name = f"icon-{size}.png"
        original = ROOT / "assets" / name
        if original.is_file():
            raw = original.read_bytes()
        else:
            chunks = sorted((ROOT / "assets").glob(f"icon-{size}.part*.b64"))
            if not chunks:
                raise RuntimeError(f"Missing approved icon source for {name}")
            source = "".join(p.read_text(encoding="ascii") for p in chunks)
            raw = base64.b64decode(re.sub(r"\s+", "", source), validate=True)

        import hashlib
        actual = hashlib.sha256(raw).hexdigest()
        if actual != expected:
            raise RuntimeError(f"Approved icon does not match: {name} sha256={actual}")
        (DIST / name).write_bytes(raw)
        print(f"Restored exact approved artwork: {name} ({len(raw)} bytes)")

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
    print("Chronoloop PWA icons: original approved PNGs 192px / 512px")

if __name__ == "__main__":
    main()
