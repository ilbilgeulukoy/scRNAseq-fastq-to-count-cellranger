#!/bin/bash

# Run Cell Ranger count for 10x Genomics single-cell RNA-seq data.
#
# This script is intended to be edited and executed on a Linux server or HPC environment.
# Large FASTQ files and reference files should not be stored in this GitHub repository.

set -euo pipefail

# -----------------------------
# User-defined parameters
# -----------------------------

SAMPLE_ID="sample01"
OUTPUT_ID="sample01_cellranger_count"

FASTQ_DIR="/path/to/fastq_directory"
TRANSCRIPTOME_REF="/path/to/refdata-gex-GRCh38"

LOCAL_CORES=16
LOCAL_MEM=64

# -----------------------------
# Run Cell Ranger
# -----------------------------

echo "Starting Cell Ranger count for sample: ${SAMPLE_ID}"
echo "FASTQ directory: ${FASTQ_DIR}"
echo "Transcriptome reference: ${TRANSCRIPTOME_REF}"
echo "Output ID: ${OUTPUT_ID}"

cellranger count \
  --id="${OUTPUT_ID}" \
  --transcriptome="${TRANSCRIPTOME_REF}" \
  --fastqs="${FASTQ_DIR}" \
  --sample="${SAMPLE_ID}" \
  --localcores="${LOCAL_CORES}" \
  --localmem="${LOCAL_MEM}"

echo "Cell Ranger count completed for sample: ${SAMPLE_ID}"
