"""Synthetic preparation journeys; no accounts, tax filings or model calls."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts"
sys.path.insert(0, str(SCRIPTS))
import workspace
import workflows
import payments


class WorkspaceFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "private"
        workspace.init_workspace(self.root, 2026, "en")
        self.evidence = self.root / "08_correspondence/synthetic.txt"
        self.evidence.write_text("Synthetic evidence only", encoding="utf-8")

    def write(self, name, value):
        path = self.root / "00_admin/inbox" / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def request(self, kind):
        value = workflows.template(kind)
        value.update(record_id="synthetic-1", period="2026-10", activity_ids=["consulting"],
                     evidence=[{"id": "proof", "path": "08_correspondence/synthetic.txt"}])
        return value

    def prepare(self, kind, value):
        result = workflows.prepare(self.root, kind, self.write("request.json", value))
        return json.loads((self.root / result["path"]).read_text(encoding="utf-8"))


class PreparationTests(WorkspaceFixture):
    def test_foreign_saas_small_business_keeps_reverse_charge_open(self):
        value = self.request("international")
        value["facts"].update(direction="purchase", supply="service", counterparty_region="non_eu",
                              customer_type="business", own_vat_regime="kleinunternehmer")
        report = self.prepare("international", value)
        self.assertIn("reverse_charge_review", report["routes"])
        self.assertEqual(report["status"], "needs_review")
        self.assertEqual(report["filing_status"], "not_submitted")
        self.assertIn("facts.service_description", report["missing"])

    def test_eu_business_sale_and_consumer_digital_sale_are_distinct_routes(self):
        value = self.request("international")
        value["facts"].update(direction="sale", supply="service", counterparty_region="eu",
                              customer_type="business", own_vat_regime="regular")
        report = self.prepare("international", value)
        self.assertIn("eu_b2b_place_and_zm_review", report["routes"])
        value["facts"].update(customer_type="consumer", service_description="automated download")
        report = self.prepare("international", value)
        self.assertIn("consumer_place_oss_review", report["routes"])
        self.assertNotIn("eu_b2b_place_and_zm_review", report["routes"])

    def test_goods_never_uses_generic_service_reverse_charge_route(self):
        value = self.request("international")
        value["facts"].update(direction="purchase", supply="goods", counterparty_region="non_eu")
        report = self.prepare("international", value)
        self.assertIn("goods_customs_review", report["routes"])
        self.assertNotIn("reverse_charge_review", report["routes"])

    def test_mixed_activity_preserves_person_wide_profile(self):
        before = (self.root / workspace.PROFILE).read_bytes()
        value = self.request("classification")
        value["facts"].update(activity_description="Teaching and selling books", mixed_activities=True)
        report = self.prepare("classification", value)
        self.assertIn("mixed_activity_review", report["routes"])
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), before)

    def test_form_requires_exact_observed_labels_and_evidence_for_reviewed_values(self):
        value = self.request("elster")
        value["facts"].update(form_id="ustva", form_version="2026", authority="Finanzamt (synthetic)",
                              eligibility_reason="Recipient tax review pending", portal_checked_on="2026-10-25")
        value["fields"] = [{"label": "Synthetic observed German label", "value": "19.00", "status": "reviewed",
                            "evidence_ids": [], "reviewer": "user", "note": "test"}]
        with self.assertRaises(workspace.WorkspaceError):
            self.prepare("elster", value)
        value["fields"][0]["evidence_ids"] = ["proof"]
        report = self.prepare("elster", value)
        self.assertEqual(report["input"]["fields"][0]["label"], "Synthetic observed German label")
        self.assertEqual(report["filing_status"], "not_submitted")

    def test_blank_form_and_unavailable_vat_verification_never_become_ready(self):
        value = self.request("elster")
        report = self.prepare("elster", value)
        self.assertIn("fields", report["missing"])
        value = self.request("international")
        value["facts"]["vat_id_check"] = "unavailable"
        report = self.prepare("international", value)
        self.assertIn("vat_id_evidence_review", report["routes"])

    def test_unknown_keys_and_filing_states_are_rejected_before_writes(self):
        for extra in ({"status": "submitted"}, {"schema_version": True}, {"activity_ids": "consulting"}):
            value = self.request("elster")
            value.update(extra)
            with self.assertRaises(workspace.WorkspaceError):
                self.prepare("elster", value)
        self.assertEqual(list((self.root / "07_exports").rglob("preparation-*.json")), [])

    def test_changed_evidence_is_detected_and_reports_are_versioned(self):
        value = self.request("classification")
        source = self.write("request.json", value)
        first = workflows.prepare(self.root, "classification", source)
        second = workflows.prepare(self.root, "classification", source)
        self.assertNotEqual(first["path"], second["path"])
        self.assertEqual(workflows.verify(self.root, first["path"])["status"], "intact")
        self.evidence.write_text("Changed synthetic evidence", encoding="utf-8")
        self.assertEqual(workflows.verify(self.root, first["path"])["status"], "changed")

    def test_historical_source_checks_must_match_record_period(self):
        value = self.request("international")
        value["period"] = "2024-11"
        value["source_checks"] = [{"url": "https://www.gesetze-im-internet.de/ustg_1980/__13b.html",
            "checked_on": "2026-10-25", "applicable_period": "2026-10", "conclusion": "Synthetic", "evidence_ids": ["proof"]}]
        with self.assertRaises(workspace.WorkspaceError):
            self.prepare("international", value)

    def test_complete_form_stays_reviewable_and_unsubmitted(self):
        value = self.request("elster")
        value["facts"] = {"form_id": "ustva", "form_version": "2026", "authority": "Synthetic Finanzamt",
            "eligibility_reason": "Synthetic reviewed scenario", "portal_checked_on": "2026-10-25",
            "account_capability": "Manual preparation only", "deadline_basis": "Synthetic evidence",
            "calculation_notes": "Synthetic base 100 EUR times 19% equals 19 EUR; illustrative only"}
        value["fields"] = [{"label": "Synthetic A & B", "value": "19.00", "status": "reviewed",
            "evidence_ids": ["proof"], "reviewer": "synthetic reviewer", "note": None}]
        value["source_checks"] = [{"url": "https://www.gesetze-im-internet.de/ustg_1980/__13b.html",
            "checked_on": "2026-10-25", "applicable_period": "2026-10", "conclusion": "Synthetic reviewed scenario",
            "evidence_ids": ["proof"]}]
        result = workflows.prepare(self.root, "elster", self.write("complete.json", value))
        report = json.loads((self.root / result["path"]).read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "ready_for_review")
        self.assertEqual(report["filing_status"], "not_submitted")
        self.assertIn("Synthetic A & B", (self.root / result["markdown_path"]).read_text(encoding="utf-8"))

    def test_outside_workspace_and_mutable_administrative_evidence_are_rejected(self):
        outside = self.root.parent / "outside.json"
        outside.write_text(json.dumps(self.request("classification")), encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workflows.prepare(self.root, "classification", outside)
        value = self.request("classification")
        value["evidence"][0]["path"] = workspace.PROFILE
        with self.assertRaises(workspace.WorkspaceError):
            self.prepare("classification", value)

    def test_cli_works_outside_repository_and_renders_russian(self):
        value = self.request("classification")
        source = self.write("request.json", value)
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "workflows.py"), "prepare", "--root", str(self.root),
            "--kind", "classification", "--input", str(source), "--language", "ru"], cwd=self.root,
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertIn("Подготовка", (self.root / report["markdown_path"]).read_text(encoding="utf-8"))


class PaymentTests(WorkspaceFixture):
    def config(self, events, bank=""):
        (self.root / "03_banking/events.csv").write_text(
            "event_id,booking_date,kind,amount,currency,related_id,transfer_id,bank_transaction_id\n" + events, encoding="utf-8")
        (self.root / "03_banking/bank.csv").write_text(
            "transaction_id,booking_date,amount,currency\n" + bank, encoding="utf-8")
        return {"schema_version": 1, "account_id": "synthetic-psp", "period": "2026-10",
            "balance_basis": "available statement balance", "coverage_confirmed": True,
            "provider_role": "processor", "sources": [{"format": "normalized", "path": "03_banking/events.csv"}],
            "bank_path": "03_banking/bank.csv", "balances": [{"currency": "EUR", "opening": "0", "closing": "0"}]}

    def payment_report(self, value):
        result = payments.prepare(self.root, self.write("payments.json", value))
        return json.loads((self.root / result["path"]).read_text(encoding="utf-8"))

    def test_gross_fee_partial_refund_payout_reconciles_without_duplicate_revenue(self):
        value = self.config("c1,2026-10-01,charge,100,EUR,,,\nf1,2026-10-01,fee,-3,EUR,c1,,\n"
            "r1,2026-10-02,refund,-20,EUR,c1,,\np1,2026-10-31,payout,-77,EUR,,,b1\n", "b1,2026-11-02,77,EUR\n")
        report = self.payment_report(value)
        self.assertEqual(report["status"], "arithmetic_matched")
        self.assertEqual(report["balances"][0]["calculated_closing"], "0")
        self.assertEqual(report["totals_by_kind"]["EUR"]["charge"], "100")
        self.assertEqual(report["payout_matches"][0]["bank_transaction_id"], "b1")
        self.assertEqual(report["tax_status"], "not_assessed")

    def test_missing_payout_link_cannot_match_by_amount_alone(self):
        value = self.config("c1,2026-10-01,charge,100,EUR,,,\np1,2026-10-02,payout,-100,EUR,,,\n", "b1,2026-10-03,100,EUR\n")
        self.assertEqual(self.payment_report(value)["status"], "needs_review")

    def test_fx_legs_remain_separate_and_do_not_create_tax_conversion(self):
        value = self.config("x1,2026-10-01,fx,-100,USD,,fx1,\nx2,2026-10-01,fx,90,EUR,,fx1,\n")
        value["balances"] = [{"currency": "USD", "opening": "100", "closing": "0"},
                              {"currency": "EUR", "opening": "0", "closing": "90"}]
        report = self.payment_report(value)
        self.assertEqual(report["status"], "needs_review")
        self.assertEqual(len(report["balances"]), 2)
        self.assertNotIn("tax_exchange_rate", report)

    def test_duplicates_unknown_types_wrong_sign_and_nonfinite_amounts_fail(self):
        for rows in ("a,2026-10-01,fee,-2,EUR,,,\na,2026-10-01,fee,-2,EUR,,,\n",
                     "a,2026-10-01,invented,2,EUR,,,\n", "a,2026-10-01,fee,2,EUR,,,\n",
                     "a,2026-10-01,charge,NaN,EUR,,,\n"):
            with self.subTest(rows=rows), self.assertRaises(workspace.WorkspaceError):
                self.payment_report(self.config(rows))

    def test_empty_or_unconfirmed_coverage_is_not_a_completed_match(self):
        self.assertEqual(self.payment_report(self.config(""))["status"], "needs_review")
        value = self.config("a,2026-10-01,charge,10,EUR,,,\n")
        value["balances"][0]["closing"] = "10"
        value["coverage_confirmed"] = False
        self.assertEqual(self.payment_report(value)["status"], "needs_review")

    def test_stripe_major_units_and_separate_fee_event(self):
        value = self.config("")
        path = self.root / "03_banking/stripe.csv"
        path.write_text("balance_transaction_id,created_utc,currency,gross,fee,net,reporting_category,is_managed_payments,withheld_tax\n"
                        "txn_1,2026-10-01 12:00:00,eur,100.00,3.00,97.00,charge,false,0\n", encoding="utf-8")
        value["sources"] = [{"path": "03_banking/stripe.csv", "format": "stripe_activity"}]
        value["balances"][0]["closing"] = "97.00"
        report = self.payment_report(value)
        self.assertEqual(report["totals_by_kind"]["EUR"]["charge"], "100.00")
        self.assertEqual(report["totals_by_kind"]["EUR"]["fee"], "-3.00")
        self.assertEqual(report["balances"][0]["calculated_closing"], "97.00")

    def test_stripe_net_mismatch_and_ambiguous_timezone_are_rejected(self):
        value = self.config("")
        path = self.root / "03_banking/stripe.csv"
        value["sources"] = [{"path": "03_banking/stripe.csv", "format": "stripe_activity"}]
        for heading, net in (("created_utc", "98"), ("created", "97")):
            path.write_text(f"balance_transaction_id,{heading},currency,gross,fee,net,reporting_category,is_managed_payments,withheld_tax\n"
                            f"txn_1,2026-10-01 12:00:00,eur,100,3,{net},charge,false,0\n", encoding="utf-8")
            with self.subTest(heading=heading), self.assertRaises(workspace.WorkspaceError):
                self.payment_report(value)

    def test_stripe_missing_tax_scope_or_truncated_optional_cell_fails_cleanly(self):
        for data in (
            b"balance_transaction_id,created_utc,currency,gross,fee,net,reporting_category\nt,2026-10-01 12:00:00,eur,100,23,77,charge\n",
            b"balance_transaction_id,created_utc,currency,gross,fee,net,reporting_category,is_managed_payments,withheld_tax,source_id\nt,2026-10-01 12:00:00,eur,100,3,97,charge,false,0\n",
        ):
            with self.subTest(data=data), self.assertRaises(workspace.WorkspaceError):
                payments.normalize(data, "stripe_activity", "synthetic.csv")

    def test_managed_payments_are_not_imported_as_simple_processing_fees(self):
        value = self.config("")
        path = self.root / "03_banking/stripe.csv"
        path.write_text("balance_transaction_id,created_utc,currency,gross,fee,net,reporting_category,is_managed_payments,withheld_tax\n"
                        "txn_1,2026-10-01 12:00:00,eur,100,22,78,charge,false,19\n", encoding="utf-8")
        value["sources"] = [{"path": "03_banking/stripe.csv", "format": "stripe_activity"}]
        with self.assertRaises(workspace.WorkspaceError):
            self.payment_report(value)

    def test_payout_bank_currency_and_duplicate_id_are_not_silently_accepted(self):
        for bank in ("b1,2026-10-03,10,USD\n", "b1,2026-10-03,10,EUR\nb1,2026-10-03,10,EUR\n"):
            value = self.config("c,2026-10-01,charge,10,EUR,,,\np,2026-10-02,payout,-10,EUR,,,b1\n", bank)
            if "USD" in bank:
                self.assertEqual(self.payment_report(value)["status"], "needs_review")
            else:
                with self.assertRaises(workspace.WorkspaceError):
                    self.payment_report(value)


if __name__ == "__main__":
    unittest.main()
