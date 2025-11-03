# AI usage report – Week 5

This document describes how I used AI tools for the **Week 5 – CYP2C variant calling and phasing** assignment in PSYC/CSC 370 (fall 2025).

## Tool used

- **Model:** ChatGPT (GPT-5 Thinking)
- **Provider:** OpenAI, accessed via chat.openai.com

## What I used AI for

1. **Environment and tooling help**
   - Advice on installing Miniforge/conda on macOS and creating a `week5-bio` environment.
   - Suggestions for which bioinformatics tools to install (minimap2, samtools, bcftools, seqkit, whatshap).
   - Example GitHub Actions workflow (`.github/workflows/week5.yml`) to run `week5/week5.ipynb` in CI.

2. **Notebook structure and pipeline design**
   - High-level outline of the steps the notebook should perform:
     - download chr10 of hg38,
     - download Illumina and PacBio FASTQ files,
     - align with minimap2,
     - call variants with bcftools,
     - subset to CYP2C19 / CYP2C9 / CYP2C8 regions,
     - phase with WhatsHap,
     - compare Illumina vs PacBio variants.
   - Example Jupyter cells using `!bash` commands to implement those steps.

3. **Debugging and adaptation**
   - Help interpreting errors when:
     - `conda`/`mamba` were not available inside Jupyter.
     - WhatsHap rejected the `--longreads` argument.
     - bcftools region subsetting complained about a BED file.
   - The AI suggested fixes such as:
     - running environment setup from the terminal instead of inside the notebook,
     - removing unsupported WhatsHap flags,
     - switching from BED-based region selection to direct `-r chr10:start-end` coordinates.

4. **IGV usage guidance**
   - Instructions for:
     - downloading and launching IGV on macOS,
     - loading `chr10.fa`, BAMs, and phased VCFs,
     - jumping to particular coordinates,
     - choosing “discordant” (Illumina-only or PacBio-only) variants based on `bcftools isec`,
     - capturing and embedding screenshots in the notebook.
   - Example wording for how to describe IGV screenshots (coverage, read support, and artifact vs. real variant reasoning).

5. **Star-allele reasoning (conceptual)**
   - General explanation of how to use phased variants together with PharmVar definitions to reason about likely CYP2C19/CYP2C9/CYP2C8 star-alleles (e.g. checking presence/absence of rs4244285, rs12248560, etc.).
   - The final star-allele conclusions and wording in the notebook are my own, based on the actual variants found in my VCFs.



