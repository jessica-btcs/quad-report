#!/usr/bin/env python3
"""The Opportunity / Issue Processing Form: draw it, or fill one.

    python3 fill_issue.py fill  <issue.json> <out.docx> [--form <form.docx>]
    python3 fill_issue.py blank <out.docx>
    python3 fill_issue.py check <form.docx>

By default the form is drawn here: an unbranded form with the same sections,
prompts and layout as the one the group uses, so nothing has to be supplied.
With --form, the owner's own copy is filled instead. Either way, boxes are
found by their printed labels, so a newer year's form with the same labels
fills the same way, and only the white answer boxes are written.

issue.json:
  {"member": "...", "meeting_date": "...", "group": "...", "dollar_value": "...",
   "issue": "...", "significant": "...", "ideal_outcome": "...",
   "background": ["...", ...], "options": ["...", ...], "direction": "...",
   "help": ["...", ...]}
A list prints one bullet per item; a string prints as written.

Needs python-docx (pip install python-docx). Prints JSON.
"""
import copy, json, re, sys

try:
    import docx
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    sys.exit("This needs python-docx.  Install it with:  pip install python-docx")

# label printed on the form -> issue.json key. Header labels fill the cell to
# their right; section labels fill the white box in the row below.
HEADER = {"member": "member", "meeting date": "meeting_date",
          "group": "group", "dollar value of issue": "dollar_value"}
SECTIONS = {"the opportunity/issue is": "issue",
            "it is significant because": "significant",
            "my ideal outcome is": "ideal_outcome",
            "relevant background information": "background",
            "my options are": "options",
            "direction im headed": "direction",
            "help i would like from": "help"}

# The drawn form: (label, prompt in the left column). Same order and words as
# the group's form.
FORM_SECTIONS = [
    ("The opportunity/issue is:", ["One or two sentences that get to the heart in no uncertain terms."]),
    ("It is significant because:", ["Effect on dollars, people, products, services, customers, vendors, "
                                    "family, timing, future, outer offices, etc."]),
    ("My ideal outcome is:", ["What I really want to happen."]),
    ("Relevant background information:", ["Concise bullet points that identify:", "•  How/when/where/why it started",
                                          "•  Who the players are", "•  The forces at work", "•  Today’s focus",
                                          "•  Future impact"]),
    ("My options are:", ["Actions I could take."]),
    ("Direction I’m headed:", ["This is the option above I plan to pursue at this moment."]),
    ("Help I would like from the group:", ["•  Options I’m missing?", "•  On the right track?",
                                           "•  What would you do differently?", "•  Why?",
                                           "•  Should I do nothing?", "•  Etc."]),
]
NAVY, GOLD, PANEL, WHITE, INK = "1C3D5A", "E8C14A", "F1F1F1", "FFFFFF", "000000"
FONT = "Calibri"


def norm(s):
    s = re.sub(r"[^a-z/# ]", "", s.lower().replace("’", "'"))
    s = re.sub(r"^vistage\s+", "", s.strip())
    return s.replace("#", "").strip()


def cell_text(tc):
    return "".join(t.text or "" for t in tc.iter(qn("w:t")))


def find_boxes(doc):
    """Return {key: answer-cell element}."""
    boxes = {}
    for tbl in doc.element.body.iter(qn("w:tbl")):  # nested tables too
        rows = tbl.tr_lst
        for ri, tr in enumerate(rows):
            tcs = tr.tc_lst
            for ci, tc in enumerate(tcs):
                label = norm(cell_text(tc))
                if not label:
                    continue
                for lab, key in SECTIONS.items():
                    if label.startswith(lab) and ri + 1 < len(rows):
                        below = rows[ri + 1].tc_lst
                        if ci < len(below):
                            boxes.setdefault(key, below[ci])
                for lab, key in HEADER.items():
                    if label.rstrip(":").strip() == lab and ci + 1 < len(tcs):
                        boxes.setdefault(key, tcs[ci + 1])
    return boxes


# ---------- drawing the unbranded form ----------

def shade(cell, fill):
    pr = cell._tc.get_or_add_tcPr()
    for old in pr.findall(qn("w:shd")):
        pr.remove(old)
    pr.append(pr.makeelement(qn("w:shd"), {qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): fill}))


def no_borders(table):
    pr = table._tbl.tblPr
    b = pr.makeelement(qn("w:tblBorders"), {})
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b.append(b.makeelement(qn(f"w:{side}"), {qn("w:val"): "nil"}))
    pr.append(b)


def white_gaps(table):
    """White hairlines between cells, like the form's white boxes on grey."""
    pr = table._tbl.tblPr
    b = pr.makeelement(qn("w:tblBorders"), {})
    for side in ("top", "left", "bottom", "right"):
        b.append(b.makeelement(qn(f"w:{side}"), {qn("w:val"): "nil"}))
    for side in ("insideH", "insideV"):
        b.append(b.makeelement(qn(f"w:{side}"), {qn("w:val"): "single", qn("w:sz"): "24",
                                                  qn("w:color"): PANEL}))
    pr.append(b)


def say(cell, lines, size=10.5, color=INK, bold=False):
    cell.text = ""
    for i, line in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(line)
        r.font.name, r.font.size, r.font.bold = FONT, Pt(size), bold
        r.font.color.rgb = RGBColor.from_string(color)


def spacer(p, pts):
    """An empty paragraph exactly `pts` tall, for the gaps on the grey panel."""
    p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(pts)
    p.paragraph_format.line_spacing_rule = 4  # exactly
    ppr = p._p.get_or_add_pPr()
    rpr = ppr.makeelement(qn("w:rPr"), {})
    rpr.append(rpr.makeelement(qn("w:sz"), {qn("w:val"): "2"}))
    ppr.append(rpr)


def widths(table, inches):
    table.autofit = False
    for row in table.rows:
        for c, w in zip(row.cells, inches):
            c.width = Inches(w)


def blank_form():
    doc = docx.Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.5)
    sec.top_margin, sec.bottom_margin = Inches(0.45), Inches(0.4)
    st = doc.styles["Normal"]
    st.font.name, st.font.size = FONT, Pt(10.5)
    st.paragraph_format.space_after = Pt(0)

    t = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("OPPORTUNITY / ISSUE PROCESSING FORM")
    r.font.name, r.font.size, r.font.bold = FONT, Pt(19), True
    r.font.color.rgb = RGBColor.from_string(NAVY)
    rule = doc.add_paragraph()
    rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rule.paragraph_format.space_before, rule.paragraph_format.space_after = Pt(2), Pt(10)
    rr = rule.add_run("━" * 6)
    rr.font.size, rr.font.color.rgb = Pt(12), RGBColor.from_string(GOLD)

    # The whole form sits on one grey panel: an outer one-cell table.
    panel = doc.add_table(rows=1, cols=1)
    no_borders(panel)
    widths(panel, [7.5])
    box = panel.rows[0].cells[0]
    shade(box, PANEL)
    spacer(box.paragraphs[0], 6)

    def header(labels, wid):
        tbl = box.add_table(rows=1, cols=4)
        white_gaps(tbl)
        widths(tbl, wid)
        row = tbl.rows[0]
        row.height, row.height_rule = Inches(0.34), WD_ROW_HEIGHT_RULE.AT_LEAST
        for i, c in enumerate(row.cells):
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            shade(c, WHITE if i % 2 else PANEL)
            say(c, [labels[i // 2]] if i % 2 == 0 else [""])
        spacer(box.add_paragraph(), 8)

    header(["Member:", "Meeting Date:"], [1.25, 2.6, 1.1, 2.35])
    header(["Group #:", "Dollar value of issue:"], [1.25, 2.6, 1.5, 1.95])

    tbl = box.add_table(rows=2 * len(FORM_SECTIONS), cols=3)
    white_gaps(tbl)
    widths(tbl, [2.4, 4.75, 0.15])
    for i, (label, prompt) in enumerate(FORM_SECTIONS):
        lab, ans = tbl.rows[2 * i], tbl.rows[2 * i + 1]
        lab.height, lab.height_rule = Inches(0.26), WD_ROW_HEIGHT_RULE.AT_LEAST
        ans.height, ans.height_rule = Inches(0.4), WD_ROW_HEIGHT_RULE.AT_LEAST
        for c in lab.cells + ans.cells:
            shade(c, PANEL)
            c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            say(c, [""])
        lab.cells[1].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.BOTTOM
        say(lab.cells[1], [label])
        say(ans.cells[0], prompt)
        shade(ans.cells[1], WHITE)
    spacer(box.add_paragraph(), 6)
    spacer(doc.add_paragraph(), 1)  # Word needs a paragraph after the panel; keep it off page 2
    return doc


# ---------- filling ----------

def write(tc, value):
    """Replace the box's contents, keeping its paragraph formatting."""
    paras = tc.findall(qn("w:p"))
    template = copy.deepcopy(paras[0])
    for r in template.findall(qn("w:r")):
        template.remove(r)
    for p in paras:
        tc.remove(p)
    if isinstance(value, list):
        lines = ["•  " + str(v).strip() for v in value if str(v).strip()]
    else:
        lines = str(value).split("\n")
    ppr = template.find(qn("w:pPr"))
    mark = ppr.find(qn("w:rPr")) if ppr is not None else None
    for line in lines or [""]:
        p = copy.deepcopy(template)
        r = p.makeelement(qn("w:r"), {})
        rpr = copy.deepcopy(mark) if mark is not None else r.makeelement(qn("w:rPr"), {})
        if rpr.find(qn("w:rFonts")) is None:
            rpr.append(rpr.makeelement(qn("w:rFonts"), {qn("w:ascii"): FONT, qn("w:hAnsi"): FONT}))
        r.append(rpr)
        t = r.makeelement(qn("w:t"), {"{http://www.w3.org/XML/1998/namespace}space": "preserve"})
        t.text = line
        r.append(t)
        p.append(r)
        tc.append(p)


def compact_tail(doc):
    """A form ends with empty paragraphs after the last table. Once the boxes
       grow, those spill onto a blank second page, so shrink them to 1pt with
       no spacing. Word needs one paragraph after a final table, so they are
       shrunk rather than removed."""
    body = doc.element.body
    for el in reversed(list(body.iterchildren())):
        tag = el.tag.split("}")[1]
        if tag == "sectPr":
            continue
        if tag != "p" or "".join(t.text or "" for t in el.iter(qn("w:t"))).strip():
            break
        p = docx.text.paragraph.Paragraph(el, doc)
        p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(1)
        for run in p.runs:
            run.font.size = Pt(1)
        ppr = el.get_or_add_pPr()
        mark = ppr.find(qn("w:rPr"))
        if mark is None:
            mark = ppr.makeelement(qn("w:rPr"), {})
            ppr.append(mark)
        for tagname in ("w:sz", "w:szCs"):
            old = mark.find(qn(tagname))
            if old is not None:
                mark.remove(old)
            mark.append(mark.makeelement(qn(tagname), {qn("w:val"): "2"}))


def wanted():
    return list(HEADER.values()) + list(SECTIONS.values())


def cmd_check(form):
    boxes = find_boxes(docx.Document(form))
    missing = [k for k in wanted() if k not in boxes]
    print(json.dumps({"ok": not missing, "found": [k for k in wanted() if k in boxes],
                      "missing": missing}, indent=2))
    sys.exit(0 if not missing else 1)


def cmd_blank(out):
    blank_form().save(out)
    print(json.dumps({"ok": True, "wrote": out}, indent=2))


def cmd_fill(issue_path, out, form=None):
    doc = docx.Document(form) if form else blank_form()
    boxes = find_boxes(doc)
    with open(issue_path, encoding="utf-8") as f:
        issue = json.load(f)
    filled, empty, unplaced = [], [], []
    for key, val in issue.items():
        if key not in boxes:
            if val not in (None, "", []):
                unplaced.append(key)
            continue
        if val in (None, "", []):
            empty.append(key)
            continue
        write(boxes[key], val)
        filled.append(key)
    compact_tail(doc)
    doc.save(out)
    print(json.dumps({"ok": not unplaced, "wrote": out, "form": form or "drawn (unbranded)",
                      "filled": filled, "left_blank": empty + [k for k in boxes if k not in issue],
                      "no_box_on_form": unplaced}, indent=2))
    sys.exit(0 if not unplaced else 2)


if __name__ == "__main__":
    a = sys.argv[1:]
    form = None
    if "--form" in a:
        form = a[a.index("--form") + 1]
        a = [x for x in a if x not in ("--form", form)]
    if len(a) == 2 and a[0] == "check":
        cmd_check(a[1])
    elif len(a) == 2 and a[0] == "blank":
        cmd_blank(a[1])
    elif len(a) == 3 and a[0] == "fill":
        cmd_fill(a[1], a[2], form)
    else:
        sys.exit(__doc__)
