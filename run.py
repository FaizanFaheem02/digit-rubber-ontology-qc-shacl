from rdflib import Graph
from pathlib import Path
import csv
import re
import logging

logging.getLogger("rdflib").setLevel(logging.ERROR)

ONTOLOGY_PATH = Path("ontology/digitrubber-edit.owl")
SPARQL_DIR = Path("sparql")
OUTPUT_DIR = Path("output_files")

SPARQL_FILES = [
    "duplicate_class_labels.sparql",
    "classes_missing_definitions.sparql",
    "classes_without_curation_status.sparql",
    "classes_missing_creation_date.sparql",
    "classes_missing_last_updated_on.sparql",
    "classes_missing_all_dates.sparql",
    "classes_missing_de_labels.sparql",
    "classes_with_underscore.sparql",
]

raw_data = ONTOLOGY_PATH.read_text(encoding="utf-8")

# -------------------------
# Normalize xsd:date problem start
# -------------------------
def normalize_xsd_date(match):
    value = match.group(1)

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return f'"{value}"^^xsd:date'

    m = re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", value)
    if m:
        return f'"{m.group(3)}-{m.group(2).zfill(2)}-{m.group(1).zfill(2)}"^^xsd:date'

    return f'"{value}"^^xsd:string'


normalized_data = re.sub(
    r'"([^"]+)"\^\^xsd:date',
    normalize_xsd_date,
    raw_data
)

# -------------------------
# Normalize xsd:date problem end
# -------------------------

g = Graph()
g.parse(data=normalized_data, format="xml")


OUTPUT_DIR.mkdir(exist_ok=True)

for sparql_file in SPARQL_FILES:
    query_path = SPARQL_DIR / sparql_file
    output_path = OUTPUT_DIR / sparql_file.replace(".sparql", ".csv")

    print(f"Running {sparql_file}")

    query_text = query_path.read_text(encoding="utf-8")
    results = g.query(query_text)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([str(v) for v in results.vars])
        for row in results:
            writer.writerow([str(v) if v else "" for v in row])

    print(f" → {output_path}")

print("QC checks finished.")
