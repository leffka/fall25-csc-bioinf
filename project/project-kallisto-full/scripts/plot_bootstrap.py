#!/usr/bin/env python
import argparse, os, json
import pandas as pd

p = argparse.ArgumentParser()
p.add_argument("--runinfo", required=True)    # quant/.../run_info.json
p.add_argument("--abundance", required=True)  # abundance.tsv
p.add_argument("--outdir", required=True)
p.add_argument("--tag", default="summary")
a = p.parse_args()
os.makedirs(a.outdir, exist_ok=True)

with open(a.runinfo) as fh:
    info = json.load(fh)

df = pd.read_csv(a.abundance, sep="\t")
summary = pd.DataFrame({
    "tpms_median": [df["tpm"].median()],
    "tpms_mean": [df["tpm"].mean()],
    "n_tx": [len(df)],
    "bootstraps": [info.get("n_bootstrap", None)]
})
summary.to_csv(os.path.join(a.outdir, f"{a.tag}.tsv"), sep="\t", index=False)
print(summary.to_string(index=False))
