#!/usr/bin/env bash
set -euxo pipefail

# Configuration
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
WORK_DIR="${ROOT_DIR}/code/work"
PY_IMPL_DIR="${ROOT_DIR}/code/genome-assembly"   # cloned upstream at runtime
CODON_IMPL_DIR="${ROOT_DIR}/code/codon"          # your converted code lives here
RESULTS_TSV="${ROOT_DIR}/week1/report.tsv"       # <-- write inside week1 now
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
  local cand
  cand="$(ls -t ${dir}/*.{fa,fasta,fna,txt} 2>/dev/null | head -n1 || true)"
  if [ -n "${cand:-}" ]; then
    echo "$cand"
  else
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
    CMD=(~/.codon/bin/codon run -release main.py "${DATA}")
  fi

  pushd "${IMPL_DIR}"
  RUNTIME="$(/usr/bin/time -f '%E' -o .rt.tmp "${CMD[@]}" 1>.run.out 2>.run.err || true; cat .rt.tmp)"

  CONTIGS=""
  if [ -d out ]; then
    CONTIGS="$(find_contigs_file out || true)"
  fi
  if [ -z "${CONTIGS:-}" ]; then
    CONTIGS="$(find_contigs_file . || true)"
  fi
  if [ -z "${CONTIGS:-}" ]; then
    echo "WARN: could not find contigs file; deriving N50 from .run.out" >&2
    CONTIGS=".run.out"
  fi
  N50="$(python "${ROOT_DIR}/code/compute_n50.py" "${CONTIGS}")"
  popd

  printf '%s\t%s\t%s\t%s\n' "${DATA}" "${LANG}" "${RUNTIME}" "${N50}" >> "${RESULTS_TSV}"
}

# 4) Initialize results
printf '%s\n' "Dataset  Language  Runtime N50" > "${RESULTS_TSV}"
printf '%s\n' "--------------------------------------------------------------------------------" >> "${RESULTS_TSV}"

# Datasets to evaluate
DATASETS=("data1" "data2" "data3")

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

# 7) Show results path
echo "Results at: ${RESULTS_TSV}"