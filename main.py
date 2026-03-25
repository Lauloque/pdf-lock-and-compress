import pathlib
import sys

from constants import (
    COMPRESSION_OPTIONS,
    DEFAULT_COMPRESSION,
    GHOSTSCRIPT,
)
from functions.compress_pdf import compress_pdf


def main():
    if not GHOSTSCRIPT:
        print(
            "❌ Ghostscript not found! Please install it and add its executable to your PATH."
        )
        sys.exit(1)

    if len(sys.argv) < 2:
        print(
            "Drag one or more PDFs onto this script or pass their paths as arguments."
        )
        sys.exit(1)

    valid_keys = list(COMPRESSION_OPTIONS.keys())

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

    # process all PDFs
    for file_path in sys.argv[1:]:
        file_path = pathlib.Path(file_path)
        if not file_path.exists() or file_path.suffix.lower() != ".pdf":
            print(f"⚠ Skipping '{file_path}': not a PDF or does not exist")
            continue
        compress_pdf(file_path, suffix, extra_args, pdf_version)


if __name__ == "__main__":
    try:
        main()
    finally:
        input("\nPress Enter to exit...")
