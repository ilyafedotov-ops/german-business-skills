# Correction XML: syntax sources and inspection limits

Checked: **2026-10-26**. Shared agent reference for bounded standalone XML
inspection, supplementing [document sources](document-sources.md). These are
extraction locations, not tax calculations, correction approval or proof that a
document conforms to EN 16931, XRechnung, ZUGFeRD or Peppol. The dated schema and
binding checks below do not establish support for every UBL 2.x release/profile.

## UBL CreditNote header subset

Match the expanded root
`{urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2}CreditNote`.
Use the existing `cac` and `cbc` namespaces from document sources; prefixes are
aliases, never identification criteria. Paths below are relative to that root.

| Candidate | Exact path |
| --- | --- |
| Document number | `cbc:ID` |
| Issue date | `cbc:IssueDate` |
| Document type | `cbc:CreditNoteTypeCode` |
| Currency | `cbc:DocumentCurrencyCode` |
| Seller / buyer legal name | `cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName` / `cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName` |
| Total excluding VAT | `cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount` |
| VAT total in document currency | `cac:TaxTotal/cbc:TaxAmount` with matching `currencyID` |
| Total including VAT | `cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount` |
| Amount due | `cac:LegalMonetaryTotal/cbc:PayableAmount` |
| Payment due date | `cac:PaymentMeans/cbc:PaymentDueDate` |

The [OASIS UBL 2.1 CreditNote schema](https://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-CreditNote-2.1.xsd)
defines this root and header structure; the [Peppol CreditNote binding](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-creditnote/)
and [document totals binding](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-creditnote/cac-LegalMonetaryTotal/)
identify the business fields. Peppol requires `CreditNoteTypeCode`; the generic
UBL 2.1 XSD allows it to be absent. Preserve the actual code, including an unknown
code; do not substitute `381` because the root is CreditNote.

CreditNote has **no root `cbc:DueDate`** in the inspected UBL 2.1 schema. The
[Invoice schema](https://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd)
has that field. The [CreditNote payment date binding](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-creditnote/cac-PaymentMeans/cbc-PaymentDueDate/)
instead uses the path above; `PaymentMeans` can repeat. Conflicting candidates
need review. Do not copy Invoice's root due-date lookup into CreditNote.

## Preceding invoice references

For both UBL Invoice and CreditNote, inspect each root-level
`cac:BillingReference/cac:InvoiceDocumentReference`; extract `cbc:ID` and optional
`cbc:IssueDate` within that same reference. Preserve their association and all
references instead of flattening IDs and dates into unrelated lists. Peppol's
[Invoice binding](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-BillingReference/cac-InvoiceDocumentReference/)
and [CreditNote binding](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-creditnote/cac-BillingReference/cac-InvoiceDocumentReference/)
require one ID per reference and allow zero or one issue date. The
[BillingReference group](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-creditnote/cac-BillingReference/)
can occur zero or more times. The date uses `YYYY-MM-DD`; the binding calls for it
when the preceding identifier is ambiguous. A missing optional date must remain
missing, never be borrowed from the current document.

For CII D16B, retain the existing `CrossIndustryInvoice` root and document type
path `rsm:ExchangedDocument/ram:TypeCode`. Let
`S = rsm:SupplyChainTradeTransaction/ram:ApplicableHeaderTradeSettlement`.
Preceding references use `S/ram:InvoiceReferencedDocument/ram:IssuerAssignedID`
and the optional date at
`S/ram:InvoiceReferencedDocument/ram:FormattedIssueDateTime/qdt:DateTimeString[@format='102']`.
Here `qdt` is **`urn:un:unece:uncefact:data:standard:QualifiedDataType:100`**,
distinct from `udt` used for the current document's issue date. Format `102`
means `YYYYMMDD`; validate the calendar date before normalization. These paths
are confirmed by [KoSIT's CII mapping](https://github.com/itplr-kosit/xrechnung-visualization/blob/811903564db35438abdb3e24fb6cfd37b92dbf78/src/xsl/cii-xr.xsl).

The [European Commission's inspected D16B schema snapshot](https://github.com/ConnectingEurope/eInvoicing-EN16931/blob/6e35e0ab8b09eb183f7d84b282e24ef95f9f5715/cii/schema/D16B%20SCRDM%20%28Subset%29/uncoupled%20clm/CII/uncefact/data/standard/CrossIndustryInvoice_ReusableAggregateBusinessInformationEntity_100pD16B.xsd)
allows zero or one header `InvoiceReferencedDocument` and zero or one
`FormattedIssueDateTime` within it. Its generic reference ID is optional in XSD,
while [EN 16931 CII rule BR-55](https://github.com/ConnectingEurope/eInvoicing-EN16931/blob/6e35e0ab8b09eb183f7d84b282e24ef95f9f5715/cii/schematron/preprocessed/EN16931-CII-validation-preprocessed.sch)
requires a nonblank ID for a preceding reference. Do not transfer UBL's repeated
group cardinality to a claim about this D16B schema. An inspector can preserve
unexpected repeated CII references as evidence and flag the multiplicity; that
does not validate them. Missing/duplicate IDs and unsupported date encodings
remain unresolved.

## Signs and acceptance boundary

### Invoice-stated prepayments and rounding

Additional check **2026-10-27**, for UBL 2.1 / Peppol BIS Billing 3.0 May 2026
and the pinned CII D16B / EN16931 1.3.17 artifacts above:

| Extracted field | UBL Invoice / CreditNote | CII, relative to `S/ram:SpecifiedTradeSettlementHeaderMonetarySummation` |
| --- | --- | --- |
| `prepaid_amount` | `cac:LegalMonetaryTotal/cbc:PrepaidAmount` | `ram:TotalPrepaidAmount` |
| `rounding_amount` | `cac:LegalMonetaryTotal/cbc:PayableRoundingAmount` | `ram:RoundingAmount` |

The [UBL prepaid binding](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-LegalMonetaryTotal/cbc-PrepaidAmount/),
[rounding binding](https://docs.peppol.eu/poacc/billing/3.0/syntax/ubl-invoice/cac-LegalMonetaryTotal/cbc-PayableRoundingAmount/)
and CreditNote totals binding above make these optional, at most once. The pinned
CII rules CII-SR-481/484 also limit each to one; the generic D16B XSD allows repeated
values. This inspector leaves duplicates unresolved and performs no profile validation.

[BR-CO-16](https://docs.peppol.eu/poacc/billing/3.0/rules/ubl-tc434/BR-CO-16/)
compares due with gross minus paid plus rounding, with separate branches when
optional fields are absent. Absence contributes zero for that formula only;
extraction retains null/`optional_missing`. Explicit zero, supplied negative signs
and decimal text remain unchanged. Empty, malformed or currency-conflicting
fields remain unresolved. For example, `119.00 - 20.00 + (-0.01) = 98.99` is a
document-total comparison, not proof of a current receivable or bank settlement.
The utility does not run this profile rule or validate its two-decimal limits.
See [customer payment continuation](operations.md#save-and-resume-a-customer-payment-reply)
before comparing these amounts with later receipts or corrections.

### Preserve economic meaning

[Peppol BIS sections 5.6 and 11.4](https://docs.peppol.eu/poacc/billing/3.0/bis/)
describe credit notes and negative invoices separately and permit negative grand
totals, including in credit notes. Preserve each source amount's sign, decimal
text and currency. Never multiply a CreditNote total by minus one, apply absolute
value, or infer a cancellation, replacement, refund, cash movement or posted
accounting effect from root/type/sign/reference alone. For example, a synthetic
CreditNote gross `119.00` stays `119.00`; a source gross `-119.00` stays negative.
Type and amount are separate evidence for review.

This subset covers header identity, parties, selected totals, due dates and
preceding-reference candidates only. Preserve original bytes and namespaced
field provenance. Line calculations, VAT treatment, attachment extraction,
reference matching to an actual workspace document, XSD/Schematron validation
and profile/codelist conformance require separate work. Report validation as
**not performed** unless an actual validator ran with identified artifacts.
