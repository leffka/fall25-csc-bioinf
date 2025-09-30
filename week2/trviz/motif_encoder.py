from typing import List, Dict, Optional
from collections import Counter

class MotifEncoder:
    """Encode motifs to ASCII symbols; group rare motifs if needed."""
    def __init__(self, private_motif_threshold=0):
        self.private_motif_threshold = private_motif_threshold

    @staticmethod
    def find_private_motif_threshold(decomposed_vntrs: List[List[str]], label_count: Optional[int] = None) -> int:
        motif_counter = Counter(m for seq in decomposed_vntrs for m in seq)
        max_labels = label_count if label_count is not None else 90
        if len(motif_counter) <= max_labels:
            return 1
        max_freq = max(motif_counter.values())
        for t in range(1, max_freq + 2):
            normal_count = sum(1 for freq in motif_counter.values() if freq >= t)
            if normal_count <= max_labels:
                return t
        return 1

    def encode(self, decomposed_vntrs: List[List[str]], motif_map_file: str, label_count: Optional[int] = None, auto: bool = True):
        motif_counter = Counter(m for seq in decomposed_vntrs for m in seq)
        if auto:
            threshold = MotifEncoder.find_private_motif_threshold(decomposed_vntrs, label_count)
        else:
            threshold = self.private_motif_threshold if self.private_motif_threshold > 0 else 1

        normal_items = [(m, c) for m, c in motif_counter.items() if c >= threshold]
        private_items = [(m, c) for m, c in motif_counter.items() if c < threshold]
        normal_items.sort(key=lambda x: -x[1])
        private_items.sort(key=lambda x: -x[1])

        symbol_map: Dict[str, str] = {}
        base_ord = ord('!')
        for i, (motif, count) in enumerate(normal_items):
            if i >= 90:
                break
            symbol_map[motif] = chr(base_ord + i)

        if private_items:
            idx = len(normal_items)
            if idx >= 90:
                idx = 89
            priv_sym = chr(base_ord + idx)
            for motif, _ in private_items:
                symbol_map[motif] = priv_sym

        with open(motif_map_file, "w") as f:
            for motif, count in sorted(motif_counter.items(), key=lambda x: -x[1]):
                f.write(f"{motif}\t{symbol_map[motif]}\t{count}\n")

        encoded = []
        for seq in decomposed_vntrs:
            encoded.append("".join(symbol_map[m] for m in seq))
        return encoded, symbol_map
