# Week 1 Report

## 0. Repository & CI
- Repo URL: <your public repo URL>
- CI Status: ✅/❌ (screenshot or describe)
- Commit (this submission): `<hash>`

## 1. Reproduction (Python)
**Source:** https://github.com/zhongyuchen/genome-assembly (commit: <hash>)  
**Exact steps I ran:**
```bash
# Example
python main.py data1
python main.py data2
python main.py data3
# (include any recursion limit / ulimit changes you needed)
```
**Did I match the README table numbers?** Yes/No (explain any deltas)

## 2. Codon Conversion
- Where my Codon code lives: `week1/code/codon/`
- What changed to make it compile/run: <types, loops, recursion, data structures>
- How I verified parity: <diff outputs, N50, spot-check contigs>

## 3. Automated Evaluation
Results produced by `week1/evaluate.sh`:

```
Dataset	Language 	Runtime 	N50
------------------------------------------------------------
<filled by CI run>
```

## 4. Reproducibility Notes
- Versions:
  - Python: `python --version`
  - Codon: `codon --version`
  - OS/CPU: `uname -a`
- Anything that blocked strict reproduction (data ambiguity, unspecified seeds, etc.).  
- If numbers don’t match the README, why I think the repo is not reproducible as-is.

## 5. (Bonus) What are data1…data4?
- Approach (BLAST contigs against nt or specific references).  
- Top hits / confidence, caveats.