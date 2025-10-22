# Gotchas / pitfalls
## 1: Record IDs must match exactly
Pair tests assume q1.fa has >q1..>q5 and t1.fa has >t1..>t5. Any mismatch (e.g., >q01) will silently yield empty sequences → meaningless timings.
## 2: Ambiguous bases are coerced to A
sequence_to_integers maps only A/C/G/T. Everything else (N, gaps, lowercase, etc.) becomes A (0). That’s fine for timing, but can skew alignment scores if you later validate correctness.
## 3: Matrix indexing is row-major
Scoring matrix is a flattened 4×4 [AA, AC, AG, AT, CA, CC, …, TT]. Index used is mat[a*4 + b]. Swapping order will corrupt scores.
## 4: Terminal gap conventions differ by method
	•	Global: penalizes terminal gaps.
	•	Semi-global: typically free gaps at one/both ends (your semiglobal_align is used for that).
	•	Local: resets negative paths to 0 (Smith–Waterman).
Mixing expectations can make outputs look “wrong” even if the code is fine.
## 5: Timing = wall-clock of a subprocess
run_and_time spawns a fresh process per run; first run may include import/initialization overhead. It’s great for apples-to-apples across entries, but not microbenchmarks.
## 6: Codon toolchain specifics
	•	On macOS you may need libomp and the install_name_tool path fix. The script guards the command, but if your OMP path is non-standard, Codon binaries may fail to start.
	•	On Linux (CI), install_name_tool doesn’t exist; the guard prevents errors.
## 7: PYTHONPATH precedence
evaluate.sh prepends repo root to PYTHONPATH, so your local modules (e.g., fasta_reader.py) shadow any site packages. If you move files, keep this invariant.
## 8: Slicing assumes long genomes
For MT-*.fa the script slices [100:600] and [300:900]. Shorter FASTAs will yield empty slices and misleading results.
## 9: Multi-record helpers vs single-record readers
	•	Whole-genome runs use read_fasta (concatenate all non-header lines).
	•	Pair runs use per-ID readers (read_fasta_records / Codon pair drivers). Mixing these up will mis-benchmark.
## 10: CI Codon/Python interop env
The workflow sets CODON_PYTHON via find_libpython. If your runner changes Python version, this value must match or Codon-Python interop fails.
## 11: Lower/uppercase
Readers uppercase sequences; headers are matched case-sensitively in pair tests.
## 12: Fixed-width table can misalign
We intentionally print with %-18s %-10s so long method names nudge columns. That’s expected.
