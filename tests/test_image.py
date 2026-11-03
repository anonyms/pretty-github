"""Pictures are drawn in the test with Pillow; the download is faked, so no network."""

import io

import pytest
from PIL import Image, ImageDraw

import image
import patterns
from image import load_image, save_pattern, to_pattern


def picture(size, background="white"):
    canvas = Image.new("RGBA", size, background)
    return canvas, ImageDraw.Draw(canvas)


def test_black_square_on_white_fills_the_grid():
    canvas, draw = picture((100, 100))
    draw.rectangle((30, 30, 59, 59), fill="black")
    # Cropped to the square, so it fills all 7 rows, darkest shade
    assert to_pattern(canvas) == ["4444444"] * 7


def test_grey_next_to_black_is_a_lighter_shade():
    canvas, draw = picture((70, 70))
    # Cells are 10 pixels wide, so the edge at 40 falls between two cells
    draw.rectangle((0, 0, 39, 69), fill=(128, 128, 128))
    draw.rectangle((40, 0, 69, 69), fill="black")
    assert to_pattern(canvas)[0] == "2222444"


def test_light_picture_is_stretched_to_shade_4():
    canvas, draw = picture((70, 70))
    draw.rectangle((0, 0, 69, 69), fill=(230, 210, 60))  # yellow
    assert set("".join(to_pattern(canvas))) == {"4"}


def test_transparent_is_blank_and_shape_survives():
    canvas, draw = picture((70, 70), background=(0, 0, 0, 0))
    draw.rectangle((0, 0, 69, 9), fill="black")  # top row
    draw.rectangle((0, 60, 9, 69), fill="black")  # bottom-left corner
    assert to_pattern(canvas) == ["4444444"] + ["       "] * 5 + ["4      "]


def test_width_keeps_proportions_and_is_capped():
    canvas, draw = picture((400, 20))
    draw.rectangle((0, 0, 399, 19), fill="black")
    assert len(to_pattern(canvas)[0]) == 52
    assert len(to_pattern(canvas, max_width=200)[0]) == 140  # 400 x 7 / 20


def test_invert_reads_light_on_dark():
    canvas, draw = picture((70, 70), background="black")
    draw.rectangle((0, 0, 69, 9), fill="white")
    # Cropped to the white bar, 70 x 10, so 49 cells wide at 7 rows
    assert to_pattern(canvas, invert=True) == ["4" * 49] * 7


def test_blank_image_suggests_invert():
    with pytest.raises(RuntimeError, match="INVERT=1"):
        to_pattern(Image.new("RGB", (10, 10), "white"))


def test_url_is_downloaded_and_opened(monkeypatch):
    canvas, draw = picture((7, 7), background="black")
    png = io.BytesIO()
    canvas.save(png, "PNG")
    monkeypatch.setattr(image, "download", lambda url: png.getvalue())
    assert load_image("https://example.com/x.png").size == (7, 7)


def test_not_an_image(tmp_path):
    path = tmp_path / "x.svg"
    path.write_text("<svg/>")
    with pytest.raises(RuntimeError, match="not SVG"):
        load_image(str(path))


def test_too_big_download(monkeypatch):
    class Response(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    big = Response(b"x" * (image.MAX_BYTES + 1))
    monkeypatch.setattr(image.urllib.request, "urlopen", lambda request, timeout: big)
    with pytest.raises(RuntimeError, match="over 10 MB"):
        image.download("https://example.com/big.png")


def test_saved_file_loads_as_a_pattern(tmp_path):
    rows = ["4 4"] * 7
    path = save_pattern("dots", rows, "https://example.com/d.png", folder=tmp_path)
    assert path.read_text().startswith("# From https://example.com/d.png\n4.4\n")
    assert patterns.read_pattern(path) == rows


def test_save_refuses_taken_or_odd_names(tmp_path):
    save_pattern("cat", ["1"] * 7, "x", folder=tmp_path)
    with pytest.raises(RuntimeError, match="already exists"):
        save_pattern("cat", ["1"] * 7, "x", folder=tmp_path)
    with pytest.raises(RuntimeError, match="lowercase"):
        save_pattern("../cat", ["1"] * 7, "x", folder=tmp_path)
