"""
Affine Gap Penalty Global Alignment Algorithm
Uses three matrices to handle gap opening and extension penalties separately.
"""

def affine_global_align(query, target, mat, gapo, gape):
    """
    Affine gap penalty global alignment algorithm using three-matrix approach.
    
    Args:
        query: Query sequence as list of integers
        target: Target sequence as list of integers
        mat: Scoring matrix (square matrix flattened)
        gapo: Gap opening penalty
        gape: Gap extension penalty
    
    Returns:
        Tuple of (alignment_score, CIGAR operations)
    """
    qlen = len(query)
    tlen = len(target)
    m = int(len(mat) ** 0.5)
    
    # Initialize negative infinity for boundary conditions
    NEG_INF = float('-inf')
    
    # Three matrices: M (match), I (insertion), D (deletion)
    M = [[NEG_INF] * (tlen + 1) for _ in range(qlen + 1)]
    I = [[NEG_INF] * (tlen + 1) for _ in range(qlen + 1)]
    D = [[NEG_INF] * (tlen + 1) for _ in range(qlen + 1)]
    
    # Traceback matrix: 0=match, 1=insertion, 2=deletion
    tb = [[0] * (tlen + 1) for _ in range(qlen + 1)]
    
    # Initialize base case
    M[0][0] = 0
    I[0][0] = NEG_INF
    D[0][0] = NEG_INF
    
    # Initialize first column (insertions)
    for i in range(1, qlen + 1):
        M[i][0] = NEG_INF
        I[i][0] = -gapo - gape * i
        D[i][0] = NEG_INF
        tb[i][0] = 1
    
    # Initialize first row (deletions)
    for j in range(1, tlen + 1):
        M[0][j] = NEG_INF
        I[0][j] = NEG_INF
        D[0][j] = -gapo - gape * j
        tb[0][j] = 2
    
    # Fill matrices using affine gap penalty model
    for i in range(1, qlen + 1):
        for j in range(1, tlen + 1):
            # Match/mismatch score
            match_score = mat[query[i - 1] * m + target[j - 1]]
            M[i][j] = match_score + max(M[i - 1][j - 1], I[i - 1][j - 1], D[i - 1][j - 1])
            
            # Insertion: gap in target (coming from query)
            # Either open a new gap or extend existing gap
            from_M = M[i - 1][j] - gapo - gape
            from_I = I[i - 1][j] - gape
            I[i][j] = max(from_M, from_I)
            
            # Deletion: gap in query (coming from target)
            # Either open a new gap or extend existing gap
            from_M_del = M[i][j - 1] - gapo - gape
            from_D = D[i][j - 1] - gape
            D[i][j] = max(from_M_del, from_D)
            
            # Determine best path for traceback
            best_score = max(M[i][j], I[i][j], D[i][j])
            if best_score == I[i][j]:
                tb[i][j] = 1  # Insertion
            elif best_score == D[i][j]:
                tb[i][j] = 2  # Deletion
            else:
                tb[i][j] = 0  # Match
    
    # Final score is the best of the three matrices at the end
    final_score = max(M[qlen][tlen], I[qlen][tlen], D[qlen][tlen])
    
    # Traceback to build CIGAR
    cigar = []
    i = qlen
    j = tlen
    
    while i > 0 or j > 0:
        if i == 0:
            # Only deletions remaining
            cigar.append((2, 1))
            j -= 1
        elif j == 0:
            # Only insertions remaining
            cigar.append((1, 1))
            i -= 1
        else:
            op = tb[i][j]
            
            if op == 0:  # Match/Mismatch
                cigar.append((0, 1))
                i -= 1
                j -= 1
            elif op == 1:  # Insertion
                cigar.append((1, 1))
                i -= 1
            else:  # Deletion
                cigar.append((2, 1))
                j -= 1
    
    # Compress CIGAR (combine consecutive same operations)
    cigar_compressed = []
    for op, count in reversed(cigar):
        if cigar_compressed and cigar_compressed[-1][0] == op:
            cigar_compressed[-1] = (op, cigar_compressed[-1][1] + count)
        else:
            cigar_compressed.append((op, count))
    
    # Convert to string format
    ops = "MID"
    result_cigar = [(length, ops[op]) for op, length in cigar_compressed]
    
    return int(final_score), result_cigar


def main():
    # Test data
    query = [0, 1, 2, 3, 0, 1, 2, 3]
    target = [0, 1, 2, 3, 2, 1, 2, 3]
    
    # Scoring matrix (4x4 for DNA: A, C, G, T)
    # Match = 2, Mismatch = -1
    mat = [ 2, -1, -1, -1,
           -1,  2, -1, -1,
           -1, -1,  2, -1,
           -1, -1, -1,  2 ]
    
    gapo = 5      # Gap opening penalty
    gape = 1      # Gap extension penalty
    
    score, cigar = affine_global_align(query, target, mat, gapo, gape)
    
    print("--- Python Affine Gap Global Alignment ---")
    print(f"Score: {score}")
    cigar_str = ''.join([f'{length}{op}' for length, op in cigar])
    print(f"CIGAR: {cigar_str}")
    print()


if __name__ == "__main__":
    main()