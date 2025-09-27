# week2/test.py

# Define a dummy decorator to handle @test in Python
def test(f):
    return f

# Check if we are running in Codon or standard Python
try:
    IS_CODON = __codon__
except NameError:
    IS_CODON = False

if IS_CODON:
    print("--- RUNNING CODON TESTS ---")
    from bio_codon.motifs import create
else:
    print("--- RUNNING PYTHON TESTS ---")
    from Bio.motifs import create

@test
def test_motif_creation():
    """Tests if the create() function works in both environments."""
    print("Testing Motif creation and length...")
    instances = ["GATTACA", "GATTACA", "GATTACA"]
    m = create(instances)
    assert len(m) == 7
    print("Test passed!")

# Run the test
test_motif_creation()