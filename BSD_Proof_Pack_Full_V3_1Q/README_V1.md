# BSD Proof Pack — README V1

Contenu principal extrait du pack original. Ajoutés :
- `V15_L4_Theorem_BSD_V1.md` : L4 + Théorème final prêts à coller dans le document V15.
- README modifié pour indiquer la présence de la section manquante.

Sandbox :
- Lancer `bash run_all.sh` dans `sandbox/` pour générer CSV/PNG/manifest.
- Vérifier les hashes via `anti_attacks/falsifiability_bsd.md`.

Notes :
- Le document Clay‑ready (V15) n'était pas présent dans l'archive ; le fichier V15_L4_Theorem_BSD_V1.md complète cette absence.


**V2 update**: scripts V2 added (delta_energy for P≠NP; multi-curves high-precision for BSD) + fresh outputs in sandbox/.

**V3 update**: added `sandbox/test_bsd_full_V3.py` (uses Sage if available) to compute L(E,1), L'(E,1) and analytic rank for given labels. Produces `bsd_full_results_V3.csv`.

**V3.1 update**: Added strict Sage-only runner `test_bsd_full_V3_1.py` + `run_all_v3_1.sh`. This version fails fast if Sage is missing and produces `bsd_full_results_V3_1.csv`.