"""
Local Alignment Algorithm (Smith-Waterman)
"""

def local_align(query, target, mat, gapo, gape):
    """
    Local alignment algorithm.
    
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
    
    # Track best score and its position
    max_score = 0
    max_i = 0
    max_j = 0
    
    # Fill DP matrix
    for i in range(1, qlen + 1):
        for j in range(1, tlen + 1):
            # Match/mismatch score
            match_score = dp[i - 1][j - 1] + mat[(query[i - 1]) * m + target[j - 1]]
            
            # Insertion (gap in target)
            insert_score = dp[i - 1][j] - gapoe - gape
            
            # Deletion (gap in query)
            delete_score = dp[i][j - 1] - gapoe - gape
            
            # Choose best option (or 0 for local alignment)
            if match_score >= insert_score and match_score >= delete_score and match_score > 0:
                dp[i][j] = match_score
                tb[i][j] = 0  # Match
            elif insert_score >= delete_score and insert_score > 0:
                dp[i][j] = insert_score
                tb[i][j] = 1  # Insertion
            elif delete_score > 0:
                dp[i][j] = delete_score
                tb[i][j] = 2  # Deletion
            else:
                dp[i][j] = 0
                tb[i][j] = -1  # Reset (no alignment)
            
            # Track maximum score
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_i = i
                max_j = j
    
    # Traceback from best position to start
    cigar = []
    i = max_i
    j = max_j
    query_start = max_i
    target_start = max_j
    
    while i > 0 and j > 0:
        op = tb[i][j]
        
        if op == -1:  # Reset point reached
            break
        elif op == 0:  # Match/Mismatch
            cigar.append((0, 1))
            i -= 1
            j -= 1
        elif op == 1:  # Insertion
            cigar.append((1, 1))
            i -= 1
        else:  # Deletion
            cigar.append((2, 1))
            j -= 1
    
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
    
    return max_score, query_start, target_start, max_i, max_j, result_cigar