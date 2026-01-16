#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/data/hodge_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
python3 "$ROOT/test_hodge_full.py" --outdir "$OUT"
echo "Hodge outputs in $OUT"
