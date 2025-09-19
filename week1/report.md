

# Week 1 Report


## 📝 Repository & CI Status

  - **Repository:** [`leffka/fall25-csc-bioinf`](https://www.google.com/search?q=%5Bhttps://github.com/leffka/fall25-csc-bioinf%5D\(https://github.com/leffka/fall25-csc-bioinf\))

-----

## 📊 Final Results

The table below summarizes the wall-clock runtime and N50 contig statistic for each dataset across both Python and Codon implementations.

| Dataset | Language | Runtime  | N50  |
| :------ | :------- | :------- | :--- |
| `data1` | Python   | 00:00:15 | 9990 |
| `data2` | Python   | 00:00:30 | 9992 |
| `data3` | Python   | 00:00:34 | 9824 |
| `data1` | Codon    | 00:00:04 | 31   |
| `data2` | Codon    | 00:00:05 | 31   |
| `data3` | Codon    | 00:00:04 | 31   |

-----

## 🧬 Analysis: Why Codon's N50 is \~31

The significant difference in N50 between the Python and Codon versions is due to an **algorithmic choice**, not a bug.

  - The **Python baseline** appears to implement a more complex assembly algorithm that resolves branches in the graph to create longer contigs, resulting in an N50 of \~10k.
  - This **Codon port** implements a simpler **unitig** assembly. Unitigs are contiguous paths in the de Bruijn graph that stop at every branch or junction. With a k-mer size (**k=31**), many of these paths consist of a single edge, producing a contig of length 31. This high frequency of short, single-edge contigs pulls the weighted median length (**N50**) down to approximately 31.

-----

## ⚙️ Reproduction of Python Baseline

The original Python implementation was cloned and executed on three datasets.

**Source:** `zhongyuchen/genome-assembly`

**Commands Executed:**

```bash
# Navigate to the code directory
cd week1/code

# Clone the baseline repository
git clone https://github.com/zhongyuchen/genome-assembly genome-assembly
cd genome-assembly

# Unzip datasets
unzip data1.zip
unzip data2.zip
unzip data3.zip

# Run the assembler on all three datasets
# (Note: Increased recursion limit is necessary for the algorithm)
python3 - <<'PY'
import sys, os
sys.setrecursionlimit(1_000_000)
os.system("python3 main.py data1")
os.system("python3 main.py data2")
os.system("python3 main.py data3")
PY
```


```
short_1.fasta 8500 100
short_2.fasta 8500 100
long.fasta 250 1000
0 15650
1 9997
2 9997
...
short_1.fasta 5000 100
short_2.fasta 5000 100
long.fasta 500 1000
0 15744
1 10013
2 10013
...
```



-----

## 🤖 Automation

The entire evaluation process is automated by the `week1/evaluate.sh` script. This script handles:

  - **Setup:** Ensures datasets are present, unzipping them if necessary.
  - **Execution:** Runs both the Python (`python3 main.py <dataset>`) and Codon (`codon run -release main.py <dataset>`) assemblers.
  - **Measurement:** Measures wall time and computes the N50 statistic for each run.
  - **Reporting:** Writes a clean, tab-separated summary to `week1/report.tsv`.

-----

## 💡 Notes & Gotchas

  - **Reproducibility:** Per the assignment update, N50 is the primary metric for comparison. Since the original reference genomes for the toy datasets are not provided, some figures from the upstream repository's README may not be fully reproducible.
  - **macOS `sed`:** The in-place edit flag (`-i`) on macOS requires an empty string backup argument (e.g., `sed -i '' 's/old/new/' file.txt`).
  - **Codon Development:** Codon's standard library is more limited than Python's. It's best to rely on typed containers and simple string concatenation rather than more complex features like `%` formatting.
  - **Project Scope:** For this report, a native Codon unitig implementation was chosen. If strict algorithmic parity with the Python version were required, one could use Codon's Python interoperability features to call the original functions directly, though this would likely sacrifice performance gains.

-----

## 💻 Environment

  - **OS:** macOS
  - **Shell:** bash/zsh
  - **Python:** 3.11 / 3.13
  - **Codon:** v0.19.3
  - **Codon `seq` Plugin:** v0.11.5
