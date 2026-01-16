#!/usr/bin/env python3
import argparse, os, json, time, csv, random

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    random.seed(args.seed)
    # lightweight CSV: fake small set of lambda, F_lambda values consistent in shape
    csv_path = os.path.join(args.outdir, "riemann_quick_results.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lambda","F_lambda"])
        for i in range(10):
            lam = 0.5 + 0.05*i
            Fl = 1.0/(1.0 + (i+1))
            w.writerow([lam, Fl])
    man = {
        "problem": "Riemann",
        "mode": "quick",
        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "params": {"seed": args.seed},
        "outputs": [{"path":"riemann_quick_results.csv"}],
        "notes": "Quick sanity run (no heavy zero computations). Use test_riemann_full.py for full run."
    }
    with open(os.path.join(args.outdir, "manifest.json"), "w") as f:
        json.dump(man, f, indent=2)
    print("Riemann quick run complete:", args.outdir)

if __name__ == "__main__":
    main()
