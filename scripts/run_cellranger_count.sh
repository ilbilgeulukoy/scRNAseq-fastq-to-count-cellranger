#!/bin/bash

# Run Cell Ranger count for 10x Genomics single-cell RNA-seq FASTQ files.
#
# This script is designed to be edited and executed on a Linux server or HPC environment.
# Large FASTQ files and reference transcriptomes should not be stored in this GitHub repository.

set -euo pipefail

# -----------------------------
# User-defined parameters
# -----------------------------

PROJECT_NAME="ovarian_cancer_scrnaseq"
SAMPLE_ID="sample01"
OUTPUT_ID="${SAMPLE_ID}_cellranger_count"

FASTQ_DIR="/path/to/fastq_directory"
TRANSCRIPTOME_REF="/path/to/refdata-gex-GRCh38"

LOCAL_CORES=16
LOCAL_MEM=64

RESULTS_DIR="results/cellranger"
LOG_DIR="logs"

# -----------------------------
# Setup
# -----------------------------

mkdir -p "${RESULTS_DIR}"
mkdir -p "${LOG_DIR}"

LOG_FILE="${LOG_DIR}/${OUTPUT_ID}.log"

echo "========================================" | tee "${LOG_FILE}"
echo "Cell Ranger count run" | tee -a "${LOG_FILE}"
echo "========================================" | tee -a "${LOG_FILE}"
echo "Project: ${PROJECT_NAME}" | tee -a "${LOG_FILE}"
echo "Sample ID: ${SAMPLE_ID}" | tee -a "${LOG_FILE}"
echo "Output ID: ${OUTPUT_ID}" | tee -a "${LOG_FILE}"
echo "FASTQ directory: ${FASTQ_DIR}" | tee -a "${LOG_FILE}"
echo "Transcriptome reference: ${TRANSCRIPTOME_REF}" | tee -a "${LOG_FILE}"
echo "Local cores: ${LOCAL_CORES}" | tee -a "${LOG_FILE}"
echo "Local memory: ${LOCAL_MEM} GB" | tee -a "${LOG_FILE}"
echo "========================================" | tee -a "${LOG_FILE}"

# -----------------------------
# Checks
# -----------------------------

if ! command -v cellranger &> /dev/null
then
    echo "ERROR: Cell Ranger is not available in PATH." | tee -a "${LOG_FILE}"
    echo "Please load Cell Ranger on the server before running this script." | tee -a "${LOG_FILE}"
    exit 1
fi

if [ ! -d "${FASTQ_DIR}" ]
then
    echo "ERROR: FASTQ directory does not exist: ${FASTQ_DIR}" | tee -a "${LOG_FILE}"
    exit 1
fi

if [ ! -d "${TRANSCRIPTOME_REF}" ]
then
    echo "ERROR: Transcriptome reference does not exist: ${TRANSCRIPTOME_REF}" | tee -a "${LOG_FILE}"
    exit 1
fi

cellranger --version | tee -a "${LOG_FILE}"

# -----------------------------
# Run Cell Ranger
# -----------------------------

cd "${RESULTS_DIR}"

cellranger count \
  --id="${OUTPUT_ID}" \
  --transcriptome="${TRANSCRIPTOME_REF}" \
  --fastqs="${FASTQ_DIR}" \
  --sample="${SAMPLE_ID}" \
  --localcores="${LOCAL_CORES}" \
  --localmem="${LOCAL_MEM}" 2>&1 | tee -a "../../${LOG_FILE}"

echo "========================================" | tee -a "../../${LOG_FILE}"
echo "Cell Ranger count completed." | tee -a "../../${LOG_FILE}"
echo "Output folder: ${RESULTS_DIR}/${OUTPUT_ID}" | tee -a "../../${LOG_FILE}"
echo "Main count matrix: ${RESULTS_DIR}/${OUTPUT_ID}/outs/filtered_feature_bc_matrix" | tee -a "../../${LOG_FILE}"
echo "========================================" | tee -a "../../${LOG_FILE}"
