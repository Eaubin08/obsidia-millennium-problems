
# falsifiability_riemann.md
# Steps to reproduce and attempt refutation quickly
1) Setup env (conda or pip) using repro/environment.yml
2) Run riemann full script:
   python3 sandbox/test_riemann_full.py --outdir ./data/riemann_test --zeros 200 --lambdas 10,30,50 --kernels gauss,fejer,poisson --seed 42 --prec 80
3) Compare manifest and CSV hashes with provided witness. If differences, raise counterexample.
