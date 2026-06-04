# scRNA-seq FASTQ to Count Matrix with Cell Ranger

This repository documents a reproducible workflow for processing 10x Genomics single-cell RNA-seq FASTQ files with Cell Ranger to generate gene-by-cell count matrices.

## Project goal

The goal of this project is to start from raw 10x Genomics FASTQ files and produce Cell Ranger count outputs, including:

- `web_summary.html`
- `metrics_summary.csv`
- `filtered_feature_bc_matrix/`
- `raw_feature_bc_matrix/`

These outputs can then be used for downstream single-cell analysis in Python or R.

## Workflow overview

```text
Raw 10x FASTQ files
        |
        v
Cell Ranger count
        |
        v
Quality metrics and gene-by-cell count matrix
        |
        v
Ready for downstream analysis


cat > scripts/run_cellranger_count.sh << 'EOF'
#!/bin/bash

# Example Cell Ranger count command
# Edit the paths below before running on a server.

cellranger count \
  --id=sample01_cellranger_count \
  --transcriptome=/path/to/refdata-gex-GRCh38 \
  --fastqs=/path/to/fastq_directory \
  --sample=sample01 \
  --localcores=16 \
  --localmem=64

## Usage

### 1. Prepare input FASTQ files

Place 10x Genomics FASTQ files on a Linux server or HPC storage system.

Example FASTQ naming pattern:

sample01_S1_L001_R1_001.fastq.gz
sample01_S1_L001_R2_001.fastq.gz
sample01_S1_L001_I1_001.fastq.gz

FASTQ files are not tracked in this repository.

### 2. Edit the configuration file

Edit:

config/sample_config.yaml

Update the following fields:

- sample_id
- fastq_directory
- transcriptome_reference
- localcores
- localmem

### 3. Edit and run the Cell Ranger script

Edit:

scripts/run_cellranger_count.sh

Then run it on a Linux server where Cell Ranger is installed:

bash scripts/run_cellranger_count.sh

### 4. Expected output

Cell Ranger creates an output folder similar to:

sample01_cellranger_count/outs/

Important output files:

- web_summary.html
- metrics_summary.csv
- filtered_feature_bc_matrix/
- raw_feature_bc_matrix/

The main count matrix for downstream analysis is:

sample01_cellranger_count/outs/filtered_feature_bc_matrix/

### 5. Validate Cell Ranger output

After Cell Ranger finishes, validate the output structure:

python scripts/check_cellranger_output.py sample01_cellranger_count

If all required files are present, the script reports:

All required Cell Ranger output files were found.

## Count matrix files

The filtered gene-by-cell count matrix is stored in:

filtered_feature_bc_matrix/

This folder contains:

- barcodes.tsv.gz
- features.tsv.gz
- matrix.mtx.gz

These files can be loaded into downstream analysis tools such as Scanpy or Seurat.
