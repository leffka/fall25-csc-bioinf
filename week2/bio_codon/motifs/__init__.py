# week2/bio_codon/motifs/__init__.py

from typing import Optional, Dict, List

# Use the special import syntax for your Codon version
from python import Bio.Align as Align
from python import Bio.Seq as Seq
import numpy as np

# Import the sibling matrix.py file
from . import matrix

# Forward declaration for the Motif class type hint
Motif = "Motif"

def create(instances: List[str], alphabet: str = "ACGT") -> Motif:
    """Create a Motif object from a list of sequences."""
    alignment = Align.Alignment(instances)
    return Motif(alphabet=alphabet, alignment=alignment)

class Motif:
    """A class representing sequence motifs (Codon-compatible)."""
    name: str
    counts: Optional[matrix.FrequencyPositionMatrix]
    length: Optional[int]
    alignment: Optional[pyobj] # Use pyobj for Python objects
    alphabet: str

    def __init__(self, alphabet: str = "ACGT", alignment: Optional[pyobj] = None, counts: Optional[Dict[str, List[float]]] = None):
        self.name = ""
        self.alphabet = alphabet

        if counts is not None and alignment is not None:
            raise ValueError("Specify either counts or an alignment, not both")
        elif counts is not None:
            self.alignment = None
            self.counts = matrix.FrequencyPositionMatrix(alphabet=alphabet, values=counts)
            self.length = self.counts.length
        elif alignment is not None:
            self.alignment = alignment
            self.length = alignment.length
            frequencies: Dict[str, List[float]] = {}
            # Iterate over the pyobj to get its data
            for letter in alphabet:
                if letter not in alignment.frequencies:
                    frequencies[letter] = [0.0 for _ in range(self.length)]
                else:
                    frequencies[letter] = [float(val) for val in alignment.frequencies[letter]]
            self.counts = matrix.FrequencyPositionMatrix(alphabet, frequencies)
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