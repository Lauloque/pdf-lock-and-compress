import sys
import pathlib
import subprocess
import shutil

# default Ghostscript executable
GHOSTSCRIPT = shutil.which("gswin64c") or shutil.which("gs")

if not GHOSTSCRIPT:
    print("❌ Ghostscript not found! Please install it and add gswin64c.exe to your PATH.")
    sys.exit(1)

# mapping from number to Ghostscript preset
COMPRESSION_OPTIONS = {
    "1": ("screen", "Maximum compression at trash quality, images ~72dpi"),
    "2": ("ebook", "Hight compression at decent quality, images ~150dpi"),
    "3": ("printer", "Medium compression at printing quality, images ~300dpi"),
}

def compress_pdf(input_path: pathlib.Path, quality: str):
    output_path = input_path.with_name(f"{input_path.stem}_{quality}.pdf")
    cmd = [
        GHOSTSCRIPT,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{quality}",
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

    # show dialogue
    print("Choose compression level (press Enter for default 'ebook'):")
    for key, (preset, description) in COMPRESSION_OPTIONS.items():
        print(f"  {key}) {preset}: {description}")

    choice = input("Your choice [1-3]: ").strip()
    if choice not in COMPRESSION_OPTIONS:
        choice = "2"  # default to ebook

    preset, description = COMPRESSION_OPTIONS[choice]
    print(f"\nSelected preset: {preset} ({description})\n")

    # process all PDFs
    for pdf_path in sys.argv[1:]:
        pdf_path = pathlib.Path(pdf_path)
        if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
            print(f"⚠ Skipping '{pdf_path}': not a PDF or does not exist")
            continue
        compress_pdf(pdf_path, preset)


if __name__ == "__main__":
    try:
        main()
    finally:
        input("\nPress Enter to exit...")
