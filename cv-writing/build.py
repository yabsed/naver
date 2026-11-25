#!/usr/bin/env python3
"""Build pdf/writing.pdf from the dated notes in this folder: python cv-writing/build.py.

The headline pieces come first, in the order listed below; then every note follows
newest-first, the headline pieces included again at their place in the sequence.
Layout lives in templates/ and follows 14-bmw/templates/cv-template.tex.

Requires Pandoc, XeLaTeX with ko.TeX and wrapfig, latexmk, Pillow, and the TeX Gyre
Termes/Heros, NanumMyeongjo, NanumGothic, D2Coding and Symbola fonts.
Pass --headlines-only to build pdf/headlines.pdf with the headline pieces alone, and
--workdir DIR to keep the intermediate Markdown, LaTeX and log.
"""

from pathlib import Path
import argparse
import math
import re
import shutil
import subprocess
import tempfile

from PIL import Image

AUTHOR = "Seol Handong"
SUBTITLE = "Selected Writing · 2026"
HEADLINES = [
    "2026-11-18-1.md",   # When the right answer becomes free
    "2026-11-10.md",     # Nvidia Is Not Jensen Huang
    "2026-11-12.md",     # The End of Washington's AI Innocence
    "2026-11-15.md",     # Jensen Huang lacked the ability to lead Nvidia in the 2020s.
    "2026-10-15.md",     # Seo Taiji Is South Korean Pop Culture's Most Dangerous Unknown in 2026
    "2026-10-12-01.md",  # A Question for DJT
    "2026-09-23.md",     # Who Chooses South Korea's Supreme Court?
    "2026-08-15-1.md",   # (untitled) I never expected to find Jane Street on The Economist's list of fools.
    "2026-08-25-1.md",   # The Jane Street Mystery: Why a Firm of Puzzle-Solvers Bet on AI Without a Safety Net
    "2026-08-07.md",     # Flowers are dumb and strong.
]
# Typed outlines: set in two columns, and "1." lines stay plain text instead of becoming lists.
OUTLINE_NOTES = {"2026-09-05.md"}
# Bold one-word lines that Keep puts above a note's link previews; the previews become captions.
LINK_LABELS = {"링크"}
# Collected notes whose pieces are divided by a short rule instead of each carrying its own date.
# The date lines stay in the Markdown; the head row still shows the range they span.
UNDATED_PIECES = {"2026-01-00.md"}

# Page geometry shared with templates/writing-template.tex.
TEXT_WIDTH_MM = 164.0
LINE_MM = 5.22          # 14.8pt leading
PARSKIP_MM = 1.76       # 5pt
EM_MM = 3.70            # 10.5pt
GAP_MM = 6.0
# Every image sits in one right-hand column and never exceeds this box.
IMAGE_MAX_W_MM = 58.0
IMAGE_MAX_H_MM = 60.0
IMAGE_SHIFT = "-4.4pt"  # lifts an image so its top meets the first line's cap height
# Page breaks. A piece (a whole note, or one dated part of a collected note) up to this estimated
# height is never split: it moves to the next page whole. A longer piece may run over, but it
# always takes at least TAIL_LINES lines with it, so no page opens with a two- or three-line stub.
KEEP_WHOLE_MM = 120.0
TAIL_LINES = 6

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
DATE = re.compile(r"^\*(≤ )?(\d{4})-(\d{2})-(\d{2})\*$")
IMAGE = re.compile(r"^!\[[^\]]*\]\(<?(attachments/[^)>]+)>?\)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
BOLD_LINE = re.compile(r"^\*\*(?!\*)(.+?)\*\*$")
ITALIC_LINE = re.compile(r"^\*{1,3}(?!\*)(.+?)\*{1,3}$")
BREAK = re.compile(r"^(-{3,}|={3,}|\*{3,})$")
LABEL = re.compile(r"^글\s*(\d+)$")
LIST_ITEM = re.compile(r"^\s*([-*+]|\d+\.)\s")
ARROW = re.compile(r"<-+>|<-{2,}|-{2,}>")
SPECIAL = re.compile(r"^\s*([-*+]\s|\d+\.\s|#{1,6}\s|>|```)")


def show(date):
    bound, year, month, day = date
    return f"{'by ' if bound else ''}{day} {MONTHS[month - 1]} {year}"


def span(dates):
    days = sorted({date[1:] for date in dates})
    if len(days) == 1:
        return show(next(date for date in dates if date[1:] == days[0]))
    (y1, m1, d1), (y2, m2, d2) = days[0], days[-1]
    if (y1, m1) == (y2, m2):
        return f"{d1}–{d2} {MONTHS[m1 - 1]} {y1}"
    if y1 == y2:
        return f"{d1} {MONTHS[m1 - 1]} – {d2} {MONTHS[m2 - 1]} {y1}"
    return f"{d1} {MONTHS[m1 - 1]} {y1} – {d2} {MONTHS[m2 - 1]} {y2}"


def parse_date(match):
    return (bool(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))


def parse(path):
    """Split one note into title, dates, standfirst, lead image and body tokens."""
    text = path.read_text(encoding="utf-8").replace("\u200b", "").replace("\ufeff", "")
    lines = text.split("\n")
    title, image, top_dates = None, None, []
    start = 0
    for start, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if DATE.match(stripped):
            top_dates.append(parse_date(DATE.match(stripped)))
        elif IMAGE.match(stripped):
            image = image or IMAGE.match(stripped).group(1)
        elif title is None and (HEADING.match(stripped) or BOLD_LINE.match(stripped)):
            match = HEADING.match(stripped) or BOLD_LINE.match(stripped)
            title = match.group(match.lastindex).strip()
        else:
            break
    else:
        start = len(lines)

    tokens, fenced = [], False
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("```"):
            fenced = not fenced
            tokens.append(("text", stripped))
        elif fenced:
            tokens.append(("text", line))
        elif not stripped:
            tokens.append(("blank",))
        elif DATE.match(stripped):
            tokens.append(("date", parse_date(DATE.match(stripped))))
        elif IMAGE.match(stripped):
            tokens.append(("image", IMAGE.match(stripped).group(1)))
        elif BREAK.match(stripped):
            tokens.append(("break",))
        elif LABEL.match(stripped):
            tokens.append(("label", f"글 {LABEL.match(stripped).group(1)}"))
        else:
            tokens.append(("text", line))

    def next_content(index):
        while index < len(tokens) and tokens[index][0] == "blank":
            index += 1
        return index

    # A label takes the date that follows it; a rule before a dated piece is redundant.
    merged, index = [], 0
    while index < len(tokens):
        token = tokens[index]
        if token[0] == "label":
            after = next_content(index + 1)
            if after < len(tokens) and tokens[after][0] == "date":
                merged.append(("piece", token[1], tokens[after][1]))
                index = after + 1
                continue
            merged.append(("piece", token[1], None))
        else:
            merged.append(token)
        index += 1
    tokens = merged
    inner_dates = [token[-1] for token in tokens if token[0] in ("date", "piece") and token[-1]]
    undated = path.name in UNDATED_PIECES
    if undated:   # keep the rules between pieces, drop the dates
        tokens = [token for token in tokens if token[0] != "date"]
    else:
        tokens = [
            token for index, token in enumerate(tokens)
            if not (token[0] == "break" and next_content(index + 1) < len(tokens)
                    and tokens[next_content(index + 1)][0] in ("date", "piece"))
        ]
    # A note's only image leads the entry. When a note has several, each opens the part it is
    # written in, and the first part's image leads.
    body_images = [token for token in tokens if token[0] == "image"]
    if image is None and len(body_images) == 1:
        image = body_images[0][1]
        tokens = [token for token in tokens if token[0] != "image"]
    elif body_images:
        placed, part_start = [], 0
        for token in tokens:
            if token[0] == "image" and part_start == 0 and image is None:
                image = token[1]
            elif token[0] == "image":
                placed.insert(part_start, token)
                part_start += 1
            else:
                placed.append(token)
                if token[0] in ("break", "date", "piece"):
                    part_start = len(placed)
        tokens = placed
    while tokens and tokens[0][0] in ("blank", "break"):
        tokens.pop(0)
    while tokens and tokens[-1][0] in ("blank", "break"):
        tokens.pop()

    deck = None
    if title and tokens and tokens[0][0] == "text" and ITALIC_LINE.match(tokens[0][1].strip()):
        if len(tokens) == 1 or tokens[1][0] == "blank":
            deck = ITALIC_LINE.match(tokens.pop(0)[1].strip()).group(1)
            while tokens and tokens[0][0] == "blank":
                tokens.pop(0)

    dates = top_dates + inner_dates
    if not dates:
        raise SystemExit(f"No *YYYY-MM-DD* date line in {path.name}")
    head_date = span(dates)
    if undated:
        pass
    elif len({show(date) for date in dates}) > 1:
        if title and top_dates:      # titled: the head shows the range, each piece its own date
            tokens.insert(0, ("date", top_dates[0]))
        elif not title:              # untitled: the head row is simply the first piece's date
            if not top_dates and tokens[0][0] == "date":
                top_dates = [tokens.pop(0)[1]]
            if top_dates:
                head_date = show(top_dates[0])
    else:  # one date for the whole note: the head row already shows it
        tokens = [("piece", token[1], None) if token[0] == "piece" else token
                  for token in tokens if token[0] != "date"]
    return {"name": path.name, "title": title, "deck": deck, "image": image,
            "date": head_date, "tokens": tokens}


def raw_latex(value):
    return ["", "```{=latex}", value, "```", ""]


def body_markdown(note, place, marks):
    outline = note["name"] in OUTLINE_NOTES
    levels = sorted({len(HEADING.match(token[1]).group(1)) for token in note["tokens"]
                     if token[0] == "text" and HEADING.match(token[1])})
    tokens = note["tokens"]
    out, fenced, in_links, after_break = [], False, False, False
    for index, token in enumerate(tokens):
        if in_links and token[0] != "blank" and not (token[0] == "text" and LIST_ITEM.match(token[1])):
            out += ["", ":::", ""]
            in_links = False
        out += [line for mark in marks.get(("close", index), []) for line in raw_latex(mark)]
        if token[0] in ("break", "date", "piece"):  # a part opening with its own image stays whole
            following = next((later for later in tokens[index + 1:] if later[0] != "blank"), None)
            if following and following[0] == "image":
                out += raw_latex(f"\\reserve{{{place(following[1])[1][1] + 14:.0f}mm}}")
        out += [line for mark in marks.get(("open", index), []) for line in raw_latex(mark)]
        if token[0] == "blank":
            out.append("")
        elif token[0] == "image":
            target, (width, _) = place(token[1])
            out += raw_latex(f"\\leadimage{{{target}}}{{{width:.1f}mm}}")
        elif token[0] == "date":
            out += raw_latex(f"\\piecedate{{{show(token[1])}}}")
        elif token[0] == "piece":
            out += raw_latex(f"\\piecehead{{{token[1]}}}{{{show(token[2]) if token[2] else ''}}}")
        elif token[0] == "break":
            out += raw_latex("\\piecebreak")
            after_break = True
        else:
            line = token[1]
            if line.startswith("```"):
                fenced = not fenced
                out.append(line)
                continue
            if fenced:
                out.append(line)
                continue
            label = BOLD_LINE.match(line.strip())
            if label and label.group(1) in LINK_LABELS:
                out += ["", "::: links", ""]
                in_links = True
                continue
            heading = HEADING.match(line)
            if heading:
                major = len(levels) > 1 and len(heading.group(1)) == levels[0]
                out += ["", f"{'###' if major else '####'} {heading.group(2)}", ""]
                continue
            if outline:
                line = re.sub(r"^(\s*\d+)\.(\s)", r"\1\\.\2", line)
            if outline or not LIST_ITEM.match(line):
                indent = len(line) - len(line.lstrip(" "))
                line = ("\u00a0" * indent if indent >= 2 else "") + line.lstrip(" ")
            line = ARROW.sub(lambda match: "".join("\\" + char for char in match.group(0)), line)
            out.append(line)
            # A one-line paragraph right after a rule reads as a label: keep it with what follows.
            if after_break and index + 2 < len(tokens) and tokens[index + 1][0] == "blank":
                out += raw_latex("\\nobreak")
            after_break = False
    if in_links:
        out += ["", ":::", ""]
    return out


def text_units(line):
    """Approximate set width of a line in ems: Hangul and CJK are full width."""
    wide = sum(1 for char in line if "\u1100" <= char <= "\ud7a3" or "\u3000" <= char <= "\u9fff")
    return wide * 0.95 + (len(line) - wide) * 0.46


def set_lines(text, size_pt, width_mm):
    return max(1, math.ceil(text_units(text) * size_pt * 0.3528 * 1.08 / width_mm))


def head_height(note, kind):
    head_mm = 6.0
    if note["title"]:
        size_pt, line_mm = (16, 6.7) if kind == "headline" else (12.3, 5.3)
        head_mm = set_lines(note["title"], size_pt, TEXT_WIDTH_MM - 34) * line_mm + 3
    if note["deck"]:
        head_mm += set_lines(note["deck"], 10.8, TEXT_WIDTH_MM) * 5.1 + 3
    return head_mm


def keep_marks(note, kind, image_size, place):
    """Decide where a note may not break across pages.

    Returns (keep_head, marks): keep_head says the head and first piece stay together, and marks
    maps ("close" | "open", token index) to the LaTeX commands emitted before that token.
    """
    tokens = note["tokens"]
    per_line = TEXT_WIDTH_MM / EM_MM
    pieces, piece, block = [], {"start": 0, "blocks": [], "image": image_size}, None
    fenced = False
    for index, token in enumerate(tokens):
        if token[0] in ("break", "date", "piece"):
            pieces.append(piece)
            piece, block = {"start": index, "blocks": [], "image": None, "marker": True}, None
        elif token[0] == "image":
            piece["image"] = place(token[1])[1]
        elif token[0] == "blank":
            block = None
        else:
            line = token[1]
            if line.startswith("```"):
                fenced = not fenced
            if block is None:
                block = {"start": index, "lines": 0, "plain": True}
                piece["blocks"].append(block)
            block["lines"] += max(1, math.ceil(text_units(line) / per_line))
            if fenced or line.startswith("```") or SPECIAL.match(line):
                block["plain"] = False  # lists, headings, quotes and panels are not one paragraph
    pieces.append(piece)

    def height(piece, first):
        text_mm = sum(block["lines"] * LINE_MM + PARSKIP_MM for block in piece["blocks"])
        if piece["image"]:  # text beside the image runs in a narrower column
            width, image_mm = piece["image"]
            narrowing = TEXT_WIDTH_MM / (TEXT_WIDTH_MM - width - GAP_MM)
            beside = image_mm / narrowing
            text_mm = max(image_mm, text_mm * narrowing) if text_mm <= beside else image_mm + text_mm - beside
        return text_mm + (head_height(note, kind) if first else 8.0 if piece.get("marker") else 0.0)

    heights = [height(piece, number == 0) for number, piece in enumerate(pieces)]
    marks = {}
    if sum(heights) + 4.0 * (len(pieces) - 1) <= KEEP_WHOLE_MM:
        return True, marks  # the whole note stays on one page
    for number, piece in enumerate(pieces):
        if number:
            marks.setdefault(("close", piece["start"]), []).append("\\keepoff")
        if heights[number] <= KEEP_WHOLE_MM:
            if number:
                marks.setdefault(("open", piece["start"]), []).append("\\keepon")
            continue
        # A long piece: its last TAIL_LINES lines never part.
        blocks, rest = piece["blocks"], 0
        for position in range(len(blocks) - 1, -1, -1):
            block = blocks[position]
            if rest + block["lines"] < TAIL_LINES and position:
                rest += block["lines"]
                continue
            wanted = max(3, TAIL_LINES - rest)  # how many of this block's closing lines must come along
            if block["plain"] and block["lines"] > wanted + 1:
                penalties = " ".join(["10000"] * (wanted - 1) + ["0"])
                marks.setdefault(("open", block["start"]), []).append(
                    f"\\widowpenalties={wanted} {penalties}\\relax")
                if position + 1 < len(blocks):
                    marks.setdefault(("open", blocks[position + 1]["start"]), []).append("\\nobreak\\keepon")
            elif position or number:
                marks.setdefault(("open", block["start"]), []).append("\\keepon")
            break
    return heights[0] <= KEEP_WHOLE_MM, marks


def layout(note, kind, image_size):
    """Estimate heights to choose how the image sits and how much room the entry needs."""
    head_mm = head_height(note, kind)
    if note["name"] in OUTLINE_NOTES:
        return {"mode": "columns", "need": head_mm + 60}
    if not image_size:
        return {"need": head_mm + (5 if note["title"] else 3) * LINE_MM}
    width, height = image_size
    per_line = (TEXT_WIDTH_MM - width - GAP_MM) / EM_MM
    text_mm, special_beside_image, new_paragraph = 0.0, False, True
    for token in note["tokens"]:
        if token[0] == "blank":
            new_paragraph = True
            continue
        if token[0] != "text":
            text_mm += LINE_MM + PARSKIP_MM
            continue
        if SPECIAL.match(token[1]) and text_mm < height + 8:
            special_beside_image = True
        text_mm += max(1, math.ceil(text_units(token[1]) / per_line)) * LINE_MM
        if new_paragraph:
            text_mm += PARSKIP_MM
            new_paragraph = False
    if special_beside_image and text_mm <= 120:
        return {"mode": "side", "need": head_mm + max(height, text_mm) + 4}
    return {"mode": "wrap", "need": head_mm + height + 5}


def prepare_image(source, target):
    """Write a print-sized copy with a plain name and return its size on the page in mm."""
    with Image.open(source) as image:
        ratio = image.width / image.height
        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGBA")
            canvas = Image.new("RGB", image.size, "white")
            canvas.paste(image, mask=image.split()[-1])
            image = canvas
        else:
            image = image.convert("RGB")
        image.thumbnail((900, 900), Image.LANCZOS)
        image.save(target, "JPEG", quality=86)
    width = min(IMAGE_MAX_W_MM, IMAGE_MAX_H_MM * ratio)
    return width, width / ratio


def entry_markdown(note, kind, root, workdir, images):
    def place(source):  # a note printed twice shares one copy of each image
        if source not in images:
            target = workdir / f"image-{len(images) + 1:03d}.jpg"
            images[source] = (target, prepare_image(root / source, target))
        return images[source]

    image_size, image_path = None, None
    if note["image"]:
        image_path, image_size = place(note["image"])
    plan = layout(note, kind, image_size)
    keep_head, marks = False, {}
    if plan.get("mode") not in ("columns", "side"):  # those two are laid out as fixed blocks already
        keep_head, marks = keep_marks(note, kind, image_size, place)
    attributes = [f'kind="{kind}"', f'date="{note["date"]}"', f'need="{plan["need"]:.0f}"']
    if keep_head:
        attributes.append('keep="1"')
    if "mode" in plan:
        attributes.append(f'mode="{plan["mode"]}"')
    if image_path:
        attributes += [f'img="{image_path}"', f'imgw="{image_size[0]:.1f}"']
    out = ["", f'::::::: {{.entry {" ".join(attributes)}}}']
    if note["title"]:
        out += [f'## {note["title"]}', ""]
    if note["deck"]:
        out += ["::: deck", note["deck"], ":::", ""]
    out += body_markdown(note, place, marks)
    out += ["", ":::::::", ""]
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workdir", type=Path, help="keep intermediate files in this directory")
    parser.add_argument("--headlines-only", action="store_true", help="build pdf/headlines.pdf without the notebook")
    arguments = parser.parse_args()

    root = Path(__file__).resolve().parent
    for executable in ("pandoc", "xelatex", "latexmk"):
        if not shutil.which(executable):
            raise SystemExit(f"Required executable not found: {executable}")

    notes = {path.name: parse(path) for path in sorted(root.glob("2026-*.md"))}
    missing = [name for name in HEADLINES if name not in notes]
    if missing:
        raise SystemExit(f"Headline notes not found: {', '.join(missing)}")
    notebook = sorted(notes, reverse=True)

    with tempfile.TemporaryDirectory(prefix="cv-writing-") as temporary:
        workdir = arguments.workdir.resolve() if arguments.workdir else Path(temporary)
        workdir.mkdir(parents=True, exist_ok=True)
        lines, images = [], {}
        sections = [("Headlines", "headline", HEADLINES), ("Notebook", "note", notebook)]
        if arguments.headlines_only:
            sections = sections[:1]
        for heading, kind, names in sections:
            lines += ["", f"# {heading}", ""]
            for name in names:
                lines += entry_markdown(notes[name], kind, root, workdir, images)
        (workdir / "writing.md").write_text("\n".join(lines), encoding="utf-8")

        subprocess.run(
            [
                "pandoc", "writing.md",
                "--from=markdown+hard_line_breaks+autolink_bare_uris-raw_html",
                "--to=latex", "--standalone",
                f"--template={root / 'templates/writing-template.tex'}",
                f"--lua-filter={root / 'templates/writing-layout.lua'}",
                f"--variable=title:{AUTHOR} | Selected Writing",
                f"--variable=author:{AUTHOR}",
                f"--variable=subtitle:{SUBTITLE}",
                f"--variable=imgshift:{IMAGE_SHIFT}",
                "--output=writing.tex",
            ],
            check=True,
            cwd=workdir,
        )
        result = subprocess.run(
            ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "writing.tex"],
            cwd=workdir, capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise SystemExit(result.stdout[-3000:] + f"\nLaTeX failed; see {workdir / 'writing.log'}")
        log = (workdir / "writing.log").read_text(encoding="utf-8", errors="replace")
        for problem in sorted(set(re.findall(r"Missing character: .*", log))):
            print(f"Warning: {problem}")

        output_dir = root / "pdf"
        output_dir.mkdir(exist_ok=True)
        output = output_dir / ("headlines.pdf" if arguments.headlines_only else "writing.pdf")
        shutil.copyfile(workdir / "writing.pdf", output)
    print(f"Created {output} ({', '.join(f'{len(names)} {heading.lower()}' for heading, _, names in sections)})")


if __name__ == "__main__":
    main()
