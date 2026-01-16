
#!/usr/bin/env python3
"""Full Riemann sandbox.
Features:
- downloads Odlyzko zeros (optional) or uses local zero_file
- computes F_lambda via mpmath zeta evaluations across sigma grid, multi-kernel
- high-precision option (mp.dps)
- exports CSV, PNG heatmap, manifest with SHA256s
- designed to run automatically via run_all_full.sh
"""
import argparse, os, json, time, csv, math
from math import isfinite
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from utils import sha256_of_file, write_manifest

def download_odlyzko(dest):
    import requests
    url = "https://web.archive.org/web/20200101000000/https://www.dtc.umn.edu/~odlyzko/zeta_tables/zetaR.1"  # archived fallback URL
    r = requests.get(url, timeout=60)
    with open(dest, "wb") as f:
        f.write(r.content)
    return dest

def parse_zero_file(path, maxzeros):
    zeros = []
    with open(path,'r',encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.strip().split()
            if not parts: continue
            try:
                t = float(parts[0])
                zeros.append(t)
                if len(zeros) >= maxzeros: break
            except:
                continue
    return zeros

def gauss_kernel(sigma_arg, lam):
    return mp.e**(-lam*(mp.mpf(sigma_arg)-mp.mpf('0.5'))**2)

def fejer_kernel(sigma_arg, lam):
    x = (sigma_arg - mp.mpf('0.5'))*mp.mpf('10.0')
    return (mp.sin(x)/x)**2 if x != 0 else mp.mpf('1.0')

def poisson_kernel(sigma_arg, lam):
    x = abs(sigma_arg - mp.mpf('0.5'))
    return 1/(1 + lam*(x**2))

def zeta_mp(s, prec):
    mp.mp.dps = prec
    return mp.zeta(s)

def compute_F_lambda(sigma, t, lam, kernel_name, prec):
    mp.mp.dps = prec
    s = mp.mpf(sigma) + mp.j*mp.mpf(t)
    z = zeta_mp(s, prec)
    if kernel_name == 'gauss': k = gauss_kernel(sigma, lam)
    elif kernel_name == 'fejer': k = fejer_kernel(sigma, lam)
    elif kernel_name == 'poisson': k = poisson_kernel(sigma, lam)
    else: raise ValueError("Unknown kernel")
    return z * k

def run(args):
    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    # zeros
    if args.zero_file and os.path.exists(args.zero_file):
        zeros = parse_zero_file(args.zero_file, args.zeros)
    else:
        zero_file = os.path.join(outdir, "odlyzko.txt")
        try:
            download_odlyzko(zero_file)
            zeros = parse_zero_file(zero_file, args.zeros)
        except Exception as e:
            # fallback small list
            zeros = [14.1347251417347,21.0220396387715,25.0108575801457,30.4248761258595,32.9350615877392][:args.zeros]

    params = {"lambdas": args.lambdas, "kernels": args.kernels, "zeros": len(zeros), "prec": args.prec, "delta": args.delta, "seed": args.seed}
    csv_path = os.path.join(outdir, "riemann_full_results.csv")
    fieldnames = ['t','lambda','kernel','sigma_min','E_min','B_delta']
    with open(csv_path, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for lam in args.lambdas:
            for kernel in args.kernels:
                for t in zeros:
                    # coarse grid then refine
                    sigmas = np.linspace(0.0,1.0,201)
                    Evals = []
                    for s in sigmas:
                        try:
                            F = compute_F_lambda(s, t, lam, kernel, args.prec)
                            Evals.append(float(abs(F)**2))
                        except Exception as e:
                            Evals.append(float('nan'))
                    if all(math.isnan(x) for x in Evals):
                        sigma_min = float('nan'); E_min = float('nan')
                    else:
                        idx = int(np.nanargmin(Evals))
                        sigma_min = float(sigmas[idx])
                        # refine around
                        a = max(0.0, sigma_min-0.01); b = min(1.0, sigma_min+0.01)
                        sig2 = np.linspace(a,b,201)
                        Evals2 = []
                        for s in sig2:
                            try:
                                F = compute_F_lambda(s, t, lam, kernel, args.prec)
                                Evals2.append(float(abs(F)**2))
                            except:
                                Evals2.append(float('nan'))
                        idx2 = int(np.nanargmin(Evals2))
                        sigma_min = float(sig2[idx2])
                        E_min = float(Evals2[idx2])
                    # compute B_delta
                    try:
                        s_plus = compute_F_lambda(sigma_min + args.delta, t, lam, kernel, args.prec)
                        s_minus = compute_F_lambda(sigma_min - args.delta, t, lam, kernel, args.prec)
                        B_delta = float(abs(s_plus - s_minus))
                    except:
                        B_delta = float('nan')
                    writer.writerow({'t':t,'lambda':lam,'kernel':kernel,'sigma_min':sigma_min,'E_min':E_min,'B_delta':B_delta})

    # make a heatmap for first lambda/kernel pair for visualization
    try:
        lam = args.lambdas[0]; kernel = args.kernels[0]; t = zeros[0]
        grid = np.zeros((201,201))
        sigmas = np.linspace(0.0,1.0,201)
        ts = np.linspace(t-0.5, t+0.5, 201)
        for i,s in enumerate(sigmas):
            for j,tt in enumerate(ts):
                try:
                    F = compute_F_lambda(s, tt, lam, kernel, args.prec)
                    grid[i,j] = float(abs(F)**2)
                except:
                    grid[i,j] = np.nan
        plt.imshow(np.log1p(grid), extent=(ts[0], ts[-1], sigmas[0], sigmas[-1]), aspect='auto', origin='lower')
        plt.xlabel('t'); plt.ylabel('sigma'); plt.title(f'log1p |F_lambda|^2 heatmap lam={lam} kernel={kernel}')
        figpath = os.path.join(outdir, "riemann_heatmap.png")
        plt.colorbar()
        plt.savefig(figpath, dpi=200)
    except Exception as e:
        figpath = None

    outputs = []
    outputs.append({"path": os.path.relpath(csv_path, start=outdir), "sha256": sha256_of_file(csv_path)})
    if figpath:
        outputs.append({"path": os.path.relpath(figpath, start=outdir), "sha256": sha256_of_file(figpath)})
    write_manifest(outdir, f"riemann_full_{int(time.time())}", "Riemann", params, outputs, notes="Full numerical run (automatic)")
    print("Riemann full run complete. Results in", outdir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--zeros", type=int, default=100)
    parser.add_argument("--lambdas", type=lambda s: [float(x) for x in s.split(',')], default="10,30,50")
    parser.add_argument("--kernels", type=lambda s: s.split(','), default="gauss,fejer,poisson")
    parser.add_argument("--delta", type=float, default=1e-4)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--prec", type=int, default=80)
    parser.add_argument("--zero_file", default="")
    args = parser.parse_args()
    run(args)
