#!/usr/bin/env python
# Run: ~/.codon/bin/codon run -release main.py data1
# Output:
#   - FASTA: ./contigs.fa
#   - Console: summary of input FASTAs + top 20 contig lengths ("index length")

import sys, re

# ---------- FASTA / dataset loading ----------

def read_fasta(path: str) -> list[str]:
    seqs: list[str] = []
    try:
        fh = open(path, "r")
    except:
        return seqs
    cur: list[str] = []
    for line in fh:
        s = line.strip()
        if not s:
            continue
        if s.startswith(">"):
            if cur:
                seqs.append("".join(cur))
                cur = []
        else:
            cur.append(s)
    if cur:
        seqs.append("".join(cur))
    fh.close()
    return seqs

def load_k(param_path: str, default_k: int = 31) -> int:
    # Minimal parser (Codon doesn't ship Python's json by default)
    try:
        txt = open(param_path, "r").read()
        m = re.search(r'"k"\s*:\s*(\d+)', txt)
        if m:
            return int(m.group(1))
    except:
        pass
    return default_k

def try_dataset_dir(d: str) -> bool:
    # If any expected file opens, assume it's the right dataset dir
    for fn in ["short_1.fasta", "short_2.fasta", "long.fasta", "param.json"]:
        try:
            open(d + "/" + fn).close()
            return True
        except:
            pass
    return False

def resolve_dataset_dir(dataset: str) -> str:
    # Assume we run from week1/code/codon
    cands: list[str] = [
        "../../../code/genome-assembly/" + dataset,  # repo-root/code/genome-assembly/<dataset>
        "../genome-assembly/" + dataset,             # sibling path option
        "genome-assembly/" + dataset,                # local fallback
    ]
    for d in cands:
        if try_dataset_dir(d):
            return d
    return ""

def load_dataset(dataset: str) -> tuple[list[str], int]:
    dsdir = resolve_dataset_dir(dataset)
    if not dsdir:
        sys.stderr.write("error: dataset folder not found; run from week1/code/codon\n")
        sys.stderr.write("tried ../../../code/genome-assembly/" + dataset +
                         " and ../genome-assembly/" + dataset + "\n")
        sys.exit(2)

    k = load_k(dsdir + "/param.json", 31)

    reads: list[str] = []
    for fn in ["short_1.fasta", "short_2.fasta", "long.fasta"]:
        fp = dsdir + "/" + fn
        seqs = read_fasta(fp)
        if len(seqs) > 0:
            read_len = len(seqs[0])
            print(fn, len(seqs), read_len)
            for s in seqs:
                reads.append(s)
    return reads, k

# ---------- de Bruijn graph + UNITIGS ----------

def build_dbg(reads: list[str], k: int) -> tuple[dict[str, list[str]], dict[str, int], dict[str, int]]:
    adj: dict[str, list[str]] = {}   # node -> outgoing nodes (multi-edges via list)
    indeg: dict[str, int] = {}       # node -> indegree
    outdeg: dict[str, int] = {}      # node -> outdegree

    def add_edge(u: str, v: str) -> None:
        if u not in adj:
            adj[u] = []
        adj[u].append(v)
        outdeg[u] = outdeg.get(u, 0) + 1
        indeg[v] = indeg.get(v, 0) + 1
        if v not in adj:
            adj[v] = []  # ensure node exists

    for s in reads:
        if len(s) < k:
            continue
        i = 0
        end = len(s) - k + 1
        while i < end:
            u = s[i:i + k - 1]
            v = s[i + 1:i + k]
            add_edge(u, v)
            i += 1

    for u in list(adj.keys()):
        if u not in indeg:
            indeg[u] = 0
        if u not in outdeg:
            outdeg[u] = 0
    return adj, indeg, outdeg

def pop_next(adj: dict[str, list[str]], u: str) -> str:
    if (u in adj) and (len(adj[u]) > 0):
        return adj[u].pop()
    return ""

def spell_contig(path_nodes: list[str]) -> str:
    if len(path_nodes) == 0:
        return ""
    pieces: list[str] = [path_nodes[0]]
    i = 1
    n = len(path_nodes)
    while i < n:
        v = path_nodes[i]
        pieces.append(v[len(v) - 1])
        i += 1
    return "".join(pieces)

def assemble_unitigs(adj: dict[str, list[str]], indeg: dict[str, int], outdeg: dict[str, int]) -> list[str]:
    contigs: list[str] = []
    # destructive copy of adjacency
    g: dict[str, list[str]] = {}
    for key in adj:
        g[key] = adj[key][:]

    nodes: list[str] = list(g.keys())

    def is_1_1(x: str) -> bool:
        return (indeg.get(x, 0) == 1) and (outdeg.get(x, 0) == 1)

    # start at branching or dead-end nodes
    for v in nodes:
        if outdeg.get(v, 0) == 0:
            continue
        if not is_1_1(v):
            while v in g and len(g[v]) > 0:
                path: list[str] = [v]
                u = v
                w = pop_next(g, u)
                while w != "":
                    path.append(w)
                    if not is_1_1(w):
                        break
                    u = w
                    w = pop_next(g, u)
                c = spell_contig(path)
                if len(c) > 0:
                    contigs.append(c)

    # cycles made only of 1-1 nodes
    for v in nodes:
        while v in g and len(g[v]) > 0:
            path = [v]
            u = v
            w = pop_next(g, u)
            steps = 0
            while (w != "") and (steps < 10_000_000):
                steps += 1
                path.append(w)
                if w == v:
                    break
                if not is_1_1(w):
                    break
                u = w
                w = pop_next(g, u)
            c = spell_contig(path)
            if len(c) > 0:
                contigs.append(c)

    return contigs

# ---------- output ----------

def write_fasta(contigs: list[str], out_path: str) -> None:
    out = open(out_path, "w")
    i = 0
    n = len(contigs)
    while i < n:
        c = contigs[i]
        out.write(">contig" + str(i) + " len=" + str(len(c)) + "\n")
        j = 0
        L = len(c)
        while j < L:
            out.write(c[j:j+80] + "\n")
            j += 80
        i += 1
    out.close()

# ---------- main ----------

def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("usage: codon run -release main.py <data1|data2|data3|data4>\n")
        sys.exit(2)
    dataset = sys.argv[1]

    reads, k = load_dataset(dataset)
    if len(reads) == 0:
        sys.stderr.write("no reads found; nothing to assemble\n")
        sys.exit(1)

    adj, indeg, outdeg = build_dbg(reads, k)
    contigs = assemble_unitigs(adj, indeg, outdeg)   # <— unitigs version

    write_fasta(contigs, "contigs.fa")

    # Print top 20 contig lengths as "index length" for evaluator
    lens: list[int] = [len(c) for c in contigs]
    lens.sort(reverse=True)
    i = 0
    n = len(lens)
    while i < n and i < 20:
        print(i, lens[i])
        i += 1

if __name__ == "__main__":
    main()