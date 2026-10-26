# Gewerbe / Freiberufler clarification

Use this worksheet when opening or changing an activity, choosing Anlage S/G, considering Gewerbesteuer, or when the user says “freelancer” without a supported German classification. Read [formation](formation.md) for registration steps and [legal boundaries](legal-boundaries.md) for regulated services.

1. Describe each actual activity and deliverable, qualifications, personal professional involvement, customers, contracts and delivery method. A job title, platform category or marketing brand is not a determination under EStG §§15/18.
2. Preserve activity IDs, existing registrations, Finanzamt correspondence and effective dates. Record whose statement or decision supports each classification; do not treat the user's proposed label as authority confirmation.
3. For mixed activities, record what can be separated operationally and economically and what is inseparably connected. Do not automatically import partnership `Abfärbung` rules into an individual's activity. Keep allocation and classification questions explicit for qualified review where unresolved.
4. Keep **legal form**, **income/activity classification**, **VAT regime**, and **profit determination** separate. Freiberufler can operate as a natural-person sole trader; using the ELSTER Einzelunternehmen questionnaire does not itself mean Gewerbe. A second activity does not restart person-wide VAT history.
5. Prepare the consequences conditionally: municipal Gewerbeanmeldung where applicable, tax registration, possible chamber/professional obligations, income inputs for Anlage S/G, and conditional Gewerbesteuer. Check separate licensing requirements. Municipal Gewerbeanmeldung is not replaced by an ELSTER draft.

`workflows.py template --kind classification` creates the factual worksheet contract; [preparation](preparation.md) explains evidence and report generation. This command never changes profile classification or VAT status. Save a supported final decision separately through the existing decision register, including reviewer and evidence.

## Sources and periods

Checked **2026-10-25**; verify the legal version applicable to the activity/tax year before use. The worksheet does not encode a profession classifier or binding decision.

- [EStG §18](https://www.gesetze-im-internet.de/estg/__18.html) and [EStG, including §15](https://www.gesetze-im-internet.de/estg/BJNR010050934.html): listed/similar professions and commercial income; a software consultant's label alone is insufficient.
- [Official EStH 2024 §15 guidance](https://esth.bundesfinanzministerium.de/esth/2024/A-Einkommensteuergesetz/II-Einkommen-2-24b/8-Die-einzelnen-Einkunftsarten-13-24b/b-Gewerbebetrieb-15-17/Paragraf-15/inhalt.html): historical reference for separable/mixed activity analysis; explicitly a **2024 edition**, not proof of an unchanged later-year outcome.
- [UStG §2](https://www.gesetze-im-internet.de/ustg_1980/__2.html): entrepreneur-wide enterprise; a small second Gewerbe does not get independent VAT history automatically.
- [GewO §14](https://www.gesetze-im-internet.de/gewo/__14.html) and [ELSTER startup guidance](https://www.elster.de/elsterweb/infoseite/unternehmensgruendung): separate municipal and tax procedures; the Einzelunternehmen form covers commercial and freelance activity.
