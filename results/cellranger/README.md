# Cell Ranger outputs

This folder is reserved for Cell Ranger count outputs.

A typical Cell Ranger output folder contains:

sample01_cellranger_count/
└── outs/
    ├── web_summary.html
    ├── metrics_summary.csv
    ├── filtered_feature_bc_matrix/
    ├── raw_feature_bc_matrix/
    ├── molecule_info.h5
    └── possorted_genome_bam.bam

Large output files such as BAM files and molecule information files should not be tracked in GitHub.

The most important output for downstream analysis is:

outs/filtered_feature_bc_matrix/
