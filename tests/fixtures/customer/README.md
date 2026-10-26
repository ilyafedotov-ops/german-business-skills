# Customer correction fixtures

Synthetic header-only XML and a bank-style CSV for local evidence-flow tests.
The invoice/credit-note amounts are fixed fixture data, not a calculation or tax
choice. These files are not schema-valid/profile-certified e-invoices; required
lines and business particulars are intentionally outside this inspection subset.
No document was issued, sent, paid or refunded in an external system.

The scenario preserves an invoice, a partial receipt and a later CreditNote
referencing the invoice. The test explicitly records a reviewed document link;
XML extraction itself must not create one. Receipt of a CreditNote does not
resolve payment, dispute, refund or accounting questions. Both EN/RU runs retain
an open task and external accounting authority without local shadow entries.
