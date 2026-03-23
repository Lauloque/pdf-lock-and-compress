import sys
import subprocess
import pathlib

QUALITIES = ["screen", "ebook", "printer", "prepress", "default"]

GHOSTSCRIPT = shutil.which("gswin64c") or shutil.which("gs")


if not GHOSTSCRIPT:
    print("❌ Ghostscript not found! Please install it and add gswin64c.exe to your PATH.")
    sys.exit(1)


def compress_pdf(input_path: str, output_path: str, quality: str):
    cmd = [
        GHOSTSCRIPT,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path,
    ]
    subprocess.run(cmd, check=True)


def process_pdf(pdf_path: str):
    pdf_path = pathlib.Path(pdf_path)
    if not pdf_path.exists():
        print(f"❌ File not found: {pdf_path}")
        return

    print(f"\nProcessing: {pdf_path.name}")
    for quality in QUALITIES:
        output_path = pdf_path.with_name(f"{pdf_path.stem}_{quality}.pdf")
        print(f"  • {quality:<8} → {output_path.name}")
        compress_pdf(str(pdf_path), str(output_path), quality)

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
