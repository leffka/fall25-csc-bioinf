# Reproducing key results from Bray et al. 2016 (kallisto)

This repo replicates the *core* claims from Bray et al. 2016 (Nat Biotechnol 34:525–7):
1) Fast transcript quantification via pseudoalignment (speed/CPU/RAM).
2) Accurate TPM estimates (vs. ground truth via simulation).
3) Quantification uncertainty via bootstraps.

We implement:
- **A. Pipeline**: build transcript index, quantify paired-end reads.
- **B. Accuracy**: simulate reads with known TPMs (Polyester) → evaluate Spearman/Pearson + MA plots.
- **C. Speed/Memory**: wall time & peak RSS via `/usr/bin/time -v`, compare to Salmon.

By default we run on the **official kallisto tiny test dataset** for quick success; you can switch to GRCh38 + your SRA samples by editing `config.yaml`.

## Prerequisites

You need **Conda** (or Mamba) installed to manage dependencies.
If you don't have it, and you have Homebrew on macOS:
```bash
brew install --cask miniconda
conda init zsh
# Then restart your terminal
```

## Quick start (macOS Apple Silicon or Linux)

```bash
conda env create -f environment.yml
conda activate kallisto-full
bash run.sh
```

## Artifacts

- `ref/` (test transcripts or GRCh38 cDNA)
- `index/` (kallisto + salmon indices)
- `data/` (test reads or your reads)
- `quant/` (kallisto & salmon results)
- `results/accuracy_simulated/` (metrics + plots)
- `results/bootstrap/` (TPM summaries)
- `results/speed/` (timing logs)

## Switch to real data

Edit `config.yaml`:
1. set `use_test_data: false`
2. set `transcript_fasta_url` (e.g., GENCODE/Ensembl GRCh38 cDNA URL)
3. set your samples: read URLs or local paths.

Then rerun `bash run.sh`.

## Notes

- Everything is fetched on demand. Do not commit data/indices/results.
- Salmon is included for a lightweight runtime comparison.
- This is a small-scale reproduction of the paper’s claims.
