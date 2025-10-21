"""
Simple FASTA file reader utility
"""

def read_fasta(filename):
    """
    Read a FASTA file and return the sequence.

    Args:
        filename: Path to FASTA file

    Returns:
        String containing the concatenated sequence (no header)
    """
    sequence = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                continue  # Skip header lines
            sequence.append(line.upper())
    return ''.join(sequence)


def sequence_to_integers(seq):
    """
    Convert DNA sequence to integer list.
    A=0, C=1, G=2, T=3

    Args:
        seq: DNA sequence string

    Returns:
        List of integers
    """
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    result = []
    for base in seq:
        if base in mapping:
            result.append(mapping[base])
        else:
            # Handle ambiguous/unknown bases (e.g., N, gaps) by treating as A
            result.append(0)
    return result


def get_subsequences(seq, query_start, query_len, target_start, target_len):
    """
    Extract query and target subsequences from a sequence.

    Args:
        seq: Full sequence as integer list
        query_start: Start position for query
        query_len: Length of query
        target_start: Start position for target
        target_len: Length of target

    Returns:
        Tuple of (query, target) as integer lists
    """
    query = seq[query_start:query_start + query_len]
    target = seq[target_start:target_start + target_len]
    return query, target


def read_fasta_records(filename):
    """
    Read a multi-record FASTA and return a dict {record_id: sequence}.

    - The record ID is taken as the first whitespace-delimited token on
      the header line (after '>'). This safely handles headers like:
          >t5 a bug was triggered "-t extz2_sse ..."
      where the ID will be parsed as 't5'.
    - Sequence lines are uppercased and concatenated; blank lines are ignored.

    Args:
        filename: Path to a FASTA file that may contain multiple records.

    Returns:
        Dict mapping record IDs (str) to concatenated sequences (str).
    """
    records = {}
    curr_id = None
    seq_parts = []
    with open(filename, 'r') as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith('>'):
                # Save previous record if any
                if curr_id is not None:
                    records[curr_id] = ''.join(seq_parts).upper()
                # New record id = first token after '>'
                curr_id = line[1:].strip().split()[0]
                seq_parts = []
            else:
                seq_parts.append(line)
        # Flush last record
        if curr_id is not None:
            records[curr_id] = ''.join(seq_parts).upper()
    return records