#!/usr/bin/env python3
"""
BSD V3.1 — Strict Sage-only sandbox (Clay-ready witness)
- Fails fast if 'sage' is not available.
- Computes L(E,1), L'(E,1) and analytic rank using Sage's L-series.
Usage:
  sage -python test_bsd_full_V3_1.py --outdir ./data_v3_1_... --curves 11a1,37a1,389a1,5077a1 --prec 200
"""
import argparse, os, csv, json, sys

try:
    # Import only works if executed under 'sage -python'
    from sageall import EllipticCurve
except Exception as e:
    sys.stderr.write("[ERROR] This V3.1 sandbox must be executed with 'sage -python'.\n")
    sys.stderr.write("Install SageMath and run: sage -python test_bsd_full_V3_1.py ...\n")
    sys.exit(2)

DEFAULT_CURVES = ["11a1","37a1","389a1","5077a1"]

def compute_rows(curves, prec=200):
    rows = []
    for lab in curves:
        try:
            E = EllipticCurve(lab)
            L = E.lseries()
            L.set_precision(prec)
            L1 = L(1)
            try:
                L1p = L.derivative()(1)
            except Exception:
                try:
                    L1p = L(1, 1)   # derivative order=1
                except Exception:
                    L1p = None
            try:
                a_rank = L.analytic_rank()
            except Exception:
                a_rank = E.analytic_rank()
            rows.append(dict(curve=lab,
                             L_at_1=float(L1),
                             L_deriv_at_1=(float(L1p) if L1p is not None else None),
                             analytic_rank=(int(a_rank) if a_rank is not None else None),
                             regulator_est=None,
                             error=None))
        except Exception as e:
            rows.append(dict(curve=lab, L_at_1=None, L_deriv_at_1=None, analytic_rank=None,
                             regulator_est=None, error=str(e)))
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--curves", default=",".join(DEFAULT_CURVES))
    ap.add_argument("--prec", type=int, default=200)
    args = ap.parse_args()
    outdir = args.outdir
    curves = [c.strip() for c in args.curves.split(",") if c.strip()]
    os.makedirs(outdir, exist_ok=True)

    rows = compute_rows(curves, prec=args.prec)

    csv_path = os.path.join(outdir, "bsd_full_results_V3_1.csv")
    cols = ["curve","L_at_1","L_deriv_at_1","analytic_rank","regulator_est","error"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in cols})

    man_path = os.path.join(outdir, "manifest.json")
    man = {"problem":"BSD","method":"sage-only","params":{"curves":curves,"prec":args.prec}}
    man["outputs"] = [{"path":"bsd_full_results_V3_1.csv"}]
    man["notes"] = "BSD V3.1 numeric witnesses computed strictly with Sage L-series."
    with open(man_path, "w") as f:
        json.dump(man, f, indent=2)

    print("[BSD V3.1] Done. CSV:", csv_path)

if __name__ == "__main__":
    main()
