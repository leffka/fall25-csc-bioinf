# Single Codon-safe test suite for the current TRviz port.
# No pytest, no os.path.*. Uses simple assertions & prints.

from trviz.main import TandemRepeatVizWorker
from trviz.utils import get_sample_and_sequence_from_fasta
from trviz.decomposer import Decomposer
from trviz.motif_encoder import MotifEncoder

def exists(path: str) -> bool:
    try:
        f = open(path, "rb"); f.close()
        return True
    except:
        return False

def assert_eq(name, got, expected):
    if got != expected:
        raise AssertionError(f"{name} failed:\n  got     = {got!r}\n  expected= {expected!r}")
    print(f"✓ {name}")

# --------------------------
# 1) End-to-end workflow test (like smoke_test but distinct)
# --------------------------
def test_workflow():
    fasta = ">s1\nACCTTGACCTTGACCTTG\n>s2\nACCTTGACCTTG\n"
    with open("e2e.fasta", "w") as f:
        f.write(fasta)
    ids, seqs = get_sample_and_sequence_from_fasta("e2e.fasta")
    w = TandemRepeatVizWorker()
    w.generate_trplot("e2e", ids, seqs, ["ACCTTG"])  # matches current port

    # Files exist
    assert exists("e2e_motif_map.txt"), "missing e2e_motif_map.txt"
    assert exists("e2e_aligned.txt"), "missing e2e_aligned.txt"
    assert exists("e2e_trplot.png"), "missing e2e_trplot.png"
    assert exists("e2e_color_map.png"), "missing e2e_color_map.png"

    # Content spot checks
    with open("e2e_motif_map.txt") as f:
        mm = f.read().strip()
    assert_eq("motif_map content", mm, "ACCTTG\t!\t5")

    with open("e2e_aligned.txt") as f:
        aligned = f.read().strip()
    expected_aligned = ">s1\n!!!\n>s2\n!!-"
    assert_eq("aligned content", aligned, expected_aligned)

# --------------------------
# 2) Decomposer tests (greedy, longest-first)
# --------------------------
def test_decomposer_basic():
    d = Decomposer()
    # exact repeats
    got = d.decompose("ACTACTACT", ["ACT"])
    assert_eq("decompose exact repeats", got, ["ACT","ACT","ACT"])

    # leftover when not divisible
    got = d.decompose("AAAAAAAAAAAAAA", ["AAAAAA","AAA"])  # 14 A's -> 2*6 + leftover 'AA'
    assert_eq("decompose leftover", got, ["AAAAAA","AAAAAA","AA"])

    # choose longest first
    got = d.decompose("ABCABCAB", ["ABC","AB"])  # 'ABC','ABC','AB'
    assert_eq("decompose longest-first", got, ["ABC","ABC","AB"])

    # mixed motifs
    got = d.decompose("ACCTTGACCTTGAC", ["ACCTTG","AC"])  # 'ACCTTG','ACCTTG','AC'
    assert_eq("decompose mixed", got, ["ACCTTG","ACCTTG","AC"])

def test_decomposer_edge_cases():
    d = Decomposer()
    # no motif matches at start -> whole sequence becomes leftover once
    got = d.decompose("XYZ", ["AC"])  # no prefix match -> leftover
    assert_eq("no match becomes leftover", got, ["XYZ"])

    # overlapping-type scenario; longest wins
    got = d.decompose("CGCCGG", ["CGG","CGC"])  # 'CGC','CGG'
    assert_eq("overlap longest-first", got, ["CGC","CGG"])

# --------------------------
# 3) Encoder tests (symbol assignment & private grouping behavior)
# --------------------------
def test_encoder_mapping():
    d = Decomposer()
    e = MotifEncoder()
    seqs = [
        d.decompose("ACCTTGACCTTG", ["ACCTTG"]),                # 2 x motif
        d.decompose("ACCTTGACCTTGACCTTG", ["ACCTTG"]),         # 3 x motif
        d.decompose("ACCTTG", ["ACCTTG"])                      # 1 x motif
    ]
    encoded, symmap = e.encode(seqs, "enc_motif_map.txt", label_count=90, auto=True)
    # Only one motif => one symbol
    symbols = sorted(set(symmap.values()))
    assert_eq("encoder single motif symbol", symbols, [symbols[0]])
    # Encoded strings should be of the same lengths as decomposed counts
    lengths_ok = [len(enc) for enc in encoded] == [2,3,1]
    assert_eq("encoder lengths", lengths_ok, True)

def test_encoder_private_grouping():
    d = Decomposer()
    e = MotifEncoder()
    # Create many rare motifs so grouping will be needed if label_count is small
    motifs = ["M1","M2","M3","M4","M5","M6","M7","M8","M9","M10"]
    seqs = [[m] for m in motifs]  # each appears once
    encoded, symmap = e.encode(seqs, "enc_small_map.txt", label_count=3, auto=True)
    # We expect <= 3 symbols in total due to label_count
    unique_symbols = sorted(set(symmap[m] for m in motifs))
    assert (len(unique_symbols) <= 3), f"too many symbols: {unique_symbols}"
    print("✓ encoder private grouping (symbol count <= 3)")

def main():
    test_workflow()
    test_decomposer_basic()
    test_decomposer_edge_cases()
    test_encoder_mapping()
    test_encoder_private_grouping()
    print("ALL TESTS PASSED")

if __name__ == "__main__":
    main()
