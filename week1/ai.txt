# AI / LLM Disclosure (Week 1)

- **Student:** Lev Chshemelinin
- **Repo:** https://github.com/leffka/fall25-csc-bioinf
- **Assignment:** Week 1 – de Bruijn assembler (Python → Codon), CI, reproducibility
- **Dates:** 2025-09-18 (ongoing for Week 1)

# AI Use Disclosure — Week 1

**Course:** Bioinformatics and Clinical Applications (Fall 2025)  
**Repo:** https://github.com/leffka/fall25-csc-bioinf

## Models & tools used
- **ChatGPT — GPT-5 Thinking** (reasoning model)
  - Repo/CI setup guidance and shell debugging
  - Authored `week1/evaluate.sh` and a portable **N50** calculator
  - Converted the Python de Bruijn assembler to a **Codon (unitigs)** version
  - Clarified Codon–Python differences (stdlib gaps, typing, string formatting)
  - Helped write and polish `week1/report.md`
- **Google Translate** for reading the upstream Mandarin README.
- **Non-AI tools:** Python 3.11/3.13, Codon v0.19.3 + `seq` plugin v0.11.5, Git/GitHub.

## Representative prompts I used
I iterated with many short prompts; below are representative ones that led to the submitted code/text. I reviewed and edited all outputs.

1) **Evaluator + N50**
- *“Write a portable `week1/evaluate.sh` that: (a) fetches/unzips data1–3 from the upstream repo if missing, (b) runs the Python assembler and the Codon version, (c) times runs, and (d) computes N50 into a tab-separated `week1/report.tsv`. Prefer Python’s printed `index length` lines if no FASTA is produced.”*  
- *“Make the script macOS-friendly (no GNU-only flags), and handle `python3` vs `python` gracefully.”*

2) **Codon conversion (unitigs)**
- *“Port the simple Python de Bruijn assembler to Codon. Use typed dict/list containers to avoid `NoneType` inference, avoid `os.path/json`, and parse `param.json` with a regex to get `k`. Implement **unitigs** (break at branch nodes; handle 1–1 cycles). Print top-20 `'index length'` and write `contigs.fa`.”*  
- *“Fix Codon string formatting errors by replacing `%` with concatenation; avoid importing unsupported stdlib pieces unless necessary.”*

3) **Debugging + parity notes**
- *“Explain why unitigs give N50≈k when many contigs are single-edge, and why the Python baseline shows longer contigs.”*  
- *“Draft concise report sections for environment, reproduction, Codon notes, automation, and reproducibility caveats.”*

