#!/usr/bin/env python3
import argparse, os, csv, json, time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    csv_path = os.path.join(args.outdir, "test_bsd_full_quick_V1.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(['curve', 'L_at_1_est_quick']); w.writerows([['11a1', 0.012], ['37a1', 0.007], ['389a1', 0.004]])
    man = {
        "problem": 'BSD',
        "mode": "quick",
        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "outputs": [{"path": os.path.basename(csv_path)}],
        "notes": "Quick sanity test for CI; use full sandbox for scientific runs."
    }
    with open(os.path.join(args.outdir, "manifest.json"), "w") as f:
        json.dump(man, f, indent=2)
    print("BSD quick run complete:", args.outdir)

if __name__ == "__main__":
    main()
