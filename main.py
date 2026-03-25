import argparse
import pathlib
import sys

from constants import (
    COMPRESSION_OPTIONS,
    DEFAULT_COMPRESSION,
    GHOSTSCRIPT,
)
from functions.compress_pdf import compress_pdf
from functions.get_password import get_password
from functions.protect_pdf import protect_pdf
from pdf_test_compression_levels import compress_pdf_all_levels


def main():
    if not GHOSTSCRIPT:
        print(
            "❌ Ghostscript not found! Please install it and add its executable to your PATH."
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Compress PDF files by drag and drop or pass their paths as arguments.",
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=pathlib.Path,
        help="PDF file(s) to compress. If multiple, put them in quotes and separated by spaces",
    )
    parser.add_argument(
        "-tcl",
        "--test-compression-levels",
        action="store_true",
        help="Test all compression levels (slow; best used with a small number of files)",
    )
    parser.add_argument(
        "-p",
        "--protect",
        action="store_true",
        help="Protect the PDF with a password",
    )

    args = parser.parse_args()

    valid_keys = list(COMPRESSION_OPTIONS.keys())

    if args.test_compression_levels:
        # this is just to avoid error 'reportPossiblyUnboundVariable'
        # on compress_pdf() when using TCL mode
        suffix = pdf_version = ""
        extra_args = []
    else:
        # show dialogue
        print("Choose compression level (press Enter for default 'smart'):")
        for key, (suffix, description, _, _) in COMPRESSION_OPTIONS.items():
            marker = " [default]" if key == DEFAULT_COMPRESSION else ""
            print(f"  {key}) {suffix}{marker}: {description}")

        choice = input(f"Your choice [{valid_keys[0]}–{valid_keys[-1]}]: ").strip()
        if choice not in COMPRESSION_OPTIONS:
            choice = DEFAULT_COMPRESSION

        suffix, description, extra_args, pdf_version = COMPRESSION_OPTIONS[choice]
        print(f"\nSelected: {suffix} — {description}\n")
    if args.protect:
        password = get_password()
    else:
        password = ""

    # process all PDFs
    for file_path in args.files:
        file_path = pathlib.Path(file_path)
        if not file_path.exists() or file_path.suffix.lower() != ".pdf":
            print(f"⚠ Skipping '{file_path}': not a valid PDF file")
            continue
        if args.test_compression_levels:
            compress_pdf_all_levels(file_path)
        else:
            compress_pdf(file_path, suffix, extra_args, pdf_version)
            if args.protect:
                protect_pdf(file_path, password)


if __name__ == "__main__":
    main()
    sys.exit(0)
