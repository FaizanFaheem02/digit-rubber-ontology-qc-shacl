from pyshacl import validate
from rdflib import Graph, XSD, Namespace
from rdflib.namespace import RDF
import rdflib.term
import csv
from pathlib import Path
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
OBO = Namespace("http://purl.obolibrary.org/obo/")
OBOINOWL = Namespace("http://www.geneontology.org/formats/oboInOwl#")


root_dir = Path(__file__).resolve().parent
shapes_dir = root_dir / "shapes"

output_dir = root_dir / "output_files"
output_dir.mkdir(exist_ok=True)

# Disable rdflib auto conversion of dates and numbers that can cause pyparsing to hang
for dt in (XSD.date, XSD.dateTime, XSD.decimal):
    rdflib.term._toPythonMapping.pop(dt, None)


data_graph = Graph()
data_graph.parse( "ontology/digitrubber-edit.owl", format="xml")

for o in data_graph.objects(None, Namespace("http://www.w3.org/2002/07/owl#").imports):
    try:
        data_graph.parse(str(o))
    except Exception as e:
        print(f"Could not load import {o}: {e}")

shacl_graph = Graph()
for shape_file in shapes_dir.rglob("*.ttl"):
    shacl_graph.parse(shape_file, format="turtle")


conforms, results_graph, results_text = validate(
    data_graph=data_graph,
    shacl_graph=shacl_graph,
    ont_graph=None,
    inference="rdfs",
    do_owl_imports=True,
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

full_graph = data_graph + results_graph

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

    labels = []

    shape_name_tmp = str(shape)

    if "ClassesWithMultipleEnglishLabels" in shape_name_tmp:
        for l in full_graph.objects(focus_node, RDFS.label):
            if getattr(l, "language", None) == "en":
                labels.append(str(l))

    elif "ClassesWithMultipleGermanLabels" in shape_name_tmp:
        for l in full_graph.objects(focus_node, RDFS.label):
            if getattr(l, "language", None) == "de":
                labels.append(str(l))

    else:
        for l in full_graph.objects(focus_node, RDFS.label):
            if getattr(l, "language", None) == "en":
                labels.append(str(l))
                break

        if not labels:
            for l in full_graph.objects(focus_node, RDFS.label):
                labels.append(str(l))
                break

    label = " | ".join(labels) if labels else ""

    definitions = []

    shape_name_tmp = str(shape)

    if "ClassMoreThanOneEnglishDefinition" in shape_name_tmp:
        for d in full_graph.objects(focus_node, OBO.IAO_0000115):
            if getattr(d, "language", None) == "en":
                definitions.append(str(d))
        for d in full_graph.objects(focus_node, SKOS.definition):
            if getattr(d, "language", None) == "en":
                definitions.append(str(d))

    elif "ClassMoreThanOneGermanDefinition" in shape_name_tmp:
        for d in full_graph.objects(focus_node, OBO.IAO_0000115):
            if getattr(d, "language", None) == "de":
                definitions.append(str(d))
        for d in full_graph.objects(focus_node, SKOS.definition):
            if getattr(d, "language", None) == "de":
                definitions.append(str(d))

    else:
        definition = None

        for d in full_graph.objects(focus_node, OBO.IAO_0000115):
            if getattr(d, "language", None) == "en":
                definition = d
                break

        if not definition:
            for d in full_graph.objects(focus_node, OBO.IAO_0000115):
                definition = d
                break

        if not definition:
            for d in full_graph.objects(focus_node, SKOS.definition):
                if getattr(d, "language", None) == "en":
                    definition = d
                    break

        if not definition:
            for d in full_graph.objects(focus_node, SKOS.definition):
                definition = d
                break

        if not definition:
            for d in full_graph.objects(focus_node, RDFS.comment):
                if getattr(d, "language", None) == "en":
                    definition = d
                    break

        if not definition:
            for d in full_graph.objects(focus_node, RDFS.comment):
                definition = d
                break

        definitions = [str(definition)] if definition else []

    definition = " | ".join(definitions) if definitions else "Definition not available"

    parent_label = None

    for parent in full_graph.objects(focus_node, RDFS.subClassOf):

        if isinstance(parent, rdflib.term.BNode):
            continue

        for l in full_graph.objects(parent, RDFS.label):
            if getattr(l, "language", None) == "en":
                parent_label = l
                break

        if not parent_label:
            for l in full_graph.objects(parent, RDFS.label):
                parent_label = l
                break

        if not parent_label:
            parent_label = str(parent).split("/")[-1]

        break  

    parent_label = str(parent_label) if parent_label else ""

    contributor = None

    for p, o in full_graph.predicate_objects(focus_node):
        if "creator" in str(p).lower() or "contributor" in str(p).lower() or "IAO_0000117" in str(p):
            contributor = o
            break

    contributor = str(contributor) if contributor else ""



    severity = results_graph.value(result, SH.resultSeverity)
    severity = str(severity).split("#")[-1]

    message = results_graph.value(result, SH.resultMessage)
    message = str(message) if message else ""

    if str(shape).endswith("DigitRubberClassesWithDuplicateBaseLabels"):
        rows_by_shape.setdefault(shape, []).append([class_id, contributor, label, parent_label, definition, message])
    else:
        rows_by_shape.setdefault(shape, []).append([class_id, contributor, label, parent_label, definition])

   # rows_by_shape.setdefault(shape, []).append( [class_id, label, severity, message])
   # rows_by_shape.setdefault(shape, []).append( [class_id, contributor, label, parent_label, definition])


for shape, rows in rows_by_shape.items():

    shape_name = str(shape).split("#")[-1]
    output_csv = output_dir / f"{shape_name}.csv"

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if shape_name == "DigitRubberClassesWithDuplicateBaseLabels":
            writer.writerow(["Class Suffix", "Contributor", "Label", "Parent", "Definition", "Message"])
        else:
            writer.writerow(["Class Suffix", "Contributor", "Label", "Parent", "Definition"])
       # writer.writerow(["Class Suffix", "Label", "Severity", "Message"])
       # writer.writerow(["Class Suffix", "Contributor", "Label", "Parent", "Definition"])
        writer.writerows(rows)

    print(f"Table written: {output_csv} ({len(rows)} violations)")