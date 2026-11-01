#!/usr/bin/env bash
# Generic CI step: run the CRA gate on a release directory and store the
# result in an append-only evidence store. Works with any CI system.
#
#   release_gate.sh <release_dir> <store_dir_or_bucket>
#
# Exit codes: 0 PASS, 1 FAIL, 3 REVIEW (from python -m cra_evidence gate).
set -euo pipefail

RELEASE="${1:?release dir}"
STORE="${2:?store}"
HERE="$(cd "$(dirname "$0")/../.." && pwd)"
POLICY="${POLICY:-$HERE/examples/policy/aldermoor-gate-policy.json}"
FEEDS="${FEEDS:-$HERE/examples/feeds}"

cd "$HERE"
set +e
python3 -m cra_evidence gate "$RELEASE" --policy "$POLICY" --feeds "$FEEDS" -v
rc=$?
set -e

# Every decision is stored, including FAIL and REVIEW: the trail of blocked
# releases is itself evidence that the gate operates (Module H audits).
case "$STORE" in
  s3://*) echo "upload to $STORE with --object-lock-mode COMPLIANCE (see github-actions example)";;
  *)      python3 -m cra_evidence store "$RELEASE" --policy "$POLICY" --feeds "$FEEDS" --store "$STORE" ;;
esac
exit $rc
