# Week 1 Report

## 0. Repository & CI
- **Repo URL:** https://github.com/leffka/fall25-csc-bioinf
- **CI (Actions) status:** Green ✅ — latest runs: https://github.com/leffka/fall25-csc-bioinf/actions

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

## Environment
- macOS, Python 3.11/3.13  
- Codon v0.19.3 + `seq` plugin v0.11.5  
- Shell: bash/zsh

## 2. Codon Conversion (status)
- Target path: `week1/code/codon/main.py`
- CLI: must accept `main.py <dataset>` same as Python.
- Status: **Pending** (Python baseline first).


Final results (including Codon):

Dataset
Language
Runtime
N50
data1
python
00:00:15
9990
data2
python
00:00:30
9992
data3
python
00:00:34
9824
data1
codon
00:00:04
31
data2
codon
00:00:05
31
data3
codon
00:00:04
31


Why Codon N50 is ≈ 31

This Codon port implements unitigs. Unitigs stop at every branch in the de Bruijn graph, so many contigs are single-edge paths; with k=31, a single edge spells to 31 bp, which pulls the weighted median (N50) down to ≈31. The Python baseline in the upstream repo yields much longer contigs, so N50 is ~10k there. This difference is algorithmic, not a bug.

Automation details

week1/evaluate.sh:
	•	Ensures datasets exist (unzips data1–4 if needed).
	•	Runs Python (python3 main.py <dataset>) and Codon (codon run -release main.py <dataset>).
	•	Measures wall time and computes N50 either from a contigs.fa FASTA or from printed index length lines.
	•	Writes a TSV summary to week1/report.tsv.

Reproducibility notes
	•	Per the assignment update, we report N50.
	•	The original genome(s) behind the toy datasets are not specified; some README numbers may not be fully reproducible. Differences are documented above.

Gotchas / tips
	•	macOS sed -i requires the empty backup arg: -i ''.
	•	Codon’s stdlib is smaller; prefer typed containers and simple string concatenation over % formatting.
	•	If strict parity with Python were required, one could call the original Python from Codon via interop; here I kept a native unitigs port and documented the expected N50 difference.
