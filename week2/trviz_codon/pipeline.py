# week2/trviz_codon/pipeline.py

from typing import Dict, List, Tuple

# Import all our ported modules
from .decomposer import Decomposer
from .motif_encoder import MotifEncoder
from .motif_aligner import MotifAligner
from .utils import sort, add_padding, get_score_matrix

def run_pipeline(
    tr_id: str,
    sample_ids: List[str],
    tr_sequences: List[str],
    motifs: List[str],
    output_dir: str,
    rearrangement_method: str = 'clustering',
    skip_alignment: bool = False,
    verbose: bool = True
) -> Dict[str, object]:
    """
    A Codon-native pipeline for trviz data processing.
    This function performs decomposition, encoding, alignment, and sorting,
    then returns the processed data.
    """
    
    # Initialize our ported tools
    decomposer = Decomposer()
    motif_encoder = MotifEncoder()
    motif_aligner = MotifAligner()
    
    if verbose:
        print(f"ID: {tr_id}")
        print(f"Motifs: {motifs}")
        print(f"Loaded {len(tr_sequences)} tandem repeat sequences")
        print("1. Decomposing TR sequences...")

    # 1. Decomposition
    decomposed_trs: List[List[str]] = []
    for tr_sequence in tr_sequences:
        decomposed_trs.append(decomposer.decompose(tr_sequence, motifs))
    decomposed_trs = decomposer.refine(decomposed_trs)
    
    if verbose:
        print("2. Encoding sequences...")

    # 2. Encoding
    encoded_trs = motif_encoder.encode(decomposed_trs,
                                       motif_map_file=f"{output_dir}/{tr_id}_motif_map.txt",
                                       auto=True)
    
    # 3. Alignment
    aligned_trs: List[str]
    sorted_sample_ids: List[str]
    if skip_alignment:
        if verbose: print("3. Skipping alignment step.")
        aligned_trs = add_padding(encoded_trs)
        sorted_sample_ids = sample_ids
    else:
        if verbose: print("3. Aligning encoded motifs...")
        score_matrix = get_score_matrix(motif_encoder.symbol_to_motif)
        sorted_sample_ids, aligned_trs = motif_aligner.align(sample_ids,
                                                             encoded_trs,
                                                             tr_id,
                                                             score_matrix,
                                                             output_dir)
                                                             
    # 4. Re-arrangement (Sorting)
    if rearrangement_method != 'clustering' and rearrangement_method is not None:
        if verbose: print(f"4. Rearranging samples using '{rearrangement_method}' method...")
        sorted_sample_ids, aligned_trs = sort(aligned_trs,
                                              sorted_sample_ids,
                                              motif_encoder.symbol_to_motif,
                                              None, # sample_order_file
                                              rearrangement_method)

    print("Pipeline complete.")
    
    # 5. Return the processed data
    # The visualization step is skipped.
    return {
        "aligned_trs": aligned_trs,
        "sample_ids": sorted_sample_ids,
        "symbol_to_motif": motif_encoder.symbol_to_motif,
        "motif_counter": motif_encoder.motif_counter,
    }