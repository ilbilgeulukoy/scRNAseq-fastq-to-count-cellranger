#!/usr/bin/env python3

"""
Run Cell Ranger count for 10x Genomics single-cell RNA-seq FASTQ files.

This Python script is designed for execution on a Linux server or HPC environment
where Cell Ranger is installed and available in PATH.

Example:
    python scripts/run_cellranger_count.py
"""

from pathlib import Path
import subprocess
import shutil
import sys


PROJECT_NAME = "ovarian_cancer_scrnaseq"
SAMPLE_ID = "sample01"
OUTPUT_ID = f"{SAMPLE_ID}_cellranger_count"

FASTQ_DIR = Path("/path/to/fastq_directory")
TRANSCRIPTOME_REF = Path("/path/to/refdata-gex-GRCh38")

LOCAL_CORES = 16
LOCAL_MEM = 64

RESULTS_DIR = Path("results/cellranger")
LOG_DIR = Path("logs")


def write_log(message: str, log_file: Path) -> None:
    print(message)
    with log_file.open("a") as handle:
        handle.write(message + "\n")


def check_cellranger_available(log_file: Path) -> None:
    if shutil.which("cellranger") is None:
        write_log("ERROR: Cell Ranger is not available in PATH.", log_file)
        write_log("Please load or install Cell Ranger on the server before running this script.", log_file)
        sys.exit(1)


def check_input_paths(log_file: Path) -> None:
    if not FASTQ_DIR.exists():
        write_log(f"ERROR: FASTQ directory does not exist: {FASTQ_DIR}", log_file)
        sys.exit(1)

    if not TRANSCRIPTOME_REF.exists():
        write_log(f"ERROR: Transcriptome reference does not exist: {TRANSCRIPTOME_REF}", log_file)
        sys.exit(1)


def run_command(command: list[str], log_file: Path, working_directory: Path) -> None:
    with log_file.open("a") as log_handle:
        process = subprocess.Popen(
            command,
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        if process.stdout is not None:
            for line in process.stdout:
                print(line, end="")
                log_handle.write(line)

        return_code = process.wait()

    if return_code != 0:
        write_log(f"ERROR: Command failed with exit code {return_code}.", log_file)
        sys.exit(return_code)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_file = LOG_DIR / f"{OUTPUT_ID}.log"

    if log_file.exists():
        log_file.unlink()

    write_log("========================================", log_file)
    write_log("Cell Ranger count run", log_file)
    write_log("========================================", log_file)
    write_log(f"Project: {PROJECT_NAME}", log_file)
    write_log(f"Sample ID: {SAMPLE_ID}", log_file)
    write_log(f"Output ID: {OUTPUT_ID}", log_file)
    write_log(f"FASTQ directory: {FASTQ_DIR}", log_file)
    write_log(f"Transcriptome reference: {TRANSCRIPTOME_REF}", log_file)
    write_log(f"Local cores: {LOCAL_CORES}", log_file)
    write_log(f"Local memory: {LOCAL_MEM} GB", log_file)
    write_log("========================================", log_file)

    check_cellranger_available(log_file)
    check_input_paths(log_file)

    version_command = ["cellranger", "--version"]
    run_command(version_command, log_file, Path.cwd())

    cellranger_command = [
        "cellranger",
        "count",
        f"--id={OUTPUT_ID}",
        f"--transcriptome={TRANSCRIPTOME_REF}",
        f"--fastqs={FASTQ_DIR}",
        f"--sample={SAMPLE_ID}",
        f"--localcores={LOCAL_CORES}",
        f"--localmem={LOCAL_MEM}",
    ]

    write_log("Starting Cell Ranger count...", log_file)
    run_command(cellranger_command, log_file, RESULTS_DIR)

    write_log("========================================", log_file)
    write_log("Cell Ranger count completed.", log_file)
    write_log(f"Output folder: {RESULTS_DIR / OUTPUT_ID}", log_file)
    write_log(f"Main count matrix: {RESULTS_DIR / OUTPUT_ID / 'outs/filtered_feature_bc_matrix'}", log_file)
    write_log("========================================", log_file)


if __name__ == "__main__":
    main()
