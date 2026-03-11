import os
import pandas as pd

INPUT_FOLDER = "output_files"
OUTPUT_FOLDER = "partner_results"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):

    if file.endswith(".csv"):

        file_path = os.path.join(INPUT_FOLDER, file)
        df = pd.read_csv(file_path)

        print("Processing:", file)
        print(df.columns)