
import numpy as np, csv, json, time, os, hashlib, random, math

out_dir = os.path.join(os.path.dirname(__file__), "outputs_V1")
os.makedirs(out_dir, exist_ok=True)

rng = np.random.default_rng(42)

def fejer_discrete(x):
    # simple averaging kernel
    return np.convolve(x, np.ones(3)/3.0, mode='same')

def gauss_discrete(x):
    k = np.array([0.27406862, 0.45186276, 0.27406862])
    return np.convolve(x, k, mode='same')

def poisson_discrete(x):
    k = np.array([0.25, 0.5, 0.25])
    return np.convolve(x, k, mode='same')

def energy(x):
    # energy = mean square (as a proxy for PF∞ metric)
    x = np.asarray(x)
    return float(np.mean(x*x))

def reduction_polynomial(x, factor=2):
    # toy "reduction": downsample + upsample
    y = x[::factor]
    z = np.repeat(y, factor)[:len(x)]
    return z

def run_suite(n_list=[256,512,1024], trials=5):
    rows = []
    kernels = {
        "fejer": fejer_discrete,
        "gauss": gauss_discrete,
        "poisson": poisson_discrete
    }
    for n in n_list:
        for t in range(trials):
            x = rng.standard_normal(n)
            for kname, kfun in kernels.items():
                xk = kfun(x)
                e0 = energy(xk)
                xr = reduction_polynomial(xk, factor=2)
                er = energy(xr)
                dE = abs(e0 - er)
                rows.append({"n": n, "trial": t, "kernel": kname, "E_before": e0, "E_after": er, "dE": dE})
    return rows

rows = run_suite()
csv_path = os.path.join(out_dir, "pneqnp_energy_deltas.csv")
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["n","trial","kernel","E_before","E_after","dE"])
    w.writeheader()
    for row in rows:
        w.writerow(row)

def write_manifest(folder, notes):
    mpath = os.path.join(folder, "manifest_V1.json")
    notes = dict(notes)
    notes["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    # hash all files in folder
    hashes = {}
    for root, _, fs in os.walk(folder):
        for fname in fs:
            p = os.path.join(root, fname)
            with open(p, "rb") as fh:
                hashes[os.path.relpath(p, folder)] = hashlib.sha256(fh.read()).hexdigest()
    notes["files_sha256"] = hashes
    with open(mpath, "w") as f:
        json.dump(notes, f, indent=2)
    return mpath

mpath = write_manifest(out_dir, {"suite": "PneqNP_V1", "comment": "Energy delta under reduction"})
print("OK PneqNP_V1:", csv_path, "manifest:", mpath)


# --- V2 additions: delta_energy + reductibility_flag ---
def pf_inf_smooth(x, rounds=2):
    # simple local averaging on boolean vectors treated as +/-1 arrays
    # Here x is numpy array of shape (m,n), values in {-1,1}
    import numpy as np
    y = x.astype(float).copy()
    m,n = y.shape
    for _ in range(rounds):
        # average with a random subset of neighbors (toy)
        shift = np.roll(y, 1, axis=1)
        y = 0.5*y + 0.5*shift
        # renormalize gently
        y = np.clip(y, -1.0, 1.0)
    return y

def variance(arr):
    import numpy as np
    return float(np.var(arr))

def run_v2_extras(outdir, rng, samples=200, nbits=128):
    import numpy as np
    # random boolean vectors
    X = rng.choice([-1,1], size=(samples, nbits))
    v0 = variance(X)
    Xs = pf_inf_smooth(X, rounds=2)
    v1 = variance(Xs)
    delta_E = max(0.0, v0 - v1)  # energy drop under smoothing
    # reductibility heuristic threshold: if delta_E significant -> structure not compressible compatibly
    threshold = 0.05 * v0  # 5% drop as toy threshold
    flag = 1 if delta_E >= threshold else 0
    return {"v0": v0, "v1": v1, "delta_energy": delta_E, "reductibility_flag": flag}

def append_v2_to_csv(csv_path, extras_dict):
    # add columns to CSV, else create a new CSV with aggregated row
    import csv, os
    if os.path.exists(csv_path):
        # read all
        with open(csv_path, "r") as f:
            rows = list(csv.DictReader(f))
        # append one aggregate row
        agg = {"graph_id":"agg","nodes":"-","d_reg":"-","spectral_gap":""}
        agg.update({k:str(v) for k,v in extras_dict.items()})
        # write new with additional columns
        cols = list(rows[0].keys())
        for k in extras_dict.keys():
            if k not in cols: cols.append(k)
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows: w.writerow(r)
            w.writerow(agg)
    else:
        # create minimal CSV
        cols = ["graph_id","nodes","d_reg","spectral_gap","delta_energy","reductibility_flag"]
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            r = {"graph_id":"agg","nodes":"-","d_reg":"-","spectral_gap":""}
            for k in ["delta_energy","reductibility_flag"]:
                r[k] = str(extras_dict.get(k,""))
            w.writerow(r)

def main_v2_patch(outdir, seed):
    import json, os, random
    rng = random.Random(seed)
    # use numpy RNG seeded as well
    import numpy as np
    np.random.seed(seed)
    res = run_v2_extras(outdir, np.random, samples=300, nbits=256)
    # manifest patch
    man_path = os.path.join(outdir, "manifest.json")
    if os.path.exists(man_path):
        with open(man_path, "r") as f: man = json.load(f)
    else:
        man = {"problem": "PneqNP", "outputs": []}
    man["v2_delta_energy"] = res["delta_energy"]
    man["v2_reductibility_flag"] = res["reductibility_flag"]
    with open(man_path, "w") as f:
        json.dump(man, f, indent=2)
    csv_path = os.path.join(outdir, "pneqnp_full_results.csv")
    append_v2_to_csv(csv_path, res)

