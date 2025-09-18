#!/usr/bin/env bash
set -euxo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
WORK_DIR="${ROOT_DIR}/code/work"
PY_IMPL_DIR="${ROOT_DIR}/code/genome-assembly"
CODON_IMPL_DIR="${ROOT_DIR}/code/codon"
RESULTS_TSV="${ROOT_DIR}/week1/report.tsv"
ZC_REPO="${ZC_REPO:-https://github.com/zhongyuchen/genome-assembly}"
ZC_REF="${ZC_REF:-master}"

mkdir -p "${WORK_DIR}"
pushd "${WORK_DIR}" >/dev/null

# Get Python path once and reuse it everywhere
PYTHON="$(command -v python3 >/dev/null 2>&1 && echo python3 || echo python)"

if [ ! -d "${PY_IMPL_DIR}" ]; then
  git clone --depth=1 --branch "${ZC_REF}" "${ZC_REPO}" "${PY_IMPL_DIR}"
fi

pushd "${PY_IMPL_DIR}"
for z in data1.zip data2.zip data3.zip data4.zip; do
  test -f "$z" && unzip -n "$z" || true
done
popd

find_contigs_fasta() {
  # Only return FASTA-like files (no arbitrary files)
  local dir="$1"
  ls -t ${dir}/*.{fa,fasta,fna} 2>/dev/null | head -n1 || true
}

fmt_hms() {
  local secs="$1"
  printf "%02d:%02d:%02d" $((secs/3600)) $(((secs%3600)/60)) $((secs%60))
}

run_with_timer() {
  local start end
  start="$(date +%s)"
  "$@" 1>.run.out 2>.run.err || true
  end="$(date +%s)"
  fmt_hms "$((end-start))"
}

run_one() {
  local DATA="$1" LANG="$2"
  local IMPL_DIR CMD CODON_BIN

  if [ "$LANG" = "python" ]; then
    IMPL_DIR="${PY_IMPL_DIR}"
    CMD=("${PYTHON}" main.py "${DATA}")
  else
    IMPL_DIR="${CODON_IMPL_DIR}"
    CODON_BIN="${HOME}/.codon/bin/codon"
    command -v codon >/dev/null 2>&1 && CODON_BIN="$(command -v codon)" || true
    CMD=("${CODON_BIN}" run -release main.py "${DATA}")
  fi

  pushd "${IMPL_DIR}"

  RUNTIME="$(run_with_timer "${CMD[@]}")"

  # Prefer a real FASTA in ./out or ./
  CONTIGS=""
  [ -d out ] && CONTIGS="$(find_contigs_fasta out || true)"
  [ -z "${CONTIGS}" ] && CONTIGS="$(find_contigs_fasta . || true)"
  # Fallback to stdout capture if no FASTA
  [ -z "${CONTIGS}" ] && CONTIGS=".run.out"

  N50="$("${PYTHON}" "${ROOT_DIR}/code/compute_n50.py" "${CONTIGS}")"
  popd

  printf '%s\t%s\t%s\t%s\n' "${DATA}" "${LANG}" "${RUNTIME}" "${N50}" >> "${RESULTS_TSV}"
}

printf '%s\n' "Dataset  Language  Runtime N50" > "${RESULTS_TSV}"
printf '%s\n' "--------------------------------------------------------------------------------" >> "${RESULTS_TSV}"

DATASETS=("data1" "data2" "data3")
for d in "${DATASETS[@]}"; do
  run_one "$d" "python"
done

if [ -f "${CODON_IMPL_DIR}/main.py" ]; then
  for d in "${DATASETS[@]}"; do
    run_one "$d" "codon"
  done
else
  echo "NOTE: Codon implementation not found at ${CODON_IMPL_DIR}/main.py; skipping Codon runs" >&2
fi

echo "Results at: ${RESULTS_TSV}"