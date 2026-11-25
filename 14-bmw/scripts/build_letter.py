#!/usr/bin/env python3
"""Build pdf/letter.pdf from source/letter.md, matching the Korean CV.

Run: python 14-bmw/scripts/build_letter.py
Requires Pandoc, XeLaTeX/ko.TeX, pypdf, and the shared Pretendard fonts.
Edit source/letter.md for content and templates/letter-template.tex for layout.
"""

from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from pypdf import PdfReader


def main():
    root = Path(__file__).resolve().parent.parent
    output_dir = root / "pdf"
    for executable in ("pandoc", "xelatex"):
        if not shutil.which(executable):
            raise SystemExit(f"Required executable not found: {executable}")

    source = (root / "source/letter.md").read_text(encoding="utf-8")
    headings = re.match(r"\A# ([^\n]+)\n\s*### ([^\n]+)\n", source)
    if not headings:
        raise SystemExit("letter.md must begin with a # company and ### subject.")
    company, subject = headings.groups()
    body = source[headings.end():].lstrip()

    # Compile in isolation and replace the PDF only after successful validation.
    with tempfile.TemporaryDirectory(prefix="bmw-letter-") as temporary:
        work = Path(temporary)
        subprocess.run([
            "pandoc", "--from=markdown", "--standalone",
            f"--template={root / 'templates/letter-template.tex'}",
            f"--variable=fontpath:{root / 'assets/fonts/Pretendard'}",
            "--metadata=lang:ko", "--metadata=author:설한동",
            f"--metadata=company:{company}", f"--metadata=subject:{subject}",
            "--metadata=email:yabsed@snu.ac.kr",
            "--metadata=phone:010-4163-0786", "--metadata=github:yabsed",
            "--output", str(work / "letter.tex"),
        ], input=body, text=True, check=True, cwd=root)
        for _ in range(2):
            result = subprocess.run([
                "xelatex", "-interaction=nonstopmode", "-halt-on-error",
                f"-output-directory={work}", str(work / "letter.tex"),
            ], cwd=root, capture_output=True, text=True)
            if result.returncode:
                print(result.stdout[-6000:])
                result.check_returncode()

        log = (work / "letter.log").read_text(encoding="utf-8")
        problems = [line for line in log.splitlines()
                    if "Overfull" in line or "Missing character" in line]
        if problems:
            raise SystemExit("Layout or font errors:\n" + "\n".join(problems))
        output = work / "letter.pdf"
        pages = len(PdfReader(output).pages)
        if pages != 1:
            raise SystemExit(f"Expected one page, got {pages}; adjust the template.")
        output_dir.mkdir(exist_ok=True)
        shutil.copyfile(output, output_dir / "letter.pdf")
    print(f"Created {output_dir / 'letter.pdf'} (1 page)")


if __name__ == "__main__":
    main()
