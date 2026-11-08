from gallery import DOCS, example_svg, gallery_svg
from patterns import patterns


def test_gallery_shows_every_pattern():
    picture = gallery_svg(patterns)
    for name in patterns:
        assert f">{name}</text>" in picture


def test_pictures_in_docs_are_up_to_date():
    # Fails after adding or changing a pattern: run make gallery and commit docs/
    assert (DOCS / "gallery.svg").read_text("utf-8") == gallery_svg(patterns)
    assert (DOCS / "example.svg").read_text("utf-8") == example_svg(patterns)
