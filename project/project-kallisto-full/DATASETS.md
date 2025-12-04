# Datasets from Bray et al. 2016 (kallisto paper)

## Overview: Yes, their data was BIG

From the kallisto paper (Nature Biotechnology 2016, DOI: 10.1038/nbt.3519):

### Main Benchmark Datasets

#### 1. **Simulated Data** (Primary Performance Testing)
- **Size**: 20 simulations × 30 million paired-end reads each
- **File Size**: ~3-4 GB per sample (compressed FASTQ)
- **Total**: ~60-80 GB for all simulations
- **Source**: Generated using RSEM from GEUVADIS sample NA12716_7
- **Purpose**: Evaluate accuracy vs. ground truth
- **Key Result**: Kallisto processed 30M reads in <10 minutes on a laptop

#### 2. **SEQC Consortium Data** (Real RNA-seq)
- **Size**: Various samples with qPCR validation
- **Purpose**: Independent validation of quantification accuracy
- **Key Feature**: Has "ground truth" TPM values from qPCR

#### 3. **Deep Sequencing Dataset**
- **Size**: 275 million reads
- **File Size**: ~30-40 GB (compressed)
- **Purpose**: Test bootstrap estimation accuracy at high depth
- **Key Result**: Demonstrated that bootstraps provide reliable uncertainty estimates

## Recommended Datasets for Reproduction

### Option 1: GEUVADIS (Easiest to Reproduce Paper Results)
The paper used GEUVADIS sample **NA12716_7** as the basis for simulations.

**GEUVADIS Project**: 465 lymphoblastoid cell line RNA-seq samples from 1000 Genomes

- **Data Type**: Illumina paired-end RNA-seq
- **Read Length**: 75bp paired-end
- **Depth**: ~60-80 million reads per sample
- **Size per Sample**: ~4-6 GB compressed
- **Access**: Available from ENA (European Nucleotide Archive)

**Example SRA accessions** (GEUVADIS samples):
```
ERR188021  # NA12716 (the sample used in the paper)
ERR188022  # NA12717
ERR188023  # NA12718
```

**How to download**:
```bash
# Using SRA toolkit
fastq-dump --split-files --gzip ERR188021

# Or add to config.yaml:
samples:
  NA12716:
    r1: "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR188/ERR188021/ERR188021_1.fastq.gz"
    r2: "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR188/ERR188021/ERR188021_2.fastq.gz"
```

### Option 2: SEQC/MAQC-III (Gold Standard with qPCR Truth)
FDA's Sequencing Quality Control project with quantitative validation.

- **Samples**: A (Universal Human Reference RNA), B (Human Brain Reference RNA)
- **Validation**: qPCR measurements for ~1000 genes
- **SRA Study**: SRP023774
- **Size**: ~3-5 GB per sample

**Example SRA accessions**:
```
SRR950078  # SEQC Sample A, replicate 1
SRR950079  # SEQC Sample A, replicate 2
SRR950080  # SEQC Sample B, replicate 1
```

### Option 3: Small Test Dataset (Quick Validation)
For testing your pipeline before running full-scale:

**SRA**: SRR1039508 (Airway smooth muscle cells, human)
- **Size**: ~1 GB compressed
- **Reads**: ~20 million paired-end
- **Runtime**: ~5-10 minutes on a laptop

```bash
samples:
  airway_sample:
    r1: "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/008/SRR1039508/SRR1039508_1.fastq.gz"
    r2: "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR103/008/SRR1039508/SRR1039508_2.fastq.gz"
```

## Human Transcriptome Reference

**GENCODE Release 46** (latest, ~240 MB compressed):
```
https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_46/gencode.v46.transcripts.fa.gz
```

**Or use the version closer to the paper (2016):**
```
GENCODE v25 (2016): https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_25/gencode.v25.transcripts.fa.gz
```

## Expected Runtime & Storage

### For a typical GEUVADIS sample (~60M reads):

| Tool | Runtime | Peak RAM | Index Size | Output Size |
|------|---------|----------|------------|-------------|
| **Kallisto** | 10-15 min | 4 GB | ~3 GB | ~10 MB |
| **Salmon** | 15-20 min | 6 GB | ~4 GB | ~15 MB |
| **Full Pipeline** | 30-40 min | 8 GB | ~7 GB | ~50 MB |

### Disk Space Requirements:
- **Input FASTQ files**: 4-6 GB per sample
- **Transcriptome FASTA**: 240 MB
- **Indices (kallisto + salmon)**: ~7 GB
- **Results**: ~50 MB per sample
- **Total**: ~12-15 GB per sample

## Quick Start with Real Data

1. **Edit `config.yaml`**:
```yaml
use_test_data: false
transcript_fasta_url: "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_25/gencode.v25.transcripts.fa.gz"

samples:
  NA12716:
    r1: "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR188/ERR188021/ERR188021_1.fastq.gz"
    r2: "ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR188/ERR188021/ERR188021_2.fastq.gz"
```

2. **Run**:
```bash
bash run.sh
```

3. **Wait**: ~30-60 minutes depending on your machine

## Notes

- The paper's **30 million read** benchmark is a **good target** for validation
- Most modern RNA-seq has **20-100 million reads** per sample
- The test data you just ran successfully had only **500K reads** (1000× smaller)
- Real data will produce **meaningful correlation metrics** (not NaN like the tiny test)

## Further Reading

- **Paper**: Bray et al. 2016, Nature Biotechnology 34:525–527
- **GEUVADIS**: https://www.ebi.ac.uk/ena/browser/view/PRJEB3366
- **SEQC/MAQC**: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA175363
- **kallisto tutorial**: https://pachterlab.github.io/kallisto/
