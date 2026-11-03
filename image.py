"""Turns a picture into a pattern file: the step behind `make image`.

The picture can be a URL or a file. It is cropped to what is drawn, shrunk to the graph's
7 rows, and each cell's darkness becomes a shade 1-4; light or transparent cells stay blank.
Seven rows is tiny, so simple, high-contrast pictures (icons, pixel art) work best.
"""

import io
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

import patterns

MAX_BYTES = 10 * 1024 * 1024
MAX_WIDTH = 52  # about a year of weeks
# Darkness 0-255 below this counts as background, so paper texture or JPEG noise stays blank
BLANK_BELOW = 40


def download(url: str) -> bytes:
    """The bytes at the URL, kept in memory; RuntimeError if it fails or is over 10 MB."""
    # Some sites refuse Python's default user agent
    request = urllib.request.Request(url, headers={"User-Agent": "pretty-github"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            # Read one byte past the limit, to tell "exactly 10 MB" from "more"
            data = response.read(MAX_BYTES + 1)
    except OSError as error:
        raise RuntimeError(f"Could not download {url}: {error}") from None
    if len(data) > MAX_BYTES:
        raise RuntimeError("The image is over 10 MB; use a smaller one")
    return data


def load_image(source: str) -> Image.Image:
    """Open a picture from a URL (http or https) or a file path."""
    if re.match(r"https?://", source):
        data = io.BytesIO(download(source))
    else:
        data = Path(source)
        if not data.exists():
            raise RuntimeError(f"No file {source}")
    try:
        image = Image.open(data)
        image.load()
    except (UnidentifiedImageError, Image.DecompressionBombError):
        raise RuntimeError("Not an image Pillow can read (PNG, JPEG, GIF, WebP; not SVG)") from None
    return image


def darkness(image: Image.Image, invert: bool = False) -> Image.Image:
    """Greyscale where 255 is darkest; transparent counts as white, so it stays blank."""
    rgba = image.convert("RGBA")
    white = Image.new("RGBA", rgba.size, "white")
    grey = Image.alpha_composite(white, rgba).convert("L")
    # invert=True is for light drawings on a dark background
    return grey if invert else ImageOps.invert(grey)


def to_pattern(image: Image.Image, invert: bool = False, max_width: int = MAX_WIDTH) -> list[str]:
    """The picture as 7 rows of digits and spaces, cropped to what is drawn."""
    dark = darkness(image, invert)
    # point() maps every pixel: background to 0, so getbbox() finds the drawing's edges
    box = dark.point(lambda value: 255 if value >= BLANK_BELOW else 0).getbbox()
    if box is None:
        raise RuntimeError("The image is blank (try INVERT=1 for light on dark)")
    dark = dark.crop(box)

    width = max(1, min(max_width, round(dark.width * 7 / dark.height)))
    # BOX averages all the pixels that fall in a cell, which suits shrinking a lot
    small = dark.resize((width, 7), Image.Resampling.BOX)
    cells = [[small.getpixel((x, y)) for x in range(width)] for y in range(7)]
    # Stretched so the picture's darkest cell is shade 4: a light-coloured drawing (a yellow
    # cat) would otherwise come out all 1s. +1 keeps the darkest cell just below 4 before int()
    darkest = max(max(row) for row in cells)
    span = darkest - BLANK_BELOW + 1
    return [
        "".join(
            " " if value < BLANK_BELOW else str(1 + int(4 * (value - BLANK_BELOW) / span))
            for value in row
        )
        for row in cells
    ]


def save_pattern(name: str, rows: list[str], source: str, folder: Path = patterns.FOLDER) -> Path:
    """Write patterns/<name>.txt; RuntimeError if the name is taken or not file-safe."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        raise RuntimeError("NAME: lowercase letters, digits and dashes, like baby-yoda")
    path = folder / f"{name}.txt"
    if path.exists():
        raise RuntimeError(f"{path.name} already exists; pick another NAME or delete it first")
    lines = [f"# From {source}"] + [row.replace(" ", ".") for row in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def main(argv: list[str]) -> None:
    if len(argv) not in (2, 3) or (len(argv) == 3 and argv[2] != "--invert"):
        raise SystemExit('Usage: make image IMAGE="https://..." NAME=cat [INVERT=1]')
    source, name = argv[:2]
    try:
        rows = to_pattern(load_image(source), invert=len(argv) == 3)
        path = save_pattern(name, rows, source)
    except RuntimeError as error:
        raise SystemExit(error) from None

    for row in rows:
        print("    " + " ".join("." if char == " " else char for char in row))
    print(f"\nSaved patterns/{path.name}")
    print(f"See it on the graph: make preview PATTERN={name} START=<a Sunday>")


if __name__ == "__main__":
    main(sys.argv[1:])
