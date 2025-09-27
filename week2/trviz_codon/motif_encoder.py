# week2/trviz_codon/motif_encoder.py

from typing import Dict, List, Tuple

# Import our newly ported utils file
from . import utils

class MotifEncoder:
    """A Codon-compatible port of the MotifEncoder class."""
    
    # Class preamble to define types for all attributes
    private_motif_threshold: int
    symbol_to_motif: Dict[str, str]
    motif_to_symbol: Dict[str, str]
    score_matrix: Dict[str, Dict[str, int]]
    motif_counter: Dict[str, int]

    def __init__(self, private_motif_threshold: int = 0):
        self.private_motif_threshold = private_motif_threshold
        self.symbol_to_motif = {}
        self.motif_to_symbol = {}
        self.score_matrix = {}
        self.motif_counter = {}

    @staticmethod
    def _divide_motifs_into_normal_and_private(motif_counter: Dict[str, int], 
                                               private_motif_threshold: int) -> Tuple[Dict[str, int], Dict[str, int]]:
        """ Divides motifs into normal and private based on a count threshold. """
        normal_motifs: Dict[str, int] = {}
        private_motifs: Dict[str, int] = {}
        
        # Replace Counter.most_common() with sorting a dictionary's items
        sorted_motifs = sorted(motif_counter.items(), key=lambda item: item[1], reverse=True)
        
        for motif, count in sorted_motifs:
            if count > private_motif_threshold:
                normal_motifs[motif] = count
            else:
                private_motifs[motif] = count
        return normal_motifs, private_motifs

    @staticmethod
    def find_private_motif_threshold(decomposed_vntrs: List[List[str]], label_count: int = 0) -> int:
        """ Finds the frequency threshold for private motifs. """
        maximum_label_count = len(utils.INDEX_TO_CHR) - 1
        if label_count > 0:
            maximum_label_count = label_count - 1

        motif_counter = utils.get_motif_counter(decomposed_vntrs)
        
        # Replace Counter.most_common() with sorting
        sorted_motifs = sorted(motif_counter.items(), key=lambda item: item[1], reverse=True)

        min_private_motif_threshold = 0
        for index, (motif, count) in enumerate(sorted_motifs):
            if index + 1 > maximum_label_count:
                min_private_motif_threshold = count
                break
        return min_private_motif_threshold

    @staticmethod
    def write_motif_map(output_file: str, motif_to_symbol: Dict[str, str], motif_counter: Dict[str, int]):
        """ Writes the motif-to-character mapping to a file. """
        # Replace Counter.most_common() with sorting
        sorted_motifs = sorted(motif_counter.items(), key=lambda item: item[1], reverse=True)
        with open(output_file, "w") as f:
            for motif, count in sorted_motifs:
                f.write(f"{motif}\t{motif_to_symbol[motif]}\t{count}\n")

    @staticmethod
    def _encode_decomposed_tr(decomposed_vntrs: List[List[str]], motif_to_symbol: Dict[str, str]) -> List[str]:
        """ Encodes TRs using the motif-to-symbol map. """
        labeled_trs: List[str] = []
        for vntr in decomposed_vntrs:
            labeled_vntr = ""
            for motif in vntr:
                labeled_vntr += str(motif_to_symbol[motif])
            labeled_trs.append(labeled_vntr)
        return labeled_trs

    def encode(self,
               decomposed_vntrs: List[List[str]],
               motif_map_file: str,
               label_count: int = 0,
               auto: bool = True) -> List[str]:
        """ Encodes decomposed tandem repeat sequences using ASCII characters. """
        
        def _index_to_char(index: int) -> str:
            """ Helper to get ASCII character from our constant list. """
            if index < 0 or index > len(utils.INDEX_TO_CHR) - 1:
                raise ValueError(f"Index should range from 0 to {len(utils.INDEX_TO_CHR) - 1}. Given: {index}")
            return utils.INDEX_TO_CHR[index]

        if label_count > 0:
            self.private_motif_threshold = self.find_private_motif_threshold(decomposed_vntrs, label_count)
        if auto:
            self.private_motif_threshold = self.find_private_motif_threshold(decomposed_vntrs)

        motif_to_symbol: Dict[str, str] = {}
        symbol_to_motif: Dict[str, str] = {}
        motif_counter = utils.get_motif_counter(decomposed_vntrs)
        self.motif_counter = motif_counter
        
        sorted_motifs = sorted(motif_counter.items(), key=lambda item: item[1], reverse=True)

        if self.private_motif_threshold > 0:
            normal_motifs, private_motifs = self._divide_motifs_into_normal_and_private(motif_counter, self.private_motif_threshold)
            
            # Get sorted lists for consistent encoding
            sorted_normal = sorted(normal_motifs.items(), key=lambda item: item[1], reverse=True)
            sorted_private = sorted(private_motifs.items(), key=lambda item: item[1], reverse=True)
            
            if len(normal_motifs) + 1 > len(utils.INDEX_TO_CHR):
                raise ValueError(f"Too many unique motifs to encode: {len(normal_motifs) + len(private_motifs)}")

            # Assign a code to all private motifs
            for motif, _ in sorted_private:
                motif_to_symbol[motif] = utils.PRIVATE_MOTIF_LABEL
            # Note: A single symbol maps to multiple private motifs. This is intended.
            # We will arbitrarily choose the first private motif for the reverse map.
            if sorted_private:
                symbol_to_motif[utils.PRIVATE_MOTIF_LABEL] = sorted_private[0][0]

            # Assign codes to normal motifs
            for index, (motif, _) in enumerate(sorted_normal):
                char = _index_to_char(index)
                motif_to_symbol[motif] = char
                symbol_to_motif[char] = motif
        else:
            unique_motif_count = len(motif_counter)
            if unique_motif_count > len(utils.INDEX_TO_CHR):
                raise ValueError(f"Too many unique motifs to encode: {unique_motif_count}")
            
            for index, (motif, _) in enumerate(sorted_motifs):
                char = _index_to_char(index)
                motif_to_symbol[motif] = char
                symbol_to_motif[char] = motif

        self.write_motif_map(motif_map_file, motif_to_symbol, motif_counter)

        self.motif_to_symbol = motif_to_symbol
        self.symbol_to_motif = symbol_to_motif

        self.score_matrix = utils.get_score_matrix(symbol_to_motif)

        encoded_trs = self._encode_decomposed_tr(decomposed_vntrs, motif_to_symbol)

        return encoded_trs