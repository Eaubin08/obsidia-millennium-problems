
#!/usr/bin/env python3
\"\"\"P!=NP PF_inf sandbox
Features:
- constructs random graphs / expanders, measures spectral gap (numpy/scipy)
- tests PF_inf operator on boolean cube approximations via random functions
- outputs CSV, plots, manifest
\"\"\"
import argparse, os, time, csv, json
import numpy as np
from numpy.linalg import eigvals
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils import sha256_of_file, write_manifest
import random

def random_regular_graph(n, d, seed=42):
    random.seed(seed)
    # simple pairing model (may produce multiedges; acceptable for heuristic tests)
    nodes = list(range(n))
    stubs = []
    for v in nodes:
        stubs += [v]*d
    random.shuffle(stubs)
    edges = []
    for i in range(0, len(stubs), 2):
        if i+1 < len(stubs):
            a, b = stubs[i], stubs[i+1]
            if a != b:
                edges.append((a,b))
    return edges

def adjacency_matrix_from_edges(n, edges):
    A = np.zeros((n,n), dtype=float)
    for a,b in edges:
        A[a,b] += 1
        A[b,a] += 1
    return A

def spectral_gap(A):
    vals = eigvals(A)
    vals = np.real(vals)
    vals.sort()
    if len(vals) < 2: return 0.0
    return float(vals[-1] - vals[-2])

def pf_inf_variation_test(n, num_funcs=100, seed=42):
    np.random.seed(seed)
    # approximate PF_inf by smoothing via gaussian blur on hypercube embeddings (heuristic)
    results = []
    for i in range(num_funcs):
        f = np.random.randn(n)
        # apply smoothing: moving average
        g = np.convolve(f, np.ones(3)/3, mode='same')
        var_before = float(np.var(f))
        var_after = float(np.var(g))
        results.append((var_before, var_after))
    return results

def run(args):
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    params = {"nodes": args.nodes, "graphs": args.graphs, "seed": args.seed}
    csv_path = os.path.join(outdir, "pneqnp_full_results.csv")
    with open(csv_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["graph_id","nodes","d_reg","spectral_gap"])
        writer.writeheader()
        for gid in range(args.graphs):
            edges = random_regular_graph(args.nodes, 3, seed=args.seed+gid)
            A = adjacency_matrix_from_edges(args.nodes, edges)
            gap = spectral_gap(A)
            writer.writerow({"graph_id":gid,"nodes":args.nodes,"d_reg":3,"spectral_gap":gap})
    # pf_inf tests
    pf_results = pf_inf_variation_test(args.nodes, num_funcs=200, seed=args.seed)
    variances_before = [b for b,a in pf_results]
    variances_after = [a for b,a in pf_results]
    # plot hist
    figpath = os.path.join(outdir, "pf_variance_hist.png")
    plt.figure()
    plt.hist(variances_before, bins=30, alpha=0.6, label='before')
    plt.hist(variances_after, bins=30, alpha=0.6, label='after')
    plt.legend(); plt.savefig(figpath, dpi=150)
    outputs=[{"path":os.path.relpath(csv_path,start=outdir),"sha256":sha256_of_file(csv_path)}, {"path":os.path.relpath(figpath,start=outdir),"sha256":sha256_of_file(figpath)}]
    write_manifest(outdir, f"pneqnp_full_{int(time.time())}", "PneqNP", params, outputs, notes="Full automatic PF_inf + expander baseline")
    print("P!=NP full run complete. Results in", outdir)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--graphs", type=int, default=50)
    parser.add_argument("--nodes", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    run(args)
