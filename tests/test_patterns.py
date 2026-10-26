import patterns


def test_known_pattern_is_returned():
    assert patterns.get_pattern("batman") is not None


def test_unknown_pattern_is_none():
    assert patterns.get_pattern("does-not-exist") is None
