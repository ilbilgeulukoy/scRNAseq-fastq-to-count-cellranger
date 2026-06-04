#!/usr/bin/env python3

from pathlib import Path
import sys

def check_cellranger_output(output_dir):
    output_dir = Path(output_dir)

    required_files = [
        "outs/web_summary.html",
        "outs/metrics_summary.csv",
        "outs/filtered_feature_bc_matrix/matrix.mtx.gz",
        "outs/filtered_feature_bc_matrix/barcodes.tsv.gz",
        "outs/filtered_feature_bc_matrix/features.tsv.gz",
        "outs/raw_feature_bc_matrix/matrix.mtx.gz",
        "outs/raw_feature_bc_matrix/barcodes.tsv.gz",
        "outs/raw_feature_bc_matrix/features.tsv.gz",
    ]

    print(f"Checking Cell Ranger output: {output_dir}\n")

    missing = []

    for file_path in required_files:
        full_path = output_dir / file_path
        if full_path.exists():
            print(f"[OK] {file_path}")
        else:
            print(f"[MISSING] {file_path}")
            missing.append(file_path)

    print("\nSummary")
    print("-------")

    if missing:
        print(f"{len(missing)} required files are missing.")
        sys.exit(1)
    else:
        print("All required Cell Ranger output files were found.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_cellranger_output.py <cellranger_output_directory>")
        sys.exit(1)

    check_cellranger_output(sys.argv[1])
