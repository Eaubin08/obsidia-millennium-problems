#!/usr/bin/env python3
# Yang-Mills (lattice) full sandbox (automatic).
# - Wilson action surrogate on toy lattice
# - Correlator decay -> spectral gap estimate
# - Exports CSV, plot, manifest with SHA256

import argparse, os, csv, time, random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils import sha256_of_file, write_manifest

def random_links(L, seed=42):
    random.seed(seed)
    U = np.random.RandomState(seed).uniform(-np.pi, np.pi, size=(L,L,L,L))  # toy phases
    return U

def wilson_loop_estimate(U, L, beta=2.0):
    plaq = np.cos(U)
    return float(np.mean(plaq))

def correlator_decay(steps=100, seed=42):
    np.random.seed(seed)
    x = np.arange(steps)
    y = np.exp(-0.2*x) + 0.05*np.random.randn(steps)
    y = np.clip(y, 1e-8, None)
    # fit log to get gap
    from numpy.linalg import lstsq
    A = np.vstack([x, np.ones_like(x)]).T
    sol = lstsq(A, -np.log(y), rcond=None)[0]
    gap = float(sol[0])
    return gap, x, y

def run(args):
    outdir = os.path.abspath(args.outdir); os.makedirs(outdir, exist_ok=True)
    L = args.L
    U = random_links(L, seed=args.seed)
    wl = wilson_loop_estimate(U, L, beta=args.beta)
    gap, x, y = correlator_decay(steps=120, seed=args.seed)
    csv_path = os.path.join(outdir, "ym_observables.csv")
    with open(csv_path,"w",newline='',encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(["L","beta","wilson_loop","gap_estimate"])
        w.writerow([L, args.beta, wl, gap])
    plt.figure(); plt.plot(x,y); plt.xlabel("t"); plt.ylabel("corr"); plt.title("Correlator decay (toy)"); plt.savefig(os.path.join(outdir,"correlator.png"), dpi=160)
    outs=[{"path":"ym_observables.csv","sha256":sha256_of_file(csv_path)},
          {"path":"correlator.png","sha256":sha256_of_file(os.path.join(outdir,"correlator.png"))}]
    params={"L":L,"beta":args.beta,"seed":args.seed}
    write_manifest(outdir, f"ym_full_{int(time.time())}", "YangMills", params, outs, notes="Toy lattice baseline")
    print("Yang-Mills run complete:", outdir)

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", required=True)
    p.add_argument("--L", type=int, default=12)
    p.add_argument("--beta", type=float, default=2.0)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    run(args)
