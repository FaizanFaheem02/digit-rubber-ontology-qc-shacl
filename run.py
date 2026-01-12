from rdflib import Graph
from rdflib.namespace import RDF, RDFS, OWL
from pathlib import Path
import csv
import logging

logging.getLogger("rdflib").setLevel(logging.ERROR)

ONTOLOGY_PATH = Path("ontology/digitrubber-edit.owl")
SPARQL_DIR = Path("sparql")
OUTPUT_DIR = Path("output_files")

SPARQL_FILES = [
    "classes_missing_all_dates.sparql",
    "classes_missing_creation_date.sparql",
    "classes_missing_de_labels.sparql",
    "classes_missing_definitions.sparql",
    "classes_missing_last_updated_on.sparql",
    "classes_with_underscore.sparql",
    "classes_without_curation_status.sparql",
    "duplicate_class_labels.sparql",  
]

g = Graph()
g.parse(ONTOLOGY_PATH, format="xml")

OUTPUT_DIR.mkdir(exist_ok=True)

for sparql_file in SPARQL_FILES:
    query_path = SPARQL_DIR / sparql_file
    output_path = OUTPUT_DIR / sparql_file.replace(".sparql", ".csv")

    print(f"Running {sparql_file}")

    query_text = query_path.read_text(encoding="utf-8")
    result = g.query(query_text)

    is_construct = hasattr(result, "graph") and result.graph is not None

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # For CONSTRUCT 
        if is_construct:
            writer.writerow(["class", "label"])

            seen = set()
            result_graph = result.graph

            for cls in result_graph.subjects(RDF.type, OWL.Class):
                if cls in seen:
                    continue
                seen.add(cls)

                label = result_graph.value(cls, RDFS.label)

                writer.writerow([
                    str(cls),
                    str(label) if label else ""
                ])

        # For SELECT
        else:
            writer.writerow([str(v) for v in result.vars])

            for row in result:
                writer.writerow([
                    str(v) if v is not None else ""
                    for v in row
                ])

    print(f" → {output_path}")

print("QC checks finished.")
