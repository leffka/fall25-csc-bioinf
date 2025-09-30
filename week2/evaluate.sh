#!/usr/bin/env bash
set -euxo pipefail

# Folder containing this script (…/week2)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "== Codon version =="
codon --version

# Make week2 modules visible to Codon↔Python interop (Pillow lives on PYTHONPATH too)
# Keep both in case you later move code under week2/code/
export PYTHONPATH="${PYTHONPATH:-}:$DIR:$DIR/trviz:$DIR/code"

# Best-effort: if CODON_PYTHON isn't set, try to auto-detect via find_libpython (if available)
if [ -z "${CODON_PYTHON:-}" ]; then
  if python3 -c "import importlib; importlib.import_module('find_libpython')" >/dev/null 2>&1; then
    export CODON_PYTHON="$(python3 - <<'PY'
import find_libpython
print(find_libpython.find_libpython())
PY
)"
  fi
fi

echo "== Running tests =="
codon run test.py

echo "== Done =="
