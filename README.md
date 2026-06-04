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
