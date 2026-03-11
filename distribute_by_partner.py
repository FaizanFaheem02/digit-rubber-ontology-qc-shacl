import os
import pandas as pd

INPUT_FOLDER = "output_files"
BASE_OUTPUT_FOLDER = "partner_results"

PARTNERS = ["Arlanxeo", "imr", "ifnano", "dik", "hsh", "jade", "m4i", "uo", "chmo", "enm", "ita", "mi", "chebi", "ncit", "envo", "Wikipedia", "geosparql"]

UNKNOWN_FOLDER = os.path.join(BASE_OUTPUT_FOLDER, "unknown")

if not os.path.exists(INPUT_FOLDER):
    raise FileNotFoundError(f"Input folder '{INPUT_FOLDER}' does not exist.")

os.makedirs(BASE_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(UNKNOWN_FOLDER, exist_ok=True)

for PARTNER_NAME in PARTNERS:

    OUTPUT_FOLDER = f"partner_results/{PARTNER_NAME}"
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

            if not unknown_rows.empty:

                unknown_rows = unknown_rows.drop(columns=["Partner"])

                unknown_file = file.replace(".csv", "_unknown.csv")
                unknown_path = os.path.join(UNKNOWN_FOLDER, unknown_file)

                unknown_rows.to_csv(unknown_path, index=False)

                print(f"unknown: Created {unknown_file}")

        if not filtered.empty:

            output_file = file.replace(".csv", f"_{PARTNER_NAME}.csv")
            output_path = os.path.join(OUTPUT_FOLDER, output_file)

            filtered.to_csv(output_path, index=False)

            print(f"{PARTNER_NAME}: Created {output_file}")