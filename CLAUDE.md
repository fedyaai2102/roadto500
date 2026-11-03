# CLAUDE-PLAYBOOK.md — Dubai tenancy documents income build

You are Claude Code working with Fedya. Your job: build five income projects in order, and walk Fedya through every step he has to do himself, one step at a time. Read this whole file before doing anything.

## 0. How to work with Fedya

Fedya is non-technical, runs a customer relations team at a Dubai landlord by day, and has about two hours on Tue/Thu/Sat evenings and 20 minutes on other days. He already has written approval from his employer to run side projects.

Rules you never break:

1. **Track progress in `PROGRESS.md`** at the repo root. Create it on the first run from the step list in this file. Every session starts with "read PROGRESS.md" and ends with updating it. Fedya will often start a session with just "continue".
2. **One step at a time.** Do the step, show Fedya the result in plain words, then stop and ask "OK to move on?" Do not run ahead.
3. **Steps tagged `[FEDYA]` are his.** You cannot do them (accounts, ID verification, payments, posting). For each one, give click-by-click instructions in short numbered lines, then wait until he types "done". Never ask for his passwords, card numbers or ID.
4. **Every legal figure gets a source retrieved today.** Notice periods, rent-increase slabs, fees, dates: search the web, open the page, cite the link and date in the file. No figure from memory. If you cannot find a source, write "VERIFY" and tell Fedya.
5. **Nothing is legal advice.** Products are templates and general information. Put this line on every document, page and listing: "General information and templates only, not legal advice. For your specific case consult a licensed legal practitioner in the UAE." Never interpret a customer's specific contract or tell them what to do.
6. **Nothing from Fedya's employer.** No tenant data, building names, internal documents or company name anywhere. His knowledge is his; their data is not.
7. **Steps tagged `★` get a fresh-eyes review before they ship.** Spawn a separate reviewer subagent that has not seen the work, give it the acceptance line, and fix what it finds. Fedya may also paste the output to his Fable chat; if he brings back notes, apply them.
8. **Ask before anything irreversible or that costs money** (buying a domain, paying for a tool, publishing a listing). State item and cost, wait for yes.
9. **Explain every command before running it**, in one plain sentence. Fedya should always know what just happened.
10. Keep replies short. Bottom line first, then the next action.

## 1. Context

- **This is a new, separate brand** in its own repo. Fedya has another project, DLandKit, with its own brand, domain and repo; do not use its name, domain, design or files here, and do not mention it in any product. Keep the two fully apart.
- **Brand name:** not chosen yet. First task of the first session: propose five short names (English, easy to spell, available as a .com or .ae and as a social handle; check availability), Fedya picks one, and it is used everywhere from then on. Until he picks, use `BRAND` as a placeholder.
- **Legal frame** to verify and cite: Dubai Law 26 of 2007 as amended by Law 33 of 2008 (tenancy), Decree 43 of 2013 (rent-increase slabs), the Dubai Land Department rental index and its 2026 status, RERA notice-service rules (notary public or registered mail). Dubai E-Trader licence (around AED 1,070/year — verify) is the launch structure; until then, sell through platforms that pay Fedya out (Fiverr, a digital storefront).
- **Money target:** 500 AED every month, recurring, by month three. Judge each project by recurring income, not first sale.

## 2. Repo layout to create on first run

```
PROGRESS.md            status of every step, updated each session
/fiverr                gig text, tags, FAQs, buyer form, order workflow, competitor table
/templates             master DOCX/PDF templates with sources (shared by all projects)
/pack                  the Move-Out Pack: files, product page, images, emails
/brand                 chosen name, logo, colours, one-page brand note
/calculator            single-file rent-increase and notice calculator
/articles              30 Q&A articles + keyword map + link map
/app                   waitlist page now; the SaaS later
/sources               one markdown file per legal fact: figure, link, retrieval date
```

## 3. Projects, in order

Do Projects 1 and 2 together in the first two weeks (they share `/templates`). Start 3 in week two. Start 4 from week three. Start 5 only after its gate.

---

### Project 1 — Fiverr gig: Dubai landlord and tenant documents

Goal: first paid order within 14 days of the gig going live; 300–800 AED in month one. Fiverr collects payment and pays out, so no invoicing problem. Fiverr keeps 20%, so quote every price to Fedya as the net figure.

What is sold: custom Dubai tenancy documents filled with the customer's facts, delivered in 24–48 hours: rent-increase notice, non-renewal notice, security-deposit deduction letter, deposit-return demand, maintenance-dispute letter, move-in and move-out condition checklists, and a plain-English glossary of standard RERA contract clauses. **Not** sold: review or interpretation of a customer's own contract.

Pricing (Fedya's; do not change without his yes):

| Tier | USD | Includes | Delivery |
|---|---|---|---|
| Basic | 25 | One notice or letter, one revision | 2 days |
| Standard | 60 | Any two documents + the RERA clause glossary | 2 days |
| Premium | 120 | Full move-out pack: checklist, deduction letter, deposit-return letter, dispute summary, 3 revisions | 1 day |

Steps:

1. `[CLAUDE]` Research Fiverr's current rules for legal-document services for a UAE seller (banned wording, legal-advice restrictions, payout methods). Then scan competitors: top 15 gigs for "Dubai tenancy", "Dubai rental agreement", "UAE legal letter" — price per tier, review count, delivery time. Save to `/fiverr/research.md` with links. Acceptance: a yes/no on whether the gig fits Fiverr's rules, plus the competitor table. `★` Then show Fedya the table and recommend whether the prices above should move.
2. `[FEDYA]` Create the Fiverr seller account and start ID verification (takes 1–2 days; start it now).
3. `[CLAUDE]` Draft the gig into `/fiverr/gig.md`: title under 80 characters with "Dubai tenancy" in it, five tags, 1,200-character description, three FAQs, and the buyer requirements form (property type, contract dates, rent, what happened, what they want). Acceptance: reads like a Dubai professional wrote it, disclaimer included, no legal-advice claim.
4. `[CLAUDE]` Build the master templates in `/templates`, one DOCX + PDF per document type, square-bracket placeholders, a "when to use" note and the governing rule cited with a link retrieved today, stored in `/sources`. Acceptance: every template cites its rule; no VERIFY left. `★` Reviewer checks every figure against its source.
5. `[CLAUDE]` Write `/fiverr/order-workflow.md`: the checklist followed on every order (read buyer form → pick template → fill → 10-point sanity check → clean PDF + DOCX). Acceptance: an order can be fulfilled in under 20 minutes.
6. `[FEDYA]` Upload the gig (you give him the fields one by one). Done = gig live.
7. `[CLAUDE]` Write the launch set into `/fiverr/launch.md`: one LinkedIn post, two forum answers for threads where people ask about deposits or notices (helpful answer first; gig link only if the forum allows), and a WhatsApp message for five people Fedya knows who own property. Acceptance: each message answers a real question; no spam tone.
8. `[FEDYA]` Post the launch set over three days, not one. Ask three property-owning contacts to place real full-price orders and leave honest reviews (zero-review gigs barely sell). Reply to every inquiry within an hour for the first two weeks.
9. `[CLAUDE]` On each order: Fedya pastes the buyer form; you fulfil it with the workflow; Fedya reads the result before delivering. Never deliver unread.
10. `[CLAUDE]` After the first three orders, write a one-paragraph summary (what was asked, delivered, rated) to `PROGRESS.md` and ask Fedya to bring it to Fable for the pricing decision.

---

### Project 2 — the Move-Out Pack

Goal: a one-time digital product at USD 39 that sells without Fedya's time per order. First sale realistically 2–4 weeks after launch; Projects 3 and 4 bring the traffic.

Product, "BRAND Move-Out Pack", one ZIP: move-in and move-out inspection checklists (room by room, photo log), deposit deduction letter, deposit-return letter, a one-page plain-English guide to what a Dubai landlord may and may not deduct, the notice-period cheat sheet (rent increase, non-renewal, eviction for sale or own use, non-payment), and a "first 30 days with a new tenant" calendar. Also a single checklist as a USD 9 tripwire.

Steps:

1. `[CLAUDE]` Research which storefronts pay out to a UAE resident without a company in 2026: Gumroad, Lemon Squeezy, Payhip, Etsy digital downloads. Payout routes (PayPal UAE, Payoneer, bank), fees, eligibility. Save to `/pack/storefront.md` as a table with a recommendation. `★` Fedya confirms the choice (and may check with Fable).
2. `[FEDYA]` Open the storefront account and connect the payout.
3. `[CLAUDE]` Assemble the pack in `/pack/files` from the reviewed `/templates`: one consistent design (the `/brand` assets), title, short intro, the document, the cited rule in a footer, as-of date, disclaimer, plus a README. Acceptance: a stranger could use it without asking a question. `★`
4. `[CLAUDE]` Write `/pack/product-page.md`: title, 150-word description leading with the deposit problem, contents list, three FAQs, a 60-word author note ("12 years in Dubai real estate", no employer name).
5. `[CLAUDE]` Make five product images in `/pack/images` at the storefront's sizes: cover, two blurred sample pages, contents list, "who it is for". Acceptance: readable on a phone.
6. `[CLAUDE]` Write `/pack/launch.md`: a LinkedIn post, posts for two Facebook groups where overseas Dubai owners gather (find the groups and their posting rules), and a 5-email buyer sequence (delivery, how to use, cheat sheet, review request, upsell), each under 150 words.
7. `[FEDYA]` Upload files and images, publish, post the launch set, add the product link to the Fiverr gig description as the self-serve option.
8. `[CLAUDE]` After 30 days or 10 sales: summarise sales, visits and sources in `PROGRESS.md`; Fedya takes it to Fable for the next-product decision.

---

### Project 3 — Free rent-increase and notice-period calculator

Goal: a one-page tool on the BRAND domain that ranks for "Dubai rent increase calculator"-type searches, captures emails, and sells the pack behind it. Earns nothing directly for 1–2 months; its job is traffic. Hosting is free.

Why it can win: the Dubai Land Department has an official increase calculator; this one answers what comes next — how much notice, by what date, what the letter says. Inputs: current rent, average market rent (user enters the index figure), renewal date. Outputs: allowed increase under the Decree 43/2013 slabs, last date to serve 90-day notice, a timeline for the other notice cases (12 months for sale or own use via notary or registered mail; 30 days for non-payment), and a "generate my notice letter" button that asks for an email and delivers the free cheat sheet plus a letter.

Steps:

1. `[CLAUDE]` Fact sheet to `/sources/calculator-facts.md`: slabs, rental-index status in 2026, the 90-day rule, eviction notice periods and service method, RERA notary fee if published. Every figure with link and retrieval date. `★` Wrong numbers here cost trust; the reviewer checks each one.
2. `[CLAUDE]` Build `/calculator/index.html`: single file, inputs, calculation, the timeline drawn on the page, plain-English explanation under each result, email form (Tally or Mailchimp/ConvertKit free tier — Fedya chooses), disclaimer. Mobile first. Acceptance: works offline in a browser, under 200 KB, no login, no cookies beyond the form.
3. `[CLAUDE]` SEO on the page: title, meta description, H1/H2 matching the 20 most likely searches (list them), FAQ block with FAQ schema, a "last updated" date. Acceptance: checklist of each item present.
4. `[FEDYA]` Buy the BRAND domain (ask first; about AED 40–60/year) and open the email tool's free tier.
5. `[CLAUDE]` Deploy to Cloudflare Pages or GitHub Pages on the BRAND domain; add Cloudflare Web Analytics (free) and Google Search Console. Walk Fedya through each click. Acceptance: live URL, analytics receiving.
6. `[CLAUDE]` Write `/calculator/distribution.md`: answers to ten existing questions on Reddit, Quora and Facebook groups where the tool is the answer, plus one LinkedIn post. Acceptance: the link answers the question asked.
7. `[FEDYA]` Post the answers over two weeks. Each month, ask Claude to re-verify the figures and bump the "last updated" date.
8. Metric: visits and emails per week. 50 emails = the pack has a buyer list and Project 5 has a waitlist. At 30 days live, summarise in `PROGRESS.md` for Fable.

---

### Project 4 — Dubai Tenancy Answers (30 articles on the BRAND domain)

Goal: 30 articles answering the exact questions landlords and tenants search for, monetised by the pack and the gig first and affiliates second. 3–4 weeks of evenings to build; realistically 0 income for about three months, then 500–2,000 AED/month if it ranks.

Fedya's edge: his team sees the real question patterns (AC failure, deposit not returned, Ejari lapse, bounced cheque). Use the patterns; never a real case, tenant or building.

Monetisation order: 1) The pack and the Fiverr gig linked from every relevant article. 2) Affiliate programmes paying for UAE referrals (movers, home insurance, cleaning, storage, furniture rental, Amazon.ae) — research which exist in 2026. 3) Display ads only after 10,000 visits/month.

Steps:

1. `[CLAUDE]` `/articles/keyword-map.md`: 60 candidate questions with search phrasing, who asks (landlord/tenant), and which product it leads to. `[FEDYA]` cuts to 30. `★`
2. `[CLAUDE]` Site skeleton: static site (Astro or plain HTML) on Cloudflare Pages: home, calculator, articles index, about, products. Acceptance: under one second on mobile; product call-to-action on every page.
3. `[CLAUDE]` Write articles five per session into `/articles`: 800–1,200 words, question as H1, answer in the first paragraph, cited law with links, a worked example with numbers, FAQ block with schema, as-of date, disclaimer. Acceptance per article: no figure without a source. Every fifth article `★` with the previous four.
4. `[FEDYA]` Read every article once before it is published. He is the fact check no model replaces.
5. `[CLAUDE]` `/articles/link-map.md`: each article links to three others and one product.
6. `[CLAUDE]` Affiliate research and sign-up instructions; insert links only where the reader would need that service, max two per article.
7. `[CLAUDE]` Per published article: one forum answer where someone asked that question; one LinkedIn post a week on the most-read article.
8. `[FEDYA]` Submit the sitemap to Search Console; report impressions weekly. At 15 and 30 articles, summarise in `PROGRESS.md` for Fable.

---

### Project 5 — BRAND Reminders (micro-SaaS)

Goal: 29 AED/month for owners of 1–5 units: rent and cheque reminders, Ejari and renewal alerts, 90-day notice countdown, one-click notices from the templates. 2–3 months to build. The only project that becomes a sellable asset. A second audience to test later: leasing executives at companies who still track lease dates and notices in Excel.

**Gate — do not start Phase B before:** 50 emails from Project 3, or 10 orders from Project 1. Below that there is no evidence anyone pays monthly.

Phase A, sell it before it exists (1 week):

1. `[CLAUDE]` `/app/waitlist/index.html`: the three alerts, a mock-up screenshot, the price, a "reserve at 19 AED/month for life" button collecting the email. Link it from the calculator and the pack emails. Target: 30 reservations in 30 days; under 15, stop and keep the money from Projects 1–4.

Phase B, the product (6–10 weeks, after Phase A passes):

1. `[CLAUDE]` Payments first, because it is the blocker: an individual without a trade licence cannot open Stripe UAE. Research merchant-of-record options accepting a UAE individual in 2026 (Lemon Squeezy, Paddle, Gumroad memberships) and whether an E-Trader licence unlocks Stripe or Tap. Table with fees and a recommendation. `★` Fedya decides (with Fable).
2. `[CLAUDE]` One-page spec with three screens as wireframes: add property and tenant; set contract and cheque dates; email + WhatsApp-link reminders. Nothing else in v1.
3. `[CLAUDE]` Build: Next.js (or similar) + Supabase (data, login) + scheduled job for reminders + the chosen payment provider. Deploy weekly. Acceptance per week: a deployed URL Fedya can click through. A week without a clickable change = stop and escalate.
4. `[CLAUDE]` Notice generator: `/templates` pre-filled from the tenant record. Acceptance: a correct 90-day notice in under one minute.
5. `[CLAUDE]` 3-email launch sequence + a 15-minute setup-call offer for the first 20 users. `[FEDYA]` does the calls; every complaint goes into `PROGRESS.md`. Acceptance: 10 paying users in month one.
6. At month three: numbers to Fable for continue, pivot or stop, and whether to get the E-Trader licence.

## 4. First session script

1. Read this file. Create `PROGRESS.md` listing every step above with status "todo".
2. Create the folders in section 2.
3. Propose five brand names with availability checked. Fedya picks one; write it to `/brand/name.md` and replace `BRAND` in `PROGRESS.md`.
4. Say to Fedya, in three lines: what you are about to do (Project 1 Step 1), roughly how long, and that you will stop after it.
5. Do Project 1 Step 1. Show the competitor table. Stop.
6. Then give Fedya Project 1 Step 2 (Fiverr account) click by click and wait for "done".
