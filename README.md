# DigitRubber Ontology – Quality Control Checks

This repository provides SHACL-based quality control checks for the DigitRubber ontology. It validates the ontology against a set of SHACL shapes and exports CSV tables in ordeer to report common ontology quality issues. The ontology is not modified, all checks are read-only. 

## How to Run

python -m venv venv<br>
.\venv\Scripts\Activate.ps1<br>
python -m pip install -r requirements.txt<br>
python shacl_validation.py

Currently, the script runs SHACL validation for one shape file. Support for running multiple shapes via configurable file paths will be added soon.

## Implemented Quality Checks (SHACL-based)

- Missing both creation and update dates
- Missing creation date
- Missing German (de) labels
- Missing definitons 
- Missing last updated on dates
- Missing English or German definitions 
- Multiple creation dates
- Multiple curation status
- Multiple German (de) definitions
- Multiple English (en) definitions
- Multiple last updated on
- Labels containing underscores
- Missing curation status

## Project Folder Structure
- ontology/        → Active DigitRubber ontology
- shapes/          → SHACL-based quality checks
- output_files/    → CSV reports
- shacl_validation.py    → Executes SHACL-based quality control checks