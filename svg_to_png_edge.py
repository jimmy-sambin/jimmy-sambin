import subprocess
import os
import tempfile
import shutil
from PIL import Image, ImageDraw

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT_DIR = r"C:\dll\GITHUB-PRO"


def render_svg(svg_name, png_name, width, height, transparent=False, circular=False):
    svg_path = os.path.join(OUT_DIR, svg_name)
    png_path = os.path.join(OUT_DIR, png_name)

    with open(svg_path, "r", encoding="utf-8") as f:
        svg_data = f.read()

    bg = "transparent" if transparent else "#020617"

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body{{margin:0;padding:0;background:{bg};overflow:hidden;}}</style>
</head><body>{svg_data}</body></html>"""

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html)
        tmp_html = tmp.name

    udd = os.path.join(tempfile.gettempdir(), f"udd_{png_name}")

    cmd = [
        EDGE,
        "--headless",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-background-timer-throttling",
        "--hide-scrollbars",
        "--window-size", f"{width},{height}",
        "--user-data-dir", udd,
        "--screenshot", png_path,
        "file:///" + tmp_html.replace("\\", "/")
    ]

    print(f"Rendering {png_name}...")
    subprocess.run(cmd, check=True)

    with Image.open(png_path) as img:
        if circular:
            img = img.convert("RGBA")
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, width - 1, height - 1), fill=255)
            out = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            out.paste(img, (0, 0), mask)
            out.save(png_path)
        else:
            img = img.convert("RGB")
            img.save(png_path)

    shutil.rmtree(udd, ignore_errors=True)
    os.unlink(tmp_html)

    size_kb = os.path.getsize(png_path) / 1024
    print(f"Saved: {png_path} ({size_kb:.1f} Ko)")


def main():
    render_svg("banner.svg", "banner.png", 1280, 420, transparent=False)
    render_svg("logo.svg", "logo.png", 512, 512, transparent=False)
    render_svg("logo-avatar.svg", "logo-avatar.png", 512, 512, transparent=True, circular=True)


if __name__ == "__main__":
    main()
