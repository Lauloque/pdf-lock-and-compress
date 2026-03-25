import pathlib
import sys

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    from PyPDF2 import PdfReader, PdfWriter

from constants import COMPRESSION_OPTIONS, DEFAULT_COMPRESSION
from main import compress_pdf

# Password is stored in a local file excluded from git (see .gitignore)
PASSWORD_FILE = pathlib.Path(__file__).parent / "owner_password.secret"


def load_or_ask_password() -> str:
    """Return the owner password from the secrets file, creating it if needed."""
    if PASSWORD_FILE.exists():
        password = PASSWORD_FILE.read_text(encoding="utf-8").strip()
        if password:
            return password
        print(f"⚠ '{PASSWORD_FILE.name}' exists but is empty.")

    # file missing or empty: ask the user
    print(f"No password found in '{PASSWORD_FILE.name}'.")
    while True:
        password = input("Enter an owner password to use for protected PDFs: ").strip()
        if password:
            break
        print("  Password cannot be empty, please try again.")

    PASSWORD_FILE.write_text(password, encoding="utf-8")
    print(f"✅ Password saved to '{PASSWORD_FILE.name}' (excluded from git).\n")
    return password


def protect_pdf(input_path: pathlib.Path, owner_password: str) -> pathlib.Path | None:
    """Protect the PDF with an empty user password and the given owner password."""
    final_path = input_path.with_name(input_path.stem + "_protected.pdf")
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # empty user password = opens freely; owner password prevents editing/copying
        writer.encrypt("", owner_password, algorithm="AES-256-R5")

        with open(final_path, "wb") as f:
            writer.write(f)

        print(f"✅ Protected '{final_path.name}'")
        return final_path
    except Exception as e:
        print(f"❌ Could not protect '{input_path.name}': {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print(
            "Drag one or more PDFs onto this script or pass their paths as arguments."
        )
        sys.exit(1)

    owner_password = load_or_ask_password()

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
    for pdf_path in sys.argv[1:]:
        pdf_path = pathlib.Path(pdf_path)
        if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
            print(f"⚠ Skipping '{pdf_path}': not a PDF or does not exist")
            continue

        compressed_path = compress_pdf(pdf_path, suffix, extra_args, pdf_version)
        if compressed_path:
            protect_pdf(compressed_path, owner_password)


if __name__ == "__main__":
    try:
        main()
    finally:
        input("\nPress Enter to exit...")
