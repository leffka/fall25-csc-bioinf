AI / LLM Disclosure (Week 2)
	•	Student:
	•	Repo: https://github.com/leffka/fall25-csc-bioinf
	•	Assignment: Week 2 – TRviz (Python → Codon), tests, CI

AI Use Disclosure — Week 2

Course: Bioinformatics and Clinical Applications (Fall 2025)
Repo: https://github.com/leffka/fall25-csc-bioinf

Models & tools used
	•	ChatGPT — GPT-5 Thinking (reasoning model)

Representative prompts I used

I iterated with many short prompts; below are representative ones that led to the submitted code/text. I reviewed and edited all outputs.
	1.	Initial port

	•	“Help me port the TRviz repository to Codon, excluding trviz/visualizer. Replace the visualizer with a Python implementation.”

	2.	Complete code + evaluator

	•	“Provide full code outputs for each file and an evaluate.sh that runs a smoke test and prints results.”

	3.	Packaged handoff

	•	“Bundle the current version into a zip I can download, unzip, and run locally.”

	4.	Python visualizer

	•	“Implement a Pillow-based visualizer in trviz/main.py that draws the TR composition and a color legend.”

	5.	Codon interop

	•	“Read the Codon docs and update imports for Python interop (explicit submodules). Configure environment variables so the Python packages can be found.”

	6.	Single tests file

	•	“Create a single test.py that exercises the workflow, decomposer, and encoder with deterministic outputs.”

	7.	Evaluator wiring

	•	“Update week2/evaluate.sh so it sets the necessary paths and runs the tests from week2/.”

	8.	CI workflow

	•	“Write a GitHub Actions YAML that installs Codon, configures the Python bridge, runs week2/evaluate.sh, and surfaces logs in Actions.”

	9.	Runner script (optional)

	•	“Add a small run_tests.py in week2/ to import and run test/test.py cleanly when invoked by Codon.”

	10.	Disclosure doc

	•	“Draft an ai.md that lists the model used and the representative prompts only.”
