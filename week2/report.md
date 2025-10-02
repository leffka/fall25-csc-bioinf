Week 2 Report

📝 Repository & CI Status
	•	Repository: leffka/fall25-csc-bioinf

⸻

📊 Final Results

End-to-end TRviz pipeline and component tests executed under Codon.

Test	Status	Artifacts
Smoke test (smoke_test.py)	Pass	toy_motif_map.txt, toy_aligned.txt, toy_trplot.png, toy_color_map.png
Workflow (test_workflow)	Pass	e2e_motif_map.txt, e2e_aligned.txt, e2e_trplot.png, e2e_color_map.png
Decomposer basic	Pass	—
Decomposer edge cases	Pass	—
Encoder mapping	Pass	enc_motif_map.txt
Encoder private grouping	Pass	enc_small_map.txt


⸻

🧬 Analysis: Port choices for Codon
	•	Visualizer moved to Pillow (Python interop) with explicit submodule imports.
	•	Outputs written to current directory (no os.path, no directory creation).
	•	FASTA reader returns List[str] IDs (avoids Optional inference).
	•	Tests are deterministic and avoid unsupported stdlib calls.

⸻

⚙️ Reproduction (local)

# Set Codon ↔ Python bridge
export CODON_PYTHON="/Library/Frameworks/Python.framework/Versions/3.11/lib/libpython3.11.dylib"
export PYTHONPATH="/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages"

# From repo root
bash week2/evaluate.sh

Outputs appear in week2/ (for smoke/e2e) and current working dir for generated files.

⸻

🤖 Automation

week2/evaluate.sh:
	•	Changes into week2/ to make trviz/ importable.
	•	Extends PYTHONPATH to include week2, week2/trviz, week2/code.
	•	Runs a Codon entry that executes the single tests file.
	•	Prints results to stdout for GitHub Actions logs.

GitHub Actions workflow:
	•	Installs Codon v0.19.3.
	•	Sets CODON_PYTHON (via find_libpython) and PYTHONPATH (site-packages).
	•	Runs bash week2/evaluate.sh.
	•	(Optional) Uploads artifacts and test-output.txt.

⸻

💡 Notes & Gotchas
	•	Use PYTHONPATH (not PYTHON_PATH).
	•	Import Pillow via Codon interop: from python import PIL.Image, PIL.ImageDraw, PIL.ImageFont.
	•	Avoid os.path, pathlib, subprocess in Codon code.
	•	Replace T | None with Optional[T] in annotations.
	•	Codon’s import base = executed file’s folder; run from week2/ (or use a small runner) so trviz is visible.

⸻

💻 Environment
	•	OS: macOS (student machine) / Ubuntu (CI)
	•	Shell: bash/zsh
	•	Python: 3.11
	•	Codon: v0.19.3
