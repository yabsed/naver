#!/usr/bin/env python3
"""Build pdf/cv.pdf for the Naver application: python naver/build.py.

One file, in this order: a contents page with links, the headline essays from cv-writing/,
then the Korean CV from 14-bmw/source/cv_kr.md.

Naver asks applicants to leave out personal details unrelated to hiring (home address, email,
mobile number, marital status, salary). The CV is therefore rebuilt here from its Markdown
source with the email, phone and city lines removed; the 14-bmw PDFs themselves are untouched.
The build fails if an email address, phone number or city still shows up in the result.

Requires what cv-writing/build.py and 14-bmw/scripts/build_cv_versions.py require, plus PyMuPDF.
Pass --keep-headlines to reuse cv-writing/pdf/headlines.pdf instead of rebuilding it.
"""

from pathlib import Path
import argparse
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile

import fitz  # PyMuPDF

ROOT = Path(__file__).resolve().parent.parent
WRITING = ROOT / "cv-writing"
CV = ROOT / "14-bmw"
OUTPUT_DIR = ROOT / "pdf"

AUTHOR = "Seol Handong"
# Contact bullets under the name that Naver does not want: email, phone, city.
PERSONAL_LINE = re.compile(r"^\*\s*(email|tel|city|이메일|전화|거주지)\s*:", re.IGNORECASE)
GITHUB_LINE = re.compile(r"^\*[ \t]*(?:github id|github)[ \t]*:[ \t]*\[[^\]]+\]\(<?(https://(github\.com/[^)>]+))>?\)[ \t]*$",
                         re.IGNORECASE | re.MULTILINE)
# Anything matching these in the finished PDF stops the build.
LEAKS = [re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), re.compile(r"01\d[- .]?\d{3,4}[- .]?\d{4}"),
         re.compile(r"Yongin|용인|mailto:", re.IGNORECASE)]
TOC_LINK = "https://toc.invalid/"   # placeholder targets on the contents page, rewritten after merging

COVER = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[left=23mm,right=23mm,top=17mm,bottom=19mm]{geometry}
\usepackage{fontspec}
\setmainfont{TeX Gyre Termes}[Ligatures=TeX]
\setsansfont{TeX Gyre Heros}[Scale=0.91]
\usepackage{kotex}
\setmainhangulfont{Pretendard}[Path=FONTPATH/,UprightFont=*-Regular.otf,BoldFont=*-SemiBold.otf,Scale=0.9]
\setsanshangulfont{Pretendard}[Path=FONTPATH/,UprightFont=*-Regular.otf,BoldFont=*-SemiBold.otf,Scale=0.86]
\usepackage{xcolor}
\definecolor{ink}{HTML}{202020}
\definecolor{muted}{HTML}{555555}
\definecolor{rulegray}{HTML}{B8B8B8}
\usepackage[unicode,hidelinks]{hyperref}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\newcommand{\cvname}[1]{{\fontsize{29}{32}\selectfont #1\par}\vspace{1pt}}
\newcommand{\cvcontact}[1]{{\sffamily\fontsize{9.4}{12}\selectfont\color{muted}#1\par}}
\newcommand{\cvsection}[1]{%
  \par\addvspace{16pt}%
  {\sffamily\fontsize{10.2}{12}\selectfont\addfontfeatures{LetterSpace=10}\MakeUppercase{#1}\par}%
  \nobreak\vspace{4pt}{\color{rulegray}\hrule height 0.3pt}\nobreak\vspace{3pt}}
\newcommand{\pageno}[1]{{\sffamily\fontsize{9.4}{11.5}\selectfont\color{muted}#1}}
% Each row is one link across the full width: #1 target page, then title, then the page shown.
\newcommand{\tocpart}[3]{\par\addvspace{17pt}%
  \href{TOCLINK#1}{\hbox to\linewidth{\strut{\fontsize{16}{19}\selectfont\bfseries #2}\hfill\pageno{#3}}}\par}
\newcommand{\tocnote}[1]{{\sffamily\fontsize{9.4}{12}\selectfont\color{muted}#1\par}\vspace{6pt}}
\newcommand{\tocitem}[3]{%
  \href{TOCLINK#1}{\hbox to\linewidth{\strut #2\enspace
    {\color{rulegray}\leaders\hbox to 4.5pt{\hss.\hss}\hfill}\enspace\pageno{#3}}}\par\vspace{2.6pt}}
\begin{document}
\color{ink}
\fontsize{10.5}{14.8}\selectfont
\cvname{AUTHOR}
\cvcontact{Selected Writing and Curriculum Vitae}
\cvsection{Contents}
ROWS
\end{document}
"""


def run(command, **options):
    result = subprocess.run(command, capture_output=True, text=True, **options)
    if result.returncode:
        raise SystemExit(f"{' '.join(map(str, command[:3]))} failed:\n{result.stdout[-4000:]}\n{result.stderr[-2000:]}")
    return result


def latex(text):
    # ko.TeX would set curly quotes in the Hangul face; ASCII quotes become curly ones in the Latin face.
    for curly, plain in (("’", "'"), ("‘", "`"), ("“", "``"), ("”", "''")):
        text = text.replace(curly, plain)
    return re.sub(r"[&%$#_{}]", lambda match: "\\" + match.group(0), text)


def without_personal(markdown):
    """Drop the email, phone and city bullets; show the GitHub address in full instead of a bare id."""
    kept = "\n".join(line for line in markdown.split("\n") if not PERSONAL_LINE.match(line))
    return GITHUB_LINE.sub(r"* GitHub: [\2](<\1>)", kept)


def build_cv(work):
    """The Korean CV, set exactly as 14-bmw/scripts/build_cv_versions.py sets it."""
    for language, stem, template, title, author in (
        ("ko", "cv_kr", "cv-kr-template.tex", "설한동 | 국문 이력서", "설한동"),
    ):
        source = work / f"{stem}.md"
        source.write_text(without_personal((CV / "source" / f"{stem}.md").read_text(encoding="utf-8")), encoding="utf-8")
        run(["pandoc", str(source), "--from=markdown", "--standalone",
             f"--template={CV / 'templates' / template}",
             f"--lua-filter={CV / 'templates/cv-layout.lua'}",
             f"--metadata=lang:{language}", f"--metadata=title:{title}", f"--metadata=author:{author}",
             f"--variable=fontpath:{CV / 'assets/fonts/Pretendard'}",
             "--output", str(work / f"{stem}.tex")], cwd=CV)
        for _ in range(2):
            run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={work}",
                 str(work / f"{stem}.tex")], cwd=CV)
        log = (work / f"{stem}.log").read_text(encoding="utf-8", errors="replace")
        problems = [line for line in log.splitlines() if "Overfull" in line or "Missing character" in line]
        if problems:
            raise SystemExit(f"{stem}: layout or font errors:\n" + "\n".join(problems))
    return work / "cv_kr.pdf"


def headline_entries(headlines_pdf):
    """(title, page index in headlines.pdf) for each headline piece, in printed order."""
    spec = importlib.util.spec_from_file_location("writing_build", WRITING / "build.py")
    writing = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(writing)
    document = fitz.open(headlines_pdf)
    entries, page_number, below = [], 0, -1.0
    for name in writing.HEADLINES:
        note = writing.parse(WRITING / name)
        title = note["title"]
        if not title:  # an untitled piece is listed by its opening sentence
            opening = next(token[1] for token in note["tokens"] if token[0] == "text")
            title = re.split(r"(?<=[.!?])\s", opening.replace("*", "").strip())[0]
        # The PDF sets typographic quotes, so search for the longest stretch without one.
        needle = max(re.split(r"['’‘\"“”]", title), key=len).strip()
        for number in range(page_number, document.page_count):
            hits = [hit for hit in document[number].search_for(needle)
                    if number > page_number or hit.y0 > below]
            if hits:
                page_number, below = number, min(hit.y0 for hit in hits)
                break
        else:
            raise SystemExit(f"Headline not found in {headlines_pdf.name}: {title}")
        entries.append((title, page_number))
    return entries


def build_cover(work, rows):
    source = (COVER.replace("FONTPATH", str(CV / "assets/fonts/Pretendard")).replace("TOCLINK", TOC_LINK)
              .replace("AUTHOR", AUTHOR).replace("ROWS", "\n".join(rows)))
    (work / "cover.tex").write_text(source, encoding="utf-8")
    run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "cover.tex"], cwd=work)
    log = (work / "cover.log").read_text(encoding="utf-8", errors="replace")
    problems = [line for line in log.splitlines() if "Overfull" in line or "Missing character" in line]
    if problems:
        raise SystemExit("cover: layout or font errors:\n" + "\n".join(problems))
    cover = work / "cover.pdf"
    if fitz.open(cover).page_count != 1:
        raise SystemExit("The contents page no longer fits on one page.")
    return cover


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--keep-headlines", action="store_true", help="reuse cv-writing/pdf/headlines.pdf as it is")
    arguments = parser.parse_args()
    for executable in ("pandoc", "xelatex"):
        if not shutil.which(executable):
            raise SystemExit(f"Required executable not found: {executable}")

    headlines = WRITING / "pdf/headlines.pdf"
    if not arguments.keep_headlines:
        run([sys.executable, str(WRITING / "build.py"), "--headlines-only"])

    with tempfile.TemporaryDirectory(prefix="naver-cv-") as temporary:
        work = Path(temporary)
        cv_kr = build_cv(work)
        pieces = headline_entries(headlines)

        # Page numbers in the merged file, counting the contents page as page 1.
        first = {"headlines": 2}
        first["cv"] = first["headlines"] + fitz.open(headlines).page_count
        last = first["cv"] + fitz.open(cv_kr).page_count - 1
        rows = [f"\\tocpart{{{first['headlines']}}}{{Headlines}}{{{first['headlines']}–{first['cv'] - 1}}}",
                "\\tocnote{Selected writing, 2026}"]
        rows += [f"\\tocitem{{{first['headlines'] + page}}}{{{latex(title)}}}{{{first['headlines'] + page}}}"
                 for title, page in pieces]
        rows += [f"\\tocpart{{{first['cv']}}}{{Technical Background}}{{{first['cv']}–{last}}}",
                 "\\tocnote{Curriculum vitae, in Korean}",
                 f"\\tocitem{{{first['cv']}}}{{기술 이력서 (국문)}}{{{first['cv']}}}"]
        cover = build_cover(work, rows)

        merged = fitz.open()
        for part in (cover, headlines, cv_kr):
            with fitz.open(part) as document:
                merged.insert_pdf(document, links=True, annots=True)
        # The contents rows were set as placeholder web links; point them at the pages instead.
        page = merged[0]
        for link in page.get_links():
            if link.get("uri", "").startswith(TOC_LINK):
                target = int(link["uri"][len(TOC_LINK):]) - 1
                page.delete_link(link)
                page.insert_link({"kind": fitz.LINK_GOTO, "from": link["from"], "page": target,
                                  "to": fitz.Point(0, 0)})
        merged.set_toc([[1, "Contents", 1], [1, "Headlines", first["headlines"]],
                        [1, "Technical Background", first["cv"]],
                        [2, "기술 이력서 (국문)", first["cv"]]])
        merged.set_metadata({"title": f"{AUTHOR} | Selected Writing and Curriculum Vitae", "author": AUTHOR})

        for number, merged_page in enumerate(merged, start=1):
            found = merged_page.get_text() + " ".join(link.get("uri", "") for link in merged_page.get_links())
            for pattern in LEAKS:
                if pattern.search(found):
                    raise SystemExit(f"Personal detail on page {number}: {pattern.search(found).group(0)}")

        OUTPUT_DIR.mkdir(exist_ok=True)
        merged.save(OUTPUT_DIR / "cv.pdf", garbage=3, deflate=True)
        # The parts, as they went into cv.pdf.
        shutil.copyfile(headlines, OUTPUT_DIR / "headlines.pdf")
        shutil.copyfile(cv_kr, OUTPUT_DIR / "cv_kr.pdf")
    print(f"Created {OUTPUT_DIR / 'cv.pdf'}: {merged.page_count} pages "
          f"(contents 1, headlines {first['headlines']}–{first['cv'] - 1}, CV {first['cv']}–{last})")


if __name__ == "__main__":
    main()
