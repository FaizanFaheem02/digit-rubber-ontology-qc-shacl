import os
import pandas as pd

INPUT_FOLDER = "output_files"
OUTPUT_FOLDER = os.path.join("partner_results", "unknown_digitrubber")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):

    if not file.endswith(".csv"):
        continue

    path = os.path.join(INPUT_FOLDER, file)
    df = pd.read_csv(path)

    # Skip files without required columns
    if "Class Suffix" not in df.columns or "Label" not in df.columns:
        continue

    # Filter DigitRubber + no partner tag
    filtered = df[
        df["Class Suffix"].str.startswith("DIGITRUBBER_", na=False) &
        ~df["Label"].str.contains(r"\[.*?\]", na=False)
    ]

    if not filtered.empty:

        output_file = file.replace(".csv", "_unknown_digitrubber.xlsx")
        output_path = os.path.join(OUTPUT_FOLDER, output_file)

        filtered.to_excel(output_path, index=False)

        print(f"Created: {output_file}")