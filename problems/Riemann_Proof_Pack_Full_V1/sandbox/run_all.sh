#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUTROOT="$ROOT/data/full_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTROOT"
LOG="$OUTROOT/run_all.log"
echo "[RUN_ALL] Riemann Hypothesis — Obsidia Sandbox start at $(date -u)" | tee -a "$LOG"
python3 "$ROOT/test_riemann_full.py" --outdir "$OUTROOT" 2>&1 | tee -a "$LOG"
echo "[RUN_ALL] Riemann Hypothesis — Obsidia Sandbox done at $(date -u)" | tee -a "$LOG"
