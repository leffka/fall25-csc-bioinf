# AI / LLM Disclosure (Week 1)

- **Student:** Lev Chshemelinin
- **Repo:** https://github.com/leffka/fall25-csc-bioinf
- **Assignment:** Week 1 – de Bruijn assembler (Python → Codon), CI, reproducibility
- **Dates:** 2025-09-18 (ongoing for Week 1)

## Models & Tools
| Purpose | Model/Version | Access Method | Date |
|---|---|---|---|
| Repo scaffolding & CI workflow creation | GPT-5 Thinking (ChatGPT) | ChatGPT web | 2025-09-18 |
| YAML error troubleshooting (line 9) | GPT-5 Thinking (ChatGPT) | ChatGPT web | 2025-09-18 |
| Evaluation automation (`week1/evaluate.sh`) | GPT-5 Thinking (ChatGPT) | ChatGPT web | 2025-09-18 |
| N50 helper script (`compute_n50.py`) | GPT-5 Thinking (ChatGPT) | ChatGPT web | 2025-09-18 |
| Step-by-step run instructions & reporting templates | GPT-5 Thinking (ChatGPT) | ChatGPT web | 2025-09-18 |

## Prompts (excerpts)
- “I created a public repository, what's next?” → request for repo + CI setup.
- “Please slow down… do I need to add it to my computer?” → request for local clone vs Codespaces.
- “It is green now, what is next?” → request for Python baseline steps.
- “Here are my numbers… fill out the docs for me.” → request to prepare `ai.md` and `report.md`.

> Full prompt history is available in the ChatGPT conversation and can be exported if needed.

## Outputs Used (from AI)
- `.github/workflows/actions.yml`
- `week1/evaluate.sh`
- `week1/code/compute_n50.py`
- Templates: `week1/ai.md`, `week1/report.md`

## Verification / Understanding
- CI installs Codon + seq plugin and runs `week1/evaluate.sh` (green).
- `compute_n50.py` computes N50 from FASTA or plain-text contigs.
- I can explain N50, timing with `/usr/bin/time -f %E`, and Codon invocation (`codon run -release`).

## Human Edits / Rationale
- Simplified YAML to avoid syntax issues.
- Will adjust `evaluate.sh` file detection if assembler writes to a different path.
- Codon port will keep Python CLI for parity.

## Risks & Mitigations
- Upstream repo may not be fully reproducible → document versions; note mismatches.
- Auto-detection of contigs could fail → point evaluator to explicit file path.
- Codon type/recursion differences → prefer typed containers; iterative loops where needed.