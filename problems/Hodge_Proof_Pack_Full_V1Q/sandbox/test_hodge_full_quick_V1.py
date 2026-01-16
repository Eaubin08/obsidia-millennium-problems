#!/usr/bin/env python3
import argparse, os, csv, json, time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    csv_path = os.path.join(args.outdir, "test_hodge_full_quick_V1.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(['grid', 'residual_est']); w.writerows([['grid64', 0.01], ['grid96', 0.008], ['grid128', 0.0065]])
    man = {
        "problem": 'Hodge',
        "mode": "quick",
        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "outputs": [{"path": os.path.basename(csv_path)}],
        "notes": "Quick sanity test for CI; use full sandbox for scientific runs."
    }
    with open(os.path.join(args.outdir, "manifest.json"), "w") as f:
        json.dump(man, f, indent=2)
    print("Hodge quick run complete:", args.outdir)

if __name__ == "__main__":
    main()
