import pathlib
import sys

from constants import COMPRESSION_OPTIONS
from functions.compress_pdf import compress_pdf


def compress_pdf_all_levels(pdf_path: pathlib.Path):
    print(f"\nProcessing: {pdf_path.name}")
    for key, (
        suffix,
        description,
        extra_args,
        pdf_version,
    ) in COMPRESSION_OPTIONS.items():
        print(f"  • [{key}] {suffix:<10} — {description}")
        compress_pdf(pdf_path, suffix, extra_args, pdf_version)

    print("✅ All compression versions generated.\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Drag one or more PDFs onto this script or pass them as arguments.")
        sys.exit(1)

    for pdf in sys.argv[1:]:
        pdf_path = pathlib.Path(pdf)
        if not pdf_path.exists():
            print(f"❌ File not found: {pdf}")
            sys.exit(1)
        compress_pdf_all_levels(pdf_path)
    sys.exit(0)
