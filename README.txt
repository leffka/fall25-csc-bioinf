This ZIP contains a Week 1 starter layout:

- `.github/workflows/actions.yml` — CI that installs Codon + seq plugin, then runs `week1/evaluate.sh`
- `week1/evaluate.sh` — orchestrates Python and Codon runs and computes N50
- `week1/code/compute_n50.py` — N50 calculator for FASTA or plain-text contigs
- `week1/ai.md` — AI disclosure template
- `week1/report.md` — report template

How to use:
1) Create your public repo `fall25-csc-bioinf` and copy these files into it.
2) Inside `week1/code/`, create two dirs:
   - `genome-assembly/` — clone the upstream Python repo here
   - `codon/` — your Codon port goes here (expose `main.py` compatible with `python main.py <dataset>`)
3) Push and check GitHub Actions → it should run `week1/evaluate.sh` and upload a summary.