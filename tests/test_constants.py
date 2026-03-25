from constants import COMPRESSION_OPTIONS, DEFAULT_COMPRESSION, GHOSTSCRIPT


def test_ghostscript():
    assert GHOSTSCRIPT is not None


def test_default_compression():
    assert DEFAULT_COMPRESSION == "3"


def test_compression_options():
    assert len(COMPRESSION_OPTIONS) == 6
