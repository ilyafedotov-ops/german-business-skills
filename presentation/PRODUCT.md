# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: freelancers and sole traders in Germany (Freiberufler and Gewerbe), many of them expats working in a second language, who already use or could use Claude or Codex. They meet German paperwork early: tax registration, invoices with mandatory details, receipts, bank statements, tax returns and Finanzamt letters.

Secondary: German-speaking founders (served by a German edition), Steuerberater and accountants judging whether the kit is careful enough to recommend, and AI builders interested in how the skills are made.

Job on the launch surfaces (LinkedIn carousel, LinkedIn video, YouTube walkthrough): understand within seconds what the kit does, believe it is careful and practical, and try it with a made-up example.

## Product Purpose

German Business Kit is seven open-source skills for Claude and Codex that help a sole trader in Germany through the business lifecycle: starting and registration, daily work (proposals, invoices, payment follow-up, letters), accounting (receipts, bank matching, month close in the chosen system), tax (sourced research, checked estimates, return preparation, Finanzamt replies), services (banks, insurance, software) and changes (a new activity, a first hire, a pause, closing). Confirmed facts, documents and next steps are saved in one private business folder so work continues next time.

## Positioning

Not another app: skills for the assistant the user already uses. It prepares; the user decides and sends. Answers rest on official sources the assistant actually opened, state their assumptions and say what could not be checked. Review, booking, authorization, submission and the authority's answer stay separate, evidenced steps.

## Operating Context

Used inside Claude Code, the Claude app or Codex. The user's world: ELSTER, the Fragebogen zur steuerlichen Erfassung, Finanzamt letters in window envelopes, invoices, receipts, bank exports, and a private folder with 01 Inbox, 02 Documents, 03 Accounts, 04 Taxes and 05 Business.

## Capabilities and Constraints

- Preview release 0.14.0-preview.1, MIT licensed, on GitHub (ilyafedotov-ops/german-business-skills). The three real answers were produced with 0.13.0-preview.2 and stay labelled with that version.
- Conversations, user guides, message catalogs and report templates are supported in English, German and Russian. Letters to German authorities are drafted in German. There is no separate application: the assistant app is the interface.
- AI assistance, not tax or legal advice. No ELSTER transmission. No complete statutory tax engine. Content the assistant reads is processed by its AI provider.

## Brand Commitments

- Name: German Business Kit.
- No existing visual asset is binding (user, 25 Nov 2026: replace freely).
- Voice: plain, careful, warm, honest about limits; German terms kept and explained.
- Must not feel like: a generic AI startup, a cold Finanzamt form, something playful about money, or a dense slide that needs zooming on a phone.

## Evidence on Hand

- Three real questions answered in English (Berlin, Hamburg, Munich): `post/real-examples.md`; raw session logs are kept outside Git.
- The same three questions asked in German (runs of 25 Nov 2026).
- Real screenshots of Claude and Codex with the kit installed, in English, German and Russian (`installer/images/` in the repository). The demo scenes use these unedited; the conversations are fictional examples.
- Repository facts: 190+ commits since 25 Oct 2026, 500+ automated tests, attested releases.
- Absent, never to be invented: customers, testimonials, user counts, press, pricing beyond "free and open source".

## Product Principles

1. It prepares, you decide and send.
2. Sources over confidence: show where an answer comes from.
3. Admit limits where they apply, not in fine print only.
4. One clear next step at a time.
5. Plain language for second-language readers; official German terms kept and explained.

## Accessibility & Inclusion

Launch visuals are read on phones in the LinkedIn feed: text must read without zooming, one idea per slide. Many readers work in a second language.
