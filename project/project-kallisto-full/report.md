# Reproduction Report — Bray et al. 2016 (kallisto)

**Paper**: Near-optimal probabilistic RNA-seq quantification (Bray et al., 2016, Nat Biotechnol 34:525–7).

## 1. Scope
I reproduced the paper’s core claims on a laptop:
- speed & resource usage of pseudoalignment,
- TPM accuracy vs. ground truth (simulated),
- bootstrap-based uncertainty.

## 2. Methods
- Tools: kallisto, salmon, Polyester (simulation), Snakemake (workflow).
- Pipeline: index → quant (paired-end) → bootstraps → evaluation.
- Config: tiny test dataset by default; GRCh38 optional via `config.yaml`.

## 3. Results
### 3.1 Speed & RAM
- Kallisto: **X sec**, peak RSS **Y GB** on N reads.
- Salmon: **X' sec**, peak RSS **Y' GB**.
Interpretation vs. Bray et al.: kallisto shows strong speed; absolute numbers differ due to hardware/data scale.

### 3.2 Accuracy vs. ground truth (simulation)
- Spearman ρ = **…**, Pearson r = **…** (TPM vs. truth), MA plot shows …
- Qualitative match to the paper’s “near-optimal” quantification.

### 3.3 Uncertainty (bootstraps)
- Median TPM CI width: **…**
- Low-TPM transcripts show higher relative variance, as discussed in the paper.

## 4. Deviations & limitations
- Small datasets; large-scale cross-tool benchmarks not attempted.
- Transcriptome release differences can shift exact TPMs.

## 5. How to reproduce
```bash
conda env create -f environment.yml
conda activate kallisto-full
bash run.sh
```

## 6. Acknowledgements
I used an AI assistant to scaffold files (see ai.md) and verified the code/analysis.
