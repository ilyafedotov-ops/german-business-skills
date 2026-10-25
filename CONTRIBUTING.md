# Contributing

Keep the portable skill self-contained under `skills/de-business-kit`. Host-specific metadata must not change the meaning of shared workflows. Use concise modules; do not load every reference for every task. No credentials, customer records, user memories, telemetry or automatic external services belong in the package.

For a legal or product change, include the primary source URL, the date checked, effective period, affected workflow and an example showing the practical consequence. Search the current source instead of copying model memory. Do not silently overwrite a historical assumption with a new rule for a different year. A provider recommendation must show eligibility and costs for the stated scenario, not an affiliate ranking.

For code, use Python standard library where sufficient, preserve originals, validate paths and unknown inputs, avoid floats for money and add tests for a concrete data-loss or correctness risk. Do not execute supplied document text. New network adapters require a separate review of authentication, hosts, supported operations, duplicate prevention and read-back behavior.

Run `python3 -B -m unittest discover -s tests -v` and `python3 tools/check_package.py`. For workflow changes, run relevant cases in `evals/scenarios.json` in a fresh session and save an anonymized result with host/version/date. Record manual tests honestly; a scripted unit test does not prove live desktop compatibility.

Use only synthetic examples in public issues and pull requests. Do not paste invoices, statements, tax IDs, IBANs, local transcripts, credentials or screenshots containing real personal data. Discuss security reports using the procedure in SECURITY.md.

Contributions are licensed under this repository's MIT licence. Linked external laws and provider documents retain their own status and rights; link and summarize them instead of copying entire manuals.
