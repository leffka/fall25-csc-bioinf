# week2/trviz_codon/motif_aligner.py

from typing import Dict, List, Tuple
# Import Python's libraries for OS interaction and file parsing
from python import os
from python import shutil
from python import subprocess
from python import Bio.SeqIO as SeqIO

class MotifAligner:
    """
    A Codon-compatible port of the MotifAligner class.
    It wraps external command-line tools for multiple sequence alignment.
    """
    def align(self,
              sample_ids: List[str],
              encoded_vntrs: List[str],
              vid: str,
              score_matrix: Dict[str, Dict[str, float]],
              output_dir: str,
              tool: str = "mafft") -> Tuple[List[str], List[str]]:
        """ Dispatches to the correct alignment tool. """
        if tool == 'mafft':
            return self._align_motifs_with_mafft(sample_ids, encoded_vntrs, vid, score_matrix, output_dir)
        elif tool == 'star':
            return self._align_motifs_with_star(sample_ids, encoded_vntrs, vid, score_matrix, output_dir)
        else:
            raise ValueError(f"Tool '{tool}' is not a supported aligner in this port.")

    @staticmethod
    def load_aligned_trs(aln_output: str) -> Tuple[List[str], List[str]]:
        """ Loads aligned tandem repeats from a FASTA file using Bio.SeqIO. """
        aligned_trs: List[str] = []
        aligned_sample_ids: List[str] = []

        with open(aln_output, "r") as handle:
            # SeqIO.parse returns a Python iterator; each 'record' is a pyobj
            for record in SeqIO.parse(handle, "fasta"):
                aligned_sample_ids.append(str(record.id))
                aligned_trs.append(str(record.seq))

        if len(aligned_trs) == 0:
            raise ValueError(f"No aligned alleles found in {aln_output}")

        return aligned_sample_ids, aligned_trs

    def _align_motifs_with_mafft(self,
                                 sample_ids: List[str],
                                 labeled_vntrs: List[str],
                                 vid: str,
                                 score_matrix: Dict[str, Dict[str, float]],
                                 output_dir: str,
                                 preserve_order: bool = True) -> Tuple[List[str], List[str]]:
        """ Aligns motifs by calling the 'mafft' command-line tool. """
        if not shutil.which("mafft"):
            raise ValueError("MAFFT is not installed or not in your PATH.")

        aln_input = f"{output_dir}/{vid}_alignment_input.fa"
        aln_output = f"{output_dir}/{vid}_alignment_output.fa"

        # 1. Write unaligned sequences to a temporary FASTA file
        data = ""
        for i in range(len(sample_ids)):
            data += f">{sample_ids[i]}\n{labeled_vntrs[i]}\n"
        with open(aln_input, "w") as f:
            f.write(data)

        # 2. Construct and run the MAFFT command
        mafft_command = ["mafft", "--quiet", "--auto", aln_input]
        if preserve_order:
            mafft_command.append("--reorder") # Note: MAFFT reorders by default, this preserves input order
            
        print("Running MAFFT alignment...")
        with open(aln_output, "w") as f_out:
            # subprocess.run is imported from Python
            subprocess.run(mafft_command, stdout=f_out)
        print("MAFFT alignment complete.")
        
        if not os.path.exists(aln_output):
            raise FileNotFoundError("Error: MAFFT alignment failed to produce an output file.")

        # 3. Read the aligned FASTA file and return the result
        aligned_sample_ids, aligned_vntrs = self.load_aligned_trs(aln_output)
        
        # 4. Clean up
        os.remove(aln_input)

        return aligned_sample_ids, aligned_vntrs

    def _align_motifs_with_star(self,
                                sample_ids: List[str],
                                labeled_vntrs: List[str],
                                vid: str,
                                score_matrix: Dict[str, Dict[str, float]],
                                output_dir: str) -> Tuple[List[str], List[str]]:
        """
        Performs a center-star alignment. This pure algorithm is accelerated by Codon.
        """
        # For simplicity in this port, the center is the longest sequence
        center_index = 0
        max_len = 0
        for i in range(len(labeled_vntrs)):
            if len(labeled_vntrs[i]) > max_len:
                max_len = len(labeled_vntrs[i])
                center_index = i
        
        center_id = sample_ids[center_index]
        center_seq = labeled_vntrs[center_index]

        # The final multiple sequence alignment will be stored here
        msa: Dict[str, List[str]] = {center_id: list(center_seq)}
        
        # Align every other sequence to the center sequence
        for i in range(len(labeled_vntrs)):
            if i == center_index:
                continue

            # This is a simplified pairwise alignment for demonstration.
            # A full implementation would use a more advanced algorithm.
            # Here, we just add gaps to the shorter sequence.
            sample_id = sample_ids[i]
            sample_seq = labeled_vntrs[i]
            
            aligned_center = list(center_seq)
            aligned_sample = list(sample_seq)
            
            # Pad the shorter sequence with gaps
            while len(aligned_sample) < len(aligned_center):
                aligned_sample.append('-')
            
            msa[sample_id] = aligned_sample

        # Convert the dictionary-based MSA to sorted lists for the return value
        final_ids: List[str] = []
        final_seqs: List[str] = []
        for sample_id in sample_ids: # Preserve original order
            if sample_id in msa:
                final_ids.append(sample_id)
                final_seqs.append("".join(msa[sample_id]))
                
        return final_ids, final_seqs