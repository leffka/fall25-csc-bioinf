#!/usr/bin/env python
import argparse, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr

p = argparse.ArgumentParser()
p.add_argument("--truth", required=True)      # truth_tpm.tsv (transcript_id \t tpm_truth)
p.add_argument("--abundance", required=True)  # kallisto abundance.tsv
p.add_argument("--outdir", required=True)
a = p.parse_args()
os.makedirs(a.outdir, exist_ok=True)

truth = pd.read_csv(a.truth, sep="\t")
est = pd.read_csv(a.abundance, sep="\t")  # abundance.tsv: target_id length eff_length est_counts tpm

df = truth.merge(est[["target_id","tpm"]], left_on="transcript_id", right_on="target_id", how="left")
df["tpm"].fillna(0.0, inplace=True)
df.rename(columns={"tpm":"tpm_est"}, inplace=True)

rho_s, _ = spearmanr(df["tpm_truth"], df["tpm_est"])
rho_p, _ = pearsonr(df["tpm_truth"], df["tpm_est"])

metrics = pd.DataFrame([{"spearman": rho_s, "pearson": rho_p, "n": len(df)}])
metrics.to_csv(os.path.join(a.outdir, "metrics.tsv"), sep="\t", index=False)

# MA plot (log-scale)
eps = 1e-6
A = 0.5 * (np.log2(df["tpm_truth"]+eps) + np.log2(df["tpm_est"]+eps))
M = np.log2(df["tpm_est"]+eps) - np.log2(df["tpm_truth"]+eps)

plt.figure(figsize=(6,4))
plt.scatter(A, M, s=6, alpha=0.4)
plt.axhline(0, linestyle="--")
plt.xlabel("A = 0.5*(log2(T_true)+log2(T_est))")
plt.ylabel("M = log2(T_est) - log2(T_true)")
plt.title(f"MA plot (Spearman={rho_s:.3f}, Pearson={rho_p:.3f})")
plt.tight_layout()
plt.savefig(os.path.join(a.outdir, "ma_plot.png"), dpi=150)

print(metrics.to_string(index=False))
