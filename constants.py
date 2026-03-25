import shutil

# default Ghostscript executable
GHOSTSCRIPT = shutil.which("gswin64c") or shutil.which("gs") or "None"


# ----- Encoding Options -----
DEFAULT_COMPRESSION = "3"
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
        "Balanced compression — targets ~150dpi at 85% JPEG quality, skips images already close to target (recommended)",
        [
            # use ebook as the base for non-image settings (fonts, streams, etc.)
            "-dPDFSETTINGS=/ebook",
            # color images
            "-dColorImageResolution=150",
            "-dColorImageDownsampleType=/Bicubic",
            "-dColorImageDownsampleThreshold=1.4",  # only resample if >210dpi
            "-dColorImageFilter=/DCTEncode",
            "-dJPEGQ=85",
            # grayscale images
            "-dGrayImageResolution=150",
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
}
