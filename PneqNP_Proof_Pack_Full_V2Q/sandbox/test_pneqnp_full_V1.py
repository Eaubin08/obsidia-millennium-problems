
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
