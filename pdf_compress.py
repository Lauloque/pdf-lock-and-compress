import sys
import pathlib
import subprocess
import shutil

# default Ghostscript executable
GHOSTSCRIPT = shutil.which("gswin64c") or shutil.which("gs")

if not GHOSTSCRIPT:
    print("❌ Ghostscript not found! Please install it and add gswin64c.exe to your PATH.")
    sys.exit(1)

# Each option is: (suffix, description, extra_gs_args, pdf_version)
# pdf_version: Ghostscript -dCompatibilityLevel value
COMPRESSION_OPTIONS = {
    "1": (
        "screen",
        "Maximum compression, very low quality — images ~72dpi",
        ["-dPDFSETTINGS=/screen"],
        "1.4",
    ),
    "2": (
        "ebook",
        "High compression, decent quality — images ~150dpi (aggressive, may cause quality loss)",
        ["-dPDFSETTINGS=/ebook"],
        "1.4",
    ),
    "3": (
        "smart",
        "Balanced compression — targets ~200dpi at 95% JPEG quality, skips images already close to target (recommended)",
        [
            # use ebook as the base for non-image settings (fonts, streams, etc.)
            "-dPDFSETTINGS=/ebook",
            # color images
            "-dColorImageResolution=200",
            "-dColorImageDownsampleType=/Bicubic",
            "-dColorImageDownsampleThreshold=1.4",  # only resample if >280dpi
            "-dColorImageFilter=/DCTEncode",
            "-dJPEGQ=95",
            # grayscale images
            "-dGrayImageResolution=200",
            "-dGrayImageDownsampleType=/Bicubic",
            "-dGrayImageDownsampleThreshold=1.4",
            "-dGrayImageFilter=/DCTEncode",
        ],
        "1.5",
    ),
    "4": (
        "printer",
        "Medium compression, print-ready quality — images ~300dpi",
        ["-dPDFSETTINGS=/printer"],
        "1.4",
    ),
    "5": (
        "prepress",
        "Low compression, professional quality — images ~300dpi, preserves color profiles",
        ["-dPDFSETTINGS=/prepress"],
        "1.4",
    ),
    "6": (
        "lossless",
        "Lossless recompression — keeps original DPI and full quality, uses ZIP/Flate instead of JPEG",
        [
            "-dPDFSETTINGS=/prepress",
            "-dDownsampleColorImages=false",
            "-dDownsampleGrayImages=false",
            "-dDownsampleMonoImages=false",
            "-dColorImageFilter=/FlateEncode",
            "-dGrayImageFilter=/FlateEncode",
        ],
        "1.4",
    ),
    "7": (
        "jpeg2000",
        "JPEG 2000 recompression — better quality-to-size ratio than standard JPEG, images ~150dpi",
        [
            "-dPDFSETTINGS=/ebook",
            "-dColorImageFilter=/JPXEncode",
            "-dGrayImageFilter=/JPXEncode",
        ],
        "1.5",
    ),
}

DEFAULT_CHOICE = "3"

def compress_pdf(input_path: pathlib.Path, suffix: str, extra_args: list, pdf_version: str):
    output_path = input_path.with_name(f"{input_path.stem}_{suffix}.pdf")
    cmd = [
        GHOSTSCRIPT,
        "-sDEVICE=pdfwrite",
        f"-dCompatibilityLevel={pdf_version}",
        *extra_args,
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        str(input_path),
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"✅ Done: '{output_path.name}'")
    except subprocess.CalledProcessError as e:
        stderr_text = e.stderr.decode(errors="ignore") if e.stderr else ""
        print(f"❌ Could not compress '{input_path.name}'.")

        if "Could not open the file" in stderr_text or "Permission denied" in stderr_text:
            print("  • The PDF might be open in another program (like Acrobat) or the file/folder is locked.")
        elif "No such file or directory" in stderr_text:
            print("  • The PDF file wasn't found in the given path.")
        else:
            print("  • An unexpected error occurred while compressing the PDF:")
            print(e)

def main():
    if len(sys.argv) < 2:
        print("Drag one or more PDFs onto this script or pass their paths as arguments.")
        sys.exit(1)

    valid_keys = list(COMPRESSION_OPTIONS.keys())

    # show dialogue
    print("Choose compression level (press Enter for default 'smart'):")
    for key, (suffix, description, _, _) in COMPRESSION_OPTIONS.items():
        marker = " [default]" if key == DEFAULT_CHOICE else ""
        print(f"  {key}) {suffix}{marker}: {description}")

    choice = input(f"Your choice [{valid_keys[0]}–{valid_keys[-1]}]: ").strip()
    if choice not in COMPRESSION_OPTIONS:
        choice = DEFAULT_CHOICE

    suffix, description, extra_args, pdf_version = COMPRESSION_OPTIONS[choice]
    print(f"\nSelected: {suffix} — {description}\n")

    # process all PDFs
    for pdf_path in sys.argv[1:]:
        pdf_path = pathlib.Path(pdf_path)
        if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
            print(f"⚠ Skipping '{pdf_path}': not a PDF or does not exist")
            continue
        compress_pdf(pdf_path, suffix, extra_args, pdf_version)


if __name__ == "__main__":
    try:
        main()
    finally:
        input("\nPress Enter to exit...")
