#!/usr/bin/env python3
"""Build pdf/cv.pdf from source/cv_en.md: python 14-bmw/scripts/build_cv.py.

Requires Pandoc, XeLaTeX, and the TeX Gyre Termes and Heros fonts.
Both English PDF filenames use source/cv_en.md as their content source.
The original source/cv.md is retained for reference.
"""

from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    output_dir = root / "pdf"
    for executable in ("pandoc", "xelatex"):
        if not shutil.which(executable):
            raise SystemExit(f"Required executable not found: {executable}")

    # Keep the existing PDF intact if compilation fails.
    with tempfile.TemporaryDirectory(prefix="bmw-cv-") as temporary:
        output = Path(temporary) / "cv.pdf"
        subprocess.run(
            [
                "pandoc", str(root / "source/cv_en.md"),
                "--from=markdown", "--standalone",
                "--pdf-engine=xelatex",
                f"--template={root / 'templates/cv-template.tex'}",
                f"--lua-filter={root / 'templates/cv-layout.lua'}",
                "--metadata=title:Seol Handong | Curriculum Vitae",
                "--metadata=author:Seol Handong",
                "--output", str(output),
            ],
            check=True,
            cwd=root,
        )
        output_dir.mkdir(exist_ok=True)
        shutil.copyfile(output, output_dir / "cv.pdf")
    print(f"Created {output_dir / 'cv.pdf'}")


if __name__ == "__main__":
    main()
