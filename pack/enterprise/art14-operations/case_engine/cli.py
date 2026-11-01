"""Command line for the Article 14 case engine.

Examples (all timestamps need an offset; use Z for UTC):
  python -m case_engine create --id ART14-0001 --type aev --title "Lumen Engine type confusion" \
      --first-signal 2026-11-06T21:40Z --source threat_intel --component lumen-engine \
      --component-products reachable --evidence lumen-browser-desktop=exploited
  python -m case_engine aware --case ART14-0001 --at 2026-11-07T01:10Z --by "PSIRT duty officer" \
      --role psirt_duty_officer --rationale "Exploit chain confirmed against shipped build"
  python -m case_engine file --case ART14-0001 --notification all --stage early_warning \
      --at 2026-11-07T07:30Z --filed-by "AR one" --checked-by "AR two" --srp-id "SRP-{n}"
  python -m case_engine due --now 2026-11-08T12:00Z
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

from . import engine, srp_pack
from .clocks import UTC, fmt_utc, parse_utc
from .store import Store

DEFAULT_STORE = os.environ.get("ART14_STORE", "art14_cases.json")


def _evidence(args, registry) -> dict:
    ev = {}
    if getattr(args, "component_products", None):
        if not args.component:
            raise engine.CaseError("--component-products needs --component")
        for p in registry["products"]:
            if args.component in p.get("components", []):
                ev[p["id"]] = args.component_products
    for item in args.evidence or []:
        for part in item.split(","):
            if part.strip():
                pid, _, tier = part.partition("=")
                ev[pid.strip()] = tier.strip()
    return ev


def _print_due(items, out):
    if not items:
        print("No open items.", file=out)
        return
    rank = {"overdue": 0, "past-target": 1, "due-soon": 2, "open": 3, "pending-trigger": 4, "met-late": 5, "met": 6}
    items = sorted(items, key=lambda i: (rank.get(i["status"], 9), i["due_at"] or datetime.max.replace(tzinfo=UTC)))
    print(f"{'STATUS':<16}{'DUE (UTC)':<22}{'CASE':<16}{'REC':<5}{'ITEM'}", file=out)
    for i in items:
        flag = "*" if i["statutory"] else " "
        line = f"{i['status']:<16}{fmt_utc(i['due_at']):<22}{i['case']:<16}{i['notification']:<5}{flag}{i['item']}"
        print(line, file=out)
        if i.get("note"):
            print(f"{'':<59}{i['note']}", file=out)
    print("* statutory deadline; other times are pack targets", file=out)


def main(argv=None, out=sys.stdout) -> int:
    p = argparse.ArgumentParser(prog="case_engine", description="CRA Article 14 case engine (Aldermoor)")
    p.add_argument("--store", default=DEFAULT_STORE)
    p.add_argument("--registry", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create")
    c.add_argument("--id")
    c.add_argument("--type", required=True, choices=engine.CASE_TYPES)
    c.add_argument("--title", required=True)
    c.add_argument("--summary", default="")
    c.add_argument("--first-signal", required=True)
    c.add_argument("--source", required=True, choices=engine.DETECTION_SOURCES)
    c.add_argument("--component")
    c.add_argument("--component-products", choices=list(engine.fanout.EVIDENCE_TIERS))
    c.add_argument("--evidence", action="append", help="pid=exploited|reachable|not_reachable[,..]")
    c.add_argument("--mode", default="per_product", choices=engine.fanout.FANOUT_MODES)
    c.add_argument("--cve")
    c.add_argument("--entity-incident", action="store_true")

    a = sub.add_parser("aware")
    for flag in ("--case", "--at", "--by", "--role", "--rationale"):
        a.add_argument(flag, required=True)
    a.add_argument("--malicious", choices=["Yes", "No", "Unknown"])
    a.add_argument("--occurred")

    nr = sub.add_parser("not-reportable")
    for flag in ("--case", "--at", "--by", "--role", "--rationale"):
        nr.add_argument(flag, required=True)
    nr.add_argument("--criterion", required=True, choices=sorted(engine.NOT_REPORTABLE_CRITERIA))

    ct = sub.add_parser("content")
    ct.add_argument("--case", required=True)
    ct.add_argument("pairs", nargs="+", help="key=value")

    lg = sub.add_parser("legal")
    for flag in ("--case", "--notification", "--at", "--by", "--role"):
        lg.add_argument(flag, required=True)
    lg.add_argument("--stage", required=True, choices=["notification", "final_report"])

    f = sub.add_parser("file")
    for flag in ("--case", "--notification", "--at", "--filed-by", "--checked-by"):
        f.add_argument(flag, required=True)
    f.add_argument("--stage", required=True, choices=engine.STAGES)
    f.add_argument("--srp-id", help="use {n} for the record id when --notification all")
    f.add_argument("--evidence-ref")

    fx = sub.add_parser("fix")
    for flag in ("--case", "--product", "--at", "--desc"):
        fx.add_argument(flag, required=True)

    nt = sub.add_parser("notice")
    for flag in ("--case", "--product", "--at", "--channel"):
        nt.add_argument(flag, required=True)
    nt.add_argument("--kind", required=True, choices=["affected_users", "all_users", "machine_readable"])

    up = sub.add_parser("upstream")
    up.add_argument("--case", required=True)
    up.add_argument("--at", required=True)

    ud = sub.add_parser("update")
    for flag in ("--case", "--notification", "--at", "--filed-by", "--checked-by", "--reason"):
        ud.add_argument(flag, required=True)

    cr = sub.add_parser("csirt-request")
    for flag in ("--case", "--notification", "--at", "--respond-by", "--request"):
        cr.add_argument(flag, required=True)

    n2 = sub.add_parser("nis2")
    for flag in ("--case", "--at", "--by", "--outcome"):
        n2.add_argument(flag, required=True)

    cl = sub.add_parser("close")
    for flag in ("--case", "--at", "--by", "--role", "--review"):
        cl.add_argument(flag, required=True)

    d = sub.add_parser("due")
    d.add_argument("--now")
    d.add_argument("--case")

    for name in ("show", "timeline"):
        s = sub.add_parser(name)
        s.add_argument("--case", required=True)

    pk = sub.add_parser("pack")
    pk.add_argument("--case", required=True)
    pk.add_argument("--notification", required=True)
    pk.add_argument("--stage", required=True, choices=engine.STAGES)
    pk.add_argument("--format", default="text", choices=["text", "json"])

    sub.add_parser("coordinator")

    args = p.parse_args(argv)
    store = Store(args.store)
    reg = engine.load_registry(args.registry)

    try:
        if args.cmd == "create":
            case = engine.create_case(reg, args.type, args.title, args.first_signal, args.source,
                                      _evidence(args, reg), component=args.component, summary=args.summary,
                                      fanout_mode=args.mode, cve_id=args.cve, case_id=args.id,
                                      entity_incident=args.entity_incident)
            store.put(case)
            fo = case["fanout"]
            print(f"Created {case['id']} ({case['type']}), state triage. Rule {fo['rule']} {fo['mode']}: "
                  f"{len(fo['reportable'])} reportable product(s) -> {len(fo['notifications'])} SRP notification(s); "
                  f"not reportable: {', '.join(fo['not_reportable']) or 'none'}. "
                  f"Coordinator CSIRT: {case['coordinator']['member_state']}.", file=out)
            return 0
        if args.cmd == "coordinator":
            r = engine.routing.derive_coordinator(reg["manufacturer"], reg["coordinator_csirts"])
            print(json.dumps(r.as_dict(), indent=2), file=out)
            return 0
        if args.cmd == "due":
            now = parse_utc(args.now) if args.now else datetime.now(UTC)
            cases = [store.get(args.case)] if args.case else store.all()
            items = [i for cs in cases for i in engine.due_items(cs, reg, now) if i["status"] not in ("met",)]
            print(f"Due items at {fmt_utc(now)}", file=out)
            _print_due(items, out)
            return 0

        case = store.get(args.case)
        if args.cmd == "aware":
            engine.declare_awareness(case, reg, args.at, args.by, args.role, args.rationale,
                                     suspected_malicious=args.malicious, occurred_at=args.occurred)
        elif args.cmd == "not-reportable":
            engine.declare_not_reportable(case, reg, args.at, args.by, args.role, args.criterion, args.rationale)
        elif args.cmd == "content":
            engine.set_content(case, **dict(pair.split("=", 1) for pair in args.pairs))
        elif args.cmd == "legal":
            ids = [n["id"] for n in case["notifications"]] if args.notification == "all" else [args.notification]
            for nid in ids:
                engine.record_legal_review(case, reg, nid, args.stage, args.at, args.by, args.role)
        elif args.cmd == "file":
            ids = [n["id"] for n in case["notifications"]] if args.notification == "all" else [args.notification]
            for nid in ids:
                srp = args.srp_id.replace("{n}", nid) if args.srp_id else None
                engine.record_submission(case, nid, args.stage, args.at, args.filed_by, args.checked_by,
                                         srp_id=srp, evidence_ref=args.evidence_ref)
        elif args.cmd == "fix":
            engine.record_fix(case, args.product, args.at, args.desc)
        elif args.cmd == "notice":
            engine.record_user_notice(case, args.product, args.kind, args.at, args.channel)
        elif args.cmd == "upstream":
            engine.record_upstream(case, args.at)
        elif args.cmd == "update":
            engine.record_update(case, args.notification, args.at, args.filed_by, args.checked_by, args.reason)
        elif args.cmd == "csirt-request":
            engine.record_csirt_request(case, args.notification, args.at, args.respond_by, args.request)
        elif args.cmd == "nis2":
            engine.log_nis2_assessment(case, args.at, args.by, args.outcome)
        elif args.cmd == "close":
            engine.close_case(case, args.at, args.by, args.role, args.review)
        elif args.cmd == "show":
            print(json.dumps(case, indent=2), file=out)
            return 0
        elif args.cmd == "timeline":
            print(f"Timeline {case['id']} ({case['type']}) state={case['state']}", file=out)
            for e in engine.timeline(case):
                print(f"{fmt_utc(parse_utc(e['at']))}  {e['action']:<28} {e['role']:<24} {e['detail']}", file=out)
            return 0
        elif args.cmd == "pack":
            pack = srp_pack.build(case, reg, args.notification, args.stage)
            print(srp_pack.render_json(pack) if args.format == "json" else srp_pack.render_text(pack), file=out)
            return 0
        store.put(case)
        print(f"{case['id']}: {args.cmd} recorded; state {case['state']}", file=out)
        return 0
    except (engine.CaseError, engine.fanout.FanoutError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
