# PDF Lock and Compress

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge&logo=gnu&logoColor=white)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Ghostscript](https://img.shields.io/badge/Requires-Ghostscript-4B9CD3?style=for-the-badge&logoColor=white)](https://www.ghostscript.com/)
[![Ko-Fi](https://img.shields.io/badge/Support-D84A4F?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/lauloque)

A small collection of drag-and-drop Python scripts to compress and/or password-protect PDF files, built on top of Ghostscript and pypdf.

---

## Scripts

**`main.py`** — Compress one or more PDFs. Drag files onto it (or pass paths as arguments), pick a compression level, and get compressed copies alongside the originals.

**`pdf_compress_n_protect.py`** — Same as above, but also encrypts the output with AES-256: requires a password to open, and locks all editing. The password is stored in a local `owner_password.secret` file (git-ignored) and only asked for once.

**`pdf_test_compression_levels.py`** — Testing utility. Runs every available compression preset on a PDF at once so you can compare results side by side.

---

## Compression levels

| # | Preset | Description |
|---|--------|-------------|
| 1 | `screen` | Maximum compression, very low quality — images ~72dpi |
| 2 | `ebook` | High compression, decent quality — images ~150dpi |
| 3 | `smart` ⭐ | 95% JPEG quality, imagages 200dpi and skips images already near target DPI — default |
| 4 | `printer` | Print-ready quality — images ~300dpi |
| 5 | `prepress` | Professional quality — ~300dpi, preserves color profiles |
| 6 | `lossless` | No quality loss — recompresses with ZIP/Flate, keeps original DPI |
| 7 | `jpeg2000` | Better ratio than JPEG — images ~150dpi *(only shown if your Ghostscript build supports it)* |

---

## Prerequisites

### Ghostscript

Ghostscript must be installed and available on your PATH. It is **not** a Python package and cannot be installed via pip.

**Linux:**
```bash
sudo apt install ghostscript        # Debian/Ubuntu/Mint
sudo dnf install ghostscript        # Fedora
sudo pacman -S ghostscript          # Arch
```

**Windows:** Download the installer from [ghostscript.com](https://www.ghostscript.com/releases/gsdnld.html) and make sure `gswin64c.exe` is added to your PATH during installation.

---

## Installation

The scripts are intended to be run directly — no installation needed beyond the prerequisites above.

Clone the repo:

```bash
git clone https://github.com/Lauloque/pdf-lock-and-compress.git
cd pdf-lock-and-compress
```

Install the Python dependency manually with `pip install pypdf` or using [`uv sync`](https://github.com/astral-sh/uv):


---

## Usage

### Drag and drop

#### Linux
Run the setup script once to generate `.desktop` files for each script:

```bash
bash make_py_files_dragndropably_LINUX.sh
```

Then drag one or more PDFs onto any `.desktop` file in your file manager. A terminal window will open, ask for your preference, and produce the output file(s) in the same folder as the originals.

#### Windows
Run `make_py_files_dragndropably_WINDOWS.reg` once (double-click → confirm) to enable drag-and-drop onto `.py` files system-wide. Then drag PDFs directly onto the script files in Explorer.

### Command line

```bash
python main.py file1.pdf file2.pdf
python pdf_compress_n_protect.py file.pdf
python pdf_test_compression_levels.py file.pdf
```

---

## Password management (`pdf_compress_n_protect.py`)

On first run the script will ask you to type a password, which will be saved into `owner_password.secret` in the project folder. This file is listed in `.gitignore` and will never be exposed publically. On subsequent runs the password is loaded automatically from that file.

To change the password, edit `owner_password.secret` in a text editor, or delete it and run the script again.

---

## Contributing

### Environment setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# install uv if you don't have it
curl -Lsf https://astral.sh/uv/install.sh | sh   # Linux/macOS
# or: pip install uv

# clone and set up
git clone https://github.com/Lauloque/pdf-lock-and-compress.git
cd pdf-lock-and-compress
uv sync --extra dev
```

From then on, prefix any Python command with `uv run` to use the project's environment:

```bash
uv run main.py myfile.pdf
```

### Adding a compression preset

All presets live in the `_ALL_OPTIONS` dict in `main.py`. Each entry is a tuple of:

```python
"key": (
    "suffix",           # appended to the output filename
    "description",      # shown in the menu
    ["-dGS_FLAG=..."],  # list of Ghostscript arguments
    "1.4",              # PDF compatibility level
)
```

Adding a new preset there makes it automatically available in all three scripts.
