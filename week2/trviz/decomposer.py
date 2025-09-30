class Decomposer:
    """Greedy motif decomposition (Codon-safe)."""
    def decompose(self, tr_sequence, motifs):
        result = []
        seq = tr_sequence
        motifs_sorted = sorted(motifs, key=len, reverse=True)
        while seq:
            matched = False
            for motif in motifs_sorted:
                if seq.startswith(motif):
                    result.append(motif)
                    seq = seq[len(motif):]
                    matched = True
                    break
            if not matched:
                result.append(seq)
                break
        return result
