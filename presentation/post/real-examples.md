# Real questions, real answers

Three questions from fictional people, each asked in a fresh, isolated Claude Code session with the released
German Business Kit 0.13.0-preview.2 (Claude Opus 5.5, high effort) on 25 November 2026. No personal settings,
plugins or MCP servers were loaded; tools allowed: web search/fetch, file reading and Python for arithmetic.
The answers below are unedited. AI-assisted self-help, not tax or legal advice.

## Berlin · Freiberufler or Gewerbe?

**Question** (skill `de-business-start`):

> Use de-business-start. I live in Berlin and have a full-time job as an employee. On the side I want to translate documents between German and Russian for private clients and small companies, maybe 800 euros a month. Is that Freiberufler or Gewerbe, what exactly do I need to register, and where? Please include links to the official sources.

**Run:** 32 s · tools: Skill ×1, Read ×6, ToolSearch ×1, WebSearch ×3, Agent ×3, WebFetch ×10

**Pages fetched:**

- https://service.berlin.de/dienstleistung/325409/
- https://www.berlin.de/sen/finanzen/steuern/informationen-fuer-steuerzahler-/faq-steuern/artikel.558266.php
- https://www.elster.de/elsterweb/infoseite/unternehmensgruendung
- https://www.gesetze-im-internet.de/estg/__18.html
- https://www.gesetze-im-internet.de/ustg_1980/__19.html
- https://www.gesetze-im-internet.de/estg/__46.html
- https://www.gesetze-im-internet.de/ao_1977/__138.html
- https://www.gesetze-im-internet.de/gewo/__6.html
- https://service.berlin.de/dienstleistung/328825/
- https://service.berlin.de/dienstleistung/328825/standort/326333/en/

**Answer:**

## Short answer: Freiberufler, not Gewerbe

Translating counts as a freelance profession. **§18(1) No. 1 EStG** lists *"Dolmetscher, Übersetzer"* by name among the freie Berufe. So in Berlin you need **one registration, with the tax office (Finanzamt) through ELSTER**. You don't need a Gewerbeanmeldung at the Ordnungsamt, and you don't join the IHK.

**One condition:** this holds if you do the translations yourself. If you later mostly pass jobs on to other translators and act as an agency, the classification can change. Then you'd need to check again.

## What to register, and where

**1. Tax registration: required, free of charge**
- **Form:** "Fragebogen zur steuerlichen Erfassung" (for a sole trader, Einzelunternehmen). It must be sent electronically through **Mein ELSTER**, so create a free account first. The account must be the full one: an account set up with e-mail only can send nothing but this questionnaire.
- **Deadline:** within **one month after you start the activity**. You don't wait to be asked. ELSTER: *"innerhalb eines Monats nach Aufnahme Ihrer Tätigkeit unaufgefordert"*. §138 AO says the same for freelancers: *"Wer eine freiberufliche Tätigkeit aufnimmt, hat dies dem … zuständigen Finanzamt mitzuteilen"*.
- **Which Finanzamt:** Berlin has 17 regional tax offices for individuals, assigned by area. Find yours by entering your address in the BZSt Finanzamtsuche or on Berlin's responsibility page (links below).
- **Result:** you receive a tax number (Steuernummer) for your freelance income. You need it on your invoices.

**2. VAT decision in the questionnaire: Kleinunternehmerregelung (§19 UStG)**
- About €800 a month is roughly €9,600 a year. Berlin's FAQ says that in the founding year only the **€25,000** limit matters. After that, the limits are €25,000 for the previous year and €100,000 for the current year.
- As a Kleinunternehmer you charge no VAT and don't file VAT returns.
- If you instead opt out of the scheme, that choice binds you for **5 years**.
- **This only applies if this is your only self-employed activity.** VAT counts all of your business activities together.

**3. Gewerbeanmeldung:** not needed. Berlin's FAQ requires the Ordnungsamt notification only for a *"gewerbliche Tätigkeit"*. Under §138 AO, freelancers report directly to the Finanzamt.

**4. Optional: certified translations (beglaubigte Übersetzungen)**
German–Russian private clients often need translations of birth certificates, diplomas and similar documents that authorities will accept. For that you need a court **Ermächtigung** (authorization). Without it you can still do ordinary translations.
- **Who grants it:** Landgericht Berlin II, Dolmetscherabteilung, Littenstraße 12–17.
- **Requirements:** a translator examination (German state or university exam, or a foreign one recognised as equivalent), a police certificate of good conduct (Führungszeugnis) and your residence or business in Berlin.
- **Cost and time:** €120–160 in total, about 3 months' processing, valid for 5 years. You apply online only.

## Things that follow from this
- **Annual income tax return:** this becomes **mandatory**, because your income without tax withheld at source will be over €410 (§46(2) No. 1 EStG). You file the Anlage S (freelance income) and the EÜR (a simple income-minus-expenses statement). The €410 applies to profit, not turnover.
- **Tax prepayments:** if the tax expected on your side income reaches €400 a year, the Finanzamt sets quarterly advance payments.
- **Your employer:** check your employment contract for a clause requiring you to report or get approval for side jobs (Nebentätigkeit). I didn't check an official source on this, because it depends on your contract.
- **Not checked:** health insurance and pension effects. They're usually minor for a side activity next to a full-time job, but I didn't verify them.

## Two questions that would change the details
1. Do you already have any other self-employed activity, now or in the past (for VAT history)?
2. Do you want to offer certified translations? If yes, do you have a recognised translator examination?

If you'd like, I can next prepare a field-by-field worksheet for the ELSTER Fragebogen, including the activity description and income estimates.

This is AI-assisted self-help, not tax or legal advice, and it can be wrong. Nothing has been registered or saved.

## Official sources (checked 25 Nov 2026)
- [§18 EStG – freie Berufe, incl. Übersetzer](https://www.gesetze-im-internet.de/estg/__18.html)
- [§138 AO – notifying the Finanzamt](https://www.gesetze-im-internet.de/ao_1977/__138.html)
- [§19 UStG – Kleinunternehmer](https://www.gesetze-im-internet.de/ustg_1980/__19.html)
- [§46 EStG – when employees must file a return](https://www.gesetze-im-internet.de/estg/__46.html)
- [§14 GewO – Gewerbeanzeige (for comparison)](https://www.gesetze-im-internet.de/gewo/__14.html)
- [ELSTER – Unternehmensgründung](https://www.elster.de/elsterweb/infoseite/unternehmensgruendung) · [Mein ELSTER](https://www.elster.de/eportal/start)
- [Service Berlin – steuerliche Anmeldung (Gründungen)](https://service.berlin.de/dienstleistung/325409/)
- [Berlin Senatsverwaltung für Finanzen – FAQ Start-up-Unternehmen](https://www.berlin.de/sen/finanzen/steuern/informationen-fuer-steuerzahler-/faq-steuern/artikel.558266.php)
- [Berlin – Zuständigkeiten der Finanzämter](https://www.berlin.de/sen/finanzen/steuern/finanzaemter/zustaendigkeit-finden/artikel.1065064.php) · [BZSt Finanzamtsuche](https://www.bzst.de/DE/Service/Behoerdenwegweiser/Finanzamtsuche/GemFa/finanzamtsuche_node.html)
- [Service Berlin – Ermächtigung von Übersetzern](https://service.berlin.de/dienstleistung/328825/)

---

## Hamburg · Kleinunternehmerregelung

**Question** (skill `de-business-tax`):

> Use de-business-tax. I'm a freelance web designer in Hamburg and started in January 2026. My revenue this year will be about 22,000 euros, all from small German businesses. Can I use the Kleinunternehmerregelung, and what happens if I go over the limit next year? Please cite official sources.

**Run:** 111 s · tools: Skill ×1, Read ×3, Grep ×2, Agent ×3, WebFetch ×8

**Pages fetched:**

- https://www.gesetze-im-internet.de/ustg_1980/__19.html
- https://finanzamt.hessen.de/steuern/umsatzsteuer-kleinunternehmer
- https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-03-18-sonderregelung-kleinunternehmer.pdf
- https://www.hamburg.de/politik-und-verwaltung/behoerden/finanzbehoerde
- https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-03-18-sonderregelung-kleinunternehmer.html

**Answer:**

**Yes, you can most likely use the Kleinunternehmerregelung for 2026.** You expect about €22,000, and the limit for your first year is €25,000. In 2027 you can stay under the scheme even if you go over €25,000. In that case regular VAT starts on **1 January 2028**. Only going over **€100,000** in 2027 would end it during 2027.

This is AI-assisted self-help, not professional tax advice. VAT is federal law, so Hamburg applies the same rules as every other state.

## 2026: your first year

- **The limit is €25,000 of actual turnover in 2026.** You don't project it to a full year or make a forecast. Hessen's tax administration says: *"Es ist keine Prognoseentscheidung oder Hochrechnung des Umsatzes auf das gesamte Kalenderjahr mehr erforderlich."* ([Finanzverwaltung Hessen: Kleinunternehmer – Neuregelung ab 2025](https://finanzamt.hessen.de/steuern/umsatzsteuer-kleinunternehmer))
- **Turnover means net payments actually received.** § 19(2) UStG counts turnover *"nach vereinnahmten Entgelten"*, so what counts is money received in 2026, not invoices you've issued. ([§ 19 UStG](https://www.gesetze-im-internet.de/ustg_1980/__19.html))
- **You have about €3,000 of room left for December.** If a payment takes you over €25,000, that payment is already taxed normally: *"ist bereits der Umsatz, der die Grenze überschreitet, der Regelbesteuerung zu unterwerfen."* Payments received before that stay VAT-free. (Hessen page)
- **Your invoices must not show VAT** and must refer to the § 19 exemption, e.g. *"Gemäß § 19 Abs. 1 UStG wird keine Umsatzsteuer berechnet."* The Hessen page bases this on § 34a UStDV, which allows a simplified invoice.
- **You don't file VAT returns.** § 19(1) sentence 2 UStG switches off the § 18 filing duties (monthly or quarterly VAT returns and the annual VAT return). In exchange, you can't reclaim the VAT on your own purchases.

## 2027 and later

The test from 2027 on is: turnover in the **previous year ≤ €25,000** and turnover in the **current year ≤ €100,000** (§ 19(1) sentence 1 UStG).

| Your 2027 turnover | VAT treatment in 2027 | VAT treatment in 2028 |
|---|---|---|
| Up to €25,000 | Kleinunternehmer | Kleinunternehmer (if 2028 stays ≤ €100,000) |
| Over €25,000, up to €100,000 | **Kleinunternehmer for all of 2027** | **Regular VAT from 1 Jan 2028** |
| Over €100,000 | Regular VAT from the payment that crosses €100,000 | Regular VAT |

The Hessen page has a matching example: €18,000 in 2025 and €60,000 in 2026 means regular VAT from 1 January 2027.

Once regular VAT applies, you add 19% VAT to your invoices, file VAT returns in ELSTER and can reclaim VAT on business purchases. Your clients are all German businesses, so most of them can reclaim the VAT you charge. That makes the switch mostly extra paperwork for you, not a higher price for them.

**Opting out on purpose:** you can give up the scheme voluntarily, for example if you have large equipment costs. That choice binds you for at least five calendar years. For 2026 you could still make it until the end of February 2028 (§ 19(3) UStG).

## What could change this

- **Other self-employed work.** All your activities count together. The €25,000 first-year rule only applies if 2026 is your first year of any self-employed activity.
- **What you chose at registration.** If you picked regular VAT in the *Fragebogen zur steuerlichen Erfassung* (the tax registration form) or have charged VAT on invoices, that needs checking. It could count as opting out.
- **Income tax is separate.** The scheme only affects VAT. Your profit is still subject to income tax.

## Sources I couldn't check today

The Federal Ministry of Finance's detailed guidance letter of 18 March 2025 ([BMF-Schreiben](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-03-18-sonderregelung-kleinunternehmer.pdf?__blob=publicationFile&v=4)) returned server errors on every try. Everything above comes from the law itself and the Hessen tax administration's official page, both read today (25 Nov 2026). I couldn't find a separate Hamburg page on this.

Nothing was saved, because you don't have a workspace set up.

**Three questions to confirm the answer for your case:**
1. Which VAT option did you choose in the registration form, and have your invoices so far been without VAT?
2. Did you have any other self-employed work before 2026, or do you have any alongside web design?
3. Is the €22,000 money actually received in 2026, and do you expect more payments to arrive before 31 December?

---

## Munich · lowering tax prepayments

**Question** (skill `de-business-tax`):

> Use de-business-tax. I'm a self-employed photographer in Munich. My 2025 income tax assessment from the Finanzamt München sets quarterly prepayments of 1,450 euros, the next one due on 10 December 2026. My profit this year dropped from about 38,000 to roughly 21,000 euros because I lost a big client. What does this mean, and can I ask them to lower the prepayments? If yes, draft a short German letter for me.

**Run:** 109 s · tools: Skill ×1, Bash ×4, Read ×5, Grep ×1, Agent ×2, WebFetch ×4

**Pages fetched:**

- https://www.gesetze-im-internet.de/estg/__37.html
- https://www.elster.de/elsterweb/helpGlobal
- https://www.elster.de/eportal/formulare-leistungen/alleformulare/eingvorauszlg
- https://www.gesetze-im-internet.de/estg/__32a.html

**Answer:**

## What this means

The Finanzamt set your prepayments from your **2025** profit of about €38,000: €1,450 a quarter, or €5,800 a year. Prepayments are due on 10 March, 10 June, 10 September and 10 December. They're meant to cover the tax you'll **probably owe for the current year** (EStG §37(1), (3)). If your 2026 profit is only about €21,000, you're paying in advance for income you don't have.

**Yes, you can ask for a reduction.** Under EStG §37(3) sentence 3, the Finanzamt can adjust prepayments to the tax expected for the current year. It can do this until the end of the 15th month after the year, so for 2026 that's March 2028. The law sets no minimum amount for a reduction.

## Rough check: how much tax might you owe for 2026?

I used the 2026 tariff from EStG §32a and made a deliberately pessimistic assumption: you're single, have no other income, and get **no deductions at all**. Even so, taxable income of €21,000 gives about **€1,819** income tax.

- If you paid the March, June and September instalments, you've already paid **€4,350**.
- In this scenario, the December instalment should be **€0**, and you'd probably get some money back.
- Health insurance, pension contributions and other deductions would lower the tax further.
- Church tax would be added on top if you're a member. The solidarity surcharge probably doesn't apply at this level, but I didn't check its threshold.

I calculated this with exact arithmetic two separate ways. I also checked that the formulas join up correctly where one tariff band meets the next (at €17,799). I haven't compared it with the official BMF calculator, so treat it as **an estimate, not checked against an official tool**. If you're married and assessed jointly, or have other income, the figure can change a lot.

## Timing: the next payment is due in 15 days

- **Send the request now.** If the Finanzamt hasn't decided by 10 December, the current notice still applies and you owe €1,450. Paying late can bring late-payment surcharges.
- **If the Finanzamt collects by direct debit, it will take the €1,450 automatically** unless it has changed the notice by then.
- If you pay and the reduction comes through later, the extra is refunded, at the latest with your 2026 tax assessment.
- **Option to decide yourself:** you can add a sentence to the letter asking the Finanzamt to defer the December instalment until it decides: *„Bis zur Entscheidung über diesen Antrag bitte ich, die Vorauszahlung zum 10.12.2026 zu stunden."* A deferral (Stundung) is a separate formal request, so I left it out of the draft.
- **How to send it:** ELSTER has a dedicated form, **„Antrag auf Anpassung von Vorauszahlungen"**. I confirmed the form exists but couldn't see its fields, so I can't say exactly where each part goes. The letter below can be your explanation in that form, or you can send it as a normal letter.
- **Trade tax:** if you're registered as a trade business rather than self-employed in a profession, trade-tax prepayments are set separately by the City of Munich. They need their own request. You only need to do anything here if you get those notices.

## Draft letter

> **Antrag auf Herabsetzung der Einkommensteuer-Vorauszahlungen 2026 und Folgejahre**
>
> **ENTWURF — nicht versandt**
>
> [Vorname Nachname]
> [Straße Nr., PLZ München]
>
> Finanzamt München
> [Anschrift laut Bescheid]
>
> [Datum]
> Steuernummer: [laut Bescheid]
>
> Sehr geehrte Damen und Herren,
>
> mit dem Einkommensteuerbescheid für 2025 vom [Datum des Bescheids] wurden Einkommensteuer-Vorauszahlungen von 1.450 € vierteljährlich festgesetzt. Grundlage war mein Gewinn aus meiner selbständigen Tätigkeit als Fotograf von rund 38.000 € im Jahr 2025.
>
> Im Jahr 2026 ist mein Gewinn deutlich gesunken, da ein wesentlicher Auftraggeber weggefallen ist. Nach meinen bisherigen Aufzeichnungen erwarte ich für 2026 einen Gewinn von rund 21.000 €. Für 2027 rechne ich derzeit mit einem Gewinn in ähnlicher Höhe.
>
> Ich beantrage daher gemäß § 37 Abs. 3 EStG,
>
> 1. die Einkommensteuer-Vorauszahlungen für 2026 an die voraussichtliche Einkommensteuer anzupassen und die Vorauszahlung zum 10. Dezember 2026 auf 0 € herabzusetzen. Einen sich ergebenden Überschuss der bereits geleisteten Vorauszahlungen bitte ich zu erstatten;
> 2. die Vorauszahlungen ab 2027 auf Grundlage eines voraussichtlichen Gewinns von rund 21.000 € neu festzusetzen.
>
> [Falls beigefügt: Eine Übersicht meiner Einnahmen und Ausgaben für Januar bis [Monat] 2026 liegt bei.]
>
> Mit freundlichen Grüßen
>
> [Name]
>
> Anlagen: [nur falls tatsächlich beigefügt: Einnahmen-/Ausgabenübersicht 2026]

The Finanzamt often asks for evidence of the lower profit. A simple income and expense summary for 2026 so far usually helps.

## Before you send

1. **Are you married and assessed jointly, or do you have other income** (employment, rent, investments)? Either could change whether asking for €0 is right.
2. **Have the March, June and September instalments actually been paid?** The €0 request assumes yes.
3. **Is the 2025 profit on the notice really about €38,000?** And is the €21,000 a solid figure, or partly a guess about December?

This is AI-assisted self-help, not professional tax advice. Only the letter above exists as a draft; I haven't saved any files or sent anything. If you answer those three questions, I can fill in the placeholders and save the letter and a short calculation note to a folder you choose.

---
