# STEP 1B — Channel change

Given by Fedya on 2026-11-03. Overrides parts of CLAUDE.md Project 1 and adds Project 1B.

## What changed and why

Research showed Fiverr's buyers are mostly in the US and Europe; Dubai buyers are not shopping there. The product (Dubai tenancy documents) stays. The shopfront changes: we go to where Dubai landlords already ask questions and take orders by WhatsApp. Fiverr becomes an optional payment link for overseas buyers only.

## Project 1 — what to keep and what to pause

- **Keep and finish:** Step 1 (competitor and rules research — still useful for pricing), Step 4 (master templates with cited sources), Step 5 (order workflow).
- **Pause:** Steps 2, 3, 6, 7, 8 (Fiverr account, gig text, upload, Fiverr launch). Mark them "paused" in PROGRESS.md. Do not delete anything already written.
- Step 9 and 10 now apply to WhatsApp orders instead of Fiverr orders.

## Project 1B — Direct orders from landlord communities

Goal: 2–4 paid document orders in the first 30 days, paid by bank transfer or payment link, taken over WhatsApp. Every document comes from `/templates`, filled with the customer's facts, reviewed by Fedya before sending.

Prices (AED, Fedya's; do not change without his yes):

| Service | AED | Delivery |
|---|---|---|
| One notice or letter (rent increase, non-renewal, deposit deduction, deposit demand, maintenance dispute), with a plain-English note on how and when to serve it | 350 | 24 h |
| Move-out pack (inspection checklist, deduction letter, deposit-return letter, dispute summary) | 650 | 24 h |
| Broker licence: branded Landlord Pack for a brokerage to give its landlord clients, updated when the law changes | 750 one-off, or 150/month | 3 days |

Steps:

1. `[CLAUDE]` Research with web search and cite, into `/channels/research.md`:
   - The five largest Telegram groups and five largest Facebook groups for Dubai landlords and property owners, in Russian and in English (name, approximate members, posting rules, whether service offers are allowed).
   - How a UAE resident legally takes payment for a small service: Dubai E-Trader licence (current price, who is eligible, what it allows), and which payment-link providers work with it (Ziina, Tap, Stripe UAE, PayPal UAE, Mamo). Table with fees.
   - Whether selling to a brokerage (a company) needs anything beyond E-Trader.
   Acceptance: every claim has a link and a retrieval date. `★` Fedya decides licence and payment provider.
2. `[CLAUDE]` Write `/channels/telegram-answers-ru.md`: ten model answers in Russian to the questions Russian-speaking Dubai landlords actually ask (rent increase rules, 90-day notice, eviction for own use or sale, deposit deductions, Ejari renewal, bounced cheque, tenant not leaving, AC and maintenance responsibility, early termination, short-term letting). Each answer: the correct general rule with its source, 80–150 words, friendly, no legal advice, and one closing line offering the drafted notice for 350 AED by WhatsApp. Acceptance: Fedya can paste each one as-is; a Russian-speaking landlord would find it clearly more competent than other replies in the group.
3. `[CLAUDE]` Write `/channels/facebook-answers-en.md`: the same ten answers in English for the overseas-owner groups, with the same closing line. Acceptance: same standard.
4. `[CLAUDE]` Write `/channels/whatsapp-flow.md`: the order flow Fedya runs by hand — greeting, the five facts to collect (property, contract dates, rent, what happened, what they want), price confirmation, payment link, delivery message, review request. Each message under 60 words, in Russian and English. Acceptance: a new customer goes from first message to paid in under ten messages.
5. `[CLAUDE]` Write `/channels/broker-offer.md`: a one-page offer for small brokerages — the problem (agents get asked, have nothing to hand over), the pack contents, the two prices, what "updated when the law changes" means, and a 60-word WhatsApp pitch to a broker Fedya knows. Then a list of 20 target brokerages in Dubai with 5–30 agents (name, website, LinkedIn of the owner or manager) found by web search. Acceptance: Fedya can send the pitch to a broker tonight. `★`
6. `[CLAUDE]` Build `/channels/landlord-pack-broker/`: the broker version of the Move-Out Pack with a placeholder for the brokerage's logo and name on every page, as DOCX and PDF. Acceptance: swapping the logo takes under five minutes.
7. `[FEDYA]` Join the groups from Step 1 (Telegram and Facebook). Post nothing for the first three days; read what people ask.
8. `[FEDYA]` Apply for the E-Trader licence and set up the payment link (Claude gives click-by-click instructions from Step 1 research).
9. `[FEDYA]` Post two answers a week per group, from the files above, adapted to the actual question. Never post an advert; the closing line is the only offer. Reply to WhatsApp inquiries within an hour.
10. `[FEDYA]` Send the broker pitch to three brokers he knows personally, then to five from the list each week.
11. `[CLAUDE]` On each order: Fedya pastes the five facts; produce the document with the order workflow; Fedya reads it before sending. Never send unread.
12. `[CLAUDE]` After 30 days, summarise in `PROGRESS.md`: answers posted, inquiries, orders, broker replies, revenue. Fedya takes it to Fable.

## Projects 2–5

Unchanged, except: wherever they link to "the Fiverr gig", link to the WhatsApp order flow instead. Project 3 and 4 move up one week; they are the channel for Dubai-local buyers who search Google.
