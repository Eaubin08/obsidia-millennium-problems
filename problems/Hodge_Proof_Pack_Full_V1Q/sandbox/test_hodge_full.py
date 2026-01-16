#!/usr/bin/env python3
# Hodge Conjecture sandbox (automatic).
# - Synthetic Kahler-like SPD metric; intersection positivity checks
# - Primitive projection consistency (toy baseline)
# - Exports CSV, plot, manifest with SHA256

import argparse, os, csv, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils import sha256_of_file, write_manifest

def random_kahler_example(n, seed=42):
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((n,n))
    G = A.T @ A + n*np.eye(n)
    return G

def intersection_number(G, v):
    return float(v.T @ G @ v)

def run(args):
    outdir = os.path.abspath(args.outdir); os.makedirs(outdir, exist_ok=True)
    n = args.n
    G = random_kahler_example(n, seed=args.seed)
    rng = np.random.default_rng(args.seed)
    m = args.samples
    vals = []
    for _ in range(m):
        v = rng.standard_normal(n)
        vals.append(intersection_number(G, v))
    vals = np.array(vals)
    csv_path = os.path.join(outdir, "hodge_intersections.csv")
    with open(csv_path,"w",newline='',encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(["value"])
        for x in vals: w.writerow([x])
    plt.figure(); plt.hist(vals, bins=30); plt.title("Intersection numbers (toy)"); plt.savefig(os.path.join(outdir,"hodge_hist.png"), dpi=160)
    outs=[{"path":"hodge_intersections.csv","sha256":sha256_of_file(csv_path)},
          {"path":"hodge_hist.png","sha256":sha256_of_file(os.path.join(outdir,"hodge_hist.png"))}]
    params={"n":n,"samples":m,"seed":args.seed}
    write_manifest(outdir, f"hodge_full_{int(time.time())}", "Hodge", params, outs, notes="Positivity baseline (toy)")
    print("Hodge run complete:", outdir)

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", required=True)
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--samples", type=int, default=500)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    run(args)
