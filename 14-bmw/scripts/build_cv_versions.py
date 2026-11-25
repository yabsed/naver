#!/usr/bin/env python3
"""Build PDF versions in pdf/ from source/cv_kr.md and source/cv_en.md.

Run: python 14-bmw/scripts/build_cv_versions.py
Requires Pandoc, XeLaTeX/ko.TeX, pypdf, and the bundled Pretendard fonts.
The English PDF uses the original cv-template.tex.
The combined version places English before Korean.
"""

from pathlib import Path
import shutil
import subprocess
import tempfile

from pypdf import PdfReader, PdfWriter


def main():
    root = Path(__file__).resolve().parent.parent
    source_dir = root / 'source'
    output_dir = root / 'pdf'
    for executable in ('pandoc', 'xelatex'):
        if not shutil.which(executable):
            raise SystemExit(f'Required executable not found: {executable}')

    with tempfile.TemporaryDirectory(prefix='bmw-cv-versions-') as temporary:
        work = Path(temporary)
        for language, stem, template, title, author in (
            ('ko', 'cv_kr', 'cv-kr-template.tex', '설한동 | 국문 이력서', '설한동'),
            ('en', 'cv_en', 'cv-template.tex', 'Seol Handong | Curriculum Vitae', 'Seol Handong'),
        ):
            subprocess.run([
                'pandoc', str(source_dir / f'{stem}.md'), '--from=markdown', '--standalone',
                f'--template={root / "templates" / template}',
                f'--lua-filter={root / "templates/cv-layout.lua"}',
                f'--metadata=lang:{language}', f'--metadata=title:{title}',
                f'--metadata=author:{author}',
                f'--variable=fontpath:{root / "assets/fonts/Pretendard"}',
                '--output', str(work / f'{stem}.tex'),
            ], check=True, cwd=root)
            for _ in range(2):
                result = subprocess.run([
                    'xelatex', '-interaction=nonstopmode', '-halt-on-error',
                    f'-output-directory={work}', str(work / f'{stem}.tex'),
                ], cwd=root, capture_output=True, text=True)
                if result.returncode:
                    print(result.stdout[-6000:])
                    result.check_returncode()
            log = (work / f'{stem}.log').read_text(encoding='utf-8')
            problems = [line for line in log.splitlines()
                        if 'Overfull' in line or 'Missing character' in line]
            if problems:
                raise SystemExit(f'{stem}: layout or font errors:\n' + '\n'.join(problems))

        writer = PdfWriter()
        writer.append(str(work / 'cv_en.pdf'), outline_item='영문 이력서 / English CV')
        writer.append(str(work / 'cv_kr.pdf'), outline_item='한국어 이력서 / Korean CV')
        writer.add_metadata({
            '/Title': '설한동 / Seol Handong | 국영문 이력서',
            '/Author': '설한동 / Seol Handong',
            '/Subject': 'English and Korean Curriculum Vitae',
        })
        writer.write(work / 'cv_merged.pdf')
        output_dir.mkdir(exist_ok=True)
        for stem in ('cv_kr', 'cv_en', 'cv_merged'):
            shutil.copyfile(work / f'{stem}.pdf', output_dir / f'{stem}.pdf')
            print(f'pdf/{stem}.pdf: {len(PdfReader(output_dir / f"{stem}.pdf").pages)} pages')

    korean = (source_dir / 'cv_kr.md').read_text(encoding='utf-8').rstrip()
    english = (source_dir / 'cv_en.md').read_text(encoding='utf-8').rstrip()
    (source_dir / 'cv_merged.md').write_text(
        f'<!-- 영문 이력서 / English CV -->\n\n{english}\n\n---\n\n'
        f'<!-- 한국어 이력서 / Korean CV -->\n\n{korean}\n',
        encoding='utf-8',
    )


if __name__ == '__main__':
    main()
