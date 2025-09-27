# week2/trviz_codon/decomposer.py

from typing import Dict, List, Set, Tuple

# Use the import syntax that works for your Codon version
import numpy as np

# Import our ported utils file
from . import utils

# --- Handle the optional Cython module ---
DP_MODULE = "DP"
decompose_cy = None
try:
    from python import trviz.cy.decompose as decompose_cython
    decompose_cy = decompose_cython.decompose_cy
    DP_MODULE = "DP_CY"
    print("Using Cython implementation for decomposition.")
except ImportError:
    print("Cython is not available. Using pure Codon implementation for decomposition.")

class Decomposer:
    """ Codon-compatible port of the Decomposer class. """
    mode: str

    def __init__(self, mode: str = DP_MODULE):
        if mode in ("DP_CY", "DP", "HMM"):
            self.mode = mode
        else:
            raise ValueError(f"{mode} is an invalid mode for the decomposer.")

    @staticmethod
    def refine(decomposed_trs: List[List[str]], verbose: bool = False) -> List[List[str]]:
        """ Refines decomposed TRs to remove redundant motifs. """
        motif_pair_counter: Dict[Tuple[str, str], int] = {}
        motif_pair_str_counter: Dict[str, int] = {}
        motif_pair_str_to_motif_pair: Dict[str, Set[Tuple[str, str]]] = {}

        # Count motif pairs
        for tr in decomposed_trs:
            for i in range(len(tr) - 1):
                first_motif, second_motif = tr[i], tr[i+1]
                motif_pair = (first_motif, second_motif)
                motif_pair_str = first_motif + second_motif
                motif_pair_counter[motif_pair] = motif_pair_counter.get(motif_pair, 0) + 1
                motif_pair_str_counter[motif_pair_str] = motif_pair_str_counter.get(motif_pair_str, 0) + 1
                if motif_pair_str not in motif_pair_str_to_motif_pair:
                    motif_pair_str_to_motif_pair[motif_pair_str] = set()
                motif_pair_str_to_motif_pair[motif_pair_str].add(motif_pair)

        refined_trs: List[List[str]] = []
        for tr in decomposed_trs:
            # (Original refinement logic would go here)
            refined_trs.append(tr)
        
        return refined_trs

    def decompose(self, sequence: str, motifs: List[str], **kwargs) -> List[str]:
        """ Decompose a sequence into motifs using the selected mode. """
        sequence = sequence.upper()
        motifs = [m.upper() for m in motifs]

        if not utils.is_valid_sequence(sequence):
            raise ValueError(f"Sequence has invalid characters: {sequence}")
        for motif in motifs:
            if not utils.is_valid_sequence(motif):
                raise ValueError(f"The motif has invalid characters: {motif}")

        if self.mode == "DP_CY" and decompose_cy is not None:
            return decompose_cy(sequence, motifs, kwargs)
        elif self.mode == "DP":
            return self._decompose_dp(sequence, motifs, **kwargs)
        else: # HMM mode
            return self._decompose_hmm(sequence, motifs, **kwargs)

    @staticmethod
    def _decompose_dp(sequence: str, motifs: List[str], **kwargs) -> List[str]:
        """ Decomposes a sequence using dynamic programming. """
        # ... (Implementation of DP, same as before) ...
        decomposed_motifs: List[str] = [] 
        return decomposed_motifs

    @staticmethod
    def _decompose_hmm(sequence: str, motifs: List[str], **kwargs) -> List[str]:
        """ Decomposes a sequence using a Hidden Markov Model. """
        from python import pomegranate
        model: pyobj = pomegranate.HiddenMarkovModel(name="RepeatFinderHMM")
        # ... (Implementation of HMM, same as before) ...
        visited_states = [] # Placeholder
        decomposed_motifs = utils.get_motifs_from_visited_states_and_region(visited_states, sequence)
        return decomposed_motifs