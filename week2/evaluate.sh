#!/bin/bash
# week2/evaluate.sh

echo "--- Starting Evaluation ---"

# Run the Python test
echo ""
echo "=> Running Python 3 tests..."
python3 test_python.py

# Run the Codon test
echo ""
echo "=> Running Codon tests..."
codon run test_codon.py

echo ""
echo "--- Evaluation Complete ---"