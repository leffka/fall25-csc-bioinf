#!/bin/bash
set -euo pipefail

# evaluate.sh — run all benchmarks and print a concise runtime table

# Repo root for imports
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export REPO_ROOT="$SCRIPT_DIR"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

# --- helper: run a command, capture wall time in ms (stdout: integer ms)
run_and_time() {
  local cmd="$1"
  local start end elapsed
  start=$(python3 -c 'import time; print(int(time.time() * 1000))')
  bash -lc "$cmd" >/dev/null 2>&1
  end=$(python3 -c 'import time; print(int(time.time() * 1000))')
  elapsed=$((end - start))
  echo "$elapsed"
}

# Table rows accumulator (already formatted strings)
ROWS=()
add_row() { ROWS+=("$(printf "%-18s %-10s %s" "$1" "$2" "${3}ms")"); }

# Datasets
FASTA_FILES=("MT-human.fa" "MT-orange.fa")

# -----------------------------
# Compile Codon binaries (quiet)
# -----------------------------
SKIP_CODON=false
if ! command -v codon >/dev/null 2>&1; then
  SKIP_CODON=true
else
  # Single-record FASTA drivers (argv[1] = fasta filename)
  cat > local_align_fasta_test.codon << 'EOF'
from local_align import local_align
import sys
def read_fasta(filename: str) -> str:
    s: list[str] = []
    with open(filename, 'r') as f:
        for line in f:
            t = line.strip()
            if not t or t.startswith('>'): continue
            s.append(t.upper())
    return ''.join(s)
def sequence_to_integers(seq: str) -> list[int]:
    r: list[int] = []
    for b in seq:
        if b=='A': r.append(0)
        elif b=='C': r.append(1)
        elif b=='G': r.append(2)
        elif b=='T': r.append(3)
        else: r.append(0)
    return r
fn: str = sys.argv[1] if len(sys.argv) > 1 else "MT-human.fa"
seq = sequence_to_integers(read_fasta(fn))
qs,ql,ts,tl = 100,500,300,600
query = seq[qs:qs+ql]
target = seq[ts:ts+tl]
mat: list[int] = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = local_align(query, target, mat, 5, 1)
EOF

  cat > global_align_fasta_test.codon << 'EOF'
from global_align import global_align
import sys
def read_fasta(filename: str) -> str:
    s: list[str] = []
    with open(filename, 'r') as f:
        for line in f:
            t = line.strip()
            if not t or t.startswith('>'): continue
            s.append(t.upper())
    return ''.join(s)
def sequence_to_integers(seq: str) -> list[int]:
    r: list[int] = []
    for b in seq:
        if b=='A': r.append(0)
        elif b=='C': r.append(1)
        elif b=='G': r.append(2)
        elif b=='T': r.append(3)
        else: r.append(0)
    return r
fn: str = sys.argv[1] if len(sys.argv) > 1 else "MT-human.fa"
seq = sequence_to_integers(read_fasta(fn))
qs,ql,ts,tl = 100,500,300,600
query = seq[qs:qs+ql]
target = seq[ts:ts+tl]
mat: list[int] = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = global_align(query, target, mat, 5, 1)
EOF

  cat > semiglobal_align_fasta_test.codon << 'EOF'
from semiglobal_align import semiglobal_align
import sys
def read_fasta(filename: str) -> str:
    s: list[str] = []
    with open(filename, 'r') as f:
        for line in f:
            t = line.strip()
            if not t or t.startswith('>'): continue
            s.append(t.upper())
    return ''.join(s)
def sequence_to_integers(seq: str) -> list[int]:
    r: list[int] = []
    for b in seq:
        if b=='A': r.append(0)
        elif b=='C': r.append(1)
        elif b=='G': r.append(2)
        elif b=='T': r.append(3)
        else: r.append(0)
    return r
fn: str = sys.argv[1] if len(sys.argv) > 1 else "MT-human.fa"
seq = sequence_to_integers(read_fasta(fn))
qs,ql,ts,tl = 100,500,300,600
query = seq[qs:qs+ql]
target = seq[ts:ts+tl]
mat: list[int] = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = semiglobal_align(query, target, mat, 5, 1)
EOF

  cat > affine_global_align_fasta_test.codon << 'EOF'
from affine_global_align import affine_global_align
import sys
def read_fasta(filename: str) -> str:
    s: list[str] = []
    with open(filename, 'r') as f:
        for line in f:
            t = line.strip()
            if not t or t.startswith('>'): continue
            s.append(t.upper())
    return ''.join(s)
def sequence_to_integers(seq: str) -> list[int]:
    r: list[int] = []
    for b in seq:
        if b=='A': r.append(0)
        elif b=='C': r.append(1)
        elif b=='G': r.append(2)
        elif b=='T': r.append(3)
        else: r.append(0)
    return r
fn: str = sys.argv[1] if len(sys.argv) > 1 else "MT-human.fa"
seq = sequence_to_integers(read_fasta(fn))
qs,ql,ts,tl = 100,500,300,600
query = seq[qs:qs+ql]
target = seq[ts:ts+tl]
mat: list[int] = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = affine_global_align(query, target, mat, 5, 1)
EOF

  # ------- Codon pair drivers (qfile, tfile, qid, tid) -------
  CODON_PAIR_HELPERS='
def get_record(filename: str, rid: str) -> str:
    seq: list[str] = []
    take: bool = False
    with open(filename, "r") as f:
        for raw in f:
            line: str = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                curr_id: str = line[1:].strip().split()[0]
                take = (curr_id == rid)
            else:
                if take:
                    seq.append(line.upper())
    return "".join(seq)

def seq_to_ints(s: str) -> list[int]:
    r: list[int] = []
    for b in s:
        if b=="A": r.append(0)
        elif b=="C": r.append(1)
        elif b=="G": r.append(2)
        elif b=="T": r.append(3)
        else: r.append(0)
    return r

import sys
if len(sys.argv) < 5:
    print("usage: <qfile> <tfile> <qid> <tid>")
    sys.exit(1)
qfile: str = sys.argv[1]
tfile: str = sys.argv[2]
qid: str = sys.argv[3]
tid: str = sys.argv[4]
qseq = seq_to_ints(get_record(qfile, qid))
tseq = seq_to_ints(get_record(tfile, tid))
mat: list[int] = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
'

  cat > pair_global_qt.codon << EOF
from global_align import global_align
$CODON_PAIR_HELPERS
_ = global_align(qseq, tseq, mat, 5, 1)
EOF

  cat > pair_local_qt.codon << EOF
from local_align import local_align
$CODON_PAIR_HELPERS
_ = local_align(qseq, tseq, mat, 5, 1)
EOF

  cat > pair_semiglobal_qt.codon << EOF
from semiglobal_align import semiglobal_align
$CODON_PAIR_HELPERS
_ = semiglobal_align(qseq, tseq, mat, 5, 1)
EOF

  cat > pair_affine_qt.codon << EOF
from affine_global_align import affine_global_align
$CODON_PAIR_HELPERS
_ = affine_global_align(qseq, tseq, mat, 5, 1)
EOF

  # Build quietly
  codon build local_align_fasta_test.codon -o local_align_fasta_test >/dev/null 2>&1
  codon build global_align_fasta_test.codon -o global_align_fasta_test >/dev/null 2>&1
  codon build semiglobal_align_fasta_test.codon -o semiglobal_align_fasta_test >/dev/null 2>&1
  codon build affine_global_align_fasta_test.codon -o affine_global_align_fasta_test >/dev/null 2>&1

  codon build pair_global_qt.codon -o pair_global_qt >/dev/null 2>&1
  codon build pair_local_qt.codon -o pair_local_qt >/dev/null 2>&1
  codon build pair_semiglobal_qt.codon -o pair_semiglobal_qt >/dev/null 2>&1
  codon build pair_affine_qt.codon -o pair_affine_qt >/dev/null 2>&1

  # Fix OMP path if available (quiet)
  if command -v install_name_tool >/dev/null 2>&1; then
    for b in local_align_fasta_test global_align_fasta_test semiglobal_align_fasta_test affine_global_align_fasta_test \
             pair_global_qt pair_local_qt pair_semiglobal_qt pair_affine_qt; do
      install_name_tool -change @loader_path/libomp.dylib /opt/homebrew/opt/libomp/lib/libomp.dylib "./$b" >/dev/null 2>&1 || true
    done
  fi
fi

# ---------------------------------
# Python tiny runners (inline code)
# ---------------------------------
PY_LOCAL_CODE=$(cat <<'PY'
import os
from fasta_reader import read_fasta, sequence_to_integers, get_subsequences
from local_align import local_align
fname = os.environ.get('FASTA_FILE', 'MT-human.fa')
seq = sequence_to_integers(read_fasta(fname))
query, target = get_subsequences(seq, 100, 500, 300, 600)
mat = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = local_align(query, target, mat, 5, 1)
PY
)

PY_GLOBAL_CODE=$(cat <<'PY'
import os
from fasta_reader import read_fasta, sequence_to_integers, get_subsequences
from global_align import global_align
fname = os.environ.get('FASTA_FILE', 'MT-human.fa')
seq = sequence_to_integers(read_fasta(fname))
query, target = get_subsequences(seq, 100, 500, 300, 600)
mat = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = global_align(query, target, mat, 5, 1)
PY
)

PY_SEMIGLOBAL_CODE=$(cat <<'PY'
import os
from fasta_reader import read_fasta, sequence_to_integers, get_subsequences
from semiglobal_align import semiglobal_align
fname = os.environ.get('FASTA_FILE', 'MT-human.fa')
seq = sequence_to_integers(read_fasta(fname))
query, target = get_subsequences(seq, 100, 500, 300, 600)
mat = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = semiglobal_align(query, target, mat, 5, 1)
PY
)

PY_AFFINE_CODE=$(cat <<'PY'
import os
from fasta_reader import read_fasta, sequence_to_integers, get_subsequences
from affine_global_align import affine_global_align
fname = os.environ.get('FASTA_FILE', 'MT-human.fa')
seq = sequence_to_integers(read_fasta(fname))
query, target = get_subsequences(seq, 100, 500, 300, 600)
mat = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
_ = affine_global_align(query, target, mat, 5, 1)
PY
)

# ---------------------------------
# Run per-FASTA (Python + Codon)
# ---------------------------------
for FASTA in "${FASTA_FILES[@]}"; do
  [ -f "$FASTA" ] || continue
  dataset=$(basename "$FASTA" .fa | tr '[:upper:]' '[:lower:]' | tr '-' '_')

  # Python
  t=$(run_and_time "FASTA_FILE='$FASTA' python3 - <<'PY'$'\n'$PY_GLOBAL_CODE$'\n'PY");       add_row "global-$dataset"     "python" "$t"
  t=$(run_and_time "FASTA_FILE='$FASTA' python3 - <<'PY'$'\n'$PY_LOCAL_CODE$'\n'PY");        add_row "local-$dataset"      "python" "$t"
  t=$(run_and_time "FASTA_FILE='$FASTA' python3 - <<'PY'$'\n'$PY_SEMIGLOBAL_CODE$'\n'PY");   add_row "semiglobal-$dataset" "python" "$t"
  t=$(run_and_time "FASTA_FILE='$FASTA' python3 - <<'PY'$'\n'$PY_AFFINE_CODE$'\n'PY");       add_row "affine-$dataset"     "python" "$t"

  # Codon
  if [ "$SKIP_CODON" = false ]; then
    t=$(run_and_time "./global_align_fasta_test '$FASTA'");        add_row "global-$dataset"     "codon" "$t"
    t=$(run_and_time "./local_align_fasta_test '$FASTA'");         add_row "local-$dataset"      "codon" "$t"
    t=$(run_and_time "./semiglobal_align_fasta_test '$FASTA'");    add_row "semiglobal-$dataset" "codon" "$t"
    t=$(run_and_time "./affine_global_align_fasta_test '$FASTA'"); add_row "affine-$dataset"     "codon" "$t"
  fi
done

# ---------------------------------
# Pair tests q1..q5 vs t1..t5 (Python + Codon)
# ---------------------------------
if [ -f "q1.fa" ] && [ -f "t1.fa" ]; then
  # Python pair runner (reuses fasta_reader.read_fasta_records)
  cat > /tmp/pair_runner.py << 'PYEOF'
import os, sys
from fasta_reader import read_fasta_records, sequence_to_integers
alg, qi, ti = sys.argv[1], sys.argv[2], sys.argv[3]
qfile = os.environ.get('QFILE', 'q1.fa')
tfile = os.environ.get('TFILE', 't1.fa')
qd = read_fasta_records(qfile); td = read_fasta_records(tfile)
qseq = sequence_to_integers(qd[qi]); tseq = sequence_to_integers(td[ti])
mat = [2,-1,-1,-1,-1,2,-1,-1,-1,-1,2,-1,-1,-1,-1,2]
if alg=="global":
    from global_align import global_align; global_align(qseq, tseq, mat, 5, 1)
elif alg=="local":
    from local_align import local_align; local_align(qseq, tseq, mat, 5, 1)
elif alg=="semiglobal":
    from semiglobal_align import semiglobal_align; semiglobal_align(qseq, tseq, mat, 5, 1)
elif alg=="affine":
    from affine_global_align import affine_global_align; affine_global_align(qseq, tseq, mat, 5, 1)
else:
    raise SystemExit("unknown alg")
PYEOF

  for i in 1 2 3 4 5; do
    # Python rows
    t=$(run_and_time "QFILE='q1.fa' TFILE='t1.fa' python3 /tmp/pair_runner.py global q${i} t${i}");     add_row "global-q${i}"     "python" "$t"
    t=$(run_and_time "QFILE='q1.fa' TFILE='t1.fa' python3 /tmp/pair_runner.py local q${i} t${i}");      add_row "local-q${i}"      "python" "$t"
    t=$(run_and_time "QFILE='q1.fa' TFILE='t1.fa' python3 /tmp/pair_runner.py semiglobal q${i} t${i}"); add_row "semiglobal-q${i}" "python" "$t"
    t=$(run_and_time "QFILE='q1.fa' TFILE='t1.fa' python3 /tmp/pair_runner.py affine q${i} t${i}");     add_row "affine-q${i}"     "python" "$t"

    # Codon rows
    if [ "$SKIP_CODON" = false ]; then
      t=$(run_and_time "./pair_global_qt q1.fa t1.fa q${i} t${i}");     add_row "global-q${i}"     "codon" "$t"
      t=$(run_and_time "./pair_local_qt q1.fa t1.fa q${i} t${i}");      add_row "local-q${i}"      "codon" "$t"
      t=$(run_and_time "./pair_semiglobal_qt q1.fa t1.fa q${i} t${i}"); add_row "semiglobal-q${i}" "codon" "$t"
      t=$(run_and_time "./pair_affine_qt q1.fa t1.fa q${i} t${i}");     add_row "affine-q${i}"     "codon" "$t"
    fi
  done
fi

# --------
# Output (fixed-width "old style")
# --------
printf "%-18s %-10s %s\n" "Method" "Language" "Runtime"
printf "%s\n" "--------------------------------------"
for r in "${ROWS[@]}"; do
  echo "$r"
done

# Cleanup (quiet)
rm -f /tmp/pair_runner.py 2>/dev/null || true
rm -f local_align_fasta_test.codon global_align_fasta_test.codon semiglobal_align_fasta_test.codon affine_global_align_fasta_test.codon 2>/dev/null || true
rm -f pair_global_qt.codon pair_local_qt.codon pair_semiglobal_qt.codon pair_affine_qt.codon 2>/dev/null || true
if [ "$SKIP_CODON" = false ]; then
  rm -f local_align_fasta_test global_align_fasta_test semiglobal_align_fasta_test affine_global_align_fasta_test 2>/dev/null || true
  rm -f pair_global_qt pair_local_qt pair_semiglobal_qt pair_affine_qt 2>/dev/null || true
fi