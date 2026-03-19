import os
import pandas as pd

INPUT_FOLDER = "output_files"
BASE_OUTPUT_FOLDER = "partner_results"

PARTNERS = ["Arlanxeo", "imr", "ifnano", "dik", "hsh", "jade", "m4i", "uo", "chmo", "enm", "ita", "mi", "chebi", "ncit", "envo", "Wikipedia", "geosparql", "edam", "pato", "efo", "ms", "obi"]

UNKNOWN_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "unknown")

if not os.path.exists(INPUT_FOLDER):
    raise FileNotFoundError(f"Input folder '{INPUT_FOLDER}' does not exist.")

os.makedirs(BASE_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(UNKNOWN_FOLDER, exist_ok=True)

for PARTNER_NAME in PARTNERS:

    OUTPUT_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, PARTNER_NAME)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for file in os.listdir(INPUT_FOLDER):

        if not file.endswith(".csv"):
            continue

        path = os.path.join(INPUT_FOLDER, file)
        df = pd.read_csv(path)

        if "DuplicateBaseLabels" in file:

            filtered = df[df["Message"].str.contains(fr"\[{PARTNER_NAME}\]", na=False)]

            if not filtered.empty:
                filtered = filtered[["Message"]]

        else:

            if "Label" not in df.columns:
                continue

            df["Partner"] = df["Label"].str.extract(r"\[(.*?)\]")

            filtered = df[df["Partner"] == PARTNER_NAME]
            filtered = filtered.drop(columns=["Partner"])

            unknown_rows = df[df["Partner"].isna()]

            if not unknown_rows.empty and PARTNER_NAME == PARTNERS[0]:

                unknown_rows = unknown_rows.drop(columns=["Partner"])

                unknown_file = file.replace(".csv", "_unknown.xlsx")
                unknown_path = os.path.join(UNKNOWN_FOLDER, unknown_file)

                unknown_rows.to_excel(unknown_path, index=False)

                print(f"unknown: Created {unknown_file}")

        if not filtered.empty:

            output_file = file.replace(".csv", f"_{PARTNER_NAME}.xlsx")
            output_path = os.path.join(OUTPUT_FOLDER, output_file)

            filtered.to_excel(output_path, index=False)

            print(f"{PARTNER_NAME}: Created {output_file}")