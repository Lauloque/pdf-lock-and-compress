import glob
import os
import subprocess


def test_compress():
    result = subprocess.run(
        [
            "python",
            "pdf_test_compression_levels.py",
            "tests/Sample.pdf",
        ]
    )
    assert result.returncode == 0
    for file_path in glob.glob("tests/Sample_*.pdf"):
        os.remove(file_path)
        print(f"Deleted {file_path}")


def test_compress_multiple():
    result = subprocess.run(
        [
            "python",
            "pdf_test_compression_levels.py",
            "tests/Sample.pdf",
            "tests/Sample.pdf",
        ]
    )
    assert result.returncode == 0
    for file_path in glob.glob("tests/Sample_*.pdf"):
        os.remove(file_path)
        print(f"Deleted {file_path}")


def test_compress_invalid_file_path():
    result = subprocess.run(
        [
            "python",
            "pdf_test_compression_levels.py",
            "tests/Sample_invalid.pdf",
        ]
    )
    assert result.returncode == 1
