"""
Global Alignment Algorithm (Needleman-Wunsch)
"""

def global_align(query, target, mat, gapo, gape):
    """
    Global alignment algorithm.
    
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
    gapoe = gapo + gape
    
    # DP matrix for scores
    dp = [[0] * (tlen + 1) for _ in range(qlen + 1)]
    # Traceback matrix: 0=match, 1=insertion, 2=deletion
    tb = [[0] * (tlen + 1) for _ in range(qlen + 1)]
    
    # Initialize first row and column
    for i in range(1, qlen + 1):
        dp[i][0] = -(gapoe + gape * (i - 1))
        tb[i][0] = 1  # Insertion
    
    for j in range(1, tlen + 1):
        dp[0][j] = -(gapoe + gape * (j - 1))
        tb[0][j] = 2  # Deletion
    
    # Fill DP matrix
    for i in range(1, qlen + 1):
        for j in range(1, tlen + 1):
            # Match/mismatch score
            match_score = dp[i - 1][j - 1] + mat[(query[i - 1]) * m + target[j - 1]]
            
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
    
    # Traceback to build CIGAR
    cigar = []
    i = qlen
    j = tlen
    
    while i > 0 or j > 0:
        if i == 0:
            # Deletions only
            cigar.append((2, 1))
            j -= 1
        elif j == 0:
            # Insertions only
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
    
    return dp[qlen][tlen], result_cigar