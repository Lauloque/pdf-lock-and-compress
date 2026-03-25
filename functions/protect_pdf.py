import pathlib

from pypdf import PdfReader, PdfWriter


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
