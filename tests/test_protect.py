import pathlib
import subprocess

from pypdf import PdfReader
from test_compress import cleanup_compressed_files

from functions.protect_pdf import protect_pdf


def test_protect_file():
    protect_pdf(pathlib.Path("tests/Sample.pdf"), "1234")
    assert PdfReader("tests/Sample_protected.pdf").is_encrypted
    cleanup_compressed_files()


def test_protect_invalid_file():
    result = subprocess.run(
        [
            "python",
            "main.py",
            "--protect",
            "tests/Sample_invalid.pdf",
        ]
    )
    assert result.returncode == 1
