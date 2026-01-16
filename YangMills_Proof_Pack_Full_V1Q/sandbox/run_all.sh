#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/data/ym_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
python3 "$ROOT/test_ym_full.py" --outdir "$OUT"
echo "YM outputs in $OUT"
