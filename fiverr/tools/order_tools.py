"""Order helpers for Leaseletter templates.

  python3 fiverr/tools/order_tools.py split T01 orders/2026-11-10-ab
      -> letter.docx (guidance removed, ready to fill) + serving-note.docx/.pdf (the guidance notes)
  python3 fiverr/tools/order_tools.py check orders/2026-11-10-ab/letter.docx
      -> lists unfilled [placeholders] and risky wording
  python3 fiverr/tools/order_tools.py finalise orders/2026-11-10-ab/letter.docx
      -> filled-in text back to plain black, then PDF (run after check passes)

Orders contain customer personal data: the /orders folder is git-ignored and never uploaded.
"""
import copy
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"

RISKY = [
    r"\blawyer\b", r"(?<!power of )\battorney\b", r"\badvocate\b", r"legal advice", r"legal opinion", r"\bguarantee", r"100% valid",
    r"\bofficial(ly)?\b", r"approved by (RERA|DLD|the government)", r"RERA[- ]approved", r"DLD[- ]approved",
    r"you will win", r"you must\b", r"your contract (says|means)", r"in your case",
]
PLACEHOLDER = re.compile(r"\[[^\]]*\]")


def find_template(code):
    hits = sorted(TEMPLATES.glob(f"{code.upper()}-*.docx"))
    if not hits:
        sys.exit(f"No template {code} in {TEMPLATES}")
    return hits[0]


def letter_start(body):
    """Index of the first body element whose paragraph starts on a new page (the letter / checklist)."""
    for i, el in enumerate(body):
        if el.tag == qn("w:p"):
            ppr = el.find(qn("w:pPr"))
            if ppr is not None and ppr.find(qn("w:pageBreakBefore")) is not None:
                return i
    return None


def to_pdf(docx_path):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(docx_path.parent), str(docx_path)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)


def split(code, outdir):
    src = find_template(code)
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    letter = Document(src)
    body = [el for el in letter.element.body if el.tag != qn("w:sectPr")]
    start = letter_start(body)
    if start is None:
        # no guidance section (e.g. T09 glossary): copy as-is
        letter.save(out / "letter.docx")
        print("No guidance section; copied", src.name)
        return
    for el in body[:start]:
        letter.element.body.remove(el)
    ppr = body[start].find(qn("w:pPr"))
    ppr.remove(ppr.find(qn("w:pageBreakBefore")))
    letter.save(out / "letter.docx")

    note = Document(src)
    nbody = [el for el in note.element.body if el.tag != qn("w:sectPr")]
    for el in nbody[start:]:
        note.element.body.remove(el)
    for par in note.paragraphs:
        if par.text.startswith("GUIDANCE NOTES"):
            for r in par.runs[1:]:
                r.text = ""
            par.runs[0].text = "HOW AND WHEN TO SERVE THIS DOCUMENT — keep this note, do not send it"
            break
    note.save(out / "serving-note.docx")
    to_pdf(out / "serving-note.docx")
    print(f"Wrote {out/'letter.docx'} and {out/'serving-note.pdf'} from {src.name}")


def all_text(doc):
    parts = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                parts.append(c.text)
    return "\n".join(parts)


def check(path):
    doc = Document(path)
    text = all_text(doc)
    footer = "\n".join(p.text for s in doc.sections for p in s.footer.paragraphs)
    problems = 0
    left = sorted(set(PLACEHOLDER.findall(text)))
    if left:
        problems += 1
        print(f"UNFILLED placeholders ({len(left)}): " + ", ".join(left))
    for pat in RISKY:
        for m in re.finditer(pat, text, flags=re.I):
            problems += 1
            ctx = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            print(f"RISKY wording '{m.group(0)}': ...{ctx}...")
    if "not legal advice" not in footer:
        problems += 1
        print("MISSING disclaimer in footer")
    if "Legal basis:" not in footer:
        problems += 1
        print("MISSING legal basis in footer")
    print("CHECK PASSED" if problems == 0 else f"{problems} problem(s) to fix")
    return problems


def finalise(path):
    path = Path(path)
    doc = Document(path)
    pars = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                pars.extend(c.paragraphs)
    n = 0
    for par in pars:
        for r in par.runs:
            if r.font.color is not None and r.font.color.rgb is not None and str(r.font.color.rgb) == "B45F06":
                r.font.color.rgb = None
                r.bold = None
                n += 1
    doc.save(path)
    to_pdf(path)
    print(f"Finalised {n} filled-in parts; wrote {path.with_suffix('.pdf').name}")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "split":
        split(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 3 and sys.argv[1] == "finalise":
        finalise(sys.argv[2])
    elif len(sys.argv) >= 3 and sys.argv[1] == "check":
        sys.exit(1 if check(sys.argv[2]) else 0)
    else:
        print(__doc__)
