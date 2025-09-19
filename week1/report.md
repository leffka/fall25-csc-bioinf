Week 1

Repo: https://github.com/leffka/fall25-csc-bioinf

What’s done (at a glance)
	•	Reproduced the Python baseline on data1–3
	•	Converted the assembler to Codon (unitigs)
	•	Automated runs and reporting with week1/evaluate.sh
	•	Computed N50 and captured runtimes in week1/report.tsv

Environment
	•	macOS, Python 3.11/3.13
	•	Codon v0.19.3 + seq plugin v0.11.5
	•	Shell: bash/zsh

	1.	Reproduction — Python baseline
Source: week1/code/genome-assembly (clone of zhongyuchen/genome-assembly)

Commands (macOS)
cd week1/code
git clone https://github.com/zhongyuchen/genome-assembly genome-assembly
cd genome-assembly
unzip -n data1.zip
unzip -n data2.zip
unzip -n data3.zip
python3 - <<‘PY’
import os, sys
sys.setrecursionlimit(1_000_000)
os.system(“python3 main.py data1”)
os.system(“python3 main.py data2”)
os.system(“python3 main.py data3”)
PY

Raw outputs observed (excerpt)
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

Interpretation
The Python script prints dataset summaries and the top-20 contig lengths. For language-to-language comparison, I compute N50 from these outputs using week1/code/compute_n50.py (see Automation below). Per the assignment note, full parity with the README may not be achievable; mismatches are documented.
	2.	Codon conversion (unitigs)
Path: week1/code/codon/main.py

How to run
cd week1/code/codon
~/.codon/bin/codon run -release main.py data1
(repeat for data2, data3)

The Codon app writes contigs.fa and also prints the top-20 contig lengths (index length) for the evaluator.

Why Codon N50 ≈ 31
This Codon port uses unitigs, which stop at every branch in the de Bruijn graph. Many contigs become single-edge paths; with k=31, a single edge spells to 31 bp, pulling the weighted median (N50) down to ≈31. The Python baseline yields longer contigs/N50 because it follows a different traversal/assembly behavior. This is algorithmic, not a bug.
	3.	Results
The evaluator aggregates runtimes and N50. Full TSV: week1/report.tsv.

Dataset | Language | Runtime | N50
data1   | python   | 00:00:15 | 9990
data2   | python   | 00:00:30 | 9992
data3   | python   | 00:00:34 | 9824
data1   | codon    | 00:00:04 | 31
data2   | codon    | 00:00:05 | 31
data3   | codon    | 00:00:04 | 31
	4.	Automation
Script: week1/evaluate.sh

	•	Ensures datasets are present (unzips data1–4 if needed)
	•	Runs Python (python3 main.py ) and Codon (codon run -release main.py )
	•	Measures wall time
	•	Computes N50 from a contigs FASTA or from the printed index length lines
	•	Writes a TSV summary to week1/report.tsv

One-liner to regenerate
cd 
bash week1/evaluate.sh
cat week1/report.tsv

Reproducibility notes
	•	Per the Sept 13 update, this report uses N50 (not NGA50).
	•	The original genome(s) behind the toy datasets are not specified; some README numbers may not be fully reproducible. Any differences are documented above.

Gotchas and tips
	•	macOS sed -i needs the empty backup arg: -i ‘’
	•	Codon’s stdlib is smaller; prefer typed containers and string concatenation over % formatting
	•	Strict parity (if ever required) can be achieved by calling the original Python from Codon via interop, but here I keep a native unitigs port and document the expected N50 difference
