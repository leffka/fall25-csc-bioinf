# Week 1 Report

## 0. Repository & CI
- **Repo URL:** https://github.com/leffka/fall25-csc-bioinf
- **CI (Actions) status:** Green ✅ — latest runs: https://github.com/leffka/fall25-csc-bioinf/actions
- **Submission commit:** `<fill after final push>`

## 1. Reproduction (Python baseline)
**Source:** `zhongyuchen/genome-assembly` (under `week1/code/genome-assembly/`).  
**Commands executed (macOS):**
```bash
cd week1/code
git clone https://github.com/zhongyuchen/genome-assembly genome-assembly
cd genome-assembly
unzip data1.zip
unzip data2.zip
unzip data3.zip

python3 - <<'PY'
import sys, os
sys.setrecursionlimit(1_000_000)
os.system("python3 main.py data1")
os.system("python3 main.py data2")
os.system("python3 main.py data3")
PY
```
**Raw outputs observed (excerpt):**
```
short_1.fasta 8500 100
short_2.fasta 8500 100
long.fasta 250 1000
0 15650
1 9997
2 9997
3 9990
4 9990
5 9956
6 9956
7 4615
8 3277
9 828
10 684
11 669
12 669
13 666
14 666
15 655
16 654
17 639
18 639
19 636
short_1.fasta 5000 100
short_2.fasta 5000 100
long.fasta 500 1000
0 15744
1 10013
2 10013
3 9992
4 9992
5 9992
6 5752
7 5171
8 4664
9 3309
10 1009
11 938
12 829
13 733
14 654
15 652
16 652
17 652
18 652
19 652
short_1.fasta 2500 100
short_2.fasta 2500 100
long.fasta 500 1000
0 9824
1 9824
2 9824
3 9824
4 9824
5 9824
6 9824
7 9824
8 3656
9 3656
10 3592
11 3592
12 2604
13 1848
14 1654
15 1517
16 1431
17 1408
18 1352
19 1239
```
**Interpretation:** These are dataset summaries/lengths from the Python assembler. To compare across languages, I compute **N50** from the produced contigs using `week1/code/compute_n50.py` (see next section).

**Match to README table?** Not directly from raw logs. Per assignment update, full reproduction may not be achievable; any mismatches are documented.

## 2. Codon Conversion (status)
- Target path: `week1/code/codon/main.py`
- CLI: must accept `main.py <dataset>` same as Python.
- Status: **Pending** (Python baseline first).

## 3. Automated Evaluation
Run:
```bash
bash week1/evaluate.sh
cat week1/report.tsv
```
This creates:
```
Dataset	Language	Runtime	N50
------------------------------------------------------------
data1	python	<mm:ss>	<value>
data2	python	<mm:ss>	<value>
data3	python	<mm:ss>	<value>
# ... codon rows appear once Codon port exists
```
I will commit `week1/report.tsv` after running the evaluator.

## 4. Reproducibility Notes
- **Python:** `python3 --version` → `<fill>`
- **Codon:** `codon --version` → `<fill>`
- **OS/CPU:** `uname -a` → `<fill>`
- Upstream may be non-reproducible as-is (data/seed ambiguity). This report records exact steps and versions; discrepancies are expected per instructor’s note.

## 5. Bonus (WIP)
- Plan: BLAST assembled contigs to infer the origin of data1…data4 and report top hits.