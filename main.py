import pathlib
import subprocess
import sys

from constants import (
    COMPRESSION_OPTIONS,
    DEFAULT_COMPRESSION,
    GHOSTSCRIPT,
)


def compress_pdf(
    input_path: pathlib.Path, suffix: str, extra_args: list, pdf_version: str
):
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
        subprocess.run(
            cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
        print(f"✅ Done: '{output_path.name}'")
        return output_path
    except subprocess.CalledProcessError as e:
        stderr_text = e.stderr.decode(errors="ignore") if e.stderr else ""
        print(f"❌ Could not compress '{input_path.name}'.")

        if (
            "Could not open the file" in stderr_text
            or "Permission denied" in stderr_text
        ):
            print(
                "  • The PDF might be open in another program (like Acrobat) or the file/folder is locked."
            )
        elif "No such file or directory" in stderr_text:
            print("  • The PDF file wasn't found in the given path.")
        else:
            print("  • An unexpected error occurred while compressing the PDF:")
            print(e)
        sys.exit(1)


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
