#!/usr/bin/env python3
"""
Compute N50 from a FASTA file or from a plain text file with one contig per line.

Usage:
  python compute_n50.py <path> [--min-len N]
If <path> is a directory, the script will search for the most recently modified FASTA-like file.
"""
import sys, os, glob
from typing import List

def read_lengths_from_fasta(path: str) -> List[int]:
    lens = []
    seq = []
    def flush():
        if seq:
            lens.append(len(''.join(seq)))
            seq.clear()
    with open(path, 'r') as fh:
        for line in fh:
            line=line.strip()
            if not line: continue
            if line.startswith('>'):
                flush()
            else:
                seq.append(line)
    flush()
    return lens

def read_lengths_from_txt(path: str) -> List[int]:
    lens = []
    with open(path, 'r') as fh:
        for line in fh:
            s=line.strip()
            if s and not s.startswith('>'):
                lens.append(len(s))
    return lens

def guess_file(d: str) -> str:
    cands = []
    for pat in ("*.fa", "*.fasta", "*.fa.gz", "*.fna", "*.txt", "*contig*"):
        cands.extend(glob.glob(os.path.join(d, pat)))
    if not cands:
        raise FileNotFoundError(f"No candidate contig files in {d}")
    cands.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return cands[0]

def n50(lengths: List[int]) -> int:
    if not lengths:
        return 0
    lengths = sorted(lengths, reverse=True)
    total = sum(lengths)
    acc = 0
    for L in lengths:
        acc += L
        if acc >= total/2:
            return L
    return lengths[-1]

def main():
    if len(sys.argv) < 2:
        print("Usage: python compute_n50.py <path>", file=sys.stderr); sys.exit(2)
    path = sys.argv[1]
    if os.path.isdir(path):
        path = guess_file(path)
    if not os.path.exists(path):
        print(f"error: {path} not found", file=sys.stderr); sys.exit(2)
    # Heuristic: FASTA if any '>' in file
    is_fasta = False
    with open(path,'r') as fh:
        for _ in range(50):
            line = fh.readline()
            if not line: break
            if line.startswith('>'):
                is_fasta = True; break
    lens = read_lengths_from_fasta(path) if is_fasta else read_lengths_from_txt(path)
    print(n50(lens))

if __name__ == "__main__":
    main()