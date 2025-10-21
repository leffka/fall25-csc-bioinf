"""
Semi-global (Fitting) Alignment Algorithm
Aligns a shorter sequence (query) within a longer sequence (target) without penalty for gaps at the ends.
"""

def semiglobal_align(query, target, mat, gapo, gape):
    """
    Semi-global (fitting) alignment algorithm.
    
    Args:
        query: Query sequence as list of integers
        target: Target sequence as list of integers
        mat: Scoring matrix (square matrix flattened)
        gapo: Gap opening penalty
        gape: Gap extension penalty
    
    Returns:
        Tuple of (alignment_score, query_start, query_end, target_start, target_end, CIGAR operations)
    """
    qlen = len(query)
    tlen = len(target)
    m = int(len(mat) ** 0.5)
    gapoe = gapo + gape
    
    # DP matrix for scores
    dp = [[0] * (tlen + 1) for _ in range(qlen + 1)]
    # Traceback matrix: 0=match, 1=insertion, 2=deletion
    tb = [[0] * (tlen + 1) for _ in range(qlen + 1)]
    
    # Initialize first column (gaps in target at the start are free for query)
    for i in range(1, qlen + 1):
        dp[i][0] = -(gapoe + gape * (i - 1))
        tb[i][0] = 1  # Insertion
    
    # First row stays at 0 (gaps in query at the start of target are free)
    for j in range(1, tlen + 1):
        dp[0][j] = 0
        tb[0][j] = 2  # Deletion
    
    # Fill DP matrix
    for i in range(1, qlen + 1):
        for j in range(1, tlen + 1):
            # Match/mismatch score
            match_score = dp[i - 1][j - 1] + mat[query[i - 1] * m + target[j - 1]]
            
            # Insertion (gap in target)
            insert_score = dp[i - 1][j] - gapoe - gape
            
            # Deletion (gap in query)
            delete_score = dp[i][j - 1] - gapoe - gape
            
            # Choose best option
            if match_score >= insert_score and match_score >= delete_score:
                dp[i][j] = match_score
                tb[i][j] = 0  # Match
            elif insert_score >= delete_score:
                dp[i][j] = insert_score
                tb[i][j] = 1  # Insertion
            else:
                dp[i][j] = delete_score
                tb[i][j] = 2  # Deletion
    
    # Find best score in last row (end of query can align anywhere in target)
    max_score = dp[qlen][0]
    max_j = 0
    for j in range(1, tlen + 1):
        if dp[qlen][j] > max_score:
            max_score = dp[qlen][j]
            max_j = j
    
    # Traceback from best position
    cigar = []
    i = qlen
    j = max_j
    query_end = qlen
    target_end = max_j
    
    while i > 0 and j > 0:
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
    
    # Handle remaining gaps at the beginning
    while i > 0:
        cigar.append((1, 1))
        i -= 1
    
    query_start = i
    target_start = j
    
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
    
    return max_score, query_start, query_end, target_start, target_end, result_cigar


def main():
    # Test data - short query fitting into longer target
    query = [0, 1, 2, 3, 0, 1, 2, 3]
    target = [3, 3, 0, 1, 2, 3, 2, 1, 2, 3, 1, 1]
    
    # Scoring matrix (4x4 for DNA: A, C, G, T)
    # Match = 2, Mismatch = -1
    mat = [ 2, -1, -1, -1,
           -1,  2, -1, -1,
           -1, -1,  2, -1,
           -1, -1, -1,  2 ]
    
    gapo = 5      # Gap opening penalty
    gape = 1      # Gap extension penalty
    
    score, q_start, q_end, t_start, t_end, cigar = semiglobal_align(query, target, mat, gapo, gape)
    
    print("--- Python Semi-global (Fitting) Alignment ---")
    print(f"Score: {score}")
    print(f"Query Range: {q_start} - {q_end}")
    print(f"Target Range: {t_start} - {t_end}")
    cigar_str = ''.join([f'{length}{op}' for length, op in cigar])
    print(f"CIGAR: {cigar_str}")
    print()


if __name__ == "__main__":
    main()