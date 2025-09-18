#!/usr/bin/env bash
set -euxo pipefail

# Configuration
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
WORK_DIR="${ROOT_DIR}/code/work"
PY_IMPL_DIR="${ROOT_DIR}/code/genome-assembly"   # cloned upstream
CODON_IMPL_DIR="${ROOT_DIR}/code/codon"          # your converted code lives here
RESULTS_TSV="${ROOT_DIR}/report.tsv"
ZC_REPO="${ZC_REPO:-https://github.com/zhongyuchen/genome-assembly}"
ZC_REF="${ZC_REF:-master}"

mkdir -p "${WORK_DIR}"
pushd "${WORK_DIR}" >/dev/null

# 1) Clone upstream Python implementation if not present
if [ ! -d "${PY_IMPL_DIR}" ]; then
  git clone --depth=1 --branch "${ZC_REF}" "${ZC_REPO}" "${PY_IMPL_DIR}"
fi

# 2) Unzip datasets (the repo ships data1..data4 zips)
pushd "${PY_IMPL_DIR}"
for z in data1.zip data2.zip data3.zip data4.zip; do
  test -f "$z" && unzip -n "$z" || true
done
popd

# Helper to find a contigs-like file newly produced in a directory
find_contigs_file() {
  local dir="$1"
  # Prefer FASTA-like names, fallback to txt
  local cand
  cand="$(ls -t ${dir}/*.{fa,fasta,fna,txt} 2>/dev/null | head -n1 || true)"
  if [ -n "${cand:-}" ]; then
    echo "$cand"
  else
    # last modified file in dir
    ls -t "${dir}"/* 2>/dev/null | head -n1
  fi
}

# 3) Run one dataset with an implementation (python|codon)
run_one() {
  local DATA="$1"       # e.g. data1
  local LANG="$2"       # python or codon
  local IMPL_DIR
  local CMD
  if [ "$LANG" = "python" ]; then
    IMPL_DIR="${PY_IMPL_DIR}"
    CMD=(python main.py "${DATA}")
  else
    IMPL_DIR="${CODON_IMPL_DIR}"
    # your Codon main should accept same interface
    CMD=(~/.codon/bin/codon run -release main.py "${DATA}")
  fi

  pushd "${IMPL_DIR}"
  # Use /usr/bin/time for clean timing
  RUNTIME="$(/usr/bin/time -f '%E' -o .rt.tmp "${CMD[@]}" 1>.run.out 2>.run.err || true; cat .rt.tmp)"
  # Try to locate an output contigs file in impl dir or a ./out dir
  CONTIGS=""
  if [ -d out ]; then
    CONTIGS="$(find_contigs_file out || true)"
  fi
  if [ -z "${CONTIGS:-}" ]; then
    # heuristics: most recent FASTA-like file in impl dir
    CONTIGS="$(find_contigs_file . || true)"
  fi
  if [ -z "${CONTIGS:-}" ]; then
    # last resort: compute N50 from stdout (one contig per line expected)
    echo "WARN: could not find contigs file; deriving N50 from .run.out" >&2
    CONTIGS=".run.out"
  fi
  N50="$(python "${ROOT_DIR}/code/compute_n50.py" "${CONTIGS}")"
  popd

  # Emit a TSV row
  printf "%s\t%s\t%s\t%s\n" "${DATA}" "${LANG}" "${RUNTIME}" "${N50}" >> "${RESULTS_TSV}"
}

# 4) Initialize results
printf "Dataset\tLanguage\tRuntime\tN50\n" > "${RESULTS_TSV}"
printf "--------------------------------------------------------------------------------\n" >> "${RESULTS_TSV}"

# Datasets to evaluate
DATASETS=("data1" "data2" "data3") # data4 is much larger; add if your runner has RAM/time

# 5) Run Python impl
for d in "${DATASETS[@]}"; do
  run_one "$d" "python"
done

# 6) Run Codon impl (expects week1/code/codon/main.py to exist)
if [ -f "${CODON_IMPL_DIR}/main.py" ]; then
  for d in "${DATASETS[@]}"; do
    run_one "$d" "codon"
  done
else
  echo "NOTE: Codon implementation not found at ${CODON_IMPL_DIR}/main.py; skipping Codon runs" >&2
fi

# 7) Show results
cat "${RESULTS_TSV}"