#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/data/ns_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
python3 "$ROOT/test_ns_full.py" --outdir "$OUT"
echo "NS outputs in $OUT"
