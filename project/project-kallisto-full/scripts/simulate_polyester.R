#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(optparse)
  library(polyester)
  library(Biostrings)
})

option_list <- list(
  make_option("--transcripts", type="character"),
  make_option("--outdir", type="character", default="data/sim"),
  make_option("--n_transcripts", type="integer", default=2000),
  make_option("--n_reads", type="integer", default=500000),
  make_option("--paired", action="store_true", default=TRUE),
  make_option("--read_len", type="integer", default=100),
  make_option("--frag_mean", type="double", default=200),
  make_option("--frag_sd", type="double", default=30),
  make_option("--seed", type="integer", default=42)
)
opt <- parse_args(OptionParser(option_list=option_list))
set.seed(opt$seed)
dir.create(opt$outdir, showWarnings=FALSE, recursive=TRUE)

fa <- readDNAStringSet(opt$transcripts)
keep <- seq_len(min(opt$n_transcripts, length(fa)))
fa <- fa[keep]
writeXStringSet(fa, file.path(opt$outdir, "sim_subset.fa"))

n <- length(fa)

# Generate realistic TPM distribution (log-normal, matches real RNA-seq)
# Most genes have low expression, few genes have very high expression
set.seed(opt$seed)
log_tpms <- rnorm(n, mean=0, sd=3)  # Log-normal parameters
tpms <- exp(log_tpms)               # Convert to linear scale
tpms <- tpms / sum(tpms) * 1e6      # Normalize to sum to 1 million (= TPM)

# Add some very high expressers (top 1%)
n_high <- max(1, floor(n * 0.01))
high_idx <- sample(n, n_high)
tpms[high_idx] <- tpms[high_idx] * runif(n_high, 10, 100)
tpms <- tpms / sum(tpms) * 1e6  # Re-normalize

cat("TPM distribution summary:\n")
cat("  Min:", min(tpms), "\n")
cat("  Median:", median(tpms), "\n")
cat("  Mean:", mean(tpms), "\n")
cat("  Max:", max(tpms), "\n")
cat("  Top 10%:", quantile(tpms, 0.9), "\n")

truth <- data.frame(transcript_id=names(fa), tpm_truth=tpms)
write.table(truth, file.path(opt$outdir, "truth_tpm.tsv"), sep="\t", row.names=FALSE, quote=FALSE)

readspertx <- round(tpms / sum(tpms) * opt$n_reads)

# Filter out transcripts with zero reads (polyester can't handle them)
keep_idx <- which(readspertx > 0)
if (length(keep_idx) == 0) {
  stop("No transcripts have assigned reads. Increase n_reads or n_transcripts.")
}

cat("Total transcripts:", n, "\n")
cat("Transcripts with >0 reads:", length(keep_idx), "\n")
cat("Total reads to simulate:", sum(readspertx[keep_idx]), "\n")

# Filter transcripts, TPMs, and reads
fa_filtered <- fa[keep_idx]
tpms_filtered <- tpms[keep_idx]
readspertx_filtered <- readspertx[keep_idx]
n_filtered <- length(keep_idx)

# Update truth table with filtered transcripts
truth_filtered <- data.frame(transcript_id=names(fa_filtered), tpm_truth=tpms_filtered)
write.table(truth_filtered, file.path(opt$outdir, "truth_tpm.tsv"), 
            sep="\t", row.names=FALSE, quote=FALSE)

# Write filtered FASTA
writeXStringSet(fa_filtered, file.path(opt$outdir, "sim_subset.fa"), compress=FALSE)

# Create fold_changes matrix with correct dimensions
fold_changes <- matrix(1, nrow=n_filtered, ncol=1)

# Run simulation
simulate_experiment(fasta=file.path(opt$outdir, "sim_subset.fa"),
                    reads_per_transcript=readspertx_filtered,
                    num_reps=1,
                    fold_changes=fold_changes,
                    paired=opt$paired,
                    readlen=opt$read_len,
                    fraglen=opt$frag_mean,
                    fragsd=opt$frag_sd,
                    outdir=file.path(opt$outdir, "poly_out"))

# Rename output files
file.rename(file.path(opt$outdir, "poly_out", "sample_01_1.fasta"),
            file.path(opt$outdir, "reads_1.fq"))
file.rename(file.path(opt$outdir, "poly_out", "sample_01_2.fasta"),
            file.path(opt$outdir, "reads_2.fq"))

# Compress
system(paste("gzip -f", file.path(opt$outdir, "reads_1.fq")))
system(paste("gzip -f", file.path(opt$outdir, "reads_2.fq")))
