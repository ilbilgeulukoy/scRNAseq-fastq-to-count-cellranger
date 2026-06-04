#!/usr/bin/env python3

"""
Check whether a Cell Ranger count output directory contains the expected files.

Usage:
    python scripts/check_cellranger_output.py results/cellranger/sample01_cellranger_count
"""

from pathlib import Path
import sys


def check_cellranger_output(output_dir: str) -> int:
    output_path = Path(output_dir)

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

    print(f"Checking Cell Ranger output directory: {output_path}\n")

    if not output_path.exists():
        print(f"[ERROR] Output directory does not exist: {output_path}")
        return 1

    missing_files = []

    for relative_file in required_files:
        full_file = output_path / relative_file

        if full_file.exists():
            print(f"[OK]      {relative_file}")
        else:
            print(f"[MISSING] {relative_file}")
            missing_files.append(relative_file)

    print("\nSummary")
    print("-------")

    if missing_files:
        print(f"{len(missing_files)} required file(s) are missing.")
        return 1

    print("All required Cell Ranger output files were found.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_cellranger_output.py <cellranger_output_directory>")
        sys.exit(1)

    exit_code = check_cellranger_output(sys.argv[1])
    sys.exit(exit_code)
