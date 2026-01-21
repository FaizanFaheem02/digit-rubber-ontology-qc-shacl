from pyshacl import validate
from rdflib import Graph, XSD
import rdflib.term
import csv
from rdflib import Namespace

for dt in (XSD.date, XSD.dateTime, XSD.decimal):
    rdflib.term._toPythonMapping.pop(dt, None)

data_graph = Graph()
data_graph.parse( "ontology/digitrubber-edit.owl", format="xml")

shacl_graph = Graph()
shacl_graph.parse( "shapes/missing_metadata/classes_missing_last_updated_on_SHACL.ttl", format="turtle")

conforms, results_graph, results_text = validate(
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    ont_graph=None,
    inference="rdfs",
    abort_on_first=False,
    allow_infos=False,
    allow_warnings=False,
    meta_shacl=False,
    advanced=True,
    js=False,
    debug=False
)


print("\n== SHACL VALIDATION RESULT ===\n")
print("Conforms:", conforms)

print("\n------ SHACL REPORT ----------------\n")
print(results_text)


SH = Namespace("http://www.w3.org/ns/shacl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

rows = []

for result in results_graph.subjects(predicate=None, object=SH.ValidationResult):
  
    focus_node = results_graph.value(result, SH.focusNode)
    class_id = str(focus_node).split("/")[-1]

    
    label = data_graph.value(focus_node, RDFS.label)
    label = str(label) if label else ""

    severity = results_graph.value(result, SH.resultSeverity)
    severity = str(severity).split("#")[-1]

    message = results_graph.value(result, SH.resultMessage)
    message = str(message)

    rows.append([class_id, label, severity, message])

output_csv = "output_files/curation_status_table.csv"

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Class", "Label", "Severity", "Message"])
    writer.writerows(rows)

print(f"\nTable written to: {output_csv}")