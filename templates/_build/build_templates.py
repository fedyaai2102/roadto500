"""Build Leaseletter master templates (DOCX) from the facts in /sources.

Run:  python3 templates/_build/build_templates.py
Then: soffice --headless --convert-to pdf --outdir templates templates/*.docx

Every legal statement below comes from a file in /sources (retrieved 2026-11-03).
When a source changes, edit the text here, bump AS_OF, rebuild.
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUT = Path(__file__).resolve().parent.parent
AS_OF = "3 November 2026"
VERSION = "v1.1"
DISCLAIMER = ("General information and templates only, not legal advice. "
              "For your specific case consult a licensed legal practitioner in the UAE.")

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
GREY = RGBColor(0x55, 0x5B, 0x66)
FILL = RGBColor(0xB4, 0x5F, 0x06)  # placeholder colour

# Official sources (all retrieved 2026-11-03; see /sources)
L26 = "https://dlp.dubai.gov.ae/Legislation%20Reference/2007/Law%20No.%20(26)%20of%202007%20Regarding%20regulation%20between%20the%20lessor%20and%20the%20lessee.html"
L33 = "https://dlp.dubai.gov.ae/Legislation%20Reference/2009/Law%20No.%20(33)%20of%202008%20Amending%20Law%20No.%20(26)%20of%202007.html"
D43 = "https://dlp.dubai.gov.ae/Legislation%20Reference/2013/Decree%20No.%20(43)%20of%202013%20Determining%20Rent%20Increase%20for%20Real%20Property.html"
D26 = "https://dlp.dubai.gov.ae/Legislation%20Reference/2013/Decree%2026%20of%202013.html"
SRI = "https://dubailand.gov.ae/en/news-media/the-smart-rent-index-mitigates-inflation-in-dubai-and-enhances-market-transparency/"
RI = "https://dubailand.gov.ae/en/eservices/rental-index/?lang=en"
RDC = "https://rdc.gov.ae/en/eservices/register-first-instance-lawsuit-rental/"
ECR72 = "https://dlp.dubai.gov.ae/Legislation%20Reference/2025/Executive%20Council%20Resolution%20No.%20(72)%20of%202025%20Amending%20Executive%20Council%20Resolution.html"
EJARI = "https://dubailand.gov.ae/en/eservices/register-renew-ejari-contract"
RET = "retrieved 2026-11-03"

PH = re.compile(r"(\[[^\]]+\])")


# ---------- low-level helpers ----------

def runs(par, text, bold=False, size=None, color=None, italic=False):
    """Add text; [placeholders] are coloured and bold so they are easy to find."""
    for part in PH.split(text):
        if not part:
            continue
        r = par.add_run(part)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        if PH.fullmatch(part):
            r.font.color.rgb = FILL
            r.bold = True
        elif color:
            r.font.color.rgb = color
    return par


def p(doc, text="", bold=False, size=None, color=None, italic=False, space_after=4, style=None):
    par = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    par.paragraph_format.space_after = Pt(space_after)
    runs(par, text, bold=bold, size=size, color=color, italic=italic)
    return par


def bullet(doc, text):
    par = doc.add_paragraph(style="List Bullet")
    par.paragraph_format.space_after = Pt(2)
    runs(par, text)
    return par


def heading(doc, text, size=12, color=NAVY, space_before=8):
    par = doc.add_paragraph()
    par.paragraph_format.space_before = Pt(space_before)
    par.paragraph_format.space_after = Pt(3)
    par.paragraph_format.keep_with_next = True
    r = par.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = color
    return par


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def table(doc, rows, widths=None, header=True, size=9):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if widths:
        t.autofit = False
        for j, w in enumerate(widths):
            t.columns[j].width = Cm(w)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.text = ""
            par = cell.paragraphs[0]
            par.paragraph_format.space_after = Pt(0)
            runs(par, str(val), bold=(header and i == 0), size=size)
            if header and i == 0:
                shade(cell, "E3E8EF")
            if widths:
                cell.width = Cm(widths[j])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def new_doc(code, title, basis):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(2.2)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    st.font.size = Pt(10.5)

    hp = sec.header.paragraphs[0]
    runs(hp, f"Leaseletter · Dubai tenancy documents · {code}", size=8, color=GREY)

    fp = sec.footer.paragraphs[0]
    runs(fp, f"Legal basis: {basis}. Law as of {AS_OF}. Template {code} {VERSION}.", size=7.5, color=GREY)
    fp2 = sec.footer.add_paragraph()
    runs(fp2, DISCLAIMER, size=7.5, color=GREY, italic=True)

    doc.core_properties.title = title
    doc.core_properties.author = "Leaseletter"
    return doc


def guidance_page(doc, title, sections, sources):
    p(doc, "GUIDANCE NOTES — remove these notes before sending", bold=True, size=9, color=FILL, space_after=2)
    heading(doc, title, size=16, space_before=0)
    for head, items in sections:
        heading(doc, head, size=11.5)
        for it in items:
            if isinstance(it, tuple) and it[0] == "table":
                table(doc, it[1], widths=it[2] if len(it) > 2 else None)
            else:
                bullet(doc, it)
    heading(doc, "Legal basis (official sources, " + RET + ")", size=11.5)
    for cite, url in sources:
        par = doc.add_paragraph(style="List Bullet")
        par.paragraph_format.space_after = Pt(2)
        runs(par, cite + " — ", size=9)
        runs(par, url, size=7.5, color=GREY)
    p(doc, "The English texts are the official translations published by the Supreme Legislation "
           "Committee, Dubai; the Arabic text prevails in case of conflict.", size=8.5, color=GREY, italic=True)
    p(doc, DISCLAIMER, size=9, bold=True, color=NAVY)


def parties_block(doc, frm_label, to_label):
    first = p(doc, "[Sender's name and address, or letterhead]", space_after=8)
    first.paragraph_format.page_break_before = True
    p(doc, "Date: [DD Month YYYY]")
    p(doc, f"To: [{to_label} full name, as in the tenancy contract]")
    p(doc, f"From: [{frm_label} full name] [— or: through authorised agent [agent name], under [power of attorney / management agreement ref]]")
    p(doc, "Property: [unit no.], [building], [community], Dubai")
    p(doc, "Ejari no.: [number]   ·   Tenancy contract dated [date], expiring on [expiry date]", space_after=8)


def signature_block(doc, role):
    p(doc, "Yours sincerely,", space_after=18)
    p(doc, "Signature: ______________________________")
    p(doc, f"Name: [full name]   ·   Capacity: [{role}]")
    p(doc, "Phone / email: [contact details]", space_after=8)


def proof_block(doc, methods):
    heading(doc, "Proof of delivery (keep with your copy)", size=10.5)
    table(doc, [["Method", "Reference / evidence", "Date"]] + [[m, "[ref]", "[date]"] for m in methods],
          widths=[5.5, 8, 3.5])


def save(doc, name):
    path = OUT / f"{name}.docx"
    doc.save(path)
    print("wrote", path.name)


# ---------- shared guidance snippets ----------

SERVE_GENERAL = [
    "The law defines a Notice as a written notification sent through a Notary Public, or delivered by registered mail, "
    "by hand, or by any other technological means approved by law (Law 26/2007 Art. 2, as amended by Law 33/2008).",
    "The law does not list which electronic means count. A Notary Public or registered mail gives the clearest proof of delivery.",
    "Government notary fee to attest a notice: AED 200 (Executive Council Resolution 72/2025). Other charges may apply.",
    "Keep a signed copy and the proof of delivery (notary record, registered-mail receipt, or the recipient's signed acknowledgement).",
]

SERVE_EVICTION = [
    "This notice must be served through a Notary Public or by registered mail only (Law 26/2007 Art. 25, as amended by Law 33/2008). "
    "Hand delivery, email or WhatsApp alone are not the methods named for eviction notices.",
    "If the matter goes to the Rental Disputes Center, it asks for the notarised notice with the notification officer's report, "
    "or the registered post with the acknowledgement receipt (RDC filing page).",
    "Government notary fee to attest a notice: AED 200 (Executive Council Resolution 72/2025). Other charges may apply.",
]

SCOPE = ("This template is general information. It does not decide whether the rule applies to your situation, "
         "and it does not interpret your tenancy contract. Disputes are decided by the Rental Disputes Center (Decree 26/2013).")


# ---------- 01 Rent-increase notice ----------

def t01():
    code = "T01"
    doc = new_doc(code, "Rent change at renewal — 90-day notice",
                  "Law 26/2007 Art. 13, 14 (as amended by Law 33/2008); Decree 43/2013 Art. 1, 3")
    guidance_page(doc, "Rent change at renewal — 90-day notice", [
        ("When to use", [
            "You are the landlord (or the landlord's authorised agent) and you want to change the rent, or another term, when the tenancy renews.",
            "Rent can be reviewed when the contract is renewed, before it expires (Art. 13, as amended).",
        ]),
        ("When to send it", [
            "The notice must be given at least 90 days before the contract expires, unless the parties agreed otherwise (Art. 14, as amended). "
            "If your contract sets a different period, that is a matter for your contract.",
            "How to count: take the expiry date and count back 90 days. Example: expiry 31 March 2027 → give notice no later than 31 December 2026. "
            "Send it earlier than the last day to allow time for delivery.",
            "Dubai Land Department: an increase is applied only if the landlord gave notice at least 90 days before expiry "
            "and the Smart Rent Index confirms the property is eligible. Without the 90-day notice, the increase is not applied.",
        ]),
        ("Check the maximum increase first", [
            "Run the official DLD Rental Index calculator for the unit (Dubai REST app, DLD website, DubaiNow, or the Ejari system) and attach the result.",
            "Decree 43/2013 caps the increase by how far the current rent is below the average rent of similar units (the percentage is of the current rent):",
            ("table", [["Current rent compared with the average for similar units", "Maximum increase"],
                       ["Up to 10% below", "No increase"],
                       ["11% to 20% below", "5%"],
                       ["21% to 30% below", "10%"],
                       ["31% to 40% below", "15%"],
                       ["More than 40% below", "20%"]], [11, 4]),
            "Worked example: current rent AED 100,000; index average AED 120,000. The current rent is 16.7% below the average "
            "(20,000 ÷ 120,000), which falls in the 11–20% band, so the maximum is 5% of AED 100,000 = AED 5,000. New rent at most AED 105,000.",
            "The calculator's result is the figure to rely on; use it rather than your own estimate.",
        ]),
        ("How to deliver it", SERVE_GENERAL),
        ("Before you send — check", [
            "Names and unit match the tenancy contract and Ejari.",
            "The delivery date is at least 90 days before the expiry date.",
            "The proposed increase is not more than the calculator allows, and the printout is attached.",
            "Signed by the landlord, or by an agent with written authority.",
        ]),
        ("What this template does not do", [SCOPE]),
    ], [
        ("Law 26/2007 Art. 13 and 14 as superseded by Law 33/2008 (90-day notice to amend terms)", L33),
        ("Law 26/2007 Art. 10 (RERA sets rent-increase criteria)", L26),
        ("Decree 43/2013 Art. 1 (increase bands) and Art. 3 (average from the RERA Rent Index)", D43),
        ("DLD statement on the Smart Rent Index and the 90-day notice, 16 Feb 2025", SRI),
        ("DLD Rental Index e-service", RI),
        ("Executive Council Resolution 72/2025, Schedule 1 (notary fee AED 200)", ECR72),
    ])

    parties_block(doc, "Landlord", "Tenant")
    heading(doc, "Notice of change to the rent at renewal", size=13, space_before=0)
    p(doc, "Dear [tenant name],")
    p(doc, "1. This is a notice under Article 14 of Law No. 26 of 2007 (as amended by Law No. 33 of 2008). "
           "On renewal of the tenancy contract for the property above, I wish to change the annual rent. "
           "This notice is given at least ninety (90) days before the contract expiry date of [expiry date].")
    p(doc, "2. The rent:")
    table(doc, [["", "AED"],
                ["Current annual rent", "[current rent]"],
                ["Proposed annual rent from [renewal start date]", "[new rent]"],
                ["Increase", "[difference] ([X]% of the current rent)"]], [11, 6])
    p(doc, "3. The Dubai Land Department Rental Index result dated [date] (copy attached) shows an average annual rent of "
           "AED [index average] for similar units and a maximum allowed increase of [Y]% for this property under Decree No. 43 of 2013. "
           "The proposed increase does not exceed this.")
    p(doc, "4. [All other terms of the tenancy contract remain unchanged.] [or: I also propose these changes: [list].]")
    p(doc, "5. Please let me know by [reply date] whether you wish to renew on these terms, so the renewal can be registered in Ejari.", space_after=10)
    signature_block(doc, "Landlord / authorised agent of the landlord")
    p(doc, "Attachment: DLD Rental Index result dated [date]", italic=True)
    proof_block(doc, ["Notary Public", "Registered mail", "By hand — tenant's signature below", "Other: [method]"])
    p(doc, "Received by tenant (hand delivery): Name [ ] · Signature ______________ · Date [ ]")
    save(doc, "T01-rent-increase-notice")


# ---------- 02 Tenant non-renewal notice ----------

def t02():
    code = "T02"
    doc = new_doc(code, "Tenant's notice of non-renewal", "Law 26/2007 Art. 6, 20, 21; Art. 2 (as amended by Law 33/2008)")
    guidance_page(doc, "Tenant's notice of non-renewal", [
        ("When to use", [
            "You are the tenant and you will not renew the tenancy contract when it expires.",
            "Landlords: a landlord who wants the property back at expiry can do so only on the grounds in Art. 25(2), with 12 months' notice — use template T03.",
        ]),
        ("When to send it", [
            "The tenancy law as amended in 2008 does not set a fixed notice period for simply not renewing. "
            "The notice period, if any, is the one in your tenancy contract.",
            "If the tenant stays on after expiry without objection from the landlord, the contract renews for the same term "
            "or for one year, whichever is shorter, on the same terms (Art. 6).",
            "Fill in the notice period and clause number from your own contract. This template does not interpret your contract.",
        ]),
        ("How to deliver it", SERVE_GENERAL),
        ("Next steps after sending", [
            "Ask for a joint move-out inspection and use template T08 (move-out checklist) with your T07 move-in checklist.",
            "The landlord may hold a security deposit and undertakes to refund it, or what remains of it, at expiry (Art. 20).",
            "At expiry the tenant returns the property in the condition received, except ordinary wear and tear or damage beyond the tenant's control (Art. 21).",
        ]),
        ("What this template does not do", [SCOPE]),
    ], [
        ("Law 26/2007 Art. 6 (automatic renewal), Art. 20 (deposit), Art. 21 (return condition)", L26),
        ("Law 26/2007 Art. 2, 14 and 25(2) as superseded by Law 33/2008", L33),
        ("Executive Council Resolution 72/2025, Schedule 1 (notary fee AED 200)", ECR72),
    ])

    parties_block(doc, "Tenant", "Landlord")
    heading(doc, "Notice that I will not renew the tenancy contract", size=13, space_before=0)
    p(doc, "Dear [landlord name],")
    p(doc, "1. I give notice that I do not wish to renew the tenancy contract for the property above, which expires on [expiry date].")
    p(doc, "2. This notice is given [number] days before the expiry date[, in line with the notice period in clause [clause no.] of the tenancy contract] [or: the tenancy contract does not set a notice period].")
    p(doc, "3. I will vacate the property and return the keys, access cards and remotes on or before [move-out date].")
    p(doc, "4. I would like to arrange a joint move-out inspection on [proposed date and time]. Please confirm or suggest another time.")
    p(doc, "5. Please refund the security deposit of AED [deposit amount], or the remainder with an itemised list of any deductions, "
           "at the end of the contract, to:")
    table(doc, [["Account name", "[name]"], ["Bank", "[bank]"], ["IBAN", "[IBAN]"]], [5, 12], header=False)
    p(doc, "6. My contact details after I move out: [phone, email, address].", space_after=10)
    signature_block(doc, "Tenant")
    proof_block(doc, ["Notary Public", "Registered mail", "By hand — landlord's signature below", "Other: [method]"])
    p(doc, "Received by landlord / agent (hand delivery): Name [ ] · Signature ______________ · Date [ ]")
    save(doc, "T02-tenant-non-renewal-notice")


# ---------- 03 Landlord eviction at expiry (12 months) ----------

def t03():
    code = "T03"
    doc = new_doc(code, "Landlord's 12-month notice to vacate at expiry",
                  "Law 26/2007 Art. 25(2) and Art. 26 (as amended by Law 33/2008)")
    guidance_page(doc, "Landlord's 12-month notice to vacate at expiry", [
        ("When to use", [
            "You are the landlord and you need the property back when the tenancy ends, for one of the four reasons in Art. 25(2) only:",
            "(a) demolish and reconstruct, or add new structures that would prevent the tenant from using the property — with the required permits;",
            "(b) restoration or comprehensive maintenance that cannot be carried out while the tenant occupies the property — verified by a technical report issued or certified by Dubai Municipality;",
            "(c) the owner's own use, or use by a first-degree relative — the owner must prove he does not own any alternative suitable property;",
            "(d) the owner wishes to sell the property.",
            "Not wanting to renew for any other reason is not one of these grounds.",
        ]),
        ("When to send it", [
            "The landlord must notify the tenant of the reasons at least 12 months before the date of eviction (Art. 25(2)).",
            "Count back 12 months from the eviction date you want. The eviction date cannot be earlier than the contract expiry date.",
            "Example: contract expires 30 November 2027 and you want vacant possession that day → serve the notice no later than 30 November 2026.",
            "Older guides quote 90 days: that was the 2007 text, replaced in 2008. The period is 12 months.",
        ]),
        ("How to deliver it", SERVE_EVICTION),
        ("Own use: rule on re-letting", [
            "If the Rental Disputes Center rules for the landlord on own use (ground c), the landlord may not rent the property to a third party "
            "for at least 2 years (residential) or 3 years (non-residential) from retaking possession (Art. 26).",
        ]),
        ("Before you send — check", [
            "Tick exactly one ground and attach the supporting document (permit, Dubai Municipality report, sale listing or agreement, or own-use statement).",
            "The eviction date is at least 12 months after the date of service and not before the contract expiry.",
            "Served by Notary Public or registered mail, and the proof is kept.",
        ]),
        ("What this template does not do", [
            SCOPE,
            "This notice does not by itself remove a tenant. If the tenant does not leave, the Rental Disputes Center decides.",
        ]),
    ], [
        ("Law 26/2007 Art. 25(2) and Art. 26 as superseded by Law 33/2008", L33),
        ("RDC filing page (documents required for an eviction case)", RDC),
        ("Executive Council Resolution 72/2025, Schedule 1 (notary fee AED 200)", ECR72),
    ])

    parties_block(doc, "Landlord", "Tenant")
    heading(doc, "Notice to vacate at the end of the tenancy — 12 months", size=13, space_before=0)
    p(doc, "Dear [tenant name],")
    p(doc, "1. Under Article 25(2) of Law No. 26 of 2007 (as amended by Law No. 33 of 2008), I notify you that I require vacant "
           "possession of the property above on [eviction date]. This date is not earlier than the contract expiry date of [expiry date] "
           "and is at least twelve (12) months after the date this notice is served on you.")
    p(doc, "2. The reason (one only):")
    p(doc, "☐  (d) I wish to sell the property.")
    p(doc, "☐  (c) I wish to retake possession for my own use / for use by my first-degree relative [name, relationship]. "
           "I confirm that I do not own any alternative real property suitable for this purpose.")
    p(doc, "☐  (a) I wish to demolish and reconstruct the property / add new structures that would prevent its use. Permit reference: [ref].")
    p(doc, "☐  (b) The property requires restoration or comprehensive maintenance that cannot be carried out while it is occupied. "
           "Dubai Municipality technical report reference: [ref].")
    p(doc, "3. Supporting documents attached: [list].")
    p(doc, "4. Please contact me to arrange the handover inspection and the return of the security deposit in line with the tenancy contract.", space_after=10)
    signature_block(doc, "Landlord / authorised agent of the landlord")
    proof_block(doc, ["Notary Public — notification officer's report", "Registered mail — acknowledgement receipt"])
    save(doc, "T03-landlord-12-month-notice-to-vacate")


# ---------- 04 Deposit deduction letter ----------

def t04():
    code = "T04"
    doc = new_doc(code, "Security deposit — statement of deductions", "Law 26/2007 Art. 20, 21; Decree 26/2013 Art. 6")
    guidance_page(doc, "Security deposit — statement of deductions", [
        ("When to use", [
            "You are the landlord, the tenant has moved out, and you are keeping part of the security deposit to cover damage or other amounts.",
        ]),
        ("The rules in plain English", [
            "The landlord may take a security deposit to ensure maintenance of the property at the end of the lease, and undertakes to refund it, "
            "or what remains of it, at expiry (Art. 20).",
            "The tenant must return the property in the same condition as received, except ordinary wear and tear or damage due to reasons beyond "
            "the tenant's control (Art. 21).",
            "The law does not define 'ordinary wear and tear', and it sets no cap on the deposit and no deadline for the refund beyond 'upon the expiry'.",
        ]),
        ("Build each deduction on evidence", [
            "For each item, show its condition at move-in (T07 move-in checklist, dated photos) and at move-out (T08 move-out checklist, dated photos).",
            "Attach a contractor quote or invoice for each amount.",
            "Refund the balance promptly and say how and when it will be paid.",
        ]),
        ("If the tenant disagrees", [
            "Give the tenant a date to reply in writing. If you cannot agree, either party may take the matter to the Rental Disputes Center, "
            "which has exclusive jurisdiction over Dubai rent disputes, with some exceptions such as free zones with their own rent tribunal (Decree 26/2013 Art. 6).",
        ]),
        ("What this template does not do", [SCOPE]),
    ], [
        ("Law 26/2007 Art. 20 (deposit) and Art. 21 (return condition)", L26),
        ("Decree 26/2013 Art. 6 (Rental Disputes Center jurisdiction)", D26),
    ])

    parties_block(doc, "Landlord", "Tenant")
    heading(doc, "Security deposit — statement of deductions", size=13, space_before=0)
    p(doc, "Dear [tenant name],")
    p(doc, "1. The tenancy of the property above ended on [end date]. You returned the keys on [date], and the move-out inspection took place "
           "on [date], attended by [names].")
    p(doc, "2. Under Article 20 of Law No. 26 of 2007, the deposit is refunded, or what remains of it, at the end of the tenancy. "
           "Under Article 21, the property is returned in the condition received, except ordinary wear and tear. "
           "The deductions below relate to items that were in better condition at move-in, as shown in the attached checklists and photos.")
    table(doc, [["No.", "Item and location", "At move-in (checklist / photo ref)", "At move-out (checklist / photo ref)", "AED", "Quote / invoice"],
                ["1", "[item]", "[ref]", "[ref]", "[amount]", "[ref]"],
                ["2", "[item]", "[ref]", "[ref]", "[amount]", "[ref]"],
                ["3", "[item]", "[ref]", "[ref]", "[amount]", "[ref]"]], [1, 4.2, 3.4, 3.4, 2, 3])
    table(doc, [["Security deposit held", "AED [deposit]"],
                ["Total deductions", "AED [total deductions]"],
                ["Balance to refund", "AED [balance]"]], [11, 6], header=False)
    p(doc, "3. The balance of AED [balance] will be paid by [bank transfer / cheque] to [account / name] on or before [date].")
    p(doc, "4. If you disagree with any item, please reply in writing by [reply date] with your reasons, so we can try to settle it.", space_after=10)
    signature_block(doc, "Landlord / authorised agent of the landlord")
    p(doc, "Attachments: move-in checklist dated [date]; move-out checklist dated [date]; photos [nos.]; quotes/invoices [refs].", italic=True)
    proof_block(doc, ["Registered mail", "Email to [address] — keep the sent copy", "By hand — tenant's signature below", "Other: [method]"])
    p(doc, "Received by tenant (hand delivery): Name [ ] · Signature ______________ · Date [ ]")
    save(doc, "T04-deposit-deduction-letter")


# ---------- 05 Deposit-return request ----------

def t05():
    code = "T05"
    doc = new_doc(code, "Request for return of security deposit", "Law 26/2007 Art. 20, 21; Decree 26/2013 Art. 6")
    guidance_page(doc, "Request for return of security deposit", [
        ("When to use", [
            "You are the tenant, the tenancy has ended, and the deposit (or part of it) has not been refunded, or deductions were made without explanation.",
        ]),
        ("The rules in plain English", [
            "The landlord may take a security deposit and undertakes to refund it, or what remains of it, at the end of the tenancy (Art. 20).",
            "The tenant returns the property in the condition received, except ordinary wear and tear or damage beyond the tenant's control (Art. 21).",
            "The law sets no fixed deadline for the refund beyond 'upon the expiry', so this letter asks for payment by a date you choose.",
        ]),
        ("Attach your evidence", [
            "Move-in checklist (T07) and move-out checklist (T08), dated photos, the key-handover receipt, and the final utility clearance if you have it.",
        ]),
        ("How to deliver it", SERVE_GENERAL[:2] + [SERVE_GENERAL[3]]),
        ("If it is not resolved", [
            "Either party may take the matter to the Rental Disputes Center, which hears Dubai rent disputes (Decree 26/2013 Art. 6). "
            "The RDC filing fee for a money claim is 3.5% of the amount claimed, minimum AED 500, maximum AED 15,000, plus small service fees (RDC filing page).",
        ]),
        ("What this template does not do", [SCOPE]),
    ], [
        ("Law 26/2007 Art. 20 (deposit) and Art. 21 (return condition)", L26),
        ("Decree 26/2013 Art. 6 (Rental Disputes Center jurisdiction)", D26),
        ("RDC filing page (fees)", RDC),
    ])

    parties_block(doc, "Tenant", "Landlord")
    heading(doc, "Request for return of the security deposit", size=13, space_before=0)
    p(doc, "Dear [landlord name],")
    p(doc, "1. The tenancy of the property above ended on [end date]. I vacated on [date] and returned the keys, access cards and remotes on [date]"
           "[, and the move-out inspection took place on [date]].")
    p(doc, "2. Under Article 20 of Law No. 26 of 2007, the landlord undertakes to refund the security deposit, or what remains of it, "
           "at the end of the tenancy. I paid a security deposit of AED [deposit amount].")
    p(doc, "3. I request:")
    p(doc, "☐  the full refund of AED [deposit amount]; or")
    p(doc, "☐  the refund of AED [amount], together with an itemised statement and evidence (photos, quotes or invoices) for any deduction,")
    p(doc, "by [payment date], to:")
    table(doc, [["Account name", "[name]"], ["Bank", "[bank]"], ["IBAN", "[IBAN]"]], [5, 12], header=False)
    p(doc, "4. I attach the move-in checklist dated [date], the move-out checklist / photos dated [date], and the key-handover receipt.")
    p(doc, "5. I would prefer to settle this directly. If we cannot agree, either of us may refer the matter to the Rental Disputes Center.", space_after=10)
    signature_block(doc, "Tenant")
    proof_block(doc, ["Registered mail", "Email to [address] — keep the sent copy", "By hand — landlord's signature below", "Other: [method]"])
    p(doc, "Received by landlord / agent (hand delivery): Name [ ] · Signature ______________ · Date [ ]")
    save(doc, "T05-deposit-return-request")


# ---------- 06 Maintenance request ----------

def t06():
    code = "T06"
    doc = new_doc(code, "Request for repair (maintenance)", "Law 26/2007 Art. 15 (as amended by Law 33/2008), 16, 17, 19")
    guidance_page(doc, "Request for repair (maintenance)", [
        ("When to use", [
            "You are the tenant and something in the property needs repair — for example the air conditioning, a leak, or electrics — "
            "and earlier requests have not been acted on.",
        ]),
        ("The rules in plain English", [
            "Unless otherwise agreed, the landlord is responsible during the tenancy for maintenance works and for repairing any defect or damage "
            "that may affect the tenant's intended use of the property (Art. 16).",
            "The landlord is responsible for defects, damage and wear and tear not caused by the tenant's fault (Art. 17).",
            "The landlord must hand over the property in good condition that allows full use as stated in the contract (Art. 15, as amended).",
            "The tenant must pay rent on time, maintain the property as an ordinary person would maintain their own, and not carry out changes or "
            "maintenance works without the landlord's permission and the required licences (Art. 19).",
            "'Unless otherwise agreed' means your contract may move some maintenance to the tenant. Check your own contract; this template does not interpret it.",
            "The law sets no repair deadline, so the letter asks for a reasonable date.",
        ]),
        ("Attach your evidence", [
            "Dated photos or video, earlier messages or ticket numbers, and any technician's report.",
        ]),
        ("How to deliver it", SERVE_GENERAL[:2] + [SERVE_GENERAL[3]]),
        ("If it is not resolved", [
            "Either party may take the matter to the Rental Disputes Center (Decree 26/2013 Art. 6).",
        ]),
        ("What this template does not do", [SCOPE]),
    ], [
        ("Law 26/2007 Art. 16, 17, 19", L26),
        ("Law 26/2007 Art. 15 as superseded by Law 33/2008", L33),
        ("Decree 26/2013 Art. 6 (Rental Disputes Center jurisdiction)", D26),
    ])

    parties_block(doc, "Tenant", "Landlord")
    heading(doc, "Request for repair: [short description, e.g. air conditioning not cooling]", size=13, space_before=0)
    p(doc, "Dear [landlord name],")
    p(doc, "1. The problem: [describe the defect and where it is]. I first noticed it on [date].")
    p(doc, "2. How it affects the use of the property: [e.g. the bedroom cannot be used / no cooling during the day].")
    p(doc, "3. Earlier reports: [date and method of each earlier report, ticket numbers].")
    p(doc, "4. Under Article 16 of Law No. 26 of 2007, unless otherwise agreed, the landlord is responsible during the tenancy for maintenance "
           "works and for repairing any defect or damage that may affect the tenant's intended use of the property.")
    p(doc, "5. I request that the repair is completed by [date]. Access is available on [days and times]; please contact me on [phone] to arrange it.")
    p(doc, "6. Photos and earlier messages are attached.", space_after=10)
    signature_block(doc, "Tenant")
    proof_block(doc, ["Email to [address] — keep the sent copy", "Registered mail", "By hand — landlord's signature below", "Other: [method]"])
    p(doc, "Received by landlord / agent (hand delivery): Name [ ] · Signature ______________ · Date [ ]")
    save(doc, "T06-maintenance-repair-request")


# ---------- 07/08 Checklists ----------

ROOMS = [
    ("Entrance / hallway", ["Front door, lock, keys", "Walls and paint", "Floor", "Lights and switches"]),
    ("Living / dining", ["Walls and paint", "Ceiling", "Floor", "Windows, blinds, curtains", "Lights, switches, sockets", "AC vent and thermostat"]),
    ("Kitchen", ["Cabinets and worktop", "Sink and taps", "Hob / oven / hood", "Fridge / freezer", "Washing machine / dishwasher", "Walls, floor, tiles"]),
    ("Bedroom 1", ["Walls and paint", "Floor", "Wardrobes", "Windows, blinds", "Lights, sockets", "AC vent and thermostat"]),
    ("Bedroom 2", ["Walls and paint", "Floor", "Wardrobes", "Windows, blinds", "Lights, sockets", "AC vent and thermostat"]),
    ("Bathroom 1", ["Toilet and flush", "Basin and taps", "Shower / bath, screen", "Tiles and grout", "Extractor fan", "Mirror and fittings"]),
    ("Bathroom 2", ["Toilet and flush", "Basin and taps", "Shower / bath, screen", "Tiles and grout", "Extractor fan", "Mirror and fittings"]),
    ("Balcony / terrace", ["Floor and drain", "Railing", "Sliding door and lock"]),
    ("Other rooms (maid's room, storage, laundry)", ["[item]", "[item]"]),
]


def header_facts(doc, title, keys_label="Keys, access cards, remotes handed over"):
    h = heading(doc, title, size=14, space_before=0)
    h.paragraph_format.page_break_before = True
    table(doc, [["Property", "[unit no.], [building], [community], Dubai"],
                ["Ejari no. / contract dates", "[number] · [start date] to [expiry date]"],
                ["Inspection date and time", "[date, time]"],
                ["Landlord / agent present", "[name]"],
                ["Tenant present", "[name]"],
                ["Electricity / water meter readings", "[reading] / [reading] (photo [no.])"],
                [keys_label, "[number of each]"],
                ["Furnished?", "☐ Unfurnished  ☐ Semi-furnished  ☐ Furnished (list items in 'Other rooms')"]],
          [6, 11], header=False)
    p(doc, "Condition codes: G = good · F = fair (minor marks) · P = poor / damaged · N/A = not present", size=9, italic=True)


def signatures(doc):
    heading(doc, "Signatures", size=11)
    table(doc, [["", "Name", "Signature", "Date"],
                ["Landlord / agent", "[name]", "", "[date]"],
                ["Tenant", "[name]", "", "[date]"]], [4, 5, 5, 3])


def photo_log(doc):
    heading(doc, "Photo log", size=11)
    p(doc, "Take dated photos of every room and every item marked F or P. Number them and list them here.", size=9)
    table(doc, [["Photo no.", "Room", "Item", "What it shows"]] + [["[no.]", "", "", ""] for _ in range(8)], [2.2, 3.5, 4, 7.3])


def t07():
    code = "T07"
    doc = new_doc(code, "Move-in condition checklist", "Law 26/2007 Art. 15 (as amended by Law 33/2008), Art. 21")
    guidance_page(doc, "Move-in condition checklist", [
        ("When to use", [
            "On the day the tenant receives the keys, with landlord (or agent) and tenant present. Both sign, both keep a copy.",
        ]),
        ("Why it matters", [
            "The landlord must hand over the property in good condition that allows full use as stated in the contract (Art. 15, as amended).",
            "At the end, the tenant returns the property in the same condition as received, except ordinary wear and tear or damage beyond the tenant's "
            "control (Art. 21). This checklist is the record of 'the condition received'.",
        ]),
        ("How to fill it in", [
            "Go room by room. Mark each item G, F, P or N/A and write a short note for anything not G.",
            "Photograph every room and each F or P item; write the photo numbers in the table and the photo log.",
            "Record meter readings and the number of keys and cards.",
            "Use the same list at move-out (template T08) so the two can be compared line by line.",
        ]),
        ("What this template does not do", [SCOPE]),
    ], [
        ("Law 26/2007 Art. 15 as superseded by Law 33/2008 (handover in good condition)", L33),
        ("Law 26/2007 Art. 21 (return in the condition received)", L26),
    ])
    header_facts(doc, "Move-in condition checklist")
    for room, items in ROOMS:
        heading(doc, room, size=10.5, space_before=4)
        table(doc, [["Item", "Code", "Notes", "Photo no."]] + [[i, "", "", ""] for i in items], [5, 1.5, 8, 2.5])
    photo_log(doc)
    signatures(doc)
    save(doc, "T07-move-in-checklist")


def t08():
    code = "T08"
    doc = new_doc(code, "Move-out condition checklist", "Law 26/2007 Art. 20, 21")
    guidance_page(doc, "Move-out condition checklist", [
        ("When to use", [
            "On the day the tenant hands back the keys, with landlord (or agent) and tenant present, next to the signed move-in checklist (T07).",
        ]),
        ("Why it matters", [
            "The tenant returns the property in the same condition as received, except ordinary wear and tear or damage beyond the tenant's control (Art. 21).",
            "The landlord undertakes to refund the security deposit, or what remains of it, at expiry (Art. 20). Any deduction should be traceable to a line "
            "on this checklist where the condition is worse than at move-in.",
            "The law does not define 'ordinary wear and tear'. Record what you see; the 'agreed?' column shows whether both parties accept the note.",
        ]),
        ("How to fill it in", [
            "Copy the move-in code for each item, then mark the move-out code.",
            "Photograph every item that changed; write the photo numbers in the table and the photo log.",
            "Record final meter readings and count the keys and cards returned.",
            "If the parties disagree on an item, write both views in the notes. Deductions go in template T04 (landlord) or are queried with T05 (tenant).",
        ]),
        ("What this template does not do", [SCOPE]),
    ], [
        ("Law 26/2007 Art. 20 (deposit) and Art. 21 (return condition)", L26),
    ])
    header_facts(doc, "Move-out condition checklist", "Keys, access cards, remotes returned")
    p(doc, "Move-in checklist dated: [date]", bold=True)
    for room, items in ROOMS:
        heading(doc, room, size=10.5, space_before=4)
        table(doc, [["Item", "In", "Out", "Notes (what changed)", "Photo no.", "Agreed?"]] + [[i, "", "", "", "", "☐ Y ☐ N"] for i in items],
              [4.2, 1.1, 1.1, 6.2, 2, 2.4])
    photo_log(doc)
    heading(doc, "Tenant's forwarding details", size=11)
    table(doc, [["Forwarding address / contact (tenant)", "[details]"]], [7, 10], header=False)
    signatures(doc)
    save(doc, "T08-move-out-checklist")


# ---------- 09 Glossary ----------

GLOSSARY = [
    ("The tenancy law",
     "Law No. 26 of 2007 regulating the relationship between landlords and tenants in Dubai. Law No. 33 of 2008 replaced eleven of its articles "
     "(2, 3, 4, 9, 13, 14, 15, 25, 26, 29, 36); the two are always read together.", "Law 26/2007; Law 33/2008 Art. 1"),
    ("Ejari (registration)",
     "All tenancy contracts, and any amendments, must be registered with RERA (the Real Estate Regulatory Agency). Registration is done through "
     "the DLD's Ejari service. DLD fee: AED 177.75 in total online (Dubai REST app or DLD website), AED 220 at a Real Estate Services Trustee Centre. "
     "The law does not say who pays; the contract may.", "Law 26/2007 Art. 4(2) as amended; DLD Ejari service page"),
    ("Notice",
     "A written notification sent through a Notary Public, or delivered by registered mail, by hand, or by any other technological means approved by law. "
     "Eviction notices are stricter: Notary Public or registered mail only.", "Art. 2 and Art. 25 as amended"),
    ("Automatic renewal",
     "If the contract expires and the tenant stays on without objection from the landlord, it renews for the same term or one year, "
     "whichever is shorter, on the same terms.", "Art. 6"),
    ("Changing the rent or terms at renewal",
     "Rent and terms can be reviewed at renewal. A party who wants to change a term must give notice at least 90 days before expiry, "
     "unless the parties agreed otherwise.", "Art. 13 and 14 as amended"),
    ("Rent-increase cap",
     "The maximum increase depends on how far the current rent is below the average rent for similar units: up to 10% below — none; "
     "11–20% — 5%; 21–30% — 10%; 31–40% — 15%; more than 40% — 20% (of the current rent). The average comes from the DLD rental index "
     "(the Smart Rental Index since 2 January 2025); the DLD calculator gives the allowed figure.", "Decree 43/2013 Art. 1, 3; DLD releases 2025"),
    ("Security deposit",
     "The landlord may take a deposit to ensure maintenance of the property at the end of the lease and undertakes to refund it, or the remainder, "
     "at expiry. The law sets no cap and no refund deadline.", "Art. 20"),
    ("Condition at the end / ordinary wear and tear",
     "The tenant returns the property in the condition received, except ordinary wear and tear or damage beyond the tenant's control. "
     "The law does not define 'ordinary wear and tear'.", "Art. 21"),
    ("Handover in good condition",
     "The landlord hands over the property in good condition that allows the tenant to use it fully as stated in the contract.", "Art. 15 as amended"),
    ("Maintenance",
     "Unless otherwise agreed, the landlord handles maintenance and repairs of defects that affect the tenant's intended use, and defects not caused "
     "by the tenant. The tenant maintains the property as an ordinary person would and makes no works without permission and licences.", "Art. 16, 17, 19"),
    ("Eviction during the contract",
     "Only on the grounds listed in the law, for example non-payment: if the tenant does not pay within 30 days of a notice requesting payment "
     "(unless otherwise agreed). Other grounds include unapproved subletting, illegal use, and serious damage. Notice by Notary Public or registered mail.",
     "Art. 25(1) as amended"),
    ("Eviction at the end of the contract",
     "Only to demolish/reconstruct (with permits), for restoration that needs the property empty (Dubai Municipality report), for the owner's or a "
     "first-degree relative's own use (owner has no other suitable property), or to sell. At least 12 months' notice before the eviction date, by "
     "Notary Public or registered mail.", "Art. 25(2) as amended"),
    ("Re-letting after own use",
     "If the landlord retakes the property for own use, it may not be rented to a third party for at least 2 years (residential) or 3 years "
     "(non-residential).", "Art. 26 as amended"),
    ("Rental Disputes Center (RDC)",
     "Hears all Dubai landlord–tenant rent disputes, including free zones, with listed exceptions. Filing fee for most cases: 3.5% of the annual rent, "
     "minimum AED 500, maximum AED 20,000; money claims: 3.5% of the amount claimed, minimum AED 500, maximum AED 15,000; plus small service fees.",
     "Decree 26/2013 Art. 6; RDC filing page"),
    ("Notary Public",
     "Government notary fee to attest a legal notice: AED 200. Other charges may apply for serving it.", "Executive Council Resolution 72/2025"),
    ("'Unless otherwise agreed'",
     "Several rules (notice to amend terms, maintenance, the 30-day non-payment period) let the contract set a different arrangement. "
     "Read your own contract alongside the law.", "Art. 14, 16, 25(1)(a)"),
]


def t09():
    code = "T09"
    doc = new_doc(code, "Dubai tenancy terms — plain-English glossary", "Law 26/2007 as amended by Law 33/2008; Decrees 43/2013 and 26/2013")
    heading(doc, "Dubai tenancy terms — plain-English glossary", size=16, space_before=0)
    p(doc, "Standard terms you will meet in a Dubai tenancy contract, with the rule behind each one. Law as of " + AS_OF + ".", color=GREY)
    p(doc, "When to use: read it alongside your own tenancy contract when signing, renewing or ending a Dubai tenancy, "
           "to understand the standard terms. It does not interpret your contract.", space_after=4)
    p(doc, DISCLAIMER, bold=True, size=9.5, color=NAVY, space_after=8)
    table(doc, [["Term", "What it means", "Rule"]] + [[a, b, c] for a, b, c in GLOSSARY], [3.6, 10.4, 3], size=9)
    heading(doc, "Official sources (" + RET + ")", size=11)
    for cite, url in [("Law 26/2007", L26), ("Law 33/2008 (amending)", L33), ("Decree 43/2013", D43), ("Decree 26/2013", D26),
                      ("DLD Smart Rental Index launch, 2 Jan 2025", "https://dubailand.gov.ae/en/news-media/smart-rental-index-announcement"),
                      ("DLD Smart Rent Index statement, 16 Feb 2025", SRI), ("DLD Ejari service", EJARI), ("RDC filing page", RDC),
                      ("Executive Council Resolution 72/2025", ECR72)]:
        par = doc.add_paragraph(style="List Bullet")
        par.paragraph_format.space_after = Pt(1)
        runs(par, cite + " — ", size=9)
        runs(par, url, size=7.5, color=GREY)
    p(doc, "The English texts are the official translations published by the Supreme Legislation Committee, Dubai; "
           "the Arabic text prevails in case of conflict.", size=8.5, color=GREY, italic=True)
    save(doc, "T09-tenancy-terms-glossary")


if __name__ == "__main__":
    for f in (t01, t02, t03, t04, t05, t06, t07, t08, t09):
        f()
