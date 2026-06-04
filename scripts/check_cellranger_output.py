#!/usr/bin/env python3

"""
Validate a Cell Ranger count output directory and summarize key QC metrics.

Usage:
    python scripts/check_cellranger_output.py results/cellranger/sample01_cellranger_count
"""

from pathlib import Path
import csv
import sys


REQUIRED_FILES = [
    "outs/web_summary.html",
    "outs/metrics_summary.csv",
    "outs/filtered_feature_bc_matrix/matrix.mtx.gz",
    "outs/filtered_feature_bc_matrix/barcodes.tsv.gz",
    "outs/filtered_feature_bc_matrix/features.tsv.gz",
    "outs/raw_feature_bc_matrix/matrix.mtx.gz",
    "outs/raw_feature_bc_matrix/barcodes.tsv.gz",
    "outs/raw_feature_bc_matrix/features.tsv.gz",
]


IMPORTANT_METRICS = [
    "Estimated Number of Cells",
    "Mean Reads per Cell",
    "Median Genes per Cell",
    "Number of Reads",
    "Valid Barcodes",
    "Sequencing Saturation",
    "Q30 Bases in RNA Read",
]


def check_required_files(output_path: Path) -> list:
    print(f"Checking Cell Ranger output directory: {output_path}\n")

    missing_files = []

    if not output_path.exists():
        print(f"[ERROR] Output directory does not exist: {output_path}")
        return REQUIRED_FILES

    for relative_file in REQUIRED_FILES:
        full_file = output_path / relative_file

        if full_file.exists():
            print(f"[OK]      {relative_file}")
        else:
            print(f"[MISSING] {relative_file}")
            missing_files.append(relative_file)

    return missing_files


def read_metrics_summary(metrics_file: Path) -> dict:
    metrics = {}

    if not metrics_file.exists():
        return metrics

    with metrics_file.open("r", newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)

    if len(rows) < 2:
        return metrics

    header = rows[0]
    values = rows[1]

    for key, value in zip(header, values):
        metrics[key.strip()] = value.strip()

    return metrics


def print_key_metrics(metrics: dict) -> None:
    print("\nKey Cell Ranger metrics")
    print("-----------------------")

    if not metrics:
        print("No metrics could be read from metrics_summary.csv.")
        return

    found_any = False

    for metric in IMPORTANT_METRICS:
        if metric in metrics:
            print(f"{metric}: {metrics[metric]}")
            found_any = True

    if not found_any:
        print("metrics_summary.csv was found, but the expected metric names were not detected.")
        print("Available metric names include:")
        for key in list(metrics.keys())[:10]:
            print(f"- {key}")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_cellranger_output.py <cellranger_output_directory>")
        return 1

    output_path = Path(sys.argv[1])
    missing_files = check_required_files(output_path)

    metrics_file = output_path / "outs" / "metrics_summary.csv"
    metrics = read_metrics_summary(metrics_file)
    print_key_metrics(metrics)

    print("\nValidation summary")
    print("------------------")

    if missing_files:
        print(f"{len(missing_files)} required file(s) are missing.")
        return 1

    print("All required Cell Ranger output files were found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
