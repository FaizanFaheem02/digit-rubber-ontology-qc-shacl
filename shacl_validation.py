from pyshacl import validate
from rdflib import Graph, XSD
from rdflib.namespace import RDF
import rdflib.term
import csv
from rdflib import Namespace
from pathlib import Path


root_dir = Path(__file__).resolve().parent
shapes_dir = root_dir / "shapes"

# Disable rdflib auto conversion of dates and numbers that can cause pyparsing to hang
for dt in (XSD.date, XSD.dateTime, XSD.decimal):
    rdflib.term._toPythonMapping.pop(dt, None)


data_graph = Graph()
data_graph.parse( "ontology/digitrubber-edit.owl", format="xml")

shacl_graph = Graph()
for shape_file in shapes_dir.rglob("*.ttl"):
    shacl_graph.parse(shape_file, format="turtle")


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


SH = Namespace("http://www.w3.org/ns/shacl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

rows_by_shape = {}


for result in results_graph.subjects(RDF.type, object=SH.ValidationResult):

    shape = results_graph.value(result, SH.sourceShape)
    focus_node = results_graph.value(result, SH.focusNode)

    value = results_graph.value(result, SH.value)

    if not shape or not focus_node:
        continue

    if isinstance(shape, rdflib.term.BNode):
        for node_shape in shacl_graph.subjects(SH.property, shape):
            shape = node_shape
            break

    class_id = str(focus_node).split("/")[-1]

    label = None
    for l in data_graph.objects(focus_node, RDFS.label):
        if getattr(l, "language", None) == "en":
           label = l
           break

    label = str(label) if label else ""

    severity = results_graph.value(result, SH.resultSeverity)
    severity = str(severity).split("#")[-1]

    message = results_graph.value(result, SH.resultMessage)
    message = str(message) if message else ""

    rows_by_shape.setdefault(shape, []).append( [class_id, label, severity, message])


for shape, rows in rows_by_shape.items():

    shape_name = str(shape).split("#")[-1]
    output_csv = f"output_files/{shape_name}.csv"

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Class Suffix", "Label", "Severity", "Message"])
        writer.writerows(rows)

    print(f"Table written: {output_csv} ({len(rows)} violations)")