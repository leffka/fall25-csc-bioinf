#!/usr/bin/env python3
"""
Compute N50 from:
 - FASTA (">" headers, sequences may span lines)
 - Plain text: one contig per line (ACGT...)
 - Numeric logs: "idx length" or "length" per line (e.g., "0 15650")

Usage:
  python compute_n50.py <path or directory>
"""
import sys, os, glob, re
from typing import List

def read_lengths_from_fasta(path: str) -> List[int]:
    lens, seq = [], []
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

def read_lengths_from_text(path: str) -> List[int]:
    lens = []
    num_pair = re.compile(r'^\s*\d+\s+(\d+)\s*$')   # "idx length"
    num_single = re.compile(r'^\s*(\d+)\s*$')       # "length"
    dna_line = re.compile(r'^[ACGTNacgtn]+$')       # contig sequence
    with open(path, 'r') as fh:
        for line in fh:
            s=line.strip()
            if not s: 
                continue
            m = num_pair.match(s)
            if m:
                lens.append(int(m.group(1))); continue
            m = num_single.match(s)
            if m:
                lens.append(int(m.group(1))); continue
            if s.startswith(">"):
                # Looks like FASTA — bail and let FASTA reader handle it
                return read_lengths_from_fasta(path)
            if dna_line.match(s):
                lens.append(len(s)); continue
            # else: ignore non-length lines
    return lens

def guess_fasta_file(d: str) -> str | None:
    for pat in ("*.fa", "*.fasta", "*.fna"):
        cands = glob.glob(os.path.join(d, pat))
        if cands:
            cands.sort(key=os.path.getmtime, reverse=True)
            return cands[0]
    return None

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
        f = guess_fasta_file(path)
        path = f if f else os.path.join(path, ".run.out")  # likely stdout capture
    if not os.path.exists(path):
        print(f"error: {path} not found", file=sys.stderr); sys.exit(2)

    # FASTA if any '>' in first lines
    is_fasta = False
    with open(path,'r') as fh:
        for _ in range(50):
            line = fh.readline()
            if not line: break
            if line.startswith('>'):
                is_fasta = True; break

    lens = read_lengths_from_fasta(path) if is_fasta else read_lengths_from_text(path)
    print(n50(lens))

if __name__ == "__main__":
    main()