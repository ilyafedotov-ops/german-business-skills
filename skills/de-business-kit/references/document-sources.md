# Document preparation: sources and inspection boundaries

Checked: **2026-10-25**. Shared English reference for the local document catalog, extraction/proposal review, overview and optional personal records archive. The XML subset below supports preparation from standalone UBL Invoice and CII XML. It is not an invoice schema, EN 16931 validator, XRechnung/ZUGFeRD certification, tax determination or proof of a complete archive. Recheck applicable sources and actual format/profile before expanding support.

## Preserve the received evidence

The [BMF E-Rechnung FAQ](https://www.bundesfinanzministerium.de/Content/DE/FAQ/e-rechnung.html), dated 23 March 2026, distinguishes ordinary PDF from structured E-Rechnung (question 2). For hybrid invoices, the structured data prevail over a conflicting visual part (12a). At least the structured part must remain intact in its original form (13). A reference to an unstructured attachment does not replace required structured invoice particulars (7a).

Product consequence: preserve the received file unchanged. Store extraction, normalized values and previews as linked derivatives with source hash and field locations. Preserve relevant attachments. A PDF with embedded XML requires separate, assessed PDF tooling; a standalone XML inspector cannot discover, extract or validate that embedded content. Do not conclude that a PDF lacks XML merely because no extraction tool ran. Never replace a received hybrid PDF with reconstructed XML or an OCR rendering.

The [BMF letter of 15 October 2025](https://www.bundesfinanzministerium.de/Content/DE/Downloads/BMF_Schreiben/Steuerarten/Umsatzsteuer/Umsatzsteuer-Anwendungserlass/2025-10-15-einfuehrung-obligatorische-e-rechnung.pdf?__blob=publicationFile&v=5), Rn. 35a, distinguishes technical validation from completeness/correctness review; substantive errors can remain after validation. Rn. 60 addresses preservation and the limited VAT point about storage outside a GoBD system. Neither a successful XML parse nor a hash check establishes compliance.

Direct BMF fetches intermittently returned HTTP 503 during this check; the official indexed FAQ and letter supplied the passages above. This is a dated source check, not evidence about an individual invoice.

## Recognize exact namespace and root combinations

Prefixes below are explanatory aliases; XML may use different prefixes or a default namespace. Match expanded namespace URI plus local name, not the spelling of the prefix or a recursive local-name search.

| Alias | Exact namespace URI |
| --- | --- |
| `ubl` | `urn:oasis:names:specification:ubl:schema:xsd:Invoice-2` |
| `cac` | `urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2` |
| `cbc` | `urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2` |
| `rsm` | `urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100` |
| `ram` | `urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100` |
| `udt` | `urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100` |

Recognized roots are `{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice` and `{urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100}CrossIndustryInvoice`. A matching root identifies a candidate syntax, not its validity or an accepted German profile. CII document type still needs inspection; the same root does not mean every document is an ordinary invoice. UBL CreditNote has a different root/namespace and needs separate support.

Primary evidence:

- [OASIS UBL 2.1 Invoice schema](https://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd) and [official example](https://docs.oasis-open.org/ubl/os-UBL-2.1/xml/UBL-Invoice-2.1-Example.xml), both fetched directly as XML for this check.
- [KoSIT CII example](https://github.com/itplr-kosit/xrechnung-testsuite/blob/1ce1dafffd035e5ce59a7ab0d3bf44ac14af16c9/src/test/business-cases/extension/04.05a-INVOICE_uncefact.xml), fetched directly as XML, and [KoSIT CII semantic mapping](https://github.com/itplr-kosit/xrechnung-visualization/blob/811903564db35438abdb3e24fb6cfd37b92dbf78/src/xsl/cii-xr.xsl). The example includes extension content: recognizing the header does not establish support for its full document.
- [KoSIT UBL semantic mapping](https://github.com/itplr-kosit/xrechnung-visualization/blob/811903564db35438abdb3e24fb6cfd37b92dbf78/src/xsl/ubl-invoice-xr.xsl).

The pinned KoSIT files document the inspected snapshot, not a claim that these are the newest normative format versions.

## Small field subset and its meaning

UBL paths below are relative to `ubl:Invoice`. They identify extraction locations, not mandatory-field completeness rules.

| Candidate field | UBL path |
| --- | --- |
| Invoice number | `cbc:ID` |
| Issue date | `cbc:IssueDate` |
| Document type | `cbc:InvoiceTypeCode` |
| Invoice currency | `cbc:DocumentCurrencyCode` |
| Seller legal name | `cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName` |
| Buyer legal name | `cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName` |
| Total excluding VAT | `cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount` |
| VAT total in invoice currency | `cac:TaxTotal/cbc:TaxAmount` with matching `currencyID` |
| Total including VAT | `cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount` |
| Amount due | `cac:LegalMonetaryTotal/cbc:PayableAmount` |

`cac:PartyName/cbc:Name` under the relevant party is its trading name; keep that label if using it as a display fallback. It does not establish the legal-name field. More than one candidate at a single-value extraction path requires review rather than silently selecting the first. Tax currency and invoice currency can differ; preserve both instead of adding their tax amounts together.

CII paths are relative to `rsm:CrossIndustryInvoice`. Define `T = rsm:SupplyChainTradeTransaction`, `A = T/ram:ApplicableHeaderTradeAgreement`, `S = T/ram:ApplicableHeaderTradeSettlement`, and `M = S/ram:SpecifiedTradeSettlementHeaderMonetarySummation`.

| Candidate field | CII path |
| --- | --- |
| Invoice number | `rsm:ExchangedDocument/ram:ID` |
| Issue date | `rsm:ExchangedDocument/ram:IssueDateTime/udt:DateTimeString[@format='102']` |
| Document type | `rsm:ExchangedDocument/ram:TypeCode` |
| Seller / buyer name | `A/ram:SellerTradeParty/ram:Name` / `A/ram:BuyerTradeParty/ram:Name` |
| Invoice currency | `S/ram:InvoiceCurrencyCode` |
| Total excluding VAT | `M/ram:TaxBasisTotalAmount` |
| VAT total in invoice currency | `M/ram:TaxTotalAmount[@currencyID=<invoice currency>]` |
| Total including VAT | `M/ram:GrandTotalAmount` |
| Amount due | `M/ram:DuePayableAmount` |

CII format `102` uses `YYYYMMDD`; the inspected UBL issue date uses `YYYY-MM-DD`. Validate calendar dates before normalization; unsupported date formats remain unresolved. The CII mapping selects invoice-currency and accounting-currency tax totals separately.

Practical example: a synthetic invoice can have net `100.00`, VAT `19.00`, gross `119.00`, an advance payment `50.00`, and amount due `69.00`. Store gross and amount due separately. The official OASIS example also has different `TaxInclusiveAmount` and `PayableAmount`. Do not force those fields to agree or infer an observed payment from a stated advance. Preserve decimal text and currency; inspect rounding, allowances, charges and rate breakdowns before broader arithmetic conclusions.

## Structural inspection contract

A bounded standard-library inspector may report: readable XML, recognized root, exact paths found, raw/normalized candidate values and unresolved conflicts. Report schema and business-rule validation as **not performed** unless a separate real validator ran. [KoSIT FAQ](https://xeinkauf.de/xrechnung/faq) explains that XRechnung combines syntax XSDs with semantic Schematron rules; validation outcomes also depend on the configuration and European artifacts.

Recommended controls for this local preparation tool:

- Reject DTD/entity declarations before expansion; apply encoding-aware handling or explicitly limit accepted encodings. Apply input size, depth and text limits. [Python XML security guidance](https://docs.python.org/3/library/xml.html#xml-security) warns about malicious XML and runtime Expat differences; standard-library availability alone is not a security guarantee.
- Do not fetch `schemaLocation`, external references, attachment URLs or XInclude targets, or execute scripts, macros or instructions found in source content. Embedded attachments remain untrusted evidence.
- Preserve null for missing/unrecognized fields. Retain raw text, source hash, namespaced path, parser/version and reviewer correction provenance. Never invent a VAT rate, date, supplier, currency or balancing amount.
- Treat extraction approval and proposed accounting/tax treatment as separate decisions. A generated overview is a navigation aid; it cannot replace original evidence or a complete archive manifest.
- Verify archive file hashes and links locally, include schema/field definitions and unresolved items, and state the covered documents/accounts/periods. A successful bundle verification proves the packaged bytes and manifest agree; it does not prove source completeness, accounting completeness, accounting-system import or GoBD conformity.

Examples for acceptance: alternate XML prefixes resolve to the same paths; an unnamespaced lookalike is unsupported; nested line-item totals do not replace header totals; duplicate header candidates trigger review; a nonmatching tax currency is not combined with the invoice-currency total; PDF inspection requests a separate extraction step; a reviewed correction leaves the original bytes and earlier extraction identifiable.
