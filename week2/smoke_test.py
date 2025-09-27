# week2/smoke_test.py

from typing import Dict, List

# Import the classes from your ported Codon library
from trviz_codon.decomposer import Decomposer
from trviz_codon.motif_encoder import MotifEncoder
from trviz_codon.motif_aligner import MotifAligner

def test_decomposer():
    """Smoke test for the ported Decomposer class."""
    print("--- 1. Testing Decomposer ---")
    decomposer = Decomposer()
    tr_sequence = "ACCTTGACCTTGACCTTGACCTTG"
    motifs = ["ACCTTG"]
    
    # Call the ported decompose method
    decomposed_result = decomposer.decompose(tr_sequence, motifs)
    
    # Check if the output matches the example
    expected = ['ACCTTG', 'ACCTTG', 'ACCTTG', 'ACCTTG']
    assert decomposed_result == expected
    print("✓ Decomposer test passed!")

def test_encoder():
    """Smoke test for the ported MotifEncoder class."""
    print("\n--- 2. Testing MotifEncoder ---")
    motif_encoder = MotifEncoder()
    decomposed_vntrs = [
        ['ACCTTG', 'ACCTTG', 'ACCTTC'],
        ['ACCTTG', 'ACCTTG', 'ACCTTG', 'ACCTTC'],
        ['ACCTTG', 'ACCTTG', 'ACCTTG', 'ACCTTC', 'ACCTTC'],
    ]
    
    # Call the ported encode method
    encoded_result = motif_encoder.encode(decomposed_vntrs, motif_map_file="motif_map.txt")

    # Check if the output matches the example
    expected = ['aab', 'aaab', 'aaabb']
    assert encoded_result == expected
    print("✓ MotifEncoder test passed!")

def test_aligner():
    """Smoke test for the ported MotifAligner class."""
    print("\n--- 3. Testing MotifAligner ---")
    motif_aligner = MotifAligner()
    sample_ids = ['sample1', 'sample2', 'sample3']
    encoded_vntrs = ['aab', 'aaab', 'aaabb']

    # Call the ported align method
    # We pass an empty dict for score_matrix as it's optional for MAFFT
    sorted_ids, aligned_seqs = motif_aligner.align(
        sample_ids=sample_ids,
        encoded_vntrs=encoded_vntrs,
        vid='test_smoke',
        score_matrix={},
        output_dir='./'
    )

    # Check that the output has the correct structure
    assert len(sorted_ids) == 3
    assert len(aligned_seqs) == 3
    assert isinstance(aligned_seqs[0], str) # Check that it returned strings
    print("✓ MotifAligner test passed!")


def main():
    """Runs all smoke tests in sequence."""
    test_decomposer()
    test_encoder()
    test_aligner()
    print("\nAll smoke tests passed successfully! ✅")

# Run the main function
main()