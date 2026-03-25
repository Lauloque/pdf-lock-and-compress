import pathlib
import sys

from constants import COMPRESSION_OPTIONS
from main import compress_pdf


def process_pdf(pdf_path: str | pathlib.Path):
    pdf_path = pathlib.Path(pdf_path)
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return

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

    try:
        for pdf in sys.argv[1:]:
            process_pdf(pdf)
    finally:
        input("\nPress Enter to exit...")
