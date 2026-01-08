# DigitRubber Ontology – Quality Control Checks

This repository provides SPARQL-based quality control checks for the DigitRubber ontology. It analyzes the ontology and exports CSV reports for common ontology quality issues. The ontology is not modified, all checks are read-only. 

## How to Run

pip install -r requirements.txt<br>
python run.py

All results are written to the output_files/ directory.

## Implemented Quality Checks (SPARQL-based)

- Missing definitions 
- Missing creation date
- Missing last update date on
- Missing both creation **and** update dates
- Missing German (de) labels (Digit Rubber classes already have English labels)
- Labels containing underscores
- Missing curation status 
- Duplicate class labels  
  (e.g. same label used by different partners)

## Project Folder Structure
- ontology/        → Active DigitRubber ontology
- sparql/          → SPARQL quality checks
- output_files/    → CSV reports
- run.py           → Executes all checks