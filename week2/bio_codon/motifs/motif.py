# week2/bio_codon/motifs/motif.py

from typing import Dict, List, Optional, Tuple, Union

# --- Codon-Only Imports ---
from python import numpy as np
Alignment = object
# --- End Imports ---

from . import matrix
from . import minimal

# Forward declaration for type hints
Motif = "Motif"

def parse(handle, fmt: str, strict: bool = True) -> List[Motif]:
    """Parse an output file from a motif finding program."""
    fmt = fmt.lower()
    if fmt == "minimal":
        return minimal.read(handle)
    else:
        raise ValueError(f"Unknown or unsupported format {fmt}")

def read(handle, fmt: str, strict: bool = True) -> Motif:
    """Read a motif from a handle using the specified file-format."""
    motifs = parse(handle, fmt, strict)
    if len(motifs) == 0:
        raise ValueError("No motifs found in handle")
    if len(motifs) > 1:
        raise ValueError("More than one motif found in handle")
    return motifs[0]

class Motif:
    """A class representing sequence motifs (Codon-compatible)."""
    # Class Preamble for Static Typing
    name: str
    alphabet: str
    length: Optional[int]
    alignment: Optional[Alignment]
    counts: Optional[matrix.FrequencyPositionMatrix]

    def __init__(self, alphabet: str = "ACGT", alignment: Optional[Alignment] = None, counts: Optional[Dict] = None):
        self.name = ""
        self.alphabet = alphabet

        if counts is not None and alignment is not None:
            raise ValueError("Specify either counts or an alignment, not both")
        elif counts is not None:
            self.alignment = None
            self.counts = matrix.FrequencyPositionMatrix(alphabet, counts)
            self.length = self.counts.length
        elif alignment is not None:
            self.alignment = alignment
            self.length = 0 # Simplified for Codon path
            self.counts = None
        else:
            self.counts = None
            self.alignment = None
            self.length = None

    def __len__(self) -> int:
        return self.length if self.length is not None else 0

    @property
    def consensus(self):
        if self.counts:
            return self.counts.consensus
        return None