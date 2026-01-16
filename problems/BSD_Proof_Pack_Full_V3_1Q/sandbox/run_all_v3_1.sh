#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/data_v3_1_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
LOG="$OUT/run_all_v3_1.log"
echo "[RUN_ALL V3.1] BSD — start at $(date -u)" | tee -a "$LOG"
# Requires Sage installed and on PATH
sage -python "$ROOT/test_bsd_full_V3_1.py" --outdir "$OUT" --curves 11a1,37a1,389a1,5077a1 --prec 200 2>&1 | tee -a "$LOG"
echo "[RUN_ALL V3.1] BSD — done at $(date -u)" | tee -a "$LOG"
echo "[RUN_ALL V3.1] Outputs in: $OUT" | tee -a "$LOG"
