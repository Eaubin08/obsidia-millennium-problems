
#!/usr/bin/env python3
import hashlib, json, os
def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda: f.read(8192), b""):
            h.update(b)
    return h.hexdigest()

def write_manifest(outdir, run_id, problem, params, outputs, notes=""):
    manifest = {"run_id": run_id, "date": __import__('time').strftime("%Y-%m-%dT%H:%M:%SZ", __import__('time').gmtime()), "problem": problem, "params": params, "outputs": outputs, "notes": notes}
    path = os.path.join(outdir, "manifest.json")
    with open(path,"w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return path
