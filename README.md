# Empirical Evaluation of Automated Program Repair for Hot Fix Development

This repository contains the artifacts and analysis scripts used in the empirical study
“Fast Over Flawless: Rethinking Automated Program Repair for Hot Fixing Time-Critical Bugs”.

The repository is provided for **double-blind review**.
All identifying information has been removed.

---

## Overview

This artifact supports reproducibility and transparency of an empirical evaluation of automated program repair (APR) tools applied to real-world hot fix bugs.
It includes processed experimental results, analysis scripts, and manual patch assessment data used to evaluate effectiveness, efficiency, and patch quality under hot fix constraints.

The study evaluates multiple APR approaches, including search-based, template-based, learning-based, and agentic techniques, using the HotBugs.jar benchmark.

---

## Repository Structure

### Data and Results

- `aggregated_results/`  
  Aggregated experimental outputs parsed from APR tool executions saved as CSVs.
  These results serve as input for all quantitative analyses reported in the paper.

- `manual_patch_analysis_cleaned/`  
  Cleaned results of the manual patch inspection process.
  This directory includes manual labels identifying symptom hiding patches (potential hot fixes).

- `HotBugs.Jar_Bug_Classes.pdf`  
  Manual classification of HotBugs.jar bugs by structural fix complexity (single-line, single-hunk, single-function, multi-function, and multi-file).

---

### Scripts

- `main.py`  
  Entry point for parsing aggregated results and computing summary statistics.

- `graphs.py`  
  Script used to generate all plots included in the paper.

- `acr_runtime.py`  
  Analysis of AutoCodeRover runtime behavior.

- `ACR_count_patches.py`  
  Script to compute total and unique patch counts per bug for AutoCodeRover.

- `cerberus_unique_patches.py`  
  Script to compute unique patch counts for APR tools executed within the Cerberus framework.

- `manual_patch_analysis.py`  
  Script supporting manual inspection and categorization of generated patches.

---

### Figures

- `plots/`  
  All figures reported in the paper.
  These plots are generated directly from the analysis scripts in this repository.

---

## License

This repository is provided for research and evaluation purposes.
Please refer to the licenses of the underlying benchmarks and repair tools for their respective reuse conditions.

---

## Contact

This repository is anonymized for review.
Questions should be directed through the paper submission system.
