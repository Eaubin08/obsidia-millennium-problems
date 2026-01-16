P ≠ NP — Obsidia Sandbox — Full Proof Pack (Autonomous)
===========================================

Contenu
-------
- sandbox/test_pneqnp_full.py : script complet (calculs, CSV/manifest, figures si applicables)
- sandbox/utils.py      : SHA256 + manifest helpers
- sandbox/run_all.sh    : lance automatiquement le script avec logs + outdir daté
- sandbox/data/         : sorties (créées au runtime)
- anti_attacks/falsifiability_pneqnp.md : checklist reproduisible pour tentative de réfutation rapide
- repro/environment.yml : dépendances Python (conda)
- repro/Dockerfile, repro/entrypoint.sh : exécution dans Docker

Exécution locale
----------------
conda env create -f repro/environment.yml -n obsidia_PneqNP_Proof_Pack_Full
conda activate obsidia_PneqNP_Proof_Pack_Full
bash sandbox/run_all.sh

Exécution Docker
----------------
docker build -t pneqnp_proof_pack_full -f repro/Dockerfile .
docker run --rm -v "$(pwd)/sandbox/data:/app/sandbox/data" pneqnp_proof_pack_full
