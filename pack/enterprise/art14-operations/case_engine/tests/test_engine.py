"""Unit tests for the Article 14 case engine. Run from art14-operations/:
    python3 -m unittest discover -s case_engine/tests -t .
"""
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from case_engine import cli, clocks, engine, fanout, routing, srp_pack
from case_engine.clocks import UTC, parse_utc

REG = engine.load_registry()
ENGINE_PRODUCTS = ["lumen-browser-desktop", "lumen-browser-mobile", "lumen-os", "lumen-webview",
                   "hearth-hub-display", "drive-sync-client"]


def engine_evidence():
    ev = {p: "reachable" for p in ENGINE_PRODUCTS}
    ev["lumen-browser-desktop"] = "exploited"
    return ev


def new_aev(mode="per_product", evidence=None):
    return engine.create_case(REG, "aev", "Lumen Engine JIT type confusion exploited in the wild",
                              "2026-11-06T21:40:00Z", "threat_intel", evidence or engine_evidence(),
                              component="lumen-engine", summary="Type confusion in the Lumen Engine JIT.",
                              fanout_mode=mode, case_id="ART14-T1")


def aware(case, at="2026-11-07T01:10:00Z", role="psirt_duty_officer", **kw):
    return engine.declare_awareness(case, REG, at, "Duty officer", role, "Exploit confirmed", **kw)


class ClockTests(unittest.TestCase):
    def test_24_and_72_hours_run_from_awareness(self):
        a = parse_utc("2026-11-07T01:10:00Z")
        self.assertEqual(clocks.early_warning_due(a), parse_utc("2026-11-08T01:10:00Z"))
        self.assertEqual(clocks.notification_due(a), parse_utc("2026-11-10T01:10:00Z"))

    def test_weekend_agnostic(self):
        friday = parse_utc("2026-11-06T18:00:00Z")  # Friday
        self.assertEqual(clocks.early_warning_due(friday).weekday(), 5)  # Saturday, no roll-forward
        self.assertEqual(clocks.notification_due(friday), parse_utc("2026-11-09T18:00:00Z"))

    def test_offsets_are_normalised_to_utc(self):
        self.assertEqual(parse_utc("2026-11-07T02:10:00+01:00"), parse_utc("2026-11-07T01:10:00Z"))
        self.assertEqual(parse_utc("2026-11-07 01:10 UTC"), parse_utc("2026-11-07T01:10:00Z"))

    def test_naive_timestamp_rejected(self):
        with self.assertRaises(clocks.ClockError):
            parse_utc("2026-11-07T01:10:00")

    def test_aev_final_14_days_after_measure(self):
        self.assertIsNone(clocks.aev_final_due(None))
        fix = parse_utc("2026-11-09T16:00:00Z")
        self.assertEqual(clocks.aev_final_due(fix), parse_utc("2026-11-23T16:00:00Z"))

    def test_si_final_one_month_after_notification_submission(self):
        self.assertIsNone(clocks.si_final_due(None))
        self.assertEqual(clocks.si_final_due(parse_utc("2026-11-10T09:00:00Z")), parse_utc("2026-12-10T09:00:00Z"))
        self.assertEqual(clocks.si_final_due(parse_utc("2027-01-31T09:00:00Z")), parse_utc("2027-02-28T09:00:00Z"))
        self.assertEqual(clocks.si_final_due(parse_utc("2028-01-31T09:00:00Z")), parse_utc("2028-02-29T09:00:00Z"))
        self.assertEqual(clocks.si_final_due(parse_utc("2026-12-15T09:00:00Z")), parse_utc("2027-01-15T09:00:00Z"))

    def test_srp_counter_quirk(self):
        ew = parse_utc("2026-11-07T07:30:00Z")
        self.assertEqual(clocks.srp_72h_counter(ew), parse_utc("2026-11-09T07:30:00Z"))

    def test_status(self):
        now = parse_utc("2026-11-08T00:00:00Z")
        due = parse_utc("2026-11-08T01:00:00Z")
        self.assertEqual(clocks.status(due, None, now), "due-soon")
        self.assertEqual(clocks.status(due, None, now + timedelta(hours=2)), "overdue")
        self.assertEqual(clocks.status(due, due + timedelta(minutes=1), now), "met-late")
        self.assertEqual(clocks.status(None, None, now), "pending-trigger")


class RoutingTests(unittest.TestCase):
    def test_aldermoor_routes_to_ireland(self):
        r = routing.derive_coordinator(REG["manufacturer"], REG["coordinator_csirts"])
        self.assertEqual(r.member_state, "IE")
        self.assertIn("main establishment", r.basis)
        self.assertIn("ncsc.gov.ie", r.csirt_url)

    def test_most_employees_when_decisions_not_determinable(self):
        m = json.loads(json.dumps(REG["manufacturer"]))
        for e in m["eu_establishments"]:
            e["product_security_decisions_predominant"] = False
        m["eu_establishments"][1]["employees"] = 99999
        self.assertEqual(routing.derive_coordinator(m, REG["coordinator_csirts"]).member_state, "DE")

    def test_non_eu_fallback_order(self):
        m = {"eu_establishments": [], "authorised_representative_member_state": None,
             "importer_member_state": "NL", "distributor_member_state": "BE", "most_users_member_state": "DE"}
        r = routing.derive_coordinator(m, REG["coordinator_csirts"])
        self.assertEqual(r.member_state, "NL")
        self.assertIn("importer", r.basis)
        m["importer_member_state"] = None
        self.assertEqual(routing.derive_coordinator(m, REG["coordinator_csirts"]).member_state, "BE")

    def test_no_data_raises(self):
        with self.assertRaises(routing.RoutingError):
            routing.derive_coordinator({"eu_establishments": []}, {})


class FanoutTests(unittest.TestCase):
    def test_component_lookup(self):
        self.assertEqual(sorted(fanout.products_with_component(REG, "lumen-engine")), sorted(ENGINE_PRODUCTS))

    def test_per_product_engine_bug_gives_six_notifications_in_27_states(self):
        plan = fanout.plan(REG, engine_evidence(), "per_product")
        self.assertEqual(len(plan["notifications"]), 6)
        union = set().union(*[set(n["member_states"]) for n in plan["notifications"]])
        self.assertEqual(len(union), 27)
        hub = [n for n in plan["notifications"] if n["products"] == ["hearth-hub-display"]][0]
        self.assertEqual(len(hub["member_states"]), 19)

    def test_grouped_gives_one(self):
        plan = fanout.plan(REG, engine_evidence(), "grouped")
        self.assertEqual(len(plan["notifications"]), 1)
        self.assertEqual(len(plan["notifications"][0]["member_states"]), 27)

    def test_not_reachable_is_excluded_and_recorded(self):
        ev = engine_evidence()
        ev["drive-sync-client"] = "not_reachable"
        plan = fanout.plan(REG, ev)
        self.assertEqual(len(plan["notifications"]), 5)
        self.assertEqual(plan["not_reportable"], ["drive-sync-client"])

    def test_bad_inputs(self):
        with self.assertRaises(fanout.FanoutError):
            fanout.plan(REG, {"no-such-product": "exploited"})
        with self.assertRaises(fanout.FanoutError):
            fanout.plan(REG, {"lumen-webview": "suspected"})


class StateMachineTests(unittest.TestCase):
    def test_awareness_needs_authority_role_and_no_approval(self):
        case = new_aev()
        with self.assertRaises(engine.CaseError):
            aware(case, role="vp_engineering")
        aware(case)
        self.assertEqual(case["state"], "aware")
        self.assertEqual(len(case["notifications"]), 6)
        self.assertEqual(case["decision_log"][-1]["action"], "awareness_declared")

    def test_awareness_cannot_precede_first_signal(self):
        with self.assertRaises(engine.CaseError):
            aware(new_aev(), at="2026-11-06T20:00:00Z")

    def test_not_reportable_path(self):
        case = engine.create_case(REG, "aev", "Bug bounty report, no exploitation", "2026-11-02T10:00:00Z",
                                  "vrp_bug_bounty", {"lumen-browser-desktop": "reachable"},
                                  component="lumen-engine", case_id="ART14-NR")
        with self.assertRaises(engine.CaseError):
            engine.declare_not_reportable(case, REG, "2026-11-02T14:00:00Z", "Lead", "psirt_lead",
                                          "no_exploitation_evidence", " ")
        engine.declare_not_reportable(case, REG, "2026-11-02T14:00:00Z", "Lead", "psirt_lead",
                                      "no_exploitation_evidence", "VRP finding, no telemetry evidence")
        self.assertEqual(case["state"], "not_reportable")
        self.assertEqual(engine.due_items(case, REG, parse_utc("2026-11-03T00:00:00Z")), [])

    def test_filing_order_four_eyes_and_legal_gates(self):
        case = new_aev()
        aware(case)
        with self.assertRaises(engine.CaseError):  # notification before early warning
            engine.record_legal_review(case, REG, "N1", "notification", "2026-11-08T10:00:00Z", "Counsel", "product_counsel")
            engine.record_submission(case, "N1", "notification", "2026-11-08T11:00:00Z", "A", "B")
        case = new_aev()
        aware(case)
        with self.assertRaises(engine.CaseError):
            engine.record_submission(case, "N1", "early_warning", "2026-11-07T07:00:00Z", "Ana", "ana", srp_id="S1")
        with self.assertRaises(engine.CaseError):
            engine.record_submission(case, "N1", "early_warning", "2026-11-07T07:00:00Z", "Ana", "Ben")  # no SRP id
        engine.record_submission(case, "N1", "early_warning", "2026-11-07T07:00:00Z", "Ana", "Ben", srp_id="S1")
        with self.assertRaises(engine.CaseError):  # legal review missing
            engine.record_submission(case, "N1", "notification", "2026-11-08T11:00:00Z", "Ana", "Ben")
        with self.assertRaises(engine.CaseError):
            engine.record_legal_review(case, REG, "N1", "early_warning", "2026-11-07T06:00:00Z", "C", "product_counsel")
        engine.record_legal_review(case, REG, "N1", "notification", "2026-11-08T10:00:00Z", "C", "product_counsel")
        engine.record_submission(case, "N1", "notification", "2026-11-08T11:00:00Z", "Ana", "Ben")
        self.assertEqual(case["state"], "aware")  # other five records still at aware

    def test_full_aev_lifecycle_and_deadlines(self):
        case = new_aev(mode="grouped")
        aware(case)
        engine.record_submission(case, "N1", "early_warning", "2026-11-07T07:30:00Z", "Ana", "Ben", srp_id="S1")
        self.assertEqual(case["state"], "early_warning_filed")
        engine.record_legal_review(case, REG, "N1", "notification", "2026-11-08T20:00:00Z", "C", "product_counsel")
        engine.record_submission(case, "N1", "notification", "2026-11-09T09:00:00Z", "Ana", "Ben")
        engine.record_legal_review(case, REG, "N1", "final_report", "2026-11-12T10:00:00Z", "C", "product_counsel")
        with self.assertRaises(engine.CaseError):  # no fix yet
            engine.record_submission(case, "N1", "final_report", "2026-11-12T11:00:00Z", "Ana", "Ben")
        engine.record_fix(case, "lumen-webview", "2026-11-12T00:00:00Z", "Lumen WebView update")
        engine.record_fix(case, "lumen-browser-desktop", "2026-11-09T16:00:00Z", "Browser stable update")
        d = engine.deadlines(case, case["notifications"][0])
        self.assertEqual(d["final_report"][0], parse_utc("2026-11-23T16:00:00Z"))  # earliest fix + 14 d
        self.assertEqual(d["early_warning"][0], parse_utc("2026-11-08T01:10:00Z"))
        engine.record_submission(case, "N1", "final_report", "2026-11-20T11:00:00Z", "Ana", "Ben")
        self.assertEqual(case["state"], "final_filed")
        with self.assertRaises(engine.CaseError):
            engine.record_update(case, "N1", "2026-11-21T10:00:00Z", "Ana", "Ben", "late detail")
        engine.close_case(case, "2026-12-01T10:00:00Z", "Lead", "psirt_lead", "PIR-1")
        self.assertEqual(case["state"], "closed")

    def test_severe_incident_final_runs_from_actual_notification(self):
        case = engine.create_case(REG, "severe_incident", "Update signing key misuse", "2026-11-10T08:00:00Z",
                                  "telemetry", {"hearth-camera": "exploited"}, case_id="ART14-SI")
        with self.assertRaises(engine.CaseError):
            aware(case, at="2026-11-10T09:00:00Z")  # suspected_malicious missing
        aware(case, at="2026-11-10T09:00:00Z", suspected_malicious="Yes")
        engine.record_submission(case, "N1", "early_warning", "2026-11-10T15:00:00Z", "Ana", "Ben", srp_id="S9")
        engine.record_legal_review(case, REG, "N1", "notification", "2026-11-11T20:00:00Z", "C", "legal_duty_counsel")
        engine.record_submission(case, "N1", "notification", "2026-11-12T10:00:00Z", "Ana", "Ben")
        d = engine.deadlines(case, case["notifications"][0])
        self.assertEqual(d["final_report"][0], parse_utc("2026-12-12T10:00:00Z"))
        with self.assertRaises(engine.CaseError):
            engine.record_fix(case, "hearth-camera", "2026-11-12T10:00:00Z", "n/a")
        items = engine.due_items(case, REG, parse_utc("2026-11-10T22:00:00Z"))
        self.assertTrue(any("NIS2" in i["item"] for i in items))

    def test_due_items_and_overdue(self):
        case = new_aev()
        aware(case)
        now = parse_utc("2026-11-08T02:00:00Z")  # 24h passed, nothing filed
        items = engine.due_items(case, REG, now)
        ew = [i for i in items if i["item"] == "SRP early warning"]
        self.assertEqual(len(ew), 6)
        self.assertTrue(all(i["status"] == "overdue" for i in ew))
        self.assertTrue(any(i["item"].startswith("Upstream report") for i in items))
        self.assertTrue(any(i["item"].startswith("User notice, impacted users") for i in items))
        later = engine.due_items(case, REG, parse_utc("2026-11-12T00:00:00Z"))
        notice = [i for i in later if i["item"].startswith("User notice, impacted users")]
        self.assertTrue(all(i["status"] == "past-target" and not i["statutory"] for i in notice))

    def test_late_product_addition_opens_new_record(self):
        ev = engine_evidence()
        ev["drive-sync-client"] = "not_reachable"
        case = new_aev(evidence=ev)
        aware(case)
        self.assertEqual(len(case["notifications"]), 5)
        engine.update_evidence(case, REG, {"drive-sync-client": "exploited"}, "2026-11-08T03:00:00Z", "Lead", "psirt_lead")
        self.assertEqual(len(case["notifications"]), 6)
        with self.assertRaises(engine.CaseError):
            engine.update_evidence(case, REG, {"lumen-webview": "not_reachable"}, "2026-11-08T04:00:00Z", "Lead", "psirt_lead")

    def test_csirt_request_tracked_until_update(self):
        case = new_aev(mode="grouped")
        aware(case)
        engine.record_submission(case, "N1", "early_warning", "2026-11-07T07:30:00Z", "Ana", "Ben", srp_id="S1")
        engine.record_csirt_request(case, "N1", "2026-11-07T12:00:00Z", "2026-11-07T18:00:00Z", "Confirm affected WebView versions")
        now = parse_utc("2026-11-07T19:00:00Z")
        req = [i for i in engine.due_items(case, REG, now) if i["item"].startswith("Intermediate")]
        self.assertEqual(req[0]["status"], "overdue")
        engine.record_update(case, "N1", "2026-11-07T19:30:00Z", "Ana", "Ben", "Versions confirmed")
        self.assertFalse([i for i in engine.due_items(case, REG, now) if i["item"].startswith("Intermediate")])


class SrpPackTests(unittest.TestCase):
    def test_early_warning_pack_ready_with_minimum_fields(self):
        case = new_aev()
        aware(case)
        pack = srp_pack.build(case, REG, "N4", "early_warning")
        self.assertTrue(pack["ready"], pack["gaps"])
        vals = {r["key"]: r["value"] for r in pack["fields"]}
        self.assertEqual(vals["aware_at"], "2026-11-07 01:10 UTC")
        self.assertIn("Lumen WebView", vals["product_name_version"])
        self.assertIn("[ART14-T1 N4/6]", vals["title"])
        self.assertEqual(len(vals["member_states"].split(", ")), 27)
        self.assertNotIn("pec_indicator", vals)

    def test_notification_pack_flags_gaps_then_ready(self):
        case = new_aev()
        aware(case)
        pack = srp_pack.build(case, REG, "N1", "notification")
        self.assertFalse(pack["ready"])
        self.assertIn("General information (product, nature of the exploit and vulnerability)", pack["gaps"])
        self.assertIn("pec_indicator", [r["key"] for r in pack["fields"]])
        engine.set_content(case, general_information="Type confusion in JIT; remote code execution in renderer.")
        self.assertTrue(srp_pack.build(case, REG, "N1", "notification")["ready"])

    def test_length_limits_and_json_export(self):
        case = new_aev()
        case["title"] = "x" * 300
        aware(case)
        pack = srp_pack.build(case, REG, "N1", "early_warning")
        self.assertTrue(any("exceeds 255" in e for e in pack["errors"]))
        exported = json.loads(srp_pack.render_json(pack))
        self.assertIn("internal", exported["schema"])
        self.assertIn("READY", srp_pack.render_text(pack))

    def test_incident_pack_has_incident_fields(self):
        case = engine.create_case(REG, "severe_incident", "Update channel compromise", "2026-11-10T08:00:00Z",
                                  "telemetry", {"hearth-camera": "exploited"}, case_id="ART14-SI2")
        aware(case, at="2026-11-10T09:00:00Z", suspected_malicious="Unknown")
        keys = [r["key"] for r in srp_pack.build(case, REG, "N1", "early_warning")["fields"]]
        self.assertIn("suspected_malicious", keys)
        self.assertNotIn("cve_id", keys)


class CliTests(unittest.TestCase):
    def run_cli(self, store, *argv):
        buf = io.StringIO()
        rc = cli.main(["--store", store, *argv], out=buf)
        return rc, buf.getvalue()

    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = str(Path(tmp) / "cases.json")
            rc, out = self.run_cli(store, "create", "--id", "ART14-C1", "--type", "aev", "--title", "Engine bug",
                                   "--first-signal", "2026-11-06T21:40Z", "--source", "threat_intel",
                                   "--component", "lumen-engine", "--component-products", "reachable",
                                   "--evidence", "lumen-browser-desktop=exploited")
            self.assertEqual(rc, 0)
            self.assertIn("6 SRP notification(s)", out)
            rc, _ = self.run_cli(store, "aware", "--case", "ART14-C1", "--at", "2026-11-07T01:10Z", "--by", "Duty",
                                 "--role", "psirt_duty_officer", "--rationale", "confirmed")
            self.assertEqual(rc, 0)
            rc, _ = self.run_cli(store, "file", "--case", "ART14-C1", "--notification", "all", "--stage",
                                 "early_warning", "--at", "2026-11-07T07:30Z", "--filed-by", "Ana",
                                 "--checked-by", "Ben", "--srp-id", "SRP-{n}")
            self.assertEqual(rc, 0)
            rc, out = self.run_cli(store, "due", "--now", "2026-11-09T09:00Z")
            self.assertIn("SRP notification", out)
            self.assertIn("SRP counter will show 2026-11-09 07:30 UTC", out)
            rc, out = self.run_cli(store, "pack", "--case", "ART14-C1", "--notification", "N2", "--stage", "early_warning")
            self.assertIn("SRP-N2", out)
            rc, out = self.run_cli(store, "timeline", "--case", "ART14-C1")
            self.assertIn("awareness_declared", out)
            rc = cli.main(["--store", store, "file", "--case", "ART14-C1", "--notification", "N1", "--stage",
                           "final_report", "--at", "2026-11-08T07:30Z", "--filed-by", "Ana", "--checked-by", "Ben"],
                          out=io.StringIO())
            self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
