from typing import List, Tuple

def get_sample_and_sequence_from_fasta(fasta_path: str) -> Tuple[List[str], List[str]]:
    sample_ids: List[str] = []
    sequences: List[str] = []
    current_seq_lines: List[str] = []

    # Keep this strictly a string so Codon does not infer Optional[str]
    current_id: str = ""
    have_id = False

    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                # if we were collecting a previous sequence, flush it
                if have_id:
                    sequences.append(''.join(current_seq_lines))
                    current_seq_lines = []
                header = line[1:].strip()
                current_id = header.split()[0] if header else 'Unnamed'
                sample_ids.append(current_id)  # always a str
                have_id = True
            else:
                current_seq_lines.append(line)

    if have_id:
        sequences.append(''.join(current_seq_lines))

    return sample_ids, sequences
