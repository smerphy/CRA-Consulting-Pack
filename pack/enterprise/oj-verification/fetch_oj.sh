#!/usr/bin/env bash
# E6 OJ verification: reproducible fetch of the authentic Official Journal text of
# Regulation (EU) 2024/2847 and its corrigenda from the Publications Office cellar.
# EUR-Lex HTML/PDF pages return bot-challenge or JavaScript shells to scripts; the
# cellar content-negotiation endpoint returns the OJ XHTML manifestation directly.
#
# Usage: bash fetch_oj.sh [output_dir]   (default: ./fetched)
# Then:  diff <(python3 -I h2t.py fetched/32024R2847.xhtml /dev/stdout) source/oj_L_2024_2847_EN.txt
# A non-empty diff, or a new corrigendum number below, means the claims register needs re-verification.
set -euo pipefail
OUT="${1:-fetched}"
mkdir -p "$OUT"
BASE="https://publications.europa.eu/resource/celex"

fetch() { # celex, language (ISO 639-2/B), file
  local enc
  enc=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")
  curl -sS -m 90 -L -H "Accept: application/xhtml+xml" -H "Accept-Language: $2" \
       -o "$3" -w "%{http_code}" "$BASE/$enc"
}

echo "Regulation (EU) 2024/2847, EN: $(fetch 32024R2847 eng "$OUT/32024R2847.xhtml")"
sha256sum "$OUT/32024R2847.xhtml"
echo "Baseline sha256 (1 Nov 2026): fe0cca4a0caec50e7cf5a91432b94a19b211f86be8584fdba56372bdcea571ed"
# The OJ PDF/A-2a edition (81 pages). Note: an unavailable type returns HTTP 200 with an error text body, so check the file type.
curl -sS -m 90 -L -H "Accept: application/pdf;type=pdfa2a" -H "Accept-Language: eng" -o "$OUT/32024R2847.pdf" "$BASE/32024R2847"
file "$OUT/32024R2847.pdf"; sha256sum "$OUT/32024R2847.pdf"
echo "Baseline sha256 (1 Nov 2026): e3ecaabddf6e321fa04097d15dfcccc7309d0fe5896240ab7625a27d74ab1b0a"

# Corrigenda are numbered R(01), R(02)... Each exists only in the language(s) it corrects.
# Known on 1 Nov 2026: R(01) EN 5.12.2024; R(02) EN 2.7.2025; R(03) FR 3.10.2025; R(04) EN 17.10.2025;
# R(05) SK 23.2.2026; R(06) FR 25.3.2026; R(07) DE 6.8.2026; R(08) SL 9.10.2026.
for n in 01 02 03 04 05 06 07 08 09 10 11 12; do
  code=$(fetch "32024R2847R($n)" eng "$OUT/R$n-eng.xhtml")
  echo "Corrigendum R($n) EN: $code"
  [ "$code" = "200" ] || rm -f "$OUT/R$n-eng.xhtml"
done

# Related acts used in the claims register
for c in 32025R2392 32026R0339 32026R0881 32024L2853; do
  echo "$c EN: $(fetch "$c" eng "$OUT/$c.xhtml")"
done
