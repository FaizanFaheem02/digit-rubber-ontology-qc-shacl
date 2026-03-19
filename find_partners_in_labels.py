import os
import pandas as pd

INPUT_FOLDER = "output_files"
OUTPUT_FOLDER = "partner_summary"

partners_found = set()

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):

    if not file.endswith(".csv"):
        continue

    path = os.path.join(INPUT_FOLDER, file)
    df = pd.read_csv(path)

    if "Label" not in df.columns:
        continue

    extracted = df["Label"].str.extract(r"\[(.*?)\]")
    partners_found.update(extracted[0].dropna().unique())

print("Partners found in labels:\n")

for partner in sorted(partners_found):
    print(partner)

result_df = pd.DataFrame(sorted(partners_found), columns=["Partner"])

output_path = os.path.join(OUTPUT_FOLDER, "partners_found.xlsx")
result_df.to_excel(output_path, index=False)

print(f"\nExcel file created: {output_path}")