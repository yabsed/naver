# BMW Financial Services Korea 지원 서류

IT Intern – AI Engineering 지원용 문서입니다. 결과 PDF는 모두 [`pdf/`](pdf/)에 있습니다.

## 결과물

| 파일 | 용도 |
| --- | --- |
| [cv_kr.pdf](pdf/cv_kr.pdf) | 국문 이력서 |
| [cv_en.pdf](pdf/cv_en.pdf) | 영문 이력서 |
| [letter.pdf](pdf/letter.pdf) | 국문 자기소개서 |
| [cv_merged.pdf](pdf/cv_merged.pdf) | 영문 → 국문 순서의 이력서 합본 |
| [cv.pdf](pdf/cv.pdf) | 기존 파일명을 유지한 영문 이력서 |

필수 제출 서류는 국문 이력서, 영문 이력서, 국문 자기소개서이며 자유 양식입니다.
채용공고 원본은 [`references/job-posting.pdf`](references/job-posting.pdf), 공고 텍스트는
[`references/job-posting.md`](references/job-posting.md)에 보관합니다.

## 원문과 디자인 수정

- 국문 이력서: [`source/cv_kr.md`](source/cv_kr.md)
- 영문 이력서: [`source/cv_en.md`](source/cv_en.md) — `cv_en.pdf`와 `cv.pdf`의 공통 원문
- 국문 자기소개서: [`source/letter.md`](source/letter.md)
- 조판과 디자인: `templates/`의 LaTeX 템플릿과 `cv-layout.lua`
- 공용 글꼴과 라이선스: `assets/fonts/Pretendard/`

`source/cv.md`는 기존 영문 원문의 보존본입니다. 이후 영문 내용 수정은 `source/cv_en.md`에 반영합니다.
`source/cv_merged.md`는 빌드 시 영문·국문 원문으로 다시 생성되므로 직접 수정하지 않습니다.

## PDF 생성

이 저장소의 루트에서 전체 결과물을 생성합니다.

```sh
python 14-bmw/build.py
```

`14-bmw` 안에서는 `python build.py`로 실행할 수 있습니다. 스크립트는 자신의 위치를 기준으로
경로를 계산하므로 다른 작업 디렉토리에서도 절대경로로 실행할 수 있습니다.

개별 생성도 가능합니다.

```sh
python 14-bmw/scripts/build_cv_versions.py
python 14-bmw/scripts/build_cv.py
python 14-bmw/scripts/build_letter.py
```

첫 번째 명령은 국문·영문·합본 이력서와 합본 Markdown을, 두 번째는 기존 이름의 `cv.pdf`를,
세 번째는 자기소개서를 생성합니다. PDF 출력 위치는 모두 `pdf/`입니다.

필요한 도구는 Python 3와 `pypdf`, Pandoc, XeLaTeX 및 ko.TeX, TeX Gyre Termes·Heros 글꼴입니다.
Pretendard 글꼴은 `assets/`에 포함되어 있습니다. 자기소개서는 A4 한 장을 기준으로 조판하며,
내용이 늘어나 한 장을 넘으면 빌드가 중단되므로 템플릿의 여백·간격을 조정해야 합니다.

각 생성 스크립트는 임시 디렉토리에서 컴파일하고 성공한 PDF를 복사합니다. 전체 빌드 중 오류가
발생하면 중단되며, 앞서 성공한 문서의 PDF는 이미 갱신되어 있을 수 있습니다.
