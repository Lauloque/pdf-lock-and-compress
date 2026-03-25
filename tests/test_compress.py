import glob
import os
import pathlib
import subprocess

from functions.compress_pdf import compress_pdf


def cleanup_compressed_files():
    for file_path in glob.glob("tests/Sample_*.pdf"):
        os.remove(file_path)
        print(f"Deleted {file_path}")


def test_compress_one_file():
    compress_pdf(pathlib.Path("tests/Sample.pdf"), "compressed", [], "1.4")
    assert os.path.exists("tests/Sample_compressed.pdf")
    cleanup_compressed_files()


def test_compress_multiple_files():
    result = subprocess.run(
        [
            "python",
            "main.py",
            "--test-compression-levels",
            "tests/Sample.pdf",
            "tests/Sample.pdf",
        ]
    )
    assert result.returncode == 0
    cleanup_compressed_files()


def test_compress_all_levels():
    result = subprocess.run(
        [
            "python",
            "main.py",
            "--test-compression-levels",
            "tests/Sample.pdf",
        ]
    )
    assert result.returncode == 0
    cleanup_compressed_files()


def test_compress_invalid_file_path():
    result = subprocess.run(
        [
            "python",
            "main.py",
            "--test-compression-levels",
            "tests/Sample_invalid.pdf",
        ]
    )
    assert result.returncode == 0
