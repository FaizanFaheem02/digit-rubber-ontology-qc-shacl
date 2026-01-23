# DigitRubber Ontology – Quality Control Checks

This repository provides SHACL-based quality control checks for the DigitRubber ontology. It validates the ontology against a set of SHACL shapes and exports CSV tables in ordeer to report common ontology quality issues. The ontology is not modified, all checks are read-only. 

## How to Run

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python shacl_validation.py
```

Currently, the script runs SHACL validation for one shape file. Support for running multiple shapes via configurable file paths will be added soon.

## Implemented Quality Checks (SHACL-based)

### consistency
- Duplicate labels

### formatting issues
- Invalid creation date
- Invalid last updated on date
- Labels with underscore 

### missing metadata
- Missing creation date 
- Missing last updated on date 
- Missing both creation and last updated on dates
- Missing German (de) labels
- Missing definitons 
- Missing English or German definitions 
- Missing curation status

### multiple values
- Multiple creation dates 
- Multiple curation status
- Multiple German (de) definitions
- Multiple English (en) definitions
- Multiple last updated on dates

## Project Folder Structure
- ontology/        → Active DigitRubber ontology
- shapes/          → SHACL-based quality checks
- output_files/    → CSV reports
- shacl_validation.py    → Executes SHACL-based quality control checks