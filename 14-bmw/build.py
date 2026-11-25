#!/usr/bin/env python3
"""Build all five PDFs: python 14-bmw/build.py.

All paths are resolved relative to this file, regardless of the working directory.
"""

from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    for script in ("build_cv_versions.py", "build_cv.py", "build_letter.py"):
        print(f"Building with scripts/{script}", flush=True)
        subprocess.run(
            [sys.executable, str(root / "scripts" / script)],
            cwd=root,
            check=True,
        )
    print(f"All five PDFs are ready in {root / 'pdf'}", flush=True)


if __name__ == "__main__":
    main()
