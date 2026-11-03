# Order workflow — every document order (WhatsApp, or Fiverr if reactivated)

Target: first message with the facts → checked letter + serving note in **under 20 minutes**.
Who does what: Fedya collects the facts and reads the result. Claude picks, fills and checks.

General information and templates only, not legal advice. For your specific case consult a licensed legal practitioner in the UAE.

> **Gate — before the first paid order:** the legal-services question in `/channels/research.md` §0 (Dubai AR 52/2022 Art. 5(a)) must be answered by a licensed UAE lawyer. Until then, do not take payment for filling documents.

## Time budget

| Stage | Who | Minutes |
|---|---|---|
| 1. Facts in | Fedya pastes the customer's facts to Claude | 2 |
| 2. Scope screen | Claude | 1 |
| 3. Pick template | Claude | 1 |
| 4. Split + fill + finalise | Claude | 5 |
| 5. 10-point check | Claude (tool + manual) | 3 |
| 6. Fedya reads | Fedya | 5 |
| 7. Deliver | Fedya | 2 |
| **Total** | | **19** |

## 1. Facts in

Fedya pastes the customer's answers. Five facts always, plus the extras for that document.

| # | Always ask | Example |
|---|---|---|
| 1 | Property: unit, building, community; Ejari number | Unit 1204, [building], [community]; Ejari 0123… |
| 2 | Contract dates: start and expiry | 1 Apr 2026 – 31 Mar 2027 |
| 3 | Rent (annual) and deposit | AED 100,000; deposit AED 5,000 |
| 4 | What happened | "Want to raise rent at renewal" |
| 5 | What they want | "A notice to the tenant" |
| + | Full names of both parties as in the contract; sender's contact details | |

Extras by template:
- **T01 rent change:** DLD Rental Index calculator result (screenshot), proposed new rent, any other changed terms.
- **T02 tenant non-renewal:** notice period and clause number from their contract (they read it, not us), move-out date, IBAN.
- **T03 12-month notice:** which of the four grounds, the supporting document reference, intended eviction date.
- **T04 deductions:** list of items, move-in and move-out checklist/photo refs, quotes or invoices, refund date.
- **T05 deposit return:** vacate and key-return dates, amount, IBAN, what evidence they have.
- **T06 repair:** what is broken, since when, earlier reports, access times.

## 2. Scope screen — stop if any of these

| Customer asks | Reply (copy) |
|---|---|
| "Read my contract / what does clause X mean?" | "I prepare the document from your facts, but I don't review or interpret contracts. For that, a licensed UAE legal practitioner is the right person." |
| "Am I allowed to…? / Will I win? / What should I do?" | "I can share the general rule and prepare the letter, but I can't advise on your specific case. A licensed UAE legal practitioner can." |
| A court or RDC case is already open | Decline: "As a case is already open, please work with a licensed legal practitioner." |
| The facts don't fit a ground in the law (e.g. landlord wants a tenant out at expiry for a reason not in T03) | Decline the document; share the general rule only. |
| Data about Fedya's employer's tenants, buildings or files | Decline. Never use employer data. |

## 3. Pick the template

| What they want | Side | Template |
|---|---|---|
| Raise or change rent/terms at renewal | Landlord | T01 |
| Not renew | Tenant | T02 |
| Get the property back at expiry (sale, own use, demolition, renovation) | Landlord | T03 |
| Keep part of the deposit | Landlord | T04 |
| Get the deposit back | Tenant | T05 |
| Get a repair done | Tenant | T06 |
| Inspection at start / end | Both | T07 / T08 |
| Understand contract terms | Both | T09 (send as is) |

Not covered yet (decline or quote separately): non-payment / 30-day notice, bounced cheque, early termination, short-term letting.

## 4. Split and fill

1. `python3 fiverr/tools/order_tools.py split T0X orders/<YYYY-MM-DD>-<initials>`
   → `letter.docx` (guidance removed) and `serving-note.pdf` (the "how and when to serve" note that comes with the AED 350 service).
2. Fill every orange `[placeholder]` in `letter.docx` from the facts. Delete options that don't apply (e.g. the unused ticks in T03).
3. Delete the proof-of-delivery rows and hand-delivery line that won't be used.
4. Rename to `<Template>-<property short>-<date>.docx`, e.g. `T01-Unit1204-2026-11-10.docx`.
5. After the check in §5 passes: `python3 fiverr/tools/order_tools.py finalise orders/<folder>/<file>.docx` → filled-in text turns plain black and the PDF is made.

`/orders` holds customer personal data. It is git-ignored: never uploaded to GitHub, deleted when the session ends. Fedya keeps the delivered copy.

## 5. Ten-point check (all must pass)

1. **Tool check passes:** `python3 fiverr/tools/order_tools.py check orders/<folder>/letter.docx` → "CHECK PASSED" (no unfilled `[ ]`, no risky wording, footer with legal basis and disclaimer).
2. **Right template and right side** (landlord vs tenant) for what the customer wants.
3. **Names** exactly as in the tenancy contract / Ejari; property and Ejari number correct.
4. **Deadline maths:** T01 — delivery at least 90 days before expiry. T03 — eviction date at least 12 months after service and not before expiry. Write the date calculation in the order notes.
5. **Money maths:** T01 — new rent ≤ the DLD calculator's maximum; % matches. T04 — deductions add up; balance = deposit − deductions.
6. **Service method** in the serving note matches the document (T03: notary or registered mail only).
7. **Attachments** listed in the letter are ones the customer actually has.
8. **No advice:** nothing about their chances, the meaning of their contract, or what they "should" do.
9. **Nothing from Fedya's employer**, and no other customer's data, anywhere in the files.
10. **Both files open** (DOCX and PDF), letter fits on 1–2 pages, layout clean.

## 6. Fedya reads

Fedya reads the PDF once, start to finish, and checks names, dates and amounts against what the customer sent. **Never send unread.** If anything is unclear, ask the customer rather than guess.

## 7. Deliver

Send three files: the letter as PDF and DOCX, plus the serving note PDF. Message (WhatsApp wording is in `/channels/whatsapp-flow.md`, Step 1B.4):
> "Here is your [document]. Please check the names, dates and amounts before you send it. The note explains when and how to serve it. General information and templates only, not legal advice."

Log the order in `PROGRESS.md` (template, date, minutes taken, price) — no customer names.

## Test run (2026-11-03, made-up facts)

T01 rent change, landlord, contract expiring 31 Mar 2027 (last day for notice 31 Dec 2026), rent AED 100,000, index average AED 120,000 → 5% band → AED 105,000. Split + fill + check + PDF took seconds of machine time; the check passed with no unfilled placeholders and no stray brackets. The 20-minute budget is driven by Fedya's collection and reading time, not the tooling.
