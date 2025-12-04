#!/usr/bin/env bash
set -euo pipefail
mkdir -p logs
snakemake -j 1 --rerun-incomplete --printshellcmds | tee logs/snakemake.log
