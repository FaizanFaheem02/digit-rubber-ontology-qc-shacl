import os
import pandas as pd

RESOLUTION_MAP = {
    "ClassesWithMultipleEnglishLabels": "Keep one English label",
    "ClassLabelWithUnderscore": "Remove underscores",

    "ClassMissingCreationDate": "Add creation date",
    "ClassMissingLastUpdateOn": "Add last update date",
    "ClassMissingCurationStatus": "Add curation status",

    "ClassMissingEnglishDefinition": "Add English definition",
    "ClassMissingGermanDefinition": "Add German definition",

    "ClassMissingEnglishLabel": "Add English label",
    "ClassMissingGermanLabel": "Add German label",

    "ClassMoreThanOneEnglishDefinition": "Keep one English definition",
    "ClassMoreThanOneGermanDefinition": "Keep one German definition",

    "DigitRubberClassesWithDuplicateBaseLabels": "Pick one label"
}

INPUT_FOLDER = "output_files"
BASE_OUTPUT_FOLDER = "partner_results"

PARTNERS = ["Arlanxeo", "imr", "ifnano", "dik", "hsh", "jade", "m4i", "uo", "chmo", "enm", "ita", "mi", "chebi", "ncit", "envo", "Wikipedia", "geosparql", "edam", "pato", "efo", "ms", "obi"]

UNKNOWN_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "unknown_complete")

UNKNOWN_DR_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "unknown_digitrubber")

if not os.path.exists(INPUT_FOLDER):
    raise FileNotFoundError(f"Input folder '{INPUT_FOLDER}' does not exist.")

os.makedirs(BASE_OUTPUT_FOLDER, exist_ok=True) 
os.makedirs(UNKNOWN_FOLDER, exist_ok=True)

os.makedirs(UNKNOWN_DR_FOLDER, exist_ok=True)

for PARTNER_NAME in PARTNERS:

    OUTPUT_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, PARTNER_NAME)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for file in os.listdir(INPUT_FOLDER):

        if not file.endswith(".csv"):
            continue

        path = os.path.join(INPUT_FOLDER, file)
        df = pd.read_csv(path)

        file_key = file.replace(".csv", "")

        resolution_text = ""

        for key, value in RESOLUTION_MAP.items():
            if key in file_key:
                resolution_text = value
                break

        if resolution_text:
            df[resolution_text] = ""

        if "DigitRubberClassesWithDuplicateBaseLabels" in file:

            if "Message" not in df.columns:
                continue

            filtered = df[["Message"]]

            if resolution_text:
                filtered[resolution_text] = ""

        else:

            if "Label" not in df.columns:
                continue

            df["Partner"] = df["Label"].str.extract(r"\[(.*?)\]")

            filtered = df[df["Partner"] == PARTNER_NAME]
            if not filtered.empty:
                cols = ["Label", "Parent", "Contributor", "Definition"]

                if resolution_text:
                    cols.append(resolution_text)

                filtered = filtered[cols]

            unknown_rows = df[df["Partner"].isna()]

            if not unknown_rows.empty and PARTNER_NAME == PARTNERS[0]:

                cols = ["Label", "Parent", "Contributor", "Definition"]

                if resolution_text:
                    cols.append(resolution_text)

                unknown_rows = unknown_rows[cols]

                unknown_file = file.replace(".csv", "_unknown.xlsx")
                unknown_path = os.path.join(UNKNOWN_FOLDER, unknown_file)

                unknown_rows.to_excel(unknown_path, index=False)

                print(f"unknown: Created {unknown_file}")

                # 🔹 UNKNOWN DIGITRUBBER (ADD HERE)
            dr_rows = df[df["Class Suffix"].str.startswith("DIGITRUBBER_", na=False) & df["Partner"].isna()]

            if not dr_rows.empty and PARTNER_NAME == PARTNERS[0]:

                cols = ["Label", "Parent", "Contributor", "Definition"]

                if resolution_text:
                    cols.append(resolution_text)

                cols = [c for c in cols if c in dr_rows.columns]

                dr_rows = dr_rows[cols]

                dr_file = file.replace(".csv", "_unknown_digitrubber.xlsx")
                dr_path = os.path.join(UNKNOWN_DR_FOLDER, dr_file)

                dr_rows.to_excel(dr_path, index=False)

                print(f"unknown_digitrubber: Created {dr_file}")

    # ends here

        if not filtered.empty:

            if "DigitRubberClassesWithDuplicateBaseLabels" in file:
                output_file = file.replace(".csv", ".xlsx")
            else:
                 output_file = file.replace(".csv", f"_{PARTNER_NAME}.xlsx")
            output_path = os.path.join(OUTPUT_FOLDER, output_file)

            filtered.to_excel(output_path, index=False)

            print(f"{PARTNER_NAME}: Created {output_file}")